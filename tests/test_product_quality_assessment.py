from dataclasses import fields, replace
from decimal import Decimal
from fractions import Fraction

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import SpecificationAssessmentService
from requirements_quality_assessment.dynamic_evidence import (
    Applicability,
    ConformanceEvaluationContext,
    ConformanceOutcome,
    DynamicEvidenceReason,
    FullModelStatus,
    ObservationSlotRef,
    assess_conformance,
    bind_quantitative_criterion,
    resolve_dynamic_observation,
)
from requirements_quality_assessment.dynamic_evidence import CriterionBindingContext
from requirements_quality_assessment.metrics import (
    ArtifactRef,
    AssessmentRef,
    MetricConstructionContext,
    MetricId,
    MetricProfileBuilder,
    NumericRepresentation,
)
from requirements_quality_assessment.performance_efficiency import (
    PerformanceEfficiencyFeatureConstructionContext,
    PerformanceEfficiencyFeatureId,
    PerformanceEfficiencyFeatureProfileBuilder,
    ProcessStage,
    ProcessStateRef,
    QbTargetGateFeatureValue,
)
from requirements_quality_assessment.product_quality import (
    MANDATORY_NON_CLAIMS,
    MODEL_REF,
    PARAMETER_SET,
    PARAMETER_SET_REF,
    BoundedProcedureState,
    CalibrationStatus,
    EvidenceChannelId,
    FullCharacteristicCoverage,
    PerformanceEfficiencyQualityAssessor,
    ProductQualityAssessment,
    ProductQualityAssessmentContext,
    ProductQualityAssessmentEventRef,
    ProductQualityResultKind,
    assess_product_quality,
)

from test_performance_efficiency_features import (
    _build,
    _bundle,
    _collection,
    _extraction,
    _feature,
)


def _context(profile, *, event_id="PE-QUALITY-EVENT-001", version="1"):
    event = ProductQualityAssessmentEventRef(
        event_id,
        version,
        profile.product_ref,
        profile.artifact_ref,
    )
    return ProductQualityAssessmentContext(
        event,
        profile.artifact_ref,
        profile.source_assessment_ref,
        profile.profile_id,
        profile.product_ref,
        profile.process_state_ref,
    )


def _assess(profile):
    return assess_product_quality(
        profile,
        MODEL_REF,
        PARAMETER_SET_REF,
        _context(profile),
    )


@pytest.mark.parametrize(
    ("observed", "outcome", "expected"),
    [
        (Decimal("1.8"), ConformanceOutcome.CONFORMS, Fraction(1, 1)),
        (Decimal("2"), ConformanceOutcome.CONFORMS, Fraction(1, 1)),
        (
            Decimal("2.3"),
            ConformanceOutcome.DOES_NOT_CONFORM,
            Fraction(0, 1),
        ),
    ],
)
def test_available_conformance_maps_to_exact_bounded_indicator(
    observed, outcome, expected
) -> None:
    assessment = _assess(_build(_bundle(observed_value=observed)))

    assert assessment.status is FullModelStatus.AVAILABLE
    assert assessment.applicability is Applicability.APPLICABLE
    assert assessment.source_conformance_outcome is outcome
    assert assessment.value == expected
    assert assessment.observed_value == expected
    assert type(assessment.value) is Fraction
    assert type(assessment.observed_value) is Fraction
    assert assessment.numeric_representation is NumericRepresentation.EXACT_FRACTION
    assert assessment.result_kind is ProductQualityResultKind.OBSERVED_REFERENCE_INDICATOR


def test_missing_observation_produces_unavailable_without_zero() -> None:
    assessment = _assess(_build(_bundle(observed_value=None)))

    assert assessment.status is FullModelStatus.UNAVAILABLE
    assert assessment.applicability is Applicability.APPLICABLE
    assert assessment.source_conformance_outcome is None
    assert assessment.value is None
    assert assessment.observed_value is None
    assert assessment.numeric_representation is NumericRepresentation.NONE
    assert assessment.evidence_coverage.bounded_procedure_state is BoundedProcedureState.UNAVAILABLE


@pytest.mark.parametrize(
    ("status", "applicability", "reason"),
    [
        (FullModelStatus.UNKNOWN, Applicability.UNKNOWN, None),
        (
            FullModelStatus.UNRESOLVED,
            Applicability.UNKNOWN,
            DynamicEvidenceReason.OBSERVATION_IDENTITY_UNRESOLVED,
        ),
        (
            FullModelStatus.UNSUPPORTED,
            Applicability.APPLICABLE,
            DynamicEvidenceReason.OBSERVATION_NUMERIC_UNSUPPORTED,
        ),
    ],
)
def test_dynamic_nonvalue_statuses_propagate_without_imputation(
    status, applicability, reason
) -> None:
    bundle = list(_bundle(observed_value=None))
    resolution = replace(
        bundle[3],
        status=status,
        applicability=applicability,
        reasons=() if reason is None else (reason,),
    )
    conformance = assess_conformance(
        bundle[2],
        resolution,
        ConformanceEvaluationContext(bundle[5].dynamic_assessment_ref),
    )
    bundle[3] = resolution
    bundle[4] = conformance

    assessment = _assess(_build(tuple(bundle)))

    assert assessment.status is status
    assert assessment.applicability is applicability
    assert assessment.value is None
    assert assessment.observed_value is None
    assert assessment.source_conformance_outcome is None


def test_no_applicable_criterion_propagates_not_applicable() -> None:
    extraction = _extraction("R001", 1, None)
    source = SpecificationAssessmentService().assess(
        (RequirementQualityAssessor().assess_record(extraction),)
    )
    artifact = ArtifactRef("SPEC-PE-NA", "1")
    source_assessment = AssessmentRef("ASSESS-PE-NA", "1", artifact)
    metric_profile = MetricProfileBuilder().build(
        source, MetricConstructionContext(artifact, source_assessment)
    )
    binding = bind_quantitative_criterion(
        extraction,
        None,
        CriterionBindingContext(artifact, source_assessment, source.snapshot_id),
    )
    collection = _collection()
    resolution = resolve_dynamic_observation(ObservationSlotRef(collection, 0), None)
    dynamic_ref = replace(
        _bundle()[5].dynamic_assessment_ref,
        assessment_id="ASSESS-PE-DYN-NA",
        artifact_ref=artifact,
        collection_ref=collection,
        product_ref=collection.product_ref,
    )
    conformance = assess_conformance(
        binding, resolution, ConformanceEvaluationContext(dynamic_ref)
    )
    feature_context = PerformanceEfficiencyFeatureConstructionContext(
        artifact,
        source_assessment,
        metric_profile.profile_id,
        dynamic_ref,
        collection.product_ref,
        ProcessStateRef("PROCESS-PE-NA", "1", ProcessStage.REFERENCE_VERIFICATION),
    )
    profile = PerformanceEfficiencyFeatureProfileBuilder().build(
        metric_profile,
        source,
        binding,
        resolution,
        conformance,
        feature_context,
    )

    assessment = _assess(profile)

    assert assessment.status is FullModelStatus.NOT_APPLICABLE
    assert assessment.applicability is Applicability.NOT_APPLICABLE
    assert assessment.value is None
    assert assessment.observed_value is None
    assert assessment.evidence_coverage.bounded_procedure_state is BoundedProcedureState.NOT_APPLICABLE


def test_qb_target_not_applicable_permits_observed_indicator() -> None:
    profile = _build(_bundle(second_unit="хв", observed_value=Decimal("1.8")))
    qb = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)

    assessment = _assess(profile)

    assert qb.status is FullModelStatus.NOT_APPLICABLE
    assert profile.status is FullModelStatus.AVAILABLE
    assert assessment.value == Fraction(1, 1)


@pytest.mark.parametrize(
    "profile",
    [
        pytest.param(
            _build(_bundle(second_bound="5", second_comparator="не нижче")),
            id="target-conflict",
        ),
        pytest.param(
            _build(_bundle(second_context="при 600 одночасних користувачах")),
            id="target-unresolved",
        ),
    ],
)
def test_qb_conflict_or_unresolved_target_produces_unresolved_without_value(
    profile,
) -> None:
    assessment = _assess(profile)

    assert assessment.status is FullModelStatus.UNRESOLVED
    assert assessment.value is None
    assert assessment.observed_value is None
    assert assessment.source_conformance_outcome is None


def test_c_v_u_values_and_unknown_states_do_not_change_the_result() -> None:
    baseline_bundle = list(_bundle(observed_value=Decimal("1.8")))
    baseline = _assess(_build(tuple(baseline_bundle)))
    metric_profile = baseline_bundle[1]
    changed_entries = []
    for entry in metric_profile.entries:
        if entry.metric_id in {
            MetricId.RQ_COMPLETENESS,
            MetricId.RQ_VERIFIABILITY,
            MetricId.RQ_UNAMBIGUITY,
        } and getattr(entry.subject_ref, "requirement_id", None) == "R001":
            source_status = replace(entry.source_status, state=entry.status.UNKNOWN)
            entry = replace(
                entry,
                status=entry.status.UNKNOWN,
                applicability=entry.applicability.APPLICABLE,
                value=None,
                numeric_representation=NumericRepresentation.NONE,
                source_status=source_status,
                provenance=replace(entry.provenance, source_status=source_status),
            )
        changed_entries.append(entry)
    baseline_bundle[1] = replace(metric_profile, entries=tuple(changed_entries))

    changed = _assess(_build(tuple(baseline_bundle)))

    assert baseline.value == changed.value == Fraction(1, 1)
    assert changed.status is FullModelStatus.AVAILABLE


def test_qb_fraction_is_preserved_context_and_not_an_assessment_operand() -> None:
    profile = _build(_bundle(observed_value=Decimal("2.3")))
    qb_index = tuple(PerformanceEfficiencyFeatureId).index(
        PerformanceEfficiencyFeatureId.SPECIFICATION_QB
    )
    qb = profile.features[qb_index]
    assert isinstance(qb.typed_value, QbTargetGateFeatureValue)
    changed_qb = replace(
        qb,
        typed_value=replace(
            qb.typed_value,
            source_exact_fraction_or_none=Fraction(0, 1),
        ),
    )
    changed_profile = replace(
        profile,
        features=(
            *profile.features[:qb_index],
            changed_qb,
            *profile.features[qb_index + 1 :],
        ),
    )

    baseline = _assess(profile)
    changed = _assess(changed_profile)

    assert baseline.value == changed.value == Fraction(0, 1)
    assert baseline.source_conformance_outcome is ConformanceOutcome.DOES_NOT_CONFORM
    assert changed.source_conformance_outcome is ConformanceOutcome.DOES_NOT_CONFORM


def test_assessment_preserves_scope_coverage_calibration_and_nonclaims() -> None:
    profile = _build(_bundle())
    assessment = _assess(profile)

    assert tuple(item.channel_id for item in assessment.evidence_coverage.items) == tuple(
        EvidenceChannelId
    )
    assert assessment.evidence_coverage.bounded_procedure_state is BoundedProcedureState.COMPLETE
    assert (
        assessment.evidence_coverage.full_performance_efficiency_coverage
        is FullCharacteristicCoverage.NOT_ESTABLISHED
    )
    assert assessment.evidence_coverage.numeric_coverage is None
    assert assessment.calibration_status is CalibrationStatus.PROVISIONAL_NOT_CALIBRATED
    assert assessment.prediction_value is None
    assert assessment.reliability is None
    assert assessment.uncertainty is None
    assert assessment.non_claims == MANDATORY_NON_CLAIMS
    assert "not complete Performance Efficiency" in assessment.scope_statement
    assert "not a prediction" in assessment.scope_statement


def test_identity_and_output_are_deterministic_and_versioned() -> None:
    profile = _build(_bundle())
    context = _context(profile)

    first = PerformanceEfficiencyQualityAssessor().assess(
        profile, MODEL_REF, PARAMETER_SET_REF, context
    )
    second = PerformanceEfficiencyQualityAssessor().assess(
        profile, MODEL_REF, PARAMETER_SET_REF, context
    )
    changed_context = _context(profile, event_id="PE-QUALITY-EVENT-002")
    changed = assess_product_quality(
        profile, MODEL_REF, PARAMETER_SET_REF, changed_context
    )

    assert first == second
    assert first.assessment_id == second.assessment_id
    assert first.assessment_id != changed.assessment_id


def test_identity_mismatch_fails_closed() -> None:
    profile = _build(_bundle())
    foreign_artifact = ArtifactRef("SPEC-FOREIGN", "1")
    foreign_event = ProductQualityAssessmentEventRef(
        "PE-QUALITY-EVENT-FOREIGN",
        "1",
        profile.product_ref,
        foreign_artifact,
    )

    with pytest.raises(ValueError, match="artifact"):
        ProductQualityAssessmentContext(
            foreign_event,
            foreign_artifact,
            profile.source_assessment_ref,
            profile.profile_id,
            profile.product_ref,
            profile.process_state_ref,
        )

    other_profile = _build(_bundle(artifact_version="2"))
    with pytest.raises(ValueError, match="artifact"):
        ProductQualityAssessmentContext(
            ProductQualityAssessmentEventRef(
                "PE-QUALITY-EVENT-MIXED",
                "1",
                profile.product_ref,
                profile.artifact_ref,
            ),
            profile.artifact_ref,
            profile.source_assessment_ref,
            other_profile.profile_id,
            profile.product_ref,
            profile.process_state_ref,
        )

    other_process = replace(
        profile.process_state_ref,
        process_state_id="PROCESS-PE-OTHER",
    )
    with pytest.raises(ValueError, match="process state"):
        ProductQualityAssessmentContext(
            ProductQualityAssessmentEventRef(
                "PE-QUALITY-EVENT-MIXED",
                "1",
                profile.product_ref,
                profile.artifact_ref,
            ),
            profile.artifact_ref,
            profile.source_assessment_ref,
            profile.profile_id,
            profile.product_ref,
            other_process,
        )


def test_provenance_continues_all_approved_source_paths() -> None:
    profile = _build(_bundle())
    assessment = _assess(profile)
    provenance = assessment.provenance
    qb = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)

    assert provenance.feature_profile_ref == profile.profile_id
    assert provenance.ordered_feature_refs == tuple(
        item.feature_entry_id for item in profile.features
    )
    assert provenance.criterion_ref_or_none is not None
    assert provenance.observation_ref_or_none is not None
    assert provenance.conformance_ref_or_none == (
        profile.provenance.conformance_assessment_ref
    )
    assert provenance.qb_metric_entry_ref == qb.source_refs[0]
    assert provenance.metric_profile_ref == profile.metric_profile_ref
    assert provenance.product_ref == profile.product_ref
    assert provenance.process_state_ref == profile.process_state_ref
    assert provenance.model_ref == MODEL_REF
    assert provenance.parameter_set_ref == PARAMETER_SET_REF


def test_parameter_set_is_empty_and_no_predictive_or_weighting_fields_exist() -> None:
    assert PARAMETER_SET.entries == ()
    field_names = {item.name for item in fields(ProductQualityAssessment)}
    assert "prediction_value" in field_names
    assert field_names.isdisjoint(
        {
            "y_hat_pe",
            "weights",
            "normalized_value",
            "probability",
            "confidence",
            "quality_score",
        }
    )

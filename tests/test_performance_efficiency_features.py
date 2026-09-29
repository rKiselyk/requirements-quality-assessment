from dataclasses import fields, replace
from decimal import Decimal
from fractions import Fraction

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import SpecificationAssessmentService
from requirements_quality_assessment.cross_analysis.domain import (
    AssessmentSnapshotId,
    CrossObservationRef,
)
from requirements_quality_assessment.detectors.quantitative import (
    QuantitativeBaselineDetector,
)
from requirements_quality_assessment.domain import (
    ComparatorLabel,
    DetectionProcessingStatus,
    FeatureDetectionOutcome,
    FeatureId,
    Requirement,
    RequirementExtractionResult,
    RequirementFeatures,
    UnitLabel,
)
from requirements_quality_assessment.dynamic_evidence import (
    Applicability,
    ConformanceEvaluationContext,
    ConformanceOutcome,
    CriterionBindingContext,
    DynamicEvidenceAssessmentRef,
    DynamicEvidenceReason,
    EnvironmentRef,
    FullModelStatus,
    ObservationCollectionRef,
    ObservationSlotRef,
    ObservationSourceKind,
    ProductRef,
    RESPONSE_TIME_METRIC_REF,
    SUPPORTED_CONTEXT_IDENTITY,
    assess_conformance,
    bind_quantitative_criterion,
    make_dynamic_observation,
    resolve_dynamic_observation,
)
from requirements_quality_assessment.metrics import (
    ArtifactRef,
    AssessmentRef,
    MetricConstructionContext,
    MetricId,
    MetricProfileBuilder,
)
from requirements_quality_assessment.performance_efficiency import (
    ConformanceFeatureValue,
    CriterionFeatureValue,
    FeatureEffect,
    FeatureReason,
    ObservationFeatureValue,
    PE_FEATURE_REGISTRY,
    PerformanceEfficiencyFeature,
    PerformanceEfficiencyFeatureConstructionContext,
    PerformanceEfficiencyFeatureId,
    PerformanceEfficiencyFeatureProfileBuilder,
    ProcessStage,
    ProcessStateRef,
    QbTargetGateDecision,
    QbTargetGateFeatureValue,
    RequirementMetricFeatureValue,
)


def _empty(feature_id: FeatureId) -> FeatureDetectionOutcome:
    return FeatureDetectionOutcome(
        feature_id, (), DetectionProcessingStatus.COMPLETE, ()
    )


def _extraction(
    requirement_id: str,
    source_line: int,
    bound: str | None,
    comparator: str = "≤",
    context_text: str = "при 500 одночасних користувачах",
    unit_text: str = "с",
) -> RequirementExtractionResult:
    text = (
        "Система зберігає дані."
        if bound is None
        else f"Час відгуку {comparator} {bound} {unit_text} {context_text}"
    )
    requirement = Requirement(requirement_id, source_line, text)
    quantitative, evidence = QuantitativeBaselineDetector().detect(requirement)
    return RequirementExtractionResult(
        requirement,
        RequirementFeatures(
            _empty(FeatureId.CONDITION_CONTEXT),
            _empty(FeatureId.EXPECTED_RESULT),
            _empty(FeatureId.ACCEPTANCE_CRITERION),
            quantitative,
            _empty(FeatureId.VERIFICATION_METHOD),
            _empty(FeatureId.VAGUE_TERM_OCCURRENCE),
        ),
        evidence,
    )


def _assessed_source(
    second_bound: str | None = "3",
    second_comparator: str = "≤",
    second_context: str = "при 500 одночасних користувачах",
    second_unit: str = "с",
):
    extractions = [_extraction("R001", 1, "2")]
    if second_bound is not None:
        extractions.append(
            _extraction(
                "R002",
                2,
                second_bound,
                second_comparator,
                second_context,
                second_unit,
            )
        )
    records = tuple(
        RequirementQualityAssessor().assess_record(item) for item in extractions
    )
    return SpecificationAssessmentService().assess(records)


def _collection(
    product_version: str = "1",
    collection_version: str = "1",
) -> ObservationCollectionRef:
    return ObservationCollectionRef(
        "PE-COLLECTION",
        collection_version,
        ProductRef("PE-PRODUCT", product_version),
        EnvironmentRef("PE-ENV", "1"),
        ObservationSourceKind.DETERMINISTIC_FIXTURE,
    )


def _bundle(
    *,
    second_bound: str | None = "3",
    second_comparator: str = "≤",
    second_context: str = "при 500 одночасних користувачах",
    second_unit: str = "с",
    observed_value: Decimal | None = Decimal("1.80"),
    artifact_version: str = "1",
    assessment_version: str = "1",
):
    source = _assessed_source(
        second_bound, second_comparator, second_context, second_unit
    )
    artifact = ArtifactRef("SPEC-PE-001", artifact_version)
    assessment = AssessmentRef("ASSESS-PE-001", assessment_version, artifact)
    metric_profile = MetricProfileBuilder().build(
        source, MetricConstructionContext(artifact, assessment)
    )
    binding_context = CriterionBindingContext(
        artifact, assessment, source.snapshot_id
    )
    binding = bind_quantitative_criterion(
        source.records[0].extraction_result,
        CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0),
        binding_context,
    )
    collection = _collection()
    slot = ObservationSlotRef(collection, 0)
    observation = (
        None
        if observed_value is None
        else make_dynamic_observation(
            slot,
            RESPONSE_TIME_METRIC_REF,
            observed_value,
            UnitLabel.SECOND,
            SUPPORTED_CONTEXT_IDENTITY,
            "PE-OBS-001",
        )
    )
    resolution = resolve_dynamic_observation(slot, observation)
    dynamic_ref = DynamicEvidenceAssessmentRef(
        "ASSESS-PE-DYN-001",
        "1",
        artifact,
        collection.product_ref,
        collection,
    )
    conformance = assess_conformance(
        binding, resolution, ConformanceEvaluationContext(dynamic_ref)
    )
    context = PerformanceEfficiencyFeatureConstructionContext(
        artifact,
        assessment,
        metric_profile.profile_id,
        dynamic_ref,
        collection.product_ref,
        ProcessStateRef(
            "PROCESS-PE-001", "1", ProcessStage.REFERENCE_VERIFICATION
        ),
    )
    return source, metric_profile, binding, resolution, conformance, context


def _build(bundle):
    source, metric_profile, binding, resolution, conformance, context = bundle
    return PerformanceEfficiencyFeatureProfileBuilder().build(
        metric_profile, source, binding, resolution, conformance, context
    )


def _feature(profile, feature_id: PerformanceEfficiencyFeatureId):
    return next(item for item in profile.features if item.feature_id is feature_id)


def test_complete_profile_has_exact_registry_roles_order_and_identity() -> None:
    bundle = _bundle()

    first = _build(bundle)
    second = _build(bundle)

    assert first == second
    assert first.profile_id == second.profile_id
    assert tuple(item.feature_id for item in first.features) == PE_FEATURE_REGISTRY
    assert tuple(item.feature_entry_id for item in first.features) == (
        first.provenance.ordered_feature_entry_refs
    )
    assert tuple(item.effect for item in first.features) == (
        FeatureEffect.REQUIRED_INPUT,
        FeatureEffect.CONTEXT_ONLY,
        FeatureEffect.CONTEXT_ONLY,
        FeatureEffect.CONTEXT_ONLY,
        FeatureEffect.ELIGIBILITY_GATE,
        FeatureEffect.REQUIRED_INPUT,
        FeatureEffect.DIRECT_RESULT_INPUT,
    )
    assert first.status is FullModelStatus.AVAILABLE
    assert first.applicability is Applicability.APPLICABLE


def test_values_are_copied_exactly_without_recalculation_or_coercion() -> None:
    _, metric_profile, binding, resolution, conformance, _ = bundle = _bundle(
        observed_value=Decimal("1.800")
    )
    profile = _build(bundle)

    criterion = _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    ).typed_value
    observation = _feature(
        profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME
    ).typed_value
    conformance_value = _feature(
        profile, PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME
    ).typed_value
    assert isinstance(criterion, CriterionFeatureValue)
    assert criterion.exact_decimal_bound is binding.criterion.bound
    assert criterion.exact_decimal_bound.as_tuple() == Decimal("2").as_tuple()
    assert isinstance(observation, ObservationFeatureValue)
    assert observation.exact_decimal_value is resolution.observation.observed_value
    assert observation.exact_decimal_value.as_tuple() == Decimal("1.800").as_tuple()
    assert isinstance(conformance_value, ConformanceFeatureValue)
    assert conformance_value.outcome is conformance.outcome is ConformanceOutcome.CONFORMS

    for feature_id, metric_id in (
        (PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS, MetricId.RQ_COMPLETENESS),
        (PerformanceEfficiencyFeatureId.REQUIREMENT_VERIFIABILITY, MetricId.RQ_VERIFIABILITY),
        (PerformanceEfficiencyFeatureId.REQUIREMENT_UNAMBIGUITY, MetricId.RQ_UNAMBIGUITY),
    ):
        feature = _feature(profile, feature_id)
        source_entry = next(
            item
            for item in metric_profile.entries
            if item.metric_id is metric_id
            and isinstance(item.subject_ref, type(binding.binding_id.requirement_subject_ref))
            and item.subject_ref.requirement_id == "R001"
        )
        if source_entry.value is None:
            assert feature.typed_value is None
        else:
            assert isinstance(feature.typed_value, RequirementMetricFeatureValue)
            assert feature.typed_value.exact_fraction_or_none is source_entry.value
            assert type(feature.typed_value.exact_fraction_or_none) is Fraction


def test_requirement_quality_features_are_context_only_and_do_not_control_readiness() -> None:
    bundle = list(_bundle())
    metric_profile = bundle[1]
    replaced_entries = []
    for entry in metric_profile.entries:
        if entry.metric_id in {
            MetricId.RQ_COMPLETENESS,
            MetricId.RQ_VERIFIABILITY,
            MetricId.RQ_UNAMBIGUITY,
        } and getattr(entry.subject_ref, "requirement_id", None) == "R001":
            source_status = replace(entry.source_status, state=entry.status.UNKNOWN)
            provenance = replace(entry.provenance, source_status=source_status)
            entry = replace(
                entry,
                status=entry.status.UNKNOWN,
                applicability=entry.applicability.APPLICABLE,
                value=None,
                numeric_representation=entry.numeric_representation.NONE,
                source_status=source_status,
                provenance=provenance,
            )
        replaced_entries.append(entry)
    bundle[1] = replace(metric_profile, entries=tuple(replaced_entries))

    profile = _build(tuple(bundle))

    assert profile.status is FullModelStatus.AVAILABLE
    assert all(
        _feature(profile, feature_id).status is FullModelStatus.UNKNOWN
        for feature_id in (
            PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS,
            PerformanceEfficiencyFeatureId.REQUIREMENT_VERIFIABILITY,
            PerformanceEfficiencyFeatureId.REQUIREMENT_UNAMBIGUITY,
        )
    )
    assert all(
        _feature(profile, feature_id).effect is FeatureEffect.CONTEXT_ONLY
        for feature_id in (
            PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS,
            PerformanceEfficiencyFeatureId.REQUIREMENT_VERIFIABILITY,
            PerformanceEfficiencyFeatureId.REQUIREMENT_UNAMBIGUITY,
        )
    )


def test_qb_target_clear_preserves_bounded_metric_without_using_its_fraction() -> None:
    source, metric_profile, *_ = bundle = _bundle()
    profile = _build(bundle)
    feature = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)
    qb_entry = next(
        item for item in metric_profile.entries if item.metric_id is MetricId.SPEC_QB_CONSISTENCY
    )

    assert isinstance(feature.typed_value, QbTargetGateFeatureValue)
    assert feature.typed_value.gate_decision is QbTargetGateDecision.TARGET_CLEAR
    assert feature.typed_value.source_exact_fraction_or_none is qb_entry.value
    assert feature.typed_value.ordered_cross_result_refs == tuple(
        item.result_id for item in source.cross_results
    )
    assert feature.effect is FeatureEffect.ELIGIBILITY_GATE


def test_same_target_qb_conflict_is_visible_and_profile_is_unresolved() -> None:
    bundle = _bundle(second_bound="5", second_comparator="не нижче")
    profile = _build(bundle)
    qb = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)
    conformance = _feature(
        profile, PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME
    )

    assert qb.status is FullModelStatus.AVAILABLE
    assert qb.typed_value.gate_decision is QbTargetGateDecision.TARGET_CONFLICT
    assert FeatureReason.QB_TARGET_CONFLICT in qb.reasons
    assert profile.status is FullModelStatus.UNRESOLVED
    assert isinstance(conformance.typed_value, ConformanceFeatureValue)
    assert conformance.typed_value.outcome is ConformanceOutcome.CONFORMS


def test_proven_different_qb_key_is_not_fabricated_as_target_evidence() -> None:
    profile = _build(_bundle(second_unit="хв"))
    qb = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)

    assert qb.status is FullModelStatus.NOT_APPLICABLE
    assert qb.applicability is Applicability.NOT_APPLICABLE
    assert qb.typed_value is None
    assert qb.source_refs[1:] == ()
    assert profile.status is FullModelStatus.AVAILABLE


def test_potential_target_qb_identity_gap_propagates_unresolved() -> None:
    profile = _build(
        _bundle(second_context="при 600 одночасних користувачах")
    )
    qb = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)

    assert qb.status is FullModelStatus.UNRESOLVED
    assert qb.typed_value is None
    assert qb.reasons == (FeatureReason.QB_TARGET_UNRESOLVED,)
    assert profile.status is FullModelStatus.UNRESOLVED


def test_unknown_criterion_controls_profile_without_erasing_context_metrics() -> None:
    bundle = list(_bundle())
    binding = replace(
        bundle[2],
        status=FullModelStatus.UNKNOWN,
        applicability=Applicability.UNKNOWN,
        criterion=None,
        reasons=(),
    )
    conformance = assess_conformance(
        binding,
        bundle[3],
        ConformanceEvaluationContext(bundle[5].dynamic_assessment_ref),
    )
    bundle[2] = binding
    bundle[4] = conformance

    profile = _build(tuple(bundle))

    assert profile.status is FullModelStatus.UNKNOWN
    assert profile.applicability is Applicability.UNKNOWN
    assert profile.target_key is None
    assert _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    ).typed_value is None
    assert all(
        _feature(profile, feature_id).effect is FeatureEffect.CONTEXT_ONLY
        for feature_id in (
            PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS,
            PerformanceEfficiencyFeatureId.REQUIREMENT_VERIFIABILITY,
            PerformanceEfficiencyFeatureId.REQUIREMENT_UNAMBIGUITY,
        )
    )


@pytest.mark.parametrize(
    ("status", "applicability", "reason"),
    [
        (
            FullModelStatus.UNAVAILABLE,
            Applicability.APPLICABLE,
            DynamicEvidenceReason.OBSERVATION_NOT_COLLECTED,
        ),
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
def test_dynamic_nonvalue_states_propagate_without_zero_or_nonconformance(
    status, applicability, reason
) -> None:
    bundle = list(_bundle(observed_value=None))
    resolution = bundle[3]
    reasons = () if reason is None else (reason,)
    resolution = replace(
        resolution,
        status=status,
        applicability=applicability,
        reasons=reasons,
    )
    dynamic_ref = bundle[5].dynamic_assessment_ref
    conformance = assess_conformance(
        bundle[2], resolution, ConformanceEvaluationContext(dynamic_ref)
    )
    bundle[3] = resolution
    bundle[4] = conformance

    profile = _build(tuple(bundle))
    observation = _feature(
        profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME
    )
    conformance_feature = _feature(
        profile, PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME
    )

    assert profile.status is status
    assert observation.status is status
    assert observation.typed_value is None
    assert conformance_feature.status is status
    assert conformance_feature.typed_value is None


def test_no_applicable_criterion_propagates_not_applicable() -> None:
    extraction = _extraction("R001", 1, None)
    source = SpecificationAssessmentService().assess(
        (RequirementQualityAssessor().assess_record(extraction),)
    )
    artifact = ArtifactRef("SPEC-PE-NA", "1")
    assessment = AssessmentRef("ASSESS-PE-NA", "1", artifact)
    metric_profile = MetricProfileBuilder().build(
        source, MetricConstructionContext(artifact, assessment)
    )
    binding = bind_quantitative_criterion(
        extraction,
        None,
        CriterionBindingContext(artifact, assessment, source.snapshot_id),
    )
    collection = _collection()
    slot = ObservationSlotRef(collection, 0)
    resolution = resolve_dynamic_observation(slot, None)
    dynamic_ref = DynamicEvidenceAssessmentRef(
        "ASSESS-PE-DYN-NA", "1", artifact, collection.product_ref, collection
    )
    conformance = assess_conformance(
        binding, resolution, ConformanceEvaluationContext(dynamic_ref)
    )
    context = PerformanceEfficiencyFeatureConstructionContext(
        artifact,
        assessment,
        metric_profile.profile_id,
        dynamic_ref,
        collection.product_ref,
        ProcessStateRef("PROCESS-PE-NA", "1", ProcessStage.REFERENCE_VERIFICATION),
    )

    profile = PerformanceEfficiencyFeatureProfileBuilder().build(
        metric_profile, source, binding, resolution, conformance, context
    )

    assert profile.status is FullModelStatus.NOT_APPLICABLE
    assert profile.applicability is Applicability.NOT_APPLICABLE
    assert profile.target_key is None
    assert all(
        item.typed_value is None
        for item in profile.features
        if item.status is not FullModelStatus.AVAILABLE
    )


def test_provenance_continuity_preserves_all_five_approved_paths() -> None:
    source, metric_profile, binding, resolution, conformance, _ = bundle = _bundle()
    profile = _build(bundle)
    criterion = _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    )
    c_feature = _feature(
        profile, PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS
    )
    qb = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)
    observation = _feature(
        profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME
    )
    conformance_feature = _feature(
        profile, PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME
    )

    c_entry = next(
        item
        for item in metric_profile.entries
        if item.metric_id is MetricId.RQ_COMPLETENESS
        and getattr(item.subject_ref, "requirement_id", None) == "R001"
    )
    assert criterion.source_refs == (binding.binding_id,)
    assert criterion.evidence_refs == binding.criterion.provenance.evidence_refs
    assert c_feature.source_refs == (c_entry.entry_id,)
    assert c_feature.evidence_refs == c_entry.provenance.evidence_refs
    assert qb.source_refs[0].metric_id is MetricId.SPEC_QB_CONSISTENCY
    assert tuple(item.result_id for item in source.cross_results) == (
        qb.typed_value.ordered_cross_result_refs
    )
    assert observation.source_refs[0].observation_id == (
        resolution.observation.observation_id
    )
    assert conformance_feature.source_refs == (conformance.conformance_id,)
    assert profile.provenance.criterion_binding_ref == binding.binding_id
    assert profile.provenance.conformance_assessment_ref == conformance.conformance_id


def test_mixed_artifact_assessment_snapshot_product_and_collection_fail_closed() -> None:
    source, metric_profile, binding, resolution, conformance, context = _bundle()
    other_artifact = ArtifactRef("SPEC-OTHER", "1")
    other_assessment = AssessmentRef("ASSESS-OTHER", "1", other_artifact)
    other_binding = bind_quantitative_criterion(
        source.records[0].extraction_result,
        CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0),
        CriterionBindingContext(other_artifact, other_assessment, source.snapshot_id),
    )
    with pytest.raises(ValueError, match="artifacts"):
        PerformanceEfficiencyFeatureProfileBuilder().build(
            metric_profile,
            source,
            other_binding,
            resolution,
            conformance,
            context,
        )

    snapshot_binding = bind_quantitative_criterion(
        source.records[0].extraction_result,
        CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0),
        CriterionBindingContext(
            context.artifact_ref,
            context.source_assessment_ref,
            AssessmentSnapshotId.from_bytes(b"other-snapshot"),
        ),
    )
    with pytest.raises(ValueError, match="snapshots"):
        PerformanceEfficiencyFeatureProfileBuilder().build(
            metric_profile,
            source,
            snapshot_binding,
            resolution,
            conformance,
            context,
        )

    other_assessment = AssessmentRef(
        "ASSESS-PE-OTHER", "1", context.artifact_ref
    )
    assessment_binding = bind_quantitative_criterion(
        source.records[0].extraction_result,
        CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0),
        CriterionBindingContext(
            context.artifact_ref, other_assessment, source.snapshot_id
        ),
    )
    with pytest.raises(ValueError, match="assessments"):
        PerformanceEfficiencyFeatureProfileBuilder().build(
            metric_profile,
            source,
            assessment_binding,
            resolution,
            conformance,
            context,
        )

    foreign_collection = _collection(product_version="2", collection_version="2")
    foreign_resolution = resolve_dynamic_observation(
        ObservationSlotRef(foreign_collection, 0), None
    )
    with pytest.raises(ValueError, match="collections"):
        PerformanceEfficiencyFeatureProfileBuilder().build(
            metric_profile,
            source,
            binding,
            foreign_resolution,
            conformance,
            context,
        )


def test_feature_contract_has_no_scoring_weighting_or_fabricated_registry_fields() -> None:
    assert tuple(PerformanceEfficiencyFeatureId) == PE_FEATURE_REGISTRY
    assert {item.name for item in fields(PerformanceEfficiencyFeature)}.isdisjoint(
        {
            "weight",
            "normalized_value",
            "rounded_value",
            "score",
            "prediction",
            "quality_probability",
            "confidence",
        }
    )
    assert len(_build(_bundle()).features) == 7


def test_profile_identity_changes_with_approved_versioned_context() -> None:
    first = _build(_bundle())
    changed_artifact = _build(_bundle(artifact_version="2"))
    changed_assessment = _build(_bundle(assessment_version="2"))

    assert first.profile_id != changed_artifact.profile_id
    assert first.profile_id != changed_assessment.profile_id

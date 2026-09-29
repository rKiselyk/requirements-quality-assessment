"""M3-02 lossless Full Model v0.1 metric-profile acceptance tests."""

from dataclasses import FrozenInstanceError, fields, replace
from decimal import Decimal
from fractions import Fraction

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import (
    BoundedNonClaimKey,
    CrossResultState,
    QbConsistencyState,
    SpecificationAssessmentService,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    CharacteristicAssessmentState,
    ComparatorComponent,
    ComparatorLabel,
    DetectionDiagnostic,
    DetectionProcessingStatus,
    Evidence,
    FeatureDetectionOutcome,
    FeatureId,
    FeatureObservation,
    NumericValueComponent,
    QuantitativeComponentName,
    QuantitativeConstraintObservation,
    Requirement,
    RequirementExtractionResult,
    RequirementFeatures,
    TextComponent,
    UnitComponent,
    UnitLabel,
)
from requirements_quality_assessment.metrics import (
    ArtifactRef,
    AssessmentRef,
    MetricApplicability,
    MetricConstructionContext,
    MetricEntry,
    MetricId,
    MetricProfileBuilder,
    MetricScope,
    MetricStatus,
    NumericRepresentation,
    RequirementCharacteristicRef,
    RequirementEvidenceRef,
    RequirementSubjectRef,
    RuleVersionAuthority,
    SourceStatusRef,
    SpecificationAggregateCounts,
    build_metric_profile,
    serialize_metric_value,
)


METRIC = "Час відгуку"
CONTEXT = "при навантаженні"


def _empty(feature_id: FeatureId):
    return FeatureDetectionOutcome(
        feature_id=feature_id,
        observations=(),
        processing_status=DetectionProcessingStatus.COMPLETE,
        diagnostics=(),
    )


def _simple_observation(
    requirement: Requirement,
    feature_id: FeatureId,
    text: str,
    evidence_id: str,
):
    start = requirement.text.index(text)
    evidence = Evidence(
        evidence_id=evidence_id,
        requirement_id=requirement.id,
        feature_id=feature_id,
        text=text,
        start_offset=start,
        end_offset=start + len(text),
        rule_id="TEST-FEATURE-001",
    )
    outcome = FeatureDetectionOutcome(
        feature_id=feature_id,
        observations=(FeatureObservation(feature_id, (evidence_id,)),),
        processing_status=DetectionProcessingStatus.COMPLETE,
        diagnostics=(),
    )
    return outcome, (evidence,)


def _quantitative_observation(
    requirement: Requirement,
    comparator: ComparatorLabel,
    value: Decimal,
    *,
    unresolved_components: tuple[QuantitativeComponentName, ...] = (),
):
    bound_text = "≤ 2" if comparator is ComparatorLabel.LESS_THAN_OR_EQUAL else "≥ 5"
    pieces = (
        ("Q:M", METRIC, "QUANT-METRIC-TEST"),
        ("Q:B", bound_text, "QUANT-BOUND-TEST"),
        ("Q:U", "с", "QUANT-UNIT-TEST"),
        ("Q:C", CONTEXT, "QUANT-CONTEXT-TEST"),
    )
    evidence = tuple(
        Evidence(
            evidence_id=evidence_id,
            requirement_id=requirement.id,
            feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
            text=text,
            start_offset=requirement.text.index(text),
            end_offset=requirement.text.index(text) + len(text),
            rule_id=rule_id,
        )
        for evidence_id, text, rule_id in pieces
        if not (
            evidence_id == "Q:M"
            and QuantitativeComponentName.METRIC in unresolved_components
        )
        and not (
            evidence_id == "Q:C"
            and QuantitativeComponentName.CONTEXT in unresolved_components
        )
    )
    refs = tuple(item.evidence_id for item in evidence)
    observation = QuantitativeConstraintObservation(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        metric=(
            None
            if QuantitativeComponentName.METRIC in unresolved_components
            else TextComponent(("Q:M",))
        ),
        comparator=ComparatorComponent(
            comparator,
            BoundaryInclusivity.INCLUSIVE,
            ("Q:B",),
        ),
        value=NumericValueComponent(value, ("Q:B",)),
        unit=UnitComponent(UnitLabel.SECOND, ("Q:U",)),
        context=(
            None
            if QuantitativeComponentName.CONTEXT in unresolved_components
            else TextComponent(("Q:C",))
        ),
        unresolved_components=unresolved_components,
        evidence_refs=refs,
    )
    return (
        FeatureDetectionOutcome(
            feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
            observations=(observation,),
            processing_status=DetectionProcessingStatus.COMPLETE,
            diagnostics=(),
        ),
        evidence,
    )


def _record(
    requirement_id: str,
    source_line: int,
    comparator: ComparatorLabel,
    value: Decimal,
    *,
    unresolved_components: tuple[QuantitativeComponentName, ...] = (),
):
    symbol = "≤ 2" if comparator is ComparatorLabel.LESS_THAN_OR_EQUAL else "≥ 5"
    requirement = Requirement(
        requirement_id,
        source_line,
        f"{METRIC} {symbol} с {CONTEXT}",
    )
    condition, condition_evidence = _simple_observation(
        requirement,
        FeatureId.CONDITION_CONTEXT,
        CONTEXT,
        "COND:E001",
    )
    expected, expected_evidence = _simple_observation(
        requirement,
        FeatureId.EXPECTED_RESULT,
        METRIC,
        "RESULT:E001",
    )
    quantitative, quantitative_evidence = _quantitative_observation(
        requirement,
        comparator,
        value,
        unresolved_components=unresolved_components,
    )
    extraction = RequirementExtractionResult(
        requirement=requirement,
        features=RequirementFeatures(
            condition_contexts=condition,
            expected_results=expected,
            acceptance_criteria=_empty(FeatureId.ACCEPTANCE_CRITERION),
            quantitative_constraints=quantitative,
            verification_methods=_empty(FeatureId.VERIFICATION_METHOD),
            vague_term_occurrences=_empty(FeatureId.VAGUE_TERM_OCCURRENCE),
        ),
        evidence=condition_evidence + expected_evidence + quantitative_evidence,
    )
    return RequirementQualityAssessor().assess_record(extraction)


def _unknown_record(requirement_id: str = "R001", source_line: int = 1):
    requirement = Requirement(requirement_id, source_line, "Система працює")
    diagnostic = DetectionDiagnostic(
        code="TEST_UNRESOLVED",
        explanation="test fixture unresolved input",
        rule_id="TEST-FEATURE-001",
    )

    def unresolved(feature_id: FeatureId):
        return FeatureDetectionOutcome(
            feature_id=feature_id,
            observations=(),
            processing_status=DetectionProcessingStatus.INCOMPLETE,
            diagnostics=(diagnostic,),
        )

    extraction = RequirementExtractionResult(
        requirement=requirement,
        features=RequirementFeatures(
            condition_contexts=unresolved(FeatureId.CONDITION_CONTEXT),
            expected_results=_empty(FeatureId.EXPECTED_RESULT),
            acceptance_criteria=_empty(FeatureId.ACCEPTANCE_CRITERION),
            quantitative_constraints=_empty(FeatureId.QUANTITATIVE_CONSTRAINT),
            verification_methods=_empty(FeatureId.VERIFICATION_METHOD),
            vague_term_occurrences=unresolved(FeatureId.VAGUE_TERM_OCCURRENCE),
        ),
        evidence=(),
    )
    return RequirementQualityAssessor().assess_record(extraction)


def _context(
    artifact_version: str = "v1", assessment_version: str = "1"
) -> MetricConstructionContext:
    artifact = ArtifactRef("SPEC-A", artifact_version)
    return MetricConstructionContext(
        artifact_ref=artifact,
        assessment_ref=AssessmentRef(
            "ASSESS-A",
            assessment_version,
            artifact,
        ),
    )


def _assess(*records):
    return SpecificationAssessmentService().assess(records)


def _entry(profile, metric_id: MetricId, requirement_id: str | None = None):
    return next(
        item
        for item in profile.entries
        if item.metric_id is metric_id
        and (
            requirement_id is None
            or (
                isinstance(item.subject_ref, RequirementSubjectRef)
                and item.subject_ref.requirement_id == requirement_id
            )
        )
    )


def test_requirement_c_v_u_and_specification_metrics_are_lossless_and_ordered():
    records = (
        _record("R001", 1, ComparatorLabel.LESS_THAN_OR_EQUAL, Decimal("2")),
        _record("R002", 2, ComparatorLabel.GREATER_THAN_OR_EQUAL, Decimal("5")),
    )
    source = _assess(*records)
    before = repr(source)

    profile = build_metric_profile(source, _context())

    assert len(profile.entries) == 10
    assert [item.metric_id for item in profile.entries] == [
        MetricId.RQ_COMPLETENESS,
        MetricId.RQ_VERIFIABILITY,
        MetricId.RQ_UNAMBIGUITY,
        MetricId.RQ_COMPLETENESS,
        MetricId.RQ_VERIFIABILITY,
        MetricId.RQ_UNAMBIGUITY,
        MetricId.SPEC_MEAN_COMPLETENESS,
        MetricId.SPEC_MEAN_VERIFIABILITY,
        MetricId.SPEC_MEAN_UNAMBIGUITY,
        MetricId.SPEC_QB_CONSISTENCY,
    ]
    for requirement_id in ("R001", "R002"):
        assert _entry(profile, MetricId.RQ_COMPLETENESS, requirement_id).value == Fraction(2, 3)
        assert _entry(profile, MetricId.RQ_VERIFIABILITY, requirement_id).value == Fraction(1, 2)
        assert _entry(profile, MetricId.RQ_UNAMBIGUITY, requirement_id).value == Fraction(1, 1)
    assert _entry(profile, MetricId.SPEC_MEAN_COMPLETENESS).value == Fraction(2, 3)
    assert _entry(profile, MetricId.SPEC_MEAN_VERIFIABILITY).value == Fraction(1, 2)
    assert _entry(profile, MetricId.SPEC_MEAN_UNAMBIGUITY).value == Fraction(1, 1)
    qb = _entry(profile, MetricId.SPEC_QB_CONSISTENCY)
    assert qb.value == Fraction(0, 1)
    assert qb.status is MetricStatus.AVAILABLE
    assert qb.applicability is MetricApplicability.APPLICABLE
    assert qb.provenance.source_metric_label == "M_cons[QB-v0.1]"
    assert qb.provenance.source_non_claim_refs == (BoundedNonClaimKey.NC_QB_BASE,)
    assert source.cross_results[0].state is CrossResultState.CONFIRMED_CONFLICT
    assert profile.entries[0].value is records[0].quality_profile.completeness.value
    assert profile.entries[6].value is source.specification_assessment.quality_profile.completeness.value
    assert qb.value is source.specification_assessment.qb_consistency.value
    assert repr(source) == before


def test_exact_fraction_representation_never_uses_float_rounding_or_imputation():
    profile = build_metric_profile(
        _assess(
            _record("R001", 1, ComparatorLabel.LESS_THAN_OR_EQUAL, Decimal("2")),
            _record("R002", 2, ComparatorLabel.GREATER_THAN_OR_EQUAL, Decimal("5")),
        ),
        _context(),
    )

    for entry in profile.entries:
        if entry.status is MetricStatus.AVAILABLE:
            assert type(entry.value) is Fraction
            assert entry.numeric_representation is NumericRepresentation.EXACT_FRACTION
        else:
            assert entry.value is None
            assert entry.numeric_representation is NumericRepresentation.NONE
    assert serialize_metric_value(Fraction(11, 18)) == {
        "kind": "FRACTION",
        "numerator": 11,
        "denominator": 18,
    }
    assert serialize_metric_value(None) is None


def test_unknown_and_not_applicable_states_preserve_status_and_applicability():
    source = _assess(_unknown_record())
    profile = build_metric_profile(source, _context())

    completeness = _entry(profile, MetricId.RQ_COMPLETENESS, "R001")
    unambiguity = _entry(profile, MetricId.RQ_UNAMBIGUITY, "R001")
    qb = _entry(profile, MetricId.SPEC_QB_CONSISTENCY)
    assert completeness.status is MetricStatus.UNKNOWN
    assert completeness.applicability is MetricApplicability.APPLICABLE
    assert completeness.value is None
    assert completeness.source_status.state.value == "UNKNOWN"
    assert unambiguity.status is MetricStatus.UNKNOWN
    assert qb.status is MetricStatus.NOT_APPLICABLE
    assert qb.applicability is MetricApplicability.NOT_APPLICABLE
    assert qb.value is None
    assert qb.provenance.source_reasons[0].value == "FEWER_THAN_TWO_REQUIREMENTS"


def test_empty_specification_has_four_not_applicable_entries_and_no_synthetic_zero():
    profile = build_metric_profile(_assess(), _context())

    assert [item.metric_id for item in profile.entries] == [
        MetricId.SPEC_MEAN_COMPLETENESS,
        MetricId.SPEC_MEAN_VERIFIABILITY,
        MetricId.SPEC_MEAN_UNAMBIGUITY,
        MetricId.SPEC_QB_CONSISTENCY,
    ]
    assert all(item.status is MetricStatus.NOT_APPLICABLE for item in profile.entries)
    assert all(
        item.applicability is MetricApplicability.NOT_APPLICABLE
        for item in profile.entries
    )
    assert all(item.value is None for item in profile.entries)
    counts = profile.entries[0].provenance.source_counts_or_observability
    assert counts == SpecificationAggregateCounts(0, 0, 0, 0)


def test_qb_unknown_applicability_distinguishes_known_applicable_comparison():
    known_applicable = _assess(
        _record("R001", 1, ComparatorLabel.LESS_THAN_OR_EQUAL, Decimal("2")),
        _record("R002", 2, ComparatorLabel.LESS_THAN_OR_EQUAL, Decimal("2")),
        _record(
            "R003",
            3,
            ComparatorLabel.LESS_THAN_OR_EQUAL,
            Decimal("2"),
            unresolved_components=(QuantitativeComponentName.METRIC,),
        ),
    )
    only_uncertain = _assess(
        _record(
            "R001",
            1,
            ComparatorLabel.LESS_THAN_OR_EQUAL,
            Decimal("2"),
            unresolved_components=(QuantitativeComponentName.METRIC,),
        ),
        _record(
            "R002",
            2,
            ComparatorLabel.LESS_THAN_OR_EQUAL,
            Decimal("2"),
            unresolved_components=(QuantitativeComponentName.METRIC,),
        ),
    )

    known_metric = _entry(
        build_metric_profile(known_applicable, _context()),
        MetricId.SPEC_QB_CONSISTENCY,
    )
    uncertain_metric = _entry(
        build_metric_profile(only_uncertain, _context()),
        MetricId.SPEC_QB_CONSISTENCY,
    )
    assert known_applicable.specification_assessment.qb_consistency.state is QbConsistencyState.UNKNOWN
    assert known_metric.status is MetricStatus.UNKNOWN
    assert known_metric.applicability is MetricApplicability.APPLICABLE
    assert uncertain_metric.status is MetricStatus.UNKNOWN
    assert uncertain_metric.applicability is MetricApplicability.UNKNOWN
    assert known_metric.value is uncertain_metric.value is None


def test_requirement_and_qb_provenance_remain_resolvable_without_new_evidence():
    source = _assess(
        _record("R001", 1, ComparatorLabel.LESS_THAN_OR_EQUAL, Decimal("2")),
        _record("R002", 2, ComparatorLabel.GREATER_THAN_OR_EQUAL, Decimal("5")),
    )
    profile = build_metric_profile(source, _context())
    completeness = _entry(profile, MetricId.RQ_COMPLETENESS, "R001")

    assert isinstance(
        completeness.source_assessment_refs[0], RequirementCharacteristicRef
    )
    assert completeness.provenance.source_trace_refs[0].governing_rule_id == "CALC-C-MVP-001"
    source_evidence_ids = {
        item.evidence_id for item in source.records[0].extraction_result.evidence
    }
    assert all(
        isinstance(ref, RequirementEvidenceRef)
        and ref.evidence_id in source_evidence_ids
        for ref in completeness.provenance.evidence_refs
    )
    assert not any(
        ref.evidence_id not in source_evidence_ids
        for ref in completeness.provenance.evidence_refs
    )

    qb = _entry(profile, MetricId.SPEC_QB_CONSISTENCY)
    assert qb.provenance.cross_result_refs == tuple(
        item.result_id for item in source.cross_results
    )
    assert qb.provenance.source_formula_operands is source.specification_assessment.qb_consistency.formula_operands
    assert qb.provenance.source_counts_or_observability is source.specification_assessment.qb_consistency.observability
    for ref in qb.provenance.evidence_refs:
        source.resolver.resolve_evidence(ref, snapshot_id=source.snapshot_id)


def test_profile_identity_and_order_are_deterministic_and_version_qualified():
    source = _assess(
        _record("R001", 1, ComparatorLabel.LESS_THAN_OR_EQUAL, Decimal("2")),
        _record("R002", 2, ComparatorLabel.GREATER_THAN_OR_EQUAL, Decimal("5")),
    )
    first = MetricProfileBuilder().build(source, _context())
    second = MetricProfileBuilder().build(source, _context())
    changed_assessment = MetricProfileBuilder().build(
        source, _context(assessment_version="2")
    )
    changed_artifact = MetricProfileBuilder().build(
        source, _context(artifact_version="v2")
    )

    assert first == second
    assert tuple(item.entry_id for item in first.entries) == tuple(
        item.entry_id for item in second.entries
    )
    assert first.profile_id != changed_assessment.profile_id
    assert first.profile_id != changed_artifact.profile_id
    assert first.entries[0].subject_ref.source_line == 1
    assert first.entries[3].subject_ref.source_line == 2


@pytest.mark.parametrize(
    "status",
    [MetricStatus.UNRESOLVED, MetricStatus.UNAVAILABLE, MetricStatus.UNSUPPORTED],
)
def test_partial_future_non_value_statuses_obey_the_closed_matrix(status):
    base = _entry(
        build_metric_profile(_assess(_unknown_record()), _context()),
        MetricId.RQ_COMPLETENESS,
        "R001",
    )
    source_status = SourceStatusRef(status)
    provenance = replace(base.provenance, source_status=source_status)

    entry = replace(
        base,
        status=status,
        applicability=MetricApplicability.UNKNOWN,
        source_status=source_status,
        provenance=provenance,
    )

    assert entry.value is None
    assert entry.numeric_representation is NumericRepresentation.NONE


def test_metric_domain_rejects_values_for_non_available_statuses_and_float_values():
    base = _entry(
        build_metric_profile(_assess(_unknown_record()), _context()),
        MetricId.RQ_COMPLETENESS,
        "R001",
    )
    with pytest.raises(ValueError, match="non-AVAILABLE"):
        replace(base, value=Fraction(0, 1))
    with pytest.raises(ValueError, match="exact Fraction"):
        replace(
            base,
            status=MetricStatus.AVAILABLE,
            applicability=MetricApplicability.APPLICABLE,
            value=0.0,
            numeric_representation=NumericRepresentation.EXACT_FRACTION,
        )


def test_registry_is_closed_and_metric_types_expose_no_scoring_or_weighting_fields():
    assert tuple(MetricId) == (
        MetricId.RQ_COMPLETENESS,
        MetricId.RQ_VERIFIABILITY,
        MetricId.RQ_UNAMBIGUITY,
        MetricId.SPEC_MEAN_COMPLETENESS,
        MetricId.SPEC_MEAN_VERIFIABILITY,
        MetricId.SPEC_MEAN_UNAMBIGUITY,
        MetricId.SPEC_QB_CONSISTENCY,
    )
    field_names = {item.name for item in fields(MetricEntry)}
    assert not field_names & {
        "weight",
        "normalized_value",
        "rounded_value",
        "rank",
        "overall_score",
        "product_quality",
    }


def test_rule_versions_and_immutability_preserve_source_version_policy():
    profile = build_metric_profile(
        _assess(
            _record("R001", 1, ComparatorLabel.LESS_THAN_OR_EQUAL, Decimal("2")),
            _record("R002", 2, ComparatorLabel.GREATER_THAN_OR_EQUAL, Decimal("5")),
        ),
        _context(),
    )
    requirement_rule = profile.entries[0].rule_refs[0]
    qb_rule = profile.entries[-1].rule_refs[0]

    assert requirement_rule.rule_id == "CALC-C-MVP-001"
    assert requirement_rule.explicit_version is None
    assert requirement_rule.version_authority is RuleVersionAuthority.STABLE_RULE_ID_POLICY
    assert qb_rule.rule_id == "QB-CONSISTENCY-001"
    assert qb_rule.explicit_version == "1"
    assert qb_rule.version_authority is RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION
    with pytest.raises(FrozenInstanceError):
        profile.entries[0].value = Fraction(0, 1)


def test_source_status_reference_preserves_the_upstream_status_type():
    assert SourceStatusRef(QbConsistencyState.UNKNOWN) != SourceStatusRef(
        CharacteristicAssessmentState.UNKNOWN
    )


def test_construction_context_is_required_and_not_inferred():
    source = _assess(_unknown_record())
    with pytest.raises(TypeError, match="MetricConstructionContext"):
        build_metric_profile(source, None)
    artifact = ArtifactRef("SPEC-A", "v1")
    with pytest.raises(ValueError, match="context artifact_ref"):
        MetricConstructionContext(
            artifact_ref=artifact,
            assessment_ref=AssessmentRef(
                "ASSESS-A",
                "1",
                ArtifactRef("SPEC-B", "v1"),
            ),
        )

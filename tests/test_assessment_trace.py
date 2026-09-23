"""Binding SRM-10/SRM-11 trace cases using manually built domain values."""

from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from fractions import Fraction

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState,
    CharacteristicId,
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DiagnosticSpan,
    Evidence,
    FeatureDetectionOutcome,
    FeatureId,
    FeatureObservation,
    FindingKind,
    NumericValueComponent,
    QuantitativeConstraintObservation,
    Requirement,
    RequirementAssessmentRecord,
    RequirementExtractionResult,
    RequirementFeatures,
    TraceDecisionCode,
    TraceEffectCode,
    UnitComponent,
    UnitLabel,
    VagueTermOccurrence,
)


SOURCE = (
    "Система повинна швидко обробити запит за 2 секунди та повернути результат "
    "для перевірки оператором."
)
_SWIFT = SOURCE.index("швидко")


def _evidence(evidence_id, feature_id, start, end=None):
    end = start + 1 if end is None else end
    return Evidence(
        evidence_id, "R001", feature_id, SOURCE[start:end], start, end, "TEST-001"
    )


def _diagnostic(code="UNRESOLVED_CANDIDATE", *, start=0):
    return DetectionDiagnostic(
        code,
        "candidate could not be resolved",
        "TEST-001",
        DiagnosticSpan(SOURCE[start:start + 1], start, start + 1),
    )


def _empty(feature_id):
    return (
        FeatureDetectionOutcome(
            feature_id, (), DetectionProcessingStatus.COMPLETE, ()
        ),
        (),
    )


def _unresolved(feature_id, *, start=0):
    return (
        FeatureDetectionOutcome(
            feature_id,
            (),
            DetectionProcessingStatus.INCOMPLETE,
            (_diagnostic(start=start),),
        ),
        (),
    )


def _simple(feature_id, *offsets, incomplete=False):
    evidence = tuple(
        _evidence(f"{feature_id.value}:E{offset}", feature_id, offset)
        for offset in offsets
    )
    observations = tuple(
        FeatureObservation(feature_id, (item.evidence_id,)) for item in evidence
    )
    diagnostics = (_diagnostic(start=max(offsets, default=0) + 1),) if incomplete else ()
    status = (
        DetectionProcessingStatus.INCOMPLETE
        if incomplete
        else DetectionProcessingStatus.COMPLETE
    )
    return FeatureDetectionOutcome(feature_id, observations, status, diagnostics), evidence


def _quantitative(*, incomplete=False):
    value_id = "quantitative_constraint:value"
    unit_id = "quantitative_constraint:unit"
    value_offset = SOURCE.index("2")
    unit_offset = SOURCE.index("секунди")
    observation = QuantitativeConstraintObservation(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        metric=None,
        comparator=None,
        value=NumericValueComponent(Decimal("2"), (value_id,)),
        unit=UnitComponent(UnitLabel.SECOND, (unit_id,)),
        context=None,
        unresolved_components=(),
        evidence_refs=(value_id, unit_id),
    )
    diagnostics = (_diagnostic(start=unit_offset + 1),) if incomplete else ()
    status = (
        DetectionProcessingStatus.INCOMPLETE
        if incomplete
        else DetectionProcessingStatus.COMPLETE
    )
    outcome = FeatureDetectionOutcome(
        FeatureId.QUANTITATIVE_CONSTRAINT,
        (observation,),
        status,
        diagnostics,
    )
    evidence = (
        _evidence(value_id, FeatureId.QUANTITATIVE_CONSTRAINT, value_offset),
        _evidence(unit_id, FeatureId.QUANTITATIVE_CONSTRAINT, unit_offset),
    )
    return outcome, evidence


def _vague(*, incomplete=False, repeated=False):
    offsets = (_SWIFT, _SWIFT) if repeated else (_SWIFT,)
    evidence = tuple(
        _evidence(
            f"vague:E{index}",
            FeatureId.VAGUE_TERM_OCCURRENCE,
            offset,
            offset + len("швидко"),
        )
        for index, offset in enumerate(offsets)
    )
    observations = tuple(
        VagueTermOccurrence(
            FeatureId.VAGUE_TERM_OCCURRENCE,
            "uk_vague_terms_v1",
            "швидко",
            (item.evidence_id,),
        )
        for item in evidence
    )
    diagnostics = (_diagnostic(start=_SWIFT + 1),) if incomplete else ()
    status = (
        DetectionProcessingStatus.INCOMPLETE
        if incomplete
        else DetectionProcessingStatus.COMPLETE
    )
    return (
        FeatureDetectionOutcome(
            FeatureId.VAGUE_TERM_OCCURRENCE, observations, status, diagnostics
        ),
        evidence,
    )


def _result(
    *, condition=None, expected=None, acceptance=None, quantitative=None,
    method=None, vague=None,
):
    families = (
        condition or _empty(FeatureId.CONDITION_CONTEXT),
        expected or _empty(FeatureId.EXPECTED_RESULT),
        acceptance or _empty(FeatureId.ACCEPTANCE_CRITERION),
        quantitative or _empty(FeatureId.QUANTITATIVE_CONSTRAINT),
        method or _empty(FeatureId.VERIFICATION_METHOD),
        vague or _empty(FeatureId.VAGUE_TERM_OCCURRENCE),
    )
    features = RequirementFeatures(*(outcome for outcome, _ in families))
    evidence = tuple(item for _, items in families for item in items)
    return RequirementExtractionResult(
        Requirement("R001", 1, SOURCE), features, evidence
    )


def _record(result):
    return RequirementQualityAssessor().assess_record(result)


def _trace(record, characteristic_id):
    return next(
        item for item in record.trace.characteristics
        if item.characteristic_id is characteristic_id
    )


def _effects(characteristic_trace):
    return tuple(item.effect_code for item in characteristic_trace.inputs)


# -- Seven binding cases from model-spec.md Section 7.17.8 -------------------


def test_positive_reference_case():
    record = _record(_result(
        condition=_simple(FeatureId.CONDITION_CONTEXT, 0),
        expected=_simple(FeatureId.EXPECTED_RESULT, 1),
        acceptance=_simple(FeatureId.ACCEPTANCE_CRITERION, 2),
    ))

    assert tuple(item.characteristic_id for item in record.trace.characteristics) == tuple(
        CharacteristicId
    )
    assert record.quality_profile.completeness.value == 1
    assert _effects(_trace(record, CharacteristicId.COMPLETENESS)) == (
        TraceEffectCode.C_PRESENT_1,
        TraceEffectCode.C_PRESENT_1,
        TraceEffectCode.C_PRESENT_1,
    )
    assert record.quality_profile.verifiability.value == 1
    assert _trace(record, CharacteristicId.VERIFIABILITY).decision_code is (
        TraceDecisionCode.V_FULL_ACCEPTANCE_TIER
    )
    assert record.quality_profile.unambiguity.value == 1
    assert _effects(_trace(record, CharacteristicId.UNAMBIGUITY)) == (
        TraceEffectCode.U_COMPLETED_SIGNAL_ABSENCE,
    )


def test_completed_absence_reference_case_has_no_fake_evidence():
    record = _record(_result())

    assert record.extraction_result.evidence == ()
    assert tuple(item.value for item in (
        record.quality_profile.completeness,
        record.quality_profile.verifiability,
        record.quality_profile.unambiguity,
    )) == (Fraction(0), Fraction(0), Fraction(1))
    assert _effects(_trace(record, CharacteristicId.COMPLETENESS)) == (
        TraceEffectCode.C_COMPLETED_ABSENCE_0,
    ) * 3
    assert _effects(_trace(record, CharacteristicId.VERIFIABILITY)) == (
        TraceEffectCode.V_COMPLETED_ABSENCE,
    ) * 3
    assert all(
        not item.observation_indexes and not item.diagnostic_indexes
        for trace in record.trace.characteristics for item in trace.inputs
    )


def test_unresolved_reference_case_preserves_diagnostic_not_evidence():
    record = _record(_result(method=_unresolved(FeatureId.VERIFICATION_METHOD)))
    verifiability = _trace(record, CharacteristicId.VERIFIABILITY)

    assert record.quality_profile.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert record.quality_profile.verifiability.value is None
    assert verifiability.decision_code is TraceDecisionCode.V_MATERIAL_INPUT_UNRESOLVED
    assert verifiability.inputs[2].effect_code is TraceEffectCode.V_UNRESOLVED_MATERIAL
    assert verifiability.inputs[2].diagnostic_indexes == (0,)
    assert verifiability.inputs[2].observation_indexes == ()
    assert record.extraction_result.evidence == ()
    assert record.extraction_result.features.verification_methods.diagnostics[0].candidate_span


def test_signal_reference_case_has_one_to_one_finding_and_evidence_provenance():
    record = _record(_result(vague=_vague()))
    unambiguity = _trace(record, CharacteristicId.UNAMBIGUITY)
    finding = record.quality_profile.unambiguity.findings[0]
    occurrence = record.extraction_result.features.vague_term_occurrences.observations[0]

    assert record.quality_profile.unambiguity.value == Fraction(1, 2)
    assert unambiguity.decision_code is TraceDecisionCode.U_SUPPORTED_SIGNAL_TIER
    assert unambiguity.inputs[0].observation_indexes == (0,)
    assert unambiguity.finding_refs == (finding.finding_id,)
    assert finding.kind is FindingKind.SIGNAL
    assert finding.code == "VAGUE_TERM_SIGNAL"
    assert finding.rule_id == "FIND-U-VAGUE-001"
    assert finding.evidence_refs == occurrence.evidence_refs
    evidence = record.extraction_result.evidence[0]
    assert SOURCE[evidence.start_offset:evidence.end_offset] == evidence.text == "швидко"


def test_v1_same_family_mixed_reference_case():
    record = _record(_result(
        acceptance=_simple(FeatureId.ACCEPTANCE_CRITERION, 2),
        quantitative=_quantitative(incomplete=True),
    ))
    trace = _trace(record, CharacteristicId.VERIFIABILITY)

    assert record.quality_profile.verifiability.value == 1
    assert trace.decision_code is TraceDecisionCode.V_FULL_ACCEPTANCE_TIER
    assert _effects(trace) == (
        TraceEffectCode.V_SELECTS_FULL_TIER,
        TraceEffectCode.V_PRESENT_NONSELECTING,
        TraceEffectCode.V_COMPLETED_ABSENCE,
    )
    assert trace.inputs[1].observation_indexes == (0,)
    assert trace.inputs[1].diagnostic_indexes == (0,)


def test_v3_unresolved_lower_sibling_reference_case():
    record = _record(_result(
        quantitative=_quantitative(),
        method=_unresolved(FeatureId.VERIFICATION_METHOD),
    ))
    trace = _trace(record, CharacteristicId.VERIFIABILITY)

    assert record.quality_profile.verifiability.value == Fraction(1, 2)
    assert trace.decision_code is TraceDecisionCode.V_PARTIAL_LOWER_TIER
    assert _effects(trace) == (
        TraceEffectCode.V_COMPLETED_ABSENCE,
        TraceEffectCode.V_SELECTS_LOWER_TIER,
        TraceEffectCode.V_UNRESOLVED_NON_MATERIAL,
    )
    assert trace.inputs[2].diagnostic_indexes == (0,)


def test_v4_provisional_lower_evidence_reference_case():
    record = _record(_result(
        acceptance=_unresolved(FeatureId.ACCEPTANCE_CRITERION),
        quantitative=_quantitative(),
    ))
    trace = _trace(record, CharacteristicId.VERIFIABILITY)

    assert record.quality_profile.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert record.quality_profile.verifiability.value is None
    assert trace.decision_code is TraceDecisionCode.V_MATERIAL_INPUT_UNRESOLVED
    assert _effects(trace) == (
        TraceEffectCode.V_UNRESOLVED_MATERIAL,
        TraceEffectCode.V_PRESENT_NONSELECTING,
        TraceEffectCode.V_COMPLETED_ABSENCE,
    )
    assert trace.inputs[1].observation_indexes == (0,)


# -- Joint validation and additional required behavior -----------------------


def test_domain_structures_are_immutable_and_use_bounded_coverage_profile():
    record = _record(_result())
    assert record.trace.coverage_profile_id == "MVP-V0.1-BOUNDED-CVU-001"
    with pytest.raises(FrozenInstanceError):
        record.trace.requirement_id = "changed"


def test_invalid_tuple_index_is_rejected_by_joint_validation():
    record = _record(_result(condition=_simple(FeatureId.CONDITION_CONTEXT, 0)))
    c_trace = record.trace.characteristics[0]
    invalid_input = replace(c_trace.inputs[0], observation_indexes=(1,))
    invalid_c = replace(c_trace, inputs=(invalid_input, *c_trace.inputs[1:]))
    invalid_trace = replace(
        record.trace,
        characteristics=(invalid_c, *record.trace.characteristics[1:]),
    )

    with pytest.raises(ValueError, match="observation indexes"):
        RequirementAssessmentRecord(
            record.extraction_result, record.quality_profile, invalid_trace
        )

    unresolved_record = _record(
        _result(method=_unresolved(FeatureId.VERIFICATION_METHOD))
    )
    v_trace = unresolved_record.trace.characteristics[1]
    invalid_method = replace(v_trace.inputs[2], diagnostic_indexes=(1,))
    invalid_v = replace(v_trace, inputs=(*v_trace.inputs[:2], invalid_method))
    invalid_trace = replace(
        unresolved_record.trace,
        characteristics=(
            unresolved_record.trace.characteristics[0],
            invalid_v,
            unresolved_record.trace.characteristics[2],
        ),
    )
    with pytest.raises(ValueError, match="diagnostic indexes"):
        RequirementAssessmentRecord(
            unresolved_record.extraction_result,
            unresolved_record.quality_profile,
            invalid_trace,
        )


def test_wrong_and_reordered_family_reference_is_rejected():
    record = _record(_result())
    c_trace = record.trace.characteristics[0]
    wrong_input = replace(c_trace.inputs[0], feature_id=FeatureId.EXPECTED_RESULT)
    invalid_c = replace(c_trace, inputs=(wrong_input, *c_trace.inputs[1:]))
    invalid_trace = replace(
        record.trace,
        characteristics=(invalid_c, *record.trace.characteristics[1:]),
    )

    with pytest.raises(ValueError, match="required feature families"):
        RequirementAssessmentRecord(
            record.extraction_result, record.quality_profile, invalid_trace
        )


def test_mismatched_requirement_profile_and_trace_are_rejected():
    record = _record(_result())
    with pytest.raises(ValueError, match="requirement_id"):
        RequirementAssessmentRecord(
            record.extraction_result,
            record.quality_profile,
            replace(record.trace, requirement_id="R999"),
        )

    wrong_c = replace(record.quality_profile.completeness, value=Fraction(1, 3))
    wrong_profile = replace(record.quality_profile, completeness=wrong_c)
    with pytest.raises(ValueError, match="quality profile"):
        RequirementAssessmentRecord(record.extraction_result, wrong_profile, record.trace)

    wrong_trace_c = replace(
        record.trace.characteristics[0],
        decision_code=TraceDecisionCode.C_REQUIRED_INPUT_UNRESOLVED,
    )
    wrong_trace = replace(
        record.trace,
        characteristics=(wrong_trace_c, *record.trace.characteristics[1:]),
    )
    with pytest.raises(ValueError, match="decision_code"):
        RequirementAssessmentRecord(record.extraction_result, record.quality_profile, wrong_trace)


def test_repeated_observations_are_all_referenced_without_extra_weight():
    record = _record(_result(
        condition=_simple(FeatureId.CONDITION_CONTEXT, 0, 1),
        expected=_simple(FeatureId.EXPECTED_RESULT, 2),
        acceptance=_simple(FeatureId.ACCEPTANCE_CRITERION, 3, 4),
        vague=_vague(repeated=True),
    ))

    assert record.quality_profile.completeness.value == 1
    assert record.quality_profile.verifiability.value == 1
    assert record.quality_profile.unambiguity.value == Fraction(1, 2)
    assert _trace(
        record, CharacteristicId.COMPLETENESS
    ).inputs[0].observation_indexes == (0, 1)
    assert _trace(
        record, CharacteristicId.VERIFIABILITY
    ).inputs[0].observation_indexes == (0, 1)
    assert len(record.quality_profile.unambiguity.findings) == 2


def test_mixed_accepted_and_unresolved_c_v_u_states_are_preserved():
    record = _record(_result(
        condition=_simple(FeatureId.CONDITION_CONTEXT, 0, incomplete=True),
        expected=_simple(FeatureId.EXPECTED_RESULT, 2),
        acceptance=_simple(FeatureId.ACCEPTANCE_CRITERION, 3, incomplete=True),
        quantitative=_quantitative(incomplete=True),
        method=_unresolved(FeatureId.VERIFICATION_METHOD),
        vague=_vague(incomplete=True),
    ))

    assert (
        record.quality_profile.completeness.state
        is CharacteristicAssessmentState.UNKNOWN
    )
    assert _trace(record, CharacteristicId.COMPLETENESS).inputs[0].effect_code is (
        TraceEffectCode.C_REQUIRED_UNRESOLVED
    )
    assert record.quality_profile.verifiability.value == 1
    assert _effects(_trace(record, CharacteristicId.VERIFIABILITY)) == (
        TraceEffectCode.V_SELECTS_FULL_TIER,
        TraceEffectCode.V_PRESENT_NONSELECTING,
        TraceEffectCode.V_UNRESOLVED_NON_MATERIAL,
    )
    assert record.quality_profile.unambiguity.value == Fraction(1, 2)
    assert _trace(
        record, CharacteristicId.UNAMBIGUITY
    ).inputs[0].diagnostic_indexes == (0,)


def test_non_signal_finding_mapping_is_rejected():
    record = _record(_result(vague=_vague()))
    finding = record.quality_profile.unambiguity.findings[0]
    wrong_finding = replace(
        finding, kind=FindingKind.QUALITY_PROBLEM, criterion_id="vague_term_occurrence"
    )
    wrong_u = replace(record.quality_profile.unambiguity, findings=(wrong_finding,))
    wrong_profile = replace(record.quality_profile, unambiguity=wrong_u)

    with pytest.raises(ValueError, match="Finding provenance"):
        RequirementAssessmentRecord(record.extraction_result, wrong_profile, record.trace)


def test_diagnostic_candidate_span_must_round_trip_without_becoming_evidence():
    bad_diagnostic = DetectionDiagnostic(
        "UNRESOLVED_CANDIDATE",
        "candidate could not be resolved",
        "TEST-001",
        DiagnosticSpan("X", 0, 1),
    )
    bad_method = (
        FeatureDetectionOutcome(
            FeatureId.VERIFICATION_METHOD,
            (),
            DetectionProcessingStatus.INCOMPLETE,
            (bad_diagnostic,),
        ),
        (),
    )
    result = _result(method=bad_method)
    profile = RequirementQualityAssessor().assess(result)

    with pytest.raises(ValueError, match="candidate span"):
        from requirements_quality_assessment.assessment_trace import (
            RequirementAssessmentTraceBuilder,
        )
        RequirementAssessmentTraceBuilder().build(result, profile)


def test_trace_order_and_assessor_results_are_deterministic_and_backward_compatible():
    result = _result(
        condition=_simple(FeatureId.CONDITION_CONTEXT, 0),
        expected=_simple(FeatureId.EXPECTED_RESULT, 1),
        acceptance=_simple(FeatureId.ACCEPTANCE_CRITERION, 2),
        vague=_vague(),
    )
    assessor = RequirementQualityAssessor()
    original_profile = assessor.assess(result)
    first = assessor.assess_record(result)
    second = assessor.assess_record(result)

    assert first == second
    assert first.quality_profile == original_profile
    assert tuple(item.characteristic_id for item in first.trace.characteristics) == (
        CharacteristicId.COMPLETENESS,
        CharacteristicId.VERIFIABILITY,
        CharacteristicId.UNAMBIGUITY,
    )
    assert tuple(item.feature_id for item in first.trace.characteristics[1].inputs) == (
        FeatureId.ACCEPTANCE_CRITERION,
        FeatureId.QUANTITATIVE_CONSTRAINT,
        FeatureId.VERIFICATION_METHOD,
    )

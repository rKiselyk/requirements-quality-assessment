"""Focused SRM-12 explainable record-reporting boundary tests."""

from decimal import Decimal

import pytest

from requirements_quality_assessment.aggregator import SpecificationQualityAggregator
from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState,
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DiagnosticSpan,
    Evidence,
    FeatureDetectionOutcome,
    FeatureId,
    FeatureObservation,
    NumericValueComponent,
    QuantitativeConstraintObservation,
    Requirement,
    RequirementExtractionResult,
    RequirementFeatures,
    TraceEffectCode,
    UnitComponent,
    UnitLabel,
    VagueTermOccurrence,
)
from requirements_quality_assessment.reporter import ConsoleReporter


SOURCE = "Якщо система працює, вона повинна швидко відповісти за 2 с тестом."


def _evidence(evidence_id: str, feature_id: FeatureId, literal: str) -> Evidence:
    start = SOURCE.index(literal)
    return Evidence(
        evidence_id,
        "R001",
        feature_id,
        literal,
        start,
        start + len(literal),
        f"DET-{feature_id.value}",
    )


def _diagnostic(feature_id: FeatureId, literal: str = "тестом") -> DetectionDiagnostic:
    start = SOURCE.index(literal)
    return DetectionDiagnostic(
        "UNRESOLVED_CANDIDATE",
        f"{feature_id.value} candidate remains unresolved",
        f"DET-{feature_id.value}",
        DiagnosticSpan(literal, start, start + len(literal)),
    )


def _empty(feature_id: FeatureId):
    return FeatureDetectionOutcome(
        feature_id, (), DetectionProcessingStatus.COMPLETE, ()
    ), ()


def _unresolved(feature_id: FeatureId, literal: str = "тестом"):
    return FeatureDetectionOutcome(
        feature_id,
        (),
        DetectionProcessingStatus.INCOMPLETE,
        (_diagnostic(feature_id, literal),),
    ), ()


def _simple(feature_id: FeatureId, literal: str, *, incomplete: bool = False):
    evidence = _evidence(f"{feature_id.value}:E001", feature_id, literal)
    diagnostics = (_diagnostic(feature_id),) if incomplete else ()
    status = (
        DetectionProcessingStatus.INCOMPLETE
        if incomplete
        else DetectionProcessingStatus.COMPLETE
    )
    return (
        FeatureDetectionOutcome(
            feature_id,
            (FeatureObservation(feature_id, (evidence.evidence_id,)),),
            status,
            diagnostics,
        ),
        (evidence,),
    )


def _quantitative(*, incomplete: bool = False):
    value_evidence = _evidence(
        "quantitative_constraint:E_VALUE", FeatureId.QUANTITATIVE_CONSTRAINT, "2"
    )
    unit_start = SOURCE.index("2 с") + 2
    unit_evidence = Evidence(
        "quantitative_constraint:E_UNIT",
        "R001",
        FeatureId.QUANTITATIVE_CONSTRAINT,
        "с",
        unit_start,
        unit_start + 1,
        "DET-quantitative_constraint",
    )
    references = (value_evidence.evidence_id, unit_evidence.evidence_id)
    observation = QuantitativeConstraintObservation(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        metric=None,
        comparator=None,
        value=NumericValueComponent(Decimal("2"), (value_evidence.evidence_id,)),
        unit=UnitComponent(UnitLabel.SECOND, (unit_evidence.evidence_id,)),
        context=None,
        unresolved_components=(),
        evidence_refs=references,
    )
    diagnostics = (_diagnostic(FeatureId.QUANTITATIVE_CONSTRAINT),) if incomplete else ()
    status = (
        DetectionProcessingStatus.INCOMPLETE
        if incomplete
        else DetectionProcessingStatus.COMPLETE
    )
    return (
        FeatureDetectionOutcome(
            FeatureId.QUANTITATIVE_CONSTRAINT,
            (observation,),
            status,
            diagnostics,
        ),
        (value_evidence, unit_evidence),
    )


def _vague():
    evidence = _evidence(
        "vague_term_occurrence:E001", FeatureId.VAGUE_TERM_OCCURRENCE, "швидко"
    )
    observation = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE,
        "uk_vague_terms_v1",
        "швидко",
        (evidence.evidence_id,),
    )
    return FeatureDetectionOutcome(
        FeatureId.VAGUE_TERM_OCCURRENCE,
        (observation,),
        DetectionProcessingStatus.COMPLETE,
        (),
    ), (evidence,)


def _record(
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
    result = RequirementExtractionResult(
        Requirement("R001", 1, SOURCE),
        RequirementFeatures(*(outcome for outcome, _ in families)),
        tuple(evidence for _, items in families for evidence in items),
    )
    return RequirementQualityAssessor().assess_record(result)


def _render(record) -> str:
    specification = SpecificationQualityAggregator().aggregate(
        (record.quality_profile,)
    )
    return ConsoleReporter().render((record,), specification)


def test_positive_case_renders_exact_evidence_and_approved_order() -> None:
    record = _record(
        condition=_simple(FeatureId.CONDITION_CONTEXT, "Якщо"),
        expected=_simple(FeatureId.EXPECTED_RESULT, "відповісти"),
        acceptance=_simple(FeatureId.ACCEPTANCE_CRITERION, "тестом"),
    )

    output = _render(record)

    assert "FORMAL RESULT" in output
    assert "HUMAN-READABLE INTERPRETATION" in output
    assert output.index("Completeness:") < output.index("Verifiability:") < output.index("Unambiguity:")
    assert "state: COMPUTED\n  value: 1" in output
    assert "decision_code: C_CRITERION_RATIO_COMPUTED" in output
    assert "effect_code: C_PRESENT_1" in output
    assert "evidence_id: condition_context:E001" in output
    assert "text: Якщо" in output
    assert "range: [0,4)" in output
    assert "feature_id: condition_context" in output
    assert "detector_rule_id: DET-condition_context" in output
    assert "Coverage disclosures (MVP-V0.1-BOUNDED-CVU-001):" in output
    assert "R3 and F1-A are researcher-approved but unimplemented" in output


def test_completed_absence_has_no_fake_evidence() -> None:
    output = _render(_record())

    assert "decision_code: V_COMPLETED_NO_EVIDENCE_TIER" in output
    assert "effect_code: C_COMPLETED_ABSENCE_0" in output
    assert "effect_code: V_COMPLETED_ABSENCE" in output
    assert "effect_code: U_COMPLETED_SIGNAL_ABSENCE" in output
    assert output.count(
        "completed_absence: no accepted observation; no Evidence was created for absence"
    ) == 7
    assert "evidence_id:" not in output
    assert "not universal semantic absence" in output


def test_unknown_diagnostic_candidate_is_distinct_from_accepted_evidence() -> None:
    output = _render(
        _record(method=_unresolved(FeatureId.VERIFICATION_METHOD, "тестом"))
    )

    assert "decision_code: V_MATERIAL_INPUT_UNRESOLVED" in output
    assert "state: UNKNOWN\n  value: UNKNOWN" in output
    assert "effect_code: V_UNRESOLVED_MATERIAL" in output
    assert "unresolved_diagnostics (not accepted Evidence):" in output
    assert "candidate_span (not accepted Evidence):" in output
    assert "text: тестом" in output
    assert f"range: [{SOURCE.index('тестом')},{SOURCE.index('тестом') + len('тестом')})" in output
    assert "evidence_id:" not in output


def test_signal_finding_resolves_source_and_is_never_described_as_a_defect() -> None:
    output = _render(_record(vague=_vague()))

    start = SOURCE.index("швидко")
    assert "decision_code: U_SUPPORTED_SIGNAL_TIER" in output
    assert "kind: SIGNAL" in output
    assert "rule_id: FIND-U-VAGUE-001" in output
    assert "evidence_id: vague_term_occurrence:E001" in output
    assert "text: швидко" in output
    assert f"range: [{start},{start + len('швидко')})" in output
    assert "SIGNAL meaning: a supported indicator only" in output
    assert "not a confirmed ambiguity, defect" in output
    assert "kind: QUALITY_PROBLEM" not in output


@pytest.mark.parametrize(
    ("record", "effects", "required_text", "forbidden_text"),
    (
        (
            _record(
                acceptance=_simple(FeatureId.ACCEPTANCE_CRITERION, "тестом"),
                quantitative=_quantitative(incomplete=True),
            ),
            ("V_SELECTS_FULL_TIER", "V_PRESENT_NONSELECTING", "V_COMPLETED_ABSENCE"),
            "accepted Evidence remains observed while the separate diagnostic candidate remains unresolved",
            "this accepted lower-tier evidence is provisional",
        ),
        (
            _record(
                quantitative=_quantitative(),
                method=_unresolved(FeatureId.VERIFICATION_METHOD),
            ),
            ("V_COMPLETED_ABSENCE", "V_SELECTS_LOWER_TIER", "V_UNRESOLVED_NON_MATERIAL"),
            "accepted lower-tier evidence fixes the computed V=1/2 class",
            "this accepted lower-tier evidence is provisional",
        ),
        (
            _record(
                acceptance=_unresolved(FeatureId.ACCEPTANCE_CRITERION),
                quantitative=_quantitative(),
            ),
            ("V_UNRESOLVED_MATERIAL", "V_PRESENT_NONSELECTING", "V_COMPLETED_ABSENCE"),
            "this accepted lower-tier evidence is provisional",
            "selects the lower tier",
        ),
    ),
    ids=("V1-same-family-mixed", "V3-unresolved-lower-sibling", "V4-provisional"),
)
def test_v_materiality_and_provisional_evidence_are_explicit(
    record, effects, required_text, forbidden_text
) -> None:
    output = _render(record)
    verifiability = output[
        output.index("Verifiability:"):output.index("Unambiguity:")
    ]

    positions = [verifiability.index(f"effect_code: {effect}") for effect in effects]
    assert positions == sorted(positions)
    assert required_text in output
    assert forbidden_text not in verifiability


def test_v4_unresolved_method_is_non_material_without_fixing_final_class() -> None:
    record = _record(
        acceptance=_unresolved(FeatureId.ACCEPTANCE_CRITERION),
        quantitative=_quantitative(),
        method=_unresolved(FeatureId.VERIFICATION_METHOD),
    )

    assessment = record.quality_profile.verifiability
    method_input = record.trace.characteristics[1].inputs[2]
    output = _render(record)
    interpretation = output[output.index("HUMAN-READABLE INTERPRETATION"):]

    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None
    assert method_input.effect_code is TraceEffectCode.V_UNRESOLVED_NON_MATERIAL
    assert "accepted lower-tier evidence establishes the provisional lower tier" in interpretation
    assert "final result remains UNKNOWN because unresolved acceptance may change the tier to V=1" in interpretation
    assert "fixes the numeric class" not in interpretation


def test_record_rendering_is_deterministic() -> None:
    record = _record(
        condition=_simple(FeatureId.CONDITION_CONTEXT, "Якщо"),
        vague=_vague(),
    )

    assert _render(record) == _render(record)

"""Issue #9 / MVP-08 CALC-U-MVP-001 Unambiguity calculator tests.

RequirementExtractionResult graphs are built by hand; no FeatureExtractor,
detectors, parser, spaCy, reader, CLI, or reporter involved.
"""

from decimal import Decimal
from fractions import Fraction

import pytest

from requirements_quality_assessment.calculators import UnambiguityCalculator
from requirements_quality_assessment.calculators.unambiguity import (
    FINDING_CODE, FINDING_RULE_ID, RULE_ID,
)
from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState, CharacteristicId, DetectionDiagnostic,
    DetectionProcessingStatus, Evidence, FeatureDetectionOutcome, FeatureId,
    FeatureObservation, Finding, FindingKind, NumericValueComponent,
    QuantitativeConstraintObservation, Requirement, RequirementExtractionResult,
    RequirementFeatures, UnitComponent, UnitLabel, VagueTermOccurrence,
)


SOURCE = (
    "Система повинна швидко обробити запит і надійно зберегти результат, "
    "а також швидко сформувати звіт для подальшого аудиту та повторного "
    "використання у системі."
)

# Real, source-faithful offsets for the approved seed literals used below --
# each Evidence span is the actual matched surface, not an arbitrary slice.
_SWIFT_1 = SOURCE.index("швидко")
_RELIABLE_1 = SOURCE.index("надійно")
_SWIFT_2 = SOURCE.index("швидко", _SWIFT_1 + 1)


def _diagnostic(code="VAGUE_UNRESOLVED_CANDIDATE", explanation="candidate cannot be resolved"):
    return DetectionDiagnostic(code, explanation, "TEST-001")


def _evidence(evidence_id, feature_id, start, end):
    return Evidence(evidence_id, "R001", feature_id, SOURCE[start:end], start, end, "TEST-001")


def _char_evidence(evidence_id, feature_id, offset):
    return _evidence(evidence_id, feature_id, offset, offset + 1)


def _empty_outcome(feature_id):
    return FeatureDetectionOutcome(feature_id, (), DetectionProcessingStatus.COMPLETE, ())


def _not_detected(feature_id):
    return _empty_outcome(feature_id), ()


def _simple_detected(feature_id, offset):
    """A DETECTED simple family (condition/expected/acceptance/verification)."""
    evidence_id = f"{feature_id.value}:E{offset}"
    observation = FeatureObservation(feature_id, (evidence_id,))
    outcome = FeatureDetectionOutcome(feature_id, (observation,), DetectionProcessingStatus.COMPLETE, ())
    return outcome, (_char_evidence(evidence_id, feature_id, offset),)


def _quantitative_detected(value_offset, unit_offset):
    """A DETECTED, domain-valid quantitative constraint observation."""
    value_evidence_id = f"quantitative:V{value_offset}"
    unit_evidence_id = f"quantitative:U{unit_offset}"
    value_component = NumericValueComponent(Decimal("2"), (value_evidence_id,))
    unit_component = UnitComponent(UnitLabel.SECOND, (unit_evidence_id,))
    observation = QuantitativeConstraintObservation(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        metric=None, comparator=None, value=value_component, unit=unit_component,
        context=None, unresolved_components=(),
        evidence_refs=(value_evidence_id, unit_evidence_id),
    )
    outcome = FeatureDetectionOutcome(
        FeatureId.QUANTITATIVE_CONSTRAINT, (observation,), DetectionProcessingStatus.COMPLETE, (),
    )
    evidence = (
        _char_evidence(value_evidence_id, FeatureId.QUANTITATIVE_CONSTRAINT, value_offset),
        _char_evidence(unit_evidence_id, FeatureId.QUANTITATIVE_CONSTRAINT, unit_offset),
    )
    return outcome, evidence


def _vague_occurrence(literal, start, tag):
    """One accepted VagueTermOccurrence plus a source-faithful matching Evidence.

    The Evidence span is the actual matched surface (SOURCE[start:end] == the
    literal), mirroring how the production vague-term detector anchors
    Evidence to the real matched text rather than an arbitrary character.
    """
    end = start + len(literal)
    evidence_id = f"vague:{tag}"
    occurrence = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE, "uk_vague_terms_v1", literal, (evidence_id,),
    )
    evidence = _evidence(evidence_id, FeatureId.VAGUE_TERM_OCCURRENCE, start, end)
    return occurrence, evidence


def _vague_detected(*occurrence_specs):
    """COMPLETE processing with one or more accepted occurrences.

    occurrence_specs is a sequence of (literal, start_offset, tag) tuples
    supplied in whatever order the test wants to exercise; the calculator is
    responsible for re-sorting into source order.
    """
    pairs = [_vague_occurrence(literal, start, tag) for literal, start, tag in occurrence_specs]
    observations = tuple(occurrence for occurrence, _ in pairs)
    evidence = tuple(item for _, item in pairs)
    outcome = FeatureDetectionOutcome(
        FeatureId.VAGUE_TERM_OCCURRENCE, observations, DetectionProcessingStatus.COMPLETE, (),
    )
    return outcome, evidence


def _vague_not_detected():
    return _not_detected(FeatureId.VAGUE_TERM_OCCURRENCE)


def _vague_unresolved(*, diagnostics=None):
    diags = diagnostics if diagnostics is not None else (_diagnostic(),)
    return FeatureDetectionOutcome(
        FeatureId.VAGUE_TERM_OCCURRENCE, (), DetectionProcessingStatus.INCOMPLETE, diags,
    ), ()


def _vague_mixed(*occurrence_specs, diagnostics=None):
    """Accepted occurrence(s) present, but processing_status is INCOMPLETE."""
    diags = diagnostics if diagnostics is not None else (_diagnostic(),)
    pairs = [_vague_occurrence(literal, start, tag) for literal, start, tag in occurrence_specs]
    observations = tuple(occurrence for occurrence, _ in pairs)
    evidence = tuple(item for _, item in pairs)
    outcome = FeatureDetectionOutcome(
        FeatureId.VAGUE_TERM_OCCURRENCE, observations, DetectionProcessingStatus.INCOMPLETE, diags,
    )
    return outcome, evidence


def _result(vague, *, condition=None, expected=None, acceptance=None,
            quantitative=None, verification=None):
    """Assemble a RequirementExtractionResult; only `vague` matters to Unambiguity."""
    vague_outcome, vague_evidence = vague
    condition_outcome, condition_evidence = condition or _not_detected(FeatureId.CONDITION_CONTEXT)
    expected_outcome, expected_evidence = expected or _not_detected(FeatureId.EXPECTED_RESULT)
    acceptance_outcome, acceptance_evidence = acceptance or _not_detected(FeatureId.ACCEPTANCE_CRITERION)
    quantitative_outcome, quantitative_evidence = quantitative or _not_detected(FeatureId.QUANTITATIVE_CONSTRAINT)
    verification_outcome, verification_evidence = verification or _not_detected(FeatureId.VERIFICATION_METHOD)

    features = RequirementFeatures(
        condition_outcome, expected_outcome, acceptance_outcome,
        quantitative_outcome, verification_outcome, vague_outcome,
    )
    evidence = (
        condition_evidence + expected_evidence + acceptance_evidence
        + quantitative_evidence + verification_evidence + vague_evidence
    )
    return RequirementExtractionResult(Requirement("R001", 1, SOURCE), features, evidence)


def _calculate(result):
    return UnambiguityCalculator().calculate(result)


def _single_signal_result():
    return _result(_vague_detected(("швидко", _SWIFT_1, "s1")))


def _two_signal_result():
    return _result(_vague_detected(
        ("швидко", _SWIFT_1, "s1"), ("надійно", _RELIABLE_1, "r1"),
    ))


# -- No signal, complete processing -> 1 --------------------------------------

def test_no_accepted_occurrence_complete_processing_yields_one():
    result = _result(_vague_not_detected())
    assessment = _calculate(result)
    assert assessment.characteristic_id is CharacteristicId.UNAMBIGUITY
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 1)
    assert assessment.assessment_rule_id == RULE_ID == "CALC-U-MVP-001"
    assert assessment.findings == ()


def test_no_signal_explanation_disclaims_universal_uniqueness():
    assessment = _calculate(_result(_vague_not_detected()))
    assert "no supported signal" in assessment.explanation
    assert "not universal proof" in assessment.explanation


# -- One or more accepted signals -> 1/2 --------------------------------------

def test_one_accepted_occurrence_yields_half():
    assessment = _calculate(_single_signal_result())
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)
    assert assessment.assessment_rule_id == RULE_ID
    assert len(assessment.findings) == 1


def test_two_accepted_occurrences_yield_half():
    assessment = _calculate(_two_signal_result())
    assert assessment.value == Fraction(1, 2)
    assert len(assessment.findings) == 2


def test_repeated_identical_literal_occurrences_still_yield_half_with_two_findings():
    result = _result(_vague_detected(
        ("швидко", _SWIFT_1, "s1"), ("швидко", _SWIFT_2, "s2"),
    ))
    assessment = _calculate(result)
    assert assessment.value == Fraction(1, 2)
    assert len(assessment.findings) == 2
    assert assessment.findings[0].finding_id != assessment.findings[1].finding_id


# -- Finding field checks ------------------------------------------------------

def test_finding_requirement_id_matches_requirement():
    assessment = _calculate(_single_signal_result())
    assert assessment.findings[0].requirement_id == "R001"


def test_finding_characteristic_id_is_unambiguity():
    assessment = _calculate(_single_signal_result())
    assert assessment.findings[0].characteristic_id is CharacteristicId.UNAMBIGUITY


def test_finding_kind_is_signal():
    assessment = _calculate(_single_signal_result())
    assert assessment.findings[0].kind is FindingKind.SIGNAL


def test_finding_code_is_vague_term_signal():
    assessment = _calculate(_single_signal_result())
    assert assessment.findings[0].code == FINDING_CODE == "VAGUE_TERM_SIGNAL"


def test_finding_rule_id_is_find_u_vague_001():
    assessment = _calculate(_single_signal_result())
    assert assessment.findings[0].rule_id == FINDING_RULE_ID == "FIND-U-VAGUE-001"


def test_finding_criterion_id_is_none():
    assessment = _calculate(_single_signal_result())
    assert assessment.findings[0].criterion_id is None


def test_finding_evidence_refs_match_occurrence_refs_exactly():
    result = _single_signal_result()
    occurrence = result.features.vague_term_occurrences.observations[0]
    assessment = _calculate(result)
    # Semantic equality (same values, same order) is the contract requirement;
    # object identity of the tuple is an implementation detail, not asserted.
    assert assessment.findings[0].evidence_refs == occurrence.evidence_refs


def test_finding_explanation_names_matched_literal_and_disclaims_confirmed_ambiguity():
    assessment = _calculate(_single_signal_result())
    explanation = assessment.findings[0].explanation
    assert "швидко" in explanation
    assert "not a confirmed ambiguity" in explanation


# -- Ordering and finding-ID determinism --------------------------------------

def test_findings_ordered_by_evidence_start_offset_not_observation_order():
    # Deliberately reversed vs. source order: "надійно" occurs after "швидко".
    result = _result(_vague_detected(
        ("надійно", _RELIABLE_1, "r1"), ("швидко", _SWIFT_1, "s1"),
    ))
    assessment = _calculate(result)
    assert assessment.findings[0].evidence_refs == ("vague:s1",)
    assert assessment.findings[1].evidence_refs == ("vague:r1",)


def test_finding_ids_assigned_in_source_order_not_input_order():
    result = _result(_vague_detected(
        ("надійно", _RELIABLE_1, "r1"), ("швидко", _SWIFT_1, "s1"),
    ))
    assessment = _calculate(result)
    assert assessment.findings[0].finding_id == f"{FINDING_RULE_ID}:F001"
    assert assessment.findings[1].finding_id == f"{FINDING_RULE_ID}:F002"


def test_finding_ids_are_unique_within_assessment():
    result = _result(_vague_detected(
        ("швидко", _SWIFT_1, "s1"), ("надійно", _RELIABLE_1, "r1"), ("швидко", _SWIFT_2, "s2"),
    ))
    assessment = _calculate(result)
    ids = [finding.finding_id for finding in assessment.findings]
    assert len(ids) == len(set(ids)) == 3


def test_finding_ids_are_stable_across_repeated_calculate_calls():
    result = _two_signal_result()
    first = _calculate(result)
    second = _calculate(result)
    assert [f.finding_id for f in first.findings] == [f.finding_id for f in second.findings]
    assert [f.evidence_refs for f in first.findings] == [f.evidence_refs for f in second.findings]


def test_ties_at_same_offset_break_by_original_observation_order():
    """A synthetic tie manually constructed per the Section 7.16.5 tie-break
    clause: two accepted occurrences whose referenced Evidence resolves to the
    identical start_offset (not a realistic detector output, since the
    approved longest-overlap policy prevents this in practice) -- original
    observation order must be preserved as the deterministic tie-breaker."""
    occurrence_a = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE, "uk_vague_terms_v1", "швидко", ("vague:tie-a",),
    )
    occurrence_b = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE, "uk_vague_terms_v1", "швидко", ("vague:tie-b",),
    )
    evidence_a = _evidence("vague:tie-a", FeatureId.VAGUE_TERM_OCCURRENCE, _SWIFT_1, _SWIFT_1 + len("швидко"))
    evidence_b = _evidence("vague:tie-b", FeatureId.VAGUE_TERM_OCCURRENCE, _SWIFT_1, _SWIFT_1 + len("швидко"))
    outcome = FeatureDetectionOutcome(
        FeatureId.VAGUE_TERM_OCCURRENCE, (occurrence_a, occurrence_b),
        DetectionProcessingStatus.COMPLETE, (),
    )
    result = _result((outcome, (evidence_a, evidence_b)))
    assessment = _calculate(result)
    assert assessment.findings[0].evidence_refs == ("vague:tie-a",)
    assert assessment.findings[1].evidence_refs == ("vague:tie-b",)
    assert assessment.findings[0].finding_id == f"{FINDING_RULE_ID}:F001"
    assert assessment.findings[1].finding_id == f"{FINDING_RULE_ID}:F002"


# -- No signal, incomplete processing -> UNKNOWN ------------------------------

def test_no_accepted_occurrence_incomplete_processing_yields_unknown():
    result = _result(_vague_unresolved())
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None
    assert assessment.assessment_rule_id is None
    assert assessment.findings == ()


def test_unknown_explanation_includes_diagnostic_code_and_explanation():
    result = _result(_vague_unresolved(diagnostics=(
        DetectionDiagnostic("VAGUE_UNRESOLVED_CANDIDATE", "candidate span ambiguous", "UK-VAGUE-001"),
    )))
    assessment = _calculate(result)
    assert "VAGUE_UNRESOLVED_CANDIDATE" in assessment.explanation
    assert "candidate span ambiguous" in assessment.explanation


def test_unknown_explanation_states_resolution_could_move_class_from_one_to_half():
    assessment = _calculate(_result(_vague_unresolved()))
    assert "from 1 to 1/2" in assessment.explanation


# -- Mixed accepted + INCOMPLETE regression -----------------------------------

def test_accepted_occurrence_with_incomplete_processing_still_yields_half_not_unknown():
    result = _result(_vague_mixed(("швидко", _SWIFT_1, "s1")))
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)
    assert assessment.assessment_rule_id == RULE_ID
    assert len(assessment.findings) == 1


def test_mixed_explanation_reports_incomplete_processing_without_changing_class():
    result = _result(_vague_mixed(("швидко", _SWIFT_1, "s1")))
    assessment = _calculate(result)
    assert "incomplete" in assessment.explanation
    assert "cannot change the class below 1/2" in assessment.explanation


def test_multiple_accepted_signals_plus_incomplete_still_yields_half():
    result = _result(_vague_mixed(
        ("швидко", _SWIFT_1, "s1"), ("надійно", _RELIABLE_1, "r1"),
    ))
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)
    assert len(assessment.findings) == 2


# -- Immutability, findings, and value-type guarantees ------------------------

def test_accepted_observations_and_evidence_are_not_mutated():
    mixed = _vague_mixed(("швидко", _SWIFT_1, "s1"))
    mixed_outcome, mixed_evidence = mixed
    result = _result(mixed)
    features_before = result.features
    evidence_before = result.evidence
    _calculate(result)
    assert result.features is features_before
    assert result.evidence is evidence_before
    assert result.features.vague_term_occurrences.observations == mixed_outcome.observations
    assert result.evidence == mixed_evidence


def test_value_is_always_fraction_or_none_never_float_or_decimal():
    one = _calculate(_result(_vague_not_detected()))
    assert type(one.value) is Fraction

    half = _calculate(_two_signal_result())
    assert type(half.value) is Fraction

    unknown = _calculate(_result(_vague_unresolved()))
    assert unknown.value is None


@pytest.mark.parametrize("build", [
    lambda: _result(_vague_not_detected()),
    lambda: _two_signal_result(),
    lambda: _result(_vague_mixed(("швидко", _SWIFT_1, "s1"))),
], ids=["one", "half", "mixed_half"])
def test_value_is_never_zero(build):
    assessment = _calculate(build())
    assert assessment.value != Fraction(0, 1)


def test_unknown_value_is_none_not_zero():
    assessment = _calculate(_result(_vague_unresolved()))
    assert assessment.value is None


@pytest.mark.parametrize("build", [
    lambda: _two_signal_result(),
    lambda: _result(_vague_mixed(("швидко", _SWIFT_1, "s1"))),
], ids=["complete_signals", "mixed_signals"])
def test_no_finding_is_ever_quality_problem(build):
    assessment = _calculate(build())
    assert assessment.findings
    assert all(finding.kind is FindingKind.SIGNAL for finding in assessment.findings)


def test_complete_no_signal_result_has_empty_findings():
    assessment = _calculate(_result(_vague_not_detected()))
    assert assessment.findings == ()


# -- Independence from all five irrelevant feature families -------------------

def test_irrelevant_families_do_not_affect_unambiguity_at_value_one():
    baseline = _result(_vague_not_detected())
    populated = _result(
        _vague_not_detected(),
        condition=_simple_detected(FeatureId.CONDITION_CONTEXT, 0),
        expected=_simple_detected(FeatureId.EXPECTED_RESULT, 1),
        acceptance=_simple_detected(FeatureId.ACCEPTANCE_CRITERION, 2),
        verification=_simple_detected(FeatureId.VERIFICATION_METHOD, 3),
        quantitative=_quantitative_detected(4, 5),
    )
    baseline_assessment = _calculate(baseline)
    populated_assessment = _calculate(populated)
    assert baseline_assessment.value == populated_assessment.value == Fraction(1, 1)
    assert baseline_assessment.state is populated_assessment.state is CharacteristicAssessmentState.COMPUTED


def test_irrelevant_families_do_not_affect_unambiguity_at_value_half():
    baseline = _two_signal_result()
    populated = _result(
        _vague_detected(("швидко", _SWIFT_1, "s1"), ("надійно", _RELIABLE_1, "r1")),
        condition=_simple_detected(FeatureId.CONDITION_CONTEXT, 0),
        expected=_simple_detected(FeatureId.EXPECTED_RESULT, 1),
        acceptance=_simple_detected(FeatureId.ACCEPTANCE_CRITERION, 2),
        verification=_simple_detected(FeatureId.VERIFICATION_METHOD, 3),
        quantitative=_quantitative_detected(4, 5),
    )
    baseline_assessment = _calculate(baseline)
    populated_assessment = _calculate(populated)
    assert baseline_assessment.value == populated_assessment.value == Fraction(1, 2)
    assert len(baseline_assessment.findings) == len(populated_assessment.findings) == 2


# -- Binding characteristic-layer cases (model-spec Section 7.16.8) ----------

def test_binding_case_a_unambiguity_is_one():
    """Case A: no vague-term signal under the seed matcher, complete scan
    -> U = 1."""
    assessment = _calculate(_result(_vague_not_detected()))
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 1)


def test_binding_case_b_unambiguity_is_half_with_one_signal():
    """Case B: the accepted "швидко" occurrence creates exactly one
    VAGUE_TERM_SIGNAL finding -> U = 1/2."""
    assessment = _calculate(_single_signal_result())
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)
    assert len(assessment.findings) == 1
    assert assessment.findings[0].code == "VAGUE_TERM_SIGNAL"


def test_binding_case_c_unambiguity_is_one():
    """Case C: no vague-term signal under the seed matcher, complete scan
    -> U = 1."""
    assessment = _calculate(_result(_vague_not_detected()))
    assert assessment.value == Fraction(1, 1)


def test_binding_case_d_unambiguity_is_one_independent_of_verifiability_unknown():
    """Case D: Verifiability is UNKNOWN due to an unresolved verification-method
    candidate, but Unambiguity depends only on vague_term_occurrences and is
    unaffected -> U = 1."""
    result = _result(
        _vague_not_detected(),
        verification=(
            FeatureDetectionOutcome(
                FeatureId.VERIFICATION_METHOD, (), DetectionProcessingStatus.INCOMPLETE,
                (DetectionDiagnostic(
                    "VERIFY_UNRESOLVED_CANDIDATE",
                    "candidate is neither a present nor an absent method", "VERIFY-UK-001",
                ),),
            ),
            (),
        ),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 1)


def test_binding_case_e_unambiguity_is_one():
    """Case E: every relevant detector complete and NOT_DETECTED, no unresolved
    candidate -> U = 1."""
    assessment = _calculate(_result(_vague_not_detected()))
    assert assessment.value == Fraction(1, 1)

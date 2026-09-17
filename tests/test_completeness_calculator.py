"""Issue #7 / MVP-06 CALC-C-MVP-001 Completeness calculator tests.

RequirementExtractionResult graphs are built by hand; no FeatureExtractor,
detectors, parser, spaCy, reader, CLI, or reporter involved.
"""

from fractions import Fraction

import pytest

from requirements_quality_assessment.calculators import CompletenessCalculator
from requirements_quality_assessment.calculators.completeness import RULE_ID
from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState, CharacteristicId, DetectionDiagnostic,
    DetectionProcessingStatus, Evidence, FeatureDetectionOutcome, FeatureId,
    FeatureObservation, Requirement, RequirementExtractionResult,
    RequirementFeatures, VagueTermOccurrence,
)


SOURCE = "System shall process the request and return a response with status code value here."

_REQUIRED = (FeatureId.CONDITION_CONTEXT, FeatureId.EXPECTED_RESULT, FeatureId.ACCEPTANCE_CRITERION)


def _diagnostic(code="UNRESOLVED_CANDIDATE", explanation="candidate cannot be resolved"):
    return DetectionDiagnostic(code, explanation, "TEST-001")


def _evidence(evidence_id, feature_id, offset):
    return Evidence(evidence_id, "R001", feature_id, SOURCE[offset:offset + 1],
                    offset, offset + 1, "TEST-001")


def _empty_outcome(feature_id):
    return FeatureDetectionOutcome(feature_id, (), DetectionProcessingStatus.COMPLETE, ())


def _detected(feature_id, offset, *, extra_offsets=()):
    """DETECTED with complete processing; may carry repeated observations."""
    evidence_ids = [f"{feature_id.value}:E{offset}"] + [
        f"{feature_id.value}:E{extra}" for extra in extra_offsets
    ]
    all_offsets = [offset, *extra_offsets]
    observations = tuple(
        FeatureObservation(feature_id, (evidence_id,))
        for evidence_id in evidence_ids
    )
    outcome = FeatureDetectionOutcome(feature_id, observations, DetectionProcessingStatus.COMPLETE, ())
    evidence = tuple(
        _evidence(evidence_id, feature_id, item_offset)
        for evidence_id, item_offset in zip(evidence_ids, all_offsets)
    )
    return outcome, evidence


def _not_detected(feature_id):
    return _empty_outcome(feature_id), ()


def _unresolved(feature_id, *, diagnostics=None):
    """No accepted observation, incomplete processing (clean UNRESOLVED)."""
    diags = diagnostics if diagnostics is not None else (_diagnostic(),)
    return FeatureDetectionOutcome(feature_id, (), DetectionProcessingStatus.INCOMPLETE, diags), ()


def _mixed(feature_id, offset, *, diagnostics=None):
    """Accepted observation present, but processing_status is INCOMPLETE."""
    diags = diagnostics if diagnostics is not None else (_diagnostic(),)
    evidence_id = f"{feature_id.value}:E{offset}"
    observation = FeatureObservation(feature_id, (evidence_id,))
    outcome = FeatureDetectionOutcome(feature_id, (observation,), DetectionProcessingStatus.INCOMPLETE, diags)
    evidence = (_evidence(evidence_id, feature_id, offset),)
    assert outcome.status.value == "DETECTED"  # confirms this is the mixed-state case
    return outcome, evidence


def _result(condition, expected, acceptance, *, verification=None, vague=None, quantitative=None):
    condition_outcome, condition_evidence = condition
    expected_outcome, expected_evidence = expected
    acceptance_outcome, acceptance_evidence = acceptance
    verification_outcome, verification_evidence = verification or _not_detected(FeatureId.VERIFICATION_METHOD)
    vague_outcome, vague_evidence = vague or _not_detected(FeatureId.VAGUE_TERM_OCCURRENCE)
    quantitative_outcome = quantitative or _empty_outcome(FeatureId.QUANTITATIVE_CONSTRAINT)

    features = RequirementFeatures(
        condition_outcome, expected_outcome, acceptance_outcome,
        quantitative_outcome, verification_outcome, vague_outcome,
    )
    evidence = (
        condition_evidence + expected_evidence + acceptance_evidence
        + verification_evidence + vague_evidence
    )
    return RequirementExtractionResult(Requirement("R001", 1, SOURCE), features, evidence)


def _calculate(result):
    return CompletenessCalculator().calculate(result)


def test_all_three_detected_yields_full_score():
    result = _result(_detected(FeatureId.CONDITION_CONTEXT, 0),
                     _detected(FeatureId.EXPECTED_RESULT, 1),
                     _detected(FeatureId.ACCEPTANCE_CRITERION, 2))
    assessment = _calculate(result)
    assert assessment.characteristic_id is CharacteristicId.COMPLETENESS
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 1)
    assert assessment.assessment_rule_id == RULE_ID == "CALC-C-MVP-001"
    assert assessment.findings == ()


def test_exactly_two_detected_yields_two_thirds():
    result = _result(_detected(FeatureId.CONDITION_CONTEXT, 0),
                     _detected(FeatureId.EXPECTED_RESULT, 1),
                     _not_detected(FeatureId.ACCEPTANCE_CRITERION))
    assessment = _calculate(result)
    assert assessment.value == Fraction(2, 3)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED


def test_exactly_one_detected_yields_one_third():
    result = _result(_not_detected(FeatureId.CONDITION_CONTEXT),
                     _detected(FeatureId.EXPECTED_RESULT, 1),
                     _not_detected(FeatureId.ACCEPTANCE_CRITERION))
    assessment = _calculate(result)
    assert assessment.value == Fraction(1, 3)


def test_all_not_detected_with_complete_processing_yields_zero():
    result = _result(_not_detected(FeatureId.CONDITION_CONTEXT),
                     _not_detected(FeatureId.EXPECTED_RESULT),
                     _not_detected(FeatureId.ACCEPTANCE_CRITERION))
    assessment = _calculate(result)
    assert assessment.value == Fraction(0, 1)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.findings == ()


def test_repeated_observations_in_one_family_still_contribute_at_most_one():
    result = _result(
        _detected(FeatureId.CONDITION_CONTEXT, 0, extra_offsets=(3, 4)),
        _detected(FeatureId.EXPECTED_RESULT, 1),
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
    )
    assert len(result.features.condition_contexts.observations) == 3
    assessment = _calculate(result)
    assert assessment.value == Fraction(2, 3)


@pytest.mark.parametrize("unresolved_family", list(_REQUIRED))
def test_each_required_family_individually_unresolved_withholds_result(unresolved_family):
    families = {
        FeatureId.CONDITION_CONTEXT: _detected(FeatureId.CONDITION_CONTEXT, 0),
        FeatureId.EXPECTED_RESULT: _detected(FeatureId.EXPECTED_RESULT, 1),
        FeatureId.ACCEPTANCE_CRITERION: _detected(FeatureId.ACCEPTANCE_CRITERION, 2),
    }
    families[unresolved_family] = _unresolved(
        unresolved_family,
        diagnostics=(DetectionDiagnostic("CANDIDATE_UNRESOLVED",
                                         f"{unresolved_family.value} candidate ambiguous",
                                         "TEST-001"),),
    )
    result = _result(families[FeatureId.CONDITION_CONTEXT],
                     families[FeatureId.EXPECTED_RESULT],
                     families[FeatureId.ACCEPTANCE_CRITERION])
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None
    assert assessment.findings == ()
    assert unresolved_family.value in assessment.explanation
    assert "candidate ambiguous" in assessment.explanation
    assert "CANDIDATE_UNRESOLVED" in assessment.explanation


def test_accepted_observation_plus_incomplete_processing_still_withholds_result():
    mixed_outcome, mixed_evidence = _mixed(
        FeatureId.CONDITION_CONTEXT, 0,
        diagnostics=(DetectionDiagnostic("COND_UNRESOLVED_CANDIDATE",
                                         "second candidate could not be bounded",
                                         "COND-UK-001"),),
    )
    result = _result((mixed_outcome, mixed_evidence),
                     _detected(FeatureId.EXPECTED_RESULT, 1),
                     _detected(FeatureId.ACCEPTANCE_CRITERION, 2))
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None
    assert assessment.findings == ()
    assert "condition/context" in assessment.explanation
    assert "second candidate could not be bounded" in assessment.explanation
    assert "COND_UNRESOLVED_CANDIDATE" in assessment.explanation


def test_accepted_observations_and_evidence_are_not_mutated_on_unknown_result():
    mixed_outcome, mixed_evidence = _mixed(FeatureId.CONDITION_CONTEXT, 0)
    result = _result((mixed_outcome, mixed_evidence),
                     _detected(FeatureId.EXPECTED_RESULT, 1),
                     _detected(FeatureId.ACCEPTANCE_CRITERION, 2))
    features_before = result.features
    evidence_before = result.evidence
    _calculate(result)
    assert result.features is features_before
    assert result.evidence is evidence_before
    assert result.features.condition_contexts.observations == mixed_outcome.observations
    assert result.evidence[0] == mixed_evidence[0]


@pytest.mark.parametrize("build", [
    lambda: _result(_detected(FeatureId.CONDITION_CONTEXT, 0),
                    _detected(FeatureId.EXPECTED_RESULT, 1),
                    _detected(FeatureId.ACCEPTANCE_CRITERION, 2)),
    lambda: _result(_not_detected(FeatureId.CONDITION_CONTEXT),
                    _not_detected(FeatureId.EXPECTED_RESULT),
                    _not_detected(FeatureId.ACCEPTANCE_CRITERION)),
    lambda: _result(_unresolved(FeatureId.CONDITION_CONTEXT),
                    _detected(FeatureId.EXPECTED_RESULT, 1),
                    _detected(FeatureId.ACCEPTANCE_CRITERION, 2)),
], ids=["all-detected", "all-not-detected", "unknown"])
def test_no_completeness_result_ever_creates_a_finding(build):
    assessment = _calculate(build())
    assert assessment.findings == ()


def test_value_is_always_fraction_or_none_never_float_or_decimal():
    computed = _calculate(_result(_detected(FeatureId.CONDITION_CONTEXT, 0),
                                  _not_detected(FeatureId.EXPECTED_RESULT),
                                  _not_detected(FeatureId.ACCEPTANCE_CRITERION)))
    assert isinstance(computed.value, Fraction)
    assert type(computed.value) is Fraction
    withheld = _calculate(_result(_unresolved(FeatureId.CONDITION_CONTEXT),
                                  _not_detected(FeatureId.EXPECTED_RESULT),
                                  _not_detected(FeatureId.ACCEPTANCE_CRITERION)))
    assert withheld.value is None


def test_quantitative_verification_and_vague_families_do_not_affect_completeness():
    verification_detected, verification_evidence = _detected(FeatureId.VERIFICATION_METHOD, 5)
    vague_observation = VagueTermOccurrence(FeatureId.VAGUE_TERM_OCCURRENCE,
                                            "uk_vague_terms_v1", "швидко", ("VAGUE:E6",))
    vague_outcome = FeatureDetectionOutcome(FeatureId.VAGUE_TERM_OCCURRENCE, (vague_observation,),
                                            DetectionProcessingStatus.COMPLETE, ())
    vague_evidence = (Evidence("VAGUE:E6", "R001", FeatureId.VAGUE_TERM_OCCURRENCE,
                               SOURCE[6:12], 6, 12, "TEST-002"),)

    baseline = _result(_detected(FeatureId.CONDITION_CONTEXT, 0),
                       _not_detected(FeatureId.EXPECTED_RESULT),
                       _not_detected(FeatureId.ACCEPTANCE_CRITERION))
    with_irrelevant_families = _result(
        _detected(FeatureId.CONDITION_CONTEXT, 0),
        _not_detected(FeatureId.EXPECTED_RESULT),
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        verification=(verification_detected, verification_evidence),
        vague=(vague_outcome, vague_evidence),
    )
    assert _calculate(baseline).value == _calculate(with_irrelevant_families).value == Fraction(1, 3)


def test_unresolved_verification_method_does_not_force_completeness_unknown():
    result = _result(
        _not_detected(FeatureId.CONDITION_CONTEXT),
        _not_detected(FeatureId.EXPECTED_RESULT),
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        verification=_unresolved(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(0, 1)

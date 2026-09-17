"""Issue #8 / MVP-07 CALC-V-MVP-001 Verifiability calculator tests.

RequirementExtractionResult graphs are built by hand; no FeatureExtractor,
detectors, parser, spaCy, reader, CLI, or reporter involved.
"""

from decimal import Decimal
from fractions import Fraction

import pytest

from requirements_quality_assessment.calculators import VerifiabilityCalculator
from requirements_quality_assessment.calculators.verifiability import RULE_ID
from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState, CharacteristicId, DetectionDiagnostic,
    DetectionProcessingStatus, Evidence, FeatureDetectionOutcome, FeatureId,
    FeatureObservation, NumericValueComponent, QuantitativeConstraintObservation,
    QuantitativeComponentName, Requirement, RequirementExtractionResult,
    RequirementFeatures, UnitComponent, UnitLabel,
)


SOURCE = (
    "System shall process the request and return a response within two "
    "seconds using the audit log verification method for extended testing "
    "purposes today and additional padding text to cover every offset used."
)


def _diagnostic(code="UNRESOLVED_CANDIDATE", explanation="candidate cannot be resolved"):
    return DetectionDiagnostic(code, explanation, "TEST-001")


def _evidence(evidence_id, feature_id, offset):
    return Evidence(evidence_id, "R001", feature_id, SOURCE[offset:offset + 1],
                    offset, offset + 1, "TEST-001")


def _empty_outcome(feature_id):
    return FeatureDetectionOutcome(feature_id, (), DetectionProcessingStatus.COMPLETE, ())


def _not_detected(feature_id):
    return _empty_outcome(feature_id), ()


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
    return outcome, evidence


def _quantitative_observation(value_offset, unit_offset, *, metric=None, context=None,
                              unresolved_components=()):
    """A structurally anchored (value + unit) quantitative constraint observation.

    metric/context stay absent by default and unresolved_components may name
    other legitimately-absent components -- the calculator must accept this
    without imposing extra component-completeness rules.
    """
    value_evidence_id = f"{FeatureId.QUANTITATIVE_CONSTRAINT.value}:V{value_offset}"
    unit_evidence_id = f"{FeatureId.QUANTITATIVE_CONSTRAINT.value}:U{unit_offset}"
    value_component = NumericValueComponent(Decimal("2"), (value_evidence_id,))
    unit_component = UnitComponent(UnitLabel.SECOND, (unit_evidence_id,))
    observation = QuantitativeConstraintObservation(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        metric=metric, comparator=None, value=value_component, unit=unit_component,
        context=context, unresolved_components=unresolved_components,
        evidence_refs=(value_evidence_id, unit_evidence_id),
    )
    evidence = (
        _evidence(value_evidence_id, FeatureId.QUANTITATIVE_CONSTRAINT, value_offset),
        _evidence(unit_evidence_id, FeatureId.QUANTITATIVE_CONSTRAINT, unit_offset),
    )
    return observation, evidence


def _quantitative_detected(value_offset, unit_offset, **kwargs):
    observation, evidence = _quantitative_observation(value_offset, unit_offset, **kwargs)
    outcome = FeatureDetectionOutcome(
        FeatureId.QUANTITATIVE_CONSTRAINT, (observation,), DetectionProcessingStatus.COMPLETE, (),
    )
    return outcome, evidence


def _quantitative_mixed(value_offset, unit_offset, *, diagnostics=None):
    diags = diagnostics if diagnostics is not None else (_diagnostic(),)
    observation, evidence = _quantitative_observation(value_offset, unit_offset)
    outcome = FeatureDetectionOutcome(
        FeatureId.QUANTITATIVE_CONSTRAINT, (observation,), DetectionProcessingStatus.INCOMPLETE, diags,
    )
    return outcome, evidence


def _quantitative_unresolved(*, diagnostics=None):
    diags = diagnostics if diagnostics is not None else (_diagnostic(),)
    return FeatureDetectionOutcome(
        FeatureId.QUANTITATIVE_CONSTRAINT, (), DetectionProcessingStatus.INCOMPLETE, diags,
    ), ()


def _quantitative_not_detected():
    return _empty_outcome(FeatureId.QUANTITATIVE_CONSTRAINT), ()


def _result(acceptance, quantitative, verification, *, condition=None, expected=None, vague=None):
    acceptance_outcome, acceptance_evidence = acceptance
    quantitative_outcome, quantitative_evidence = quantitative
    verification_outcome, verification_evidence = verification
    condition_outcome, condition_evidence = condition or _not_detected(FeatureId.CONDITION_CONTEXT)
    expected_outcome, expected_evidence = expected or _not_detected(FeatureId.EXPECTED_RESULT)
    vague_outcome, vague_evidence = vague or _not_detected(FeatureId.VAGUE_TERM_OCCURRENCE)

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
    return VerifiabilityCalculator().calculate(result)


# -- Tier 1: accepted acceptance criterion -> 1 -------------------------------

def test_accepted_acceptance_criterion_yields_full_score():
    result = _result(
        _detected(FeatureId.ACCEPTANCE_CRITERION, 0),
        _quantitative_not_detected(),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.characteristic_id is CharacteristicId.VERIFIABILITY
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 1)
    assert assessment.assessment_rule_id == RULE_ID == "CALC-V-MVP-001"
    assert assessment.findings == ()


def test_repeated_acceptance_observations_still_yield_one():
    result = _result(
        _detected(FeatureId.ACCEPTANCE_CRITERION, 0, extra_offsets=(1, 2)),
        _quantitative_not_detected(),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assert len(result.features.acceptance_criteria.observations) == 3
    assessment = _calculate(result)
    assert assessment.value == Fraction(1, 1)


def test_accepted_acceptance_with_incomplete_quantitative_processing_yields_one():
    result = _result(
        _detected(FeatureId.ACCEPTANCE_CRITERION, 0),
        _quantitative_unresolved(),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 1)


def test_accepted_acceptance_with_incomplete_verification_processing_yields_one():
    result = _result(
        _detected(FeatureId.ACCEPTANCE_CRITERION, 0),
        _quantitative_not_detected(),
        _unresolved(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 1)


def test_accepted_acceptance_in_mixed_outcome_still_yields_one():
    mixed_outcome, mixed_evidence = _mixed(FeatureId.ACCEPTANCE_CRITERION, 0)
    result = _result(
        (mixed_outcome, mixed_evidence),
        _quantitative_not_detected(),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 1)


# -- Tier 2: no acceptance, accepted lower-tier evidence -> 1/2 ---------------

def test_no_acceptance_accepted_quantitative_yields_half():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_detected(1, 2),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)
    assert assessment.assessment_rule_id == RULE_ID


def test_no_acceptance_accepted_verification_yields_half():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _detected(FeatureId.VERIFICATION_METHOD, 3),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)


def test_both_lower_tier_paths_accepted_still_yields_half():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_detected(1, 2),
        _detected(FeatureId.VERIFICATION_METHOD, 3),
    )
    assessment = _calculate(result)
    assert assessment.value == Fraction(1, 2)


def test_repeated_quantitative_observations_do_not_increase_half():
    value_component, evidence_a = _quantitative_observation(1, 2)
    value_component_b, evidence_b = _quantitative_observation(4, 5)
    outcome = FeatureDetectionOutcome(
        FeatureId.QUANTITATIVE_CONSTRAINT, (value_component, value_component_b),
        DetectionProcessingStatus.COMPLETE, (),
    )
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        (outcome, evidence_a + evidence_b),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assert len(result.features.quantitative_constraints.observations) == 2
    assessment = _calculate(result)
    assert assessment.value == Fraction(1, 2)


def test_repeated_verification_observations_do_not_increase_half():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _detected(FeatureId.VERIFICATION_METHOD, 3, extra_offsets=(4, 5)),
    )
    assert len(result.features.verification_methods.observations) == 3
    assessment = _calculate(result)
    assert assessment.value == Fraction(1, 2)


def test_absent_acceptance_accepted_quantitative_incomplete_verification_yields_half():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_detected(1, 2),
        _unresolved(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)


def test_absent_acceptance_accepted_verification_incomplete_quantitative_yields_half():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_unresolved(),
        _detected(FeatureId.VERIFICATION_METHOD, 3),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)


def test_absent_acceptance_mixed_quantitative_still_yields_half():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_mixed(1, 2),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)


# -- Tier 3: complete absence of all three -> 0 -------------------------------

def test_all_three_complete_absent_yields_zero():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(0, 1)
    assert assessment.findings == ()


# -- Material-dependency UNKNOWN propagation ----------------------------------

def test_incomplete_acceptance_with_accepted_quantitative_yields_unknown():
    result = _result(
        _unresolved(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_detected(1, 2),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None
    assert assessment.assessment_rule_id is None
    assert assessment.findings == ()


def test_incomplete_acceptance_with_accepted_verification_yields_unknown():
    result = _result(
        _unresolved(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _detected(FeatureId.VERIFICATION_METHOD, 3),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None


def test_absent_acceptance_no_lower_tier_incomplete_quantitative_yields_unknown():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_unresolved(),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None


def test_absent_acceptance_no_lower_tier_incomplete_verification_yields_unknown():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _unresolved(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None


def test_both_lower_tier_incomplete_with_no_evidence_yields_unknown():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_unresolved(),
        _unresolved(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None


def test_unknown_explanation_names_material_acceptance_family_and_diagnostic():
    result = _result(
        _unresolved(FeatureId.ACCEPTANCE_CRITERION, diagnostics=(
            DetectionDiagnostic("ACCEPT_UNRESOLVED_CANDIDATE",
                                "candidate could not be bounded", "ACCEPT-UK-001"),
        )),
        _quantitative_detected(1, 2),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert "acceptance criterion" in assessment.explanation
    assert "ACCEPT_UNRESOLVED_CANDIDATE" in assessment.explanation
    assert "candidate could not be bounded" in assessment.explanation


def test_unknown_explanation_names_material_lower_tier_family_and_diagnostic():
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _unresolved(FeatureId.VERIFICATION_METHOD, diagnostics=(
            DetectionDiagnostic("VERIFY_UNRESOLVED_CANDIDATE",
                                "method phrase ambiguous", "VERIFY-UK-001"),
        )),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert "verification method" in assessment.explanation
    assert "VERIFY_UNRESOLVED_CANDIDATE" in assessment.explanation
    assert "method phrase ambiguous" in assessment.explanation


# -- Immutability, findings, and value-type guarantees ------------------------

def test_accepted_observations_and_evidence_are_not_mutated():
    mixed_outcome, mixed_evidence = _mixed(FeatureId.ACCEPTANCE_CRITERION, 0)
    result = _result(
        (mixed_outcome, mixed_evidence),
        _quantitative_not_detected(),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    features_before = result.features
    evidence_before = result.evidence
    _calculate(result)
    assert result.features is features_before
    assert result.evidence is evidence_before
    assert result.features.acceptance_criteria.observations == mixed_outcome.observations
    assert result.evidence[0] == mixed_evidence[0]


@pytest.mark.parametrize("build", [
    lambda: _result(_detected(FeatureId.ACCEPTANCE_CRITERION, 0),
                    _quantitative_not_detected(), _not_detected(FeatureId.VERIFICATION_METHOD)),
    lambda: _result(_not_detected(FeatureId.ACCEPTANCE_CRITERION),
                    _quantitative_detected(1, 2), _not_detected(FeatureId.VERIFICATION_METHOD)),
    lambda: _result(_not_detected(FeatureId.ACCEPTANCE_CRITERION),
                    _quantitative_not_detected(), _not_detected(FeatureId.VERIFICATION_METHOD)),
    lambda: _result(_unresolved(FeatureId.ACCEPTANCE_CRITERION),
                    _quantitative_not_detected(), _not_detected(FeatureId.VERIFICATION_METHOD)),
], ids=["full", "partial", "zero", "unknown"])
def test_no_verifiability_result_ever_creates_a_finding(build):
    assessment = _calculate(build())
    assert assessment.findings == ()


def test_value_is_always_fraction_or_none_never_float_or_decimal():
    full = _calculate(_result(_detected(FeatureId.ACCEPTANCE_CRITERION, 0),
                              _quantitative_not_detected(), _not_detected(FeatureId.VERIFICATION_METHOD)))
    assert type(full.value) is Fraction

    half = _calculate(_result(_not_detected(FeatureId.ACCEPTANCE_CRITERION),
                              _quantitative_detected(1, 2), _not_detected(FeatureId.VERIFICATION_METHOD)))
    assert type(half.value) is Fraction

    zero = _calculate(_result(_not_detected(FeatureId.ACCEPTANCE_CRITERION),
                              _quantitative_not_detected(), _not_detected(FeatureId.VERIFICATION_METHOD)))
    assert type(zero.value) is Fraction

    unknown = _calculate(_result(_unresolved(FeatureId.ACCEPTANCE_CRITERION),
                                 _quantitative_not_detected(), _not_detected(FeatureId.VERIFICATION_METHOD)))
    assert unknown.value is None


def test_irrelevant_families_do_not_affect_verifiability():
    baseline = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_detected(1, 2),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    with_irrelevant_families = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_detected(1, 2),
        _not_detected(FeatureId.VERIFICATION_METHOD),
        condition=_detected(FeatureId.CONDITION_CONTEXT, 10),
        expected=_detected(FeatureId.EXPECTED_RESULT, 11),
    )
    baseline_assessment = _calculate(baseline)
    other_assessment = _calculate(with_irrelevant_families)
    assert baseline_assessment.value == other_assessment.value == Fraction(1, 2)
    assert baseline_assessment.state is other_assessment.state is CharacteristicAssessmentState.COMPUTED


def test_quantitative_observation_without_metric_or_context_still_counts_as_lower_tier_evidence():
    """A structurally anchored (value + unit) observation is sufficient evidence.

    The calculator must not impose extra component-completeness checks
    (metric, context, unresolved_components) beyond bool(observations).
    """
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_detected(1, 2, metric=None, context=None,
                               unresolved_components=(QuantitativeComponentName.METRIC,
                                                       QuantitativeComponentName.CONTEXT)),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)


# -- Binding characteristic-layer cases (model-spec Section 7.16.8) ----------

def test_binding_case_a_verifiability_is_one():
    """Case A: accepted acceptance criterion + accepted quantitative constraint
    + NOT_DETECTED verification method -> V = 1 (acceptance alone suffices)."""
    result = _result(
        _detected(FeatureId.ACCEPTANCE_CRITERION, 0),
        _quantitative_detected(1, 2),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 1)


def test_binding_case_b_verifiability_is_zero():
    """Case B: no acceptance/quantitative/verification accepted, complete
    processing -> V = 0."""
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _not_detected(FeatureId.VERIFICATION_METHOD),
        expected=_detected(FeatureId.EXPECTED_RESULT, 10),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(0, 1)


def test_binding_case_c_verifiability_is_half():
    """Case C: no acceptance accepted; accepted verification-method observation
    is the named lower-tier evidence path, no material unresolved candidate
    -> V = 1/2."""
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _detected(FeatureId.VERIFICATION_METHOD, 3),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(1, 2)


def test_binding_case_d_verifiability_is_unknown():
    """Case D: verification-method family has VERIFY_UNRESOLVED_CANDIDATE, no
    accepted method, incomplete processing; no acceptance/quantitative accepted
    -> state = UNKNOWN, value = None."""
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _unresolved(FeatureId.VERIFICATION_METHOD, diagnostics=(
            DetectionDiagnostic("VERIFY_UNRESOLVED_CANDIDATE",
                                "candidate is neither a present nor an absent method",
                                "VERIFY-UK-001"),
        )),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.UNKNOWN
    assert assessment.value is None


def test_binding_case_e_verifiability_is_zero():
    """Case E: every relevant detector has completed, all NOT_DETECTED, no
    unresolved candidate -> V = 0."""
    result = _result(
        _not_detected(FeatureId.ACCEPTANCE_CRITERION),
        _quantitative_not_detected(),
        _not_detected(FeatureId.VERIFICATION_METHOD),
    )
    assessment = _calculate(result)
    assert assessment.state is CharacteristicAssessmentState.COMPUTED
    assert assessment.value == Fraction(0, 1)

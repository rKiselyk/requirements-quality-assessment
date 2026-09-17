"""Issue #10 / MVP-09A Section 11 requirement quality profile contract tests."""

from dataclasses import FrozenInstanceError, fields
from fractions import Fraction

import pytest

from requirements_quality_assessment.domain import (
    CharacteristicAssessment, CharacteristicAssessmentState, CharacteristicId,
    Finding, FindingKind, RequirementQualityProfile,
)


def _finding(*, finding_id="F1", requirement_id="R001",
             characteristic_id=CharacteristicId.UNAMBIGUITY,
             kind=FindingKind.SIGNAL, code="VAGUE_TERM_SIGNAL",
             rule_id="FIND-U-VAGUE-001", criterion_id=None,
             evidence_refs=("E1",), explanation="Potential ambiguity indicator."):
    return Finding(finding_id, requirement_id, characteristic_id, kind, code,
                    rule_id, criterion_id, evidence_refs, explanation)


def _assessment(*, characteristic_id, state=CharacteristicAssessmentState.COMPUTED,
                 value=Fraction(1, 1), assessment_rule_id="CALC-X-MVP-001",
                 findings=(), explanation="computed"):
    return CharacteristicAssessment(characteristic_id, state, value,
                                    assessment_rule_id, findings, explanation)


def _computed(characteristic_id, value, assessment_rule_id, explanation="computed"):
    return _assessment(characteristic_id=characteristic_id, value=value,
                       assessment_rule_id=assessment_rule_id, explanation=explanation)


def test_three_valid_computed_assessments_construct_a_valid_profile() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 3), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 2), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness is completeness
    assert profile.verifiability is verifiability
    assert profile.unambiguity is unambiguity


def test_profile_preserves_exact_fraction_values() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 3), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 2), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.value == Fraction(1, 3)
    assert profile.verifiability.value == Fraction(1, 2)
    assert profile.unambiguity.value == Fraction(1, 1)


def test_profile_preserves_assessment_rule_id_per_component() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.assessment_rule_id == "CALC-C-MVP-001"
    assert profile.verifiability.assessment_rule_id == "CALC-V-MVP-001"
    assert profile.unambiguity.assessment_rule_id == "CALC-U-MVP-001"


def test_profile_preserves_explanations_unchanged() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1),
                             "CALC-C-MVP-001", explanation="complete per rule")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1),
                              "CALC-V-MVP-001", explanation="verifiable per rule")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1),
                            "CALC-U-MVP-001", explanation="unambiguous per rule")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.explanation == "complete per rule"
    assert profile.verifiability.explanation == "verifiable per rule"
    assert profile.unambiguity.explanation == "unambiguous per rule"


def test_unambiguity_signal_findings_remain_unchanged_in_component() -> None:
    signal = _finding(finding_id="FIND-U-VAGUE-001", characteristic_id=CharacteristicId.UNAMBIGUITY,
                      kind=FindingKind.SIGNAL, code="VAGUE_TERM_SIGNAL",
                      rule_id="FIND-U-VAGUE-001")
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    unambiguity = _assessment(characteristic_id=CharacteristicId.UNAMBIGUITY,
                              value=Fraction(1, 2), assessment_rule_id="CALC-U-MVP-001",
                              findings=(signal,))

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.unambiguity.findings == (signal,)


def test_mixed_computed_and_unknown_states_are_valid_without_profile_level_state() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")
    verifiability = _assessment(characteristic_id=CharacteristicId.VERIFIABILITY,
                                state=CharacteristicAssessmentState.UNKNOWN, value=None,
                                assessment_rule_id=None, explanation="withheld")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.state is CharacteristicAssessmentState.COMPUTED
    assert profile.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert profile.unambiguity.state is CharacteristicAssessmentState.COMPUTED
    assert not hasattr(profile, "state")
    assert not hasattr(profile, "value")


def test_not_applicable_component_is_preserved_and_not_converted_to_zero() -> None:
    completeness = _assessment(characteristic_id=CharacteristicId.COMPLETENESS,
                               state=CharacteristicAssessmentState.NOT_APPLICABLE, value=None,
                               assessment_rule_id=None, explanation="not applicable")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.state is CharacteristicAssessmentState.NOT_APPLICABLE
    assert profile.completeness.value is None


def test_wrong_characteristic_in_completeness_slot_is_rejected() -> None:
    wrong = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    with pytest.raises(ValueError):
        RequirementQualityProfile(wrong, verifiability, unambiguity)


def test_wrong_characteristic_in_verifiability_slot_is_rejected() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")
    wrong = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    with pytest.raises(ValueError):
        RequirementQualityProfile(completeness, wrong, unambiguity)


def test_wrong_characteristic_in_unambiguity_slot_is_rejected() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    wrong = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")

    with pytest.raises(ValueError):
        RequirementQualityProfile(completeness, verifiability, wrong)


def test_non_characteristic_assessment_component_is_rejected_with_type_error() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    with pytest.raises(TypeError):
        RequirementQualityProfile("not an assessment", verifiability, unambiguity)
    with pytest.raises(TypeError):
        RequirementQualityProfile(completeness, "not an assessment", unambiguity)
    with pytest.raises(TypeError):
        RequirementQualityProfile(completeness, verifiability, "not an assessment")


def test_profile_is_immutable() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")
    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    with pytest.raises(FrozenInstanceError):
        profile.completeness = completeness


def test_profile_has_exactly_the_three_approved_fields_and_no_scalar_result() -> None:
    assert {field.name for field in fields(RequirementQualityProfile)} == {
        "completeness", "verifiability", "unambiguity",
    }
    for forbidden in ("score", "value", "overall_score", "requirement_quality_score", "state"):
        assert not hasattr(RequirementQualityProfile, forbidden)

    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")
    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    for forbidden in ("score", "value", "overall_score", "requirement_quality_score", "state"):
        assert not hasattr(profile, forbidden)


def test_construction_performs_no_arithmetic_and_preserves_component_values() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 3), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 2), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness == completeness
    assert profile.verifiability == verifiability
    assert profile.unambiguity == unambiguity
    assert profile.completeness.value == Fraction(1, 3)
    assert profile.verifiability.value == Fraction(1, 2)
    assert profile.unambiguity.value == Fraction(1, 1)
    assert isinstance(profile.completeness.value, Fraction)
    assert isinstance(profile.verifiability.value, Fraction)
    assert isinstance(profile.unambiguity.value, Fraction)


def test_binding_case_a_all_computed_full_marks() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.value == Fraction(1, 1)
    assert profile.verifiability.value == Fraction(1, 1)
    assert profile.unambiguity.value == Fraction(1, 1)


def test_binding_case_b_mixed_fractions() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(1, 3), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(0, 1), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 2), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.value == Fraction(1, 3)
    assert profile.verifiability.value == Fraction(0, 1)
    assert profile.unambiguity.value == Fraction(1, 2)


def test_binding_case_c_mixed_fractions_reversed() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(0, 1), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 2), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.value == Fraction(0, 1)
    assert profile.verifiability.value == Fraction(1, 2)
    assert profile.unambiguity.value == Fraction(1, 1)


def test_binding_case_d_verifiability_unknown() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(0, 1), "CALC-C-MVP-001")
    verifiability = _assessment(characteristic_id=CharacteristicId.VERIFIABILITY,
                                state=CharacteristicAssessmentState.UNKNOWN, value=None,
                                assessment_rule_id=None, explanation="withheld")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.value == Fraction(0, 1)
    assert profile.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert profile.verifiability.value is None
    assert profile.unambiguity.value == Fraction(1, 1)


def test_binding_case_e_all_zero_and_full() -> None:
    completeness = _computed(CharacteristicId.COMPLETENESS, Fraction(0, 1), "CALC-C-MVP-001")
    verifiability = _computed(CharacteristicId.VERIFIABILITY, Fraction(0, 1), "CALC-V-MVP-001")
    unambiguity = _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "CALC-U-MVP-001")

    profile = RequirementQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.value == Fraction(0, 1)
    assert profile.verifiability.value == Fraction(0, 1)
    assert profile.unambiguity.value == Fraction(1, 1)

"""Issue #7 / Section 7.16 shared characteristic-assessment contract tests."""

from dataclasses import FrozenInstanceError, fields
from fractions import Fraction

import pytest

from requirements_quality_assessment.domain import (
    CharacteristicAssessment, CharacteristicAssessmentState, CharacteristicId,
    Finding, FindingKind,
)


def _finding(*, finding_id="F1", requirement_id="R001",
             characteristic_id=CharacteristicId.UNAMBIGUITY,
             kind=FindingKind.SIGNAL, code="VAGUE_TERM_SIGNAL",
             rule_id="FIND-U-VAGUE-001", criterion_id=None,
             evidence_refs=("E1",), explanation="Potential ambiguity indicator."):
    return Finding(finding_id, requirement_id, characteristic_id, kind, code,
                    rule_id, criterion_id, evidence_refs, explanation)


def _assessment(*, characteristic_id=CharacteristicId.COMPLETENESS,
                 state=CharacteristicAssessmentState.COMPUTED,
                 value=Fraction(1, 1), assessment_rule_id="CALC-C-MVP-001",
                 findings=(), explanation="computed"):
    return CharacteristicAssessment(characteristic_id, state, value,
                                    assessment_rule_id, findings, explanation)


def test_characteristic_id_state_and_finding_kind_have_exact_membership() -> None:
    assert {member.value for member in CharacteristicId} == {
        "COMPLETENESS", "VERIFIABILITY", "UNAMBIGUITY",
    }
    assert {member.value for member in CharacteristicAssessmentState} == {
        "COMPUTED", "NOT_APPLICABLE", "UNKNOWN",
    }
    assert {member.value for member in FindingKind} == {"SIGNAL", "QUALITY_PROBLEM"}


def test_finding_construction_and_immutability() -> None:
    finding = _finding()
    assert {field.name for field in fields(Finding)} == {
        "finding_id", "requirement_id", "characteristic_id", "kind", "code",
        "rule_id", "criterion_id", "evidence_refs", "explanation",
    }
    with pytest.raises(FrozenInstanceError):
        finding.code = "OTHER"


@pytest.mark.parametrize("field_name", [
    "finding_id", "requirement_id", "code", "rule_id", "explanation",
])
def test_finding_rejects_empty_required_strings(field_name) -> None:
    with pytest.raises(ValueError):
        _finding(**{field_name: ""})


def test_finding_rejects_wrong_typed_characteristic_id_and_kind() -> None:
    with pytest.raises(TypeError):
        _finding(characteristic_id="UNAMBIGUITY")
    with pytest.raises(TypeError):
        _finding(kind="SIGNAL")


def test_finding_criterion_id_and_evidence_refs_invariants() -> None:
    with pytest.raises(ValueError):
        _finding(criterion_id="")
    assert _finding(criterion_id="CRIT-1").criterion_id == "CRIT-1"
    with pytest.raises(TypeError):
        _finding(evidence_refs=["E1"])
    with pytest.raises(TypeError):
        _finding(evidence_refs=(1,))


def test_signal_finding_requires_non_empty_evidence_refs() -> None:
    with pytest.raises(ValueError):
        _finding(kind=FindingKind.SIGNAL, evidence_refs=())
    with pytest.raises(ValueError):
        _finding(kind=FindingKind.SIGNAL, criterion_id="CRIT-1", evidence_refs=())


def test_empty_evidence_refs_requires_quality_problem_with_criterion_id() -> None:
    # A QUALITY_PROBLEM with no criterion_id still cannot omit evidence_refs.
    with pytest.raises(ValueError):
        _finding(kind=FindingKind.QUALITY_PROBLEM, code="SOME_PROBLEM",
                 rule_id="RULE-X", criterion_id=None, evidence_refs=())


def test_absence_shaped_quality_problem_is_structurally_representable() -> None:
    # This only confirms the shape from Section 7.16.5 can be represented; it
    # does not imply any absence-based QUALITY_PROBLEM rule is approved or
    # that any calculator in this task creates one.
    finding = _finding(kind=FindingKind.QUALITY_PROBLEM, code="SOME_PROBLEM",
                       rule_id="RULE-X", criterion_id="CRIT-1", evidence_refs=())
    assert finding.evidence_refs == ()
    assert finding.kind is FindingKind.QUALITY_PROBLEM
    assert finding.criterion_id == "CRIT-1"


def test_computed_assessment_requires_fraction_in_bounds_and_rule_id() -> None:
    assessment = _assessment()
    assert assessment.value == Fraction(1, 1)
    with pytest.raises(FrozenInstanceError):
        assessment.value = Fraction(0, 1)
    with pytest.raises(ValueError):
        _assessment(value=None)
    with pytest.raises(ValueError):
        _assessment(value=1)  # int, not Fraction
    with pytest.raises(ValueError):
        _assessment(value=Fraction(4, 3))
    with pytest.raises(ValueError):
        _assessment(value=Fraction(-1, 3))
    with pytest.raises(ValueError):
        _assessment(assessment_rule_id=None)


@pytest.mark.parametrize("bad_rule_id", ["", 5])
def test_assessment_rule_id_must_be_none_or_non_empty_string_for_every_state(bad_rule_id) -> None:
    with pytest.raises((ValueError, TypeError)):
        _assessment(assessment_rule_id=bad_rule_id)
    with pytest.raises((ValueError, TypeError)):
        _assessment(state=CharacteristicAssessmentState.UNKNOWN, value=None,
                     assessment_rule_id=bad_rule_id)


def test_unknown_state_requires_none_value_but_no_rule_id() -> None:
    assessment = _assessment(state=CharacteristicAssessmentState.UNKNOWN, value=None,
                             assessment_rule_id=None, explanation="withheld")
    assert assessment.assessment_rule_id is None
    with pytest.raises(ValueError):
        _assessment(state=CharacteristicAssessmentState.UNKNOWN, value=Fraction(1, 3),
                    assessment_rule_id=None)


def test_unknown_state_may_carry_findings_matching_its_characteristic() -> None:
    signal = _finding(characteristic_id=CharacteristicId.UNAMBIGUITY)
    assessment = _assessment(
        characteristic_id=CharacteristicId.UNAMBIGUITY,
        state=CharacteristicAssessmentState.UNKNOWN, value=None,
        assessment_rule_id=None, findings=(signal,), explanation="withheld",
    )
    assert assessment.findings == (signal,)


def test_not_applicable_state_requires_none_value_and_forbids_rule_id_requirement() -> None:
    assessment = _assessment(state=CharacteristicAssessmentState.NOT_APPLICABLE,
                             value=None, assessment_rule_id=None,
                             explanation="not applicable")
    assert assessment.assessment_rule_id is None
    with pytest.raises(ValueError):
        _assessment(state=CharacteristicAssessmentState.NOT_APPLICABLE,
                    value=Fraction(0, 1), assessment_rule_id=None)


def test_not_applicable_state_forbids_quality_problem_finding() -> None:
    problem = _finding(kind=FindingKind.QUALITY_PROBLEM,
                       characteristic_id=CharacteristicId.COMPLETENESS,
                       code="SOME_PROBLEM", rule_id="RULE-X")
    with pytest.raises(ValueError):
        _assessment(state=CharacteristicAssessmentState.NOT_APPLICABLE, value=None,
                    assessment_rule_id=None, findings=(problem,))


def test_finding_characteristic_id_must_match_assessment() -> None:
    mismatched = _finding(characteristic_id=CharacteristicId.VERIFIABILITY)
    with pytest.raises(ValueError):
        _assessment(characteristic_id=CharacteristicId.COMPLETENESS,
                    findings=(mismatched,))


def test_duplicate_finding_ids_within_one_assessment_are_rejected() -> None:
    first = _finding(finding_id="F1", characteristic_id=CharacteristicId.COMPLETENESS,
                     code="A", rule_id="RULE-A")
    second = _finding(finding_id="F1", characteristic_id=CharacteristicId.COMPLETENESS,
                      code="B", rule_id="RULE-B")
    with pytest.raises(ValueError):
        _assessment(characteristic_id=CharacteristicId.COMPLETENESS,
                    findings=(first, second))


def test_findings_must_be_a_tuple_of_finding() -> None:
    with pytest.raises(TypeError):
        _assessment(findings=[_finding(characteristic_id=CharacteristicId.COMPLETENESS)])
    with pytest.raises(TypeError):
        _assessment(findings=("not a finding",))


def test_assessment_rejects_empty_explanation_and_wrong_typed_ids() -> None:
    with pytest.raises(ValueError):
        _assessment(explanation="")
    with pytest.raises(TypeError):
        _assessment(characteristic_id="COMPLETENESS")
    with pytest.raises(TypeError):
        _assessment(state="COMPUTED")

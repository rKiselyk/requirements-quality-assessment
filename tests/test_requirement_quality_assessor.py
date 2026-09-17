"""Issue #10 / MVP-09B RequirementQualityAssessor orchestration tests.

RequirementQualityAssessor is exercised only against manually constructed
domain objects and small injected stub calculators; no FeatureExtractor,
detectors, parser, spaCy, reader, or CLI involved.
"""

from fractions import Fraction

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.calculators.completeness import (
    RULE_ID as COMPLETENESS_RULE_ID,
)
from requirements_quality_assessment.calculators.unambiguity import (
    RULE_ID as UNAMBIGUITY_RULE_ID,
)
from requirements_quality_assessment.calculators.verifiability import (
    RULE_ID as VERIFIABILITY_RULE_ID,
)
from requirements_quality_assessment.domain import (
    CharacteristicAssessment, CharacteristicAssessmentState, CharacteristicId,
    DetectionProcessingStatus, FeatureDetectionOutcome, FeatureId, Finding,
    FindingKind, Requirement, RequirementExtractionResult, RequirementFeatures,
    RequirementQualityProfile,
)


SOURCE = "System shall process the request and return a response with status code value here."


def _empty_outcome(feature_id):
    return FeatureDetectionOutcome(feature_id, (), DetectionProcessingStatus.COMPLETE, ())


def _all_complete_result():
    """All six detection families COMPLETE with no observations."""
    features = RequirementFeatures(
        _empty_outcome(FeatureId.CONDITION_CONTEXT),
        _empty_outcome(FeatureId.EXPECTED_RESULT),
        _empty_outcome(FeatureId.ACCEPTANCE_CRITERION),
        _empty_outcome(FeatureId.QUANTITATIVE_CONSTRAINT),
        _empty_outcome(FeatureId.VERIFICATION_METHOD),
        _empty_outcome(FeatureId.VAGUE_TERM_OCCURRENCE),
    )
    return RequirementExtractionResult(Requirement("R001", 1, SOURCE), features, ())


def _computed_assessment(characteristic_id, value, rule_id, findings=()):
    return CharacteristicAssessment(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.COMPUTED,
        value=value,
        assessment_rule_id=rule_id,
        findings=findings,
        explanation="test fixture",
    )


def _unknown_assessment(characteristic_id):
    return CharacteristicAssessment(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.UNKNOWN,
        value=None,
        assessment_rule_id=None,
        findings=(),
        explanation="test fixture",
    )


def _not_applicable_assessment(characteristic_id):
    return CharacteristicAssessment(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.NOT_APPLICABLE,
        value=None,
        assessment_rule_id=None,
        findings=(),
        explanation="test fixture",
    )


class _StubCalculator:
    def __init__(self, assessment):
        self._assessment = assessment
        self.calls = []

    def calculate(self, result):
        self.calls.append(result)
        return self._assessment


def _stub_trio(completeness_assessment, verifiability_assessment, unambiguity_assessment):
    completeness_calculator = _StubCalculator(completeness_assessment)
    verifiability_calculator = _StubCalculator(verifiability_assessment)
    unambiguity_calculator = _StubCalculator(unambiguity_assessment)
    assessor = RequirementQualityAssessor(
        completeness_calculator=completeness_calculator,
        verifiability_calculator=verifiability_calculator,
        unambiguity_calculator=unambiguity_calculator,
    )
    return assessor, completeness_calculator, verifiability_calculator, unambiguity_calculator


# -- 1. Default production wiring ---------------------------------------------

def test_default_production_wiring_uses_the_three_approved_calculators():
    profile = RequirementQualityAssessor().assess(_all_complete_result())

    assert profile.completeness.state is CharacteristicAssessmentState.COMPUTED
    assert profile.completeness.value == Fraction(0, 1)
    assert profile.completeness.assessment_rule_id == COMPLETENESS_RULE_ID

    assert profile.verifiability.state is CharacteristicAssessmentState.COMPUTED
    assert profile.verifiability.value == Fraction(0, 1)
    assert profile.verifiability.assessment_rule_id == VERIFIABILITY_RULE_ID

    assert profile.unambiguity.state is CharacteristicAssessmentState.COMPUTED
    assert profile.unambiguity.value == Fraction(1, 1)
    assert profile.unambiguity.assessment_rule_id == UNAMBIGUITY_RULE_ID


# -- 2. Exact injected assessment preservation --------------------------------

def test_injected_assessments_are_preserved_by_identity():
    completeness_assessment = _computed_assessment(
        CharacteristicId.COMPLETENESS, Fraction(1, 3), "STUB-C"
    )
    verifiability_assessment = _computed_assessment(
        CharacteristicId.VERIFIABILITY, Fraction(1, 2), "STUB-V"
    )
    unambiguity_assessment = _computed_assessment(
        CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "STUB-U"
    )
    assessor, *_ = _stub_trio(
        completeness_assessment, verifiability_assessment, unambiguity_assessment
    )

    profile = assessor.assess(_all_complete_result())

    assert profile.completeness is completeness_assessment
    assert profile.verifiability is verifiability_assessment
    assert profile.unambiguity is unambiguity_assessment


# -- 3. Same input passed to every calculator ---------------------------------

def test_same_extraction_result_is_passed_to_every_calculator():
    result = _all_complete_result()
    assessor, completeness_calculator, verifiability_calculator, unambiguity_calculator = _stub_trio(
        _computed_assessment(CharacteristicId.COMPLETENESS, Fraction(0, 1), "STUB-C"),
        _computed_assessment(CharacteristicId.VERIFIABILITY, Fraction(0, 1), "STUB-V"),
        _computed_assessment(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "STUB-U"),
    )

    assessor.assess(result)

    assert completeness_calculator.calls[0] is result
    assert verifiability_calculator.calls[0] is result
    assert unambiguity_calculator.calls[0] is result


# -- 4. Exactly one call per calculator ----------------------------------------

def test_each_calculator_is_called_exactly_once_per_assess_call():
    result = _all_complete_result()
    assessor, completeness_calculator, verifiability_calculator, unambiguity_calculator = _stub_trio(
        _computed_assessment(CharacteristicId.COMPLETENESS, Fraction(0, 1), "STUB-C"),
        _computed_assessment(CharacteristicId.VERIFIABILITY, Fraction(0, 1), "STUB-V"),
        _computed_assessment(CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "STUB-U"),
    )

    assessor.assess(result)

    assert len(completeness_calculator.calls) == 1
    assert len(verifiability_calculator.calls) == 1
    assert len(unambiguity_calculator.calls) == 1


# -- 5. Mixed states preserved --------------------------------------------------

def test_mixed_component_states_are_preserved_without_overall_state():
    completeness_assessment = _computed_assessment(
        CharacteristicId.COMPLETENESS, Fraction(1, 1), "STUB-C"
    )
    verifiability_assessment = _unknown_assessment(CharacteristicId.VERIFIABILITY)
    unambiguity_assessment = _computed_assessment(
        CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "STUB-U"
    )
    assessor, *_ = _stub_trio(
        completeness_assessment, verifiability_assessment, unambiguity_assessment
    )

    profile = assessor.assess(_all_complete_result())

    assert profile.completeness.state is CharacteristicAssessmentState.COMPUTED
    assert profile.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert profile.unambiguity.state is CharacteristicAssessmentState.COMPUTED
    assert not hasattr(profile, "state")


# -- 6. NOT_APPLICABLE preserved -------------------------------------------------

def test_not_applicable_component_is_preserved_unchanged():
    verifiability_assessment = _not_applicable_assessment(CharacteristicId.VERIFIABILITY)
    assessor = RequirementQualityAssessor(
        verifiability_calculator=_StubCalculator(verifiability_assessment),
    )

    profile = assessor.assess(_all_complete_result())

    assert profile.verifiability is verifiability_assessment
    assert profile.verifiability.state is CharacteristicAssessmentState.NOT_APPLICABLE
    assert profile.verifiability.value is None


# -- 7. Exact Fraction preservation ----------------------------------------------

def test_exact_fraction_values_are_not_normalized_or_converted():
    completeness_assessment = _computed_assessment(
        CharacteristicId.COMPLETENESS, Fraction(1, 3), "STUB-C"
    )
    verifiability_assessment = _computed_assessment(
        CharacteristicId.VERIFIABILITY, Fraction(1, 2), "STUB-V"
    )
    unambiguity_assessment = _computed_assessment(
        CharacteristicId.UNAMBIGUITY, Fraction(1, 1), "STUB-U"
    )
    assessor, *_ = _stub_trio(
        completeness_assessment, verifiability_assessment, unambiguity_assessment
    )

    profile = assessor.assess(_all_complete_result())

    assert profile.completeness.value == Fraction(1, 3)
    assert profile.verifiability.value == Fraction(1, 2)
    assert profile.unambiguity.value == Fraction(1, 1)
    assert type(profile.completeness.value) is Fraction
    assert type(profile.verifiability.value) is Fraction
    assert type(profile.unambiguity.value) is Fraction


# -- 8. Finding preservation ------------------------------------------------------

def test_findings_are_preserved_unchanged_in_their_owning_assessment():
    finding = Finding(
        finding_id="FIND-U-VAGUE-001:F001",
        requirement_id="R001",
        characteristic_id=CharacteristicId.UNAMBIGUITY,
        kind=FindingKind.SIGNAL,
        code="VAGUE_TERM_SIGNAL",
        rule_id="FIND-U-VAGUE-001",
        criterion_id=None,
        evidence_refs=("UK-VAGUE-001:E001",),
        explanation=(
            "FIND-U-VAGUE-001 matched the approved seed literal 'швидко' "
            "(uk_vague_terms_v1) as a potential ambiguity indicator; this is "
            "not a confirmed ambiguity or a confirmed quality defect."
        ),
    )
    unambiguity_assessment = _computed_assessment(
        CharacteristicId.UNAMBIGUITY, Fraction(1, 2), UNAMBIGUITY_RULE_ID, findings=(finding,)
    )
    assessor = RequirementQualityAssessor(
        unambiguity_calculator=_StubCalculator(unambiguity_assessment),
    )

    profile = assessor.assess(_all_complete_result())

    assert profile.unambiguity is unambiguity_assessment
    assert profile.unambiguity.findings == (finding,)
    assert profile.unambiguity.findings[0] is finding


# -- 9. Wrong characteristic output is rejected by the profile contract ----------

def test_wrong_characteristic_output_is_rejected_by_profile_contract():
    wrong_assessment = _computed_assessment(
        CharacteristicId.VERIFIABILITY, Fraction(0, 1), "STUB-WRONG"
    )
    assessor = RequirementQualityAssessor(
        completeness_calculator=_StubCalculator(wrong_assessment),
    )

    with pytest.raises(ValueError):
        assessor.assess(_all_complete_result())


# -- 10. Input is not mutated -----------------------------------------------------

def test_extraction_result_is_not_mutated():
    result = _all_complete_result()
    features_before = result.features
    evidence_before = result.evidence
    requirement_before = result.requirement

    RequirementQualityAssessor().assess(result)

    assert result.features is features_before
    assert result.evidence is evidence_before
    assert result.requirement is requirement_before


# -- 11. No aggregation/scalar output ----------------------------------------------

def test_assess_returns_exactly_a_requirement_quality_profile():
    profile = RequirementQualityAssessor().assess(_all_complete_result())

    assert type(profile) is RequirementQualityProfile
    assert not hasattr(profile, "score")
    assert not hasattr(profile, "overall")


# -- 12. Repeated deterministic use -------------------------------------------------

def test_repeated_calls_on_the_same_input_are_deterministic():
    result = _all_complete_result()
    assessor = RequirementQualityAssessor()

    first = assessor.assess(result)
    second = assessor.assess(result)

    assert first.completeness == second.completeness
    assert first.verifiability == second.verifiability
    assert first.unambiguity == second.unambiguity

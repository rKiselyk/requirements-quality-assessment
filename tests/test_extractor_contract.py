"""Contract tests without a production feature detector."""

from dataclasses import fields
import inspect
import subprocess
import sys
from typing import get_type_hints

from requirements_quality_assessment.domain import (
    DetectionProcessingStatus, FeatureDetectionOutcome, FeatureId,
    Evidence, FeatureObservation, Requirement, RequirementExtractionResult,
    RequirementFeatures,
)
from requirements_quality_assessment.extractor import FeatureExtractor


def _features(*, observed_condition: bool = False) -> RequirementFeatures:
    def outcome(
        feature_id: FeatureId, observations: tuple[FeatureObservation, ...] = ()
    ) -> FeatureDetectionOutcome[FeatureObservation]:
        return FeatureDetectionOutcome(
            feature_id=feature_id,
            observations=observations,
            processing_status=DetectionProcessingStatus.COMPLETE,
            diagnostics=(),
        )

    condition_observations = (
        (FeatureObservation(FeatureId.CONDITION_CONTEXT, ("E1",)),)
        if observed_condition else ()
    )
    return RequirementFeatures(
        condition_contexts=outcome(FeatureId.CONDITION_CONTEXT, condition_observations),
        expected_results=outcome(FeatureId.EXPECTED_RESULT),
        acceptance_criteria=outcome(FeatureId.ACCEPTANCE_CRITERION),
        quantitative_constraints=outcome(FeatureId.QUANTITATIVE_CONSTRAINT),
        verification_methods=outcome(FeatureId.VERIFICATION_METHOD),
        vague_term_occurrences=outcome(FeatureId.VAGUE_TERM_OCCURRENCE),
    )


class StubExtractor:
    def __init__(self, result: RequirementExtractionResult) -> None:
        self.result = result

    def extract(self, requirement: Requirement) -> RequirementExtractionResult:
        assert isinstance(requirement, Requirement)
        return self.result


class AlternateExtractor:
    def __init__(self, result: RequirementExtractionResult) -> None:
        self.result = result

    def extract(self, requirement: Requirement) -> RequirementExtractionResult:
        assert isinstance(requirement, Requirement)
        return self.result


def _run_extractor(
    extractor: FeatureExtractor, requirement: Requirement
) -> RequirementExtractionResult:
    return extractor.extract(requirement)


def test_extract_accepts_requirement_and_returns_evidence_with_six_family_features() -> None:
    requirement = Requirement("R001", 2, "Система формує звіт.")
    result = RequirementExtractionResult(requirement, _features(), ())

    returned = StubExtractor(result).extract(requirement)

    assert returned is result
    assert isinstance(returned, RequirementExtractionResult)
    assert returned.requirement is requirement
    assert returned.evidence == ()
    assert {field.name for field in fields(returned.features)} == {
        "condition_contexts", "expected_results", "acceptance_criteria",
        "quantitative_constraints", "verification_methods", "vague_term_occurrences",
    }


def test_structural_implementations_are_replaceable_for_a_protocol_consumer() -> None:
    requirement = Requirement("R002", 3, "Якщо є запит, система формує звіт.")
    first_result = RequirementExtractionResult(requirement, _features(), ())
    second_result = RequirementExtractionResult(
        requirement, _features(observed_condition=True),
        (Evidence("E1", requirement.id, FeatureId.CONDITION_CONTEXT,
                  requirement.text[:4], 0, 4, "COND-UK-001"),),
    )

    assert _run_extractor(StubExtractor(first_result), requirement) is first_result
    assert _run_extractor(AlternateExtractor(second_result), requirement) is second_result
    assert (second_result.features.condition_contexts.observations
            != first_result.features.condition_contexts.observations)


def test_public_signature_has_only_domain_input_and_output() -> None:
    parameters = inspect.signature(FeatureExtractor.extract).parameters
    hints = get_type_hints(FeatureExtractor.extract)

    assert tuple(parameters) == ("self", "requirement")
    assert hints == {"requirement": Requirement, "return": RequirementExtractionResult}


def test_importing_boundary_requires_no_nlp_runtime() -> None:
    subprocess.run(
        [sys.executable, "-c", (
            "from requirements_quality_assessment.extractor import FeatureExtractor; "
            "import sys; assert 'spacy' not in sys.modules; "
            "assert 'stanza' not in sys.modules"
        )],
        check=True,
        capture_output=True,
        text=True,
    )

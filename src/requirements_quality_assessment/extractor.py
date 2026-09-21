"""Replaceable boundary and production orchestration for feature detection."""

from typing import Protocol

from .detectors import (
    AcceptanceCriterionBaselineDetector,
    ConditionContextBaselineDetector,
    ConditionContextDetector,
    ExpectedResultBaselineDetector,
    QuantitativeBaselineDetector,
    UkVagueTermDetector,
    VerificationMethodBaselineDetector,
)
from .domain import (
    Evidence,
    FeatureDetectionOutcome,
    FeatureObservation,
    QuantitativeConstraintObservation,
    Requirement,
    RequirementExtractionResult,
    RequirementFeatures,
    VagueTermOccurrence,
)
from .parsing import SpaCyRequirementParser


class FeatureExtractor(Protocol):
    def extract(self, requirement: Requirement) -> RequirementExtractionResult:
        ...


class _SimpleFeatureDetector(Protocol):
    def detect(
        self, requirement: Requirement
    ) -> tuple[FeatureDetectionOutcome[FeatureObservation], tuple[Evidence, ...]]:
        ...


class _QuantitativeFeatureDetector(Protocol):
    def detect(
        self, requirement: Requirement
    ) -> tuple[
        FeatureDetectionOutcome[QuantitativeConstraintObservation],
        tuple[Evidence, ...],
    ]:
        ...


class _VagueTermDetector(Protocol):
    def detect(
        self, requirement: Requirement
    ) -> tuple[FeatureDetectionOutcome[VagueTermOccurrence], tuple[Evidence, ...]]:
        ...


class BaselineFeatureExtractor:
    """Assemble the six approved detector-family results without reinterpretation."""

    def __init__(
        self,
        condition_context_detector: _SimpleFeatureDetector | None = None,
        expected_result_detector: _SimpleFeatureDetector | None = None,
        acceptance_criterion_detector: _SimpleFeatureDetector | None = None,
        quantitative_detector: _QuantitativeFeatureDetector | None = None,
        verification_method_detector: _SimpleFeatureDetector | None = None,
        vague_term_detector: _VagueTermDetector | None = None,
    ) -> None:
        parser = SpaCyRequirementParser()
        quantitative = (
            quantitative_detector
            if quantitative_detector is not None
            else QuantitativeBaselineDetector()
        )
        condition = (
            condition_context_detector
            if condition_context_detector is not None
            else ConditionContextDetector(parser=parser, quantitative_detector=quantitative)
        )
        expected = (
            expected_result_detector
            if expected_result_detector is not None
            else ExpectedResultBaselineDetector(
                parser=parser,
                # COND-UK-002 authorizes condition observations only. Preserve
                # RESULT-UK-001's frozen separation and unresolved-candidate gate.
                condition_detector=(
                    condition_context_detector
                    if condition_context_detector is not None
                    else ConditionContextBaselineDetector(quantitative)
                ),
            )
        )

        self._condition_context_detector = condition
        self._expected_result_detector = expected
        self._acceptance_criterion_detector = (
            acceptance_criterion_detector
            if acceptance_criterion_detector is not None
            else AcceptanceCriterionBaselineDetector(
                expected_result_detector=expected,
                quantitative_detector=quantitative,
            )
        )
        self._quantitative_detector = quantitative
        self._verification_method_detector = (
            verification_method_detector
            if verification_method_detector is not None
            else VerificationMethodBaselineDetector(parser=parser)
        )
        self._vague_term_detector = (
            vague_term_detector
            if vague_term_detector is not None
            else UkVagueTermDetector()
        )

    def extract(self, requirement: Requirement) -> RequirementExtractionResult:
        condition_outcome, condition_evidence = (
            self._condition_context_detector.detect(requirement)
        )
        expected_outcome, expected_evidence = (
            self._expected_result_detector.detect(requirement)
        )
        acceptance_outcome, acceptance_evidence = (
            self._acceptance_criterion_detector.detect(requirement)
        )
        quantitative_outcome, quantitative_evidence = (
            self._quantitative_detector.detect(requirement)
        )
        verification_outcome, verification_evidence = (
            self._verification_method_detector.detect(requirement)
        )
        vague_outcome, vague_evidence = self._vague_term_detector.detect(requirement)

        features = RequirementFeatures(
            condition_contexts=condition_outcome,
            expected_results=expected_outcome,
            acceptance_criteria=acceptance_outcome,
            quantitative_constraints=quantitative_outcome,
            verification_methods=verification_outcome,
            vague_term_occurrences=vague_outcome,
        )
        family_evidence = (
            condition_evidence,
            expected_evidence,
            acceptance_evidence,
            quantitative_evidence,
            verification_evidence,
            vague_evidence,
        )
        unified_evidence = tuple(
            item
            for _, _, item in sorted(
                (
                    (family_index, local_index, item)
                    for family_index, evidence in enumerate(family_evidence)
                    for local_index, item in enumerate(evidence)
                ),
                key=lambda entry: (
                    entry[2].start_offset,
                    entry[2].end_offset,
                    entry[0],
                    entry[1],
                ),
            )
        )
        return RequirementExtractionResult(
            requirement=requirement,
            features=features,
            evidence=unified_evidence,
        )

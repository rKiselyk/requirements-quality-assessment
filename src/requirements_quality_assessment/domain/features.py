"""The six approved feature-family contracts; no quality interpretation."""

from dataclasses import dataclass

from .core import FeatureId
from .detection import FeatureDetectionOutcome
from .quantitative import QuantitativeConstraintObservation, _check_refs


@dataclass(frozen=True, slots=True)
class FeatureObservation:
    feature_id: FeatureId
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.feature_id, FeatureId):
            raise TypeError("feature_id must be an approved FeatureId")
        if self.feature_id not in {
            FeatureId.CONDITION_CONTEXT, FeatureId.EXPECTED_RESULT,
            FeatureId.ACCEPTANCE_CRITERION, FeatureId.VERIFICATION_METHOD,
        }:
            raise ValueError("simple observation requires a simple feature family")
        _check_refs(self.evidence_refs)


@dataclass(frozen=True, slots=True)
class VagueTermOccurrence:
    feature_id: FeatureId
    vocabulary_id: str
    matched_literal: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.feature_id is not FeatureId.VAGUE_TERM_OCCURRENCE:
            raise ValueError("vague-term observation requires vague_term_occurrence feature_id")
        if self.vocabulary_id != "uk_vague_terms_v1":
            raise ValueError("MVP vague-term occurrence requires uk_vague_terms_v1")
        # Canonical literals are a provenance label, not the source spelling.
        if self.matched_literal not in {
            "в реальному часі", "у реальному часі", "реальний час", "швидко",
            "швидкою", "зручною", "надійною", "надійно",
            "надійний захист", "надійно захищені",
        }:
            raise ValueError("matched_literal must be an approved canonical seed literal")
        _check_refs(self.evidence_refs)


@dataclass(frozen=True, slots=True)
class RequirementFeatures:
    condition_contexts: FeatureDetectionOutcome[FeatureObservation]
    expected_results: FeatureDetectionOutcome[FeatureObservation]
    acceptance_criteria: FeatureDetectionOutcome[FeatureObservation]
    quantitative_constraints: FeatureDetectionOutcome[QuantitativeConstraintObservation]
    verification_methods: FeatureDetectionOutcome[FeatureObservation]
    vague_term_occurrences: FeatureDetectionOutcome[VagueTermOccurrence]

    def __post_init__(self) -> None:
        families = (
            (self.condition_contexts, FeatureId.CONDITION_CONTEXT, FeatureObservation),
            (self.expected_results, FeatureId.EXPECTED_RESULT, FeatureObservation),
            (self.acceptance_criteria, FeatureId.ACCEPTANCE_CRITERION, FeatureObservation),
            (self.quantitative_constraints, FeatureId.QUANTITATIVE_CONSTRAINT, QuantitativeConstraintObservation),
            (self.verification_methods, FeatureId.VERIFICATION_METHOD, FeatureObservation),
            (self.vague_term_occurrences, FeatureId.VAGUE_TERM_OCCURRENCE, VagueTermOccurrence),
        )
        for outcome, feature_id, observation_type in families:
            if not isinstance(outcome, FeatureDetectionOutcome):
                raise TypeError("each family must be a FeatureDetectionOutcome")
            if outcome.feature_id is not feature_id:
                raise ValueError("outcome feature_id must match its family")
            if any(not isinstance(item, observation_type) for item in outcome.observations):
                raise TypeError("outcome observations must match their family type")

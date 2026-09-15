"""Accepted evidence registry returned with the six feature-family outcomes."""

from dataclasses import dataclass
from typing import Iterator

from .core import Evidence, FeatureId, Requirement
from .features import RequirementFeatures


def _accepted_evidence_refs(
    features: RequirementFeatures,
) -> Iterator[tuple[FeatureId, str]]:
    """Yield the approved family and reference for each accepted graph edge."""
    simple_outcomes = (
        features.condition_contexts, features.expected_results,
        features.acceptance_criteria, features.verification_methods,
    )
    for outcome in simple_outcomes:
        for observation in outcome.observations:
            for ref in observation.evidence_refs:
                yield outcome.feature_id, ref

    for observation in features.quantitative_constraints.observations:
        for ref in observation.evidence_refs:
            yield FeatureId.QUANTITATIVE_CONSTRAINT, ref
        for component in (
            observation.metric, observation.comparator, observation.value,
            observation.unit, observation.context,
        ):
            if component is not None:
                for ref in component.evidence_refs:
                    yield FeatureId.QUANTITATIVE_CONSTRAINT, ref

    for observation in features.vague_term_occurrences.observations:
        for ref in observation.evidence_refs:
            yield FeatureId.VAGUE_TERM_OCCURRENCE, ref


@dataclass(frozen=True, slots=True)
class RequirementExtractionResult:
    requirement: Requirement
    features: RequirementFeatures
    evidence: tuple[Evidence, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.requirement, Requirement):
            raise TypeError("requirement must be a Requirement")
        if not isinstance(self.features, RequirementFeatures):
            raise TypeError("features must be RequirementFeatures")
        if not isinstance(self.evidence, tuple) or any(
            not isinstance(item, Evidence) for item in self.evidence
        ):
            raise TypeError("evidence must be a tuple of Evidence")

        evidence_by_id: dict[str, Evidence] = {}
        for item in self.evidence:
            if item.requirement_id != self.requirement.id:
                raise ValueError("evidence requirement_id must match requirement.id")
            if not 0 <= item.start_offset <= item.end_offset <= len(self.requirement.text):
                raise ValueError("evidence offsets must fall within Requirement.text")
            if self.requirement.text[item.start_offset:item.end_offset] != item.text:
                raise ValueError("evidence text must round-trip to Requirement.text")
            if item.evidence_id in evidence_by_id:
                raise ValueError("duplicate evidence_id in extraction result")
            evidence_by_id[item.evidence_id] = item

        for feature_id, ref in _accepted_evidence_refs(self.features):
            item = evidence_by_id.get(ref)
            if item is None:
                raise ValueError(f"dangling accepted evidence_ref: {ref!r}")
            if item.feature_id is not feature_id:
                raise ValueError(
                    f"accepted evidence_ref {ref!r} must match {feature_id.value} feature family"
                )

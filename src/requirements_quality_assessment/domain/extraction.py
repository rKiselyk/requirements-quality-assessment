"""Accepted evidence registry returned with the six feature-family outcomes."""

from dataclasses import dataclass
from typing import Iterator

from .core import Evidence, Requirement
from .features import RequirementFeatures


def _accepted_evidence_refs(features: RequirementFeatures) -> Iterator[str]:
    """Traverse only approved observation and quantitative component references."""
    simple_outcomes = (
        features.condition_contexts, features.expected_results,
        features.acceptance_criteria, features.verification_methods,
    )
    for outcome in simple_outcomes:
        for observation in outcome.observations:
            yield from observation.evidence_refs

    for observation in features.quantitative_constraints.observations:
        yield from observation.evidence_refs
        for component in (
            observation.metric, observation.comparator, observation.value,
            observation.unit, observation.context,
        ):
            if component is not None:
                yield from component.evidence_refs

    for observation in features.vague_term_occurrences.observations:
        yield from observation.evidence_refs


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

        evidence_ids: set[str] = set()
        for item in self.evidence:
            if item.requirement_id != self.requirement.id:
                raise ValueError("evidence requirement_id must match requirement.id")
            if self.requirement.text[item.start_offset:item.end_offset] != item.text:
                raise ValueError("evidence text must round-trip to Requirement.text")
            if item.evidence_id in evidence_ids:
                raise ValueError("duplicate evidence_id in extraction result")
            evidence_ids.add(item.evidence_id)

        for ref in _accepted_evidence_refs(self.features):
            if ref not in evidence_ids:
                raise ValueError(f"dangling accepted evidence_ref: {ref!r}")

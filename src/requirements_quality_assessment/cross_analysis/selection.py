"""Exhaustive deterministic observation-pair selection for QB-v0.1.

Selection materializes the complete cross-requirement comparison universe.  It
does not decide applicability, normalize operands, compare bounds, or assign a
scientific disposition.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .domain import (
    AssessmentSnapshotId,
    CrossObservationRef,
    RequirementOrderKey,
    SnapshotCountManifest,
    SnapshotRequirementManifest,
)
from .projection import CrossRequirementProjection


@dataclass(frozen=True, slots=True, order=True)
class CrossCandidateOrderKey:
    """Stable source-order identity of one Cartesian-product member."""

    earlier_requirement: RequirementOrderKey
    later_requirement: RequirementOrderKey
    left_observation_index: int
    right_observation_index: int

    def __post_init__(self) -> None:
        if not isinstance(self.earlier_requirement, RequirementOrderKey):
            raise TypeError("earlier_requirement must be a RequirementOrderKey")
        if not isinstance(self.later_requirement, RequirementOrderKey):
            raise TypeError("later_requirement must be a RequirementOrderKey")
        if self.earlier_requirement.source_order >= self.later_requirement.source_order:
            raise ValueError("candidate requirements must be distinct and in source order")
        for value, name in (
            (self.left_observation_index, "left_observation_index"),
            (self.right_observation_index, "right_observation_index"),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")
            if value < 0:
                raise ValueError(f"{name} must be non-negative")


@dataclass(frozen=True, slots=True)
class CrossObservationPairCandidate:
    """One non-scientific candidate for later IMP-06 assessment."""

    snapshot_id: AssessmentSnapshotId
    earlier_requirement: RequirementOrderKey
    later_requirement: RequirementOrderKey
    left: CrossObservationRef
    right: CrossObservationRef
    order_key: CrossCandidateOrderKey = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, AssessmentSnapshotId):
            raise TypeError("snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.earlier_requirement, RequirementOrderKey):
            raise TypeError("earlier_requirement must be a RequirementOrderKey")
        if not isinstance(self.later_requirement, RequirementOrderKey):
            raise TypeError("later_requirement must be a RequirementOrderKey")
        if not isinstance(self.left, CrossObservationRef):
            raise TypeError("left must be a CrossObservationRef")
        if not isinstance(self.right, CrossObservationRef):
            raise TypeError("right must be a CrossObservationRef")
        if self.left.requirement_id != self.earlier_requirement.requirement_id:
            raise ValueError("left observation must belong to the earlier requirement")
        if self.right.requirement_id != self.later_requirement.requirement_id:
            raise ValueError("right observation must belong to the later requirement")

        key = CrossCandidateOrderKey(
            earlier_requirement=self.earlier_requirement,
            later_requirement=self.later_requirement,
            left_observation_index=self.left.observation_index,
            right_observation_index=self.right.observation_index,
        )
        object.__setattr__(self, "order_key", key)

    @property
    def participants(self) -> tuple[RequirementOrderKey, RequirementOrderKey]:
        """Return the exact participant shape consumed by later pair assessment."""

        return (self.earlier_requirement, self.later_requirement)

    @property
    def observation_refs(self) -> tuple[CrossObservationRef, CrossObservationRef]:
        """Return the ordered observation-ref pair without resolving its values."""

        return (self.left, self.right)


def _validated_requirements(
    projection: CrossRequirementProjection,
) -> tuple[SnapshotRequirementManifest, ...]:
    if not isinstance(projection, CrossRequirementProjection):
        raise TypeError("projection must be a CrossRequirementProjection")

    snapshot = projection.snapshot
    if projection.snapshot_id != projection.resolver.snapshot_id:
        raise ValueError("projection snapshot and resolver identities must match")
    projection.resolver.assert_snapshot(snapshot)

    requirements = projection.requirements
    if not isinstance(requirements, tuple) or any(
        not isinstance(item, SnapshotRequirementManifest) for item in requirements
    ):
        raise TypeError("projection requirements must be snapshot requirement manifests")
    if tuple(item.source_order for item in requirements) != tuple(range(len(requirements))):
        raise ValueError("projection requirements must be in contiguous source order")
    if len({item.requirement_id for item in requirements}) != len(requirements):
        raise ValueError("projection requirement IDs must be unique")
    if snapshot.counts != SnapshotCountManifest.from_requirements(requirements):
        raise ValueError("projection count/order manifest does not match requirements")
    if AssessmentSnapshotId.from_bytes(snapshot.canonical_bytes()) != snapshot.snapshot_id:
        raise ValueError("projection snapshot identity does not match its canonical content")

    for requirement in requirements:
        expected_indexes = tuple(range(len(requirement.observations)))
        actual_indexes = tuple(
            observation.ref.observation_index
            for observation in requirement.observations
        )
        if actual_indexes != expected_indexes:
            raise ValueError("projection observations must be in contiguous source order")
        if any(
            observation.ref.requirement_id != requirement.requirement_id
            for observation in requirement.observations
        ):
            raise ValueError("projection observations must have their requirement owner")

    return requirements


class ExhaustivePairSelector:
    """Enumerate every cross-requirement observation pair exactly once."""

    def candidate_count(self, projection: CrossRequirementProjection) -> int:
        """Return ``sum(i < j, O_i * O_j)`` for the validated projection."""

        requirements = _validated_requirements(projection)
        return sum(
            len(left.observations) * len(right.observations)
            for left_index, left in enumerate(requirements)
            for right in requirements[left_index + 1 :]
        )

    def select(
        self,
        projection: CrossRequirementProjection,
    ) -> tuple[CrossObservationPairCandidate, ...]:
        """Materialize the approved ``i, j, left observation, right observation`` order."""

        requirements = _validated_requirements(projection)
        candidates = tuple(
            CrossObservationPairCandidate(
                snapshot_id=projection.snapshot_id,
                earlier_requirement=earlier.order_key,
                later_requirement=later.order_key,
                left=left.ref,
                right=right.ref,
            )
            for earlier_index, earlier in enumerate(requirements)
            for later in requirements[earlier_index + 1 :]
            for left in earlier.observations
            for right in later.observations
        )

        expected_count = sum(
            len(left.observations) * len(right.observations)
            for left_index, left in enumerate(requirements)
            for right in requirements[left_index + 1 :]
        )
        keys = tuple(candidate.order_key for candidate in candidates)
        if len(candidates) != expected_count:
            raise RuntimeError("exhaustive selector omitted a conceptual candidate")
        if len(set(keys)) != len(keys):
            raise RuntimeError("exhaustive selector emitted a duplicate candidate")
        if keys != tuple(sorted(keys)):
            raise RuntimeError("exhaustive selector emitted non-deterministic order")

        return candidates


__all__ = [
    "CrossCandidateOrderKey",
    "CrossObservationPairCandidate",
    "ExhaustivePairSelector",
]

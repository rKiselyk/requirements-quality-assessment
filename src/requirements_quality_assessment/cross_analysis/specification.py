"""Immutable composition boundary for local and QB specification results.

This module deliberately composes the two independently calculated results.
It does not derive an overall value or reinterpret either result.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..domain import RequirementAssessmentRecord, SpecificationQualityProfile
from .domain import (
    AssessmentSnapshotId,
    CrossRequirementResult,
    QbConsistencyAssessment,
    QbMaterialityResult,
)
from .projection import CrossEvidenceResolver, CrossRequirementProjection


def _quality_profile_population(profile: SpecificationQualityProfile) -> int:
    counts = (
        profile.completeness.total_count,
        profile.verifiability.total_count,
        profile.unambiguity.total_count,
    )
    if len(set(counts)) != 1:
        raise ValueError(
            "quality-profile characteristics must describe one source population"
        )
    return counts[0]


@dataclass(frozen=True, slots=True)
class SpecificationAssessment:
    """The unchanged local profile beside the separate QB assessment."""

    snapshot_id: AssessmentSnapshotId
    quality_profile: SpecificationQualityProfile
    qb_consistency: QbConsistencyAssessment

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, AssessmentSnapshotId):
            raise TypeError("snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.quality_profile, SpecificationQualityProfile):
            raise TypeError("quality_profile must be a SpecificationQualityProfile")
        if not isinstance(self.qb_consistency, QbConsistencyAssessment):
            raise TypeError("qb_consistency must be a QbConsistencyAssessment")
        if self.qb_consistency.snapshot_id != self.snapshot_id:
            raise ValueError(
                "SpecificationAssessment and QB consistency cannot cross snapshots"
            )

        local_population = _quality_profile_population(self.quality_profile)
        qb_population = self.qb_consistency.observability.total_requirement_count
        if local_population != qb_population:
            raise ValueError(
                "local and QB results must describe the same source population"
            )


@dataclass(frozen=True, slots=True)
class SpecificationAssessmentResult:
    """Finished application output retained for the later reporting layer."""

    records: tuple[RequirementAssessmentRecord, ...]
    specification_assessment: SpecificationAssessment
    projection: CrossRequirementProjection
    cross_results: tuple[CrossRequirementResult, ...]
    materiality: QbMaterialityResult

    def __post_init__(self) -> None:
        if not isinstance(self.records, tuple) or any(
            not isinstance(item, RequirementAssessmentRecord) for item in self.records
        ):
            raise TypeError("records must be a tuple of RequirementAssessmentRecord values")
        if not isinstance(self.specification_assessment, SpecificationAssessment):
            raise TypeError(
                "specification_assessment must be a SpecificationAssessment"
            )
        if not isinstance(self.projection, CrossRequirementProjection):
            raise TypeError("projection must be a CrossRequirementProjection")
        if not isinstance(self.cross_results, tuple) or any(
            not isinstance(item, CrossRequirementResult)
            for item in self.cross_results
        ):
            raise TypeError(
                "cross_results must be a tuple of CrossRequirementResult values"
            )
        if not isinstance(self.materiality, QbMaterialityResult):
            raise TypeError("materiality must be a QbMaterialityResult")

        snapshot_id = self.projection.snapshot_id
        if self.specification_assessment.snapshot_id != snapshot_id:
            raise ValueError("assessment and projection cannot cross snapshots")
        if self.materiality.snapshot_id != snapshot_id:
            raise ValueError("materiality result and projection cannot cross snapshots")
        if any(item.snapshot_id != snapshot_id for item in self.cross_results):
            raise ValueError("cross results and projection cannot cross snapshots")

        manifests = self.projection.requirements
        if len(self.records) != len(manifests):
            raise ValueError("records and projection must describe the same source set")
        if (
            self.specification_assessment.qb_consistency.observability.total_requirement_count
            != len(manifests)
        ):
            raise ValueError(
                "QB assessment and projection must describe the same source population"
            )
        for source_order, (record, manifest) in enumerate(
            zip(self.records, manifests, strict=True)
        ):
            requirement = record.extraction_result.requirement
            if (
                manifest.source_order != source_order
                or manifest.requirement_id != requirement.id
                or manifest.source_line != requirement.source_line
            ):
                raise ValueError(
                    "records and projection must preserve one ordered source set"
                )
            if (
                self.projection.resolver.resolve_requirement(requirement.id)
                is not requirement
            ):
                raise ValueError(
                    "projection resolver must retain the exact source requirement"
                )

        order_keys = tuple(item.order_key for item in self.cross_results)
        if order_keys != tuple(sorted(order_keys)):
            raise ValueError("cross results must preserve canonical deterministic order")

        consistency = self.specification_assessment.qb_consistency
        if (
            tuple(item.result_id for item in self.cross_results)
            != consistency.cross_result_ids
        ):
            raise ValueError(
                "cross results must be the exact ordered QB aggregation inputs"
            )
        if (
            tuple(item.diagnostic_ref for item in self.materiality.audit_records)
            != consistency.materiality_diagnostic_refs
        ):
            raise ValueError(
                "materiality audits must be the exact QB aggregation inputs"
            )

    @property
    def snapshot_id(self) -> AssessmentSnapshotId:
        return self.specification_assessment.snapshot_id

    @property
    def resolver(self) -> CrossEvidenceResolver:
        """Expose the snapshot-scoped Evidence resolver needed by IMP-10."""

        return self.projection.resolver


__all__ = ["SpecificationAssessment", "SpecificationAssessmentResult"]

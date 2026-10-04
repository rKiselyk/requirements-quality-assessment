"""Thin application sequencing for the complete IMP-09 assessment pipeline."""

from __future__ import annotations

from ..aggregator import SpecificationQualityAggregator
from ..assessor import RequirementQualityAssessor
from ..domain import Requirement, RequirementAssessmentRecord
from ..extractor import BaselineFeatureExtractor
from .aggregation import QbConsistencyAggregator
from .comparison import QbObservationPairAssessor
from .materiality import QbMaterialityClassifier
from .projection import CrossRequirementProjector
from .selection import ExhaustivePairSelector
from .specification import SpecificationAssessment, SpecificationAssessmentResult


def _validate_records(
    records: tuple[RequirementAssessmentRecord, ...],
) -> None:
    if not isinstance(records, tuple):
        raise TypeError("records must be an immutable ordered tuple")
    if any(not isinstance(item, RequirementAssessmentRecord) for item in records):
        raise TypeError("records must contain RequirementAssessmentRecord values")

    # Re-run the accepted record boundary validation so corrupted/stale objects
    # cannot pass merely because they were valid at some earlier construction.
    for record in records:
        RequirementAssessmentRecord(
            record.extraction_result,
            record.quality_profile,
            record.trace,
        )

    requirements = tuple(item.extraction_result.requirement for item in records)
    requirement_ids = tuple(item.id for item in requirements)
    if len(requirement_ids) != len(set(requirement_ids)):
        raise ValueError("records must contain unique requirement IDs")
    source_lines = tuple(item.source_line for item in requirements)
    if any(right <= left for left, right in zip(source_lines, source_lines[1:])):
        raise ValueError("records must be in strict source-line order")


class SpecificationAssessmentService:
    """Sequence accepted local and cross components without owning science."""

    def __init__(
        self,
        *,
        quality_aggregator=None,
        projector=None,
        materiality_classifier=None,
        pair_selector=None,
        pair_assessor=None,
        consistency_aggregator=None,
    ) -> None:
        self._quality_aggregator = (
            SpecificationQualityAggregator()
            if quality_aggregator is None
            else quality_aggregator
        )
        self._projector = (
            CrossRequirementProjector() if projector is None else projector
        )
        self._materiality_classifier = (
            QbMaterialityClassifier()
            if materiality_classifier is None
            else materiality_classifier
        )
        self._pair_selector = (
            ExhaustivePairSelector() if pair_selector is None else pair_selector
        )
        self._pair_assessor = (
            QbObservationPairAssessor() if pair_assessor is None else pair_assessor
        )
        self._consistency_aggregator = (
            QbConsistencyAggregator()
            if consistency_aggregator is None
            else consistency_aggregator
        )

    def assess(
        self,
        records: tuple[RequirementAssessmentRecord, ...],
    ) -> SpecificationAssessmentResult:
        """Assess one already-completed ordered local record collection."""

        _validate_records(records)

        quality_profile = self._quality_aggregator.aggregate(
            tuple(record.quality_profile for record in records)
        )
        projection = self._projector.project(records)
        materiality = self._materiality_classifier.classify(projection)
        candidates = self._pair_selector.select(projection)
        cross_results = tuple(
            self._pair_assessor.assess(candidate, projection)
            for candidate in candidates
        )
        qb_consistency = self._consistency_aggregator.aggregate(
            projection.snapshot,
            cross_results,
            materiality,
        )
        assessment = SpecificationAssessment(
            snapshot_id=projection.snapshot_id,
            quality_profile=quality_profile,
            qb_consistency=qb_consistency,
        )
        return SpecificationAssessmentResult(
            records=records,
            specification_assessment=assessment,
            projection=projection,
            cross_results=cross_results,
            materiality=materiality,
        )


def assess_specification(
    requirements: tuple[Requirement, ...],
    *,
    extractor=None,
    assessor=None,
    specification_service=None,
) -> SpecificationAssessmentResult:
    """Run the accepted pipeline while keeping delivery adapters orchestration-only."""

    if not isinstance(requirements, tuple):
        raise TypeError("requirements must be an immutable ordered tuple")
    production_types = all(isinstance(item, Requirement) for item in requirements)
    if not production_types and extractor is None and assessor is None:
        raise TypeError("requirements must contain Requirement values")

    active_extractor = BaselineFeatureExtractor() if extractor is None else extractor
    active_assessor = RequirementQualityAssessor() if assessor is None else assessor
    active_service = (
        SpecificationAssessmentService()
        if specification_service is None
        else specification_service
    )
    records = tuple(
        active_assessor.assess_record(active_extractor.extract(requirement))
        for requirement in requirements
    )
    return active_service.assess(records)


__all__ = ["SpecificationAssessmentService", "assess_specification"]

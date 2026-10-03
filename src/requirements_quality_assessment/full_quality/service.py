"""Calculation-free TC-01 composition service."""

from .domain import (
    EXTERNAL_PROPERTY_IDS,
    ExternalPropertyAssessment,
    FullRequirementQualityProfile,
)
from ..domain import RequirementAssessmentRecord
from ..metrics import ArtifactRef, AssessmentRef, RequirementSubjectRef


class FullRequirementQualityProfileComposer:
    """Compose an accepted C/V/U record with all six explicit external inputs."""

    def compose(
        self,
        record: RequirementAssessmentRecord,
        *,
        artifact_ref: ArtifactRef,
        assessment_ref: AssessmentRef,
        external_assessments: tuple[ExternalPropertyAssessment, ...],
    ) -> FullRequirementQualityProfile:
        if not isinstance(record, RequirementAssessmentRecord):
            raise TypeError("record must be a RequirementAssessmentRecord")
        if not isinstance(external_assessments, tuple) or any(
            not isinstance(item, ExternalPropertyAssessment)
            for item in external_assessments
        ):
            raise TypeError("external_assessments must be a tuple of external assessments")
        property_ids = tuple(item.property_id for item in external_assessments)
        if len(property_ids) != len(set(property_ids)):
            raise ValueError("external assessments must not contain duplicate properties")
        if set(property_ids) != set(EXTERNAL_PROPERTY_IDS):
            raise ValueError("external assessments must contain exactly the six external properties")

        requirement = record.extraction_result.requirement
        requirement_ref = RequirementSubjectRef(
            artifact_ref,
            requirement.id,
            requirement.source_line,
        )
        by_property = {item.property_id: item for item in external_assessments}
        return FullRequirementQualityProfile(
            artifact_ref=artifact_ref,
            assessment_ref=assessment_ref,
            requirement_ref=requirement_ref,
            automatic_record=record,
            singularity=by_property[EXTERNAL_PROPERTY_IDS[0]],
            presentation_conformance=by_property[EXTERNAL_PROPERTY_IDS[1]],
            correctness=by_property[EXTERNAL_PROPERTY_IDS[2]],
            feasibility=by_property[EXTERNAL_PROPERTY_IDS[3]],
            necessity=by_property[EXTERNAL_PROPERTY_IDS[4]],
            relevance=by_property[EXTERNAL_PROPERTY_IDS[5]],
        )


def compose_full_requirement_quality_profile(
    record: RequirementAssessmentRecord,
    *,
    artifact_ref: ArtifactRef,
    assessment_ref: AssessmentRef,
    external_assessments: tuple[ExternalPropertyAssessment, ...],
) -> FullRequirementQualityProfile:
    return FullRequirementQualityProfileComposer().compose(
        record,
        artifact_ref=artifact_ref,
        assessment_ref=assessment_ref,
        external_assessments=external_assessments,
    )


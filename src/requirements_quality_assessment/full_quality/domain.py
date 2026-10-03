"""TC-01 immutable nine-property requirement-quality representation.

The module composes accepted C/V/U results with externally supplied judgments.
It defines no calculation, normalization, aggregation, or overall score.
"""

from dataclasses import dataclass
from enum import Enum

from ..domain import (
    CharacteristicAssessment,
    CharacteristicId,
    CharacteristicTrace,
    RequirementAssessmentRecord,
)
from ..metrics import ArtifactRef, AssessmentRef, ContractRef, RequirementSubjectRef, RuleRef


def _require_identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


class RequirementQualityPropertyId(str, Enum):
    COMPLETENESS = "COMPLETENESS"
    VERIFIABILITY = "VERIFIABILITY"
    UNAMBIGUITY = "UNAMBIGUITY"
    SINGULARITY = "SINGULARITY"
    PRESENTATION_CONFORMANCE = "PRESENTATION_CONFORMANCE"
    CORRECTNESS = "CORRECTNESS"
    FEASIBILITY = "FEASIBILITY"
    NECESSITY = "NECESSITY"
    RELEVANCE = "RELEVANCE"


AUTOMATIC_PROPERTY_IDS = (
    RequirementQualityPropertyId.COMPLETENESS,
    RequirementQualityPropertyId.VERIFIABILITY,
    RequirementQualityPropertyId.UNAMBIGUITY,
)

EXTERNAL_PROPERTY_IDS = (
    RequirementQualityPropertyId.SINGULARITY,
    RequirementQualityPropertyId.PRESENTATION_CONFORMANCE,
    RequirementQualityPropertyId.CORRECTNESS,
    RequirementQualityPropertyId.FEASIBILITY,
    RequirementQualityPropertyId.NECESSITY,
    RequirementQualityPropertyId.RELEVANCE,
)


class PropertyAssessmentOrigin(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    EXTERNAL_EXPERT = "EXTERNAL_EXPERT"


class ExternalAssessmentState(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNKNOWN = "UNKNOWN"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True, slots=True, order=True)
class ExternalAssessmentSourceRef:
    """Versioned identity of the expert, process, or external source."""

    source_id: str
    source_version: str

    def __post_init__(self) -> None:
        _require_identifier(self.source_id, "source_id")
        _require_identifier(self.source_version, "source_version")


@dataclass(frozen=True, slots=True, order=True)
class ExternalPropertyJudgment:
    """Opaque contract-defined judgment; deliberately not a numeric scale."""

    judgment_id: str

    def __post_init__(self) -> None:
        _require_identifier(self.judgment_id, "judgment_id")


@dataclass(frozen=True, slots=True)
class ExternalAssessmentProvenance:
    source_ref: ExternalAssessmentSourceRef
    requirement_ref: RequirementSubjectRef
    artifact_ref: ArtifactRef
    assessment_contract_ref: ContractRef
    assessment_rule_ref: RuleRef

    def __post_init__(self) -> None:
        if not isinstance(self.source_ref, ExternalAssessmentSourceRef):
            raise TypeError("source_ref must be an ExternalAssessmentSourceRef")
        if not isinstance(self.requirement_ref, RequirementSubjectRef):
            raise TypeError("requirement_ref must be a RequirementSubjectRef")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if not isinstance(self.assessment_contract_ref, ContractRef):
            raise TypeError("assessment_contract_ref must be a ContractRef")
        if not isinstance(self.assessment_rule_ref, RuleRef):
            raise TypeError("assessment_rule_ref must be a RuleRef")
        if self.requirement_ref.artifact_ref != self.artifact_ref:
            raise ValueError("provenance requirement and artifact refs must agree")


@dataclass(frozen=True, slots=True)
class ExternalPropertyAssessment:
    property_id: RequirementQualityPropertyId
    state: ExternalAssessmentState
    judgment: ExternalPropertyJudgment | None
    provenance: ExternalAssessmentProvenance
    explanation: str

    def __post_init__(self) -> None:
        if self.property_id not in EXTERNAL_PROPERTY_IDS:
            raise ValueError("property_id must identify an externally assessed property")
        if not isinstance(self.state, ExternalAssessmentState):
            raise TypeError("state must be an ExternalAssessmentState")
        if not isinstance(self.provenance, ExternalAssessmentProvenance):
            raise TypeError("provenance must be ExternalAssessmentProvenance")
        _require_identifier(self.explanation, "explanation")
        if self.state is ExternalAssessmentState.AVAILABLE:
            if not isinstance(self.judgment, ExternalPropertyJudgment):
                raise ValueError("AVAILABLE requires an ExternalPropertyJudgment")
        elif self.judgment is not None:
            raise ValueError(f"{self.state.value} requires judgment=None")


_AUTOMATIC_CHARACTERISTICS = {
    RequirementQualityPropertyId.COMPLETENESS: CharacteristicId.COMPLETENESS,
    RequirementQualityPropertyId.VERIFIABILITY: CharacteristicId.VERIFIABILITY,
    RequirementQualityPropertyId.UNAMBIGUITY: CharacteristicId.UNAMBIGUITY,
}


@dataclass(frozen=True, slots=True)
class RequirementPropertyAssessment:
    """One typed slot in a full profile, preserving its source object."""

    property_id: RequirementQualityPropertyId
    origin: PropertyAssessmentOrigin
    automatic_assessment: CharacteristicAssessment | None = None
    automatic_trace: CharacteristicTrace | None = None
    external_assessment: ExternalPropertyAssessment | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.property_id, RequirementQualityPropertyId):
            raise TypeError("property_id must be a RequirementQualityPropertyId")
        if not isinstance(self.origin, PropertyAssessmentOrigin):
            raise TypeError("origin must be a PropertyAssessmentOrigin")
        if self.origin is PropertyAssessmentOrigin.AUTOMATIC:
            if self.property_id not in AUTOMATIC_PROPERTY_IDS:
                raise ValueError("automatic origin requires a C/V/U property")
            if not isinstance(self.automatic_assessment, CharacteristicAssessment):
                raise TypeError("automatic origin requires CharacteristicAssessment")
            if not isinstance(self.automatic_trace, CharacteristicTrace):
                raise TypeError("automatic origin requires CharacteristicTrace")
            expected = _AUTOMATIC_CHARACTERISTICS[self.property_id]
            if self.automatic_assessment.characteristic_id is not expected:
                raise ValueError("automatic assessment identity must match property_id")
            if self.automatic_trace.characteristic_id is not expected:
                raise ValueError("automatic trace identity must match property_id")
            if self.external_assessment is not None:
                raise ValueError("automatic property cannot carry an external assessment")
        else:
            if self.property_id not in EXTERNAL_PROPERTY_IDS:
                raise ValueError("external origin requires an external property")
            if self.automatic_assessment is not None or self.automatic_trace is not None:
                raise ValueError("external property cannot carry automatic data")
            if not isinstance(self.external_assessment, ExternalPropertyAssessment):
                raise TypeError("external origin requires ExternalPropertyAssessment")
            if self.external_assessment.property_id is not self.property_id:
                raise ValueError("external assessment identity must match property_id")


@dataclass(frozen=True, slots=True)
class FullRequirementQualityProfile:
    """Exactly nine independent property results with no integrated scalar."""

    artifact_ref: ArtifactRef
    assessment_ref: AssessmentRef
    requirement_ref: RequirementSubjectRef
    automatic_record: RequirementAssessmentRecord
    singularity: ExternalPropertyAssessment
    presentation_conformance: ExternalPropertyAssessment
    correctness: ExternalPropertyAssessment
    feasibility: ExternalPropertyAssessment
    necessity: ExternalPropertyAssessment
    relevance: ExternalPropertyAssessment

    def __post_init__(self) -> None:
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if not isinstance(self.assessment_ref, AssessmentRef):
            raise TypeError("assessment_ref must be an AssessmentRef")
        if self.assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("assessment_ref must name the profile artifact_ref")
        if not isinstance(self.requirement_ref, RequirementSubjectRef):
            raise TypeError("requirement_ref must be a RequirementSubjectRef")
        if self.requirement_ref.artifact_ref != self.artifact_ref:
            raise ValueError("requirement_ref must name the profile artifact_ref")
        if not isinstance(self.automatic_record, RequirementAssessmentRecord):
            raise TypeError("automatic_record must be a RequirementAssessmentRecord")
        requirement = self.automatic_record.extraction_result.requirement
        if (
            requirement.id != self.requirement_ref.requirement_id
            or requirement.source_line != self.requirement_ref.source_line
        ):
            raise ValueError("automatic record and profile requirement identities must agree")

        expected_slots = (
            ("singularity", RequirementQualityPropertyId.SINGULARITY),
            (
                "presentation_conformance",
                RequirementQualityPropertyId.PRESENTATION_CONFORMANCE,
            ),
            ("correctness", RequirementQualityPropertyId.CORRECTNESS),
            ("feasibility", RequirementQualityPropertyId.FEASIBILITY),
            ("necessity", RequirementQualityPropertyId.NECESSITY),
            ("relevance", RequirementQualityPropertyId.RELEVANCE),
        )
        seen: set[RequirementQualityPropertyId] = set()
        for field_name, expected_property in expected_slots:
            assessment = getattr(self, field_name)
            if not isinstance(assessment, ExternalPropertyAssessment):
                raise TypeError(f"{field_name} must be an ExternalPropertyAssessment")
            if assessment.property_id is not expected_property:
                raise ValueError(f"{field_name} carries the wrong property identity")
            if assessment.property_id in seen:
                raise ValueError("external properties must not be duplicated")
            seen.add(assessment.property_id)
            provenance = assessment.provenance
            if provenance.artifact_ref != self.artifact_ref:
                raise ValueError("external assessment artifact identity must match profile")
            if provenance.requirement_ref != self.requirement_ref:
                raise ValueError("external assessment requirement identity must match profile")

    @property
    def completeness(self) -> CharacteristicAssessment:
        return self.automatic_record.quality_profile.completeness

    @property
    def verifiability(self) -> CharacteristicAssessment:
        return self.automatic_record.quality_profile.verifiability

    @property
    def unambiguity(self) -> CharacteristicAssessment:
        return self.automatic_record.quality_profile.unambiguity

    @property
    def properties(self) -> tuple[RequirementPropertyAssessment, ...]:
        automatic_assessments = (
            self.completeness,
            self.verifiability,
            self.unambiguity,
        )
        automatic = tuple(
            RequirementPropertyAssessment(
                property_id,
                PropertyAssessmentOrigin.AUTOMATIC,
                assessment,
                trace,
            )
            for property_id, assessment, trace in zip(
                AUTOMATIC_PROPERTY_IDS,
                automatic_assessments,
                self.automatic_record.trace.characteristics,
                strict=True,
            )
        )
        external_assessments = (
            self.singularity,
            self.presentation_conformance,
            self.correctness,
            self.feasibility,
            self.necessity,
            self.relevance,
        )
        external = tuple(
            RequirementPropertyAssessment(
                assessment.property_id,
                PropertyAssessmentOrigin.EXTERNAL_EXPERT,
                external_assessment=assessment,
            )
            for assessment in external_assessments
        )
        return automatic + external

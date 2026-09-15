"""Detection processing state, separate from criterion applicability."""

from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from .core import FeatureId, validate_span


class DetectionStatus(str, Enum):
    DETECTED = "DETECTED"
    NOT_DETECTED = "NOT_DETECTED"
    UNRESOLVED = "UNRESOLVED"


class DetectionProcessingStatus(str, Enum):
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"


@dataclass(frozen=True, slots=True)
class DiagnosticSpan:
    text: str
    start_offset: int
    end_offset: int

    def __post_init__(self) -> None:
        validate_span(self.text, self.start_offset, self.end_offset)


@dataclass(frozen=True, slots=True)
class DetectionDiagnostic:
    code: str
    explanation: str
    rule_id: str
    candidate_span: DiagnosticSpan | None = None


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class FeatureDetectionOutcome(Generic[T]):
    feature_id: FeatureId
    observations: tuple[T, ...]
    processing_status: DetectionProcessingStatus
    diagnostics: tuple[DetectionDiagnostic, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.feature_id, FeatureId):
            raise TypeError("feature_id must be an approved FeatureId")
        if not isinstance(self.observations, tuple) or not isinstance(self.diagnostics, tuple):
            raise TypeError("observations and diagnostics must be tuples")
        if not isinstance(self.processing_status, DetectionProcessingStatus):
            raise TypeError("processing_status must be a DetectionProcessingStatus")
        if any(not isinstance(item, DetectionDiagnostic) for item in self.diagnostics):
            raise TypeError("diagnostics must contain DetectionDiagnostic instances")
        if self.processing_status is DetectionProcessingStatus.COMPLETE and self.diagnostics:
            raise ValueError("complete detection cannot have diagnostics")
        if self.processing_status is DetectionProcessingStatus.INCOMPLETE and not self.diagnostics:
            raise ValueError("incomplete detection requires diagnostics")
        if any(getattr(item, "feature_id", None) is not self.feature_id for item in self.observations):
            raise ValueError("every observation must match the outcome feature_id")

    @property
    def status(self) -> DetectionStatus:
        if self.observations:
            return DetectionStatus.DETECTED
        if self.processing_status is DetectionProcessingStatus.COMPLETE:
            return DetectionStatus.NOT_DETECTED
        return DetectionStatus.UNRESOLVED

"""Source requirement and accepted, source-aligned evidence contracts."""

from dataclasses import dataclass
from enum import Enum


class FeatureId(str, Enum):
    CONDITION_CONTEXT = "condition_context"
    EXPECTED_RESULT = "expected_result"
    ACCEPTANCE_CRITERION = "acceptance_criterion"
    QUANTITATIVE_CONSTRAINT = "quantitative_constraint"
    VERIFICATION_METHOD = "verification_method"
    VAGUE_TERM_OCCURRENCE = "vague_term_occurrence"


class CriterionApplicability(str, Enum):
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNKNOWN = "UNKNOWN"


def validate_span(text: str, start_offset: int, end_offset: int) -> None:
    if not isinstance(text, str):
        raise TypeError("span text must be a string")
    if not isinstance(start_offset, int) or not isinstance(end_offset, int):
        raise TypeError("span offsets must be integers")
    if start_offset < 0 or end_offset < start_offset:
        raise ValueError("span offsets must be nonnegative and ordered")
    if len(text) != end_offset - start_offset:
        raise ValueError("span text length must match its Unicode code-point extent")


@dataclass(frozen=True, slots=True)
class Requirement:
    id: str
    source_line: int
    text: str

    def __post_init__(self) -> None:
        if not isinstance(self.source_line, int) or self.source_line < 1:
            raise ValueError("source_line must be a positive integer")
        if not isinstance(self.text, str) or not self.text or self.text != self.text.strip():
            raise ValueError("text must be non-empty and already trimmed")


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    requirement_id: str
    feature_id: FeatureId
    text: str
    start_offset: int
    end_offset: int
    rule_id: str

    def __post_init__(self) -> None:
        validate_span(self.text, self.start_offset, self.end_offset)
        if not isinstance(self.feature_id, FeatureId):
            raise TypeError("feature_id must be an approved FeatureId")

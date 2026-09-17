"""Approved Section 7.16 characteristic/finding contracts; no scoring logic."""

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction


class CharacteristicId(str, Enum):
    COMPLETENESS = "COMPLETENESS"
    VERIFIABILITY = "VERIFIABILITY"
    UNAMBIGUITY = "UNAMBIGUITY"


class CharacteristicAssessmentState(str, Enum):
    COMPUTED = "COMPUTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNKNOWN = "UNKNOWN"


class FindingKind(str, Enum):
    SIGNAL = "SIGNAL"
    QUALITY_PROBLEM = "QUALITY_PROBLEM"


def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value)


@dataclass(frozen=True, slots=True)
class Finding:
    finding_id: str
    requirement_id: str
    characteristic_id: CharacteristicId
    kind: FindingKind
    code: str
    rule_id: str
    criterion_id: str | None
    evidence_refs: tuple[str, ...]
    explanation: str

    def __post_init__(self) -> None:
        for name in ("finding_id", "requirement_id", "code", "rule_id", "explanation"):
            if not _non_empty_str(getattr(self, name)):
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.characteristic_id, CharacteristicId):
            raise TypeError("characteristic_id must be an approved CharacteristicId")
        if not isinstance(self.kind, FindingKind):
            raise TypeError("kind must be an approved FindingKind")
        if self.criterion_id is not None and not _non_empty_str(self.criterion_id):
            raise ValueError("criterion_id must be None or a non-empty string")
        if not isinstance(self.evidence_refs, tuple) or any(
            not isinstance(ref, str) for ref in self.evidence_refs
        ):
            raise TypeError("evidence_refs must be a tuple of strings")


@dataclass(frozen=True, slots=True)
class CharacteristicAssessment:
    characteristic_id: CharacteristicId
    state: CharacteristicAssessmentState
    value: Fraction | None
    assessment_rule_id: str | None
    findings: tuple[Finding, ...]
    explanation: str

    def __post_init__(self) -> None:
        if not isinstance(self.characteristic_id, CharacteristicId):
            raise TypeError("characteristic_id must be an approved CharacteristicId")
        if not isinstance(self.state, CharacteristicAssessmentState):
            raise TypeError("state must be an approved CharacteristicAssessmentState")
        if not _non_empty_str(self.explanation):
            raise ValueError("explanation must be a non-empty string")
        if self.assessment_rule_id is not None and not _non_empty_str(self.assessment_rule_id):
            raise ValueError("assessment_rule_id must be None or a non-empty string")
        if not isinstance(self.findings, tuple) or any(
            not isinstance(finding, Finding) for finding in self.findings
        ):
            raise TypeError("findings must be a tuple of Finding")

        if self.state is CharacteristicAssessmentState.COMPUTED:
            if not isinstance(self.value, Fraction):
                raise ValueError("COMPUTED state requires a Fraction value")
            if not Fraction(0, 1) <= self.value <= Fraction(1, 1):
                raise ValueError("COMPUTED value must fall within [0, 1]")
            if self.assessment_rule_id is None:
                raise ValueError("COMPUTED state requires a non-null assessment_rule_id")
        elif self.value is not None:
            raise ValueError(f"{self.state.value} state requires value to be None")

        if (self.state is CharacteristicAssessmentState.NOT_APPLICABLE
                and any(finding.kind is FindingKind.QUALITY_PROBLEM for finding in self.findings)):
            raise ValueError("NOT_APPLICABLE state cannot carry a QUALITY_PROBLEM finding")

        seen_finding_ids: set[str] = set()
        for finding in self.findings:
            if finding.characteristic_id is not self.characteristic_id:
                raise ValueError("finding characteristic_id must match the assessment")
            if finding.finding_id in seen_finding_ids:
                raise ValueError("finding_id must be unique within an assessment")
            seen_finding_ids.add(finding.finding_id)

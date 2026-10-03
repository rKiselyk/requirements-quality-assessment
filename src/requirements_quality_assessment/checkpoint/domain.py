"""Immutable contracts for externally parameterized scalar checkpoints."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from ..dynamic_evidence import Applicability, FullModelStatus
from ..metrics import ArtifactRef, ContractRef, RuleRef, RuleVersionAuthority
from ..performance_efficiency import ProcessStateRef


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


CHECKPOINT_CONTRACT_REF = ContractRef("FULL-MODEL-V1.0-SCALAR-CHECKPOINT", "1")
CHECKPOINT_RULE_REF = RuleRef(
    "CHECKPOINT-SCALAR-PREDICATE-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)


class CheckpointComparator(str, Enum):
    GREATER_THAN_OR_EQUAL = ">="
    GREATER_THAN = ">"
    LESS_THAN_OR_EQUAL = "<="
    LESS_THAN = "<"
    EQUAL = "=="


class CheckpointOutcome(str, Enum):
    SATISFIED = "SATISFIED"
    NOT_SATISFIED = "NOT_SATISFIED"
    UNRESOLVED = "UNRESOLVED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class CheckpointReason(str, Enum):
    PREDICATE_TRUE = "PREDICATE_TRUE"
    PREDICATE_FALSE = "PREDICATE_FALSE"
    SOURCE_NOT_APPLICABLE = "SOURCE_NOT_APPLICABLE"
    SOURCE_VALUE_UNRESOLVED = "SOURCE_VALUE_UNRESOLVED"
    ARTIFACT_PROVENANCE_MISMATCH = "ARTIFACT_PROVENANCE_MISMATCH"
    PROCESS_STATE_PROVENANCE_MISMATCH = "PROCESS_STATE_PROVENANCE_MISMATCH"


@dataclass(frozen=True, slots=True, order=True)
class ThresholdPolicyRef:
    policy_id: str
    policy_version: str

    def __post_init__(self) -> None:
        _identifier(self.policy_id, "policy_id")
        _identifier(self.policy_version, "policy_version")


@dataclass(frozen=True, slots=True, order=True)
class PolicyProviderRef:
    provider_id: str
    provider_version: str

    def __post_init__(self) -> None:
        _identifier(self.provider_id, "provider_id")
        _identifier(self.provider_version, "provider_version")


@dataclass(frozen=True, slots=True, order=True)
class PolicySourceRef:
    source_id: str
    source_version: str

    def __post_init__(self) -> None:
        _identifier(self.source_id, "source_id")
        _identifier(self.source_version, "source_version")


@dataclass(frozen=True, slots=True)
class ThresholdPolicy:
    policy_id: str
    policy_version: str
    source_ref: PolicySourceRef
    provider_ref: PolicyProviderRef
    rationale: str
    comparator: CheckpointComparator
    threshold: Fraction
    governing_contract_ref: ContractRef

    def __post_init__(self) -> None:
        _identifier(self.policy_id, "policy_id")
        _identifier(self.policy_version, "policy_version")
        if not isinstance(self.source_ref, PolicySourceRef):
            raise TypeError("source_ref must be a PolicySourceRef")
        if not isinstance(self.provider_ref, PolicyProviderRef):
            raise TypeError("provider_ref must be a PolicyProviderRef")
        _identifier(self.rationale, "rationale")
        if not isinstance(self.comparator, CheckpointComparator):
            raise TypeError("comparator must be a CheckpointComparator")
        if not isinstance(self.threshold, Fraction):
            raise TypeError("threshold must be an exact Fraction")
        if not isinstance(self.governing_contract_ref, ContractRef):
            raise TypeError("governing_contract_ref must be a ContractRef")

    @property
    def ref(self) -> ThresholdPolicyRef:
        return ThresholdPolicyRef(self.policy_id, self.policy_version)


@dataclass(frozen=True, slots=True)
class SelectedCheckpointResult:
    """Lossless scalar selection; this record never recomputes its source result."""

    result_ref: object
    result_identity: str
    status: FullModelStatus
    applicability: Applicability
    exact_value: Fraction | None
    artifact_ref: ArtifactRef
    process_state_ref: ProcessStateRef
    governing_contract_or_rule_ref: ContractRef | RuleRef
    reason_codes: tuple[object, ...]
    provenance: tuple[object, ...]

    def __post_init__(self) -> None:
        if self.result_ref is None:
            raise ValueError("result_ref must not be None")
        _identifier(self.result_identity, "result_identity")
        if not isinstance(self.status, FullModelStatus):
            raise TypeError("status must be a FullModelStatus")
        if not isinstance(self.applicability, Applicability):
            raise TypeError("applicability must be an Applicability")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        if not isinstance(self.governing_contract_or_rule_ref, (ContractRef, RuleRef)):
            raise TypeError("governing result reference must be a ContractRef or RuleRef")
        if not isinstance(self.reason_codes, tuple) or any(
            item is None for item in self.reason_codes
        ):
            raise TypeError("reason_codes must be an immutable tuple")
        if not isinstance(self.provenance, tuple) or not self.provenance or any(
            item is None for item in self.provenance
        ):
            raise ValueError("selected result requires immutable source provenance")

        allowed_applicability = {
            FullModelStatus.AVAILABLE: {Applicability.APPLICABLE},
            FullModelStatus.NOT_APPLICABLE: {Applicability.NOT_APPLICABLE},
            FullModelStatus.UNKNOWN: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNAVAILABLE: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNRESOLVED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNSUPPORTED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
        }[self.status]
        if self.applicability not in allowed_applicability:
            raise ValueError("selected result status/applicability is inconsistent")
        if self.status is FullModelStatus.AVAILABLE:
            if not isinstance(self.exact_value, Fraction):
                raise ValueError("AVAILABLE selected result requires an exact Fraction")
        elif self.exact_value is not None:
            raise ValueError("non-AVAILABLE selected result cannot carry a value")


@dataclass(frozen=True, slots=True)
class CheckpointRequest:
    checkpoint_id: str
    checkpoint_version: str
    selected_result: SelectedCheckpointResult
    threshold_policy: ThresholdPolicy
    process_state_ref: ProcessStateRef
    artifact_ref: ArtifactRef

    def __post_init__(self) -> None:
        _identifier(self.checkpoint_id, "checkpoint_id")
        _identifier(self.checkpoint_version, "checkpoint_version")
        if not isinstance(self.selected_result, SelectedCheckpointResult):
            raise TypeError("selected_result must be a SelectedCheckpointResult")
        if not isinstance(self.threshold_policy, ThresholdPolicy):
            raise TypeError("threshold_policy must be explicitly supplied")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")


@dataclass(frozen=True, slots=True)
class CheckpointEvaluationProvenance:
    selected_result_ref: object
    selected_result_provenance: tuple[object, ...]
    threshold_policy_ref: ThresholdPolicyRef
    policy_source_ref: PolicySourceRef
    policy_provider_ref: PolicyProviderRef
    process_state_ref: ProcessStateRef
    artifact_ref: ArtifactRef
    governing_policy_contract_ref: ContractRef
    checkpoint_contract_ref: ContractRef
    evaluator_rule_ref: RuleRef


@dataclass(frozen=True, slots=True)
class CheckpointEvaluation:
    checkpoint_id: str
    checkpoint_version: str
    selected_result: SelectedCheckpointResult
    threshold_policy: ThresholdPolicy
    process_state_ref: ProcessStateRef
    artifact_ref: ArtifactRef
    outcome: CheckpointOutcome
    reason_codes: tuple[CheckpointReason, ...]
    checkpoint_contract_ref: ContractRef
    evaluator_rule_ref: RuleRef
    provenance: CheckpointEvaluationProvenance

    def __post_init__(self) -> None:
        _identifier(self.checkpoint_id, "checkpoint_id")
        _identifier(self.checkpoint_version, "checkpoint_version")
        if not isinstance(self.selected_result, SelectedCheckpointResult):
            raise TypeError("selected_result must be a SelectedCheckpointResult")
        if not isinstance(self.threshold_policy, ThresholdPolicy):
            raise TypeError("threshold_policy must be a ThresholdPolicy")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if not isinstance(self.outcome, CheckpointOutcome):
            raise TypeError("outcome must be a CheckpointOutcome")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes or any(
            not isinstance(item, CheckpointReason) for item in self.reason_codes
        ):
            raise TypeError("reason_codes must contain CheckpointReason values")
        if self.checkpoint_contract_ref != CHECKPOINT_CONTRACT_REF:
            raise ValueError("checkpoint evaluation requires the TC-04 contract")
        if self.evaluator_rule_ref != CHECKPOINT_RULE_REF:
            raise ValueError("checkpoint evaluation requires the TC-04 evaluator rule")
        if not isinstance(self.provenance, CheckpointEvaluationProvenance):
            raise TypeError("provenance must be CheckpointEvaluationProvenance")
        if (
            self.provenance.selected_result_ref != self.selected_result.result_ref
            or self.provenance.selected_result_provenance
            != self.selected_result.provenance
            or self.provenance.threshold_policy_ref != self.threshold_policy.ref
            or self.provenance.policy_source_ref != self.threshold_policy.source_ref
            or self.provenance.policy_provider_ref != self.threshold_policy.provider_ref
            or self.provenance.process_state_ref != self.process_state_ref
            or self.provenance.artifact_ref != self.artifact_ref
            or self.provenance.governing_policy_contract_ref
            != self.threshold_policy.governing_contract_ref
            or self.provenance.checkpoint_contract_ref != self.checkpoint_contract_ref
            or self.provenance.evaluator_rule_ref != self.evaluator_rule_ref
        ):
            raise ValueError("checkpoint evaluation and provenance must agree")


__all__ = [name for name in globals() if not name.startswith("_")]

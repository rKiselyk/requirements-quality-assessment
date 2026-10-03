"""Immutable domain records for the bounded Full Model v0.1 ``A_corr``.

Proposal records contain no replacement payload.  M3-09 may create a later
``APPLIED`` record version, but only from an externally supplied revision.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..defect_quality import (
    DEFECT_QUALITY_RISK_CONTRACT_REF,
    PROBLEM_RULE_REF,
    RELATION_RULE_REF,
    ConfirmedSupportedProblemId,
    ConfirmedSupportedProblemRef,
    DefectPopulationSnapshotRef,
    DefectQualityRelationRef,
    ProblemClaimResolutionRef,
)
from ..defect_quality.domain import (
    AssessmentSnapshotId,
    ComparisonKey,
    CrossEvidenceRef,
    CrossResultId,
)
from ..dynamic_evidence import Applicability, FullModelStatus
from ..metrics import (
    FULL_MODEL_CONTRACT_REF,
    ArtifactRef,
    AssessmentRef,
    ContractRef,
    RequirementSubjectRef,
    RuleRef,
    RuleVersionAuthority,
)
from ..performance_efficiency import ProcessStateRef
from ..risk import (
    RISK_MODEL_REF,
    RISK_PARAMETER_SET_REF,
    RISK_RULE_REF,
    BoundedRiskAssessmentId,
    BoundedRiskAssessmentRef,
    RiskModelRef,
    RiskParameterSetRef,
)


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


def _typed_tuple(value: object, item_type: type, name: str) -> None:
    if not isinstance(value, tuple) or any(not isinstance(item, item_type) for item in value):
        raise TypeError(f"{name} must be a tuple of {item_type.__name__} values")


def _unique(value: tuple[object, ...], name: str) -> None:
    if len(value) != len(set(value)):
        raise ValueError(f"{name} must not contain duplicates")


def _validate_status_applicability(
    status: FullModelStatus,
    applicability: Applicability,
) -> None:
    if not isinstance(status, FullModelStatus):
        raise TypeError("status must be a FullModelStatus")
    if not isinstance(applicability, Applicability):
        raise TypeError("applicability must be an Applicability")
    allowed = {
        FullModelStatus.AVAILABLE: {Applicability.APPLICABLE},
        FullModelStatus.NOT_APPLICABLE: {Applicability.NOT_APPLICABLE},
        FullModelStatus.UNKNOWN: {Applicability.APPLICABLE, Applicability.UNKNOWN},
        FullModelStatus.UNRESOLVED: {
            Applicability.APPLICABLE,
            Applicability.UNKNOWN,
        },
        FullModelStatus.UNAVAILABLE: {
            Applicability.APPLICABLE,
            Applicability.UNKNOWN,
        },
        FullModelStatus.UNSUPPORTED: {
            Applicability.APPLICABLE,
            Applicability.UNKNOWN,
        },
    }[status]
    if applicability not in allowed:
        raise ValueError("status/applicability combination is not allowed")


PROCESS_REASSESSMENT_CONTRACT_REF = ContractRef(
    "FULL-MODEL-V0.1-PROCESS-REASSESSMENT",
    "1",
)
ACTION_RULE_REF = RuleRef(
    "ACTION-RECONCILE-QB-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)
VERIFICATION_RULE_REF = RuleRef(
    "REEVAL-FULL-MODEL-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)
ACTION_RECORD_VERSION = "1"


class CorrectiveActionKind(str, Enum):
    RECONCILE_QUANTITATIVE_BOUNDS = "RECONCILE_QUANTITATIVE_BOUNDS"


class CorrectiveActionStatus(str, Enum):
    PROPOSED = "PROPOSED"
    APPLIED = "APPLIED"
    REJECTED = "REJECTED"


class ProposedChangeKind(str, Enum):
    REPLACE_REQUIREMENT_TEXT = "REPLACE_REQUIREMENT_TEXT"


class CorrectiveActionReason(str, Enum):
    ELIGIBLE_RISK_IDENTIFIED = "ELIGIBLE_RISK_IDENTIFIED"
    NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE = (
        "NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE"
    )
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    SOURCE_ASSESSMENT_UNKNOWN = "SOURCE_ASSESSMENT_UNKNOWN"
    SOURCE_IDENTITY_OR_COHERENCE_UNRESOLVED = (
        "SOURCE_IDENTITY_OR_COHERENCE_UNRESOLVED"
    )
    SOURCE_UNSUPPORTED = "SOURCE_UNSUPPORTED"
    REQUESTED_ACTION_KIND_UNSUPPORTED = "REQUESTED_ACTION_KIND_UNSUPPORTED"


class CorrectiveActionRationale(str, Enum):
    STAKEHOLDER_RECONCILIATION_REQUIRED = (
        "The two target requirements contain an exact QB-v0.1 confirmed conflict on "
        "the same complete quantitative comparison key. Stakeholder reconciliation is "
        "requested because the system cannot determine which bound expresses intent."
    )


class CorrectiveActionExpectedOutcome(str, Enum):
    LATER_RERUN_MAY_NOT_IDENTIFY_EXACT_CONFLICT = (
        "A later rerun may no longer identify that exact confirmed conflict."
    )


class CorrectiveActionNonOptimalityClaim(str, Enum):
    CANDIDATE_NOT_OPTIMALITY_CLAIM = "CANDIDATE_NOT_OPTIMALITY_CLAIM"


@dataclass(frozen=True, slots=True, order=True)
class RequirementLineageId:
    artifact_id: str
    origin_artifact_version: str
    origin_requirement_id: str
    origin_source_line: int

    def __post_init__(self) -> None:
        _identifier(self.artifact_id, "artifact_id")
        _identifier(self.origin_artifact_version, "origin_artifact_version")
        _identifier(self.origin_requirement_id, "origin_requirement_id")
        if type(self.origin_source_line) is not int or self.origin_source_line < 1:
            raise ValueError("origin_source_line must be a positive integer")


@dataclass(frozen=True, slots=True, order=True)
class ActionTargetRequirement:
    lineage_id: RequirementLineageId
    subject_ref: RequirementSubjectRef

    def __post_init__(self) -> None:
        if not isinstance(self.lineage_id, RequirementLineageId):
            raise TypeError("lineage_id must be a RequirementLineageId")
        if not isinstance(self.subject_ref, RequirementSubjectRef):
            raise TypeError("subject_ref must be a RequirementSubjectRef")
        if (
            self.lineage_id.artifact_id != self.subject_ref.artifact_ref.artifact_id
            or self.lineage_id.origin_artifact_version
            != self.subject_ref.artifact_ref.artifact_version
            or self.lineage_id.origin_requirement_id != self.subject_ref.requirement_id
            or self.lineage_id.origin_source_line != self.subject_ref.source_line
        ):
            raise ValueError("initial lineage identity must resolve to its exact subject")


@dataclass(frozen=True, slots=True, order=True)
class ActionCreatorSource:
    source_id: str
    source_version: str

    def __post_init__(self) -> None:
        _identifier(self.source_id, "source_id")
        _identifier(self.source_version, "source_version")


@dataclass(frozen=True, slots=True)
class CorrectiveActionContext:
    action_instance_id: str
    action_record_version: str
    creator_source: ActionCreatorSource
    target_artifact_ref: ArtifactRef
    target_requirement_lineages: tuple[RequirementLineageId, ...]
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    requested_action_kind: CorrectiveActionKind | str = (
        CorrectiveActionKind.RECONCILE_QUANTITATIVE_BOUNDS
    )
    full_model_contract_ref: ContractRef = FULL_MODEL_CONTRACT_REF
    defect_risk_contract_ref: ContractRef = DEFECT_QUALITY_RISK_CONTRACT_REF
    process_reassessment_contract_ref: ContractRef = PROCESS_REASSESSMENT_CONTRACT_REF
    action_rule_ref: RuleRef = ACTION_RULE_REF
    verification_rule_ref: RuleRef = VERIFICATION_RULE_REF

    def __post_init__(self) -> None:
        _identifier(self.action_instance_id, "action_instance_id")
        _identifier(self.action_record_version, "action_record_version")
        if not isinstance(self.creator_source, ActionCreatorSource):
            raise TypeError("creator_source must be an ActionCreatorSource")
        if not isinstance(self.target_artifact_ref, ArtifactRef):
            raise TypeError("target_artifact_ref must be an ArtifactRef")
        _typed_tuple(
            self.target_requirement_lineages,
            RequirementLineageId,
            "target_requirement_lineages",
        )
        if len(self.target_requirement_lineages) not in {0, 2}:
            raise ValueError("target_requirement_lineages requires zero or two entries")
        _unique(self.target_requirement_lineages, "target_requirement_lineages")
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        requested = (
            self.requested_action_kind.value
            if isinstance(self.requested_action_kind, CorrectiveActionKind)
            else self.requested_action_kind
        )
        _identifier(requested, "requested_action_kind")
        if self.source_assessment_ref.artifact_ref != self.target_artifact_ref:
            raise ValueError("action context cannot mix artifact and assessment versions")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("unsupported Full Model contract")
        if self.defect_risk_contract_ref != DEFECT_QUALITY_RISK_CONTRACT_REF:
            raise ValueError("unsupported defect-quality-risk contract")
        if self.process_reassessment_contract_ref != PROCESS_REASSESSMENT_CONTRACT_REF:
            raise ValueError("unsupported process-reassessment contract")
        if self.action_rule_ref != ACTION_RULE_REF:
            raise ValueError("unsupported corrective-action rule")
        if self.verification_rule_ref != VERIFICATION_RULE_REF:
            raise ValueError("unsupported corrective-action verification rule")


@dataclass(frozen=True, slots=True)
class CorrectiveActionId:
    action_instance_id: str
    rule_ref: RuleRef
    originating_risk_id: BoundedRiskAssessmentId
    originating_problem_id: ConfirmedSupportedProblemId
    target_artifact_ref: ArtifactRef

    def __post_init__(self) -> None:
        _identifier(self.action_instance_id, "action_instance_id")
        if self.rule_ref != ACTION_RULE_REF:
            raise ValueError("corrective-action identity requires the approved rule")


@dataclass(frozen=True, slots=True)
class ActionRef:
    action_id: CorrectiveActionId
    action_record_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.action_id, CorrectiveActionId):
            raise TypeError("action_id must be a CorrectiveActionId")
        _identifier(self.action_record_version, "action_record_version")


@dataclass(frozen=True, slots=True, order=True)
class RevisionRef:
    revision_id: str
    revision_version: str

    def __post_init__(self) -> None:
        _identifier(self.revision_id, "revision_id")
        _identifier(self.revision_version, "revision_version")


@dataclass(frozen=True, slots=True, order=True)
class ActionApplicationId:
    application_instance_id: str
    action_before_ref: ActionRef
    revision_ref: RevisionRef
    child_artifact_ref: ArtifactRef

    def __post_init__(self) -> None:
        _identifier(self.application_instance_id, "application_instance_id")
        if not isinstance(self.action_before_ref, ActionRef):
            raise TypeError("action_before_ref must be an ActionRef")
        if not isinstance(self.revision_ref, RevisionRef):
            raise TypeError("revision_ref must be a RevisionRef")
        if not isinstance(self.child_artifact_ref, ArtifactRef):
            raise TypeError("child_artifact_ref must be an ArtifactRef")


@dataclass(frozen=True, slots=True, order=True)
class ActionApplicationRef:
    application_id: ActionApplicationId
    application_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.application_id, ActionApplicationId):
            raise TypeError("application_id must be an ActionApplicationId")
        _identifier(self.application_version, "application_version")


@dataclass(frozen=True, slots=True)
class CorrectiveActionResolutionId:
    action_instance_id: str
    source_risk_ref: BoundedRiskAssessmentRef
    requested_action_kind: str
    rule_ref: RuleRef

    def __post_init__(self) -> None:
        _identifier(self.action_instance_id, "action_instance_id")
        _identifier(self.requested_action_kind, "requested_action_kind")
        if self.rule_ref != ACTION_RULE_REF:
            raise ValueError("resolution identity requires the approved action rule")


@dataclass(frozen=True, slots=True)
class CorrectiveActionProvenance:
    originating_risk_ref: BoundedRiskAssessmentRef
    originating_problem_ref: ConfirmedSupportedProblemRef
    originating_relation_ref: DefectQualityRelationRef
    problem_resolution_ref: ProblemClaimResolutionRef
    defect_population_ref: DefectPopulationSnapshotRef
    source_cross_result_ref: CrossResultId
    participant_refs: tuple[RequirementSubjectRef, RequirementSubjectRef]
    target_requirements: tuple[ActionTargetRequirement, ActionTargetRequirement]
    comparison_key: ComparisonKey
    ordered_evidence_refs: tuple[CrossEvidenceRef, ...]
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    full_model_contract_ref: ContractRef
    defect_risk_contract_ref: ContractRef
    process_reassessment_contract_ref: ContractRef
    problem_rule_ref: RuleRef
    relation_rule_ref: RuleRef
    risk_model_ref: RiskModelRef
    risk_rule_ref: RuleRef
    risk_parameter_set_ref: RiskParameterSetRef
    action_rule_ref: RuleRef
    verification_rule_ref: RuleRef

    def __post_init__(self) -> None:
        _typed_tuple(self.participant_refs, RequirementSubjectRef, "participant_refs")
        _typed_tuple(self.target_requirements, ActionTargetRequirement, "target_requirements")
        _typed_tuple(self.ordered_evidence_refs, CrossEvidenceRef, "ordered_evidence_refs")
        if len(self.participant_refs) != 2 or len(self.target_requirements) != 2:
            raise ValueError("action provenance requires exactly two ordered targets")
        if tuple(item.subject_ref for item in self.target_requirements) != self.participant_refs:
            raise ValueError("action provenance targets must preserve participant order")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("action provenance cannot mix artifact assessments")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("action provenance requires the Full Model contract")
        if self.defect_risk_contract_ref != DEFECT_QUALITY_RISK_CONTRACT_REF:
            raise ValueError("action provenance requires the defect-risk contract")
        if self.process_reassessment_contract_ref != PROCESS_REASSESSMENT_CONTRACT_REF:
            raise ValueError("action provenance requires the process contract")
        if self.problem_rule_ref != PROBLEM_RULE_REF or self.relation_rule_ref != RELATION_RULE_REF:
            raise ValueError("action provenance requires the approved problem and relation rules")
        if self.risk_model_ref != RISK_MODEL_REF or self.risk_rule_ref != RISK_RULE_REF:
            raise ValueError("action provenance requires the approved risk model and rule")
        if self.risk_parameter_set_ref != RISK_PARAMETER_SET_REF:
            raise ValueError("action provenance requires the approved risk parameter set")
        if self.action_rule_ref != ACTION_RULE_REF or self.verification_rule_ref != VERIFICATION_RULE_REF:
            raise ValueError("action provenance requires the approved action rules")


@dataclass(frozen=True, slots=True)
class CorrectiveAction:
    action_id: CorrectiveActionId
    action_record_version: str
    predecessor_action_ref: ActionRef | None
    action_kind: CorrectiveActionKind
    status: CorrectiveActionStatus
    rule_ref: RuleRef
    originating_risk_ref: BoundedRiskAssessmentRef
    originating_problem_ref: ConfirmedSupportedProblemRef
    originating_relation_ref: DefectQualityRelationRef
    target_artifact_ref: ArtifactRef
    target_requirements: tuple[ActionTargetRequirement, ActionTargetRequirement]
    comparison_key: ComparisonKey
    rationale: CorrectiveActionRationale
    proposed_change_kind: ProposedChangeKind
    expected_bounded_outcome: CorrectiveActionExpectedOutcome
    verification_rule_ref: RuleRef
    external_revision_ref: RevisionRef | None
    application_ref: ActionApplicationRef | None
    rejection_source_ref: None
    creator_source: ActionCreatorSource
    provenance: CorrectiveActionProvenance
    non_optimality_claim: CorrectiveActionNonOptimalityClaim

    def __post_init__(self) -> None:
        expected_id = CorrectiveActionId(
            self.action_id.action_instance_id,
            self.rule_ref,
            self.originating_risk_ref.risk_assessment_id,
            self.originating_problem_ref.problem_id,
            self.target_artifact_ref,
        )
        if self.action_id != expected_id:
            raise ValueError("action_id must be the contract-defined structured identity")
        _identifier(self.action_record_version, "action_record_version")
        if self.action_kind is not CorrectiveActionKind.RECONCILE_QUANTITATIVE_BOUNDS:
            raise ValueError("unsupported corrective-action kind")
        if not isinstance(self.status, CorrectiveActionStatus):
            raise TypeError("status must be a CorrectiveActionStatus")
        if self.rule_ref != ACTION_RULE_REF:
            raise ValueError("corrective action requires ACTION-RECONCILE-QB-001 / 1")
        _typed_tuple(self.target_requirements, ActionTargetRequirement, "target_requirements")
        if len(self.target_requirements) != 2:
            raise ValueError("corrective action requires exactly two ordered targets")
        if any(item.subject_ref.artifact_ref != self.target_artifact_ref for item in self.target_requirements):
            raise ValueError("corrective-action targets cannot cross artifact versions")
        if self.rationale is not CorrectiveActionRationale.STAKEHOLDER_RECONCILIATION_REQUIRED:
            raise ValueError("corrective action requires the normative bounded rationale")
        if self.proposed_change_kind is not ProposedChangeKind.REPLACE_REQUIREMENT_TEXT:
            raise ValueError("corrective action supports replacement proposals only")
        if self.expected_bounded_outcome is not CorrectiveActionExpectedOutcome.LATER_RERUN_MAY_NOT_IDENTIFY_EXACT_CONFLICT:
            raise ValueError("corrective action requires the bounded non-promissory outcome")
        if self.verification_rule_ref != VERIFICATION_RULE_REF:
            raise ValueError("corrective action requires REEVAL-FULL-MODEL-001 / 1")
        if self.status is CorrectiveActionStatus.PROPOSED:
            if self.predecessor_action_ref is not None or any(
                item is not None
                for item in (
                    self.external_revision_ref,
                    self.application_ref,
                    self.rejection_source_ref,
                )
            ):
                raise ValueError(
                    "a proposal cannot carry predecessor, application, or rejection references"
                )
        elif self.status is CorrectiveActionStatus.APPLIED:
            if (
                self.predecessor_action_ref is None
                or self.external_revision_ref is None
                or self.application_ref is None
                or self.rejection_source_ref is not None
            ):
                raise ValueError(
                    "an APPLIED action requires predecessor, revision, and application references"
                )
            if (
                self.predecessor_action_ref.action_id != self.action_id
                or self.predecessor_action_ref.action_record_version
                == self.action_record_version
            ):
                raise ValueError(
                    "an APPLIED action must be a distinct version of the same action"
                )
        else:
            if (
                self.predecessor_action_ref is None
                or self.rejection_source_ref is None
                or self.external_revision_ref is not None
                or self.application_ref is not None
            ):
                raise ValueError(
                    "a REJECTED action requires only predecessor and rejection references"
                )
        if self.non_optimality_claim is not CorrectiveActionNonOptimalityClaim.CANDIDATE_NOT_OPTIMALITY_CLAIM:
            raise ValueError("corrective action requires the candidate non-optimality claim")
        if (
            self.provenance.originating_risk_ref != self.originating_risk_ref
            or self.provenance.originating_problem_ref != self.originating_problem_ref
            or self.provenance.originating_relation_ref != self.originating_relation_ref
            or self.provenance.target_requirements != self.target_requirements
            or self.provenance.comparison_key != self.comparison_key
            or self.provenance.artifact_ref != self.target_artifact_ref
            or self.provenance.action_rule_ref != self.rule_ref
            or self.provenance.verification_rule_ref != self.verification_rule_ref
        ):
            raise ValueError("action and provenance must preserve one source graph")

    @property
    def ref(self) -> ActionRef:
        return ActionRef(self.action_id, self.action_record_version)


@dataclass(frozen=True, slots=True)
class CorrectiveActionResolutionProvenance:
    source_risk_ref: BoundedRiskAssessmentRef
    source_problem_ref: ConfirmedSupportedProblemRef | None
    source_relation_ref: DefectQualityRelationRef
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    participant_refs: tuple[RequirementSubjectRef, ...]
    target_requirements: tuple[ActionTargetRequirement, ...]
    ordered_evidence_refs: tuple[CrossEvidenceRef, ...]
    full_model_contract_ref: ContractRef
    defect_risk_contract_ref: ContractRef
    process_reassessment_contract_ref: ContractRef
    source_risk_model_ref: RiskModelRef
    source_risk_rule_ref: RuleRef
    source_risk_parameter_set_ref: RiskParameterSetRef
    action_rule_ref: RuleRef

    def __post_init__(self) -> None:
        _typed_tuple(self.participant_refs, RequirementSubjectRef, "participant_refs")
        _typed_tuple(self.target_requirements, ActionTargetRequirement, "target_requirements")
        _typed_tuple(self.ordered_evidence_refs, CrossEvidenceRef, "ordered_evidence_refs")
        if len(self.participant_refs) not in {0, 2}:
            raise ValueError("resolution provenance requires zero or two participants")
        if self.target_requirements and tuple(
            item.subject_ref for item in self.target_requirements
        ) != self.participant_refs:
            raise ValueError("resolution targets must preserve participant order")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("resolution provenance cannot mix artifact assessments")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("resolution provenance requires the Full Model contract")
        if self.defect_risk_contract_ref != DEFECT_QUALITY_RISK_CONTRACT_REF:
            raise ValueError("resolution provenance requires the defect-risk contract")
        if self.process_reassessment_contract_ref != PROCESS_REASSESSMENT_CONTRACT_REF:
            raise ValueError("resolution provenance requires the process contract")
        if self.source_risk_model_ref != RISK_MODEL_REF or self.source_risk_rule_ref != RISK_RULE_REF:
            raise ValueError("resolution provenance requires the approved risk model and rule")
        if self.source_risk_parameter_set_ref != RISK_PARAMETER_SET_REF:
            raise ValueError("resolution provenance requires the approved risk parameter set")
        if self.action_rule_ref != ACTION_RULE_REF:
            raise ValueError("resolution provenance requires the approved action rule")


@dataclass(frozen=True, slots=True)
class CorrectiveActionResolution:
    resolution_id: CorrectiveActionResolutionId
    status: FullModelStatus
    applicability: Applicability
    action_ref: ActionRef | None
    reason_codes: tuple[CorrectiveActionReason, ...]
    source_risk_ref: BoundedRiskAssessmentRef
    source_problem_ref: ConfirmedSupportedProblemRef | None
    source_relation_ref: DefectQualityRelationRef
    rule_ref: RuleRef
    provenance: CorrectiveActionResolutionProvenance
    action: CorrectiveAction | None

    def __post_init__(self) -> None:
        _validate_status_applicability(self.status, self.applicability)
        _typed_tuple(self.reason_codes, CorrectiveActionReason, "reason_codes")
        if len(self.reason_codes) != 1:
            raise ValueError("a corrective-action resolution requires one controlling reason")
        if self.rule_ref != ACTION_RULE_REF:
            raise ValueError("resolution requires ACTION-RECONCILE-QB-001 / 1")
        if self.resolution_id.source_risk_ref != self.source_risk_ref:
            raise ValueError("resolution identity must preserve the source risk")
        if self.status is FullModelStatus.AVAILABLE:
            if self.action is None or self.action_ref != self.action.ref:
                raise ValueError("AVAILABLE resolution requires its exact action")
            if self.action.status is not CorrectiveActionStatus.PROPOSED:
                raise ValueError("AVAILABLE M3-08 resolution requires a PROPOSED action")
        elif self.action is not None or self.action_ref is not None:
            raise ValueError("non-AVAILABLE resolution cannot fabricate an action")
        if (
            self.provenance.source_risk_ref != self.source_risk_ref
            or self.provenance.source_problem_ref != self.source_problem_ref
            or self.provenance.source_relation_ref != self.source_relation_ref
            or self.provenance.action_rule_ref != self.rule_ref
        ):
            raise ValueError("resolution and provenance must preserve one source graph")


__all__ = [
    "ACTION_RECORD_VERSION",
    "ACTION_RULE_REF",
    "PROCESS_REASSESSMENT_CONTRACT_REF",
    "VERIFICATION_RULE_REF",
    "ActionCreatorSource",
    "ActionApplicationId",
    "ActionApplicationRef",
    "ActionRef",
    "ActionTargetRequirement",
    "CorrectiveAction",
    "CorrectiveActionContext",
    "CorrectiveActionExpectedOutcome",
    "CorrectiveActionId",
    "CorrectiveActionKind",
    "CorrectiveActionNonOptimalityClaim",
    "CorrectiveActionProvenance",
    "CorrectiveActionRationale",
    "CorrectiveActionReason",
    "CorrectiveActionResolution",
    "CorrectiveActionResolutionId",
    "CorrectiveActionResolutionProvenance",
    "CorrectiveActionStatus",
    "ProposedChangeKind",
    "RequirementLineageId",
    "RevisionRef",
]

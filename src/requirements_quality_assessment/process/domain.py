"""Immutable records for the bounded Full Model v0.1 process projection."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..corrective_action import (
    PROCESS_REASSESSMENT_CONTRACT_REF,
    ActionApplicationRef,
    ActionRef,
    ArtifactTransitionId,
)
from ..defect_quality import (
    ConfirmedSupportedProblemRef,
    DefectPopulationSnapshotRef,
    DefectQualityRelationRef,
)
from ..dynamic_evidence import Applicability, FullModelStatus, ProductRef
from ..metrics import (
    FULL_MODEL_CONTRACT_REF,
    ArtifactRef,
    AssessmentRef,
    ContractRef,
    MetricProfileId,
    RequirementSubjectRef,
    RuleRef,
    RuleVersionAuthority,
)
from ..performance_efficiency import (
    PerformanceEfficiencyFeatureProfileId,
    ProcessStage,
    ProcessStateRef,
)
from ..reassessment import ComponentVersionSet, ReassessmentRef
from ..risk import BoundedRiskAssessmentRef, ProductQualityAssessmentRef


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


PROCESS_RULE_REF = RuleRef(
    "PROCESS-REFERENCE-VERIFICATION-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)


class ProcessComponentRole(str, Enum):
    REQUIREMENT_ASSESSMENT = "REQUIREMENT_ASSESSMENT"
    SPECIFICATION_ASSESSMENT = "SPECIFICATION_ASSESSMENT"
    METRIC_PROFILE = "METRIC_PROFILE"
    PE_FEATURE_PROFILE = "PE_FEATURE_PROFILE"
    PRODUCT_QUALITY_ASSESSMENT = "PRODUCT_QUALITY_ASSESSMENT"
    DEFECT_POPULATION = "DEFECT_POPULATION"
    CONFIRMED_PROBLEM = "CONFIRMED_PROBLEM"
    DEFECT_QUALITY_RELATION = "DEFECT_QUALITY_RELATION"
    BOUNDED_RISK_ASSESSMENT = "BOUNDED_RISK_ASSESSMENT"
    CORRECTIVE_ACTION = "CORRECTIVE_ACTION"


class ProcessEvidenceRole(str, Enum):
    STATIC_REQUIREMENT = "STATIC_REQUIREMENT"
    QB = "QB"
    DYNAMIC_CRITERION = "DYNAMIC_CRITERION"
    DYNAMIC_OBSERVATION = "DYNAMIC_OBSERVATION"
    CONFORMANCE = "CONFORMANCE"


class DissertationStage(str, Enum):
    """The sole dissertation-stage identity admitted by the bounded projection."""

    TAU_T = "τ^T"


PROCESS_STAGE_MAPPING = (
    (ProcessStage.REFERENCE_VERIFICATION, DissertationStage.TAU_T),
)


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
        FullModelStatus.UNAVAILABLE: {Applicability.APPLICABLE, Applicability.UNKNOWN},
        FullModelStatus.UNKNOWN: {Applicability.APPLICABLE, Applicability.UNKNOWN},
        FullModelStatus.UNRESOLVED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
        FullModelStatus.UNSUPPORTED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
    }[status]
    if applicability not in allowed:
        raise ValueError("process association status/applicability is inconsistent")


@dataclass(frozen=True, slots=True, order=True)
class RequirementAssessmentRef:
    assessment_ref: AssessmentRef
    requirement_subject_ref: RequirementSubjectRef

    def __post_init__(self) -> None:
        if self.assessment_ref.artifact_ref != self.requirement_subject_ref.artifact_ref:
            raise ValueError("requirement assessment ref cannot mix artifact versions")


@dataclass(frozen=True, slots=True, order=True)
class SpecificationAssessmentRef:
    assessment_ref: AssessmentRef
    snapshot_id: object

    def __post_init__(self) -> None:
        if self.snapshot_id is None:
            raise ValueError("snapshot_id must not be None")

    @property
    def artifact_ref(self) -> ArtifactRef:
        return self.assessment_ref.artifact_ref


MetricProfileRef = MetricProfileId
PerformanceEfficiencyFeatureProfileRef = PerformanceEfficiencyFeatureProfileId
DefectPopulationRef = DefectPopulationSnapshotRef


@dataclass(frozen=True, slots=True, order=True)
class ArtifactTransitionRef:
    transition_id: ArtifactTransitionId

    def __post_init__(self) -> None:
        if not isinstance(self.transition_id, ArtifactTransitionId):
            raise TypeError("transition_id must be an ArtifactTransitionId")


@dataclass(frozen=True, slots=True, order=True)
class ComparisonRef:
    comparison_id: str
    comparison_version: str

    def __post_init__(self) -> None:
        _identifier(self.comparison_id, "comparison_id")
        _identifier(self.comparison_version, "comparison_version")


@dataclass(frozen=True, slots=True)
class ProcessComponentAssociation:
    role: ProcessComponentRole
    result_ref: object | None
    status: FullModelStatus
    applicability: Applicability
    subject_or_scope_ref: object
    producing_contract_or_rule_ref: ContractRef | RuleRef
    reason_codes: tuple[object, ...]
    provenance: tuple[object, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.role, ProcessComponentRole):
            raise TypeError("role must be a ProcessComponentRole")
        _validate_status_applicability(self.status, self.applicability)
        if self.result_ref is None and self.status is FullModelStatus.AVAILABLE:
            raise ValueError("AVAILABLE component association requires a result ref")
        if self.result_ref is None and not self.reason_codes:
            raise ValueError("missing component result requires a typed reason")
        if self.subject_or_scope_ref is None:
            raise ValueError("component association requires an explicit subject or scope")
        if not isinstance(self.producing_contract_or_rule_ref, (ContractRef, RuleRef)):
            raise TypeError("producing ref must be a ContractRef or RuleRef")
        if not isinstance(self.reason_codes, tuple) or any(
            item is None for item in self.reason_codes
        ):
            raise TypeError("reason_codes must be a tuple of typed values")
        if not isinstance(self.provenance, tuple) or not self.provenance or any(
            item is None for item in self.provenance
        ):
            raise ValueError("component association requires immutable provenance")


@dataclass(frozen=True, slots=True)
class ProcessEvidenceAssociation:
    role: ProcessEvidenceRole
    evidence_ref: object | None
    status: FullModelStatus
    applicability: Applicability
    artifact_or_product_ref: ArtifactRef | ProductRef
    source_or_collection_ref: object
    context_ref_or_none: object | None
    reuse_decision_ref_or_none: object | None
    reason_codes: tuple[object, ...]
    provenance: tuple[object, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.role, ProcessEvidenceRole):
            raise TypeError("role must be a ProcessEvidenceRole")
        _validate_status_applicability(self.status, self.applicability)
        if self.evidence_ref is None and self.status is FullModelStatus.AVAILABLE:
            raise ValueError("AVAILABLE evidence association requires an evidence ref")
        if self.evidence_ref is None and not self.reason_codes:
            raise ValueError("missing evidence requires a typed reason")
        if not isinstance(self.artifact_or_product_ref, (ArtifactRef, ProductRef)):
            raise TypeError("artifact_or_product_ref must be an ArtifactRef or ProductRef")
        if self.source_or_collection_ref is None:
            raise ValueError("evidence association requires its source or collection ref")
        if not isinstance(self.reason_codes, tuple) or any(
            item is None for item in self.reason_codes
        ):
            raise TypeError("reason_codes must be a tuple of typed values")
        if not isinstance(self.provenance, tuple) or not self.provenance or any(
            item is None for item in self.provenance
        ):
            raise ValueError("evidence association requires immutable provenance")


@dataclass(frozen=True, slots=True)
class ProcessAssessmentStateProvenance:
    process_state_ref: ProcessStateRef
    process_lineage_id: str
    artifact_ref: ArtifactRef
    assessment_ref: AssessmentRef
    predecessor_process_state_ref: ProcessStateRef | None
    artifact_transition_ref_or_none: ArtifactTransitionRef | None
    action_application_ref_or_none: ActionApplicationRef | None
    reassessment_ref_or_none: ReassessmentRef | None
    comparison_refs: tuple[ComparisonRef, ...]
    evidence_associations: tuple[ProcessEvidenceAssociation, ...]
    component_associations: tuple[ProcessComponentAssociation, ...]
    component_version_set: ComponentVersionSet
    full_model_contract_ref: ContractRef = FULL_MODEL_CONTRACT_REF
    process_reassessment_contract_ref: ContractRef = PROCESS_REASSESSMENT_CONTRACT_REF
    rule_ref: RuleRef = PROCESS_RULE_REF

    def __post_init__(self) -> None:
        _identifier(self.process_lineage_id, "process_lineage_id")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("process provenance requires FULL-MODEL-V0.1-CONTRACT / 1")
        if self.process_reassessment_contract_ref != PROCESS_REASSESSMENT_CONTRACT_REF:
            raise ValueError("process provenance requires the process contract / 1")
        if self.rule_ref != PROCESS_RULE_REF:
            raise ValueError("process provenance requires the approved process rule")


@dataclass(frozen=True, slots=True)
class ProcessAssessmentState:
    process_state_id: str
    process_state_version: str
    process_lineage_id: str
    stage: ProcessStage
    artifact_ref: ArtifactRef
    artifact_transition_ref_or_none: ArtifactTransitionRef | None
    assessment_ref: AssessmentRef
    full_model_contract_ref: ContractRef
    component_version_set: ComponentVersionSet
    evidence_associations: tuple[ProcessEvidenceAssociation, ...]
    component_associations: tuple[ProcessComponentAssociation, ...]
    requirement_assessment_refs: tuple[RequirementAssessmentRef, ...]
    specification_assessment_ref: SpecificationAssessmentRef
    metric_profile_ref: MetricProfileRef
    pe_feature_profile_ref: PerformanceEfficiencyFeatureProfileRef | None
    product_quality_assessment_ref: ProductQualityAssessmentRef | None
    defect_population_ref: DefectPopulationRef
    confirmed_problem_refs: tuple[ConfirmedSupportedProblemRef, ...]
    defect_quality_relation_refs: tuple[DefectQualityRelationRef, ...]
    bounded_risk_assessment_refs: tuple[BoundedRiskAssessmentRef, ...]
    corrective_action_refs: tuple[ActionRef, ...]
    predecessor_process_state_ref: ProcessStateRef | None
    reassessment_ref: ReassessmentRef | None
    provenance: ProcessAssessmentStateProvenance

    @property
    def ref(self) -> ProcessStateRef:
        return ProcessStateRef(
            self.process_state_id,
            self.process_state_version,
            self.stage,
        )

    def __post_init__(self) -> None:
        _identifier(self.process_state_id, "process_state_id")
        _identifier(self.process_state_version, "process_state_version")
        _identifier(self.process_lineage_id, "process_lineage_id")
        if self.stage is not ProcessStage.REFERENCE_VERIFICATION:
            raise ValueError("M_process v0.1 supports REFERENCE_VERIFICATION only")
        if self.process_lineage_id != self.process_state_id:
            raise ValueError("process lineage must equal the reserved stable process ID")
        if self.assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("process assessment and artifact versions must agree")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("process state requires FULL-MODEL-V0.1-CONTRACT / 1")
        if self.provenance.process_state_ref != self.ref:
            raise ValueError("process provenance must identify the materialized state")
        if (
            self.provenance.process_lineage_id != self.process_lineage_id
            or self.provenance.artifact_ref != self.artifact_ref
            or self.provenance.assessment_ref != self.assessment_ref
            or self.provenance.predecessor_process_state_ref
            != self.predecessor_process_state_ref
            or self.provenance.artifact_transition_ref_or_none
            != self.artifact_transition_ref_or_none
            or self.provenance.reassessment_ref_or_none != self.reassessment_ref
            or self.provenance.evidence_associations != self.evidence_associations
            or self.provenance.component_associations != self.component_associations
            or self.provenance.component_version_set != self.component_version_set
        ):
            raise ValueError("process state and provenance must preserve one input graph")


@dataclass(frozen=True, slots=True, order=True)
class ProcessStateTransitionId:
    transition_id: str

    def __post_init__(self) -> None:
        _identifier(self.transition_id, "transition_id")


@dataclass(frozen=True, slots=True)
class ProcessStateTransitionProvenance:
    predecessor_process_state_ref: ProcessStateRef
    successor_process_state_ref: ProcessStateRef
    artifact_transition_ref: ArtifactTransitionRef
    action_application_ref: ActionApplicationRef
    reassessment_ref: ReassessmentRef
    comparison_refs: tuple[ComparisonRef, ...]
    process_reassessment_contract_ref: ContractRef = PROCESS_REASSESSMENT_CONTRACT_REF
    rule_ref: RuleRef = PROCESS_RULE_REF


@dataclass(frozen=True, slots=True)
class ProcessStateTransition:
    transition_id: ProcessStateTransitionId
    predecessor_process_state_ref: ProcessStateRef
    successor_process_state_ref: ProcessStateRef
    artifact_transition_ref: ArtifactTransitionRef
    action_application_ref: ActionApplicationRef
    reassessment_ref: ReassessmentRef
    comparison_refs: tuple[ComparisonRef, ...]
    rule_ref: RuleRef
    provenance: ProcessStateTransitionProvenance

    def __post_init__(self) -> None:
        if self.predecessor_process_state_ref == self.successor_process_state_ref:
            raise ValueError("process transition requires distinct state identities")
        if (
            self.predecessor_process_state_ref.process_state_id
            != self.successor_process_state_ref.process_state_id
        ):
            raise ValueError("process transition must preserve the process lineage")
        if (
            self.predecessor_process_state_ref.stage
            is not ProcessStage.REFERENCE_VERIFICATION
            or self.successor_process_state_ref.stage
            is not ProcessStage.REFERENCE_VERIFICATION
        ):
            raise ValueError("process transition supports REFERENCE_VERIFICATION only")
        if self.rule_ref != PROCESS_RULE_REF:
            raise ValueError("process transition requires the approved process rule")
        if (
            self.provenance.predecessor_process_state_ref
            != self.predecessor_process_state_ref
            or self.provenance.successor_process_state_ref
            != self.successor_process_state_ref
            or self.provenance.artifact_transition_ref != self.artifact_transition_ref
            or self.provenance.action_application_ref != self.action_application_ref
            or self.provenance.reassessment_ref != self.reassessment_ref
            or self.provenance.comparison_refs != self.comparison_refs
            or self.provenance.rule_ref != self.rule_ref
        ):
            raise ValueError("process transition and provenance must agree")


__all__ = [name for name in globals() if not name.startswith("_")]

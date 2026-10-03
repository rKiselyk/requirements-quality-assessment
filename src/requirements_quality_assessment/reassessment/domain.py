"""Typed M3-09 reassessment and before/after comparison records."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from ..corrective_action import (
    PROCESS_REASSESSMENT_CONTRACT_REF,
    ActionApplicationRef,
    ArtifactTransition,
    RequirementLineageId,
)
from ..dynamic_evidence import Applicability, FullModelStatus
from ..metrics import (
    FULL_MODEL_CONTRACT_REF,
    ArtifactRef,
    AssessmentRef,
    ContractRef,
    RuleRef,
    RuleVersionAuthority,
)
from ..performance_efficiency import ProcessStage, ProcessStateRef
from ..product_quality import CalibrationStatus


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


REASSESSMENT_RULE_REF = RuleRef(
    "REEVAL-FULL-MODEL-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)
COMPARISON_RULE_REF = RuleRef(
    "COMPARE-FULL-MODEL-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)


@dataclass(frozen=True, slots=True, order=True)
class VersionedComponentRef:
    component_role: str
    component_id: str
    component_version: str

    def __post_init__(self) -> None:
        _identifier(self.component_role, "component_role")
        _identifier(self.component_id, "component_id")
        _identifier(self.component_version, "component_version")


@dataclass(frozen=True, slots=True)
class ComponentVersionSet:
    components: tuple[VersionedComponentRef, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.components, tuple) or any(
            not isinstance(item, VersionedComponentRef) for item in self.components
        ):
            raise TypeError("components must be VersionedComponentRef values")
        if not self.components:
            raise ValueError("component version set must not be empty")
        roles = tuple(item.component_role for item in self.components)
        if len(roles) != len(set(roles)):
            raise ValueError("component roles must be unique")


class EvidenceReuseDisposition(str, Enum):
    REUSE_ALLOWED = "REUSE_ALLOWED"
    REBUILD_OR_RECOLLECT_REQUIRED = "REBUILD_OR_RECOLLECT_REQUIRED"


class EvidenceReuseReason(str, Enum):
    EXACT_IDENTITY_AND_CONTEXT_MATCH = "EXACT_IDENTITY_AND_CONTEXT_MATCH"
    IDENTITY_OR_CONTEXT_CHANGED = "IDENTITY_OR_CONTEXT_CHANGED"
    VALIDITY_NOT_ESTABLISHED = "VALIDITY_NOT_ESTABLISHED"


@dataclass(frozen=True, slots=True)
class ExactIdentityCheck:
    field_name: str
    expected: object
    actual: object
    matches: bool

    def __post_init__(self) -> None:
        _identifier(self.field_name, "field_name")
        if self.matches is not (self.expected == self.actual):
            raise ValueError("matches must report exact equality")


@dataclass(frozen=True, slots=True)
class EvidenceReuseProvenance:
    source_process_state_ref: ProcessStateRef
    target_process_state_ref: ProcessStateRef
    source_contract_ref: ContractRef
    reassessment_rule_ref: RuleRef = REASSESSMENT_RULE_REF


@dataclass(frozen=True, slots=True)
class EvidenceReuseDecision:
    source_evidence_ref: object
    target_process_state_ref: ProcessStateRef
    decision: EvidenceReuseDisposition
    exact_identity_checks: tuple[ExactIdentityCheck, ...]
    reason_codes: tuple[EvidenceReuseReason, ...]
    provenance: EvidenceReuseProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.decision, EvidenceReuseDisposition):
            raise TypeError("decision must be an EvidenceReuseDisposition")
        if not isinstance(self.exact_identity_checks, tuple) or any(
            not isinstance(item, ExactIdentityCheck)
            for item in self.exact_identity_checks
        ):
            raise TypeError("exact_identity_checks must be ExactIdentityCheck values")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes or any(
            not isinstance(item, EvidenceReuseReason) for item in self.reason_codes
        ):
            raise TypeError("reason_codes must be EvidenceReuseReason values")
        if self.target_process_state_ref != self.provenance.target_process_state_ref:
            raise ValueError("reuse provenance must name the target process state")
        if self.decision is EvidenceReuseDisposition.REUSE_ALLOWED:
            if not self.exact_identity_checks or not all(
                item.matches for item in self.exact_identity_checks
            ):
                raise ValueError("REUSE_ALLOWED requires every exact check to match")
            if self.reason_codes != (
                EvidenceReuseReason.EXACT_IDENTITY_AND_CONTEXT_MATCH,
            ):
                raise ValueError("REUSE_ALLOWED requires the exact-match reason")


@dataclass(frozen=True, slots=True)
class ReassessmentContext:
    predecessor_process_state_ref: ProcessStateRef
    action_application_ref: ActionApplicationRef
    parent_artifact_ref: ArtifactRef
    child_artifact_ref: ArtifactRef
    child_assessment_ref: AssessmentRef
    full_model_contract_ref: ContractRef
    component_version_set: ComponentVersionSet
    evidence_reuse_decisions: tuple[EvidenceReuseDecision, ...]
    stage: ProcessStage

    def __post_init__(self) -> None:
        if self.parent_artifact_ref.artifact_id != self.child_artifact_ref.artifact_id:
            raise ValueError("parent and child must share the stable artifact identity")
        if self.parent_artifact_ref == self.child_artifact_ref:
            raise ValueError("parent and child artifact versions must be distinct")
        if self.child_assessment_ref.artifact_ref != self.child_artifact_ref:
            raise ValueError("child assessment must identify the child artifact")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("reassessment requires FULL-MODEL-V0.1-CONTRACT / 1")
        if self.stage is not ProcessStage.REFERENCE_VERIFICATION:
            raise ValueError("M3-09 supports REFERENCE_VERIFICATION only")
        if not isinstance(self.evidence_reuse_decisions, tuple) or any(
            not isinstance(item, EvidenceReuseDecision)
            for item in self.evidence_reuse_decisions
        ):
            raise TypeError("evidence_reuse_decisions must be typed decisions")


@dataclass(frozen=True, slots=True, order=True)
class AssessmentResultRef:
    result_family: str
    result_id: object
    artifact_ref: ArtifactRef

    def __post_init__(self) -> None:
        _identifier(self.result_family, "result_family")
        if self.result_id is None:
            raise ValueError("result_id must not be None")


@dataclass(frozen=True, slots=True, order=True)
class ComparisonRequestRef:
    comparison_id: str
    comparison_version: str

    def __post_init__(self) -> None:
        _identifier(self.comparison_id, "comparison_id")
        _identifier(self.comparison_version, "comparison_version")


class ReassessmentReason(str, Enum):
    FULL_MODEL_PATH_REBUILT = "FULL_MODEL_PATH_REBUILT"
    REQUIRED_CURRENT_EVIDENCE_UNAVAILABLE = "REQUIRED_CURRENT_EVIDENCE_UNAVAILABLE"
    IDENTITY_OR_PROVENANCE_UNRESOLVED = "IDENTITY_OR_PROVENANCE_UNRESOLVED"
    REQUESTED_PATH_UNSUPPORTED = "REQUESTED_PATH_UNSUPPORTED"


@dataclass(frozen=True, slots=True, order=True)
class ReassessmentRef:
    reassessment_id: str
    reassessment_version: str

    def __post_init__(self) -> None:
        _identifier(self.reassessment_id, "reassessment_id")
        _identifier(self.reassessment_version, "reassessment_version")


@dataclass(frozen=True, slots=True)
class ReassessmentProvenance:
    reassessment_ref: ReassessmentRef
    action_application_ref: ActionApplicationRef
    predecessor_process_state_ref: ProcessStateRef
    child_process_state_ref: ProcessStateRef | None
    parent_artifact_ref: ArtifactRef
    child_artifact_ref: ArtifactRef
    child_assessment_ref: AssessmentRef
    produced_result_refs: tuple[AssessmentResultRef, ...]
    component_version_set: ComponentVersionSet
    evidence_reuse_decisions: tuple[EvidenceReuseDecision, ...]
    full_model_contract_ref: ContractRef
    process_reassessment_contract_ref: ContractRef = PROCESS_REASSESSMENT_CONTRACT_REF
    rule_ref: RuleRef = REASSESSMENT_RULE_REF


@dataclass(frozen=True, slots=True)
class ReassessmentRun:
    reassessment_id: str
    reassessment_version: str
    context: ReassessmentContext
    status: FullModelStatus
    child_process_state_ref: ProcessStateRef | None
    produced_result_refs: tuple[AssessmentResultRef, ...]
    comparison_request_refs: tuple[ComparisonRequestRef, ...]
    reason_codes: tuple[ReassessmentReason, ...]
    rule_ref: RuleRef
    provenance: ReassessmentProvenance
    produced_results: tuple[object, ...]

    def __post_init__(self) -> None:
        _identifier(self.reassessment_id, "reassessment_id")
        _identifier(self.reassessment_version, "reassessment_version")
        if self.rule_ref != REASSESSMENT_RULE_REF:
            raise ValueError("reassessment requires REEVAL-FULL-MODEL-001 / 1")
        if not isinstance(self.status, FullModelStatus):
            raise TypeError("status must be a FullModelStatus")
        if len(self.produced_result_refs) != len(self.produced_results):
            raise ValueError("every produced result requires one ordered reference")
        if self.provenance.reassessment_ref != self.ref:
            raise ValueError("reassessment provenance must identify this run")
        if self.provenance.produced_result_refs != self.produced_result_refs:
            raise ValueError("reassessment provenance must preserve result order")

    @property
    def ref(self) -> ReassessmentRef:
        return ReassessmentRef(self.reassessment_id, self.reassessment_version)


class ComparisonResultFamily(str, Enum):
    REQUIREMENT_METRIC = "REQUIREMENT_METRIC"
    SPECIFICATION_METRIC = "SPECIFICATION_METRIC"
    QB_CONSISTENCY = "QB_CONSISTENCY"
    CRITERION_CONFORMANCE = "CRITERION_CONFORMANCE"
    PERFORMANCE_EFFICIENCY_FEATURE = "PERFORMANCE_EFFICIENCY_FEATURE"
    PRODUCT_QUALITY = "PRODUCT_QUALITY"
    CONFIRMED_PROBLEM = "CONFIRMED_PROBLEM"
    DEFECT_QUALITY_RELATION = "DEFECT_QUALITY_RELATION"
    BOUNDED_RISK = "BOUNDED_RISK"


class ComparisonValueKind(str, Enum):
    EXACT_FRACTION = "EXACT_FRACTION"
    CATEGORICAL_STATE = "CATEGORICAL_STATE"


@dataclass(frozen=True, slots=True)
class ComparisonSubject:
    result_family: ComparisonResultFamily
    metric_or_characteristic_id: str
    stable_subject_identity: tuple[object, ...]
    ordered_lineage_population: tuple[RequirementLineageId, ...]
    scope_identity: tuple[object, ...]
    evidence_context: tuple[object, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.result_family, ComparisonResultFamily):
            raise TypeError("result_family must be a ComparisonResultFamily")
        _identifier(self.metric_or_characteristic_id, "metric_or_characteristic_id")
        for name, value in (
            ("stable_subject_identity", self.stable_subject_identity),
            ("ordered_lineage_population", self.ordered_lineage_population),
            ("scope_identity", self.scope_identity),
            ("evidence_context", self.evidence_context),
        ):
            if not isinstance(value, tuple):
                raise TypeError(f"{name} must be a tuple")


@dataclass(frozen=True, slots=True)
class ComparableResult:
    result_ref: AssessmentResultRef
    subject: ComparisonSubject | None
    value_kind: ComparisonValueKind
    status: FullModelStatus
    applicability: Applicability
    exact_value: Fraction | None
    categorical_state: str | None
    numeric_scale_or_none: str | None
    process_stage: ProcessStage
    rule_refs: tuple[object, ...]
    model_refs: tuple[object, ...]
    parameter_set_refs: tuple[object, ...]
    source_contract_ref: ContractRef
    calibration_status_or_none: CalibrationStatus | None

    def __post_init__(self) -> None:
        if not isinstance(self.result_ref, AssessmentResultRef):
            raise TypeError("result_ref must be an AssessmentResultRef")
        if not isinstance(self.value_kind, ComparisonValueKind):
            raise TypeError("value_kind must be a ComparisonValueKind")
        if not isinstance(self.status, FullModelStatus):
            raise TypeError("status must be a FullModelStatus")
        if not isinstance(self.applicability, Applicability):
            raise TypeError("applicability must be an Applicability")
        if not isinstance(self.process_stage, ProcessStage):
            raise TypeError("process_stage must be a ProcessStage")
        if self.value_kind is ComparisonValueKind.EXACT_FRACTION:
            if self.status is FullModelStatus.AVAILABLE:
                if not isinstance(self.exact_value, Fraction):
                    raise ValueError("available numeric result requires an exact Fraction")
                _identifier(self.numeric_scale_or_none, "numeric_scale_or_none")
            elif self.exact_value is not None:
                raise ValueError("non-available numeric result cannot carry a value")
            if self.categorical_state is not None:
                raise ValueError("numeric results cannot carry a categorical state")
        elif self.exact_value is not None or self.numeric_scale_or_none is not None:
            raise ValueError("categorical results cannot carry numeric fields")
        elif (
            self.status is FullModelStatus.AVAILABLE
            and not isinstance(self.categorical_state, str)
        ):
            raise ValueError("available categorical result requires its typed state")


class CompatibilityComponentKind(str, Enum):
    RULE = "RULE"
    MODEL = "MODEL"
    PARAMETER_SET = "PARAMETER_SET"


class CompatibilityDisposition(str, Enum):
    COMPATIBLE_FOR_COMPARISON = "COMPATIBLE_FOR_COMPARISON"
    INCOMPATIBLE = "INCOMPATIBLE"


@dataclass(frozen=True, slots=True)
class SemanticCompatibilityDeclaration:
    declaration_id: str
    component_kind: CompatibilityComponentKind
    before_ref: object
    after_ref: object
    comparison_scope: ComparisonSubject
    disposition: CompatibilityDisposition
    rationale: str
    authority_ref: ContractRef
    provenance: tuple[object, ...]

    def __post_init__(self) -> None:
        _identifier(self.declaration_id, "declaration_id")
        _identifier(self.rationale, "rationale")


class ComparisonKind(str, Enum):
    UNCHANGED = "UNCHANGED"
    INCREASED = "INCREASED"
    DECREASED = "DECREASED"
    STATE_CHANGED = "STATE_CHANGED"
    NOT_COMPARABLE = "NOT_COMPARABLE"


class ComparisonReason(str, Enum):
    EXACT_VALUES_EQUAL = "EXACT_VALUES_EQUAL"
    EXACT_VALUE_INCREASED = "EXACT_VALUE_INCREASED"
    EXACT_VALUE_DECREASED = "EXACT_VALUE_DECREASED"
    STRUCTURED_STATE_UNCHANGED = "STRUCTURED_STATE_UNCHANGED"
    STRUCTURED_STATE_CHANGED = "STRUCTURED_STATE_CHANGED"
    REQUIRED_RESULT_UNAVAILABLE = "REQUIRED_RESULT_UNAVAILABLE"
    RESULT_IDENTITY_UNRESOLVED = "RESULT_IDENTITY_UNRESOLVED"
    RESULT_FAMILY_MISMATCH = "RESULT_FAMILY_MISMATCH"
    VALUE_KIND_OR_SCALE_MISMATCH = "VALUE_KIND_OR_SCALE_MISMATCH"
    METRIC_OR_CHARACTERISTIC_MISMATCH = "METRIC_OR_CHARACTERISTIC_MISMATCH"
    SUBJECT_LINEAGE_MISSING_OR_MISMATCH = "SUBJECT_LINEAGE_MISSING_OR_MISMATCH"
    ARTIFACT_ANCESTRY_MISSING_OR_MISMATCH = "ARTIFACT_ANCESTRY_MISSING_OR_MISMATCH"
    SCOPE_OR_POPULATION_MISMATCH = "SCOPE_OR_POPULATION_MISMATCH"
    RULE_SEMANTICS_INCOMPATIBLE = "RULE_SEMANTICS_INCOMPATIBLE"
    MODEL_SEMANTICS_INCOMPATIBLE = "MODEL_SEMANTICS_INCOMPATIBLE"
    PARAMETER_SEMANTICS_INCOMPATIBLE = "PARAMETER_SEMANTICS_INCOMPATIBLE"
    EVIDENCE_CONTEXT_MISMATCH = "EVIDENCE_CONTEXT_MISMATCH"
    PROCESS_STAGE_MISMATCH = "PROCESS_STAGE_MISMATCH"
    APPLICABILITY_SEMANTICS_INCOMPATIBLE = "APPLICABILITY_SEMANTICS_INCOMPATIBLE"
    RESULT_FAMILY_UNSUPPORTED = "RESULT_FAMILY_UNSUPPORTED"


class ComparisonClaim(str, Enum):
    STRUCTURED_CHANGE_ONLY = "STRUCTURED_CHANGE_ONLY"


class ComparisonNonClaim(str, Enum):
    NO_DIRECTIONAL_QUALITY_INTERPRETATION = "NO_DIRECTIONAL_QUALITY_INTERPRETATION"
    NO_CAUSAL_EFFECT_INFERENCE = "NO_CAUSAL_EFFECT_INFERENCE"
    NO_ACTION_SUCCESS_INFERENCE = "NO_ACTION_SUCCESS_INFERENCE"
    NO_STAKEHOLDER_INTENT_VALIDATION = "NO_STAKEHOLDER_INTENT_VALIDATION"


@dataclass(frozen=True, slots=True)
class ComparisonRequest:
    comparison_id: str
    comparison_version: str
    before: ComparableResult | None
    after: ComparableResult | None
    artifact_transition: ArtifactTransition | None
    compatibility_declarations: tuple[SemanticCompatibilityDeclaration, ...] = ()

    def __post_init__(self) -> None:
        _identifier(self.comparison_id, "comparison_id")
        _identifier(self.comparison_version, "comparison_version")

    @property
    def ref(self) -> ComparisonRequestRef:
        return ComparisonRequestRef(self.comparison_id, self.comparison_version)


@dataclass(frozen=True, slots=True)
class ResultStateAndValue:
    status: FullModelStatus
    applicability: Applicability
    exact_value: Fraction | None
    categorical_state: str | None


@dataclass(frozen=True, slots=True)
class ResultComparison:
    comparison_id: str
    comparison_version: str
    before_result_ref: AssessmentResultRef | None
    after_result_ref: AssessmentResultRef | None
    comparison_subject: ComparisonSubject | None
    status: FullModelStatus
    comparison_kind: ComparisonKind | None
    before_state_and_value: ResultStateAndValue | None
    after_state_and_value: ResultStateAndValue | None
    reason_codes: tuple[ComparisonReason, ...]
    rule_ref: RuleRef
    compatibility_declaration_refs: tuple[str, ...]
    parameter_set_refs: tuple[object, ...]
    calibration_status_or_none: CalibrationStatus | None
    explanation: str
    provenance: tuple[object, ...]
    claims: tuple[ComparisonClaim, ...]
    non_claims: tuple[ComparisonNonClaim, ...]

    def __post_init__(self) -> None:
        if self.rule_ref != COMPARISON_RULE_REF:
            raise ValueError("comparison requires COMPARE-FULL-MODEL-001 / 1")
        if self.status is FullModelStatus.AVAILABLE:
            if self.comparison_kind is None:
                raise ValueError("available comparison requires a conclusion")
        elif self.comparison_kind is not None:
            raise ValueError("non-available comparison cannot fabricate a conclusion")


MANDATORY_COMPARISON_NON_CLAIMS = tuple(ComparisonNonClaim)


__all__ = [name for name in globals() if not name.startswith("_")]

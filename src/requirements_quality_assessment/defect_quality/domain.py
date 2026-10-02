"""Immutable domain records for the bounded Full Model v0.1 ``D -> R_DQ`` path.

The types in this module deliberately model only the contract-approved QB
conflict projection and its relevance to Performance Efficiency. They contain
no risk, severity, probability, impact, priority, or corrective-action fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..cross_analysis import (
    RESULT_CANONICAL_VERSION,
    AssessmentSnapshot,
    AssessmentSnapshotId,
    BoundedConflictSubtype,
    BoundedNonClaimKey,
    ComparisonKey,
    ConflictClass,
    CrossDiagnosticRef,
    CrossEvidenceRef,
    CrossObservationRef,
    CrossRequirementResult,
    CrossResultId,
    CrossResultState,
)
from ..dynamic_evidence import Applicability, FullModelStatus
from ..metrics import (
    FULL_MODEL_CONTRACT_REF,
    ArtifactRef,
    AssessmentRef,
    ContractRef,
    QbConsistencyAssessmentRef,
    RequirementSubjectRef,
    RuleRef,
    RuleVersionAuthority,
    SpecificationSubjectRef,
)
from ..performance_efficiency import (
    ProcessStateRef,
    ProductQualityCharacteristicId,
)


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


def _typed_tuple(
    value: object,
    item_types: type | tuple[type, ...],
    name: str,
) -> None:
    if not isinstance(value, tuple) or any(
        not isinstance(item, item_types) for item in value
    ):
        raise TypeError(f"{name} must be a tuple of approved values")


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
        FullModelStatus.UNKNOWN: {
            Applicability.APPLICABLE,
            Applicability.UNKNOWN,
        },
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


class ProblemClaimSourceKind(str, Enum):
    QB_CROSS_REQUIREMENT_RESULT = "QB_CROSS_REQUIREMENT_RESULT"
    DETECTOR_OBSERVATION = "DETECTOR_OBSERVATION"
    DIAGNOSTIC = "DIAGNOSTIC"
    SIGNAL_FINDING = "SIGNAL_FINDING"
    CHARACTERISTIC_ASSESSMENT = "CHARACTERISTIC_ASSESSMENT"
    SPECIFICATION_AGGREGATE = "SPECIFICATION_AGGREGATE"
    COMPLETED_ABSENCE = "COMPLETED_ABSENCE"
    CONFORMANCE_ASSESSMENT = "CONFORMANCE_ASSESSMENT"
    PRODUCT_QUALITY_ASSESSMENT = "PRODUCT_QUALITY_ASSESSMENT"
    OTHER_CONFLICT_CLAIM = "OTHER_CONFLICT_CLAIM"
    FUTURE_APPROVED_SOURCE = "FUTURE_APPROVED_SOURCE"


class ProblemDisposition(str, Enum):
    CONFIRMED_SUPPORTED_PROBLEM = "CONFIRMED_SUPPORTED_PROBLEM"
    NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE = (
        "NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE"
    )


class ProblemKind(str, Enum):
    CONFIRMED_SUPPORTED_PROBLEM = "CONFIRMED_SUPPORTED_PROBLEM"


class DefectType(str, Enum):
    SPECIFICATION_INCONSISTENCY = "SPECIFICATION_INCONSISTENCY"


class ProblemResolutionReason(str, Enum):
    CONFIRMED_QB_CONFLICT = "CONFIRMED_QB_CONFLICT"
    QB_COMPATIBLE_WITHIN_RULE = "QB_COMPATIBLE_WITHIN_RULE"
    QB_ASSESSMENT_UNRESOLVED = "QB_ASSESSMENT_UNRESOLVED"
    QB_OUTSIDE_V0_1_APPLICABILITY = "QB_OUTSIDE_V0_1_APPLICABILITY"
    SUPPORTED_SOURCE_UNAVAILABLE = "SUPPORTED_SOURCE_UNAVAILABLE"
    SOURCE_STATE_UNKNOWN = "SOURCE_STATE_UNKNOWN"
    SOURCE_KIND_UNSUPPORTED = "SOURCE_KIND_UNSUPPORTED"


class ProblemNonClaim(str, Enum):
    NOT_GENERAL_SPECIFICATION_CONSISTENCY = "NC-D-001"
    NOT_PRODUCT_DEFECT = "NC-D-002"
    NOT_CV_OR_U_SIGNAL_PROMOTION = "NC-D-003"
    NOT_RQD_016_CLOSURE = "NC-D-004"
    NO_SEVERITY_OR_CONFIDENCE_SCORE = "NC-D-005"
    NO_CAUSAL_CLAIM = "NC-D-006"


class RelationKind(str, Enum):
    BOUNDED_RISK_RELEVANCE = "BOUNDED_RISK_RELEVANCE"


class RelationReason(str, Enum):
    EXACT_RESPONSE_TIME_KEY = "EXACT_RESPONSE_TIME_KEY"
    NO_CONFIRMED_SUPPORTED_PROBLEM = "NO_CONFIRMED_SUPPORTED_PROBLEM"
    DIFFERENT_RESOLVED_METRIC = "DIFFERENT_RESOLVED_METRIC"
    UNSUPPORTED_RESPONSE_TIME_CONTEXT_OR_UNIT = (
        "UNSUPPORTED_RESPONSE_TIME_CONTEXT_OR_UNIT"
    )
    PROBLEM_CLAIM_UNRESOLVED = "PROBLEM_CLAIM_UNRESOLVED"
    PROBLEM_CLAIM_UNSUPPORTED = "PROBLEM_CLAIM_UNSUPPORTED"
    PROBLEM_CLAIM_UNAVAILABLE = "PROBLEM_CLAIM_UNAVAILABLE"
    PROBLEM_CLAIM_UNKNOWN = "PROBLEM_CLAIM_UNKNOWN"
    PROBLEM_CLAIM_NOT_APPLICABLE = "PROBLEM_CLAIM_NOT_APPLICABLE"


class RelationNonClaim(str, Enum):
    NOT_NUMERIC_RHO = "NC-RDQ-001"
    NOT_CAUSALITY = "NC-RDQ-002"
    NOT_PROBABILITY_OR_IMPACT = "NC-RDQ-003"
    NOT_PROOF_OF_POOR_PRODUCT_PERFORMANCE = "NC-RDQ-004"
    NOT_MAPPING_BEYOND_EXACT_RESPONSE_TIME_KEY = "NC-RDQ-005"


class DefectQualityCalibrationStatus(str, Enum):
    PROVISIONAL_NOT_CALIBRATED = "PROVISIONAL_NOT_CALIBRATED"


class BoundOperandPosition(str, Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


MANDATORY_PROBLEM_NON_CLAIMS = tuple(ProblemNonClaim)
MANDATORY_RELATION_NON_CLAIMS = tuple(RelationNonClaim)

DEFECT_QUALITY_RISK_CONTRACT_REF = ContractRef(
    "FULL-MODEL-V0.1-DEFECT-QUALITY-RISK", "1"
)
QB_NORMALIZATION_CONTRACT_REF = ContractRef("QB-NORMALIZATION", "1")
PROBLEM_RULE_REF = RuleRef(
    "D-QB-CONFLICT-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)
RELATION_RULE_REF = RuleRef(
    "R_DQ-PE-QB-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)


@dataclass(frozen=True, slots=True, order=True)
class TypedSourceRef:
    source_kind: ProblemClaimSourceKind
    source_id: str
    source_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.source_kind, ProblemClaimSourceKind):
            raise TypeError("source_kind must be a ProblemClaimSourceKind")
        _identifier(self.source_id, "source_id")
        _identifier(self.source_version, "source_version")


@dataclass(frozen=True, slots=True)
class TypedProblemClaimSource:
    source_claim_ref: TypedSourceRef
    status: FullModelStatus
    applicability: Applicability
    cross_result: CrossRequirementResult | None = None
    source_snapshot: AssessmentSnapshot | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_claim_ref, TypedSourceRef):
            raise TypeError("source_claim_ref must be a TypedSourceRef")
        _validate_status_applicability(self.status, self.applicability)
        is_qb = (
            self.source_claim_ref.source_kind
            is ProblemClaimSourceKind.QB_CROSS_REQUIREMENT_RESULT
        )
        if not is_qb:
            if self.cross_result is not None or self.source_snapshot is not None:
                raise ValueError("non-QB claims cannot carry QB records")
            return
        if self.cross_result is None:
            if self.source_snapshot is not None:
                raise ValueError("an absent QB result cannot carry a source snapshot")
            if self.status not in {
                FullModelStatus.UNAVAILABLE,
                FullModelStatus.UNKNOWN,
            }:
                raise ValueError("an absent QB result must be UNAVAILABLE or UNKNOWN")
            return
        if not isinstance(self.cross_result, CrossRequirementResult):
            raise TypeError("cross_result must be a CrossRequirementResult or None")
        if not isinstance(self.source_snapshot, AssessmentSnapshot):
            raise TypeError("a QB result requires its AssessmentSnapshot")
        if self.cross_result.snapshot_id != self.source_snapshot.snapshot_id:
            raise ValueError("QB claim result and source snapshot cannot differ")
        expected_ref = TypedSourceRef(
            ProblemClaimSourceKind.QB_CROSS_REQUIREMENT_RESULT,
            self.cross_result.result_id.value,
            RESULT_CANONICAL_VERSION,
        )
        if self.source_claim_ref != expected_ref:
            raise ValueError("QB source reference must name the exact cross result")
        expected_status = {
            CrossResultState.CONFIRMED_CONFLICT: FullModelStatus.AVAILABLE,
            CrossResultState.COMPATIBLE_WITHIN_RULE: FullModelStatus.AVAILABLE,
            CrossResultState.ASSESSMENT_UNRESOLVED: FullModelStatus.UNRESOLVED,
            CrossResultState.OUTSIDE_V0_1_APPLICABILITY: (
                FullModelStatus.NOT_APPLICABLE
            ),
        }[self.cross_result.state]
        if self.status is not expected_status:
            raise ValueError("QB source status must preserve its cross-result state")
        if self.cross_result.state is CrossResultState.OUTSIDE_V0_1_APPLICABILITY:
            if self.applicability is not Applicability.NOT_APPLICABLE:
                raise ValueError("outside QB results must be NOT_APPLICABLE")
        elif self.cross_result.state is CrossResultState.ASSESSMENT_UNRESOLVED:
            if self.applicability not in {
                Applicability.APPLICABLE,
                Applicability.UNKNOWN,
            }:
                raise ValueError("unresolved QB applicability must remain open")
        elif self.applicability is not Applicability.APPLICABLE:
            raise ValueError("completed QB results must be APPLICABLE")

    @classmethod
    def from_qb_result(
        cls,
        result: CrossRequirementResult,
        snapshot: AssessmentSnapshot,
        *,
        unresolved_applicability: Applicability = Applicability.APPLICABLE,
    ) -> TypedProblemClaimSource:
        status = {
            CrossResultState.CONFIRMED_CONFLICT: FullModelStatus.AVAILABLE,
            CrossResultState.COMPATIBLE_WITHIN_RULE: FullModelStatus.AVAILABLE,
            CrossResultState.ASSESSMENT_UNRESOLVED: FullModelStatus.UNRESOLVED,
            CrossResultState.OUTSIDE_V0_1_APPLICABILITY: (
                FullModelStatus.NOT_APPLICABLE
            ),
        }[result.state]
        applicability = {
            CrossResultState.CONFIRMED_CONFLICT: Applicability.APPLICABLE,
            CrossResultState.COMPATIBLE_WITHIN_RULE: Applicability.APPLICABLE,
            CrossResultState.ASSESSMENT_UNRESOLVED: unresolved_applicability,
            CrossResultState.OUTSIDE_V0_1_APPLICABILITY: (
                Applicability.NOT_APPLICABLE
            ),
        }[result.state]
        return cls(
            TypedSourceRef(
                ProblemClaimSourceKind.QB_CROSS_REQUIREMENT_RESULT,
                result.result_id.value,
                RESULT_CANONICAL_VERSION,
            ),
            status,
            applicability,
            result,
            snapshot,
        )

    @classmethod
    def unsupported(
        cls,
        source_kind: ProblemClaimSourceKind,
        source_id: str,
        source_version: str,
        *,
        applicability: Applicability = Applicability.APPLICABLE,
    ) -> TypedProblemClaimSource:
        if source_kind in {
            ProblemClaimSourceKind.QB_CROSS_REQUIREMENT_RESULT,
            ProblemClaimSourceKind.FUTURE_APPROVED_SOURCE,
        }:
            raise ValueError("use a QB or future-source constructor for this kind")
        return cls(
            TypedSourceRef(source_kind, source_id, source_version),
            (
                FullModelStatus.AVAILABLE
                if applicability is Applicability.APPLICABLE
                else FullModelStatus.UNKNOWN
            ),
            applicability,
        )


@dataclass(frozen=True, slots=True)
class DefectConstructionContext:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    full_model_contract_ref: ContractRef = FULL_MODEL_CONTRACT_REF
    defect_risk_contract_ref: ContractRef = DEFECT_QUALITY_RISK_CONTRACT_REF
    problem_rule_ref: RuleRef = PROBLEM_RULE_REF

    def __post_init__(self) -> None:
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("source assessment must name the context artifact")
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("unsupported Full Model contract")
        if self.defect_risk_contract_ref != DEFECT_QUALITY_RISK_CONTRACT_REF:
            raise ValueError("unsupported defect-quality contract")
        if self.problem_rule_ref != PROBLEM_RULE_REF:
            raise ValueError("unsupported problem construction rule")


@dataclass(frozen=True, slots=True, order=True)
class ProblemClaimResolutionId:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    source_claim_ref: TypedSourceRef
    problem_rule_ref: RuleRef


@dataclass(frozen=True, slots=True, order=True)
class ProblemClaimResolutionRef:
    resolution_id: ProblemClaimResolutionId


@dataclass(frozen=True, slots=True, order=True)
class ConfirmedSupportedProblemId:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    source_cross_result_ref: CrossResultId
    problem_rule_ref: RuleRef


@dataclass(frozen=True, slots=True, order=True)
class ConfirmedSupportedProblemRef:
    problem_id: ConfirmedSupportedProblemId


@dataclass(frozen=True, slots=True, order=True)
class QbBoundOperandRef:
    source_cross_result_ref: CrossResultId
    position: BoundOperandPosition
    source_observation_ref: CrossObservationRef


@dataclass(frozen=True, slots=True)
class ConflictClassificationRef:
    source_cross_result_ref: CrossResultId
    conflict_class: ConflictClass
    conflict_subtype: BoundedConflictSubtype


@dataclass(frozen=True, slots=True)
class ConfirmedProblemProvenance:
    source_cross_result_ref: CrossResultId
    source_snapshot_id: AssessmentSnapshotId
    participant_refs: tuple[RequirementSubjectRef, RequirementSubjectRef]
    source_observation_refs: tuple[CrossObservationRef, CrossObservationRef]
    comparison_key: ComparisonKey
    exact_operand_refs: tuple[QbBoundOperandRef, QbBoundOperandRef]
    ordered_cross_evidence_refs: tuple[CrossEvidenceRef, ...]
    diagnostic_refs: tuple[CrossDiagnosticRef, ...]
    normalization_contract_ref: ContractRef
    coverage_profile_ref: ContractRef
    comparison_rule_ref: ContractRef
    conflict_classification_ref: ConflictClassificationRef
    source_non_claim_refs: tuple[BoundedNonClaimKey, ...]
    problem_rule_ref: RuleRef

    def __post_init__(self) -> None:
        _typed_tuple(self.participant_refs, RequirementSubjectRef, "participant_refs")
        if len(self.participant_refs) != 2:
            raise ValueError("problem provenance requires two participants")
        _typed_tuple(
            self.source_observation_refs,
            CrossObservationRef,
            "source_observation_refs",
        )
        if len(self.source_observation_refs) != 2:
            raise ValueError("problem provenance requires two observations")
        _typed_tuple(self.exact_operand_refs, QbBoundOperandRef, "exact_operand_refs")
        if len(self.exact_operand_refs) != 2:
            raise ValueError("problem provenance requires two operand refs")
        _typed_tuple(
            self.ordered_cross_evidence_refs,
            CrossEvidenceRef,
            "ordered_cross_evidence_refs",
        )
        _typed_tuple(self.diagnostic_refs, CrossDiagnosticRef, "diagnostic_refs")
        _typed_tuple(
            self.source_non_claim_refs,
            BoundedNonClaimKey,
            "source_non_claim_refs",
        )
        if self.normalization_contract_ref != QB_NORMALIZATION_CONTRACT_REF:
            raise ValueError("problem provenance requires QB-NORMALIZATION / 1")
        if self.problem_rule_ref != PROBLEM_RULE_REF:
            raise ValueError("problem provenance requires D-QB-CONFLICT-001 / 1")


@dataclass(frozen=True, slots=True)
class ConfirmedSupportedProblem:
    problem_id: ConfirmedSupportedProblemId
    problem_kind: ProblemKind
    defect_type: DefectType
    conflict_class: ConflictClass
    conflict_subtype: BoundedConflictSubtype
    target_ref: SpecificationSubjectRef
    participant_refs: tuple[RequirementSubjectRef, RequirementSubjectRef]
    source_cross_result_ref: CrossResultId
    source_observation_refs: tuple[CrossObservationRef, CrossObservationRef]
    comparison_key: ComparisonKey
    operand_refs: tuple[QbBoundOperandRef, QbBoundOperandRef]
    status: FullModelStatus
    applicability: Applicability
    evidence_refs: tuple[CrossEvidenceRef, ...]
    diagnostic_refs: tuple[CrossDiagnosticRef, ...]
    explanation: str
    provenance: ConfirmedProblemProvenance
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    rule_ref: RuleRef
    non_claims: tuple[ProblemNonClaim, ...]

    def __post_init__(self) -> None:
        expected_id = ConfirmedSupportedProblemId(
            self.artifact_ref,
            self.source_assessment_ref,
            self.source_snapshot_id,
            self.source_cross_result_ref,
            self.rule_ref,
        )
        if self.problem_id != expected_id:
            raise ValueError("problem_id must be the structured problem identity")
        if self.problem_kind is not ProblemKind.CONFIRMED_SUPPORTED_PROBLEM:
            raise ValueError("unsupported problem kind")
        if self.defect_type is not DefectType.SPECIFICATION_INCONSISTENCY:
            raise ValueError("unsupported defect type")
        if self.conflict_class is not ConflictClass.LOGICAL_CONFLICT:
            raise ValueError("problem requires LOGICAL_CONFLICT")
        if (
            self.conflict_subtype
            is not BoundedConflictSubtype.DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY
        ):
            raise ValueError("problem requires the direct quantitative subtype")
        if self.target_ref != SpecificationSubjectRef(self.artifact_ref):
            raise ValueError("problem target must be the specification artifact")
        _typed_tuple(self.participant_refs, RequirementSubjectRef, "participant_refs")
        _typed_tuple(
            self.source_observation_refs,
            CrossObservationRef,
            "source_observation_refs",
        )
        _typed_tuple(self.operand_refs, QbBoundOperandRef, "operand_refs")
        if any(
            len(values) != 2
            for values in (
                self.participant_refs,
                self.source_observation_refs,
                self.operand_refs,
            )
        ):
            raise ValueError("problem requires exactly two participants and operands")
        if any(item.artifact_ref != self.artifact_ref for item in self.participant_refs):
            raise ValueError("problem participants cannot cross artifacts")
        if tuple(item.requirement_id for item in self.participant_refs) != tuple(
            item.requirement_id for item in self.source_observation_refs
        ):
            raise ValueError("problem observations must belong to its participants")
        if tuple(item.source_observation_ref for item in self.operand_refs) != (
            self.source_observation_refs
        ):
            raise ValueError("problem operand refs must preserve observation order")
        if tuple(item.position for item in self.operand_refs) != (
            BoundOperandPosition.LEFT,
            BoundOperandPosition.RIGHT,
        ):
            raise ValueError("problem operand refs must preserve left/right order")
        if any(
            item.source_cross_result_ref != self.source_cross_result_ref
            for item in self.operand_refs
        ):
            raise ValueError("problem operand refs must name the source cross result")
        _validate_status_applicability(self.status, self.applicability)
        if (
            self.status is not FullModelStatus.AVAILABLE
            or self.applicability is not Applicability.APPLICABLE
        ):
            raise ValueError("a confirmed problem must be AVAILABLE/APPLICABLE")
        _typed_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        _typed_tuple(self.diagnostic_refs, CrossDiagnosticRef, "diagnostic_refs")
        _identifier(self.explanation, "explanation")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("problem cannot mix artifacts and assessments")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        if self.rule_ref != PROBLEM_RULE_REF:
            raise ValueError("problem requires D-QB-CONFLICT-001 / 1")
        if self.non_claims != MANDATORY_PROBLEM_NON_CLAIMS:
            raise ValueError("problem must carry all mandatory non-claims in order")
        if (
            self.provenance.source_cross_result_ref != self.source_cross_result_ref
            or self.provenance.source_snapshot_id != self.source_snapshot_id
            or self.provenance.participant_refs != self.participant_refs
            or self.provenance.source_observation_refs != self.source_observation_refs
            or self.provenance.comparison_key != self.comparison_key
            or self.provenance.exact_operand_refs != self.operand_refs
            or self.provenance.ordered_cross_evidence_refs != self.evidence_refs
            or self.provenance.diagnostic_refs != self.diagnostic_refs
            or self.provenance.problem_rule_ref != self.rule_ref
        ):
            raise ValueError("problem and provenance must preserve the same source graph")

    @property
    def ref(self) -> ConfirmedSupportedProblemRef:
        return ConfirmedSupportedProblemRef(self.problem_id)


@dataclass(frozen=True, slots=True)
class ProblemClaimResolution:
    resolution_id: ProblemClaimResolutionId
    source_claim_ref: TypedSourceRef
    status: FullModelStatus
    applicability: Applicability
    disposition: ProblemDisposition | None
    problem: ConfirmedSupportedProblem | None
    explanation: str
    reasons: tuple[ProblemResolutionReason, ...]
    evidence_refs: tuple[CrossEvidenceRef, ...]
    provenance_refs: tuple[TypedSourceRef | ContractRef | RuleRef, ...]
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    rule_ref: RuleRef

    def __post_init__(self) -> None:
        expected_id = ProblemClaimResolutionId(
            self.artifact_ref,
            self.source_assessment_ref,
            self.source_snapshot_id,
            self.source_claim_ref,
            self.rule_ref,
        )
        if self.resolution_id != expected_id:
            raise ValueError("resolution_id must be the structured resolution identity")
        _validate_status_applicability(self.status, self.applicability)
        _identifier(self.explanation, "explanation")
        _typed_tuple(self.reasons, ProblemResolutionReason, "reasons")
        if len(self.reasons) != 1:
            raise ValueError("a problem resolution requires one controlling reason")
        _typed_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        _typed_tuple(
            self.provenance_refs,
            (TypedSourceRef, ContractRef, RuleRef),
            "provenance_refs",
        )
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("resolution cannot mix artifacts and assessments")
        if self.rule_ref != PROBLEM_RULE_REF:
            raise ValueError("resolution requires D-QB-CONFLICT-001 / 1")
        if self.status is FullModelStatus.AVAILABLE:
            if self.disposition is ProblemDisposition.CONFIRMED_SUPPORTED_PROBLEM:
                if self.problem is None:
                    raise ValueError("positive disposition requires a problem")
            elif (
                self.disposition
                is ProblemDisposition.NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE
            ):
                if self.problem is not None:
                    raise ValueError("no-problem disposition cannot carry a problem")
            else:
                raise ValueError("AVAILABLE resolution requires a disposition")
        elif self.disposition is not None or self.problem is not None:
            raise ValueError("non-AVAILABLE resolutions cannot fabricate a problem")
        if self.problem is not None and (
            self.problem.artifact_ref != self.artifact_ref
            or self.problem.source_assessment_ref != self.source_assessment_ref
            or self.problem.source_snapshot_id != self.source_snapshot_id
            or self.problem.rule_ref != self.rule_ref
        ):
            raise ValueError("problem and resolution contexts must agree")

    @property
    def ref(self) -> ProblemClaimResolutionRef:
        return ProblemClaimResolutionRef(self.resolution_id)


@dataclass(frozen=True, slots=True, order=True)
class DefectPopulationId:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    problem_rule_ref: RuleRef


@dataclass(frozen=True, slots=True, order=True)
class DefectPopulationSnapshotRef:
    population_id: DefectPopulationId


@dataclass(frozen=True, slots=True)
class DefectPopulationSnapshot:
    population_id: DefectPopulationId
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    status: FullModelStatus
    applicability: Applicability
    members: tuple[ConfirmedSupportedProblemRef, ...]
    population_complete: bool
    problem_resolution_refs: tuple[ProblemClaimResolutionRef, ...]
    unresolved_resolution_refs: tuple[ProblemClaimResolutionRef, ...]
    source_qb_assessment_ref: QbConsistencyAssessmentRef
    provenance_refs: tuple[TypedSourceRef | ContractRef | RuleRef, ...]
    rule_ref: RuleRef

    def __post_init__(self) -> None:
        if self.population_id != DefectPopulationId(
            self.artifact_ref,
            self.source_assessment_ref,
            self.source_snapshot_id,
            self.rule_ref,
        ):
            raise ValueError("population_id must be the structured population identity")
        _validate_status_applicability(self.status, self.applicability)
        _typed_tuple(self.members, ConfirmedSupportedProblemRef, "members")
        _typed_tuple(
            self.problem_resolution_refs,
            ProblemClaimResolutionRef,
            "problem_resolution_refs",
        )
        _typed_tuple(
            self.unresolved_resolution_refs,
            ProblemClaimResolutionRef,
            "unresolved_resolution_refs",
        )
        _unique(self.members, "members")
        _unique(self.problem_resolution_refs, "problem_resolution_refs")
        _unique(self.unresolved_resolution_refs, "unresolved_resolution_refs")
        if type(self.population_complete) is not bool:
            raise TypeError("population_complete must be a boolean")
        if self.status is FullModelStatus.AVAILABLE and not self.population_complete:
            raise ValueError("AVAILABLE population must be complete")
        if self.status is FullModelStatus.NOT_APPLICABLE and (
            not self.population_complete or self.members
        ):
            raise ValueError("NOT_APPLICABLE population must be complete and empty")
        if self.status in {FullModelStatus.UNKNOWN, FullModelStatus.UNRESOLVED} and (
            self.population_complete
        ):
            raise ValueError("unknown or unresolved populations must be incomplete")
        if self.source_qb_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("population QB assessment cannot cross artifacts")
        if self.source_qb_assessment_ref.assessment_ref != self.source_assessment_ref:
            raise ValueError("population QB assessment cannot cross assessments")
        if self.source_qb_assessment_ref.snapshot_id != self.source_snapshot_id:
            raise ValueError("population QB assessment cannot cross snapshots")
        if self.rule_ref != PROBLEM_RULE_REF:
            raise ValueError("population requires D-QB-CONFLICT-001 / 1")

    @property
    def ref(self) -> DefectPopulationSnapshotRef:
        return DefectPopulationSnapshotRef(self.population_id)


@dataclass(frozen=True, slots=True)
class DefectQualityRelationContext:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    full_model_contract_ref: ContractRef = FULL_MODEL_CONTRACT_REF
    defect_risk_contract_ref: ContractRef = DEFECT_QUALITY_RISK_CONTRACT_REF
    relation_rule_ref: RuleRef = RELATION_RULE_REF

    def __post_init__(self) -> None:
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("source assessment must name the relation artifact")
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("unsupported Full Model contract")
        if self.defect_risk_contract_ref != DEFECT_QUALITY_RISK_CONTRACT_REF:
            raise ValueError("unsupported defect-quality contract")
        if self.relation_rule_ref != RELATION_RULE_REF:
            raise ValueError("unsupported defect-quality relation rule")


@dataclass(frozen=True, slots=True, order=True)
class DefectQualityRelationId:
    problem_resolution_ref: ProblemClaimResolutionRef
    problem_ref: ConfirmedSupportedProblemRef | None
    characteristic_id: ProductQualityCharacteristicId
    relation_rule_ref: RuleRef


@dataclass(frozen=True, slots=True, order=True)
class DefectQualityRelationRef:
    relation_id: DefectQualityRelationId


@dataclass(frozen=True, slots=True)
class DefectQualityRelationProvenance:
    problem_resolution_ref: ProblemClaimResolutionRef
    problem_ref: ConfirmedSupportedProblemRef | None
    source_cross_result_ref: CrossResultId | None
    comparison_key: ComparisonKey | None
    characteristic_id: ProductQualityCharacteristicId
    relation_rule_ref: RuleRef
    rationale_code: RelationReason
    evidence_refs: tuple[CrossEvidenceRef, ...]
    source_contract_refs: tuple[ContractRef, ...]

    def __post_init__(self) -> None:
        _typed_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        _typed_tuple(self.source_contract_refs, ContractRef, "source_contract_refs")
        _unique(self.source_contract_refs, "source_contract_refs")
        if (
            self.characteristic_id
            is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY
        ):
            raise ValueError("relation provenance supports Performance Efficiency only")
        if self.relation_rule_ref != RELATION_RULE_REF:
            raise ValueError("relation provenance requires R_DQ-PE-QB-001 / 1")


@dataclass(frozen=True, slots=True)
class DefectQualityRelation:
    relation_id: DefectQualityRelationId
    problem_resolution_ref: ProblemClaimResolutionRef
    problem_ref: ConfirmedSupportedProblemRef | None
    characteristic_id: ProductQualityCharacteristicId
    relation_kind: RelationKind | None
    status: FullModelStatus
    applicability: Applicability
    rationale: str
    reasons: tuple[RelationReason, ...]
    source_result_refs: tuple[TypedSourceRef, ...]
    evidence_refs: tuple[CrossEvidenceRef, ...]
    provenance: DefectQualityRelationProvenance
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    rule_ref: RuleRef
    calibration_status: DefectQualityCalibrationStatus
    non_claims: tuple[RelationNonClaim, ...]

    def __post_init__(self) -> None:
        expected_id = DefectQualityRelationId(
            self.problem_resolution_ref,
            self.problem_ref,
            self.characteristic_id,
            self.rule_ref,
        )
        if self.relation_id != expected_id:
            raise ValueError("relation_id must be the structured relation identity")
        if (
            self.characteristic_id
            is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY
        ):
            raise ValueError("R_DQ supports Performance Efficiency only")
        _validate_status_applicability(self.status, self.applicability)
        if self.status is FullModelStatus.AVAILABLE:
            if self.relation_kind is not RelationKind.BOUNDED_RISK_RELEVANCE:
                raise ValueError("AVAILABLE relation requires bounded relevance")
            if self.problem_ref is None:
                raise ValueError("AVAILABLE relation requires a confirmed problem")
        elif self.relation_kind is not None:
            raise ValueError("non-AVAILABLE relation cannot carry a relation kind")
        _identifier(self.rationale, "rationale")
        _typed_tuple(self.reasons, RelationReason, "reasons")
        if len(self.reasons) != 1:
            raise ValueError("a relation requires one controlling reason")
        _typed_tuple(self.source_result_refs, TypedSourceRef, "source_result_refs")
        _typed_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("relation cannot mix artifacts and assessments")
        if self.rule_ref != RELATION_RULE_REF:
            raise ValueError("relation requires R_DQ-PE-QB-001 / 1")
        if (
            self.calibration_status
            is not DefectQualityCalibrationStatus.PROVISIONAL_NOT_CALIBRATED
        ):
            raise ValueError("the bounded relation is provisional and uncalibrated")
        if self.non_claims != MANDATORY_RELATION_NON_CLAIMS:
            raise ValueError("relation must carry all mandatory non-claims in order")
        if (
            self.provenance.problem_resolution_ref != self.problem_resolution_ref
            or self.provenance.problem_ref != self.problem_ref
            or self.provenance.characteristic_id != self.characteristic_id
            or self.provenance.relation_rule_ref != self.rule_ref
            or self.provenance.rationale_code is not self.reasons[0]
            or self.provenance.evidence_refs != self.evidence_refs
        ):
            raise ValueError("relation and provenance must preserve the same source graph")

    @property
    def ref(self) -> DefectQualityRelationRef:
        return DefectQualityRelationRef(self.relation_id)


__all__ = [
    "DEFECT_QUALITY_RISK_CONTRACT_REF",
    "MANDATORY_PROBLEM_NON_CLAIMS",
    "MANDATORY_RELATION_NON_CLAIMS",
    "PROBLEM_RULE_REF",
    "QB_NORMALIZATION_CONTRACT_REF",
    "RELATION_RULE_REF",
    "BoundOperandPosition",
    "ConfirmedProblemProvenance",
    "ConfirmedSupportedProblem",
    "ConfirmedSupportedProblemId",
    "ConfirmedSupportedProblemRef",
    "ConflictClassificationRef",
    "DefectConstructionContext",
    "DefectPopulationId",
    "DefectPopulationSnapshot",
    "DefectPopulationSnapshotRef",
    "DefectQualityCalibrationStatus",
    "DefectQualityRelation",
    "DefectQualityRelationContext",
    "DefectQualityRelationId",
    "DefectQualityRelationProvenance",
    "DefectQualityRelationRef",
    "DefectType",
    "ProblemClaimResolution",
    "ProblemClaimResolutionId",
    "ProblemClaimResolutionRef",
    "ProblemClaimSourceKind",
    "ProblemDisposition",
    "ProblemKind",
    "ProblemNonClaim",
    "ProblemResolutionReason",
    "QbBoundOperandRef",
    "RelationKind",
    "RelationNonClaim",
    "RelationReason",
    "TypedProblemClaimSource",
    "TypedSourceRef",
]

"""Immutable domain records for the bounded Full Model v0.1 ``M_risk``.

The module implements categorical risk identification only. It deliberately
contains no numeric risk, probability, likelihood, impact, severity,
criticality, confidence, uncertainty, priority, rank, or corrective action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..cross_analysis import AssessmentSnapshotId, CrossEvidenceRef, CrossResultId
from ..defect_quality import (
    DEFECT_QUALITY_RISK_CONTRACT_REF,
    ConfirmedSupportedProblemRef,
    DefectPopulationSnapshotRef,
    DefectQualityRelationRef,
    ProblemClaimResolutionRef,
)
from ..dynamic_evidence import Applicability, FullModelStatus, ProductRef
from ..metrics import (
    FULL_MODEL_CONTRACT_REF,
    ArtifactRef,
    AssessmentRef,
    ContractRef,
    RequirementSubjectRef,
    RuleRef,
    RuleVersionAuthority,
)
from ..performance_efficiency import ProcessStateRef, ProductQualityCharacteristicId
from ..product_quality import (
    CalibrationStatus,
    ProductQualityAssessmentId,
    ProductQualityResultKind,
    ProductQualityScope,
)


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


def _typed_tuple(value: object, item_types: type | tuple[type, ...], name: str) -> None:
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


class RiskClassification(str, Enum):
    RISK_IDENTIFIED = "RISK_IDENTIFIED"


class RiskNonClaim(str, Enum):
    IDENTIFIED_PRESENCE_NOT_MAGNITUDE = "NC-RISK-001"
    NO_PROBABILITY_OR_LIKELIHOOD = "NC-RISK-002"
    NO_IMPACT_SEVERITY_OR_CRITICALITY = "NC-RISK-003"
    NO_WEIGHT_THRESHOLD_OR_AGGREGATE_RISK = "NC-RISK-004"
    NO_PRIORITY_OR_RANK = "NC-RISK-005"
    NOT_PRODUCT_FAILURE_OR_QUALITY_SCORE = "NC-RISK-006"
    NO_CAUSAL_CLAIM = "NC-RISK-007"
    ABSENCE_OF_BOUNDED_RISK_NOT_ABSENCE_OF_RISK = "NC-RISK-008"
    PROVISIONAL_NOT_CALIBRATED = "NC-RISK-009"


MANDATORY_RISK_NON_CLAIMS = tuple(RiskNonClaim)

RISK_MODEL_ID = "FULL-MODEL-V0.1-M-RISK-PE-QB"
RISK_MODEL_VERSION = "1"
RISK_RULE_ID = "RISK-PE-QB-001"
RISK_RULE_VERSION = "1"
RISK_PARAMETER_SET_ID = "RISK-PE-QB-001-PARAMETERS"
RISK_PARAMETER_SET_VERSION = "1"


@dataclass(frozen=True, slots=True, order=True)
class RiskModelRef:
    model_id: str
    model_version: str

    def __post_init__(self) -> None:
        _identifier(self.model_id, "model_id")
        _identifier(self.model_version, "model_version")


@dataclass(frozen=True, slots=True, order=True)
class RiskParameterSetRef:
    parameter_set_id: str
    parameter_set_version: str

    def __post_init__(self) -> None:
        _identifier(self.parameter_set_id, "parameter_set_id")
        _identifier(self.parameter_set_version, "parameter_set_version")


RISK_MODEL_REF = RiskModelRef(RISK_MODEL_ID, RISK_MODEL_VERSION)
RISK_RULE_REF = RuleRef(
    RISK_RULE_ID,
    RISK_RULE_VERSION,
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)
RISK_PARAMETER_SET_REF = RiskParameterSetRef(
    RISK_PARAMETER_SET_ID,
    RISK_PARAMETER_SET_VERSION,
)


@dataclass(frozen=True, slots=True)
class RiskParameterSet:
    parameter_set_id: str
    version: str
    entries: tuple[object, ...]
    source_or_rationale: str
    calibration_status: CalibrationStatus
    scope: str
    non_claim: str
    approved_contract_ref: ContractRef

    def __post_init__(self) -> None:
        if RiskParameterSetRef(self.parameter_set_id, self.version) != RISK_PARAMETER_SET_REF:
            raise ValueError("unsupported risk parameter set")
        if self.entries != ():
            raise ValueError("the v0.1 risk parameter set must remain empty")
        _identifier(self.source_or_rationale, "source_or_rationale")
        _identifier(self.scope, "scope")
        _identifier(self.non_claim, "non_claim")
        if self.calibration_status is not CalibrationStatus.PROVISIONAL_NOT_CALIBRATED:
            raise ValueError("the risk parameter set is provisional and not calibrated")
        if self.approved_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("risk parameters require the Full Model v0.1 contract")

    @property
    def parameter_set_ref(self) -> RiskParameterSetRef:
        return RiskParameterSetRef(self.parameter_set_id, self.version)


RISK_PARAMETER_SET = RiskParameterSet(
    parameter_set_id=RISK_PARAMETER_SET_ID,
    version=RISK_PARAMETER_SET_VERSION,
    entries=(),
    source_or_rationale="parent Full Model categorical reference rule",
    calibration_status=CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
    scope="presence of one bounded PE-related specification risk scenario",
    non_claim="no probability, impact, magnitude, severity, or priority",
    approved_contract_ref=FULL_MODEL_CONTRACT_REF,
)


@dataclass(frozen=True, slots=True, order=True)
class ProductQualityAssessmentRef:
    assessment_id: ProductQualityAssessmentId
    product_quality_assessment_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.assessment_id, ProductQualityAssessmentId):
            raise TypeError("assessment_id must be a ProductQualityAssessmentId")
        _identifier(
            self.product_quality_assessment_version,
            "product_quality_assessment_version",
        )


# M3-05 exposes the immutable scope value itself rather than a second scope-ID
# wrapper.  The risk contract's scope reference therefore resolves to that
# existing immutable value without inventing another identity.
ProductQualityScopeRef = ProductQualityScope


@dataclass(frozen=True, slots=True)
class ProductQualityContext:
    assessment_ref: ProductQualityAssessmentRef
    status: FullModelStatus
    applicability: Applicability
    result_kind: ProductQualityResultKind
    scope_ref: ProductQualityScopeRef
    product_ref: ProductRef

    def __post_init__(self) -> None:
        if not isinstance(self.assessment_ref, ProductQualityAssessmentRef):
            raise TypeError("assessment_ref must be a ProductQualityAssessmentRef")
        _validate_status_applicability(self.status, self.applicability)
        if self.result_kind is not ProductQualityResultKind.OBSERVED_REFERENCE_INDICATOR:
            raise ValueError("risk context requires the observed reference indicator")
        if not isinstance(self.scope_ref, ProductQualityScope):
            raise TypeError("scope_ref must preserve the ProductQualityScope")
        if not isinstance(self.product_ref, ProductRef):
            raise TypeError("product_ref must be a ProductRef")
        if self.scope_ref.product_ref != self.product_ref:
            raise ValueError("product-quality scope and product reference must agree")
        if (
            self.scope_ref.characteristic_id
            is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY
        ):
            raise ValueError("product-quality context must target Performance Efficiency")


@dataclass(frozen=True, slots=True, order=True)
class RiskAssessmentEventRef:
    event_id: str
    event_version: str
    artifact_ref: ArtifactRef
    process_state_ref: ProcessStateRef

    def __post_init__(self) -> None:
        _identifier(self.event_id, "event_id")
        _identifier(self.event_version, "event_version")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")


@dataclass(frozen=True, slots=True)
class RiskAssessmentContext:
    assessment_event_ref: RiskAssessmentEventRef
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    full_model_contract_ref: ContractRef = FULL_MODEL_CONTRACT_REF
    defect_risk_contract_ref: ContractRef = DEFECT_QUALITY_RISK_CONTRACT_REF
    model_ref: RiskModelRef = RISK_MODEL_REF
    rule_ref: RuleRef = RISK_RULE_REF
    parameter_set_ref: RiskParameterSetRef = RISK_PARAMETER_SET_REF

    def __post_init__(self) -> None:
        if self.assessment_event_ref.artifact_ref != self.artifact_ref:
            raise ValueError("risk event must name the context artifact")
        if self.assessment_event_ref.process_state_ref != self.process_state_ref:
            raise ValueError("risk event must name the context process state")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("source assessment must name the risk artifact")
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("unsupported Full Model contract")
        if self.defect_risk_contract_ref != DEFECT_QUALITY_RISK_CONTRACT_REF:
            raise ValueError("unsupported defect-quality-risk contract")
        if self.model_ref != RISK_MODEL_REF:
            raise ValueError("unsupported risk model")
        if self.rule_ref != RISK_RULE_REF:
            raise ValueError("unsupported risk classifier rule")
        if self.parameter_set_ref != RISK_PARAMETER_SET_REF:
            raise ValueError("unsupported risk parameter set")


@dataclass(frozen=True, slots=True, order=True)
class SpecificationRiskSubject:
    artifact_ref: ArtifactRef
    participant_refs: tuple[RequirementSubjectRef, ...]
    affected_characteristic_id: ProductQualityCharacteristicId

    def __post_init__(self) -> None:
        _typed_tuple(self.participant_refs, RequirementSubjectRef, "participant_refs")
        if len(self.participant_refs) not in {0, 2}:
            raise ValueError("risk subject requires zero or two participants")
        _unique(self.participant_refs, "participant_refs")
        if (
            self.affected_characteristic_id
            is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY
        ):
            raise ValueError("risk subject supports Performance Efficiency only")


@dataclass(frozen=True, slots=True, order=True)
class BoundedRiskAssessmentInputId:
    subject: SpecificationRiskSubject
    problem_resolution_ref: ProblemClaimResolutionRef
    defect_population_ref: DefectPopulationSnapshotRef
    relation_ref: DefectQualityRelationRef
    product_quality_assessment_ref: ProductQualityAssessmentRef
    process_state_ref: ProcessStateRef


RiskInputProvenanceRef = (
    ProblemClaimResolutionRef
    | ConfirmedSupportedProblemRef
    | DefectPopulationSnapshotRef
    | DefectQualityRelationRef
    | ProductQualityAssessmentRef
    | AssessmentRef
    | ContractRef
    | RuleRef
    | RiskModelRef
    | RiskParameterSetRef
)


@dataclass(frozen=True, slots=True)
class BoundedRiskAssessmentInput:
    input_id: BoundedRiskAssessmentInputId
    subject: SpecificationRiskSubject
    problem_resolution_ref: ProblemClaimResolutionRef
    problem_ref: ConfirmedSupportedProblemRef | None
    defect_population_ref: DefectPopulationSnapshotRef
    defect_population_status: FullModelStatus
    relation_ref: DefectQualityRelationRef
    characteristic_id: ProductQualityCharacteristicId
    product_quality_context: ProductQualityContext
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    evidence_refs: tuple[CrossEvidenceRef, ...]
    provenance_refs: tuple[RiskInputProvenanceRef, ...]

    def __post_init__(self) -> None:
        expected_id = BoundedRiskAssessmentInputId(
            self.subject,
            self.problem_resolution_ref,
            self.defect_population_ref,
            self.relation_ref,
            self.product_quality_context.assessment_ref,
            self.process_state_ref,
        )
        if self.input_id != expected_id:
            raise ValueError("input_id must be the structured bounded-risk identity")
        if self.subject.artifact_ref != self.artifact_ref:
            raise ValueError("risk subject and input artifact must agree")
        if self.subject.affected_characteristic_id is not self.characteristic_id:
            raise ValueError("risk subject and input characteristic must agree")
        if self.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
            raise ValueError("M_risk supports Performance Efficiency only")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("risk input cannot mix artifacts and assessments")
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.defect_population_status, FullModelStatus):
            raise TypeError("defect_population_status must be a FullModelStatus")
        _typed_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        _typed_tuple(
            self.provenance_refs,
            (
                ProblemClaimResolutionRef,
                ConfirmedSupportedProblemRef,
                DefectPopulationSnapshotRef,
                DefectQualityRelationRef,
                ProductQualityAssessmentRef,
                AssessmentRef,
                ContractRef,
                RuleRef,
                RiskModelRef,
                RiskParameterSetRef,
            ),
            "provenance_refs",
        )
        _unique(self.evidence_refs, "evidence_refs")
        _unique(self.provenance_refs, "provenance_refs")
        if self.problem_ref is None and self.subject.participant_refs:
            raise ValueError("a subject without a problem cannot carry participants")


@dataclass(frozen=True, slots=True)
class BoundedRiskProvenance:
    problem_resolution_ref: ProblemClaimResolutionRef
    problem_ref_or_none: ConfirmedSupportedProblemRef | None
    defect_population_ref: DefectPopulationSnapshotRef
    defect_population_status: FullModelStatus
    relation_ref: DefectQualityRelationRef
    product_quality_context: ProductQualityContext
    source_cross_result_ref_or_none: CrossResultId | None
    participant_refs: tuple[RequirementSubjectRef, ...]
    ordered_evidence_refs: tuple[CrossEvidenceRef, ...]
    source_assessment_refs: tuple[AssessmentRef | ProductQualityAssessmentRef, ...]
    artifact_ref: ArtifactRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    full_model_contract_ref: ContractRef
    defect_risk_contract_ref: ContractRef
    model_ref: RiskModelRef
    rule_ref: RuleRef
    parameter_set_ref: RiskParameterSetRef

    def __post_init__(self) -> None:
        _typed_tuple(self.participant_refs, RequirementSubjectRef, "participant_refs")
        if len(self.participant_refs) not in {0, 2}:
            raise ValueError("risk provenance requires zero or two participants")
        _typed_tuple(
            self.ordered_evidence_refs,
            CrossEvidenceRef,
            "ordered_evidence_refs",
        )
        _typed_tuple(
            self.source_assessment_refs,
            (AssessmentRef, ProductQualityAssessmentRef),
            "source_assessment_refs",
        )
        _unique(self.participant_refs, "participant_refs")
        _unique(self.ordered_evidence_refs, "ordered_evidence_refs")
        _unique(self.source_assessment_refs, "source_assessment_refs")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("risk provenance requires the Full Model contract")
        if self.defect_risk_contract_ref != DEFECT_QUALITY_RISK_CONTRACT_REF:
            raise ValueError("risk provenance requires the defect-risk contract")
        if self.model_ref != RISK_MODEL_REF or self.rule_ref != RISK_RULE_REF:
            raise ValueError("risk provenance requires the approved model and rule")
        if self.parameter_set_ref != RISK_PARAMETER_SET_REF:
            raise ValueError("risk provenance requires the approved parameter set")


@dataclass(frozen=True, slots=True, order=True)
class BoundedRiskAssessmentId:
    assessment_event_ref: RiskAssessmentEventRef
    subject: SpecificationRiskSubject
    problem_resolution_ref: ProblemClaimResolutionRef
    defect_population_ref: DefectPopulationSnapshotRef
    relation_ref: DefectQualityRelationRef
    product_quality_assessment_ref: ProductQualityAssessmentRef
    model_ref: RiskModelRef
    rule_ref: RuleRef
    parameter_set_ref: RiskParameterSetRef


@dataclass(frozen=True, slots=True, order=True)
class BoundedRiskAssessmentRef:
    risk_assessment_id: BoundedRiskAssessmentId


@dataclass(frozen=True, slots=True)
class BoundedRiskAssessment:
    risk_assessment_id: BoundedRiskAssessmentId
    assessment_event_ref: RiskAssessmentEventRef
    subject: SpecificationRiskSubject
    characteristic_id: ProductQualityCharacteristicId
    status: FullModelStatus
    applicability: Applicability
    classification: RiskClassification | None
    risk_statement: str
    explanation: str
    problem_resolution_ref: ProblemClaimResolutionRef
    problem_ref: ConfirmedSupportedProblemRef | None
    defect_population_ref: DefectPopulationSnapshotRef
    defect_population_status: FullModelStatus
    relation_ref: DefectQualityRelationRef
    product_quality_context: ProductQualityContext
    evidence_refs: tuple[CrossEvidenceRef, ...]
    provenance: BoundedRiskProvenance
    model_ref: RiskModelRef
    rule_ref: RuleRef
    parameter_set_ref: RiskParameterSetRef
    calibration_status: CalibrationStatus
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    non_claims: tuple[RiskNonClaim, ...]

    def __post_init__(self) -> None:
        expected_id = BoundedRiskAssessmentId(
            self.assessment_event_ref,
            self.subject,
            self.problem_resolution_ref,
            self.defect_population_ref,
            self.relation_ref,
            self.product_quality_context.assessment_ref,
            self.model_ref,
            self.rule_ref,
            self.parameter_set_ref,
        )
        if self.risk_assessment_id != expected_id:
            raise ValueError("risk_assessment_id must be the structured risk identity")
        if self.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
            raise ValueError("M_risk supports Performance Efficiency only")
        if self.subject.affected_characteristic_id is not self.characteristic_id:
            raise ValueError("risk subject and result characteristic must agree")
        _validate_status_applicability(self.status, self.applicability)
        if self.status is FullModelStatus.AVAILABLE:
            if self.classification is not RiskClassification.RISK_IDENTIFIED:
                raise ValueError("AVAILABLE risk requires RISK_IDENTIFIED")
            if self.problem_ref is None:
                raise ValueError("RISK_IDENTIFIED requires a confirmed problem")
        elif self.classification is not None:
            raise ValueError("non-AVAILABLE risk cannot carry a classification")
        _identifier(self.risk_statement, "risk_statement")
        _identifier(self.explanation, "explanation")
        _typed_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        if self.model_ref != RISK_MODEL_REF or self.rule_ref != RISK_RULE_REF:
            raise ValueError("risk assessment requires the approved model and rule")
        if self.parameter_set_ref != RISK_PARAMETER_SET_REF:
            raise ValueError("risk assessment requires the approved parameter set")
        if self.calibration_status is not CalibrationStatus.PROVISIONAL_NOT_CALIBRATED:
            raise ValueError("risk assessment must remain provisionally uncalibrated")
        if self.non_claims != MANDATORY_RISK_NON_CLAIMS:
            raise ValueError("risk assessment must carry all non-claims in order")
        if self.assessment_event_ref.artifact_ref != self.artifact_ref:
            raise ValueError("risk event and result artifact must agree")
        if self.assessment_event_ref.process_state_ref != self.process_state_ref:
            raise ValueError("risk event and result process state must agree")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("risk result cannot mix artifacts and assessments")
        if (
            self.provenance.problem_resolution_ref != self.problem_resolution_ref
            or self.provenance.problem_ref_or_none != self.problem_ref
            or self.provenance.defect_population_ref != self.defect_population_ref
            or self.provenance.defect_population_status is not self.defect_population_status
            or self.provenance.relation_ref != self.relation_ref
            or self.provenance.product_quality_context != self.product_quality_context
            or self.provenance.participant_refs != self.subject.participant_refs
            or self.provenance.ordered_evidence_refs != self.evidence_refs
            or self.provenance.artifact_ref != self.artifact_ref
            or self.provenance.source_snapshot_id != self.source_snapshot_id
            or self.provenance.process_state_ref != self.process_state_ref
            or self.provenance.model_ref != self.model_ref
            or self.provenance.rule_ref != self.rule_ref
            or self.provenance.parameter_set_ref != self.parameter_set_ref
        ):
            raise ValueError("risk result and provenance must preserve one source graph")

    @property
    def ref(self) -> BoundedRiskAssessmentRef:
        return BoundedRiskAssessmentRef(self.risk_assessment_id)


__all__ = [
    "MANDATORY_RISK_NON_CLAIMS",
    "RISK_MODEL_ID",
    "RISK_MODEL_REF",
    "RISK_MODEL_VERSION",
    "RISK_PARAMETER_SET",
    "RISK_PARAMETER_SET_ID",
    "RISK_PARAMETER_SET_REF",
    "RISK_PARAMETER_SET_VERSION",
    "RISK_RULE_ID",
    "RISK_RULE_REF",
    "RISK_RULE_VERSION",
    "BoundedRiskAssessment",
    "BoundedRiskAssessmentId",
    "BoundedRiskAssessmentInput",
    "BoundedRiskAssessmentInputId",
    "BoundedRiskAssessmentRef",
    "BoundedRiskProvenance",
    "ProductQualityAssessmentRef",
    "ProductQualityContext",
    "ProductQualityScopeRef",
    "RiskAssessmentContext",
    "RiskAssessmentEventRef",
    "RiskClassification",
    "RiskModelRef",
    "RiskNonClaim",
    "RiskParameterSet",
    "RiskParameterSetRef",
    "SpecificationRiskSubject",
]

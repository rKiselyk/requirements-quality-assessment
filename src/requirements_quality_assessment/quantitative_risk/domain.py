"""Typed contracts for one externally parameterized local risk ``r_ij``."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from ..cross_analysis import AssessmentSnapshotId
from ..defect_quality import (
    ConfirmedSupportedProblem, ConfirmedSupportedProblemRef,
    DefectQualityRelation, DefectQualityRelationRef, RelationKind,
)
from ..dynamic_evidence import FullModelStatus
from ..metrics import (ArtifactRef, AssessmentRef, ContractRef,
                       NumericRepresentation, RuleRef, RuleVersionAuthority)
from ..performance_efficiency import ProcessStateRef, ProductQualityCharacteristicId
from ..product_quality import CalibrationStatus


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


QUANTITATIVE_RISK_CONTRACT_REF = ContractRef(
    "FULL-MODEL-V0.1-QUANTITATIVE-LOCAL-RISK", "1"
)
QUANTITATIVE_RISK_RULE_REF = RuleRef(
    "R-IJ-PE-001", "1", RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION
)
QUANTITATIVE_RISK_CALCULATION_RULE = "r_ij = rho_ij * p_ij * I_ij * kappa_j(C)"


class QuantitativeRiskOperandKind(str, Enum):
    RHO = "RHO"
    PROBABILITY = "PROBABILITY"
    IMPACT = "IMPACT"
    CONTEXT_FACTOR = "CONTEXT_FACTOR"


class QuantitativeRiskResultKind(str, Enum):
    LOCAL_RISK_R_IJ = "LOCAL_RISK_R_IJ"


class QuantitativeRiskResultState(str, Enum):
    AVAILABLE = "AVAILABLE"
    CALCULATION_WITHHELD = "CALCULATION_WITHHELD"


class QuantitativeRiskScope(str, Enum):
    EXTERNALLY_PARAMETERIZED_BOUNDED_PE_REFERENCE = (
        "EXTERNALLY_PARAMETERIZED_BOUNDED_PE_REFERENCE"
    )


class QuantitativeRiskNonClaim(str, Enum):
    NOT_CATEGORICAL_RISK_CLASSIFICATION = "NC-Q-RISK-001"
    NO_AUTOMATIC_OPERAND_ESTIMATION = "NC-Q-RISK-002"
    NOT_AGGREGATE_RISK_J = "NC-Q-RISK-003"
    NO_PRIORITY_RANK_OR_THRESHOLD = "NC-Q-RISK-004"
    NO_CAUSAL_CLAIM = "NC-Q-RISK-005"
    PROVISIONAL_NOT_EMPIRICALLY_CALIBRATED = "NC-Q-RISK-006"


MANDATORY_QUANTITATIVE_RISK_NON_CLAIMS = tuple(QuantitativeRiskNonClaim)


@dataclass(frozen=True, slots=True, order=True)
class QuantitativeRiskOperandId:
    kind: QuantitativeRiskOperandKind
    operand_id: str
    operand_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, QuantitativeRiskOperandKind):
            raise TypeError("kind must be a QuantitativeRiskOperandKind")
        _identifier(self.operand_id, "operand_id")
        _identifier(self.operand_version, "operand_version")


@dataclass(frozen=True, slots=True, order=True)
class QuantitativeRiskOperandSourceRef:
    source_id: str
    source_version: str
    provider_id: str
    provider_version: str

    def __post_init__(self) -> None:
        _identifier(self.source_id, "source_id")
        _identifier(self.source_version, "source_version")
        _identifier(self.provider_id, "provider_id")
        _identifier(self.provider_version, "provider_version")


@dataclass(frozen=True, slots=True, order=True)
class QuantitativeRiskContextRef:
    context_id: str
    context_version: str

    def __post_init__(self) -> None:
        _identifier(self.context_id, "context_id")
        _identifier(self.context_version, "context_version")


@dataclass(frozen=True, slots=True)
class QuantitativeRiskOperandProvenance:
    source_ref: QuantitativeRiskOperandSourceRef
    source_or_rationale: str
    calibration_status: CalibrationStatus
    governing_contract_ref: ContractRef
    artifact_ref: ArtifactRef
    problem_ref: ConfirmedSupportedProblemRef
    relation_ref: DefectQualityRelationRef
    characteristic_id: ProductQualityCharacteristicId
    process_state_ref: ProcessStateRef
    context_ref: QuantitativeRiskContextRef | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_ref, QuantitativeRiskOperandSourceRef):
            raise TypeError("source_ref must be versioned operand-source provenance")
        _identifier(self.source_or_rationale, "source_or_rationale")
        if self.calibration_status not in {
            CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
            CalibrationStatus.EXPERIMENTAL_CALIBRATION_REQUIRED,
        }:
            raise ValueError("TC-03 operands cannot claim experimental calibration")
        if self.governing_contract_ref != QUANTITATIVE_RISK_CONTRACT_REF:
            raise ValueError("operand requires the quantitative-risk contract")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if not isinstance(self.problem_ref, ConfirmedSupportedProblemRef):
            raise TypeError("problem_ref must be a ConfirmedSupportedProblemRef")
        if not isinstance(self.relation_ref, DefectQualityRelationRef):
            raise TypeError("relation_ref must be a DefectQualityRelationRef")
        if self.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
            raise ValueError("quantitative local risk supports Performance Efficiency only")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        if self.problem_ref.problem_id.artifact_ref != self.artifact_ref:
            raise ValueError("operand provenance cannot cross artifacts")
        relation_id = self.relation_ref.relation_id
        if relation_id.problem_ref != self.problem_ref:
            raise ValueError("operand provenance cannot cross problems or relations")
        if relation_id.characteristic_id is not self.characteristic_id:
            raise ValueError("operand provenance cannot cross characteristics")


@dataclass(frozen=True, slots=True)
class QuantitativeRiskOperand:
    operand_id: QuantitativeRiskOperandId
    kind: QuantitativeRiskOperandKind
    state: FullModelStatus
    value: Fraction | None
    provenance: QuantitativeRiskOperandProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.operand_id, QuantitativeRiskOperandId):
            raise TypeError("operand_id must be a QuantitativeRiskOperandId")
        if self.operand_id.kind is not self.kind:
            raise ValueError("operand identity and kind must agree")
        if not isinstance(self.state, FullModelStatus):
            raise TypeError("state must be a FullModelStatus")
        if not isinstance(self.provenance, QuantitativeRiskOperandProvenance):
            raise TypeError("provenance must be QuantitativeRiskOperandProvenance")
        if self.state is FullModelStatus.AVAILABLE:
            if type(self.value) is not Fraction:
                raise TypeError("an AVAILABLE operand requires an exact Fraction value")
        elif self.value is not None:
            raise ValueError("a non-AVAILABLE operand requires value=None")
        if self.kind is QuantitativeRiskOperandKind.RHO and self.value is not None:
            if not Fraction(0, 1) <= self.value <= Fraction(1, 1):
                raise ValueError("rho_ij must be within [0,1]")
        if self.kind is QuantitativeRiskOperandKind.CONTEXT_FACTOR:
            if self.provenance.context_ref is None:
                raise ValueError("context-factor provenance requires a context reference")
        elif self.provenance.context_ref is not None:
            raise ValueError("only context-factor provenance may carry a context reference")

    @property
    def ref(self) -> QuantitativeRiskOperandId:
        return self.operand_id


@dataclass(frozen=True, slots=True)
class QuantitativeRiskCalculationContext:
    calculation_id: str
    calculation_version: str
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    governing_contract_ref: ContractRef = QUANTITATIVE_RISK_CONTRACT_REF
    calculation_rule_ref: RuleRef = QUANTITATIVE_RISK_RULE_REF

    def __post_init__(self) -> None:
        _identifier(self.calculation_id, "calculation_id")
        _identifier(self.calculation_version, "calculation_version")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("calculation context cannot cross artifacts")
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        if self.governing_contract_ref != QUANTITATIVE_RISK_CONTRACT_REF:
            raise ValueError("unsupported quantitative-risk contract")
        if self.calculation_rule_ref != QUANTITATIVE_RISK_RULE_REF:
            raise ValueError("unsupported quantitative-risk rule")


@dataclass(frozen=True, slots=True)
class QuantitativeRiskCalculationRequest:
    confirmed_problem: ConfirmedSupportedProblem
    relation: DefectQualityRelation
    context: QuantitativeRiskCalculationContext
    rho: QuantitativeRiskOperand
    probability: QuantitativeRiskOperand
    impact: QuantitativeRiskOperand
    context_factor: QuantitativeRiskOperand

    def __post_init__(self) -> None:
        if not isinstance(self.confirmed_problem, ConfirmedSupportedProblem):
            raise TypeError("confirmed_problem must be a ConfirmedSupportedProblem")
        if not isinstance(self.relation, DefectQualityRelation):
            raise TypeError("relation must be a DefectQualityRelation")
        if not isinstance(self.context, QuantitativeRiskCalculationContext):
            raise TypeError("context must be a QuantitativeRiskCalculationContext")
        expected = (
            (self.rho, QuantitativeRiskOperandKind.RHO, "rho"),
            (self.probability, QuantitativeRiskOperandKind.PROBABILITY, "probability"),
            (self.impact, QuantitativeRiskOperandKind.IMPACT, "impact"),
            (self.context_factor, QuantitativeRiskOperandKind.CONTEXT_FACTOR, "context_factor"),
        )
        for operand, kind, slot in expected:
            if not isinstance(operand, QuantitativeRiskOperand):
                raise TypeError(f"{slot} must be a QuantitativeRiskOperand")
            if operand.kind is not kind:
                raise ValueError(f"{slot} requires operand kind {kind.value}")
        textual_identities = {
            (operand.operand_id.operand_id, operand.operand_id.operand_version)
            for operand in self.operands
        }
        if len(textual_identities) != 4:
            raise ValueError("the four operand identities must be unique")
        problem_ref = self.confirmed_problem.ref
        relation_ref = self.relation.ref
        if self.relation.problem_ref != problem_ref:
            raise ValueError("relation must reference the exact confirmed problem")
        if (self.relation.status is not FullModelStatus.AVAILABLE
                or self.relation.relation_kind is not RelationKind.BOUNDED_RISK_RELEVANCE):
            raise ValueError("quantitative calculation requires an AVAILABLE relation")
        if self.confirmed_problem.artifact_ref != self.context.artifact_ref:
            raise ValueError("calculation cannot cross artifacts")
        if self.confirmed_problem.source_assessment_ref != self.context.source_assessment_ref:
            raise ValueError("calculation cannot cross source assessments")
        if self.confirmed_problem.source_snapshot_id != self.context.source_snapshot_id:
            raise ValueError("calculation cannot cross source snapshots")
        if self.confirmed_problem.process_state_ref != self.context.process_state_ref:
            raise ValueError("calculation cannot cross process states")
        if self.relation.artifact_ref != self.context.artifact_ref:
            raise ValueError("relation and calculation cannot cross artifacts")
        if self.relation.process_state_ref != self.context.process_state_ref:
            raise ValueError("relation and calculation cannot cross process states")
        for operand in self.operands:
            provenance = operand.provenance
            if provenance.problem_ref != problem_ref:
                raise ValueError("operand bundle cannot cross problems")
            if provenance.relation_ref != relation_ref:
                raise ValueError("operand bundle cannot cross relations")
            if provenance.artifact_ref != self.context.artifact_ref:
                raise ValueError("operand bundle cannot cross artifacts")
            if provenance.process_state_ref != self.context.process_state_ref:
                raise ValueError("operand bundle cannot cross process states")
            if provenance.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
                raise ValueError("operand bundle cannot cross characteristics")

    @property
    def operands(self) -> tuple[QuantitativeRiskOperand, ...]:
        return (self.rho, self.probability, self.impact, self.context_factor)


@dataclass(frozen=True, slots=True, order=True)
class QuantitativeLocalRiskAssessmentId:
    calculation_id: str
    calculation_version: str
    problem_ref: ConfirmedSupportedProblemRef
    relation_ref: DefectQualityRelationRef
    operand_refs: tuple[QuantitativeRiskOperandId, ...]
    rule_ref: RuleRef

    def __post_init__(self) -> None:
        _identifier(self.calculation_id, "calculation_id")
        _identifier(self.calculation_version, "calculation_version")
        if not isinstance(self.problem_ref, ConfirmedSupportedProblemRef):
            raise TypeError("problem_ref must be a ConfirmedSupportedProblemRef")
        if not isinstance(self.relation_ref, DefectQualityRelationRef):
            raise TypeError("relation_ref must be a DefectQualityRelationRef")
        if (
            not isinstance(self.operand_refs, tuple)
            or len(self.operand_refs) != 4
            or any(not isinstance(item, QuantitativeRiskOperandId) for item in self.operand_refs)
        ):
            raise TypeError("operand_refs must contain exactly four typed references")
        if tuple(item.kind for item in self.operand_refs) != tuple(QuantitativeRiskOperandKind):
            raise ValueError("operand_refs must use the four kinds in contract order")
        if self.rule_ref != QUANTITATIVE_RISK_RULE_REF:
            raise ValueError("assessment identity requires the quantitative-risk rule")


@dataclass(frozen=True, slots=True)
class QuantitativeRiskCalculationProvenance:
    problem_ref: ConfirmedSupportedProblemRef
    relation_ref: DefectQualityRelationRef
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    characteristic_id: ProductQualityCharacteristicId
    operands: tuple[QuantitativeRiskOperand, ...]
    governing_contract_ref: ContractRef
    calculation_rule_ref: RuleRef
    calculation_rule: str

    def __post_init__(self) -> None:
        if len(self.operands) != 4:
            raise ValueError("calculation provenance requires exactly four operands")
        if tuple(item.kind for item in self.operands) != tuple(QuantitativeRiskOperandKind):
            raise ValueError("calculation provenance requires operands in contract order")
        if self.governing_contract_ref != QUANTITATIVE_RISK_CONTRACT_REF:
            raise ValueError("calculation provenance requires the governing contract")
        if self.calculation_rule_ref != QUANTITATIVE_RISK_RULE_REF:
            raise ValueError("calculation provenance requires the governing rule")
        if self.calculation_rule != QUANTITATIVE_RISK_CALCULATION_RULE:
            raise ValueError("calculation provenance requires the exact local-risk rule")


@dataclass(frozen=True, slots=True)
class QuantitativeLocalRiskAssessment:
    assessment_id: QuantitativeLocalRiskAssessmentId
    result_kind: QuantitativeRiskResultKind
    state: QuantitativeRiskResultState
    scope: QuantitativeRiskScope
    problem_ref: ConfirmedSupportedProblemRef
    relation_ref: DefectQualityRelationRef
    characteristic_id: ProductQualityCharacteristicId
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    process_state_ref: ProcessStateRef
    operands: tuple[QuantitativeRiskOperand, ...]
    numeric_representation: NumericRepresentation
    local_risk: Fraction | None
    calibration_statuses: tuple[CalibrationStatus, ...]
    governing_contract_ref: ContractRef
    calculation_rule_ref: RuleRef
    calculation_rule: str
    provenance: QuantitativeRiskCalculationProvenance
    explanation: str
    non_claims: tuple[QuantitativeRiskNonClaim, ...]

    def __post_init__(self) -> None:
        expected_id = QuantitativeLocalRiskAssessmentId(
            self.assessment_id.calculation_id,
            self.assessment_id.calculation_version,
            self.problem_ref,
            self.relation_ref,
            tuple(item.ref for item in self.operands),
            self.calculation_rule_ref,
        )
        if self.assessment_id != expected_id:
            raise ValueError("assessment_id must preserve the exact calculation graph")
        if self.result_kind is not QuantitativeRiskResultKind.LOCAL_RISK_R_IJ:
            raise ValueError("unsupported quantitative-risk result kind")
        if self.scope is not QuantitativeRiskScope.EXTERNALLY_PARAMETERIZED_BOUNDED_PE_REFERENCE:
            raise ValueError("unsupported quantitative-risk scope")
        if tuple(item.kind for item in self.operands) != tuple(QuantitativeRiskOperandKind):
            raise ValueError("result requires the four operands in contract order")
        expected = tuple(item.provenance.calibration_status for item in self.operands)
        if self.calibration_statuses != expected:
            raise ValueError("result must preserve every operand calibration status")
        if self.state is QuantitativeRiskResultState.AVAILABLE:
            if type(self.local_risk) is not Fraction:
                raise TypeError("AVAILABLE local risk requires an exact Fraction")
            if self.numeric_representation is not NumericRepresentation.EXACT_FRACTION:
                raise ValueError("AVAILABLE local risk requires EXACT_FRACTION")
            if not Fraction(0, 1) <= self.local_risk <= Fraction(1, 1):
                raise ValueError("r_ij must be within [0,1]")
            if any(item.state is not FullModelStatus.AVAILABLE for item in self.operands):
                raise ValueError("AVAILABLE local risk requires four AVAILABLE operands")
        else:
            if self.local_risk is not None:
                raise ValueError("withheld local risk cannot carry a numeric value")
            if self.numeric_representation is not NumericRepresentation.NONE:
                raise ValueError("withheld local risk requires numeric representation NONE")
            if all(item.state is FullModelStatus.AVAILABLE for item in self.operands):
                raise ValueError("a complete operand bundle cannot be withheld")
        if self.non_claims != MANDATORY_QUANTITATIVE_RISK_NON_CLAIMS:
            raise ValueError("result must preserve all quantitative-risk non-claims")
        if (
            self.provenance.problem_ref != self.problem_ref
            or self.provenance.relation_ref != self.relation_ref
            or self.provenance.artifact_ref != self.artifact_ref
            or self.provenance.source_assessment_ref != self.source_assessment_ref
            or self.provenance.source_snapshot_id != self.source_snapshot_id
            or self.provenance.process_state_ref != self.process_state_ref
            or self.provenance.characteristic_id is not self.characteristic_id
            or self.provenance.operands != self.operands
            or self.provenance.governing_contract_ref != self.governing_contract_ref
            or self.provenance.calculation_rule_ref != self.calculation_rule_ref
            or self.provenance.calculation_rule != self.calculation_rule
        ):
            raise ValueError("result and provenance must preserve the same source graph")
        if self.governing_contract_ref != QUANTITATIVE_RISK_CONTRACT_REF:
            raise ValueError("result requires the quantitative-risk contract")
        if self.calculation_rule_ref != QUANTITATIVE_RISK_RULE_REF:
            raise ValueError("result requires the quantitative-risk rule")
        if self.calculation_rule != QUANTITATIVE_RISK_CALCULATION_RULE:
            raise ValueError("result requires the exact local-risk calculation rule")
        _identifier(self.explanation, "explanation")

    @property
    def ref(self) -> QuantitativeLocalRiskAssessmentId:
        return self.assessment_id


__all__ = [name for name in globals() if name.startswith("Quantitative") or name.startswith("MANDATORY_") or name.startswith("QUANTITATIVE_")]

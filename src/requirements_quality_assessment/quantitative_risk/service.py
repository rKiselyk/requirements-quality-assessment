"""Pure validation and exact multiplication for one local ``r_ij``."""

from fractions import Fraction

from ..dynamic_evidence import FullModelStatus
from ..metrics import NumericRepresentation
from ..performance_efficiency import ProductQualityCharacteristicId
from .domain import (
    MANDATORY_QUANTITATIVE_RISK_NON_CLAIMS, QUANTITATIVE_RISK_CALCULATION_RULE,
    QuantitativeLocalRiskAssessment, QuantitativeLocalRiskAssessmentId,
    QuantitativeRiskCalculationProvenance, QuantitativeRiskCalculationRequest,
    QuantitativeRiskResultKind, QuantitativeRiskResultState, QuantitativeRiskScope,
)


class QuantitativeLocalRiskCalculator:
    """Calculate only when all four explicit operands are AVAILABLE."""

    def calculate(self, request: QuantitativeRiskCalculationRequest) -> QuantitativeLocalRiskAssessment:
        if not isinstance(request, QuantitativeRiskCalculationRequest):
            raise TypeError("request must be a QuantitativeRiskCalculationRequest")
        operands = request.operands
        all_available = all(item.state is FullModelStatus.AVAILABLE for item in operands)
        local_risk = None
        if all_available:
            local_risk = Fraction(1, 1)
            for operand in operands:
                local_risk *= operand.value
            if not Fraction(0, 1) <= local_risk <= Fraction(1, 1):
                raise ValueError("computed r_ij is outside [0,1]; it is not clamped")
        problem_ref, relation_ref, context = (
            request.confirmed_problem.ref, request.relation.ref, request.context
        )
        provenance = QuantitativeRiskCalculationProvenance(
            problem_ref, relation_ref, context.artifact_ref, context.source_assessment_ref,
            context.source_snapshot_id, context.process_state_ref,
            ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY, operands,
            context.governing_contract_ref, context.calculation_rule_ref,
            QUANTITATIVE_RISK_CALCULATION_RULE,
        )
        state = (QuantitativeRiskResultState.AVAILABLE if all_available
                 else QuantitativeRiskResultState.CALCULATION_WITHHELD)
        return QuantitativeLocalRiskAssessment(
            QuantitativeLocalRiskAssessmentId(
                context.calculation_id, context.calculation_version, problem_ref,
                relation_ref, tuple(item.ref for item in operands), context.calculation_rule_ref,
            ),
            QuantitativeRiskResultKind.LOCAL_RISK_R_IJ, state,
            QuantitativeRiskScope.EXTERNALLY_PARAMETERIZED_BOUNDED_PE_REFERENCE,
            problem_ref, relation_ref, ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
            context.artifact_ref, context.source_assessment_ref, context.source_snapshot_id,
            context.process_state_ref, operands,
            NumericRepresentation.EXACT_FRACTION if all_available else NumericRepresentation.NONE,
            local_risk, tuple(item.provenance.calibration_status for item in operands),
            context.governing_contract_ref, context.calculation_rule_ref,
            QUANTITATIVE_RISK_CALCULATION_RULE, provenance,
            ("Exact local r_ij was calculated from four explicitly supplied, versioned "
             "operands; no operand was inferred." if all_available else
             "Local r_ij was withheld because at least one explicit operand is not "
             "AVAILABLE; every operand state and provenance is preserved."),
            MANDATORY_QUANTITATIVE_RISK_NON_CLAIMS,
        )


def calculate_quantitative_local_risk(request: QuantitativeRiskCalculationRequest) -> QuantitativeLocalRiskAssessment:
    return QuantitativeLocalRiskCalculator().calculate(request)


__all__ = ["QuantitativeLocalRiskCalculator", "calculate_quantitative_local_risk"]

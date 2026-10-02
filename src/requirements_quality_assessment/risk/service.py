"""Pure construction and classification services for bounded ``M_risk``."""

from __future__ import annotations

from ..defect_quality import (
    PROBLEM_RULE_REF,
    RELATION_RULE_REF,
    DefectPopulationSnapshot,
    DefectQualityRelation,
    ProblemClaimResolution,
    ProblemDisposition,
    RelationKind,
)
from ..dynamic_evidence import Applicability, FullModelStatus
from ..performance_efficiency import ProductQualityCharacteristicId
from ..product_quality import CalibrationStatus, ProductQualityAssessment
from .domain import (
    MANDATORY_RISK_NON_CLAIMS,
    RISK_MODEL_REF,
    RISK_PARAMETER_SET_REF,
    RISK_RULE_REF,
    BoundedRiskAssessment,
    BoundedRiskAssessmentId,
    BoundedRiskAssessmentInput,
    BoundedRiskAssessmentInputId,
    BoundedRiskProvenance,
    ProductQualityAssessmentRef,
    ProductQualityContext,
    RiskAssessmentContext,
    RiskClassification,
    SpecificationRiskSubject,
)


def _product_quality_context(
    assessment: ProductQualityAssessment,
) -> ProductQualityContext:
    return ProductQualityContext(
        ProductQualityAssessmentRef(
            assessment.assessment_id,
            assessment.product_quality_assessment_version,
        ),
        assessment.status,
        assessment.applicability,
        assessment.result_kind,
        assessment.scope,
        assessment.product_ref,
    )


def _validate_source_graph(
    problem_resolution: ProblemClaimResolution,
    defect_population: DefectPopulationSnapshot,
    relation: DefectQualityRelation,
    product_quality_assessment: ProductQualityAssessment,
    context: RiskAssessmentContext,
) -> None:
    if not isinstance(problem_resolution, ProblemClaimResolution):
        raise TypeError("problem_resolution must be a ProblemClaimResolution")
    if not isinstance(defect_population, DefectPopulationSnapshot):
        raise TypeError("defect_population must be a DefectPopulationSnapshot")
    if not isinstance(relation, DefectQualityRelation):
        raise TypeError("relation must be a DefectQualityRelation")
    if not isinstance(product_quality_assessment, ProductQualityAssessment):
        raise TypeError("product_quality_assessment must be a ProductQualityAssessment")
    if not isinstance(context, RiskAssessmentContext):
        raise TypeError("context must be a RiskAssessmentContext")

    records = (problem_resolution, defect_population, relation)
    if any(item.artifact_ref != context.artifact_ref for item in records):
        raise ValueError("risk inputs cannot mix artifact identities or versions")
    if any(
        item.source_assessment_ref != context.source_assessment_ref
        for item in records
    ):
        raise ValueError("risk inputs cannot mix source assessments or versions")
    if any(item.source_snapshot_id != context.source_snapshot_id for item in records):
        raise ValueError("risk inputs cannot mix source snapshots")
    if relation.process_state_ref != context.process_state_ref:
        raise ValueError("risk relation cannot cross process-state versions")
    if (
        problem_resolution.problem is not None
        and problem_resolution.problem.process_state_ref != context.process_state_ref
    ):
        raise ValueError("risk problem cannot cross process-state versions")

    if defect_population.rule_ref != PROBLEM_RULE_REF:
        raise ValueError("risk population requires D-QB-CONFLICT-001 / 1")
    if relation.rule_ref != RELATION_RULE_REF:
        raise ValueError("risk relation requires R_DQ-PE-QB-001 / 1")
    if relation.problem_resolution_ref != problem_resolution.ref:
        raise ValueError("relation must resolve the supplied problem resolution")
    expected_problem_ref = (
        None if problem_resolution.problem is None else problem_resolution.problem.ref
    )
    if relation.problem_ref != expected_problem_ref:
        raise ValueError("relation and problem resolution must name the same problem")
    if problem_resolution.ref not in defect_population.problem_resolution_refs:
        raise ValueError("defect population must contain the problem resolution")
    if expected_problem_ref is not None and expected_problem_ref not in defect_population.members:
        raise ValueError("defect population must contain the confirmed problem")
    if relation.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
        raise ValueError("risk relation must target Performance Efficiency")

    if product_quality_assessment.artifact_ref != context.artifact_ref:
        raise ValueError("product-quality context cannot cross artifact versions")
    if (
        product_quality_assessment.feature_profile_ref.source_assessment_ref
        != context.source_assessment_ref
    ):
        raise ValueError("product-quality context cannot cross source assessments")
    if (
        product_quality_assessment.provenance.process_state_ref
        != context.process_state_ref
    ):
        raise ValueError("product-quality context cannot cross process-state versions")
    if (
        product_quality_assessment.characteristic_id
        is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY
    ):
        raise ValueError("product-quality context must target Performance Efficiency")


def build_risk_assessment_input(
    problem_resolution: ProblemClaimResolution,
    defect_population: DefectPopulationSnapshot,
    relation: DefectQualityRelation,
    product_quality_assessment: ProductQualityAssessment,
    context: RiskAssessmentContext,
) -> BoundedRiskAssessmentInput:
    """Build the exact typed M3-07 input without reconstructing upstream facts."""

    _validate_source_graph(
        problem_resolution,
        defect_population,
        relation,
        product_quality_assessment,
        context,
    )
    problem = problem_resolution.problem
    problem_ref = None if problem is None else problem.ref
    participants = () if problem is None else problem.participant_refs
    evidence_refs = () if problem is None else problem.evidence_refs
    product_context = _product_quality_context(product_quality_assessment)
    subject = SpecificationRiskSubject(
        context.artifact_ref,
        participants,
        ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
    )
    input_id = BoundedRiskAssessmentInputId(
        subject,
        problem_resolution.ref,
        defect_population.ref,
        relation.ref,
        product_context.assessment_ref,
        context.process_state_ref,
    )
    provenance_refs = (
        problem_resolution.ref,
        *((problem_ref,) if problem_ref is not None else ()),
        defect_population.ref,
        relation.ref,
        product_context.assessment_ref,
        context.source_assessment_ref,
        context.full_model_contract_ref,
        context.defect_risk_contract_ref,
        PROBLEM_RULE_REF,
        RELATION_RULE_REF,
        context.model_ref,
        context.rule_ref,
        context.parameter_set_ref,
    )
    return BoundedRiskAssessmentInput(
        input_id=input_id,
        subject=subject,
        problem_resolution_ref=problem_resolution.ref,
        problem_ref=problem_ref,
        defect_population_ref=defect_population.ref,
        defect_population_status=defect_population.status,
        relation_ref=relation.ref,
        characteristic_id=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
        product_quality_context=product_context,
        artifact_ref=context.artifact_ref,
        source_assessment_ref=context.source_assessment_ref,
        source_snapshot_id=context.source_snapshot_id,
        process_state_ref=context.process_state_ref,
        evidence_refs=evidence_refs,
        provenance_refs=provenance_refs,
    )


def _validate_input_resolution(
    risk_input: BoundedRiskAssessmentInput,
    problem_resolution: ProblemClaimResolution,
    defect_population: DefectPopulationSnapshot,
    relation: DefectQualityRelation,
    product_quality_assessment: ProductQualityAssessment,
    context: RiskAssessmentContext,
) -> None:
    _validate_source_graph(
        problem_resolution,
        defect_population,
        relation,
        product_quality_assessment,
        context,
    )
    expected = build_risk_assessment_input(
        problem_resolution,
        defect_population,
        relation,
        product_quality_assessment,
        context,
    )
    if risk_input != expected:
        raise ValueError("bounded risk input does not resolve to the supplied records")


def _classification_state(
    resolution: ProblemClaimResolution,
    relation: DefectQualityRelation,
) -> tuple[FullModelStatus, Applicability, RiskClassification | None]:
    if (
        resolution.status is FullModelStatus.NOT_APPLICABLE
        or resolution.disposition
        is ProblemDisposition.NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE
    ):
        return FullModelStatus.NOT_APPLICABLE, Applicability.NOT_APPLICABLE, None
    if resolution.status is not FullModelStatus.AVAILABLE:
        return resolution.status, resolution.applicability, None
    if resolution.disposition is not ProblemDisposition.CONFIRMED_SUPPORTED_PROBLEM:
        raise ValueError("AVAILABLE positive risk input requires a known disposition")
    if resolution.problem is None:
        raise ValueError("positive problem disposition requires a problem record")
    if relation.status is not FullModelStatus.AVAILABLE:
        return relation.status, relation.applicability, None
    if relation.applicability is not Applicability.APPLICABLE:
        raise ValueError("AVAILABLE relation must be APPLICABLE")
    if relation.relation_kind is not RelationKind.BOUNDED_RISK_RELEVANCE:
        raise ValueError("AVAILABLE relation must be BOUNDED_RISK_RELEVANCE")
    return (
        FullModelStatus.AVAILABLE,
        Applicability.APPLICABLE,
        RiskClassification.RISK_IDENTIFIED,
    )


def _risk_statement(classification: RiskClassification | None) -> str:
    if classification is RiskClassification.RISK_IDENTIFIED:
        return (
            "An approved confirmed specification problem and its bounded "
            "relation identify a Performance Efficiency realization/verification "
            "risk scenario."
        )
    return (
        "No bounded risk classification is available under "
        "RISK-PE-QB-001 / 1 for this typed input state."
    )


def _explanation(
    risk_input: BoundedRiskAssessmentInput,
    status: FullModelStatus,
    classification: RiskClassification | None,
    population_complete: bool,
) -> str:
    population_text = (
        "The bounded defect population is complete."
        if population_complete
        else (
            "The bounded defect population is incomplete; this individual "
            "classification does not claim that all defects or risks were found."
        )
    )
    quality = risk_input.product_quality_context
    if classification is RiskClassification.RISK_IDENTIFIED:
        return (
            f"Problem {risk_input.problem_ref!r} and relation "
            f"{risk_input.relation_ref!r} satisfy RISK-PE-QB-001 / 1. "
            f"Product-quality assessment {quality.assessment_ref!r} is preserved "
            f"as independent context with status {quality.status.value} and does "
            "not create, clear, or scale the result. Parameter set "
            "RISK-PE-QB-001-PARAMETERS / 1 has no entries and calibration is "
            f"PROVISIONAL_NOT_CALIBRATED. No risk magnitude was computed. {population_text}"
        )
    return (
        f"RISK-PE-QB-001 / 1 preserves controlling status {status.value}; "
        f"product-quality context status {quality.status.value} is not a decision "
        f"operand. No classification or numeric zero is inferred. {population_text}"
    )


class RiskAssessor:
    """Classify a validated typed M3-06 path under the sole M3-07 rule."""

    def assess(
        self,
        risk_input: BoundedRiskAssessmentInput,
        problem_resolution: ProblemClaimResolution,
        defect_population: DefectPopulationSnapshot,
        relation: DefectQualityRelation,
        product_quality_assessment: ProductQualityAssessment,
        context: RiskAssessmentContext,
    ) -> BoundedRiskAssessment:
        if not isinstance(risk_input, BoundedRiskAssessmentInput):
            raise TypeError("risk_input must be a BoundedRiskAssessmentInput")
        _validate_input_resolution(
            risk_input,
            problem_resolution,
            defect_population,
            relation,
            product_quality_assessment,
            context,
        )
        status, applicability, classification = _classification_state(
            problem_resolution,
            relation,
        )
        problem = problem_resolution.problem
        source_cross_result_ref = (
            None if problem is None else problem.source_cross_result_ref
        )
        provenance = BoundedRiskProvenance(
            problem_resolution_ref=risk_input.problem_resolution_ref,
            problem_ref_or_none=risk_input.problem_ref,
            defect_population_ref=risk_input.defect_population_ref,
            defect_population_status=risk_input.defect_population_status,
            relation_ref=risk_input.relation_ref,
            product_quality_context=risk_input.product_quality_context,
            source_cross_result_ref_or_none=source_cross_result_ref,
            participant_refs=risk_input.subject.participant_refs,
            ordered_evidence_refs=risk_input.evidence_refs,
            source_assessment_refs=(
                risk_input.source_assessment_ref,
                risk_input.product_quality_context.assessment_ref,
            ),
            artifact_ref=risk_input.artifact_ref,
            source_snapshot_id=risk_input.source_snapshot_id,
            process_state_ref=risk_input.process_state_ref,
            full_model_contract_ref=context.full_model_contract_ref,
            defect_risk_contract_ref=context.defect_risk_contract_ref,
            model_ref=context.model_ref,
            rule_ref=context.rule_ref,
            parameter_set_ref=context.parameter_set_ref,
        )
        risk_id = BoundedRiskAssessmentId(
            context.assessment_event_ref,
            risk_input.subject,
            risk_input.problem_resolution_ref,
            risk_input.defect_population_ref,
            risk_input.relation_ref,
            risk_input.product_quality_context.assessment_ref,
            context.model_ref,
            context.rule_ref,
            context.parameter_set_ref,
        )
        return BoundedRiskAssessment(
            risk_assessment_id=risk_id,
            assessment_event_ref=context.assessment_event_ref,
            subject=risk_input.subject,
            characteristic_id=risk_input.characteristic_id,
            status=status,
            applicability=applicability,
            classification=classification,
            risk_statement=_risk_statement(classification),
            explanation=_explanation(
                risk_input,
                status,
                classification,
                defect_population.population_complete,
            ),
            problem_resolution_ref=risk_input.problem_resolution_ref,
            problem_ref=risk_input.problem_ref,
            defect_population_ref=risk_input.defect_population_ref,
            defect_population_status=risk_input.defect_population_status,
            relation_ref=risk_input.relation_ref,
            product_quality_context=risk_input.product_quality_context,
            evidence_refs=risk_input.evidence_refs,
            provenance=provenance,
            model_ref=RISK_MODEL_REF,
            rule_ref=RISK_RULE_REF,
            parameter_set_ref=RISK_PARAMETER_SET_REF,
            calibration_status=CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
            artifact_ref=risk_input.artifact_ref,
            source_assessment_ref=risk_input.source_assessment_ref,
            source_snapshot_id=risk_input.source_snapshot_id,
            process_state_ref=risk_input.process_state_ref,
            non_claims=MANDATORY_RISK_NON_CLAIMS,
        )


def assess_risk(
    problem_resolution: ProblemClaimResolution,
    defect_population: DefectPopulationSnapshot,
    relation: DefectQualityRelation,
    product_quality_assessment: ProductQualityAssessment,
    context: RiskAssessmentContext,
) -> BoundedRiskAssessment:
    """Convenience entry point that builds and consumes the exact risk input."""

    risk_input = build_risk_assessment_input(
        problem_resolution,
        defect_population,
        relation,
        product_quality_assessment,
        context,
    )
    return RiskAssessor().assess(
        risk_input,
        problem_resolution,
        defect_population,
        relation,
        product_quality_assessment,
        context,
    )


__all__ = ["RiskAssessor", "assess_risk", "build_risk_assessment_input"]

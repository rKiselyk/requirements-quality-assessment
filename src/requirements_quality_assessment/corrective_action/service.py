"""Pure proposal service for the bounded ``M_risk -> A_corr`` transition."""

from __future__ import annotations

from ..defect_quality import (
    PROBLEM_RULE_REF,
    RELATION_RULE_REF,
    ConfirmedSupportedProblem,
    DefectQualityRelation,
    RelationKind,
)
from ..dynamic_evidence import Applicability, FullModelStatus
from ..risk import (
    RISK_MODEL_REF,
    RISK_PARAMETER_SET_REF,
    RISK_RULE_REF,
    BoundedRiskAssessment,
    RiskClassification,
)
from .domain import (
    ACTION_RULE_REF,
    ActionTargetRequirement,
    CorrectiveAction,
    CorrectiveActionContext,
    CorrectiveActionExpectedOutcome,
    CorrectiveActionId,
    CorrectiveActionKind,
    CorrectiveActionNonOptimalityClaim,
    CorrectiveActionProvenance,
    CorrectiveActionRationale,
    CorrectiveActionReason,
    CorrectiveActionResolution,
    CorrectiveActionResolutionId,
    CorrectiveActionResolutionProvenance,
    CorrectiveActionStatus,
    ProposedChangeKind,
)


def _requested_kind(context: CorrectiveActionContext) -> str:
    value = context.requested_action_kind
    return value.value if isinstance(value, CorrectiveActionKind) else value


def _validate_source_refs(
    risk: BoundedRiskAssessment,
    problem: ConfirmedSupportedProblem | None,
    relation: DefectQualityRelation | None,
    context: CorrectiveActionContext,
) -> None:
    if not isinstance(risk, BoundedRiskAssessment):
        raise TypeError("risk must be a BoundedRiskAssessment")
    if problem is not None and not isinstance(problem, ConfirmedSupportedProblem):
        raise TypeError("problem must be a ConfirmedSupportedProblem or None")
    if relation is not None and not isinstance(relation, DefectQualityRelation):
        raise TypeError("relation must be a DefectQualityRelation or None")
    if not isinstance(context, CorrectiveActionContext):
        raise TypeError("context must be a CorrectiveActionContext")

    if risk.model_ref != RISK_MODEL_REF or risk.rule_ref != RISK_RULE_REF:
        raise ValueError("corrective action requires the approved M3-07 risk model and rule")
    if risk.parameter_set_ref != RISK_PARAMETER_SET_REF:
        raise ValueError("corrective action requires the approved risk parameter set")
    if risk.artifact_ref != context.target_artifact_ref:
        raise ValueError("corrective action cannot cross artifact identities or versions")
    if risk.source_assessment_ref != context.source_assessment_ref:
        raise ValueError("corrective action cannot cross assessment identities or versions")
    if risk.source_snapshot_id != context.source_snapshot_id:
        raise ValueError("corrective action cannot cross assessment snapshots")
    if risk.process_state_ref != context.process_state_ref:
        raise ValueError("corrective action cannot cross process-state versions")

    if problem is not None:
        if problem.ref != risk.problem_ref:
            raise ValueError("problem does not resolve the risk problem reference")
        if (
            problem.artifact_ref != risk.artifact_ref
            or problem.source_assessment_ref != risk.source_assessment_ref
            or problem.source_snapshot_id != risk.source_snapshot_id
        ):
            raise ValueError("problem cannot cross the risk artifact, assessment, or snapshot")
        if problem.process_state_ref != risk.process_state_ref:
            raise ValueError("problem cannot cross the risk process state")
        if problem.rule_ref != PROBLEM_RULE_REF:
            raise ValueError("corrective action requires D-QB-CONFLICT-001 / 1")

    if relation is not None:
        if relation.ref != risk.relation_ref:
            raise ValueError("relation does not resolve the risk relation reference")
        if (
            relation.artifact_ref != risk.artifact_ref
            or relation.source_assessment_ref != risk.source_assessment_ref
            or relation.source_snapshot_id != risk.source_snapshot_id
        ):
            raise ValueError("relation cannot cross the risk artifact, assessment, or snapshot")
        if relation.process_state_ref != risk.process_state_ref:
            raise ValueError("relation cannot cross the risk process state")
        if relation.problem_resolution_ref != risk.problem_resolution_ref:
            raise ValueError("relation and risk must preserve the same problem resolution")
        if relation.problem_ref != risk.problem_ref:
            raise ValueError("relation and risk must preserve the same problem reference")
        if relation.rule_ref != RELATION_RULE_REF:
            raise ValueError("corrective action requires R_DQ-PE-QB-001 / 1")

    participants = risk.subject.participant_refs
    lineages = context.target_requirement_lineages
    if lineages:
        targets = tuple(
            ActionTargetRequirement(lineage, participant)
            for lineage, participant in zip(lineages, participants, strict=True)
        )
        if len(targets) != len(participants):
            raise ValueError("lineage population must match the risk participants")


def _targets(
    risk: BoundedRiskAssessment,
    context: CorrectiveActionContext,
) -> tuple[ActionTargetRequirement, ...]:
    if not context.target_requirement_lineages:
        return ()
    if len(risk.subject.participant_refs) != 2:
        raise ValueError("target lineages cannot be attached without two risk participants")
    return tuple(
        ActionTargetRequirement(lineage, participant)
        for lineage, participant in zip(
            context.target_requirement_lineages,
            risk.subject.participant_refs,
            strict=True,
        )
    )


def _resolution_state(
    risk: BoundedRiskAssessment,
    problem: ConfirmedSupportedProblem | None,
    relation: DefectQualityRelation | None,
    context: CorrectiveActionContext,
) -> tuple[FullModelStatus, Applicability, CorrectiveActionReason]:
    if _requested_kind(context) != CorrectiveActionKind.RECONCILE_QUANTITATIVE_BOUNDS.value:
        return (
            FullModelStatus.UNSUPPORTED,
            (
                risk.applicability
                if risk.applicability is not Applicability.NOT_APPLICABLE
                else Applicability.UNKNOWN
            ),
            CorrectiveActionReason.REQUESTED_ACTION_KIND_UNSUPPORTED,
        )
    if risk.status is FullModelStatus.NOT_APPLICABLE:
        return (
            FullModelStatus.NOT_APPLICABLE,
            Applicability.NOT_APPLICABLE,
            CorrectiveActionReason.NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE,
        )
    if risk.status is FullModelStatus.UNAVAILABLE:
        return risk.status, risk.applicability, CorrectiveActionReason.SOURCE_UNAVAILABLE
    if risk.status is FullModelStatus.UNKNOWN:
        return (
            risk.status,
            risk.applicability,
            CorrectiveActionReason.SOURCE_ASSESSMENT_UNKNOWN,
        )
    if risk.status is FullModelStatus.UNRESOLVED:
        return (
            risk.status,
            risk.applicability,
            CorrectiveActionReason.SOURCE_IDENTITY_OR_COHERENCE_UNRESOLVED,
        )
    if risk.status is FullModelStatus.UNSUPPORTED:
        return risk.status, risk.applicability, CorrectiveActionReason.SOURCE_UNSUPPORTED
    if risk.status is not FullModelStatus.AVAILABLE:
        raise ValueError("unsupported risk status")
    if (
        risk.classification is not RiskClassification.RISK_IDENTIFIED
        or problem is None
        or relation is None
        or len(context.target_requirement_lineages) != 2
    ):
        return (
            FullModelStatus.UNRESOLVED,
            risk.applicability,
            CorrectiveActionReason.SOURCE_IDENTITY_OR_COHERENCE_UNRESOLVED,
        )
    return (
        FullModelStatus.AVAILABLE,
        Applicability.APPLICABLE,
        CorrectiveActionReason.ELIGIBLE_RISK_IDENTIFIED,
    )


def _resolution_provenance(
    risk: BoundedRiskAssessment,
    context: CorrectiveActionContext,
    targets: tuple[ActionTargetRequirement, ...],
) -> CorrectiveActionResolutionProvenance:
    return CorrectiveActionResolutionProvenance(
        source_risk_ref=risk.ref,
        source_problem_ref=risk.problem_ref,
        source_relation_ref=risk.relation_ref,
        artifact_ref=risk.artifact_ref,
        source_assessment_ref=risk.source_assessment_ref,
        source_snapshot_id=risk.source_snapshot_id,
        process_state_ref=risk.process_state_ref,
        participant_refs=risk.subject.participant_refs,
        target_requirements=targets,
        ordered_evidence_refs=risk.evidence_refs,
        full_model_contract_ref=context.full_model_contract_ref,
        defect_risk_contract_ref=context.defect_risk_contract_ref,
        process_reassessment_contract_ref=context.process_reassessment_contract_ref,
        source_risk_model_ref=risk.model_ref,
        source_risk_rule_ref=risk.rule_ref,
        source_risk_parameter_set_ref=risk.parameter_set_ref,
        action_rule_ref=context.action_rule_ref,
    )


def _build_action(
    risk: BoundedRiskAssessment,
    problem: ConfirmedSupportedProblem,
    relation: DefectQualityRelation,
    context: CorrectiveActionContext,
    targets: tuple[ActionTargetRequirement, ActionTargetRequirement],
) -> CorrectiveAction:
    if relation.status is not FullModelStatus.AVAILABLE:
        raise ValueError("RISK_IDENTIFIED requires the supplied relation to be AVAILABLE")
    if relation.applicability is not Applicability.APPLICABLE:
        raise ValueError("RISK_IDENTIFIED requires an APPLICABLE relation")
    if relation.relation_kind is not RelationKind.BOUNDED_RISK_RELEVANCE:
        raise ValueError("RISK_IDENTIFIED requires BOUNDED_RISK_RELEVANCE")
    if problem.status is not FullModelStatus.AVAILABLE:
        raise ValueError("RISK_IDENTIFIED requires an AVAILABLE confirmed problem")
    if problem.participant_refs != risk.subject.participant_refs:
        raise ValueError("risk and problem must preserve the same ordered participants")
    if problem.evidence_refs != risk.evidence_refs:
        raise ValueError("risk and problem must preserve the same evidence order")
    if risk.provenance.source_cross_result_ref_or_none != problem.source_cross_result_ref:
        raise ValueError("risk and problem must preserve the same cross result")

    provenance = CorrectiveActionProvenance(
        originating_risk_ref=risk.ref,
        originating_problem_ref=problem.ref,
        originating_relation_ref=relation.ref,
        problem_resolution_ref=risk.problem_resolution_ref,
        defect_population_ref=risk.defect_population_ref,
        source_cross_result_ref=problem.source_cross_result_ref,
        participant_refs=problem.participant_refs,
        target_requirements=targets,
        comparison_key=problem.comparison_key,
        ordered_evidence_refs=problem.evidence_refs,
        artifact_ref=risk.artifact_ref,
        source_assessment_ref=risk.source_assessment_ref,
        source_snapshot_id=risk.source_snapshot_id,
        process_state_ref=risk.process_state_ref,
        full_model_contract_ref=context.full_model_contract_ref,
        defect_risk_contract_ref=context.defect_risk_contract_ref,
        process_reassessment_contract_ref=context.process_reassessment_contract_ref,
        problem_rule_ref=problem.rule_ref,
        relation_rule_ref=relation.rule_ref,
        risk_model_ref=risk.model_ref,
        risk_rule_ref=risk.rule_ref,
        risk_parameter_set_ref=risk.parameter_set_ref,
        action_rule_ref=context.action_rule_ref,
        verification_rule_ref=context.verification_rule_ref,
    )
    action_id = CorrectiveActionId(
        context.action_instance_id,
        context.action_rule_ref,
        risk.risk_assessment_id,
        problem.problem_id,
        context.target_artifact_ref,
    )
    return CorrectiveAction(
        action_id=action_id,
        action_record_version=context.action_record_version,
        predecessor_action_ref=None,
        action_kind=CorrectiveActionKind.RECONCILE_QUANTITATIVE_BOUNDS,
        status=CorrectiveActionStatus.PROPOSED,
        rule_ref=ACTION_RULE_REF,
        originating_risk_ref=risk.ref,
        originating_problem_ref=problem.ref,
        originating_relation_ref=relation.ref,
        target_artifact_ref=risk.artifact_ref,
        target_requirements=targets,
        comparison_key=problem.comparison_key,
        rationale=CorrectiveActionRationale.STAKEHOLDER_RECONCILIATION_REQUIRED,
        proposed_change_kind=ProposedChangeKind.REPLACE_REQUIREMENT_TEXT,
        expected_bounded_outcome=(
            CorrectiveActionExpectedOutcome.LATER_RERUN_MAY_NOT_IDENTIFY_EXACT_CONFLICT
        ),
        verification_rule_ref=context.verification_rule_ref,
        external_revision_ref=None,
        application_ref=None,
        rejection_source_ref=None,
        creator_source=context.creator_source,
        provenance=provenance,
        non_optimality_claim=(
            CorrectiveActionNonOptimalityClaim.CANDIDATE_NOT_OPTIMALITY_CLAIM
        ),
    )


def propose_corrective_action(
    risk: BoundedRiskAssessment,
    problem: ConfirmedSupportedProblem | None,
    relation: DefectQualityRelation | None,
    context: CorrectiveActionContext,
) -> CorrectiveActionResolution:
    """Resolve the sole bounded action kind from an approved M3-07 result.

    The function creates a proposal record only. It never creates replacement
    text, mutates a requirement/specification, or creates a successor artifact.
    """

    _validate_source_refs(risk, problem, relation, context)
    targets = _targets(risk, context)
    status, applicability, reason = _resolution_state(
        risk,
        problem,
        relation,
        context,
    )
    action = None
    if status is FullModelStatus.AVAILABLE:
        if problem is None or relation is None or len(targets) != 2:
            raise ValueError("AVAILABLE action resolution requires complete typed sources")
        action = _build_action(risk, problem, relation, context, targets)
    requested_kind = _requested_kind(context)
    resolution_id = CorrectiveActionResolutionId(
        context.action_instance_id,
        risk.ref,
        requested_kind,
        context.action_rule_ref,
    )
    provenance = _resolution_provenance(risk, context, targets)
    return CorrectiveActionResolution(
        resolution_id=resolution_id,
        status=status,
        applicability=applicability,
        action_ref=None if action is None else action.ref,
        reason_codes=(reason,),
        source_risk_ref=risk.ref,
        source_problem_ref=risk.problem_ref,
        source_relation_ref=risk.relation_ref,
        rule_ref=context.action_rule_ref,
        provenance=provenance,
        action=action,
    )


__all__ = ["propose_corrective_action"]

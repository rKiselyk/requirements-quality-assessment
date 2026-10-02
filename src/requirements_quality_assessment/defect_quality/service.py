"""Pure services for the approved bounded ``P -> D -> R_DQ`` projection."""

from __future__ import annotations

from ..cross_analysis import (
    QB_COMPARISON_RULE,
    QB_COVERAGE_PROFILE,
    AssessmentSnapshot,
    AssessmentSnapshotId,
    BoundedConflictSubtype,
    ComparisonOperand,
    ConflictClass,
    ContractVersionDescriptor,
    CrossRequirementResult,
    CrossResultId,
    CrossResultState,
    QbConsistencyAssessment,
    QbConsistencyState,
)
from ..domain import UnitLabel
from ..dynamic_evidence import (
    Applicability,
    FullModelStatus,
)
from ..dynamic_evidence.domain import SUPPORTED_CONTEXT_TEXT, SUPPORTED_METRIC_TEXT
from ..metrics import (
    ContractRef,
    QbConsistencyAssessmentRef,
    RequirementSubjectRef,
    SpecificationSubjectRef,
)
from ..performance_efficiency import ProductQualityCharacteristicId
from .domain import (
    DEFECT_QUALITY_RISK_CONTRACT_REF,
    MANDATORY_PROBLEM_NON_CLAIMS,
    MANDATORY_RELATION_NON_CLAIMS,
    PROBLEM_RULE_REF,
    QB_NORMALIZATION_CONTRACT_REF,
    RELATION_RULE_REF,
    BoundOperandPosition,
    ConfirmedProblemProvenance,
    ConfirmedSupportedProblem,
    ConfirmedSupportedProblemId,
    ConflictClassificationRef,
    DefectConstructionContext,
    DefectPopulationId,
    DefectPopulationSnapshot,
    DefectQualityCalibrationStatus,
    DefectQualityRelation,
    DefectQualityRelationContext,
    DefectQualityRelationId,
    DefectQualityRelationProvenance,
    DefectType,
    ProblemClaimResolution,
    ProblemClaimResolutionId,
    ProblemClaimSourceKind,
    ProblemDisposition,
    ProblemKind,
    ProblemResolutionReason,
    QbBoundOperandRef,
    RelationKind,
    RelationReason,
    TypedProblemClaimSource,
)


def _contract_ref(value: ContractVersionDescriptor) -> ContractRef:
    return ContractRef(value.contract_id, value.version)


def _validate_context(
    source_claim: TypedProblemClaimSource,
    context: DefectConstructionContext,
) -> None:
    if not isinstance(source_claim, TypedProblemClaimSource):
        raise TypeError("source_claim must be a TypedProblemClaimSource")
    if not isinstance(context, DefectConstructionContext):
        raise TypeError("context must be a DefectConstructionContext")
    if source_claim.cross_result is not None and (
        source_claim.cross_result.snapshot_id != context.source_snapshot_id
    ):
        raise ValueError("source claim and construction context cannot cross snapshots")


def _find_requirement(snapshot: AssessmentSnapshot, requirement_id: str):
    matches = tuple(
        item for item in snapshot.requirements if item.requirement_id == requirement_id
    )
    if len(matches) != 1:
        raise ValueError("source participant must resolve exactly once in the snapshot")
    return matches[0]


def _find_observation(snapshot: AssessmentSnapshot, ref):
    requirement = _find_requirement(snapshot, ref.requirement_id)
    if ref.observation_index >= len(requirement.observations):
        raise ValueError("source observation reference is dangling")
    observation = requirement.observations[ref.observation_index]
    if observation.ref != ref:
        raise ValueError("source observation reference resolves inconsistently")
    return observation


def _validate_operand(
    operand: ComparisonOperand,
    observation,
    result: CrossRequirementResult,
) -> None:
    if operand.observation_ref != observation.ref:
        raise ValueError("operand and observation references must agree")
    if (
        operand.comparator != observation.comparator
        or operand.inclusivity != observation.inclusivity
        or operand.value != observation.value
        or operand.unit != observation.unit
    ):
        raise ValueError("operand values must resolve to the source observation")
    key = result.comparison_key
    if key is None:
        raise ValueError("a confirmed source requires a complete comparison key")
    if (
        operand.normalized_metric != key.normalized_metric
        or operand.normalized_context != key.normalized_context
        or operand.unit != key.unit
    ):
        raise ValueError("operand identities must equal the authoritative comparison key")


def _validate_ordered_references(
    result: CrossRequirementResult,
    snapshot: AssessmentSnapshot,
) -> None:
    participant_rank = {
        participant.requirement_id: index
        for index, participant in enumerate(result.participants)
    }
    evidence_by_ref = {
        evidence.ref: evidence
        for requirement in snapshot.requirements
        for evidence in requirement.evidence
    }
    if any(ref not in evidence_by_ref for ref in result.evidence_refs):
        raise ValueError("source cross result contains dangling Evidence")
    expected_evidence = tuple(
        sorted(
            result.evidence_refs,
            key=lambda ref: (
                participant_rank[ref.requirement_id],
                evidence_by_ref[ref].start_offset,
                evidence_by_ref[ref].end_offset,
                ref.evidence_id,
            ),
        )
    )
    if result.evidence_refs != expected_evidence:
        raise ValueError("source cross Evidence must preserve deterministic source order")

    diagnostics = {
        diagnostic.ref
        for requirement in snapshot.requirements
        for diagnostic in requirement.diagnostics
    }
    if any(ref not in diagnostics for ref in result.diagnostic_refs):
        raise ValueError("source cross result contains a dangling diagnostic")


def _validate_confirmed_source(
    result: CrossRequirementResult,
    snapshot: AssessmentSnapshot,
    context: DefectConstructionContext,
) -> tuple[RequirementSubjectRef, RequirementSubjectRef]:
    if snapshot.snapshot_id != AssessmentSnapshotId.from_bytes(
        snapshot.canonical_bytes()
    ):
        raise ValueError("source snapshot content contradicts its identity")
    if result.result_id != CrossResultId.from_bytes(
        result.canonical_identity_bytes()
    ):
        raise ValueError("source cross-result content contradicts its identity")
    if result.state is not CrossResultState.CONFIRMED_CONFLICT:
        raise ValueError("confirmed source validation requires CONFIRMED_CONFLICT")
    if result.conflict_class is not ConflictClass.LOGICAL_CONFLICT:
        raise ValueError("confirmed source requires LOGICAL_CONFLICT")
    if (
        result.conflict_subtype
        is not BoundedConflictSubtype.DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY
    ):
        raise ValueError("confirmed source requires the direct quantitative subtype")
    if snapshot.snapshot_id != context.source_snapshot_id:
        raise ValueError("source snapshot and construction context cannot differ")
    if result.comparison_contract != QB_COMPARISON_RULE:
        raise ValueError("source result requires QB-COMPARE-001 / 1")
    if result.coverage_profile != QB_COVERAGE_PROFILE:
        raise ValueError("source result requires QB-v0.1 / 1 coverage")
    if snapshot.contracts.coverage_profile != QB_COVERAGE_PROFILE:
        raise ValueError("source snapshot requires QB-v0.1 / 1 coverage")
    if _contract_ref(snapshot.contracts.normalization) != QB_NORMALIZATION_CONTRACT_REF:
        raise ValueError("source snapshot requires QB-NORMALIZATION / 1")

    requirement_manifests = tuple(
        _find_requirement(snapshot, participant.requirement_id)
        for participant in result.participants
    )
    if tuple(item.order_key for item in requirement_manifests) != result.participants:
        raise ValueError("source participants must preserve exact snapshot identities")
    observations = tuple(
        _find_observation(snapshot, ref) for ref in result.observation_refs
    )
    _validate_operand(result.operands.left, observations[0], result)
    _validate_operand(result.operands.right, observations[1], result)
    _validate_ordered_references(result, snapshot)
    if any(not observation.evidence_refs for observation in observations):
        raise ValueError("each source operand requires quantitative Evidence")
    expected_evidence = {
        ref for observation in observations for ref in observation.evidence_refs
    }
    if set(result.evidence_refs) != expected_evidence:
        raise ValueError("source cross Evidence must cover both exact operands")

    return tuple(
        RequirementSubjectRef(
            context.artifact_ref,
            manifest.requirement_id,
            manifest.source_line,
        )
        for manifest in requirement_manifests
    )


def _problem_explanation(result: CrossRequirementResult) -> str:
    key = result.comparison_key
    left = result.operands.left
    right = result.operands.right
    return (
        "QB-v0.1 confirmed an empty admissible-set intersection for "
        f"{result.participants[0].requirement_id}/{left.observation_ref.observation_index} "
        f"({left.comparator.value} {left.value} {key.unit.value}) and "
        f"{result.participants[1].requirement_id}/{right.observation_ref.observation_index} "
        f"({right.comparator.value} {right.value} {key.unit.value}) under metric "
        f"'{key.normalized_metric}' and context '{key.normalized_context}'. "
        "This is a confirmed specification inconsistency, not a product defect."
    )


def _build_problem(
    result: CrossRequirementResult,
    snapshot: AssessmentSnapshot,
    context: DefectConstructionContext,
) -> ConfirmedSupportedProblem:
    participants = _validate_confirmed_source(result, snapshot, context)
    operand_refs = (
        QbBoundOperandRef(
            result.result_id,
            BoundOperandPosition.LEFT,
            result.observation_refs[0],
        ),
        QbBoundOperandRef(
            result.result_id,
            BoundOperandPosition.RIGHT,
            result.observation_refs[1],
        ),
    )
    problem_id = ConfirmedSupportedProblemId(
        context.artifact_ref,
        context.source_assessment_ref,
        context.source_snapshot_id,
        result.result_id,
        context.problem_rule_ref,
    )
    provenance = ConfirmedProblemProvenance(
        source_cross_result_ref=result.result_id,
        source_snapshot_id=result.snapshot_id,
        participant_refs=participants,
        source_observation_refs=result.observation_refs,
        comparison_key=result.comparison_key,
        exact_operand_refs=operand_refs,
        ordered_cross_evidence_refs=result.evidence_refs,
        diagnostic_refs=result.diagnostic_refs,
        normalization_contract_ref=QB_NORMALIZATION_CONTRACT_REF,
        coverage_profile_ref=_contract_ref(result.coverage_profile),
        comparison_rule_ref=_contract_ref(result.comparison_contract),
        conflict_classification_ref=ConflictClassificationRef(
            result.result_id,
            result.conflict_class,
            result.conflict_subtype,
        ),
        source_non_claim_refs=result.non_claim_keys,
        problem_rule_ref=context.problem_rule_ref,
    )
    return ConfirmedSupportedProblem(
        problem_id=problem_id,
        problem_kind=ProblemKind.CONFIRMED_SUPPORTED_PROBLEM,
        defect_type=DefectType.SPECIFICATION_INCONSISTENCY,
        conflict_class=result.conflict_class,
        conflict_subtype=result.conflict_subtype,
        target_ref=SpecificationSubjectRef(context.artifact_ref),
        participant_refs=participants,
        source_cross_result_ref=result.result_id,
        source_observation_refs=result.observation_refs,
        comparison_key=result.comparison_key,
        operand_refs=operand_refs,
        status=FullModelStatus.AVAILABLE,
        applicability=Applicability.APPLICABLE,
        evidence_refs=result.evidence_refs,
        diagnostic_refs=result.diagnostic_refs,
        explanation=_problem_explanation(result),
        provenance=provenance,
        artifact_ref=context.artifact_ref,
        source_assessment_ref=context.source_assessment_ref,
        source_snapshot_id=context.source_snapshot_id,
        process_state_ref=context.process_state_ref,
        rule_ref=context.problem_rule_ref,
        non_claims=MANDATORY_PROBLEM_NON_CLAIMS,
    )


class DefectBuilder:
    """Resolve one typed source claim under ``D-QB-CONFLICT-001 / 1``."""

    def resolve(
        self,
        source_claim: TypedProblemClaimSource,
        context: DefectConstructionContext,
    ) -> ProblemClaimResolution:
        _validate_context(source_claim, context)
        resolution_id = ProblemClaimResolutionId(
            context.artifact_ref,
            context.source_assessment_ref,
            context.source_snapshot_id,
            source_claim.source_claim_ref,
            context.problem_rule_ref,
        )
        provenance_refs = (
            source_claim.source_claim_ref,
            context.full_model_contract_ref,
            context.defect_risk_contract_ref,
            *(
                (
                    QB_NORMALIZATION_CONTRACT_REF,
                    _contract_ref(source_claim.cross_result.coverage_profile),
                    _contract_ref(source_claim.cross_result.comparison_contract),
                )
                if source_claim.cross_result is not None
                else ()
            ),
            context.problem_rule_ref,
        )
        kind = source_claim.source_claim_ref.source_kind
        if kind is not ProblemClaimSourceKind.QB_CROSS_REQUIREMENT_RESULT:
            status = (
                source_claim.status
                if kind is ProblemClaimSourceKind.FUTURE_APPROVED_SOURCE
                and source_claim.status is FullModelStatus.UNKNOWN
                else FullModelStatus.UNSUPPORTED
            )
            reason = (
                ProblemResolutionReason.SOURCE_STATE_UNKNOWN
                if status is FullModelStatus.UNKNOWN
                else ProblemResolutionReason.SOURCE_KIND_UNSUPPORTED
            )
            return ProblemClaimResolution(
                resolution_id,
                source_claim.source_claim_ref,
                status,
                source_claim.applicability,
                None,
                None,
                "The typed source has no approved Full Model v0.1 problem rule.",
                (reason,),
                (),
                provenance_refs,
                context.artifact_ref,
                context.source_assessment_ref,
                context.source_snapshot_id,
                context.problem_rule_ref,
            )

        result = source_claim.cross_result
        if result is None:
            reason = (
                ProblemResolutionReason.SUPPORTED_SOURCE_UNAVAILABLE
                if source_claim.status is FullModelStatus.UNAVAILABLE
                else ProblemResolutionReason.SOURCE_STATE_UNKNOWN
            )
            return ProblemClaimResolution(
                resolution_id,
                source_claim.source_claim_ref,
                source_claim.status,
                source_claim.applicability,
                None,
                None,
                "The supported QB source result is not available for this version.",
                (reason,),
                (),
                provenance_refs,
                context.artifact_ref,
                context.source_assessment_ref,
                context.source_snapshot_id,
                context.problem_rule_ref,
            )

        if result.state is CrossResultState.CONFIRMED_CONFLICT:
            problem = _build_problem(result, source_claim.source_snapshot, context)
            return ProblemClaimResolution(
                resolution_id,
                source_claim.source_claim_ref,
                FullModelStatus.AVAILABLE,
                Applicability.APPLICABLE,
                ProblemDisposition.CONFIRMED_SUPPORTED_PROBLEM,
                problem,
                "The exact accepted QB conflict satisfies D-QB-CONFLICT-001 / 1.",
                (ProblemResolutionReason.CONFIRMED_QB_CONFLICT,),
                result.evidence_refs,
                provenance_refs,
                context.artifact_ref,
                context.source_assessment_ref,
                context.source_snapshot_id,
                context.problem_rule_ref,
            )
        if result.state is CrossResultState.COMPATIBLE_WITHIN_RULE:
            reason = ProblemResolutionReason.QB_COMPATIBLE_WITHIN_RULE
            status = FullModelStatus.AVAILABLE
            applicability = Applicability.APPLICABLE
            disposition = (
                ProblemDisposition.NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE
            )
            explanation = (
                "The accepted QB result is compatible within the bounded rule; "
                "no confirmed supported problem is constructed."
            )
        elif result.state is CrossResultState.ASSESSMENT_UNRESOLVED:
            reason = ProblemResolutionReason.QB_ASSESSMENT_UNRESOLVED
            status = FullModelStatus.UNRESOLVED
            applicability = source_claim.applicability
            disposition = None
            explanation = (
                "The QB problem claim remains unresolved and is not converted into "
                "a confirmed problem."
            )
        else:
            reason = ProblemResolutionReason.QB_OUTSIDE_V0_1_APPLICABILITY
            status = FullModelStatus.NOT_APPLICABLE
            applicability = Applicability.NOT_APPLICABLE
            disposition = None
            explanation = (
                "The QB result is outside v0.1 applicability and is not a problem."
            )
        return ProblemClaimResolution(
            resolution_id,
            source_claim.source_claim_ref,
            status,
            applicability,
            disposition,
            None,
            explanation,
            (reason,),
            result.evidence_refs,
            provenance_refs,
            context.artifact_ref,
            context.source_assessment_ref,
            context.source_snapshot_id,
            context.problem_rule_ref,
        )


def resolve_problem_claim(
    source_claim: TypedProblemClaimSource,
    context: DefectConstructionContext,
) -> ProblemClaimResolution:
    return DefectBuilder().resolve(source_claim, context)


def build_defect_population(
    resolutions: tuple[ProblemClaimResolution, ...],
    qb_assessment: QbConsistencyAssessment,
    context: DefectConstructionContext,
) -> DefectPopulationSnapshot:
    if not isinstance(resolutions, tuple) or any(
        not isinstance(item, ProblemClaimResolution) for item in resolutions
    ):
        raise TypeError("resolutions must be a tuple of ProblemClaimResolution values")
    if not isinstance(qb_assessment, QbConsistencyAssessment):
        raise TypeError("qb_assessment must be a QbConsistencyAssessment")
    if qb_assessment.snapshot_id != context.source_snapshot_id:
        raise ValueError("QB assessment and population context cannot cross snapshots")
    if any(
        item.artifact_ref != context.artifact_ref
        or item.source_assessment_ref != context.source_assessment_ref
        or item.source_snapshot_id != context.source_snapshot_id
        or item.rule_ref != context.problem_rule_ref
        for item in resolutions
    ):
        raise ValueError("population resolutions must share one construction context")
    if tuple(item.source_claim_ref.source_id for item in resolutions) != tuple(
        item.value for item in qb_assessment.cross_result_ids
    ):
        raise ValueError("population resolutions must preserve QB source-result order")

    members = tuple(
        item.problem.ref
        for item in resolutions
        if item.disposition is ProblemDisposition.CONFIRMED_SUPPORTED_PROBLEM
    )
    unresolved = tuple(
        item.ref
        for item in resolutions
        if item.status in {FullModelStatus.UNRESOLVED, FullModelStatus.UNKNOWN}
    )
    if qb_assessment.state is QbConsistencyState.COMPUTED:
        if unresolved:
            raise ValueError("a computed QB universe cannot contain unresolved claims")
        status = FullModelStatus.AVAILABLE
        applicability = Applicability.APPLICABLE
        complete = True
    elif qb_assessment.state is QbConsistencyState.UNKNOWN:
        status = FullModelStatus.UNRESOLVED if unresolved else FullModelStatus.UNKNOWN
        applicability = Applicability.UNKNOWN
        complete = False
    else:
        if resolutions or members:
            raise ValueError("a not-applicable QB universe must have no cross results")
        status = FullModelStatus.NOT_APPLICABLE
        applicability = Applicability.NOT_APPLICABLE
        complete = True

    aggregation_ref = _contract_ref(qb_assessment.aggregation_rule)
    coverage_ref = _contract_ref(qb_assessment.coverage_profile)
    qb_ref = QbConsistencyAssessmentRef(
        context.source_assessment_ref,
        context.artifact_ref,
        context.source_snapshot_id,
        aggregation_ref,
        coverage_ref,
    )
    return DefectPopulationSnapshot(
        population_id=DefectPopulationId(
            context.artifact_ref,
            context.source_assessment_ref,
            context.source_snapshot_id,
            context.problem_rule_ref,
        ),
        artifact_ref=context.artifact_ref,
        source_assessment_ref=context.source_assessment_ref,
        source_snapshot_id=context.source_snapshot_id,
        status=status,
        applicability=applicability,
        members=members,
        population_complete=complete,
        problem_resolution_refs=tuple(item.ref for item in resolutions),
        unresolved_resolution_refs=unresolved,
        source_qb_assessment_ref=qb_ref,
        provenance_refs=(
            context.full_model_contract_ref,
            context.defect_risk_contract_ref,
            aggregation_ref,
            coverage_ref,
            context.problem_rule_ref,
        ),
        rule_ref=context.problem_rule_ref,
    )


def _relation_context_agrees(
    resolution: ProblemClaimResolution,
    context: DefectQualityRelationContext,
) -> None:
    if not isinstance(resolution, ProblemClaimResolution):
        raise TypeError("problem_resolution must be a ProblemClaimResolution")
    if not isinstance(context, DefectQualityRelationContext):
        raise TypeError("relation_context must be a DefectQualityRelationContext")
    if (
        resolution.artifact_ref != context.artifact_ref
        or resolution.source_assessment_ref != context.source_assessment_ref
        or resolution.source_snapshot_id != context.source_snapshot_id
    ):
        raise ValueError("problem resolution and relation context cannot mix versions")
    if resolution.problem is not None and (
        resolution.problem.process_state_ref != context.process_state_ref
    ):
        raise ValueError("problem and relation must share one process state")


def _relation_state(
    resolution: ProblemClaimResolution,
) -> tuple[FullModelStatus, Applicability, RelationKind | None, RelationReason, str]:
    problem = resolution.problem
    if (
        resolution.disposition
        is ProblemDisposition.NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE
    ):
        return (
            FullModelStatus.NOT_APPLICABLE,
            Applicability.NOT_APPLICABLE,
            None,
            RelationReason.NO_CONFIRMED_SUPPORTED_PROBLEM,
            "No confirmed supported problem exists within the bounded source rule.",
        )
    if resolution.status is not FullModelStatus.AVAILABLE:
        reasons = {
            FullModelStatus.UNRESOLVED: RelationReason.PROBLEM_CLAIM_UNRESOLVED,
            FullModelStatus.UNSUPPORTED: RelationReason.PROBLEM_CLAIM_UNSUPPORTED,
            FullModelStatus.UNAVAILABLE: RelationReason.PROBLEM_CLAIM_UNAVAILABLE,
            FullModelStatus.UNKNOWN: RelationReason.PROBLEM_CLAIM_UNKNOWN,
            FullModelStatus.NOT_APPLICABLE: (
                RelationReason.PROBLEM_CLAIM_NOT_APPLICABLE
            ),
        }
        return (
            resolution.status,
            resolution.applicability,
            None,
            reasons[resolution.status],
            "The problem resolution has no available confirmed problem to map.",
        )
    if problem is None:
        raise ValueError("an available positive resolution requires its problem")
    key = problem.comparison_key
    if key.normalized_metric != SUPPORTED_METRIC_TEXT:
        return (
            FullModelStatus.NOT_APPLICABLE,
            Applicability.NOT_APPLICABLE,
            None,
            RelationReason.DIFFERENT_RESOLVED_METRIC,
            "The confirmed problem has a resolved metric outside the PE reference key.",
        )
    if key.normalized_context != SUPPORTED_CONTEXT_TEXT or key.unit is not UnitLabel.SECOND:
        return (
            FullModelStatus.UNSUPPORTED,
            Applicability.APPLICABLE,
            None,
            RelationReason.UNSUPPORTED_RESPONSE_TIME_CONTEXT_OR_UNIT,
            "The response-time problem has an unsupported context or unit; no "
            "equivalence or conversion is inferred.",
        )
    return (
        FullModelStatus.AVAILABLE,
        Applicability.APPLICABLE,
        RelationKind.BOUNDED_RISK_RELEVANCE,
        RelationReason.EXACT_RESPONSE_TIME_KEY,
        "Mutually incompatible response-time targets for the exact unit and "
        "context are relevant to selecting, implementing, and verifying an "
        "authoritative Performance Efficiency target. This is relevance only, "
        "not causality or proof of poor product performance.",
    )


class DefectQualityMapper:
    """Apply the exact ``R_DQ-PE-QB-001 / 1`` relevance relation."""

    def relate(
        self,
        problem_resolution: ProblemClaimResolution,
        relation_context: DefectQualityRelationContext,
    ) -> DefectQualityRelation:
        _relation_context_agrees(problem_resolution, relation_context)
        status, applicability, relation_kind, reason, rationale = _relation_state(
            problem_resolution
        )
        problem = problem_resolution.problem
        problem_ref = problem.ref if problem is not None else None
        relation_id = DefectQualityRelationId(
            problem_resolution.ref,
            problem_ref,
            ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
            relation_context.relation_rule_ref,
        )
        evidence_refs = problem.evidence_refs if problem is not None else ()
        source_cross_result_ref = (
            problem.source_cross_result_ref if problem is not None else None
        )
        comparison_key = problem.comparison_key if problem is not None else None
        source_contract_refs = (
            relation_context.full_model_contract_ref,
            relation_context.defect_risk_contract_ref,
            QB_NORMALIZATION_CONTRACT_REF,
            *(
                (
                    problem.provenance.coverage_profile_ref,
                    problem.provenance.comparison_rule_ref,
                )
                if problem is not None
                else ()
            ),
        )
        provenance = DefectQualityRelationProvenance(
            problem_resolution_ref=problem_resolution.ref,
            problem_ref=problem_ref,
            source_cross_result_ref=source_cross_result_ref,
            comparison_key=comparison_key,
            characteristic_id=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
            relation_rule_ref=relation_context.relation_rule_ref,
            rationale_code=reason,
            evidence_refs=evidence_refs,
            source_contract_refs=source_contract_refs,
        )
        return DefectQualityRelation(
            relation_id=relation_id,
            problem_resolution_ref=problem_resolution.ref,
            problem_ref=problem_ref,
            characteristic_id=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
            relation_kind=relation_kind,
            status=status,
            applicability=applicability,
            rationale=rationale,
            reasons=(reason,),
            source_result_refs=(problem_resolution.source_claim_ref,),
            evidence_refs=evidence_refs,
            provenance=provenance,
            artifact_ref=relation_context.artifact_ref,
            source_assessment_ref=relation_context.source_assessment_ref,
            source_snapshot_id=relation_context.source_snapshot_id,
            process_state_ref=relation_context.process_state_ref,
            rule_ref=relation_context.relation_rule_ref,
            calibration_status=(
                DefectQualityCalibrationStatus.PROVISIONAL_NOT_CALIBRATED
            ),
            non_claims=MANDATORY_RELATION_NON_CLAIMS,
        )


def relate_problem_to_quality(
    problem_resolution: ProblemClaimResolution,
    relation_context: DefectQualityRelationContext,
) -> DefectQualityRelation:
    return DefectQualityMapper().relate(problem_resolution, relation_context)


__all__ = [
    "DefectBuilder",
    "DefectQualityMapper",
    "build_defect_population",
    "relate_problem_to_quality",
    "resolve_problem_claim",
]

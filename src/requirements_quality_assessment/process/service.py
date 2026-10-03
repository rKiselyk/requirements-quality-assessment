"""Pure assembly and validation for the one-stage M_process projection."""

from __future__ import annotations

from dataclasses import dataclass

from ..corrective_action import ActionApplication, ActionRef, ArtifactTransition
from ..defect_quality import (
    ConfirmedSupportedProblemRef,
    DefectQualityRelationRef,
)
from ..dynamic_evidence import FullModelStatus
from ..metrics import FULL_MODEL_CONTRACT_REF, ArtifactRef, AssessmentRef, ContractRef
from ..performance_efficiency import ProcessStage, ProcessStateRef
from ..reassessment import ComponentVersionSet, ReassessmentRun, ResultComparison
from ..risk import BoundedRiskAssessmentRef, ProductQualityAssessmentRef
from .domain import (
    PROCESS_RULE_REF,
    ArtifactTransitionRef,
    ComparisonRef,
    DefectPopulationRef,
    MetricProfileRef,
    PerformanceEfficiencyFeatureProfileRef,
    ProcessAssessmentState,
    ProcessAssessmentStateProvenance,
    ProcessComponentAssociation,
    ProcessComponentRole,
    ProcessEvidenceAssociation,
    ProcessEvidenceRole,
    ProcessStateTransition,
    ProcessStateTransitionId,
    ProcessStateTransitionProvenance,
    RequirementAssessmentRef,
    SpecificationAssessmentRef,
)


@dataclass(frozen=True, slots=True)
class ProcessStateAssembly:
    process_lineage_id: str
    artifact_ref: ArtifactRef
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
    predecessor_process_state_ref: ProcessStateRef | None = None
    artifact_transition_or_none: ArtifactTransition | None = None
    action_application_or_none: ActionApplication | None = None
    reassessment_run_or_none: ReassessmentRun | None = None
    comparisons: tuple[ResultComparison, ...] = ()


_COMPONENT_ORDER = {role: index for index, role in enumerate(ProcessComponentRole)}
_EVIDENCE_ORDER = {role: index for index, role in enumerate(ProcessEvidenceRole)}


def _typed_tuple(value: object, item_type: type, name: str) -> None:
    if not isinstance(value, tuple) or any(not isinstance(item, item_type) for item in value):
        raise TypeError(f"{name} must be a tuple of {item_type.__name__} values")


def _validate_association_order_and_coverage(
    assembly: ProcessStateAssembly,
) -> None:
    _typed_tuple(
        assembly.component_associations,
        ProcessComponentAssociation,
        "component_associations",
    )
    _typed_tuple(
        assembly.evidence_associations,
        ProcessEvidenceAssociation,
        "evidence_associations",
    )
    component_roles = tuple(item.role for item in assembly.component_associations)
    component_order = tuple(_COMPONENT_ORDER[item] for item in component_roles)
    if component_order != tuple(sorted(component_order)):
        raise ValueError("component associations must preserve contract registry order")
    missing_roles = tuple(role for role in ProcessComponentRole if role not in component_roles)
    if missing_roles:
        raise ValueError(f"every component role requires an association: {missing_roles!r}")
    evidence_roles = tuple(item.role for item in assembly.evidence_associations)
    evidence_order = tuple(_EVIDENCE_ORDER[item] for item in evidence_roles)
    if evidence_order != tuple(sorted(evidence_order)):
        raise ValueError("evidence associations must preserve contract registry order")
    missing_evidence = tuple(role for role in ProcessEvidenceRole if role not in evidence_roles)
    if missing_evidence:
        raise ValueError(f"every evidence role requires an association: {missing_evidence!r}")


def _association_refs(
    assembly: ProcessStateAssembly,
    role: ProcessComponentRole,
) -> tuple[object, ...]:
    return tuple(
        item.result_ref
        for item in assembly.component_associations
        if item.role is role and item.result_ref is not None
    )


def _validate_convenience_refs(assembly: ProcessStateAssembly) -> None:
    expected = {
        ProcessComponentRole.REQUIREMENT_ASSESSMENT: assembly.requirement_assessment_refs,
        ProcessComponentRole.SPECIFICATION_ASSESSMENT: (
            assembly.specification_assessment_ref,
        ),
        ProcessComponentRole.METRIC_PROFILE: (assembly.metric_profile_ref,),
        ProcessComponentRole.PE_FEATURE_PROFILE: (
            () if assembly.pe_feature_profile_ref is None else (assembly.pe_feature_profile_ref,)
        ),
        ProcessComponentRole.PRODUCT_QUALITY_ASSESSMENT: (
            ()
            if assembly.product_quality_assessment_ref is None
            else (assembly.product_quality_assessment_ref,)
        ),
        ProcessComponentRole.DEFECT_POPULATION: (assembly.defect_population_ref,),
        ProcessComponentRole.CONFIRMED_PROBLEM: assembly.confirmed_problem_refs,
        ProcessComponentRole.DEFECT_QUALITY_RELATION: assembly.defect_quality_relation_refs,
        ProcessComponentRole.BOUNDED_RISK_ASSESSMENT: assembly.bounded_risk_assessment_refs,
        ProcessComponentRole.CORRECTIVE_ACTION: assembly.corrective_action_refs,
    }
    for role, convenience_refs in expected.items():
        if _association_refs(assembly, role) != convenience_refs:
            raise ValueError(
                f"{role.value} convenience refs must equal their component associations"
            )


def _validate_current_refs(
    process_state_ref: ProcessStateRef,
    assembly: ProcessStateAssembly,
) -> None:
    artifact = assembly.artifact_ref
    assessment = assembly.assessment_ref
    if assessment.artifact_ref != artifact:
        raise ValueError("assessment ref must identify the process artifact version")
    if assembly.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
        raise ValueError("process assembly requires FULL-MODEL-V0.1-CONTRACT / 1")
    if assembly.process_lineage_id != process_state_ref.process_state_id:
        raise ValueError("process lineage must equal the reserved stable process ID")

    if any(
        item.assessment_ref != assessment
        or item.requirement_subject_ref.artifact_ref != artifact
        for item in assembly.requirement_assessment_refs
    ):
        raise ValueError("requirement assessment refs cannot mix artifact or assessment")
    if assembly.specification_assessment_ref.assessment_ref != assessment:
        raise ValueError("specification assessment ref cannot mix assessments")
    if (
        assembly.metric_profile_ref.artifact_ref != artifact
        or assembly.metric_profile_ref.assessment_ref != assessment
    ):
        raise ValueError("MetricProfile ref cannot mix artifact or assessment")
    if assembly.pe_feature_profile_ref is not None and (
        assembly.pe_feature_profile_ref.artifact_ref != artifact
        or assembly.pe_feature_profile_ref.source_assessment_ref != assessment
        or assembly.pe_feature_profile_ref.metric_profile_ref
        != assembly.metric_profile_ref
        or assembly.pe_feature_profile_ref.process_state_ref != process_state_ref
    ):
        raise ValueError("X_PE ref cannot mix artifact, assessment, metric, or process state")
    if assembly.product_quality_assessment_ref is not None:
        quality_id = assembly.product_quality_assessment_ref.assessment_id
        if (
            quality_id.assessment_event_ref.artifact_ref != artifact
            or quality_id.feature_profile_ref.process_state_ref != process_state_ref
            or quality_id.feature_profile_ref.source_assessment_ref != assessment
        ):
            raise ValueError("product-quality ref cannot mix process context")
    population_id = assembly.defect_population_ref.population_id
    if (
        population_id.artifact_ref != artifact
        or population_id.source_assessment_ref != assessment
    ):
        raise ValueError("defect population ref cannot mix artifact or assessment")
    if any(
        ref.problem_id.artifact_ref != artifact
        or ref.problem_id.source_assessment_ref != assessment
        for ref in assembly.confirmed_problem_refs
    ):
        raise ValueError("confirmed problem refs cannot mix artifact or assessment")
    if any(
        ref.relation_id.problem_resolution_ref.resolution_id.artifact_ref != artifact
        or ref.relation_id.problem_resolution_ref.resolution_id.source_assessment_ref
        != assessment
        for ref in assembly.defect_quality_relation_refs
    ):
        raise ValueError("defect-quality relation refs cannot mix artifact or assessment")
    if any(
        ref.risk_assessment_id.assessment_event_ref.artifact_ref != artifact
        or ref.risk_assessment_id.assessment_event_ref.process_state_ref
        != process_state_ref
        for ref in assembly.bounded_risk_assessment_refs
    ):
        raise ValueError("bounded risk refs cannot mix artifact or process state")

    for evidence in assembly.evidence_associations:
        if isinstance(evidence.artifact_or_product_ref, ArtifactRef) and (
            evidence.artifact_or_product_ref != artifact
        ):
            raise ValueError("evidence association cannot mix artifact versions")
        reuse = evidence.reuse_decision_ref_or_none
        if reuse is not None and (
            getattr(reuse, "target_process_state_ref", None) != process_state_ref
        ):
            raise ValueError("evidence reuse decision must target this process state")


def _validate_initial_lineage(
    process_state_ref: ProcessStateRef,
    assembly: ProcessStateAssembly,
) -> None:
    if assembly.predecessor_process_state_ref is None:
        if any(
            item is not None
            for item in (
                assembly.artifact_transition_or_none,
                assembly.action_application_or_none,
                assembly.reassessment_run_or_none,
            )
        ) or assembly.comparisons:
            raise ValueError("initial process state cannot fabricate reassessment lineage")
        if any(
            ref.action_id.target_artifact_ref != assembly.artifact_ref
            or ref.action_id.originating_risk_id.assessment_event_ref.process_state_ref
            != process_state_ref
            for ref in assembly.corrective_action_refs
        ):
            raise ValueError("initial corrective actions must bind to this process state")
        return

    predecessor = assembly.predecessor_process_state_ref
    if predecessor == process_state_ref:
        raise ValueError("successor process state identity must be distinct")
    if (
        predecessor.process_state_id != process_state_ref.process_state_id
        or predecessor.stage is not process_state_ref.stage
    ):
        raise ValueError("successor must preserve process lineage and stage")
    if any(
        item is None
        for item in (
            assembly.artifact_transition_or_none,
            assembly.action_application_or_none,
            assembly.reassessment_run_or_none,
        )
    ):
        raise ValueError("successor process state requires transition/application/ReEval")

    transition = assembly.artifact_transition_or_none
    application = assembly.action_application_or_none
    reassessment = assembly.reassessment_run_or_none
    assert transition is not None and application is not None and reassessment is not None
    if transition.child_artifact_ref != assembly.artifact_ref:
        raise ValueError("artifact transition must identify the state artifact")
    if (
        application.transition != transition
        or application.ref != transition.action_application_ref
    ):
        raise ValueError("action application and artifact transition lineage disagree")
    action_origin = application.action_before_ref.action_id
    if (
        action_origin.target_artifact_ref != transition.parent_artifact_ref
        or action_origin.originating_risk_id.assessment_event_ref.process_state_ref
        != predecessor
    ):
        raise ValueError("application action must originate in the predecessor lineage")
    if reassessment.child_process_state_ref != process_state_ref:
        raise ValueError("ReEval must bind to the reserved process-state ref")
    if (
        reassessment.context.predecessor_process_state_ref != predecessor
        or reassessment.context.action_application_ref != application.ref
        or reassessment.context.parent_artifact_ref != transition.parent_artifact_ref
        or reassessment.context.child_artifact_ref != assembly.artifact_ref
        or reassessment.context.child_assessment_ref != assembly.assessment_ref
        or reassessment.context.component_version_set != assembly.component_version_set
        or reassessment.context.full_model_contract_ref
        != assembly.full_model_contract_ref
        or reassessment.context.stage is not process_state_ref.stage
    ):
        raise ValueError("ReEval context and successor process lineage disagree")
    if reassessment.status is not FullModelStatus.AVAILABLE:
        raise ValueError("a successor state requires a completed AVAILABLE ReEval")
    if application.action_after_ref not in assembly.corrective_action_refs:
        raise ValueError("successor state must preserve the applied action ref")
    if any(
        ref.action_id != application.action_after_ref.action_id
        for ref in assembly.corrective_action_refs
    ):
        raise ValueError("successor corrective-action refs cannot mix action lineages")

    for comparison in assembly.comparisons:
        before = comparison.before_result_ref
        after = comparison.after_result_ref
        if before is not None and before.artifact_ref != transition.parent_artifact_ref:
            raise ValueError("comparison before ref must identify the parent artifact")
        if after is not None and after.artifact_ref != assembly.artifact_ref:
            raise ValueError("comparison after ref must identify the child artifact")


def _comparison_refs(
    comparisons: tuple[ResultComparison, ...],
) -> tuple[ComparisonRef, ...]:
    return tuple(
        ComparisonRef(item.comparison_id, item.comparison_version)
        for item in comparisons
    )


def assemble_process_state(
    process_state_ref: ProcessStateRef,
    assembly: ProcessStateAssembly,
) -> ProcessAssessmentState:
    """Materialize an immutable state from already-produced records and refs.

    This boundary validates and associates values only. It invokes no extractor,
    calculator, quality model, risk classifier, action selector, comparison, or
    reporting behavior.
    """

    if not isinstance(process_state_ref, ProcessStateRef):
        raise TypeError("process_state_ref must be a reserved ProcessStateRef")
    if not isinstance(assembly, ProcessStateAssembly):
        raise TypeError("assembly must be a ProcessStateAssembly")
    if process_state_ref.stage is not ProcessStage.REFERENCE_VERIFICATION:
        raise ValueError("M_process v0.1 supports REFERENCE_VERIFICATION only")
    _typed_tuple(
        assembly.requirement_assessment_refs,
        RequirementAssessmentRef,
        "requirement_assessment_refs",
    )
    _typed_tuple(
        assembly.confirmed_problem_refs,
        ConfirmedSupportedProblemRef,
        "confirmed_problem_refs",
    )
    _typed_tuple(
        assembly.defect_quality_relation_refs,
        DefectQualityRelationRef,
        "defect_quality_relation_refs",
    )
    _typed_tuple(
        assembly.bounded_risk_assessment_refs,
        BoundedRiskAssessmentRef,
        "bounded_risk_assessment_refs",
    )
    _typed_tuple(assembly.corrective_action_refs, ActionRef, "corrective_action_refs")
    _typed_tuple(assembly.comparisons, ResultComparison, "comparisons")
    if not isinstance(assembly.component_version_set, ComponentVersionSet):
        raise TypeError("component_version_set must be a ComponentVersionSet")

    _validate_association_order_and_coverage(assembly)
    _validate_convenience_refs(assembly)
    _validate_current_refs(process_state_ref, assembly)
    _validate_initial_lineage(process_state_ref, assembly)

    artifact_transition_ref = (
        None
        if assembly.artifact_transition_or_none is None
        else ArtifactTransitionRef(assembly.artifact_transition_or_none.transition_id)
    )
    action_application_ref = (
        None
        if assembly.action_application_or_none is None
        else assembly.action_application_or_none.ref
    )
    reassessment_ref = (
        None
        if assembly.reassessment_run_or_none is None
        else assembly.reassessment_run_or_none.ref
    )
    comparison_refs = _comparison_refs(assembly.comparisons)
    provenance = ProcessAssessmentStateProvenance(
        process_state_ref=process_state_ref,
        process_lineage_id=assembly.process_lineage_id,
        artifact_ref=assembly.artifact_ref,
        assessment_ref=assembly.assessment_ref,
        predecessor_process_state_ref=assembly.predecessor_process_state_ref,
        artifact_transition_ref_or_none=artifact_transition_ref,
        action_application_ref_or_none=action_application_ref,
        reassessment_ref_or_none=reassessment_ref,
        comparison_refs=comparison_refs,
        evidence_associations=assembly.evidence_associations,
        component_associations=assembly.component_associations,
        component_version_set=assembly.component_version_set,
        full_model_contract_ref=assembly.full_model_contract_ref,
    )
    return ProcessAssessmentState(
        process_state_id=process_state_ref.process_state_id,
        process_state_version=process_state_ref.process_state_version,
        process_lineage_id=assembly.process_lineage_id,
        stage=process_state_ref.stage,
        artifact_ref=assembly.artifact_ref,
        artifact_transition_ref_or_none=artifact_transition_ref,
        assessment_ref=assembly.assessment_ref,
        full_model_contract_ref=assembly.full_model_contract_ref,
        component_version_set=assembly.component_version_set,
        evidence_associations=assembly.evidence_associations,
        component_associations=assembly.component_associations,
        requirement_assessment_refs=assembly.requirement_assessment_refs,
        specification_assessment_ref=assembly.specification_assessment_ref,
        metric_profile_ref=assembly.metric_profile_ref,
        pe_feature_profile_ref=assembly.pe_feature_profile_ref,
        product_quality_assessment_ref=assembly.product_quality_assessment_ref,
        defect_population_ref=assembly.defect_population_ref,
        confirmed_problem_refs=assembly.confirmed_problem_refs,
        defect_quality_relation_refs=assembly.defect_quality_relation_refs,
        bounded_risk_assessment_refs=assembly.bounded_risk_assessment_refs,
        corrective_action_refs=assembly.corrective_action_refs,
        predecessor_process_state_ref=assembly.predecessor_process_state_ref,
        reassessment_ref=reassessment_ref,
        provenance=provenance,
    )


def assemble_process_transition(
    transition_id: str,
    predecessor: ProcessAssessmentState,
    successor: ProcessAssessmentState,
) -> ProcessStateTransition:
    """Associate two immutable states without mutating either state."""

    if not isinstance(predecessor, ProcessAssessmentState) or not isinstance(
        successor, ProcessAssessmentState
    ):
        raise TypeError("predecessor and successor must be ProcessAssessmentState values")
    if successor.predecessor_process_state_ref != predecessor.ref:
        raise ValueError("successor must identify the exact predecessor state")
    provenance = successor.provenance
    if (
        provenance.artifact_transition_ref_or_none is None
        or provenance.action_application_ref_or_none is None
        or provenance.reassessment_ref_or_none is None
    ):
        raise ValueError("successor lacks required transition lineage")
    transition_ref = ProcessStateTransitionId(transition_id)
    transition_provenance = ProcessStateTransitionProvenance(
        predecessor.ref,
        successor.ref,
        provenance.artifact_transition_ref_or_none,
        provenance.action_application_ref_or_none,
        provenance.reassessment_ref_or_none,
        provenance.comparison_refs,
    )
    return ProcessStateTransition(
        transition_ref,
        predecessor.ref,
        successor.ref,
        provenance.artifact_transition_ref_or_none,
        provenance.action_application_ref_or_none,
        provenance.reassessment_ref_or_none,
        provenance.comparison_refs,
        PROCESS_RULE_REF,
        transition_provenance,
    )


__all__ = [
    "ProcessStateAssembly",
    "assemble_process_state",
    "assemble_process_transition",
]

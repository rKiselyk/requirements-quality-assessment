"""M3-09 orchestration for rebuilding a child artifact from current content."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from ..assessor import RequirementQualityAssessor
from ..corrective_action import RequirementLineageId, SpecificationVersion
from ..cross_analysis import (
    ComparisonKey,
    CrossObservationRef,
    SpecificationAssessmentService,
)
from ..cross_analysis.specification import SpecificationAssessmentResult
from ..defect_quality import (
    DefectConstructionContext,
    DefectPopulationSnapshot,
    DefectQualityRelation,
    DefectQualityRelationContext,
    ProblemClaimResolution,
    TypedProblemClaimSource,
    build_defect_population,
    relate_problem_to_quality,
    resolve_problem_claim,
)
from ..domain import Requirement, RequirementAssessmentRecord
from ..dynamic_evidence import (
    Applicability,
    ConformanceAssessment,
    ConformanceEvaluationContext,
    CriterionBindingContext,
    CriterionBindingResult,
    DynamicEvidenceAssessmentRef,
    DynamicObservation,
    FullModelStatus,
    ObservationResolution,
    ObservationSlotRef,
    assess_conformance,
    bind_quantitative_criterion,
    resolve_dynamic_observation,
)
from ..dynamic_evidence.domain import DynamicObservationRef
from ..extractor import BaselineFeatureExtractor
from ..metrics import ArtifactRef, MetricConstructionContext, MetricProfile, MetricProfileBuilder
from ..performance_efficiency import (
    PerformanceEfficiencyFeatureConstructionContext,
    PerformanceEfficiencyFeatureProfile,
    PerformanceEfficiencyFeatureProfileBuilder,
    ProcessStage,
    ProcessStateRef,
)
from ..product_quality import (
    MODEL_REF,
    PARAMETER_SET_REF,
    ProductQualityAssessment,
    ProductQualityAssessmentContext,
    ProductQualityAssessmentEventRef,
    assess_product_quality,
)
from ..risk import (
    BoundedRiskAssessment,
    RiskAssessmentContext,
    RiskAssessmentEventRef,
    assess_risk,
)
from .domain import (
    REASSESSMENT_RULE_REF,
    AssessmentResultRef,
    ComparisonRequestRef,
    EvidenceReuseDecision,
    EvidenceReuseDisposition,
    ReassessmentContext,
    ReassessmentProvenance,
    ReassessmentReason,
    ReassessmentRef,
    ReassessmentRun,
    _identifier,
)


@dataclass(frozen=True, slots=True)
class CoreReassessmentResults:
    specification_version: SpecificationVersion
    requirement_records: tuple[RequirementAssessmentRecord, ...]
    specification_assessment: SpecificationAssessmentResult
    metric_profile: MetricProfile

    def __post_init__(self) -> None:
        child_ref = self.specification_version.artifact_ref
        if self.metric_profile.artifact_ref != child_ref:
            raise ValueError("metric profile must identify the reassessed child artifact")
        if self.metric_profile.source_snapshot_id != self.specification_assessment.projection.snapshot_id:
            raise ValueError("metric profile must preserve the rebuilt child snapshot")


class DynamicObservationUse(str, Enum):
    CURRENT_VERSION_EVIDENCE = "CURRENT_VERSION_EVIDENCE"
    EXPLICIT_REUSE = "EXPLICIT_REUSE"


_REQUIRED_REUSE_CHECKS = (
    "product_ref",
    "observation_source_kind",
    "collection_ref",
    "metric_ref",
    "unit",
    "context_identity",
    "applicability",
    "process_stage",
    "source_contract_permission",
)


@dataclass(frozen=True, slots=True)
class ReferenceFullModelReassessmentInputs:
    selected_criterion_lineage: RequirementLineageId
    selected_observation_ref: CrossObservationRef
    observation_slot_ref: ObservationSlotRef
    observation_or_none: DynamicObservation | None
    observation_use: DynamicObservationUse
    observation_reuse_decision_or_none: EvidenceReuseDecision | None
    dynamic_assessment_ref: DynamicEvidenceAssessmentRef
    product_quality_event_ref: ProductQualityAssessmentEventRef
    risk_event_ref: RiskAssessmentEventRef
    target_lineages: tuple[RequirementLineageId, RequirementLineageId]
    target_comparison_key: ComparisonKey

    def __post_init__(self) -> None:
        if not isinstance(self.selected_criterion_lineage, RequirementLineageId):
            raise TypeError("selected_criterion_lineage must be a RequirementLineageId")
        if not isinstance(self.selected_observation_ref, CrossObservationRef):
            raise TypeError("selected_observation_ref must be a CrossObservationRef")
        if not isinstance(self.observation_slot_ref, ObservationSlotRef):
            raise TypeError("observation_slot_ref must be an ObservationSlotRef")
        if self.observation_or_none is not None and (
            self.observation_or_none.slot_ref != self.observation_slot_ref
        ):
            raise ValueError("observation must occupy the supplied slot")
        if not isinstance(self.observation_use, DynamicObservationUse):
            raise TypeError("observation_use must be a DynamicObservationUse")
        if self.observation_use is DynamicObservationUse.EXPLICIT_REUSE:
            if (
                self.observation_or_none is None
                or self.observation_reuse_decision_or_none is None
            ):
                raise ValueError("explicit observation reuse requires evidence and a decision")
        elif self.observation_reuse_decision_or_none is not None:
            raise ValueError("current-version evidence cannot carry a reuse decision")
        if not isinstance(self.dynamic_assessment_ref, DynamicEvidenceAssessmentRef):
            raise TypeError("dynamic_assessment_ref must be a DynamicEvidenceAssessmentRef")
        if not isinstance(
            self.product_quality_event_ref, ProductQualityAssessmentEventRef
        ):
            raise TypeError(
                "product_quality_event_ref must be a ProductQualityAssessmentEventRef"
            )
        if not isinstance(self.risk_event_ref, RiskAssessmentEventRef):
            raise TypeError("risk_event_ref must be a RiskAssessmentEventRef")
        if (
            not isinstance(self.target_lineages, tuple)
            or len(self.target_lineages) != 2
            or any(
                not isinstance(item, RequirementLineageId)
                for item in self.target_lineages
            )
            or len(set(self.target_lineages)) != 2
        ):
            raise ValueError("target_lineages requires two distinct lineage IDs")
        if not isinstance(self.target_comparison_key, ComparisonKey):
            raise TypeError("target_comparison_key must be a ComparisonKey")


@dataclass(frozen=True, slots=True)
class FullModelDownstreamRecords:
    artifact_ref: ArtifactRef
    criterion_binding: CriterionBindingResult
    observation_resolution: ObservationResolution
    conformance: ConformanceAssessment
    feature_profile: PerformanceEfficiencyFeatureProfile
    product_quality_assessment: ProductQualityAssessment
    problem_resolutions: tuple[ProblemClaimResolution, ...]
    defect_population: DefectPopulationSnapshot
    target_problem_resolution: ProblemClaimResolution
    defect_quality_relation: DefectQualityRelation
    risk_assessment: BoundedRiskAssessment

    def __post_init__(self) -> None:
        if self.criterion_binding.binding_id.artifact_ref != self.artifact_ref:
            raise ValueError("criterion binding must identify the child artifact")
        if self.conformance.dynamic_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("conformance must identify the child artifact")
        if self.feature_profile.artifact_ref != self.artifact_ref:
            raise ValueError("feature profile must identify the child artifact")
        if self.product_quality_assessment.artifact_ref != self.artifact_ref:
            raise ValueError("product-quality result must identify the child artifact")
        if any(item.artifact_ref != self.artifact_ref for item in self.problem_resolutions):
            raise ValueError("problem resolutions must identify the child artifact")
        if self.defect_population.artifact_ref != self.artifact_ref:
            raise ValueError("defect population must identify the child artifact")
        if self.defect_quality_relation.artifact_ref != self.artifact_ref:
            raise ValueError("defect relation must identify the child artifact")
        if self.risk_assessment.artifact_ref != self.artifact_ref:
            raise ValueError("risk result must identify the child artifact")


@dataclass(frozen=True, slots=True)
class DownstreamReassessmentResults:
    results: tuple[object, ...]
    result_refs: tuple[AssessmentResultRef, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.results, tuple) or not isinstance(self.result_refs, tuple):
            raise TypeError("downstream results and refs must be tuples")
        if len(self.results) != len(self.result_refs):
            raise ValueError("every downstream result requires one reference")
        if not self.results:
            raise ValueError(
                "the full-model downstream path must return typed component results"
            )


class DownstreamRebuilder(Protocol):
    def __call__(
        self,
        core: CoreReassessmentResults,
        context: ReassessmentContext,
        child_process_state_ref: ProcessStateRef,
    ) -> DownstreamReassessmentResults: ...


@dataclass(frozen=True, slots=True)
class ReassessmentIdentityContext:
    reassessment_id: str
    reassessment_version: str
    child_process_state_ref: ProcessStateRef

    def __post_init__(self) -> None:
        _identifier(self.reassessment_id, "reassessment_id")
        _identifier(self.reassessment_version, "reassessment_version")
        if self.child_process_state_ref.stage is not ProcessStage.REFERENCE_VERIFICATION:
            raise ValueError("child process state must use REFERENCE_VERIFICATION")


@dataclass(frozen=True, slots=True)
class ReassessmentServices:
    extractor: object
    requirement_assessor: object
    specification_assessor: object
    metric_builder: object

    @classmethod
    def approved_defaults(cls) -> "ReassessmentServices":
        return cls(
            BaselineFeatureExtractor(),
            RequirementQualityAssessor(),
            SpecificationAssessmentService(),
            MetricProfileBuilder(),
        )


class ReferenceFullModelDownstreamRebuilder:
    """Invoke the approved dynamic, feature, quality, defect, relation, and risk services."""

    def __init__(self, inputs: ReferenceFullModelReassessmentInputs) -> None:
        if not isinstance(inputs, ReferenceFullModelReassessmentInputs):
            raise TypeError("inputs must be ReferenceFullModelReassessmentInputs")
        self._inputs = inputs

    def _validate_context(
        self,
        core: CoreReassessmentResults,
        context: ReassessmentContext,
        child_process_state_ref: ProcessStateRef,
    ) -> None:
        inputs = self._inputs
        child_ref = context.child_artifact_ref
        if inputs.dynamic_assessment_ref.artifact_ref != child_ref:
            raise ValueError("dynamic assessment must identify the child artifact")
        if (
            inputs.dynamic_assessment_ref.collection_ref
            != inputs.observation_slot_ref.collection_ref
        ):
            raise ValueError("dynamic assessment and observation slot must share a collection")
        if inputs.product_quality_event_ref.artifact_ref != child_ref:
            raise ValueError("product-quality event must identify the child artifact")
        if (
            inputs.product_quality_event_ref.product_ref
            != inputs.dynamic_assessment_ref.product_ref
        ):
            raise ValueError("product-quality event and dynamic evidence must share a product")
        if inputs.risk_event_ref.artifact_ref != child_ref:
            raise ValueError("risk event must identify the child artifact")
        if inputs.risk_event_ref.process_state_ref != child_process_state_ref:
            raise ValueError("risk event must identify the child process state")
        lineages = tuple(item.lineage_id for item in core.specification_version.requirements)
        if inputs.selected_criterion_lineage not in lineages:
            raise ValueError("selected criterion lineage is absent from the child")
        if any(item not in lineages for item in inputs.target_lineages):
            raise ValueError("action target lineage is absent from the child")
        selected = next(
            item
            for item in core.specification_version.requirements
            if item.lineage_id == inputs.selected_criterion_lineage
        )
        if inputs.selected_observation_ref.requirement_id != selected.subject_ref.requirement_id:
            raise ValueError("selected observation does not belong to the criterion lineage")

        if inputs.observation_use is DynamicObservationUse.EXPLICIT_REUSE:
            decision = inputs.observation_reuse_decision_or_none
            observation = inputs.observation_or_none
            if decision not in context.evidence_reuse_decisions:
                raise ValueError("observation reuse decision is absent from reassessment context")
            if decision.decision is not EvidenceReuseDisposition.REUSE_ALLOWED:
                raise ValueError("observation reuse was not allowed")
            if decision.source_evidence_ref != DynamicObservationRef(
                observation.observation_id
            ):
                raise ValueError("reuse decision references the wrong observation")
            checks = {item.field_name: item for item in decision.exact_identity_checks}
            if tuple(checks) != _REQUIRED_REUSE_CHECKS:
                raise ValueError("reuse decision does not contain the exact required checks")
            expected_values = {
                "product_ref": observation.product_ref,
                "observation_source_kind": observation.source_kind,
                "collection_ref": observation.collection_ref,
                "metric_ref": observation.metric_ref,
                "unit": observation.unit,
                "context_identity": observation.context_identity,
                "applicability": Applicability.APPLICABLE,
                "process_stage": child_process_state_ref.stage,
                "source_contract_permission": True,
            }
            if any(
                not item.matches
                or item.expected != expected_values[name]
                or item.actual != expected_values[name]
                for name, item in checks.items()
            ):
                raise ValueError("observation reuse exact identity/context check failed")

    def __call__(
        self,
        core: CoreReassessmentResults,
        context: ReassessmentContext,
        child_process_state_ref: ProcessStateRef,
    ) -> DownstreamReassessmentResults:
        self._validate_context(core, context, child_process_state_ref)
        inputs = self._inputs
        specification = core.specification_version
        selected = next(
            item
            for item in specification.requirements
            if item.lineage_id == inputs.selected_criterion_lineage
        )
        selected_record = next(
            item
            for item in core.requirement_records
            if item.extraction_result.requirement.id
            == selected.subject_ref.requirement_id
        )
        binding = bind_quantitative_criterion(
            selected_record.extraction_result,
            inputs.selected_observation_ref,
            CriterionBindingContext(
                context.child_artifact_ref,
                context.child_assessment_ref,
                core.specification_assessment.snapshot_id,
            ),
        )
        observation_resolution = resolve_dynamic_observation(
            inputs.observation_slot_ref,
            inputs.observation_or_none,
        )
        conformance = assess_conformance(
            binding,
            observation_resolution,
            ConformanceEvaluationContext(inputs.dynamic_assessment_ref),
        )
        feature_context = PerformanceEfficiencyFeatureConstructionContext(
            context.child_artifact_ref,
            context.child_assessment_ref,
            core.metric_profile.profile_id,
            inputs.dynamic_assessment_ref,
            inputs.dynamic_assessment_ref.product_ref,
            child_process_state_ref,
        )
        feature_profile = PerformanceEfficiencyFeatureProfileBuilder().build(
            core.metric_profile,
            core.specification_assessment,
            binding,
            observation_resolution,
            conformance,
            feature_context,
        )
        product_quality = assess_product_quality(
            feature_profile,
            MODEL_REF,
            PARAMETER_SET_REF,
            ProductQualityAssessmentContext(
                inputs.product_quality_event_ref,
                context.child_artifact_ref,
                context.child_assessment_ref,
                feature_profile.profile_id,
                inputs.dynamic_assessment_ref.product_ref,
                child_process_state_ref,
            ),
        )

        construction_context = DefectConstructionContext(
            context.child_artifact_ref,
            context.child_assessment_ref,
            core.specification_assessment.snapshot_id,
            child_process_state_ref,
        )
        relation_context = DefectQualityRelationContext(
            context.child_artifact_ref,
            context.child_assessment_ref,
            core.specification_assessment.snapshot_id,
            child_process_state_ref,
        )
        resolutions = tuple(
            resolve_problem_claim(
                TypedProblemClaimSource.from_qb_result(
                    item,
                    core.specification_assessment.projection.snapshot,
                ),
                construction_context,
            )
            for item in core.specification_assessment.cross_results
        )
        population = build_defect_population(
            resolutions,
            core.specification_assessment.specification_assessment.qb_consistency,
            construction_context,
        )
        target_ids = tuple(
            next(
                item.subject_ref.requirement_id
                for item in specification.requirements
                if item.lineage_id == lineage
            )
            for lineage in inputs.target_lineages
        )
        target_pairs = tuple(
            (result, resolution)
            for result, resolution in zip(
                core.specification_assessment.cross_results,
                resolutions,
                strict=True,
            )
            if tuple(item.requirement_id for item in result.observation_refs)
            == target_ids
            and result.comparison_key == inputs.target_comparison_key
        )
        if len(target_pairs) != 1:
            raise ValueError("the exact action lineage/key scope must resolve once in v2")
        target_resolution = target_pairs[0][1]
        relation = relate_problem_to_quality(target_resolution, relation_context)
        risk = assess_risk(
            target_resolution,
            population,
            relation,
            product_quality,
            RiskAssessmentContext(
                inputs.risk_event_ref,
                context.child_artifact_ref,
                context.child_assessment_ref,
                core.specification_assessment.snapshot_id,
                child_process_state_ref,
            ),
        )
        records = FullModelDownstreamRecords(
            context.child_artifact_ref,
            binding,
            observation_resolution,
            conformance,
            feature_profile,
            product_quality,
            resolutions,
            population,
            target_resolution,
            relation,
            risk,
        )
        return DownstreamReassessmentResults(
            (records,),
            (
                AssessmentResultRef(
                    "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH",
                    risk.risk_assessment_id,
                    context.child_artifact_ref,
                ),
            ),
        )


def _rebuild_core(
    specification: SpecificationVersion,
    context: ReassessmentContext,
    services: ReassessmentServices,
) -> CoreReassessmentResults:
    requirements = tuple(
        Requirement(
            item.subject_ref.requirement_id,
            item.subject_ref.source_line,
            item.text,
        )
        for item in specification.requirements
    )
    records = tuple(
        services.requirement_assessor.assess_record(
            services.extractor.extract(requirement)
        )
        for requirement in requirements
    )
    specification_assessment = services.specification_assessor.assess(records)
    metric_profile = services.metric_builder.build(
        specification_assessment,
        MetricConstructionContext(
            context.child_artifact_ref,
            context.child_assessment_ref,
        ),
    )
    return CoreReassessmentResults(
        specification,
        records,
        specification_assessment,
        metric_profile,
    )


def reevaluate(
    specification: SpecificationVersion,
    context: ReassessmentContext,
    identity: ReassessmentIdentityContext,
    downstream_rebuilder: DownstreamRebuilder,
    *,
    services: ReassessmentServices | None = None,
    comparison_request_refs: tuple[ComparisonRequestRef, ...] = (),
) -> ReassessmentRun:
    """Rebuild v2; no v1 assessment value is an input to this operation.

    The fixed local/QB/Metric-Profile path is invoked directly through existing
    services.  The dynamic-evidence through risk portion is supplied as an
    orchestration callback because its external observation, selected
    criterion, product, collection, and environment contexts are deliberately
    caller-owned.  That callback must use the existing approved services and
    return typed child-version records; this boundary only sequences and
    validates them.
    """

    if not isinstance(specification, SpecificationVersion):
        raise TypeError("specification must be a SpecificationVersion")
    if not isinstance(context, ReassessmentContext):
        raise TypeError("context must be a ReassessmentContext")
    if not isinstance(identity, ReassessmentIdentityContext):
        raise TypeError("identity must be a ReassessmentIdentityContext")
    if not callable(downstream_rebuilder):
        raise TypeError("downstream_rebuilder must be callable")
    if specification.artifact_ref != context.child_artifact_ref:
        raise ValueError("reassessment must consume the exact child artifact")
    if specification.parent_artifact_ref != context.parent_artifact_ref:
        raise ValueError("reassessment parent identity does not match the child")
    if specification.created_by_application_ref != context.action_application_ref:
        raise ValueError("reassessment must preserve the action application link")
    if identity.child_process_state_ref == context.predecessor_process_state_ref:
        raise ValueError("child process-state identity must be distinct")
    if (
        identity.child_process_state_ref.process_state_id
        != context.predecessor_process_state_ref.process_state_id
    ):
        raise ValueError("reassessment must preserve process lineage identity")
    if any(
        item.target_process_state_ref != identity.child_process_state_ref
        for item in context.evidence_reuse_decisions
    ):
        raise ValueError("evidence reuse decisions must target the child process state")
    if not isinstance(comparison_request_refs, tuple) or any(
        not isinstance(item, ComparisonRequestRef) for item in comparison_request_refs
    ):
        raise TypeError("comparison_request_refs must be ComparisonRequestRef values")

    selected_services = services or ReassessmentServices.approved_defaults()
    core = _rebuild_core(specification, context, selected_services)
    downstream = downstream_rebuilder(
        core,
        context,
        identity.child_process_state_ref,
    )
    if not isinstance(downstream, DownstreamReassessmentResults):
        raise TypeError("downstream_rebuilder must return DownstreamReassessmentResults")
    if any(
        item.artifact_ref != context.child_artifact_ref
        for item in downstream.result_refs
    ):
        raise ValueError("downstream reassessment results cannot reuse v1 artifact refs")
    for result in downstream.results:
        artifact_ref = getattr(result, "artifact_ref", None)
        if artifact_ref is None:
            raise ValueError(
                "every downstream typed result must expose its child artifact_ref"
            )
        if artifact_ref != context.child_artifact_ref:
            raise ValueError(
                "downstream reassessment results cannot inherit v1 artifact values"
            )

    core_ref = AssessmentResultRef(
        "CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH",
        context.child_assessment_ref,
        context.child_artifact_ref,
    )
    produced_results = (core, *downstream.results)
    produced_refs = (core_ref, *downstream.result_refs)
    reassessment_ref = ReassessmentRef(
        identity.reassessment_id,
        identity.reassessment_version,
    )
    provenance = ReassessmentProvenance(
        reassessment_ref=reassessment_ref,
        action_application_ref=context.action_application_ref,
        predecessor_process_state_ref=context.predecessor_process_state_ref,
        child_process_state_ref=identity.child_process_state_ref,
        parent_artifact_ref=context.parent_artifact_ref,
        child_artifact_ref=context.child_artifact_ref,
        child_assessment_ref=context.child_assessment_ref,
        produced_result_refs=produced_refs,
        component_version_set=context.component_version_set,
        evidence_reuse_decisions=context.evidence_reuse_decisions,
        full_model_contract_ref=context.full_model_contract_ref,
    )
    return ReassessmentRun(
        reassessment_id=identity.reassessment_id,
        reassessment_version=identity.reassessment_version,
        context=context,
        status=FullModelStatus.AVAILABLE,
        child_process_state_ref=identity.child_process_state_ref,
        produced_result_refs=produced_refs,
        comparison_request_refs=comparison_request_refs,
        reason_codes=(ReassessmentReason.FULL_MODEL_PATH_REBUILT,),
        rule_ref=REASSESSMENT_RULE_REF,
        provenance=provenance,
        produced_results=produced_results,
    )


__all__ = [
    "CoreReassessmentResults",
    "DownstreamReassessmentResults",
    "DownstreamRebuilder",
    "DynamicObservationUse",
    "FullModelDownstreamRecords",
    "ReferenceFullModelDownstreamRebuilder",
    "ReferenceFullModelReassessmentInputs",
    "ReassessmentIdentityContext",
    "ReassessmentServices",
    "reevaluate",
]

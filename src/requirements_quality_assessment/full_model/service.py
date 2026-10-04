"""Canonical application orchestration for the approved Full Model path.

This module connects accepted services.  It contains no scoring, prediction,
risk multiplication, checkpoint predicate, or defect-classification rule.
"""

from __future__ import annotations

from enum import Enum

from ..assessor import RequirementQualityAssessor
from ..checkpoint import CheckpointRequest, evaluate_checkpoint, select_metric_result
from ..corrective_action import (
    ACTION_RECORD_VERSION, ACTION_RULE_REF, ExternalRevisionProvenance,
    ExternallySuppliedRevision, RequirementTextReplacement,
    apply_external_revision, create_initial_specification_version,
    propose_corrective_action, CorrectiveActionContext,
)
from ..cross_analysis import SpecificationAssessmentService
from ..defect_quality import (
    DEFECT_QUALITY_RISK_CONTRACT_REF, PROBLEM_RULE_REF, RELATION_RULE_REF,
    DefectConstructionContext, DefectQualityRelationContext,
    TypedProblemClaimSource, build_defect_population, relate_problem_to_quality,
    resolve_problem_claim,
)
from ..dynamic_evidence import (
    BINDING_RULE_REF, DYNAMIC_CONTRACT_REF, EVALUATOR_RULE_REF,
    RESPONSE_TIME_METRIC_REF, Applicability, ConformanceEvaluationContext,
    CriterionBindingContext, FullModelStatus, ObservationSlotRef,
    assess_conformance, bind_quantitative_criterion, make_dynamic_observation,
    resolve_dynamic_observation,
)
from ..dynamic_evidence.domain import DynamicObservationRef
from ..extractor import BaselineFeatureExtractor
from ..full_model_reporter import FullModelReportBundle
from ..full_quality import compose_full_requirement_quality_profile
from ..metrics import (
    FULL_MODEL_CONTRACT_REF, MetricConstructionContext, MetricId,
    MetricProfileBuilder, RequirementSubjectRef,
)
from ..performance_efficiency import (
    FEATURE_CONTRACT_REF, PerformanceEfficiencyFeatureConstructionContext,
    PerformanceEfficiencyFeatureProfileBuilder, ProcessStage,
)
from ..process import (
    ProcessComponentAssociation, ProcessComponentRole,
    ProcessEvidenceAssociation, ProcessEvidenceRole, ProcessStateAssembly,
    RequirementAssessmentRef, SpecificationAssessmentRef,
    assemble_process_state, assemble_process_transition,
)
from ..product_quality import (
    ASSESSMENT_CONTRACT_REF, MODEL_REF, PARAMETER_SET_REF, PROCEDURE_RULE_REF,
    ProductQualityAssessmentContext, assess_product_quality,
)
from ..product_quality_prediction import (
    PerformanceEfficiencyPredictionRequest, predict_performance_efficiency,
)
from ..quantitative_risk import (
    QUANTITATIVE_RISK_CONTRACT_REF, QuantitativeRiskCalculationContext,
    QuantitativeRiskCalculationRequest, QuantitativeRiskOperand,
    QuantitativeRiskOperandId, QuantitativeRiskOperandKind,
    QuantitativeRiskOperandProvenance, calculate_quantitative_local_risk,
)
from ..reassessment import (
    AssessmentResultRef, ComparableResult, ComparisonRequest,
    ComparisonResultFamily, ComparisonSubject, ComparisonValueKind,
    DynamicObservationUse, EvidenceReuseDecision, EvidenceReuseProvenance,
    ReferenceFullModelDownstreamRebuilder,
    ReferenceFullModelReassessmentInputs, ReassessmentContext, compare,
    reevaluate,
)
from ..risk import (
    RISK_MODEL_REF, RISK_PARAMETER_SET_REF, RISK_RULE_REF,
    RiskAssessmentContext, assess_risk,
)
from .domain import FullModelRequest, FullModelResult, FullModelServiceReportBundle


class _AssemblyReason(str, Enum):
    NO_CONFIRMED_PROBLEM = "NO_CONFIRMED_PROBLEM"


def _available_component(role, result_ref, scope, producing_ref=FULL_MODEL_CONTRACT_REF):
    return ProcessComponentAssociation(
        role, result_ref, FullModelStatus.AVAILABLE, Applicability.APPLICABLE,
        scope, producing_ref, (), (result_ref,),
    )


def _evidence_associations(artifact, product, source, binding, observation, conformance, *, reuse=None):
    values = (
        (ProcessEvidenceRole.STATIC_REQUIREMENT,
         tuple(record.extraction_result.evidence for record in source.records),
         artifact, source.snapshot_id, None),
        (ProcessEvidenceRole.QB, tuple(item.result_id for item in source.cross_results),
         artifact, source.snapshot_id, None),
        (ProcessEvidenceRole.DYNAMIC_CRITERION, binding.binding_id, artifact,
         binding.provenance.requirement_subject_ref, None),
        (ProcessEvidenceRole.DYNAMIC_OBSERVATION,
         DynamicObservationRef(observation.observation_id), product,
         observation.collection_ref, reuse),
        (ProcessEvidenceRole.CONFORMANCE, conformance.conformance_id, artifact,
         conformance.dynamic_assessment_ref, None),
    )
    return tuple(
        ProcessEvidenceAssociation(
            role, evidence_ref, FullModelStatus.AVAILABLE, Applicability.APPLICABLE,
            subject, source_ref,
            observation.context_identity if role is not ProcessEvidenceRole.STATIC_REQUIREMENT else None,
            reuse_ref, (), (evidence_ref, source_ref),
        )
        for role, evidence_ref, subject, source_ref, reuse_ref in values
    )


def _requirement_and_specification_refs(source, artifact, assessment):
    requirement_refs = tuple(
        RequirementAssessmentRef(
            assessment,
            RequirementSubjectRef(artifact, record.extraction_result.requirement.id,
                                  record.extraction_result.requirement.source_line),
        )
        for record in source.records
    )
    return requirement_refs, SpecificationAssessmentRef(assessment, source.snapshot_id)


def _component_associations(source, artifact, assessment, metric, feature, quality,
                            population, problem, relation, risk, action_ref):
    requirement_refs, specification_ref = _requirement_and_specification_refs(
        source, artifact, assessment
    )
    if problem is None:
        problem_association = ProcessComponentAssociation(
            ProcessComponentRole.CONFIRMED_PROBLEM, None,
            FullModelStatus.NOT_APPLICABLE, Applicability.NOT_APPLICABLE,
            artifact, PROBLEM_RULE_REF, (_AssemblyReason.NO_CONFIRMED_PROBLEM,),
            (artifact,),
        )
    else:
        problem_association = _available_component(
            ProcessComponentRole.CONFIRMED_PROBLEM, problem.ref, artifact,
            PROBLEM_RULE_REF,
        )
    return (
        (
            *(_available_component(ProcessComponentRole.REQUIREMENT_ASSESSMENT,
                                   item, item.requirement_subject_ref)
              for item in requirement_refs),
            _available_component(ProcessComponentRole.SPECIFICATION_ASSESSMENT,
                                 specification_ref, artifact),
            _available_component(ProcessComponentRole.METRIC_PROFILE,
                                 metric.profile_id, artifact),
            ProcessComponentAssociation(ProcessComponentRole.PE_FEATURE_PROFILE,
                feature.profile_id, feature.status, feature.applicability,
                feature.product_ref, FEATURE_CONTRACT_REF, (), (feature.profile_id,)),
            ProcessComponentAssociation(ProcessComponentRole.PRODUCT_QUALITY_ASSESSMENT,
                risk.product_quality_context.assessment_ref, quality.status,
                quality.applicability, quality.product_ref, ASSESSMENT_CONTRACT_REF,
                (), (risk.product_quality_context.assessment_ref,)),
            _available_component(ProcessComponentRole.DEFECT_POPULATION,
                                 population.ref, artifact,
                                 DEFECT_QUALITY_RISK_CONTRACT_REF),
            problem_association,
            ProcessComponentAssociation(ProcessComponentRole.DEFECT_QUALITY_RELATION,
                relation.ref, relation.status, relation.applicability, artifact,
                RELATION_RULE_REF, relation.reasons, (relation.ref,)),
            ProcessComponentAssociation(ProcessComponentRole.BOUNDED_RISK_ASSESSMENT,
                risk.ref, risk.status, risk.applicability, artifact, RISK_RULE_REF,
                (), (risk.ref,)),
            _available_component(ProcessComponentRole.CORRECTIVE_ACTION,
                                 action_ref, artifact, ACTION_RULE_REF),
        ), requirement_refs, specification_ref,
    )


def _comparable(artifact, subject, identity, *, status, applicability, value_kind,
                exact_value=None, categorical_state=None, rules=(), models=(),
                parameters=(), calibration=None):
    return ComparableResult(
        AssessmentResultRef("FULL-MODEL-SERVICE-COMPARABLE", identity, artifact),
        subject, value_kind, status, applicability, exact_value, categorical_state,
        "EXACT_FRACTION" if value_kind is ComparisonValueKind.EXACT_FRACTION else None,
        ProcessStage.REFERENCE_VERIFICATION, rules, models, parameters,
        FULL_MODEL_CONTRACT_REF, calibration,
    )


class FullModelService:
    """Execute the supported Full Model research path in one public call."""

    def run(self, request: FullModelRequest) -> FullModelResult:
        if not isinstance(request, FullModelRequest):
            raise TypeError("request must be a FullModelRequest")
        self._validate_request(request)
        extractor = BaselineFeatureExtractor()
        assessor = RequirementQualityAssessor()
        records_v1 = tuple(assessor.assess_record(extractor.extract(item))
                           for item in request.requirements)
        source_v1 = SpecificationAssessmentService().assess(records_v1)
        metric_v1 = MetricProfileBuilder().build(
            source_v1, MetricConstructionContext(request.artifact_v1, request.assessment_v1)
        )
        parent = create_initial_specification_version(request.artifact_v1, request.requirements)
        selected_record = next(
            (record for record in records_v1
             if record.extraction_result.requirement.id == request.selected_requirement_id),
            None,
        )
        if selected_record is None:
            raise ValueError("selected_requirement_id is absent from requirements")
        binding_v1 = bind_quantitative_criterion(
            selected_record.extraction_result, request.selected_observation_ref,
            CriterionBindingContext(request.artifact_v1, request.assessment_v1,
                                    source_v1.snapshot_id),
        )
        slot = ObservationSlotRef(request.collection_ref, request.observation_slot_index)
        observation = make_dynamic_observation(
            slot, RESPONSE_TIME_METRIC_REF, request.observed_value,
            request.observation_unit, request.criterion_context, request.observation_id,
        )
        observation_resolution_v1 = resolve_dynamic_observation(slot, observation)
        conformance_v1 = assess_conformance(
            binding_v1, observation_resolution_v1,
            ConformanceEvaluationContext(request.dynamic_assessment_v1),
        )
        feature_v1 = PerformanceEfficiencyFeatureProfileBuilder().build(
            metric_v1, source_v1, binding_v1, observation_resolution_v1,
            conformance_v1,
            PerformanceEfficiencyFeatureConstructionContext(
                request.artifact_v1, request.assessment_v1, metric_v1.profile_id,
                request.dynamic_assessment_v1, request.product_ref,
                request.process_ref_v1,
            ),
        )
        quality_v1 = assess_product_quality(
            feature_v1, MODEL_REF, PARAMETER_SET_REF,
            ProductQualityAssessmentContext(
                request.product_quality_event_v1, request.artifact_v1,
                request.assessment_v1, feature_v1.profile_id, request.product_ref,
                request.process_ref_v1,
            ),
        )
        construction_v1 = DefectConstructionContext(
            request.artifact_v1, request.assessment_v1, source_v1.snapshot_id,
            request.process_ref_v1,
        )
        relation_context_v1 = DefectQualityRelationContext(
            request.artifact_v1, request.assessment_v1, source_v1.snapshot_id,
            request.process_ref_v1,
        )
        resolutions_v1 = tuple(
            resolve_problem_claim(
                TypedProblemClaimSource.from_qb_result(result, source_v1.projection.snapshot),
                construction_v1,
            ) for result in source_v1.cross_results
        )
        population_v1 = build_defect_population(
            resolutions_v1, source_v1.specification_assessment.qb_consistency,
            construction_v1,
        )
        problem_resolution_v1 = next((item for item in resolutions_v1 if item.problem is not None), None)
        if problem_resolution_v1 is None:
            raise ValueError("supported full-model path requires a confirmed QB problem")
        problem_v1 = problem_resolution_v1.problem
        relation_v1 = relate_problem_to_quality(problem_resolution_v1, relation_context_v1)
        risk_v1 = assess_risk(
            problem_resolution_v1, population_v1, relation_v1, quality_v1,
            RiskAssessmentContext(
                request.risk_event_v1, request.artifact_v1, request.assessment_v1,
                source_v1.snapshot_id, request.process_ref_v1,
            ),
        )
        action_resolution = propose_corrective_action(
            risk_v1, problem_v1, relation_v1,
            CorrectiveActionContext(
                request.action_id, ACTION_RECORD_VERSION, request.action_creator,
                request.artifact_v1, tuple(item.lineage_id for item in parent.requirements),
                request.assessment_v1, source_v1.snapshot_id, request.process_ref_v1,
            ),
        )
        action = action_resolution.action
        if action is None:
            raise ValueError("supported full-model path did not produce a corrective action")

        by_id = {item.subject_ref.requirement_id: item for item in parent.requirements}
        replacements = tuple(
            RequirementTextReplacement(by_id[item.requirement_id].lineage_id,
                                       by_id[item.requirement_id].subject_ref,
                                       item.replacement_text)
            for item in request.revision.replacements
        )
        revision_ref = request.revision.revision_ref
        revision = ExternallySuppliedRevision(
            revision_ref.revision_id, revision_ref.revision_version,
            request.revision.provider_kind, request.revision.provider_ref,
            action.ref, request.artifact_v1, request.revision.child_artifact_ref,
            replacements, request.revision.reason,
            ExternalRevisionProvenance(
                revision_ref, action.ref, request.artifact_v1,
                request.revision.child_artifact_ref, request.revision.provider_ref,
            ),
        )
        application = apply_external_revision(
            action, revision, parent, request.revision.application_identity
        )
        child = application.child_specification
        reuse = EvidenceReuseDecision(
            DynamicObservationRef(observation.observation_id), request.process_ref_v2,
            request.reuse.disposition, request.reuse.identity_checks,
            request.reuse.reasons,
            EvidenceReuseProvenance(request.process_ref_v1, request.process_ref_v2,
                                    DYNAMIC_CONTRACT_REF),
        )
        reassessment_context = ReassessmentContext(
            request.process_ref_v1, application.ref, request.artifact_v1,
            request.revision.child_artifact_ref, request.assessment_v2,
            FULL_MODEL_CONTRACT_REF, request.component_versions, (reuse,),
            ProcessStage.REFERENCE_VERIFICATION,
        )
        downstream_inputs = ReferenceFullModelReassessmentInputs(
            by_id[request.selected_requirement_id].lineage_id,
            request.selected_observation_ref, slot, observation,
            DynamicObservationUse.EXPLICIT_REUSE, reuse,
            request.dynamic_assessment_v2, request.product_quality_event_v2,
            request.risk_event_v2,
            tuple(item.lineage_id for item in action.target_requirements),
            action.comparison_key,
        )
        reassessment = reevaluate(
            child, reassessment_context, request.reassessment_identity,
            ReferenceFullModelDownstreamRebuilder(downstream_inputs),
        )
        core_v2, downstream_v2 = reassessment.produced_results
        comparisons = self._comparisons(
            request, parent, observation, action, application, metric_v1,
            problem_resolution_v1, risk_v1, quality_v1, core_v2, downstream_v2,
        )
        process_v1, process_v2 = self._process_states(
            request, source_v1, metric_v1, binding_v1, observation,
            conformance_v1, feature_v1, quality_v1, population_v1, problem_v1,
            relation_v1, risk_v1, action, application, reassessment, reuse,
            comparisons, core_v2, downstream_v2,
        )
        process_transition = assemble_process_transition(
            request.process_transition_id, process_v1, process_v2
        )

        full_profiles = tuple(
            compose_full_requirement_quality_profile(
                next(record for record in records_v1
                     if record.extraction_result.requirement.id == item.requirement_id),
                artifact_ref=request.artifact_v1, assessment_ref=request.assessment_v1,
                external_assessments=item.external_assessments,
            ) for item in request.full_quality
        )
        prediction = None
        if request.prediction is not None:
            prediction = predict_performance_efficiency(
                feature_v1,
                PerformanceEfficiencyPredictionRequest(
                    request.prediction.event_ref, feature_v1.profile_id,
                    request.prediction.context, request.prediction.parameter_set,
                ),
                request.prediction.predictor,
            )
        quantitative = ()
        if request.quantitative_risk is not None:
            supplied = request.quantitative_risk
            if tuple(item.kind for item in supplied.operands) != tuple(QuantitativeRiskOperandKind):
                raise ValueError("quantitative-risk operands must use all four kinds in contract order")
            q_context = QuantitativeRiskCalculationContext(
                supplied.calculation_id, supplied.calculation_version,
                request.artifact_v1, request.assessment_v1, source_v1.snapshot_id,
                request.process_ref_v1,
            )
            operands = tuple(
                QuantitativeRiskOperand(
                    QuantitativeRiskOperandId(item.kind, item.operand_id,
                                              item.operand_version),
                    item.kind, item.state, item.value,
                    QuantitativeRiskOperandProvenance(
                        item.source_ref, item.source_or_rationale,
                        item.calibration_status, QUANTITATIVE_RISK_CONTRACT_REF,
                        request.artifact_v1, problem_v1.ref, relation_v1.ref,
                        relation_v1.characteristic_id, request.process_ref_v1,
                        item.context_ref,
                    ),
                ) for item in supplied.operands
            )
            q_request = QuantitativeRiskCalculationRequest(
                problem_v1, relation_v1, q_context, *operands
            )
            quantitative = (calculate_quantitative_local_risk(q_request),)
        checkpoints = tuple(
            self._checkpoint(item, metric_v1, core_v2.metric_profile,
                             process_v1, process_v2)
            for item in request.checkpoints
        )
        bundle = FullModelServiceReportBundle(
            assessment_result=source_v1, metric_profile=metric_v1,
            criterion_binding=binding_v1,
            observation_resolution=observation_resolution_v1,
            conformance=conformance_v1, feature_profile=feature_v1,
            product_quality_assessment=quality_v1,
            problem_resolutions=resolutions_v1, defect_population=population_v1,
            defect_quality_relations=(relation_v1,), risk_assessments=(risk_v1,),
            corrective_action_resolutions=(action_resolution,),
            specification_versions=(parent, child), external_revisions=(revision,),
            action_applications=(application,), reassessment_runs=(reassessment,),
            comparisons=comparisons, process_states=(process_v1, process_v2),
            process_transitions=(process_transition,),
            predicted_product_quality=prediction,
            quantitative_risk_assessments=quantitative,
            checkpoint_evaluations=checkpoints,
            full_requirement_quality_profiles=full_profiles,
        )
        return FullModelResult(
            source_v1, metric_v1, binding_v1, observation_resolution_v1,
            conformance_v1, feature_v1, quality_v1, resolutions_v1,
            population_v1, (relation_v1,), (risk_v1,), action_resolution,
            parent, child, revision, application, reassessment, comparisons,
            process_v1, process_v2, process_transition, bundle, full_profiles,
            prediction, quantitative, checkpoints,
        )

    @staticmethod
    def _validate_request(r):
        if not r.requirements:
            raise ValueError("requirements must not be empty")
        if r.assessment_v1.artifact_ref != r.artifact_v1:
            raise ValueError("v1 assessment and artifact must agree")
        if r.collection_ref.product_ref != r.product_ref or r.collection_ref.environment_ref != r.environment_ref:
            raise ValueError("collection, product, and environment identities must agree")
        if r.collection_ref.source_kind is not r.observation_source_kind:
            raise ValueError("collection and observation source kinds must agree")
        if r.revision.child_artifact_ref != r.assessment_v2.artifact_ref:
            raise ValueError("v2 assessment and revised artifact must agree")
        if r.process_ref_v1.stage is not ProcessStage.REFERENCE_VERIFICATION or r.process_ref_v2.stage is not ProcessStage.REFERENCE_VERIFICATION:
            raise ValueError("supported path requires REFERENCE_VERIFICATION process stages")
        if len(r.comparison_ids) != 4 or len(set(r.comparison_ids)) != 4:
            raise ValueError("comparison_ids must contain four unique identities")

    @staticmethod
    def _checkpoint(item, metric_v1, metric_v2, process_v1, process_v2):
        if item.result_version == "v1":
            profile, state = metric_v1, process_v1
        elif item.result_version == "v2":
            profile, state = metric_v2, process_v2
        else:
            raise ValueError("checkpoint result_version must be 'v1' or 'v2'")
        entry = next(x for x in profile.entries if x.metric_id is MetricId.SPEC_QB_CONSISTENCY)
        selected = select_metric_result(entry, state)
        return evaluate_checkpoint(CheckpointRequest(
            item.checkpoint_id, item.checkpoint_version, selected,
            item.threshold_policy, state.ref, state.artifact_ref,
        ))

    @staticmethod
    def _comparisons(r, parent, observation, action, application, metric_v1,
                     problem_v1, risk_v1, quality_v1, core_v2, downstream_v2):
        qb_v1 = next(x for x in metric_v1.entries if x.metric_id is MetricId.SPEC_QB_CONSISTENCY)
        qb_v2 = next(x for x in core_v2.metric_profile.entries if x.metric_id is MetricId.SPEC_QB_CONSISTENCY)
        lineages = tuple(item.lineage_id for item in parent.requirements)
        key_scope = (action.comparison_key.normalized_metric,
                     action.comparison_key.normalized_context,
                     action.comparison_key.unit.value)
        def subject(family, identifier):
            return ComparisonSubject(family, identifier,
                (r.artifact_v1.artifact_id, *key_scope, identifier), lineages,
                key_scope, (observation.observation_id,))
        subjects = (
            subject(ComparisonResultFamily.QB_CONSISTENCY, MetricId.SPEC_QB_CONSISTENCY.value),
            subject(ComparisonResultFamily.CONFIRMED_PROBLEM, "CONFIRMED_SUPPORTED_PROBLEM"),
            subject(ComparisonResultFamily.BOUNDED_RISK, "PERFORMANCE_EFFICIENCY"),
            subject(ComparisonResultFamily.PRODUCT_QUALITY, "PERFORMANCE_EFFICIENCY"),
        )
        before_after = (
            (_comparable(r.artifact_v1, subjects[0], qb_v1.entry_id,
                status=FullModelStatus.AVAILABLE, applicability=Applicability.APPLICABLE,
                value_kind=ComparisonValueKind.EXACT_FRACTION, exact_value=qb_v1.value,
                rules=qb_v1.rule_refs),
             _comparable(r.revision.child_artifact_ref, subjects[0], qb_v2.entry_id,
                status=FullModelStatus.AVAILABLE, applicability=Applicability.APPLICABLE,
                value_kind=ComparisonValueKind.EXACT_FRACTION, exact_value=qb_v2.value,
                rules=qb_v2.rule_refs)),
            (_comparable(r.artifact_v1, subjects[1], problem_v1.ref,
                status=problem_v1.status, applicability=problem_v1.applicability,
                value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                categorical_state=problem_v1.disposition.value, rules=(PROBLEM_RULE_REF,)),
             _comparable(r.revision.child_artifact_ref, subjects[1],
                downstream_v2.target_problem_resolution.ref,
                status=downstream_v2.target_problem_resolution.status,
                applicability=downstream_v2.target_problem_resolution.applicability,
                value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                categorical_state=(downstream_v2.target_problem_resolution.disposition.value
                    if downstream_v2.target_problem_resolution.disposition is not None else None),
                rules=(PROBLEM_RULE_REF,))),
            (_comparable(r.artifact_v1, subjects[2], risk_v1.ref,
                status=risk_v1.status, applicability=risk_v1.applicability,
                value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                categorical_state=risk_v1.classification.value, rules=(RISK_RULE_REF,),
                models=(RISK_MODEL_REF,), parameters=(RISK_PARAMETER_SET_REF,),
                calibration=risk_v1.calibration_status),
             _comparable(r.revision.child_artifact_ref, subjects[2], downstream_v2.risk_assessment.ref,
                status=downstream_v2.risk_assessment.status,
                applicability=downstream_v2.risk_assessment.applicability,
                value_kind=ComparisonValueKind.CATEGORICAL_STATE, rules=(RISK_RULE_REF,),
                models=(RISK_MODEL_REF,), parameters=(RISK_PARAMETER_SET_REF,),
                calibration=downstream_v2.risk_assessment.calibration_status)),
            (_comparable(r.artifact_v1, subjects[3], quality_v1.assessment_id,
                status=quality_v1.status, applicability=quality_v1.applicability,
                value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                rules=(PROCEDURE_RULE_REF,), models=(MODEL_REF,),
                parameters=(PARAMETER_SET_REF,), calibration=quality_v1.calibration_status),
             _comparable(r.revision.child_artifact_ref, subjects[3],
                downstream_v2.product_quality_assessment.assessment_id,
                status=downstream_v2.product_quality_assessment.status,
                applicability=downstream_v2.product_quality_assessment.applicability,
                value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                categorical_state="AVAILABLE", rules=(PROCEDURE_RULE_REF,),
                models=(MODEL_REF,), parameters=(PARAMETER_SET_REF,),
                calibration=downstream_v2.product_quality_assessment.calibration_status)),
        )
        return tuple(compare(ComparisonRequest(cid, r.comparison_version, before,
                                                after, application.transition))
                     for cid, (before, after) in zip(r.comparison_ids, before_after, strict=True))

    @staticmethod
    def _process_states(r, source_v1, metric_v1, binding_v1, observation,
                        conformance_v1, feature_v1, quality_v1, population_v1,
                        problem_v1, relation_v1, risk_v1, action, application,
                        reassessment, reuse, comparisons, core_v2, downstream_v2):
        assoc1, req1, spec1 = _component_associations(
            source_v1, r.artifact_v1, r.assessment_v1, metric_v1, feature_v1,
            quality_v1, population_v1, problem_v1, relation_v1, risk_v1, action.ref)
        p1 = assemble_process_state(r.process_ref_v1, ProcessStateAssembly(
            r.process_ref_v1.process_state_id, r.artifact_v1, r.assessment_v1,
            FULL_MODEL_CONTRACT_REF, r.component_versions,
            _evidence_associations(r.artifact_v1, r.product_ref, source_v1,
                                   binding_v1, observation, conformance_v1),
            assoc1, req1, spec1, metric_v1.profile_id, feature_v1.profile_id,
            risk_v1.product_quality_context.assessment_ref, population_v1.ref,
            (problem_v1.ref,), (relation_v1.ref,), (risk_v1.ref,), (action.ref,),
        ))
        source_v2 = core_v2.specification_assessment
        problem2 = downstream_v2.target_problem_resolution.problem
        assoc2, req2, spec2 = _component_associations(
            source_v2, r.revision.child_artifact_ref, r.assessment_v2,
            core_v2.metric_profile, downstream_v2.feature_profile,
            downstream_v2.product_quality_assessment, downstream_v2.defect_population,
            problem2, downstream_v2.defect_quality_relation,
            downstream_v2.risk_assessment, application.action_after_ref)
        p2 = assemble_process_state(r.process_ref_v2, ProcessStateAssembly(
            r.process_ref_v2.process_state_id, r.revision.child_artifact_ref,
            r.assessment_v2, FULL_MODEL_CONTRACT_REF, r.component_versions,
            _evidence_associations(r.revision.child_artifact_ref, r.product_ref,
                source_v2, downstream_v2.criterion_binding, observation,
                downstream_v2.conformance, reuse=reuse),
            assoc2, req2, spec2, core_v2.metric_profile.profile_id,
            downstream_v2.feature_profile.profile_id,
            downstream_v2.risk_assessment.product_quality_context.assessment_ref,
            downstream_v2.defect_population.ref, (() if problem2 is None else (problem2.ref,)),
            (downstream_v2.defect_quality_relation.ref,),
            (downstream_v2.risk_assessment.ref,), (application.action_after_ref,),
            r.process_ref_v1, application.transition, application, reassessment,
            comparisons,
        ))
        return p1, p2


__all__ = ["FullModelService"]

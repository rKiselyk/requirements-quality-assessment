"""M3-12 canonical Full Model v0.1 end-to-end acceptance scenario."""

from dataclasses import dataclass, fields
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from hashlib import sha256

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.corrective_action import (
    ACTION_RECORD_VERSION,
    ACTION_RULE_REF,
    APPLICATION_RULE_REF,
    PROCESS_REASSESSMENT_CONTRACT_REF,
    ActionCreatorSource,
    ApplicationIdentityContext,
    CorrectiveActionContext,
    CorrectiveActionKind,
    ExternalProviderRef,
    ExternalRevisionProvenance,
    ExternalRevisionProviderKind,
    ExternallySuppliedRevision,
    RequirementTextReplacement,
    RevisionRef,
    apply_external_revision,
    create_initial_specification_version,
    propose_corrective_action,
)
from requirements_quality_assessment.cross_analysis import (
    CrossObservationRef,
    CrossResultState,
    QbConsistencyState,
    SpecificationAssessmentService,
)
from requirements_quality_assessment.defect_quality import (
    DEFECT_QUALITY_RISK_CONTRACT_REF,
    PROBLEM_RULE_REF,
    RELATION_RULE_REF,
    DefectConstructionContext,
    DefectQualityRelationContext,
    ProblemDisposition,
    TypedProblemClaimSource,
    build_defect_population,
    relate_problem_to_quality,
    resolve_problem_claim,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorLabel,
    FeatureId,
    Requirement,
    UnitLabel,
)
from requirements_quality_assessment.dynamic_evidence import (
    BINDING_RULE_REF,
    DYNAMIC_CONTRACT_REF,
    EVALUATOR_RULE_REF,
    RESPONSE_TIME_METRIC_REF,
    SUPPORTED_CONTEXT_IDENTITY,
    Applicability,
    ConformanceEvaluationContext,
    ConformanceOutcome,
    CriterionBindingContext,
    DynamicEvidenceAssessmentRef,
    EnvironmentRef,
    FullModelStatus,
    ObservationCollectionRef,
    ObservationSlotRef,
    ObservationSourceKind,
    ProductRef,
    assess_conformance,
    bind_quantitative_criterion,
    make_dynamic_observation,
    resolve_dynamic_observation,
)
from requirements_quality_assessment.dynamic_evidence.domain import DynamicObservationRef
from requirements_quality_assessment.extractor import BaselineFeatureExtractor
from requirements_quality_assessment.full_model_reporter import (
    AuditFullModelReporter,
    FullModelReportBundle,
    UserFullModelReporter,
)
from requirements_quality_assessment.metrics import (
    FULL_MODEL_CONTRACT_REF,
    ArtifactRef,
    AssessmentRef,
    MetricConstructionContext,
    MetricId,
    MetricProfileBuilder,
    RequirementSubjectRef,
)
from requirements_quality_assessment.performance_efficiency import (
    FEATURE_CONTRACT_REF,
    MAPPING_RULE_REF,
    PerformanceEfficiencyFeatureId,
    PerformanceEfficiencyFeatureConstructionContext,
    PerformanceEfficiencyFeatureProfileBuilder,
    ProcessStage,
    ProcessStateRef,
    QbTargetGateDecision,
)
from requirements_quality_assessment.process import (
    PROCESS_RULE_REF,
    PROCESS_STAGE_MAPPING,
    DissertationStage,
    ProcessComponentAssociation,
    ProcessComponentRole,
    ProcessEvidenceAssociation,
    ProcessEvidenceRole,
    ProcessStateAssembly,
    RequirementAssessmentRef,
    SpecificationAssessmentRef,
    assemble_process_state,
    assemble_process_transition,
)
from requirements_quality_assessment.product_quality import (
    ASSESSMENT_CONTRACT_REF,
    MODEL_REF,
    PARAMETER_SET,
    PARAMETER_SET_REF,
    PROCEDURE_RULE_REF,
    CalibrationStatus,
    ProductQualityAssessmentContext,
    ProductQualityAssessmentEventRef,
    assess_product_quality,
)
from requirements_quality_assessment.reassessment import (
    COMPARISON_RULE_REF,
    REASSESSMENT_RULE_REF,
    AssessmentResultRef,
    ComparableResult,
    ComparisonKind,
    ComparisonRequest,
    ComparisonResultFamily,
    ComparisonSubject,
    ComparisonValueKind,
    ComponentVersionSet,
    DynamicObservationUse,
    EvidenceReuseDecision,
    EvidenceReuseDisposition,
    EvidenceReuseProvenance,
    EvidenceReuseReason,
    ExactIdentityCheck,
    ReferenceFullModelDownstreamRebuilder,
    ReferenceFullModelReassessmentInputs,
    ReassessmentContext,
    ReassessmentIdentityContext,
    VersionedComponentRef,
    compare,
    reevaluate,
)
from requirements_quality_assessment.risk import (
    RISK_MODEL_REF,
    RISK_PARAMETER_SET,
    RISK_PARAMETER_SET_REF,
    RISK_RULE_REF,
    RiskAssessmentContext,
    RiskAssessmentEventRef,
    RiskClassification,
    assess_risk,
)


V1_R001 = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
V1_R002 = "Час відгуку не нижче 5 с при 500 одночасних користувачах"
V2_R002 = "Час відгуку ≤ 5 с при 500 одночасних користувачах"
OBSERVED_RESPONSE_TIME = Decimal("1.8")


class _AssemblyReason(str, Enum):
    NO_CONFIRMED_PROBLEM = "NO_CONFIRMED_PROBLEM"


COMPONENT_VERSIONS = ComponentVersionSet(
    (
        VersionedComponentRef("FULL_MODEL_CONTRACT", "FULL-MODEL-V0.1-CONTRACT", "1"),
        VersionedComponentRef("DYNAMIC_EVIDENCE", "FULL-MODEL-V0.1-DYNAMIC-EVIDENCE", "1"),
        VersionedComponentRef("PE_FEATURES", "FULL-MODEL-V0.1-PRODUCT-QUALITY-FEATURE", "1"),
        VersionedComponentRef("PRODUCT_QUALITY", "FULL-MODEL-V0.1-PRODUCT-QUALITY-ASSESSMENT", "1"),
        VersionedComponentRef("DEFECT_RISK", "FULL-MODEL-V0.1-DEFECT-QUALITY-RISK", "1"),
        VersionedComponentRef("PROCESS_REASSESSMENT", "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", "1"),
    )
)


@dataclass(frozen=True)
class _Scenario:
    parent: object
    child: object
    source_v1: object
    metric_v1: object
    binding_v1: object
    observation_resolution_v1: object
    conformance_v1: object
    feature_v1: object
    quality_v1: object
    problem_v1: object
    population_v1: object
    relation_v1: object
    risk_v1: object
    action_resolution: object
    revision: object
    application: object
    reuse: object
    reassessment: object
    comparisons: tuple[object, ...]
    process_v1: object
    process_v2: object
    process_transition: object
    report_bundle: FullModelReportBundle


def _available_component(role, result_ref, scope, producing_ref=FULL_MODEL_CONTRACT_REF):
    return ProcessComponentAssociation(
        role,
        result_ref,
        FullModelStatus.AVAILABLE,
        Applicability.APPLICABLE,
        scope,
        producing_ref,
        (),
        (result_ref,),
    )


def _evidence_associations(
    artifact,
    product,
    source,
    binding,
    observation,
    conformance,
    *,
    reuse=None,
):
    values = (
        (
            ProcessEvidenceRole.STATIC_REQUIREMENT,
            tuple(record.extraction_result.evidence for record in source.records),
            artifact,
            source.snapshot_id,
            None,
        ),
        (
            ProcessEvidenceRole.QB,
            tuple(item.result_id for item in source.cross_results),
            artifact,
            source.snapshot_id,
            None,
        ),
        (
            ProcessEvidenceRole.DYNAMIC_CRITERION,
            binding.binding_id,
            artifact,
            binding.provenance.requirement_subject_ref,
            None,
        ),
        (
            ProcessEvidenceRole.DYNAMIC_OBSERVATION,
            DynamicObservationRef(observation.observation_id),
            product,
            observation.collection_ref,
            reuse,
        ),
        (
            ProcessEvidenceRole.CONFORMANCE,
            conformance.conformance_id,
            artifact,
            conformance.dynamic_assessment_ref,
            None,
        ),
    )
    return tuple(
        ProcessEvidenceAssociation(
            role,
            evidence_ref,
            FullModelStatus.AVAILABLE,
            Applicability.APPLICABLE,
            subject,
            source_ref,
            SUPPORTED_CONTEXT_IDENTITY if role is not ProcessEvidenceRole.STATIC_REQUIREMENT else None,
            reuse_ref,
            (),
            (evidence_ref, source_ref),
        )
        for role, evidence_ref, subject, source_ref, reuse_ref in values
    )


def _requirement_and_specification_refs(source, artifact, assessment):
    requirement_refs = tuple(
        RequirementAssessmentRef(
            assessment,
            RequirementSubjectRef(
                artifact,
                record.extraction_result.requirement.id,
                record.extraction_result.requirement.source_line,
            ),
        )
        for record in source.records
    )
    return requirement_refs, SpecificationAssessmentRef(assessment, source.snapshot_id)


def _component_associations(
    source,
    artifact,
    assessment,
    metric,
    feature,
    quality,
    population,
    problem,
    relation,
    risk,
    action_ref,
):
    requirement_refs, specification_ref = _requirement_and_specification_refs(
        source, artifact, assessment
    )
    problem_association = (
        _available_component(
            ProcessComponentRole.CONFIRMED_PROBLEM,
            problem.ref,
            artifact,
            PROBLEM_RULE_REF,
        )
        if problem is not None
        else ProcessComponentAssociation(
            ProcessComponentRole.CONFIRMED_PROBLEM,
            None,
            FullModelStatus.NOT_APPLICABLE,
            Applicability.NOT_APPLICABLE,
            artifact,
            PROBLEM_RULE_REF,
            (_AssemblyReason.NO_CONFIRMED_PROBLEM,),
            (artifact,),
        )
    )
    return (
        (
            *(
                _available_component(
                    ProcessComponentRole.REQUIREMENT_ASSESSMENT,
                    item,
                    item.requirement_subject_ref,
                )
                for item in requirement_refs
            ),
            _available_component(
                ProcessComponentRole.SPECIFICATION_ASSESSMENT,
                specification_ref,
                artifact,
            ),
            _available_component(
                ProcessComponentRole.METRIC_PROFILE,
                metric.profile_id,
                artifact,
            ),
            ProcessComponentAssociation(
                ProcessComponentRole.PE_FEATURE_PROFILE,
                feature.profile_id,
                feature.status,
                feature.applicability,
                feature.product_ref,
                FEATURE_CONTRACT_REF,
                (),
                (feature.profile_id,),
            ),
            ProcessComponentAssociation(
                ProcessComponentRole.PRODUCT_QUALITY_ASSESSMENT,
                risk.product_quality_context.assessment_ref,
                quality.status,
                quality.applicability,
                quality.product_ref,
                ASSESSMENT_CONTRACT_REF,
                (),
                (risk.product_quality_context.assessment_ref,),
            ),
            _available_component(
                ProcessComponentRole.DEFECT_POPULATION,
                population.ref,
                artifact,
                DEFECT_QUALITY_RISK_CONTRACT_REF,
            ),
            problem_association,
            ProcessComponentAssociation(
                ProcessComponentRole.DEFECT_QUALITY_RELATION,
                relation.ref,
                relation.status,
                relation.applicability,
                artifact,
                RELATION_RULE_REF,
                relation.reasons,
                (relation.ref,),
            ),
            ProcessComponentAssociation(
                ProcessComponentRole.BOUNDED_RISK_ASSESSMENT,
                risk.ref,
                risk.status,
                risk.applicability,
                artifact,
                RISK_RULE_REF,
                (),
                (risk.ref,),
            ),
            _available_component(
                ProcessComponentRole.CORRECTIVE_ACTION,
                action_ref,
                artifact,
                ACTION_RULE_REF,
            ),
        ),
        requirement_refs,
        specification_ref,
    )


def _comparable(
    artifact,
    subject,
    result_identity,
    *,
    status,
    applicability,
    value_kind,
    exact_value=None,
    categorical_state=None,
    rules=(),
    models=(),
    parameters=(),
    calibration=None,
):
    return ComparableResult(
        AssessmentResultRef("M3-12-COMPARABLE", result_identity, artifact),
        subject,
        value_kind,
        status,
        applicability,
        exact_value,
        categorical_state,
        "EXACT_FRACTION" if value_kind is ComparisonValueKind.EXACT_FRACTION else None,
        ProcessStage.REFERENCE_VERIFICATION,
        rules,
        models,
        parameters,
        FULL_MODEL_CONTRACT_REF,
        calibration,
    )


def _build_scenario() -> _Scenario:
    requirements = (
        Requirement("R001", 1, V1_R001),
        Requirement("R002", 2, V1_R002),
    )
    extractor = BaselineFeatureExtractor()
    assessor = RequirementQualityAssessor()
    records_v1 = tuple(
        assessor.assess_record(extractor.extract(requirement))
        for requirement in requirements
    )
    source_v1 = SpecificationAssessmentService().assess(records_v1)
    artifact_v1 = ArtifactRef("SPEC-PROCESS-REF-001", "v1")
    assessment_v1 = AssessmentRef("ASSESS-PROCESS-REF-001", "v1", artifact_v1)
    process_ref_v1 = ProcessStateRef(
        "PROCESS-PROCESS-REF-001", "v1", ProcessStage.REFERENCE_VERIFICATION
    )
    metric_v1 = MetricProfileBuilder().build(
        source_v1, MetricConstructionContext(artifact_v1, assessment_v1)
    )
    parent = create_initial_specification_version(artifact_v1, requirements)

    selected_observation_ref = CrossObservationRef(
        "R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0
    )
    binding_v1 = bind_quantitative_criterion(
        records_v1[0].extraction_result,
        selected_observation_ref,
        CriterionBindingContext(artifact_v1, assessment_v1, source_v1.snapshot_id),
    )
    product = ProductRef("PRODUCT-REF-001", "1")
    collection = ObservationCollectionRef(
        "COLLECTION-REF-001",
        "1",
        product,
        EnvironmentRef("ENV-REF-001", "1"),
        ObservationSourceKind.DETERMINISTIC_FIXTURE,
    )
    slot = ObservationSlotRef(collection, 0)
    observation = make_dynamic_observation(
        slot,
        RESPONSE_TIME_METRIC_REF,
        OBSERVED_RESPONSE_TIME,
        UnitLabel.SECOND,
        SUPPORTED_CONTEXT_IDENTITY,
        "OBSERVATION-REF-001",
    )
    observation_resolution_v1 = resolve_dynamic_observation(slot, observation)
    dynamic_ref_v1 = DynamicEvidenceAssessmentRef(
        "DYNAMIC-ASSESSMENT-REF-001", "v1", artifact_v1, product, collection
    )
    conformance_v1 = assess_conformance(
        binding_v1,
        observation_resolution_v1,
        ConformanceEvaluationContext(dynamic_ref_v1),
    )
    feature_v1 = PerformanceEfficiencyFeatureProfileBuilder().build(
        metric_v1,
        source_v1,
        binding_v1,
        observation_resolution_v1,
        conformance_v1,
        PerformanceEfficiencyFeatureConstructionContext(
            artifact_v1,
            assessment_v1,
            metric_v1.profile_id,
            dynamic_ref_v1,
            product,
            process_ref_v1,
        ),
    )
    quality_event_v1 = ProductQualityAssessmentEventRef(
        "PRODUCT-QUALITY-EVENT-REF-001", "v1", product, artifact_v1
    )
    quality_v1 = assess_product_quality(
        feature_v1,
        MODEL_REF,
        PARAMETER_SET_REF,
        ProductQualityAssessmentContext(
            quality_event_v1,
            artifact_v1,
            assessment_v1,
            feature_v1.profile_id,
            product,
            process_ref_v1,
        ),
    )

    construction_v1 = DefectConstructionContext(
        artifact_v1, assessment_v1, source_v1.snapshot_id, process_ref_v1
    )
    relation_context_v1 = DefectQualityRelationContext(
        artifact_v1, assessment_v1, source_v1.snapshot_id, process_ref_v1
    )
    resolutions_v1 = tuple(
        resolve_problem_claim(
            TypedProblemClaimSource.from_qb_result(
                result, source_v1.projection.snapshot
            ),
            construction_v1,
        )
        for result in source_v1.cross_results
    )
    population_v1 = build_defect_population(
        resolutions_v1,
        source_v1.specification_assessment.qb_consistency,
        construction_v1,
    )
    problem_v1 = resolutions_v1[0]
    relation_v1 = relate_problem_to_quality(problem_v1, relation_context_v1)
    risk_v1 = assess_risk(
        problem_v1,
        population_v1,
        relation_v1,
        quality_v1,
        RiskAssessmentContext(
            RiskAssessmentEventRef(
                "RISK-EVENT-REF-001", "v1", artifact_v1, process_ref_v1
            ),
            artifact_v1,
            assessment_v1,
            source_v1.snapshot_id,
            process_ref_v1,
        ),
    )
    action_resolution = propose_corrective_action(
        risk_v1,
        problem_v1.problem,
        relation_v1,
        CorrectiveActionContext(
            "A-REF-001",
            ACTION_RECORD_VERSION,
            ActionCreatorSource("CORRECTIVE-ACTION-PROPOSER", "1"),
            artifact_v1,
            tuple(item.lineage_id for item in parent.requirements),
            assessment_v1,
            source_v1.snapshot_id,
            process_ref_v1,
        ),
    )
    action = action_resolution.action
    assert action is not None

    child_ref = ArtifactRef(artifact_v1.artifact_id, "v2")
    revision_ref = RevisionRef("REV-REF-001", "v1")
    provider_ref = ExternalProviderRef("QB-CONFLICT-REFERENCE", "1")
    replacement = RequirementTextReplacement(
        parent.requirements[1].lineage_id,
        parent.requirements[1].subject_ref,
        V2_R002,
    )
    revision = ExternallySuppliedRevision(
        revision_ref.revision_id,
        revision_ref.revision_version,
        ExternalRevisionProviderKind.CONTROLLED_REFERENCE_FIXTURE,
        provider_ref,
        action.ref,
        artifact_v1,
        child_ref,
        (replacement,),
        "Controlled Full Model v0.1 QB conflict reference fixture",
        ExternalRevisionProvenance(
            revision_ref,
            action.ref,
            artifact_v1,
            child_ref,
            provider_ref,
        ),
    )
    application = apply_external_revision(
        action,
        revision,
        parent,
        ApplicationIdentityContext(
            "APP-REF-001", "v1", "v2", "ARTIFACT-TRANSITION-REF-001"
        ),
    )
    child = application.child_specification

    process_ref_v2 = ProcessStateRef(
        process_ref_v1.process_state_id,
        "v2",
        ProcessStage.REFERENCE_VERIFICATION,
    )
    exact_reuse_values = (
        ("product_ref", observation.product_ref),
        ("observation_source_kind", observation.source_kind),
        ("collection_ref", observation.collection_ref),
        ("metric_ref", observation.metric_ref),
        ("unit", observation.unit),
        ("context_identity", observation.context_identity),
        ("applicability", Applicability.APPLICABLE),
        ("process_stage", process_ref_v2.stage),
        ("source_contract_permission", True),
    )
    reuse = EvidenceReuseDecision(
        DynamicObservationRef(observation.observation_id),
        process_ref_v2,
        EvidenceReuseDisposition.REUSE_ALLOWED,
        tuple(
            ExactIdentityCheck(name, value, value, True)
            for name, value in exact_reuse_values
        ),
        (EvidenceReuseReason.EXACT_IDENTITY_AND_CONTEXT_MATCH,),
        EvidenceReuseProvenance(process_ref_v1, process_ref_v2, DYNAMIC_CONTRACT_REF),
    )
    assessment_v2 = AssessmentRef("ASSESS-PROCESS-REF-001", "v2", child_ref)
    reassessment_context = ReassessmentContext(
        process_ref_v1,
        application.ref,
        artifact_v1,
        child_ref,
        assessment_v2,
        FULL_MODEL_CONTRACT_REF,
        COMPONENT_VERSIONS,
        (reuse,),
        ProcessStage.REFERENCE_VERIFICATION,
    )
    downstream_inputs = ReferenceFullModelReassessmentInputs(
        parent.requirements[0].lineage_id,
        selected_observation_ref,
        slot,
        observation,
        DynamicObservationUse.EXPLICIT_REUSE,
        reuse,
        DynamicEvidenceAssessmentRef(
            "DYNAMIC-ASSESSMENT-REF-001", "v2", child_ref, product, collection
        ),
        ProductQualityAssessmentEventRef(
            "PRODUCT-QUALITY-EVENT-REF-001", "v2", product, child_ref
        ),
        RiskAssessmentEventRef(
            "RISK-EVENT-REF-001", "v2", child_ref, process_ref_v2
        ),
        tuple(item.lineage_id for item in action.target_requirements),
        action.comparison_key,
    )
    reassessment = reevaluate(
        child,
        reassessment_context,
        ReassessmentIdentityContext("REEVAL-REF-001", "v1", process_ref_v2),
        ReferenceFullModelDownstreamRebuilder(downstream_inputs),
    )
    core_v2, downstream_v2 = reassessment.produced_results
    qb_v1 = next(
        entry for entry in metric_v1.entries
        if entry.metric_id is MetricId.SPEC_QB_CONSISTENCY
    )
    qb_v2 = next(
        entry for entry in core_v2.metric_profile.entries
        if entry.metric_id is MetricId.SPEC_QB_CONSISTENCY
    )
    lineages = tuple(item.lineage_id for item in parent.requirements)
    key_scope = (
        action.comparison_key.normalized_metric,
        action.comparison_key.normalized_context,
        action.comparison_key.unit.value,
    )

    def subject(family, identifier):
        return ComparisonSubject(
            family,
            identifier,
            (artifact_v1.artifact_id, *key_scope, identifier),
            lineages,
            key_scope,
            (observation.observation_id,),
        )

    qb_subject = subject(ComparisonResultFamily.QB_CONSISTENCY, MetricId.SPEC_QB_CONSISTENCY.value)
    problem_subject = subject(ComparisonResultFamily.CONFIRMED_PROBLEM, "CONFIRMED_SUPPORTED_PROBLEM")
    risk_subject = subject(ComparisonResultFamily.BOUNDED_RISK, "PERFORMANCE_EFFICIENCY")
    quality_subject = subject(ComparisonResultFamily.PRODUCT_QUALITY, "PERFORMANCE_EFFICIENCY")
    comparisons = (
        compare(
            ComparisonRequest(
                "COMPARE-QB-REF-001",
                "v1",
                _comparable(
                    artifact_v1,
                    qb_subject,
                    qb_v1.entry_id,
                    status=FullModelStatus.AVAILABLE,
                    applicability=Applicability.APPLICABLE,
                    value_kind=ComparisonValueKind.EXACT_FRACTION,
                    exact_value=qb_v1.value,
                    rules=qb_v1.rule_refs,
                ),
                _comparable(
                    child_ref,
                    qb_subject,
                    qb_v2.entry_id,
                    status=FullModelStatus.AVAILABLE,
                    applicability=Applicability.APPLICABLE,
                    value_kind=ComparisonValueKind.EXACT_FRACTION,
                    exact_value=qb_v2.value,
                    rules=qb_v2.rule_refs,
                ),
                application.transition,
            )
        ),
        compare(
            ComparisonRequest(
                "COMPARE-PROBLEM-REF-001",
                "v1",
                _comparable(
                    artifact_v1,
                    problem_subject,
                    problem_v1.ref,
                    status=problem_v1.status,
                    applicability=problem_v1.applicability,
                    value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                    categorical_state=problem_v1.disposition.value,
                    rules=(PROBLEM_RULE_REF,),
                ),
                _comparable(
                    child_ref,
                    problem_subject,
                    downstream_v2.target_problem_resolution.ref,
                    status=downstream_v2.target_problem_resolution.status,
                    applicability=downstream_v2.target_problem_resolution.applicability,
                    value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                    categorical_state=(
                        downstream_v2.target_problem_resolution.disposition.value
                        if downstream_v2.target_problem_resolution.disposition is not None
                        else None
                    ),
                    rules=(PROBLEM_RULE_REF,),
                ),
                application.transition,
            )
        ),
        compare(
            ComparisonRequest(
                "COMPARE-RISK-REF-001",
                "v1",
                _comparable(
                    artifact_v1,
                    risk_subject,
                    risk_v1.ref,
                    status=risk_v1.status,
                    applicability=risk_v1.applicability,
                    value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                    categorical_state=risk_v1.classification.value,
                    rules=(RISK_RULE_REF,),
                    models=(RISK_MODEL_REF,),
                    parameters=(RISK_PARAMETER_SET_REF,),
                    calibration=risk_v1.calibration_status,
                ),
                _comparable(
                    child_ref,
                    risk_subject,
                    downstream_v2.risk_assessment.ref,
                    status=downstream_v2.risk_assessment.status,
                    applicability=downstream_v2.risk_assessment.applicability,
                    value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                    rules=(RISK_RULE_REF,),
                    models=(RISK_MODEL_REF,),
                    parameters=(RISK_PARAMETER_SET_REF,),
                    calibration=downstream_v2.risk_assessment.calibration_status,
                ),
                application.transition,
            )
        ),
        compare(
            ComparisonRequest(
                "COMPARE-PRODUCT-QUALITY-REF-001",
                "v1",
                _comparable(
                    artifact_v1,
                    quality_subject,
                    quality_v1.assessment_id,
                    status=quality_v1.status,
                    applicability=quality_v1.applicability,
                    value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                    rules=(PROCEDURE_RULE_REF,),
                    models=(MODEL_REF,),
                    parameters=(PARAMETER_SET_REF,),
                    calibration=quality_v1.calibration_status,
                ),
                _comparable(
                    child_ref,
                    quality_subject,
                    downstream_v2.product_quality_assessment.assessment_id,
                    status=downstream_v2.product_quality_assessment.status,
                    applicability=downstream_v2.product_quality_assessment.applicability,
                    value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                    categorical_state="AVAILABLE",
                    rules=(PROCEDURE_RULE_REF,),
                    models=(MODEL_REF,),
                    parameters=(PARAMETER_SET_REF,),
                    calibration=downstream_v2.product_quality_assessment.calibration_status,
                ),
                application.transition,
            )
        ),
    )

    associations_v1, requirement_refs_v1, specification_ref_v1 = _component_associations(
        source_v1,
        artifact_v1,
        assessment_v1,
        metric_v1,
        feature_v1,
        quality_v1,
        population_v1,
        problem_v1.problem,
        relation_v1,
        risk_v1,
        action.ref,
    )
    process_v1 = assemble_process_state(
        process_ref_v1,
        ProcessStateAssembly(
            process_ref_v1.process_state_id,
            artifact_v1,
            assessment_v1,
            FULL_MODEL_CONTRACT_REF,
            COMPONENT_VERSIONS,
            _evidence_associations(
                artifact_v1,
                product,
                source_v1,
                binding_v1,
                observation,
                conformance_v1,
            ),
            associations_v1,
            requirement_refs_v1,
            specification_ref_v1,
            metric_v1.profile_id,
            feature_v1.profile_id,
            risk_v1.product_quality_context.assessment_ref,
            population_v1.ref,
            (problem_v1.problem.ref,),
            (relation_v1.ref,),
            (risk_v1.ref,),
            (action.ref,),
        ),
    )

    source_v2 = core_v2.specification_assessment
    associations_v2, requirement_refs_v2, specification_ref_v2 = _component_associations(
        source_v2,
        child_ref,
        assessment_v2,
        core_v2.metric_profile,
        downstream_v2.feature_profile,
        downstream_v2.product_quality_assessment,
        downstream_v2.defect_population,
        downstream_v2.target_problem_resolution.problem,
        downstream_v2.defect_quality_relation,
        downstream_v2.risk_assessment,
        application.action_after_ref,
    )
    process_v2 = assemble_process_state(
        process_ref_v2,
        ProcessStateAssembly(
            process_ref_v2.process_state_id,
            child_ref,
            assessment_v2,
            FULL_MODEL_CONTRACT_REF,
            COMPONENT_VERSIONS,
            _evidence_associations(
                child_ref,
                product,
                source_v2,
                downstream_v2.criterion_binding,
                observation,
                downstream_v2.conformance,
                reuse=reuse,
            ),
            associations_v2,
            requirement_refs_v2,
            specification_ref_v2,
            core_v2.metric_profile.profile_id,
            downstream_v2.feature_profile.profile_id,
            downstream_v2.risk_assessment.product_quality_context.assessment_ref,
            downstream_v2.defect_population.ref,
            (),
            (downstream_v2.defect_quality_relation.ref,),
            (downstream_v2.risk_assessment.ref,),
            (application.action_after_ref,),
            process_ref_v1,
            application.transition,
            application,
            reassessment,
            comparisons,
        ),
    )
    process_transition = assemble_process_transition(
        "PROCESS-TRANSITION-REF-001", process_v1, process_v2
    )
    report_bundle = FullModelReportBundle(
        assessment_result=source_v1,
        metric_profile=metric_v1,
        criterion_binding=binding_v1,
        observation_resolution=observation_resolution_v1,
        conformance=conformance_v1,
        feature_profile=feature_v1,
        product_quality_assessment=quality_v1,
        problem_resolutions=resolutions_v1,
        defect_population=population_v1,
        defect_quality_relations=(relation_v1,),
        risk_assessments=(risk_v1,),
        corrective_action_resolutions=(action_resolution,),
        specification_versions=(parent, child),
        external_revisions=(revision,),
        action_applications=(application,),
        reassessment_runs=(reassessment,),
        comparisons=comparisons,
        process_states=(process_v1, process_v2),
        process_transitions=(process_transition,),
    )
    return _Scenario(
        parent,
        child,
        source_v1,
        metric_v1,
        binding_v1,
        observation_resolution_v1,
        conformance_v1,
        feature_v1,
        quality_v1,
        problem_v1,
        population_v1,
        relation_v1,
        risk_v1,
        action_resolution,
        revision,
        application,
        reuse,
        reassessment,
        comparisons,
        process_v1,
        process_v2,
        process_transition,
        report_bundle,
    )


def test_m3_12_full_model_v0_1_canonical_end_to_end_acceptance() -> None:
    scenario = _build_scenario()
    cross = scenario.source_v1.cross_results[0]
    qb_v1 = scenario.source_v1.specification_assessment.qb_consistency
    action = scenario.action_resolution.action
    core_v2, downstream_v2 = scenario.reassessment.produced_results
    qb_v2 = core_v2.specification_assessment.specification_assessment.qb_consistency

    assert tuple(item.text for item in scenario.parent.requirements) == (V1_R001, V1_R002)
    assert cross.state is CrossResultState.CONFIRMED_CONFLICT
    assert cross.comparison_key.normalized_metric == "час відгуку"
    assert cross.comparison_key.normalized_context == "при 500 одночасних користувачах"
    assert cross.comparison_key.unit is UnitLabel.SECOND
    assert (cross.operands.left.value, cross.operands.right.value) == (
        Decimal("2"),
        Decimal("5"),
    )
    assert (
        cross.operands.left.comparator,
        cross.operands.left.inclusivity,
        cross.operands.right.comparator,
        cross.operands.right.inclusivity,
    ) == (
        ComparatorLabel.LESS_THAN_OR_EQUAL,
        BoundaryInclusivity.INCLUSIVE,
        ComparatorLabel.GREATER_THAN_OR_EQUAL,
        BoundaryInclusivity.INCLUSIVE,
    )
    assert cross.operands.left.normalized_metric == cross.operands.right.normalized_metric
    assert cross.operands.left.normalized_context == cross.operands.right.normalized_context
    assert cross.operands.left.unit is cross.operands.right.unit is UnitLabel.SECOND
    assert tuple(item.requirement_id for item in cross.observation_refs) == ("R001", "R002")
    assert qb_v1.state is QbConsistencyState.COMPUTED
    assert qb_v1.rconf_participant_ids == ("R001", "R002")
    assert qb_v1.value == Fraction(0, 1)
    assert scenario.problem_v1.disposition is ProblemDisposition.CONFIRMED_SUPPORTED_PROBLEM
    assert scenario.problem_v1.problem is not None
    assert scenario.relation_v1.status is FullModelStatus.AVAILABLE
    assert scenario.risk_v1.classification is RiskClassification.RISK_IDENTIFIED
    assert action is not None
    assert action.action_kind is CorrectiveActionKind.RECONCILE_QUANTITATIVE_BOUNDS

    assert scenario.observation_resolution_v1.observation.observed_value == OBSERVED_RESPONSE_TIME
    assert scenario.observation_resolution_v1.observation.source_kind is ObservationSourceKind.DETERMINISTIC_FIXTURE
    assert scenario.conformance_v1.outcome is ConformanceOutcome.CONFORMS
    qb_gate_v1 = next(
        item
        for item in scenario.feature_v1.features
        if item.feature_id is PerformanceEfficiencyFeatureId.SPECIFICATION_QB
    )
    assert qb_gate_v1.typed_value.gate_decision is QbTargetGateDecision.TARGET_CONFLICT
    assert scenario.quality_v1.status is FullModelStatus.UNRESOLVED
    assert scenario.quality_v1.value is None

    assert scenario.revision.provider_kind is ExternalRevisionProviderKind.CONTROLLED_REFERENCE_FIXTURE
    assert tuple(item.text for item in scenario.parent.requirements) == (V1_R001, V1_R002)
    assert tuple(item.text for item in scenario.child.requirements) == (V1_R001, V2_R002)
    assert scenario.child.artifact_ref != scenario.parent.artifact_ref
    assert tuple(item.lineage_id for item in scenario.child.requirements) == tuple(
        item.lineage_id for item in scenario.parent.requirements
    )
    assert tuple(item.lineage_id for item in scenario.child.changed_subjects) == (
        scenario.parent.requirements[1].lineage_id,
    )
    assert scenario.child.requirements[1].text == V2_R002

    assert scenario.reuse.decision is EvidenceReuseDisposition.REUSE_ALLOWED
    assert downstream_v2.observation_resolution.observation is scenario.observation_resolution_v1.observation
    assert tuple(item.extraction_result.requirement.text for item in core_v2.requirement_records) == (
        V1_R001,
        V2_R002,
    )
    assert qb_v2.state is QbConsistencyState.COMPUTED
    assert qb_v2.value == Fraction(1, 1)
    assert downstream_v2.target_problem_resolution.problem is None
    assert downstream_v2.target_problem_resolution.status is FullModelStatus.AVAILABLE
    assert downstream_v2.target_problem_resolution.disposition is (
        ProblemDisposition.NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE
    )
    assert downstream_v2.defect_quality_relation.status is FullModelStatus.NOT_APPLICABLE
    assert downstream_v2.risk_assessment.status is FullModelStatus.NOT_APPLICABLE
    assert downstream_v2.risk_assessment.classification is None
    assert downstream_v2.product_quality_assessment.status is FullModelStatus.AVAILABLE
    assert downstream_v2.product_quality_assessment.value == Fraction(1, 1)

    assert tuple(item.comparison_kind for item in scenario.comparisons) == (
        ComparisonKind.INCREASED,
        ComparisonKind.STATE_CHANGED,
        ComparisonKind.STATE_CHANGED,
        ComparisonKind.STATE_CHANGED,
    )
    assert scenario.comparisons[0].before_state_and_value.exact_value == Fraction(0, 1)
    assert scenario.comparisons[0].after_state_and_value.exact_value == Fraction(1, 1)
    assert scenario.comparisons[2].before_state_and_value.categorical_state == "RISK_IDENTIFIED"
    assert scenario.comparisons[2].after_state_and_value.status is FullModelStatus.NOT_APPLICABLE

    assert PROCESS_STAGE_MAPPING == (
        (ProcessStage.REFERENCE_VERIFICATION, DissertationStage.TAU_T),
    )
    assert scenario.process_v1.ref == scenario.process_v2.predecessor_process_state_ref
    assert scenario.process_v2.artifact_transition_ref_or_none.transition_id == scenario.application.transition.transition_id
    assert scenario.process_v2.reassessment_ref == scenario.reassessment.ref
    assert scenario.process_v2.provenance.comparison_refs
    assert scenario.process_transition.predecessor_process_state_ref == scenario.process_v1.ref
    assert scenario.process_transition.successor_process_state_ref == scenario.process_v2.ref
    process_fields = {field.name for field in fields(scenario.process_v2)}
    assert process_fields.isdisjoint(
        {"K_0", "checkpoint", "proceed", "release_decision", "process_score"}
    )

    assert (FULL_MODEL_CONTRACT_REF.contract_id, FULL_MODEL_CONTRACT_REF.version) == (
        "FULL-MODEL-V0.1-CONTRACT",
        "1",
    )
    assert (DYNAMIC_CONTRACT_REF.contract_id, DYNAMIC_CONTRACT_REF.version) == (
        "FULL-MODEL-V0.1-DYNAMIC-EVIDENCE",
        "1",
    )
    assert (FEATURE_CONTRACT_REF.contract_id, FEATURE_CONTRACT_REF.version) == (
        "FULL-MODEL-V0.1-PRODUCT-QUALITY-FEATURE",
        "1",
    )
    assert (ASSESSMENT_CONTRACT_REF.contract_id, ASSESSMENT_CONTRACT_REF.version) == (
        "FULL-MODEL-V0.1-PRODUCT-QUALITY-ASSESSMENT",
        "1",
    )
    assert (
        DEFECT_QUALITY_RISK_CONTRACT_REF.contract_id,
        DEFECT_QUALITY_RISK_CONTRACT_REF.version,
    ) == ("FULL-MODEL-V0.1-DEFECT-QUALITY-RISK", "1")
    assert (
        PROCESS_REASSESSMENT_CONTRACT_REF.contract_id,
        PROCESS_REASSESSMENT_CONTRACT_REF.version,
    ) == ("FULL-MODEL-V0.1-PROCESS-REASSESSMENT", "1")
    assert all(ref.explicit_version == "1" for ref in (
        BINDING_RULE_REF,
        EVALUATOR_RULE_REF,
        MAPPING_RULE_REF,
        PROCEDURE_RULE_REF,
        PROBLEM_RULE_REF,
        RELATION_RULE_REF,
        RISK_RULE_REF,
        ACTION_RULE_REF,
        APPLICATION_RULE_REF,
        REASSESSMENT_RULE_REF,
        COMPARISON_RULE_REF,
        PROCESS_RULE_REF,
    ))
    assert MODEL_REF.model_version == "1"
    assert RISK_MODEL_REF.model_version == "1"
    assert PARAMETER_SET.entries == ()
    assert RISK_PARAMETER_SET.entries == ()
    assert scenario.quality_v1.calibration_status is CalibrationStatus.PROVISIONAL_NOT_CALIBRATED

    user_report = UserFullModelReporter().render(scenario.report_bundle)
    audit_report = AuditFullModelReporter().render(scenario.report_bundle)
    assert UserFullModelReporter().render(scenario.report_bundle) == user_report
    assert AuditFullModelReporter().render(scenario.report_bundle) == audit_report
    assert sha256(user_report.encode("utf-8")).hexdigest() == (
        "27bc841fa93e9b297419ef9af5251399100ac0f8104f870c609335d1007d9314"
    )
    assert sha256(audit_report.encode("utf-8")).hexdigest() == (
        "daa7fe519ca2b1f3fcf9119f50a6b5676938c8932f36c2d19e64559fa51dc608"
    )
    for expected in (
        "QB consistency: 0/1 (state=COMPUTED; bounded=QB-v0.1)",
        "RISK_IDENTIFIED",
        "RECONCILE_QUANTITATIVE_BOUNDS",
        "provider=CONTROLLED_REFERENCE_FIXTURE",
        "S(v2) — QB consistency: 1/1 (state=COMPUTED)",
        "S(v2) — bounded PE indicator: 1/1 (status=AVAILABLE)",
        "comparison=INCREASED",
        "comparison=STATE_CHANGED",
        "stage=REFERENCE_VERIFICATION",
    ):
        assert expected in user_report
    for expected in (
        "Decimal('1.8')",
        "Fraction(0,1)",
        "Fraction(1,1)",
        "CONTROLLED_REFERENCE_FIXTURE",
        "REUSE_ALLOWED",
        "comparison_kind: INCREASED",
        "comparison_kind: STATE_CHANGED",
        "component_associations:",
        "evidence_associations:",
    ):
        assert expected in audit_report
    forbidden_claims = (
        "improved",
        "worsened",
        "safer",
        "risk reduced",
        "successful correction",
        "product quality improved",
        "causal effect",
    )
    assert not any(claim in user_report.lower() for claim in forbidden_claims)

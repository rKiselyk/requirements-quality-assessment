from dataclasses import fields, replace
from decimal import Decimal
from enum import Enum

import pytest

from requirements_quality_assessment.corrective_action import (
    PROCESS_REASSESSMENT_CONTRACT_REF,
)
from requirements_quality_assessment.cross_analysis import CrossObservationRef
from requirements_quality_assessment.domain import FeatureId, UnitLabel
from requirements_quality_assessment.dynamic_evidence import (
    DYNAMIC_CONTRACT_REF,
    RESPONSE_TIME_METRIC_REF,
    SUPPORTED_CONTEXT_IDENTITY,
    Applicability,
    DynamicEvidenceAssessmentRef,
    EnvironmentRef,
    FullModelStatus,
    ObservationCollectionRef,
    ObservationSlotRef,
    ObservationSourceKind,
    ProductRef,
    make_dynamic_observation,
)
from requirements_quality_assessment.dynamic_evidence.domain import DynamicObservationRef
from requirements_quality_assessment.metrics import (
    FULL_MODEL_CONTRACT_REF,
    AssessmentRef,
    RequirementSubjectRef,
)
from requirements_quality_assessment.performance_efficiency import (
    ProcessStage,
    ProcessStateRef,
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
    ProcessStateTransition,
    RequirementAssessmentRef,
    SpecificationAssessmentRef,
    assemble_process_state,
    assemble_process_transition,
)
from requirements_quality_assessment.product_quality import ProductQualityAssessmentEventRef
from requirements_quality_assessment.reassessment import (
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
    reevaluate,
)
from requirements_quality_assessment.risk import RiskAssessmentEventRef

from test_corrective_action import _positive
from test_defect_quality_mapping import UPPER_TWO
from test_performance_efficiency_features import _build, _bundle
from test_versioned_reassessment import _application_bundle


class _AbsenceReason(str, Enum):
    NOT_PRODUCED = "NOT_PRODUCED"


COMPONENT_VERSIONS = ComponentVersionSet(
    (
        VersionedComponentRef("FULL_MODEL_CONTRACT", "FULL-MODEL-V0.1-CONTRACT", "1"),
        VersionedComponentRef("PROCESS_RULE", "PROCESS-REFERENCE-VERIFICATION-001", "1"),
    )
)


def _available_component(role, result_ref, scope):
    return ProcessComponentAssociation(
        role,
        result_ref,
        FullModelStatus.AVAILABLE,
        Applicability.APPLICABLE,
        scope,
        FULL_MODEL_CONTRACT_REF,
        (),
        (result_ref,),
    )


def _absent_component(role, scope, status=FullModelStatus.NOT_APPLICABLE):
    applicability = (
        Applicability.NOT_APPLICABLE
        if status is FullModelStatus.NOT_APPLICABLE
        else Applicability.UNKNOWN
    )
    return ProcessComponentAssociation(
        role,
        None,
        status,
        applicability,
        scope,
        FULL_MODEL_CONTRACT_REF,
        (_AbsenceReason.NOT_PRODUCED,),
        (scope,),
    )


def _evidence(artifact, product):
    values = []
    for role in ProcessEvidenceRole:
        subject = product if role is ProcessEvidenceRole.DYNAMIC_OBSERVATION else artifact
        evidence_ref = (role.value, "EVIDENCE")
        values.append(
            ProcessEvidenceAssociation(
                role,
                evidence_ref,
                FullModelStatus.AVAILABLE,
                Applicability.APPLICABLE,
                subject,
                (role.value, "SOURCE"),
                None,
                None,
                (),
                (evidence_ref,),
            )
        )
    return tuple(values)


def _v1_assembly():
    bundle, risk, resolution = _positive()
    source, quality, problem_resolution, population, relation, _ = bundle
    action = resolution.action
    feature_bundle = _bundle(observed_value=Decimal("1.8"))
    feature_profile = _build(feature_bundle)
    metric_profile = feature_bundle[1]
    artifact = risk.artifact_ref
    assessment = risk.source_assessment_ref
    process_ref = risk.process_state_ref
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
    specification_ref = SpecificationAssessmentRef(assessment, source.snapshot_id)
    quality_ref = risk.product_quality_context.assessment_ref
    problem_refs = (problem_resolution.problem.ref,)
    relation_refs = (relation.ref,)
    risk_refs = (risk.ref,)
    action_refs = (action.ref,)
    component_associations = (
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
            metric_profile.profile_id,
            artifact,
        ),
        _available_component(
            ProcessComponentRole.PE_FEATURE_PROFILE,
            feature_profile.profile_id,
            feature_profile.product_ref,
        ),
        _available_component(
            ProcessComponentRole.PRODUCT_QUALITY_ASSESSMENT,
            quality_ref,
            quality.product_ref,
        ),
        _available_component(
            ProcessComponentRole.DEFECT_POPULATION,
            population.ref,
            artifact,
        ),
        _available_component(
            ProcessComponentRole.CONFIRMED_PROBLEM,
            problem_refs[0],
            artifact,
        ),
        _available_component(
            ProcessComponentRole.DEFECT_QUALITY_RELATION,
            relation_refs[0],
            artifact,
        ),
        _available_component(
            ProcessComponentRole.BOUNDED_RISK_ASSESSMENT,
            risk_refs[0],
            artifact,
        ),
        _available_component(
            ProcessComponentRole.CORRECTIVE_ACTION,
            action_refs[0],
            artifact,
        ),
    )
    assembly = ProcessStateAssembly(
        process_ref.process_state_id,
        artifact,
        assessment,
        FULL_MODEL_CONTRACT_REF,
        COMPONENT_VERSIONS,
        _evidence(artifact, quality.product_ref),
        component_associations,
        requirement_refs,
        specification_ref,
        metric_profile.profile_id,
        feature_profile.profile_id,
        quality_ref,
        population.ref,
        problem_refs,
        relation_refs,
        risk_refs,
        action_refs,
    )
    return process_ref, assembly


def _v2_reassessment():
    action, parent, _, application = _application_bundle()
    child = application.child_specification
    predecessor = ProcessStateRef(
        "PROCESS-PE-001", "1", ProcessStage.REFERENCE_VERIFICATION
    )
    child_process = ProcessStateRef(
        "PROCESS-PE-001", "2", ProcessStage.REFERENCE_VERIFICATION
    )
    product = ProductRef("PRODUCT-REF", "1")
    collection = ObservationCollectionRef(
        "COLLECTION-REF",
        "1",
        product,
        EnvironmentRef("ENV-REF", "1"),
        ObservationSourceKind.DETERMINISTIC_FIXTURE,
    )
    slot = ObservationSlotRef(collection, 0)
    observation = make_dynamic_observation(
        slot,
        RESPONSE_TIME_METRIC_REF,
        Decimal("1.8"),
        UnitLabel.SECOND,
        SUPPORTED_CONTEXT_IDENTITY,
        "OBSERVATION-REF-001",
    )
    exact_values = (
        ("product_ref", observation.product_ref),
        ("observation_source_kind", observation.source_kind),
        ("collection_ref", observation.collection_ref),
        ("metric_ref", observation.metric_ref),
        ("unit", observation.unit),
        ("context_identity", observation.context_identity),
        ("applicability", Applicability.APPLICABLE),
        ("process_stage", child_process.stage),
        ("source_contract_permission", True),
    )
    reuse = EvidenceReuseDecision(
        DynamicObservationRef(observation.observation_id),
        child_process,
        EvidenceReuseDisposition.REUSE_ALLOWED,
        tuple(ExactIdentityCheck(name, value, value, True) for name, value in exact_values),
        (EvidenceReuseReason.EXACT_IDENTITY_AND_CONTEXT_MATCH,),
        EvidenceReuseProvenance(predecessor, child_process, DYNAMIC_CONTRACT_REF),
    )
    child_assessment = AssessmentRef("ASSESS-FULL-REF", "v2", child.artifact_ref)
    versions = ComponentVersionSet(
        (VersionedComponentRef("FULL_MODEL_PATH", "FULL-MODEL-V0.1", "1"),)
    )
    context = ReassessmentContext(
        predecessor,
        application.ref,
        parent.artifact_ref,
        child.artifact_ref,
        child_assessment,
        FULL_MODEL_CONTRACT_REF,
        versions,
        (reuse,),
        ProcessStage.REFERENCE_VERIFICATION,
    )
    dynamic_ref = DynamicEvidenceAssessmentRef(
        "DYNAMIC-ASSESSMENT-REF",
        "v2",
        child.artifact_ref,
        product,
        collection,
    )
    inputs = ReferenceFullModelReassessmentInputs(
        action.target_requirements[0].lineage_id,
        CrossObservationRef(
            child.requirements[0].subject_ref.requirement_id,
            FeatureId.QUANTITATIVE_CONSTRAINT,
            0,
        ),
        slot,
        observation,
        DynamicObservationUse.EXPLICIT_REUSE,
        reuse,
        dynamic_ref,
        ProductQualityAssessmentEventRef(
            "PRODUCT-QUALITY-EVENT-REF",
            "v2",
            product,
            child.artifact_ref,
        ),
        RiskAssessmentEventRef(
            "RISK-EVENT-REF",
            "v2",
            child.artifact_ref,
            child_process,
        ),
        tuple(item.lineage_id for item in action.target_requirements),
        action.comparison_key,
    )
    run = reevaluate(
        child,
        context,
        ReassessmentIdentityContext("REEVAL-FULL-REF", "1", child_process),
        ReferenceFullModelDownstreamRebuilder(inputs),
    )
    return parent, application, run, reuse


def _v2_assembly():
    parent, application, run, reuse = _v2_reassessment()
    process_ref = run.child_process_state_ref
    core = run.produced_results[0]
    downstream = run.produced_results[1]
    artifact = run.context.child_artifact_ref
    assessment = run.context.child_assessment_ref
    source = core.specification_assessment
    requirement_refs = tuple(
        RequirementAssessmentRef(
            assessment,
            RequirementSubjectRef(
                artifact,
                record.extraction_result.requirement.id,
                record.extraction_result.requirement.source_line,
            ),
        )
        for record in core.requirement_records
    )
    specification_ref = SpecificationAssessmentRef(assessment, source.snapshot_id)
    feature_ref = downstream.feature_profile.profile_id
    quality_ref = downstream.risk_assessment.product_quality_context.assessment_ref
    population_ref = downstream.defect_population.ref
    relation_ref = downstream.defect_quality_relation.ref
    risk_ref = downstream.risk_assessment.ref
    action_ref = application.action_after_ref
    component_associations = (
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
            core.metric_profile.profile_id,
            artifact,
        ),
        ProcessComponentAssociation(
            ProcessComponentRole.PE_FEATURE_PROFILE,
            feature_ref,
            downstream.feature_profile.status,
            downstream.feature_profile.applicability,
            downstream.feature_profile.product_ref,
            FULL_MODEL_CONTRACT_REF,
            (),
            (feature_ref,),
        ),
        ProcessComponentAssociation(
            ProcessComponentRole.PRODUCT_QUALITY_ASSESSMENT,
            quality_ref,
            downstream.product_quality_assessment.status,
            downstream.product_quality_assessment.applicability,
            downstream.product_quality_assessment.product_ref,
            FULL_MODEL_CONTRACT_REF,
            (),
            (quality_ref,),
        ),
        _available_component(
            ProcessComponentRole.DEFECT_POPULATION,
            population_ref,
            artifact,
        ),
        _absent_component(ProcessComponentRole.CONFIRMED_PROBLEM, artifact),
        ProcessComponentAssociation(
            ProcessComponentRole.DEFECT_QUALITY_RELATION,
            relation_ref,
            downstream.defect_quality_relation.status,
            downstream.defect_quality_relation.applicability,
            artifact,
            downstream.defect_quality_relation.rule_ref,
            downstream.defect_quality_relation.reasons,
            (relation_ref,),
        ),
        ProcessComponentAssociation(
            ProcessComponentRole.BOUNDED_RISK_ASSESSMENT,
            risk_ref,
            downstream.risk_assessment.status,
            downstream.risk_assessment.applicability,
            artifact,
            downstream.risk_assessment.rule_ref,
            (),
            (risk_ref,),
        ),
        _available_component(
            ProcessComponentRole.CORRECTIVE_ACTION,
            action_ref,
            artifact,
        ),
    )
    evidence = tuple(
        replace(
            item,
            reuse_decision_ref_or_none=(
                reuse
                if item.role is ProcessEvidenceRole.DYNAMIC_OBSERVATION
                else None
            ),
        )
        for item in _evidence(artifact, downstream.feature_profile.product_ref)
    )
    assembly = ProcessStateAssembly(
        process_ref.process_state_id,
        artifact,
        assessment,
        FULL_MODEL_CONTRACT_REF,
        run.context.component_version_set,
        evidence,
        component_associations,
        requirement_refs,
        specification_ref,
        core.metric_profile.profile_id,
        feature_ref,
        quality_ref,
        population_ref,
        (),
        (relation_ref,),
        (risk_ref,),
        (action_ref,),
        run.context.predecessor_process_state_ref,
        application.transition,
        application,
        run,
        (),
    )
    return parent, application, run, process_ref, assembly


def _without_optional_downstream(assembly):
    omitted = {
        ProcessComponentRole.PE_FEATURE_PROFILE,
        ProcessComponentRole.PRODUCT_QUALITY_ASSESSMENT,
        ProcessComponentRole.CONFIRMED_PROBLEM,
        ProcessComponentRole.DEFECT_QUALITY_RELATION,
        ProcessComponentRole.BOUNDED_RISK_ASSESSMENT,
        ProcessComponentRole.CORRECTIVE_ACTION,
    }
    associations = []
    replaced_roles = set()
    for item in assembly.component_associations:
        if item.role not in omitted:
            associations.append(item)
        elif item.role not in replaced_roles:
            associations.append(_absent_component(item.role, item.subject_or_scope_ref))
            replaced_roles.add(item.role)
    return replace(
        assembly,
        component_associations=tuple(associations),
        pe_feature_profile_ref=None,
        product_quality_assessment_ref=None,
        confirmed_problem_refs=(),
        defect_quality_relation_refs=(),
        bounded_risk_assessment_refs=(),
        corrective_action_refs=(),
    )


def test_valid_v1_state_assembly_is_exact_deterministic_and_immutable() -> None:
    reserved_ref, assembly = _v1_assembly()

    first = assemble_process_state(reserved_ref, assembly)
    second = assemble_process_state(reserved_ref, assembly)

    assert first == second
    assert first.ref == reserved_ref
    assert first.process_lineage_id == reserved_ref.process_state_id
    assert first.artifact_ref == assembly.artifact_ref
    assert first.assessment_ref == assembly.assessment_ref
    assert first.component_version_set is assembly.component_version_set
    assert first.evidence_associations is assembly.evidence_associations
    assert first.provenance.process_state_ref == reserved_ref
    with pytest.raises(Exception):
        first.process_state_version = "changed"


def test_valid_v2_state_preserves_reassessment_application_and_transition_lineage() -> None:
    parent, application, run, reserved_ref, assembly = _v2_assembly()

    state = assemble_process_state(reserved_ref, assembly)

    assert state.ref == reserved_ref == run.child_process_state_ref
    assert state.predecessor_process_state_ref == run.context.predecessor_process_state_ref
    assert state.artifact_ref == application.child_artifact_ref
    assert state.artifact_transition_ref_or_none.transition_id == (
        application.transition.transition_id
    )
    assert state.reassessment_ref == run.ref
    assert state.provenance.action_application_ref_or_none == application.ref
    assert state.provenance.reassessment_ref_or_none == run.ref
    assert state.provenance.component_version_set == run.context.component_version_set
    assert state.provenance.evidence_associations[-2].reuse_decision_ref_or_none is not None
    assert application.parent_artifact_ref == parent.artifact_ref


def test_v2_transition_is_separate_and_does_not_mutate_v1() -> None:
    _, application, _, child_ref, child_assembly = _v2_assembly()
    baseline_ref, baseline_assembly = _v1_assembly()
    baseline_state = assemble_process_state(baseline_ref, baseline_assembly)
    baseline_before = baseline_state
    child_state = assemble_process_state(child_ref, child_assembly)
    transition = assemble_process_transition(
        "PROCESS-TRANSITION", baseline_state, child_state
    )

    assert isinstance(transition, ProcessStateTransition)
    assert transition.predecessor_process_state_ref == baseline_state.ref
    assert transition.successor_process_state_ref == child_state.ref
    assert transition.action_application_ref == application.ref
    assert baseline_state == baseline_before


def test_v2_mixed_process_and_reassessment_lineage_fail_closed() -> None:
    _, _, run, reserved_ref, assembly = _v2_assembly()

    with pytest.raises(ValueError, match="process state"):
        assemble_process_state(
            replace(reserved_ref, process_state_version="v3"),
            replace(assembly, process_lineage_id=reserved_ref.process_state_id),
        )
    with pytest.raises(ValueError, match="assessment"):
        assemble_process_state(
            reserved_ref,
            replace(
                assembly,
                assessment_ref=replace(
                    run.context.child_assessment_ref,
                    assessment_version="other",
                ),
            ),
        )


def test_exact_reference_verification_tau_t_mapping_and_closed_rule() -> None:
    assert PROCESS_STAGE_MAPPING == (
        (ProcessStage.REFERENCE_VERIFICATION, DissertationStage.TAU_T),
    )
    assert DissertationStage.TAU_T.value == "τ^T"
    assert (PROCESS_RULE_REF.rule_id, PROCESS_RULE_REF.explicit_version) == (
        "PROCESS-REFERENCE-VERIFICATION-001",
        "1",
    )
    assert PROCESS_REASSESSMENT_CONTRACT_REF.version == "1"


def test_optional_components_remain_typed_absence_not_zero() -> None:
    reserved_ref, assembly = _v1_assembly()
    state = assemble_process_state(reserved_ref, _without_optional_downstream(assembly))

    assert state.pe_feature_profile_ref is None
    assert state.product_quality_assessment_ref is None
    absent = tuple(
        item
        for item in state.component_associations
        if item.role
        in {
            ProcessComponentRole.PE_FEATURE_PROFILE,
            ProcessComponentRole.PRODUCT_QUALITY_ASSESSMENT,
        }
    )
    assert all(item.status is FullModelStatus.NOT_APPLICABLE for item in absent)
    assert all(item.result_ref is None for item in absent)
    assert all(item.reason_codes == (_AbsenceReason.NOT_PRODUCED,) for item in absent)
    assert not any(item.result_ref == 0 for item in absent)


def test_mixed_artifact_assessment_and_process_state_fail_closed() -> None:
    reserved_ref, assembly = _v1_assembly()
    foreign_artifact = replace(assembly.artifact_ref, artifact_version="foreign")
    foreign_assessment = AssessmentRef("ASSESS-FOREIGN", "1", foreign_artifact)

    with pytest.raises(ValueError, match="assessment ref"):
        assemble_process_state(
            reserved_ref,
            replace(assembly, artifact_ref=foreign_artifact),
        )
    with pytest.raises(ValueError, match="assessment ref"):
        assemble_process_state(
            reserved_ref,
            replace(assembly, assessment_ref=foreign_assessment),
        )
    with pytest.raises(ValueError, match="X_PE"):
        assemble_process_state(
            replace(reserved_ref, process_state_version="foreign"),
            assembly,
        )


def test_unsupported_stage_fails_closed_even_if_a_ref_is_forged() -> None:
    reserved_ref, assembly = _v1_assembly()
    forged = object.__new__(ProcessStateRef)
    object.__setattr__(forged, "process_state_id", reserved_ref.process_state_id)
    object.__setattr__(forged, "process_state_version", reserved_ref.process_state_version)
    object.__setattr__(forged, "stage", "REQUIREMENTS")

    with pytest.raises(ValueError, match="REFERENCE_VERIFICATION"):
        assemble_process_state(forged, assembly)


def test_every_component_role_is_required_and_convenience_refs_must_match() -> None:
    reserved_ref, assembly = _v1_assembly()

    with pytest.raises(ValueError, match="every component role"):
        assemble_process_state(
            reserved_ref,
            replace(
                assembly,
                component_associations=tuple(
                    item
                    for item in assembly.component_associations
                    if item.role is not ProcessComponentRole.CORRECTIVE_ACTION
                ),
            ),
        )
    with pytest.raises(ValueError, match="convenience refs"):
        assemble_process_state(
            reserved_ref,
            replace(assembly, corrective_action_refs=()),
        )


def test_process_state_has_no_checkpoint_decision_score_or_reporting_fields() -> None:
    reserved_ref, assembly = _v1_assembly()
    state = assemble_process_state(reserved_ref, assembly)
    names = {item.name for item in fields(state)}

    assert names.isdisjoint(
        {
            "checkpoint",
            "checkpoint_threshold",
            "critical_risk",
            "proceed",
            "release_decision",
            "process_score",
            "report",
            "rendered_output",
        }
    )


def test_assembly_module_imports_no_calculator_risk_action_or_report_service() -> None:
    import requirements_quality_assessment.process.service as service

    assert not {
        "RequirementQualityAssessor",
        "PerformanceEfficiencyQualityAssessor",
        "RiskAssessor",
        "propose_corrective_action",
        "compare",
        "ConsoleReporter",
    }.intersection(vars(service))

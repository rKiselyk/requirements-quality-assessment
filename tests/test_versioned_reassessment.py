from dataclasses import replace
from decimal import Decimal
from fractions import Fraction

import pytest

from requirements_quality_assessment.corrective_action import (
    APPLICATION_RULE_REF,
    ActionApplicationReason,
    ApplicationIdentityContext,
    ExternalProviderRef,
    ExternalRevisionProvenance,
    ExternalRevisionProviderKind,
    ExternallySuppliedRevision,
    RequirementLineageId,
    RequirementTextReplacement,
    RevisionRef,
    apply_external_revision,
    create_initial_specification_version,
)
from requirements_quality_assessment.cross_analysis import CrossObservationRef
from requirements_quality_assessment.domain import FeatureId, Requirement, UnitLabel
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
    ArtifactRef,
    AssessmentRef,
    MetricId,
)
from requirements_quality_assessment.performance_efficiency import (
    ProcessStage,
    ProcessStateRef,
)
from requirements_quality_assessment.product_quality import (
    ProductQualityAssessmentEventRef,
)
from requirements_quality_assessment.reassessment import (
    AssessmentResultRef,
    ComponentVersionSet,
    DownstreamReassessmentResults,
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
from test_defect_quality_mapping import LOWER_FIVE, UPPER_TWO


REVISED_LOWER = "Час відгуку ≤ 5 с при 500 одночасних користувачах"


def _application_bundle(replacement_text=REVISED_LOWER):
    _, _, resolution = _positive()
    action = resolution.action
    requirements = tuple(
        Requirement(
            target.subject_ref.requirement_id,
            target.subject_ref.source_line,
            text,
        )
        for target, text in zip(
            action.target_requirements,
            (UPPER_TWO, LOWER_FIVE),
            strict=True,
        )
    )
    parent = create_initial_specification_version(action.target_artifact_ref, requirements)
    child_ref = ArtifactRef(action.target_artifact_ref.artifact_id, "fixture-child-v2")
    revision_ref = RevisionRef("REV-REF-001", "fixture-revision-v1")
    provider_ref = ExternalProviderRef("QB-CONFLICT-REFERENCE", "1")
    replacement = RequirementTextReplacement(
        action.target_requirements[1].lineage_id,
        action.target_requirements[1].subject_ref,
        replacement_text,
    )
    provenance = ExternalRevisionProvenance(
        revision_ref,
        action.ref,
        parent.artifact_ref,
        child_ref,
        provider_ref,
    )
    revision = ExternallySuppliedRevision(
        revision_ref.revision_id,
        revision_ref.revision_version,
        ExternalRevisionProviderKind.CONTROLLED_REFERENCE_FIXTURE,
        provider_ref,
        action.ref,
        parent.artifact_ref,
        child_ref,
        (replacement,),
        "Controlled QB conflict reference scenario",
        provenance,
    )
    application = apply_external_revision(
        action,
        revision,
        parent,
        ApplicationIdentityContext(
            "APP-REF-001",
            "application-record-v1",
            "applied-action-record-v2",
            "TRANSITION-REF-001",
        ),
    )
    return action, parent, revision, application


def test_controlled_external_revision_creates_distinct_immutable_child() -> None:
    action, parent, revision, application = _application_bundle()

    assert parent.artifact_ref == action.target_artifact_ref
    assert application.parent_artifact_ref == parent.artifact_ref
    assert application.child_artifact_ref == revision.requested_child_artifact_ref
    assert application.child_artifact_ref != parent.artifact_ref
    assert application.child_specification.parent_artifact_ref == parent.artifact_ref
    assert application.child_specification.created_by_application_ref == application.ref
    assert application.transition.action_application_ref == application.ref
    assert application.rule_ref == APPLICATION_RULE_REF
    assert application.status is FullModelStatus.AVAILABLE
    assert application.reason_codes == (
        ActionApplicationReason.EXTERNAL_REVISION_MATERIALIZED,
    )


def test_parent_is_unchanged_lineage_is_stable_and_text_is_exact() -> None:
    _, parent, _, application = _application_bundle("Час відгуку ≤ 5 с; точно!")
    parent_before = parent
    child = application.child_specification

    assert parent == parent_before
    assert tuple(item.text for item in parent.requirements) == (UPPER_TWO, LOWER_FIVE)
    assert tuple(item.lineage_id for item in child.requirements) == tuple(
        item.lineage_id for item in parent.requirements
    )
    assert child.requirements[0].text == parent.requirements[0].text
    assert child.requirements[1].text == "Час відгуку ≤ 5 с; точно!"
    assert child.requirements[1].predecessor_subject_ref == parent.requirements[1].subject_ref
    assert application.changed_subjects == child.changed_subjects
    assert tuple(item.lineage_id for item in child.changed_subjects) == (
        parent.requirements[1].lineage_id,
    )


def test_application_creates_a_distinct_applied_action_record() -> None:
    action, _, revision, application = _application_bundle()
    applied = application.applied_action

    assert action.status.value == "PROPOSED"
    assert applied.status.value == "APPLIED"
    assert applied.action_id == action.action_id
    assert applied.action_record_version != action.action_record_version
    assert applied.predecessor_action_ref == action.ref
    assert applied.external_revision_ref == revision.ref
    assert applied.application_ref == application.ref


def test_non_target_wrong_subject_parent_or_action_fails_closed() -> None:
    action, parent, revision, _ = _application_bundle()
    identity = ApplicationIdentityContext("APP-X", "1", "2", "TRANS-X")
    foreign_lineage = RequirementLineageId(
        parent.artifact_ref.artifact_id,
        parent.artifact_ref.artifact_version,
        "R999",
        999,
    )
    foreign = RequirementTextReplacement(
        foreign_lineage,
        revision.replacements[0].expected_parent_subject_ref,
        "Зовнішній текст",
    )
    foreign_revision = replace(
        revision,
        replacements=(foreign,),
        provenance=replace(revision.provenance),
    )
    with pytest.raises(ValueError, match="target"):
        apply_external_revision(action, foreign_revision, parent, identity)

    wrong_subject = replace(
        revision.replacements[0],
        expected_parent_subject_ref=parent.requirements[0].subject_ref,
    )
    with pytest.raises(ValueError, match="expected subject"):
        apply_external_revision(
            action,
            replace(revision, replacements=(wrong_subject,)),
            parent,
            identity,
        )

    other_parent = create_initial_specification_version(
        ArtifactRef(parent.artifact_ref.artifact_id, "other"),
        tuple(
            Requirement(
                item.subject_ref.requirement_id,
                item.subject_ref.source_line,
                item.text,
            )
            for item in parent.requirements
        ),
    )
    with pytest.raises(ValueError, match="parent"):
        apply_external_revision(
            action,
            revision,
            other_parent,
            identity,
        )

    with pytest.raises(ValueError, match="action"):
        apply_external_revision(
            replace(action, action_record_version="different-proposal"),
            revision,
            parent,
            identity,
        )


def test_revision_shape_rejects_trimming_and_embedded_lines() -> None:
    _, _, _, application = _application_bundle()
    lineage = application.child_specification.requirements[0].lineage_id
    subject = application.transition.changed_subjects[0].before_subject_ref

    with pytest.raises(ValueError, match="trimmed"):
        RequirementTextReplacement(lineage, subject, " padded ")
    with pytest.raises(ValueError, match="line break"):
        RequirementTextReplacement(lineage, subject, "one\ntwo")


def test_reevaluation_rebuilds_the_controlled_child_not_v1_cached_values() -> None:
    _, parent, _, application = _application_bundle()
    child = application.child_specification
    child_assessment = AssessmentRef("ASSESS-REF", "child-assessment-v2", child.artifact_ref)
    predecessor_process = ProcessStateRef(
        "PROCESS-REF", "process-v1", ProcessStage.REFERENCE_VERIFICATION
    )
    child_process = ProcessStateRef(
        "PROCESS-REF", "process-v2", ProcessStage.REFERENCE_VERIFICATION
    )
    context = ReassessmentContext(
        predecessor_process,
        application.ref,
        parent.artifact_ref,
        child.artifact_ref,
        child_assessment,
        FULL_MODEL_CONTRACT_REF,
        ComponentVersionSet(
            (
                VersionedComponentRef("FULL_MODEL_PATH", "FULL-MODEL-V0.1", "1"),
            )
        ),
        (),
        ProcessStage.REFERENCE_VERIFICATION,
    )

    def downstream(core, supplied_context, supplied_process):
        assert supplied_context is context
        assert supplied_process == child_process
        assert tuple(
            item.extraction_result.requirement.text
            for item in core.requirement_records
        ) == (UPPER_TWO, REVISED_LOWER)
        qb_entry = next(
            item
            for item in core.metric_profile.entries
            if item.metric_id is MetricId.SPEC_QB_CONSISTENCY
        )
        assert qb_entry.value == Fraction(1, 1)
        return DownstreamReassessmentResults(
            (qb_entry,),
            (
                AssessmentResultRef(
                    "DOWNSTREAM-CURRENT-EVIDENCE-MARKER",
                    qb_entry.entry_id,
                    child.artifact_ref,
                ),
            ),
        )

    identity = ReassessmentIdentityContext("REEVAL-REF-001", "1", child_process)
    first = reevaluate(child, context, identity, downstream)
    second = reevaluate(child, context, identity, downstream)

    assert first == second
    assert first.status is FullModelStatus.AVAILABLE
    assert first.context.child_artifact_ref == child.artifact_ref
    assert first.provenance.parent_artifact_ref == parent.artifact_ref
    assert first.provenance.action_application_ref == application.ref
    assert first.produced_result_refs == second.produced_result_refs
    assert first.produced_results[0].specification_version == child


def test_reference_reassessment_rebuilds_dynamic_through_risk_path() -> None:
    action, parent, _, application = _application_bundle()
    child = application.child_specification
    predecessor_process = ProcessStateRef(
        "PROCESS-FULL-REF", "v1", ProcessStage.REFERENCE_VERIFICATION
    )
    child_process = ProcessStateRef(
        "PROCESS-FULL-REF", "v2", ProcessStage.REFERENCE_VERIFICATION
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
        EvidenceReuseProvenance(
            predecessor_process,
            child_process,
            DYNAMIC_CONTRACT_REF,
        ),
    )
    child_assessment = AssessmentRef("ASSESS-FULL-REF", "v2", child.artifact_ref)
    context = ReassessmentContext(
        predecessor_process,
        application.ref,
        parent.artifact_ref,
        child.artifact_ref,
        child_assessment,
        FULL_MODEL_CONTRACT_REF,
        ComponentVersionSet(
            (VersionedComponentRef("FULL_MODEL_PATH", "FULL-MODEL-V0.1", "1"),)
        ),
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
    downstream = run.produced_results[1]

    assert downstream.observation_resolution.observation is observation
    assert downstream.product_quality_assessment.value == Fraction(1, 1)
    assert downstream.target_problem_resolution.problem is None
    assert downstream.risk_assessment.status is FullModelStatus.NOT_APPLICABLE
    assert downstream.risk_assessment.classification is None
    assert downstream.risk_assessment.artifact_ref == child.artifact_ref


def test_reassessment_rejects_parent_artifact_and_cached_v1_result_refs() -> None:
    _, parent, _, application = _application_bundle()
    child = application.child_specification
    context = ReassessmentContext(
        ProcessStateRef("PROCESS", "1", ProcessStage.REFERENCE_VERIFICATION),
        application.ref,
        parent.artifact_ref,
        child.artifact_ref,
        AssessmentRef("ASSESS", "2", child.artifact_ref),
        FULL_MODEL_CONTRACT_REF,
        ComponentVersionSet((VersionedComponentRef("PATH", "FULL", "1"),)),
        (),
        ProcessStage.REFERENCE_VERIFICATION,
    )
    identity = ReassessmentIdentityContext(
        "REEVAL", "1", ProcessStateRef("PROCESS", "2", ProcessStage.REFERENCE_VERIFICATION)
    )

    def stale(*_):
        return DownstreamReassessmentResults(
            (object(),),
            (AssessmentResultRef("STALE", "v1-result", parent.artifact_ref),),
        )

    with pytest.raises(ValueError, match="v1"):
        reevaluate(child, context, identity, stale)


def test_m3_09_records_do_not_assemble_m3_10_process_state() -> None:
    _, _, _, application = _application_bundle()

    assert not hasattr(application, "process_assessment_state")
    assert not hasattr(application.child_specification, "process_components")

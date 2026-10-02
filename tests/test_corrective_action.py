from dataclasses import fields, replace

import pytest

from requirements_quality_assessment.corrective_action import (
    ACTION_RECORD_VERSION,
    ACTION_RULE_REF,
    PROCESS_REASSESSMENT_CONTRACT_REF,
    VERIFICATION_RULE_REF,
    ActionCreatorSource,
    CorrectiveAction,
    CorrectiveActionContext,
    CorrectiveActionExpectedOutcome,
    CorrectiveActionKind,
    CorrectiveActionNonOptimalityClaim,
    CorrectiveActionReason,
    CorrectiveActionStatus,
    ProposedChangeKind,
    RequirementLineageId,
    propose_corrective_action,
)
from requirements_quality_assessment.dynamic_evidence import (
    Applicability,
    FullModelStatus,
)
from requirements_quality_assessment.metrics import ArtifactRef, AssessmentRef
from requirements_quality_assessment.performance_efficiency import ProcessStateRef

from test_defect_quality_mapping import LOWER_FIVE, UPPER_FIVE, UPPER_TWO
from test_risk_assessment import _assessed, _risk_bundle


def _lineages(risk):
    return tuple(
        RequirementLineageId(
            item.artifact_ref.artifact_id,
            item.artifact_ref.artifact_version,
            item.requirement_id,
            item.source_line,
        )
        for item in risk.subject.participant_refs
    )


def _context(risk, *, lineages=None, requested_action_kind=None):
    kwargs = {}
    if requested_action_kind is not None:
        kwargs["requested_action_kind"] = requested_action_kind
    return CorrectiveActionContext(
        action_instance_id="A-REF-001",
        action_record_version=ACTION_RECORD_VERSION,
        creator_source=ActionCreatorSource("CORRECTIVE-ACTION-PROPOSER", "1"),
        target_artifact_ref=risk.artifact_ref,
        target_requirement_lineages=(
            _lineages(risk) if lineages is None else lineages
        ),
        source_assessment_ref=risk.source_assessment_ref,
        source_snapshot_id=risk.source_snapshot_id,
        process_state_ref=risk.process_state_ref,
        **kwargs,
    )


def _positive():
    bundle = _risk_bundle()
    risk = _assessed(bundle)
    return bundle, risk, propose_corrective_action(
        risk,
        bundle[2].problem,
        bundle[4],
        _context(risk),
    )


def test_risk_identified_produces_exact_approved_proposal() -> None:
    bundle, risk, resolution = _positive()
    action = resolution.action

    assert resolution.status is FullModelStatus.AVAILABLE
    assert resolution.applicability is Applicability.APPLICABLE
    assert resolution.reason_codes == (
        CorrectiveActionReason.ELIGIBLE_RISK_IDENTIFIED,
    )
    assert action is not None
    assert action.action_kind is CorrectiveActionKind.RECONCILE_QUANTITATIVE_BOUNDS
    assert action.status is CorrectiveActionStatus.PROPOSED
    assert action.proposed_change_kind is ProposedChangeKind.REPLACE_REQUIREMENT_TEXT
    assert action.rule_ref == ACTION_RULE_REF
    assert action.verification_rule_ref == VERIFICATION_RULE_REF
    assert resolution.action_ref == action.ref
    assert action.originating_risk_ref == risk.ref
    assert action.originating_problem_ref == bundle[2].problem.ref
    assert action.originating_relation_ref == bundle[4].ref


def test_exact_contract_rule_model_and_version_references_are_preserved() -> None:
    _, risk, resolution = _positive()
    action = resolution.action

    assert action is not None
    assert (ACTION_RULE_REF.rule_id, ACTION_RULE_REF.explicit_version) == (
        "ACTION-RECONCILE-QB-001",
        "1",
    )
    assert (
        PROCESS_REASSESSMENT_CONTRACT_REF.contract_id,
        PROCESS_REASSESSMENT_CONTRACT_REF.version,
    ) == ("FULL-MODEL-V0.1-PROCESS-REASSESSMENT", "1")
    assert (VERIFICATION_RULE_REF.rule_id, VERIFICATION_RULE_REF.explicit_version) == (
        "REEVAL-FULL-MODEL-001",
        "1",
    )
    assert action.action_record_version == "1"
    assert action.provenance.risk_model_ref == risk.model_ref
    assert action.provenance.risk_rule_ref == risk.rule_ref
    assert action.provenance.risk_parameter_set_ref == risk.parameter_set_ref


def test_identity_and_full_resolution_are_deterministic() -> None:
    bundle = _risk_bundle()
    risk = _assessed(bundle)
    context = _context(risk)

    first = propose_corrective_action(risk, bundle[2].problem, bundle[4], context)
    second = propose_corrective_action(risk, bundle[2].problem, bundle[4], context)

    assert first == second
    assert first.resolution_id == second.resolution_id
    assert first.action.action_id == second.action.action_id
    assert first.action.ref == second.action.ref


def test_action_identity_has_exact_contract_components() -> None:
    bundle, risk, resolution = _positive()
    action_id = resolution.action.action_id

    assert action_id.action_instance_id == "A-REF-001"
    assert action_id.rule_ref == ACTION_RULE_REF
    assert action_id.originating_risk_id == risk.risk_assessment_id
    assert action_id.originating_problem_id == bundle[2].problem.problem_id
    assert action_id.target_artifact_ref == risk.artifact_ref


def test_targets_preserve_ordered_requirement_refs_and_lineages() -> None:
    _, risk, resolution = _positive()
    action = resolution.action

    assert tuple(item.subject_ref for item in action.target_requirements) == (
        risk.subject.participant_refs
    )
    assert tuple(item.lineage_id for item in action.target_requirements) == _lineages(risk)


def test_complete_problem_relation_risk_and_evidence_provenance_is_preserved() -> None:
    bundle, risk, resolution = _positive()
    problem = bundle[2].problem
    relation = bundle[4]
    provenance = resolution.action.provenance

    assert provenance.originating_risk_ref == risk.ref
    assert provenance.originating_problem_ref == problem.ref
    assert provenance.originating_relation_ref == relation.ref
    assert provenance.problem_resolution_ref == risk.problem_resolution_ref
    assert provenance.defect_population_ref == risk.defect_population_ref
    assert provenance.source_cross_result_ref == problem.source_cross_result_ref
    assert provenance.comparison_key == problem.comparison_key
    assert provenance.ordered_evidence_refs == problem.evidence_refs
    assert provenance.problem_rule_ref == problem.rule_ref
    assert provenance.relation_rule_ref == relation.rule_ref


def test_artifact_assessment_snapshot_and_process_identities_are_preserved() -> None:
    _, risk, resolution = _positive()
    provenance = resolution.action.provenance

    assert provenance.artifact_ref == risk.artifact_ref
    assert provenance.source_assessment_ref == risk.source_assessment_ref
    assert provenance.source_snapshot_id == risk.source_snapshot_id
    assert provenance.process_state_ref == risk.process_state_ref
    assert resolution.provenance.artifact_ref == risk.artifact_ref
    assert resolution.provenance.process_state_ref == risk.process_state_ref


def test_proposal_has_no_bound_revision_application_or_resolution_claim() -> None:
    _, _, resolution = _positive()
    action = resolution.action
    names = {item.name for item in fields(CorrectiveAction)}

    assert action.status is CorrectiveActionStatus.PROPOSED
    assert action.predecessor_action_ref is None
    assert action.external_revision_ref is None
    assert action.application_ref is None
    assert action.rejection_source_ref is None
    assert action.expected_bounded_outcome is (
        CorrectiveActionExpectedOutcome.LATER_RERUN_MAY_NOT_IDENTIFY_EXACT_CONFLICT
    )
    assert action.non_optimality_claim is (
        CorrectiveActionNonOptimalityClaim.CANDIDATE_NOT_OPTIMALITY_CLAIM
    )
    assert names.isdisjoint(
        {
            "replacement_text",
            "replacement_bound",
            "replacement_value",
            "selected_bound",
            "stakeholder_intent",
            "risk_resolved",
            "product_quality_improved",
            "child_artifact",
            "successor_specification",
            "reassessment",
        }
    )


def test_proposal_does_not_mutate_any_upstream_record_or_create_successor() -> None:
    bundle = _risk_bundle()
    risk = _assessed(bundle)
    before = (bundle, risk)

    resolution = propose_corrective_action(
        risk,
        bundle[2].problem,
        bundle[4],
        _context(risk),
    )

    assert (bundle, risk) == before
    assert resolution.action.target_artifact_ref == risk.artifact_ref
    assert not hasattr(resolution, "specification_version")
    assert not hasattr(resolution.action, "child_artifact_ref")


@pytest.mark.parametrize(
    ("status", "applicability", "reason"),
    [
        (
            FullModelStatus.UNAVAILABLE,
            Applicability.APPLICABLE,
            CorrectiveActionReason.SOURCE_UNAVAILABLE,
        ),
        (
            FullModelStatus.UNKNOWN,
            Applicability.UNKNOWN,
            CorrectiveActionReason.SOURCE_ASSESSMENT_UNKNOWN,
        ),
        (
            FullModelStatus.UNRESOLVED,
            Applicability.APPLICABLE,
            CorrectiveActionReason.SOURCE_IDENTITY_OR_COHERENCE_UNRESOLVED,
        ),
        (
            FullModelStatus.UNSUPPORTED,
            Applicability.APPLICABLE,
            CorrectiveActionReason.SOURCE_UNSUPPORTED,
        ),
    ],
)
def test_nonpositive_risk_states_propagate_without_an_action(
    status,
    applicability,
    reason,
) -> None:
    bundle = _risk_bundle()
    risk = replace(
        _assessed(bundle),
        status=status,
        applicability=applicability,
        classification=None,
    )

    resolution = propose_corrective_action(
        risk,
        bundle[2].problem,
        bundle[4],
        _context(risk),
    )

    assert resolution.status is status
    assert resolution.applicability is applicability
    assert resolution.reason_codes == (reason,)
    assert resolution.action is None
    assert resolution.action_ref is None


def test_not_applicable_risk_does_not_create_an_action() -> None:
    bundle = _risk_bundle(UPPER_TWO, UPPER_FIVE)
    risk = _assessed(bundle)

    resolution = propose_corrective_action(
        risk,
        None,
        bundle[4],
        _context(risk, lineages=()),
    )

    assert resolution.status is FullModelStatus.NOT_APPLICABLE
    assert resolution.applicability is Applicability.NOT_APPLICABLE
    assert resolution.action is None
    assert resolution.reason_codes == (
        CorrectiveActionReason.NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE,
    )


def test_actual_unresolved_m3_07_path_does_not_create_an_action() -> None:
    bundle = _risk_bundle(
        "Система працює не більше 2 с",
        "Система працює не нижче 5 с",
    )
    risk = _assessed(bundle)

    resolution = propose_corrective_action(
        risk,
        None,
        bundle[4],
        _context(risk, lineages=()),
    )

    assert resolution.status is FullModelStatus.UNRESOLVED
    assert resolution.action is None


def test_unregistered_action_kind_is_unsupported() -> None:
    bundle = _risk_bundle()
    risk = _assessed(bundle)

    resolution = propose_corrective_action(
        risk,
        bundle[2].problem,
        bundle[4],
        _context(risk, requested_action_kind="SELECT_PREFERRED_BOUND"),
    )

    assert resolution.status is FullModelStatus.UNSUPPORTED
    assert resolution.action is None
    assert resolution.reason_codes == (
        CorrectiveActionReason.REQUESTED_ACTION_KIND_UNSUPPORTED,
    )


def test_missing_required_lineages_is_unresolved_not_a_partial_action() -> None:
    bundle = _risk_bundle()
    risk = _assessed(bundle)

    resolution = propose_corrective_action(
        risk,
        bundle[2].problem,
        bundle[4],
        _context(risk, lineages=()),
    )

    assert resolution.status is FullModelStatus.UNRESOLVED
    assert resolution.action is None


def test_mismatched_artifact_and_version_fail_closed() -> None:
    bundle = _risk_bundle()
    risk = _assessed(bundle)
    other_artifact = ArtifactRef(risk.artifact_ref.artifact_id, "v2")
    other_assessment = AssessmentRef(
        risk.source_assessment_ref.assessment_id,
        risk.source_assessment_ref.assessment_version,
        other_artifact,
    )
    context = replace(
        _context(risk),
        target_artifact_ref=other_artifact,
        source_assessment_ref=other_assessment,
    )

    with pytest.raises(ValueError, match="artifact"):
        propose_corrective_action(risk, bundle[2].problem, bundle[4], context)


def test_mismatched_assessment_snapshot_and_process_state_fail_closed() -> None:
    bundle = _risk_bundle()
    risk = _assessed(bundle)
    other_assessment = AssessmentRef(
        "ASSESS-OTHER",
        "2",
        risk.artifact_ref,
    )
    with pytest.raises(ValueError, match="assessment"):
        propose_corrective_action(
            risk,
            bundle[2].problem,
            bundle[4],
            replace(_context(risk), source_assessment_ref=other_assessment),
        )

    other_bundle = _risk_bundle(UPPER_TWO, LOWER_FIVE, UPPER_FIVE)
    with pytest.raises(ValueError, match="snapshot"):
        propose_corrective_action(
            risk,
            bundle[2].problem,
            bundle[4],
            replace(
                _context(risk),
                source_snapshot_id=other_bundle[0].snapshot_id,
            ),
        )

    other_process = ProcessStateRef(
        risk.process_state_ref.process_state_id,
        "2",
        risk.process_state_ref.stage,
    )
    with pytest.raises(ValueError, match="process-state"):
        propose_corrective_action(
            risk,
            bundle[2].problem,
            bundle[4],
            replace(_context(risk), process_state_ref=other_process),
        )


def test_mismatched_problem_relation_and_requirement_participants_fail_closed() -> None:
    bundle = _risk_bundle()
    risk = _assessed(bundle)
    foreign_bundle = _risk_bundle(UPPER_TWO, LOWER_FIVE, UPPER_FIVE)

    with pytest.raises(ValueError, match="problem"):
        propose_corrective_action(
            risk,
            foreign_bundle[2].problem,
            bundle[4],
            _context(risk),
        )

    with pytest.raises(ValueError, match="relation"):
        propose_corrective_action(
            risk,
            bundle[2].problem,
            foreign_bundle[4],
            _context(risk),
        )

    reversed_lineages = tuple(reversed(_lineages(risk)))
    with pytest.raises(ValueError, match="lineage"):
        propose_corrective_action(
            risk,
            bundle[2].problem,
            bundle[4],
            _context(risk, lineages=reversed_lineages),
        )


def test_action_schema_has_no_numeric_risk_or_optimization_fields() -> None:
    names = {item.name for item in fields(CorrectiveAction)}

    assert names.isdisjoint(
        {
            "probability",
            "likelihood",
            "severity",
            "impact",
            "criticality",
            "priority",
            "rank",
            "risk_reduction",
            "expected_risk_reduction",
            "cost",
            "optimality_score",
            "value",
        }
    )

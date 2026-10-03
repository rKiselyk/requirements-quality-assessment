from dataclasses import FrozenInstanceError, fields, replace
from fractions import Fraction

import pytest

from requirements_quality_assessment.checkpoint import (
    CHECKPOINT_CONTRACT_REF,
    CHECKPOINT_RULE_REF,
    CheckpointComparator,
    CheckpointOutcome,
    CheckpointReason,
    CheckpointRequest,
    PolicyProviderRef,
    PolicySourceRef,
    SelectedCheckpointResult,
    ThresholdPolicy,
    evaluate_checkpoint,
    select_metric_result,
)
from requirements_quality_assessment.dynamic_evidence import (
    Applicability,
    FullModelStatus,
)
from requirements_quality_assessment.full_model_reporter import (
    AuditFullModelReporter,
    FullModelReportBundle,
    UserFullModelReporter,
)
from requirements_quality_assessment.metrics import ArtifactRef, ContractRef, MetricId
from requirements_quality_assessment.performance_efficiency import (
    ProcessStage,
    ProcessStateRef,
)

from test_full_model_v0_1_e2e_acceptance import _build_scenario


POLICY_CONTRACT = ContractRef("REFERENCE-CHECKPOINT-POLICY", "1")
PROVIDER = PolicyProviderRef("CONTROLLED-REFERENCE-FIXTURE", "1")
SOURCE = PolicySourceRef("TC-04-REFERENCE-SCENARIO", "1")


def _policy(comparator=CheckpointComparator.GREATER_THAN_OR_EQUAL, threshold=Fraction(1, 1)):
    return ThresholdPolicy(
        "QB-REFERENCE-CHECKPOINT-POLICY",
        "1",
        SOURCE,
        PROVIDER,
        "Fixture-only evaluator execution and reassessment-sensitivity check.",
        comparator,
        threshold,
        POLICY_CONTRACT,
    )


def _selected(
    *,
    value=Fraction(1, 1),
    status=FullModelStatus.AVAILABLE,
    applicability=Applicability.APPLICABLE,
):
    artifact = ArtifactRef("SPEC", "1")
    process = ProcessStateRef("PROCESS", "1", ProcessStage.REFERENCE_VERIFICATION)
    return SelectedCheckpointResult(
        "RESULT-REF",
        MetricId.SPEC_QB_CONSISTENCY.value,
        status,
        applicability,
        value if status is FullModelStatus.AVAILABLE else None,
        artifact,
        process,
        POLICY_CONTRACT,
        (() if status is FullModelStatus.AVAILABLE else (f"UPSTREAM_{status.value}",)),
        ("SOURCE-PROVENANCE",),
    )


def _evaluate(selected=None, policy=None, **changes):
    selected = selected or _selected()
    values = dict(
        checkpoint_id="CHECKPOINT-QB",
        checkpoint_version="1",
        selected_result=selected,
        threshold_policy=policy or _policy(),
        process_state_ref=selected.process_state_ref,
        artifact_ref=selected.artifact_ref,
    )
    values.update(changes)
    return evaluate_checkpoint(CheckpointRequest(**values))


def test_checkpoint_and_policy_are_typed_versioned_and_immutable():
    policy = _policy()
    evaluation = _evaluate(policy=policy)

    assert policy.ref.policy_id == "QB-REFERENCE-CHECKPOINT-POLICY"
    assert policy.ref.policy_version == "1"
    assert evaluation.checkpoint_id == "CHECKPOINT-QB"
    assert evaluation.checkpoint_version == "1"
    assert evaluation.checkpoint_contract_ref == CHECKPOINT_CONTRACT_REF
    assert evaluation.evaluator_rule_ref == CHECKPOINT_RULE_REF
    with pytest.raises(FrozenInstanceError):
        policy.threshold = Fraction(0, 1)


def test_no_default_threshold_or_policy_and_float_is_rejected():
    with pytest.raises(TypeError):
        ThresholdPolicy(
            "POLICY", "1", SOURCE, PROVIDER, "Explicit rationale", CheckpointComparator.EQUAL
        )
    with pytest.raises(TypeError, match="exact Fraction"):
        ThresholdPolicy(
            "POLICY",
            "1",
            SOURCE,
            PROVIDER,
            "Explicit rationale",
            CheckpointComparator.EQUAL,
            1.0,
            POLICY_CONTRACT,
        )
    assert isinstance(_policy().threshold, Fraction)


@pytest.mark.parametrize(
    ("comparator", "value", "threshold", "expected"),
    (
        (CheckpointComparator.GREATER_THAN_OR_EQUAL, Fraction(2), Fraction(1), True),
        (CheckpointComparator.GREATER_THAN, Fraction(2), Fraction(1), True),
        (CheckpointComparator.LESS_THAN_OR_EQUAL, Fraction(1), Fraction(2), True),
        (CheckpointComparator.LESS_THAN, Fraction(1), Fraction(2), True),
        (CheckpointComparator.EQUAL, Fraction(1), Fraction(1), True),
        (CheckpointComparator.GREATER_THAN, Fraction(1), Fraction(1), False),
        (CheckpointComparator.LESS_THAN, Fraction(1), Fraction(1), False),
    ),
)
def test_each_comparator_and_equal_boundary(comparator, value, threshold, expected):
    result = _evaluate(
        selected=_selected(value=value),
        policy=_policy(comparator, threshold),
    )
    assert result.outcome is (
        CheckpointOutcome.SATISFIED if expected else CheckpointOutcome.NOT_SATISFIED
    )


def test_available_satisfied_and_not_satisfied_are_deterministic():
    request_result = _evaluate(selected=_selected(value=Fraction(1)))
    assert request_result.outcome is CheckpointOutcome.SATISFIED
    assert request_result.reason_codes == (CheckpointReason.PREDICATE_TRUE,)
    assert _evaluate(selected=_selected(value=Fraction(0))).outcome is CheckpointOutcome.NOT_SATISFIED
    assert _evaluate(selected=_selected(value=Fraction(1))) == request_result


@pytest.mark.parametrize(
    "status",
    (
        FullModelStatus.UNKNOWN,
        FullModelStatus.UNAVAILABLE,
        FullModelStatus.UNRESOLVED,
        FullModelStatus.UNSUPPORTED,
    ),
)
def test_missing_states_are_unresolved_and_never_become_zero(status):
    selected = _selected(status=status, applicability=Applicability.UNKNOWN)
    result = _evaluate(selected=selected)

    assert selected.exact_value is None
    assert result.selected_result.status is status
    assert result.selected_result.reason_codes == (f"UPSTREAM_{status.value}",)
    assert result.outcome is CheckpointOutcome.UNRESOLVED
    assert result.reason_codes == (CheckpointReason.SOURCE_VALUE_UNRESOLVED,)


def test_not_applicable_remains_not_applicable_without_a_comparison_value():
    selected = _selected(
        status=FullModelStatus.NOT_APPLICABLE,
        applicability=Applicability.NOT_APPLICABLE,
    )
    result = _evaluate(selected=selected)
    assert selected.exact_value is None
    assert result.outcome is CheckpointOutcome.NOT_APPLICABLE


def test_cross_artifact_and_process_state_provenance_fail_closed():
    selected = _selected()
    wrong_artifact = _evaluate(
        selected=selected,
        artifact_ref=ArtifactRef("SPEC", "2"),
    )
    wrong_process = _evaluate(
        selected=selected,
        process_state_ref=ProcessStateRef(
            "PROCESS", "2", ProcessStage.REFERENCE_VERIFICATION
        ),
    )
    assert wrong_artifact.outcome is CheckpointOutcome.UNRESOLVED
    assert wrong_artifact.reason_codes == (
        CheckpointReason.ARTIFACT_PROVENANCE_MISMATCH,
    )
    assert wrong_process.outcome is CheckpointOutcome.UNRESOLVED
    assert wrong_process.reason_codes == (
        CheckpointReason.PROCESS_STATE_PROVENANCE_MISMATCH,
    )


def test_real_v1_v2_qb_results_use_the_same_external_fixture_policy():
    scenario = _build_scenario()
    qb_v1 = next(
        entry for entry in scenario.metric_v1.entries
        if entry.metric_id is MetricId.SPEC_QB_CONSISTENCY
    )
    core_v2 = scenario.reassessment.produced_results[0]
    qb_v2 = next(
        entry for entry in core_v2.metric_profile.entries
        if entry.metric_id is MetricId.SPEC_QB_CONSISTENCY
    )
    selected_v1 = select_metric_result(qb_v1, scenario.process_v1)
    selected_v2 = select_metric_result(qb_v2, scenario.process_v2)
    policy = _policy()

    result_v1 = _evaluate(selected=selected_v1, policy=policy)
    result_v2 = _evaluate(selected=selected_v2, policy=policy)

    assert selected_v1.exact_value == Fraction(0, 1)
    assert selected_v2.exact_value == Fraction(1, 1)
    assert result_v1.outcome is CheckpointOutcome.NOT_SATISFIED
    assert result_v2.outcome is CheckpointOutcome.SATISFIED
    assert result_v1.threshold_policy is policy
    assert result_v2.threshold_policy is policy
    assert result_v1.provenance.selected_result_provenance[0] is qb_v1.provenance
    assert result_v2.provenance.selected_result_provenance[0] is qb_v2.provenance


def test_metric_adapter_rejects_a_metric_from_another_process_artifact():
    scenario = _build_scenario()
    qb_v1 = next(
        entry for entry in scenario.metric_v1.entries
        if entry.metric_id is MetricId.SPEC_QB_CONSISTENCY
    )

    with pytest.raises(ValueError, match="same artifact"):
        select_metric_result(qb_v1, scenario.process_v2)


def test_checkpoint_result_has_no_lifecycle_decision_field_or_value():
    result = _evaluate()
    names = {field.name.upper() for field in fields(result)}
    assert not names & {"PROCEED", "RELEASE", "GO", "NO_GO"}
    assert "PROCEED" not in repr(result).upper()
    assert "RELEASE" not in repr(result).upper()


def test_reporters_separate_predicate_satisfaction_from_lifecycle_decisions():
    scenario = _build_scenario()
    qb = next(
        entry for entry in scenario.metric_v1.entries
        if entry.metric_id is MetricId.SPEC_QB_CONSISTENCY
    )
    evaluation = _evaluate(
        selected=select_metric_result(qb, scenario.process_v1),
        policy=_policy(),
    )
    bundle = replace(
        scenario.report_bundle,
        checkpoint_evaluations=(evaluation,),
    )

    user = UserFullModelReporter().render_projection(bundle)
    audit = AuditFullModelReporter().render_projection(bundle)
    assert "SPEC.QB_CONSISTENCY=0/1" in user
    assert "predicate=>= 1/1" in user
    assert "Outcome: NOT_SATISFIED" in user
    assert "НЕ є дозволом RELEASE або PROCEED" in user
    for expected in (
        "checkpoint_id: CHECKPOINT-QB",
        "selected_result: SelectedCheckpointResult",
        "result_identity: SPEC.QB_CONSISTENCY",
        "status: AVAILABLE",
        "exact_value: Fraction(0,1)",
        "threshold_policy: ThresholdPolicy",
        "policy_id: QB-REFERENCE-CHECKPOINT-POLICY",
        "comparator: >=",
        "provider_id: CONTROLLED-REFERENCE-FIXTURE",
        "source_id: TC-04-REFERENCE-SCENARIO",
        "governing_contract_ref: ContractRef",
        "process_state_ref: ProcessStateRef",
        "threshold: Fraction(1,1)",
        "evaluator_rule_ref: RuleRef",
        "outcome: NOT_SATISFIED",
    ):
        assert expected in audit


def test_bundle_checkpoint_field_is_appended_after_historical_prefix():
    names = tuple(field.name for field in fields(FullModelReportBundle))
    assert names[-3:] == (
        "predicted_product_quality",
        "quantitative_risk_assessments",
        "checkpoint_evaluations",
    )

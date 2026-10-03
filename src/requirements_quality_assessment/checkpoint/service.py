"""Deterministic scalar checkpoint evaluation and source adapters."""

from __future__ import annotations

from fractions import Fraction

from ..dynamic_evidence import Applicability, FullModelStatus
from ..metrics import MetricEntry
from ..process import ProcessAssessmentState
from .domain import (
    CHECKPOINT_CONTRACT_REF,
    CHECKPOINT_RULE_REF,
    CheckpointComparator,
    CheckpointEvaluation,
    CheckpointEvaluationProvenance,
    CheckpointOutcome,
    CheckpointReason,
    CheckpointRequest,
    SelectedCheckpointResult,
)


def select_metric_result(
    entry: MetricEntry,
    process_state: ProcessAssessmentState,
) -> SelectedCheckpointResult:
    """Select an existing metric without recalculating its value or state."""

    if not isinstance(entry, MetricEntry):
        raise TypeError("entry must be a MetricEntry")
    if not isinstance(process_state, ProcessAssessmentState):
        raise TypeError("process_state must be a ProcessAssessmentState")
    if entry.artifact_ref != process_state.artifact_ref:
        raise ValueError("metric and process state must identify the same artifact")
    if entry.assessment_ref != process_state.assessment_ref:
        raise ValueError("metric and process state must identify the same assessment")
    if entry.entry_id.profile_id != process_state.metric_profile_ref:
        raise ValueError("metric must belong to the process state's metric profile")

    return SelectedCheckpointResult(
        result_ref=entry.entry_id,
        result_identity=entry.metric_id.value,
        status=FullModelStatus(entry.status.value),
        applicability=Applicability(entry.applicability.value),
        exact_value=entry.value,
        artifact_ref=entry.artifact_ref,
        process_state_ref=process_state.ref,
        governing_contract_or_rule_ref=entry.registry_ref,
        reason_codes=entry.provenance.source_reasons,
        provenance=(
            entry.provenance,
            entry.source_status,
            entry.source_assessment_refs,
            entry.rule_refs,
            entry.assessment_ref,
        ),
    )


def _predicate(
    comparator: CheckpointComparator,
    value: Fraction,
    threshold: Fraction,
) -> bool:
    return {
        CheckpointComparator.GREATER_THAN_OR_EQUAL: lambda: value >= threshold,
        CheckpointComparator.GREATER_THAN: lambda: value > threshold,
        CheckpointComparator.LESS_THAN_OR_EQUAL: lambda: value <= threshold,
        CheckpointComparator.LESS_THAN: lambda: value < threshold,
        CheckpointComparator.EQUAL: lambda: value == threshold,
    }[comparator]()


def evaluate_checkpoint(request: CheckpointRequest) -> CheckpointEvaluation:
    if not isinstance(request, CheckpointRequest):
        raise TypeError("request must be a CheckpointRequest")
    selected = request.selected_result

    if selected.artifact_ref != request.artifact_ref:
        outcome = CheckpointOutcome.UNRESOLVED
        reasons = (CheckpointReason.ARTIFACT_PROVENANCE_MISMATCH,)
    elif selected.process_state_ref != request.process_state_ref:
        outcome = CheckpointOutcome.UNRESOLVED
        reasons = (CheckpointReason.PROCESS_STATE_PROVENANCE_MISMATCH,)
    elif selected.status is FullModelStatus.NOT_APPLICABLE:
        outcome = CheckpointOutcome.NOT_APPLICABLE
        reasons = (CheckpointReason.SOURCE_NOT_APPLICABLE,)
    elif selected.status is not FullModelStatus.AVAILABLE:
        outcome = CheckpointOutcome.UNRESOLVED
        reasons = (CheckpointReason.SOURCE_VALUE_UNRESOLVED,)
    elif _predicate(
        request.threshold_policy.comparator,
        selected.exact_value,
        request.threshold_policy.threshold,
    ):
        outcome = CheckpointOutcome.SATISFIED
        reasons = (CheckpointReason.PREDICATE_TRUE,)
    else:
        outcome = CheckpointOutcome.NOT_SATISFIED
        reasons = (CheckpointReason.PREDICATE_FALSE,)

    provenance = CheckpointEvaluationProvenance(
        selected.result_ref,
        selected.provenance,
        request.threshold_policy.ref,
        request.threshold_policy.source_ref,
        request.threshold_policy.provider_ref,
        request.process_state_ref,
        request.artifact_ref,
        request.threshold_policy.governing_contract_ref,
        CHECKPOINT_CONTRACT_REF,
        CHECKPOINT_RULE_REF,
    )
    return CheckpointEvaluation(
        request.checkpoint_id,
        request.checkpoint_version,
        selected,
        request.threshold_policy,
        request.process_state_ref,
        request.artifact_ref,
        outcome,
        reasons,
        CHECKPOINT_CONTRACT_REF,
        CHECKPOINT_RULE_REF,
        provenance,
    )

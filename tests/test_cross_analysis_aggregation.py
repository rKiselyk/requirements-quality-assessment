from dataclasses import replace
from decimal import Decimal

import pytest

from requirements_quality_assessment.cross_analysis import (
    AssessmentSnapshot,
    BoundedNonClaimKey,
    ComparisonKey,
    ComparisonOperand,
    ComparisonOperands,
    CrossDiagnosticRef,
    CrossEvidenceRef,
    CrossObservationRef,
    CrossRelationKind,
    CrossRequirementResult,
    CrossResultState,
    CrossUnresolvedReason,
    OutsideApplicabilityReason,
    QB_COMPARISON_RULE,
    QB_CONTRACT_MANIFEST,
    QB_COVERAGE_PROFILE,
    QB_MATERIALITY_RULE,
    QbConflictSetBuilder,
    QbMaterialityAuditRecord,
    QbMaterialityDisposition,
    QbMaterialityGateOutcomes,
    QbMaterialityResult,
    RequirementOrderKey,
    SnapshotCountManifest,
    SnapshotDiagnosticManifest,
    SnapshotEvidenceManifest,
    SnapshotObservationManifest,
    SnapshotRequirementManifest,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorLabel,
    DetectionProcessingStatus,
    FeatureId,
    UnitLabel,
)


def _requirement(
    requirement_id: str,
    source_order: int,
    *,
    material_diagnostic: bool = False,
) -> SnapshotRequirementManifest:
    text = "Метрика <= 2 SECOND Контекст"
    metric_start = text.index("Метрика")
    bound_start = text.index("<= 2 SECOND")
    context_start = text.index("Контекст")
    metric = SnapshotEvidenceManifest(
        ref=CrossEvidenceRef(requirement_id, "M:E001"),
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        text="Метрика",
        start_offset=metric_start,
        end_offset=metric_start + len("Метрика"),
        rule_id="M-RULE",
    )
    bound = SnapshotEvidenceManifest(
        ref=CrossEvidenceRef(requirement_id, "B:E001"),
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        text="<= 2 SECOND",
        start_offset=bound_start,
        end_offset=bound_start + len("<= 2 SECOND"),
        rule_id="B-RULE",
    )
    context = SnapshotEvidenceManifest(
        ref=CrossEvidenceRef(requirement_id, "C:E001"),
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        text="Контекст",
        start_offset=context_start,
        end_offset=context_start + len("Контекст"),
        rule_id="C-RULE",
    )
    observation = SnapshotObservationManifest(
        ref=CrossObservationRef(
            requirement_id,
            FeatureId.QUANTITATIVE_CONSTRAINT,
            0,
        ),
        metric_evidence_refs=(metric.ref,),
        comparator=ComparatorLabel.LESS_THAN_OR_EQUAL,
        inclusivity=BoundaryInclusivity.INCLUSIVE,
        comparator_evidence_refs=(bound.ref,),
        value=Decimal("2"),
        value_evidence_refs=(bound.ref,),
        unit=UnitLabel.SECOND,
        unit_evidence_refs=(bound.ref,),
        context_evidence_refs=(context.ref,),
        unresolved_components=(),
        evidence_refs=(metric.ref, bound.ref, context.ref),
    )
    diagnostics = (
        (
            SnapshotDiagnosticManifest(
                ref=CrossDiagnosticRef(
                    requirement_id,
                    FeatureId.QUANTITATIVE_CONSTRAINT,
                    0,
                ),
                code="QUANT_UNRESOLVED_NUMERIC_CANDIDATE",
                rule_id="QUANT-001",
                candidate_text=None,
                start_offset=None,
                end_offset=None,
            ),
        )
        if material_diagnostic
        else ()
    )
    return SnapshotRequirementManifest(
        requirement_id=requirement_id,
        source_order=source_order,
        source_line=source_order + 1,
        text=text,
        processing_status=(
            DetectionProcessingStatus.INCOMPLETE
            if material_diagnostic
            else DetectionProcessingStatus.COMPLETE
        ),
        observations=(observation,),
        evidence=(metric, bound, context),
        diagnostics=diagnostics,
    )


def _snapshot(
    count: int = 4,
    *,
    material_diagnostic: bool = False,
) -> AssessmentSnapshot:
    requirements = tuple(
        _requirement(
            f"R{index + 1:03d}",
            index,
            material_diagnostic=material_diagnostic and index == 0,
        )
        for index in range(count)
    )
    return AssessmentSnapshot(
        requirements=requirements,
        contracts=QB_CONTRACT_MANIFEST,
        counts=SnapshotCountManifest.from_requirements(requirements),
    )


def _materiality(
    snapshot: AssessmentSnapshot,
    *,
    material: bool = False,
) -> QbMaterialityResult:
    if not material:
        return QbMaterialityResult(
            snapshot_id=snapshot.snapshot_id,
            materiality_rule=QB_MATERIALITY_RULE,
            audit_records=(),
            global_unresolved_diagnostic_count=0,
            qb_material_count=0,
            qb_non_material_count=0,
        )

    requirement = snapshot.requirements[0]
    diagnostic = requirement.diagnostics[0]
    audit = QbMaterialityAuditRecord(
        snapshot_id=snapshot.snapshot_id,
        requirement_id=requirement.requirement_id,
        requirement_source_order=requirement.source_order,
        diagnostic_ref=diagnostic.ref,
        diagnostic_code=diagnostic.code,
        diagnostic_rule_id=diagnostic.rule_id,
        candidate_text=diagnostic.candidate_text,
        diagnostic_start_offset=diagnostic.start_offset,
        diagnostic_end_offset=diagnostic.end_offset,
        matched_context_evidence_ref=None,
        matched_allowlist_contract=None,
        materiality_rule=QB_MATERIALITY_RULE,
        gate_outcomes=QbMaterialityGateOutcomes(
            exact_diagnostic_code=False,
            exact_diagnostic_rule=False,
            exact_candidate_text=False,
            candidate_inside_context=False,
            same_observation=False,
            allowlisted_contract_guarantee=False,
            no_qb_competition=False,
            provenance_integrity=False,
        ),
        disposition=QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED,
    )
    return QbMaterialityResult(
        snapshot_id=snapshot.snapshot_id,
        materiality_rule=QB_MATERIALITY_RULE,
        audit_records=(audit,),
        global_unresolved_diagnostic_count=1,
        qb_material_count=1,
        qb_non_material_count=0,
    )


def _operand(
    snapshot: AssessmentSnapshot,
    requirement_id: str,
    comparator: ComparatorLabel,
    value: Decimal,
) -> ComparisonOperand:
    return ComparisonOperand(
        snapshot_id=snapshot.snapshot_id,
        observation_ref=CrossObservationRef(
            requirement_id,
            FeatureId.QUANTITATIVE_CONSTRAINT,
            0,
        ),
        normalized_metric="метрика",
        normalized_context="контекст",
        comparator=comparator,
        inclusivity=BoundaryInclusivity.INCLUSIVE,
        value=value,
        unit=UnitLabel.SECOND,
    )


def _result(
    snapshot: AssessmentSnapshot,
    left_index: int,
    right_index: int,
    state: CrossResultState,
) -> CrossRequirementResult:
    left_requirement = snapshot.requirements[left_index]
    right_requirement = snapshot.requirements[right_index]
    left = _operand(
        snapshot,
        left_requirement.requirement_id,
        ComparatorLabel.LESS_THAN_OR_EQUAL,
        Decimal("2"),
    )
    right = _operand(
        snapshot,
        right_requirement.requirement_id,
        ComparatorLabel.GREATER_THAN_OR_EQUAL,
        Decimal("5"),
    )
    values = {
        "snapshot_id": snapshot.snapshot_id,
        "participants": (left_requirement.order_key, right_requirement.order_key),
        "observation_refs": (left.observation_ref, right.observation_ref),
        "operands": ComparisonOperands(left, right),
        "comparison_contract": QB_COMPARISON_RULE,
        "coverage_profile": QB_COVERAGE_PROFILE,
        "relation_kind": CrossRelationKind.QUANTITATIVE_BOUND,
        "evidence_refs": (
            CrossEvidenceRef(left_requirement.requirement_id, "B:E001"),
            CrossEvidenceRef(right_requirement.requirement_id, "B:E001"),
        ),
        "diagnostic_refs": (),
        "comparison_key": ComparisonKey("метрика", "контекст", UnitLabel.SECOND),
        "non_claim_keys": (BoundedNonClaimKey.NC_QB_BASE,),
    }
    if state is CrossResultState.CONFIRMED_CONFLICT:
        return CrossRequirementResult.confirmed_conflict(**values)
    if state is CrossResultState.COMPATIBLE_WITHIN_RULE:
        return CrossRequirementResult.compatible_within_rule(**values)
    values.pop("comparison_key")
    if state is CrossResultState.ASSESSMENT_UNRESOLVED:
        return CrossRequirementResult.assessment_unresolved(
            unresolved_reasons=(CrossUnresolvedReason.MISSING_METRIC,),
            **values,
        )
    return CrossRequirementResult.outside_v0_1_applicability(
        outside_reasons=(OutsideApplicabilityReason.METRIC_MISMATCH,),
        **values,
    )


def _build(
    snapshot: AssessmentSnapshot,
    *results: CrossRequirementResult,
    materiality: QbMaterialityResult | None = None,
):
    return QbConflictSetBuilder().build(
        snapshot,
        results,
        materiality or _materiality(snapshot),
    )


def test_no_results_produces_empty_complete_rconf() -> None:
    conflict_set = _build(_snapshot())

    assert conflict_set.participant_ids == ()
    assert conflict_set.rconf_complete is True


@pytest.mark.parametrize(
    "state",
    [
        CrossResultState.COMPATIBLE_WITHIN_RULE,
        CrossResultState.OUTSIDE_V0_1_APPLICABILITY,
    ],
)
def test_non_conflict_results_produce_empty_complete_rconf(
    state: CrossResultState,
) -> None:
    snapshot = _snapshot()

    conflict_set = _build(snapshot, _result(snapshot, 0, 1, state))

    assert conflict_set.participant_ids == ()
    assert conflict_set.rconf_complete is True


def test_unresolved_result_adds_no_speculative_members() -> None:
    snapshot = _snapshot()

    conflict_set = _build(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.ASSESSMENT_UNRESOLVED),
    )

    assert conflict_set.participant_ids == ()
    assert conflict_set.rconf_complete is False


def test_one_conflict_adds_both_participants() -> None:
    snapshot = _snapshot()

    conflict_set = _build(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
    )

    assert conflict_set.participant_ids == ("R001", "R002")
    assert conflict_set.rconf_complete is True


def test_overlapping_conflicts_deduplicate_participants() -> None:
    snapshot = _snapshot()

    conflict_set = _build(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
        _result(snapshot, 0, 2, CrossResultState.CONFIRMED_CONFLICT),
    )

    assert conflict_set.participant_ids == ("R001", "R002", "R003")


def test_disjoint_conflicts_add_every_unique_participant() -> None:
    snapshot = _snapshot()

    conflict_set = _build(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
        _result(snapshot, 2, 3, CrossResultState.CONFIRMED_CONFLICT),
    )

    assert conflict_set.participant_ids == ("R001", "R002", "R003", "R004")


def test_mixed_four_state_input_adds_only_confirmed_participants() -> None:
    snapshot = _snapshot()

    conflict_set = _build(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
        _result(snapshot, 0, 2, CrossResultState.COMPATIBLE_WITHIN_RULE),
        _result(snapshot, 1, 2, CrossResultState.ASSESSMENT_UNRESOLVED),
        _result(snapshot, 2, 3, CrossResultState.OUTSIDE_V0_1_APPLICABILITY),
    )

    assert conflict_set.participant_ids == ("R001", "R002")
    assert conflict_set.rconf_complete is False


def test_output_uses_source_order_independent_of_result_order() -> None:
    snapshot = _snapshot()
    earlier = _result(snapshot, 0, 2, CrossResultState.CONFIRMED_CONFLICT)
    later = _result(snapshot, 1, 3, CrossResultState.CONFIRMED_CONFLICT)

    forward = _build(snapshot, earlier, later)
    reverse = _build(snapshot, later, earlier)

    assert forward.participant_ids == ("R001", "R002", "R003", "R004")
    assert reverse == forward


def test_repeated_execution_is_deterministic() -> None:
    snapshot = _snapshot()
    results = (
        _result(snapshot, 0, 2, CrossResultState.CONFIRMED_CONFLICT),
        _result(snapshot, 1, 3, CrossResultState.CONFIRMED_CONFLICT),
    )

    assert _build(snapshot, *results) == _build(snapshot, *results)


def test_unresolved_pair_preserves_confirmed_members_in_partial_rconf() -> None:
    snapshot = _snapshot()

    conflict_set = _build(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
        _result(snapshot, 2, 3, CrossResultState.ASSESSMENT_UNRESOLVED),
    )

    assert conflict_set.participant_ids == ("R001", "R002")
    assert conflict_set.rconf_complete is False


def test_material_unresolved_extraction_preserves_confirmed_members() -> None:
    snapshot = _snapshot(material_diagnostic=True)

    conflict_set = _build(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
        materiality=_materiality(snapshot, material=True),
    )

    assert conflict_set.participant_ids == ("R001", "R002")
    assert conflict_set.rconf_complete is False


def test_duplicate_result_id_is_rejected() -> None:
    snapshot = _snapshot()
    result = _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT)

    with pytest.raises(ValueError, match="IDs.*duplicates"):
        _build(snapshot, result, result)


def test_result_from_foreign_snapshot_is_rejected() -> None:
    snapshot = _snapshot()
    foreign = _snapshot(3)
    result = _result(foreign, 0, 1, CrossResultState.CONFIRMED_CONFLICT)

    with pytest.raises(ValueError, match="cross snapshots"):
        _build(snapshot, result)


def test_unknown_participant_is_rejected() -> None:
    snapshot = _snapshot()
    result = _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT)
    object.__setattr__(
        result,
        "participants",
        (result.participants[0], RequirementOrderKey(9, "R999")),
    )

    with pytest.raises(ValueError, match="unknown participant"):
        _build(snapshot, result)


def test_noncanonical_reversed_participants_are_rejected() -> None:
    snapshot = _snapshot()
    result = _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT)
    object.__setattr__(result, "participants", tuple(reversed(result.participants)))

    with pytest.raises(ValueError, match="canonical source order"):
        _build(snapshot, result)


def test_self_pair_is_rejected_if_frozen_value_is_corrupted() -> None:
    snapshot = _snapshot()
    result = _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT)
    object.__setattr__(result, "participants", (result.participants[0],) * 2)

    with pytest.raises(ValueError, match="self-pair"):
        _build(snapshot, result)


def test_foreign_result_ownership_is_rejected() -> None:
    snapshot = _snapshot()
    result = _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT)
    object.__setattr__(
        result,
        "participants",
        (result.participants[0], replace(result.participants[1], source_order=3)),
    )

    with pytest.raises(ValueError, match="foreign participant ownership"):
        _build(snapshot, result)


def test_invalid_completeness_inputs_are_rejected() -> None:
    snapshot = _snapshot()
    builder = QbConflictSetBuilder()

    with pytest.raises(TypeError, match="QbMaterialityResult"):
        builder.build(snapshot, (), object())  # type: ignore[arg-type]

    foreign_materiality = _materiality(_snapshot(3))
    with pytest.raises(ValueError, match="cross snapshots"):
        builder.build(snapshot, (), foreign_materiality)

    corrupt = _materiality(snapshot)
    object.__setattr__(corrupt, "qb_material_count", 1)
    with pytest.raises(ValueError, match="QB-material count"):
        builder.build(snapshot, (), corrupt)

    diagnostic_snapshot = _snapshot(material_diagnostic=True)
    incomplete_coverage = _materiality(diagnostic_snapshot)
    with pytest.raises(ValueError, match="cover every snapshot diagnostic"):
        builder.build(diagnostic_snapshot, (), incomplete_coverage)


def test_non_tuple_results_are_rejected() -> None:
    snapshot = _snapshot()

    with pytest.raises(TypeError, match="results must be a tuple"):
        QbConflictSetBuilder().build(  # type: ignore[arg-type]
            snapshot,
            [],
            _materiality(snapshot),
        )

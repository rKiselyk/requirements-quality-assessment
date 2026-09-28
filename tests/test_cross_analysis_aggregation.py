from dataclasses import replace
from decimal import Decimal
from fractions import Fraction

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
    QB_CONSISTENCY_RULE,
    QB_CONTRACT_MANIFEST,
    QB_COVERAGE_PROFILE,
    QB_MATERIALITY_RULE,
    QB_NON_CLAIMS,
    QB_NON_MATERIAL_CONTEXT_ALLOWLIST,
    QbConflictSetBuilder,
    QbConsistencyAggregator,
    QbConsistencyReason,
    QbConsistencyState,
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


def _snapshot_from_requirements(
    requirements: tuple[SnapshotRequirementManifest, ...],
) -> AssessmentSnapshot:
    return AssessmentSnapshot(
        requirements=requirements,
        contracts=QB_CONTRACT_MANIFEST,
        counts=SnapshotCountManifest.from_requirements(requirements),
    )


def _without_quantitative_observation(
    requirement_id: str,
    source_order: int,
) -> SnapshotRequirementManifest:
    requirement = _requirement(requirement_id, source_order)
    return replace(requirement, observations=(), evidence=())


def _with_second_observation(
    requirement_id: str,
    source_order: int,
) -> SnapshotRequirementManifest:
    requirement = _requirement(requirement_id, source_order)
    second = replace(
        requirement.observations[0],
        ref=CrossObservationRef(
            requirement_id,
            FeatureId.QUANTITATIVE_CONSTRAINT,
            1,
        ),
    )
    return replace(
        requirement,
        observations=(requirement.observations[0], second),
    )


def _result_for_observations(
    snapshot: AssessmentSnapshot,
    left_observation_index: int,
    right_observation_index: int,
    state: CrossResultState,
) -> CrossRequirementResult:
    base = _result(snapshot, 0, 1, state)
    left_ref = replace(
        base.observation_refs[0],
        observation_index=left_observation_index,
    )
    right_ref = replace(
        base.observation_refs[1],
        observation_index=right_observation_index,
    )
    operands = ComparisonOperands(
        replace(base.operands.left, observation_ref=left_ref),
        replace(base.operands.right, observation_ref=right_ref),
    )
    return replace(
        base,
        observation_refs=(left_ref, right_ref),
        operands=operands,
    )


def _aggregate(
    snapshot: AssessmentSnapshot,
    *results: CrossRequirementResult,
    materiality: QbMaterialityResult | None = None,
):
    return QbConsistencyAggregator().aggregate(
        snapshot,
        results,
        materiality or _materiality(snapshot),
    )


def _non_materiality(snapshot: AssessmentSnapshot) -> QbMaterialityResult:
    requirement = snapshot.requirements[0]
    diagnostic = requirement.diagnostics[0]
    audit = QbMaterialityAuditRecord(
        snapshot_id=snapshot.snapshot_id,
        requirement_id=requirement.requirement_id,
        requirement_source_order=requirement.source_order,
        diagnostic_ref=diagnostic.ref,
        diagnostic_code=diagnostic.code,
        diagnostic_rule_id=diagnostic.rule_id,
        candidate_text="500",
        diagnostic_start_offset=0,
        diagnostic_end_offset=3,
        matched_context_evidence_ref=requirement.evidence[-1].ref,
        matched_allowlist_contract=QB_NON_MATERIAL_CONTEXT_ALLOWLIST[0].contract,
        materiality_rule=QB_MATERIALITY_RULE,
        gate_outcomes=QbMaterialityGateOutcomes(
            exact_diagnostic_code=True,
            exact_diagnostic_rule=True,
            exact_candidate_text=True,
            candidate_inside_context=True,
            same_observation=True,
            allowlisted_contract_guarantee=True,
            no_qb_competition=True,
            provenance_integrity=True,
        ),
        disposition=QbMaterialityDisposition.QB_NON_MATERIAL,
    )
    return QbMaterialityResult(
        snapshot_id=snapshot.snapshot_id,
        materiality_rule=QB_MATERIALITY_RULE,
        audit_records=(audit,),
        global_unresolved_diagnostic_count=1,
        qb_material_count=0,
        qb_non_material_count=1,
    )


@pytest.mark.parametrize("count", [0, 1])
def test_imp08_empty_and_single_requirement_are_not_applicable(count: int) -> None:
    assessment = _aggregate(_snapshot(count))

    assert assessment.state is QbConsistencyState.NOT_APPLICABLE
    assert assessment.value is None
    assert assessment.rconf_participant_ids == ()
    assert assessment.rconf_complete is True
    assert assessment.reasons == (
        QbConsistencyReason.FEWER_THAN_TWO_REQUIREMENTS,
    )
    assert assessment.observability.total_requirement_count == count
    assert assessment.observability.total_requirement_pair_count == 0


def test_imp08_completed_universe_with_no_applicable_comparison_is_na() -> None:
    snapshot = _snapshot(3)
    outside = tuple(
        _result(snapshot, left, right, CrossResultState.OUTSIDE_V0_1_APPLICABILITY)
        for left, right in ((0, 1), (0, 2), (1, 2))
    )

    assessment = _aggregate(snapshot, *outside)

    assert assessment.state is QbConsistencyState.NOT_APPLICABLE
    assert assessment.value is None
    assert assessment.rconf_complete is True
    assert assessment.reasons == (
        QbConsistencyReason.NO_APPLICABLE_COMPARISONS,
    )
    assert assessment.observability.outside_applicability_count == 3
    assert assessment.observability.applicable_comparison_count == 0


def test_imp08_all_compatible_computes_exact_one_with_non_claims() -> None:
    snapshot = _snapshot(2)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
    )

    assert assessment.state is QbConsistencyState.COMPUTED
    assert assessment.value == Fraction(1, 1)
    assert isinstance(assessment.value, Fraction)
    assert assessment.non_claim_contract == QB_NON_CLAIMS
    assert assessment.non_claim_keys == (BoundedNonClaimKey.NC_QB_BASE,)
    assert assessment.aggregation_rule == QB_CONSISTENCY_RULE
    assert assessment.coverage_profile == QB_COVERAGE_PROFILE


def test_imp08_isolated_requirement_remains_in_formula_denominator() -> None:
    requirements = (
        _requirement("R001", 0),
        _requirement("R002", 1),
        _without_quantitative_observation("R003", 2),
    )
    snapshot = _snapshot_from_requirements(requirements)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
    )

    assert assessment.state is QbConsistencyState.COMPUTED
    assert assessment.rconf_participant_ids == ("R001", "R002")
    assert assessment.value == Fraction(1, 3)
    assert assessment.formula_operands.total_requirement_count == 3
    assert assessment.observability.requirements_with_observations_count == 2
    assert assessment.observability.requirements_in_applicable_comparisons_count == 2
    assert assessment.observability.total_requirement_pair_count == 3
    assert assessment.observability.total_observation_pair_count == 1


def test_imp08_fraction_is_reduced_exactly() -> None:
    requirements = tuple(
        _requirement(f"R{index + 1:03d}", index)
        if index < 2
        else _without_quantitative_observation(f"R{index + 1:03d}", index)
        for index in range(6)
    )
    snapshot = _snapshot_from_requirements(requirements)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
    )

    assert assessment.value == Fraction(2, 3)
    assert assessment.value.numerator == 2
    assert assessment.value.denominator == 3


def test_imp08_overlapping_conflicts_count_unique_rconf_participants() -> None:
    snapshot = _snapshot(3)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
        _result(snapshot, 0, 2, CrossResultState.COMPATIBLE_WITHIN_RULE),
        _result(snapshot, 1, 2, CrossResultState.CONFIRMED_CONFLICT),
    )

    assert assessment.rconf_participant_ids == ("R001", "R002", "R003")
    assert assessment.observability.observed_rconf_count == 3
    assert assessment.observability.confirmed_conflict_count == 2
    assert assessment.observability.compatible_count == 1
    assert assessment.observability.applicable_comparison_count == 3
    assert assessment.observability.requirements_in_applicable_comparisons_count == 3
    assert assessment.value == Fraction(0, 1)


def test_imp08_unresolved_pair_withholds_value_and_retains_partial_rconf() -> None:
    snapshot = _snapshot(3)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
        _result(snapshot, 0, 2, CrossResultState.ASSESSMENT_UNRESOLVED),
        _result(snapshot, 1, 2, CrossResultState.OUTSIDE_V0_1_APPLICABILITY),
    )

    assert assessment.state is QbConsistencyState.UNKNOWN
    assert assessment.value is None
    assert assessment.rconf_participant_ids == ("R001", "R002")
    assert assessment.rconf_complete is False
    assert assessment.reasons == (
        QbConsistencyReason.ASSESSMENT_UNRESOLVED_PAIR,
    )
    assert assessment.observability.confirmed_conflict_count == 1
    assert assessment.observability.unresolved_count == 1
    assert assessment.observability.outside_applicability_count == 1


def test_imp08_compatible_plus_unresolved_is_unknown() -> None:
    snapshot = _snapshot(3)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
        _result(snapshot, 0, 2, CrossResultState.ASSESSMENT_UNRESOLVED),
        _result(snapshot, 1, 2, CrossResultState.OUTSIDE_V0_1_APPLICABILITY),
    )

    assert assessment.state is QbConsistencyState.UNKNOWN
    assert assessment.value is None
    assert assessment.observability.applicable_comparison_count == 1


def test_imp08_material_diagnostic_without_pair_result_is_unknown() -> None:
    requirements = (
        _requirement("R001", 0, material_diagnostic=True),
        _without_quantitative_observation("R002", 1),
    )
    snapshot = _snapshot_from_requirements(requirements)
    assessment = _aggregate(
        snapshot,
        materiality=_materiality(snapshot, material=True),
    )

    assert assessment.state is QbConsistencyState.UNKNOWN
    assert assessment.value is None
    assert assessment.rconf_complete is False
    assert assessment.reasons == (
        QbConsistencyReason.QB_MATERIAL_UNRESOLVED_EXTRACTION,
    )
    assert assessment.observability.total_observation_pair_count == 0
    assert assessment.observability.global_unresolved_extraction_count == 1
    assert assessment.observability.qb_material_unresolved_count == 1


def test_imp08_non_material_diagnostic_does_not_force_unknown() -> None:
    snapshot = _snapshot(2, material_diagnostic=True)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
        materiality=_non_materiality(snapshot),
    )

    assert assessment.state is QbConsistencyState.COMPUTED
    assert assessment.value == Fraction(1, 1)
    assert assessment.observability.global_unresolved_extraction_count == 1
    assert assessment.observability.qb_material_unresolved_count == 0
    assert assessment.observability.qb_non_material_diagnostic_count == 1


def test_imp08_first_gate_makes_single_requirement_rconf_complete() -> None:
    snapshot = _snapshot(1, material_diagnostic=True)
    assessment = _aggregate(
        snapshot,
        materiality=_materiality(snapshot, material=True),
    )

    assert assessment.state is QbConsistencyState.NOT_APPLICABLE
    assert assessment.rconf_complete is True
    assert assessment.observability.qb_material_unresolved_count == 1


def test_imp08_unknown_preserves_both_distinct_material_causes() -> None:
    snapshot = _snapshot(2, material_diagnostic=True)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.ASSESSMENT_UNRESOLVED),
        materiality=_materiality(snapshot, material=True),
    )

    assert assessment.state is QbConsistencyState.UNKNOWN
    assert assessment.reasons == (
        QbConsistencyReason.QB_MATERIAL_UNRESOLVED_EXTRACTION,
        QbConsistencyReason.ASSESSMENT_UNRESOLVED_PAIR,
    )
    assert assessment.observability.qb_material_unresolved_count == 1
    assert assessment.observability.unresolved_count == 1


def test_imp08_four_state_counts_and_applicable_requirement_deduplication() -> None:
    snapshot = _snapshot(4)
    states = (
        (0, 1, CrossResultState.CONFIRMED_CONFLICT),
        (0, 2, CrossResultState.COMPATIBLE_WITHIN_RULE),
        (0, 3, CrossResultState.ASSESSMENT_UNRESOLVED),
        (1, 2, CrossResultState.OUTSIDE_V0_1_APPLICABILITY),
        (1, 3, CrossResultState.OUTSIDE_V0_1_APPLICABILITY),
        (2, 3, CrossResultState.COMPATIBLE_WITHIN_RULE),
    )
    assessment = _aggregate(
        snapshot,
        *(_result(snapshot, left, right, state) for left, right, state in states),
    )
    metadata = assessment.observability

    assert metadata.total_requirement_pair_count == 6
    assert metadata.total_observation_pair_count == 6
    assert metadata.confirmed_conflict_count == 1
    assert metadata.compatible_count == 2
    assert metadata.unresolved_count == 1
    assert metadata.outside_applicability_count == 2
    assert metadata.applicable_comparison_count == 3
    assert metadata.requirements_in_applicable_comparisons_count == 4


def test_imp08_multiple_observations_preserve_exhaustive_result_counts() -> None:
    snapshot = _snapshot_from_requirements(
        (
            _with_second_observation("R001", 0),
            _with_second_observation("R002", 1),
        )
    )
    states = (
        CrossResultState.CONFIRMED_CONFLICT,
        CrossResultState.COMPATIBLE_WITHIN_RULE,
        CrossResultState.ASSESSMENT_UNRESOLVED,
        CrossResultState.OUTSIDE_V0_1_APPLICABILITY,
    )
    observation_indexes = ((0, 0), (0, 1), (1, 0), (1, 1))

    assessment = _aggregate(
        snapshot,
        *(
            _result_for_observations(snapshot, left, right, state)
            for (left, right), state in zip(observation_indexes, states, strict=True)
        ),
    )

    metadata = assessment.observability
    assert metadata.total_requirement_pair_count == 1
    assert metadata.total_observation_pair_count == 4
    assert (
        metadata.confirmed_conflict_count,
        metadata.compatible_count,
        metadata.unresolved_count,
        metadata.outside_applicability_count,
    ) == (1, 1, 1, 1)


def test_imp08_requires_the_complete_exhaustive_observation_pair_universe() -> None:
    snapshot = _snapshot(3)

    with pytest.raises(ValueError, match="exhaustive observation-pair universe"):
        _aggregate(
            snapshot,
            _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
        )


def test_imp08_rejects_duplicate_observation_pair_results() -> None:
    snapshot = _snapshot(2)

    with pytest.raises(ValueError, match="observation-pair results"):
        _aggregate(
            snapshot,
            _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
            _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
        )


def test_imp08_rejects_conflict_set_not_produced_by_imp07_semantics() -> None:
    snapshot = _snapshot(2)
    result = _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT)
    wrong = replace(_build(snapshot, result), participant_ids=("R001",))

    with pytest.raises(ValueError, match="IMP-07 builder output"):
        QbConsistencyAggregator().aggregate(
            snapshot,
            (result,),
            _materiality(snapshot),
            wrong,
        )


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"total_requirement_pair_count": 0}, "total_requirement_pair_count"),
        ({"total_observation_pair_count": 2}, "four result-state counts"),
        ({"applicable_comparison_count": 0}, "conflict plus compatible"),
        (
            {"global_unresolved_extraction_count": 1},
            "material plus non-material",
        ),
        ({"requirements_with_observations_count": 3}, "cannot exceed"),
        (
            {"requirements_in_applicable_comparisons_count": 3},
            "cannot exceed",
        ),
        ({"observed_rconf_count": 3}, "cannot exceed"),
    ],
)
def test_imp08_observability_rejects_every_invalid_count_equation(
    changes: dict[str, int],
    message: str,
) -> None:
    snapshot = _snapshot(2)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
    )

    with pytest.raises(ValueError, match=message):
        replace(assessment.observability, **changes)


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"value": None}, "COMPUTED requires"),
        ({"value": Fraction(1, 2)}, "exact bounded formula"),
        ({"state": QbConsistencyState.UNKNOWN, "value": None}, "incomplete R_conf"),
        (
            {"state": QbConsistencyState.NOT_APPLICABLE, "value": None},
            "applicable comparisons",
        ),
        ({"rconf_complete": False}, "observability rconf_complete"),
        ({"rconf_participant_ids": ("R001",)}, "observed_rconf_count"),
        ({"cross_result_ids": ()}, "cover every observation-pair"),
        ({"non_claim_keys": ()}, "NC-QB-BASE"),
        (
            {"aggregation_rule": replace(QB_CONSISTENCY_RULE, version="2")},
            "QB-CONSISTENCY-001 / 1",
        ),
        (
            {"non_claim_contract": replace(QB_NON_CLAIMS, version="2")},
            "QB-NON-CLAIMS-001 / 1",
        ),
    ],
)
def test_imp08_assessment_rejects_illegal_state_value_and_contract_combinations(
    changes: dict[str, object],
    message: str,
) -> None:
    snapshot = _snapshot(2)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
    )

    with pytest.raises(ValueError, match=message):
        replace(assessment, **changes)


def test_imp08_unknown_requires_a_material_unresolved_cause() -> None:
    snapshot = _snapshot(2)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
    )
    incomplete_metadata = replace(assessment.observability, rconf_complete=False)

    with pytest.raises(ValueError, match="material unresolved cause"):
        replace(
            assessment,
            state=QbConsistencyState.UNKNOWN,
            value=None,
            rconf_complete=False,
            observability=incomplete_metadata,
        )


def test_imp08_unknown_rejects_a_numeric_value_and_complete_rconf() -> None:
    snapshot = _snapshot(2)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.ASSESSMENT_UNRESOLVED),
    )

    with pytest.raises(ValueError, match="numeric value"):
        replace(assessment, value=Fraction(1, 1))

    complete_metadata = replace(assessment.observability, rconf_complete=True)
    with pytest.raises(ValueError, match="incomplete R_conf"):
        replace(
            assessment,
            rconf_complete=True,
            observability=complete_metadata,
        )


def test_imp08_computed_rejects_unresolved_inputs_and_incomplete_rconf() -> None:
    snapshot = _snapshot(3)
    unresolved = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
        _result(snapshot, 0, 2, CrossResultState.ASSESSMENT_UNRESOLVED),
        _result(snapshot, 1, 2, CrossResultState.OUTSIDE_V0_1_APPLICABILITY),
    )

    with pytest.raises(ValueError, match="unresolved material inputs"):
        replace(
            unresolved,
            state=QbConsistencyState.COMPUTED,
            value=Fraction(1, 1),
            reasons=(),
        )

    computed_snapshot = _snapshot(2)
    computed = _aggregate(
        computed_snapshot,
        _result(
            computed_snapshot,
            0,
            1,
            CrossResultState.COMPATIBLE_WITHIN_RULE,
        ),
    )
    incomplete_metadata = replace(computed.observability, rconf_complete=False)
    with pytest.raises(ValueError, match="complete R_conf"):
        replace(
            computed,
            rconf_complete=False,
            observability=incomplete_metadata,
        )


def test_imp08_not_applicable_rejects_numeric_value_and_incomplete_rconf() -> None:
    assessment = _aggregate(_snapshot(1))

    with pytest.raises(ValueError, match="numeric value"):
        replace(assessment, value=Fraction(1, 1))

    incomplete_metadata = replace(assessment.observability, rconf_complete=False)
    with pytest.raises(ValueError, match="complete empty R_conf"):
        replace(
            assessment,
            rconf_complete=False,
            observability=incomplete_metadata,
        )


def test_imp08_value_rejects_float_arithmetic() -> None:
    snapshot = _snapshot(2)
    assessment = _aggregate(
        snapshot,
        _result(snapshot, 0, 1, CrossResultState.COMPATIBLE_WITHIN_RULE),
    )

    with pytest.raises(TypeError, match="exact Fraction"):
        replace(assessment, value=1.0)


def test_imp08_repeated_aggregation_is_deterministic() -> None:
    snapshot = _snapshot(3)
    results = (
        _result(snapshot, 1, 2, CrossResultState.CONFIRMED_CONFLICT),
        _result(snapshot, 0, 2, CrossResultState.COMPATIBLE_WITHIN_RULE),
        _result(snapshot, 0, 1, CrossResultState.CONFIRMED_CONFLICT),
    )
    aggregator = QbConsistencyAggregator()

    first = aggregator.aggregate(snapshot, results, _materiality(snapshot))
    second = aggregator.aggregate(snapshot, results, _materiality(snapshot))

    assert first == second
    assert first.cross_result_ids == tuple(
        result.result_id for result in sorted(results, key=lambda item: item.order_key)
    )

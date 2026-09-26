from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from inspect import signature
from pathlib import Path

import pytest

from requirements_quality_assessment.cross_analysis import (
    RESULT_CANONICAL_VERSION,
    SNAPSHOT_CANONICAL_VERSION,
    AssessmentSnapshot,
    AssessmentSnapshotId,
    BoundedConflictSubtype,
    BoundedNonClaimKey,
    ComparisonKey,
    ComparisonOperand,
    ComparisonOperands,
    ConflictClass,
    ContractVersionDescriptor,
    CrossAnalysisContractManifest,
    CrossDiagnosticRef,
    CrossEvidenceOrderKey,
    CrossEvidenceRef,
    CrossObservationOrderKey,
    CrossObservationRef,
    CrossRelationKind,
    CrossRequirementResult,
    CrossResultId,
    CrossResultOrderKey,
    CrossResultState,
    CrossUnresolvedReason,
    OutsideApplicabilityReason,
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
    QuantitativeComponentName,
    UnitLabel,
)


GOLDEN = Path(__file__).parent / "fixtures" / "qb_snapshot_canonical_001.json"


def _descriptor(name: str, version: str = "1") -> ContractVersionDescriptor:
    return ContractVersionDescriptor(name, version)


def _contracts(**versions: str) -> CrossAnalysisContractManifest:
    return CrossAnalysisContractManifest(
        projection=_descriptor("QB-PROJECTION", versions.get("projection", "1")),
        normalization=_descriptor("QB-NORMALIZATION", versions.get("normalization", "1")),
        comparison=_descriptor("QB-COMPARISON", versions.get("comparison", "1")),
        materiality=_descriptor("QB-MATERIALITY", versions.get("materiality", "1")),
        aggregation=_descriptor("QB-AGGREGATION", versions.get("aggregation", "1")),
        coverage_profile=_descriptor("QB-v0.1", versions.get("coverage", "1")),
    )


def _evidence(
    requirement_id: str,
    evidence_id: str,
    requirement_text: str,
    surface: str,
    rule_id: str,
) -> SnapshotEvidenceManifest:
    start = requirement_text.index(surface)
    return SnapshotEvidenceManifest(
        ref=CrossEvidenceRef(requirement_id, evidence_id),
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        text=surface,
        start_offset=start,
        end_offset=start + len(surface),
        rule_id=rule_id,
    )


def _requirement(
    requirement_id: str,
    source_order: int,
    source_line: int,
    value: Decimal,
    *,
    comparator: ComparatorLabel = ComparatorLabel.LESS_THAN_OR_EQUAL,
) -> SnapshotRequirementManifest:
    text = f"Метрика {comparator.value} {value} SECOND Контекст"
    metric = _evidence(requirement_id, "M:E001", text, "Метрика", "M-RULE")
    bound_surface = f"{comparator.value} {value} SECOND"
    bound = _evidence(requirement_id, "B:E001", text, bound_surface, "B-RULE")
    context = _evidence(requirement_id, "C:E001", text, "Контекст", "C-RULE")
    refs = (metric.ref, bound.ref, context.ref)
    observation = SnapshotObservationManifest(
        ref=CrossObservationRef(
            requirement_id,
            FeatureId.QUANTITATIVE_CONSTRAINT,
            0,
        ),
        metric_evidence_refs=(metric.ref,),
        comparator=comparator,
        inclusivity=BoundaryInclusivity.INCLUSIVE,
        comparator_evidence_refs=(bound.ref,),
        value=value,
        value_evidence_refs=(bound.ref,),
        unit=UnitLabel.SECOND,
        unit_evidence_refs=(bound.ref,),
        context_evidence_refs=(context.ref,),
        unresolved_components=(),
        evidence_refs=refs,
    )
    return SnapshotRequirementManifest(
        requirement_id=requirement_id,
        source_order=source_order,
        source_line=source_line,
        text=text,
        processing_status=DetectionProcessingStatus.COMPLETE,
        observations=(observation,),
        evidence=(metric, bound, context),
        diagnostics=(),
    )


def _snapshot(
    *,
    left_value: Decimal = Decimal("2.00"),
    right_value: Decimal = Decimal("5"),
    contracts: CrossAnalysisContractManifest | None = None,
) -> AssessmentSnapshot:
    requirements = (
        _requirement("R001", 0, 1, left_value),
        _requirement(
            "R002",
            1,
            2,
            right_value,
            comparator=ComparatorLabel.GREATER_THAN_OR_EQUAL,
        ),
    )
    return AssessmentSnapshot(
        requirements=requirements,
        contracts=contracts or _contracts(),
        counts=SnapshotCountManifest.from_requirements(requirements),
    )


def _empty_snapshot() -> AssessmentSnapshot:
    requirements = ()
    return AssessmentSnapshot(
        requirements=requirements,
        contracts=_contracts(),
        counts=SnapshotCountManifest.from_requirements(requirements),
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


def _result_values(snapshot: AssessmentSnapshot) -> dict[str, object]:
    left = _operand(snapshot, "R001", ComparatorLabel.LESS_THAN_OR_EQUAL, Decimal("2"))
    right = _operand(
        snapshot,
        "R002",
        ComparatorLabel.GREATER_THAN_OR_EQUAL,
        Decimal("5"),
    )
    return {
        "snapshot_id": snapshot.snapshot_id,
        "participants": (RequirementOrderKey(0, "R001"), RequirementOrderKey(1, "R002")),
        "observation_refs": (left.observation_ref, right.observation_ref),
        "operands": ComparisonOperands(left, right),
        "comparison_contract": snapshot.contracts.comparison,
        "coverage_profile": snapshot.contracts.coverage_profile,
        "relation_kind": CrossRelationKind.QUANTITATIVE_BOUND,
        "evidence_refs": (
            CrossEvidenceRef("R001", "B:E001"),
            CrossEvidenceRef("R002", "B:E001"),
        ),
        "diagnostic_refs": (),
        "comparison_key": ComparisonKey("метрика", "контекст", UnitLabel.SECOND),
        "non_claim_keys": (BoundedNonClaimKey.NC_QB_BASE,),
    }


def _confirmed(snapshot: AssessmentSnapshot) -> CrossRequirementResult:
    return CrossRequirementResult.confirmed_conflict(**_result_values(snapshot))


def _result_for_state(
    snapshot: AssessmentSnapshot,
    state: CrossResultState,
) -> CrossRequirementResult:
    values = _result_values(snapshot)
    if state is CrossResultState.CONFIRMED_CONFLICT:
        return CrossRequirementResult.confirmed_conflict(**values)
    if state is CrossResultState.COMPATIBLE_WITHIN_RULE:
        return CrossRequirementResult.compatible_within_rule(**values)
    values.pop("comparison_key")
    if state is CrossResultState.ASSESSMENT_UNRESOLVED:
        return CrossRequirementResult.assessment_unresolved(
            unresolved_reasons=(CrossUnresolvedReason.MISSING_METRIC,),
            diagnostic_refs=(
                CrossDiagnosticRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0),
            ),
            **{key: value for key, value in values.items() if key != "diagnostic_refs"},
        )
    return CrossRequirementResult.outside_v0_1_applicability(
        outside_reasons=(OutsideApplicabilityReason.METRIC_MISMATCH,),
        **values,
    )


def test_canonical_versions_are_explicit() -> None:
    assert SNAPSHOT_CANONICAL_VERSION == "QB-SNAPSHOT-CANONICAL-001"
    assert RESULT_CANONICAL_VERSION == "QB-RESULT-CANONICAL-001"


@pytest.mark.parametrize(
    ("factory", "args"),
    [
        (CrossEvidenceRef, ("", "E001")),
        (CrossEvidenceRef, ("R001", " E001")),
        (ContractVersionDescriptor, ("RULE", "")),
        (RequirementOrderKey, (-1, "R001")),
        (CrossEvidenceOrderKey, (0, 5, 4, "E001")),
    ],
)
def test_primitives_reject_malformed_identifiers_and_indexes(factory, args) -> None:
    with pytest.raises((TypeError, ValueError)):
        factory(*args)


def test_qualified_refs_have_the_approved_shape() -> None:
    observation = CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0)
    evidence = CrossEvidenceRef("R001", "QUANT-001:E001")
    diagnostic = CrossDiagnosticRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 1)

    assert (observation.requirement_id, observation.observation_index) == ("R001", 0)
    assert (evidence.requirement_id, evidence.evidence_id) == (
        "R001",
        "QUANT-001:E001",
    )
    assert (diagnostic.requirement_id, diagnostic.diagnostic_index) == ("R001", 1)


@pytest.mark.parametrize("ref_type", [CrossObservationRef, CrossDiagnosticRef])
def test_feature_qualified_refs_reject_non_quantitative_feature(ref_type) -> None:
    with pytest.raises(ValueError, match="quantitative"):
        ref_type("R001", FeatureId.EXPECTED_RESULT, 0)


@pytest.mark.parametrize("index", [-1, True, 1.5])
def test_feature_qualified_refs_reject_malformed_index(index) -> None:
    with pytest.raises((TypeError, ValueError)):
        CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, index)


def test_contract_manifest_is_immutable_and_rejects_duplicate_roles() -> None:
    contracts = _contracts()
    with pytest.raises(FrozenInstanceError):
        contracts.projection = _descriptor("OTHER")
    with pytest.raises(ValueError, match="unique"):
        CrossAnalysisContractManifest(
            projection=_descriptor("SAME"),
            normalization=_descriptor("SAME"),
            comparison=_descriptor("C"),
            materiality=_descriptor("M"),
            aggregation=_descriptor("A"),
            coverage_profile=_descriptor("P"),
        )


def test_typed_reason_vocabularies_are_exact() -> None:
    assert {item.value for item in CrossUnresolvedReason} == {
        "MISSING_METRIC",
        "UNRESOLVED_METRIC",
        "MISSING_CONTEXT",
        "UNRESOLVED_CONTEXT",
        "MISSING_UNIT",
        "MISSING_VALUE",
        "MISSING_COMPARATOR",
        "UNRESOLVED_INCLUSIVITY",
        "MATERIAL_UNRESOLVED_EXTRACTION",
    }
    assert {item.value for item in OutsideApplicabilityReason} == {
        "METRIC_MISMATCH",
        "CONTEXT_MISMATCH",
        "UNIT_MISMATCH",
        "COMPARATOR_OUTSIDE_PROFILE",
    }


def test_reason_tuples_require_approved_order_and_pair_reasons_exclude_aggregate_reason() -> None:
    values = _result_values(_snapshot())
    values.pop("comparison_key")
    with pytest.raises(ValueError, match="deterministic order"):
        CrossRequirementResult.assessment_unresolved(
            unresolved_reasons=(
                CrossUnresolvedReason.MISSING_CONTEXT,
                CrossUnresolvedReason.MISSING_METRIC,
            ),
            **values,
        )
    with pytest.raises(ValueError, match="aggregate-level"):
        CrossRequirementResult.assessment_unresolved(
            unresolved_reasons=(CrossUnresolvedReason.MATERIAL_UNRESOLVED_EXTRACTION,),
            **values,
        )


def test_supplied_comparator_and_processing_shapes_fail_fast_when_corrupt() -> None:
    requirement = _requirement("R001", 0, 1, Decimal("2"))
    with pytest.raises(ValueError, match="inclusivity"):
        replace(requirement.observations[0], inclusivity=BoundaryInclusivity.UNRESOLVED)
    with pytest.raises(ValueError, match="requires diagnostics"):
        replace(requirement, processing_status=DetectionProcessingStatus.INCOMPLETE)

    snapshot = _snapshot()
    operand = _operand(snapshot, "R001", ComparatorLabel.LESS_THAN_OR_EQUAL, Decimal("2"))
    with pytest.raises(ValueError, match="inclusivity"):
        replace(operand, inclusivity=BoundaryInclusivity.UNRESOLVED)


def _anchor_observation(
    *,
    metric: bool = False,
    comparator: bool = False,
    value: bool = False,
    unit: bool = False,
    context: bool = False,
) -> SnapshotObservationManifest:
    metric_ref = CrossEvidenceRef("R001", "M:E001")
    bound_ref = CrossEvidenceRef("R001", "B:E001")
    context_ref = CrossEvidenceRef("R001", "C:E001")
    metric_refs = (metric_ref,) if metric else ()
    comparator_refs = (bound_ref,) if comparator else ()
    value_refs = (bound_ref,) if value else ()
    unit_refs = (bound_ref,) if unit else ()
    context_refs = (context_ref,) if context else ()
    evidence_refs = tuple(
        dict.fromkeys(
            metric_refs + comparator_refs + value_refs + unit_refs + context_refs
        )
    )
    return SnapshotObservationManifest(
        ref=CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0),
        metric_evidence_refs=metric_refs,
        comparator=ComparatorLabel.LESS_THAN_OR_EQUAL if comparator else None,
        inclusivity=BoundaryInclusivity.INCLUSIVE if comparator else None,
        comparator_evidence_refs=comparator_refs,
        value=Decimal("2") if value else None,
        value_evidence_refs=value_refs,
        unit=UnitLabel.SECOND if unit else None,
        unit_evidence_refs=unit_refs,
        context_evidence_refs=context_refs,
        unresolved_components=(),
        evidence_refs=evidence_refs,
    )


@pytest.mark.parametrize(
    "components",
    [
        {"metric": True},
        {"context": True},
        {"value": True},
        {"comparator": True},
        {"unit": True},
    ],
    ids=[
        "metric-only",
        "context-only",
        "value-only",
        "comparator-without-value",
        "unit-without-value",
    ],
)
def test_snapshot_observation_rejects_impossible_source_anchor(components) -> None:
    with pytest.raises(ValueError, match="requires value and either comparator or unit"):
        _anchor_observation(**components)


@pytest.mark.parametrize(
    "components",
    [
        {"comparator": True, "value": True},
        {"value": True, "unit": True},
        {
            "metric": True,
            "comparator": True,
            "value": True,
            "unit": True,
            "context": True,
        },
    ],
    ids=["comparator-and-value", "value-and-unit", "fully-linked"],
)
def test_snapshot_observation_accepts_frozen_source_anchor_forms(components) -> None:
    assert isinstance(_anchor_observation(**components), SnapshotObservationManifest)


def test_manifest_rejects_foreign_and_dangling_ownership() -> None:
    valid = _requirement("R001", 0, 1, Decimal("2"))
    with pytest.raises(ValueError, match="owner"):
        replace(
            valid.observations[0],
            ref=CrossObservationRef("R999", FeatureId.QUANTITATIVE_CONSTRAINT, 0),
        )

    missing = CrossEvidenceRef("R001", "MISSING")
    dangling = replace(
        valid.observations[0],
        metric_evidence_refs=valid.observations[0].metric_evidence_refs + (missing,),
        evidence_refs=valid.observations[0].evidence_refs + (missing,),
    )
    with pytest.raises(ValueError, match="dangling"):
        replace(valid, observations=(dangling,))


def test_manifest_rejects_duplicate_requirement_identity_and_noncanonical_order() -> None:
    first = _requirement("R001", 0, 1, Decimal("2"))
    duplicate = _requirement("R001", 1, 2, Decimal("5"))
    requirements = (first, duplicate)
    with pytest.raises(ValueError, match="duplicates"):
        AssessmentSnapshot(
            requirements=requirements,
            contracts=_contracts(),
            counts=SnapshotCountManifest.from_requirements(requirements),
        )

    reversed_order = (
        _requirement("R001", 1, 1, Decimal("2")),
        _requirement("R002", 0, 2, Decimal("5")),
    )
    with pytest.raises(ValueError, match="source order"):
        AssessmentSnapshot(
            requirements=reversed_order,
            contracts=_contracts(),
            counts=SnapshotCountManifest.from_requirements(reversed_order),
        )


def test_snapshot_rejects_incorrect_count_manifest() -> None:
    requirements = (_requirement("R001", 0, 1, Decimal("2")),)
    counts = SnapshotCountManifest.from_requirements(requirements)
    incorrect_entry = replace(counts.requirements[0], evidence_count=4)
    incorrect = replace(counts, evidence_count=4, requirements=(incorrect_entry,))
    with pytest.raises(ValueError, match="does not match"):
        AssessmentSnapshot(requirements, _contracts(), incorrect)


def test_same_snapshot_input_has_same_identity() -> None:
    assert _snapshot().snapshot_id == _snapshot().snapshot_id
    assert _snapshot().canonical_bytes() == _snapshot().canonical_bytes()


def test_changed_qb_manifest_fact_changes_snapshot_identity() -> None:
    original = _snapshot()
    requirements = (
        replace(original.requirements[0], source_line=11),
        original.requirements[1],
    )
    changed = AssessmentSnapshot(
        requirements,
        original.contracts,
        SnapshotCountManifest.from_requirements(requirements),
    )
    assert changed.snapshot_id != original.snapshot_id


def test_changed_contract_version_changes_snapshot_identity() -> None:
    assert _snapshot().snapshot_id != _snapshot(contracts=_contracts(comparison="2")).snapshot_id


def test_local_quality_and_reporting_data_are_not_snapshot_inputs() -> None:
    parameters = signature(AssessmentSnapshot).parameters
    assert "quality_profile" not in parameters
    assert "characteristic_assessments" not in parameters
    assert "trace" not in parameters
    assert "explanation" not in parameters
    assert "report" not in parameters
    assert "path" not in parameters
    assert "timestamp" not in parameters


def test_snapshot_canonical_encoding_matches_golden_fixture() -> None:
    golden = GOLDEN.read_text(encoding="utf-8").rstrip("\r\n").encode("utf-8")
    assert _empty_snapshot().canonical_bytes() == golden


def test_decimal_encoding_is_exact_and_scale_sensitive() -> None:
    two_places = _snapshot(left_value=Decimal("2.00"))
    one_place = _snapshot(left_value=Decimal("2.0"))

    assert two_places.snapshot_id != one_place.snapshot_id
    assert b'["exponent","-2"]' in two_places.canonical_bytes()
    assert b'["digits","2","0","0"]' in two_places.canonical_bytes()


def test_ordering_keys_follow_source_and_observation_semantics() -> None:
    keys = [
        CrossObservationOrderKey(RequirementOrderKey(1, "R002"), 0),
        CrossObservationOrderKey(RequirementOrderKey(0, "R001"), 1),
        CrossObservationOrderKey(RequirementOrderKey(0, "R001"), 0),
    ]
    assert sorted(keys) == [keys[2], keys[1], keys[0]]

    evidence_keys = [
        CrossEvidenceOrderKey(1, 0, 2, "E001"),
        CrossEvidenceOrderKey(0, 5, 7, "E002"),
        CrossEvidenceOrderKey(0, 1, 3, "E003"),
    ]
    assert sorted(evidence_keys) == [evidence_keys[2], evidence_keys[1], evidence_keys[0]]


def test_all_four_result_states_have_valid_constructors() -> None:
    snapshot = _snapshot()
    values = _result_values(snapshot)
    confirmed = CrossRequirementResult.confirmed_conflict(**values)
    compatible = CrossRequirementResult.compatible_within_rule(**values)

    unresolved_values = values | {
        "comparison_key": None,
        "diagnostic_refs": (
            CrossDiagnosticRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0),
        ),
    }
    unresolved = CrossRequirementResult.assessment_unresolved(
        unresolved_reasons=(CrossUnresolvedReason.UNRESOLVED_METRIC,),
        **{key: value for key, value in unresolved_values.items() if key != "comparison_key"},
    )
    outside = CrossRequirementResult.outside_v0_1_applicability(
        outside_reasons=(OutsideApplicabilityReason.METRIC_MISMATCH,),
        **{key: value for key, value in values.items() if key != "comparison_key"},
    )

    assert [item.state for item in (confirmed, compatible, unresolved, outside)] == list(
        CrossResultState
    )
    assert confirmed.conflict_class is ConflictClass.LOGICAL_CONFLICT
    assert (
        confirmed.conflict_subtype
        is BoundedConflictSubtype.DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY
    )
    assert compatible.conflict_subtype is None


@pytest.mark.parametrize("state", list(CrossResultState))
@pytest.mark.parametrize(
    "evidence_refs",
    [
        (),
        (CrossEvidenceRef("R001", "B:E001"),),
        (CrossEvidenceRef("R002", "B:E001"),),
    ],
    ids=["empty", "left-only", "right-only"],
)
def test_every_result_state_requires_evidence_from_both_participants(
    state: CrossResultState,
    evidence_refs: tuple[CrossEvidenceRef, ...],
) -> None:
    result = _result_for_state(_snapshot(), state)
    with pytest.raises(ValueError, match="Evidence from both participants"):
        replace(result, evidence_refs=evidence_refs)


@pytest.mark.parametrize("state", list(CrossResultState))
def test_every_result_state_rejects_foreign_evidence(state: CrossResultState) -> None:
    result = _result_for_state(_snapshot(), state)
    with pytest.raises(ValueError, match="owned by a participant"):
        replace(
            result,
            evidence_refs=result.evidence_refs + (CrossEvidenceRef("R999", "E001"),),
        )


def test_diagnostics_are_supplemental_to_both_participant_evidence() -> None:
    result = _result_for_state(_snapshot(), CrossResultState.ASSESSMENT_UNRESOLVED)
    assert result.diagnostic_refs
    with pytest.raises(ValueError, match="Evidence from both participants"):
        replace(
            result,
            evidence_refs=(CrossEvidenceRef("R001", "B:E001"),),
        )


@pytest.mark.parametrize(
    "changes",
    [
        {"conflict_class": None},
        {"conflict_subtype": None},
        {"unresolved_reasons": (CrossUnresolvedReason.MISSING_METRIC,)},
        {"outside_reasons": (OutsideApplicabilityReason.UNIT_MISMATCH,)},
        {"comparison_key": None},
        {"evidence_refs": (CrossEvidenceRef("R001", "B:E001"),)},
    ],
)
def test_confirmed_conflict_rejects_every_illegal_field_family(changes) -> None:
    with pytest.raises(ValueError):
        replace(_confirmed(_snapshot()), **changes)


@pytest.mark.parametrize(
    "changes",
    [
        {"conflict_class": ConflictClass.LOGICAL_CONFLICT},
        {
            "conflict_subtype": BoundedConflictSubtype.DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY
        },
        {"unresolved_reasons": (CrossUnresolvedReason.MISSING_CONTEXT,)},
        {"outside_reasons": (OutsideApplicabilityReason.CONTEXT_MISMATCH,)},
    ],
)
def test_compatible_rejects_conflict_and_reason_payloads(changes) -> None:
    result = CrossRequirementResult.compatible_within_rule(**_result_values(_snapshot()))
    with pytest.raises(ValueError):
        replace(result, **changes)


def test_unresolved_requires_typed_reason_and_both_evidence_owners() -> None:
    snapshot = _snapshot()
    values = _result_values(snapshot)
    values.pop("comparison_key")
    with pytest.raises(ValueError, match="typed unresolved reasons"):
        CrossRequirementResult.assessment_unresolved(unresolved_reasons=(), **values)
    values["evidence_refs"] = ()
    with pytest.raises(ValueError, match="Evidence from both participants"):
        CrossRequirementResult.assessment_unresolved(
            unresolved_reasons=(CrossUnresolvedReason.MISSING_METRIC,),
            **values,
        )


def test_outside_requires_reason_and_is_never_compatible() -> None:
    values = _result_values(_snapshot())
    values.pop("comparison_key")
    with pytest.raises(ValueError, match="typed outside reasons"):
        CrossRequirementResult.outside_v0_1_applicability(outside_reasons=(), **values)


def test_results_reject_self_pair_reversed_pair_and_foreign_ownership() -> None:
    result = _confirmed(_snapshot())
    with pytest.raises(ValueError, match="self-pair"):
        replace(
            result,
            participants=(RequirementOrderKey(0, "R001"), RequirementOrderKey(1, "R001")),
        )
    with pytest.raises(ValueError, match="source ordered"):
        replace(result, participants=tuple(reversed(result.participants)))
    with pytest.raises(ValueError, match="participant"):
        replace(
            result,
            evidence_refs=result.evidence_refs + (CrossEvidenceRef("R999", "E001"),),
        )


def test_results_reject_cross_snapshot_composition() -> None:
    first = _snapshot()
    second = _snapshot(contracts=_contracts(projection="2"))
    result = _confirmed(first)
    foreign_left = replace(result.operands.left, snapshot_id=second.snapshot_id)
    with pytest.raises(ValueError, match="cross snapshots"):
        replace(result, operands=ComparisonOperands(foreign_left, result.operands.right))


def test_same_result_inputs_have_same_stable_result_id() -> None:
    snapshot = _snapshot()
    assert _confirmed(snapshot).result_id == _confirmed(snapshot).result_id


def test_valid_canonical_identity_remains_stable_after_invariant_tightening() -> None:
    snapshot = _snapshot()
    assert snapshot.snapshot_id.value == (
        "qb-snapshot-sha256:9d0056ed37b9215e6f81c2f1950d0d51"
        "c1195490561f58a94917724a535e19f7"
    )
    assert _confirmed(snapshot).result_id.value == (
        "qb-result-sha256:d2680f29680df1400b03af14eb301beaf"
        "723794c31de1c8f47c5d941bba6159f"
    )


def test_result_identity_changes_with_state_and_contract_version() -> None:
    snapshot = _snapshot()
    confirmed = _confirmed(snapshot)
    compatible = CrossRequirementResult.compatible_within_rule(**_result_values(snapshot))
    changed_contract = replace(
        confirmed,
        comparison_contract=_descriptor("QB-COMPARISON", "2"),
    )

    assert confirmed.result_id != compatible.result_id
    assert confirmed.result_id != changed_contract.result_id


def test_result_order_is_requirement_then_observation_then_rule_then_id() -> None:
    first = _confirmed(_snapshot())
    later_observation = replace(
        first,
        observation_refs=(
            replace(first.observation_refs[0], observation_index=1),
            first.observation_refs[1],
        ),
        operands=ComparisonOperands(
            replace(
                first.operands.left,
                observation_ref=replace(first.observation_refs[0], observation_index=1),
            ),
            first.operands.right,
        ),
    )
    assert first.order_key < later_observation.order_key
    assert isinstance(first.order_key, CrossResultOrderKey)


def test_stable_identity_wrappers_reject_arbitrary_ids() -> None:
    with pytest.raises(ValueError, match="SHA-256"):
        AssessmentSnapshotId("random")
    with pytest.raises(ValueError, match="SHA-256"):
        CrossResultId("random")


def test_domain_values_are_frozen_and_authoritative_collections_are_tuples() -> None:
    snapshot = _snapshot()
    result = _confirmed(snapshot)
    with pytest.raises(FrozenInstanceError):
        result.state = CrossResultState.COMPATIBLE_WITHIN_RULE
    assert isinstance(snapshot.requirements, tuple)
    assert isinstance(result.evidence_refs, tuple)


def test_diagnostic_manifest_validates_shape_and_source_round_trip() -> None:
    text = "Метрика 500"
    diagnostic = SnapshotDiagnosticManifest(
        ref=CrossDiagnosticRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0),
        code="QUANT_UNRESOLVED_NUMERIC_CANDIDATE",
        rule_id="QUANT-001",
        candidate_text="500",
        start_offset=8,
        end_offset=11,
    )
    assert diagnostic.candidate_text == "500"
    with pytest.raises(ValueError, match="all present or all absent"):
        replace(diagnostic, end_offset=None)


def test_non_claim_key_is_the_bounded_approved_key() -> None:
    assert tuple(BoundedNonClaimKey) == (BoundedNonClaimKey.NC_QB_BASE,)
    with pytest.raises(ValueError, match="NC-QB-BASE"):
        replace(_confirmed(_snapshot()), non_claim_keys=())

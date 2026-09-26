from dataclasses import replace
from decimal import Decimal

import pytest

from requirements_quality_assessment.cross_analysis import (
    AssessmentSnapshot,
    BoundedConflictSubtype,
    ComparisonOperand,
    ComparisonOperands,
    CrossAnalysisContractManifest,
    CrossEvidenceRef,
    CrossEvidenceResolver,
    CrossObservationRef,
    CrossRequirementProjection,
    CrossResultState,
    CrossUnresolvedReason,
    ExhaustivePairSelector,
    OutsideApplicabilityReason,
    QB_COMPARISON_RULE,
    QB_CONTRACT_MANIFEST,
    QB_COVERAGE_PROFILE,
    QbApplicabilityEvaluator,
    QbObservationPairAssessor,
    QbSupportedBoundValidator,
    SnapshotCountManifest,
    SnapshotEvidenceManifest,
    SnapshotObservationManifest,
    SnapshotRequirementManifest,
    SupportedBoundDirection,
    direct_bound_conflict,
    normalize_qb_identity_text,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorComponent,
    ComparatorLabel,
    DetectionProcessingStatus,
    Evidence,
    FeatureId,
    NumericValueComponent,
    QuantitativeComponentName,
    QuantitativeConstraintObservation,
    Requirement,
    TextComponent,
    UnitComponent,
    UnitLabel,
)


def _projection(
    left: dict,
    right: dict,
    *,
    contracts: CrossAnalysisContractManifest = QB_CONTRACT_MANIFEST,
) -> CrossRequirementProjection:
    requirement_manifests = []
    requirements = []
    observations = []
    evidence_values = []

    for source_order, values in enumerate((left, right)):
        requirement_id = f"R{source_order + 1:03d}"
        metric = values.get("metric", "Час відгуку")
        context = values.get("context", "при 500 одночасних користувачах")
        comparator = values.get("comparator", ComparatorLabel.LESS_THAN_OR_EQUAL)
        inclusivity = values.get(
            "inclusivity",
            (
                BoundaryInclusivity.UNRESOLVED
                if comparator is ComparatorLabel.UPPER_BOUND
                else None
                if comparator is ComparatorLabel.NOT_LESS_FREQUENT or comparator is None
                else BoundaryInclusivity.INCLUSIVE
            ),
        )
        value = values.get("value", Decimal("2"))
        unit = values.get("unit", UnitLabel.SECOND)
        unresolved = values.get("unresolved", ())

        surfaces = []
        if metric is not None:
            surfaces.append(("M", metric, "METRIC-RULE"))
        bound_surface = values.get("bound_surface", f"межа-{source_order + 1}")
        surfaces.append(("B", bound_surface, "BOUND-RULE"))
        if context is not None:
            surfaces.append(("C", context, "CONTEXT-RULE"))
        text = "[" + "] | [".join(item[1] for item in surfaces) + "]"
        requirement = Requirement(requirement_id, source_order + 1, text)

        source_evidence = []
        manifests = []
        refs = {}
        search_from = 0
        for code, surface, rule_id in surfaces:
            start = text.index(surface, search_from)
            search_from = start + len(surface)
            evidence_id = f"{code}:E001"
            ref = CrossEvidenceRef(requirement_id, evidence_id)
            item = Evidence(
                evidence_id=evidence_id,
                requirement_id=requirement_id,
                feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
                text=surface,
                start_offset=start,
                end_offset=start + len(surface),
                rule_id=rule_id,
            )
            source_evidence.append(item)
            manifests.append(
                SnapshotEvidenceManifest(
                    ref=ref,
                    feature_id=item.feature_id,
                    text=item.text,
                    start_offset=item.start_offset,
                    end_offset=item.end_offset,
                    rule_id=item.rule_id,
                )
            )
            refs[code] = evidence_id

        metric_component = None if metric is None else TextComponent((refs["M"],))
        comparator_component = (
            None
            if comparator is None
            else ComparatorComponent(comparator, inclusivity, (refs["B"],))
        )
        value_component = (
            None if value is None else NumericValueComponent(value, (refs["B"],))
        )
        unit_component = (
            None if unit is None else UnitComponent(unit, (refs["B"],))
        )
        context_component = None if context is None else TextComponent((refs["C"],))
        component_ids = tuple(
            dict.fromkeys(
                evidence_id
                for component in (
                    metric_component,
                    comparator_component,
                    value_component,
                    unit_component,
                    context_component,
                )
                if component is not None
                for evidence_id in component.evidence_refs
            )
        )
        source_observation = QuantitativeConstraintObservation(
            feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
            metric=metric_component,
            comparator=comparator_component,
            value=value_component,
            unit=unit_component,
            context=context_component,
            unresolved_components=unresolved,
            evidence_refs=component_ids,
        )
        observation_ref = CrossObservationRef(
            requirement_id, FeatureId.QUANTITATIVE_CONSTRAINT, 0
        )
        qualify = lambda ids: tuple(
            CrossEvidenceRef(requirement_id, item) for item in ids
        )
        manifest_observation = SnapshotObservationManifest(
            ref=observation_ref,
            metric_evidence_refs=qualify(
                () if metric_component is None else metric_component.evidence_refs
            ),
            comparator=comparator,
            inclusivity=inclusivity,
            comparator_evidence_refs=qualify(
                ()
                if comparator_component is None
                else comparator_component.evidence_refs
            ),
            value=value,
            value_evidence_refs=qualify(
                () if value_component is None else value_component.evidence_refs
            ),
            unit=unit,
            unit_evidence_refs=qualify(
                () if unit_component is None else unit_component.evidence_refs
            ),
            context_evidence_refs=qualify(
                () if context_component is None else context_component.evidence_refs
            ),
            unresolved_components=unresolved,
            evidence_refs=qualify(component_ids),
        )
        requirement_manifests.append(
            SnapshotRequirementManifest(
                requirement_id=requirement_id,
                source_order=source_order,
                source_line=source_order + 1,
                text=text,
                processing_status=DetectionProcessingStatus.COMPLETE,
                observations=(manifest_observation,),
                evidence=tuple(manifests),
                diagnostics=(),
            )
        )
        requirements.append((requirement_id, requirement))
        observations.append((observation_ref, source_observation))
        evidence_values.extend(
            (CrossEvidenceRef(requirement_id, item.evidence_id), item)
            for item in source_evidence
        )

    manifest_tuple = tuple(requirement_manifests)
    snapshot = AssessmentSnapshot(
        requirements=manifest_tuple,
        contracts=contracts,
        counts=SnapshotCountManifest.from_requirements(manifest_tuple),
    )
    resolver = CrossEvidenceResolver(
        snapshot_id=snapshot.snapshot_id,
        _requirements=tuple(requirements),
        _evidence=tuple(evidence_values),
        _observations=tuple(observations),
        _diagnostics=(),
    )
    return CrossRequirementProjection(snapshot=snapshot, resolver=resolver)


def _assess(left: dict, right: dict):
    projection = _projection(left, right)
    candidate = ExhaustivePairSelector().select(projection)[0]
    return QbObservationPairAssessor().assess(candidate, projection)


def test_normalization_is_exact_nfc_casefold_whitespace_and_trim() -> None:
    assert normalize_qb_identity_text(" \tЧАС\u00a0 ДІИ\u0306\n") == "час дій"
    assert normalize_qb_identity_text("Метрика, А") == "метрика, а"
    assert normalize_qb_identity_text("Метрика А") == "метрика а"


def test_rc_qb_001_and_002_conflict_in_either_operand_order() -> None:
    upper = {"comparator": ComparatorLabel.LESS_THAN_OR_EQUAL, "value": Decimal("2")}
    lower = {
        "comparator": ComparatorLabel.GREATER_THAN_OR_EQUAL,
        "value": Decimal("5"),
    }

    first = _assess(upper, lower)
    reversed_result = _assess(lower, upper)

    for result in (first, reversed_result):
        assert result.state is CrossResultState.CONFIRMED_CONFLICT
        assert (
            result.conflict_subtype
            is BoundedConflictSubtype.DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY
        )
        assert result.comparison_contract == QB_COMPARISON_RULE
        assert result.coverage_profile == QB_COVERAGE_PROFILE


@pytest.mark.parametrize(
    ("left_comparator", "left_value", "right_comparator", "right_value"),
    [
        (ComparatorLabel.LESS_THAN_OR_EQUAL, "5", ComparatorLabel.GREATER_THAN_OR_EQUAL, "2"),
        (ComparatorLabel.LESS_THAN_OR_EQUAL, "2", ComparatorLabel.LESS_THAN_OR_EQUAL, "5"),
        (ComparatorLabel.GREATER_THAN_OR_EQUAL, "5", ComparatorLabel.GREATER_THAN_OR_EQUAL, "2"),
        (ComparatorLabel.LESS_THAN_OR_EQUAL, "5", ComparatorLabel.GREATER_THAN_OR_EQUAL, "5"),
    ],
    ids=["RC-QB-004", "two-uppers", "RC-QB-006", "RC-QB-007"],
)
def test_supported_compatible_predicate_cases(
    left_comparator, left_value, right_comparator, right_value
) -> None:
    result = _assess(
        {"comparator": left_comparator, "value": Decimal(left_value)},
        {"comparator": right_comparator, "value": Decimal(right_value)},
    )

    assert result.state is CrossResultState.COMPATIBLE_WITHIN_RULE
    assert result.comparison_key.normalized_metric == "час відгуку"
    assert result.comparison_key.normalized_context == "при 500 одночасних користувачах"
    assert result.comparison_key.unit is UnitLabel.SECOND


def test_rc_qb_008_normalization_reaches_same_key() -> None:
    result = _assess(
        {"metric": " ЧАС\u00a0 ДІЙ ", "context": "ПІД ЧАС  ДІЙ"},
        {"metric": "час діи\u0306", "context": "під час діи\u0306"},
    )

    assert result.state is CrossResultState.COMPATIBLE_WITHIN_RULE
    assert result.comparison_key.normalized_metric == "час дій"
    assert result.comparison_key.normalized_context == "під час дій"


@pytest.mark.parametrize(
    ("left", "right", "reason"),
    [
        (
            {"metric": "час відгуку"},
            {"metric": "час відповіді"},
            OutsideApplicabilityReason.METRIC_MISMATCH,
        ),
        (
            {"context": "стандартне навантаження"},
            {"context": "пікове навантаження"},
            OutsideApplicabilityReason.CONTEXT_MISMATCH,
        ),
        (
            {"unit": UnitLabel.SECOND},
            {"unit": UnitLabel.MINUTE},
            OutsideApplicabilityReason.UNIT_MISMATCH,
        ),
    ],
    ids=["RC-QB-009", "RC-QB-010", "RC-QB-012"],
)
def test_resolved_identity_mismatches_are_outside(left, right, reason) -> None:
    result = _assess(left, right)

    assert result.state is CrossResultState.OUTSIDE_V0_1_APPLICABILITY
    assert result.outside_reasons == (reason,)
    assert result.comparison_key is None


def test_punctuation_remains_significant() -> None:
    result = _assess({"metric": "час, відгуку"}, {"metric": "час відгуку"})

    assert result.outside_reasons == (OutsideApplicabilityReason.METRIC_MISMATCH,)


def test_mismatch_precedes_unrelated_missing_field() -> None:
    result = _assess(
        {"metric": "метрика а", "context": None},
        {"metric": "метрика б", "context": None},
    )

    assert result.state is CrossResultState.OUTSIDE_V0_1_APPLICABILITY
    assert result.outside_reasons == (OutsideApplicabilityReason.METRIC_MISMATCH,)
    assert result.unresolved_reasons == ()


def test_rc_qb_015_explicit_unresolved_metric_and_context() -> None:
    result = _assess(
        {
            "metric": None,
            "unresolved": (QuantitativeComponentName.METRIC,),
        },
        {
            "context": None,
            "unresolved": (QuantitativeComponentName.CONTEXT,),
        },
    )

    assert result.state is CrossResultState.ASSESSMENT_UNRESOLVED
    assert result.unresolved_reasons == (
        CrossUnresolvedReason.UNRESOLVED_METRIC,
        CrossUnresolvedReason.UNRESOLVED_CONTEXT,
    )


def test_missing_inputs_and_upper_bound_inclusivity_reasons_are_complete() -> None:
    result = _assess(
        {
            "metric": None,
            "context": None,
            "comparator": ComparatorLabel.UPPER_BOUND,
            "unit": None,
        },
        {},
    )

    assert result.state is CrossResultState.ASSESSMENT_UNRESOLVED
    assert result.unresolved_reasons == (
        CrossUnresolvedReason.MISSING_METRIC,
        CrossUnresolvedReason.MISSING_CONTEXT,
        CrossUnresolvedReason.MISSING_UNIT,
        CrossUnresolvedReason.UNRESOLVED_INCLUSIVITY,
    )


def test_rc_qb_017_outside_comparator_precedes_identity_inputs() -> None:
    result = _assess(
        {
            "metric": None,
            "context": None,
            "comparator": ComparatorLabel.NOT_LESS_FREQUENT,
        },
        {},
    )

    assert result.state is CrossResultState.OUTSIDE_V0_1_APPLICABILITY
    assert result.outside_reasons == (
        OutsideApplicabilityReason.COMPARATOR_OUTSIDE_PROFILE,
    )


def _operand(**changes) -> ComparisonOperand:
    values = {
        "snapshot_id": _projection({}, {}).snapshot_id,
        "observation_ref": CrossObservationRef(
            "R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0
        ),
        "normalized_metric": "метрика",
        "normalized_context": "контекст",
        "comparator": ComparatorLabel.LESS_THAN_OR_EQUAL,
        "inclusivity": BoundaryInclusivity.INCLUSIVE,
        "value": Decimal("1"),
        "unit": UnitLabel.SECOND,
    }
    values.update(changes)
    return ComparisonOperand(**values)


@pytest.mark.parametrize(
    ("changes", "reason"),
    [
        ({"normalized_metric": None}, CrossUnresolvedReason.MISSING_METRIC),
        ({"normalized_context": None}, CrossUnresolvedReason.MISSING_CONTEXT),
        ({"unit": None}, CrossUnresolvedReason.MISSING_UNIT),
        ({"value": None}, CrossUnresolvedReason.MISSING_VALUE),
        (
            {"comparator": None, "inclusivity": None},
            CrossUnresolvedReason.MISSING_COMPARATOR,
        ),
    ],
)
def test_evaluator_covers_every_missing_reason(changes, reason) -> None:
    left = _operand(**changes)
    right = replace(_operand(), observation_ref=replace(left.observation_ref, requirement_id="R002"))
    right = replace(right, snapshot_id=left.snapshot_id)

    decision = QbApplicabilityEvaluator().evaluate(ComparisonOperands(left, right))

    assert reason in decision.unresolved_reasons


def test_direct_predicate_uses_exact_high_precision_decimal() -> None:
    projection = _projection({}, {})
    snapshot_id = projection.snapshot_id
    left = replace(
        _operand(
            snapshot_id=snapshot_id,
            comparator=ComparatorLabel.GREATER_THAN_OR_EQUAL,
            value=Decimal("1.0000000000000000000000000001"),
        ),
        observation_ref=CrossObservationRef(
            "R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0
        ),
    )
    right = replace(
        _operand(
            snapshot_id=snapshot_id,
            value=Decimal("1.0000000000000000000000000000"),
        ),
        observation_ref=CrossObservationRef(
            "R002", FeatureId.QUANTITATIVE_CONSTRAINT, 0
        ),
    )
    validator = QbSupportedBoundValidator()

    lower = validator.validate(left)
    upper = validator.validate(right)

    assert lower.direction is SupportedBoundDirection.LOWER
    assert upper.direction is SupportedBoundDirection.UPPER
    assert direct_bound_conflict(lower, upper)


def test_result_preserves_evidence_from_both_owners_and_has_stable_id() -> None:
    projection = _projection({}, {})
    candidate = ExhaustivePairSelector().select(projection)[0]
    assessor = QbObservationPairAssessor()

    first = assessor.assess(candidate, projection)
    second = assessor.assess(candidate, projection)

    assert {item.requirement_id for item in first.evidence_refs} == {"R001", "R002"}
    assert [item.requirement_id for item in first.evidence_refs] == [
        "R001",
        "R001",
        "R001",
        "R002",
        "R002",
        "R002",
    ]
    assert first.result_id == second.result_id


def test_candidate_snapshot_and_provenance_corruption_fail_fast() -> None:
    projection = _projection({}, {})
    candidate = ExhaustivePairSelector().select(projection)[0]
    foreign = _projection({"value": Decimal("3")}, {})

    with pytest.raises(ValueError, match="cross snapshots"):
        QbObservationPairAssessor().assess(candidate, foreign)

    evidence = projection.resolver._evidence[0][1]
    object.__setattr__(evidence, "text", "пошкоджено")
    with pytest.raises(ValueError, match="Evidence|span|provenance"):
        QbObservationPairAssessor().assess(candidate, projection)


def test_snapshot_contract_corruption_fails_fast() -> None:
    projection = _projection({}, {})
    candidate = ExhaustivePairSelector().select(projection)[0]
    changed = replace(
        projection.snapshot.contracts,
        coverage_profile=replace(QB_COVERAGE_PROFILE, version="2"),
    )
    object.__setattr__(projection.snapshot, "contracts", changed)

    with pytest.raises(ValueError, match="coverage|identity"):
        QbObservationPairAssessor().assess(candidate, projection)

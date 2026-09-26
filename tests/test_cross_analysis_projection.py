from dataclasses import FrozenInstanceError, replace
from decimal import Decimal

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import (
    IMP_02_EXTRACTION_CONTRACTS,
    QB_CONTRACT_MANIFEST,
    CrossDiagnosticRef,
    CrossObservationRef,
    CrossRequirementProjector,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorLabel,
    FeatureId,
    QuantitativeComponentName,
    Requirement,
    TextComponent,
    UnitLabel,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor


UPPER_C0 = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
LOWER_C0 = "Час відгуку не нижче 5 с при 500 одночасних користувачах"


def _record(requirement_id: str, source_line: int, text: str):
    result = BaselineFeatureExtractor().extract(
        Requirement(requirement_id, source_line, text)
    )
    return RequirementQualityAssessor().assess_record(result)


def _project(*records):
    return CrossRequirementProjector().project(records)


def test_valid_multi_record_projection_and_resolver_round_trip() -> None:
    records = (
        _record("R001", 1, UPPER_C0),
        _record("R002", 3, LOWER_C0),
    )

    projection = _project(*records)
    first, second = projection.requirements

    assert [item.requirement_id for item in projection.requirements] == ["R001", "R002"]
    assert [item.source_order for item in projection.requirements] == [0, 1]
    assert [item.source_line for item in projection.requirements] == [1, 3]
    assert projection.snapshot.counts.requirement_count == 2
    assert projection.snapshot.counts.observation_count == 2
    assert projection.snapshot.counts.diagnostic_count == 2

    original_result = records[0].extraction_result
    observation_ref = first.observations[0].ref
    evidence_ref = first.observations[0].metric_evidence_refs[0]
    diagnostic_ref = first.diagnostics[0].ref
    assert projection.resolver.resolve_requirement("R001") is original_result.requirement
    assert (
        projection.resolver.resolve_observation(observation_ref)
        is original_result.features.quantitative_constraints.observations[0]
    )
    assert projection.resolver.resolve_evidence(evidence_ref) is original_result.evidence[0]
    assert (
        projection.resolver.resolve_diagnostic(diagnostic_ref)
        is original_result.features.quantitative_constraints.diagnostics[0]
    )
    assert second.observations[0].ref.observation_index == 0


@pytest.mark.parametrize(
    ("text", "expected_count"),
    [
        ("Система працює", 0),
        ("Система працює не більше 2 с", 1),
        ("Система працює не більше 2 с та не нижче 3 с", 2),
    ],
)
def test_zero_one_and_multiple_observations_have_stable_indexes(
    text: str,
    expected_count: int,
) -> None:
    requirement = _project(_record("R001", 1, text)).requirements[0]

    assert len(requirement.observations) == expected_count
    assert tuple(item.ref.observation_index for item in requirement.observations) == tuple(
        range(expected_count)
    )


def test_identical_qb_input_and_contracts_have_stable_snapshot_identity() -> None:
    first = _project(_record("R001", 1, UPPER_C0))
    second = _project(_record("R001", 1, UPPER_C0))

    assert first.snapshot.canonical_bytes() == second.snapshot.canonical_bytes()
    assert first.snapshot_id == second.snapshot_id
    assert first.snapshot.contracts is QB_CONTRACT_MANIFEST


def test_duplicate_requirement_ids_fail_fast() -> None:
    with pytest.raises(ValueError, match="unique requirement IDs"):
        _project(
            _record("R001", 1, "Система працює"),
            _record("R001", 2, "Система відповідає"),
        )


@pytest.mark.parametrize("lines", [(2, 1), (1, 1)])
def test_non_strict_source_order_fails_fast(lines: tuple[int, int]) -> None:
    with pytest.raises(ValueError, match="strict source-line order"):
        _project(
            _record("R001", lines[0], "Система працює"),
            _record("R002", lines[1], "Система відповідає"),
        )


def test_foreign_evidence_fails_fast() -> None:
    record = _record("R001", 1, UPPER_C0)
    evidence = record.extraction_result.evidence[0]
    object.__setattr__(evidence, "requirement_id", "R999")

    with pytest.raises(ValueError, match="foreign requirement"):
        _project(record)


def test_duplicate_evidence_ids_fail_fast() -> None:
    record = _record("R001", 1, UPPER_C0)
    result = record.extraction_result
    object.__setattr__(result, "evidence", result.evidence + (result.evidence[0],))

    with pytest.raises(ValueError, match="duplicate Evidence ID"):
        _project(record)


def test_wrong_evidence_feature_family_fails_fast() -> None:
    record = _record("R001", 1, UPPER_C0)
    evidence = record.extraction_result.evidence[0]
    object.__setattr__(evidence, "feature_id", FeatureId.EXPECTED_RESULT)

    with pytest.raises(ValueError, match="quantitative feature family"):
        _project(record)


def test_dangling_component_evidence_fails_fast() -> None:
    record = _record("R001", 1, "Система працює не більше 2 с")
    observation = record.extraction_result.features.quantitative_constraints.observations[0]
    object.__setattr__(observation, "metric", TextComponent(("MISSING",)))
    object.__setattr__(
        observation,
        "evidence_refs",
        ("MISSING", *observation.evidence_refs),
    )

    with pytest.raises(ValueError, match="dangling Evidence ref"):
        _project(record)


def test_resolver_rejects_evidence_not_used_by_requested_component() -> None:
    projection = _project(_record("R001", 1, UPPER_C0))
    observation = projection.requirements[0].observations[0]
    scalar_ref = observation.value_evidence_refs[0]

    with pytest.raises(ValueError, match="not legitimately used"):
        projection.resolver.resolve_evidence(
            scalar_ref,
            observation_ref=observation.ref,
            component=QuantitativeComponentName.METRIC,
        )


def test_out_of_range_observation_and_invalid_diagnostic_refs_fail() -> None:
    projection = _project(_record("R001", 1, UPPER_C0))

    with pytest.raises(ValueError, match="out of range"):
        projection.resolver.resolve_observation(
            CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 1)
        )
    with pytest.raises(ValueError, match="out of range"):
        projection.resolver.resolve_diagnostic(
            CrossDiagnosticRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 1)
        )


def test_evidence_span_mismatch_fails_fast() -> None:
    record = _record("R001", 1, UPPER_C0)
    evidence = record.extraction_result.evidence[0]
    object.__setattr__(evidence, "text", "Час відповіді")

    with pytest.raises(ValueError, match="Evidence span must round-trip"):
        _project(record)


def test_diagnostic_span_mismatch_fails_fast() -> None:
    record = _record("R001", 1, UPPER_C0)
    diagnostic = record.extraction_result.features.quantitative_constraints.diagnostics[0]
    object.__setattr__(diagnostic.candidate_span, "text", "501")

    with pytest.raises(ValueError, match="diagnostic span must round-trip"):
        _project(record)


def test_resolver_rejects_cross_snapshot_misuse() -> None:
    first = _project(_record("R001", 1, UPPER_C0))
    second = _project(_record("R001", 1, LOWER_C0))
    ref = first.requirements[0].observations[0].ref

    assert first.snapshot_id != second.snapshot_id
    with pytest.raises(ValueError, match="across assessment snapshots"):
        first.resolver.resolve_observation(ref, snapshot_id=second.snapshot_id)


def test_input_records_remain_unchanged_and_projection_is_immutable() -> None:
    records = (
        _record("R001", 1, UPPER_C0),
        _record("R002", 2, LOWER_C0),
    )
    before = repr(records)

    projection = _project(*records)

    assert repr(records) == before
    with pytest.raises(FrozenInstanceError):
        projection.snapshot = projection.snapshot


def test_exact_upper_and_lower_c0_projection() -> None:
    upper, lower = _project(
        _record("R001", 1, UPPER_C0),
        _record("R002", 2, LOWER_C0),
    ).requirements

    upper_observation = upper.observations[0]
    assert upper_observation.comparator is ComparatorLabel.LESS_THAN_OR_EQUAL
    assert upper_observation.inclusivity is BoundaryInclusivity.INCLUSIVE
    assert upper_observation.value == Decimal("2")
    assert upper_observation.unit is UnitLabel.SECOND
    assert [item.rule_id for item in upper.evidence] == [
        "QUANT-METRIC-001",
        "QUANT-001",
        "QUANT-CONTEXT-001",
    ]

    lower_observation = lower.observations[0]
    assert lower_observation.comparator is ComparatorLabel.GREATER_THAN_OR_EQUAL
    assert lower_observation.inclusivity is BoundaryInclusivity.INCLUSIVE
    assert lower_observation.value == Decimal("5")
    assert lower_observation.unit is UnitLabel.SECOND
    assert [item.rule_id for item in lower.evidence] == [
        "QUANT-LB-METRIC-001",
        "QUANT-UK-001",
        "QUANT-LB-CONTEXT-001",
    ]
    assert [(item.code, item.rule_id, item.candidate_text) for item in lower.diagnostics] == [
        ("QUANT_UNRESOLVED_NUMERIC_CANDIDATE", "QUANT-001", "500")
    ]


def test_contract_manifest_contains_only_current_qb_contract_slots() -> None:
    assert [
        (descriptor.contract_id, descriptor.version)
        for descriptor in (
            QB_CONTRACT_MANIFEST.projection,
            QB_CONTRACT_MANIFEST.normalization,
            QB_CONTRACT_MANIFEST.comparison,
            QB_CONTRACT_MANIFEST.materiality,
            QB_CONTRACT_MANIFEST.aggregation,
            QB_CONTRACT_MANIFEST.coverage_profile,
        )
    ] == [
        ("QB-PROJECTION", "1"),
        ("QB-NORMALIZATION", "1"),
        ("QB-COMPARISON", "1"),
        ("QB-MATERIALITY", "1"),
        ("QB-AGGREGATION", "1"),
        ("QB-v0.1", "1"),
    ]


def test_manifest_explicitly_versions_both_imp_02_extraction_contracts() -> None:
    assert QB_CONTRACT_MANIFEST.extraction_contracts == IMP_02_EXTRACTION_CONTRACTS
    assert [
        (descriptor.contract_id, descriptor.version)
        for descriptor in QB_CONTRACT_MANIFEST.extraction_contracts
    ] == [
        ("QUANT-LB-METRIC-001", "1"),
        ("QUANT-LB-CONTEXT-001", "1"),
    ]


def test_extraction_contract_version_affects_identity_without_lower_bridge_evidence() -> None:
    record = _record("R001", 1, "Система працює")
    baseline = CrossRequirementProjector().project((record,))
    changed_dependencies = (
        replace(IMP_02_EXTRACTION_CONTRACTS[0], version="2"),
        IMP_02_EXTRACTION_CONTRACTS[1],
    )
    changed_manifest = replace(
        QB_CONTRACT_MANIFEST,
        extraction_contracts=changed_dependencies,
    )
    changed = CrossRequirementProjector().project((record,), changed_manifest)

    assert baseline.requirements[0].evidence == ()
    assert baseline.snapshot_id != changed.snapshot_id
    assert baseline.snapshot.canonical_bytes() != changed.snapshot.canonical_bytes()


def test_architecture_slots_do_not_allocate_future_production_rule_ids() -> None:
    manifest_ids = {
        descriptor.contract_id
        for descriptor in (
            QB_CONTRACT_MANIFEST.projection,
            QB_CONTRACT_MANIFEST.normalization,
            QB_CONTRACT_MANIFEST.comparison,
            QB_CONTRACT_MANIFEST.materiality,
            QB_CONTRACT_MANIFEST.aggregation,
            QB_CONTRACT_MANIFEST.coverage_profile,
            *QB_CONTRACT_MANIFEST.extraction_contracts,
        )
    }

    assert manifest_ids.isdisjoint(
        {"QB-MATERIALITY-001", "QB-COMPARE-001", "QB-CONSISTENCY-001"}
    )

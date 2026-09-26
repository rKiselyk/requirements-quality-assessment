from dataclasses import replace

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import (
    QB_CONTRACT_MANIFEST,
    QB_MATERIALITY_RULE,
    QB_NON_MATERIAL_CONTEXT_ALLOWLIST,
    ContractVersionDescriptor,
    CrossEvidenceRef,
    CrossRequirementProjector,
    QbMaterialityClassifier,
    QbMaterialityDisposition,
)
from requirements_quality_assessment.domain import (
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DiagnosticSpan,
    QuantitativeComponentName,
    Requirement,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor


UPPER_C0 = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
LOWER_C0 = "Час відгуку не нижче 5 с при 500 одночасних користувачах"


def _record(requirement_id: str, source_line: int, text: str):
    result = BaselineFeatureExtractor().extract(
        Requirement(requirement_id, source_line, text)
    )
    return RequirementQualityAssessor().assess_record(result)


def _project(*records, contracts=QB_CONTRACT_MANIFEST):
    return CrossRequirementProjector().project(records, contracts)


def _classify(*records, contracts=QB_CONTRACT_MANIFEST):
    projection = _project(*records, contracts=contracts)
    return projection, QbMaterialityClassifier().classify(projection)


@pytest.mark.parametrize(
    ("text", "contract_id"),
    [
        (UPPER_C0, "QUANT-CONTEXT-001"),
        (LOWER_C0, "QUANT-LB-CONTEXT-001"),
    ],
)
def test_exact_upper_and_lower_c0_are_qb_non_material(
    text: str,
    contract_id: str,
) -> None:
    projection, result = _classify(_record("R001", 1, text))

    audit = result.audit_records[0]
    assert audit.disposition is QbMaterialityDisposition.QB_NON_MATERIAL
    assert audit.gate_outcomes.all_passed
    assert audit.snapshot_id == projection.snapshot_id
    assert audit.requirement_id == "R001"
    assert audit.diagnostic_code == "QUANT_UNRESOLVED_NUMERIC_CANDIDATE"
    assert audit.diagnostic_rule_id == "QUANT-001"
    assert audit.candidate_text == "500"
    assert audit.matched_context_evidence_ref is not None
    assert audit.matched_allowlist_contract == ContractVersionDescriptor(
        contract_id,
        "1",
    )
    assert audit.materiality_rule == QB_MATERIALITY_RULE
    assert result.global_unresolved_diagnostic_count == 1
    assert result.qb_material_count == 0
    assert result.qb_non_material_count == 1


def test_allowlist_is_closed_to_exactly_two_versioned_context_contracts() -> None:
    assert tuple(
        (item.contract.contract_id, item.contract.version)
        for item in QB_NON_MATERIAL_CONTEXT_ALLOWLIST
    ) == (
        ("QUANT-CONTEXT-001", "1"),
        ("QUANT-LB-CONTEXT-001", "1"),
    )
    assert all(
        item.non_independent_role_guaranteed
        for item in QB_NON_MATERIAL_CONTEXT_ALLOWLIST
    )


def _valid_non_material_audit():
    _, result = _classify(_record("R001", 1, UPPER_C0))
    return result.audit_records[0]


def test_non_material_audit_requires_context_evidence_ref() -> None:
    audit = _valid_non_material_audit()

    with pytest.raises(ValueError, match="requires matched context Evidence"):
        replace(audit, matched_context_evidence_ref=None)


def test_non_material_audit_requires_allowlist_contract() -> None:
    audit = _valid_non_material_audit()

    with pytest.raises(ValueError, match="requires a matched allowlist contract"):
        replace(audit, matched_allowlist_contract=None)


def test_non_material_audit_requires_candidate_span() -> None:
    audit = _valid_non_material_audit()

    with pytest.raises(ValueError, match="requires a diagnostic candidate span"):
        replace(
            audit,
            candidate_text=None,
            diagnostic_start_offset=None,
            diagnostic_end_offset=None,
        )


@pytest.mark.parametrize("material", [False, True])
def test_audit_rejects_foreign_owner_context_evidence_for_any_disposition(
    material: bool,
) -> None:
    audit = _valid_non_material_audit()
    foreign_ref = CrossEvidenceRef(
        requirement_id="R999",
        evidence_id=audit.matched_context_evidence_ref.evidence_id,
    )
    gates = (
        replace(audit.gate_outcomes, provenance_integrity=False)
        if material
        else audit.gate_outcomes
    )
    disposition = (
        QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED
        if material
        else QbMaterialityDisposition.QB_NON_MATERIAL
    )

    with pytest.raises(ValueError, match="must have the audit requirement owner"):
        replace(
            audit,
            matched_context_evidence_ref=foreign_ref,
            gate_outcomes=gates,
            disposition=disposition,
        )


def test_non_material_audit_rejects_any_failed_gate() -> None:
    audit = _valid_non_material_audit()
    failed_gates = replace(
        audit.gate_outcomes,
        provenance_integrity=False,
    )

    with pytest.raises(ValueError, match="must follow all eight gates"):
        replace(audit, gate_outcomes=failed_gates)


def test_material_audit_rejects_all_eight_gates_passed() -> None:
    audit = _valid_non_material_audit()

    with pytest.raises(ValueError, match="must follow all eight gates"):
        replace(
            audit,
            disposition=QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED,
        )


@pytest.mark.parametrize(
    ("attribute", "changed", "gate"),
    [
        ("code", "OTHER_DIAGNOSTIC", "exact_diagnostic_code"),
        ("rule_id", "OTHER-RULE", "exact_diagnostic_rule"),
    ],
)
def test_wrong_diagnostic_identity_fails_closed(
    attribute: str,
    changed: str,
    gate: str,
) -> None:
    record = _record("R001", 1, UPPER_C0)
    diagnostic = record.extraction_result.features.quantitative_constraints.diagnostics[0]
    object.__setattr__(diagnostic, attribute, changed)

    _, result = _classify(record)

    audit = result.audit_records[0]
    assert not getattr(audit.gate_outcomes, gate)
    assert audit.gate_outcomes.no_qb_competition
    assert audit.gate_outcomes.provenance_integrity
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_value_other_than_ascii_500_fails_closed() -> None:
    _, result = _classify(
        _record(
            "R001",
            1,
            "Час відгуку ≤ 2 с при 600 одночасних користувачах",
        )
    )

    audit = result.audit_records[0]
    assert not audit.gate_outcomes.exact_candidate_text
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_candidate_outside_exact_context_evidence_fails_closed() -> None:
    record = _record("R001", 1, UPPER_C0)
    result = record.extraction_result
    extended = f"{UPPER_C0} 500"
    object.__setattr__(result, "requirement", Requirement("R001", 1, extended))
    diagnostic = result.features.quantitative_constraints.diagnostics[0]
    object.__setattr__(
        diagnostic,
        "candidate_span",
        DiagnosticSpan("500", len(extended) - 3, len(extended)),
    )

    _, materiality = _classify(record)

    audit = materiality.audit_records[0]
    assert audit.gate_outcomes.exact_candidate_text
    assert not audit.gate_outcomes.candidate_inside_context
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_context_not_tied_to_the_same_observation_fails_closed() -> None:
    record = _record("R001", 1, UPPER_C0)
    outcome = record.extraction_result.features.quantitative_constraints
    observation = outcome.observations[0]
    context_refs = observation.context.evidence_refs
    object.__setattr__(observation, "context", None)
    object.__setattr__(
        observation,
        "evidence_refs",
        tuple(ref for ref in observation.evidence_refs if ref not in context_refs),
    )

    _, result = _classify(record)

    audit = result.audit_records[0]
    assert audit.gate_outcomes.candidate_inside_context
    assert not audit.gate_outcomes.same_observation
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_wrong_context_evidence_owner_fails_provenance_closed() -> None:
    projection = _project(_record("R001", 1, UPPER_C0))
    context_ref = projection.requirements[0].observations[0].context_evidence_refs[0]
    context = projection.resolver.resolve_evidence(context_ref)
    object.__setattr__(context, "requirement_id", "R999")

    result = QbMaterialityClassifier().classify(projection)

    audit = result.audit_records[0]
    assert not audit.gate_outcomes.provenance_integrity
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_context_contract_outside_allowlist_fails_closed() -> None:
    record = _record("R001", 1, UPPER_C0)
    context = next(
        item
        for item in record.extraction_result.evidence
        if item.rule_id == "QUANT-CONTEXT-001"
    )
    object.__setattr__(context, "rule_id", "QUANT-CONTEXT-999")

    _, result = _classify(record)

    audit = result.audit_records[0]
    assert audit.gate_outcomes.candidate_inside_context
    assert audit.gate_outcomes.same_observation
    assert not audit.gate_outcomes.allowlisted_contract_guarantee
    assert audit.gate_outcomes.provenance_integrity
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_changed_lower_context_contract_version_fails_closed() -> None:
    changed_contracts = replace(
        QB_CONTRACT_MANIFEST,
        extraction_contracts=tuple(
            replace(item, version="2")
            if item.contract_id == "QUANT-LB-CONTEXT-001"
            else item
            for item in QB_CONTRACT_MANIFEST.extraction_contracts
        ),
    )

    _, result = _classify(
        _record("R001", 1, LOWER_C0),
        contracts=changed_contracts,
    )

    audit = result.audit_records[0]
    assert not audit.gate_outcomes.allowlisted_contract_guarantee
    assert audit.gate_outcomes.provenance_integrity
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_extra_unresolved_diagnostic_invalidates_initially_eligible_500() -> None:
    record = _record("R001", 1, UPPER_C0)
    outcome = record.extraction_result.features.quantitative_constraints
    original = outcome.diagnostics[0]
    extra = DetectionDiagnostic(
        code="OTHER_DIAGNOSTIC",
        explanation="Test-only competing unresolved fact.",
        rule_id="QUANT-001",
        candidate_span=original.candidate_span,
    )
    object.__setattr__(outcome, "diagnostics", (original, extra))

    _, result = _classify(record)

    assert [item.disposition for item in result.audit_records] == [
        QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED,
        QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED,
    ]
    assert not result.audit_records[0].gate_outcomes.no_qb_competition
    assert result.global_unresolved_diagnostic_count == 2
    assert result.qb_material_count == 2
    assert result.qb_non_material_count == 0


def test_unresolved_observation_component_invalidates_eligible_500() -> None:
    record = _record("R001", 1, UPPER_C0)
    observation = (
        record.extraction_result.features.quantitative_constraints.observations[0]
    )
    metric_refs = observation.metric.evidence_refs
    object.__setattr__(observation, "metric", None)
    object.__setattr__(
        observation,
        "unresolved_components",
        (QuantitativeComponentName.METRIC,),
    )
    object.__setattr__(
        observation,
        "evidence_refs",
        tuple(ref for ref in observation.evidence_refs if ref not in metric_refs),
    )

    _, result = _classify(record)

    audit = result.audit_records[0]
    assert not audit.gate_outcomes.no_qb_competition
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_unresolved_component_elsewhere_in_snapshot_invalidates_eligible_500() -> None:
    candidate = _record("R001", 1, UPPER_C0)
    other = _record("R002", 2, "Система працює не більше 3 с")
    observation = other.extraction_result.features.quantitative_constraints.observations[0]
    object.__setattr__(
        observation,
        "unresolved_components",
        (QuantitativeComponentName.METRIC,),
    )

    _, result = _classify(candidate, other)

    audit = result.audit_records[0]
    assert audit.gate_outcomes.provenance_integrity
    assert not audit.gate_outcomes.no_qb_competition
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_competing_observation_invalidates_eligible_500() -> None:
    record = _record("R001", 1, UPPER_C0)
    outcome = record.extraction_result.features.quantitative_constraints
    observation = outcome.observations[0]
    context_refs = observation.context.evidence_refs
    competitor = replace(
        observation,
        context=None,
        evidence_refs=tuple(
            ref for ref in observation.evidence_refs if ref not in context_refs
        ),
    )
    object.__setattr__(outcome, "observations", (observation, competitor))

    _, result = _classify(record)

    audit = result.audit_records[0]
    assert audit.gate_outcomes.same_observation
    assert not audit.gate_outcomes.no_qb_competition
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_malformed_dangling_context_provenance_fails_closed() -> None:
    projection = _project(_record("R001", 1, UPPER_C0))
    object.__setattr__(projection.resolver, "_evidence", ())

    result = QbMaterialityClassifier().classify(projection)

    audit = result.audit_records[0]
    assert not audit.gate_outcomes.provenance_integrity
    assert audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED


def test_later_snapshot_diagnostic_turns_earlier_eligible_500_material() -> None:
    first = _record("R001", 1, UPPER_C0)
    second = _record("R002", 2, UPPER_C0)
    later = second.extraction_result.features.quantitative_constraints.diagnostics[0]
    object.__setattr__(later, "code", "OTHER_DIAGNOSTIC")

    _, result = _classify(first, second)

    assert result.audit_records[0].gate_outcomes.exact_diagnostic_code
    assert not result.audit_records[0].gate_outcomes.no_qb_competition
    assert result.audit_records[0].disposition is (
        QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED
    )


def test_counts_order_and_frozen_source_behavior_are_preserved() -> None:
    records = (
        _record("R900", 2, LOWER_C0),
        _record("R100", 7, UPPER_C0),
    )
    before = repr(records)
    projection, result = _classify(*records)

    assert [item.requirement_id for item in result.audit_records] == ["R900", "R100"]
    assert [item.diagnostic_ref.diagnostic_index for item in result.audit_records] == [0, 0]
    assert result.global_unresolved_diagnostic_count == 2
    assert result.qb_material_count == 0
    assert result.qb_non_material_count == 2
    assert result.global_unresolved_diagnostic_count == (
        result.qb_material_count + result.qb_non_material_count
    )
    assert result.global_unresolved_quantitative_extraction_count == 2
    assert result.qb_material_unresolved_quantitative_extraction_count == 0
    assert result.qb_non_material_preserved_diagnostic_count == 2
    assert repr(records) == before
    assert all(
        item.processing_status is DetectionProcessingStatus.INCOMPLETE
        for item in projection.requirements
    )
    assert all(len(item.diagnostics) == 1 for item in projection.requirements)
    assert all(
        record.extraction_result.features.quantitative_constraints.processing_status
        is DetectionProcessingStatus.INCOMPLETE
        for record in records
    )
    assert all(
        len(record.extraction_result.features.quantitative_constraints.diagnostics) == 1
        for record in records
    )

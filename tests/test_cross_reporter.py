"""IMP-10 additive cross-requirement reporting tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from fractions import Fraction
from pathlib import Path

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import (
    CrossResultState,
    QbConsistencyState,
    SpecificationAssessmentService,
)
from requirements_quality_assessment.cross_reporter import (
    AssessmentReportBundle,
    AuditCrossRequirementReporter,
    UserCrossRequirementReporter,
)
from requirements_quality_assessment.domain import Requirement
from requirements_quality_assessment.extractor import BaselineFeatureExtractor
from requirements_quality_assessment.reporter import ConsoleReporter, UserConsoleReporter


UPPER_TWO = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
UPPER_FIVE = "Час відгуку ≤ 5 с при 500 одночасних користувачах"
LOWER_FIVE = "Час відгуку не нижче 5 с при 500 одночасних користувачах"
UPPER_FIVE_MINUTES = "Час відгуку ≤ 5 хв при 500 одночасних користувачах"
UNRESOLVED = "Система працює не більше 3 с"


def _records(*texts: str):
    extractor = BaselineFeatureExtractor()
    assessor = RequirementQualityAssessor()
    return tuple(
        assessor.assess_record(
            extractor.extract(Requirement(f"R{index:03d}", index, text))
        )
        for index, text in enumerate(texts, start=1)
    )


def _result(*texts: str):
    return SpecificationAssessmentService().assess(_records(*texts))


def _all_pair_states_result():
    return _result(
        UPPER_TWO,
        LOWER_FIVE,
        UNRESOLVED,
        UPPER_FIVE_MINUTES,
        UPPER_FIVE,
    )


def test_report_bundle_wraps_one_finished_result_without_copying_science() -> None:
    result = _result(UPPER_TWO, LOWER_FIVE)
    bundle = AssessmentReportBundle.from_result(result)

    assert bundle.assessment_result is result
    assert bundle.records is result.records
    assert bundle.specification_assessment is result.specification_assessment
    assert bundle.cross_results is result.cross_results
    assert bundle.materiality is result.materiality
    assert bundle.resolver is result.resolver
    assert bundle.snapshot_id == result.snapshot_id
    with pytest.raises(FrozenInstanceError):
        bundle.assessment_result = object()
    with pytest.raises(TypeError, match="SpecificationAssessmentResult"):
        AssessmentReportBundle(object())


def test_composed_reports_append_cross_sections_without_changing_local_sections() -> None:
    result = _result(UPPER_TWO, LOWER_FIVE)

    local_audit = ConsoleReporter().render(
        result.records,
        result.specification_assessment.quality_profile,
    )
    local_user = UserConsoleReporter().render(
        result.records,
        result.specification_assessment.quality_profile,
    )
    audit = ConsoleReporter().render_assessment(result)
    user = UserConsoleReporter().render_assessment(result)

    assert audit.startswith(local_audit + "\n\nCross-Requirement Consistency\n")
    assert user.startswith(local_user + "\n\nУзгодженість вимог\n")
    assert audit[: len(local_audit)] == local_audit
    assert user[: len(local_user)] == local_user


def test_audit_renders_aggregate_contracts_operands_and_every_observability_count() -> None:
    result = _all_pair_states_result()
    output = ConsoleReporter().render_assessment(result)
    assessment = result.specification_assessment.qb_consistency

    assert "Cross-Requirement Consistency" in output
    assert "coverage_profile: QB-v0.1 / 1" in output
    assert "aggregation_rule: QB-CONSISTENCY-001 / 1" in output
    assert "non_claim_contract: QB-NON-CLAIMS-001 / 1" in output
    assert "non_claim_keys: NC-QB-BASE" in output
    assert "formula_operands:" in output
    assert "observed_R_conf: R001, R002" in output
    assert "rconf_complete: no" in output
    for field_name in (
        "total_requirement_count",
        "requirements_with_observations_count",
        "requirements_in_applicable_comparisons_count",
        "total_requirement_pair_count",
        "total_observation_pair_count",
        "confirmed_conflict_count",
        "compatible_count",
        "unresolved_count",
        "outside_applicability_count",
        "applicable_comparison_count",
        "global_unresolved_extraction_count",
        "qb_material_unresolved_count",
        "qb_non_material_diagnostic_count",
        "observed_rconf_count",
        "rconf_complete",
    ):
        assert f"  {field_name}:" in output
    assert str(assessment.formula_operands.total_requirement_count) in output


def test_audit_renders_all_pair_states_in_authoritative_order() -> None:
    result = _all_pair_states_result()
    output = AuditCrossRequirementReporter().render(
        AssessmentReportBundle.from_result(result)
    )

    expected_ids = [item.result_id.value for item in result.cross_results]
    positions = [output.index(f"result_id: {item}") for item in expected_ids]
    assert positions == sorted(positions)
    assert {item.state for item in result.cross_results} == set(CrossResultState)
    for state in CrossResultState:
        assert f"state: {state.value}" in output
    assert "comparison_contract: QB-COMPARE-001 / 1" in output
    assert "relation_kind: QUANTITATIVE_BOUND" in output
    assert "unresolved_reasons: MISSING_METRIC, MISSING_CONTEXT" in output
    assert "outside_reasons: UNIT_MISMATCH" in output
    assert "conflict_class: LOGICAL_CONFLICT" in output
    assert "conflict_subtype: DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY" in output


def test_confirmed_conflict_resolves_exact_two_owner_evidence_in_source_order() -> None:
    result = _result(UPPER_TWO, LOWER_FIVE)
    conflict = result.cross_results[0]
    output = AuditCrossRequirementReporter().render(
        AssessmentReportBundle.from_result(result)
    )

    assert conflict.state is CrossResultState.CONFIRMED_CONFLICT
    owner_positions = []
    for ref in conflict.evidence_refs:
        evidence = result.resolver.resolve_evidence(ref, snapshot_id=result.snapshot_id)
        rendered = (
            f"owner_requirement: {ref.requirement_id}\n"
            f"        evidence_id: {evidence.evidence_id}\n"
            f"        text: {evidence.text}\n"
            f"        range: [{evidence.start_offset},{evidence.end_offset})"
        )
        assert rendered in output
        owner_positions.append(output.index(f"ref: {ref.requirement_id}:{ref.evidence_id}"))
    assert {item.requirement_id for item in conflict.evidence_refs} == {"R001", "R002"}
    assert owner_positions == sorted(owner_positions)


def test_user_renders_all_four_pair_states_with_bounded_meanings() -> None:
    output = UserCrossRequirementReporter().render(
        AssessmentReportBundle.from_result(_all_pair_states_result())
    )

    for state in CrossResultState:
        assert f"[{state.value}]" in output
    assert "несумісні в межах правила QB-v0.1" in output
    assert "спільно здійсненні лише в межах цього правила QB-v0.1" in output
    assert "пару не вдалося однозначно оцінити за QB-v0.1" in output
    assert "пара перебуває поза межами чинного правила QB-v0.1" in output
    assert "одиниці вимірювання не збігаються" in output
    assert "Структуровані значення:" in output
    assert "R001: «" in output
    assert "R002: «" in output


@pytest.mark.parametrize(
    ("texts", "state", "expected"),
    [
        ((UPPER_TWO, UPPER_FIVE), QbConsistencyState.COMPUTED, "1"),
        ((UPPER_TWO, UNRESOLVED), QbConsistencyState.UNKNOWN, "UNKNOWN"),
        ((UPPER_TWO,), QbConsistencyState.NOT_APPLICABLE, "NOT_APPLICABLE"),
    ],
)
def test_user_renders_all_three_aggregate_states(texts, state, expected) -> None:
    result = _result(*texts)
    output = UserCrossRequirementReporter().render(
        AssessmentReportBundle.from_result(result)
    )

    assert result.specification_assessment.qb_consistency.state is state
    assert f"Стан: {state.value}" in output
    assert f"Узгодженість у межах QB-v0.1: {expected}" in output


def test_computed_one_and_not_applicable_are_visibly_distinct() -> None:
    computed = _result(UPPER_TWO, UPPER_FIVE)
    not_applicable = _result(UPPER_TWO)
    computed_output = UserConsoleReporter().render_assessment(computed)
    not_applicable_output = UserConsoleReporter().render_assessment(not_applicable)

    assert computed.specification_assessment.qb_consistency.value == Fraction(1, 1)
    assert "Стан: COMPUTED" in computed_output
    assert "Узгодженість у межах QB-v0.1: 1" in computed_output
    assert "не означає універсальної узгодженості" in computed_output
    assert "Стан: NOT_APPLICABLE" in not_applicable_output
    assert "Узгодженість у межах QB-v0.1: NOT_APPLICABLE" in not_applicable_output
    assert "менше двох вимог" in not_applicable_output
    assert computed_output != not_applicable_output


def test_computed_fraction_is_rendered_exactly_without_decimal_or_percentage() -> None:
    result = _result(UPPER_TWO, LOWER_FIVE, UPPER_FIVE)
    assessment = result.specification_assessment.qb_consistency
    audit = ConsoleReporter().render_assessment(result)
    user = UserConsoleReporter().render_assessment(result)

    assert assessment.state is QbConsistencyState.COMPUTED
    assert assessment.value == Fraction(1, 3)
    assert "value: 1/3" in audit
    assert "Узгодженість у межах QB-v0.1: 1/3" in user
    cross_section = user.partition("Узгодженість вимог")[2]
    assert "0.333" not in cross_section
    assert "%" not in cross_section


def test_not_applicable_explains_no_applicable_comparisons() -> None:
    result = _result(
        "Система має обробляти запити.",
        "Система має журналювати події.",
    )
    output = UserConsoleReporter().render_assessment(result)

    assert "Стан: NOT_APPLICABLE" in output
    assert "немає порівнянь, застосовних у межах QB-v0.1" in output


def test_unknown_has_no_numeric_value_and_keeps_partial_rconf() -> None:
    result = _result(UPPER_TWO, LOWER_FIVE, UNRESOLVED)
    assessment = result.specification_assessment.qb_consistency
    output = UserConsoleReporter().render_assessment(result)

    assert assessment.state is QbConsistencyState.UNKNOWN
    assert assessment.value is None
    assert assessment.rconf_participant_ids == ("R001", "R002")
    assert "Узгодженість у межах QB-v0.1: UNKNOWN" in output
    assert "Підтверджені учасники конфліктів: R001, R002" in output
    assert "R_conf complete: no" in output
    assert "Числове значення не обчислено" in output
    cross_section = output.partition("Узгодженість вимог")[2]
    assert "Узгодженість у межах QB-v0.1: 1/" not in cross_section
    assert "Узгодженість у межах QB-v0.1: 0" not in cross_section


def test_material_and_non_material_diagnostics_remain_visible_in_audit() -> None:
    non_material = _result(UPPER_TWO, LOWER_FIVE)
    material = _result(
        "Час відгуку ≤ 2 с при 600 одночасних користувачах",
        UPPER_FIVE,
    )
    non_material_output = ConsoleReporter().render_assessment(non_material)
    material_output = ConsoleReporter().render_assessment(material)

    assert "qb_non_material_count: 2" in non_material_output
    assert "disposition: QB_NON_MATERIAL" in non_material_output
    assert "quantitative_extraction_status:\n  - R001: INCOMPLETE" in non_material_output
    assert "matched_context_evidence_ref:" in non_material_output
    assert "matched_allowlist_contract:" in non_material_output
    assert "qb_material_count: 2" in material_output
    assert "disposition: QB_MATERIAL_UNRESOLVED" in material_output
    for gate in (
        "exact_diagnostic_code",
        "exact_diagnostic_rule",
        "exact_candidate_text",
        "candidate_inside_context",
        "same_observation",
        "allowlisted_contract_guarantee",
        "no_qb_competition",
        "provenance_integrity",
    ):
        assert f"{gate}:" in material_output


def test_bounded_non_claims_are_report_level_and_apply_to_computed_one() -> None:
    result = _result(UPPER_TWO, UPPER_FIVE)
    audit = ConsoleReporter().render_assessment(result)
    user = UserConsoleReporter().render_assessment(result)

    assert "non_claim_contract: QB-NON-CLAIMS-001 / 1" in audit
    assert "non_claim_keys: NC-QB-BASE" in audit
    assert "QB-v0.1 does not establish:" in audit
    assert "product quality" in audit
    assert "defect probability" in audit
    assert audit.count("Bounded non-claims:") == 1
    assert "Межі QB-v0.1:" in user
    assert "не визначає якість програмного продукту" in user
    assert "загальну скалярну оцінку специфікації" in user


def test_cross_reporter_has_no_scientific_component_or_fraction_dependency() -> None:
    source = (
        Path(__file__).parents[1]
        / "src"
        / "requirements_quality_assessment"
        / "cross_reporter.py"
    ).read_text(encoding="utf-8")

    for forbidden in (
        "QbObservationPairAssessor",
        "QbConsistencyAggregator",
        "QbConflictSetBuilder",
        "QbMaterialityClassifier",
        "ExhaustivePairSelector",
        "BaselineFeatureExtractor",
        "RequirementQualityAssessor",
        "SpecificationQualityAggregator",
        "from fractions import Fraction",
        ".exact_value(",
    ):
        assert forbidden not in source

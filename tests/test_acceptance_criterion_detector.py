"""Approved ACCEPT-QUANT-001 first-production composition behavior."""

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import subprocess
import sys

import pytest

from requirements_quality_assessment.detectors import (
    AcceptanceCriterionBaselineDetector,
    ExpectedResultBaselineDetector,
    QuantitativeBaselineDetector,
)
from requirements_quality_assessment.detectors.acceptance_criterion import (
    DEPENDENCY_BLOCKED_CODE,
    RULE_ID,
    UNRESOLVED_CANDIDATE_CODE,
)
from requirements_quality_assessment.detectors.expected_result import (
    PARSER_BLOCKED_CODE as RESULT_PARSER_BLOCKED_CODE,
    RULE_ID as RESULT_RULE_ID,
    UNRESOLVED_CANDIDATE_CODE as RESULT_UNRESOLVED_CANDIDATE_CODE,
)
from requirements_quality_assessment.detectors.quantitative import (
    QUANT_RULE_ID,
    QUANT_UK_RULE_ID,
    UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorComponent,
    ComparatorLabel,
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DetectionStatus,
    DiagnosticSpan,
    Evidence,
    FeatureDetectionOutcome,
    FeatureId,
    FeatureObservation,
    NumericValueComponent,
    QuantitativeConstraintObservation,
    Requirement,
    UnitComponent,
    UnitLabel,
)


@dataclass
class _FakeDetector:
    result: tuple[FeatureDetectionOutcome, tuple[Evidence, ...]]
    calls: int = 0

    def detect(self, requirement: Requirement):
        self.calls += 1
        return self.result


def _source(
    requirement: Requirement,
    evidence_id: str,
    feature_id: FeatureId,
    start: int,
    end: int,
    rule_id: str,
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        requirement_id=requirement.id,
        feature_id=feature_id,
        text=requirement.text[start:end],
        start_offset=start,
        end_offset=end,
        rule_id=rule_id,
    )


def _result_source(
    requirement: Requirement,
    start: int,
    end: int,
    ordinal: int = 1,
    *,
    rule_id: str = RESULT_RULE_ID,
) -> Evidence:
    return _source(
        requirement,
        f"{rule_id}:E{ordinal:03d}",
        FeatureId.EXPECTED_RESULT,
        start,
        end,
        rule_id,
    )


def _quant_source(
    requirement: Requirement,
    start: int,
    end: int,
    ordinal: int = 1,
    *,
    rule_id: str = QUANT_UK_RULE_ID,
) -> Evidence:
    return _source(
        requirement,
        f"{rule_id}:E{ordinal:03d}",
        FeatureId.QUANTITATIVE_CONSTRAINT,
        start,
        end,
        rule_id,
    )


def _expected_result(
    evidence: tuple[Evidence, ...] = (),
    diagnostics: tuple[DetectionDiagnostic, ...] = (),
):
    observations = tuple(
        FeatureObservation(
            feature_id=FeatureId.EXPECTED_RESULT,
            evidence_refs=(source.evidence_id,),
        )
        for source in evidence
    )
    return (
        FeatureDetectionOutcome(
            feature_id=FeatureId.EXPECTED_RESULT,
            observations=observations,
            processing_status=(
                DetectionProcessingStatus.INCOMPLETE
                if diagnostics
                else DetectionProcessingStatus.COMPLETE
            ),
            diagnostics=diagnostics,
        ),
        evidence,
    )


def _quant_observation(
    evidence_refs: tuple[str, ...],
    *,
    comparator: ComparatorLabel | None = ComparatorLabel.LESS_THAN_OR_EQUAL,
    inclusivity: BoundaryInclusivity | None = BoundaryInclusivity.INCLUSIVE,
    unit: UnitLabel | None = UnitLabel.SECOND,
) -> QuantitativeConstraintObservation:
    comparator_component = (
        None
        if comparator is None
        else ComparatorComponent(comparator, inclusivity, evidence_refs)
    )
    unit_component = (
        None if unit is None else UnitComponent(unit, evidence_refs)
    )
    return QuantitativeConstraintObservation(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        metric=None,
        comparator=comparator_component,
        value=NumericValueComponent(Decimal("2"), evidence_refs),
        unit=unit_component,
        context=None,
        unresolved_components=(),
        evidence_refs=evidence_refs,
    )


def _quantitative_result(
    evidence: tuple[Evidence, ...] = (),
    observations: tuple[QuantitativeConstraintObservation, ...] | None = None,
    diagnostics: tuple[DetectionDiagnostic, ...] = (),
):
    if observations is None:
        observations = tuple(
            _quant_observation((source.evidence_id,)) for source in evidence
        )
    return (
        FeatureDetectionOutcome(
            feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
            observations=observations,
            processing_status=(
                DetectionProcessingStatus.INCOMPLETE
                if diagnostics
                else DetectionProcessingStatus.COMPLETE
            ),
            diagnostics=diagnostics,
        ),
        evidence,
    )


def _span(requirement: Requirement, start: int, end: int) -> DiagnosticSpan:
    return DiagnosticSpan(requirement.text[start:end], start, end)


def _upstream_diagnostic(
    code: str,
    rule_id: str,
    span: DiagnosticSpan | None,
) -> DetectionDiagnostic:
    return DetectionDiagnostic(code, "upstream detail", rule_id, span)


def _scan(
    requirement: Requirement,
    expected_result,
    quantitative_result,
):
    expected = _FakeDetector(expected_result)
    quantitative = _FakeDetector(quantitative_result)
    expected_before = expected.result
    quantitative_before = quantitative.result
    outcome, evidence = AcceptanceCriterionBaselineDetector(
        expected_result_detector=expected,
        quantitative_detector=quantitative,
    ).detect(requirement)

    assert expected.calls == quantitative.calls == 1
    assert expected.result == expected_before
    assert quantitative.result == quantitative_before
    assert outcome.feature_id is FeatureId.ACCEPTANCE_CRITERION
    assert len(outcome.observations) == len(evidence)
    for observation, source in zip(outcome.observations, evidence):
        assert observation == FeatureObservation(
            FeatureId.ACCEPTANCE_CRITERION, (source.evidence_id,)
        )
        assert source.requirement_id == requirement.id
        assert source.feature_id is FeatureId.ACCEPTANCE_CRITERION
        assert source.rule_id == RULE_ID
        assert requirement.text[source.start_offset:source.end_offset] == source.text
    for diagnostic in outcome.diagnostics:
        assert diagnostic.rule_id == RULE_ID
        if diagnostic.candidate_span is not None:
            span = diagnostic.candidate_span
            assert requirement.text[span.start_offset:span.end_offset] == span.text
    return outcome, evidence


def _single_composition(
    text: str,
    quant_text: str,
    *,
    comparator: ComparatorLabel | None = ComparatorLabel.LESS_THAN_OR_EQUAL,
    inclusivity: BoundaryInclusivity | None = BoundaryInclusivity.INCLUSIVE,
    unit: UnitLabel | None = UnitLabel.SECOND,
):
    requirement = Requirement("R045", 11, text)
    result_end = len(text.removesuffix("."))
    result = _result_source(requirement, 0, result_end)
    start = text.index(quant_text)
    quant = _quant_source(requirement, start, start + len(quant_text))
    observation = _quant_observation(
        (quant.evidence_id,),
        comparator=comparator,
        inclusivity=inclusivity,
        unit=unit,
    )
    return requirement, _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((quant,), (observation,)),
    )


def test_constructor_defaults_and_public_export():
    detector = AcceptanceCriterionBaselineDetector()
    assert isinstance(
        detector._expected_result_detector, ExpectedResultBaselineDetector
    )
    assert isinstance(detector._quantitative_detector, QuantitativeBaselineDetector)


@pytest.mark.parametrize(
    "comparator",
    [
        ComparatorLabel.LESS_THAN_OR_EQUAL,
        ComparatorLabel.GREATER_THAN_OR_EQUAL,
    ],
)
def test_resolved_inclusive_comparators_are_judgeable(comparator):
    text = "Система повинна відповісти не більше ніж за 2 с."
    _, (outcome, evidence) = _single_composition(
        text,
        "не більше ніж за 2 с",
        comparator=comparator,
    )
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert [source.text for source in evidence] == [text[:-1]]


def test_exact_value_and_unit_without_comparator_is_judgeable():
    text = "Система повинна завершити операцію за 2 с."
    _, (outcome, evidence) = _single_composition(
        text,
        "2 с",
        comparator=None,
        inclusivity=None,
    )
    assert outcome.status is DetectionStatus.DETECTED
    assert [source.text for source in evidence] == [text[:-1]]


def test_no_other_comparator_is_judgeable():
    text = "Система повинна повторювати дію не рідше 2."
    _, (outcome, evidence) = _single_composition(
        text,
        "2",
        comparator=ComparatorLabel.NOT_LESS_FREQUENT,
        inclusivity=None,
        unit=None,
    )
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.code for item in outcome.diagnostics] == [
        UNRESOLVED_CANDIDATE_CODE
    ]


def test_upper_bound_unresolved_preserves_do_candidate_span():
    text = "Система повинна відповісти до 2 с."
    requirement, (outcome, evidence) = _single_composition(
        text,
        "до 2 с",
        comparator=ComparatorLabel.UPPER_BOUND,
        inclusivity=BoundaryInclusivity.UNRESOLVED,
    )
    assert evidence == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    diagnostic = outcome.diagnostics[0]
    assert diagnostic.code == UNRESOLVED_CANDIDATE_CODE
    assert diagnostic.candidate_span == _span(
        requirement, text.index("до 2 с"), text.index("до 2 с") + len("до 2 с")
    )


def test_non_judgeable_multi_evidence_uses_minimal_complete_cover():
    text = "Система повинна відповісти до 2 с."
    requirement = Requirement("R045", 11, text)
    result = _result_source(requirement, 0, len(text) - 1)
    first = _quant_source(requirement, text.index("до"), text.index("до") + 2)
    second = _quant_source(
        requirement,
        text.index("2 с"),
        text.index("2 с") + len("2 с"),
        2,
    )
    observation = _quant_observation(
        (first.evidence_id, second.evidence_id),
        comparator=ComparatorLabel.UPPER_BOUND,
        inclusivity=BoundaryInclusivity.UNRESOLVED,
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((first, second), (observation,)),
    )
    assert evidence == ()
    assert outcome.diagnostics[0].candidate_span.text == "до 2 с"


def test_multiple_quantitative_anchors_create_one_clause_level_criterion():
    text = (
        "новий маршрут для 95 % запитів має бути сформований "
        "не більше ніж за 4 с"
    )
    requirement = Requirement("R045", 11, text)
    result = _result_source(requirement, 0, len(text))
    percent_start = text.index("95 %")
    duration_start = text.index("не більше")
    percent = _quant_source(
        requirement,
        percent_start,
        percent_start + len("95 %"),
        rule_id=QUANT_RULE_ID,
    )
    duration = _quant_source(
        requirement,
        duration_start,
        len(text),
        1,
        rule_id=QUANT_UK_RULE_ID,
    )
    observations = (
        _quant_observation(
            (percent.evidence_id,), comparator=None, inclusivity=None,
            unit=UnitLabel.PERCENT,
        ),
        _quant_observation((duration.evidence_id,)),
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((percent, duration), observations),
    )
    assert outcome.status is DetectionStatus.DETECTED
    assert len(outcome.observations) == len(evidence) == 1
    assert evidence[0].text == text


def test_two_result_clauses_are_source_ordered_with_independent_ids():
    text = "Система повинна діяти за 2 с; сервіс має відповісти за 2 с."
    requirement = Requirement("R045", 11, text)
    second_start = text.index("сервіс")
    results = (
        _result_source(requirement, second_start, len(text) - 1, 2),
        _result_source(requirement, 0, text.index(";"), 1),
    )
    first_quant_start = text.index("2 с")
    second_quant_start = text.index("2 с", first_quant_start + 1)
    quantities = (
        _quant_source(
            requirement, second_quant_start, second_quant_start + 3, 2,
            rule_id=QUANT_RULE_ID,
        ),
        _quant_source(
            requirement, first_quant_start, first_quant_start + 3, 1,
            rule_id=QUANT_RULE_ID,
        ),
    )
    observations = tuple(
        _quant_observation(
            (source.evidence_id,), comparator=None, inclusivity=None
        )
        for source in quantities
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result(results),
        _quantitative_result(quantities, observations),
    )
    assert outcome.status is DetectionStatus.DETECTED
    assert [source.start_offset for source in evidence] == [0, second_start]
    assert [source.evidence_id for source in evidence] == [
        "ACCEPT-QUANT-001:E001",
        "ACCEPT-QUANT-001:E002",
    ]
    assert {source.evidence_id for source in evidence}.isdisjoint(
        {source.evidence_id for source in (*results, *quantities)}
    )


def test_condition_only_quantity_outside_result_is_excluded():
    text = (
        "Система повинна відповісти не більше ніж за 2 с "
        "при 500 одночасних користувачах."
    )
    requirement = Requirement("R045", 11, text)
    condition_start = text.index("при 500")
    result = _result_source(requirement, 0, condition_start - 1)
    bound_start = text.index("не більше")
    bound = _quant_source(requirement, bound_start, text.index(" при"))
    condition = _quant_source(
        requirement,
        text.index("500"),
        text.index("500") + 3,
        1,
        rule_id=QUANT_RULE_ID,
    )
    observations = (
        _quant_observation((bound.evidence_id,)),
        _quant_observation((condition.evidence_id,), unit=None),
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((bound, condition), observations),
    )
    assert outcome.status is DetectionStatus.DETECTED
    assert [source.text for source in evidence] == [result.text]
    assert outcome.diagnostics == ()


def test_load_context_upper_bound_outside_result_is_not_a_criterion():
    text = (
        "Система повинна залишатися доступною при навантаженні "
        "до 300 одночасних запитів."
    )
    requirement = Requirement("R045", 11, text)
    result_end = text.index(" при")
    result = _result_source(requirement, 0, result_end)
    quant_start = text.index("до 300")
    quant = _quant_source(requirement, quant_start, quant_start + len("до 300"))
    observation = _quant_observation(
        (quant.evidence_id,),
        comparator=ComparatorLabel.UPPER_BOUND,
        inclusivity=BoundaryInclusivity.UNRESOLVED,
        unit=None,
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((quant,), (observation,)),
    )
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.diagnostics == evidence == ()


@pytest.mark.parametrize("technical", ["TLS 1.3", "OAuth 2.0"])
def test_technical_versions_do_not_become_acceptance_targets(technical):
    text = f"Система повинна використовувати {technical}."
    requirement = Requirement("R045", 11, text)
    result = _result_source(requirement, 0, len(text) - 1)
    quantitative = QuantitativeBaselineDetector().detect(requirement)
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        quantitative,
    )
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.diagnostics == evidence == ()


def test_quantitative_fragment_without_result_does_not_create_acceptance():
    requirement = Requirement("R045", 11, "Профіль 95 %.")
    quantitative = QuantitativeBaselineDetector().detect(requirement)
    outcome, evidence = _scan(
        requirement,
        _expected_result(),
        quantitative,
    )
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.diagnostics == evidence == ()


def test_result_without_quantitative_candidate_is_complete_not_detected():
    requirement = Requirement("R045", 11, "Система повинна сформувати звіт.")
    result = _result_source(requirement, 0, len(requirement.text) - 1)
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result(),
    )
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.diagnostics == evidence == ()


def test_only_result_uk_001_evidence_can_govern_acceptance():
    requirement = Requirement("R045", 11, "Система повинна діяти за 2 с.")
    result = _result_source(
        requirement, 0, len(requirement.text) - 1, rule_id="RESULT-OTHER-001"
    )
    start = requirement.text.index("2 с")
    quant = _quant_source(
        requirement, start, start + 3, rule_id=QUANT_RULE_ID
    )
    observation = _quant_observation(
        (quant.evidence_id,), comparator=None, inclusivity=None
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((quant,), (observation,)),
    )
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert evidence == ()


def test_complete_quantitative_evidence_must_use_only_approved_rules():
    requirement = Requirement("R045", 11, "Система повинна діяти за 2 с.")
    result = _result_source(requirement, 0, len(requirement.text) - 1)
    start = requirement.text.index("2 с")
    quant = _quant_source(
        requirement, start, start + 3, rule_id="QUANT-OTHER-001"
    )
    observation = _quant_observation(
        (quant.evidence_id,), comparator=None, inclusivity=None
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((quant,), (observation,)),
    )
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert evidence == ()


def test_all_quantitative_evidence_must_fit_inside_one_result_span():
    text = "Система повинна діяти за 2 с; контекст 95 %."
    requirement = Requirement("R045", 11, text)
    result = _result_source(requirement, 0, text.index(";"))
    first_start = text.index("2 с")
    second_start = text.index("95 %")
    first = _quant_source(
        requirement, first_start, first_start + 3, rule_id=QUANT_RULE_ID
    )
    second = _quant_source(
        requirement, second_start, second_start + 4, 2, rule_id=QUANT_RULE_ID
    )
    observation = _quant_observation(
        (first.evidence_id, second.evidence_id),
        comparator=None,
        inclusivity=None,
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((first, second), (observation,)),
    )
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.diagnostics == evidence == ()


def test_unresolved_quantitative_diagnostic_inside_result_preserves_exact_span():
    text = "Система повинна використати профіль 95."
    requirement = Requirement("R045", 11, text)
    result = _result_source(requirement, 0, len(text) - 1)
    start = text.index("95")
    diagnostic = _upstream_diagnostic(
        UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
        QUANT_RULE_ID,
        _span(requirement, start, start + 2),
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result(diagnostics=(diagnostic,)),
    )
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].candidate_span == diagnostic.candidate_span


def test_accepted_criterion_and_unresolved_numeric_candidate_form_mixed_state():
    text = "Система повинна діяти за 2 с з профілем 95."
    requirement = Requirement("R045", 11, text)
    result = _result_source(requirement, 0, len(text) - 1)
    quant_start = text.index("2 с")
    quant = _quant_source(
        requirement, quant_start, quant_start + 3, rule_id=QUANT_RULE_ID
    )
    observation = _quant_observation(
        (quant.evidence_id,), comparator=None, inclusivity=None
    )
    unresolved_start = text.index("95")
    diagnostic = _upstream_diagnostic(
        UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
        QUANT_RULE_ID,
        _span(requirement, unresolved_start, unresolved_start + 2),
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((quant,), (observation,), (diagnostic,)),
    )
    assert len(evidence) == 1
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics[0].candidate_span.text == "95"


def test_unresolved_result_overlapping_accepted_quantitative_uses_result_span():
    text = "Система контролює профіль 95 %."
    requirement = Requirement("R045", 11, text)
    result_span = _span(requirement, 0, len(text) - 1)
    expected_diagnostic = _upstream_diagnostic(
        RESULT_UNRESOLVED_CANDIDATE_CODE,
        RESULT_RULE_ID,
        result_span,
    )
    start = text.index("95 %")
    quant = _quant_source(
        requirement, start, start + 4, rule_id=QUANT_RULE_ID
    )
    observation = _quant_observation(
        (quant.evidence_id,), comparator=None, inclusivity=None,
        unit=UnitLabel.PERCENT,
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result(diagnostics=(expected_diagnostic,)),
        _quantitative_result((quant,), (observation,)),
    )
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].candidate_span == result_span


def test_unresolved_result_overlapping_unresolved_quantitative_uses_result_span():
    text = "Система контролює профіль 95."
    requirement = Requirement("R045", 11, text)
    result_span = _span(requirement, 0, len(text) - 1)
    expected_diagnostic = _upstream_diagnostic(
        RESULT_UNRESOLVED_CANDIDATE_CODE, RESULT_RULE_ID, result_span
    )
    start = text.index("95")
    quant_diagnostic = _upstream_diagnostic(
        UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
        QUANT_RULE_ID,
        _span(requirement, start, start + 2),
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result(diagnostics=(expected_diagnostic,)),
        _quantitative_result(diagnostics=(quant_diagnostic,)),
    )
    assert evidence == ()
    assert outcome.diagnostics[0].candidate_span == result_span


def test_unresolved_result_without_quantitative_overlap_is_not_translated():
    requirement = Requirement("R045", 11, "Система контролює стан.")
    diagnostic = _upstream_diagnostic(
        RESULT_UNRESOLVED_CANDIDATE_CODE,
        RESULT_RULE_ID,
        _span(requirement, 0, len(requirement.text) - 1),
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result(diagnostics=(diagnostic,)),
        _quantitative_result(),
    )
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.diagnostics == evidence == ()


def test_result_parser_blocked_returns_exact_dependency_diagnostic():
    requirement = Requirement("R045", 11, "Система повинна діяти за 2 с.")
    blocked = _upstream_diagnostic(
        RESULT_PARSER_BLOCKED_CODE, RESULT_RULE_ID, None
    )
    start = requirement.text.index("2 с")
    quant = _quant_source(
        requirement, start, start + 3, rule_id=QUANT_RULE_ID
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result(diagnostics=(blocked,)),
        _quantitative_result((quant,)),
    )
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert len(outcome.diagnostics) == 1
    diagnostic = outcome.diagnostics[0]
    assert diagnostic.code == DEPENDENCY_BLOCKED_CODE
    assert diagnostic.candidate_span is None
    assert "upstream detail" not in diagnostic.explanation


def test_repeated_identical_clauses_at_distinct_offsets_remain_distinct():
    clause = "Система повинна діяти за 2 с"
    text = f"{clause}; {clause}."
    requirement = Requirement("R045", 11, text)
    second_start = text.index(clause, 1)
    results = (
        _result_source(requirement, 0, len(clause), 1),
        _result_source(requirement, second_start, second_start + len(clause), 2),
    )
    first_quant = text.index("2 с")
    second_quant = text.index("2 с", first_quant + 1)
    quantities = (
        _quant_source(
            requirement, first_quant, first_quant + 3, 1,
            rule_id=QUANT_RULE_ID,
        ),
        _quant_source(
            requirement, second_quant, second_quant + 3, 2,
            rule_id=QUANT_RULE_ID,
        ),
    )
    observations = tuple(
        _quant_observation(
            (source.evidence_id,), comparator=None, inclusivity=None
        )
        for source in quantities
    )
    _, evidence = _scan(
        requirement,
        _expected_result(results),
        _quantitative_result(quantities, observations),
    )
    assert [source.text for source in evidence] == [clause, clause]
    assert [source.start_offset for source in evidence] == [0, second_start]


def test_diagnostics_are_source_ordered_and_duplicate_paths_are_collapsed():
    text = "Система повинна мати 95 та діяти до 2 с."
    requirement = Requirement("R045", 11, text)
    result = _result_source(requirement, 0, len(text) - 1)
    upper_start = text.index("до 2 с")
    upper = _quant_source(requirement, upper_start, upper_start + len("до 2 с"))
    observation = _quant_observation(
        (upper.evidence_id,),
        comparator=ComparatorLabel.UPPER_BOUND,
        inclusivity=BoundaryInclusivity.UNRESOLVED,
    )
    number_start = text.index("95")
    duplicate_span = _span(requirement, number_start, number_start + 2)
    diagnostics = (
        _upstream_diagnostic(
            UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE, QUANT_RULE_ID, duplicate_span
        ),
        _upstream_diagnostic(
            UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE, QUANT_RULE_ID, duplicate_span
        ),
    )
    outcome, evidence = _scan(
        requirement,
        _expected_result((result,)),
        _quantitative_result((upper,), (observation,), diagnostics),
    )
    assert evidence == ()
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "95",
        "до 2 с",
    ]


def test_default_detectors_integrate_for_binding_cases():
    project_root = Path(__file__).parents[1]
    source_root = project_root / "src"
    script = f"""
import sys
sys.path.insert(0, {str(source_root)!r})
from requirements_quality_assessment.detectors import (
    AcceptanceCriterionBaselineDetector,
)
from requirements_quality_assessment.detectors.acceptance_criterion import (
    DEPENDENCY_BLOCKED_CODE,
    UNRESOLVED_CANDIDATE_CODE,
)
from requirements_quality_assessment.domain import DetectionStatus, Requirement

cases = (
    (
        "Система повинна відповісти не більше ніж за 2 с.",
        DetectionStatus.DETECTED,
        "Система повинна відповісти не більше ніж за 2 с",
    ),
    (
        "Система повинна завершити операцію за 2 с.",
        DetectionStatus.DETECTED,
        "Система повинна завершити операцію за 2 с",
    ),
    (
        "Система повинна відповісти до 2 с.",
        DetectionStatus.UNRESOLVED,
        None,
    ),
)
detector = AcceptanceCriterionBaselineDetector()
observed = []
for text, status, expected_text in cases:
    outcome, evidence = detector.detect(Requirement("R045", 11, text))
    if outcome.diagnostics and outcome.diagnostics[0].code == DEPENDENCY_BLOCKED_CODE:
        raise SystemExit(5)
    observed.append((outcome, evidence))
    assert outcome.status is status
    assert [source.text for source in evidence] == (
        [] if expected_text is None else [expected_text]
    )
assert observed[2][0].diagnostics[0].code == UNRESOLVED_CANDIDATE_CODE
"""
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-c", script],
        cwd=project_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode == 5:
        pytest.skip("optional pinned parser is unavailable")
    assert result.returncode == 0, result.stderr

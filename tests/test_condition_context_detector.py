"""Approved COND-UK-001 first-production behavior."""

import unicodedata

import pytest

from requirements_quality_assessment.detectors import (
    ConditionContextBaselineDetector,
    QuantitativeBaselineDetector,
)
from requirements_quality_assessment.detectors.condition_context import (
    RULE_ID,
    UNRESOLVED_CANDIDATE_CODE,
)
from requirements_quality_assessment.domain import (
    DetectionProcessingStatus,
    DetectionStatus,
    FeatureId,
    FeatureObservation,
    Requirement,
)


def scan(text: str):
    requirement = Requirement("R011", 7, text)
    outcome, evidence = ConditionContextBaselineDetector().detect(requirement)

    assert outcome.feature_id is FeatureId.CONDITION_CONTEXT
    assert all(isinstance(item, FeatureObservation) for item in outcome.observations)
    assert len(outcome.observations) == len(evidence)
    assert [item.start_offset for item in evidence] == sorted(
        item.start_offset for item in evidence
    )
    for observation, source in zip(outcome.observations, evidence):
        assert observation.feature_id is FeatureId.CONDITION_CONTEXT
        assert observation.evidence_refs == (source.evidence_id,)
        assert source.requirement_id == requirement.id
        assert source.feature_id is FeatureId.CONDITION_CONTEXT
        assert source.rule_id == RULE_ID
        assert text[source.start_offset:source.end_offset] == source.text

    for diagnostic in outcome.diagnostics:
        assert diagnostic.code == UNRESOLVED_CANDIDATE_CODE
        assert diagnostic.rule_id == RULE_ID
        assert diagnostic.candidate_span is not None
        span = diagnostic.candidate_span
        assert text[span.start_offset:span.end_offset] == span.text
    return outcome, evidence


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "Якщо сервіс недоступний, система повинна зберегти запит.",
            "Якщо сервіс недоступний",
        ),
        (
            "Маршрут доставки повинен перераховуватися у разі зміни дорожньої ситуації.",
            "у разі зміни дорожньої ситуації",
        ),
        (
            "Система повинна залишатися доступною під час пікового навантаження.",
            "під час пікового навантаження",
        ),
    ],
)
def test_normative_reference_cases(text, expected):
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.diagnostics == ()
    assert [item.text for item in evidence] == [expected]


def test_quantitative_reference_case_reuses_accepted_anchor():
    text = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert [item.text for item in evidence] == ["при 500 одночасних користувачах"]
    assert evidence[0].evidence_id == "COND-UK-001:E001"
    assert outcome.observations[0].evidence_refs == ("COND-UK-001:E001",)


def test_binding_unresolved_case_is_diagnostic_only():
    text = "Система повідомляє про помилку при перевірці."
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert len(outcome.diagnostics) == 1
    span = outcome.diagnostics[0].candidate_span
    assert (span.text, span.start_offset, span.end_offset) == (
        "при перевірці", 31, 44,
    )


def test_uppercase_markers_and_normative_anchors_are_casefolded():
    text = "ЯКЩО СЕРВІС НЕДОСТУПНИЙ, СИСТЕМА ПОВИННА ЗБЕРЕГТИ ЗАПИТ."
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["ЯКЩО СЕРВІС НЕДОСТУПНИЙ"]


def test_decomposed_unicode_before_and_inside_candidate_preserves_offsets():
    decomposed = unicodedata.normalize("NFD", "Ї")
    assert len(decomposed) == 2
    text = f"{decomposed}: Система повинна діяти при зміні {decomposed}ї стану."
    outcome, evidence = scan(text)
    start = text.index("при")
    expected = f"при зміні {decomposed}ї стану"
    assert outcome.status is DetectionStatus.DETECTED
    assert [(item.start_offset, item.end_offset, item.text) for item in evidence] == [
        (start, start + len(expected), expected),
    ]


@pytest.mark.parametrize(
    "marker",
    ["У\tРАЗІ", "ПІД\u00a0\u00a0ЧАС"],
)
def test_unicode_whitespace_in_multi_token_marker_is_preserved(marker):
    text = f"Система МАЄ діяти {marker} збою."
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [f"{marker} збою"]


@pytest.mark.parametrize("boundary", [".", ";", "?", "!"])
def test_attachment_does_not_cross_hard_punctuation(boundary):
    text = f"Система повинна діяти{boundary} при збої."
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.candidate_span.text for item in outcome.diagnostics] == ["при збої"]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "Система повинна використовувати TLS 1.3 при навантаженні.",
            "при навантаженні",
        ),
        (
            "Система має використовувати OAuth 2.0 під час авторизації.",
            "під час авторизації",
        ),
    ],
)
def test_approved_technical_version_dot_does_not_split_condition_segment(
    text, expected,
):
    requirement = Requirement("R011", 7, text)
    quantitative_detector = QuantitativeBaselineDetector()
    quantitative_before = quantitative_detector.detect(requirement)

    outcome, evidence = ConditionContextBaselineDetector(
        quantitative_detector,
    ).detect(requirement)

    quantitative_after = quantitative_detector.detect(requirement)
    quantitative_outcome, quantitative_evidence = quantitative_before
    assert quantitative_before == quantitative_after
    assert quantitative_outcome.observations == quantitative_evidence == ()
    assert quantitative_outcome.diagnostics == ()
    assert (
        quantitative_outcome.processing_status
        is DetectionProcessingStatus.COMPLETE
    )
    assert quantitative_outcome.status is DetectionStatus.NOT_DETECTED

    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.diagnostics == ()
    assert [item.text for item in evidence] == [expected]


def test_semicolon_separated_segments_are_processed_independently():
    text = (
        "Система повинна діяти у разі збою; "
        "сервіс має сповістити під час відновлення."
    )
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert [item.text for item in evidence] == [
        "у разі збою", "під час відновлення",
    ]


@pytest.mark.parametrize(
    "text",
    [
        "Система повинна активувати прилад.",
        "Система повинна виконати x-при-перевірку.",
    ],
)
def test_marker_does_not_match_inside_larger_joined_word(text):
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.status is DetectionStatus.NOT_DETECTED


@pytest.mark.parametrize("text", ["при", "Система повинна діяти при."])
def test_bare_marker_is_not_a_candidate(text):
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_no_marker_is_complete_not_detected():
    outcome, evidence = scan("Система формує звіт.")
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_postposed_yakshcho_is_not_accepted():
    text = "Система повинна зберегти запит якщо сервіс недоступний."
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "якщо сервіс недоступний",
    ]


def test_leading_candidate_without_approved_attachment_is_unresolved():
    text = "Якщо сервіс недоступний, система зберігає запит."
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "Якщо сервіс недоступний",
    ]


def test_comma_after_governing_anchor_does_not_change_leading_boundary():
    text = (
        "Якщо сервіс недоступний, система повинна зберегти запит, журнал і стан."
    )
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert [item.text for item in evidence] == ["Якщо сервіс недоступний"]


def test_unresolved_quantitative_candidate_is_not_an_attachment_anchor():
    text = "Профіль 95 при навантаженні."
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "при навантаженні",
    ]


def test_decimal_comma_in_approved_numeric_expression_is_not_clause_delimiter():
    text = "Якщо доступність 99,9 %, система повинна сповістити оператора."
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert [item.text for item in evidence] == ["Якщо доступність 99,9 %"]


def test_repeated_conditions_have_source_ordered_evidence_ids():
    text = (
        "Система повинна діяти у разі збою; "
        "система повинна сповістити у разі збою."
    )
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["у разі збою", "у разі збою"]
    assert [item.evidence_id for item in evidence] == [
        "COND-UK-001:E001", "COND-UK-001:E002",
    ]
    assert [item.evidence_refs for item in outcome.observations] == [
        ("COND-UK-001:E001",), ("COND-UK-001:E002",),
    ]


def test_accepted_and_unresolved_candidates_preserve_mixed_state():
    text = (
        "Система повинна діяти у разі збою; "
        "система повідомляє при перевірці."
    )
    outcome, evidence = scan(text)
    assert [item.text for item in evidence] == ["у разі збою"]
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "при перевірці",
    ]
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED


def test_only_approved_marker_inventory_is_supported():
    text = (
        "Система повинна діяти коли виникає збій; "
        "система має сповістити за умови відмови."
    )
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_normative_tokens_are_attachment_only():
    outcome, evidence = scan("Система повинна діяти у разі збою.")
    assert len(outcome.observations) == len(evidence) == 1
    observation = outcome.observations[0]
    assert observation.feature_id is FeatureId.CONDITION_CONTEXT
    assert not hasattr(observation, "expected_results")


def test_repeated_runs_are_deterministically_equal():
    text = "Якщо є збій, система повинна діяти; сервіс повідомляє при перевірці."
    assert scan(text) == scan(text)

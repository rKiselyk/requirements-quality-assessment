"""Approved QUANT-001 and QUANT-UK-001 first-production behavior."""

from decimal import Decimal
import subprocess
import sys
import unicodedata

import pytest

from requirements_quality_assessment.detectors import QuantitativeBaselineDetector
from requirements_quality_assessment.detectors.quantitative import (
    QUANT_RULE_ID,
    QUANT_UK_RULE_ID,
    UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorLabel,
    DetectionProcessingStatus,
    DetectionStatus,
    FeatureId,
    Requirement,
    UnitLabel,
)


def scan(text: str):
    requirement = Requirement("R007", 3, text)
    outcome, evidence = QuantitativeBaselineDetector().detect(requirement)

    assert outcome.feature_id is FeatureId.QUANTITATIVE_CONSTRAINT
    assert len(outcome.observations) == len(evidence)
    assert [item.start_offset for item in evidence] == sorted(
        item.start_offset for item in evidence
    )
    for observation, source in zip(outcome.observations, evidence):
        assert source.requirement_id == requirement.id
        assert source.feature_id is FeatureId.QUANTITATIVE_CONSTRAINT
        assert source.rule_id in {QUANT_RULE_ID, QUANT_UK_RULE_ID}
        assert text[source.start_offset:source.end_offset] == source.text
        assert observation.feature_id is FeatureId.QUANTITATIVE_CONSTRAINT
        assert observation.metric is None
        assert observation.context is None
        assert observation.unresolved_components == ()
        component_refs = {
            ref
            for component in (
                observation.metric,
                observation.comparator,
                observation.value,
                observation.unit,
                observation.context,
            )
            if component is not None
            for ref in component.evidence_refs
        }
        assert set(observation.evidence_refs) == component_refs
        assert observation.evidence_refs == (source.evidence_id,)

    for diagnostic in outcome.diagnostics:
        assert diagnostic.code == UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE
        assert diagnostic.rule_id == QUANT_RULE_ID
        assert diagnostic.candidate_span is not None
        span = diagnostic.candidate_span
        assert text[span.start_offset:span.end_offset] == span.text
        assert all(
            not (source.start_offset == span.start_offset
                 and source.end_offset == span.end_offset)
            for source in evidence
        )
    return outcome, evidence


@pytest.mark.parametrize(
    ("text", "rule_id", "label", "inclusivity", "value", "unit"),
    [
        ("≤ 2", QUANT_RULE_ID, ComparatorLabel.LESS_THAN_OR_EQUAL,
         BoundaryInclusivity.INCLUSIVE, Decimal("2"), None),
        ("≤ 2 с", QUANT_RULE_ID, ComparatorLabel.LESS_THAN_OR_EQUAL,
         BoundaryInclusivity.INCLUSIVE, Decimal("2"), UnitLabel.SECOND),
        ("не довше 3 с", QUANT_UK_RULE_ID, ComparatorLabel.LESS_THAN_OR_EQUAL,
         BoundaryInclusivity.INCLUSIVE, Decimal("3"), UnitLabel.SECOND),
        ("не довше ніж 3 с", QUANT_UK_RULE_ID, ComparatorLabel.LESS_THAN_OR_EQUAL,
         BoundaryInclusivity.INCLUSIVE, Decimal("3"), UnitLabel.SECOND),
        ("не більше 3 с", QUANT_UK_RULE_ID, ComparatorLabel.LESS_THAN_OR_EQUAL,
         BoundaryInclusivity.INCLUSIVE, Decimal("3"), UnitLabel.SECOND),
        ("не більше ніж 3 с", QUANT_UK_RULE_ID, ComparatorLabel.LESS_THAN_OR_EQUAL,
         BoundaryInclusivity.INCLUSIVE, Decimal("3"), UnitLabel.SECOND),
        ("не нижче 99,9 %", QUANT_UK_RULE_ID, ComparatorLabel.GREATER_THAN_OR_EQUAL,
         BoundaryInclusivity.INCLUSIVE, Decimal("99.9"), UnitLabel.PERCENT),
        ("не нижче 99,9%", QUANT_UK_RULE_ID, ComparatorLabel.GREATER_THAN_OR_EQUAL,
         BoundaryInclusivity.INCLUSIVE, Decimal("99.9"), UnitLabel.PERCENT),
        ("≤ 95%", QUANT_RULE_ID, ComparatorLabel.LESS_THAN_OR_EQUAL,
         BoundaryInclusivity.INCLUSIVE, Decimal("95"), UnitLabel.PERCENT),
        ("до 300", QUANT_UK_RULE_ID, ComparatorLabel.UPPER_BOUND,
         BoundaryInclusivity.UNRESOLVED, Decimal("300"), None),
        ("не довше ніж за 2 с", QUANT_UK_RULE_ID,
         ComparatorLabel.LESS_THAN_OR_EQUAL, BoundaryInclusivity.INCLUSIVE,
         Decimal("2"), UnitLabel.SECOND),
        ("не більше ніж за 4 с", QUANT_UK_RULE_ID,
         ComparatorLabel.LESS_THAN_OR_EQUAL, BoundaryInclusivity.INCLUSIVE,
         Decimal("4"), UnitLabel.SECOND),
    ],
)
def test_comparator_reference_cases(
    text, rule_id, label, inclusivity, value, unit,
):
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.diagnostics == ()
    assert [item.text for item in evidence] == [text]
    assert [item.rule_id for item in evidence] == [rule_id]
    observation = outcome.observations[0]
    assert observation.comparator.label is label
    assert observation.comparator.inclusivity is inclusivity
    assert observation.value.decimal_value == value
    assert observation.unit is None if unit is None else observation.unit.label is unit


@pytest.mark.parametrize(
    ("text", "value", "unit"),
    [
        ("3 с", Decimal("3"), UnitLabel.SECOND),
        ("10 секунд", Decimal("10"), UnitLabel.SECOND),
        ("5 хв", Decimal("5"), UnitLabel.MINUTE),
        ("5 хвилин", Decimal("5"), UnitLabel.MINUTE),
        ("99,9 %", Decimal("99.9"), UnitLabel.PERCENT),
        ("99,9%", Decimal("99.9"), UnitLabel.PERCENT),
        ("95 %", Decimal("95"), UnitLabel.PERCENT),
        ("95%", Decimal("95"), UnitLabel.PERCENT),
    ],
)
def test_value_unit_fallbacks_and_every_supported_unit(text, value, unit):
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.diagnostics == ()
    assert [item.text for item in evidence] == [text]
    assert [item.rule_id for item in evidence] == [QUANT_RULE_ID]
    observation = outcome.observations[0]
    assert observation.comparator is None
    assert observation.value.decimal_value == value
    assert observation.unit.label is unit


def test_nested_fallback_is_suppressed_inside_comparator_anchor():
    outcome, evidence = scan("не більше 3 с")
    assert len(outcome.observations) == len(evidence) == 1
    assert evidence[0].text == "не більше 3 с"
    assert outcome.observations[0].comparator is not None


def test_casefold_and_unicode_whitespace_preserve_exact_source():
    text = "НЕ\tБІЛЬШЕ\u00a0\u00a03 с"
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert evidence[0].text == text
    assert outcome.observations[0].comparator.label is ComparatorLabel.LESS_THAN_OR_EQUAL


def test_provenance_maps_normalized_view_back_to_original_code_points():
    decomposed_prefix = unicodedata.normalize("NFD", "Ї")
    assert len(decomposed_prefix) > len(unicodedata.normalize("NFC", decomposed_prefix))
    text = f"{decomposed_prefix}: НЕ БІЛЬШЕ 3 с."
    outcome, evidence = scan(text)
    start = text.index("НЕ")
    assert outcome.status is DetectionStatus.DETECTED
    assert [(item.start_offset, item.end_offset, item.text) for item in evidence] == [
        (start, start + len("НЕ БІЛЬШЕ 3 с"), "НЕ БІЛЬШЕ 3 с")
    ]


@pytest.mark.parametrize("text", [
    "псевдодо 300",
    "x-до 300",
])
def test_short_comparator_does_not_match_inside_joined_word(text):
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert [item.candidate_span.text for item in outcome.diagnostics] == ["300"]


def test_punctuation_cannot_replace_comparator_token_separator():
    outcome, evidence = scan("не,більше 3 с")
    assert [item.text for item in evidence] == ["3 с"]
    assert outcome.observations[0].comparator is None


@pytest.mark.parametrize("text", [
    "не рідше одного разу на 5 с",
    "не рідше одного разу на 10 секунд",
    "не рідше одного разу на 5 хв",
    "не рідше одного разу на 5 хвилин",
    "НЕ\tРІДШЕ\u00a0ОДНОГО  РАЗУ\tНА\u00a05 с",
])
def test_exact_deferred_frequency_construction_is_protected(text):
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_deferred_frequency_protection_is_not_broadened():
    outcome, evidence = scan("не рідше 5 с")
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["5 с"]
    assert outcome.observations[0].comparator is None


def test_multiple_anchors_are_separate_source_ordered_and_numbered_per_rule():
    text = "не більше 3 с; ≤ 2 с; до 300"
    outcome, evidence = scan(text)
    assert [item.text for item in evidence] == ["не більше 3 с", "≤ 2 с", "до 300"]
    assert [item.evidence_id for item in evidence] == [
        "QUANT-UK-001:E001", "QUANT-001:E001", "QUANT-UK-001:E002",
    ]
    assert len(outcome.observations) == 3


def test_unicode_code_point_offsets_exclude_surrounding_text_and_punctuation():
    text = "🙂 Час відгуку: ≤ 2 с."
    outcome, evidence = scan(text)
    start = text.index("≤")
    assert outcome.status is DetectionStatus.DETECTED
    assert [(item.start_offset, item.end_offset, item.text) for item in evidence] == [
        (start, start + len("≤ 2 с"), "≤ 2 с")
    ]
    observation = outcome.observations[0]
    assert observation.metric is None
    assert observation.context is None


def test_bare_numeric_candidate_is_unresolved_diagnostic_only():
    text = "Система використовує профіль 95."
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert len(outcome.diagnostics) == 1
    span = outcome.diagnostics[0].candidate_span
    assert (span.text, span.start_offset, span.end_offset) == (
        "95", text.index("95"), text.index("95") + 2,
    )


def test_accepted_anchor_and_bare_number_preserve_mixed_state():
    outcome, evidence = scan("Час ≤ 2 с; профіль 95.")
    assert [item.text for item in evidence] == ["≤ 2 с"]
    assert len(outcome.observations) == 1
    assert [item.candidate_span.text for item in outcome.diagnostics] == ["95"]
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED


def test_diagnostics_are_source_ordered_and_not_duplicated():
    outcome, evidence = scan("Профілі 95 і 17.")
    assert evidence == ()
    assert [item.candidate_span.text for item in outcome.diagnostics] == ["95", "17"]


@pytest.mark.parametrize("text", ["TLS 1.3", "OAuth 2.0"])
def test_approved_technical_versions_are_negative(text):
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


@pytest.mark.parametrize("text", [
    "1.5 с",
    "≤ 1.5 с",
    "1e5 с",
    "1 000 с",
    "1234 567 с",
    "1-5 с",
    "+ 5 с",
])
def test_unsupported_numeric_form_is_not_partially_salvaged(text):
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_unsupported_written_out_number_is_not_parsed():
    outcome, evidence = scan("не більше трьох секунд")
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.status is DetectionStatus.NOT_DETECTED


@pytest.mark.parametrize("text", [
    "3 сек",
    "3 секунда",
    "3 секунди",
    "3 мс",
    "3 seconds",
    "3 відсотків",
])
def test_unsupported_unit_alias_is_not_normalized(text):
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert [item.candidate_span.text for item in outcome.diagnostics] == ["3"]


@pytest.mark.parametrize("text", ["3 хвилинами", "3 секундний"])
def test_unit_literal_is_not_matched_inside_longer_word(text):
    outcome, evidence = scan(text)
    assert outcome.observations == evidence == ()
    assert [item.candidate_span.text for item in outcome.diagnostics] == ["3"]


def test_joined_alphabetic_unit_is_not_authorized_by_percent_layout():
    outcome, evidence = scan("3с")
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_no_numeric_candidate_is_complete_not_detected():
    outcome, evidence = scan("Система формує звіт.")
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_repeated_runs_are_deterministically_equal():
    text = "не нижче 99,9 %; ≤ 2 с; профіль 95"
    assert scan(text) == scan(text)


def test_detector_import_and_run_without_spacy():
    code = (
        "import sys; "
        "from requirements_quality_assessment.detectors import QuantitativeBaselineDetector; "
        "from requirements_quality_assessment.domain import Requirement; "
        "QuantitativeBaselineDetector().detect(Requirement('R1', 1, '≤ 2 с')); "
        "assert 'spacy' not in sys.modules"
    )
    subprocess.run([sys.executable, "-c", code], check=True)

"""Approved UK-VAGUE-001 behavior from model-spec Section 7.14.8."""

import subprocess
import sys
import unicodedata

import pytest

from requirements_quality_assessment.detectors import UkVagueTermDetector
from requirements_quality_assessment.detectors.vague_terms import RULE_ID, VOCABULARY, VOCABULARY_ID
from requirements_quality_assessment.domain import (
    DetectionProcessingStatus, DetectionStatus, FeatureId, Requirement,
)


def scan(text: str):
    requirement = Requirement("R007", 3, text)
    outcome, evidence = UkVagueTermDetector().detect(requirement)
    assert outcome.feature_id is FeatureId.VAGUE_TERM_OCCURRENCE
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.diagnostics == ()
    assert all(item.feature_id is FeatureId.VAGUE_TERM_OCCURRENCE
               and item.requirement_id == requirement.id and item.rule_id == RULE_ID
               and text[item.start_offset:item.end_offset] == item.text
               for item in evidence)
    assert all(item.feature_id is FeatureId.VAGUE_TERM_OCCURRENCE
               and item.vocabulary_id == VOCABULARY_ID
               and item.matched_literal in VOCABULARY
               and item.evidence_refs == (source.evidence_id,)
               for item, source in zip(outcome.observations, evidence))
    assert len(outcome.observations) == len(evidence)
    assert [item.start_offset for item in evidence] == sorted(
        item.start_offset for item in evidence
    )
    assert [item.evidence_id for item in evidence] == [
        f"{RULE_ID}:E{number:03d}" for number in range(1, len(evidence) + 1)
    ]
    return outcome, evidence


@pytest.mark.parametrize("literal", VOCABULARY)
def test_exact_ten_canonical_literals(literal):
    outcome, evidence = scan(f"«{literal}»")
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.matched_literal for item in outcome.observations] == [literal]
    assert [item.text for item in evidence] == [literal]
    assert [(item.start_offset, item.end_offset) for item in evidence] == [
        (1, 1 + len(literal))
    ]


def test_case_reference_preserves_uppercase_source():
    outcome, evidence = scan("Система повинна ШВИДКО сформувати звіт.")
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.matched_literal for item in outcome.observations] == ["швидко"]
    assert [(item.text, item.start_offset, item.end_offset) for item in evidence] == [
        ("ШВИДКО", 16, 22)
    ]


def test_longer_word_reference_is_complete_no_hit():
    outcome, evidence = scan("Система працює надшвидко.")
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.observations == evidence == ()


def test_repeated_reference_has_distinct_source_order_evidence():
    outcome, evidence = scan("Швидко сформувати звіт і швидко надіслати його.")
    assert outcome.status is DetectionStatus.DETECTED
    assert [(item.start_offset, item.end_offset, item.text) for item in evidence] == [
        (0, 6, "Швидко"), (25, 31, "швидко")
    ]


def test_punctuation_reference_excludes_surrounding_marks():
    outcome, evidence = scan("Система повинна працювати «швидко», надійно.")
    assert outcome.status is DetectionStatus.DETECTED
    assert [(item.start_offset, item.end_offset, item.text) for item in evidence] == [
        (27, 33, "швидко"), (36, 43, "надійно")
    ]


def test_overlap_reference_selects_longer_phrase_before_ids():
    reference = "Персональні та комерційні дані повинні бути надійно захищені."
    reference_outcome, reference_evidence = scan(reference)
    assert [item.matched_literal for item in reference_outcome.observations] == [
        "надійно захищені"
    ]
    assert [(item.start_offset, item.end_offset, item.text) for item in reference_evidence] == [
        (44, 60, "надійно захищені")
    ]

    outcome, evidence = scan(
        reference + " швидко"
    )
    assert [item.matched_literal for item in outcome.observations] == [
        "надійно захищені", "швидко"
    ]
    assert [(item.start_offset, item.end_offset, item.text) for item in evidence] == [
        (44, 60, "надійно захищені"), (62, 68, "швидко")
    ]


@pytest.mark.parametrize("text", [
    "дуже-швидко", "x'швидко", "x’швидко", "xʼшвидко",
    "x_швидко", "x‿швидко", "x-швидко", "реальному часі",
    "у реальному,часі", "швидка", "надійні", "швидко́",
])
def test_no_joined_word_inflection_or_punctuation_substitution(text):
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert evidence == ()


@pytest.mark.parametrize("text", ["(швидко)", "«швидко»", "швидко,"])
def test_ordinary_punctuation_forms_boundaries(text):
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["швидко"]


@pytest.mark.parametrize("separator", ["  ", "\t", "\u00a0", "\n"])
def test_phrase_preserves_original_unicode_whitespace(separator):
    text = f"У реальному{separator}часі система реагує."
    outcome, evidence = scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.matched_literal for item in outcome.observations] == [
        "у реальному часі"
    ]
    assert [item.text for item in evidence] == [f"У реальному{separator}часі"]


def test_decomposed_ukrainian_letter_preserves_original_spelling():
    decomposed = unicodedata.normalize("NFD", "надійно")
    assert len(decomposed) > len("надійно")
    text = f"Система діє {decomposed}."
    outcome, evidence = scan(text)
    assert [item.matched_literal for item in outcome.observations] == ["надійно"]
    assert [(item.start_offset, item.end_offset, item.text) for item in evidence] == [
        (text.index(decomposed), text.index(decomposed) + len(decomposed), decomposed)
    ]


def test_casefold_expansion_before_occurrence_preserves_original_offsets():
    text = "ẞ: швидко"
    assert len("ẞ".casefold()) == 2
    outcome, evidence = scan(text)
    assert [item.matched_literal for item in outcome.observations] == ["швидко"]
    assert [(item.start_offset, item.end_offset, item.text) for item in evidence] == [
        (3, 9, "швидко")
    ]


def test_repeated_runs_are_deterministically_equal():
    text = "Швидко і надійно захищені, швидко."
    assert scan(text) == scan(text)


def test_detector_import_and_run_without_spacy():
    code = (
        "import sys; "
        "from requirements_quality_assessment.detectors import UkVagueTermDetector; "
        "from requirements_quality_assessment.domain import Requirement; "
        "UkVagueTermDetector().detect(Requirement('R1', 1, 'швидко')); "
        "assert 'spacy' not in sys.modules"
    )
    subprocess.run([sys.executable, "-c", code], check=True)

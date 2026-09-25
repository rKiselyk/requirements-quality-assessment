"""Approved RESULT-UK-001 first-production behavior."""

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

import pytest

from requirements_quality_assessment.detectors import (
    DirectivePassiveExpectedResultDetector,
    ExpectedResultBaselineDetector,
    ExpectedResultDetector,
    QuantitativeBaselineDetector,
)
from requirements_quality_assessment.detectors.directive_passive_result import (
    IMPERATIVE_SURFACES,
    PARSER_BLOCKED_CODE as COVERAGE_PARSER_BLOCKED_CODE,
    RULE_ID as COVERAGE_RULE_ID,
    UNRESOLVED_CODE as COVERAGE_UNRESOLVED_CODE,
)
from requirements_quality_assessment.detectors.expected_result import (
    NORMATIVE_SURFACES,
    PARSER_BLOCKED_CODE,
    RULE_ID,
    UNRESOLVED_CANDIDATE_CODE,
)
from requirements_quality_assessment.domain import (
    DetectionProcessingStatus,
    DetectionStatus,
    DiagnosticSpan,
    FeatureId,
    FeatureObservation,
    MorphFeature,
    ParsedRequirement,
    ParserDiagnostic,
    ParserDiagnosticCode,
    ParserMetadata,
    ParserOutcome,
    Requirement,
    SentenceAnnotation,
    TokenAnnotation,
)


@dataclass(frozen=True)
class _TokenSpec:
    surface: str
    upos: str | None
    head: int | None
    relation: str | None
    morphology: tuple[MorphFeature, ...] = ()
    sentence_id: int = 0
    lemma: str | None = None


class _FakeParser:
    def __init__(self, outcome: ParserOutcome):
        self.outcome = outcome
        self.calls = 0

    def parse(self, requirement: Requirement) -> ParserOutcome:
        self.calls += 1
        return self.outcome


def _participle() -> tuple[MorphFeature, ...]:
    return (MorphFeature("VerbForm", ("Part",)),)


def _negation() -> tuple[MorphFeature, ...]:
    return (MorphFeature("Polarity", ("Neg",)),)


def _infinitive() -> tuple[MorphFeature, ...]:
    return (MorphFeature("VerbForm", ("Inf",)),)


def _impersonal_finite() -> tuple[MorphFeature, ...]:
    return (
        MorphFeature("Person", ("0",)),
        MorphFeature("VerbForm", ("Fin",)),
    )


def _parsed(
    requirement: Requirement,
    specs: tuple[_TokenSpec, ...],
    sentence_ranges: tuple[tuple[int, int], ...] | None = None,
) -> ParsedRequirement:
    if sentence_ranges is None:
        sentence_ranges = ((0, len(requirement.text)),)
    sentences = tuple(
        SentenceAnnotation(sentence_id, start, end)
        for sentence_id, (start, end) in enumerate(sentence_ranges)
    )
    cursors = {sentence_id: start for sentence_id, (start, _) in enumerate(sentence_ranges)}
    tokens = []
    for token_id, spec in enumerate(specs):
        start = requirement.text.index(spec.surface, cursors[spec.sentence_id])
        end = start + len(spec.surface)
        cursors[spec.sentence_id] = end
        tokens.append(
            TokenAnnotation(
                token_id=token_id,
                sentence_id=spec.sentence_id,
                text=spec.surface,
                start_offset=start,
                end_offset=end,
                lemma=spec.lemma,
                upos=spec.upos,
                morphology=spec.morphology,
                head_token_id=spec.head,
                dependency_relation=spec.relation,
            )
        )
    return ParsedRequirement(
        requirement_id=requirement.id,
        text=requirement.text,
        sentences=sentences,
        tokens=tuple(tokens),
        parser=ParserMetadata("fake", "1", "fake-uk", "1", "uk"),
    )


def _active_specs(
    subject: str,
    normative: str,
    predicate: str,
    object_: str | None = None,
    *,
    subject_relation: str = "nsubj",
    sentence_id: int = 0,
    token_id_base: int = 0,
) -> tuple[_TokenSpec, ...]:
    specs = [
        _TokenSpec(subject, "NOUN", token_id_base + 1, subject_relation, sentence_id=sentence_id),
        _TokenSpec(normative, "ADJ", None, "ROOT", sentence_id=sentence_id),
        _TokenSpec(predicate, "VERB", token_id_base + 1, "xcomp", sentence_id=sentence_id),
    ]
    if object_ is not None:
        specs.append(
            _TokenSpec(object_, "NOUN", token_id_base + 2, "obj", sentence_id=sentence_id)
        )
    return tuple(specs)


def _scan(
    text: str,
    specs: tuple[_TokenSpec, ...],
    *,
    sentence_ranges: tuple[tuple[int, int], ...] | None = None,
):
    requirement = Requirement("R040", 9, text)
    parser = _FakeParser(ParserOutcome(_parsed(requirement, specs, sentence_ranges), ()))
    outcome, evidence = ExpectedResultBaselineDetector(parser=parser).detect(requirement)

    assert parser.calls == 1
    assert outcome.feature_id is FeatureId.EXPECTED_RESULT
    assert all(isinstance(item, FeatureObservation) for item in outcome.observations)
    assert len(outcome.observations) == len(evidence)
    assert [item.start_offset for item in evidence] == sorted(
        item.start_offset for item in evidence
    )
    for observation, source in zip(outcome.observations, evidence):
        assert observation.feature_id is FeatureId.EXPECTED_RESULT
        assert observation.evidence_refs == (source.evidence_id,)
        assert source.requirement_id == requirement.id
        assert source.feature_id is FeatureId.EXPECTED_RESULT
        assert source.rule_id == RULE_ID
        assert text[source.start_offset:source.end_offset] == source.text
    for diagnostic in outcome.diagnostics:
        assert diagnostic.rule_id == RULE_ID
        if diagnostic.candidate_span is not None:
            span = diagnostic.candidate_span
            assert text[span.start_offset:span.end_offset] == span.text
    return requirement, outcome, evidence


def _scan_coverage(
    text: str,
    specs: tuple[_TokenSpec, ...],
    *,
    sentence_ranges: tuple[tuple[int, int], ...] | None = None,
):
    requirement = Requirement("R043", 12, text)
    parser = _FakeParser(ParserOutcome(_parsed(requirement, specs, sentence_ranges), ()))
    outcome, evidence = DirectivePassiveExpectedResultDetector(parser).detect(
        requirement
    )
    assert parser.calls == 1
    return requirement, outcome, evidence


@pytest.mark.parametrize("directive", sorted(IMPERATIVE_SURFACES))
def test_bounded_imperative_directives_are_expected_results(directive):
    text = f"{directive.capitalize()} журнал аудиту."
    specs = (
        _TokenSpec(
            directive.capitalize(), "VERB", None, "ROOT", _infinitive()
        ),
        _TokenSpec("журнал", "NOUN", 0, "obj"),
        _TokenSpec("аудиту", "NOUN", 1, "nmod"),
    )
    _, outcome, evidence = _scan_coverage(text, specs)

    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert len(outcome.observations) == len(evidence) == 1
    assert outcome.observations[0].evidence_refs == ("RESULT-UK-003:E001",)
    assert (
        evidence[0].rule_id,
        evidence[0].text,
        evidence[0].start_offset,
        evidence[0].end_offset,
    ) == (COVERAGE_RULE_ID, text[:-1], 0, len(text) - 1)


@pytest.mark.parametrize(
    ("text", "specs"),
    [
        (
            "Завдання: додати журнал.",
            (
                _TokenSpec("Завдання", "NOUN", None, "ROOT"),
                _TokenSpec(":", "PUNCT", 0, "punct"),
                _TokenSpec("додати", "VERB", 0, "acl", _infinitive()),
                _TokenSpec("журнал", "NOUN", 2, "obj"),
            ),
        ),
        (
            "Щоб додати журнал, відкрийте меню.",
            (
                _TokenSpec("Щоб", "SCONJ", 1, "mark"),
                _TokenSpec("додати", "VERB", 3, "advcl", _infinitive()),
                _TokenSpec("журнал", "NOUN", 1, "obj"),
                _TokenSpec("відкрийте", "VERB", None, "ROOT"),
                _TokenSpec("меню", "NOUN", 3, "obj"),
            ),
        ),
        (
            "Додати.",
            (
                _TokenSpec("Додати", "VERB", None, "ROOT", _infinitive()),
            ),
        ),
        (
            "Перенести журнал.",
            (
                _TokenSpec("Перенести", "VERB", None, "ROOT", _infinitive()),
                _TokenSpec("журнал", "NOUN", 0, "obj"),
            ),
        ),
    ],
)
def test_headings_fragments_unrelated_and_unlisted_infinitives_are_not_detected(
    text, specs
):
    _, outcome, evidence = _scan_coverage(text, specs)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.observations == evidence == outcome.diagnostics == ()


def test_imperative_predicate_coordination_remains_unresolved():
    text = "Додати модуль і створити схему."
    specs = (
        _TokenSpec("Додати", "VERB", None, "ROOT", _infinitive()),
        _TokenSpec("модуль", "NOUN", 0, "obj"),
        _TokenSpec("і", "CCONJ", 3, "cc"),
        _TokenSpec("створити", "VERB", 0, "conj", _infinitive()),
        _TokenSpec("схему", "NOUN", 3, "obj"),
    )
    _, outcome, evidence = _scan_coverage(text, specs)
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.code for item in outcome.diagnostics] == [
        COVERAGE_UNRESOLVED_CODE
    ]
    assert outcome.diagnostics[0].candidate_span == DiagnosticSpan(
        text[:-1], 0, len(text) - 1
    )


@pytest.mark.parametrize("normative", ["Має", "Повинно"])
def test_simple_impersonal_passive_is_an_expected_result(normative):
    text = f"{normative} бути створено журнал аудиту."
    specs = (
        _TokenSpec(normative, "VERB" if normative == "Має" else "ADJ", None, "ROOT"),
        _TokenSpec("бути", "AUX", 2, "aux", _infinitive(), lemma="бути"),
        _TokenSpec("створено", "VERB", 0, "xcomp", _impersonal_finite()),
        _TokenSpec("журнал", "NOUN", 2, "obj"),
        _TokenSpec("аудиту", "NOUN", 3, "nmod"),
    )
    _, outcome, evidence = _scan_coverage(text, specs)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert [(item.text, item.start_offset, item.end_offset) for item in evidence] == [
        (text[:-1], 0, len(text) - 1)
    ]


def test_coordinated_passive_results_remain_unresolved_without_partial_evidence():
    text = "Має бути створено журнал і надіслано звіт."
    specs = (
        _TokenSpec("Має", "VERB", None, "ROOT"),
        _TokenSpec("бути", "AUX", 2, "aux", _infinitive(), lemma="бути"),
        _TokenSpec("створено", "VERB", 0, "xcomp", _impersonal_finite()),
        _TokenSpec("журнал", "NOUN", 2, "obj"),
        _TokenSpec("і", "CCONJ", 5, "cc"),
        _TokenSpec("надіслано", "VERB", 2, "conj", _impersonal_finite()),
        _TokenSpec("звіт", "NOUN", 5, "obj"),
    )
    _, outcome, evidence = _scan_coverage(text, specs)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].code == COVERAGE_UNRESOLVED_CODE
    assert outcome.diagnostics[0].candidate_span.text == text[:-1]


def test_simple_passive_requires_explicit_result_object():
    text = "Має бути створено."
    specs = (
        _TokenSpec("Має", "VERB", None, "ROOT"),
        _TokenSpec("бути", "AUX", 2, "aux", _infinitive(), lemma="бути"),
        _TokenSpec("створено", "VERB", 0, "xcomp", _impersonal_finite()),
    )
    _, outcome, evidence = _scan_coverage(text, specs)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.observations == evidence == outcome.diagnostics == ()


def test_coverage_evidence_keeps_absolute_offsets_across_hard_segments():
    text = "Журнал подій; Додати модуль аудиту."
    expected = "Додати модуль аудиту"
    start = text.index(expected)
    specs = (
        _TokenSpec("Журнал", "NOUN", None, "ROOT"),
        _TokenSpec("подій", "NOUN", 0, "nmod"),
        _TokenSpec("Додати", "VERB", None, "ROOT", _infinitive()),
        _TokenSpec("модуль", "NOUN", 2, "obj"),
        _TokenSpec("аудиту", "NOUN", 3, "nmod"),
    )
    _, outcome, evidence = _scan_coverage(text, specs)
    assert outcome.status is DetectionStatus.DETECTED
    assert (evidence[0].text, evidence[0].start_offset, evidence[0].end_offset) == (
        expected,
        start,
        start + len(expected),
    )


def test_coverage_parser_block_is_unresolved_only_for_source_candidate():
    requirement = Requirement("R043", 12, "Додати журнал.")
    parser = _FakeParser(
        ParserOutcome(
            None,
            (
                ParserDiagnostic(
                    ParserDiagnosticCode.PARSER_UNAVAILABLE, "provider detail"
                ),
            ),
        )
    )
    outcome, evidence = DirectivePassiveExpectedResultDetector(parser).detect(
        requirement
    )
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].code == COVERAGE_PARSER_BLOCKED_CODE


def test_composite_preserves_result_uk_001_behavior():
    text = "Система повинна сформувати звіт."
    requirement = Requirement("R043", 12, text)
    parser = _FakeParser(
        ParserOutcome(
            _parsed(requirement, _active_specs("Система", "повинна", "сформувати", "звіт")),
            (),
        )
    )
    outcome, evidence = ExpectedResultDetector(parser).detect(requirement)
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert [(item.rule_id, item.text) for item in evidence] == [
        (RULE_ID, text[:-1])
    ]


def test_simple_active_binding_case():
    text = "Система повинна сформувати звіт."
    _, outcome, evidence = _scan(
        text, _active_specs("Система", "повинна", "сформувати", "звіт")
    )
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert [item.text for item in evidence] == ["Система повинна сформувати звіт"]


@pytest.mark.parametrize("normative", sorted(NORMATIVE_SURFACES))
def test_all_five_exact_normative_surfaces(normative):
    text = f"Система {normative} сформувати звіт."
    _, outcome, evidence = _scan(
        text, _active_specs("Система", normative, "сформувати", "звіт")
    )
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [text[:-1]]


def test_uppercase_normative_surface_is_casefolded_but_evidence_is_original():
    text = "СИСТЕМА ПОВИННА СФОРМУВАТИ ЗВІТ."
    _, outcome, evidence = _scan(
        text, _active_specs("СИСТЕМА", "ПОВИННА", "СФОРМУВАТИ", "ЗВІТ")
    )
    assert outcome.status is DetectionStatus.DETECTED
    assert evidence[0].text == text[:-1]


def test_nsubj_subtype_is_an_explicit_local_subject():
    text = "Маршрут має бути сформований."
    specs = (
        _TokenSpec("Маршрут", "NOUN", 1, "nsubj:pass"),
        _TokenSpec("має", "VERB", None, "ROOT"),
        _TokenSpec("бути", "AUX", 3, "cop"),
        _TokenSpec("сформований", "ADJ", 1, "xcomp", _participle()),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [text[:-1]]


def test_missing_explicit_subject_is_unresolved():
    text = "Потрібно повинна сформувати звіт."
    specs = (
        _TokenSpec("Потрібно", "ADV", 1, "advmod"),
        _TokenSpec("повинна", "ADJ", None, "ROOT"),
        _TokenSpec("сформувати", "VERB", 1, "xcomp"),
        _TokenSpec("звіт", "NOUN", 2, "obj"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].code == UNRESOLVED_CANDIDATE_CODE


def test_passive_binding_case_uses_participial_morphology():
    text = "новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с"
    specs = (
        _TokenSpec("новий", "ADJ", 1, "amod"),
        _TokenSpec("маршрут", "NOUN", 6, "nsubj"),
        _TokenSpec("для", "ADP", 4, "case"),
        _TokenSpec("95", "NUM", 4, "nummod"),
        _TokenSpec("%", "NOUN", 1, "nmod"),
        _TokenSpec("запитів", "NOUN", 4, "nmod"),
        _TokenSpec("має", "VERB", None, "ROOT"),
        _TokenSpec("бути", "AUX", 8, "cop"),
        _TokenSpec("сформований", "ADJ", 6, "xcomp", _participle()),
        _TokenSpec("не", "PART", 10, "advmod"),
        _TokenSpec("більше", "ADV", 14, "advmod"),
        _TokenSpec("ніж", "SCONJ", 10, "fixed"),
        _TokenSpec("за", "ADP", 14, "case"),
        _TokenSpec("4", "NUM", 14, "nummod:gov"),
        _TokenSpec("с", "NOUN", 8, "obl"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [text]


def test_leading_condition_is_removed_using_cond_uk_001():
    text = "Якщо сервіс недоступний, система повинна зберегти запит."
    specs = (
        _TokenSpec("Якщо", "SCONJ", 2, "mark"),
        _TokenSpec("сервіс", "NOUN", 2, "nsubj"),
        _TokenSpec("недоступний", "ADJ", 5, "advcl"),
        _TokenSpec(",", "PUNCT", 2, "punct"),
        _TokenSpec("система", "NOUN", 5, "nsubj"),
        _TokenSpec("повинна", "ADJ", None, "ROOT"),
        _TokenSpec("зберегти", "VERB", 5, "xcomp"),
        _TokenSpec("запит", "NOUN", 6, "obj"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["система повинна зберегти запит"]
    assert evidence[0].start_offset == text.index("система")


def test_postposed_condition_is_removed_using_cond_uk_001():
    text = "Система повинна залишатися доступною під час пікового навантаження."
    specs = (
        _TokenSpec("Система", "NOUN", 1, "nsubj"),
        _TokenSpec("повинна", "ADJ", None, "ROOT"),
        _TokenSpec("залишатися", "VERB", 1, "xcomp"),
        _TokenSpec("доступною", "ADJ", 2, "xcomp:sp"),
        _TokenSpec("під", "ADP", 5, "case"),
        _TokenSpec("час", "NOUN", 3, "obl"),
        _TokenSpec("пікового", "ADJ", 7, "amod"),
        _TokenSpec("навантаження", "NOUN", 5, "nmod"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["Система повинна залишатися доступною"]


def test_unresolved_condition_keeps_result_candidate_unresolved():
    text = "Система повинна повідомити при перевірці, стан."
    specs = _active_specs("Система", "повинна", "повідомити") + (
        _TokenSpec("при", "ADP", 4, "case"),
        _TokenSpec("перевірці", "NOUN", 2, "obl"),
        _TokenSpec("стан", "NOUN", 2, "obj"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.code for item in outcome.diagnostics] == [UNRESOLVED_CANDIDATE_CODE]
    assert outcome.diagnostics[0].candidate_span.text == text[:-1]


def test_quantitative_overlap_has_no_mutation_or_copied_references():
    text = "новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с"
    requirement = Requirement("R040", 9, text)
    specs = (
        _TokenSpec("маршрут", "NOUN", 4, "nsubj"),
        _TokenSpec("95", "NUM", 2, "nummod"),
        _TokenSpec("%", "NOUN", 0, "nmod"),
        _TokenSpec("запитів", "NOUN", 2, "nmod"),
        _TokenSpec("має", "VERB", None, "ROOT"),
        _TokenSpec("бути", "AUX", 6, "cop"),
        _TokenSpec("сформований", "ADJ", 4, "xcomp", _participle()),
        _TokenSpec("4", "NUM", 8, "nummod"),
        _TokenSpec("с", "NOUN", 6, "obl"),
    )
    quantitative = QuantitativeBaselineDetector()
    before = quantitative.detect(requirement)
    parser = _FakeParser(ParserOutcome(_parsed(requirement, specs), ()))
    outcome, evidence = ExpectedResultBaselineDetector(parser=parser).detect(requirement)
    after = quantitative.detect(requirement)

    assert before == after
    assert before[0].observations
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.observations[0].evidence_refs == ("RESULT-UK-001:E001",)
    assert set(outcome.observations[0].evidence_refs).isdisjoint(
        before[0].observations[0].evidence_refs
    )
    assert evidence[0].text == text


@pytest.mark.parametrize("technical", ["TLS 1.3", "OAuth 2.0"])
def test_parser_sentence_preserves_technical_version_dots(technical):
    text = f"Система повинна використовувати {technical}."
    specs = _active_specs("Система", "повинна", "використовувати") + (
        _TokenSpec(technical.split()[0], "PROPN", 2, "obj"),
        _TokenSpec(technical.split()[1], "NUM", 3, "nummod"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [text[:-1]]


def test_semicolon_segments_are_independent():
    text = "Система повинна діяти; сервіс має сповістити."
    specs = (
        *_active_specs("Система", "повинна", "діяти"),
        *_active_specs("сервіс", "має", "сповістити", token_id_base=3),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [
        "Система повинна діяти",
        "сервіс має сповістити",
    ]


def test_unicode_before_result_preserves_absolute_offsets():
    text = "Їжак; Система повинна сформувати звіт."
    specs = (
        _TokenSpec("Їжак", "NOUN", None, "ROOT"),
        *_active_specs(
            "Система", "повинна", "сформувати", "звіт", token_id_base=1
        ),
    )
    _, outcome, evidence = _scan(text, specs)
    expected = "Система повинна сформувати звіт"
    assert outcome.status is DetectionStatus.DETECTED
    assert (evidence[0].start_offset, evidence[0].end_offset, evidence[0].text) == (
        text.index(expected),
        text.index(expected) + len(expected),
        expected,
    )


def test_indicative_only_apparent_behavior_is_unresolved():
    text = "Система контролює обробку запитів."
    specs = (
        _TokenSpec("Система", "NOUN", 1, "nsubj"),
        _TokenSpec("контролює", "VERB", None, "ROOT"),
        _TokenSpec("обробку", "NOUN", 1, "obj"),
        _TokenSpec("запитів", "NOUN", 2, "nmod"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.observations == evidence == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    diagnostic = outcome.diagnostics[0]
    assert diagnostic.code == UNRESOLVED_CANDIDATE_CODE
    assert diagnostic.candidate_span.text == text[:-1]


def test_descriptive_conflict_is_not_a_result_candidate():
    text = (
        "У двох частинах документа задано різний час завершення неактивної "
        "сесії: 15 і 30 хвилин."
    )
    specs = (
        _TokenSpec("задано", "VERB", None, "ROOT"),
        _TokenSpec("час", "NOUN", 0, "obj"),
        _TokenSpec("15", "NUM", 1, "nummod"),
        _TokenSpec("30", "NUM", 1, "nummod"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_multiple_normative_anchors_in_one_segment_are_unresolved():
    text = "Система повинна та має сформувати звіт."
    specs = (
        _TokenSpec("Система", "NOUN", 1, "nsubj"),
        _TokenSpec("повинна", "ADJ", None, "ROOT"),
        _TokenSpec("має", "VERB", 1, "conj"),
        _TokenSpec("сформувати", "VERB", 1, "xcomp"),
        _TokenSpec("звіт", "NOUN", 3, "obj"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert len(outcome.diagnostics) == 1


def test_coordination_is_unresolved():
    text = "Система повинна сформувати звіт і надіслати лист."
    specs = (
        *_active_specs("Система", "повинна", "сформувати", "звіт"),
        _TokenSpec("надіслати", "VERB", 2, "conj"),
        _TokenSpec("лист", "NOUN", 4, "obj"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].code == UNRESOLVED_CANDIDATE_CODE


def test_parser_visible_negation_is_unresolved():
    text = "Система не повинна видаляти журнал."
    specs = (
        _TokenSpec("Система", "NOUN", 2, "nsubj"),
        _TokenSpec("не", "PART", 2, "advmod", _negation()),
        _TokenSpec("повинна", "ADJ", None, "ROOT"),
        _TokenSpec("видаляти", "VERB", 2, "xcomp"),
        _TokenSpec("журнал", "NOUN", 3, "obj"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].code == UNRESOLVED_CANDIDATE_CODE


@pytest.mark.parametrize(
    "code",
    [
        ParserDiagnosticCode.PARSER_UNAVAILABLE,
        ParserDiagnosticCode.PARSER_PROCESSING_FAILED,
        ParserDiagnosticCode.OFFSET_INVARIANT_FAILED,
    ],
)
def test_result_preventing_parser_failures_are_blocked(code):
    requirement = Requirement("R040", 9, "Система повинна діяти.")
    parser = _FakeParser(
        ParserOutcome(None, (ParserDiagnostic(code, "provider detail"),))
    )
    outcome, evidence = ExpectedResultBaselineDetector(parser=parser).detect(requirement)
    assert outcome.observations == evidence == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert len(outcome.diagnostics) == 1
    diagnostic = outcome.diagnostics[0]
    assert diagnostic.code == PARSER_BLOCKED_CODE
    assert diagnostic.rule_id == RULE_ID
    assert diagnostic.candidate_span is None
    assert code.value in diagnostic.explanation
    assert "provider detail" not in diagnostic.explanation


def test_annotation_incomplete_blocks_even_with_parsed_requirement():
    requirement = Requirement("R040", 9, "Система повинна діяти.")
    parsed = _parsed(
        requirement, _active_specs("Система", "повинна", "діяти")
    )
    parser = _FakeParser(
        ParserOutcome(
            parsed,
            (
                ParserDiagnostic(
                    ParserDiagnosticCode.ANNOTATION_INCOMPLETE,
                    "missing provider annotation",
                ),
            ),
        )
    )
    outcome, evidence = ExpectedResultBaselineDetector(parser=parser).detect(requirement)
    assert outcome.observations == evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].code == PARSER_BLOCKED_CODE
    assert "ANNOTATION_INCOMPLETE" in outcome.diagnostics[0].explanation


def test_no_candidate_is_complete_not_detected():
    text = "Довідкова інформація 2026."
    specs = (
        _TokenSpec("Довідкова", "ADJ", 1, "amod"),
        _TokenSpec("інформація", "NOUN", None, "ROOT"),
        _TokenSpec("2026", "NUM", 1, "nummod"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.observations == evidence == outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_repeated_source_distinct_clauses_keep_source_ordered_ids():
    first = "Система повинна діяти."
    second = "Система повинна діяти."
    text = f"{first} {second}"
    second_start = len(first) + 1
    specs = (
        *_active_specs("Система", "повинна", "діяти"),
        *_active_specs(
            "Система",
            "повинна",
            "діяти",
            sentence_id=1,
            token_id_base=3,
        ),
    )
    _, outcome, evidence = _scan(
        text,
        specs,
        sentence_ranges=((0, len(first)), (second_start, len(text))),
    )
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [first[:-1], second[:-1]]
    assert [item.evidence_id for item in evidence] == [
        "RESULT-UK-001:E001",
        "RESULT-UK-001:E002",
    ]
    assert evidence[0].start_offset != evidence[1].start_offset


def test_mixed_accepted_and_unresolved_segments_preserve_both_states():
    text = "Система повинна діяти; сервіс контролює стан."
    specs = (
        *_active_specs("Система", "повинна", "діяти"),
        _TokenSpec("сервіс", "NOUN", 4, "nsubj"),
        _TokenSpec("контролює", "VERB", None, "ROOT"),
        _TokenSpec("стан", "NOUN", 4, "obj"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert [item.text for item in evidence] == ["Система повинна діяти"]
    assert [item.evidence_id for item in evidence] == ["RESULT-UK-001:E001"]
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "сервіс контролює стан"
    ]
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED


def test_diagnostics_are_source_ordered():
    text = "Сервіс контролює стан; сформувати повинна звіт."
    specs = (
        _TokenSpec("Сервіс", "NOUN", 1, "nsubj"),
        _TokenSpec("контролює", "VERB", None, "ROOT"),
        _TokenSpec("стан", "NOUN", 1, "obj"),
        _TokenSpec("сформувати", "VERB", 4, "xcomp"),
        _TokenSpec("повинна", "ADJ", None, "ROOT"),
        _TokenSpec("звіт", "NOUN", 3, "obj"),
    )
    _, outcome, evidence = _scan(text, specs)
    assert outcome.observations == evidence == ()
    starts = [item.candidate_span.start_offset for item in outcome.diagnostics]
    assert starts == sorted(starts)
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "Сервіс контролює стан",
        "сформувати повинна звіт",
    ]


def test_default_pinned_parser_smoke_for_binding_cases():
    project_root = Path(__file__).parents[1]
    source_root = project_root / "src"
    script = f"""
import sys
sys.path.insert(0, {str(source_root)!r})
from requirements_quality_assessment.detectors import ExpectedResultBaselineDetector
from requirements_quality_assessment.detectors.expected_result import PARSER_BLOCKED_CODE
from requirements_quality_assessment.domain import DetectionProcessingStatus, DetectionStatus, Requirement

texts = (
    "Система повинна сформувати звіт.",
    "новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с",
)
detector = ExpectedResultBaselineDetector()
for text in texts:
    outcome, evidence = detector.detect(Requirement("R040", 9, text))
    if outcome.diagnostics and outcome.diagnostics[0].code == PARSER_BLOCKED_CODE:
        raise SystemExit(5)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [text.removesuffix(".")]
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

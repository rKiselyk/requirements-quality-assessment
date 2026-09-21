"""SRM-04A: model-spec §7.14.16.2 and binding P01/P02/P15/P16."""

from dataclasses import replace
from importlib.metadata import PackageNotFoundError, version

import pytest

from requirements_quality_assessment.detectors import (
    ConditionContextBaselineDetector, ConditionContextDetector, PostposedConditionDetector,
)
from requirements_quality_assessment.detectors.postposed_condition import (
    PARSER_BLOCKED_CODE, RULE_ID, UNRESOLVED_CODE,
)
from requirements_quality_assessment.domain import (
    DetectionProcessingStatus, DetectionStatus, FeatureId, MorphFeature,
    ParsedRequirement, ParserDiagnostic, ParserDiagnosticCode, ParserMetadata,
    ParserOutcome, Requirement, SentenceAnnotation, TokenAnnotation,
)
from requirements_quality_assessment.parsing import SpaCyRequirementParser


P01 = "Система повинна зберегти запит, якщо сервіс не відповідає."
P02 = "Система повинна показати слово «якщо» у довідці."
P15 = "Система повинна зберегти запит якщо сервіс не відповідає."
P16 = "Система повинна зберегти запит і повідомити оператора, якщо сервіс не відповідає."
FIN = (MorphFeature("VerbForm", ("Fin",)),)
INF = (MorphFeature("VerbForm", ("Inf",)),)


class StubParser:
    def __init__(self, outcome):
        self.outcome = outcome
        self.calls = 0

    def parse(self, requirement):
        self.calls += 1
        return self.outcome


def fixture(text=P01):
    requirement = Requirement("R072", 12, text)
    rows = [
        ("Система", "NOUN", 1, "nsubj", ()),
        ("повинна", "ADJ", None, "ROOT", ()),
        ("зберегти", "VERB", 1, "xcomp", INF),
        ("запит", "NOUN", 2, "obj", ()),
        (",", "PUNCT", 8, "punct", ()),
        ("якщо", "SCONJ", 8, "mark", ()),
        ("сервіс", "NOUN", 8, "nsubj", ()),
        ("не", "PART", 8, "advmod", (MorphFeature("Polarity", ("Neg",)),)),
        ("відповідає", "VERB", 1, "advcl", FIN),
        (".", "PUNCT", 1, "punct", ()),
    ]
    if text == P16:
        rows = rows[:4] + [
            ("і", "CCONJ", 5, "cc", ()),
            ("повідомити", "VERB", 2, "conj", INF),
            ("оператора", "NOUN", 5, "obj", ()),
        ] + [(s, p, h + 3 if h == 8 else h, r, m) for s, p, h, r, m in rows[4:]]
    tokens = []
    cursor = 0
    for i, (surface, upos, head, relation, morph) in enumerate(rows):
        # Preserve source case and all Unicode whitespace in parameterized P01.
        start = text.casefold().index(surface.casefold(), cursor)
        end = start + len(surface)
        tokens.append(TokenAnnotation(i, 0, text[start:end], start, end,
                                      surface.casefold(), upos, morph, head, relation))
        cursor = end
    parsed = ParsedRequirement(requirement.id, text, (SentenceAnnotation(0, 0, len(text)),),
                               tuple(tokens), ParserMetadata("fixture", "1", "uk", "1", "uk"))
    return requirement, parsed


def scan(requirement, parsed, *, composed=False, diagnostics=()):
    parser = StubParser(ParserOutcome(parsed, diagnostics))
    cls = ConditionContextDetector if composed else PostposedConditionDetector
    outcome, evidence = cls(parser=parser).detect(requirement)
    assert parser.calls == 1
    for source in evidence:
        assert requirement.text[source.start_offset:source.end_offset] == source.text
        assert source.requirement_id == requirement.id
        assert source.feature_id is FeatureId.CONDITION_CONTEXT
    for diagnostic in outcome.diagnostics:
        span = diagnostic.candidate_span
        assert requirement.text[span.start_offset:span.end_offset] == span.text
    return outcome, evidence


def assert_unresolved(outcome, evidence, code=UNRESOLVED_CODE):
    assert evidence == outcome.observations == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [(d.rule_id, d.code) for d in outcome.diagnostics] == [(RULE_ID, code)]


@pytest.mark.parametrize("composed", [False, True])
def test_p01_exact_evidence_and_ownership(composed):
    requirement, parsed = fixture()
    outcome, evidence = scan(requirement, parsed, composed=composed)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert len(evidence) == 1
    source = evidence[0]
    assert (source.evidence_id, source.rule_id, source.start_offset, source.end_offset,
            source.text) == ("COND-UK-002:E001", RULE_ID, 32, 57, "якщо сервіс не відповідає")
    assert outcome.observations[0].evidence_refs == (source.evidence_id,)
    assert PostposedConditionDetector(StubParser(ParserOutcome(parsed, ()))).detect(requirement) == (
        outcome, evidence)


@pytest.mark.parametrize("text", [P02, P15, P01.replace("якщо", "якщось"),
                                  P01.replace("якщо", "коли"),
                                  "Система повинна показати «текст, якщо сервіс не відповідає»."])
def test_no_source_candidate_is_complete_without_parser(text):
    parser = StubParser(None)
    outcome, evidence = PostposedConditionDetector(parser).detect(Requirement("R", 1, text))
    assert parser.calls == 0
    assert evidence == outcome.observations == outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_p15_falls_through_to_unchanged_baseline():
    requirement = Requirement("R", 1, P15)
    assert ConditionContextDetector(StubParser(None)).detect(requirement) == (
        ConditionContextBaselineDetector().detect(requirement))


def test_p16_multiple_results_are_unresolved_and_owned():
    requirement, parsed = fixture(P16)
    outcome, evidence = scan(requirement, parsed, composed=True)
    assert_unresolved(outcome, evidence)
    span = outcome.diagnostics[0].candidate_span
    assert (span.start_offset, span.end_offset, span.text) == (
        55, 80, "якщо сервіс не відповідає")


def test_neutral_ud_root_label_is_accepted():
    requirement, parsed = fixture()
    tokens = tuple(replace(t, dependency_relation="root") if t.token_id == 1 else t
                   for t in parsed.tokens)
    outcome, evidence = scan(requirement, replace(parsed, tokens=tokens))
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert len(evidence) == 1


@pytest.mark.parametrize(("index", "changes"), [
    (5, {"dependency_relation": "advmod"}),
    (5, {"head_token_id": 2}),
    (8, {"dependency_relation": "ccomp"}),
    (8, {"head_token_id": 2}),  # connected infinitive is not the chain head
    (8, {"upos": "ADJ", "morphology": ()}),  # zero-copula/adjectival
    (8, {"morphology": INF}),
    (2, {"morphology": FIN}),
    (2, {"dependency_relation": "obj"}),
    (0, {"dependency_relation": "obj"}),
    (3, {"dependency_relation": "nsubj", "head_token_id": 1}),
    (3, {"head_token_id": 8}),  # condition descendant outside suffix
    (6, {"head_token_id": 1}),  # suffix is not fully projected
    (6, {"dependency_relation": "conj"}),
    (6, {"upos": "VERB", "morphology": FIN}),
    (6, {"dependency_relation": "advcl"}),
    (1, {"morphology": (MorphFeature("Polarity", ("Neg",)),)}),
])
def test_exact_graph_and_scope_failures_are_unresolved(index, changes):
    requirement, parsed = fixture()
    tokens = list(parsed.tokens)
    tokens[index] = replace(tokens[index], **changes)
    outcome, evidence = scan(requirement, replace(parsed, tokens=tuple(tokens)))
    assert_unresolved(outcome, evidence)


@pytest.mark.parametrize(("index", "changes"), [
    (5, {"dependency_relation": None}), (5, {"head_token_id": None}),
    (8, {"upos": None}), (8, {"morphology": ()}),
    (2, {"morphology": ()}), (0, {"lemma": None}),
])
def test_missing_required_annotations_are_blocked(index, changes):
    requirement, parsed = fixture()
    tokens = list(parsed.tokens)
    tokens[index] = replace(tokens[index], **changes)
    outcome, evidence = scan(requirement, replace(parsed, tokens=tuple(tokens)), composed=True)
    assert_unresolved(outcome, evidence, PARSER_BLOCKED_CODE)


@pytest.mark.parametrize("code", list(ParserDiagnosticCode))
def test_parser_diagnostics_block_only_owned_candidate(code):
    requirement, parsed = fixture()
    outcome, evidence = scan(requirement, None, composed=True,
                             diagnostics=(ParserDiagnostic(code, "fixture failure"),))
    assert_unresolved(outcome, evidence, PARSER_BLOCKED_CODE)
    assert outcome.diagnostics[0].candidate_span.text == P01[32:57]


@pytest.mark.parametrize("text", [P01.upper(), P01.replace(", ", ",\u2003\t"),
                                  P01.replace("Система", "Си\u0301стема")])
def test_original_source_case_whitespace_and_unicode_offsets(text):
    # The accent fixture changes a prefix token without normalizing source text.
    if "\u0301" in text:
        requirement, parsed = fixture()
        tokens = tuple(replace(t, text=text[:8], end_offset=t.end_offset + 1)
                       if t.token_id == 0 else replace(
                           t, start_offset=t.start_offset + 1, end_offset=t.end_offset + 1)
                       for t in parsed.tokens)
        requirement = replace(requirement, text=text)
        parsed = replace(parsed, text=text, tokens=tokens,
                         sentences=(SentenceAnnotation(0, 0, len(text)),))
    else:
        requirement, parsed = fixture(text)
    outcome, evidence = scan(requirement, parsed)
    assert outcome.status is DetectionStatus.DETECTED
    assert evidence[0].start_offset == text.casefold().index("якщо")
    assert evidence[0].text == text[evidence[0].start_offset:-1]


def joined_fixture(second_text=P01, separator="; "):
    first, parsed_first = fixture()
    second, parsed_second = fixture(second_text)
    text = first.text[:-1] + separator + second.text
    shift = len(first.text[:-1] + separator)
    first_tokens = parsed_first.tokens[:-1]
    base = len(first_tokens)
    second_tokens = tuple(replace(t, token_id=t.token_id + base,
                                  head_token_id=None if t.head_token_id is None else t.head_token_id + base,
                                  start_offset=t.start_offset + shift,
                                  end_offset=t.end_offset + shift)
                          for t in parsed_second.tokens)
    requirement = replace(first, text=text)
    parsed = replace(parsed_first, text=text, tokens=first_tokens + second_tokens,
                     sentences=(SentenceAnnotation(0, 0, len(text)),))
    return requirement, parsed


def test_distinct_segments_use_independent_source_ordered_ids():
    requirement, parsed = joined_fixture()
    # Segment recognition uses absolute offsets without requiring a token for
    # the semicolon excluded from both source intervals.
    outcome, evidence = scan(requirement, parsed, composed=True)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert [e.evidence_id for e in evidence] == ["COND-UK-002:E001", "COND-UK-002:E002"]
    assert evidence[0].text == evidence[1].text
    assert evidence[0].start_offset < evidence[1].start_offset


def test_accepted_and_unresolved_segments_preserve_detection_state():
    requirement, parsed = joined_fixture(P16)
    outcome, evidence = scan(requirement, parsed, composed=True)
    assert len(evidence) == 1
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert [d.code for d in outcome.diagnostics] == [UNRESOLVED_CODE]


def test_multiple_markers_within_one_segment_are_not_accepted():
    requirement, parsed = joined_fixture(separator=", ")
    boundary = len(P01) - 1
    separator = TokenAnnotation(9, 0, ",", boundary, boundary + 1,
                                ",", "PUNCT", (), 8, "punct")
    second_tokens = tuple(replace(t, token_id=t.token_id + 1,
                                  head_token_id=None if t.head_token_id is None else t.head_token_id + 1)
                          for t in parsed.tokens[9:])
    parsed = replace(parsed, tokens=parsed.tokens[:9] + (separator,) + second_tokens)
    # Both comma-shaped candidates are owned; neither is a simple binary clause.
    outcome, evidence = scan(requirement, parsed, composed=True)
    assert evidence == outcome.observations == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert [(d.rule_id, d.code) for d in outcome.diagnostics] == [(RULE_ID, UNRESOLVED_CODE)] * 2


def test_heads_cannot_cross_semicolon_segments():
    requirement, parsed = joined_fixture()
    tokens = list(parsed.tokens)
    # The second condition points to the first result, in the same sentence.
    tokens[17] = replace(tokens[17], head_token_id=1)
    outcome, evidence = scan(requirement, replace(parsed, tokens=tuple(tokens)), composed=True)
    assert len(evidence) == 1
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert [d.code for d in outcome.diagnostics] == [UNRESOLVED_CODE]


def test_missing_suffix_token_blocks_instead_of_inventing_projection():
    requirement, parsed = fixture()
    parsed = replace(parsed, tokens=tuple(t for t in parsed.tokens if t.text != "не"))
    outcome, evidence = scan(requirement, parsed)
    assert_unresolved(outcome, evidence, PARSER_BLOCKED_CODE)


def test_incomplete_parser_outcome_with_retained_annotations_is_blocked():
    requirement, parsed = fixture()
    outcome, evidence = scan(requirement, parsed, diagnostics=(ParserDiagnostic(
        ParserDiagnosticCode.ANNOTATION_INCOMPLETE, "required annotation is missing"),))
    assert_unresolved(outcome, evidence, PARSER_BLOCKED_CODE)


def test_missing_sentence_annotations_cannot_be_replaced_by_source_punctuation():
    requirement, parsed = fixture()
    outcome, evidence = scan(requirement, replace(parsed, sentences=(), tokens=()))
    assert_unresolved(outcome, evidence, PARSER_BLOCKED_CODE)


def test_incomplete_annotations_keep_an_independent_accepted_segment():
    requirement, parsed = joined_fixture()
    tokens = list(parsed.tokens)
    tokens[17] = replace(tokens[17], morphology=())
    outcome, evidence = scan(requirement, replace(parsed, tokens=tuple(tokens)), composed=True)
    assert len(evidence) == 1
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert [d.code for d in outcome.diagnostics] == [PARSER_BLOCKED_CODE]


def test_ownership_preserves_other_markers_and_independent_baseline_evidence():
    requirement, parsed = fixture()
    tail = " Система повинна діяти у разі збою; система повідомляє при перевірці."
    text = requirement.text + tail
    requirement = replace(requirement, text=text)
    parsed = replace(parsed, text=text)
    outcome, evidence = scan(requirement, parsed, composed=True)
    assert [(e.rule_id, e.text) for e in evidence] == [
        (RULE_ID, "якщо сервіс не відповідає"), ("COND-UK-001", "у разі збою"),
    ]
    assert [(d.rule_id, d.candidate_span.text) for d in outcome.diagnostics] == [
        ("COND-UK-001", "при перевірці"),
    ]
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED


@pytest.mark.parametrize("text", [
    "Якщо сервіс недоступний, система повинна зберегти запит.",
    "Система повинна діяти у разі збою.",
    "Під час перевірки система повинна діяти.",
    "Система повинна діяти при навантаженні.",
])
def test_existing_templates_do_not_invoke_extension_parser(text):
    requirement = Requirement("R", 1, text)
    parser = StubParser(None)
    assert ConditionContextDetector(parser).detect(requirement) == (
        ConditionContextBaselineDetector().detect(requirement))
    assert parser.calls == 0


@pytest.fixture(scope="module")
def pinned_p01():
    required_versions = {
        "spacy": "3.8.16",
        "uk-core-news-sm": "3.8.0",
    }
    installed_versions = {}
    for distribution, required_version in required_versions.items():
        try:
            installed_versions[distribution] = version(distribution)
        except PackageNotFoundError:
            pytest.fail(
                f"Mandatory pinned backend is unavailable: {distribution} "
                f"{required_version} is not installed.",
                pytrace=False,
            )
    assert installed_versions == required_versions, (
        "Mandatory pinned backend version mismatch: "
        f"required {required_versions}, installed {installed_versions}."
    )

    requirement = Requirement("R072", 12, P01)
    outcome = SpaCyRequirementParser().parse(requirement)
    if outcome.diagnostics:
        details = "; ".join(
            f"{diagnostic.code.value}: {diagnostic.explanation}"
            for diagnostic in outcome.diagnostics
        )
        pytest.fail(
            f"Mandatory pinned backend could not execute P01: {details}",
            pytrace=False,
        )
    parsed = outcome.parsed_requirement
    assert parsed is not None, "Mandatory pinned backend returned no P01 parse."
    assert (parsed.parser.library_version, parsed.parser.model_version) == ("3.8.16", "3.8.0")
    return requirement, parsed


def test_pinned_p01_graph_and_delimiter_projection(pinned_p01):
    requirement, parsed = pinned_p01
    tokens = {t.text: t for t in parsed.tokens}
    for source, relation, target in [
        ("якщо", "mark", "відповідає"), ("відповідає", "advcl", "повинна"),
        ("зберегти", "xcomp", "повинна"), ("Система", "nsubj", "повинна"),
        (",", "punct", "відповідає"),
    ]:
        assert tokens[source].dependency_relation == relation
        assert tokens[source].head_token_id == tokens[target].token_id
    assert MorphFeature("VerbForm", ("Fin",)) in tokens["відповідає"].morphology
    assert MorphFeature("VerbForm", ("Inf",)) in tokens["зберегти"].morphology
    outcome, evidence = scan(requirement, parsed, composed=True)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.diagnostics == ()
    assert [(e.start_offset, e.end_offset) for e in evidence] == [(32, 57)]


@pytest.mark.parametrize("change", ["missing_mark", "missing_finite", "changed_advcl"])
def test_pinned_p01_missing_or_changed_annotation_is_never_repaired(pinned_p01, change):
    requirement, parsed = pinned_p01
    tokens = list(parsed.tokens)
    target = next(t for t in tokens if t.text == ("якщо" if change == "missing_mark" else "відповідає"))
    if change == "missing_mark":
        updated = replace(target, dependency_relation=None)
    elif change == "missing_finite":
        updated = replace(target, morphology=tuple(f for f in target.morphology if f.name != "VerbForm"))
    else:
        updated = replace(target, dependency_relation="ccomp")
    tokens[target.token_id] = updated
    outcome, evidence = scan(requirement, replace(parsed, tokens=tuple(tokens)), composed=True)
    assert_unresolved(outcome, evidence,
                      UNRESOLVED_CODE if change == "changed_advcl" else PARSER_BLOCKED_CODE)


@pytest.fixture(scope="module")
def pinned_extractor(pinned_p01):
    from requirements_quality_assessment.extractor import BaselineFeatureExtractor

    return BaselineFeatureExtractor()


@pytest.mark.parametrize("text", [P01, P16, P01.replace("не відповідає", "недоступний")])
def test_production_adds_only_condition_rule_and_preserves_result_contract(pinned_extractor, text):
    from requirements_quality_assessment.detectors import ExpectedResultBaselineDetector

    requirement = Requirement("R072", 12, text)
    result = pinned_extractor.extract(requirement)
    expected, expected_evidence = ExpectedResultBaselineDetector().detect(requirement)
    assert result.features.expected_results == expected
    assert tuple(e for e in result.evidence if e.feature_id is FeatureId.EXPECTED_RESULT) == expected_evidence
    assert not any(e.rule_id in {"RESULT-UK-002", "ACCEPT-UK-001"} for e in result.evidence)
    condition = result.features.condition_contexts
    if text == P01:
        assert condition.processing_status is DetectionProcessingStatus.COMPLETE
        assert condition.observations[0].evidence_refs == ("COND-UK-002:E001",)
    else:
        assert condition.status is DetectionStatus.UNRESOLVED
        assert [d.code for d in condition.diagnostics] == [UNRESOLVED_CODE]


@pytest.mark.parametrize(("text", "family", "expected_spans", "status"), [
    ("Якщо сервіс недоступний, система повинна зберегти запит.",
     "condition_contexts", [("COND-UK-001", 0, 23)], DetectionStatus.DETECTED),
    ("Якщо сервіс недоступний, система повинна зберегти запит.",
     "expected_results", [("RESULT-UK-001", 25, 55)], DetectionStatus.DETECTED),
    ("Система повинна відповісти не більше ніж за 2 с.",
     "acceptance_criteria", [("ACCEPT-QUANT-001", 0, 47)], DetectionStatus.DETECTED),
    ("Виконання перевіряється навантажувальним тестом.",
     "verification_methods", [("VERIFY-UK-001", 24, 47)], DetectionStatus.DETECTED),
    ("Система контролює обробку запитів.", "expected_results", [], DetectionStatus.UNRESOLVED),
])
def test_pinned_mvp_regression_anchors(pinned_extractor, text, family, expected_spans, status):
    result = pinned_extractor.extract(Requirement("R072", 12, text))
    outcome = getattr(result.features, family)
    assert outcome.status is status
    assert [(e.rule_id, e.start_offset, e.end_offset) for e in result.evidence
            if e.feature_id is outcome.feature_id] == expected_spans

"""SRM-04B / model-spec §7.14.16.3, .5 and .7 acceptance gate."""

from dataclasses import replace
from importlib.metadata import PackageNotFoundError, version
import re

import pytest

from requirements_quality_assessment.detectors import (
    CoordinatedExpectedResultDetector, ExpectedResultBaselineDetector, ExpectedResultDetector,
)
from requirements_quality_assessment.detectors.coordinated_result import (
    PARSER_BLOCKED_CODE, RULE_ID, UNRESOLVED_CODE,
)
from requirements_quality_assessment.domain import (
    DetectionProcessingStatus, DetectionStatus, FeatureId, MorphFeature, ParsedRequirement,
    ParserDiagnostic, ParserDiagnosticCode, ParserMetadata, ParserOutcome, Requirement,
    SentenceAnnotation, TokenAnnotation,
)
from requirements_quality_assessment.parsing import SpaCyRequirementParser


P03 = "Система повинна зберегти запит і повідомити оператора."
P04 = "Система повинна показати напис «зберегти і повідомити»."
P17 = "Система повинна зберегти запит і не повідомляти оператора."
P18 = "Система повинна зберегти запит або повідомити оператора."
P01 = "Система повинна зберегти запит, якщо сервіс не відповідає."
P16 = "Система повинна зберегти запит і повідомити оператора, якщо сервіс не відповідає."
INF = (MorphFeature("VerbForm", ("Inf",)),)
FIN = (MorphFeature("VerbForm", ("Fin",)),)


class StubParser:
    def __init__(self, parsed, diagnostics=()):
        self.outcome = ParserOutcome(parsed, diagnostics)
        self.calls = 0

    def parse(self, requirement):
        self.calls += 1
        return self.outcome


def fixture(text=P03):
    # Fixed parser-neutral graph; source variants only change exact offsets.
    requirement = Requirement("R072", 12, text)
    matches = tuple(re.finditer(r"\w+|[^\w\s]", text))
    specs = [("NOUN", 1, "nsubj", ()), ("ADJ", None, "ROOT", ()),
             ("VERB", 1, "xcomp", INF), ("NOUN", 2, "obj", ()),
             ("CCONJ", 5, "cc", ()), ("VERB", 2, "conj", INF),
             ("NOUN", 5, "obj", ()), ("PUNCT", 1, "punct", ())]
    assert len(matches) == len(specs)
    tokens = tuple(TokenAnnotation(i, 0, m.group(), m.start(), m.end(),
                                   m.group().casefold(), upos, morph, head, dep)
                   for i, (m, (upos, head, dep, morph)) in enumerate(zip(matches, specs)))
    parsed = ParsedRequirement(requirement.id, text, (SentenceAnnotation(0, 0, len(text)),),
                               tokens, ParserMetadata("fixture", "1", "fixture", "1", "uk"))
    return requirement, parsed


def scan(requirement, parsed, *, composed=True, diagnostics=()):
    parser = StubParser(parsed, diagnostics)
    cls = ExpectedResultDetector if composed else CoordinatedExpectedResultDetector
    result = cls(parser).detect(requirement)
    assert parser.calls == 1
    outcome, evidence = result
    assert len({e.evidence_id for e in evidence}) == len(evidence)
    assert len({(e.rule_id, e.start_offset, e.end_offset) for e in evidence}) == len(evidence)
    assert all(e.text == requirement.text[e.start_offset:e.end_offset] for e in evidence)
    by_id = {e.evidence_id: e for e in evidence}
    for observation in outcome.observations:
        sources = [by_id[ref] for ref in observation.evidence_refs]
        assert sources == sorted(sources, key=lambda e: (e.start_offset, e.end_offset, e.evidence_id))
        assert all(e.feature_id is FeatureId.EXPECTED_RESULT for e in sources)
    return result


def assert_unresolved(outcome, evidence, code=UNRESOLVED_CODE):
    assert evidence == outcome.observations == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [(d.rule_id, d.code) for d in outcome.diagnostics] == [(RULE_ID, code)]


def assert_p03(outcome, evidence):
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert [(e.evidence_id, e.start_offset, e.end_offset, e.text) for e in evidence] == [
        (f"{RULE_ID}:E001", 0, 15, "Система повинна"),
        (f"{RULE_ID}:E002", 0, 30, "Система повинна зберегти запит"),
        (f"{RULE_ID}:E003", 33, 53, "повідомити оператора"),
    ]
    assert [o.evidence_refs for o in outcome.observations] == [
        (f"{RULE_ID}:E002",), (f"{RULE_ID}:E001", f"{RULE_ID}:E003"),
    ]


def test_p03_exact_evidence_and_two_observations():
    requirement, parsed = fixture()
    assert_p03(*scan(requirement, parsed))
    assert scan(requirement, parsed) == scan(requirement, parsed)


@pytest.mark.parametrize("normative", ["повинен", "повинна", "повинні", "має", "мають"])
def test_only_approved_normative_surfaces(normative):
    requirement, parsed = fixture(P03.replace("повинна", normative))
    outcome, evidence = scan(requirement, parsed)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert len(evidence) == 3


@pytest.mark.parametrize(("index", "changes"), [
    (5, {"head_token_id": 1}), (4, {"head_token_id": 2}),
    (5, {"dependency_relation": "xcomp"}), (4, {"dependency_relation": "advmod"}),
    (2, {"dependency_relation": "obj"}), (2, {"head_token_id": 0}),
    (0, {"head_token_id": 5}), (0, {"dependency_relation": "obj"}),
    (0, {"dependency_relation": "nsubj:pass"}),
    (3, {"dependency_relation": "nsubj", "head_token_id": 1}),
    (6, {"dependency_relation": "nsubj", "head_token_id": 5}),
    (2, {"morphology": FIN}), (5, {"morphology": FIN}),
    (5, {"morphology": (MorphFeature("VerbForm", ("Part",)),)}),
    (2, {"morphology": INF + (MorphFeature("Voice", ("Pass",)),)}),
    (3, {"dependency_relation": "neg"}),
    (3, {"morphology": (MorphFeature("Polarity", ("Neg",)),)}),
    (3, {"dependency_relation": "orphan"}), (3, {"dependency_relation": "conj"}),
    (3, {"dependency_relation": "cc"}), (3, {"upos": "CCONJ"}),
    (3, {"upos": "VERB", "morphology": INF}),
    (3, {"upos": "ADJ", "morphology": (MorphFeature("VerbForm", ("Part",)),)}),
])
def test_changed_graph_and_exclusions_are_unresolved(index, changes):
    requirement, parsed = fixture()
    tokens = list(parsed.tokens)
    tokens[index] = replace(tokens[index], **changes)
    outcome, evidence = scan(requirement, replace(parsed, tokens=tuple(tokens)))
    assert_unresolved(outcome, evidence)
    assert outcome.diagnostics[0].candidate_span.text == P03[:-1]


@pytest.mark.parametrize(("index", "changes"), [
    (5, {"dependency_relation": None}), (4, {"dependency_relation": None}),
    (5, {"head_token_id": None}), (4, {"head_token_id": None}),
    (0, {"head_token_id": None}), (0, {"dependency_relation": None}),
    (2, {"head_token_id": None}), (2, {"dependency_relation": None}),
    (2, {"morphology": ()}), (5, {"morphology": ()}),
    (2, {"upos": None}), (5, {"upos": None}), (0, {"lemma": None}),
])
def test_p14_missing_annotations_are_blocked(index, changes):
    requirement, parsed = fixture()
    tokens = list(parsed.tokens)
    tokens[index] = replace(tokens[index], **changes)
    outcome, evidence = scan(requirement, replace(parsed, tokens=tuple(tokens)))
    assert_unresolved(outcome, evidence, PARSER_BLOCKED_CODE)
    span = outcome.diagnostics[0].candidate_span
    assert (span.start_offset, span.end_offset, span.text) == (0, 53, P03[:-1])


@pytest.mark.parametrize("code", list(ParserDiagnosticCode))
def test_parser_failure_is_blocked_without_inventing_a_sentence_boundary(code):
    requirement, _ = fixture()
    outcome, evidence = scan(requirement, None, diagnostics=(ParserDiagnostic(code, "fixture"),))
    assert_unresolved(outcome, evidence, PARSER_BLOCKED_CODE)
    assert outcome.diagnostics[0].candidate_span is None


def test_retained_incomplete_parse_keeps_known_candidate_span():
    requirement, parsed = fixture()
    outcome, evidence = scan(requirement, parsed, diagnostics=(ParserDiagnostic(
        ParserDiagnosticCode.ANNOTATION_INCOMPLETE, "fixture"),))
    assert_unresolved(outcome, evidence, PARSER_BLOCKED_CODE)
    assert outcome.diagnostics[0].candidate_span.text == P03[:-1]


def test_missing_sentence_annotations_are_blocked():
    requirement, parsed = fixture()
    assert_unresolved(*scan(requirement, replace(parsed, sentences=(), tokens=())), PARSER_BLOCKED_CODE)


def test_noncontiguous_token_coverage_is_blocked():
    requirement, parsed = fixture()
    # Keep IDs/heads valid while leaving original object text unannotated.
    parsed = replace(parsed, tokens=tuple(t for t in parsed.tokens if t.token_id != 3))
    assert_unresolved(*scan(requirement, parsed), PARSER_BLOCKED_CODE)


@pytest.mark.parametrize("field", ["requirement_id", "text"])
def test_invalid_parser_identity_has_one_extension_blocking_diagnostic(field):
    requirement, parsed = fixture()
    parsed = replace(parsed, **{field: "other" if field == "requirement_id" else parsed.text + " "})
    assert_unresolved(*scan(requirement, parsed), PARSER_BLOCKED_CODE)


def test_missing_source_coordinator_annotation_is_blocked():
    requirement, parsed = fixture()
    parsed = replace(parsed, tokens=tuple(t for t in parsed.tokens if t.token_id != 4))
    assert_unresolved(*scan(requirement, parsed), PARSER_BLOCKED_CODE)


@pytest.mark.parametrize("relation", ["xcomp", "ccomp", "aux", "cop"])
def test_approved_normative_chain_relations(relation):
    requirement, parsed = fixture()
    tokens = tuple(replace(t, dependency_relation=relation) if t.token_id == 2 else t
                   for t in parsed.tokens)
    assert_p03(*scan(requirement, replace(parsed, tokens=tokens)))


def test_normative_chain_can_have_lexical_root_without_repair():
    requirement, parsed = fixture()
    tokens = list(parsed.tokens)
    tokens[0] = replace(tokens[0], head_token_id=2)
    tokens[1] = replace(tokens[1], head_token_id=2, dependency_relation="aux")
    tokens[2] = replace(tokens[2], head_token_id=None, dependency_relation="root")
    assert_p03(*scan(requirement, replace(parsed, tokens=tuple(tokens))))


def test_unapproved_normative_surface_falls_through():
    requirement, parsed = fixture(P03.replace("повинна", "мусить"))
    outcome, evidence = scan(requirement, parsed, composed=False)
    assert evidence == outcome.observations == outcome.diagnostics == ()
    assert scan(requirement, parsed) == ExpectedResultBaselineDetector(StubParser(parsed)).detect(requirement)


@pytest.mark.parametrize("incomplete_lemma", [False, True])
def test_noun_coordination_is_not_claimed_by_binary_verb_dispatch(incomplete_lemma):
    requirement, parsed = fixture(P03.replace("повідомити оператора", "відповідь сервера"))
    tokens = list(parsed.tokens)
    tokens[5] = replace(tokens[5], upos="NOUN", morphology=(), head_token_id=3)
    if incomplete_lemma:
        tokens[3] = replace(tokens[3], lemma=None)
    parsed = replace(parsed, tokens=tuple(tokens))
    outcome, evidence = scan(requirement, parsed, composed=False)
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert evidence == outcome.diagnostics == ()
    assert scan(requirement, parsed) == ExpectedResultBaselineDetector(StubParser(parsed)).detect(requirement)


@pytest.mark.parametrize("text", [P03.replace(" і ", " та "), P03.replace(" ", "\u2003\t"),
                                  P03.replace("Система", "СИСТЕМА"),
                                  P03.replace("Система", "Система😀")])
def test_source_offsets_and_order(text):
    if "😀" in text:
        requirement, parsed = fixture()
        text = P03.replace("Система", "Систем😀")
        requirement = replace(requirement, text=text)
        parsed = replace(parsed, text=text, tokens=(replace(parsed.tokens[0], text=text[:7]),)
                         + parsed.tokens[1:])
    else:
        requirement, parsed = fixture(text)
    outcome, evidence = scan(requirement, parsed)
    assert len(evidence) == 3
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert len(outcome.observations) == 2


def joined_fixture(separator="; ", baseline_first=False):
    requirement, first = fixture()
    _, second = fixture()
    if baseline_first:
        first_text = "Система повинна зберегти запит"
        first_tokens = first.tokens[:4]
    else:
        first_text = P03[:-1]
        first_tokens = first.tokens[:-1]
    shift = len(first_text + separator)
    base = len(first_tokens)
    sentence_id = 1 if separator == ". " else 0
    second_tokens = tuple(replace(t, token_id=t.token_id + base, sentence_id=sentence_id,
                                  head_token_id=None if t.head_token_id is None else t.head_token_id + base,
                                  start_offset=t.start_offset + shift, end_offset=t.end_offset + shift)
                          for t in second.tokens)
    text = first_text + separator + P03
    sentences = ((SentenceAnnotation(0, 0, len(text)),) if not sentence_id else
                 (SentenceAnnotation(0, 0, shift - 1), SentenceAnnotation(1, shift, len(text))))
    return replace(requirement, text=text), replace(first, text=text, sentences=sentences,
                                                   tokens=first_tokens + second_tokens)


@pytest.mark.parametrize("separator", ["; ", ". "])
def test_independent_segments_and_deterministic_ids(separator):
    requirement, parsed = joined_fixture(separator)
    outcome, evidence = scan(requirement, parsed)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert len(outcome.observations) == 4
    assert [e.evidence_id for e in evidence] == [f"{RULE_ID}:E{i:03d}" for i in range(1, 7)]
    assert [o.evidence_refs[-1] for o in outcome.observations] == [
        f"{RULE_ID}:E002", f"{RULE_ID}:E003", f"{RULE_ID}:E005", f"{RULE_ID}:E006"]


@pytest.mark.parametrize("blocked", [False, True])
@pytest.mark.parametrize("baseline_first", [False, True])
def test_accepted_plus_unresolved_or_blocked_preserves_independent_results(blocked, baseline_first):
    requirement, parsed = joined_fixture(baseline_first=baseline_first)
    tokens = list(parsed.tokens)
    tokens[-3] = replace(tokens[-3], dependency_relation=None if blocked else "xcomp")
    outcome, evidence = scan(requirement, replace(parsed, tokens=tuple(tokens)))
    assert len(evidence) == (1 if baseline_first else 3)
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert [d.code for d in outcome.diagnostics] == [PARSER_BLOCKED_CODE if blocked else UNRESOLVED_CODE]


def test_baseline_and_extension_merge_in_predicate_source_order():
    requirement, parsed = joined_fixture(baseline_first=True)
    outcome, evidence = scan(requirement, parsed)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert [o.evidence_refs for o in outcome.observations] == [
        ("RESULT-UK-001:E001",), (f"{RULE_ID}:E002",), (f"{RULE_ID}:E001", f"{RULE_ID}:E003")]
    assert len(evidence) == 4


def test_head_cannot_cross_semicolon_segment():
    requirement, parsed = joined_fixture()
    tokens = list(parsed.tokens)
    tokens[-3] = replace(tokens[-3], head_token_id=2)
    outcome, evidence = scan(requirement, replace(parsed, tokens=tuple(tokens)))
    assert len(evidence) == 3
    assert outcome.status is DetectionStatus.DETECTED
    assert [d.code for d in outcome.diagnostics] == [UNRESOLVED_CODE]


@pytest.fixture(scope="module")
def pinned_parser():
    required = {"spacy": "3.8.16", "uk-core-news-sm": "3.8.0"}
    for distribution, expected in required.items():
        try:
            actual = version(distribution)
        except PackageNotFoundError:
            pytest.fail(f"Mandatory pinned backend unavailable: {distribution}=={expected}", pytrace=False)
        assert actual == expected, f"Mandatory pinned backend mismatch: {distribution}=={actual}; need {expected}"
    return SpaCyRequirementParser()


def pinned_parse(parser, text):
    requirement = Requirement("R072", 12, text)
    outcome = parser.parse(requirement)
    assert not outcome.diagnostics, f"Mandatory pinned backend failed: {outcome.diagnostics}"
    assert outcome.parsed_requirement is not None
    parsed = outcome.parsed_requirement
    assert (parsed.parser.library_version, parsed.parser.model_version) == ("3.8.16", "3.8.0")
    return requirement, parsed


@pytest.fixture(scope="module")
def pinned_p03(pinned_parser):
    return pinned_parse(pinned_parser, P03)


@pytest.mark.parametrize("coordinator", ["і", "та"])
def test_pinned_p03_exact_graph_and_evidence(pinned_parser, coordinator):
    requirement, parsed = pinned_parse(pinned_parser, P03.replace(" і ", f" {coordinator} "))
    tokens = {t.text: t for t in parsed.tokens}
    for source, relation, head in [
        ("Система", "nsubj", "повинна"), ("зберегти", "xcomp", "повинна"),
        ("повідомити", "conj", "зберегти"), (coordinator, "cc", "повідомити"),
    ]:
        assert tokens[source].dependency_relation == relation
        assert tokens[source].head_token_id == tokens[head].token_id
    for word in ["зберегти", "повідомити"]:
        assert tokens[word].upos == "VERB"
        assert INF[0] in tokens[word].morphology
    outcome, evidence = scan(requirement, parsed)
    if coordinator == "і":
        assert_p03(outcome, evidence)
    else:
        assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
        assert [(e.start_offset, e.end_offset) for e in evidence] == [(0, 15), (0, 30), (34, 54)]


@pytest.mark.parametrize(("word", "changes", "code"), [
    ("і", {"dependency_relation": None}, PARSER_BLOCKED_CODE),
    ("і", {"head_token_id": None}, PARSER_BLOCKED_CODE),
    ("повідомити", {"dependency_relation": None}, PARSER_BLOCKED_CODE),
    ("повідомити", {"head_token_id": None}, PARSER_BLOCKED_CODE),
    ("зберегти", {"morphology": ()}, PARSER_BLOCKED_CODE),
    ("повідомити", {"morphology": ()}, PARSER_BLOCKED_CODE),
    ("повідомити", {"head_token_id": 1}, UNRESOLVED_CODE),
    ("і", {"head_token_id": 2}, UNRESOLVED_CODE),
    ("повідомити", {"dependency_relation": "xcomp"}, UNRESOLVED_CODE),
])
def test_pinned_p14_or_changed_annotation_is_never_repaired(pinned_p03, word, changes, code):
    requirement, parsed = pinned_p03
    tokens = tuple(replace(t, **changes) if t.text == word else t for t in parsed.tokens)
    outcome, evidence = scan(requirement, replace(parsed, tokens=tokens))
    assert_unresolved(outcome, evidence, code)
    assert outcome.diagnostics[0].candidate_span.text == P03[:-1]


@pytest.mark.parametrize("text", [P04, P18, P18.replace("або", "чи"),
                                  P18.replace("або", "але"),
                                  "Система повинна зберегти запит і відповідь."])
def test_pinned_completed_negatives_fall_through_unchanged(pinned_parser, text):
    requirement, parsed = pinned_parse(pinned_parser, text)
    outcome, evidence = scan(requirement, parsed, composed=False)
    assert evidence == outcome.observations == outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert scan(requirement, parsed) == ExpectedResultBaselineDetector(StubParser(parsed)).detect(requirement)


@pytest.mark.parametrize("text", [P17,
    "Система повинна зберегти запит і повідомити оператора та сформувати звіт.",
    P03.replace(" і ", " і та "),
    P03.replace(" і ", ", і "), P03.replace(" і ", ": і "),
    P03.replace(" і ", " — і "), P16,
    "Якщо сервіс недоступний, система повинна зберегти запит і повідомити оператора.",
])
def test_pinned_negation_arity_and_boundaries_are_unresolved(pinned_parser, text):
    requirement, parsed = pinned_parse(pinned_parser, text)
    outcome, evidence = scan(requirement, parsed)
    assert_unresolved(outcome, evidence)
    assert outcome.diagnostics[0].candidate_span.text == text[:-1]


def test_production_p03_integration(pinned_p03):
    from requirements_quality_assessment.extractor import BaselineFeatureExtractor

    requirement, _ = pinned_p03
    result = BaselineFeatureExtractor().extract(requirement)
    assert_p03(result.features.expected_results,
               tuple(e for e in result.evidence if e.feature_id is FeatureId.EXPECTED_RESULT))


@pytest.mark.parametrize("text", [P01, P16])
def test_pinned_srm04a_p01_p16_preserved(pinned_parser, text):
    from requirements_quality_assessment.extractor import BaselineFeatureExtractor

    pinned_parse(pinned_parser, text)
    result = BaselineFeatureExtractor().extract(Requirement("R072", 12, text))
    condition = result.features.condition_contexts
    if text == P01:
        assert condition.processing_status is DetectionProcessingStatus.COMPLETE
        assert condition.observations[0].evidence_refs == ("COND-UK-002:E001",)
    else:
        assert condition.processing_status is DetectionProcessingStatus.INCOMPLETE
        assert condition.status is DetectionStatus.UNRESOLVED
        assert [d.code for d in condition.diagnostics] == ["COND_POSTPOSED_YAKSHCHO_UNRESOLVED"]
        assert [d.code for d in result.features.expected_results.diagnostics] == [UNRESOLVED_CODE]


@pytest.mark.parametrize("text", [
    "Система повинна сформувати звіт.",
    "Якщо сервіс недоступний, система повинна зберегти запит.",
    "Система повинна відповісти не більше ніж за 2 с.",
    "Система повинна зберегти запит і повідомити оператора за 2 с.",
    "Виконання перевіряється навантажувальним тестом.",
    "Система контролює обробку запитів.",
    "Система повинна швидко зберегти запит.",
])
def test_pinned_unrelated_families_and_mvp_results_preserved(pinned_parser, text):
    from requirements_quality_assessment.extractor import BaselineFeatureExtractor

    requirement, _ = pinned_parse(pinned_parser, text)
    baseline = BaselineFeatureExtractor(expected_result_detector=ExpectedResultBaselineDetector(pinned_parser)).extract(requirement)
    result = BaselineFeatureExtractor().extract(requirement)
    for family in ["condition_contexts", "acceptance_criteria", "quantitative_constraints",
                   "verification_methods", "vague_term_occurrences"]:
        assert getattr(result.features, family) == getattr(baseline.features, family)
    assert tuple(e for e in result.evidence if e.feature_id is not FeatureId.EXPECTED_RESULT) == tuple(
        e for e in baseline.evidence if e.feature_id is not FeatureId.EXPECTED_RESULT)
    if " і " not in text:
        assert result.features.expected_results == baseline.features.expected_results

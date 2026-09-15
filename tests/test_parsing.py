"""Parser infrastructure contracts, independent of feature detectors and calculators."""

from dataclasses import fields, is_dataclass
import importlib.metadata
import inspect
from typing import get_type_hints

import pytest

from requirements_quality_assessment.domain.core import Requirement
from requirements_quality_assessment.domain.parser import (
    MorphFeature, ParsedRequirement, ParserDiagnosticCode, ParserOutcome,
)
from requirements_quality_assessment.parsing import RequirementParser, SpaCyRequirementParser


TEXT = "Система зберігає звіт! Далі вона надсилає повідомлення."


class FakeMorph:
    def __init__(self, values: dict[str, str]):
        self.values = values

    def to_dict(self) -> dict[str, str]:
        return self.values


class FakeToken:
    def __init__(self, index: int, text: str, offset: int, morphology: dict[str, str]):
        self.i = index
        self.text = text
        self.idx = offset
        self.lemma_ = text.lower()
        self.pos_ = "NOUN"
        self.dep_ = "dep"
        self.morph = FakeMorph(morphology)
        self.head = self


class FakeSentence:
    def __init__(self, text: str, start: int, tokens: list[FakeToken]):
        self.text = text
        self.start_char = start
        self.end_char = start + len(text)
        self.tokens = tokens

    def __iter__(self):
        return iter(self.tokens)


class FakeDoc:
    def __init__(self, text: str, sentences: list[FakeSentence]):
        self.text = text
        self.sents = sentences
        self.tokens = [token for sentence in sentences for token in sentence]

    def __iter__(self):
        return iter(self.tokens)


def fake_doc(text: str = TEXT) -> FakeDoc:
    first = "Система зберігає звіт!"
    second = "Далі вона надсилає повідомлення."
    words = ["Система", "зберігає", "звіт", "!", "Далі", "вона", "надсилає", "повідомлення", "."]
    tokens = []
    cursor = 0
    for index, word in enumerate(words):
        offset = text.index(word, cursor)
        tokens.append(FakeToken(index + 10, word, offset, {
            "Number": "Sing", "Case": "Nom,Acc" if index == 0 else "Nom",
        }))
        cursor = offset + len(word)
    tokens[0].dep_ = "ROOT"
    tokens[1].head = tokens[0]
    tokens[2].head = tokens[1]
    tokens[3].head = tokens[0]
    tokens[4].dep_ = "ROOT"
    for token in tokens[5:]:
        token.head = tokens[4]
    return FakeDoc(text, [
        FakeSentence(first, 0, tokens[:4]),
        FakeSentence(second, text.index(second), tokens[4:]),
    ])


def parser_for(doc: FakeDoc) -> SpaCyRequirementParser:
    return SpaCyRequirementParser(_loader=lambda: (lambda _text: doc, "3.8.16", "3.8.0"))


def _assert_source_contract(parsed: ParsedRequirement, requirement: Requirement) -> None:
    assert parsed.requirement_id == requirement.id
    assert parsed.text == requirement.text
    assert [s.sentence_id for s in parsed.sentences] == list(range(len(parsed.sentences)))
    assert [t.token_id for t in parsed.tokens] == list(range(len(parsed.tokens)))
    assert [s.start_offset for s in parsed.sentences] == sorted(
        s.start_offset for s in parsed.sentences
    )
    assert [t.start_offset for t in parsed.tokens] == sorted(t.start_offset for t in parsed.tokens)
    assert all(requirement.text[t.start_offset:t.end_offset] == t.text for t in parsed.tokens)
    assert all(0 <= s.start_offset < s.end_offset <= len(requirement.text)
               for s in parsed.sentences)
    assert all(requirement.text[s.start_offset:s.end_offset] for s in parsed.sentences)
    by_id = {token.token_id: token for token in parsed.tokens}
    assert all(t.head_token_id is None or by_id[t.head_token_id].sentence_id == t.sentence_id
               for t in parsed.tokens)


def _assert_domain_only(value: object) -> None:
    if isinstance(value, tuple):
        for item in value:
            _assert_domain_only(item)
    elif is_dataclass(value):
        assert type(value).__module__.startswith("requirements_quality_assessment.domain.")
        for field in fields(value):
            _assert_domain_only(getattr(value, field.name))
    else:
        assert isinstance(value, (str, int, type(None)))


def test_public_boundary_and_domain_only_conversion() -> None:
    requirement = Requirement("R007", 23, TEXT)
    outcome: ParserOutcome = parser_for(fake_doc()).parse(requirement)
    assert outcome.diagnostics == ()
    parsed = outcome.parsed_requirement
    assert parsed is not None
    _assert_source_contract(parsed, requirement)
    assert len(parsed.sentences) == 2
    assert [(s.start_offset, s.end_offset) for s in parsed.sentences] == [
        (0, len("Система зберігає звіт!")),
        (TEXT.index("Далі"), len(TEXT)),
    ]
    assert parsed.tokens[0].head_token_id is None
    assert parsed.tokens[1].head_token_id == 0  # provider ID 10 is not exposed
    assert parsed.tokens[4].head_token_id is None
    assert parsed.tokens[5].head_token_id == 4
    assert all(isinstance(t.lemma, (str, type(None)))
               and isinstance(t.upos, (str, type(None)))
               and isinstance(t.dependency_relation, (str, type(None)))
               for t in parsed.tokens)
    assert parsed.tokens[0].morphology == (
        MorphFeature("Case", ("Acc", "Nom")), MorphFeature("Number", ("Sing",)),
    )
    assert parsed.parser.provider_id == "spacy"
    assert (parsed.parser.library_version, parsed.parser.model_package,
            parsed.parser.model_version, parsed.parser.language) == (
        "3.8.16", "uk_core_news_sm", "3.8.0", "uk",
    )

    _assert_domain_only(outcome)
    assert get_type_hints(RequirementParser.parse) == {
        "requirement": Requirement, "return": ParserOutcome,
    }
    assert tuple(inspect.signature(RequirementParser.parse).parameters) == (
        "self", "requirement",
    )


def test_unavailable_backend_returns_approved_diagnostic() -> None:
    def missing():
        raise ImportError("no model")

    outcome = SpaCyRequirementParser(_loader=missing).parse(Requirement("R1", 1, TEXT))
    assert outcome.parsed_requirement is None
    assert [d.code for d in outcome.diagnostics] == [ParserDiagnosticCode.PARSER_UNAVAILABLE]
    assert "spaCy 3.8.16" in outcome.diagnostics[0].explanation
    assert "no model" not in outcome.diagnostics[0].explanation


def test_provider_processing_failure_returns_approved_diagnostic() -> None:
    def fail(_text: str):
        raise RuntimeError("provider detail")

    parser = SpaCyRequirementParser(_loader=lambda: (fail, "3.8.16", "3.8.0"))
    outcome = parser.parse(Requirement("R1", 1, TEXT))
    assert outcome.parsed_requirement is None
    assert [d.code for d in outcome.diagnostics] == [
        ParserDiagnosticCode.PARSER_PROCESSING_FAILED,
    ]
    assert "provider detail" not in outcome.diagnostics[0].explanation


@pytest.mark.parametrize("damage", ["token", "sentence", "document"])
def test_offset_invariant_failure_discards_parse(damage: str) -> None:
    doc = fake_doc()
    if damage == "token":
        doc.tokens[0].idx += 1
    elif damage == "sentence":
        doc.sents[0].end_char += 1
    else:
        doc.text = doc.text.lower()
    outcome = parser_for(doc).parse(Requirement("R1", 1, TEXT))
    assert outcome.parsed_requirement is None
    assert [d.code for d in outcome.diagnostics] == [
        ParserDiagnosticCode.OFFSET_INVARIANT_FAILED,
    ]


def test_missing_parser_level_annotations_retains_only_source_aligned_result() -> None:
    doc = FakeDoc(TEXT, [])
    outcome = parser_for(doc).parse(Requirement("R1", 1, TEXT))
    assert outcome.parsed_requirement is not None
    assert outcome.parsed_requirement.tokens == ()
    assert [d.code for d in outcome.diagnostics] == [
        ParserDiagnosticCode.ANNOTATION_INCOMPLETE,
    ]


def test_unmappable_dependency_head_prevents_result() -> None:
    doc = fake_doc()
    doc.tokens[1].head = doc.tokens[4]
    outcome = parser_for(doc).parse(Requirement("R1", 1, TEXT))
    assert outcome.parsed_requirement is None
    assert [d.code for d in outcome.diagnostics] == [
        ParserDiagnosticCode.PARSER_PROCESSING_FAILED,
    ]


def test_real_selected_backend_source_smoke() -> None:
    pytest.importorskip("spacy")
    try:
        if (importlib.metadata.version("spacy") != "3.8.16"
                or importlib.metadata.version("uk-core-news-sm") != "3.8.0"):
            pytest.skip("Selected parser versions are not installed")
    except importlib.metadata.PackageNotFoundError:
        pytest.skip("Selected Ukrainian model package is not installed")
    requirement = Requirement("R009", 2, TEXT)
    outcome = SpaCyRequirementParser().parse(requirement)
    assert outcome.diagnostics == ()
    assert outcome.parsed_requirement is not None
    _assert_source_contract(outcome.parsed_requirement, requirement)
    assert len(outcome.parsed_requirement.sentences) == 2
    assert outcome.parsed_requirement.parser.library_version == "3.8.16"
    assert outcome.parsed_requirement.parser.model_version == "3.8.0"
    _assert_domain_only(outcome)

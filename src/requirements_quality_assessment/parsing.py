"""Replaceable parser infrastructure; no feature or quality interpretation."""

from collections.abc import Callable
from typing import Protocol

from .domain.core import Requirement
from .domain.parser import (
    MorphFeature, ParsedRequirement, ParserDiagnostic, ParserDiagnosticCode,
    ParserMetadata, ParserOutcome, SentenceAnnotation, TokenAnnotation,
)


class RequirementParser(Protocol):
    def parse(self, requirement: Requirement) -> ParserOutcome:
        ...


class _OffsetFailure(Exception):
    """A provider source span cannot be represented against the input text."""


def _load_selected_model() -> tuple[object, str, str]:
    import importlib.metadata

    import spacy

    library_version = importlib.metadata.version("spacy")
    model_version = importlib.metadata.version("uk-core-news-sm")
    if library_version != "3.8.16" or model_version != "3.8.0":
        raise RuntimeError("Selected spaCy 3.8.16 / uk_core_news_sm 3.8.0 is not installed")

    nlp = spacy.load("uk_core_news_sm", disable=["ner"])
    required = {"morphologizer", "parser", "attribute_ruler", "lemmatizer"}
    if (nlp.lang != "uk" or nlp.meta.get("version") != model_version
            or not required.issubset(nlp.pipe_names) or "ner" in nlp.pipe_names):
        raise RuntimeError("Selected Ukrainian model lacks the required enabled pipeline")
    return nlp, library_version, model_version


def _diagnostic(code: ParserDiagnosticCode, explanation: str) -> ParserOutcome:
    return ParserOutcome(None, (ParserDiagnostic(code, explanation),))


def _source_span(text: str, start: int, end: int, provider_text: str) -> None:
    if (not isinstance(start, int) or not isinstance(end, int)
            or start < 0 or end <= start or end > len(text)
            or text[start:end] != provider_text):
        raise _OffsetFailure("Provider annotation does not round-trip against Requirement.text")


def _morphology(token: object) -> tuple[MorphFeature, ...]:
    # MorphAnalysis.to_dict() is copied immediately: no provider object is retained.
    features = token.morph.to_dict()
    return tuple(sorted(
        (MorphFeature(str(name), tuple(sorted(str(value).split(","))))
         for name, value in features.items()),
        key=lambda feature: (feature.name, feature.values),
    ))


def _convert(requirement: Requirement, doc: object, library_version: str,
             model_version: str) -> ParserOutcome:
    text = requirement.text
    if doc.text != text:
        raise _OffsetFailure("Provider document text differs from Requirement.text")

    provider_tokens = list(doc)
    provider_sentences = list(doc.sents)
    if not provider_tokens or not provider_sentences:
        # Tokenization and sentence boundaries are minimum parser capabilities.
        parsed = ParsedRequirement(
            requirement.id, text, (), (),
            ParserMetadata("spacy", library_version, "uk_core_news_sm", model_version, "uk"),
        )
        return ParserOutcome(parsed, (ParserDiagnostic(
            ParserDiagnosticCode.ANNOTATION_INCOMPLETE,
            "Selected parser did not provide both tokens and sentence boundaries",
        ),))

    token_ids = {token.i: index for index, token in enumerate(provider_tokens)}
    if len(token_ids) != len(provider_tokens):
        raise ValueError("Provider token indices are not unique")
    sentence_ids: dict[int, int] = {}
    sentences = []
    for sentence_id, sentence in enumerate(provider_sentences):
        _source_span(text, sentence.start_char, sentence.end_char, sentence.text)
        if sentences and sentence.start_char < sentences[-1].end_offset:
            raise _OffsetFailure("Provider sentences overlap or are not source ordered")
        sentences.append(SentenceAnnotation(sentence_id, sentence.start_char, sentence.end_char))
        for token in sentence:
            if token.i not in token_ids or token.i in sentence_ids:
                raise ValueError("Provider sentence mapping is incomplete or overlapping")
            _source_span(text, token.idx, token.idx + len(token.text), token.text)
            if not (sentence.start_char <= token.idx
                    and token.idx + len(token.text) <= sentence.end_char):
                raise _OffsetFailure("Provider token is outside its sentence source span")
            sentence_ids[token.i] = sentence_id
    if set(sentence_ids) != set(token_ids):
        raise ValueError("Provider tokens are not covered by sentences")

    tokens = []
    for token_id, token in enumerate(provider_tokens):
        start = token.idx
        end = start + len(token.text)
        _source_span(text, start, end, token.text)
        if tokens and start < tokens[-1].end_offset:
            raise _OffsetFailure("Provider tokens overlap or are not source ordered")
        sentence_id = sentence_ids[token.i]
        head_id = None if token.head.i == token.i else token_ids.get(token.head.i)
        if token.head.i != token.i and (head_id is None
                                         or sentence_ids[token.head.i] != sentence_id):
            raise ValueError("Provider dependency head cannot be mapped within its sentence")
        tokens.append(TokenAnnotation(
            token_id=token_id, sentence_id=sentence_id, text=token.text,
            start_offset=start, end_offset=end,
            lemma=token.lemma_ or None, upos=token.pos_ or None,
            morphology=_morphology(token), head_token_id=head_id,
            dependency_relation=token.dep_ or None,
        ))

    parsed = ParsedRequirement(
        requirement_id=requirement.id, text=text, sentences=tuple(sentences),
        tokens=tuple(tokens),
        parser=ParserMetadata("spacy", library_version, "uk_core_news_sm", model_version, "uk"),
    )
    return ParserOutcome(parsed, ())


class SpaCyRequirementParser:
    """Offline adapter for the pinned Ukrainian model, with a private test loader seam."""

    def __init__(self, *, _loader: Callable[[], tuple[object, str, str]] = _load_selected_model):
        self._loader = _loader
        self._backend: object | None = None
        self._versions: tuple[str, str] | None = None

    def parse(self, requirement: Requirement) -> ParserOutcome:
        if self._backend is None:
            try:
                self._backend, library_version, model_version = self._loader()
                self._versions = (library_version, model_version)
            except Exception:
                return _diagnostic(
                    ParserDiagnosticCode.PARSER_UNAVAILABLE,
                    "Selected spaCy 3.8.16 / uk_core_news_sm 3.8.0 parser is unavailable",
                )
        try:
            doc = self._backend(requirement.text)
        except Exception:
            return _diagnostic(
                ParserDiagnosticCode.PARSER_PROCESSING_FAILED,
                "Selected spaCy parser failed while processing the requirement",
            )
        try:
            if self._versions is None:
                raise RuntimeError("Selected parser metadata is absent")
            return _convert(requirement, doc, *self._versions)
        except _OffsetFailure:
            return _diagnostic(
                ParserDiagnosticCode.OFFSET_INVARIANT_FAILED,
                "Provider annotation cannot round-trip against exact Requirement.text offsets",
            )
        except Exception:
            return _diagnostic(
                ParserDiagnosticCode.PARSER_PROCESSING_FAILED,
                "Selected spaCy parser could not produce valid domain annotations",
            )

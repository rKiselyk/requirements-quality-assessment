"""Parser-neutral, exact-source annotation and processing contracts."""

from dataclasses import dataclass
from enum import Enum


def _offsets(start: int, end: int) -> None:
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("annotation offsets must be integers")
    if start < 0 or end < start:
        raise ValueError("annotation offsets must be nonnegative and ordered")


@dataclass(frozen=True, slots=True)
class ParserMetadata:
    provider_id: str
    library_version: str
    model_package: str
    model_version: str
    language: str


@dataclass(frozen=True, slots=True)
class MorphFeature:
    name: str
    values: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.values, tuple) or any(not isinstance(v, str) for v in self.values):
            raise TypeError("morphology values must be a tuple of strings")
        if self.values != tuple(sorted(self.values)):
            raise ValueError("morphology values must be sorted")


@dataclass(frozen=True, slots=True)
class SentenceAnnotation:
    sentence_id: int
    start_offset: int
    end_offset: int

    def __post_init__(self) -> None:
        if not isinstance(self.sentence_id, int) or self.sentence_id < 0:
            raise ValueError("sentence_id must be zero-based")
        _offsets(self.start_offset, self.end_offset)


@dataclass(frozen=True, slots=True)
class TokenAnnotation:
    token_id: int
    sentence_id: int
    text: str
    start_offset: int
    end_offset: int
    lemma: str | None
    upos: str | None
    morphology: tuple[MorphFeature, ...]
    head_token_id: int | None
    dependency_relation: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.token_id, int) or self.token_id < 0:
            raise ValueError("token_id must be zero-based")
        if not isinstance(self.sentence_id, int) or self.sentence_id < 0:
            raise ValueError("sentence_id must be zero-based")
        _offsets(self.start_offset, self.end_offset)
        if not isinstance(self.text, str) or len(self.text) != self.end_offset - self.start_offset:
            raise ValueError("token text must match its Unicode code-point extent")
        if not isinstance(self.morphology, tuple) or any(
            not isinstance(m, MorphFeature) for m in self.morphology
        ):
            raise TypeError("morphology must be a tuple of MorphFeature")
        if self.morphology != tuple(sorted(self.morphology, key=lambda m: (m.name, m.values))):
            raise ValueError("morphology must be sorted by feature name and value")
        if self.head_token_id is not None and (
            not isinstance(self.head_token_id, int) or self.head_token_id < 0
        ):
            raise ValueError("head_token_id must refer to a domain token or be None")


@dataclass(frozen=True, slots=True)
class ParsedRequirement:
    requirement_id: str
    text: str
    sentences: tuple[SentenceAnnotation, ...]
    tokens: tuple[TokenAnnotation, ...]
    parser: ParserMetadata

    def __post_init__(self) -> None:
        if not isinstance(self.text, str):
            raise TypeError("parsed text must be a string")
        if not isinstance(self.sentences, tuple) or any(
            not isinstance(s, SentenceAnnotation) for s in self.sentences
        ):
            raise TypeError("sentences must be a tuple of SentenceAnnotation")
        if not isinstance(self.tokens, tuple) or any(
            not isinstance(t, TokenAnnotation) for t in self.tokens
        ):
            raise TypeError("tokens must be a tuple of TokenAnnotation")
        if not isinstance(self.parser, ParserMetadata):
            raise TypeError("parser must be ParserMetadata")
        sentence_ids = [s.sentence_id for s in self.sentences]
        token_ids = [t.token_id for t in self.tokens]
        if sentence_ids != sorted(set(sentence_ids)) or token_ids != sorted(set(token_ids)):
            raise ValueError("sentence and token IDs must be unique and source ordered")
        if (sentence_ids and sentence_ids[0] != 0) or (token_ids and token_ids[0] != 0):
            raise ValueError("sentence and token IDs must begin at zero")
        if any(a.start_offset > b.start_offset for a, b in zip(self.sentences, self.sentences[1:])):
            raise ValueError("sentences must be in source order")
        if any(a.start_offset > b.start_offset for a, b in zip(self.tokens, self.tokens[1:])):
            raise ValueError("tokens must be in source order")
        if any(s.end_offset > len(self.text) for s in self.sentences):
            raise ValueError("sentence offset exceeds source text")
        by_id = {token.token_id: token for token in self.tokens}
        for token in self.tokens:
            if token.sentence_id not in sentence_ids:
                raise ValueError("token references an absent sentence")
            if self.text[token.start_offset:token.end_offset] != token.text:
                raise ValueError("token must round-trip against exact parsed text")
            if token.head_token_id is not None and (
                token.head_token_id not in by_id
                or by_id[token.head_token_id].sentence_id != token.sentence_id
            ):
                raise ValueError("non-root head must reference a token in the same sentence")


class ParserDiagnosticCode(str, Enum):
    PARSER_UNAVAILABLE = "PARSER_UNAVAILABLE"
    PARSER_PROCESSING_FAILED = "PARSER_PROCESSING_FAILED"
    ANNOTATION_INCOMPLETE = "ANNOTATION_INCOMPLETE"
    OFFSET_INVARIANT_FAILED = "OFFSET_INVARIANT_FAILED"


@dataclass(frozen=True, slots=True)
class ParserDiagnostic:
    code: ParserDiagnosticCode
    explanation: str

    def __post_init__(self) -> None:
        if not isinstance(self.code, ParserDiagnosticCode):
            raise TypeError("code must be an approved ParserDiagnosticCode")


@dataclass(frozen=True, slots=True)
class ParserOutcome:
    parsed_requirement: ParsedRequirement | None
    diagnostics: tuple[ParserDiagnostic, ...]

    def __post_init__(self) -> None:
        if self.parsed_requirement is not None and not isinstance(
            self.parsed_requirement, ParsedRequirement
        ):
            raise TypeError("parsed_requirement must be ParsedRequirement or None")
        if not isinstance(self.diagnostics, tuple) or any(
            not isinstance(d, ParserDiagnostic) or not isinstance(d.code, ParserDiagnosticCode)
            for d in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of approved ParserDiagnostic")
        if self.parsed_requirement is None and not self.diagnostics:
            raise ValueError("absent parsed result requires a diagnostic")
        preventing = {
            ParserDiagnosticCode.PARSER_UNAVAILABLE,
            ParserDiagnosticCode.PARSER_PROCESSING_FAILED,
            ParserDiagnosticCode.OFFSET_INVARIANT_FAILED,
        }
        if self.parsed_requirement is not None and any(
            diagnostic.code in preventing for diagnostic in self.diagnostics
        ):
            raise ValueError("result-preventing diagnostic cannot accompany a parsed result")

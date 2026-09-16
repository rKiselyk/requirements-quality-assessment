"""VERIFY-UK-001: narrow parser/template verification-method detection."""

from dataclasses import dataclass
import re
import unicodedata

from ..domain.core import Evidence, FeatureId, Requirement
from ..domain.detection import (
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DiagnosticSpan,
    FeatureDetectionOutcome,
)
from ..domain.features import FeatureObservation
from ..domain.parser import (
    MorphFeature,
    ParsedRequirement,
    ParserDiagnosticCode,
    SentenceAnnotation,
    TokenAnnotation,
)
from ..parsing import RequirementParser, SpaCyRequirementParser


RULE_ID = "VERIFY-UK-001"
UNRESOLVED_CANDIDATE_CODE = "VERIFY_UNRESOLVED_CANDIDATE"
PARSER_BLOCKED_CODE = "VERIFY_PARSER_BLOCKED"

METHOD_HEAD_LEMMAS = frozenset({"тест", "інспекція", "аналіз", "експеримент"})
SOURCE_CANDIDATE_PHRASES = (
    "відтворювана процедура перевірки",
    "експериментальна процедура",
    "негативні security tests",
    "процедура перевірки",
    "тестовий оракул",
    "тестовий випадок",
    "метод аналізу",
    "acceptance test",
    "security tests",
    "security test",
    "NFR test",
    "tests",
    "test",
)
VERIFICATION_PREDICATES = frozenset({"перевіряється", "перевіряються"})
VERIFICATION_LABELS = (
    "процедура перевірки",
    "метод перевірки",
    "перевірка",
)
LABEL_DELIMITERS = frozenset({":", "—", "-"})
DECLARATION_SURFACE = "визначено"
METHOD_COORDINATORS = frozenset({"та", "і"})

_TEST_FAMILY_PHRASES = frozenset(
    {
        "тестовий оракул",
        "тестовий випадок",
        "негативні security tests",
        "acceptance test",
        "security tests",
        "security test",
        "NFR test",
        "tests",
        "test",
    }
)
_PROTECTED_SLA_CANDIDATE = "спосіб розрахунку SLA"
_PARSER_BLOCKING_CODES = frozenset(
    {
        ParserDiagnosticCode.PARSER_UNAVAILABLE,
        ParserDiagnosticCode.PARSER_PROCESSING_FAILED,
        ParserDiagnosticCode.ANNOTATION_INCOMPLETE,
        ParserDiagnosticCode.OFFSET_INVARIANT_FAILED,
    }
)
_TERMINAL_SENTENCE_PUNCTUATION = frozenset(".?!")
_UNRESOLVED_EXPLANATION = (
    "Approved verification-method candidate cannot be resolved by the "
    "VERIFY-UK-001 first-production grammar."
)


@dataclass(frozen=True, slots=True)
class _Segment:
    sentence_id: int
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class _Span:
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class _PhraseCandidate:
    literal: str
    start: int
    end: int


def _comparison_view(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


def _view_with_provenance(text: str) -> tuple[str, tuple[tuple[int, int], ...]]:
    """Return an NFC/casefold view with original code-point provenance."""
    previous = ""
    spans: list[tuple[int, int]] = []
    for end in range(1, len(text) + 1):
        current = _comparison_view(text[:end])
        left = 0
        while left < min(len(previous), len(current)) and previous[left] == current[left]:
            left += 1
        right = 0
        while (
            right < min(len(previous), len(current)) - left
            and previous[-right - 1] == current[-right - 1]
        ):
            right += 1
        replaced = spans[left : len(previous) - right]
        start = min((span[0] for span in replaced), default=end - 1)
        spans[left : len(previous) - right] = [
            (start, end)
        ] * (len(current) - left - right)
        previous = current
    return previous, tuple(spans)


def _word_constituent(character: str) -> bool:
    category = unicodedata.category(character)
    return category[0] in "LMN" or category == "Pc" or character in "'’ʼ-"


def _outer_boundaries(text: str, start: int, end: int) -> bool:
    return (
        (start == 0 or not _word_constituent(text[start - 1]))
        and (end == len(text) or not _word_constituent(text[end]))
    )


def _literal_pattern(literal: str) -> re.Pattern[str]:
    tokens = _comparison_view(literal).split(" ")
    return re.compile(r"\s+".join(re.escape(token) for token in tokens))


def _literal_spans(
    text: str,
    view: str,
    provenance: tuple[tuple[int, int], ...],
    literal: str,
) -> tuple[_Span, ...]:
    pattern = _literal_pattern(literal)
    matches: list[_Span] = []
    for match in re.finditer(f"(?=({pattern.pattern}))", view):
        view_start, view_end = match.start(1), match.end(1)
        start = provenance[view_start][0]
        end = provenance[view_end - 1][1]
        if (
            _outer_boundaries(text, start, end)
            and pattern.fullmatch(_comparison_view(text[start:end]))
        ):
            matches.append(_Span(start, end))
    return tuple(matches)


def _trim_interval(text: str, start: int, end: int) -> tuple[int, int]:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    while end > start and text[end - 1] in _TERMINAL_SENTENCE_PUNCTUATION:
        end -= 1
        while end > start and text[end - 1].isspace():
            end -= 1
    return start, end


def _sentence_segments(text: str, sentence: SentenceAnnotation) -> tuple[_Segment, ...]:
    segments: list[_Segment] = []
    start = sentence.start_offset
    for index in range(sentence.start_offset, sentence.end_offset):
        if text[index] != ";":
            continue
        segment_start, segment_end = _trim_interval(text, start, index)
        if segment_start < segment_end:
            segments.append(_Segment(sentence.sentence_id, segment_start, segment_end))
        start = index + 1
    segment_start, segment_end = _trim_interval(text, start, sentence.end_offset)
    if segment_start < segment_end:
        segments.append(_Segment(sentence.sentence_id, segment_start, segment_end))
    return tuple(segments)


def _tokens_in_span(
    parsed: ParsedRequirement,
    sentence_id: int,
    start: int,
    end: int,
) -> tuple[TokenAnnotation, ...]:
    return tuple(
        token
        for token in parsed.tokens
        if token.sentence_id == sentence_id
        and start <= token.start_offset
        and token.end_offset <= end
    )


def _has_morph_value(token: TokenAnnotation, feature_name: str, value: str) -> bool:
    return any(
        isinstance(feature, MorphFeature)
        and feature.name == feature_name
        and value in feature.values
        for feature in token.morphology
    )


def _is_oblique(relation: str | None) -> bool:
    return relation == "obl" or bool(relation and relation.startswith("obl:"))


def _ukrainian_heads(tokens: tuple[TokenAnnotation, ...]) -> tuple[TokenAnnotation, ...]:
    return tuple(
        token
        for token in tokens
        if token.lemma is not None
        and _comparison_view(token.lemma) in METHOD_HEAD_LEMMAS
    )


def _has_neighboring_verbal_material(tokens: tuple[TokenAnnotation, ...]) -> bool:
    """Reject an A member whose suffix is not solely a named method phrase.

    VERIFY-UK-001 does not allocate grammar for carving a method noun phrase
    out of neighboring behavior.  A parser-visible verb inside the proposed
    member therefore makes its complete Evidence boundary unresolved.
    """
    return any(token.upos in {"VERB", "AUX"} for token in tokens)


def _selected_phrase_candidates(
    text: str,
    view: str,
    provenance: tuple[tuple[int, int], ...],
    segment: _Segment,
) -> tuple[_PhraseCandidate, ...]:
    candidates = [
        _PhraseCandidate(literal, span.start, span.end)
        for literal in SOURCE_CANDIDATE_PHRASES
        for span in _literal_spans(text, view, provenance, literal)
        if segment.start <= span.start and span.end <= segment.end
    ]
    candidates.sort(
        key=lambda item: (item.start, -(item.end - item.start), SOURCE_CANDIDATE_PHRASES.index(item.literal))
    )
    selected: list[_PhraseCandidate] = []
    for candidate in candidates:
        if any(
            candidate.start < existing.end and existing.start < candidate.end
            for existing in selected
        ):
            continue
        selected.append(candidate)
    return tuple(sorted(selected, key=lambda item: (item.start, item.end)))


def _split_members(
    text: str,
    tokens: tuple[TokenAnnotation, ...],
    start: int,
    end: int,
) -> tuple[tuple[_Span, ...], bool]:
    coordinators = tuple(
        token
        for token in tokens
        if start <= token.start_offset
        and token.end_offset <= end
        and _comparison_view(token.text) in METHOD_COORDINATORS
    )
    members: list[_Span] = []
    cursor = start
    for coordinator in coordinators:
        member_start, member_end = _trim_interval(text, cursor, coordinator.start_offset)
        if member_start >= member_end:
            return (), True
        members.append(_Span(member_start, member_end))
        cursor = coordinator.end_offset
    member_start, member_end = _trim_interval(text, cursor, end)
    if member_start >= member_end:
        return (), bool(coordinators)
    members.append(_Span(member_start, member_end))
    return tuple(members), False


def _phrase_candidates_in_span(
    candidates: tuple[_PhraseCandidate, ...], start: int, end: int
) -> tuple[_PhraseCandidate, ...]:
    return tuple(
        candidate
        for candidate in candidates
        if start <= candidate.start and candidate.end <= end
    )


def _member_has_candidate(
    parsed: ParsedRequirement,
    segment: _Segment,
    candidates: tuple[_PhraseCandidate, ...],
    member: _Span,
) -> bool:
    return _member_candidate_count(parsed, segment, candidates, member) > 0


def _member_candidate_count(
    parsed: ParsedRequirement,
    segment: _Segment,
    candidates: tuple[_PhraseCandidate, ...],
    member: _Span,
) -> int:
    tokens = _tokens_in_span(parsed, segment.sentence_id, member.start, member.end)
    phrases = _phrase_candidates_in_span(candidates, member.start, member.end)
    uncovered_heads = tuple(
        head
        for head in _ukrainian_heads(tokens)
        if not any(
            phrase.start <= head.start_offset and head.end_offset <= phrase.end
            for phrase in phrases
        )
    )
    return len(phrases) + len(uncovered_heads)


def _match_label(
    text: str,
    view: str,
    provenance: tuple[tuple[int, int], ...],
    segment: _Segment,
) -> tuple[_Span, int] | None:
    # Construction B gives ``-`` delimiter meaning even without surrounding
    # whitespace.  Its template-specific right edge therefore cannot use the
    # ordinary lexical boundary rule, which deliberately treats hyphen as a
    # joining character everywhere else.
    labels: list[_Span] = []
    for label in VERIFICATION_LABELS:
        pattern = _literal_pattern(label)
        for match in pattern.finditer(view):
            view_start, view_end = match.start(), match.end()
            start = provenance[view_start][0]
            end = provenance[view_end - 1][1]
            if (
                start == segment.start
                and end <= segment.end
                and pattern.fullmatch(_comparison_view(text[start:end]))
            ):
                labels.append(_Span(start, end))
    if not labels:
        return None
    label = max(labels, key=lambda item: item.end)
    cursor = label.end
    while cursor < segment.end and text[cursor].isspace():
        cursor += 1
    if cursor >= segment.end or text[cursor] not in LABEL_DELIMITERS:
        return None
    delimiter_end = cursor + 1
    cursor = delimiter_end
    while cursor < segment.end and text[cursor].isspace():
        cursor += 1
    return _Span(label.start, delimiter_end), cursor


def _match_declaration(
    text: str,
    view: str,
    provenance: tuple[tuple[int, int], ...],
    segment: _Segment,
) -> tuple[_Span, int] | None:
    declaration = next(
        (
            span
            for span in _literal_spans(text, view, provenance, DECLARATION_SURFACE)
            if span.start == segment.start and span.end <= segment.end
        ),
        None,
    )
    if declaration is None:
        return None
    method_start = declaration.end
    while method_start < segment.end and text[method_start].isspace():
        method_start += 1
    return declaration, method_start


def _test_method_begins_at(
    parsed: ParsedRequirement,
    segment: _Segment,
    candidates: tuple[_PhraseCandidate, ...],
    method_start: int,
) -> bool:
    if any(
        candidate.start == method_start and candidate.literal in _TEST_FAMILY_PHRASES
        for candidate in candidates
    ):
        return True
    tokens = _tokens_in_span(parsed, segment.sentence_id, method_start, segment.end)
    return bool(
        tokens
        and tokens[0].start_offset == method_start
        and tokens[0].lemma is not None
        and _comparison_view(tokens[0].lemma) == "тест"
    )


def _unresolved_diagnostic(text: str, span: _Span) -> DetectionDiagnostic:
    return DetectionDiagnostic(
        code=UNRESOLVED_CANDIDATE_CODE,
        explanation=_UNRESOLVED_EXPLANATION,
        rule_id=RULE_ID,
        candidate_span=DiagnosticSpan(text[span.start : span.end], span.start, span.end),
    )


def _overlaps(left: _Span, right: _Span) -> bool:
    return left.start < right.end and right.start < left.end


class VerificationMethodBaselineDetector:
    """Detect exactly the approved VERIFY-UK-001 constructions A, B, and C."""

    def __init__(self, parser: RequirementParser | None = None):
        self._parser = parser if parser is not None else SpaCyRequirementParser()

    def detect(
        self,
        requirement: Requirement,
    ) -> tuple[
        FeatureDetectionOutcome[FeatureObservation],
        tuple[Evidence, ...],
    ]:
        parser_outcome = self._parser.parse(requirement)
        blocking_codes = tuple(
            diagnostic.code
            for diagnostic in parser_outcome.diagnostics
            if diagnostic.code in _PARSER_BLOCKING_CODES
        )
        parsed = parser_outcome.parsed_requirement
        if (
            blocking_codes
            or parsed is None
            or parsed.requirement_id != requirement.id
            or parsed.text != requirement.text
        ):
            reason = ", ".join(code.value for code in blocking_codes)
            if not reason:
                reason = "invalid parser result"
            diagnostic = DetectionDiagnostic(
                code=PARSER_BLOCKED_CODE,
                explanation=(
                    "Parser-required verification-method analysis is blocked by "
                    f"{reason}."
                ),
                rule_id=RULE_ID,
            )
            return (
                FeatureDetectionOutcome(
                    feature_id=FeatureId.VERIFICATION_METHOD,
                    observations=(),
                    processing_status=DetectionProcessingStatus.INCOMPLETE,
                    diagnostics=(diagnostic,),
                ),
                (),
            )

        text = requirement.text
        view, provenance = _view_with_provenance(text)
        accepted: list[_Span] = []
        unresolved: list[_Span] = []
        context_spans: list[_Span] = []

        for sentence in parsed.sentences:
            for segment in _sentence_segments(text, sentence):
                segment_tokens = _tokens_in_span(
                    parsed, segment.sentence_id, segment.start, segment.end
                )
                phrase_candidates = _selected_phrase_candidates(
                    text, view, provenance, segment
                )

                label_match = _match_label(text, view, provenance, segment)
                if label_match is not None:
                    label_span, method_start = label_match
                    context_spans.append(label_span)
                    if method_start < segment.end:
                        members, ambiguous = _split_members(
                            text, segment_tokens, method_start, segment.end
                        )
                        if ambiguous or not members or any(
                            _member_candidate_count(
                                parsed, segment, phrase_candidates, member
                            ) != 1
                            for member in members
                        ):
                            unresolved.append(_Span(method_start, segment.end))
                        else:
                            accepted.extend(members)
                    continue

                declaration_match = _match_declaration(
                    text, view, provenance, segment
                )
                if declaration_match is not None:
                    declaration_span, method_start = declaration_match
                    context_spans.append(declaration_span)
                    members, ambiguous = _split_members(
                        text, segment_tokens, method_start, segment.end
                    ) if method_start < segment.end else ((), False)
                    if (
                        len(members) == 1
                        and not ambiguous
                        and _member_candidate_count(
                            parsed, segment, phrase_candidates, members[0]
                        ) == 1
                        and _test_method_begins_at(
                            parsed, segment, phrase_candidates, method_start
                        )
                    ):
                        accepted.append(members[0])
                    # Non-test or non-immediate candidates are discovered below.

                predicates = tuple(
                    token
                    for token in segment_tokens
                    if _comparison_view(token.text) in VERIFICATION_PREDICATES
                )
                if predicates:
                    if len(predicates) != 1:
                        if phrase_candidates or _ukrainian_heads(segment_tokens):
                            unresolved.append(_Span(segment.start, segment.end))
                    else:
                        predicate = predicates[0]
                        method_start = predicate.end_offset
                        while method_start < segment.end and text[method_start].isspace():
                            method_start += 1
                        if method_start < segment.end:
                            members, ambiguous = _split_members(
                                text, segment_tokens, method_start, segment.end
                            )
                            if ambiguous or not members:
                                unresolved.append(_Span(method_start, segment.end))
                            else:
                                member_heads = tuple(
                                    _ukrainian_heads(
                                        _tokens_in_span(
                                            parsed,
                                            segment.sentence_id,
                                            member.start,
                                            member.end,
                                        )
                                    )
                                    for member in members
                                )
                                if any(len(heads) != 1 for heads in member_heads):
                                    if any(heads for heads in member_heads) or any(
                                        _member_has_candidate(
                                            parsed, segment, phrase_candidates, member
                                        )
                                        for member in members
                                    ):
                                        unresolved.append(_Span(method_start, segment.end))
                                else:
                                    valid = []
                                    for index, (member, heads) in enumerate(
                                        zip(members, member_heads)
                                    ):
                                        head = heads[0]
                                        member_tokens = _tokens_in_span(
                                            parsed,
                                            segment.sentence_id,
                                            member.start,
                                            member.end,
                                        )
                                        role_ok = (
                                            _has_morph_value(head, "Case", "Ins")
                                            and not _has_neighboring_verbal_material(
                                                member_tokens
                                            )
                                        )
                                        if index == 0:
                                            role_ok = (
                                                role_ok
                                                and _is_oblique(
                                                    head.dependency_relation
                                                )
                                                and head.head_token_id
                                                == predicate.token_id
                                            )
                                        valid.append(role_ok)
                                    if all(valid):
                                        accepted.extend(members)
                                    else:
                                        unresolved.extend(
                                            member
                                            for member, role_ok in zip(members, valid)
                                            if not role_ok
                                        )

                handled = (*accepted, *unresolved, *context_spans)
                for candidate in phrase_candidates:
                    span = _Span(candidate.start, candidate.end)
                    if not any(_overlaps(span, item) for item in handled):
                        unresolved.append(span)

                for sla_span in _literal_spans(
                    text, view, provenance, _PROTECTED_SLA_CANDIDATE
                ):
                    if not (
                        segment.start <= sla_span.start
                        and sla_span.end <= segment.end
                    ):
                        continue
                    if not any(_overlaps(sla_span, item) for item in (*accepted, *unresolved)):
                        unresolved.append(sla_span)

                for head in _ukrainian_heads(segment_tokens):
                    span = _Span(head.start_offset, segment.end)
                    if not any(_overlaps(span, item) for item in (*accepted, *unresolved)):
                        unresolved.append(span)

        accepted = sorted(set(accepted), key=lambda item: (item.start, item.end))
        accepted_spans = tuple(accepted)
        unresolved = sorted(
            {
                item
                for item in unresolved
                if item.start < item.end
                and not any(_overlaps(item, source) for source in accepted_spans)
            },
            key=lambda item: (item.start, item.end),
        )

        evidence = tuple(
            Evidence(
                evidence_id=f"{RULE_ID}:E{ordinal:03d}",
                requirement_id=requirement.id,
                feature_id=FeatureId.VERIFICATION_METHOD,
                text=text[candidate.start : candidate.end],
                start_offset=candidate.start,
                end_offset=candidate.end,
                rule_id=RULE_ID,
            )
            for ordinal, candidate in enumerate(accepted, start=1)
        )
        observations = tuple(
            FeatureObservation(
                feature_id=FeatureId.VERIFICATION_METHOD,
                evidence_refs=(source.evidence_id,),
            )
            for source in evidence
        )
        diagnostics = tuple(
            _unresolved_diagnostic(text, candidate) for candidate in unresolved
        )
        processing_status = (
            DetectionProcessingStatus.INCOMPLETE
            if diagnostics
            else DetectionProcessingStatus.COMPLETE
        )
        return (
            FeatureDetectionOutcome(
                feature_id=FeatureId.VERIFICATION_METHOD,
                observations=observations,
                processing_status=processing_status,
                diagnostics=diagnostics,
            ),
            evidence,
        )

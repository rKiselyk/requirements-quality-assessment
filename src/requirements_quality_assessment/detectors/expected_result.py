"""RESULT-UK-001: narrow parser-assisted expected-result detection."""

from dataclasses import dataclass
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
    ParsedRequirement,
    ParserDiagnosticCode,
    SentenceAnnotation,
    TokenAnnotation,
)
from ..parsing import RequirementParser, SpaCyRequirementParser
from .condition_context import (
    RULE_ID as CONDITION_RULE_ID,
    UNRESOLVED_CANDIDATE_CODE as CONDITION_UNRESOLVED_CANDIDATE_CODE,
    ConditionContextBaselineDetector,
)


RULE_ID = "RESULT-UK-001"
UNRESOLVED_CANDIDATE_CODE = "RESULT_UNRESOLVED_CANDIDATE"
PARSER_BLOCKED_CODE = "RESULT_PARSER_BLOCKED"

NORMATIVE_SURFACES = frozenset({"повинен", "повинна", "повинні", "має", "мають"})

_PARSER_BLOCKING_CODES = frozenset(
    {
        ParserDiagnosticCode.PARSER_UNAVAILABLE,
        ParserDiagnosticCode.PARSER_PROCESSING_FAILED,
        ParserDiagnosticCode.ANNOTATION_INCOMPLETE,
        ParserDiagnosticCode.OFFSET_INVARIANT_FAILED,
    }
)
_CONNECTIVE_RELATIONS = frozenset({"xcomp", "ccomp", "aux", "cop"})
_TERMINAL_SENTENCE_PUNCTUATION = frozenset(".?!")
_UNRESOLVED_EXPLANATION = (
    "Approved expected-result candidate cannot be resolved by the "
    "RESULT-UK-001 first-production grammar."
)


@dataclass(frozen=True, slots=True)
class _Segment:
    sentence_id: int
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class _AcceptedCandidate:
    start: int
    end: int


def _comparison_view(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


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


def _sentence_segments(
    text: str,
    sentence: SentenceAnnotation,
) -> tuple[_Segment, ...]:
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


def _accepted_condition_evidence(
    outcome: FeatureDetectionOutcome[FeatureObservation],
    evidence: tuple[Evidence, ...],
) -> tuple[Evidence, ...]:
    by_id = {source.evidence_id: source for source in evidence}
    accepted: list[Evidence] = []
    for observation in outcome.observations:
        for reference in observation.evidence_refs:
            source = by_id.get(reference)
            if (
                source is not None
                and source.feature_id is FeatureId.CONDITION_CONTEXT
                and source.rule_id == CONDITION_RULE_ID
            ):
                accepted.append(source)
    return tuple(sorted(accepted, key=lambda item: (item.start_offset, item.end_offset)))


def _remove_edge_conditions(
    text: str,
    segment: _Segment,
    condition_evidence: tuple[Evidence, ...],
) -> tuple[int, int]:
    start, end = segment.start, segment.end

    for source in condition_evidence:
        if source.start_offset != start or source.end_offset > end:
            continue
        cursor = source.end_offset
        while cursor < end and text[cursor].isspace():
            cursor += 1
        if cursor < end and text[cursor] == ",":
            start = cursor + 1
            while start < end and text[start].isspace():
                start += 1
            break

    for source in reversed(condition_evidence):
        if source.end_offset == end and start <= source.start_offset:
            end = source.start_offset
            while end > start and text[end - 1].isspace():
                end -= 1
            break

    return start, end


def _tokens_in_candidate(
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


def _is_subject_relation(relation: str | None) -> bool:
    return relation == "nsubj" or bool(relation and relation.startswith("nsubj:"))


def _is_participial_verbal_form(token: TokenAnnotation) -> bool:
    return any(
        feature.name == "VerbForm" and "Part" in feature.values
        for feature in token.morphology
    )


def _is_behavior_predicate(token: TokenAnnotation) -> bool:
    return token.upos == "VERB" or _is_participial_verbal_form(token)


def _has_parser_visible_negation(
    tokens: tuple[TokenAnnotation, ...],
    component: frozenset[int],
) -> bool:
    return any(
        (token.token_id in component or token.head_token_id in component)
        and feature.name == "Polarity"
        and "Neg" in feature.values
        for token in tokens
        for feature in token.morphology
    )


def _has_coordination(tokens: tuple[TokenAnnotation, ...]) -> bool:
    return any(
        token.dependency_relation == "conj"
        or bool(
            token.dependency_relation
            and token.dependency_relation.startswith("conj:")
        )
        for token in tokens
    )


def _predicate_component(
    anchor: TokenAnnotation,
    tokens: tuple[TokenAnnotation, ...],
) -> frozenset[int]:
    by_id = {token.token_id: token for token in tokens}
    neighbors: dict[int, set[int]] = {token_id: set() for token_id in by_id}
    for token in tokens:
        if (
            token.head_token_id in by_id
            and token.dependency_relation in _CONNECTIVE_RELATIONS
        ):
            neighbors[token.token_id].add(token.head_token_id)
            neighbors[token.head_token_id].add(token.token_id)

    pending = [anchor.token_id]
    connected: set[int] = set()
    while pending:
        token_id = pending.pop()
        if token_id in connected:
            continue
        connected.add(token_id)
        pending.extend(neighbors[token_id] - connected)
    return frozenset(connected)


def _has_associated_subject(
    tokens: tuple[TokenAnnotation, ...],
    component: frozenset[int],
) -> bool:
    return any(
        _is_subject_relation(token.dependency_relation)
        and token.head_token_id in component
        for token in tokens
    )


def _has_independently_headed_predicate(
    tokens: tuple[TokenAnnotation, ...],
    component: frozenset[int],
    normative_ids: frozenset[int],
) -> bool:
    subject_heads = {
        token.head_token_id
        for token in tokens
        if _is_subject_relation(token.dependency_relation)
    }
    return any(
        token.token_id not in component
        and token.token_id not in normative_ids
        and _is_behavior_predicate(token)
        and (token.head_token_id is None or token.token_id in subject_heads)
        for token in tokens
    )


def _has_apparent_local_subject_behavior(
    tokens: tuple[TokenAnnotation, ...],
) -> bool:
    subject_heads = {
        token.head_token_id
        for token in tokens
        if _is_subject_relation(token.dependency_relation)
    }
    return any(
        token.token_id in subject_heads and _is_behavior_predicate(token)
        for token in tokens
    )


def _condition_unresolved_in_segment(
    segment: _Segment,
    outcome: FeatureDetectionOutcome[FeatureObservation],
) -> bool:
    return any(
        diagnostic.code == CONDITION_UNRESOLVED_CANDIDATE_CODE
        and diagnostic.candidate_span is not None
        and diagnostic.candidate_span.start_offset < segment.end
        and segment.start < diagnostic.candidate_span.end_offset
        for diagnostic in outcome.diagnostics
    )


def _unresolved_diagnostic(text: str, start: int, end: int) -> DetectionDiagnostic:
    return DetectionDiagnostic(
        code=UNRESOLVED_CANDIDATE_CODE,
        explanation=_UNRESOLVED_EXPLANATION,
        rule_id=RULE_ID,
        candidate_span=DiagnosticSpan(text[start:end], start, end),
    )


class ExpectedResultBaselineDetector:
    """Detect the approved RESULT-UK-001 normative-modal subset."""

    def __init__(
        self,
        parser: RequirementParser | None = None,
        condition_detector: ConditionContextBaselineDetector | None = None,
    ):
        self._parser = parser if parser is not None else SpaCyRequirementParser()
        self._condition_detector = (
            condition_detector
            if condition_detector is not None
            else ConditionContextBaselineDetector()
        )

    def detect(
        self,
        requirement: Requirement,
        *,
        owned_segments: frozenset[tuple[int, int]] = frozenset(),
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
                    "Parser-required expected-result analysis is blocked by "
                    f"{reason}."
                ),
                rule_id=RULE_ID,
            )
            return (
                FeatureDetectionOutcome(
                    feature_id=FeatureId.EXPECTED_RESULT,
                    observations=(),
                    processing_status=DetectionProcessingStatus.INCOMPLETE,
                    diagnostics=(diagnostic,),
                ),
                (),
            )

        condition_outcome, condition_sources = self._condition_detector.detect(
            requirement
        )
        accepted_conditions = _accepted_condition_evidence(
            condition_outcome, condition_sources
        )

        accepted: list[_AcceptedCandidate] = []
        diagnostics: list[DetectionDiagnostic] = []
        for sentence in parsed.sentences:
            for segment in _sentence_segments(requirement.text, sentence):
                if (segment.start, segment.end) in owned_segments:
                    continue
                start, end = _remove_edge_conditions(
                    requirement.text, segment, accepted_conditions
                )
                if start >= end:
                    continue
                tokens = _tokens_in_candidate(
                    parsed, segment.sentence_id, start, end
                )
                normative = tuple(
                    token
                    for token in tokens
                    if _comparison_view(token.text) in NORMATIVE_SURFACES
                )
                apparent_behavior = _has_apparent_local_subject_behavior(tokens)
                condition_unresolved = _condition_unresolved_in_segment(
                    segment, condition_outcome
                )

                if not normative:
                    if apparent_behavior:
                        diagnostics.append(
                            _unresolved_diagnostic(requirement.text, start, end)
                        )
                    continue

                if (
                    len(normative) != 1
                    or condition_unresolved
                    or _has_coordination(tokens)
                ):
                    diagnostics.append(
                        _unresolved_diagnostic(requirement.text, start, end)
                    )
                    continue

                anchor = normative[0]
                component = _predicate_component(anchor, tokens)
                normative_ids = frozenset(token.token_id for token in normative)
                predicates = tuple(
                    token
                    for token in tokens
                    if token.token_id in component
                    and token.token_id not in normative_ids
                    and _is_behavior_predicate(token)
                )
                if (
                    not predicates
                    or not _has_associated_subject(tokens, component)
                    or _has_parser_visible_negation(tokens, component)
                    or _has_independently_headed_predicate(
                        tokens, component, normative_ids
                    )
                ):
                    diagnostics.append(
                        _unresolved_diagnostic(requirement.text, start, end)
                    )
                    continue

                accepted.append(_AcceptedCandidate(start, end))

        accepted.sort(key=lambda item: (item.start, item.end))
        diagnostics.sort(
            key=lambda item: (
                item.candidate_span.start_offset
                if item.candidate_span is not None
                else len(requirement.text) + 1,
                item.candidate_span.end_offset
                if item.candidate_span is not None
                else len(requirement.text) + 1,
            )
        )
        evidence = tuple(
            Evidence(
                evidence_id=f"{RULE_ID}:E{ordinal:03d}",
                requirement_id=requirement.id,
                feature_id=FeatureId.EXPECTED_RESULT,
                text=requirement.text[candidate.start:candidate.end],
                start_offset=candidate.start,
                end_offset=candidate.end,
                rule_id=RULE_ID,
            )
            for ordinal, candidate in enumerate(accepted, start=1)
        )
        observations = tuple(
            FeatureObservation(
                feature_id=FeatureId.EXPECTED_RESULT,
                evidence_refs=(source.evidence_id,),
            )
            for source in evidence
        )
        processing_status = (
            DetectionProcessingStatus.INCOMPLETE
            if diagnostics
            else DetectionProcessingStatus.COMPLETE
        )
        return (
            FeatureDetectionOutcome(
                feature_id=FeatureId.EXPECTED_RESULT,
                observations=observations,
                processing_status=processing_status,
                diagnostics=tuple(diagnostics),
            ),
            evidence,
        )

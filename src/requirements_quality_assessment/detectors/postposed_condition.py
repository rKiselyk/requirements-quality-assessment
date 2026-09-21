"""COND-UK-002, bounded by model-spec §7.14.16.2; no stored attachment model."""

import re

from ..domain.core import Evidence, FeatureId, Requirement
from ..domain.detection import (
    DetectionDiagnostic, DetectionProcessingStatus, DiagnosticSpan,
    FeatureDetectionOutcome,
)
from ..domain.features import FeatureObservation
from ..domain.parser import ParsedRequirement, TokenAnnotation
from ..parsing import RequirementParser, SpaCyRequirementParser
from .condition_context import (
    ConditionContextBaselineDetector, _hard_segments, _literal_spans,
    _view_with_provenance,
)
from .expected_result import (
    NORMATIVE_SURFACES, _comparison_view, _has_coordination,
    _has_parser_visible_negation, _is_behavior_predicate, _is_subject_relation,
    _predicate_component, _sentence_segments, _tokens_in_candidate, _trim_interval,
)
from .quantitative import QuantitativeBaselineDetector


RULE_ID = "COND-UK-002"
UNRESOLVED_CODE = "COND_POSTPOSED_YAKSHCHO_UNRESOLVED"
PARSER_BLOCKED_CODE = "COND_POSTPOSED_YAKSHCHO_PARSER_BLOCKED"


def _markers(text: str) -> tuple[tuple[int, int], ...]:
    view, provenance = _view_with_provenance(text)
    quotes = tuple((match.start(), match.end()) for match in re.finditer("«[^»]*»", text))
    return tuple(
        (start, end)
        for start, end in _literal_spans(text, view, provenance, "якщо")
        if not any(left <= start and end <= right for left, right in quotes)
    )


def _source_candidates(text: str) -> tuple[tuple[int, int, int], ...]:
    """Return delimiter/marker spans without depending on parser availability."""
    candidates = []
    for start, end in _markers(text):
        comma = start - 1
        while comma >= 0 and text[comma].isspace():
            comma -= 1
        if comma >= 0 and text[comma] == ",":
            candidates.append((comma, start, end))
    return tuple(candidates)


def _verb_form(token: TokenAnnotation, value: str) -> bool:
    return any(f.name == "VerbForm" and value in f.values for f in token.morphology)


def _annotations_complete(
    text: str, tokens: tuple[TokenAnnotation, ...], start: int, end: int,
) -> bool:
    cursor = start
    for token in tokens:
        if (token.start_offset < cursor or token.end_offset <= token.start_offset
                or text[cursor:token.start_offset].strip()
                or not token.lemma or not token.upos or not token.dependency_relation
                or (token.head_token_id is None and token.dependency_relation.casefold() != "root")
                or (token.upos == "VERB"
                    and not any(f.name == "VerbForm" and f.values for f in token.morphology))):
            return False
        cursor = token.end_offset
    return bool(tokens) and not text[cursor:end].strip()


def _recognized(
    parsed: ParsedRequirement, sentence_id: int, start: int, end: int,
    comma: int, marker_start: int, marker_end: int,
) -> bool:
    text = parsed.text
    prefix_start, prefix_end = _trim_interval(text, start, comma)
    prefix = _tokens_in_candidate(parsed, sentence_id, prefix_start, prefix_end)
    suffix = _tokens_in_candidate(parsed, sentence_id, marker_start, end)
    local = _tokens_in_candidate(parsed, sentence_id, start, end)
    local_ids = {t.token_id for t in local}
    if (not prefix or not suffix
            or len([m for m in _markers(text) if start <= m[0] < end]) != 1
            or _has_coordination(local)
            or any(t.head_token_id is not None and t.head_token_id not in local_ids
                   for t in local)):
        return False

    normative = tuple(t for t in prefix if _comparison_view(t.text) in NORMATIVE_SURFACES)
    if len(normative) != 1:
        return False
    component = _predicate_component(normative[0], prefix)
    predicates = tuple(t for t in prefix if t != normative[0] and _is_behavior_predicate(t))
    subjects = tuple(t for t in prefix if _is_subject_relation(t.dependency_relation))
    chain_heads = tuple(t for t in prefix
                        if t.token_id in component and t.head_token_id not in component)
    if (len(predicates) != 1 or predicates[0].token_id not in component
            or predicates[0].upos != "VERB" or not _verb_form(predicates[0], "Inf")
            or len(subjects) != 1 or subjects[0].head_token_id not in component
            or len(chain_heads) != 1
            or _has_parser_visible_negation(prefix, component)
            or any(t.dependency_relation == "neg" for t in prefix)):
        return False

    marker = next((t for t in suffix
                   if (t.start_offset, t.end_offset) == (marker_start, marker_end)), None)
    by_id = {t.token_id: t for t in local}
    head = by_id.get(marker.head_token_id) if marker is not None else None
    if (marker is None or marker.dependency_relation != "mark" or head is None
            or head not in suffix or head.upos != "VERB" or not _verb_form(head, "Fin")
            or head.dependency_relation != "advcl"
            or head.head_token_id != chain_heads[0].token_id
            or len([t for t in suffix if t.upos == "VERB" and _verb_form(t, "Fin")]) != 1
            or any(t != head and t.dependency_relation in {"advcl", "mark"} for t in suffix
                   if t != marker)):
        return False

    # Traverse within the parser sentence, including tokens outside this segment,
    # so a nonpunctuation descendant outside the suffix cannot be hidden.
    descendants = {head.token_id}
    pending = [head.token_id]
    while pending:
        parent = pending.pop()
        for token in parsed.tokens:
            if token.head_token_id == parent and token.token_id not in descendants:
                descendants.add(token.token_id)
                pending.append(token.token_id)
    if any(t.token_id not in descendants for t in suffix):
        return False
    if any(t.token_id in descendants and t.upos != "PUNCT"
           and not (marker_start <= t.start_offset and t.end_offset <= end)
           for t in parsed.tokens):
        return False
    # Complete annotations already prove whitespace-only gaps between tokens.
    return suffix[0].start_offset == marker_start and suffix[-1].end_offset == end


class PostposedConditionDetector:
    """Emit only the approved COND-UK-002 contribution."""

    def __init__(self, parser: RequirementParser | None = None):
        self._parser = parser if parser is not None else SpaCyRequirementParser()

    def detect(self, requirement: Requirement) -> tuple[
        FeatureDetectionOutcome[FeatureObservation], tuple[Evidence, ...],
    ]:
        text = requirement.text
        candidates = _source_candidates(text)
        accepted: set[tuple[int, int]] = set()
        diagnostics = []
        parser_outcome = self._parser.parse(requirement) if candidates else None
        parsed = parser_outcome.parsed_requirement if parser_outcome else None
        blocked = (parsed is None or bool(parser_outcome and parser_outcome.diagnostics)
                   or parsed.requirement_id != requirement.id or parsed.text != text)
        segments = (() if blocked else tuple(
            segment for sentence in parsed.sentences
            for segment in _sentence_segments(text, sentence)
        ))
        for comma, marker_start, marker_end in candidates:
            segment = next((s for s in segments
                            if s.start <= comma and marker_end <= s.end), None)
            # Source fallback only bounds diagnostics; it never proves acceptance.
            end = next((end for start, end in _hard_segments(text)
                        if start <= marker_start < end), len(text))
            _, end = _trim_interval(text, marker_start, end)
            code = PARSER_BLOCKED_CODE
            if segment is not None:
                end = segment.end
                tokens = _tokens_in_candidate(parsed, segment.sentence_id, segment.start, end)
                if _annotations_complete(text, tokens, segment.start, end):
                    if _recognized(parsed, segment.sentence_id, segment.start, end,
                                   comma, marker_start, marker_end):
                        accepted.add((marker_start, end))
                        continue
                    code = UNRESOLVED_CODE
            diagnostics.append(DetectionDiagnostic(
                code=code,
                explanation=("Required parser annotations for COND-UK-002 are unavailable or incomplete."
                             if code == PARSER_BLOCKED_CODE else
                             "Postposed якщо candidate does not satisfy the bounded COND-UK-002 graph and source contract."),
                rule_id=RULE_ID,
                candidate_span=DiagnosticSpan(text[marker_start:end], marker_start, end),
            ))
        evidence = tuple(Evidence(
            evidence_id=f"{RULE_ID}:E{ordinal:03d}", requirement_id=requirement.id,
            feature_id=FeatureId.CONDITION_CONTEXT, text=text[start:end],
            start_offset=start, end_offset=end, rule_id=RULE_ID,
        ) for ordinal, (start, end) in enumerate(sorted(accepted), 1))
        return _outcome(evidence, tuple(diagnostics)), evidence


def _outcome(evidence: tuple[Evidence, ...], diagnostics: tuple[DetectionDiagnostic, ...]
             ) -> FeatureDetectionOutcome[FeatureObservation]:
    return FeatureDetectionOutcome(
        feature_id=FeatureId.CONDITION_CONTEXT,
        observations=tuple(FeatureObservation(FeatureId.CONDITION_CONTEXT, (e.evidence_id,))
                           for e in evidence),
        processing_status=(DetectionProcessingStatus.INCOMPLETE if diagnostics
                           else DetectionProcessingStatus.COMPLETE),
        diagnostics=diagnostics,
    )


class ConditionContextDetector:
    """Dispatch COND-UK-002 before the unchanged COND-UK-001 templates."""

    def __init__(self, parser: RequirementParser | None = None,
                 quantitative_detector: QuantitativeBaselineDetector | None = None):
        self._postposed = PostposedConditionDetector(parser)
        self._baseline = ConditionContextBaselineDetector(quantitative_detector)

    def detect(self, requirement: Requirement) -> tuple[
        FeatureDetectionOutcome[FeatureObservation], tuple[Evidence, ...],
    ]:
        extension, new_evidence = self._postposed.detect(requirement)
        owned = frozenset((start, end) for _, start, end in _source_candidates(requirement.text))
        baseline, old_evidence = self._baseline.detect(requirement, owned_marker_spans=owned)
        evidence = tuple(sorted(old_evidence + new_evidence,
                                key=lambda e: (e.start_offset, e.end_offset, e.rule_id)))
        diagnostics = tuple(sorted(baseline.diagnostics + extension.diagnostics,
                                   key=lambda d: (d.candidate_span.start_offset,
                                                  d.candidate_span.end_offset)))
        return _outcome(evidence, diagnostics), evidence

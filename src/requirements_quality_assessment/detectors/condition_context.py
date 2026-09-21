"""COND-UK-001: narrow Ukrainian condition/context baseline detection."""

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
from .quantitative import (
    QUANT_RULE_ID,
    QUANT_UK_RULE_ID,
    QuantitativeBaselineDetector,
    _unsupported_numeric_spans,
)


RULE_ID = "COND-UK-001"
UNRESOLVED_CANDIDATE_CODE = "COND_UNRESOLVED_CANDIDATE"

_MARKERS = ("якщо", "у разі", "під час", "після", "при")
_POSTPOSED_MARKERS = frozenset({"у разі", "під час", "після", "при"})
_NORMATIVE_ANCHORS = ("повинен", "повинна", "повинні", "має", "мають")
_HARD_BOUNDARIES = frozenset(".;?!")
_UNRESOLVED_EXPLANATION = (
    "Approved condition/context candidate cannot be attached or bounded by "
    "the COND-UK-001 first-production templates."
)


@dataclass(frozen=True, slots=True)
class _MarkerMatch:
    literal: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class _AcceptedCandidate:
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class _UnresolvedCandidate:
    start: int
    end: int


def _matching_view(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


def _view_with_provenance(text: str) -> tuple[str, tuple[tuple[int, int], ...]]:
    """Return an NFC/casefold view with original code-point provenance."""
    previous = ""
    spans: list[tuple[int, int]] = []
    for end in range(1, len(text) + 1):
        current = _matching_view(text[:end])
        left = 0
        while left < min(len(previous), len(current)) and previous[left] == current[left]:
            left += 1
        right = 0
        while (right < min(len(previous), len(current)) - left
               and previous[-right - 1] == current[-right - 1]):
            right += 1
        replaced = spans[left:len(previous) - right]
        start = min((span[0] for span in replaced), default=end - 1)
        spans[left:len(previous) - right] = (
            [(start, end)] * (len(current) - left - right)
        )
        previous = current
    return previous, tuple(spans)


def _word_constituent(character: str) -> bool:
    category = unicodedata.category(character)
    return category[0] in "LMN" or category == "Pc" or character in "'’ʼ-"


def _outer_boundaries(text: str, start: int, end: int) -> bool:
    return ((start == 0 or not _word_constituent(text[start - 1]))
            and (end == len(text) or not _word_constituent(text[end])))


def _literal_pattern(literal: str) -> re.Pattern[str]:
    tokens = _matching_view(literal).split(" ")
    return re.compile(r"\s+".join(re.escape(token) for token in tokens))


def _literal_spans(
    text: str,
    view: str,
    provenance: tuple[tuple[int, int], ...],
    literal: str,
) -> tuple[tuple[int, int], ...]:
    pattern = _literal_pattern(literal)
    spans: list[tuple[int, int]] = []
    for match in re.finditer(f"(?=({pattern.pattern}))", view):
        view_start, view_end = match.start(1), match.end(1)
        start = provenance[view_start][0]
        end = provenance[view_end - 1][1]
        if (_outer_boundaries(text, start, end)
                and pattern.fullmatch(_matching_view(text[start:end]))):
            spans.append((start, end))
    return tuple(spans)


def _hard_segments(text: str) -> tuple[tuple[int, int], ...]:
    protected_numeric_spans = _unsupported_numeric_spans(text)
    segments: list[tuple[int, int]] = []
    start = 0
    for index, character in enumerate(text):
        if (character == "."
                and any(span_start < index < span_end
                        for span_start, span_end in protected_numeric_spans)):
            continue
        if character in _HARD_BOUNDARIES:
            segments.append((start, index))
            start = index + 1
    if start < len(text):
        segments.append((start, len(text)))
    return tuple(segments)


def _trim_end(text: str, start: int, end: int) -> int:
    while end > start and text[end - 1].isspace():
        end -= 1
    return end


def _first_non_whitespace(text: str, start: int, end: int) -> int:
    while start < end and text[start].isspace():
        start += 1
    return start


def _has_non_empty_complement(text: str, marker_end: int, candidate_end: int) -> bool:
    return bool(text[marker_end:candidate_end].strip())


def _span_is_within(start: int, end: int, portion_start: int, portion_end: int) -> bool:
    return portion_start <= start and end <= portion_end


class ConditionContextBaselineDetector:
    """Detect the approved leading and postposed COND-UK-001 templates."""

    def __init__(self, quantitative_detector: QuantitativeBaselineDetector | None = None):
        self._quantitative_detector = quantitative_detector or QuantitativeBaselineDetector()

    def detect(
        self,
        requirement: Requirement,
        *,
        owned_marker_spans: frozenset[tuple[int, int]] = frozenset(),
    ) -> tuple[
        FeatureDetectionOutcome[FeatureObservation],
        tuple[Evidence, ...],
    ]:
        text = requirement.text
        view, provenance = _view_with_provenance(text)
        markers = tuple(sorted(
            (
                _MarkerMatch(literal, start, end)
                for literal in _MARKERS
                for start, end in _literal_spans(text, view, provenance, literal)
                if (start, end) not in owned_marker_spans
            ),
            key=lambda item: (item.start, item.end),
        ))
        normative_spans = tuple(
            span
            for literal in _NORMATIVE_ANCHORS
            for span in _literal_spans(text, view, provenance, literal)
        )

        quantitative_outcome, quantitative_evidence = (
            self._quantitative_detector.detect(requirement)
        )
        quantitative_by_id = {
            source.evidence_id: source for source in quantitative_evidence
        }
        accepted_quantitative_spans: list[tuple[int, int]] = []
        for observation in quantitative_outcome.observations:
            referenced = tuple(
                quantitative_by_id[reference]
                for reference in observation.evidence_refs
                if reference in quantitative_by_id
            )
            if (referenced and len(referenced) == len(observation.evidence_refs)
                    and all(source.rule_id in {QUANT_RULE_ID, QUANT_UK_RULE_ID}
                            for source in referenced)):
                accepted_quantitative_spans.extend(
                    (source.start_offset, source.end_offset) for source in referenced
                )

        protected_comma_spans = [
            (source.start_offset, source.end_offset)
            for source in quantitative_evidence
        ]
        protected_comma_spans.extend(
            (diagnostic.candidate_span.start_offset,
             diagnostic.candidate_span.end_offset)
            for diagnostic in quantitative_outcome.diagnostics
            if diagnostic.candidate_span is not None
        )

        def has_attachment(portion_start: int, portion_end: int) -> bool:
            if any(_span_is_within(start, end, portion_start, portion_end)
                   for start, end in normative_spans):
                return True
            return any(_span_is_within(start, end, portion_start, portion_end)
                       for start, end in accepted_quantitative_spans)

        def is_protected_comma(index: int) -> bool:
            return any(start <= index < end for start, end in protected_comma_spans)

        accepted: list[_AcceptedCandidate] = []
        unresolved: list[_UnresolvedCandidate] = []

        for segment_start, raw_segment_end in _hard_segments(text):
            segment_end = _trim_end(text, segment_start, raw_segment_end)
            if segment_start == segment_end:
                continue
            segment_markers = [
                marker for marker in markers
                if segment_start <= marker.start and marker.end <= segment_end
            ]
            if not segment_markers:
                continue

            leading_start = _first_non_whitespace(text, segment_start, segment_end)
            leading_marker = next(
                (marker for marker in segment_markers if marker.start == leading_start),
                None,
            )
            leading_candidate_end: int | None = None
            if leading_marker is not None:
                commas = [
                    index
                    for index in range(leading_marker.end, segment_end)
                    if text[index] == "," and not is_protected_comma(index)
                ]
                viable_commas = [
                    index for index in commas
                    if _has_non_empty_complement(text, leading_marker.end, index)
                    and has_attachment(index + 1, segment_end)
                ]
                if len(viable_commas) == 1:
                    candidate_end = _trim_end(
                        text, leading_marker.end, viable_commas[0],
                    )
                    accepted.append(_AcceptedCandidate(
                        leading_marker.start, candidate_end,
                    ))
                    leading_candidate_end = viable_commas[0]
                elif commas:
                    first_comma = commas[0]
                    if _has_non_empty_complement(
                        text, leading_marker.end, first_comma,
                    ):
                        candidate_end = _trim_end(
                            text, leading_marker.end,
                            first_comma if len(commas) == 1 else segment_end,
                        )
                        unresolved.append(_UnresolvedCandidate(
                            leading_marker.start, candidate_end,
                        ))
                        leading_candidate_end = (
                            first_comma if len(commas) == 1 else segment_end
                        )
                elif _has_non_empty_complement(
                    text, leading_marker.end, segment_end,
                ):
                    unresolved.append(_UnresolvedCandidate(
                        leading_marker.start, segment_end,
                    ))
                    leading_candidate_end = segment_end

            postposed_markers = [
                marker for marker in segment_markers
                if marker is not leading_marker
                and (leading_candidate_end is None
                     or marker.start >= leading_candidate_end)
                and _has_non_empty_complement(text, marker.end, segment_end)
            ]
            if len(postposed_markers) > 1:
                unresolved.extend(
                    _UnresolvedCandidate(marker.start, segment_end)
                    for marker in postposed_markers
                )
                continue

            for marker in postposed_markers:
                if marker.literal not in _POSTPOSED_MARKERS:
                    unresolved.append(_UnresolvedCandidate(marker.start, segment_end))
                    continue
                candidate_has_comma = any(
                    text[index] == "," and not is_protected_comma(index)
                    for index in range(marker.end, segment_end)
                )
                if (not candidate_has_comma
                        and has_attachment(segment_start, marker.start)):
                    accepted.append(_AcceptedCandidate(marker.start, segment_end))
                else:
                    unresolved.append(_UnresolvedCandidate(marker.start, segment_end))

        accepted.sort(key=lambda item: (item.start, item.end))
        unresolved.sort(key=lambda item: (item.start, item.end))

        evidence = tuple(
            Evidence(
                evidence_id=f"{RULE_ID}:E{ordinal:03d}",
                requirement_id=requirement.id,
                feature_id=FeatureId.CONDITION_CONTEXT,
                text=text[candidate.start:candidate.end],
                start_offset=candidate.start,
                end_offset=candidate.end,
                rule_id=RULE_ID,
            )
            for ordinal, candidate in enumerate(accepted, start=1)
        )
        observations = tuple(
            FeatureObservation(
                feature_id=FeatureId.CONDITION_CONTEXT,
                evidence_refs=(source.evidence_id,),
            )
            for source in evidence
        )
        diagnostics = tuple(
            DetectionDiagnostic(
                code=UNRESOLVED_CANDIDATE_CODE,
                explanation=_UNRESOLVED_EXPLANATION,
                rule_id=RULE_ID,
                candidate_span=DiagnosticSpan(
                    text[candidate.start:candidate.end],
                    candidate.start,
                    candidate.end,
                ),
            )
            for candidate in unresolved
        )
        processing_status = (
            DetectionProcessingStatus.INCOMPLETE
            if diagnostics else DetectionProcessingStatus.COMPLETE
        )
        return (
            FeatureDetectionOutcome(
                feature_id=FeatureId.CONDITION_CONTEXT,
                observations=observations,
                processing_status=processing_status,
                diagnostics=diagnostics,
            ),
            evidence,
        )

"""UK-VAGUE-001: exact uk_vague_terms_v1 source-preserving lexical detection."""

from dataclasses import dataclass
import re
import unicodedata

from ..domain.core import Evidence, FeatureId, Requirement
from ..domain.detection import DetectionProcessingStatus, FeatureDetectionOutcome
from ..domain.features import VagueTermOccurrence


VOCABULARY_ID = "uk_vague_terms_v1"
RULE_ID = "UK-VAGUE-001"
VOCABULARY = (
    "в реальному часі",
    "у реальному часі",
    "реальний час",
    "швидко",
    "швидкою",
    "зручною",
    "надійною",
    "надійно",
    "надійний захист",
    "надійно захищені",
)


def _matching_view(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


def _view_with_provenance(text: str) -> tuple[str, tuple[tuple[int, int], ...]]:
    """Map each derived-view code point to its covering original interval.

    Incremental NFC then casefold may compose or expand code points. Rebuilding
    each prefix lets a changed region inherit all original points contributing
    to it; unchanged prefix/suffix regions keep their established provenance.
    """
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
    return (category[0] in "LMN" or category == "Pc"
            or character in "'’ʼ-")


def _outer_boundaries(text: str, start: int, end: int) -> bool:
    return ((start == 0 or not _word_constituent(text[start - 1]))
            and (end == len(text) or not _word_constituent(text[end])))


def _literal_pattern(literal: str) -> re.Pattern[str]:
    tokens = _matching_view(literal).split(" ")
    return re.compile(r"\s+".join(re.escape(token) for token in tokens))


@dataclass(frozen=True, slots=True)
class _Candidate:
    literal: str
    vocabulary_index: int
    start: int
    end: int


class UkVagueTermDetector:
    """Detect approved Ukrainian seed occurrences without parser assistance."""

    def detect(
        self, requirement: Requirement,
    ) -> tuple[FeatureDetectionOutcome[VagueTermOccurrence], tuple[Evidence, ...]]:
        text = requirement.text
        view, provenance = _view_with_provenance(text)
        candidates: list[_Candidate] = []
        for index, literal in enumerate(VOCABULARY):
            pattern = _literal_pattern(literal)
            # Lookahead enumerates candidates even if another literal overlaps.
            for match in re.finditer(f"(?=({pattern.pattern}))", view):
                view_start, view_end = match.start(1), match.end(1)
                start = provenance[view_start][0]
                end = provenance[view_end - 1][1]
                if (_outer_boundaries(text, start, end)
                        and pattern.fullmatch(_matching_view(text[start:end]))):
                    candidates.append(_Candidate(literal, index, start, end))

        candidates.sort(key=lambda item: (item.start, -(item.end - item.start),
                                          item.vocabulary_index))
        selected: list[_Candidate] = []
        for candidate in candidates:
            if not selected or candidate.start >= selected[-1].end:
                selected.append(candidate)

        evidence = tuple(
            Evidence(
                evidence_id=f"{RULE_ID}:E{ordinal:03d}",
                requirement_id=requirement.id,
                feature_id=FeatureId.VAGUE_TERM_OCCURRENCE,
                text=text[item.start:item.end],
                start_offset=item.start,
                end_offset=item.end,
                rule_id=RULE_ID,
            )
            for ordinal, item in enumerate(selected, start=1)
        )
        observations = tuple(
            VagueTermOccurrence(
                feature_id=FeatureId.VAGUE_TERM_OCCURRENCE,
                vocabulary_id=VOCABULARY_ID,
                matched_literal=item.literal,
                evidence_refs=(source.evidence_id,),
            )
            for item, source in zip(selected, evidence)
        )
        return (
            FeatureDetectionOutcome(
                feature_id=FeatureId.VAGUE_TERM_OCCURRENCE,
                observations=observations,
                processing_status=DetectionProcessingStatus.COMPLETE,
                diagnostics=(),
            ),
            evidence,
        )

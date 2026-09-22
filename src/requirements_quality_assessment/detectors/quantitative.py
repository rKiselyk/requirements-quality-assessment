"""First-production source-span quantitative lexical detection."""

from dataclasses import dataclass, replace
from decimal import Decimal
import re
import unicodedata

from ..domain.core import Evidence, FeatureId, Requirement
from ..domain.detection import (
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DiagnosticSpan,
    FeatureDetectionOutcome,
)
from ..domain.quantitative import (
    BoundaryInclusivity,
    ComparatorComponent,
    ComparatorLabel,
    NumericValueComponent,
    QuantitativeConstraintObservation,
    TextComponent,
    UnitComponent,
    UnitLabel,
)


QUANT_RULE_ID = "QUANT-001"
QUANT_UK_RULE_ID = "QUANT-UK-001"
QUANT_METRIC_RULE_ID = "QUANT-METRIC-001"
UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE = "QUANT_UNRESOLVED_NUMERIC_CANDIDATE"

_NUMERIC_PATTERN = re.compile(r"[0-9]+(?:,[0-9]+)?")
_UNSUPPORTED_NUMERIC_PATTERNS = (
    re.compile(r"[0-9]+\.[0-9]+"),
    re.compile(r"[0-9]+(?:,[0-9]+)?[eE][+-]?[0-9]+"),
    re.compile(r"[0-9]+(?:[ \u00a0][0-9]{3})+"),
    re.compile(r"[0-9]+(?:,[0-9]+)?\s*[-–—]\s*[0-9]+(?:,[0-9]+)?"),
    re.compile(r"[0-9]+(?:/[0-9]+){1,2}"),
    re.compile(r"[0-9]+(?:,[0-9]+){2,}"),
    re.compile(r"[+−-]\s*[0-9]+(?:,[0-9]+)?"),
)
_UNRESOLVED_EXPLANATION = (
    "Approved numeric candidate is not linked to an approved comparator or unit."
)
_DURATION_INTRODUCER = "за"
_DEFERRED_FREQUENCY_LITERAL = "не рідше одного разу на"

_UNIT_LABELS = {
    "с": UnitLabel.SECOND,
    "секунд": UnitLabel.SECOND,
    "хв": UnitLabel.MINUTE,
    "хвилин": UnitLabel.MINUTE,
    "%": UnitLabel.PERCENT,
}
_UNIT_SURFACES = tuple(sorted(_UNIT_LABELS, key=len, reverse=True))
_DURATION_UNIT_SURFACES = frozenset({"с", "секунд", "хв", "хвилин"})
_METRIC_TEXT = "Час відгуку"
_METRIC_PREFIX = f"{_METRIC_TEXT} "
_HARD_BOUNDARIES = frozenset(".;?!")


@dataclass(frozen=True, slots=True)
class _ComparatorSpec:
    literal: str
    label: ComparatorLabel
    inclusivity: BoundaryInclusivity
    allows_duration_introducer: bool = False


_UK_COMPARATORS = (
    _ComparatorSpec(
        "не довше ніж",
        ComparatorLabel.LESS_THAN_OR_EQUAL,
        BoundaryInclusivity.INCLUSIVE,
        True,
    ),
    _ComparatorSpec(
        "не більше ніж",
        ComparatorLabel.LESS_THAN_OR_EQUAL,
        BoundaryInclusivity.INCLUSIVE,
        True,
    ),
    _ComparatorSpec(
        "не довше",
        ComparatorLabel.LESS_THAN_OR_EQUAL,
        BoundaryInclusivity.INCLUSIVE,
    ),
    _ComparatorSpec(
        "не більше",
        ComparatorLabel.LESS_THAN_OR_EQUAL,
        BoundaryInclusivity.INCLUSIVE,
    ),
    _ComparatorSpec(
        "не нижче",
        ComparatorLabel.GREATER_THAN_OR_EQUAL,
        BoundaryInclusivity.INCLUSIVE,
    ),
    _ComparatorSpec(
        "до",
        ComparatorLabel.UPPER_BOUND,
        BoundaryInclusivity.UNRESOLVED,
    ),
)


@dataclass(frozen=True, slots=True)
class _Candidate:
    rule_id: str
    start: int
    end: int
    value_start: int
    value_end: int
    value_text: str
    comparator_label: ComparatorLabel | None
    inclusivity: BoundaryInclusivity | None
    unit_label: UnitLabel | None


@dataclass(frozen=True, slots=True)
class _ValueUnit:
    value_start: int
    value_end: int
    value_text: str
    unit_end: int | None
    unit_surface: str | None
    unit_label: UnitLabel | None


@dataclass(frozen=True, slots=True)
class _ProtectedSpan:
    start: int
    end: int
    value_start: int
    value_end: int


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


def _is_ascii_digit(character: str) -> bool:
    return "0" <= character <= "9"


def _supported_numeric_span(text: str, start: int, end: int) -> bool:
    if not _outer_boundaries(text, start, end):
        return False
    if start > 0 and text[start - 1] in "+−":
        return False
    if end < len(text) - 1 and text[end] in ".," and _is_ascii_digit(text[end + 1]):
        return False
    if start >= 2 and text[start - 1] in ".," and _is_ascii_digit(text[start - 2]):
        return False
    return True


def _unsupported_numeric_spans(text: str) -> tuple[tuple[int, int], ...]:
    return tuple(
        (match.start(), match.end())
        for pattern in _UNSUPPORTED_NUMERIC_PATTERNS
        for match in pattern.finditer(text)
    )


def _match_unit(text: str, start: int) -> tuple[str, UnitLabel, int] | None:
    for surface in _UNIT_SURFACES:
        if not text.startswith(surface, start):
            continue
        end = start + len(surface)
        if surface != "%" and not _outer_boundaries(text, start, end):
            continue
        return surface, _UNIT_LABELS[surface], end
    return None


def _match_unit_after_value(
    text: str,
    value_end: int,
) -> tuple[str, UnitLabel, int] | None:
    if text.startswith("%", value_end):
        return "%", UnitLabel.PERCENT, value_end + 1
    separator = re.match(r"\s+", text[value_end:])
    if separator is None:
        return None
    return _match_unit(text, value_end + separator.end())


def _match_value_unit(
    text: str,
    after_prefix: int,
    *,
    allows_duration_introducer: bool = False,
) -> _ValueUnit | None:
    separator = re.match(r"\s+", text[after_prefix:])
    if separator is None:
        return None
    cursor = after_prefix + separator.end()

    if allows_duration_introducer and text.startswith(_DURATION_INTRODUCER, cursor):
        introducer_end = cursor + len(_DURATION_INTRODUCER)
        following = re.match(r"\s+", text[introducer_end:])
        if (_outer_boundaries(text, cursor, introducer_end) and following is not None):
            cursor = introducer_end + following.end()

    numeric = _NUMERIC_PATTERN.match(text, cursor)
    if (numeric is None
            or not _supported_numeric_span(text, numeric.start(), numeric.end())
            or _contained(numeric.start(), numeric.end(), _unsupported_numeric_spans(text))):
        return None

    unit = _match_unit_after_value(text, numeric.end())
    if unit is None:
        return _ValueUnit(
            numeric.start(), numeric.end(), numeric.group(), None, None, None,
        )
    unit_surface, unit_label, unit_end = unit
    return _ValueUnit(
        numeric.start(), numeric.end(), numeric.group(), unit_end,
        unit_surface, unit_label,
    )


def _protected_frequency_spans(
    text: str,
    view: str,
    provenance: tuple[tuple[int, int], ...],
) -> tuple[_ProtectedSpan, ...]:
    protected: list[_ProtectedSpan] = []
    for start, fixed_end in _literal_spans(
        text, view, provenance, _DEFERRED_FREQUENCY_LITERAL,
    ):
        value_unit = _match_value_unit(text, fixed_end)
        if (value_unit is None or value_unit.unit_surface not in _DURATION_UNIT_SURFACES
                or value_unit.unit_end is None):
            continue
        protected.append(_ProtectedSpan(
            start, value_unit.unit_end,
            value_unit.value_start, value_unit.value_end,
        ))
    return tuple(protected)


def _uk_candidates(
    text: str,
    view: str,
    provenance: tuple[tuple[int, int], ...],
) -> tuple[_Candidate, ...]:
    candidates: dict[tuple[int, int], _Candidate] = {}
    for spec in _UK_COMPARATORS:
        for start, comparator_end in _literal_spans(
            text, view, provenance, spec.literal,
        ):
            value_unit = _match_value_unit(
                text,
                comparator_end,
                allows_duration_introducer=spec.allows_duration_introducer,
            )
            if value_unit is None:
                continue
            end = value_unit.unit_end or value_unit.value_end
            candidate = _Candidate(
                QUANT_UK_RULE_ID, start, end,
                value_unit.value_start, value_unit.value_end, value_unit.value_text,
                spec.label, spec.inclusivity, value_unit.unit_label,
            )
            candidates[(start, end)] = candidate
    return tuple(sorted(candidates.values(), key=lambda item: (item.start, item.end)))


def _symbolic_candidates(text: str) -> tuple[_Candidate, ...]:
    candidates: list[_Candidate] = []
    for match in re.finditer("≤", text):
        value_unit = _match_value_unit(text, match.end())
        if value_unit is None:
            continue
        candidates.append(_Candidate(
            QUANT_RULE_ID, match.start(), value_unit.unit_end or value_unit.value_end,
            value_unit.value_start, value_unit.value_end, value_unit.value_text,
            ComparatorLabel.LESS_THAN_OR_EQUAL,
            BoundaryInclusivity.INCLUSIVE,
            value_unit.unit_label,
        ))
    return tuple(candidates)


def _numeric_spans(text: str) -> tuple[tuple[int, int, str], ...]:
    unsupported = _unsupported_numeric_spans(text)
    return tuple(
        (match.start(), match.end(), match.group())
        for match in _NUMERIC_PATTERN.finditer(text)
        if _supported_numeric_span(text, match.start(), match.end())
        and not _contained(match.start(), match.end(), unsupported)
    )


def _fallback_candidates(text: str) -> tuple[_Candidate, ...]:
    candidates: list[_Candidate] = []
    for start, end, value_text in _numeric_spans(text):
        unit = _match_unit_after_value(text, end)
        if unit is None:
            continue
        _, unit_label, unit_end = unit
        candidates.append(_Candidate(
            QUANT_RULE_ID, start, unit_end, start, end, value_text,
            None, None, unit_label,
        ))
    return tuple(candidates)


def _contained(start: int, end: int, spans: tuple[tuple[int, int], ...]) -> bool:
    return any(span_start <= start and end <= span_end for span_start, span_end in spans)


def _accepted_candidates(
    text: str,
    view: str,
    provenance: tuple[tuple[int, int], ...],
    protected: tuple[_ProtectedSpan, ...],
) -> tuple[_Candidate, ...]:
    uk = _uk_candidates(text, view, provenance)
    symbolic = _symbolic_candidates(text)
    comparator_spans = tuple((item.start, item.end) for item in (*uk, *symbolic))
    protected_spans = tuple((item.start, item.end) for item in protected)
    fallback = tuple(
        item for item in _fallback_candidates(text)
        if not _contained(item.start, item.end, comparator_spans)
        and not _contained(item.start, item.end, protected_spans)
    )
    return tuple(sorted((*uk, *symbolic, *fallback), key=lambda item: item.start))


def _evidence_and_observations(
    requirement: Requirement,
    candidates: tuple[_Candidate, ...],
) -> tuple[tuple[Evidence, ...], tuple[QuantitativeConstraintObservation, ...]]:
    counters = {QUANT_RULE_ID: 0, QUANT_UK_RULE_ID: 0}
    evidence: list[Evidence] = []
    observations: list[QuantitativeConstraintObservation] = []
    for candidate in candidates:
        counters[candidate.rule_id] += 1
        evidence_id = f"{candidate.rule_id}:E{counters[candidate.rule_id]:03d}"
        source = Evidence(
            evidence_id=evidence_id,
            requirement_id=requirement.id,
            feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
            text=requirement.text[candidate.start:candidate.end],
            start_offset=candidate.start,
            end_offset=candidate.end,
            rule_id=candidate.rule_id,
        )
        refs = (evidence_id,)
        comparator = None
        if candidate.comparator_label is not None:
            comparator = ComparatorComponent(
                candidate.comparator_label, candidate.inclusivity, refs,
            )
        unit = None
        if candidate.unit_label is not None:
            unit = UnitComponent(candidate.unit_label, refs)
        observation = QuantitativeConstraintObservation(
            feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
            metric=None,
            comparator=comparator,
            value=NumericValueComponent(
                Decimal(candidate.value_text.replace(",", ".")), refs,
            ),
            unit=unit,
            context=None,
            unresolved_components=(),
            evidence_refs=refs,
        )
        evidence.append(source)
        observations.append(observation)
    return tuple(evidence), tuple(observations)


def _is_eligible_metric_anchor(
    observation: QuantitativeConstraintObservation,
    source: Evidence,
) -> bool:
    comparator = observation.comparator
    return (
        source.rule_id == QUANT_RULE_ID
        and comparator is not None
        and comparator.label is ComparatorLabel.LESS_THAN_OR_EQUAL
        and comparator.inclusivity is BoundaryInclusivity.INCLUSIVE
        and observation.value is not None
        and observation.unit is not None
        and observation.unit.label in {UnitLabel.SECOND, UnitLabel.MINUTE}
    )


def _hard_clause_end(text: str) -> int:
    return next(
        (index for index, character in enumerate(text) if character in _HARD_BOUNDARIES),
        len(text),
    )


def _exact_metric_surface_count(text: str, end: int) -> int:
    return sum(
        1
        for match in re.finditer(re.escape(_METRIC_TEXT), text[:end])
        if _outer_boundaries(text, match.start(), match.end())
    )


def _enrich_response_time_metric(
    requirement: Requirement,
    evidence: tuple[Evidence, ...],
    observations: tuple[QuantitativeConstraintObservation, ...],
) -> tuple[tuple[Evidence, ...], tuple[QuantitativeConstraintObservation, ...]]:
    """Attach the exact QUANT-METRIC-001 prefix to one accepted scalar anchor."""
    if not requirement.text.startswith(_METRIC_PREFIX):
        return evidence, observations

    by_id = {source.evidence_id: source for source in evidence}
    accepted = tuple(
        (index, observation, source)
        for index, observation in enumerate(observations)
        if len(observation.evidence_refs) == 1
        for source in (by_id.get(observation.evidence_refs[0]),)
        if source is not None and _is_eligible_metric_anchor(observation, source)
    )
    clause_end = _hard_clause_end(requirement.text)
    clause_anchors = tuple(
        item for item in accepted if item[2].start_offset < clause_end
    )
    if (
        len(clause_anchors) != 1
        or clause_anchors[0][2].start_offset != len(_METRIC_PREFIX)
        or _exact_metric_surface_count(requirement.text, clause_end) != 1
    ):
        return evidence, observations

    observation_index, observation, _ = clause_anchors[0]
    metric_id = f"{QUANT_METRIC_RULE_ID}:E001"
    metric_evidence = Evidence(
        evidence_id=metric_id,
        requirement_id=requirement.id,
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        text=_METRIC_TEXT,
        start_offset=0,
        end_offset=len(_METRIC_TEXT),
        rule_id=QUANT_METRIC_RULE_ID,
    )
    enriched = replace(
        observation,
        metric=TextComponent((metric_id,)),
        evidence_refs=(metric_id, *observation.evidence_refs),
    )
    enriched_observations = list(observations)
    enriched_observations[observation_index] = enriched
    return (metric_evidence, *evidence), tuple(enriched_observations)


def _diagnostics(
    text: str,
    candidates: tuple[_Candidate, ...],
    protected: tuple[_ProtectedSpan, ...],
) -> tuple[DetectionDiagnostic, ...]:
    accepted_spans = tuple(
        (candidate.value_start, candidate.value_end) for candidate in candidates
    )
    protected_spans = tuple((item.start, item.end) for item in protected)
    diagnostics: list[DetectionDiagnostic] = []
    for start, end, value_text in _numeric_spans(text):
        if (_contained(start, end, accepted_spans)
                or _contained(start, end, protected_spans)):
            continue
        diagnostics.append(DetectionDiagnostic(
            code=UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
            explanation=_UNRESOLVED_EXPLANATION,
            rule_id=QUANT_RULE_ID,
            candidate_span=DiagnosticSpan(value_text, start, end),
        ))
    return tuple(diagnostics)


class QuantitativeBaselineDetector:
    """Detect the approved QUANT-001 and QUANT-UK-001 lexical baseline."""

    def detect(
        self,
        requirement: Requirement,
    ) -> tuple[
        FeatureDetectionOutcome[QuantitativeConstraintObservation],
        tuple[Evidence, ...],
    ]:
        text = requirement.text
        view, provenance = _view_with_provenance(text)
        protected = _protected_frequency_spans(text, view, provenance)
        candidates = _accepted_candidates(text, view, provenance, protected)
        evidence, observations = _evidence_and_observations(requirement, candidates)
        evidence, observations = _enrich_response_time_metric(
            requirement, evidence, observations,
        )
        diagnostics = _diagnostics(text, candidates, protected)
        processing_status = (
            DetectionProcessingStatus.INCOMPLETE
            if diagnostics else DetectionProcessingStatus.COMPLETE
        )
        return (
            FeatureDetectionOutcome(
                feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
                observations=observations,
                processing_status=processing_status,
                diagnostics=diagnostics,
            ),
            evidence,
        )

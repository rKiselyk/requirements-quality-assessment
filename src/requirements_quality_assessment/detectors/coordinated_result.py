"""RESULT-UK-002: the closed binary grammar in model-spec §7.14.16.3."""

from dataclasses import dataclass
import re

from ..domain.core import Evidence, FeatureId, Requirement
from ..domain.detection import (
    DetectionDiagnostic, DetectionProcessingStatus, DiagnosticSpan,
    FeatureDetectionOutcome,
)
from ..domain.features import FeatureObservation
from ..domain.parser import ParserOutcome, TokenAnnotation
from ..parsing import RequirementParser, SpaCyRequirementParser
from .condition_context import (
    ConditionContextBaselineDetector, _literal_spans, _view_with_provenance,
)
from .expected_result import (
    ExpectedResultBaselineDetector, NORMATIVE_SURFACES, _comparison_view,
    _is_behavior_predicate, _is_subject_relation, _predicate_component,
    _sentence_segments, _tokens_in_candidate, _trim_interval,
)


RULE_ID = "RESULT-UK-002"
UNRESOLVED_CODE = "RESULT_COORD_UNRESOLVED_CANDIDATE"
PARSER_BLOCKED_CODE = "RESULT_COORD_PARSER_BLOCKED"


def _quoted_spans(text: str) -> tuple[tuple[int, int], ...]:
    return tuple((m.start(), m.end()) for m in re.finditer("«[^»]*»", text))


def _source_spans(text: str, surfaces: frozenset[str]) -> tuple[tuple[int, int], ...]:
    view, provenance = _view_with_provenance(text)
    quotes = _quoted_spans(text)
    return tuple(sorted(
        (start, end) for surface in surfaces
        for start, end in _literal_spans(text, view, provenance, surface)
        if not any(left <= start and end <= right for left, right in quotes)
    ))


def _source_covered(tokens: tuple[TokenAnnotation, ...], text: str, start: int, end: int) -> bool:
    cursor = start
    for token in tokens:
        if (token.start_offset < cursor or token.end_offset <= token.start_offset
                or text[cursor:token.start_offset].strip()):
            return False
        cursor = token.end_offset
    return bool(tokens) and not text[cursor:end].strip()


def _complete(tokens: tuple[TokenAnnotation, ...], text: str, start: int, end: int) -> bool:
    return _source_covered(tokens, text, start, end) and all(
        token.lemma and token.upos and token.dependency_relation
        and (token.head_token_id is not None or token.dependency_relation.casefold() == "root")
        and (token.upos != "VERB" or any(
            f.name == "VerbForm" and f.values for f in token.morphology))
        for token in tokens
    )


def _recognized(tokens: tuple[TokenAnnotation, ...], text: str,
                start: int, end: int, coordinators: tuple[tuple[int, int], ...],
                condition_spans: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    """Return three exact spans only after proving both source and graph."""
    normative = tuple(t for t in tokens if _comparison_view(t.text) in NORMATIVE_SURFACES)
    predicates = tuple(t for t in tokens if t not in normative and _is_behavior_predicate(t))
    subjects = tuple(t for t in tokens if _is_subject_relation(t.dependency_relation))
    if len(normative) != 1 or len(predicates) != 2 or len(subjects) != 1 or len(coordinators) != 1:
        return ()
    anchor, = normative
    first, second = predicates
    coordinator = next((t for t in tokens
                        if (t.start_offset, t.end_offset) == coordinators[0]), None)
    component = _predicate_component(anchor, tokens)
    local_ids = {t.token_id for t in tokens}
    if (coordinator is None or coordinator.text not in {"і", "та"}
            or coordinator.dependency_relation != "cc"
            or coordinator.head_token_id != second.token_id
            or second.dependency_relation != "conj" or second.head_token_id != first.token_id
            or first.token_id not in component or subjects[0].head_token_id not in component
            or subjects[0].dependency_relation == "nsubj:pass"
            or any(left <= t.start_offset and t.end_offset <= right
                   for left, right in _quoted_spans(text)
                   for t in (anchor, first, second, subjects[0]))
            or not (subjects[0].end_offset <= anchor.start_offset
                    < anchor.end_offset <= first.start_offset < first.end_offset
                    <= coordinator.start_offset < coordinator.end_offset <= second.start_offset)
            or any(t.upos != "VERB" or not any(
                f.name == "VerbForm" and f.values == ("Inf",) for f in t.morphology)
                   for t in predicates)
            or any(t.head_token_id is not None and t.head_token_id not in local_ids for t in tokens)
            or any(left < end and start < right for left, right in condition_spans)):
        return ()
    for token in tokens:
        relation = token.dependency_relation.split(":")[0]
        if (relation in {"neg", "orphan", "advcl", "mark"}
                or (relation == "conj" and token != second)
                or (relation == "cc" and token != coordinator)
                or (token.upos == "CCONJ" and token != coordinator)
                or _comparison_view(token.text) in {"або", "чи"}
                or any((f.name == "Polarity" and "Neg" in f.values)
                       or (f.name == "Voice" and "Pass" in f.values)
                       for f in token.morphology)
                or (token.upos == "PUNCT" and any(c in token.text for c in ",:;–—-.?!…"))):
            return ()
    first_start, first_end = _trim_interval(text, start, coordinator.start_offset)
    second_start, second_end = _trim_interval(text, coordinator.end_offset, end)
    if not (first_start == start and anchor.end_offset < first_end
            and second_start <= second.start_offset and second.end_offset <= second_end):
        return ()
    return ((start, anchor.end_offset), (start, first_end), (second_start, second_end))


@dataclass(frozen=True)
class _FixedParser:
    outcome: ParserOutcome

    def parse(self, requirement: Requirement) -> ParserOutcome:
        return self.outcome


def _outcome(observations: tuple[FeatureObservation, ...],
             diagnostics: tuple[DetectionDiagnostic, ...]) -> FeatureDetectionOutcome[FeatureObservation]:
    return FeatureDetectionOutcome(
        feature_id=FeatureId.EXPECTED_RESULT, observations=observations,
        processing_status=(DetectionProcessingStatus.INCOMPLETE if diagnostics
                           else DetectionProcessingStatus.COMPLETE),
        diagnostics=diagnostics,
    )


class CoordinatedExpectedResultDetector:
    """Emit only RESULT-UK-002, with segment ownership kept internal."""

    def __init__(self, parser: RequirementParser | None = None):
        self._parser = parser if parser is not None else SpaCyRequirementParser()

    def detect(self, requirement: Requirement) -> tuple[
        FeatureDetectionOutcome[FeatureObservation], tuple[Evidence, ...],
    ]:
        outcome, evidence, _ = self._detect(requirement, self._parser.parse(requirement))
        return outcome, evidence

    def _detect(self, requirement: Requirement, parser_outcome: ParserOutcome) -> tuple[
        FeatureDetectionOutcome[FeatureObservation], tuple[Evidence, ...],
        frozenset[tuple[int, int]],
    ]:
        text = requirement.text
        anchors = _source_spans(text, NORMATIVE_SURFACES)
        coordinators = _source_spans(text, frozenset({"і", "та"}))
        parsed = parser_outcome.parsed_requirement
        valid = parsed is not None and parsed.text == text and parsed.requirement_id == requirement.id
        segments = tuple(s for sentence in parsed.sentences
                         for s in _sentence_segments(text, sentence)) if valid else ()
        conditions, sources = ConditionContextBaselineDetector().detect(requirement)
        condition_spans = tuple((e.start_offset, e.end_offset) for e in sources) + tuple(
            (d.candidate_span.start_offset, d.candidate_span.end_offset)
            for d in conditions.diagnostics if d.candidate_span is not None)
        accepted = []
        owned = set()
        diagnostics = []
        # Without parser boundaries, source cannot prove a complete candidate
        # interval or a two-verb graph. Report blocking without inventing either.
        if not segments and anchors and coordinators:
            diagnostics.append(DetectionDiagnostic(
                code=PARSER_BLOCKED_CODE, rule_id=RULE_ID,
                explanation="Parser boundaries and coordination annotations are unavailable.",
            ))
        for segment in segments:
            start, end = segment.start, segment.end
            local_coordinators = tuple(s for s in coordinators if start <= s[0] and s[1] <= end)
            if not local_coordinators or not any(start <= a and b <= end for a, b in anchors):
                continue
            tokens = _tokens_in_candidate(parsed, segment.sentence_id, start, end)
            complete = _complete(tokens, text, start, end)
            predicates = tuple(t for t in tokens if _comparison_view(t.text) not in NORMATIVE_SURFACES
                               and _is_behavior_predicate(t))
            # Completed noun/object coordination is not this rule's candidate.
            # Missing annotations cannot establish that negative conclusion.
            apparent = any(any(t.end_offset <= left for t in predicates)
                           and any(right <= t.start_offset for t in predicates)
                           for left, right in local_coordinators)
            shape_unknown = (not _source_covered(tokens, text, start, end)
                             or any(not t.upos for t in tokens))
            if not apparent and not shape_unknown:
                continue
            owned.add((start, end))
            spans = ()
            code = PARSER_BLOCKED_CODE
            if complete and not parser_outcome.diagnostics:
                code = UNRESOLVED_CODE
                spans = _recognized(tokens, text, start, end, local_coordinators, condition_spans)
            if spans:
                accepted.append(spans)
            else:
                diagnostics.append(DetectionDiagnostic(
                    code=code, rule_id=RULE_ID,
                    explanation=("Required RESULT-UK-002 parser annotations are incomplete."
                                 if code == PARSER_BLOCKED_CODE else
                                 "Candidate fails the closed RESULT-UK-002 graph or source contract."),
                    candidate_span=DiagnosticSpan(text[start:end], start, end),
                ))
        spans = sorted({span for group in accepted for span in group})
        evidence = tuple(Evidence(
            evidence_id=f"{RULE_ID}:E{ordinal:03d}", requirement_id=requirement.id,
            feature_id=FeatureId.EXPECTED_RESULT, text=text[start:end],
            start_offset=start, end_offset=end, rule_id=RULE_ID,
        ) for ordinal, (start, end) in enumerate(spans, 1))
        by_span = {(e.start_offset, e.end_offset): e.evidence_id for e in evidence}
        observations = tuple(observation for anchor, first, second in sorted(set(accepted))
                             for observation in (
                                 FeatureObservation(FeatureId.EXPECTED_RESULT, (by_span[first],)),
                                 FeatureObservation(FeatureId.EXPECTED_RESULT,
                                                    (by_span[anchor], by_span[second])),
                             ))
        return _outcome(observations, tuple(diagnostics)), evidence, frozenset(owned)


class ExpectedResultDetector:
    """Dispatch binary candidates before the unchanged single-result grammar."""

    def __init__(self, parser: RequirementParser | None = None,
                 condition_detector: ConditionContextBaselineDetector | None = None):
        self._parser = parser if parser is not None else SpaCyRequirementParser()
        self._condition_detector = condition_detector

    def detect(self, requirement: Requirement) -> tuple[
        FeatureDetectionOutcome[FeatureObservation], tuple[Evidence, ...],
    ]:
        parser_outcome = self._parser.parse(requirement)
        extension, new_evidence, owned = CoordinatedExpectedResultDetector()._detect(
            requirement, parser_outcome)
        baseline, old_evidence = ExpectedResultBaselineDetector(
            _FixedParser(parser_outcome), self._condition_detector,
        ).detect(requirement, owned_segments=owned)
        # A global parser failure has no accepted baseline contribution. Keep
        # its original diagnostic only when the extension has no candidate.
        parsed = parser_outcome.parsed_requirement
        if extension.diagnostics and (parser_outcome.diagnostics or parsed is None
                                      or parsed.requirement_id != requirement.id
                                      or parsed.text != requirement.text):
            return extension, new_evidence
        evidence = tuple(sorted(old_evidence + new_evidence,
                                key=lambda e: (e.start_offset, e.end_offset, e.evidence_id)))
        by_id = {e.evidence_id: e for e in evidence}
        observations = tuple(sorted(baseline.observations + extension.observations,
                                    key=lambda o: by_id[o.evidence_refs[-1]].start_offset))
        diagnostics = tuple(sorted(baseline.diagnostics + extension.diagnostics,
                                   key=lambda d: (d.candidate_span.start_offset
                                                  if d.candidate_span else len(requirement.text) + 1,
                                                  d.candidate_span.end_offset
                                                  if d.candidate_span else len(requirement.text) + 1)))
        return _outcome(observations, diagnostics), evidence

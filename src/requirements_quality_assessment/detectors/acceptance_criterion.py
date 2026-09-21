"""Approved quantitative and conditioned-literal acceptance composition."""

from ..domain.core import Evidence, FeatureId, Requirement
from ..domain.detection import (
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DiagnosticSpan,
    FeatureDetectionOutcome,
)
from ..domain.features import FeatureObservation
from ..domain.parser import ParsedRequirement, TokenAnnotation
from ..domain.quantitative import (
    BoundaryInclusivity,
    ComparatorLabel,
    QuantitativeConstraintObservation,
)
from ..parsing import RequirementParser, SpaCyRequirementParser
from .condition_context import (
    RULE_ID as CONDITION_RULE_ID,
    ConditionContextBaselineDetector,
    _word_constituent,
)
from .expected_result import (
    PARSER_BLOCKED_CODE as RESULT_PARSER_BLOCKED_CODE,
    RULE_ID as RESULT_RULE_ID,
    UNRESOLVED_CANDIDATE_CODE as RESULT_UNRESOLVED_CANDIDATE_CODE,
    ExpectedResultBaselineDetector,
)
from .quantitative import (
    QUANT_RULE_ID,
    QUANT_UK_RULE_ID,
    UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
    QuantitativeBaselineDetector,
    _unsupported_numeric_spans,
)


RULE_ID = "ACCEPT-QUANT-001"
UNRESOLVED_CANDIDATE_CODE = "ACCEPT_UNRESOLVED_CANDIDATE"
DEPENDENCY_BLOCKED_CODE = "ACCEPT_DEPENDENCY_BLOCKED"

_QUANTITATIVE_RULE_IDS = frozenset({QUANT_RULE_ID, QUANT_UK_RULE_ID})
_NON_JUDGEABLE_EXPLANATION = (
    "A contained accepted quantitative candidate is not judgeable under "
    "ACCEPT-QUANT-001."
)
_UNRESOLVED_QUANTITATIVE_EXPLANATION = (
    "A contained quantitative candidate remains unresolved under "
    "ACCEPT-QUANT-001."
)
_UNRESOLVED_RESULT_EXPLANATION = (
    "Quantitative acceptance linkage cannot be established for an unresolved "
    "expected-result candidate."
)
_DEPENDENCY_BLOCKED_EXPLANATION = (
    "Required expected-result analysis is blocked for ACCEPT-QUANT-001."
)

LITERAL_RULE_ID = "ACCEPT-UK-001"
LITERAL_UNRESOLVED_CANDIDATE_CODE = "ACCEPT_LITERAL_UNRESOLVED_CANDIDATE"
LITERAL_DEPENDENCY_BLOCKED_CODE = "ACCEPT_LITERAL_DEPENDENCY_BLOCKED"

_LITERAL_UNRESOLVED_EXPLANATION = (
    "Conditioned exact-message candidate cannot be resolved under "
    "ACCEPT-UK-001."
)
_LITERAL_DEPENDENCY_BLOCKED_EXPLANATION = (
    "Required condition or expected-result analysis is blocked for "
    "ACCEPT-UK-001."
)


def _is_judgeable(observation: QuantitativeConstraintObservation) -> bool:
    comparator = observation.comparator
    if comparator is None:
        return observation.value is not None and observation.unit is not None
    return (
        comparator.label
        in {
            ComparatorLabel.LESS_THAN_OR_EQUAL,
            ComparatorLabel.GREATER_THAN_OR_EQUAL,
        }
        and comparator.inclusivity is BoundaryInclusivity.INCLUSIVE
    )


def _contains(container: Evidence, source: Evidence | DiagnosticSpan) -> bool:
    return (
        container.start_offset <= source.start_offset
        and source.end_offset <= container.end_offset
    )


def _overlaps(left: DiagnosticSpan, right: Evidence | DiagnosticSpan) -> bool:
    return (
        left.start_offset < right.end_offset
        and right.start_offset < left.end_offset
    )


def _diagnostic(
    code: str,
    explanation: str,
    candidate_span: DiagnosticSpan | None = None,
) -> DetectionDiagnostic:
    return DetectionDiagnostic(
        code=code,
        explanation=explanation,
        rule_id=RULE_ID,
        candidate_span=candidate_span,
    )


class AcceptanceCriterionBaselineDetector:
    """Compose accepted result and quantitative evidence under ACCEPT-QUANT-001."""

    def __init__(
        self,
        expected_result_detector: ExpectedResultBaselineDetector | None = None,
        quantitative_detector: QuantitativeBaselineDetector | None = None,
    ):
        self._expected_result_detector = (
            expected_result_detector
            if expected_result_detector is not None
            else ExpectedResultBaselineDetector()
        )
        self._quantitative_detector = (
            quantitative_detector
            if quantitative_detector is not None
            else QuantitativeBaselineDetector()
        )

    def detect(
        self,
        requirement: Requirement,
    ) -> tuple[
        FeatureDetectionOutcome[FeatureObservation],
        tuple[Evidence, ...],
    ]:
        expected_outcome, expected_evidence = (
            self._expected_result_detector.detect(requirement)
        )
        quantitative_outcome, quantitative_evidence = (
            self._quantitative_detector.detect(requirement)
        )

        if any(
            item.code == RESULT_PARSER_BLOCKED_CODE
            for item in expected_outcome.diagnostics
        ):
            diagnostic = _diagnostic(
                DEPENDENCY_BLOCKED_CODE,
                _DEPENDENCY_BLOCKED_EXPLANATION,
            )
            return (
                FeatureDetectionOutcome(
                    feature_id=FeatureId.ACCEPTANCE_CRITERION,
                    observations=(),
                    processing_status=DetectionProcessingStatus.INCOMPLETE,
                    diagnostics=(diagnostic,),
                ),
                (),
            )

        expected_by_id = {
            source.evidence_id: source for source in expected_evidence
        }
        accepted_results_by_span: dict[tuple[int, int], Evidence] = {}
        for observation in expected_outcome.observations:
            if observation.feature_id is not FeatureId.EXPECTED_RESULT:
                continue
            sources = tuple(
                expected_by_id.get(reference)
                for reference in observation.evidence_refs
            )
            if (
                not sources
                or any(source is None for source in sources)
                or any(
                    source.feature_id is not FeatureId.EXPECTED_RESULT
                    or source.rule_id != RESULT_RULE_ID
                    for source in sources
                    if source is not None
                )
            ):
                continue
            for source in sources:
                if source is not None:
                    accepted_results_by_span.setdefault(
                        (source.start_offset, source.end_offset), source
                    )
        accepted_results = tuple(
            sorted(
                accepted_results_by_span.values(),
                key=lambda item: (item.start_offset, item.end_offset),
            )
        )

        quantitative_by_id = {
            source.evidence_id: source for source in quantitative_evidence
        }
        accepted_quantitative: list[
            tuple[QuantitativeConstraintObservation, tuple[Evidence, ...]]
        ] = []
        for observation in quantitative_outcome.observations:
            if not isinstance(observation, QuantitativeConstraintObservation):
                continue
            if observation.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
                continue
            sources = tuple(
                quantitative_by_id.get(reference)
                for reference in observation.evidence_refs
            )
            if (
                not sources
                or any(source is None for source in sources)
                or any(
                    source.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT
                    or source.rule_id not in _QUANTITATIVE_RULE_IDS
                    for source in sources
                    if source is not None
                )
            ):
                continue
            accepted_quantitative.append(
                (observation, tuple(source for source in sources if source is not None))
            )

        unresolved_quantitative_spans = tuple(
            diagnostic.candidate_span
            for diagnostic in quantitative_outcome.diagnostics
            if (
                diagnostic.code == UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE
                and diagnostic.candidate_span is not None
            )
        )

        accepted_result_spans: list[Evidence] = []
        diagnostics: list[tuple[str, DetectionDiagnostic]] = []
        diagnostic_keys: set[tuple[str, int | None, int | None]] = set()

        def add_diagnostic(
            cause: str,
            explanation: str,
            span: DiagnosticSpan | None,
        ) -> None:
            key = (
                cause,
                span.start_offset if span is not None else None,
                span.end_offset if span is not None else None,
            )
            if key in diagnostic_keys:
                return
            diagnostic_keys.add(key)
            diagnostics.append(
                (
                    cause,
                    _diagnostic(
                        UNRESOLVED_CANDIDATE_CODE,
                        explanation,
                        span,
                    ),
                )
            )

        for result in accepted_results:
            judgeable = False
            for observation, sources in accepted_quantitative:
                if not all(_contains(result, source) for source in sources):
                    continue
                if _is_judgeable(observation):
                    judgeable = True
                    continue
                start = min(source.start_offset for source in sources)
                end = max(source.end_offset for source in sources)
                add_diagnostic(
                    "accepted-non-judgeable",
                    _NON_JUDGEABLE_EXPLANATION,
                    DiagnosticSpan(requirement.text[start:end], start, end),
                )

            for span in unresolved_quantitative_spans:
                if _contains(result, span):
                    add_diagnostic(
                        "unresolved-quantitative",
                        _UNRESOLVED_QUANTITATIVE_EXPLANATION,
                        span,
                    )

            if judgeable:
                accepted_result_spans.append(result)

        accepted_quantitative_evidence = tuple(
            source
            for _, sources in accepted_quantitative
            for source in sources
        )
        for diagnostic in expected_outcome.diagnostics:
            result_span = diagnostic.candidate_span
            if (
                diagnostic.code != RESULT_UNRESOLVED_CANDIDATE_CODE
                or result_span is None
            ):
                continue
            overlaps_quantitative = any(
                _overlaps(result_span, source)
                for source in accepted_quantitative_evidence
            ) or any(
                _overlaps(result_span, span)
                for span in unresolved_quantitative_spans
            )
            if overlaps_quantitative:
                add_diagnostic(
                    "unresolved-result",
                    _UNRESOLVED_RESULT_EXPLANATION,
                    result_span,
                )

        diagnostics.sort(
            key=lambda item: (
                item[1].candidate_span is None,
                item[1].candidate_span.start_offset
                if item[1].candidate_span is not None
                else len(requirement.text) + 1,
                item[1].candidate_span.end_offset
                if item[1].candidate_span is not None
                else len(requirement.text) + 1,
            )
        )

        evidence = tuple(
            Evidence(
                evidence_id=f"{RULE_ID}:E{ordinal:03d}",
                requirement_id=requirement.id,
                feature_id=FeatureId.ACCEPTANCE_CRITERION,
                text=requirement.text[result.start_offset:result.end_offset],
                start_offset=result.start_offset,
                end_offset=result.end_offset,
                rule_id=RULE_ID,
            )
            for ordinal, result in enumerate(accepted_result_spans, start=1)
        )
        observations = tuple(
            FeatureObservation(
                feature_id=FeatureId.ACCEPTANCE_CRITERION,
                evidence_refs=(source.evidence_id,),
            )
            for source in evidence
        )
        outcome_diagnostics = tuple(item[1] for item in diagnostics)
        processing_status = (
            DetectionProcessingStatus.INCOMPLETE
            if outcome_diagnostics
            else DetectionProcessingStatus.COMPLETE
        )
        return (
            FeatureDetectionOutcome(
                feature_id=FeatureId.ACCEPTANCE_CRITERION,
                observations=observations,
                processing_status=processing_status,
                diagnostics=outcome_diagnostics,
            ),
            evidence,
        )


def _accepted_sources(
    outcome: FeatureDetectionOutcome[FeatureObservation],
    evidence: tuple[Evidence, ...],
    feature_id: FeatureId,
    rule_id: str,
) -> tuple[Evidence, ...]:
    by_id = {source.evidence_id: source for source in evidence}
    accepted: dict[tuple[int, int], Evidence] = {}
    for observation in outcome.observations:
        for reference in observation.evidence_refs:
            source = by_id.get(reference)
            if (
                source is not None
                and source.feature_id is feature_id
                and source.rule_id == rule_id
            ):
                accepted.setdefault(
                    (source.start_offset, source.end_offset), source
                )
    return tuple(
        sorted(
            accepted.values(),
            key=lambda item: (item.start_offset, item.end_offset),
        )
    )


def _exact_occurrences(
    text: str,
    start: int,
    end: int,
    surface: str,
) -> tuple[tuple[int, int], ...]:
    occurrences: list[tuple[int, int]] = []
    cursor = start
    while True:
        found = text.find(surface, cursor, end)
        if found < 0:
            break
        found_end = found + len(surface)
        if (
            (found == start or not _word_constituent(text[found - 1]))
            and (found_end == end or not _word_constituent(text[found_end]))
        ):
            occurrences.append((found, found_end))
        cursor = found + 1
    return tuple(occurrences)


def _has_exact_pair(text: str, start: int, end: int) -> bool:
    return bool(
        _exact_occurrences(text, start, end, "показати")
        and _exact_occurrences(text, start, end, "повідомлення")
    )


def _tokens_for_result(
    parsed: ParsedRequirement,
    result: Evidence,
) -> tuple[TokenAnnotation, ...]:
    return tuple(
        token
        for token in parsed.tokens
        if result.start_offset <= token.start_offset
        and token.end_offset <= result.end_offset
    )


def _exact_predicate_object(
    parsed: ParsedRequirement,
    result: Evidence,
) -> tuple[TokenAnnotation, TokenAnnotation] | None:
    tokens = _tokens_for_result(parsed, result)
    predicate_spans = _exact_occurrences(
        parsed.text, result.start_offset, result.end_offset, "показати"
    )
    object_spans = _exact_occurrences(
        parsed.text, result.start_offset, result.end_offset, "повідомлення"
    )
    if len(predicate_spans) != 1 or len(object_spans) != 1:
        return None
    predicates = tuple(
        token
        for token in tokens
        if (token.start_offset, token.end_offset) == predicate_spans[0]
        and token.text == "показати"
        and token.lemma == "показати"
    )
    objects = tuple(
        token
        for token in tokens
        if (token.start_offset, token.end_offset) == object_spans[0]
        and token.text == "повідомлення"
        and token.lemma == "повідомлення"
    )
    if len(predicates) != 1 or len(objects) != 1:
        return None
    predicate, object_token = predicates[0], objects[0]
    if (
        predicate.sentence_id != object_token.sentence_id
        or object_token.dependency_relation != "obj"
        or object_token.head_token_id != predicate.token_id
    ):
        return None
    return predicate, object_token


def _literal_state(
    text: str,
    result: Evidence,
    object_token: TokenAnnotation,
) -> str:
    """Return accepted, negative, or unresolved for the exact source suffix."""
    result_text = text[result.start_offset:result.end_offset]
    open_count = result_text.count("«")
    close_count = result_text.count("»")
    if open_count == close_count == 0:
        return "negative"
    if open_count != 1 or close_count != 1:
        return "unresolved"

    suffix = text[object_token.end_offset:result.end_offset]
    trimmed = suffix.strip()
    if not trimmed.startswith("«") or not trimmed.endswith("»"):
        return "unresolved"
    if trimmed.count("«") != 1 or trimmed.count("»") != 1:
        return "unresolved"
    content = trimmed[1:-1]
    if not content:
        return "negative"
    return "accepted"


def _partitioned_result(
    text: str,
    parsed: ParsedRequirement,
    result: Evidence,
    conditions: tuple[Evidence, ...],
    results: tuple[Evidence, ...],
) -> Evidence | None:
    segments = tuple(
        (start, end)
        for start, end in _source_segments(text)
        if start <= result.start_offset and result.end_offset <= end
    )
    if len(segments) != 1:
        return None
    segment_start, segment_end = segments[0]
    if not any(
        sentence.start_offset <= segment_start
        and segment_end <= sentence.end_offset
        for sentence in parsed.sentences
    ):
        return None
    local_conditions = tuple(
        source
        for source in conditions
        if segment_start <= source.start_offset
        and source.end_offset <= segment_end
    )
    local_results = tuple(
        source
        for source in results
        if segment_start <= source.start_offset
        and source.end_offset <= segment_end
    )
    if len(local_conditions) != 1 or len(local_results) != 1:
        return None
    condition = local_conditions[0]
    if (
        condition.start_offset != segment_start
        or result.end_offset != segment_end
    ):
        return None
    cursor = condition.end_offset
    while cursor < result.start_offset and text[cursor].isspace():
        cursor += 1
    if cursor >= result.start_offset or text[cursor] != ",":
        return None
    cursor += 1
    while cursor < result.start_offset and text[cursor].isspace():
        cursor += 1
    if cursor != result.start_offset:
        return None
    return condition


def _conditions_in_result_segment(
    text: str,
    result: Evidence,
    conditions: tuple[Evidence, ...],
) -> tuple[Evidence, ...]:
    segments = tuple(
        (start, end)
        for start, end in _source_segments(text)
        if start <= result.start_offset and result.end_offset <= end
    )
    if len(segments) != 1:
        return ()
    segment_start, segment_end = segments[0]
    return tuple(
        source
        for source in conditions
        if segment_start <= source.start_offset
        and source.end_offset <= segment_end
    )


def _source_segments(text: str) -> tuple[tuple[int, int], ...]:
    protected_numeric_spans = _unsupported_numeric_spans(text)
    raw_segments: list[tuple[int, int]] = []
    start = 0
    guillemet_depth = 0
    for index, character in enumerate(text):
        if character == "«":
            guillemet_depth += 1
            continue
        if character == "»" and guillemet_depth:
            guillemet_depth -= 1
            continue
        if character not in ".;?!" or guillemet_depth:
            continue
        if character == "." and any(
            span_start < index < span_end
            for span_start, span_end in protected_numeric_spans
        ):
            continue
        raw_segments.append((start, index))
        start = index + 1
    if start < len(text):
        raw_segments.append((start, len(text)))

    segments: list[tuple[int, int]] = []
    for raw_start, raw_end in raw_segments:
        start, end = raw_start, raw_end
        while start < end and text[start].isspace():
            start += 1
        while end > start and text[end - 1].isspace():
            end -= 1
        if start < end:
            segments.append((start, end))
    return tuple(segments)


def _leading_literal_candidate_segments(
    text: str,
) -> tuple[tuple[int, int], ...]:
    candidates: list[tuple[int, int]] = []
    for segment_start, segment_end in _source_segments(text):
        start = segment_start
        while start < segment_end and text[start].isspace():
            start += 1
        marker_end = start + len("Якщо")
        if (
            text[start:marker_end].casefold() == "якщо"
            and marker_end < segment_end
            and not _word_constituent(text[marker_end])
            and _has_exact_pair(text, marker_end, segment_end)
        ):
            candidates.append((segment_start, segment_end))
    return tuple(candidates)


def _sources_in_segment(
    sources: tuple[Evidence, ...],
    segment: tuple[int, int],
) -> tuple[Evidence, ...]:
    start, end = segment
    return tuple(
        source
        for source in sources
        if start <= source.start_offset and source.end_offset <= end
    )


def _dependency_incomplete_in_segment(
    outcome: FeatureDetectionOutcome[FeatureObservation],
    segment: tuple[int, int],
) -> bool:
    if outcome.processing_status is DetectionProcessingStatus.COMPLETE:
        return False
    start, end = segment
    return any(
        diagnostic.candidate_span is None
        or (
            diagnostic.candidate_span.start_offset < end
            and start < diagnostic.candidate_span.end_offset
        )
        for diagnostic in outcome.diagnostics
    )


class LiteralAcceptanceCriterionDetector:
    """Implement only ACCEPT-UK-001's conditioned exact-message rule."""

    def __init__(
        self,
        parser: RequirementParser | None = None,
        condition_detector: ConditionContextBaselineDetector | None = None,
        expected_result_detector: ExpectedResultBaselineDetector | None = None,
    ) -> None:
        self._parser = parser if parser is not None else SpaCyRequirementParser()
        self._condition_detector = (
            condition_detector
            if condition_detector is not None
            else ConditionContextBaselineDetector()
        )
        self._expected_result_detector = (
            expected_result_detector
            if expected_result_detector is not None
            else ExpectedResultBaselineDetector()
        )

    def detect(
        self,
        requirement: Requirement,
    ) -> tuple[
        FeatureDetectionOutcome[FeatureObservation],
        tuple[Evidence, ...],
    ]:
        condition_outcome, condition_evidence = self._condition_detector.detect(
            requirement
        )
        expected_outcome, expected_evidence = (
            self._expected_result_detector.detect(requirement)
        )
        conditions = _accepted_sources(
            condition_outcome,
            condition_evidence,
            FeatureId.CONDITION_CONTEXT,
            CONDITION_RULE_ID,
        )
        results = _accepted_sources(
            expected_outcome,
            expected_evidence,
            FeatureId.EXPECTED_RESULT,
            RESULT_RULE_ID,
        )

        source_candidates = _leading_literal_candidate_segments(requirement.text)
        dependency_blocked = any(
            (
                not _sources_in_segment(conditions, segment)
                and _dependency_incomplete_in_segment(
                    condition_outcome, segment
                )
            )
            or (
                not _sources_in_segment(results, segment)
                and _dependency_incomplete_in_segment(expected_outcome, segment)
            )
            for segment in source_candidates
        )

        parser_outcome = self._parser.parse(requirement)
        parsed = parser_outcome.parsed_requirement
        parser_valid = (
            parsed is not None
            and parsed.requirement_id == requirement.id
            and parsed.text == requirement.text
            and bool(parsed.sentences)
            and not parser_outcome.diagnostics
        )

        accepted_pairs: set[tuple[int, int, int, int]] = set()
        unresolved_spans: set[tuple[int, int]] = set()
        for result in results:
            if not _has_exact_pair(
                requirement.text, result.start_offset, result.end_offset
            ):
                continue
            if not conditions:
                # With completed condition analysis, an unconditional exact
                # output is a determinate negative even if parser data is absent.
                continue
            if not parser_valid:
                unresolved_spans.add((result.start_offset, result.end_offset))
                continue
            assert parsed is not None
            if not _conditions_in_result_segment(
                requirement.text, result, conditions
            ):
                # An exact output without an accepted leading COND-UK-001
                # condition is explicitly outside this bounded rule.
                continue
            condition = _partitioned_result(
                requirement.text, parsed, result, conditions, results
            )
            pair = _exact_predicate_object(parsed, result)
            if condition is None or pair is None:
                unresolved_spans.add((result.start_offset, result.end_offset))
                continue
            _, object_token = pair
            literal_state = _literal_state(requirement.text, result, object_token)
            if literal_state == "accepted":
                accepted_pairs.add(
                    (
                        condition.start_offset,
                        condition.end_offset,
                        result.start_offset,
                        result.end_offset,
                    )
                )
            elif literal_state == "unresolved":
                unresolved_spans.add((result.start_offset, result.end_offset))

        spans = tuple(
            sorted(
                {
                    (condition_start, condition_end)
                    for condition_start, condition_end, _, _ in accepted_pairs
                }
                | {
                    (result_start, result_end)
                    for _, _, result_start, result_end in accepted_pairs
                }
            )
        )
        evidence = tuple(
            Evidence(
                evidence_id=f"{LITERAL_RULE_ID}:E{ordinal:03d}",
                requirement_id=requirement.id,
                feature_id=FeatureId.ACCEPTANCE_CRITERION,
                text=requirement.text[start:end],
                start_offset=start,
                end_offset=end,
                rule_id=LITERAL_RULE_ID,
            )
            for ordinal, (start, end) in enumerate(spans, start=1)
        )
        by_span = {
            (source.start_offset, source.end_offset): source.evidence_id
            for source in evidence
        }
        observations = tuple(
            FeatureObservation(
                feature_id=FeatureId.ACCEPTANCE_CRITERION,
                evidence_refs=(
                    by_span[(condition_start, condition_end)],
                    by_span[(result_start, result_end)],
                ),
            )
            for condition_start, condition_end, result_start, result_end in sorted(
                accepted_pairs, key=lambda item: (item[2], item[3], item[0], item[1])
            )
        )
        diagnostics = tuple(
            DetectionDiagnostic(
                code=LITERAL_UNRESOLVED_CANDIDATE_CODE,
                explanation=_LITERAL_UNRESOLVED_EXPLANATION,
                rule_id=LITERAL_RULE_ID,
                candidate_span=DiagnosticSpan(
                    requirement.text[start:end], start, end
                ),
            )
            for start, end in sorted(unresolved_spans)
        )
        if dependency_blocked:
            diagnostics += (
                DetectionDiagnostic(
                    code=LITERAL_DEPENDENCY_BLOCKED_CODE,
                    explanation=_LITERAL_DEPENDENCY_BLOCKED_EXPLANATION,
                    rule_id=LITERAL_RULE_ID,
                ),
            )
        processing_status = (
            DetectionProcessingStatus.INCOMPLETE
            if diagnostics
            else DetectionProcessingStatus.COMPLETE
        )
        return (
            FeatureDetectionOutcome(
                feature_id=FeatureId.ACCEPTANCE_CRITERION,
                observations=observations,
                processing_status=processing_status,
                diagnostics=diagnostics,
            ),
            evidence,
        )


def _acceptance_result_span(
    observation: FeatureObservation,
    evidence_by_id: dict[str, Evidence],
) -> tuple[int, int]:
    sources = tuple(evidence_by_id[reference] for reference in observation.evidence_refs)
    literal_results = tuple(
        source
        for source in sources
        if source.rule_id == LITERAL_RULE_ID
    )
    if literal_results:
        source = max(
            literal_results,
            key=lambda item: (item.start_offset, item.end_offset),
        )
    else:
        source = max(sources, key=lambda item: (item.start_offset, item.end_offset))
    return source.start_offset, source.end_offset


def _acceptance_ref_key(source: Evidence) -> tuple[int, int, int, str]:
    precedence = 0 if source.rule_id == RULE_ID else 1
    return (
        source.start_offset,
        source.end_offset,
        precedence,
        source.evidence_id,
    )


class AcceptanceCriterionDetector:
    """Merge ACCEPT-QUANT-001 and ACCEPT-UK-001 by complete result span."""

    def __init__(
        self,
        parser: RequirementParser | None = None,
        condition_detector: ConditionContextBaselineDetector | None = None,
        expected_result_detector: ExpectedResultBaselineDetector | None = None,
        literal_expected_result_detector: ExpectedResultBaselineDetector | None = None,
        quantitative_detector: QuantitativeBaselineDetector | None = None,
    ) -> None:
        expected = (
            expected_result_detector
            if expected_result_detector is not None
            else ExpectedResultBaselineDetector()
        )
        self._quantitative = AcceptanceCriterionBaselineDetector(
            expected_result_detector=expected,
            quantitative_detector=quantitative_detector,
        )
        self._literal = LiteralAcceptanceCriterionDetector(
            parser=parser,
            condition_detector=condition_detector,
            expected_result_detector=(
                literal_expected_result_detector
                if literal_expected_result_detector is not None
                else expected
            ),
        )

    def detect(
        self,
        requirement: Requirement,
    ) -> tuple[
        FeatureDetectionOutcome[FeatureObservation],
        tuple[Evidence, ...],
    ]:
        quantitative_outcome, quantitative_evidence = self._quantitative.detect(
            requirement
        )
        literal_outcome, literal_evidence = self._literal.detect(requirement)
        evidence = tuple(
            sorted(
                quantitative_evidence + literal_evidence,
                key=_acceptance_ref_key,
            )
        )
        by_id = {source.evidence_id: source for source in evidence}
        grouped_refs: dict[tuple[int, int], set[str]] = {}
        for observation in (
            quantitative_outcome.observations + literal_outcome.observations
        ):
            result_span = _acceptance_result_span(observation, by_id)
            grouped_refs.setdefault(result_span, set()).update(
                observation.evidence_refs
            )
        observations = tuple(
            FeatureObservation(
                feature_id=FeatureId.ACCEPTANCE_CRITERION,
                evidence_refs=tuple(
                    sorted(references, key=lambda ref: _acceptance_ref_key(by_id[ref]))
                ),
            )
            for _, references in sorted(grouped_refs.items())
        )
        diagnostics = tuple(
            sorted(
                quantitative_outcome.diagnostics + literal_outcome.diagnostics,
                key=lambda item: (
                    item.candidate_span is None,
                    item.candidate_span.start_offset
                    if item.candidate_span is not None
                    else len(requirement.text) + 1,
                    item.candidate_span.end_offset
                    if item.candidate_span is not None
                    else len(requirement.text) + 1,
                    item.rule_id,
                    item.code,
                ),
            )
        )
        processing_status = (
            DetectionProcessingStatus.INCOMPLETE
            if diagnostics
            else DetectionProcessingStatus.COMPLETE
        )
        return (
            FeatureDetectionOutcome(
                feature_id=FeatureId.ACCEPTANCE_CRITERION,
                observations=observations,
                processing_status=processing_status,
                diagnostics=diagnostics,
            ),
            evidence,
        )

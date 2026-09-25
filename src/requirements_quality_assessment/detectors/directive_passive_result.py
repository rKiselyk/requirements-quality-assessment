"""RESULT-UK-003: bounded directive and simple-passive result coverage."""

from dataclasses import dataclass
import re

from ..domain.core import Evidence, FeatureId, Requirement
from ..domain.detection import (
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DiagnosticSpan,
    FeatureDetectionOutcome,
)
from ..domain.features import FeatureObservation
from ..domain.parser import ParsedRequirement, ParserOutcome, TokenAnnotation
from ..parsing import RequirementParser, SpaCyRequirementParser
from .expected_result import (
    _comparison_view,
    _is_behavior_predicate,
    _sentence_segments,
    _tokens_in_candidate,
)


RULE_ID = "RESULT-UK-003"
UNRESOLVED_CODE = "RESULT_COVERAGE_UNRESOLVED_CANDIDATE"
PARSER_BLOCKED_CODE = "RESULT_COVERAGE_PARSER_BLOCKED"

IMPERATIVE_SURFACES = frozenset(
    {
        "забезпечити",
        "реалізувати",
        "підтримувати",
        "створити",
        "додати",
        "передбачити",
    }
)
_IMPERSONAL_PASSIVE_SURFACES = frozenset({"має", "повинно"})
_SOURCE_CANDIDATE = re.compile(
    rf"^(?:{'|'.join(sorted(IMPERATIVE_SURFACES | _IMPERSONAL_PASSIVE_SURFACES))})\b",
    re.IGNORECASE,
)
_AMBIGUOUS_RELATIONS = frozenset(
    {"advcl", "acl", "ccomp", "parataxis", "conj", "orphan"}
)


@dataclass(frozen=True, slots=True)
class _AcceptedCandidate:
    start: int
    end: int


def _has_morphology(token: TokenAnnotation, name: str, value: str) -> bool:
    return any(
        feature.name == name and value in feature.values
        for feature in token.morphology
    )


def _relation_base(token: TokenAnnotation) -> str:
    return (token.dependency_relation or "").split(":", 1)[0]


def _is_root(token: TokenAnnotation) -> bool:
    return token.head_token_id is None and _comparison_view(
        token.dependency_relation or ""
    ) == "root"


def _source_covered(
    tokens: tuple[TokenAnnotation, ...], text: str, start: int, end: int
) -> bool:
    cursor = start
    for token in tokens:
        if (
            token.start_offset < cursor
            or token.end_offset <= token.start_offset
            or text[cursor:token.start_offset].strip()
        ):
            return False
        cursor = token.end_offset
    return bool(tokens) and not text[cursor:end].strip()


def _has_negation(tokens: tuple[TokenAnnotation, ...]) -> bool:
    return any(
        _relation_base(token) == "neg"
        or _has_morphology(token, "Polarity", "Neg")
        for token in tokens
    )


def _has_ambiguous_scope(
    tokens: tuple[TokenAnnotation, ...], predicate_ids: frozenset[int]
) -> bool:
    return (
        _has_negation(tokens)
        or any(
            _relation_base(token) in _AMBIGUOUS_RELATIONS
            for token in tokens
            if token.token_id in predicate_ids or _is_behavior_predicate(token)
        )
    )


def _direct_objects(
    tokens: tuple[TokenAnnotation, ...], predicate_id: int
) -> tuple[TokenAnnotation, ...]:
    return tuple(
        token
        for token in tokens
        if _relation_base(token) == "obj" and token.head_token_id == predicate_id
    )


def _imperative_state(
    tokens: tuple[TokenAnnotation, ...], start: int
) -> str:
    if not tokens:
        return "outside"
    anchor = tokens[0]
    if (
        anchor.start_offset != start
        or _comparison_view(anchor.text) not in IMPERATIVE_SURFACES
        or anchor.upos != "VERB"
        or not _has_morphology(anchor, "VerbForm", "Inf")
        or not _is_root(anchor)
    ):
        return "outside"
    if not _direct_objects(tokens, anchor.token_id):
        return "outside"
    predicates = tuple(token for token in tokens if _is_behavior_predicate(token))
    if len(predicates) != 1 or _has_ambiguous_scope(
        tokens, frozenset(token.token_id for token in predicates)
    ):
        return "unresolved"
    return "accepted"


def _passive_state(tokens: tuple[TokenAnnotation, ...], start: int) -> str:
    if not tokens:
        return "outside"
    anchor = tokens[0]
    if (
        anchor.start_offset != start
        or _comparison_view(anchor.text) not in _IMPERSONAL_PASSIVE_SURFACES
        or not _is_root(anchor)
    ):
        return "outside"
    auxiliaries = tuple(
        token
        for token in tokens
        if token.upos == "AUX"
        and _comparison_view(token.lemma or "") == "бути"
        and _relation_base(token) in {"aux", "cop"}
    )
    predicates = tuple(
        token
        for token in tokens
        if token.token_id != anchor.token_id
        and token.upos == "VERB"
        and _has_morphology(token, "VerbForm", "Fin")
        and _has_morphology(token, "Person", "0")
    )
    if len(auxiliaries) != 1 or len(predicates) != 1:
        return "outside" if not predicates else "unresolved"
    predicate = predicates[0]
    auxiliary = auxiliaries[0]
    if (
        predicate.head_token_id != anchor.token_id
        or _relation_base(predicate) not in {"xcomp", "ccomp"}
        or auxiliary.head_token_id != predicate.token_id
        or not _direct_objects(tokens, predicate.token_id)
    ):
        return "outside"
    if any(
        (token.dependency_relation or "").startswith("nsubj")
        for token in tokens
    ):
        return "outside"
    behavior = tuple(
        token
        for token in tokens
        if token.token_id != anchor.token_id and _is_behavior_predicate(token)
    )
    if len(behavior) != 1 or behavior[0] != predicate or _has_ambiguous_scope(
        tokens,
        frozenset(
            {predicate.token_id}
            | ({anchor.token_id} if _is_behavior_predicate(anchor) else set())
        ),
    ):
        return "unresolved"
    return "accepted"


def _candidate_kind(text: str, start: int, end: int) -> str | None:
    match = _SOURCE_CANDIDATE.match(_comparison_view(text[start:end]))
    if match is None:
        return None
    surface = match.group(0)
    return "imperative" if surface in IMPERATIVE_SURFACES else "passive"


def _outcome(
    observations: tuple[FeatureObservation, ...],
    diagnostics: tuple[DetectionDiagnostic, ...],
) -> FeatureDetectionOutcome[FeatureObservation]:
    return FeatureDetectionOutcome(
        feature_id=FeatureId.EXPECTED_RESULT,
        observations=observations,
        processing_status=(
            DetectionProcessingStatus.INCOMPLETE
            if diagnostics
            else DetectionProcessingStatus.COMPLETE
        ),
        diagnostics=diagnostics,
    )


class DirectivePassiveExpectedResultDetector:
    """Detect only the bounded RESULT-UK-003 coverage constructions."""

    def __init__(self, parser: RequirementParser | None = None):
        self._parser = parser if parser is not None else SpaCyRequirementParser()

    def detect(
        self, requirement: Requirement
    ) -> tuple[
        FeatureDetectionOutcome[FeatureObservation], tuple[Evidence, ...]
    ]:
        outcome, evidence, _ = self._detect(
            requirement, self._parser.parse(requirement)
        )
        return outcome, evidence

    def _detect(
        self, requirement: Requirement, parser_outcome: ParserOutcome
    ) -> tuple[
        FeatureDetectionOutcome[FeatureObservation],
        tuple[Evidence, ...],
        frozenset[tuple[int, int]],
    ]:
        text = requirement.text
        parsed = parser_outcome.parsed_requirement
        valid = (
            parsed is not None
            and parsed.requirement_id == requirement.id
            and parsed.text == text
            and bool(parsed.sentences)
            and not parser_outcome.diagnostics
        )
        source_candidate = bool(_SOURCE_CANDIDATE.match(_comparison_view(text)))
        if not valid:
            diagnostics = ()
            if source_candidate:
                diagnostics = (
                    DetectionDiagnostic(
                        code=PARSER_BLOCKED_CODE,
                        explanation=(
                            "Parser annotations required by RESULT-UK-003 are "
                            "unavailable or incomplete."
                        ),
                        rule_id=RULE_ID,
                    ),
                )
            return _outcome((), diagnostics), (), frozenset()

        assert isinstance(parsed, ParsedRequirement)
        accepted: list[_AcceptedCandidate] = []
        diagnostics: list[DetectionDiagnostic] = []
        owned: set[tuple[int, int]] = set()
        for sentence in parsed.sentences:
            for segment in _sentence_segments(text, sentence):
                kind = _candidate_kind(text, segment.start, segment.end)
                if kind is None:
                    continue
                tokens = _tokens_in_candidate(
                    parsed, segment.sentence_id, segment.start, segment.end
                )
                if not _source_covered(tokens, text, segment.start, segment.end):
                    continue
                state = (
                    _imperative_state(tokens, segment.start)
                    if kind == "imperative"
                    else _passive_state(tokens, segment.start)
                )
                if state == "outside":
                    continue
                owned.add((segment.start, segment.end))
                if state == "accepted":
                    accepted.append(_AcceptedCandidate(segment.start, segment.end))
                else:
                    diagnostics.append(
                        DetectionDiagnostic(
                            code=UNRESOLVED_CODE,
                            explanation=(
                                "RESULT-UK-003 candidate has ambiguous predicate "
                                "scope, coordination, attachment, or negation."
                            ),
                            rule_id=RULE_ID,
                            candidate_span=DiagnosticSpan(
                                text[segment.start:segment.end],
                                segment.start,
                                segment.end,
                            ),
                        )
                    )

        accepted.sort(key=lambda item: (item.start, item.end))
        diagnostics.sort(
            key=lambda item: (
                item.candidate_span.start_offset
                if item.candidate_span is not None
                else len(text) + 1,
                item.candidate_span.end_offset
                if item.candidate_span is not None
                else len(text) + 1,
            )
        )
        evidence = tuple(
            Evidence(
                evidence_id=f"{RULE_ID}:E{ordinal:03d}",
                requirement_id=requirement.id,
                feature_id=FeatureId.EXPECTED_RESULT,
                text=text[candidate.start:candidate.end],
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
        return _outcome(observations, tuple(diagnostics)), evidence, frozenset(owned)

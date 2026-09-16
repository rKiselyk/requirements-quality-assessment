"""ACCEPT-QUANT-001: quantitative acceptance-criterion composition."""

from ..domain.core import Evidence, FeatureId, Requirement
from ..domain.detection import (
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DiagnosticSpan,
    FeatureDetectionOutcome,
)
from ..domain.features import FeatureObservation
from ..domain.quantitative import (
    BoundaryInclusivity,
    ComparatorLabel,
    QuantitativeConstraintObservation,
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

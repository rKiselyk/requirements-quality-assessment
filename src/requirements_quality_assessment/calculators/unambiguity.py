"""CALC-U-MVP-001: MVP v0.1 Unambiguity characteristic calculator."""

from fractions import Fraction

from ..domain.assessment import (
    CharacteristicAssessment, CharacteristicAssessmentState, CharacteristicId,
    Finding, FindingKind,
)
from ..domain.detection import DetectionProcessingStatus
from ..domain.extraction import RequirementExtractionResult


RULE_ID = "CALC-U-MVP-001"
FINDING_RULE_ID = "FIND-U-VAGUE-001"
FINDING_CODE = "VAGUE_TERM_SIGNAL"


def _diagnostic_reasons(outcome) -> str:
    return "; ".join(
        f"{diagnostic.code}: {diagnostic.explanation}"
        for diagnostic in outcome.diagnostics
    )


class UnambiguityCalculator:
    """Computes CALC-U-MVP-001 from an immutable RequirementExtractionResult.

    Only vague_term_occurrences drives Unambiguity; the other five feature
    families are irrelevant to this characteristic. Any accepted occurrence(s),
    regardless of count and regardless of whether sibling candidates remain
    unresolved, yield 1/2 -- signal count is explainability information, not a
    cumulative numeric penalty. Absence of any accepted occurrence yields 1
    once processing is complete, or withholds the result as UNKNOWN while
    processing remains incomplete, because resolution could still surface a
    signal and move the class from 1 to 1/2. CALC-U-MVP-001 never produces 0;
    that value is reserved for a future, separately approved
    confirmed-material-ambiguity rule.
    """

    def calculate(self, result: RequirementExtractionResult) -> CharacteristicAssessment:
        outcome = result.features.vague_term_occurrences

        if outcome.observations:
            return self._computed_from_signals(result, outcome)

        if outcome.processing_status is DetectionProcessingStatus.COMPLETE:
            return self._computed(
                Fraction(1, 1),
                f"{RULE_ID} computed 1: the approved MVP vague-term detector found "
                "no supported signal after complete processing; this is absence of "
                "the supported signal class, not universal proof that the "
                "requirement has exactly one semantically valid interpretation in "
                "every possible context.",
            )

        return self._unknown(
            "no accepted vague-term occurrence, and vague-term-occurrence "
            f"processing is incomplete ({_diagnostic_reasons(outcome)}); resolving "
            "the unresolved candidate could still establish an accepted supported "
            "signal and change the class from 1 to 1/2."
        )

    def _computed_from_signals(self, result, outcome) -> CharacteristicAssessment:
        evidence_by_id = {item.evidence_id: item for item in result.evidence}

        def source_offset(occurrence) -> int:
            return min(
                evidence_by_id[ref].start_offset for ref in occurrence.evidence_refs
            )

        ordered = sorted(
            enumerate(outcome.observations),
            key=lambda indexed: (source_offset(indexed[1]), indexed[0]),
        )

        findings = tuple(
            Finding(
                finding_id=f"{FINDING_RULE_ID}:F{position:03d}",
                requirement_id=result.requirement.id,
                characteristic_id=CharacteristicId.UNAMBIGUITY,
                kind=FindingKind.SIGNAL,
                code=FINDING_CODE,
                rule_id=FINDING_RULE_ID,
                criterion_id=None,
                evidence_refs=occurrence.evidence_refs,
                explanation=(
                    f"{FINDING_RULE_ID} matched the approved seed literal "
                    f"{occurrence.matched_literal!r} (uk_vague_terms_v1) as a "
                    "potential ambiguity indicator; this is not a confirmed "
                    "ambiguity or a confirmed quality defect."
                ),
            )
            for position, (_, occurrence) in enumerate(ordered, start=1)
        )

        explanation = (
            f"{RULE_ID} computed 1/2: {len(findings)} accepted vague-term "
            f"occurrence(s) were each converted to one {FINDING_CODE} finding "
            f"under {FINDING_RULE_ID}; every accepted signal maps to the same "
            "1/2 class (signal count is not cumulative), and each Finding is an "
            "indicator, not a confirmed ambiguity."
        )
        if outcome.processing_status is DetectionProcessingStatus.INCOMPLETE:
            explanation += (
                " Vague-term-occurrence processing is additionally incomplete "
                f"({_diagnostic_reasons(outcome)}); additional unresolved "
                "candidates cannot change the class below 1/2."
            )

        return self._computed(Fraction(1, 2), explanation, findings)

    @staticmethod
    def _computed(
        value: Fraction, explanation: str, findings: tuple[Finding, ...] = (),
    ) -> CharacteristicAssessment:
        return CharacteristicAssessment(
            characteristic_id=CharacteristicId.UNAMBIGUITY,
            state=CharacteristicAssessmentState.COMPUTED,
            value=value,
            assessment_rule_id=RULE_ID,
            findings=findings,
            explanation=explanation,
        )

    @staticmethod
    def _unknown(reason: str) -> CharacteristicAssessment:
        return CharacteristicAssessment(
            characteristic_id=CharacteristicId.UNAMBIGUITY,
            state=CharacteristicAssessmentState.UNKNOWN,
            value=None,
            assessment_rule_id=None,
            findings=(),
            explanation=f"Unambiguity withheld under {RULE_ID}: {reason}",
        )

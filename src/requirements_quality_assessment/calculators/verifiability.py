"""CALC-V-MVP-001: MVP v0.1 Verifiability characteristic calculator."""

from fractions import Fraction

from ..domain.assessment import (
    CharacteristicAssessment, CharacteristicAssessmentState, CharacteristicId,
)
from ..domain.detection import DetectionProcessingStatus
from ..domain.extraction import RequirementExtractionResult


RULE_ID = "CALC-V-MVP-001"

_LOWER_TIER_FAMILIES = (
    ("quantitative_constraints", "quantitative constraint"),
    ("verification_methods", "verification method"),
)


def _diagnostic_reasons(outcome) -> str:
    return "; ".join(
        f"{diagnostic.code}: {diagnostic.explanation}"
        for diagnostic in outcome.diagnostics
    )


class VerifiabilityCalculator:
    """Computes CALC-V-MVP-001 from an immutable RequirementExtractionResult.

    acceptance_criteria, quantitative_constraints, and verification_methods are
    alternative evidence paths, not additive/mandatory criteria: an accepted
    acceptance criterion alone yields 1; absent that, an accepted quantitative
    constraint or verification method yields 1/2; absent all three after
    complete relevant processing, 0. An unresolved family withholds the result
    only when resolving it could still change the numeric class.
    """

    def calculate(self, result: RequirementExtractionResult) -> CharacteristicAssessment:
        acceptance = result.features.acceptance_criteria

        if acceptance.observations:
            return self._computed(
                Fraction(1, 1),
                f"{RULE_ID} computed 1: an accepted acceptance criterion establishes full "
                "Verifiability; incomplete or absent lower-tier (quantitative constraint, "
                "verification method) evidence cannot change this class, and additional "
                "unresolved acceptance-criterion candidates cannot raise it further.",
            )

        if acceptance.processing_status is DetectionProcessingStatus.INCOMPLETE:
            return self._unknown(
                "no accepted acceptance criterion, and acceptance criterion detection is "
                f"incomplete ({_diagnostic_reasons(acceptance)}); resolving it could still "
                "establish an accepted acceptance criterion and change the class to 1."
            )

        lower_tier = [
            (attribute_name, label, getattr(result.features, attribute_name))
            for attribute_name, label in _LOWER_TIER_FAMILIES
        ]
        accepted_lower = [
            (label, outcome) for _, label, outcome in lower_tier if outcome.observations
        ]
        if accepted_lower:
            contributors = " and ".join(label for label, _ in accepted_lower)
            return self._computed(
                Fraction(1, 2),
                f"{RULE_ID} computed 1/2: no accepted acceptance criterion (family complete, "
                f"absent); an accepted {contributors} establishes partial Verifiability; "
                "repeated lower-tier observations and any unresolved sibling lower-tier "
                "candidate cannot change this class.",
            )

        unresolved_lower = [
            (label, outcome) for _, label, outcome in lower_tier
            if outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
        ]
        if unresolved_lower:
            reasons = "; ".join(
                f"{label} (unresolved: {_diagnostic_reasons(outcome)})"
                for label, outcome in unresolved_lower
            )
            return self._unknown(
                "no accepted acceptance criterion (family complete, absent), no accepted "
                f"quantitative constraint or verification method, and {reasons}; resolving "
                "the unresolved candidate could still establish an accepted quantitative "
                "constraint or verification method and change the class from 0 to 1/2."
            )

        return self._computed(
            Fraction(0, 1),
            f"{RULE_ID} computed 0: acceptance criterion, quantitative constraint, and "
            "verification method families are all complete with no accepted observation "
            "(a completed absence of operationalization evidence, not a Finding).",
        )

    @staticmethod
    def _computed(value: Fraction, explanation: str) -> CharacteristicAssessment:
        return CharacteristicAssessment(
            characteristic_id=CharacteristicId.VERIFIABILITY,
            state=CharacteristicAssessmentState.COMPUTED,
            value=value,
            assessment_rule_id=RULE_ID,
            findings=(),
            explanation=explanation,
        )

    @staticmethod
    def _unknown(reason: str) -> CharacteristicAssessment:
        return CharacteristicAssessment(
            characteristic_id=CharacteristicId.VERIFIABILITY,
            state=CharacteristicAssessmentState.UNKNOWN,
            value=None,
            assessment_rule_id=None,
            findings=(),
            explanation=f"Verifiability withheld under {RULE_ID}: {reason}",
        )

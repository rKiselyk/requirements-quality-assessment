"""CALC-C-MVP-001: MVP v0.1 Completeness characteristic calculator."""

from fractions import Fraction

from ..domain.assessment import (
    CharacteristicAssessment, CharacteristicAssessmentState, CharacteristicId,
)
from ..domain.detection import DetectionProcessingStatus
from ..domain.extraction import RequirementExtractionResult


RULE_ID = "CALC-C-MVP-001"

_REQUIRED_FAMILIES = (
    ("condition_contexts", "condition/context"),
    ("expected_results", "expected result/reaction"),
    ("acceptance_criteria", "acceptance/fulfilment criterion"),
)


def _diagnostic_reasons(outcome) -> str:
    return "; ".join(
        f"{diagnostic.code}: {diagnostic.explanation}"
        for diagnostic in outcome.diagnostics
    )


class CompletenessCalculator:
    """Computes CALC-C-MVP-001 from an immutable RequirementExtractionResult."""

    def calculate(self, result: RequirementExtractionResult) -> CharacteristicAssessment:
        families = [
            (attribute_name, label, getattr(result.features, attribute_name))
            for attribute_name, label in _REQUIRED_FAMILIES
        ]

        unresolved = [
            (label, outcome) for _, label, outcome in families
            if outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
        ]
        if unresolved:
            reasons = "; ".join(
                f"{label} (unresolved: {_diagnostic_reasons(outcome)})"
                for label, outcome in unresolved
            )
            return CharacteristicAssessment(
                characteristic_id=CharacteristicId.COMPLETENESS,
                state=CharacteristicAssessmentState.UNKNOWN,
                value=None,
                assessment_rule_id=None,
                findings=(),
                explanation=(
                    f"Completeness withheld under {RULE_ID}: required detector "
                    f"processing is incomplete for {reasons}."
                ),
            )

        contributions = [
            (label, bool(outcome.observations)) for _, label, outcome in families
        ]
        detected_count = sum(1 for _, detected in contributions if detected)
        value = Fraction(detected_count, 3)
        criteria_summary = "; ".join(
            f"{label}={'DETECTED' if detected else 'NOT_DETECTED'}"
            for label, detected in contributions
        )
        return CharacteristicAssessment(
            characteristic_id=CharacteristicId.COMPLETENESS,
            state=CharacteristicAssessmentState.COMPUTED,
            value=value,
            assessment_rule_id=RULE_ID,
            findings=(),
            explanation=(
                f"{RULE_ID} computed {value} from {detected_count}/3 required "
                f"criteria detected: {criteria_summary}."
            ),
        )

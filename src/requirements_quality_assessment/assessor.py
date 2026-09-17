"""Replaceable boundary and production orchestration for characteristic assessment."""

from typing import Protocol

from .calculators import (
    CompletenessCalculator,
    UnambiguityCalculator,
    VerifiabilityCalculator,
)
from .domain import (
    CharacteristicAssessment,
    RequirementExtractionResult,
    RequirementQualityProfile,
)


class _CharacteristicCalculator(Protocol):
    def calculate(
        self, result: RequirementExtractionResult
    ) -> CharacteristicAssessment:
        ...


class RequirementQualityAssessor:
    """Assemble the three approved characteristic calculator results without reinterpretation."""

    def __init__(
        self,
        completeness_calculator: _CharacteristicCalculator | None = None,
        verifiability_calculator: _CharacteristicCalculator | None = None,
        unambiguity_calculator: _CharacteristicCalculator | None = None,
    ) -> None:
        self._completeness_calculator = (
            completeness_calculator
            if completeness_calculator is not None
            else CompletenessCalculator()
        )
        self._verifiability_calculator = (
            verifiability_calculator
            if verifiability_calculator is not None
            else VerifiabilityCalculator()
        )
        self._unambiguity_calculator = (
            unambiguity_calculator
            if unambiguity_calculator is not None
            else UnambiguityCalculator()
        )

    def assess(
        self, result: RequirementExtractionResult
    ) -> RequirementQualityProfile:
        completeness = self._completeness_calculator.calculate(result)
        verifiability = self._verifiability_calculator.calculate(result)
        unambiguity = self._unambiguity_calculator.calculate(result)

        return RequirementQualityProfile(
            completeness=completeness,
            verifiability=verifiability,
            unambiguity=unambiguity,
        )

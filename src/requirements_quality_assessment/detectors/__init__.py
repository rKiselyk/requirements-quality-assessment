"""Independently composable feature detectors."""

from .condition_context import ConditionContextBaselineDetector
from .expected_result import ExpectedResultBaselineDetector
from .quantitative import QuantitativeBaselineDetector
from .vague_terms import UkVagueTermDetector

__all__ = [
    "ConditionContextBaselineDetector",
    "ExpectedResultBaselineDetector",
    "QuantitativeBaselineDetector",
    "UkVagueTermDetector",
]

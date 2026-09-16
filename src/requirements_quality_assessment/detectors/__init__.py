"""Independently composable feature detectors."""

from .condition_context import ConditionContextBaselineDetector
from .quantitative import QuantitativeBaselineDetector
from .vague_terms import UkVagueTermDetector

__all__ = [
    "ConditionContextBaselineDetector",
    "QuantitativeBaselineDetector",
    "UkVagueTermDetector",
]

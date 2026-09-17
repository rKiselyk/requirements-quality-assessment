"""Approved immutable domain data contracts for MVP v0.1."""

from .assessment import (
    CharacteristicAssessment, CharacteristicAssessmentState, CharacteristicId,
    Finding, FindingKind,
)
from .core import CriterionApplicability, Evidence, FeatureId, Requirement
from .detection import (
    DetectionDiagnostic, DetectionProcessingStatus, DetectionStatus,
    DiagnosticSpan, FeatureDetectionOutcome,
)
from .extraction import RequirementExtractionResult
from .features import FeatureObservation, RequirementFeatures, VagueTermOccurrence
from .parser import (
    MorphFeature, ParsedRequirement, ParserDiagnostic, ParserDiagnosticCode,
    ParserMetadata, ParserOutcome, SentenceAnnotation, TokenAnnotation,
)
from .quantitative import (
    BoundaryInclusivity, ComparatorComponent, ComparatorLabel,
    NumericValueComponent, QuantitativeComponentName,
    QuantitativeConstraintObservation, TextComponent, UnitComponent, UnitLabel,
)

__all__ = [
    "BoundaryInclusivity", "CharacteristicAssessment", "CharacteristicAssessmentState",
    "CharacteristicId", "ComparatorComponent", "ComparatorLabel",
    "CriterionApplicability", "DetectionDiagnostic", "DetectionProcessingStatus",
    "DetectionStatus", "DiagnosticSpan", "Evidence", "FeatureDetectionOutcome",
    "FeatureId", "FeatureObservation", "Finding", "FindingKind", "MorphFeature",
    "NumericValueComponent", "ParsedRequirement", "ParserDiagnostic",
    "ParserDiagnosticCode", "ParserMetadata", "ParserOutcome",
    "QuantitativeComponentName", "QuantitativeConstraintObservation",
    "Requirement", "RequirementExtractionResult", "RequirementFeatures",
    "SentenceAnnotation", "TextComponent",
    "TokenAnnotation", "UnitComponent", "UnitLabel", "VagueTermOccurrence",
]

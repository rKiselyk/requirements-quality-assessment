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
from .profile import RequirementQualityProfile
from .quantitative import (
    BoundaryInclusivity, ComparatorComponent, ComparatorLabel,
    NumericValueComponent, QuantitativeComponentName,
    QuantitativeConstraintObservation, TextComponent, UnitComponent, UnitLabel,
)
from .specification_profile import (
    SpecificationCharacteristicAggregate, SpecificationQualityProfile,
)
from .trace import (
    COVERAGE_PROFILE_ID, CharacteristicTrace, FeatureInputTrace,
    RequirementAssessmentRecord, RequirementAssessmentTrace,
    TraceDecisionCode, TraceEffectCode,
)

__all__ = [
    "BoundaryInclusivity", "CharacteristicAssessment", "CharacteristicAssessmentState",
    "CharacteristicId", "CharacteristicTrace", "ComparatorComponent", "ComparatorLabel",
    "COVERAGE_PROFILE_ID",
    "CriterionApplicability", "DetectionDiagnostic", "DetectionProcessingStatus",
    "DetectionStatus", "DiagnosticSpan", "Evidence", "FeatureDetectionOutcome",
    "FeatureId", "FeatureInputTrace", "FeatureObservation", "Finding", "FindingKind",
    "MorphFeature",
    "NumericValueComponent", "ParsedRequirement", "ParserDiagnostic",
    "ParserDiagnosticCode", "ParserMetadata", "ParserOutcome",
    "QuantitativeComponentName", "QuantitativeConstraintObservation",
    "Requirement", "RequirementAssessmentRecord", "RequirementAssessmentTrace",
    "RequirementExtractionResult", "RequirementFeatures", "RequirementQualityProfile",
    "SentenceAnnotation",
    "SpecificationCharacteristicAggregate", "SpecificationQualityProfile",
    "TextComponent", "TokenAnnotation", "TraceDecisionCode", "TraceEffectCode",
    "UnitComponent", "UnitLabel",
    "VagueTermOccurrence",
]

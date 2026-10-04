"""Lossless projection of accepted domain records into API response models."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from typing import Any

from ..cross_analysis.specification import SpecificationAssessmentResult
from ..domain import FeatureDetectionOutcome, RequirementAssessmentRecord
from .schemas import AnalyzeResponse


def _canonical(value: Any) -> Any:
    """Convert typed domain data without rounding or semantic reinterpretation."""

    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [_canonical(item) for item in value]
    if isinstance(value, list):
        return [_canonical(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in value.items()}
    if is_dataclass(value):
        return {
            item.name: _canonical(getattr(value, item.name))
            for item in fields(value)
        }
    raise TypeError(f"unsupported API serialization type: {type(value).__name__}")


def _feature_outcome(value: FeatureDetectionOutcome) -> dict[str, Any]:
    projected = _canonical(value)
    projected["status"] = value.status.value
    return projected


def _record(record: RequirementAssessmentRecord) -> dict[str, Any]:
    extraction = record.extraction_result
    features = extraction.features
    return {
        "requirement": _canonical(extraction.requirement),
        "features": {
            item.name: _feature_outcome(getattr(features, item.name))
            for item in fields(features)
        },
        "evidence": _canonical(extraction.evidence),
        "quality_profile": _canonical(record.quality_profile),
        "trace": _canonical(record.trace),
    }


_SECTIONS = (
    ("overview", "AVAILABLE", None),
    ("requirements", "AVAILABLE", None),
    ("specification", "AVAILABLE", None),
    ("audit", "AVAILABLE", None),
    ("product_quality", "UNAVAILABLE", "EXTERNAL_EVIDENCE_NOT_SUPPLIED"),
    ("risk", "UNAVAILABLE", "CONFIRMED_PROBLEM_AND_RISK_INPUTS_NOT_AVAILABLE"),
    ("corrective_actions", "UNAVAILABLE", "CONFIRMED_PROBLEM_NOT_AVAILABLE"),
    ("process", "UNAVAILABLE", "FULL_MODEL_LIFECYCLE_NOT_INVOKED"),
    ("reassessment", "UNAVAILABLE", "INITIAL_ASSESSMENT_HAS_NO_REASSESSMENT"),
    ("comparison", "UNAVAILABLE", "INITIAL_ASSESSMENT_HAS_NO_COMPARISON"),
)


def serialize_analysis(result: SpecificationAssessmentResult) -> AnalyzeResponse:
    """Project one completed accepted result into canonical HTTP transport data."""

    assessment = result.specification_assessment
    payload = {
        "contract_version": "research-api-v1",
        "analysis_case": "INITIAL",
        "requirements": [_record(record) for record in result.records],
        "specification": {
            "snapshot_id": result.snapshot_id.value,
            "quality_profile": _canonical(assessment.quality_profile),
            "qb_consistency": _canonical(assessment.qb_consistency),
            "cross_results": _canonical(result.cross_results),
            "materiality": _canonical(result.materiality),
            "projection_snapshot": _canonical(result.projection.snapshot),
        },
        "section_availability": [
            {"section": section, "availability": availability, "reason_code": reason}
            for section, availability, reason in _SECTIONS
        ],
        "limitations": [
            "NO_COMBINED_QUALITY_SCORE",
            "TEXT_ONLY_INITIAL_ASSESSMENT",
            "UKRAINIAN_LANGUAGE_PROFILE",
            "BOUNDED_RESEARCH_MODEL",
        ],
    }
    return AnalyzeResponse.model_validate(payload)


__all__ = ["serialize_analysis"]

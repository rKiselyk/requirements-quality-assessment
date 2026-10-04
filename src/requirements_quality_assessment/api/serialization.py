"""Lossless projection of accepted domain records into API response models."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any

from ..cross_analysis.specification import SpecificationAssessmentResult
from ..domain import FeatureDetectionOutcome, RequirementAssessmentRecord
from ..full_model.domain import FullModelResult
from ..full_model.controlled_scenario import ControlledResearchReferenceScenario
from .schemas import AnalyzeResponse, ReassessmentPriorContext


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


_INITIAL_SECTIONS = (
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


def _specification(result: SpecificationAssessmentResult) -> dict[str, Any]:
    assessment = result.specification_assessment
    return {
        "snapshot_id": result.snapshot_id.value,
        "quality_profile": _canonical(assessment.quality_profile),
        "qb_consistency": _canonical(assessment.qb_consistency),
        "cross_results": _canonical(result.cross_results),
        "materiality": _canonical(result.materiality),
        "projection_snapshot": _canonical(result.projection.snapshot),
    }


def _section_payload(sections) -> list[dict[str, Any]]:
    return [
        {"section": section, "availability": availability, "reason_code": reason}
        for section, availability, reason in sections
    ]


def _full_model_payload(result: FullModelResult) -> dict[str, Any]:
    """Serialize produced scientific records once; omit the duplicate report bundle."""

    return {
        item.name: _canonical(getattr(result, item.name))
        for item in fields(result)
        if item.name != "report_bundle"
    }


def build_reassessment_context(
    result: FullModelResult,
    scenario: ControlledResearchReferenceScenario,
) -> ReassessmentPriorContext:
    """Project the accepted lifecycle prerequisites needed for stateless replay."""

    context = {
        "scenario": {
            "id": scenario.scenario_id,
            "version": scenario.scenario_version,
        },
        "initial_specification": _canonical(result.initial_specification),
        "initial_specification_assessment": _canonical(
            result.initial_specification_assessment
        ),
        "predecessor_process_state": _canonical(result.process_v1),
        "corrective_action_resolution": _canonical(
            result.corrective_action_resolution
        ),
        "action_application": _canonical(result.action_application),
        "external_revision": _canonical(result.external_revision),
        "revised_specification": _canonical(result.revised_specification),
        "evidence_reuse_decisions": _canonical(
            result.reassessment.context.evidence_reuse_decisions
        ),
        "reassessment_identity": {
            "reassessment_id": result.reassessment.reassessment_id,
            "reassessment_version": result.reassessment.reassessment_version,
            "child_process_state_ref": _canonical(
                result.reassessment.child_process_state_ref
            ),
            "component_version_set": _canonical(
                result.reassessment.context.component_version_set
            ),
        },
        "successor_process_state": _canonical(result.process_v2),
        "process_transition": _canonical(result.process_transition),
        "comparisons": _canonical(result.comparisons),
    }
    encoded = json.dumps(
        context,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    context["context_digest"] = "sha256:" + sha256(encoded).hexdigest()
    return ReassessmentPriorContext.model_validate(context)


def serialize_initial(result: SpecificationAssessmentResult) -> AnalyzeResponse:
    """Project one ordinary initial specification assessment."""

    payload = {
        "contract_version": "research-api-v1",
        "analysis_case": "INITIAL",
        "controlled_scenario": None,
        "requirements": [_record(record) for record in result.records],
        "specification": _specification(result),
        "section_availability": [
            {"section": section, "availability": availability, "reason_code": reason}
            for section, availability, reason in _INITIAL_SECTIONS
        ],
        "full_model": None,
        "reassessment_context": None,
        "limitations": [
            "NO_COMBINED_QUALITY_SCORE",
            "TEXT_ONLY_INITIAL_ASSESSMENT",
            "UKRAINIAN_LANGUAGE_PROFILE",
            "BOUNDED_RESEARCH_MODEL",
        ],
    }
    return AnalyzeResponse.model_validate(payload)


def _lifecycle_sections(result: FullModelResult) -> list[dict[str, Any]]:
    sections = (
        ("overview", "AVAILABLE", None),
        ("requirements", "AVAILABLE", None),
        ("specification", "AVAILABLE", None),
        ("product_quality", "AVAILABLE", None),
        ("risk", "AVAILABLE", None),
        ("corrective_actions", "AVAILABLE", None),
        ("process", "AVAILABLE", None),
        ("audit", "AVAILABLE", None),
        (
            "reassessment",
            "AVAILABLE" if result.reassessment is not None else "UNAVAILABLE",
            None if result.reassessment is not None else "REASSESSMENT_NOT_PRODUCED",
        ),
        (
            "comparison",
            "AVAILABLE" if result.comparisons else "UNAVAILABLE",
            None if result.comparisons else "COMPARISONS_NOT_PRODUCED",
        ),
    )
    return _section_payload(sections)


def serialize_controlled_demo(
    result: FullModelResult,
    scenario: ControlledResearchReferenceScenario,
) -> AnalyzeResponse:
    source = result.initial_specification_assessment
    return AnalyzeResponse.model_validate({
        "contract_version": "research-api-v1",
        "analysis_case": "CONTROLLED_DEMO",
        "controlled_scenario": {
            "id": scenario.scenario_id,
            "version": scenario.scenario_version,
        },
        "requirements": [_record(record) for record in source.records],
        "specification": _specification(source),
        "section_availability": _lifecycle_sections(result),
        "full_model": _full_model_payload(result),
        "reassessment_context": build_reassessment_context(result, scenario),
        "limitations": [
            "NO_COMBINED_QUALITY_SCORE",
            "CONTROLLED_RESEARCH_FIXTURE_DATA",
            "PROVISIONAL_NOT_CALIBRATED",
            "NO_CAUSAL_OR_RELEASE_CLAIM",
            "BOUNDED_RESEARCH_MODEL",
        ],
    })


def serialize_reassessment(
    result: FullModelResult,
    scenario: ControlledResearchReferenceScenario,
) -> AnalyzeResponse:
    core_v2 = result.reassessment.produced_results[0]
    source = core_v2.specification_assessment
    return AnalyzeResponse.model_validate({
        "contract_version": "research-api-v1",
        "analysis_case": "REASSESSMENT",
        "controlled_scenario": {
            "id": scenario.scenario_id,
            "version": scenario.scenario_version,
        },
        "requirements": [_record(record) for record in core_v2.requirement_records],
        "specification": _specification(source),
        "section_availability": _lifecycle_sections(result),
        "full_model": _full_model_payload(result),
        "reassessment_context": build_reassessment_context(result, scenario),
        "limitations": [
            "NO_ARBITRARY_V1_V2_COMPARISON",
            "CONTROLLED_RESEARCH_FIXTURE_DATA",
            "PROVISIONAL_NOT_CALIBRATED",
            "NO_CAUSAL_OR_RELEASE_CLAIM",
            "BOUNDED_RESEARCH_MODEL",
        ],
    })


__all__ = [
    "build_reassessment_context",
    "serialize_controlled_demo",
    "serialize_initial",
    "serialize_reassessment",
]

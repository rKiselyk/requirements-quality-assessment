"""Pydantic transport contracts for Research API v1."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RequirementInput(ApiModel):
    """One source-ordered requirement; scientific IDs are server-generated."""

    text: str = Field(strict=True)

    @field_validator("text")
    @classmethod
    def trim_text(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("text must contain non-whitespace characters")
        return trimmed


class ControlledScenarioIdentity(ApiModel):
    id: str = Field(strict=True)
    version: str = Field(strict=True)


class InitialAnalyzeRequest(ApiModel):
    case: Literal["INITIAL"]
    requirements: list[RequirementInput]


class ControlledDemoAnalyzeRequest(ApiModel):
    case: Literal["CONTROLLED_DEMO"]
    scenario: ControlledScenarioIdentity


class ReassessmentPriorContext(ApiModel):
    """Canonical stateless lifecycle prerequisites returned by CONTROLLED_DEMO."""

    scenario: ControlledScenarioIdentity
    context_digest: str
    initial_specification: dict[str, Any]
    initial_specification_assessment: dict[str, Any]
    predecessor_process_state: dict[str, Any]
    corrective_action_resolution: dict[str, Any]
    action_application: dict[str, Any]
    external_revision: dict[str, Any]
    revised_specification: dict[str, Any]
    evidence_reuse_decisions: list[dict[str, Any]]
    reassessment_identity: dict[str, Any]
    successor_process_state: dict[str, Any]
    process_transition: dict[str, Any]
    comparisons: list[dict[str, Any]]


class ReassessmentAnalyzeRequest(ApiModel):
    case: Literal["REASSESSMENT"]
    requirements: list[RequirementInput]
    prior_context: ReassessmentPriorContext


AnalyzeRequest = Annotated[
    InitialAnalyzeRequest | ControlledDemoAnalyzeRequest | ReassessmentAnalyzeRequest,
    Field(discriminator="case"),
]


class ExactFractionResponse(ApiModel):
    numerator: int
    denominator: int


class RequirementIdentityResponse(ApiModel):
    id: str
    source_line: int
    text: str


class EvidenceResponse(ApiModel):
    evidence_id: str
    requirement_id: str
    feature_id: str
    text: str
    start_offset: int
    end_offset: int
    rule_id: str


class DiagnosticSpanResponse(ApiModel):
    text: str
    start_offset: int
    end_offset: int


class DetectionDiagnosticResponse(ApiModel):
    code: str
    explanation: str
    rule_id: str
    candidate_span: DiagnosticSpanResponse | None


class FeatureDetectionResponse(ApiModel):
    feature_id: str
    status: str
    processing_status: str
    observations: list[dict[str, Any]]
    diagnostics: list[DetectionDiagnosticResponse]


class RequirementFeaturesResponse(ApiModel):
    condition_contexts: FeatureDetectionResponse
    expected_results: FeatureDetectionResponse
    acceptance_criteria: FeatureDetectionResponse
    quantitative_constraints: FeatureDetectionResponse
    verification_methods: FeatureDetectionResponse
    vague_term_occurrences: FeatureDetectionResponse


class FindingResponse(ApiModel):
    finding_id: str
    requirement_id: str
    characteristic_id: str
    kind: str
    code: str
    rule_id: str
    criterion_id: str | None
    evidence_refs: list[str]
    explanation: str


class CharacteristicAssessmentResponse(ApiModel):
    characteristic_id: str
    state: str
    value: ExactFractionResponse | None
    assessment_rule_id: str | None
    findings: list[FindingResponse]
    explanation: str


class RequirementQualityProfileResponse(ApiModel):
    completeness: CharacteristicAssessmentResponse
    verifiability: CharacteristicAssessmentResponse
    unambiguity: CharacteristicAssessmentResponse


class FeatureInputTraceResponse(ApiModel):
    feature_id: str
    applicability: str | None
    observation_indexes: list[int]
    diagnostic_indexes: list[int]
    effect_code: str


class CharacteristicTraceResponse(ApiModel):
    characteristic_id: str
    governing_rule_id: str
    decision_code: str
    inputs: list[FeatureInputTraceResponse]
    finding_refs: list[str]


class RequirementAssessmentTraceResponse(ApiModel):
    requirement_id: str
    characteristics: list[CharacteristicTraceResponse]
    coverage_profile_id: str


class RequirementResultResponse(ApiModel):
    requirement: RequirementIdentityResponse
    features: RequirementFeaturesResponse
    evidence: list[EvidenceResponse]
    quality_profile: RequirementQualityProfileResponse
    trace: RequirementAssessmentTraceResponse


class SpecificationAggregateResponse(ApiModel):
    characteristic_id: str
    state: str
    value: ExactFractionResponse | None
    computed_count: int
    unknown_count: int
    not_applicable_count: int
    total_count: int
    aggregation_rule_id: str


class SpecificationQualityProfileResponse(ApiModel):
    completeness: SpecificationAggregateResponse
    verifiability: SpecificationAggregateResponse
    unambiguity: SpecificationAggregateResponse


class SpecificationResultResponse(ApiModel):
    snapshot_id: str
    quality_profile: SpecificationQualityProfileResponse
    qb_consistency: dict[str, Any]
    cross_results: list[dict[str, Any]]
    materiality: dict[str, Any]
    projection_snapshot: dict[str, Any]


class SectionAvailabilityResponse(ApiModel):
    section: str
    availability: Literal["AVAILABLE", "UNAVAILABLE"]
    reason_code: str | None


class AnalyzeResponse(ApiModel):
    contract_version: Literal["research-api-v1"]
    analysis_case: Literal["INITIAL", "CONTROLLED_DEMO", "REASSESSMENT"]
    controlled_scenario: ControlledScenarioIdentity | None
    requirements: list[RequirementResultResponse]
    specification: SpecificationResultResponse
    section_availability: list[SectionAvailabilityResponse]
    full_model: dict[str, Any] | None
    reassessment_context: ReassessmentPriorContext | None
    limitations: list[str]


class HealthResponse(ApiModel):
    status: Literal["ok"]


class ErrorDetail(ApiModel):
    code: str
    details: dict[str, Any]
    path: list[str | int] | None = None


class ErrorResponse(ApiModel):
    error: ErrorDetail

"""Immutable domain records for the bounded Full Model v0.1 ``M_quality``.

These records describe one observed response-time conformance indicator. They
deliberately do not model predicted or complete Performance Efficiency.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from ..domain import UnitLabel
from ..dynamic_evidence import (
    Applicability,
    ConformanceAssessmentId,
    ConformanceOutcome,
    CriterionContextIdentity,
    DynamicEvidenceAssessmentRef,
    DynamicMetricRef,
    EnvironmentRef,
    FullModelStatus,
    ObservationCollectionRef,
    ProductRef,
    RESPONSE_TIME_METRIC_REF,
)
from ..dynamic_evidence.domain import CriterionRef, DynamicObservationRef
from ..metrics import (
    FULL_MODEL_CONTRACT_REF,
    ArtifactRef,
    AssessmentRef,
    ContractRef,
    MetricEntryId,
    MetricProfileId,
    NumericRepresentation,
    RequirementSubjectRef,
    RuleRef,
    RuleVersionAuthority,
)
from ..performance_efficiency import (
    PE_FEATURE_REGISTRY,
    FeatureDiagnosticRef,
    FeatureEvidenceRef,
    PerformanceEfficiencyFeatureEntryId,
    PerformanceEfficiencyFeatureProfileId,
    ProcessStage,
    ProcessStateRef,
    ProductQualityCharacteristicId,
    QbCrossResultRef,
)
from ..performance_efficiency.domain import FeatureSourceRef


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


def _typed_tuple(value: object, item_types: type | tuple[type, ...], name: str) -> None:
    if not isinstance(value, tuple) or any(
        not isinstance(item, item_types) for item in value
    ):
        raise TypeError(f"{name} must be a tuple of approved values")


class ProductQualityResultKind(str, Enum):
    OBSERVED_REFERENCE_INDICATOR = "OBSERVED_REFERENCE_INDICATOR"


class CalibrationStatus(str, Enum):
    EXPERIMENTALLY_CALIBRATED = "EXPERIMENTALLY_CALIBRATED"
    PROVISIONAL_NOT_CALIBRATED = "PROVISIONAL_NOT_CALIBRATED"
    EXPERIMENTAL_CALIBRATION_REQUIRED = "EXPERIMENTAL_CALIBRATION_REQUIRED"


class ProductQualityScopeKind(str, Enum):
    SINGLE_CRITERION_SINGLE_OBSERVATION = "SINGLE_CRITERION_SINGLE_OBSERVATION"


class FullCharacteristicCoverage(str, Enum):
    NOT_ESTABLISHED = "NOT_ESTABLISHED"


class EvidenceCoverageKind(str, Enum):
    BOUNDED_REQUIRED_CHANNEL_INVENTORY = "BOUNDED_REQUIRED_CHANNEL_INVENTORY"


class EvidenceProcedureScope(str, Enum):
    SINGLE_RESPONSE_TIME_CRITERION = "SINGLE_RESPONSE_TIME_CRITERION"


class BoundedProcedureState(str, Enum):
    COMPLETE = "COMPLETE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"
    UNRESOLVED = "UNRESOLVED"
    UNSUPPORTED = "UNSUPPORTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvidenceChannelId(str, Enum):
    RESPONSE_TIME_CRITERION = "RESPONSE_TIME_CRITERION"
    TARGET_QB_GATE = "TARGET_QB_GATE"
    RESPONSE_TIME_OBSERVATION = "RESPONSE_TIME_OBSERVATION"
    RESPONSE_TIME_CONFORMANCE = "RESPONSE_TIME_CONFORMANCE"
    REQUIREMENT_C_CONTEXT = "REQUIREMENT_C_CONTEXT"
    REQUIREMENT_V_CONTEXT = "REQUIREMENT_V_CONTEXT"
    REQUIREMENT_U_CONTEXT = "REQUIREMENT_U_CONTEXT"


class EvidenceRole(str, Enum):
    REQUIRED = "REQUIRED"
    GATE = "GATE"
    CONTEXT_ONLY = "CONTEXT_ONLY"


class ProductQualityNonClaim(str, Enum):
    NOT_COMPLETE_PERFORMANCE_EFFICIENCY = "NC-PE-001"
    NOT_PREDICTED_PRODUCT_QUALITY = "NC-PE-002"
    NOT_ACTUAL_AGGREGATED_Y_PE = "NC-PE-003"
    NOT_PROBABILITY_CONFIDENCE_RELIABILITY_OR_ACCURACY = "NC-PE-004"
    NO_MODEL_UNCERTAINTY_ESTIMATE = "NC-PE-005"
    NO_CAUSAL_CLAIM_FROM_REQUIREMENT_QUALITY = "NC-PE-006"
    NO_VALIDATION_OF_REQUIREMENT_TARGET_OR_STAKEHOLDER_NEED = "NC-PE-007"
    NO_OTHER_PE_METRICS_OR_CONTEXTS_ASSESSED = "NC-PE-008"
    NO_SCALAR_OVERALL_PRODUCT_OR_REQUIREMENT_QUALITY = "NC-PE-009"


MANDATORY_NON_CLAIMS = tuple(ProductQualityNonClaim)

ASSESSMENT_CONTRACT_REF = ContractRef(
    "FULL-MODEL-V0.1-PRODUCT-QUALITY-ASSESSMENT", "1"
)
MODEL_ID = "FULL-MODEL-V0.1-M-QUALITY-PE"
MODEL_VERSION = "1"
ASSESSMENT_PROCEDURE_ID = "PE-OBS-CONFORMANCE-001"
PROCEDURE_VERSION = "1"
PARAMETER_SET_ID = "PE-OBS-CONFORMANCE-001-PARAMETERS"
PARAMETER_SET_VERSION = "1"


@dataclass(frozen=True, slots=True, order=True)
class ModelRef:
    model_id: str
    model_version: str

    def __post_init__(self) -> None:
        _identifier(self.model_id, "model_id")
        _identifier(self.model_version, "model_version")


@dataclass(frozen=True, slots=True, order=True)
class ParameterSetRef:
    parameter_set_id: str
    parameter_set_version: str

    def __post_init__(self) -> None:
        _identifier(self.parameter_set_id, "parameter_set_id")
        _identifier(self.parameter_set_version, "parameter_set_version")


MODEL_REF = ModelRef(MODEL_ID, MODEL_VERSION)
PROCEDURE_RULE_REF = RuleRef(
    ASSESSMENT_PROCEDURE_ID,
    PROCEDURE_VERSION,
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)
PARAMETER_SET_REF = ParameterSetRef(PARAMETER_SET_ID, PARAMETER_SET_VERSION)


@dataclass(frozen=True, slots=True)
class ParameterSet:
    parameter_set_id: str
    version: str
    entries: tuple[object, ...]
    source_or_rationale: str
    calibration_status: CalibrationStatus
    scope: str
    non_claim: str
    approved_contract_ref: ContractRef

    def __post_init__(self) -> None:
        if ParameterSetRef(self.parameter_set_id, self.version) != PARAMETER_SET_REF:
            raise ValueError("unsupported product-quality parameter set")
        if self.entries != ():
            raise ValueError("the v0.1 product-quality parameter set must be empty")
        _identifier(self.source_or_rationale, "source_or_rationale")
        _identifier(self.scope, "scope")
        _identifier(self.non_claim, "non_claim")
        if self.calibration_status is not CalibrationStatus.PROVISIONAL_NOT_CALIBRATED:
            raise ValueError("the v0.1 parameter set is provisional and not calibrated")
        if self.approved_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("parameter set requires the Full Model v0.1 contract")

    @property
    def parameter_set_ref(self) -> ParameterSetRef:
        return ParameterSetRef(self.parameter_set_id, self.version)


PARAMETER_SET = ParameterSet(
    parameter_set_id=PARAMETER_SET_ID,
    version=PARAMETER_SET_VERSION,
    entries=(),
    source_or_rationale="Full Model v0.1 Section 10 binary procedure.",
    calibration_status=CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
    scope="One response-time criterion conformance encoding.",
    non_claim="No empirical coefficient or predictive calibration.",
    approved_contract_ref=FULL_MODEL_CONTRACT_REF,
)


@dataclass(frozen=True, slots=True, order=True)
class ProductQualityAssessmentEventRef:
    assessment_event_id: str
    assessment_event_version: str
    product_ref: ProductRef
    artifact_ref: ArtifactRef

    def __post_init__(self) -> None:
        _identifier(self.assessment_event_id, "assessment_event_id")
        _identifier(self.assessment_event_version, "assessment_event_version")
        if not isinstance(self.product_ref, ProductRef):
            raise TypeError("product_ref must be a ProductRef")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")


@dataclass(frozen=True, slots=True)
class ProductQualityAssessmentContext:
    assessment_event_ref: ProductQualityAssessmentEventRef
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    feature_profile_ref: PerformanceEfficiencyFeatureProfileId
    product_ref: ProductRef
    process_state_ref: ProcessStateRef
    full_model_contract_ref: ContractRef = FULL_MODEL_CONTRACT_REF
    assessment_contract_ref: ContractRef = ASSESSMENT_CONTRACT_REF

    def __post_init__(self) -> None:
        if not isinstance(self.assessment_event_ref, ProductQualityAssessmentEventRef):
            raise TypeError("assessment_event_ref must be a ProductQualityAssessmentEventRef")
        if self.assessment_event_ref.artifact_ref != self.artifact_ref:
            raise ValueError("assessment event must name the context artifact")
        if self.assessment_event_ref.product_ref != self.product_ref:
            raise ValueError("assessment event must name the context product")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("source assessment must name the context artifact")
        if self.feature_profile_ref.artifact_ref != self.artifact_ref:
            raise ValueError("feature profile must name the context artifact")
        if self.feature_profile_ref.source_assessment_ref != self.source_assessment_ref:
            raise ValueError("feature profile must name the source assessment")
        if self.feature_profile_ref.product_ref != self.product_ref:
            raise ValueError("feature profile must name the context product")
        if self.feature_profile_ref.process_state_ref != self.process_state_ref:
            raise ValueError("feature profile must name the process state")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("unsupported Full Model contract")
        if self.assessment_contract_ref != ASSESSMENT_CONTRACT_REF:
            raise ValueError("unsupported product-quality assessment contract")


@dataclass(frozen=True, slots=True, order=True)
class ProductQualityAssessmentId:
    assessment_event_ref: ProductQualityAssessmentEventRef
    feature_profile_ref: PerformanceEfficiencyFeatureProfileId
    characteristic_id: ProductQualityCharacteristicId
    result_kind: ProductQualityResultKind
    model_ref: ModelRef
    procedure_rule_ref: RuleRef
    parameter_set_ref: ParameterSetRef


@dataclass(frozen=True, slots=True)
class ProductQualityScope:
    scope_kind: ProductQualityScopeKind
    characteristic_id: ProductQualityCharacteristicId
    dynamic_metric_ref: DynamicMetricRef
    criterion_ref: CriterionRef | None
    requirement_subject_ref: RequirementSubjectRef | None
    observation_ref: DynamicObservationRef | None
    conformance_ref: ConformanceAssessmentId | None
    product_ref: ProductRef
    environment_ref: EnvironmentRef | None
    collection_ref: ObservationCollectionRef | None
    context_identity: CriterionContextIdentity | None
    unit: UnitLabel | None
    process_stage: ProcessStage
    full_characteristic_coverage: FullCharacteristicCoverage

    def __post_init__(self) -> None:
        if self.scope_kind is not ProductQualityScopeKind.SINGLE_CRITERION_SINGLE_OBSERVATION:
            raise ValueError("unsupported product-quality scope")
        if self.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
            raise ValueError("product-quality scope supports Performance Efficiency only")
        if self.process_stage is not ProcessStage.REFERENCE_VERIFICATION:
            raise ValueError("product-quality scope requires REFERENCE_VERIFICATION")
        if self.full_characteristic_coverage is not FullCharacteristicCoverage.NOT_ESTABLISHED:
            raise ValueError("full Performance Efficiency coverage is not established")
        if self.dynamic_metric_ref != RESPONSE_TIME_METRIC_REF:
            raise ValueError("scope requires the approved response-time metric")
        if self.unit is not None and self.unit is not UnitLabel.SECOND:
            raise ValueError("scope supports SECOND or an absent unit only")
        if self.collection_ref is not None:
            if self.collection_ref.product_ref != self.product_ref:
                raise ValueError("scope collection and product must agree")
            if self.environment_ref != self.collection_ref.environment_ref:
                raise ValueError("scope collection and environment must agree")


@dataclass(frozen=True, slots=True)
class EvidenceCoverageItem:
    channel_id: EvidenceChannelId
    role: EvidenceRole
    feature_ref: PerformanceEfficiencyFeatureEntryId
    status: FullModelStatus
    applicability: Applicability
    source_refs: tuple[FeatureSourceRef, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.channel_id, EvidenceChannelId):
            raise TypeError("channel_id must be an EvidenceChannelId")
        if not isinstance(self.role, EvidenceRole):
            raise TypeError("role must be an EvidenceRole")
        if not isinstance(self.source_refs, tuple) or not self.source_refs:
            raise ValueError("coverage items require source references")


@dataclass(frozen=True, slots=True)
class BoundedEvidenceCoverage:
    coverage_kind: EvidenceCoverageKind
    procedure_scope: EvidenceProcedureScope
    items: tuple[EvidenceCoverageItem, ...]
    bounded_procedure_state: BoundedProcedureState
    full_performance_efficiency_coverage: FullCharacteristicCoverage
    numeric_coverage: None

    def __post_init__(self) -> None:
        if self.coverage_kind is not EvidenceCoverageKind.BOUNDED_REQUIRED_CHANNEL_INVENTORY:
            raise ValueError("unsupported evidence coverage kind")
        if self.procedure_scope is not EvidenceProcedureScope.SINGLE_RESPONSE_TIME_CRITERION:
            raise ValueError("unsupported evidence procedure scope")
        _typed_tuple(self.items, EvidenceCoverageItem, "items")
        if tuple(item.channel_id for item in self.items) != tuple(EvidenceChannelId):
            raise ValueError("evidence coverage must use the normative seven-channel order")
        if self.full_performance_efficiency_coverage is not FullCharacteristicCoverage.NOT_ESTABLISHED:
            raise ValueError("full Performance Efficiency coverage is not established")
        if self.numeric_coverage is not None:
            raise ValueError("numeric evidence coverage is not defined")


ProductQualitySourceAssessmentRef = AssessmentRef | DynamicEvidenceAssessmentRef


@dataclass(frozen=True, slots=True)
class ProductQualityAssessmentProvenance:
    feature_profile_ref: PerformanceEfficiencyFeatureProfileId
    ordered_feature_refs: tuple[PerformanceEfficiencyFeatureEntryId, ...]
    criterion_ref_or_none: CriterionRef | None
    requirement_subject_ref_or_none: RequirementSubjectRef | None
    metric_profile_ref: MetricProfileId
    qb_metric_entry_ref: MetricEntryId
    ordered_qb_cross_result_refs: tuple[QbCrossResultRef, ...]
    observation_ref_or_none: DynamicObservationRef | None
    conformance_ref_or_none: ConformanceAssessmentId | None
    product_ref: ProductRef
    environment_ref_or_none: EnvironmentRef | None
    collection_ref_or_none: ObservationCollectionRef | None
    process_state_ref: ProcessStateRef
    source_evidence_refs: tuple[FeatureEvidenceRef, ...]
    source_diagnostic_refs: tuple[FeatureDiagnosticRef, ...]
    source_assessment_refs: tuple[ProductQualitySourceAssessmentRef, ...]
    contract_refs: tuple[ContractRef, ...]
    rule_refs: tuple[RuleRef, ...]
    model_ref: ModelRef
    parameter_set_ref: ParameterSetRef

    def __post_init__(self) -> None:
        _typed_tuple(
            self.ordered_feature_refs,
            PerformanceEfficiencyFeatureEntryId,
            "ordered_feature_refs",
        )
        _typed_tuple(self.ordered_qb_cross_result_refs, QbCrossResultRef, "QB refs")
        _typed_tuple(
            self.source_evidence_refs,
            FeatureEvidenceRef,
            "source_evidence_refs",
        )
        _typed_tuple(
            self.source_diagnostic_refs,
            FeatureDiagnosticRef,
            "source_diagnostic_refs",
        )
        _typed_tuple(
            self.source_assessment_refs,
            (AssessmentRef, DynamicEvidenceAssessmentRef),
            "source_assessment_refs",
        )
        _typed_tuple(self.contract_refs, ContractRef, "contract_refs")
        _typed_tuple(self.rule_refs, RuleRef, "rule_refs")
        for values, name in (
            (self.ordered_feature_refs, "ordered_feature_refs"),
            (self.ordered_qb_cross_result_refs, "ordered_qb_cross_result_refs"),
            (self.source_evidence_refs, "source_evidence_refs"),
            (self.source_diagnostic_refs, "source_diagnostic_refs"),
            (self.source_assessment_refs, "source_assessment_refs"),
            (self.contract_refs, "contract_refs"),
            (self.rule_refs, "rule_refs"),
        ):
            if len(values) != len(set(values)):
                raise ValueError(f"{name} must not contain duplicates")
        if tuple(item.feature_id for item in self.ordered_feature_refs) != PE_FEATURE_REGISTRY:
            raise ValueError("provenance feature refs must use X_PE registry order")
        if self.metric_profile_ref != self.feature_profile_ref.metric_profile_ref:
            raise ValueError("provenance metric and feature profile refs must agree")
        if self.product_ref != self.feature_profile_ref.product_ref:
            raise ValueError("provenance product and feature profile refs must agree")
        if self.process_state_ref != self.feature_profile_ref.process_state_ref:
            raise ValueError("provenance process state and feature profile refs must agree")
        if self.collection_ref_or_none is not None:
            if self.collection_ref_or_none.product_ref != self.product_ref:
                raise ValueError("provenance collection and product must agree")
            if self.environment_ref_or_none != self.collection_ref_or_none.environment_ref:
                raise ValueError("provenance collection and environment must agree")
        if self.model_ref != MODEL_REF or self.parameter_set_ref != PARAMETER_SET_REF:
            raise ValueError("provenance requires the approved model and parameter set")
        if ASSESSMENT_CONTRACT_REF not in self.contract_refs:
            raise ValueError("provenance requires the assessment contract")
        if PROCEDURE_RULE_REF not in self.rule_refs:
            raise ValueError("provenance requires the assessment procedure")


@dataclass(frozen=True, slots=True)
class ProductQualityAssessment:
    assessment_id: ProductQualityAssessmentId
    assessment_event_ref: ProductQualityAssessmentEventRef
    characteristic_id: ProductQualityCharacteristicId
    product_ref: ProductRef
    artifact_ref: ArtifactRef
    feature_profile_ref: PerformanceEfficiencyFeatureProfileId
    scope: ProductQualityScope
    scope_statement: str
    result_kind: ProductQualityResultKind
    status: FullModelStatus
    applicability: Applicability
    source_conformance_outcome: ConformanceOutcome | None
    value: Fraction | None
    prediction_value: None
    observed_value: Fraction | None
    numeric_representation: NumericRepresentation
    evidence_coverage: BoundedEvidenceCoverage
    reliability: None
    uncertainty: None
    explanation: str
    feature_refs: tuple[PerformanceEfficiencyFeatureEntryId, ...]
    evidence_refs: tuple[FeatureEvidenceRef, ...]
    provenance: ProductQualityAssessmentProvenance
    model_ref: ModelRef
    procedure_rule_ref: RuleRef
    parameter_set_ref: ParameterSetRef
    calibration_status: CalibrationStatus
    artifact_version: str
    source_assessment_version: str
    product_version: str
    product_quality_assessment_version: str
    non_claims: tuple[ProductQualityNonClaim, ...]

    def __post_init__(self) -> None:
        expected_id = ProductQualityAssessmentId(
            self.assessment_event_ref,
            self.feature_profile_ref,
            self.characteristic_id,
            self.result_kind,
            self.model_ref,
            self.procedure_rule_ref,
            self.parameter_set_ref,
        )
        if self.assessment_id != expected_id:
            raise ValueError("assessment_id must be the structured assessment identity")
        if self.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
            raise ValueError("M_quality supports Performance Efficiency only")
        if self.result_kind is not ProductQualityResultKind.OBSERVED_REFERENCE_INDICATOR:
            raise ValueError("unsupported product-quality result kind")
        if self.prediction_value is not None or self.reliability is not None or self.uncertainty is not None:
            raise ValueError("prediction, reliability, and uncertainty must remain absent")
        if self.calibration_status is not CalibrationStatus.PROVISIONAL_NOT_CALIBRATED:
            raise ValueError("M_quality results must remain provisionally uncalibrated")
        if self.model_ref != MODEL_REF or self.procedure_rule_ref != PROCEDURE_RULE_REF:
            raise ValueError("assessment requires the approved model and procedure")
        if self.parameter_set_ref != PARAMETER_SET_REF:
            raise ValueError("assessment requires the approved empty parameter set")
        if self.non_claims != MANDATORY_NON_CLAIMS:
            raise ValueError("assessment must preserve all mandatory non-claims in order")
        _identifier(self.scope_statement, "scope_statement")
        _identifier(self.explanation, "explanation")
        _typed_tuple(self.feature_refs, PerformanceEfficiencyFeatureEntryId, "feature_refs")
        if tuple(item.feature_id for item in self.feature_refs) != PE_FEATURE_REGISTRY:
            raise ValueError("feature refs must remain in X_PE registry order")
        if self.evidence_refs != self.provenance.source_evidence_refs:
            raise ValueError("assessment and provenance evidence refs must agree")
        if self.feature_refs != self.provenance.ordered_feature_refs:
            raise ValueError("assessment and provenance feature refs must agree")
        if self.assessment_event_ref.product_ref != self.product_ref:
            raise ValueError("assessment event and result product refs must agree")
        if self.assessment_event_ref.artifact_ref != self.artifact_ref:
            raise ValueError("assessment event and result artifact refs must agree")
        if self.feature_profile_ref.product_ref != self.product_ref:
            raise ValueError("feature profile and result product refs must agree")
        if self.feature_profile_ref.artifact_ref != self.artifact_ref:
            raise ValueError("feature profile and result artifact refs must agree")
        if self.scope.product_ref != self.product_ref:
            raise ValueError("scope and result product refs must agree")
        if self.scope.characteristic_id is not self.characteristic_id:
            raise ValueError("scope and result characteristic refs must agree")
        if self.provenance.feature_profile_ref != self.feature_profile_ref:
            raise ValueError("provenance and result feature profile refs must agree")
        if self.provenance.product_ref != self.product_ref:
            raise ValueError("provenance and result product refs must agree")
        expected_procedure_state = (
            BoundedProcedureState.COMPLETE
            if self.status is FullModelStatus.AVAILABLE
            else BoundedProcedureState(self.status.value)
        )
        if self.evidence_coverage.bounded_procedure_state is not expected_procedure_state:
            raise ValueError("evidence coverage state must match assessment status")
        if self.status is FullModelStatus.AVAILABLE:
            if self.applicability is not Applicability.APPLICABLE:
                raise ValueError("available assessment must be applicable")
            expected = {
                ConformanceOutcome.CONFORMS: Fraction(1, 1),
                ConformanceOutcome.DOES_NOT_CONFORM: Fraction(0, 1),
            }.get(self.source_conformance_outcome)
            if expected is None or self.value != expected or self.observed_value != expected:
                raise ValueError("available assessment must preserve the exact outcome mapping")
            if type(self.value) is not Fraction or type(self.observed_value) is not Fraction:
                raise TypeError("available indicators must be exact Fraction values")
            if self.numeric_representation is not NumericRepresentation.EXACT_FRACTION:
                raise ValueError("available assessment requires EXACT_FRACTION")
        else:
            allowed = {
                FullModelStatus.UNAVAILABLE: {Applicability.APPLICABLE, Applicability.UNKNOWN},
                FullModelStatus.UNKNOWN: {Applicability.APPLICABLE, Applicability.UNKNOWN},
                FullModelStatus.UNRESOLVED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
                FullModelStatus.UNSUPPORTED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
                FullModelStatus.NOT_APPLICABLE: {Applicability.NOT_APPLICABLE},
            }[self.status]
            if self.applicability not in allowed:
                raise ValueError("assessment status/applicability combination is invalid")
            if self.source_conformance_outcome is not None or self.value is not None or self.observed_value is not None:
                raise ValueError("non-available assessments cannot carry an outcome or value")
            if self.numeric_representation is not NumericRepresentation.NONE:
                raise ValueError("non-available assessment requires numeric representation NONE")
        if self.artifact_version != self.artifact_ref.artifact_version:
            raise ValueError("artifact version must match the artifact reference")
        if self.source_assessment_version != self.feature_profile_ref.source_assessment_ref.assessment_version:
            raise ValueError("source assessment version must match the feature profile")
        if self.product_version != self.product_ref.product_version:
            raise ValueError("product version must match the product reference")
        if self.product_quality_assessment_version != self.assessment_event_ref.assessment_event_version:
            raise ValueError("product-quality assessment version must match its event")


__all__ = [
    "ASSESSMENT_CONTRACT_REF",
    "ASSESSMENT_PROCEDURE_ID",
    "BoundedEvidenceCoverage",
    "BoundedProcedureState",
    "CalibrationStatus",
    "EvidenceChannelId",
    "EvidenceCoverageItem",
    "EvidenceCoverageKind",
    "EvidenceProcedureScope",
    "EvidenceRole",
    "FullCharacteristicCoverage",
    "MANDATORY_NON_CLAIMS",
    "MODEL_ID",
    "MODEL_REF",
    "MODEL_VERSION",
    "ModelRef",
    "PARAMETER_SET",
    "PARAMETER_SET_ID",
    "PARAMETER_SET_REF",
    "PARAMETER_SET_VERSION",
    "PROCEDURE_RULE_REF",
    "PROCEDURE_VERSION",
    "ParameterSet",
    "ParameterSetRef",
    "ProductQualityAssessment",
    "ProductQualityAssessmentContext",
    "ProductQualityAssessmentEventRef",
    "ProductQualityAssessmentId",
    "ProductQualityAssessmentProvenance",
    "ProductQualityNonClaim",
    "ProductQualityResultKind",
    "ProductQualityScope",
    "ProductQualityScopeKind",
]

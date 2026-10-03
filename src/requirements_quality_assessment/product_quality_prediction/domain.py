"""Typed boundary for bounded Performance Efficiency prediction.

This module represents the inputs and output of ``F_theta,PE``. It does not
select an evaluator, invent parameters, or reinterpret the observed product-
quality indicator.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from typing import Protocol

from ..dynamic_evidence import (
    Applicability,
    CriterionContextIdentity,
    EnvironmentRef,
    FullModelStatus,
    ObservationCollectionRef,
    ProductRef,
)
from ..metrics import (
    ArtifactRef,
    ContractRef,
    NumericRepresentation,
    RuleRef,
    RuleVersionAuthority,
)
from ..performance_efficiency import (
    PerformanceEfficiencyFeatureEntryId,
    PerformanceEfficiencyFeatureId,
    PerformanceEfficiencyFeatureProfileId,
    ProcessStateRef,
    ProductQualityCharacteristicId,
)
from ..performance_efficiency.domain import (
    FeatureSourceReason,
    FeatureSourceRef,
    PeFeatureValue,
)


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


def _typed_tuple(value: object, item_type: type, name: str) -> None:
    if not isinstance(value, tuple) or any(not isinstance(item, item_type) for item in value):
        raise TypeError(f"{name} must be a tuple of {item_type.__name__} values")


PREDICTION_CONTRACT_REF = ContractRef(
    "FULL-MODEL-V1.0-PE-PRODUCT-QUALITY-PREDICTION", "1"
)
PREDICTION_RULE_REF = RuleRef(
    "F-THETA-PE-001", "1", RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION
)


class PredictionResultKind(str, Enum):
    PREDICTED_PERFORMANCE_EFFICIENCY = "PREDICTED_PERFORMANCE_EFFICIENCY"


class PredictionCalibrationStatus(str, Enum):
    PROVISIONAL_NOT_CALIBRATED = "PROVISIONAL_NOT_CALIBRATED"
    EXPERIMENTAL_CALIBRATION_REQUIRED = "EXPERIMENTAL_CALIBRATION_REQUIRED"


class PredictionContextField(str, Enum):
    PRODUCT = "PRODUCT"
    ARTIFACT = "ARTIFACT"
    PROCESS_STATE = "PROCESS_STATE"
    ENVIRONMENT = "ENVIRONMENT"
    OBSERVATION_COLLECTION = "OBSERVATION_COLLECTION"
    RESPONSE_TIME_CRITERION_CONTEXT = "RESPONSE_TIME_CRITERION_CONTEXT"


class PredictionWithheldReason(str, Enum):
    REQUIRED_X_PE_INPUT_NOT_AVAILABLE = "REQUIRED_X_PE_INPUT_NOT_AVAILABLE"
    REQUIRED_CONTEXT_INPUT_NOT_AVAILABLE = "REQUIRED_CONTEXT_INPUT_NOT_AVAILABLE"


@dataclass(frozen=True, slots=True, order=True)
class PredictorRef:
    predictor_id: str
    predictor_version: str

    def __post_init__(self) -> None:
        _identifier(self.predictor_id, "predictor_id")
        _identifier(self.predictor_version, "predictor_version")


@dataclass(frozen=True, slots=True, order=True)
class PredictionParameterSetIdentity:
    parameter_set_id: str
    parameter_set_version: str

    def __post_init__(self) -> None:
        _identifier(self.parameter_set_id, "parameter_set_id")
        _identifier(self.parameter_set_version, "parameter_set_version")


@dataclass(frozen=True, slots=True, order=True)
class PredictionParameterSetRef:
    identity: PredictionParameterSetIdentity
    predictor_ref: PredictorRef

    def __post_init__(self) -> None:
        if not isinstance(self.identity, PredictionParameterSetIdentity):
            raise TypeError("identity must be a PredictionParameterSetIdentity")
        if not isinstance(self.predictor_ref, PredictorRef):
            raise TypeError("predictor_ref must be a PredictorRef")


@dataclass(frozen=True, slots=True)
class PredictorDefinition:
    predictor_ref: PredictorRef
    supported_characteristic: ProductQualityCharacteristicId
    invocation_contract_ref: ContractRef
    required_feature_ids: tuple[PerformanceEfficiencyFeatureId, ...]
    required_context_fields: tuple[PredictionContextField, ...]
    required_parameter_names: tuple[str, ...]
    parameter_set_identity: PredictionParameterSetIdentity
    calibration_status: PredictionCalibrationStatus
    source_or_rationale: str

    def __post_init__(self) -> None:
        if not isinstance(self.predictor_ref, PredictorRef):
            raise TypeError("predictor_ref must be a PredictorRef")
        if self.supported_characteristic is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
            raise ValueError("the bounded prediction contract supports Performance Efficiency only")
        if self.invocation_contract_ref != PREDICTION_CONTRACT_REF:
            raise ValueError("unsupported prediction invocation contract")
        _typed_tuple(self.required_feature_ids, PerformanceEfficiencyFeatureId, "required_feature_ids")
        _typed_tuple(self.required_context_fields, PredictionContextField, "required_context_fields")
        if not isinstance(self.required_parameter_names, tuple):
            raise TypeError("required_parameter_names must be a tuple")
        for name in self.required_parameter_names:
            _identifier(name, "required parameter name")
        for values, name in (
            (self.required_feature_ids, "required_feature_ids"),
            (self.required_context_fields, "required_context_fields"),
            (self.required_parameter_names, "required_parameter_names"),
        ):
            if not values:
                raise ValueError(f"{name} must not be empty")
            if len(values) != len(set(values)):
                raise ValueError(f"{name} must not contain duplicates")
        if not isinstance(self.parameter_set_identity, PredictionParameterSetIdentity):
            raise TypeError("parameter_set_identity must be versioned")
        if not isinstance(self.calibration_status, PredictionCalibrationStatus):
            raise TypeError("calibration_status must be a PredictionCalibrationStatus")
        _identifier(self.source_or_rationale, "source_or_rationale")


PredictionParameterValue = Fraction | Decimal


@dataclass(frozen=True, slots=True)
class PredictionParameter:
    name: str
    exact_value: PredictionParameterValue

    def __post_init__(self) -> None:
        _identifier(self.name, "parameter name")
        if type(self.exact_value) not in {Fraction, Decimal}:
            raise TypeError("prediction parameters require an exact Fraction or Decimal")


@dataclass(frozen=True, slots=True)
class PredictionParameterSet:
    identity: PredictionParameterSetIdentity
    predictor_ref: PredictorRef
    entries: tuple[PredictionParameter, ...]
    source_or_rationale: str
    calibration_status: PredictionCalibrationStatus
    governing_contract_ref: ContractRef

    def __post_init__(self) -> None:
        if not isinstance(self.identity, PredictionParameterSetIdentity):
            raise TypeError("identity must be a PredictionParameterSetIdentity")
        if not isinstance(self.predictor_ref, PredictorRef):
            raise TypeError("predictor_ref must be a PredictorRef")
        _typed_tuple(self.entries, PredictionParameter, "entries")
        names = tuple(item.name for item in self.entries)
        if len(names) != len(set(names)):
            raise ValueError("prediction parameter names must not contain duplicates")
        _identifier(self.source_or_rationale, "source_or_rationale")
        if not isinstance(self.calibration_status, PredictionCalibrationStatus):
            raise TypeError("calibration_status must be a PredictionCalibrationStatus")
        if self.governing_contract_ref != PREDICTION_CONTRACT_REF:
            raise ValueError("parameter set requires the prediction contract")

    @property
    def parameter_set_ref(self) -> PredictionParameterSetRef:
        return PredictionParameterSetRef(self.identity, self.predictor_ref)


@dataclass(frozen=True, slots=True)
class PerformanceEfficiencyPredictionContext:
    product_ref: ProductRef
    artifact_ref: ArtifactRef
    process_state_ref: ProcessStateRef
    environment_ref_or_none: EnvironmentRef | None
    collection_ref_or_none: ObservationCollectionRef | None
    criterion_context_or_none: CriterionContextIdentity | None

    def __post_init__(self) -> None:
        if not isinstance(self.product_ref, ProductRef):
            raise TypeError("product_ref must be a ProductRef")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if not isinstance(self.process_state_ref, ProcessStateRef):
            raise TypeError("process_state_ref must be a ProcessStateRef")
        if self.environment_ref_or_none is not None and not isinstance(
            self.environment_ref_or_none, EnvironmentRef
        ):
            raise TypeError("environment_ref_or_none must be an EnvironmentRef or None")
        if self.collection_ref_or_none is not None:
            if not isinstance(self.collection_ref_or_none, ObservationCollectionRef):
                raise TypeError("collection_ref_or_none must be an ObservationCollectionRef or None")
            if self.collection_ref_or_none.product_ref != self.product_ref:
                raise ValueError("prediction context collection must name the context product")
            if self.collection_ref_or_none.environment_ref != self.environment_ref_or_none:
                raise ValueError("prediction context collection and environment must agree")
        if self.criterion_context_or_none is not None and not isinstance(
            self.criterion_context_or_none, CriterionContextIdentity
        ):
            raise TypeError("criterion_context_or_none must be a CriterionContextIdentity or None")


PredictionContextValue = (
    ProductRef
    | ArtifactRef
    | ProcessStateRef
    | EnvironmentRef
    | ObservationCollectionRef
    | CriterionContextIdentity
)


@dataclass(frozen=True, slots=True)
class SelectedPredictionContext:
    field: PredictionContextField
    value_or_none: PredictionContextValue | None

    def __post_init__(self) -> None:
        if not isinstance(self.field, PredictionContextField):
            raise TypeError("field must be a PredictionContextField")
        expected_type = {
            PredictionContextField.PRODUCT: ProductRef,
            PredictionContextField.ARTIFACT: ArtifactRef,
            PredictionContextField.PROCESS_STATE: ProcessStateRef,
            PredictionContextField.ENVIRONMENT: EnvironmentRef,
            PredictionContextField.OBSERVATION_COLLECTION: ObservationCollectionRef,
            PredictionContextField.RESPONSE_TIME_CRITERION_CONTEXT: CriterionContextIdentity,
        }[self.field]
        if self.value_or_none is not None and not isinstance(self.value_or_none, expected_type):
            raise TypeError("selected context value does not match its declared field")


@dataclass(frozen=True, slots=True)
class SelectedPredictionInput:
    feature_ref: PerformanceEfficiencyFeatureEntryId
    feature_id: PerformanceEfficiencyFeatureId
    typed_value: PeFeatureValue

    def __post_init__(self) -> None:
        if self.feature_ref.feature_id is not self.feature_id:
            raise ValueError("selected input reference must name its feature")
        if self.typed_value is None:
            raise ValueError("selected evaluator inputs require a typed value")


@dataclass(frozen=True, slots=True)
class PredictionInputTrace:
    feature_ref: PerformanceEfficiencyFeatureEntryId
    feature_id: PerformanceEfficiencyFeatureId
    status: FullModelStatus
    applicability: Applicability
    source_refs: tuple[FeatureSourceRef, ...]
    upstream_reasons: tuple[FeatureSourceReason, ...]

    def __post_init__(self) -> None:
        if self.feature_ref.feature_id is not self.feature_id:
            raise ValueError("input trace reference must name its feature")
        if not isinstance(self.status, FullModelStatus):
            raise TypeError("status must be a FullModelStatus")
        if not isinstance(self.applicability, Applicability):
            raise TypeError("applicability must be an Applicability")
        if not isinstance(self.source_refs, tuple) or not isinstance(self.upstream_reasons, tuple):
            raise TypeError("input trace references and reasons must remain tuples")


@dataclass(frozen=True, slots=True, order=True)
class PredictionEventRef:
    prediction_event_id: str
    prediction_event_version: str

    def __post_init__(self) -> None:
        _identifier(self.prediction_event_id, "prediction_event_id")
        _identifier(self.prediction_event_version, "prediction_event_version")


@dataclass(frozen=True, slots=True)
class PerformanceEfficiencyPredictionRequest:
    event_ref: PredictionEventRef
    feature_profile_id: PerformanceEfficiencyFeatureProfileId
    context: PerformanceEfficiencyPredictionContext
    parameter_set: PredictionParameterSet
    governing_contract_ref: ContractRef = PREDICTION_CONTRACT_REF

    def __post_init__(self) -> None:
        if not isinstance(self.event_ref, PredictionEventRef):
            raise TypeError("event_ref must be a PredictionEventRef")
        if not isinstance(self.feature_profile_id, PerformanceEfficiencyFeatureProfileId):
            raise TypeError("feature_profile_id must be a PerformanceEfficiencyFeatureProfileId")
        if not isinstance(self.context, PerformanceEfficiencyPredictionContext):
            raise TypeError("context must be a PerformanceEfficiencyPredictionContext")
        if not isinstance(self.parameter_set, PredictionParameterSet):
            raise TypeError("parameter_set must be a PredictionParameterSet")
        if self.governing_contract_ref != PREDICTION_CONTRACT_REF:
            raise ValueError("request requires the prediction contract")


@dataclass(frozen=True, slots=True)
class PerformanceEfficiencyEvaluationInput:
    selected_inputs: tuple[SelectedPredictionInput, ...]
    selected_context: tuple[SelectedPredictionContext, ...]
    parameters: tuple[PredictionParameter, ...]

    def __post_init__(self) -> None:
        _typed_tuple(self.selected_inputs, SelectedPredictionInput, "selected_inputs")
        _typed_tuple(self.selected_context, SelectedPredictionContext, "selected_context")
        _typed_tuple(self.parameters, PredictionParameter, "parameters")


class PerformanceEfficiencyPredictor(Protocol):
    """In-process evaluator supplied explicitly by the researcher/caller."""

    @property
    def definition(self) -> PredictorDefinition: ...

    def evaluate(self, evaluation_input: PerformanceEfficiencyEvaluationInput) -> Fraction: ...


@dataclass(frozen=True, slots=True)
class PerformanceEfficiencyPredictionProvenance:
    feature_profile_ref: PerformanceEfficiencyFeatureProfileId
    input_traces: tuple[PredictionInputTrace, ...]
    context_inputs: tuple[SelectedPredictionContext, ...]
    predictor_definition: PredictorDefinition
    parameter_set_ref: PredictionParameterSetRef
    parameter_entries: tuple[PredictionParameter, ...]
    parameter_source_or_rationale: str
    contract_refs: tuple[ContractRef, ...]
    rule_refs: tuple[RuleRef, ...]
    withheld_reason_or_none: PredictionWithheldReason | None

    def __post_init__(self) -> None:
        _typed_tuple(self.input_traces, PredictionInputTrace, "input_traces")
        _typed_tuple(self.context_inputs, SelectedPredictionContext, "context_inputs")
        _typed_tuple(self.parameter_entries, PredictionParameter, "parameter_entries")
        _typed_tuple(self.contract_refs, ContractRef, "contract_refs")
        _typed_tuple(self.rule_refs, RuleRef, "rule_refs")
        _identifier(self.parameter_source_or_rationale, "parameter_source_or_rationale")
        if PREDICTION_CONTRACT_REF not in self.contract_refs:
            raise ValueError("prediction provenance requires the prediction contract")
        if PREDICTION_RULE_REF not in self.rule_refs:
            raise ValueError("prediction provenance requires the F_theta rule")
        definition = self.predictor_definition
        if self.parameter_set_ref.predictor_ref != definition.predictor_ref:
            raise ValueError("prediction provenance cannot mix predictor identities")
        if self.parameter_set_ref.identity != definition.parameter_set_identity:
            raise ValueError("prediction provenance cannot mix theta identities")
        if tuple(item.feature_id for item in self.input_traces) != definition.required_feature_ids:
            raise ValueError("prediction input traces must match the declared feature inventory")
        if any(
            item.feature_ref.profile_id != self.feature_profile_ref
            for item in self.input_traces
        ):
            raise ValueError("prediction input traces must name the source X_PE profile")
        if tuple(item.field for item in self.context_inputs) != definition.required_context_fields:
            raise ValueError("prediction context must match the declared context inventory")
        if tuple(item.name for item in self.parameter_entries) != definition.required_parameter_names:
            raise ValueError("prediction theta entries must match the declared parameter inventory")


@dataclass(frozen=True, slots=True)
class PredictedPerformanceEfficiency:
    event_ref: PredictionEventRef
    result_kind: PredictionResultKind
    characteristic_id: ProductQualityCharacteristicId
    status: FullModelStatus
    applicability: Applicability
    predicted_value: Fraction | None
    numeric_representation: NumericRepresentation
    predictor_ref: PredictorRef
    parameter_set_ref: PredictionParameterSetRef
    calibration_status: PredictionCalibrationStatus
    selected_input_refs: tuple[PerformanceEfficiencyFeatureEntryId, ...]
    context_inputs: tuple[SelectedPredictionContext, ...]
    artifact_ref: ArtifactRef
    product_ref: ProductRef
    process_state_ref: ProcessStateRef
    governing_contract_ref: ContractRef
    rule_refs: tuple[RuleRef, ...]
    explanation: str
    provenance: PerformanceEfficiencyPredictionProvenance

    def __post_init__(self) -> None:
        if self.result_kind is not PredictionResultKind.PREDICTED_PERFORMANCE_EFFICIENCY:
            raise ValueError("prediction result kind must identify predicted Performance Efficiency")
        if self.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
            raise ValueError("prediction result supports Performance Efficiency only")
        _typed_tuple(self.selected_input_refs, PerformanceEfficiencyFeatureEntryId, "selected_input_refs")
        _typed_tuple(self.context_inputs, SelectedPredictionContext, "context_inputs")
        _typed_tuple(self.rule_refs, RuleRef, "rule_refs")
        _identifier(self.explanation, "explanation")
        if self.governing_contract_ref != PREDICTION_CONTRACT_REF:
            raise ValueError("prediction result requires the prediction contract")
        allowed = {
            FullModelStatus.AVAILABLE: {Applicability.APPLICABLE},
            FullModelStatus.NOT_APPLICABLE: {Applicability.NOT_APPLICABLE},
            FullModelStatus.UNKNOWN: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNRESOLVED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNAVAILABLE: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNSUPPORTED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
        }[self.status]
        if self.applicability not in allowed:
            raise ValueError("prediction status/applicability combination is invalid")
        if self.predictor_ref != self.provenance.predictor_definition.predictor_ref:
            raise ValueError("prediction result and provenance must name the same predictor")
        if self.parameter_set_ref != self.provenance.parameter_set_ref:
            raise ValueError("prediction result and provenance must name the same theta")
        if self.calibration_status is not self.provenance.predictor_definition.calibration_status:
            raise ValueError("prediction result calibration must match its configuration")
        if self.selected_input_refs != tuple(
            item.feature_ref for item in self.provenance.input_traces
        ):
            raise ValueError("prediction result must preserve the declared X_PE references")
        if self.context_inputs != self.provenance.context_inputs:
            raise ValueError("prediction result must preserve the selected context")
        profile_ref = self.provenance.feature_profile_ref
        if (
            self.artifact_ref != profile_ref.artifact_ref
            or self.product_ref != profile_ref.product_ref
            or self.process_state_ref != profile_ref.process_state_ref
        ):
            raise ValueError("prediction result identities must agree with X_PE")
        if self.rule_refs != self.provenance.rule_refs:
            raise ValueError("prediction result must preserve provenance rules")
        if self.status is FullModelStatus.AVAILABLE:
            if self.applicability is not Applicability.APPLICABLE:
                raise ValueError("available predictions must be applicable")
            if type(self.predicted_value) is not Fraction:
                raise TypeError("available predictions require an exact Fraction")
            if not Fraction(0, 1) <= self.predicted_value <= Fraction(1, 1):
                raise ValueError("predicted Performance Efficiency must be in [0,1]")
            if self.numeric_representation is not NumericRepresentation.EXACT_FRACTION:
                raise ValueError("available predictions require EXACT_FRACTION")
            if self.provenance.withheld_reason_or_none is not None:
                raise ValueError("available predictions cannot have a withheld reason")
        else:
            if self.predicted_value is not None:
                raise ValueError("withheld predictions cannot carry a numeric value")
            if self.numeric_representation is not NumericRepresentation.NONE:
                raise ValueError("withheld predictions require numeric representation NONE")
            if self.provenance.withheld_reason_or_none is None:
                raise ValueError("withheld predictions require a typed withheld reason")


__all__ = [
    "PREDICTION_CONTRACT_REF",
    "PREDICTION_RULE_REF",
    "PerformanceEfficiencyEvaluationInput",
    "PerformanceEfficiencyPredictionContext",
    "PerformanceEfficiencyPredictionProvenance",
    "PerformanceEfficiencyPredictionRequest",
    "PerformanceEfficiencyPredictor",
    "PredictedPerformanceEfficiency",
    "PredictionCalibrationStatus",
    "PredictionContextField",
    "PredictionEventRef",
    "PredictionInputTrace",
    "PredictionParameter",
    "PredictionParameterSet",
    "PredictionParameterSetIdentity",
    "PredictionParameterSetRef",
    "PredictionResultKind",
    "PredictionWithheldReason",
    "PredictorDefinition",
    "PredictorRef",
    "SelectedPredictionContext",
    "SelectedPredictionInput",
]

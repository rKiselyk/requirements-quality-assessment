"""Execution service for explicitly supplied bounded ``F_theta,PE`` evaluators."""

from __future__ import annotations

from fractions import Fraction

from ..dynamic_evidence import Applicability, FullModelStatus
from ..metrics import NumericRepresentation
from ..performance_efficiency import (
    CriterionFeatureValue,
    ObservationFeatureValue,
    PerformanceEfficiencyFeatureId,
    PerformanceEfficiencyFeatureProfile,
    ProductQualityCharacteristicId,
)
from .domain import (
    PREDICTION_CONTRACT_REF,
    PREDICTION_RULE_REF,
    PerformanceEfficiencyEvaluationInput,
    PerformanceEfficiencyPredictionProvenance,
    PerformanceEfficiencyPredictionRequest,
    PerformanceEfficiencyPredictor,
    PredictedPerformanceEfficiency,
    PredictionContextField,
    PredictionInputTrace,
    PredictionResultKind,
    PredictionWithheldReason,
    PredictorDefinition,
    SelectedPredictionContext,
    SelectedPredictionInput,
)


def _feature(profile: PerformanceEfficiencyFeatureProfile, feature_id: PerformanceEfficiencyFeatureId):
    return next(item for item in profile.features if item.feature_id is feature_id)


def _context_value(request: PerformanceEfficiencyPredictionRequest, field: PredictionContextField):
    context = request.context
    return {
        PredictionContextField.PRODUCT: context.product_ref,
        PredictionContextField.ARTIFACT: context.artifact_ref,
        PredictionContextField.PROCESS_STATE: context.process_state_ref,
        PredictionContextField.ENVIRONMENT: context.environment_ref_or_none,
        PredictionContextField.OBSERVATION_COLLECTION: context.collection_ref_or_none,
        PredictionContextField.RESPONSE_TIME_CRITERION_CONTEXT: context.criterion_context_or_none,
    }[field]


def _validate_request_context(
    profile: PerformanceEfficiencyFeatureProfile,
    request: PerformanceEfficiencyPredictionRequest,
) -> None:
    if request.feature_profile_id != profile.profile_id:
        raise ValueError("prediction request must name the supplied X_PE profile")
    context = request.context
    if context.artifact_ref != profile.artifact_ref:
        raise ValueError("prediction context must name the X_PE artifact")
    if context.product_ref != profile.product_ref:
        raise ValueError("prediction context must name the X_PE product")
    if context.process_state_ref != profile.process_state_ref:
        raise ValueError("prediction context must name the X_PE process state")
    if context.environment_ref_or_none is not None and (
        context.environment_ref_or_none != profile.provenance.environment_ref_or_none
    ):
        raise ValueError("prediction environment must come from X_PE provenance")
    if context.collection_ref_or_none is not None and (
        context.collection_ref_or_none != profile.provenance.collection_ref_or_none
    ):
        raise ValueError("prediction collection must come from X_PE provenance")
    if context.criterion_context_or_none is not None:
        available_contexts = tuple(
            value.context_identity
            for value in (
                _feature(profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME).typed_value,
                _feature(profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME).typed_value,
            )
            if isinstance(value, (CriterionFeatureValue, ObservationFeatureValue))
        )
        if context.criterion_context_or_none not in available_contexts:
            raise ValueError("prediction criterion context must come from X_PE")


def _validate_configuration(
    definition: PredictorDefinition,
    request: PerformanceEfficiencyPredictionRequest,
) -> None:
    parameters = request.parameter_set
    if parameters.predictor_ref != definition.predictor_ref:
        raise ValueError("theta belongs to a different predictor identity/version")
    if parameters.identity != definition.parameter_set_identity:
        raise ValueError("theta identity/version does not match the predictor contract")
    if parameters.calibration_status is not definition.calibration_status:
        raise ValueError("theta calibration status does not match the predictor contract")
    names = tuple(item.name for item in parameters.entries)
    if names != definition.required_parameter_names:
        raise ValueError("theta entries must exactly match the declared parameter order")


def _provenance(
    profile: PerformanceEfficiencyFeatureProfile,
    request: PerformanceEfficiencyPredictionRequest,
    definition: PredictorDefinition,
    traces: tuple[PredictionInputTrace, ...],
    context_inputs: tuple[SelectedPredictionContext, ...],
    withheld_reason: PredictionWithheldReason | None,
) -> PerformanceEfficiencyPredictionProvenance:
    return PerformanceEfficiencyPredictionProvenance(
        feature_profile_ref=profile.profile_id,
        input_traces=traces,
        context_inputs=context_inputs,
        predictor_definition=definition,
        parameter_set_ref=request.parameter_set.parameter_set_ref,
        parameter_entries=request.parameter_set.entries,
        parameter_source_or_rationale=request.parameter_set.source_or_rationale,
        contract_refs=tuple(
            dict.fromkeys((*profile.provenance.source_contract_refs, PREDICTION_CONTRACT_REF))
        ),
        rule_refs=tuple(
            dict.fromkeys((*profile.provenance.rule_refs, PREDICTION_RULE_REF))
        ),
        withheld_reason_or_none=withheld_reason,
    )


def _result(
    profile: PerformanceEfficiencyFeatureProfile,
    request: PerformanceEfficiencyPredictionRequest,
    definition: PredictorDefinition,
    traces: tuple[PredictionInputTrace, ...],
    context_inputs: tuple[SelectedPredictionContext, ...],
    *,
    status: FullModelStatus,
    applicability: Applicability,
    value: Fraction | None,
    withheld_reason: PredictionWithheldReason | None,
    explanation: str,
) -> PredictedPerformanceEfficiency:
    provenance = _provenance(
        profile, request, definition, traces, context_inputs, withheld_reason
    )
    return PredictedPerformanceEfficiency(
        event_ref=request.event_ref,
        result_kind=PredictionResultKind.PREDICTED_PERFORMANCE_EFFICIENCY,
        characteristic_id=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
        status=status,
        applicability=applicability,
        predicted_value=value,
        numeric_representation=(
            NumericRepresentation.EXACT_FRACTION
            if value is not None
            else NumericRepresentation.NONE
        ),
        predictor_ref=definition.predictor_ref,
        parameter_set_ref=request.parameter_set.parameter_set_ref,
        calibration_status=request.parameter_set.calibration_status,
        selected_input_refs=tuple(item.feature_ref for item in traces),
        context_inputs=context_inputs,
        artifact_ref=profile.artifact_ref,
        product_ref=profile.product_ref,
        process_state_ref=profile.process_state_ref,
        governing_contract_ref=PREDICTION_CONTRACT_REF,
        rule_refs=provenance.rule_refs,
        explanation=explanation,
        provenance=provenance,
    )


class PerformanceEfficiencyPredictionService:
    """Project ``X_PE`` and explicit ``C``/theta into a supplied evaluator."""

    def predict(
        self,
        feature_profile: PerformanceEfficiencyFeatureProfile,
        request: PerformanceEfficiencyPredictionRequest,
        predictor: PerformanceEfficiencyPredictor,
    ) -> PredictedPerformanceEfficiency:
        if not isinstance(feature_profile, PerformanceEfficiencyFeatureProfile):
            raise TypeError("feature_profile must be a PerformanceEfficiencyFeatureProfile")
        if not isinstance(request, PerformanceEfficiencyPredictionRequest):
            raise TypeError("request must be a PerformanceEfficiencyPredictionRequest")
        definition = predictor.definition
        if not isinstance(definition, PredictorDefinition):
            raise TypeError("predictor.definition must be a PredictorDefinition")
        _validate_request_context(feature_profile, request)
        _validate_configuration(definition, request)

        required_features = tuple(
            _feature(feature_profile, feature_id)
            for feature_id in definition.required_feature_ids
        )
        traces = tuple(
            PredictionInputTrace(
                feature.feature_entry_id,
                feature.feature_id,
                feature.status,
                feature.applicability,
                feature.source_refs,
                feature.reasons,
            )
            for feature in required_features
        )
        context_inputs = tuple(
            SelectedPredictionContext(field, _context_value(request, field))
            for field in definition.required_context_fields
        )

        missing_feature = next(
            (
                feature
                for feature in required_features
                if feature.status is not FullModelStatus.AVAILABLE
            ),
            None,
        )
        if missing_feature is not None:
            reasons = ", ".join(reason.value for reason in missing_feature.reasons)
            detail = reasons or "no upstream typed reason supplied"
            return _result(
                feature_profile,
                request,
                definition,
                traces,
                context_inputs,
                status=missing_feature.status,
                applicability=missing_feature.applicability,
                value=None,
                withheld_reason=PredictionWithheldReason.REQUIRED_X_PE_INPUT_NOT_AVAILABLE,
                explanation=(
                    f"Prediction withheld: required X_PE input {missing_feature.feature_id.value} "
                    f"has state {missing_feature.status.value}; {detail}. No value was imputed "
                    "and the evaluator was not invoked."
                ),
            )

        missing_context = next(
            (item for item in context_inputs if item.value_or_none is None), None
        )
        if missing_context is not None:
            return _result(
                feature_profile,
                request,
                definition,
                traces,
                context_inputs,
                status=FullModelStatus.UNAVAILABLE,
                applicability=Applicability.APPLICABLE,
                value=None,
                withheld_reason=PredictionWithheldReason.REQUIRED_CONTEXT_INPUT_NOT_AVAILABLE,
                explanation=(
                    f"Prediction withheld: required context input {missing_context.field.value} "
                    "is unavailable. No context default was supplied and the evaluator was not invoked."
                ),
            )

        selected_inputs = tuple(
            SelectedPredictionInput(
                feature.feature_entry_id, feature.feature_id, feature.typed_value
            )
            for feature in required_features
        )
        evaluation_input = PerformanceEfficiencyEvaluationInput(
            selected_inputs,
            context_inputs,
            request.parameter_set.entries,
        )
        value = predictor.evaluate(evaluation_input)
        if type(value) is not Fraction:
            raise TypeError("predictor output must be an exact Fraction")
        if not Fraction(0, 1) <= value <= Fraction(1, 1):
            raise ValueError("predictor output must be in [0,1]; it is not clamped")

        return _result(
            feature_profile,
            request,
            definition,
            traces,
            context_inputs,
            status=FullModelStatus.AVAILABLE,
            applicability=Applicability.APPLICABLE,
            value=value,
            withheld_reason=None,
            explanation=(
                f"Predicted Performance Efficiency y_hat_PE={value.numerator}/{value.denominator} "
                f"was produced by explicitly supplied predictor {definition.predictor_ref.predictor_id} "
                f"version {definition.predictor_ref.predictor_version} and theta "
                f"{request.parameter_set.identity.parameter_set_id} version "
                f"{request.parameter_set.identity.parameter_set_version}. This bounded result is "
                "distinct from observed product-quality evidence and makes no predictive-validity, "
                "confidence, uncertainty, causal, or universal-model claim."
            ),
        )


def predict_performance_efficiency(
    feature_profile: PerformanceEfficiencyFeatureProfile,
    request: PerformanceEfficiencyPredictionRequest,
    predictor: PerformanceEfficiencyPredictor,
) -> PredictedPerformanceEfficiency:
    """Execute one explicitly supplied, versioned ``F_theta,PE`` evaluator."""

    return PerformanceEfficiencyPredictionService().predict(
        feature_profile, request, predictor
    )


__all__ = [
    "PerformanceEfficiencyPredictionService",
    "predict_performance_efficiency",
]

from dataclasses import FrozenInstanceError, fields, replace
from fractions import Fraction

import pytest

from requirements_quality_assessment.dynamic_evidence import (
    Applicability,
    ConformanceOutcome,
    DynamicEvidenceReason,
    FullModelStatus,
)
from requirements_quality_assessment.full_model_reporter import (
    AuditFullModelReporter,
    FullModelReportBundle,
    UserFullModelReporter,
)
from requirements_quality_assessment.performance_efficiency import (
    ConformanceFeatureValue,
    CriterionFeatureValue,
    PerformanceEfficiencyFeatureId,
    ProductQualityCharacteristicId,
    RequirementMetricFeatureValue,
)
from requirements_quality_assessment.product_quality import (
    ProductQualityAssessment,
    ProductQualityResultKind,
)
from requirements_quality_assessment.product_quality_prediction import (
    PREDICTION_CONTRACT_REF,
    PerformanceEfficiencyEvaluationInput,
    PerformanceEfficiencyPredictionContext,
    PerformanceEfficiencyPredictionRequest,
    PredictedPerformanceEfficiency,
    PredictionCalibrationStatus,
    PredictionContextField,
    PredictionEventRef,
    PredictionParameter,
    PredictionParameterSet,
    PredictionParameterSetIdentity,
    PredictionResultKind,
    PredictionWithheldReason,
    PredictorDefinition,
    PredictorRef,
    predict_performance_efficiency,
)

from test_performance_efficiency_features import _build, _bundle, _feature
from test_product_quality_assessment import _assess
from test_corrective_action import _positive


PREDICTOR_REF = PredictorRef("TC02-CONTROLLED-REFERENCE-PE", "1")
PARAMETER_IDENTITY = PredictionParameterSetIdentity(
    "TC02-CONTROLLED-REFERENCE-THETA", "1"
)


def _definition(
    *,
    required_features=(
        PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS,
        PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME,
    ),
    required_context=(
        PredictionContextField.PRODUCT,
        PredictionContextField.ENVIRONMENT,
        PredictionContextField.RESPONSE_TIME_CRITERION_CONTEXT,
    ),
):
    return PredictorDefinition(
        predictor_ref=PREDICTOR_REF,
        supported_characteristic=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
        invocation_contract_ref=PREDICTION_CONTRACT_REF,
        required_feature_ids=required_features,
        required_context_fields=required_context,
        required_parameter_names=("requirement_weight",),
        parameter_set_identity=PARAMETER_IDENTITY,
        calibration_status=PredictionCalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
        source_or_rationale=(
            "Controlled TC-02 fixture proving deterministic contract execution only; "
            "not a calibrated or universal model."
        ),
    )


class ControlledReferencePredictor:
    def __init__(self, definition=None, output=None):
        self._definition = definition or _definition()
        self.output = output
        self.calls = 0

    @property
    def definition(self):
        return self._definition

    def evaluate(self, evaluation_input: PerformanceEfficiencyEvaluationInput):
        self.calls += 1
        if self.output is not None:
            return self.output
        inputs = {item.feature_id: item.typed_value for item in evaluation_input.selected_inputs}
        completeness = inputs[PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS]
        conformance = inputs[PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME]
        assert isinstance(completeness, RequirementMetricFeatureValue)
        assert isinstance(conformance, ConformanceFeatureValue)
        weight = evaluation_input.parameters[0].exact_value
        assert type(weight) is Fraction
        conformance_value = Fraction(
            int(conformance.outcome is ConformanceOutcome.CONFORMS), 1
        )
        return (
            weight * completeness.exact_fraction_or_none
            + (Fraction(1, 1) - weight) * conformance_value
        )


def _parameters(**changes):
    values = {
        "identity": PARAMETER_IDENTITY,
        "predictor_ref": PREDICTOR_REF,
        "entries": (PredictionParameter("requirement_weight", Fraction(1, 4)),),
        "source_or_rationale": (
            "Explicit TC-02 controlled reference theta; fixture values have no "
            "predictive-validity claim."
        ),
        "calibration_status": PredictionCalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
        "governing_contract_ref": PREDICTION_CONTRACT_REF,
    }
    values.update(changes)
    return PredictionParameterSet(**values)


def _context(profile, *, environment=True, criterion=True):
    criterion_value = _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    ).typed_value
    assert isinstance(criterion_value, CriterionFeatureValue)
    return PerformanceEfficiencyPredictionContext(
        product_ref=profile.product_ref,
        artifact_ref=profile.artifact_ref,
        process_state_ref=profile.process_state_ref,
        environment_ref_or_none=(
            profile.provenance.environment_ref_or_none if environment else None
        ),
        collection_ref_or_none=(
            profile.provenance.collection_ref_or_none if environment else None
        ),
        criterion_context_or_none=(
            criterion_value.context_identity if criterion else None
        ),
    )


def _request(profile, *, parameters=None, context=None):
    return PerformanceEfficiencyPredictionRequest(
        event_ref=PredictionEventRef("TC02-PREDICTION-EVENT", "1"),
        feature_profile_id=profile.profile_id,
        context=context or _context(profile),
        parameter_set=parameters or _parameters(),
    )


def _predict(profile=None, *, predictor=None, request=None):
    profile = profile or _build(_bundle())
    predictor = predictor or ControlledReferencePredictor()
    request = request or _request(profile)
    return predict_performance_efficiency(profile, request, predictor)


def test_prediction_contracts_are_typed_versioned_immutable_and_distinct() -> None:
    profile = _build(_bundle())
    predictor = ControlledReferencePredictor()
    prediction = _predict(profile, predictor=predictor)
    observed = _assess(profile)

    assert predictor.definition.predictor_ref == PREDICTOR_REF
    assert predictor.definition.parameter_set_identity == PARAMETER_IDENTITY
    assert prediction.parameter_set_ref.identity == PARAMETER_IDENTITY
    assert isinstance(prediction, PredictedPerformanceEfficiency)
    assert isinstance(observed, ProductQualityAssessment)
    assert type(prediction) is not type(observed)
    assert prediction.result_kind is PredictionResultKind.PREDICTED_PERFORMANCE_EFFICIENCY
    assert observed.result_kind is ProductQualityResultKind.OBSERVED_REFERENCE_INDICATOR
    assert observed.prediction_value is None
    with pytest.raises(FrozenInstanceError):
        prediction.predicted_value = Fraction(0, 1)
    with pytest.raises(FrozenInstanceError):
        request_parameters = _parameters()
        request_parameters.entries = ()


def test_prediction_cannot_be_requested_without_an_explicit_predictor() -> None:
    profile = _build(_bundle())
    with pytest.raises(TypeError):
        predict_performance_efficiency(profile, _request(profile))


def test_controlled_reference_prediction_is_exact_reproducible_and_traceable() -> None:
    profile = _build(_bundle())
    predictor = ControlledReferencePredictor()
    request = _request(profile)

    first = predict_performance_efficiency(profile, request, predictor)
    second = predict_performance_efficiency(profile, request, predictor)

    completeness = _feature(
        profile, PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS
    ).typed_value.exact_fraction_or_none
    expected = Fraction(1, 4) * completeness + Fraction(3, 4)
    assert first == second
    assert first.predicted_value == expected
    assert type(first.predicted_value) is Fraction
    assert Fraction(0, 1) <= first.predicted_value <= Fraction(1, 1)
    assert first.predictor_ref == PREDICTOR_REF
    assert first.parameter_set_ref.identity == PARAMETER_IDENTITY
    assert first.calibration_status is PredictionCalibrationStatus.PROVISIONAL_NOT_CALIBRATED
    assert tuple(item.feature_id for item in first.provenance.input_traces) == (
        PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS,
        PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME,
    )
    assert tuple(item.field for item in first.context_inputs) == (
        PredictionContextField.PRODUCT,
        PredictionContextField.ENVIRONMENT,
        PredictionContextField.RESPONSE_TIME_CRITERION_CONTEXT,
    )
    assert first.provenance.parameter_entries == request.parameter_set.entries
    assert first.provenance.withheld_reason_or_none is None
    assert predictor.calls == 2


@pytest.mark.parametrize(
    ("status", "applicability"),
    (
        (FullModelStatus.UNKNOWN, Applicability.UNKNOWN),
        (FullModelStatus.UNAVAILABLE, Applicability.APPLICABLE),
        (FullModelStatus.UNRESOLVED, Applicability.UNKNOWN),
        (FullModelStatus.NOT_APPLICABLE, Applicability.NOT_APPLICABLE),
    ),
)
def test_missing_required_x_pe_state_withholds_without_zero_or_invocation(
    status, applicability
) -> None:
    profile = _build(_bundle())
    features = tuple(
        replace(
            item,
            status=status,
            applicability=applicability,
            typed_value=None,
            reasons=(),
        )
        if item.feature_id is PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS
        else item
        for item in profile.features
    )
    profile = replace(profile, features=features)
    predictor = ControlledReferencePredictor()

    result = _predict(profile, predictor=predictor)

    assert result.status is status
    assert result.applicability is applicability
    assert result.predicted_value is None
    assert result.provenance.input_traces[0].status is status
    assert result.provenance.withheld_reason_or_none is (
        PredictionWithheldReason.REQUIRED_X_PE_INPUT_NOT_AVAILABLE
    )
    assert predictor.calls == 0


def test_missing_required_context_withholds_without_hidden_default() -> None:
    profile = _build(_bundle())
    predictor = ControlledReferencePredictor()
    request = _request(profile, context=_context(profile, environment=False))

    result = _predict(profile, predictor=predictor, request=request)

    assert result.status is FullModelStatus.UNAVAILABLE
    assert result.predicted_value is None
    assert result.provenance.withheld_reason_or_none is (
        PredictionWithheldReason.REQUIRED_CONTEXT_INPUT_NOT_AVAILABLE
    )
    assert next(
        item
        for item in result.context_inputs
        if item.field is PredictionContextField.ENVIRONMENT
    ).value_or_none is None
    assert predictor.calls == 0


def test_upstream_missing_input_reason_and_source_reference_survive_withholding() -> None:
    profile = _build(_bundle(observed_value=None))
    definition = _definition(
        required_features=(PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME,)
    )
    predictor = ControlledReferencePredictor(definition=definition)

    result = _predict(profile, predictor=predictor)

    trace = result.provenance.input_traces[0]
    assert result.status is FullModelStatus.UNAVAILABLE
    assert result.predicted_value is None
    assert DynamicEvidenceReason.OBSERVATION_NOT_COLLECTED in trace.upstream_reasons
    assert trace.source_refs == _feature(
        profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME
    ).source_refs
    assert "OBSERVATION_NOT_COLLECTED" in result.explanation
    assert predictor.calls == 0


def test_theta_must_match_predictor_identity_version_and_complete_inventory() -> None:
    profile = _build(_bundle())

    wrong_predictor = _parameters(predictor_ref=PredictorRef("OTHER", "1"))
    with pytest.raises(ValueError, match="different predictor"):
        _predict(profile, request=_request(profile, parameters=wrong_predictor))

    wrong_version = _parameters(
        identity=PredictionParameterSetIdentity(PARAMETER_IDENTITY.parameter_set_id, "2")
    )
    with pytest.raises(ValueError, match="identity/version"):
        _predict(profile, request=_request(profile, parameters=wrong_version))

    missing = _parameters(entries=())
    with pytest.raises(ValueError, match="exactly match"):
        _predict(profile, request=_request(profile, parameters=missing))


def test_theta_rejects_duplicate_entries_and_inexact_float_values() -> None:
    entry = PredictionParameter("requirement_weight", Fraction(1, 4))
    with pytest.raises(ValueError, match="duplicates"):
        _parameters(entries=(entry, entry))
    with pytest.raises(TypeError, match="exact Fraction or Decimal"):
        PredictionParameter("requirement_weight", 0.25)


@pytest.mark.parametrize("value", (Fraction(-1, 10), Fraction(11, 10)))
def test_predictor_output_outside_unit_interval_is_rejected_without_clamping(value) -> None:
    with pytest.raises(ValueError, match=r"\[0,1\]"):
        _predict(predictor=ControlledReferencePredictor(output=value))


def test_predictor_float_output_is_rejected() -> None:
    with pytest.raises(TypeError, match="exact Fraction"):
        _predict(predictor=ControlledReferencePredictor(output=0.5))


def test_user_and_audit_views_separate_observed_and_predicted_records() -> None:
    dynamic = _bundle()
    profile = _build(dynamic)
    observed = _assess(profile)
    prediction = _predict(profile)
    bundle = FullModelReportBundle(
        assessment_result=dynamic[0],
        feature_profile=profile,
        product_quality_assessment=observed,
        predicted_product_quality=prediction,
    )

    user = UserFullModelReporter().render_projection(bundle)
    audit = AuditFullModelReporter().render_projection(bundle)

    assert "Спостережуваний показник якості продукту" in user
    assert "OBSERVED_REFERENCE_INDICATOR" in user
    assert "Прогнозована якість продукту (ŷ_PE)" in user
    assert "PREDICTED_PERFORMANCE_EFFICIENCY" in user
    assert "Predicted product quality (y_hat_PE)" in audit
    for expected in (
        "predictor_id: TC02-CONTROLLED-REFERENCE-PE",
        "parameter_set_id: TC02-CONTROLLED-REFERENCE-THETA",
        "calibration_status: PROVISIONAL_NOT_CALIBRATED",
        "input_traces:",
        "context_inputs:",
        "predicted_value: Fraction(",
        "provenance:",
    ):
        assert expected in audit


def test_omitted_prediction_keeps_existing_report_output_byte_for_byte() -> None:
    dynamic = _bundle()
    profile = _build(dynamic)
    observed = _assess(profile)
    implicit = FullModelReportBundle(
        assessment_result=dynamic[0],
        feature_profile=profile,
        product_quality_assessment=observed,
    )
    explicit = FullModelReportBundle(
        assessment_result=dynamic[0],
        feature_profile=profile,
        product_quality_assessment=observed,
        predicted_product_quality=None,
    )

    assert UserFullModelReporter().render(implicit) == UserFullModelReporter().render(explicit)
    assert AuditFullModelReporter().render(implicit) == AuditFullModelReporter().render(explicit)
    assert "Прогнозована якість продукту" not in UserFullModelReporter().render(implicit)
    assert "Predicted product quality" not in AuditFullModelReporter().render(implicit)


def test_prediction_field_is_appended_after_the_complete_legacy_bundle_sequence() -> None:
    legacy_fields = (
        "assessment_result",
        "metric_profile",
        "criterion_binding",
        "observation_resolution",
        "conformance",
        "feature_profile",
        "product_quality_assessment",
        "problem_resolutions",
        "defect_population",
        "defect_quality_relations",
        "risk_assessments",
        "corrective_action_resolutions",
        "corrective_actions",
        "specification_versions",
        "external_revisions",
        "action_applications",
        "reassessment_runs",
        "comparisons",
        "process_states",
        "process_transitions",
    )
    assert tuple(item.name for item in fields(FullModelReportBundle)) == (
        *legacy_fields,
        "predicted_product_quality",
        "quantitative_risk_assessments",
    )

    dynamic = _bundle()
    profile = _build(dynamic)
    observed = _assess(profile)
    risk_bundle, _, _ = _positive()
    problem_resolution = risk_bundle[2]

    historical_positional_bundle = FullModelReportBundle(
        dynamic[0],
        None,
        None,
        None,
        None,
        profile,
        observed,
        (problem_resolution,),
    )

    assert historical_positional_bundle.problem_resolutions == (problem_resolution,)
    assert historical_positional_bundle.predicted_product_quality is None
    assert historical_positional_bundle.quantitative_risk_assessments == ()

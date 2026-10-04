"""Explicit fixture data for the TC-06 Full Model v1.0 acceptance scenario."""

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction

from requirements_quality_assessment.checkpoint import (
    CheckpointComparator,
    PolicyProviderRef,
    PolicySourceRef,
    ThresholdPolicy,
)
from requirements_quality_assessment.corrective_action import (
    ActionCreatorSource,
    ApplicationIdentityContext,
    ExternalProviderRef,
    ExternalRevisionProviderKind,
    RevisionRef,
)
from requirements_quality_assessment.cross_analysis import CrossObservationRef
from requirements_quality_assessment.domain import FeatureId, Requirement, UnitLabel
from requirements_quality_assessment.dynamic_evidence import (
    DYNAMIC_CONTRACT_REF,
    RESPONSE_TIME_METRIC_REF,
    SUPPORTED_CONTEXT_IDENTITY,
    Applicability,
    ConformanceOutcome,
    DynamicEvidenceAssessmentRef,
    EnvironmentRef,
    FullModelStatus,
    ObservationCollectionRef,
    ObservationSlotRef,
    ObservationSourceKind,
    ProductRef,
    make_dynamic_observation,
)
from requirements_quality_assessment.full_model import (
    CheckpointExtensionInput,
    EvidenceReuseInput,
    ExternalRequirementReplacement,
    ExternalRevisionInput,
    FullModelRequest,
    FullQualityExtensionInput,
    PredictionExtensionInput,
    QuantitativeRiskExtensionInput,
    QuantitativeRiskOperandInput,
)
from requirements_quality_assessment.full_quality import (
    EXTERNAL_PROPERTY_IDS,
    ExternalAssessmentProvenance,
    ExternalAssessmentSourceRef,
    ExternalAssessmentState,
    ExternalPropertyAssessment,
    ExternalPropertyJudgment,
)
from requirements_quality_assessment.metrics import (
    ArtifactRef,
    AssessmentRef,
    ContractRef,
    MetricId,
    RequirementSubjectRef,
    RuleRef,
    RuleVersionAuthority,
)
from requirements_quality_assessment.performance_efficiency import (
    ConformanceFeatureValue,
    PerformanceEfficiencyFeatureId,
    ProcessStage,
    ProcessStateRef,
    ProductQualityCharacteristicId,
    RequirementMetricFeatureValue,
)
from requirements_quality_assessment.product_quality import (
    CalibrationStatus,
    ProductQualityAssessmentEventRef,
)
from requirements_quality_assessment.product_quality_prediction import (
    PREDICTION_CONTRACT_REF,
    PerformanceEfficiencyEvaluationInput,
    PerformanceEfficiencyPredictionContext,
    PredictionCalibrationStatus,
    PredictionContextField,
    PredictionEventRef,
    PredictionParameter,
    PredictionParameterSet,
    PredictionParameterSetIdentity,
    PredictorDefinition,
    PredictorRef,
)
from requirements_quality_assessment.quantitative_risk import (
    QuantitativeRiskContextRef,
    QuantitativeRiskOperandKind,
    QuantitativeRiskOperandSourceRef,
)
from requirements_quality_assessment.reassessment import (
    ComponentVersionSet,
    EvidenceReuseDisposition,
    EvidenceReuseReason,
    ExactIdentityCheck,
    ReassessmentIdentityContext,
    VersionedComponentRef,
)
from requirements_quality_assessment.risk import RiskAssessmentEventRef


SCENARIO_ID = "CONTROLLED_RESEARCH_REFERENCE_SCENARIO"
V1_R001 = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
V1_R002 = "Час відгуку не нижче 5 с при 500 одночасних користувачах"
V2_R002 = "Час відгуку ≤ 5 с при 500 одночасних користувачах"

PREDICTOR_REF = PredictorRef("TC06-CONTROLLED-REFERENCE-PE", "1")
PARAMETER_IDENTITY = PredictionParameterSetIdentity("TC06-CONTROLLED-THETA", "1")


class ControlledResearchReferencePredictor:
    """Fixture-only deterministic evaluator; it is not a production predictor."""

    def __init__(self) -> None:
        self.calls = 0
        self._definition = PredictorDefinition(
            predictor_ref=PREDICTOR_REF,
            supported_characteristic=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
            invocation_contract_ref=PREDICTION_CONTRACT_REF,
            required_feature_ids=(
                PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS,
                PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME,
            ),
            required_context_fields=(
                PredictionContextField.PRODUCT,
                PredictionContextField.ENVIRONMENT,
                PredictionContextField.RESPONSE_TIME_CRITERION_CONTEXT,
            ),
            required_parameter_names=("requirement_weight",),
            parameter_set_identity=PARAMETER_IDENTITY,
            calibration_status=PredictionCalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
            source_or_rationale=(
                "TC-06 controlled fixture for deterministic contract execution only; "
                "no confidence, calibration, or universal predictive-validity claim."
            ),
        )

    @property
    def definition(self) -> PredictorDefinition:
        return self._definition

    def evaluate(self, evaluation_input: PerformanceEfficiencyEvaluationInput) -> Fraction:
        self.calls += 1
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


@dataclass(frozen=True, slots=True)
class ControlledResearchReferenceScenario:
    scenario_id: str
    request: FullModelRequest
    predictor: ControlledResearchReferencePredictor
    threshold_policy: ThresholdPolicy


def _external_assessments(
    requirement_id: str,
    source_line: int,
    artifact: ArtifactRef,
) -> tuple[ExternalPropertyAssessment, ...]:
    requirement_ref = RequirementSubjectRef(artifact, requirement_id, source_line)
    return tuple(
        ExternalPropertyAssessment(
            property_id=property_id,
            state=ExternalAssessmentState.AVAILABLE,
            judgment=ExternalPropertyJudgment(
                f"TC06-{requirement_id}-{property_id.value}-EXPERT-JUDGMENT"
            ),
            provenance=ExternalAssessmentProvenance(
                source_ref=ExternalAssessmentSourceRef("TC06-CONTROLLED-EXPERT", "1"),
                requirement_ref=requirement_ref,
                artifact_ref=artifact,
                assessment_contract_ref=ContractRef("TC06-EXTERNAL-PROPERTIES", "1"),
                assessment_rule_ref=RuleRef(
                    f"TC06-EXTERNAL-{property_id.value}",
                    "1",
                    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
                ),
            ),
            explanation="Explicit controlled expert fixture; not inferred from requirement text.",
        )
        for property_id in EXTERNAL_PROPERTY_IDS
    )


def _build_controlled_research_reference_scenario() -> ControlledResearchReferenceScenario:
    requirements = (
        Requirement("R001", 1, V1_R001),
        Requirement("R002", 2, V1_R002),
    )
    artifact_v1 = ArtifactRef("SPEC-TC06-REFERENCE", "v1")
    artifact_v2 = ArtifactRef("SPEC-TC06-REFERENCE", "v2")
    assessment_v1 = AssessmentRef("ASSESS-TC06-REFERENCE", "v1", artifact_v1)
    assessment_v2 = AssessmentRef("ASSESS-TC06-REFERENCE", "v2", artifact_v2)
    process_v1 = ProcessStateRef(
        "PROCESS-TC06-REFERENCE", "v1", ProcessStage.REFERENCE_VERIFICATION
    )
    process_v2 = ProcessStateRef(
        "PROCESS-TC06-REFERENCE", "v2", ProcessStage.REFERENCE_VERIFICATION
    )
    product = ProductRef("PRODUCT-TC06-REFERENCE", "1")
    environment = EnvironmentRef("ENV-TC06-REFERENCE", "1")
    collection = ObservationCollectionRef(
        "COLLECTION-TC06-REFERENCE",
        "1",
        product,
        environment,
        ObservationSourceKind.DETERMINISTIC_FIXTURE,
    )
    slot = ObservationSlotRef(collection, 0)
    observation = make_dynamic_observation(
        slot,
        RESPONSE_TIME_METRIC_REF,
        Decimal("1.8"),
        UnitLabel.SECOND,
        SUPPORTED_CONTEXT_IDENTITY,
        "OBSERVATION-TC06-REFERENCE",
    )
    reuse_checks = (
        ("product_ref", observation.product_ref),
        ("observation_source_kind", observation.source_kind),
        ("collection_ref", observation.collection_ref),
        ("metric_ref", observation.metric_ref),
        ("unit", observation.unit),
        ("context_identity", observation.context_identity),
        ("applicability", Applicability.APPLICABLE),
        ("process_stage", process_v2.stage),
        ("source_contract_permission", True),
    )
    component_versions = ComponentVersionSet((
        VersionedComponentRef("FULL_MODEL_CONTRACT", "FULL-MODEL-V0.1-CONTRACT", "1"),
        VersionedComponentRef(
            "DYNAMIC_EVIDENCE", "FULL-MODEL-V0.1-DYNAMIC-EVIDENCE", "1"
        ),
        VersionedComponentRef(
            "PE_FEATURES", "FULL-MODEL-V0.1-PRODUCT-QUALITY-FEATURE", "1"
        ),
        VersionedComponentRef(
            "PRODUCT_QUALITY", "FULL-MODEL-V0.1-PRODUCT-QUALITY-ASSESSMENT", "1"
        ),
        VersionedComponentRef(
            "DEFECT_RISK", "FULL-MODEL-V0.1-DEFECT-QUALITY-RISK", "1"
        ),
        VersionedComponentRef(
            "PROCESS_REASSESSMENT", "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", "1"
        ),
    ))
    predictor = ControlledResearchReferencePredictor()
    parameter_set = PredictionParameterSet(
        identity=PARAMETER_IDENTITY,
        predictor_ref=PREDICTOR_REF,
        entries=(PredictionParameter("requirement_weight", Fraction(1, 4)),),
        source_or_rationale=(
            "Explicit TC-06 fixture theta; demonstrational and not calibrated."
        ),
        calibration_status=PredictionCalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
        governing_contract_ref=PREDICTION_CONTRACT_REF,
    )
    prediction = PredictionExtensionInput(
        event_ref=PredictionEventRef("PREDICTION-TC06-REFERENCE", "1"),
        context=PerformanceEfficiencyPredictionContext(
            product,
            artifact_v1,
            process_v1,
            environment,
            collection,
            SUPPORTED_CONTEXT_IDENTITY,
        ),
        parameter_set=parameter_set,
        predictor=predictor,
    )
    operand_values = (
        Fraction(1, 2),
        Fraction(1, 4),
        Fraction(3, 4),
        Fraction(2, 3),
    )
    operands = tuple(
        QuantitativeRiskOperandInput(
            kind=kind,
            operand_id=f"TC06-{kind.value}",
            operand_version="1",
            state=FullModelStatus.AVAILABLE,
            value=value,
            source_ref=QuantitativeRiskOperandSourceRef(
                f"TC06-{kind.value}-SOURCE", "1", "TC06-CONTROLLED-PROVIDER", "1"
            ),
            source_or_rationale=(
                "Explicit normalized TC-06 fixture operand; no calibration claim."
            ),
            calibration_status=CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
            context_ref=(
                QuantitativeRiskContextRef("TC06-CONTEXT", "1")
                if kind is QuantitativeRiskOperandKind.CONTEXT_FACTOR
                else None
            ),
        )
        for kind, value in zip(QuantitativeRiskOperandKind, operand_values, strict=True)
    )
    threshold_policy = ThresholdPolicy(
        "TC06-QB-CHECKPOINT-POLICY",
        "1",
        PolicySourceRef(SCENARIO_ID, "1"),
        PolicyProviderRef("TC06-CONTROLLED-PROVIDER", "1"),
        "Fixture-only v1/v2 predicate evaluation; not a release policy.",
        CheckpointComparator.GREATER_THAN_OR_EQUAL,
        Fraction(1, 1),
        ContractRef("TC06-CHECKPOINT-POLICY", "1"),
    )
    request = FullModelRequest(
        requirements=requirements,
        artifact_v1=artifact_v1,
        assessment_v1=assessment_v1,
        process_ref_v1=process_v1,
        selected_observation_ref=CrossObservationRef(
            "R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0
        ),
        selected_requirement_id="R001",
        product_ref=product,
        environment_ref=environment,
        collection_ref=collection,
        observation_source_kind=ObservationSourceKind.DETERMINISTIC_FIXTURE,
        observation_slot_index=0,
        observation_id="OBSERVATION-TC06-REFERENCE",
        observed_value=Decimal("1.8"),
        observation_unit=UnitLabel.SECOND,
        criterion_context=SUPPORTED_CONTEXT_IDENTITY,
        dynamic_assessment_v1=DynamicEvidenceAssessmentRef(
            "DYNAMIC-TC06-REFERENCE", "v1", artifact_v1, product, collection
        ),
        product_quality_event_v1=ProductQualityAssessmentEventRef(
            "PRODUCT-QUALITY-TC06-REFERENCE", "v1", product, artifact_v1
        ),
        risk_event_v1=RiskAssessmentEventRef(
            "RISK-TC06-REFERENCE", "v1", artifact_v1, process_v1
        ),
        action_id="ACTION-TC06-REFERENCE",
        action_creator=ActionCreatorSource("TC06-CORRECTIVE-ACTION-PROPOSER", "1"),
        revision=ExternalRevisionInput(
            child_artifact_ref=artifact_v2,
            revision_ref=RevisionRef("REVISION-TC06-REFERENCE", "1"),
            provider_kind=ExternalRevisionProviderKind.CONTROLLED_REFERENCE_FIXTURE,
            provider_ref=ExternalProviderRef("TC06-QB-CONFLICT-REVISION", "1"),
            replacements=(ExternalRequirementReplacement("R002", V2_R002),),
            reason="Explicit externally supplied TC-06 controlled revision.",
            application_identity=ApplicationIdentityContext(
                "APPLICATION-TC06-REFERENCE", "1", "v2", "ARTIFACT-TRANSITION-TC06"
            ),
        ),
        process_ref_v2=process_v2,
        assessment_v2=assessment_v2,
        reuse=EvidenceReuseInput(
            EvidenceReuseDisposition.REUSE_ALLOWED,
            tuple(
                ExactIdentityCheck(name, value, value, True)
                for name, value in reuse_checks
            ),
            (EvidenceReuseReason.EXACT_IDENTITY_AND_CONTEXT_MATCH,),
        ),
        dynamic_assessment_v2=DynamicEvidenceAssessmentRef(
            "DYNAMIC-TC06-REFERENCE", "v2", artifact_v2, product, collection
        ),
        product_quality_event_v2=ProductQualityAssessmentEventRef(
            "PRODUCT-QUALITY-TC06-REFERENCE", "v2", product, artifact_v2
        ),
        risk_event_v2=RiskAssessmentEventRef(
            "RISK-TC06-REFERENCE", "v2", artifact_v2, process_v2
        ),
        reassessment_identity=ReassessmentIdentityContext(
            "REASSESSMENT-TC06-REFERENCE", "1", process_v2
        ),
        component_versions=component_versions,
        comparison_ids=(
            "COMPARE-TC06-QB",
            "COMPARE-TC06-PROBLEM",
            "COMPARE-TC06-RISK",
            "COMPARE-TC06-PRODUCT-QUALITY",
        ),
        comparison_version="1",
        process_transition_id="PROCESS-TRANSITION-TC06",
        full_quality=(
            FullQualityExtensionInput(
                "R001", _external_assessments("R001", 1, artifact_v1)
            ),
            FullQualityExtensionInput(
                "R002", _external_assessments("R002", 2, artifact_v1)
            ),
        ),
        prediction=prediction,
        quantitative_risk=QuantitativeRiskExtensionInput(
            "QUANTITATIVE-RISK-TC06", "1", operands
        ),
        checkpoints=(
            CheckpointExtensionInput(
                "CHECKPOINT-TC06-QB-V1",
                "1",
                "v1",
                MetricId.SPEC_QB_CONSISTENCY,
                threshold_policy,
            ),
            CheckpointExtensionInput(
                "CHECKPOINT-TC06-QB-V2",
                "1",
                "v2",
                MetricId.SPEC_QB_CONSISTENCY,
                threshold_policy,
            ),
        ),
    )
    return ControlledResearchReferenceScenario(
        SCENARIO_ID, request, predictor, threshold_policy
    )


CONTROLLED_RESEARCH_REFERENCE_SCENARIO = (
    _build_controlled_research_reference_scenario()
)


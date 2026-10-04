"""Public immutable application contract for the supported Full Model path."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction

from ..checkpoint import CheckpointEvaluation, ThresholdPolicy
from ..corrective_action import (
    ActionApplication, ActionCreatorSource, ApplicationIdentityContext,
    CorrectiveActionResolution, ExternalProviderRef,
    ExternalRevisionProviderKind, ExternallySuppliedRevision, RevisionRef,
    SpecificationVersion,
)
from ..cross_analysis import CrossObservationRef, SpecificationAssessmentResult
from ..defect_quality import DefectPopulationSnapshot, DefectQualityRelation, ProblemClaimResolution
from ..domain import Requirement, UnitLabel
from ..dynamic_evidence import (
    ConformanceAssessment, CriterionBindingResult, CriterionContextIdentity,
    DynamicEvidenceAssessmentRef, EnvironmentRef, ObservationCollectionRef,
    FullModelStatus, ObservationResolution, ObservationSourceKind, ProductRef,
)
from ..full_model_reporter import FullModelReportBundle
from ..full_quality import ExternalPropertyAssessment, FullRequirementQualityProfile
from ..metrics import ArtifactRef, AssessmentRef, MetricId, MetricProfile
from ..performance_efficiency import PerformanceEfficiencyFeatureProfile, ProcessStateRef
from ..process import ProcessAssessmentState, ProcessStateTransition
from ..product_quality import ProductQualityAssessment, ProductQualityAssessmentEventRef
from ..product_quality import CalibrationStatus
from ..product_quality_prediction import (
    PerformanceEfficiencyPredictionContext, PerformanceEfficiencyPredictor,
    PredictionEventRef, PredictionParameterSet, PredictedPerformanceEfficiency,
)
from ..quantitative_risk import (
    QuantitativeLocalRiskAssessment, QuantitativeRiskContextRef,
    QuantitativeRiskOperandKind, QuantitativeRiskOperandSourceRef,
)
from ..reassessment import (
    ComponentVersionSet, EvidenceReuseDisposition, EvidenceReuseReason,
    ExactIdentityCheck, ReassessmentIdentityContext, ReassessmentRun,
    ResultComparison,
)
from ..risk import BoundedRiskAssessment, RiskAssessmentEventRef


@dataclass(frozen=True, slots=True)
class ExternalRequirementReplacement:
    requirement_id: str
    replacement_text: str


@dataclass(frozen=True, slots=True)
class ExternalRevisionInput:
    child_artifact_ref: ArtifactRef
    revision_ref: RevisionRef
    provider_kind: ExternalRevisionProviderKind
    provider_ref: ExternalProviderRef
    replacements: tuple[ExternalRequirementReplacement, ...]
    reason: str
    application_identity: ApplicationIdentityContext


@dataclass(frozen=True, slots=True)
class EvidenceReuseInput:
    disposition: EvidenceReuseDisposition
    identity_checks: tuple[ExactIdentityCheck, ...]
    reasons: tuple[EvidenceReuseReason, ...]


@dataclass(frozen=True, slots=True)
class FullQualityExtensionInput:
    requirement_id: str
    external_assessments: tuple[ExternalPropertyAssessment, ...]


@dataclass(frozen=True, slots=True)
class PredictionExtensionInput:
    event_ref: PredictionEventRef
    context: PerformanceEfficiencyPredictionContext
    parameter_set: PredictionParameterSet
    predictor: PerformanceEfficiencyPredictor


@dataclass(frozen=True, slots=True)
class QuantitativeRiskOperandInput:
    kind: QuantitativeRiskOperandKind
    operand_id: str
    operand_version: str
    state: FullModelStatus
    value: Fraction | None
    source_ref: QuantitativeRiskOperandSourceRef
    source_or_rationale: str
    calibration_status: CalibrationStatus
    context_ref: QuantitativeRiskContextRef | None = None


@dataclass(frozen=True, slots=True)
class QuantitativeRiskExtensionInput:
    calculation_id: str
    calculation_version: str
    operands: tuple[QuantitativeRiskOperandInput, ...]


@dataclass(frozen=True, slots=True)
class CheckpointExtensionInput:
    checkpoint_id: str
    checkpoint_version: str
    result_version: str
    metric_id: MetricId
    threshold_policy: ThresholdPolicy


@dataclass(frozen=True, slots=True)
class FullModelServiceReportBundle(FullModelReportBundle):
    """Additive TC-05 bundle without mutating the accepted base bundle layout."""

    full_requirement_quality_profiles: tuple[FullRequirementQualityProfile, ...] = ()

    def __post_init__(self) -> None:
        super(FullModelServiceReportBundle, self).__post_init__()
        if not isinstance(self.full_requirement_quality_profiles, tuple) or any(
            not isinstance(item, FullRequirementQualityProfile)
            for item in self.full_requirement_quality_profiles
        ):
            raise TypeError("full_requirement_quality_profiles must contain typed profiles")


@dataclass(frozen=True, slots=True)
class FullModelRequest:
    requirements: tuple[Requirement, ...]
    artifact_v1: ArtifactRef
    assessment_v1: AssessmentRef
    process_ref_v1: ProcessStateRef
    selected_observation_ref: CrossObservationRef
    selected_requirement_id: str
    product_ref: ProductRef
    environment_ref: EnvironmentRef
    collection_ref: ObservationCollectionRef
    observation_source_kind: ObservationSourceKind
    observation_slot_index: int
    observation_id: str
    observed_value: Decimal
    observation_unit: UnitLabel
    criterion_context: CriterionContextIdentity
    dynamic_assessment_v1: DynamicEvidenceAssessmentRef
    product_quality_event_v1: ProductQualityAssessmentEventRef
    risk_event_v1: RiskAssessmentEventRef
    action_id: str
    action_creator: ActionCreatorSource
    revision: ExternalRevisionInput
    process_ref_v2: ProcessStateRef
    assessment_v2: AssessmentRef
    reuse: EvidenceReuseInput
    dynamic_assessment_v2: DynamicEvidenceAssessmentRef
    product_quality_event_v2: ProductQualityAssessmentEventRef
    risk_event_v2: RiskAssessmentEventRef
    reassessment_identity: ReassessmentIdentityContext
    component_versions: ComponentVersionSet
    comparison_ids: tuple[str, str, str, str]
    comparison_version: str
    process_transition_id: str
    full_quality: tuple[FullQualityExtensionInput, ...] = ()
    prediction: PredictionExtensionInput | None = None
    quantitative_risk: QuantitativeRiskExtensionInput | None = None
    checkpoints: tuple[CheckpointExtensionInput, ...] = ()


@dataclass(frozen=True, slots=True)
class FullModelResult:
    initial_specification_assessment: SpecificationAssessmentResult
    metric_profile: MetricProfile
    criterion_binding: CriterionBindingResult
    observation_resolution: ObservationResolution
    conformance: ConformanceAssessment
    feature_profile: PerformanceEfficiencyFeatureProfile
    observed_product_quality: ProductQualityAssessment
    problem_resolutions: tuple[ProblemClaimResolution, ...]
    defect_population: DefectPopulationSnapshot
    defect_quality_relations: tuple[DefectQualityRelation, ...]
    risk_assessments: tuple[BoundedRiskAssessment, ...]
    corrective_action_resolution: CorrectiveActionResolution
    initial_specification: SpecificationVersion
    revised_specification: SpecificationVersion
    external_revision: ExternallySuppliedRevision
    action_application: ActionApplication
    reassessment: ReassessmentRun
    comparisons: tuple[ResultComparison, ...]
    process_v1: ProcessAssessmentState
    process_v2: ProcessAssessmentState
    process_transition: ProcessStateTransition
    report_bundle: FullModelServiceReportBundle
    full_quality_profiles: tuple[FullRequirementQualityProfile, ...] = ()
    prediction: PredictedPerformanceEfficiency | None = None
    quantitative_risk_assessments: tuple[QuantitativeLocalRiskAssessment, ...] = ()
    checkpoint_evaluations: tuple[CheckpointEvaluation, ...] = ()

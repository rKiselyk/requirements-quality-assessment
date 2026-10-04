"""TC-06 candidate acceptance for the integrated Full Model v1.0 research path."""

from dataclasses import fields
from fractions import Fraction
from hashlib import sha256

from requirements_quality_assessment.checkpoint import CheckpointOutcome
from requirements_quality_assessment.corrective_action import ExternalRevisionProviderKind
from requirements_quality_assessment.cross_analysis import CrossResultState
from requirements_quality_assessment.defect_quality import (
    ProblemDisposition,
    RelationNonClaim,
)
from requirements_quality_assessment.dynamic_evidence import (
    Applicability,
    ConformanceOutcome,
    FullModelStatus,
)
from requirements_quality_assessment.full_model import FullModelService
from requirements_quality_assessment.full_model_reporter import (
    AuditFullModelReporter,
    UserFullModelReporter,
)
from requirements_quality_assessment.full_quality import (
    AUTOMATIC_PROPERTY_IDS,
    EXTERNAL_PROPERTY_IDS,
    ExternalAssessmentState,
    PropertyAssessmentOrigin,
)
from requirements_quality_assessment.metrics import MetricId
from requirements_quality_assessment.product_quality import ProductQualityAssessment
from requirements_quality_assessment.product_quality_prediction import (
    PredictedPerformanceEfficiency,
    PredictionCalibrationStatus,
    PredictionResultKind,
)
from requirements_quality_assessment.quantitative_risk import (
    QuantitativeRiskOperandKind,
)
from requirements_quality_assessment.reassessment import ComparisonKind
from requirements_quality_assessment.risk import RiskClassification

from reference_acceptance_data import (
    CONTROLLED_RESEARCH_REFERENCE_SCENARIO,
    PARAMETER_IDENTITY,
    PREDICTOR_REF,
    SCENARIO_ID,
    V1_R001,
    V1_R002,
    V2_R002,
)


EXPECTED_USER_SHA256 = "32f1be06e5dffb85745ae222d0cd1f4bb7e1ceb3ab754fcbf92bb84df38e8789"
EXPECTED_AUDIT_SHA256 = "c8f2ed47719207fdbff1f6cfa6b2242b0f3b86692dcbcea72ec711c807b14923"


def test_controlled_research_reference_scenario_covers_full_model_v1() -> None:
    scenario = CONTROLLED_RESEARCH_REFERENCE_SCENARIO
    assert scenario.scenario_id == SCENARIO_ID == "CONTROLLED_RESEARCH_REFERENCE_SCENARIO"

    # This is the single public application call in the canonical acceptance scenario.
    result = FullModelService().run(scenario.request)

    source_v1 = result.initial_specification_assessment
    core_v2, downstream_v2 = result.reassessment.produced_results
    qb_v1 = next(
        item for item in result.metric_profile.entries
        if item.metric_id is MetricId.SPEC_QB_CONSISTENCY
    )
    qb_v2 = next(
        item for item in core_v2.metric_profile.entries
        if item.metric_id is MetricId.SPEC_QB_CONSISTENCY
    )

    # 1-4: ingestion, automatic C/V/U, nine properties, metrics and QB.
    assert tuple(
        record.extraction_result.requirement.text for record in source_v1.records
    ) == (V1_R001, V1_R002)
    assert tuple(
        record.extraction_result.requirement.id for record in source_v1.records
    ) == ("R001", "R002")
    assert len(result.full_quality_profiles) == 2
    for profile in result.full_quality_profiles:
        assert tuple(item.property_id for item in profile.properties[:3]) == (
            AUTOMATIC_PROPERTY_IDS
        )
        assert all(
            item.origin is PropertyAssessmentOrigin.AUTOMATIC
            and item.automatic_assessment is not None
            and item.external_assessment is None
            for item in profile.properties[:3]
        )
        assert tuple(item.property_id for item in profile.properties[3:]) == (
            EXTERNAL_PROPERTY_IDS
        )
        assert all(
            item.origin is PropertyAssessmentOrigin.EXTERNAL_EXPERT
            and item.external_assessment is not None
            and item.external_assessment.state is ExternalAssessmentState.AVAILABLE
            and item.external_assessment.provenance.source_ref.source_id
            == "TC06-CONTROLLED-EXPERT"
            and item.external_assessment.provenance.source_ref.source_version == "1"
            and item.automatic_assessment is None
            for item in profile.properties[3:]
        )
        assert not {
            "score", "overall_score", "integrated_score", "quality_score"
        } & {item.name for item in fields(profile)}
    assert qb_v1.value == Fraction(0, 1)
    assert source_v1.cross_results[0].state is CrossResultState.CONFIRMED_CONFLICT

    # 5-10: dynamic evidence, conformance, X_PE, observed and predicted PE.
    assert result.criterion_binding.status is FullModelStatus.AVAILABLE
    assert result.criterion_binding.criterion is not None
    assert result.observation_resolution.status is FullModelStatus.AVAILABLE
    assert result.observation_resolution.observation is not None
    assert result.conformance.outcome is ConformanceOutcome.CONFORMS
    assert result.feature_profile.status is FullModelStatus.UNRESOLVED
    assert isinstance(result.observed_product_quality, ProductQualityAssessment)
    assert result.prediction is not None
    assert isinstance(result.prediction, PredictedPerformanceEfficiency)
    assert type(result.prediction) is not type(result.observed_product_quality)
    assert result.prediction.result_kind is (
        PredictionResultKind.PREDICTED_PERFORMANCE_EFFICIENCY
    )
    assert result.prediction.predicted_value == Fraction(5, 6)
    assert result.prediction.predictor_ref == PREDICTOR_REF
    assert result.prediction.parameter_set_ref.identity == PARAMETER_IDENTITY
    assert result.prediction.calibration_status is (
        PredictionCalibrationStatus.PROVISIONAL_NOT_CALIBRATED
    )
    assert scenario.predictor.calls == 1

    # 11-15: problem, structural R_DQ, categorical risk, r_ij, action.
    problem = next(item for item in result.problem_resolutions if item.problem is not None)
    assert problem.disposition is ProblemDisposition.CONFIRMED_SUPPORTED_PROBLEM
    relation = result.defect_quality_relations[0]
    assert RelationNonClaim.NOT_NUMERIC_RHO in relation.non_claims
    assert "rho" not in {item.name for item in fields(relation)}
    categorical_risk = result.risk_assessments[0]
    assert categorical_risk.classification is RiskClassification.RISK_IDENTIFIED
    quantitative_risk = result.quantitative_risk_assessments[0]
    assert tuple(item.kind for item in quantitative_risk.operands) == tuple(
        QuantitativeRiskOperandKind
    )
    assert tuple(item.value for item in quantitative_risk.operands) == (
        Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(2, 3)
    )
    assert all(
        item.provenance.source_ref.provider_id == "TC06-CONTROLLED-PROVIDER"
        and item.provenance.source_ref.provider_version == "1"
        for item in quantitative_risk.operands
    )
    assert quantitative_risk.local_risk == Fraction(1, 16)
    assert not {"aggregate_risk", "Risk_j", "priority"} & {
        item.name for item in fields(quantitative_risk)
    }
    assert result.corrective_action_resolution.action is not None

    # 16-20: external revision, reassessment, literal comparisons, checkpoints, process.
    assert result.external_revision.provider_kind is (
        ExternalRevisionProviderKind.CONTROLLED_REFERENCE_FIXTURE
    )
    assert tuple(item.text for item in result.initial_specification.requirements) == (
        V1_R001, V1_R002
    )
    assert tuple(item.text for item in result.revised_specification.requirements) == (
        V1_R001, V2_R002
    )
    assert tuple(item.lineage_id for item in result.initial_specification.requirements) == tuple(
        item.lineage_id for item in result.revised_specification.requirements
    )
    assert qb_v2.value == Fraction(1, 1)
    assert downstream_v2.target_problem_resolution.disposition is (
        ProblemDisposition.NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE
    )
    assert downstream_v2.target_problem_resolution.problem is None
    assert downstream_v2.risk_assessment.status is FullModelStatus.NOT_APPLICABLE
    assert downstream_v2.risk_assessment.classification is None
    assert tuple(item.comparison_kind for item in result.comparisons) == (
        ComparisonKind.INCREASED,
        ComparisonKind.STATE_CHANGED,
        ComparisonKind.STATE_CHANGED,
        ComparisonKind.STATE_CHANGED,
    )
    assert result.comparisons[0].before_state_and_value.exact_value == Fraction(0, 1)
    assert result.comparisons[0].after_state_and_value.exact_value == Fraction(1, 1)
    assert tuple(item.outcome for item in result.checkpoint_evaluations) == (
        CheckpointOutcome.NOT_SATISFIED,
        CheckpointOutcome.SATISFIED,
    )
    assert all(
        item.selected_result.result_identity == MetricId.SPEC_QB_CONSISTENCY.value
        and item.threshold_policy is scenario.threshold_policy
        and item.threshold_policy.threshold == Fraction(1, 1)
        for item in result.checkpoint_evaluations
    )
    assert CheckpointOutcome.SATISFIED.value not in {"PROCEED", "RELEASE"}
    assert all(
        not {"proceed", "release", "release_decision"}
        & {field.name for field in fields(item)}
        for item in result.checkpoint_evaluations
    )
    assert result.process_v2.predecessor_process_state_ref == result.process_v1.ref
    assert result.process_transition.predecessor_process_state_ref == result.process_v1.ref
    assert result.process_transition.successor_process_state_ref == result.process_v2.ref

    # Missing states retain no value and remain distinct from the exact v1 QB zero.
    assert result.observed_product_quality.status is FullModelStatus.UNRESOLVED
    assert result.observed_product_quality.value is None
    assert downstream_v2.risk_assessment.status is FullModelStatus.NOT_APPLICABLE
    assert downstream_v2.risk_assessment.classification is None
    assert qb_v1.value == Fraction(0, 1)

    # 21-22: deterministic USER/AUDIT projections with explicit v1.0 identity.
    user_report = UserFullModelReporter().render(result.report_bundle)
    audit_report = AuditFullModelReporter().render(result.report_bundle)
    assert "Повна модель v1.0" in user_report
    assert "Full Model v1.0 audit path" in audit_report
    assert "НЕ є дозволом RELEASE або PROCEED" in user_report
    for expected in (
        "Якість вимог і специфікації",
        "Спостережуваний показник якості продукту",
        "Прогнозована якість продукту",
        "Категоріальний обмежений ризик: RISK_IDENTIFIED",
        "Кількісний r_ij: 1/16",
        "Outcome: NOT_SATISFIED",
        "Outcome: SATISFIED",
        "Переоцінювання і порівняння",
        "Перехід стану процесу",
    ):
        assert expected in user_report
    for expected in (
        "Nine-property requirement quality profiles",
        "Predicted product quality (y_hat_PE)",
        "Quantitative local risk r_ij",
        "Parameterized checkpoint evaluations",
        "Before/after comparisons",
        "Process state transitions",
        "local_risk: Fraction(1,16)",
        "outcome: SATISFIED",
    ):
        assert expected in audit_report
    forbidden = (
        "automatic improvement",
        "successful correction",
        "causal effect",
        "risk reduction proved",
        "release approved",
        "proceed authorized",
        "автоматичне покращення",
        "успішне виправлення",
        "зниження ризику доведено",
        "випуск схвалено",
    )
    combined = f"{user_report}\n{audit_report}".lower()
    assert not any(claim in combined for claim in forbidden)
    assert "не встановлює причинний ефект" in user_report
    assert sha256(user_report.encode("utf-8")).hexdigest() == EXPECTED_USER_SHA256
    assert sha256(audit_report.encode("utf-8")).hexdigest() == EXPECTED_AUDIT_SHA256

"""TC-05 public application-facade acceptance tests."""

from dataclasses import fields, replace
from decimal import Decimal
from fractions import Fraction
import json

from requirements_quality_assessment.corrective_action import (
    ActionCreatorSource, ApplicationIdentityContext, ExternalProviderRef,
    ExternalRevisionProviderKind, RevisionRef,
)
from requirements_quality_assessment.cross_analysis import CrossObservationRef
from requirements_quality_assessment.domain import FeatureId, Requirement, UnitLabel
from requirements_quality_assessment.dynamic_evidence import (
    DYNAMIC_CONTRACT_REF, RESPONSE_TIME_METRIC_REF, SUPPORTED_CONTEXT_IDENTITY,
    Applicability, DynamicEvidenceAssessmentRef, EnvironmentRef, FullModelStatus,
    ObservationCollectionRef, ObservationSlotRef, ObservationSourceKind,
    ProductRef, make_dynamic_observation,
)
from requirements_quality_assessment.full_model import (
    CheckpointExtensionInput, EvidenceReuseInput, ExternalRequirementReplacement,
    ExternalRevisionInput, FullModelRequest, FullModelResult, FullModelService,
    FullQualityExtensionInput, PredictionExtensionInput,
    QuantitativeRiskExtensionInput, QuantitativeRiskOperandInput,
)
from requirements_quality_assessment.full_model_reporter import AuditFullModelReporter, UserFullModelReporter
from requirements_quality_assessment.full_quality import (
    EXTERNAL_PROPERTY_IDS, ExternalAssessmentProvenance,
    ExternalAssessmentSourceRef, ExternalAssessmentState,
    ExternalPropertyAssessment, ExternalPropertyJudgment,
)
from requirements_quality_assessment.checkpoint import (
    CheckpointComparator, CheckpointOutcome, PolicyProviderRef, PolicySourceRef,
    ThresholdPolicy,
)
from requirements_quality_assessment.cli import main
from requirements_quality_assessment.metrics import (
    ArtifactRef, AssessmentRef, ContractRef, MetricId, RequirementSubjectRef,
    RuleRef, RuleVersionAuthority,
)
from requirements_quality_assessment.performance_efficiency import ProcessStage, ProcessStateRef
from requirements_quality_assessment.product_quality import CalibrationStatus, ProductQualityAssessmentEventRef
from requirements_quality_assessment.product_quality_prediction import (
    PerformanceEfficiencyPredictionContext, PredictionEventRef,
)
from requirements_quality_assessment.quantitative_risk import (
    QuantitativeRiskContextRef, QuantitativeRiskOperandKind,
    QuantitativeRiskOperandSourceRef,
)
from requirements_quality_assessment.reassessment import (
    ComponentVersionSet, EvidenceReuseDisposition, EvidenceReuseProvenance,
    EvidenceReuseReason, ExactIdentityCheck, ReassessmentIdentityContext,
    VersionedComponentRef,
)
from requirements_quality_assessment.risk import RiskAssessmentEventRef, RiskClassification
from test_product_quality_prediction import ControlledReferencePredictor, _parameters


def _request():
    requirements = (
        Requirement("R001", 1, "Час відгуку ≤ 2 с при 500 одночасних користувачах"),
        Requirement("R002", 2, "Час відгуку не нижче 5 с при 500 одночасних користувачах"),
    )
    artifact1 = ArtifactRef("SPEC-PROCESS-REF-001", "v1")
    artifact2 = ArtifactRef("SPEC-PROCESS-REF-001", "v2")
    assessment1 = AssessmentRef("ASSESS-PROCESS-REF-001", "v1", artifact1)
    assessment2 = AssessmentRef("ASSESS-PROCESS-REF-001", "v2", artifact2)
    process1 = ProcessStateRef("PROCESS-PROCESS-REF-001", "v1", ProcessStage.REFERENCE_VERIFICATION)
    process2 = ProcessStateRef("PROCESS-PROCESS-REF-001", "v2", ProcessStage.REFERENCE_VERIFICATION)
    product = ProductRef("PRODUCT-REF-001", "1")
    environment = EnvironmentRef("ENV-REF-001", "1")
    collection = ObservationCollectionRef(
        "COLLECTION-REF-001", "1", product, environment,
        ObservationSourceKind.DETERMINISTIC_FIXTURE,
    )
    slot = ObservationSlotRef(collection, 0)
    observation = make_dynamic_observation(
        slot, RESPONSE_TIME_METRIC_REF, Decimal("1.8"), UnitLabel.SECOND,
        SUPPORTED_CONTEXT_IDENTITY, "OBSERVATION-REF-001",
    )
    checks = (
        ("product_ref", observation.product_ref),
        ("observation_source_kind", observation.source_kind),
        ("collection_ref", observation.collection_ref),
        ("metric_ref", observation.metric_ref),
        ("unit", observation.unit),
        ("context_identity", observation.context_identity),
        ("applicability", Applicability.APPLICABLE),
        ("process_stage", process2.stage),
        ("source_contract_permission", True),
    )
    versions = ComponentVersionSet((
        VersionedComponentRef("FULL_MODEL_CONTRACT", "FULL-MODEL-V0.1-CONTRACT", "1"),
        VersionedComponentRef("DYNAMIC_EVIDENCE", "FULL-MODEL-V0.1-DYNAMIC-EVIDENCE", "1"),
        VersionedComponentRef("PE_FEATURES", "FULL-MODEL-V0.1-PRODUCT-QUALITY-FEATURE", "1"),
        VersionedComponentRef("PRODUCT_QUALITY", "FULL-MODEL-V0.1-PRODUCT-QUALITY-ASSESSMENT", "1"),
        VersionedComponentRef("DEFECT_RISK", "FULL-MODEL-V0.1-DEFECT-QUALITY-RISK", "1"),
        VersionedComponentRef("PROCESS_REASSESSMENT", "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", "1"),
    ))
    return FullModelRequest(
        requirements, artifact1, assessment1, process1,
        CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0), "R001",
        product, environment, collection, ObservationSourceKind.DETERMINISTIC_FIXTURE,
        0, "OBSERVATION-REF-001", Decimal("1.8"), UnitLabel.SECOND,
        SUPPORTED_CONTEXT_IDENTITY,
        DynamicEvidenceAssessmentRef("DYNAMIC-ASSESSMENT-REF-001", "v1", artifact1, product, collection),
        ProductQualityAssessmentEventRef("PRODUCT-QUALITY-EVENT-REF-001", "v1", product, artifact1),
        RiskAssessmentEventRef("RISK-EVENT-REF-001", "v1", artifact1, process1),
        "A-REF-001", ActionCreatorSource("CORRECTIVE-ACTION-PROPOSER", "1"),
        ExternalRevisionInput(
            artifact2, RevisionRef("REV-REF-001", "v1"),
            ExternalRevisionProviderKind.CONTROLLED_REFERENCE_FIXTURE,
            ExternalProviderRef("QB-CONFLICT-REFERENCE", "1"),
            (ExternalRequirementReplacement("R002", "Час відгуку ≤ 5 с при 500 одночасних користувачах"),),
            "Controlled explicit TC-05 test revision",
            ApplicationIdentityContext("APP-REF-001", "v1", "v2", "ARTIFACT-TRANSITION-REF-001"),
        ),
        process2, assessment2,
        EvidenceReuseInput(
            EvidenceReuseDisposition.REUSE_ALLOWED,
            tuple(ExactIdentityCheck(name, value, value, True) for name, value in checks),
            (EvidenceReuseReason.EXACT_IDENTITY_AND_CONTEXT_MATCH,),
        ),
        DynamicEvidenceAssessmentRef("DYNAMIC-ASSESSMENT-REF-001", "v2", artifact2, product, collection),
        ProductQualityAssessmentEventRef("PRODUCT-QUALITY-EVENT-REF-001", "v2", product, artifact2),
        RiskAssessmentEventRef("RISK-EVENT-REF-001", "v2", artifact2, process2),
        ReassessmentIdentityContext("REEVAL-REF-001", "v1", process2), versions,
        ("COMPARE-QB-REF-001", "COMPARE-PROBLEM-REF-001", "COMPARE-RISK-REF-001", "COMPARE-PRODUCT-QUALITY-REF-001"),
        "v1", "PROCESS-TRANSITION-REF-001",
    )


def test_one_public_call_executes_canonical_core_path_deterministically():
    first = FullModelService().run(_request())
    second = FullModelService().run(_request())
    assert isinstance(first, FullModelResult)
    assert first == second
    qb1 = next(x for x in first.metric_profile.entries if x.metric_id is MetricId.SPEC_QB_CONSISTENCY)
    core2 = first.reassessment.produced_results[0]
    qb2 = next(x for x in core2.metric_profile.entries if x.metric_id is MetricId.SPEC_QB_CONSISTENCY)
    assert qb1.value == Fraction(0, 1)
    assert qb2.value == Fraction(1, 1)
    assert first.risk_assessments[0].classification is RiskClassification.RISK_IDENTIFIED
    assert first.action_application.child_specification is first.revised_specification
    assert first.reassessment.produced_results[1].target_problem_resolution.problem is None
    assert len(first.comparisons) == 4
    assert first.report_bundle.process_states == (first.process_v1, first.process_v2)
    assert first.full_quality_profiles == ()
    assert first.prediction is None
    assert first.quantitative_risk_assessments == ()
    assert first.checkpoint_evaluations == ()


def test_result_is_typed_data_not_rendered_text():
    result = FullModelService().run(_request())
    assert "report_bundle" in {item.name for item in fields(result)}
    assert not any(item.name in {"user_text", "audit_text", "rendered"} for item in fields(result))


def _config_dict():
    component_versions = [
        {"kind": kind, "id": identity, "version": "1"}
        for kind, identity in (
            ("FULL_MODEL_CONTRACT", "FULL-MODEL-V0.1-CONTRACT"),
            ("DYNAMIC_EVIDENCE", "FULL-MODEL-V0.1-DYNAMIC-EVIDENCE"),
            ("PE_FEATURES", "FULL-MODEL-V0.1-PRODUCT-QUALITY-FEATURE"),
            ("PRODUCT_QUALITY", "FULL-MODEL-V0.1-PRODUCT-QUALITY-ASSESSMENT"),
            ("DEFECT_RISK", "FULL-MODEL-V0.1-DEFECT-QUALITY-RISK"),
            ("PROCESS_REASSESSMENT", "FULL-MODEL-V0.1-PROCESS-REASSESSMENT"),
        )
    ]
    return {
        "artifact_v1": {"id": "SPEC-PROCESS-REF-001", "version": "v1"},
        "artifact_v2": {"id": "SPEC-PROCESS-REF-001", "version": "v2"},
        "assessment_v1": {"id": "ASSESS-PROCESS-REF-001", "version": "v1"},
        "assessment_v2": {"id": "ASSESS-PROCESS-REF-001", "version": "v2"},
        "process": {"id": "PROCESS-PROCESS-REF-001", "v1_version": "v1", "v2_version": "v2", "stage": ProcessStage.REFERENCE_VERIFICATION.value, "transition_id": "PROCESS-TRANSITION-REF-001"},
        "selected_criterion": {"requirement_id": "R001", "feature_id": FeatureId.QUANTITATIVE_CONSTRAINT.value, "occurrence": 0},
        "product": {"id": "PRODUCT-REF-001", "version": "1"},
        "environment": {"id": "ENV-REF-001", "version": "1"},
        "collection": {"id": "COLLECTION-REF-001", "version": "1", "source_kind": ObservationSourceKind.DETERMINISTIC_FIXTURE.value},
        "observation": {"id": "OBSERVATION-REF-001", "slot_index": 0, "value": "1.8", "unit": UnitLabel.SECOND.value, "context": {"normalization_contract": {"id": SUPPORTED_CONTEXT_IDENTITY.normalization_contract_ref.contract_id, "version": SUPPORTED_CONTEXT_IDENTITY.normalization_contract_ref.version}, "normalized_text": SUPPORTED_CONTEXT_IDENTITY.normalized_text}},
        "events": {"dynamic_id": "DYNAMIC-ASSESSMENT-REF-001", "product_quality_id": "PRODUCT-QUALITY-EVENT-REF-001", "risk_id": "RISK-EVENT-REF-001", "v1_version": "v1", "v2_version": "v2"},
        "action": {"id": "A-REF-001", "creator": {"id": "CORRECTIVE-ACTION-PROPOSER", "version": "1"}},
        "revision": {"identity": {"id": "REV-REF-001", "version": "v1"}, "provider_kind": ExternalRevisionProviderKind.CONTROLLED_REFERENCE_FIXTURE.value, "provider": {"id": "QB-CONFLICT-REFERENCE", "version": "1"}, "replacements": [{"requirement_id": "R002", "text": "Час відгуку ≤ 5 с при 500 одночасних користувачах"}], "reason": "Controlled explicit TC-05 CLI revision", "application": {"id": "APP-REF-001", "version": "v1", "child_version": "v2", "transition_id": "ARTIFACT-TRANSITION-REF-001"}},
        "evidence_reuse": {"disposition": EvidenceReuseDisposition.REUSE_ALLOWED.value, "reasons": [EvidenceReuseReason.EXACT_IDENTITY_AND_CONTEXT_MATCH.value], "source_contract_permission": True},
        "reassessment": {"id": "REEVAL-REF-001", "version": "v1"},
        "component_versions": component_versions,
        "comparisons": {"ids": ["COMPARE-QB-REF-001", "COMPARE-PROBLEM-REF-001", "COMPARE-RISK-REF-001", "COMPARE-PRODUCT-QUALITY-REF-001"], "version": "v1"},
    }


def test_full_model_cli_user_and_audit_use_explicit_config(tmp_path, capsys):
    requirements = tmp_path / "requirements.txt"
    requirements.write_text("Час відгуку ≤ 2 с при 500 одночасних користувачах\nЧас відгуку не нижче 5 с при 500 одночасних користувачах\n", encoding="utf-8")
    config = tmp_path / "full-model.json"
    config.write_text(json.dumps(_config_dict(), ensure_ascii=False), encoding="utf-8")
    for view in ("user", "audit"):
        assert main(["--mode", "full-model", "--config", str(config), "--view", view, str(requirements)]) == 0
        captured = capsys.readouterr()
        assert captured.err == ""
        assert "Full Model v0.1" in captured.out if view == "audit" else "Повна модель v0.1" in captured.out


def test_full_model_cli_missing_or_invalid_config_fails_cleanly(tmp_path, capsys):
    requirements = tmp_path / "requirements.txt"
    requirements.write_text("вимога\n", encoding="utf-8")
    assert main(["--mode", "full-model", str(requirements)]) != 0
    missing = capsys.readouterr()
    assert "--config is required" in missing.err
    assert "Traceback" not in missing.err
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{}", encoding="utf-8")
    assert main(["--mode", "full-model", "--config", str(invalid), str(requirements)]) != 0
    captured = capsys.readouterr()
    assert "invalid full-model config" in captured.err
    assert "Traceback" not in captured.err


def test_explicit_tc01_tc02_tc03_tc04_extensions_are_invoked_and_reported():
    base_request = _request()
    requirement_ref = RequirementSubjectRef(base_request.artifact_v1, "R001", 1)
    external = tuple(
        ExternalPropertyAssessment(
            property_id, ExternalAssessmentState.AVAILABLE,
            ExternalPropertyJudgment(f"EXPLICIT-{property_id.value}"),
            ExternalAssessmentProvenance(
                ExternalAssessmentSourceRef("TC05-EXPERT", "1"), requirement_ref,
                base_request.artifact_v1, ContractRef("TC05-EXTERNAL", "1"),
                RuleRef(f"TC05-{property_id.value}", "1", RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION),
            ),
            "Explicit external TC-05 test judgment.",
        ) for property_id in EXTERNAL_PROPERTY_IDS
    )
    prediction = PredictionExtensionInput(
        event_ref=PredictionEventRef("TC05-PREDICTION", "1"),
        context=PerformanceEfficiencyPredictionContext(
            base_request.product_ref, base_request.artifact_v1,
            base_request.process_ref_v1, base_request.environment_ref,
            base_request.collection_ref, base_request.criterion_context,
        ),
        parameter_set=_parameters(), predictor=ControlledReferencePredictor(),
    )
    values = (Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(2, 3))
    operands = []
    for kind, value in zip(QuantitativeRiskOperandKind, values, strict=True):
        operands.append(QuantitativeRiskOperandInput(
            kind, f"TC05-{kind.value}", "1",
            FullModelStatus.AVAILABLE,
            value,
            QuantitativeRiskOperandSourceRef(f"TC05-{kind.value}", "1", "TC05-PROVIDER", "1"),
            "Explicit TC-05 operand; no calibration claim.",
            CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
            QuantitativeRiskContextRef("TC05-CONTEXT", "1") if kind is QuantitativeRiskOperandKind.CONTEXT_FACTOR else None,
        ))
    quantitative = QuantitativeRiskExtensionInput("TC05-Q-RISK", "1", tuple(operands))
    policy = ThresholdPolicy(
        "TC05-QB-POLICY", "1", PolicySourceRef("TC05-SOURCE", "1"),
        PolicyProviderRef("TC05-PROVIDER", "1"), "Explicit test threshold.",
        CheckpointComparator.GREATER_THAN_OR_EQUAL, Fraction(1, 1),
        ContractRef("TC05-POLICY", "1"),
    )
    result = FullModelService().run(replace(
        base_request,
        full_quality=(FullQualityExtensionInput("R001", external),),
        prediction=prediction,
        quantitative_risk=quantitative,
        checkpoints=(CheckpointExtensionInput("TC05-CHECKPOINT", "1", "v2", policy),),
    ))
    assert len(result.full_quality_profiles) == 1
    assert result.prediction is not None
    assert result.quantitative_risk_assessments[0].local_risk == Fraction(1, 16)
    assert result.checkpoint_evaluations[0].outcome is CheckpointOutcome.SATISFIED
    assert "SINGULARITY" in AuditFullModelReporter().render(result.report_bundle)
    assert "Прогнозована якість" in UserFullModelReporter().render(result.report_bundle)

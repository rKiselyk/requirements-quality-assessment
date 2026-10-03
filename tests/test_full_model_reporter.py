from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from requirements_quality_assessment.full_model_reporter import (
    AuditFullModelReporter,
    FullModelReportBundle,
    UserFullModelReporter,
)
from requirements_quality_assessment.process import (
    assemble_process_state,
    assemble_process_transition,
)
from requirements_quality_assessment.reassessment import (
    ComparisonRequest,
    ComparisonResultFamily,
    ComparisonValueKind,
    compare,
)
from requirements_quality_assessment.dynamic_evidence import (
    Applicability,
    DynamicEvidenceReason,
    FullModelStatus,
)
from requirements_quality_assessment.product_quality import CalibrationStatus
from requirements_quality_assessment.reporter import ConsoleReporter, UserConsoleReporter

from test_corrective_action import _positive
from test_performance_efficiency_features import _build, _bundle
from test_process_state import _v1_assembly, _v2_assembly, _v2_reassessment
from test_reassessment_comparison import _comparable, _subject
from test_versioned_reassessment import _application_bundle


def _comparison_bundle():
    _, parent, revision, application = _application_bundle()
    artifact_before = parent.artifact_ref
    artifact_after = application.child_artifact_ref

    qb_subject = _subject(
        parent,
        family=ComparisonResultFamily.QB_CONSISTENCY,
    )
    qb = compare(
        ComparisonRequest(
            "COMPARE-QB",
            "1",
            _comparable(artifact_before, qb_subject, value=Fraction(0, 1)),
            _comparable(artifact_after, qb_subject, value=Fraction(1, 1)),
            application.transition,
        )
    )

    def categorical(identifier, family, before, after, *, after_status=None):
        subject = _subject(
            parent,
            family=family,
            metric_or_characteristic_id=identifier,
            stable_subject_identity=(artifact_before.artifact_id, identifier),
        )
        status = after_status or FullModelStatus.AVAILABLE
        applicability = (
            Applicability.NOT_APPLICABLE
            if status is FullModelStatus.NOT_APPLICABLE
            else Applicability.APPLICABLE
        )
        return compare(
            ComparisonRequest(
                f"COMPARE-{identifier}",
                "1",
                _comparable(
                    artifact_before,
                    subject,
                    value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                    categorical_state=before,
                    calibration=(
                        CalibrationStatus.PROVISIONAL_NOT_CALIBRATED
                        if family is ComparisonResultFamily.BOUNDED_RISK
                        else None
                    ),
                ),
                _comparable(
                    artifact_after,
                    subject,
                    status=status,
                    applicability=applicability,
                    value_kind=ComparisonValueKind.CATEGORICAL_STATE,
                    categorical_state=after,
                    calibration=(
                        CalibrationStatus.PROVISIONAL_NOT_CALIBRATED
                        if family is ComparisonResultFamily.BOUNDED_RISK
                        else None
                    ),
                ),
                application.transition,
            )
        )

    problem = categorical(
        "CONFIRMED_PROBLEM",
        ComparisonResultFamily.CONFIRMED_PROBLEM,
        "PRESENT",
        None,
        after_status=FullModelStatus.NOT_APPLICABLE,
    )
    risk = categorical(
        "BOUNDED_RISK",
        ComparisonResultFamily.BOUNDED_RISK,
        "RISK_IDENTIFIED",
        None,
        after_status=FullModelStatus.NOT_APPLICABLE,
    )
    product = categorical(
        "BOUNDED_PRODUCT_QUALITY_STATE",
        ComparisonResultFamily.PRODUCT_QUALITY,
        "UNRESOLVED",
        "AVAILABLE",
    )
    return revision, application, (qb, problem, risk, product)


def _report_bundle():
    risk_bundle, risk, action_resolution = _positive()
    source, quality, problem, population, relation, _ = risk_bundle
    dynamic = _bundle()
    feature = _build(dynamic)
    assert quality.feature_profile_ref == feature.profile_id

    _, application, run, _ = _v2_reassessment()
    revision, _, comparisons = _comparison_bundle()
    v1_ref, v1_assembly = _v1_assembly()
    v1_state = assemble_process_state(v1_ref, v1_assembly)
    _, application_for_state, _, v2_ref, v2_assembly = _v2_assembly()
    v2_state = assemble_process_state(v2_ref, v2_assembly)
    transition = assemble_process_transition(
        "PROCESS-TRANSITION-REPORT",
        v1_state,
        v2_state,
    )
    assert application.ref == application_for_state.ref

    return FullModelReportBundle(
        assessment_result=source,
        metric_profile=dynamic[1],
        criterion_binding=dynamic[2],
        observation_resolution=dynamic[3],
        conformance=dynamic[4],
        feature_profile=feature,
        product_quality_assessment=quality,
        problem_resolutions=(problem,),
        defect_population=population,
        defect_quality_relations=(relation,),
        risk_assessments=(risk,),
        corrective_action_resolutions=(action_resolution,),
        specification_versions=(application.child_specification,),
        external_revisions=(revision,),
        action_applications=(application,),
        reassessment_runs=(run,),
        comparisons=comparisons,
        process_states=(v1_state, v2_state),
        process_transitions=(transition,),
    )


def test_user_full_model_path_is_bounded_and_keeps_layers_distinct():
    output = UserFullModelReporter().render(_report_bundle())

    for expected in (
        "Якість вимог і специфікації",
        "C/V/U вище є профілем якості вимог",
        "Спостережуваний показник якості продукту",
        "X_PE:",
        "Обмежена оцінка Performance Efficiency",
        "Підтверджена підтримувана проблема",
        "R_DQ:",
        "RISK_IDENTIFIED",
        "RECONCILE_QUANTITATIVE_BOUNDS",
        "Зовнішня ревізія",
        "ReEval:",
        "S(v2) — якість вимог",
        "Перехід стану процесу",
    ):
        assert expected in output
    assert "не повне оцінювання Performance Efficiency" in output
    assert "не означає відсутність дефектів" in output


def test_user_comparisons_preserve_literal_change_semantics_without_claims():
    output = UserFullModelReporter().render(_report_bundle())

    assert "0/1 (status=AVAILABLE; applicability=APPLICABLE) → 1/1" in output
    assert output.count("comparison=STATE_CHANGED") == 3
    assert "comparison=INCREASED" in output
    lowered = output.lower()
    for forbidden in (
        "improved",
        "worsened",
        "unsafe",
        "risk reduced",
        "action successful",
        "causal effect",
    ):
        assert forbidden not in lowered


def test_audit_full_model_path_preserves_exact_values_and_provenance():
    output = AuditFullModelReporter().render(_report_bundle())

    for expected in (
        "artifact_id: SPEC-PE-001",
        "artifact_version: 1",
        "observed_value: Decimal('1.80')",
        "value: Fraction(1,1)",
        "comparison_kind: INCREASED",
        "exact_value: Fraction(0,1)",
        "exact_value: Fraction(1,1)",
        "rule_ref: RuleRef",
        "model_ref: ModelRef",
        "parameter_set_ref: ParameterSetRef",
        "evidence_refs:",
        "process_state_ref: ProcessStateRef",
        "parent_artifact_ref: ArtifactRef",
        "child_artifact_ref: ArtifactRef",
        "comparison_refs:",
        "component_associations:",
        "evidence_associations:",
        "non_claims:",
    ):
        assert expected in output
    assert ".8" in output
    assert "0.333" not in output


def test_full_model_output_is_deterministic_and_existing_entry_points_compose_it():
    bundle = _report_bundle()
    user = UserFullModelReporter().render(bundle)
    audit = AuditFullModelReporter().render(bundle)

    assert UserFullModelReporter().render(bundle) == user
    assert AuditFullModelReporter().render(bundle) == audit
    assert UserConsoleReporter().render_full_model(bundle) == user
    assert ConsoleReporter().render_full_model(bundle) == audit


@pytest.mark.parametrize(
    ("status", "applicability", "reason"),
    (
        (
            FullModelStatus.UNAVAILABLE,
            Applicability.APPLICABLE,
            DynamicEvidenceReason.SOURCE_ASSESSMENT_UNAVAILABLE,
        ),
        (
            FullModelStatus.UNKNOWN,
            Applicability.UNKNOWN,
            DynamicEvidenceReason.SOURCE_ASSESSMENT_UNAVAILABLE,
        ),
        (
            FullModelStatus.UNRESOLVED,
            Applicability.UNKNOWN,
            DynamicEvidenceReason.SOURCE_OBSERVATION_SELECTION_UNRESOLVED,
        ),
        (
            FullModelStatus.UNSUPPORTED,
            Applicability.APPLICABLE,
            DynamicEvidenceReason.COMPARATOR_UNSUPPORTED,
        ),
        (
            FullModelStatus.NOT_APPLICABLE,
            Applicability.NOT_APPLICABLE,
            DynamicEvidenceReason.NO_APPLICABLE_RESPONSE_TIME_CRITERION,
        ),
    ),
)
def test_all_nonvalue_statuses_are_rendered_literally(status, applicability, reason):
    dynamic = _bundle()
    binding = replace(
        dynamic[2],
        status=status,
        applicability=applicability,
        criterion=(
            dynamic[2].criterion
            if status is FullModelStatus.UNSUPPORTED
            else None
        ),
        reasons=(reason,),
    )
    bundle = FullModelReportBundle(
        assessment_result=dynamic[0],
        criterion_binding=binding,
    )

    user = UserFullModelReporter().render_projection(bundle)
    audit = AuditFullModelReporter().render_projection(bundle)

    assert f"status={status.value}" in user
    assert f"applicability={applicability.value}" in user
    assert f"status: {status.value}" in audit
    assert f"applicability: {applicability.value}" in audit
    assert "value: 0" not in audit


def test_existing_reporters_remain_free_of_full_model_scientific_components():
    source = (
        Path(__file__).parents[1]
        / "src"
        / "requirements_quality_assessment"
        / "full_model_reporter.py"
    ).read_text(encoding="utf-8")

    for forbidden in (
        "PerformanceEfficiencyFeatureProfileBuilder",
        "PerformanceEfficiencyQualityAssessor",
        "DefectBuilder",
        "DefectQualityMapper",
        "RiskAssessor",
        "propose_corrective_action",
        "apply_external_revision(",
        "reevaluate(",
        "compare(",
        "assemble_process_state(",
        "assemble_process_transition(",
        "float(",
    ):
        assert forbidden not in source

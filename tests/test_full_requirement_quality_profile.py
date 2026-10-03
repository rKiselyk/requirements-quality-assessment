from dataclasses import FrozenInstanceError, fields, replace
from fractions import Fraction
from unittest.mock import patch

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState,
    DetectionProcessingStatus,
    FeatureDetectionOutcome,
    FeatureId,
    Requirement,
    RequirementExtractionResult,
    RequirementFeatures,
)
from requirements_quality_assessment.full_quality import (
    EXTERNAL_PROPERTY_IDS,
    AuditFullRequirementQualityReporter,
    ExternalAssessmentProvenance,
    ExternalAssessmentSourceRef,
    ExternalAssessmentState,
    ExternalPropertyAssessment,
    ExternalPropertyJudgment,
    FullRequirementQualityProfile,
    FullRequirementQualityProfileComposer,
    PropertyAssessmentOrigin,
    RequirementQualityPropertyId,
    UserFullRequirementQualityReporter,
)
from requirements_quality_assessment.metrics import (
    ArtifactRef,
    AssessmentRef,
    ContractRef,
    RequirementSubjectRef,
    RuleRef,
    RuleVersionAuthority,
)
from requirements_quality_assessment.reporter import ConsoleReporter, UserConsoleReporter


def _record():
    requirement = Requirement("R001", 3, "Система повинна зберегти запис.")

    def empty(feature_id: FeatureId) -> FeatureDetectionOutcome:
        return FeatureDetectionOutcome(
            feature_id, (), DetectionProcessingStatus.COMPLETE, ()
        )

    result = RequirementExtractionResult(
        requirement,
        RequirementFeatures(
            condition_contexts=empty(FeatureId.CONDITION_CONTEXT),
            expected_results=empty(FeatureId.EXPECTED_RESULT),
            acceptance_criteria=empty(FeatureId.ACCEPTANCE_CRITERION),
            quantitative_constraints=empty(FeatureId.QUANTITATIVE_CONSTRAINT),
            verification_methods=empty(FeatureId.VERIFICATION_METHOD),
            vague_term_occurrences=empty(FeatureId.VAGUE_TERM_OCCURRENCE),
        ),
        (),
    )
    return RequirementQualityAssessor().assess_record(result)


def _context():
    artifact = ArtifactRef("SPEC-TC01", "7")
    assessment = AssessmentRef("ASSESS-TC01", "2", artifact)
    requirement = RequirementSubjectRef(artifact, "R001", 3)
    return artifact, assessment, requirement


def _external(
    property_id: RequirementQualityPropertyId,
    state: ExternalAssessmentState,
    *,
    artifact: ArtifactRef | None = None,
    requirement: RequirementSubjectRef | None = None,
) -> ExternalPropertyAssessment:
    default_artifact, _, default_requirement = _context()
    artifact = artifact or default_artifact
    requirement = requirement or default_requirement
    judgment = (
        ExternalPropertyJudgment(f"EXPERT-{property_id.value}-PASS")
        if state is ExternalAssessmentState.AVAILABLE
        else None
    )
    return ExternalPropertyAssessment(
        property_id=property_id,
        state=state,
        judgment=judgment,
        provenance=ExternalAssessmentProvenance(
            source_ref=ExternalAssessmentSourceRef("EXPERT-PANEL-A", "2026-10-03"),
            requirement_ref=requirement,
            artifact_ref=artifact,
            assessment_contract_ref=ContractRef("TC01-EXPERT-ASSESSMENT", "1"),
            assessment_rule_ref=RuleRef(
                f"RULE-{property_id.value}",
                "1",
                RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
            ),
        ),
        explanation=f"External judgment for {property_id.value}.",
    )


def _external_set() -> tuple[ExternalPropertyAssessment, ...]:
    states = (
        ExternalAssessmentState.AVAILABLE,
        ExternalAssessmentState.UNKNOWN,
        ExternalAssessmentState.UNAVAILABLE,
        ExternalAssessmentState.NOT_APPLICABLE,
        ExternalAssessmentState.UNRESOLVED,
        ExternalAssessmentState.AVAILABLE,
    )
    return tuple(
        _external(property_id, state)
        for property_id, state in zip(EXTERNAL_PROPERTY_IDS, states, strict=True)
    )


def _profile() -> FullRequirementQualityProfile:
    artifact, assessment, _ = _context()
    return FullRequirementQualityProfileComposer().compose(
        _record(),
        artifact_ref=artifact,
        assessment_ref=assessment,
        external_assessments=_external_set(),
    )


def test_complete_profile_has_exactly_nine_typed_properties_and_origins() -> None:
    profile = _profile()

    assert tuple(item.property_id for item in profile.properties) == tuple(
        RequirementQualityPropertyId
    )
    assert len(profile.properties) == 9
    assert tuple(item.origin for item in profile.properties[:3]) == (
        PropertyAssessmentOrigin.AUTOMATIC,
    ) * 3
    assert tuple(item.origin for item in profile.properties[3:]) == (
        PropertyAssessmentOrigin.EXTERNAL_EXPERT,
    ) * 6


def test_profile_reuses_exact_cvu_assessments_findings_and_traces_without_rerun() -> None:
    record = _record()
    artifact, assessment, _ = _context()
    with patch.object(
        RequirementQualityAssessor,
        "assess",
        side_effect=AssertionError("C/V/U calculator path was rerun"),
    ):
        profile = FullRequirementQualityProfileComposer().compose(
            record,
            artifact_ref=artifact,
            assessment_ref=assessment,
            external_assessments=_external_set(),
        )

    assert profile.automatic_record is record
    assert profile.completeness is record.quality_profile.completeness
    assert profile.verifiability is record.quality_profile.verifiability
    assert profile.unambiguity is record.quality_profile.unambiguity
    assert profile.completeness.value == Fraction(0, 1)
    assert profile.verifiability.value == Fraction(0, 1)
    assert profile.unambiguity.value == Fraction(1, 1)
    assert all(
        isinstance(assessment.value, Fraction)
        for assessment in (
            profile.completeness,
            profile.verifiability,
            profile.unambiguity,
        )
    )
    assert profile.unambiguity.findings is record.quality_profile.unambiguity.findings
    assert tuple(item.automatic_trace for item in profile.properties[:3]) == (
        record.trace.characteristics
    )


def test_profile_is_immutable_and_has_no_scalar_overall_score_field() -> None:
    profile = _profile()
    with pytest.raises(FrozenInstanceError):
        profile.relevance = profile.relevance

    field_names = {field.name for field in fields(FullRequirementQualityProfile)}
    assert field_names.isdisjoint({"score", "value", "mean", "quality_score"})
    for forbidden in ("score", "value", "mean", "quality_score"):
        assert not hasattr(profile, forbidden)


def test_external_states_preserve_judgment_or_typed_absence_literally() -> None:
    assessments = _profile().properties[3:]

    assert {item.property_id for item in assessments} == set(EXTERNAL_PROPERTY_IDS)
    for item in assessments:
        external = item.external_assessment
        assert external is not None
        if external.state is ExternalAssessmentState.AVAILABLE:
            assert isinstance(external.judgment, ExternalPropertyJudgment)
        else:
            assert external.judgment is None
            assert external.state in {
                ExternalAssessmentState.UNKNOWN,
                ExternalAssessmentState.UNAVAILABLE,
                ExternalAssessmentState.NOT_APPLICABLE,
                ExternalAssessmentState.UNRESOLVED,
            }


def test_external_value_state_contract_rejects_invalid_combinations() -> None:
    provenance = _external_set()[0].provenance
    with pytest.raises(ValueError, match="AVAILABLE requires"):
        ExternalPropertyAssessment(
            RequirementQualityPropertyId.SINGULARITY,
            ExternalAssessmentState.AVAILABLE,
            None,
            provenance,
            "Missing supplied judgment.",
        )
    with pytest.raises(ValueError, match="UNKNOWN requires judgment=None"):
        ExternalPropertyAssessment(
            RequirementQualityPropertyId.SINGULARITY,
            ExternalAssessmentState.UNKNOWN,
            ExternalPropertyJudgment("FORBIDDEN"),
            provenance,
            "A non-value state cannot carry a judgment.",
        )
    with pytest.raises(ValueError, match="externally assessed property"):
        ExternalPropertyAssessment(
            RequirementQualityPropertyId.COMPLETENESS,
            ExternalAssessmentState.AVAILABLE,
            ExternalPropertyJudgment("FORBIDDEN"),
            provenance,
            "C/V/U cannot enter the external boundary.",
        )


def test_composer_rejects_missing_or_duplicated_external_properties() -> None:
    record = _record()
    artifact, assessment, _ = _context()
    values = _external_set()

    with pytest.raises(ValueError, match="exactly the six"):
        FullRequirementQualityProfileComposer().compose(
            record,
            artifact_ref=artifact,
            assessment_ref=assessment,
            external_assessments=values[:-1],
        )
    with pytest.raises(ValueError, match="duplicate"):
        FullRequirementQualityProfileComposer().compose(
            record,
            artifact_ref=artifact,
            assessment_ref=assessment,
            external_assessments=values[:-1] + (values[0],),
        )


def test_profile_rejects_wrong_slot_and_mismatched_provenance_identities() -> None:
    profile = _profile()
    with pytest.raises(ValueError, match="wrong property identity"):
        replace(profile, singularity=profile.correctness)

    foreign_artifact = ArtifactRef("SPEC-FOREIGN", "1")
    foreign_requirement = RequirementSubjectRef(foreign_artifact, "R999", 9)
    mismatched_artifact = _external(
        RequirementQualityPropertyId.RELEVANCE,
        ExternalAssessmentState.UNKNOWN,
        artifact=foreign_artifact,
        requirement=foreign_requirement,
    )
    with pytest.raises(ValueError, match="artifact identity"):
        replace(profile, relevance=mismatched_artifact)

    artifact, _, requirement = _context()
    mismatched_requirement = _external(
        RequirementQualityPropertyId.RELEVANCE,
        ExternalAssessmentState.UNKNOWN,
        artifact=artifact,
        requirement=RequirementSubjectRef(artifact, "R999", 9),
    )
    with pytest.raises(ValueError, match="requirement identity"):
        replace(profile, relevance=mismatched_requirement)

    with pytest.raises(ValueError, match="requirement and artifact refs must agree"):
        ExternalAssessmentProvenance(
            ExternalAssessmentSourceRef("SOURCE", "1"),
            requirement,
            ArtifactRef(artifact.artifact_id, "different-version"),
            ContractRef("CONTRACT", "1"),
            RuleRef("RULE", "1", RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION),
        )


def test_user_and_audit_reports_show_all_properties_origins_states_and_provenance() -> None:
    profile = _profile()
    user = UserFullRequirementQualityReporter().render(profile)
    audit = AuditFullRequirementQualityReporter().render(profile)

    assert user.count("[AUTOMATIC]") == 3
    assert user.count("[EXTERNAL_EXPERT]") == 6
    for property_id in RequirementQualityPropertyId:
        assert property_id.value in audit
    for state in ("UNKNOWN", "UNAVAILABLE", "NOT_APPLICABLE", "UNRESOLVED"):
        assert state in user
        assert f"state: {state}" in audit
    for expected in (
        "source_id: EXPERT-PANEL-A",
        "source_version: 2026-10-03",
        "provenance_requirement_id: R001",
        "provenance_artifact_id: SPEC-TC01",
        "provenance_artifact_version: 7",
        "assessment_contract_id: TC01-EXPERT-ASSESSMENT",
        "assessment_contract_version: 1",
        "assessment_rule_version: 1",
    ):
        assert expected in audit
    assert "No integrated scalar requirement-quality score is calculated." in user
    assert "no integrated scalar requirement-quality score is defined" in audit


def test_existing_reporter_boundaries_expose_additive_full_profile_projection() -> None:
    profile = _profile()

    assert ConsoleReporter().render_full_requirement_quality(profile) == (
        AuditFullRequirementQualityReporter().render(profile)
    )
    assert UserConsoleReporter().render_full_requirement_quality(profile) == (
        UserFullRequirementQualityReporter().render(profile)
    )


def test_existing_cvu_states_remain_their_original_contract() -> None:
    profile = _profile()

    assert profile.completeness.state is CharacteristicAssessmentState.COMPUTED
    assert profile.verifiability.state is CharacteristicAssessmentState.COMPUTED
    assert profile.unambiguity.state is CharacteristicAssessmentState.COMPUTED

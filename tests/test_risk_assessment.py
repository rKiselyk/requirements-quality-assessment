from dataclasses import fields, replace
from decimal import Decimal
from fractions import Fraction
from inspect import signature

import pytest

from requirements_quality_assessment.defect_quality import (
    RELATION_RULE_REF,
    DefectConstructionContext,
    DefectQualityRelation,
    DefectQualityRelationContext,
    ProblemClaimSourceKind,
    RelationKind,
    TypedProblemClaimSource,
    TypedSourceRef,
    build_defect_population,
    relate_problem_to_quality,
    resolve_problem_claim,
)
from requirements_quality_assessment.dynamic_evidence import (
    Applicability,
    FullModelStatus,
)
from requirements_quality_assessment.metrics import ArtifactRef, AssessmentRef
from requirements_quality_assessment.performance_efficiency import (
    ProcessStateRef,
    ProductQualityCharacteristicId,
)
from requirements_quality_assessment.product_quality import CalibrationStatus
from requirements_quality_assessment.risk import (
    MANDATORY_RISK_NON_CLAIMS,
    RISK_MODEL_REF,
    RISK_PARAMETER_SET,
    RISK_PARAMETER_SET_REF,
    RISK_RULE_REF,
    BoundedRiskAssessment,
    BoundedRiskAssessmentInput,
    ProductQualityAssessmentRef,
    RiskAssessmentContext,
    RiskAssessmentEventRef,
    RiskClassification,
    RiskNonClaim,
    RiskAssessor,
    assess_risk,
    build_risk_assessment_input,
)

from test_defect_quality_mapping import (
    LOWER_FIVE,
    UPPER_FIVE,
    UPPER_TWO,
    _assessment,
    _outside_result,
)
from test_product_quality_assessment import _assess
from test_performance_efficiency_features import _build, _bundle


def _product_quality(observed=Decimal("1.8")):
    return _assess(_build(_bundle(observed_value=observed)))


def _contexts(source, product_quality, *, event_version="1"):
    artifact = product_quality.artifact_ref
    assessment = product_quality.feature_profile_ref.source_assessment_ref
    process = product_quality.provenance.process_state_ref
    construction = DefectConstructionContext(
        artifact,
        assessment,
        source.snapshot_id,
        process,
    )
    relation = DefectQualityRelationContext(
        artifact,
        assessment,
        source.snapshot_id,
        process,
    )
    event = RiskAssessmentEventRef(
        "RISK-EVENT-001",
        event_version,
        artifact,
        process,
    )
    risk = RiskAssessmentContext(
        event,
        artifact,
        assessment,
        source.snapshot_id,
        process,
    )
    return construction, relation, risk


def _risk_bundle(
    *texts,
    observed=Decimal("1.8"),
    population_source=None,
):
    texts = texts or (UPPER_TWO, LOWER_FIVE)
    source = _assessment(*texts)
    product_quality = _product_quality(observed)
    construction, relation_context, risk_context = _contexts(
        source, product_quality
    )
    resolutions = tuple(
        resolve_problem_claim(
            TypedProblemClaimSource.from_qb_result(
                item, source.projection.snapshot
            ),
            construction,
        )
        for item in source.cross_results
    )
    population = build_defect_population(
        resolutions,
        population_source or source.specification_assessment.qb_consistency,
        construction,
    )
    resolution = resolutions[0]
    relation = relate_problem_to_quality(resolution, relation_context)
    return (
        source,
        product_quality,
        resolution,
        population,
        relation,
        risk_context,
    )


def _assessed(bundle):
    _, quality, resolution, population, relation, context = bundle
    return assess_risk(resolution, population, relation, quality, context)


def test_confirmed_problem_and_valid_relation_produce_exact_risk_result() -> None:
    result = _assessed(_risk_bundle())

    assert result.status is FullModelStatus.AVAILABLE
    assert result.applicability is Applicability.APPLICABLE
    assert result.classification is RiskClassification.RISK_IDENTIFIED
    assert result.characteristic_id is ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY
    assert result.model_ref == RISK_MODEL_REF
    assert result.rule_ref == RISK_RULE_REF
    assert result.parameter_set_ref == RISK_PARAMETER_SET_REF
    assert result.calibration_status is CalibrationStatus.PROVISIONAL_NOT_CALIBRATED


def test_model_rule_and_empty_parameter_set_have_exact_identities() -> None:
    assert (RISK_MODEL_REF.model_id, RISK_MODEL_REF.model_version) == (
        "FULL-MODEL-V0.1-M-RISK-PE-QB",
        "1",
    )
    assert (RISK_RULE_REF.rule_id, RISK_RULE_REF.explicit_version) == (
        "RISK-PE-QB-001",
        "1",
    )
    assert (
        RISK_PARAMETER_SET_REF.parameter_set_id,
        RISK_PARAMETER_SET_REF.parameter_set_version,
    ) == ("RISK-PE-QB-001-PARAMETERS", "1")
    assert RISK_PARAMETER_SET.entries == ()
    assert (
        RISK_PARAMETER_SET.calibration_status
        is CalibrationStatus.PROVISIONAL_NOT_CALIBRATED
    )


def test_risk_identity_and_full_result_are_deterministic() -> None:
    bundle = _risk_bundle()

    first = _assessed(bundle)
    second = _assessed(bundle)

    assert first == second
    assert first.risk_assessment_id == second.risk_assessment_id
    assert first.ref == second.ref


def test_risk_identity_changes_with_versioned_event() -> None:
    bundle = list(_risk_bundle())
    first = _assessed(tuple(bundle))
    context = bundle[-1]
    event = replace(context.assessment_event_ref, event_version="2")
    bundle[-1] = replace(context, assessment_event_ref=event)

    second = _assessed(tuple(bundle))

    assert first.risk_assessment_id != second.risk_assessment_id


def test_provenance_reaches_problem_relation_qb_and_population() -> None:
    source, _, resolution, population, relation, _ = bundle = _risk_bundle()
    result = _assessed(bundle)

    assert result.problem_ref == resolution.problem.ref
    assert result.relation_ref == relation.ref
    assert result.defect_population_ref == population.ref
    assert result.provenance.problem_ref_or_none == resolution.problem.ref
    assert result.provenance.relation_ref == relation.ref
    assert result.provenance.source_cross_result_ref_or_none == (
        resolution.problem.source_cross_result_ref
    )
    assert result.provenance.source_cross_result_ref_or_none == (
        source.cross_results[0].result_id
    )
    assert result.evidence_refs == resolution.problem.evidence_refs


def test_incomplete_population_preserves_individual_risk_without_completeness_claim() -> None:
    bundle = _risk_bundle(
        UPPER_TWO,
        LOWER_FIVE,
        "Система працює не більше 3 с",
    )
    result = _assessed(bundle)

    assert bundle[3].population_complete is False
    assert bundle[3].status is FullModelStatus.UNRESOLVED
    assert result.classification is RiskClassification.RISK_IDENTIFIED
    assert result.defect_population_status is FullModelStatus.UNRESOLVED
    assert result.provenance.defect_population_status is FullModelStatus.UNRESOLVED
    assert "incomplete" in result.explanation
    assert "does not claim that all defects or risks were found" in result.explanation


@pytest.mark.parametrize(
    ("texts", "expected_status"),
    [
        ((UPPER_TWO, UPPER_FIVE), FullModelStatus.NOT_APPLICABLE),
        (
            ("Система працює не більше 2 с", "Система працює не нижче 5 с"),
            FullModelStatus.UNRESOLVED,
        ),
    ],
)
def test_no_problem_and_unresolved_problem_do_not_identify_risk(
    texts, expected_status
) -> None:
    result = _assessed(_risk_bundle(*texts))

    assert result.status is expected_status
    assert result.classification is None


def test_not_applicable_problem_path_does_not_identify_risk() -> None:
    source = _assessment(UPPER_TWO, LOWER_FIVE)
    quality = _product_quality()
    construction, relation_context, risk_context = _contexts(source, quality)
    outside = _outside_result(source.cross_results[0])
    resolution = resolve_problem_claim(
        TypedProblemClaimSource.from_qb_result(outside, source.projection.snapshot),
        construction,
    )
    base_resolution = resolve_problem_claim(
        TypedProblemClaimSource.from_qb_result(
            source.cross_results[0], source.projection.snapshot
        ),
        construction,
    )
    base_population = build_defect_population(
        (base_resolution,),
        source.specification_assessment.qb_consistency,
        construction,
    )
    population = replace(
        base_population,
        status=FullModelStatus.NOT_APPLICABLE,
        applicability=Applicability.NOT_APPLICABLE,
        members=(),
        population_complete=True,
        problem_resolution_refs=(resolution.ref,),
        unresolved_resolution_refs=(),
    )
    relation = relate_problem_to_quality(resolution, relation_context)

    result = assess_risk(resolution, population, relation, quality, risk_context)

    assert result.status is FullModelStatus.NOT_APPLICABLE
    assert result.classification is None


@pytest.mark.parametrize(
    ("status", "applicability"),
    [
        (FullModelStatus.UNSUPPORTED, Applicability.APPLICABLE),
        (FullModelStatus.UNAVAILABLE, Applicability.APPLICABLE),
        (FullModelStatus.UNKNOWN, Applicability.UNKNOWN),
    ],
)
def test_unsupported_unavailable_and_unknown_problem_states_propagate(
    status, applicability
) -> None:
    source = _assessment(UPPER_TWO, LOWER_FIVE)
    quality = _product_quality()
    construction, relation_context, risk_context = _contexts(source, quality)
    if status is FullModelStatus.UNSUPPORTED:
        claim = TypedProblemClaimSource.unsupported(
            ProblemClaimSourceKind.SIGNAL_FINDING,
            "FIND-U-VAGUE-001",
            "1",
        )
    else:
        claim = TypedProblemClaimSource(
            TypedSourceRef(
                ProblemClaimSourceKind.QB_CROSS_REQUIREMENT_RESULT,
                f"QB-{status.value}",
                "1",
            ),
            status,
            applicability,
        )
    resolution = resolve_problem_claim(claim, construction)
    relation = relate_problem_to_quality(resolution, relation_context)
    base_resolution = resolve_problem_claim(
        TypedProblemClaimSource.from_qb_result(
            source.cross_results[0], source.projection.snapshot
        ),
        construction,
    )
    base_population = build_defect_population(
        (base_resolution,),
        source.specification_assessment.qb_consistency,
        construction,
    )
    population_status = {
        FullModelStatus.UNSUPPORTED: FullModelStatus.AVAILABLE,
        FullModelStatus.UNAVAILABLE: FullModelStatus.UNAVAILABLE,
        FullModelStatus.UNKNOWN: FullModelStatus.UNKNOWN,
    }[status]
    population = replace(
        base_population,
        status=population_status,
        applicability=(
            Applicability.APPLICABLE
            if population_status is not FullModelStatus.UNKNOWN
            else Applicability.UNKNOWN
        ),
        members=(),
        population_complete=population_status is FullModelStatus.AVAILABLE,
        problem_resolution_refs=(resolution.ref,),
        unresolved_resolution_refs=(
            (resolution.ref,)
            if population_status is FullModelStatus.UNKNOWN
            else ()
        ),
    )

    result = assess_risk(resolution, population, relation, quality, risk_context)

    assert result.status is status
    assert result.applicability is applicability
    assert result.classification is None


def test_missing_or_invalid_relation_cannot_produce_positive_risk() -> None:
    bundle = _risk_bundle()
    with pytest.raises(TypeError, match="relation"):
        assess_risk(bundle[2], bundle[3], None, bundle[1], bundle[5])

    with pytest.raises(ValueError, match="structured risk identity"):
        replace(
            _assessed(bundle),
            rule_ref=RELATION_RULE_REF,
        )


@pytest.mark.parametrize("observed", [Decimal("1.8"), Decimal("2.3")])
def test_product_quality_polarity_does_not_change_confirmed_risk(observed) -> None:
    result = _assessed(_risk_bundle(observed=observed))

    expected = Fraction(1, 1) if observed <= Decimal("2") else Fraction(0, 1)
    assert result.product_quality_context.status is FullModelStatus.AVAILABLE
    assert result.classification is RiskClassification.RISK_IDENTIFIED
    assert _product_quality(observed).value == expected


def test_unavailable_product_quality_context_does_not_erase_confirmed_risk() -> None:
    result = _assessed(_risk_bundle(observed=None))

    assert result.product_quality_context.status is FullModelStatus.UNAVAILABLE
    assert result.classification is RiskClassification.RISK_IDENTIFIED


def test_nonconformance_cannot_create_risk_without_typed_d_and_relation() -> None:
    result = _assessed(
        _risk_bundle(UPPER_TWO, UPPER_FIVE, observed=Decimal("2.3"))
    )

    assert result.product_quality_context.status is FullModelStatus.AVAILABLE
    assert _product_quality(Decimal("2.3")).value == Fraction(0, 1)
    assert result.status is FullModelStatus.NOT_APPLICABLE
    assert result.classification is None


def test_input_is_explicit_and_resolves_to_the_exact_typed_records() -> None:
    _, quality, resolution, population, relation, context = bundle = _risk_bundle()
    risk_input = build_risk_assessment_input(
        resolution, population, relation, quality, context
    )

    assert isinstance(risk_input, BoundedRiskAssessmentInput)
    assert risk_input.problem_resolution_ref == resolution.ref
    assert risk_input.problem_ref == resolution.problem.ref
    assert risk_input.defect_population_ref == population.ref
    assert risk_input.relation_ref == relation.ref
    assert risk_input.product_quality_context.assessment_ref == (
        ProductQualityAssessmentRef(
            quality.assessment_id,
            quality.product_quality_assessment_version,
        )
    )
    assert RiskAssessor().assess(
        risk_input, resolution, population, relation, quality, context
    ) == _assessed(bundle)


def test_tampered_risk_input_fails_closed() -> None:
    _, quality, resolution, population, relation, context = _risk_bundle()
    risk_input = build_risk_assessment_input(
        resolution, population, relation, quality, context
    )

    with pytest.raises(ValueError, match="does not resolve"):
        RiskAssessor().assess(
            replace(risk_input, defect_population_status=FullModelStatus.UNKNOWN),
            resolution,
            population,
            relation,
            quality,
            context,
        )


def test_mixed_artifact_assessment_snapshot_and_process_state_fail_closed() -> None:
    _, quality, resolution, population, relation, context = _risk_bundle()
    other_artifact = ArtifactRef("SPEC-OTHER", "2")
    other_assessment = AssessmentRef("ASSESS-OTHER", "2", other_artifact)
    other_event = replace(context.assessment_event_ref, artifact_ref=other_artifact)
    foreign_artifact_context = replace(
        context,
        assessment_event_ref=other_event,
        artifact_ref=other_artifact,
        source_assessment_ref=other_assessment,
    )
    with pytest.raises(ValueError, match="artifact"):
        assess_risk(
            resolution, population, relation, quality, foreign_artifact_context
        )

    same_artifact_assessment = AssessmentRef(
        "ASSESS-OTHER", "2", context.artifact_ref
    )
    with pytest.raises(ValueError, match="assessment"):
        assess_risk(
            resolution,
            population,
            relation,
            quality,
            replace(context, source_assessment_ref=same_artifact_assessment),
        )

    other_source = _assessment(UPPER_TWO, UPPER_FIVE)
    with pytest.raises(ValueError, match="snapshot"):
        assess_risk(
            resolution,
            population,
            relation,
            quality,
            replace(context, source_snapshot_id=other_source.snapshot_id),
        )

    other_process = ProcessStateRef(
        context.process_state_ref.process_state_id,
        "2",
        context.process_state_ref.stage,
    )
    other_process_event = replace(
        context.assessment_event_ref,
        process_state_ref=other_process,
    )
    with pytest.raises(ValueError, match="process-state"):
        assess_risk(
            resolution,
            population,
            relation,
            quality,
            replace(
                context,
                assessment_event_ref=other_process_event,
                process_state_ref=other_process,
            ),
        )


def test_only_performance_efficiency_is_a_supported_target() -> None:
    assert tuple(ProductQualityCharacteristicId) == (
        ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
    )
    relation = _risk_bundle()[4]
    with pytest.raises(ValueError):
        replace(relation, characteristic_id="RELIABILITY")


def test_result_has_only_categorical_risk_and_no_theoretical_numeric_fields() -> None:
    names = {item.name for item in fields(BoundedRiskAssessment)}
    forbidden = {
        "value",
        "risk",
        "risk_score",
        "probability",
        "likelihood",
        "impact",
        "severity",
        "criticality",
        "priority",
        "confidence",
        "uncertainty",
        "rho_ij",
        "p_ij",
        "I_ij",
        "kappa_j",
        "r_ij",
        "Psi_j",
        "Risk_j",
        "Pi_i",
        "corrective_action",
    }

    assert names.isdisjoint(forbidden)
    assert RISK_PARAMETER_SET.entries == ()


def test_all_risk_nonclaims_are_present_in_contract_order() -> None:
    result = _assessed(_risk_bundle())

    assert result.non_claims == MANDATORY_RISK_NON_CLAIMS
    assert result.non_claims == tuple(RiskNonClaim)
    assert result.non_claims[-1] is RiskNonClaim.PROVISIONAL_NOT_CALIBRATED


def test_public_risk_api_has_no_direct_qb_result_operand() -> None:
    parameter_names = tuple(signature(assess_risk).parameters)

    assert parameter_names == (
        "problem_resolution",
        "defect_population",
        "relation",
        "product_quality_assessment",
        "context",
    )
    assert "cross_result" not in parameter_names
    assert "qb_result" not in parameter_names


def test_wrong_relation_rule_fails_closed() -> None:
    relation = _risk_bundle()[4]

    with pytest.raises(ValueError, match="structured relation identity"):
        replace(relation, rule_ref=RISK_RULE_REF)


def test_relation_kind_is_required_for_positive_result() -> None:
    source, quality, resolution, population, relation, context = _risk_bundle()
    assert source.cross_results
    with pytest.raises(ValueError, match="AVAILABLE relation"):
        replace(relation, relation_kind=None)

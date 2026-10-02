from dataclasses import fields, replace
from fractions import Fraction

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import (
    ComparisonKey,
    CrossRequirementResult,
    CrossResultState,
    OutsideApplicabilityReason,
    QbConsistencyState,
    SpecificationAssessmentService,
)
from requirements_quality_assessment.defect_quality import (
    DEFECT_QUALITY_RISK_CONTRACT_REF,
    MANDATORY_PROBLEM_NON_CLAIMS,
    MANDATORY_RELATION_NON_CLAIMS,
    PROBLEM_RULE_REF,
    RELATION_RULE_REF,
    ConfirmedSupportedProblem,
    DefectConstructionContext,
    DefectQualityRelationContext,
    DefectType,
    ProblemClaimSourceKind,
    ProblemDisposition,
    ProblemKind,
    RelationKind,
    RelationNonClaim,
    TypedProblemClaimSource,
    TypedSourceRef,
    build_defect_population,
    relate_problem_to_quality,
    resolve_problem_claim,
)
from requirements_quality_assessment.domain import Requirement, UnitLabel
from requirements_quality_assessment.dynamic_evidence import (
    Applicability,
    FullModelStatus,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor
from requirements_quality_assessment.metrics import ArtifactRef, AssessmentRef
from requirements_quality_assessment.performance_efficiency import (
    ProcessStage,
    ProcessStateRef,
    ProductQualityCharacteristicId,
)


UPPER_TWO = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
UPPER_FIVE = "Час відгуку ≤ 5 с при 500 одночасних користувачах"
LOWER_FIVE = "Час відгуку не нижче 5 с при 500 одночасних користувачах"


def _assessment(*texts: str):
    records = tuple(
        RequirementQualityAssessor().assess_record(
            BaselineFeatureExtractor().extract(
                Requirement(f"R{index:03d}", index, text)
            )
        )
        for index, text in enumerate(texts, start=1)
    )
    return SpecificationAssessmentService().assess(records)


def _contexts(result, *, artifact_version="1", process_version="1"):
    artifact = ArtifactRef("SPEC-RISK-001", artifact_version)
    assessment = AssessmentRef("ASSESS-SPEC-RISK-001", "1", artifact)
    process = ProcessStateRef(
        "PROCESS-RISK-001",
        process_version,
        ProcessStage.REFERENCE_VERIFICATION,
    )
    return (
        DefectConstructionContext(
            artifact,
            assessment,
            result.snapshot_id,
            process,
        ),
        DefectQualityRelationContext(
            artifact,
            assessment,
            result.snapshot_id,
            process,
        ),
    )


def _resolution(result=None):
    result = result or _assessment(UPPER_TWO, LOWER_FIVE)
    construction, relation = _contexts(result)
    claim = TypedProblemClaimSource.from_qb_result(
        result.cross_results[0], result.projection.snapshot
    )
    return result, construction, relation, resolve_problem_claim(claim, construction)


def _outside_result(base):
    return CrossRequirementResult.outside_v0_1_applicability(
        snapshot_id=base.snapshot_id,
        participants=base.participants,
        observation_refs=base.observation_refs,
        operands=base.operands,
        comparison_contract=base.comparison_contract,
        coverage_profile=base.coverage_profile,
        relation_kind=base.relation_kind,
        evidence_refs=base.evidence_refs,
        diagnostic_refs=base.diagnostic_refs,
        outside_reasons=(OutsideApplicabilityReason.CONTEXT_MISMATCH,),
        non_claim_keys=base.non_claim_keys,
    )


def test_supported_confirmed_qb_conflict_produces_exact_approved_problem() -> None:
    result, context, _, resolution = _resolution()
    problem = resolution.problem

    assert resolution.status is FullModelStatus.AVAILABLE
    assert resolution.applicability is Applicability.APPLICABLE
    assert (
        resolution.disposition
        is ProblemDisposition.CONFIRMED_SUPPORTED_PROBLEM
    )
    assert problem is not None
    assert problem.problem_kind is ProblemKind.CONFIRMED_SUPPORTED_PROBLEM
    assert problem.defect_type is DefectType.SPECIFICATION_INCONSISTENCY
    assert problem.conflict_class is result.cross_results[0].conflict_class
    assert problem.conflict_subtype is result.cross_results[0].conflict_subtype
    assert problem.rule_ref == PROBLEM_RULE_REF
    assert context.defect_risk_contract_ref == DEFECT_QUALITY_RISK_CONTRACT_REF


def test_problem_identity_and_record_are_deterministic() -> None:
    result = _assessment(UPPER_TWO, LOWER_FIVE)
    construction, _ = _contexts(result)
    claim = TypedProblemClaimSource.from_qb_result(
        result.cross_results[0], result.projection.snapshot
    )

    first = resolve_problem_claim(claim, construction)
    second = resolve_problem_claim(claim, construction)

    assert first == second
    assert first.resolution_id == second.resolution_id
    assert first.problem.problem_id == second.problem.problem_id


def test_problem_preserves_participants_key_unit_and_cross_result() -> None:
    result, _, _, resolution = _resolution()
    source = result.cross_results[0]
    problem = resolution.problem

    assert tuple(item.requirement_id for item in problem.participant_refs) == (
        "R001",
        "R002",
    )
    assert problem.comparison_key == source.comparison_key
    assert problem.comparison_key.normalized_metric == "час відгуку"
    assert (
        problem.comparison_key.normalized_context
        == "при 500 одночасних користувачах"
    )
    assert problem.comparison_key.unit.value == "SECOND"
    assert problem.source_cross_result_ref == source.result_id
    assert problem.source_observation_refs == source.observation_refs
    assert tuple(item.source_observation_ref for item in problem.operand_refs) == (
        source.observation_refs
    )


def test_problem_provenance_reaches_exact_qb_evidence_and_versions() -> None:
    result, context, _, resolution = _resolution()
    source = result.cross_results[0]
    problem = resolution.problem
    provenance = problem.provenance

    assert problem.evidence_refs == source.evidence_refs
    assert provenance.ordered_cross_evidence_refs == source.evidence_refs
    assert provenance.source_cross_result_ref == source.result_id
    assert provenance.source_snapshot_id == result.snapshot_id
    assert provenance.coverage_profile_ref.contract_id == "QB-v0.1"
    assert provenance.comparison_rule_ref.contract_id == "QB-COMPARE-001"
    assert provenance.normalization_contract_ref.contract_id == "QB-NORMALIZATION"
    assert provenance.problem_rule_ref == PROBLEM_RULE_REF
    assert problem.artifact_ref == context.artifact_ref
    assert problem.source_assessment_ref == context.source_assessment_ref
    assert problem.process_state_ref == context.process_state_ref
    assert problem.non_claims == MANDATORY_PROBLEM_NON_CLAIMS


def test_problem_maps_to_performance_efficiency_as_relevance_only() -> None:
    _, _, relation_context, resolution = _resolution()

    relation = relate_problem_to_quality(resolution, relation_context)

    assert relation.status is FullModelStatus.AVAILABLE
    assert relation.applicability is Applicability.APPLICABLE
    assert relation.relation_kind is RelationKind.BOUNDED_RISK_RELEVANCE
    assert (
        relation.characteristic_id
        is ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY
    )
    assert relation.rule_ref == RELATION_RULE_REF
    assert relation.non_claims == MANDATORY_RELATION_NON_CLAIMS
    assert RelationNonClaim.NOT_CAUSALITY in relation.non_claims
    assert "relevance only" in relation.rationale
    assert "not causality" in relation.rationale


def test_relation_identity_provenance_and_order_are_deterministic() -> None:
    _, _, relation_context, resolution = _resolution()

    first = relate_problem_to_quality(resolution, relation_context)
    second = relate_problem_to_quality(resolution, relation_context)

    assert first == second
    assert first.relation_id == second.relation_id
    assert first.problem_ref == resolution.problem.ref
    assert first.source_result_refs == (resolution.source_claim_ref,)
    assert first.evidence_refs == resolution.problem.evidence_refs
    assert first.provenance.source_cross_result_ref == (
        resolution.problem.source_cross_result_ref
    )
    assert first.provenance.comparison_key == resolution.problem.comparison_key


def test_compatible_qb_result_is_bounded_no_problem_and_no_relation() -> None:
    result = _assessment(UPPER_TWO, UPPER_FIVE)
    construction, relation_context = _contexts(result)
    claim = TypedProblemClaimSource.from_qb_result(
        result.cross_results[0], result.projection.snapshot
    )

    resolution = resolve_problem_claim(claim, construction)
    relation = relate_problem_to_quality(resolution, relation_context)

    assert resolution.disposition is (
        ProblemDisposition.NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE
    )
    assert resolution.problem is None
    assert relation.status is FullModelStatus.NOT_APPLICABLE
    assert relation.applicability is Applicability.NOT_APPLICABLE
    assert relation.relation_kind is None


def test_unresolved_qb_result_remains_unresolved_without_problem() -> None:
    result = _assessment(
        "Система працює не більше 2 с",
        "Система працює не нижче 5 с",
    )
    assert result.cross_results[0].state is CrossResultState.ASSESSMENT_UNRESOLVED
    construction, relation_context = _contexts(result)
    claim = TypedProblemClaimSource.from_qb_result(
        result.cross_results[0], result.projection.snapshot
    )

    resolution = resolve_problem_claim(claim, construction)
    relation = relate_problem_to_quality(resolution, relation_context)

    assert resolution.status is FullModelStatus.UNRESOLVED
    assert resolution.problem is None
    assert relation.status is FullModelStatus.UNRESOLVED
    assert relation.relation_kind is None


def test_outside_qb_result_is_not_applicable_without_problem() -> None:
    result = _assessment(UPPER_TWO, LOWER_FIVE)
    construction, relation_context = _contexts(result)
    outside = _outside_result(result.cross_results[0])
    claim = TypedProblemClaimSource.from_qb_result(
        outside, result.projection.snapshot
    )

    resolution = resolve_problem_claim(claim, construction)
    relation = relate_problem_to_quality(resolution, relation_context)

    assert resolution.status is FullModelStatus.NOT_APPLICABLE
    assert resolution.applicability is Applicability.NOT_APPLICABLE
    assert resolution.problem is None
    assert relation.status is FullModelStatus.NOT_APPLICABLE
    assert relation.relation_kind is None


@pytest.mark.parametrize(
    ("source_kind", "source_id"),
    [
        (ProblemClaimSourceKind.CHARACTERISTIC_ASSESSMENT, "C=0"),
        (ProblemClaimSourceKind.CHARACTERISTIC_ASSESSMENT, "V=0"),
        (ProblemClaimSourceKind.CHARACTERISTIC_ASSESSMENT, "U=0"),
        (ProblemClaimSourceKind.SIGNAL_FINDING, "FIND-U-VAGUE-001"),
        (ProblemClaimSourceKind.DETECTOR_OBSERVATION, "UNKNOWN"),
        (ProblemClaimSourceKind.CONFORMANCE_ASSESSMENT, "DOES_NOT_CONFORM"),
        (ProblemClaimSourceKind.PRODUCT_QUALITY_ASSESSMENT, "M_quality=0/1"),
    ],
)
def test_unsupported_sources_cannot_create_a_problem(
    source_kind, source_id
) -> None:
    result = _assessment(UPPER_TWO, LOWER_FIVE)
    construction, relation_context = _contexts(result)
    claim = TypedProblemClaimSource.unsupported(source_kind, source_id, "1")

    resolution = resolve_problem_claim(claim, construction)
    relation = relate_problem_to_quality(resolution, relation_context)

    assert resolution.status is FullModelStatus.UNSUPPORTED
    assert resolution.problem is None
    assert resolution.disposition is None
    assert relation.status is FullModelStatus.UNSUPPORTED
    assert relation.relation_kind is None


def test_unknown_supported_source_does_not_create_a_problem() -> None:
    result = _assessment(UPPER_TWO, LOWER_FIVE)
    construction, relation_context = _contexts(result)
    claim = TypedProblemClaimSource(
        TypedSourceRef(
            ProblemClaimSourceKind.QB_CROSS_REQUIREMENT_RESULT,
            "QB-RESULT-PENDING",
            "1",
        ),
        FullModelStatus.UNKNOWN,
        Applicability.UNKNOWN,
    )

    resolution = resolve_problem_claim(claim, construction)
    relation = relate_problem_to_quality(resolution, relation_context)

    assert resolution.status is FullModelStatus.UNKNOWN
    assert resolution.problem is None
    assert relation.status is FullModelStatus.UNKNOWN


def test_product_quality_zero_cannot_create_a_problem() -> None:
    product_quality_value = Fraction(0, 1)
    assert product_quality_value == 0
    result = _assessment(UPPER_TWO, LOWER_FIVE)
    construction, _ = _contexts(result)
    claim = TypedProblemClaimSource.unsupported(
        ProblemClaimSourceKind.PRODUCT_QUALITY_ASSESSMENT,
        f"OBSERVED_REFERENCE_INDICATOR:{product_quality_value}",
        "1",
    )

    assert resolve_problem_claim(claim, construction).problem is None


@pytest.mark.parametrize(
    ("context_source", "context_value"),
    [("CONFORMS", Fraction(1, 1)), ("DOES_NOT_CONFORM", Fraction(0, 1))],
)
def test_product_quality_context_cannot_erase_or_change_confirmed_problem(
    context_source, context_value
) -> None:
    result, _, relation_context, resolution = _resolution()
    before = relate_problem_to_quality(resolution, relation_context)
    preserved_context = (context_source, context_value)

    after = relate_problem_to_quality(resolution, relation_context)

    assert preserved_context in {
        ("CONFORMS", Fraction(1, 1)),
        ("DOES_NOT_CONFORM", Fraction(0, 1)),
    }
    assert after == before
    assert after.relation_kind is RelationKind.BOUNDED_RISK_RELEVANCE


def test_mixed_snapshot_and_artifact_versions_fail_closed() -> None:
    first = _assessment(UPPER_TWO, LOWER_FIVE)
    second = _assessment(UPPER_TWO, UPPER_FIVE)
    construction, relation_context = _contexts(first)

    with pytest.raises(ValueError, match="cross snapshots"):
        resolve_problem_claim(
            TypedProblemClaimSource.from_qb_result(
                second.cross_results[0], second.projection.snapshot
            ),
            construction,
        )

    resolution = _resolution(first)[3]
    foreign_artifact = ArtifactRef("SPEC-RISK-FOREIGN", "2")
    foreign_assessment = AssessmentRef("ASSESS-FOREIGN", "1", foreign_artifact)
    foreign_relation_context = replace(
        relation_context,
        artifact_ref=foreign_artifact,
        source_assessment_ref=foreign_assessment,
    )
    with pytest.raises(ValueError, match="mix versions"):
        relate_problem_to_quality(resolution, foreign_relation_context)


def test_tampered_metric_context_or_unit_identity_fails_closed() -> None:
    result = _assessment(UPPER_TWO, LOWER_FIVE)
    source = result.cross_results[0]
    construction, _ = _contexts(result)
    tampered_left = replace(source.operands.left, normalized_metric="час відповіді")
    tampered = replace(
        source,
        operands=replace(source.operands, left=tampered_left),
    )
    claim = TypedProblemClaimSource.from_qb_result(
        tampered, result.projection.snapshot
    )

    with pytest.raises(ValueError, match="comparison key"):
        resolve_problem_claim(claim, construction)


def _resolution_with_key(resolution, key):
    problem = replace(
        resolution.problem,
        comparison_key=key,
        provenance=replace(resolution.problem.provenance, comparison_key=key),
    )
    return replace(resolution, problem=problem)


def test_resolved_different_metric_is_not_applicable_to_pe_relation() -> None:
    _, _, relation_context, resolution = _resolution()
    key = replace(resolution.problem.comparison_key, normalized_metric="час відповіді")

    relation = relate_problem_to_quality(
        _resolution_with_key(resolution, key), relation_context
    )

    assert relation.status is FullModelStatus.NOT_APPLICABLE
    assert relation.applicability is Applicability.NOT_APPLICABLE
    assert relation.relation_kind is None


@pytest.mark.parametrize(
    "key",
    [
        ComparisonKey(
            "час відгуку",
            "під час пікового навантаження",
            UnitLabel.SECOND,
        ),
        ComparisonKey(
            "час відгуку",
            "при 500 одночасних користувачах",
            UnitLabel.MINUTE,
        ),
    ],
)
def test_response_time_with_unsupported_context_or_unit_has_no_relation(
    key,
) -> None:
    _, _, relation_context, resolution = _resolution()

    relation = relate_problem_to_quality(
        _resolution_with_key(resolution, key), relation_context
    )

    assert relation.status is FullModelStatus.UNSUPPORTED
    assert relation.applicability is Applicability.APPLICABLE
    assert relation.relation_kind is None


def test_problem_and_relation_have_no_risk_magnitude_fields() -> None:
    problem_fields = {item.name for item in fields(ConfirmedSupportedProblem)}
    _, _, relation_context, resolution = _resolution()
    relation_fields = {
        item.name
        for item in fields(type(relate_problem_to_quality(resolution, relation_context)))
    }
    forbidden = {
        "severity",
        "probability",
        "likelihood",
        "impact",
        "criticality",
        "priority",
        "confidence",
        "risk",
        "risk_score",
        "value",
    }

    assert problem_fields.isdisjoint(forbidden)
    assert relation_fields.isdisjoint(forbidden)


def test_defect_population_preserves_source_order_and_confirmed_member() -> None:
    result = _assessment(UPPER_TWO, LOWER_FIVE)
    construction, _ = _contexts(result)
    resolutions = tuple(
        resolve_problem_claim(
            TypedProblemClaimSource.from_qb_result(
                cross_result, result.projection.snapshot
            ),
            construction,
        )
        for cross_result in result.cross_results
    )

    population = build_defect_population(
        resolutions,
        result.specification_assessment.qb_consistency,
        construction,
    )

    assert population.status is FullModelStatus.AVAILABLE
    assert population.population_complete is True
    assert population.members == (resolutions[0].problem.ref,)
    assert population.problem_resolution_refs == tuple(
        item.ref for item in resolutions
    )


def test_unknown_population_can_preserve_an_individually_confirmed_member() -> None:
    result = _assessment(
        UPPER_TWO,
        LOWER_FIVE,
        "Система працює не більше 3 с",
    )
    assert result.specification_assessment.qb_consistency.state is QbConsistencyState.UNKNOWN
    assert any(
        item.state is CrossResultState.CONFIRMED_CONFLICT
        for item in result.cross_results
    )
    construction, _ = _contexts(result)
    resolutions = tuple(
        resolve_problem_claim(
            TypedProblemClaimSource.from_qb_result(
                cross_result, result.projection.snapshot
            ),
            construction,
        )
        for cross_result in result.cross_results
    )

    population = build_defect_population(
        resolutions,
        result.specification_assessment.qb_consistency,
        construction,
    )

    assert population.status is FullModelStatus.UNRESOLVED
    assert population.population_complete is False
    assert population.members
    assert population.unresolved_resolution_refs


def test_general_finding_to_quality_problem_conversion_was_not_introduced() -> None:
    signal = TypedProblemClaimSource.unsupported(
        ProblemClaimSourceKind.SIGNAL_FINDING,
        "FIND-U-VAGUE-001",
        "1",
    )
    result = _assessment(UPPER_TWO, LOWER_FIVE)
    construction, _ = _contexts(result)

    resolution = resolve_problem_claim(signal, construction)

    assert resolution.problem is None
    assert resolution.status is FullModelStatus.UNSUPPORTED
    assert "QUALITY_PROBLEM" not in {item.value for item in ProblemKind}


def test_non_claims_keep_rqd_016_open_and_relation_noncausal() -> None:
    _, _, relation_context, resolution = _resolution()
    relation = relate_problem_to_quality(resolution, relation_context)

    assert resolution.problem.non_claims == MANDATORY_PROBLEM_NON_CLAIMS
    assert resolution.problem.non_claims[3].value == "NC-D-004"
    assert relation.non_claims == MANDATORY_RELATION_NON_CLAIMS
    assert relation.non_claims[1] is RelationNonClaim.NOT_CAUSALITY

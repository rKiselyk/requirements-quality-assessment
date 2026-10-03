from dataclasses import FrozenInstanceError, fields, replace
from fractions import Fraction

import pytest

from requirements_quality_assessment.defect_quality import (
    DefectQualityRelationRef,
    RelationNonClaim,
)
from requirements_quality_assessment.dynamic_evidence import FullModelStatus
from requirements_quality_assessment.full_model_reporter import (
    AuditFullModelReporter,
    FullModelReportBundle,
    UserFullModelReporter,
)
from requirements_quality_assessment.metrics import ArtifactRef, AssessmentRef
from requirements_quality_assessment.performance_efficiency import (
    ProcessStateRef,
    ProductQualityCharacteristicId,
)
from requirements_quality_assessment.product_quality import CalibrationStatus
from requirements_quality_assessment.quantitative_risk import (
    QUANTITATIVE_RISK_CALCULATION_RULE,
    QUANTITATIVE_RISK_CONTRACT_REF,
    QuantitativeLocalRiskAssessment,
    QuantitativeRiskCalculationContext,
    QuantitativeRiskCalculationRequest,
    QuantitativeRiskContextRef,
    QuantitativeRiskOperand,
    QuantitativeRiskOperandId,
    QuantitativeRiskOperandKind,
    QuantitativeRiskOperandProvenance,
    QuantitativeRiskOperandSourceRef,
    QuantitativeRiskResultState,
    calculate_quantitative_local_risk,
)
from requirements_quality_assessment.risk import BoundedRiskAssessment

from test_risk_assessment import _assessed, _risk_bundle


VALUES = {
    QuantitativeRiskOperandKind.RHO: Fraction(1, 2),
    QuantitativeRiskOperandKind.PROBABILITY: Fraction(1, 4),
    QuantitativeRiskOperandKind.IMPACT: Fraction(3, 4),
    QuantitativeRiskOperandKind.CONTEXT_FACTOR: Fraction(2, 3),
}


def _graph():
    bundle = _risk_bundle()
    source, _, resolution, _, relation, _ = bundle
    problem = resolution.problem
    assert problem is not None
    context = QuantitativeRiskCalculationContext(
        "Q-RISK-CALC-REF-001",
        "1",
        problem.artifact_ref,
        problem.source_assessment_ref,
        problem.source_snapshot_id,
        problem.process_state_ref,
    )
    return bundle, source, problem, relation, context


def _operand(
    kind,
    problem,
    relation,
    *,
    state=FullModelStatus.AVAILABLE,
    value="DEFAULT",
    provenance_overrides=None,
):
    provenance_args = dict(
        source_ref=QuantitativeRiskOperandSourceRef(
            f"TC03-{kind.value}-SOURCE", "1", "CONTROLLED-REFERENCE-PROVIDER", "1"
        ),
        source_or_rationale="controlled TC-03 executability fixture; not calibrated",
        calibration_status=CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
        governing_contract_ref=QUANTITATIVE_RISK_CONTRACT_REF,
        artifact_ref=problem.artifact_ref,
        problem_ref=problem.ref,
        relation_ref=relation.ref,
        characteristic_id=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
        process_state_ref=problem.process_state_ref,
        context_ref=(
            QuantitativeRiskContextRef("TC03-CONTEXT", "1")
            if kind is QuantitativeRiskOperandKind.CONTEXT_FACTOR
            else None
        ),
    )
    provenance_args.update(provenance_overrides or {})
    actual = VALUES[kind] if value == "DEFAULT" else value
    return QuantitativeRiskOperand(
        QuantitativeRiskOperandId(kind, f"TC03-{kind.value}", "1"),
        kind,
        state,
        actual,
        QuantitativeRiskOperandProvenance(**provenance_args),
    )


def _request(*, states=None, values=None):
    bundle, source, problem, relation, context = _graph()
    states = states or {}
    values = values or {}
    operands = {
        kind: _operand(
            kind,
            problem,
            relation,
            state=states.get(kind, FullModelStatus.AVAILABLE),
            value=values.get(kind, "DEFAULT"),
        )
        for kind in QuantitativeRiskOperandKind
    }
    request = QuantitativeRiskCalculationRequest(
        problem,
        relation,
        context,
        operands[QuantitativeRiskOperandKind.RHO],
        operands[QuantitativeRiskOperandKind.PROBABILITY],
        operands[QuantitativeRiskOperandKind.IMPACT],
        operands[QuantitativeRiskOperandKind.CONTEXT_FACTOR],
    )
    return bundle, source, problem, relation, request


def test_domain_is_distinct_typed_versioned_and_immutable():
    _, _, _, _, request = _request()
    result = calculate_quantitative_local_risk(request)

    assert type(result) is QuantitativeLocalRiskAssessment
    assert not isinstance(result, BoundedRiskAssessment)
    assert tuple(QuantitativeRiskOperandKind) == (
        QuantitativeRiskOperandKind.RHO,
        QuantitativeRiskOperandKind.PROBABILITY,
        QuantitativeRiskOperandKind.IMPACT,
        QuantitativeRiskOperandKind.CONTEXT_FACTOR,
    )
    for operand in request.operands:
        assert operand.operand_id.operand_id
        assert operand.operand_id.operand_version == "1"
        assert operand.provenance.source_ref.source_version == "1"
        assert operand.provenance.source_ref.provider_version == "1"
        assert operand.provenance.calibration_status is CalibrationStatus.PROVISIONAL_NOT_CALIBRATED
    with pytest.raises(FrozenInstanceError):
        request.rho.provenance.source_or_rationale = "changed"


def test_controlled_reference_is_exact_and_deterministic():
    _, _, problem, relation, request = _request()
    first = calculate_quantitative_local_risk(request)
    second = calculate_quantitative_local_risk(request)

    assert first == second
    assert first.assessment_id == second.assessment_id
    assert first.state is QuantitativeRiskResultState.AVAILABLE
    assert first.local_risk == Fraction(1, 16)
    assert first.provenance.problem_ref == problem.ref
    assert first.provenance.relation_ref == relation.ref
    assert first.provenance.artifact_ref == problem.artifact_ref
    assert first.provenance.process_state_ref == problem.process_state_ref
    assert first.provenance.characteristic_id is ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY
    assert first.calculation_rule == QUANTITATIVE_RISK_CALCULATION_RULE
    assert tuple(item.ref for item in first.provenance.operands) == tuple(
        item.ref for item in request.operands
    )


def test_explicit_available_zero_is_data_not_absence():
    _, _, _, _, request = _request(
        values={QuantitativeRiskOperandKind.PROBABILITY: Fraction(0, 1)}
    )
    result = calculate_quantitative_local_risk(request)

    assert result.state is QuantitativeRiskResultState.AVAILABLE
    assert result.local_risk == Fraction(0, 1)
    assert request.probability.state is FullModelStatus.AVAILABLE
    assert request.probability.value == Fraction(0, 1)


@pytest.mark.parametrize(
    "state",
    [
        FullModelStatus.UNKNOWN,
        FullModelStatus.UNAVAILABLE,
        FullModelStatus.UNRESOLVED,
        FullModelStatus.NOT_APPLICABLE,
    ],
)
def test_nonvalue_states_withhold_without_imputing_zero(state):
    _, _, _, _, request = _request(
        states={QuantitativeRiskOperandKind.PROBABILITY: state},
        values={QuantitativeRiskOperandKind.PROBABILITY: None},
    )
    result = calculate_quantitative_local_risk(request)

    assert result.state is QuantitativeRiskResultState.CALCULATION_WITHHELD
    assert result.local_risk is None
    assert result.operands[1].state is state
    assert result.operands[1].value is None


def test_heterogeneous_missing_states_all_survive_without_precedence():
    _, _, _, _, request = _request(
        states={
            QuantitativeRiskOperandKind.PROBABILITY: FullModelStatus.UNKNOWN,
            QuantitativeRiskOperandKind.IMPACT: FullModelStatus.UNAVAILABLE,
        },
        values={
            QuantitativeRiskOperandKind.PROBABILITY: None,
            QuantitativeRiskOperandKind.IMPACT: None,
        },
    )
    result = calculate_quantitative_local_risk(request)

    assert result.local_risk is None
    assert tuple(item.state for item in result.provenance.operands) == (
        FullModelStatus.AVAILABLE,
        FullModelStatus.UNKNOWN,
        FullModelStatus.UNAVAILABLE,
        FullModelStatus.AVAILABLE,
    )


def test_operand_value_binding_and_numeric_contract_fail_closed():
    _, _, problem, relation, _ = _graph()
    with pytest.raises(TypeError, match="exact Fraction"):
        _operand(QuantitativeRiskOperandKind.RHO, problem, relation, value=0.5)
    with pytest.raises(ValueError, match="value=None"):
        _operand(
            QuantitativeRiskOperandKind.PROBABILITY,
            problem,
            relation,
            state=FullModelStatus.UNKNOWN,
            value=Fraction(0, 1),
        )


@pytest.mark.parametrize("kind", tuple(QuantitativeRiskOperandKind))
@pytest.mark.parametrize("value", (Fraction(-1, 10), Fraction(11, 10)))
def test_every_available_operand_rejects_values_outside_unit_interval(kind, value):
    _, _, problem, relation, _ = _graph()

    with pytest.raises(ValueError, match=rf"{kind.value}.*\[0,1\]"):
        _operand(kind, problem, relation, value=value)


@pytest.mark.parametrize("kind", tuple(QuantitativeRiskOperandKind))
@pytest.mark.parametrize("value", (Fraction(0, 1), Fraction(1, 1)))
def test_every_available_operand_accepts_closed_unit_interval_boundaries(kind, value):
    _, _, problem, relation, _ = _graph()

    operand = _operand(kind, problem, relation, value=value)

    assert operand.state is FullModelStatus.AVAILABLE
    assert operand.value == value


def test_probability_above_one_fails_during_operand_construction():
    with pytest.raises(ValueError, match=r"PROBABILITY.*\[0,1\]"):
        _request(values={QuantitativeRiskOperandKind.PROBABILITY: Fraction(2, 1)})


def test_wrong_duplicate_or_missing_operand_slots_fail_closed():
    _, _, _, _, request = _request()
    with pytest.raises(ValueError, match="probability requires"):
        replace(request, probability=request.rho)
    with pytest.raises(TypeError, match="impact"):
        replace(request, impact=None)
    duplicate_textual_id = replace(
        request.probability.operand_id,
        operand_id=request.rho.operand_id.operand_id,
        operand_version=request.rho.operand_id.operand_version,
    )
    with pytest.raises(ValueError, match="identities must be unique"):
        replace(
            request,
            probability=replace(
                request.probability,
                operand_id=duplicate_textual_id,
            ),
        )


def test_cross_graph_and_wrong_characteristic_inputs_fail_closed():
    _, _, problem, relation, request = _request()
    fake_artifact = ArtifactRef(problem.artifact_ref.artifact_id, "cross-artifact")
    fake_assessment = AssessmentRef("CROSS-ASSESSMENT", "1", fake_artifact)
    with pytest.raises(ValueError, match="cross artifacts"):
        replace(
            request,
            context=replace(
                request.context,
                artifact_ref=fake_artifact,
                source_assessment_ref=fake_assessment,
            ),
        )

    other_process = ProcessStateRef(
        problem.process_state_ref.process_state_id,
        "cross-process",
        problem.process_state_ref.stage,
    )
    with pytest.raises(ValueError, match="cross process"):
        replace(request, context=replace(request.context, process_state_ref=other_process))

    same_artifact_assessment = AssessmentRef(
        "CROSS-RELATION-ASSESSMENT",
        "1",
        problem.artifact_ref,
    )
    relation_with_other_assessment = replace(
        relation,
        source_assessment_ref=same_artifact_assessment,
    )
    with pytest.raises(ValueError, match="relation.*source assessments"):
        replace(request, relation=relation_with_other_assessment)

    other_snapshot = replace(
        problem.source_snapshot_id,
        value="qb-snapshot-sha256:" + "2" * 64,
    )
    relation_with_other_snapshot = replace(
        relation,
        source_snapshot_id=other_snapshot,
    )
    with pytest.raises(ValueError, match="relation.*source snapshots"):
        replace(request, relation=relation_with_other_snapshot)

    fake_problem_ref = replace(
        problem.ref,
        problem_id=replace(problem.problem_id, source_snapshot_id=replace(
            problem.source_snapshot_id, value="qb-snapshot-sha256:" + "0" * 64
        )),
    )
    fake_relation_ref = DefectQualityRelationRef(
        replace(relation.relation_id, problem_ref=fake_problem_ref)
    )
    fake_provenance = replace(
        request.rho.provenance,
        problem_ref=fake_problem_ref,
        relation_ref=fake_relation_ref,
    )
    with pytest.raises(ValueError, match="cross problems"):
        replace(request, rho=replace(request.rho, provenance=fake_provenance))

    alternate_relation_ref = DefectQualityRelationRef(
        replace(relation.relation_id, problem_resolution_ref=replace(
            relation.problem_resolution_ref,
            resolution_id=replace(
                relation.problem_resolution_ref.resolution_id,
                source_snapshot_id=replace(
                    problem.source_snapshot_id, value="qb-snapshot-sha256:" + "1" * 64
                ),
            ),
        ))
    )
    with pytest.raises(ValueError, match="cross relations"):
        replace(
            request,
            rho=replace(
                request.rho,
                provenance=replace(request.rho.provenance, relation_ref=alternate_relation_ref),
            ),
        )

    with pytest.raises(ValueError, match="Performance Efficiency"):
        replace(
            request.rho.provenance,
            characteristic_id="NOT_PERFORMANCE_EFFICIENCY",
        )


def test_structural_relation_remains_nonnumeric_and_unmodified():
    _, _, _, relation, request = _request()
    before = relation
    calculate_quantitative_local_risk(request)

    assert relation == before
    assert RelationNonClaim.NOT_NUMERIC_RHO in relation.non_claims
    assert "rho" not in {item.name for item in fields(type(relation))}


def test_reporting_distinguishes_categorical_numeric_and_withheld_results():
    risk_bundle, source, _, _, request = _request()
    categorical = _assessed(risk_bundle)
    available = calculate_quantitative_local_risk(request)
    bundle = FullModelReportBundle(
        assessment_result=source,
        risk_assessments=(categorical,),
        quantitative_risk_assessments=(available,),
    )
    user = UserFullModelReporter().render_projection(bundle)
    audit = AuditFullModelReporter().render_projection(bundle)

    assert "Категоріальний обмежений ризик: RISK_IDENTIFIED" in user
    assert "Кількісний локальний ризик r_ij" in user
    assert "Кількісний r_ij: 1/16" in user
    assert "extern" not in user.lower() or "зовніш" in user.lower()
    for expected in (
        "Quantitative local risk r_ij",
        "operand_version: 1",
        "provider_version: 1",
        "source_or_rationale:",
        "calibration_status: PROVISIONAL_NOT_CALIBRATED",
        "calculation_rule: r_ij = rho_ij * p_ij * I_ij * kappa_j(C)",
        "local_risk: Fraction(1,16)",
    ):
        assert expected in audit

    withheld_request = replace(
        request,
        probability=replace(
            request.probability,
            state=FullModelStatus.UNKNOWN,
            value=None,
        ),
    )
    withheld = calculate_quantitative_local_risk(withheld_request)
    withheld_bundle = replace(bundle, quantitative_risk_assessments=(withheld,))
    withheld_user = UserFullModelReporter().render_projection(withheld_bundle)
    withheld_audit = AuditFullModelReporter().render_projection(withheld_bundle)
    assert "CALCULATION_WITHHELD" in withheld_user
    assert "local_risk: NONE" in withheld_audit
    assert "state: UNKNOWN" in withheld_audit


def test_omitted_quantitative_risk_is_byte_compatible_and_field_is_appended():
    risk_bundle, source, _, _, _ = _request()
    categorical = _assessed(risk_bundle)
    implicit = FullModelReportBundle(source, risk_assessments=(categorical,))
    explicit = FullModelReportBundle(
        source,
        risk_assessments=(categorical,),
        quantitative_risk_assessments=(),
    )
    assert UserFullModelReporter().render(implicit) == UserFullModelReporter().render(explicit)
    assert AuditFullModelReporter().render(implicit) == AuditFullModelReporter().render(explicit)
    names = tuple(item.name for item in fields(FullModelReportBundle))
    assert names[-2:] == ("predicted_product_quality", "quantitative_risk_assessments")

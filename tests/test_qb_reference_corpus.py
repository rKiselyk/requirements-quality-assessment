"""IMP-11 binding reference-corpus and exact end-to-end acceptance.

The acceptance data below is an executable transcription of
``docs/cross-requirement-consistency-reference-cases.md``.  It deliberately
does not parse that Markdown or infer alternative expectations.  Domain cases
start from the documented immutable quantitative observations; end-to-end
cases use the real reader, extractor, local assessor, and specification
assessment service.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal
from fractions import Fraction

import pytest

from requirements_quality_assessment.aggregator import SpecificationQualityAggregator
from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import (
    BoundedConflictSubtype,
    BoundedNonClaimKey,
    ConflictClass,
    CrossResultState,
    CrossUnresolvedReason,
    OutsideApplicabilityReason,
    QbConsistencyState,
    QbMaterialityDisposition,
    SpecificationAssessmentService,
    normalize_qb_identity_text,
)
from requirements_quality_assessment.detectors.quantitative import (
    QUANT_LB_CONTEXT_RULE_ID,
    QUANT_LB_METRIC_RULE_ID,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorComponent,
    ComparatorLabel,
    DetectionProcessingStatus,
    DetectionStatus,
    Evidence,
    FeatureDetectionOutcome,
    FeatureId,
    NumericValueComponent,
    QuantitativeComponentName,
    QuantitativeConstraintObservation,
    Requirement,
    RequirementAssessmentRecord,
    TextComponent,
    UnitComponent,
    UnitLabel,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor
from requirements_quality_assessment.reader import RequirementReader
from requirements_quality_assessment.reporter import ConsoleReporter, UserConsoleReporter


DOMAIN = "BINDING_DOMAIN_CONTRACT_REFERENCE_CASE"
END_TO_END = "BINDING_END_TO_END_REFERENCE_CASE"


@dataclass(frozen=True, slots=True)
class EvidenceExpected:
    evidence_id: str
    rule_id: str
    text: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class DiagnosticExpected:
    text: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class ObservationExpected:
    metric_id: str | None
    scalar_id: str
    context_id: str | None
    comparator: ComparatorLabel
    inclusivity: BoundaryInclusivity | None
    value: Decimal
    unit: UnitLabel | None
    unresolved: tuple[QuantitativeComponentName, ...] = ()

    @property
    def evidence_ids(self) -> tuple[str, ...]:
        return tuple(
            item
            for item in (self.metric_id, self.scalar_id, self.context_id)
            if item is not None
        )


@dataclass(frozen=True, slots=True)
class InputExpected:
    text: str
    evidence: tuple[EvidenceExpected, ...] = ()
    observations: tuple[ObservationExpected, ...] = ()
    processing: DetectionProcessingStatus = DetectionProcessingStatus.COMPLETE
    diagnostics: tuple[DiagnosticExpected, ...] = ()


@dataclass(frozen=True, slots=True)
class ResultExpected:
    participants: tuple[str, str]
    observation_indexes: tuple[int, int]
    state: CrossResultState
    unresolved: tuple[CrossUnresolvedReason, ...] = ()
    outside: tuple[OutsideApplicabilityReason, ...] = ()


@dataclass(frozen=True, slots=True)
class CorpusCase:
    case_id: str
    boundary: str
    inputs: tuple[InputExpected, ...]
    results: tuple[ResultExpected, ...]
    rconf: tuple[str, ...]
    aggregate_state: QbConsistencyState
    aggregate_value: Fraction | None
    # Production QbConsistencyObservability field order, not the abbreviated
    # corpus META order.
    metadata: tuple[int | bool, ...]


def _e(
    evidence_id: str,
    text: str,
    start: int,
    end: int,
    rule_id: str | None = None,
) -> EvidenceExpected:
    return EvidenceExpected(evidence_id, rule_id or evidence_id, text, start, end)


def _obs(
    metric_id: str | None,
    scalar_id: str,
    context_id: str | None,
    comparator: ComparatorLabel,
    value: str,
    unit: UnitLabel | None = UnitLabel.SECOND,
    *,
    inclusivity: BoundaryInclusivity | None = BoundaryInclusivity.INCLUSIVE,
    unresolved: tuple[QuantitativeComponentName, ...] = (),
) -> ObservationExpected:
    return ObservationExpected(
        metric_id,
        scalar_id,
        context_id,
        comparator,
        inclusivity,
        Decimal(value),
        unit,
        unresolved,
    )


def _input(
    text: str,
    evidence: tuple[EvidenceExpected, ...] = (),
    observations: tuple[ObservationExpected, ...] = (),
    *,
    processing: DetectionProcessingStatus = DetectionProcessingStatus.COMPLETE,
    diagnostics: tuple[DiagnosticExpected, ...] = (),
) -> InputExpected:
    return InputExpected(text, evidence, observations, processing, diagnostics)


def _result(
    left: str,
    right: str,
    state: CrossResultState,
    *,
    indexes: tuple[int, int] = (0, 0),
    unresolved: tuple[CrossUnresolvedReason, ...] = (),
    outside: tuple[OutsideApplicabilityReason, ...] = (),
) -> ResultExpected:
    return ResultExpected((left, right), indexes, state, unresolved, outside)


def _meta(
    nr: int,
    nrq: int,
    nra: int,
    npairs: int,
    nq: int,
    na: int,
    nc: int,
    nw: int,
    nu: int,
    no: int,
    nx: int,
    nrconf: int,
    complete: bool,
    *,
    material: int | None = None,
    non_material: int = 0,
) -> tuple[int | bool, ...]:
    if material is None:
        material = nx
    return (
        nr,
        nrq,
        nra,
        npairs,
        nq,
        nc,
        nw,
        nu,
        no,
        na,
        nx,
        material,
        non_material,
        nrconf,
        complete,
    )


# Section 3.4 domain-projection templates.  M/B/C are intentionally local
# Evidence IDs exactly as declared by the corpus.
def _domain_bound(
    text: str,
    metric: tuple[str, int, int] | None,
    bound: tuple[str, int, int],
    context: tuple[str, int, int] | None,
    comparator: ComparatorLabel,
    value: str,
    unit: UnitLabel | None = UnitLabel.SECOND,
    *,
    inclusivity: BoundaryInclusivity | None = BoundaryInclusivity.INCLUSIVE,
    unresolved: tuple[QuantitativeComponentName, ...] = (),
) -> InputExpected:
    evidence = []
    if metric is not None:
        evidence.append(_e("M", metric[0], metric[1], metric[2], "M"))
    evidence.append(_e("B", bound[0], bound[1], bound[2], "B"))
    if context is not None:
        evidence.append(_e("C", context[0], context[1], context[2], "C"))
    return _input(
        text,
        tuple(evidence),
        (
            _obs(
                None if metric is None else "M",
                "B",
                None if context is None else "C",
                comparator,
                value,
                unit,
                inclusivity=inclusivity,
                unresolved=unresolved,
            ),
        ),
    )


STD_CONTEXT = "при 500 одночасних користувачах"


def _upper(value: str, *, unit: UnitLabel = UnitLabel.SECOND) -> InputExpected:
    unit_text = "с" if unit is UnitLabel.SECOND else "хв"
    bound = f"≤ {value} {unit_text}"
    text = f"Час відгуку {bound} {STD_CONTEXT}"
    bound_end = 12 + len(bound)
    return _domain_bound(
        text,
        ("Час відгуку", 0, 11),
        (bound, 12, bound_end),
        (STD_CONTEXT, bound_end + 1, len(text)),
        ComparatorLabel.LESS_THAN_OR_EQUAL,
        value,
        unit,
    )


def _lower(value: str) -> InputExpected:
    bound = f"не нижче {value} с"
    text = f"Час відгуку {bound} {STD_CONTEXT}"
    return _domain_bound(
        text,
        ("Час відгуку", 0, 11),
        (bound, 12, 12 + len(bound)),
        (STD_CONTEXT, 13 + len(bound), len(text)),
        ComparatorLabel.GREATER_THAN_OR_EQUAL,
        value,
    )


D_U2_S = _upper("2")
D_U5_S = _upper("5")
D_U1_S = _upper("1")
D_U1_M = _upper("1", unit=UnitLabel.MINUTE)
D_L5_S = _lower("5")
D_L2_S = _lower("2")
D_SYN_U2 = _domain_bound(
    "Час відповіді ≤ 2 с при 500 одночасних користувачах",
    ("Час відповіді", 0, 13),
    ("≤ 2 с", 14, 19),
    (STD_CONTEXT, 20, 51),
    ComparatorLabel.LESS_THAN_OR_EQUAL,
    "2",
)
D_CTX_U2 = _domain_bound(
    "Час відгуку ≤ 2 с під час пікового навантаження",
    ("Час відгуку", 0, 11),
    ("≤ 2 с", 12, 17),
    ("під час пікового навантаження", 18, 47),
    ComparatorLabel.LESS_THAN_OR_EQUAL,
    "2",
)
D_FREQ = _domain_bound(
    "Час відгуку не рідше одного разу на 5 с при 500 одночасних користувачах",
    ("Час відгуку", 0, 11),
    ("не рідше одного разу на 5 с", 12, 39),
    (STD_CONTEXT, 40, 71),
    ComparatorLabel.NOT_LESS_FREQUENT,
    "5",
    inclusivity=None,
)
D_UNRES_M = _domain_bound(
    "≤ 2 с при 500 одночасних користувачах",
    None,
    ("≤ 2 с", 0, 5),
    (STD_CONTEXT, 6, 37),
    ComparatorLabel.LESS_THAN_OR_EQUAL,
    "2",
    unresolved=(QuantitativeComponentName.METRIC,),
)
D_UNRES_C = _domain_bound(
    "Час відгуку ≤ 2 с",
    ("Час відгуку", 0, 11),
    ("≤ 2 с", 12, 17),
    None,
    ComparatorLabel.LESS_THAN_OR_EQUAL,
    "2",
    unresolved=(QuantitativeComponentName.CONTEXT,),
)
D_UNRES_C_ONE = replace(
    D_UNRES_C,
    text="Час відгуку ≤ 1 с",
    evidence=(
        _e("M", "Час відгуку", 0, 11, "M"),
        _e("B", "≤ 1 с", 12, 17, "B"),
    ),
    observations=(
        _obs(
            "M",
            "B",
            None,
            ComparatorLabel.LESS_THAN_OR_EQUAL,
            "1",
            unresolved=(QuantitativeComponentName.CONTEXT,),
        ),
    ),
)
D_NORM_1 = _domain_bound(
    "ЧАС  ДІЙ ≤ 2 с ПІД ЧАС  ДІЙ",
    ("ЧАС  ДІЙ", 0, 8),
    ("≤ 2 с", 9, 14),
    ("ПІД ЧАС  ДІЙ", 15, 27),
    ComparatorLabel.LESS_THAN_OR_EQUAL,
    "2",
)
D_NORM_2 = _domain_bound(
    "час дій ≤ 5 с під час дій",
    ("час дій", 0, 8),
    ("≤ 5 с", 9, 14),
    ("під час дій", 15, 27),
    ComparatorLabel.LESS_THAN_OR_EQUAL,
    "5",
)
D_NONE = _input("Система формує звіт.")


# Section 3.3 exact production-extractor templates.
def _upper_e2e(value: str, unit_text: str = "с") -> InputExpected:
    unit = UnitLabel.SECOND if unit_text == "с" else UnitLabel.MINUTE
    text = f"Час відгуку ≤ {value} {unit_text} {STD_CONTEXT}"
    scalar = f"≤ {value} {unit_text}"
    scalar_end = 12 + len(scalar)
    context_start = scalar_end + 1
    return _input(
        text,
        (
            _e("QUANT-METRIC-001:E001", "Час відгуку", 0, 11, "QUANT-METRIC-001"),
            _e("QUANT-001:E001", scalar, 12, scalar_end, "QUANT-001"),
            _e(
                "QUANT-CONTEXT-001:E001",
                STD_CONTEXT,
                context_start,
                len(text),
                "QUANT-CONTEXT-001",
            ),
        ),
        (
            _obs(
                "QUANT-METRIC-001:E001",
                "QUANT-001:E001",
                "QUANT-CONTEXT-001:E001",
                ComparatorLabel.LESS_THAN_OR_EQUAL,
                value,
                unit,
            ),
        ),
        processing=DetectionProcessingStatus.INCOMPLETE,
        diagnostics=(DiagnosticExpected("500", context_start + 4, context_start + 7),),
    )


E_U2_S_C = _upper_e2e("2")
E_U5_S_C = _upper_e2e("5")
E_U1_M_C = _upper_e2e("1", "хв")


def _upper_no_context(value: str) -> InputExpected:
    text = f"Час відгуку ≤ {value} с"
    return _input(
        text,
        (
            _e("QUANT-METRIC-001:E001", "Час відгуку", 0, 11, "QUANT-METRIC-001"),
            _e("QUANT-001:E001", f"≤ {value} с", 12, 17, "QUANT-001"),
        ),
        (
            _obs(
                "QUANT-METRIC-001:E001",
                "QUANT-001:E001",
                None,
                ComparatorLabel.LESS_THAN_OR_EQUAL,
                value,
            ),
        ),
    )


def _upper_no_metric(value: str) -> InputExpected:
    return _input(
        f"≤ {value} с",
        (_e("QUANT-001:E001", f"≤ {value} с", 0, 5, "QUANT-001"),),
        (
            _obs(
                None,
                "QUANT-001:E001",
                None,
                ComparatorLabel.LESS_THAN_OR_EQUAL,
                value,
            ),
        ),
    )


E_U2_S_NC = _upper_no_context("2")
E_U5_S_NC = _upper_no_context("5")
E_U2_S_NM = _upper_no_metric("2")
E_U5_S_NM = _upper_no_metric("5")
E_U3_S_NM = _upper_no_metric("3")
E_UPPER = _input(
    "до 300",
    (_e("QUANT-UK-001:E001", "до 300", 0, 6, "QUANT-UK-001"),),
    (
        _obs(
            None,
            "QUANT-UK-001:E001",
            None,
            ComparatorLabel.UPPER_BOUND,
            "300",
            None,
            inclusivity=BoundaryInclusivity.UNRESOLVED,
        ),
    ),
)
E_MULTI = _input(
    "Час відгуку ≤ 2 с та ≤ 5 с",
    (
        _e("QUANT-001:E001", "≤ 2 с", 12, 17, "QUANT-001"),
        _e("QUANT-001:E002", "≤ 5 с", 21, 26, "QUANT-001"),
    ),
    (
        _obs(None, "QUANT-001:E001", None, ComparatorLabel.LESS_THAN_OR_EQUAL, "2"),
        _obs(None, "QUANT-001:E002", None, ComparatorLabel.LESS_THAN_OR_EQUAL, "5"),
    ),
)
E_NONE_1 = _input("Система формує звіт.")
E_NONE_2 = _input("Система зберігає журнал.")
E_X95 = _input(
    "Система використовує профіль 95.",
    processing=DetectionProcessingStatus.INCOMPLETE,
    diagnostics=(DiagnosticExpected("95", 29, 31),),
)


C = CrossResultState.CONFIRMED_CONFLICT
W = CrossResultState.COMPATIBLE_WITHIN_RULE
U = CrossResultState.ASSESSMENT_UNRESOLVED
O = CrossResultState.OUTSIDE_V0_1_APPLICABILITY
MM = (CrossUnresolvedReason.MISSING_METRIC, CrossUnresolvedReason.MISSING_CONTEXT)
MC = (CrossUnresolvedReason.MISSING_CONTEXT,)
UC = (CrossUnresolvedReason.UNRESOLVED_CONTEXT,)


CASES = (
    CorpusCase("RC-QB-001", DOMAIN, (D_U2_S, D_L5_S), (_result("R001", "R002", C),), ("R001", "R002"), QbConsistencyState.COMPUTED, Fraction(0, 1), _meta(2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 2, True)),
    CorpusCase("RC-QB-002", DOMAIN, (D_L5_S, D_U2_S), (_result("R001", "R002", C),), ("R001", "R002"), QbConsistencyState.COMPUTED, Fraction(0, 1), _meta(2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 2, True)),
    CorpusCase("RC-QB-003", DOMAIN, (D_U2_S, D_L5_S, D_U1_S), (_result("R001", "R002", C), _result("R001", "R003", W), _result("R002", "R003", C)), ("R001", "R002", "R003"), QbConsistencyState.COMPUTED, Fraction(0, 1), _meta(3, 3, 3, 3, 3, 3, 2, 1, 0, 0, 0, 3, True)),
    CorpusCase("RC-QB-004", DOMAIN, (D_U5_S, D_L2_S), (_result("R001", "R002", W),), (), QbConsistencyState.COMPUTED, Fraction(1, 1), _meta(2, 2, 2, 1, 1, 1, 0, 1, 0, 0, 0, 0, True)),
    CorpusCase("RC-QB-005", END_TO_END, (E_U2_S_C, E_U5_S_C), (_result("R001", "R002", W),), (), QbConsistencyState.COMPUTED, Fraction(1, 1), _meta(2, 2, 2, 1, 1, 1, 0, 1, 0, 0, 2, 0, True, material=0, non_material=2)),
    CorpusCase("RC-QB-006", DOMAIN, (D_L5_S, D_L2_S), (_result("R001", "R002", W),), (), QbConsistencyState.COMPUTED, Fraction(1, 1), _meta(2, 2, 2, 1, 1, 1, 0, 1, 0, 0, 0, 0, True)),
    CorpusCase("RC-QB-007", DOMAIN, (D_U5_S, D_L5_S), (_result("R001", "R002", W),), (), QbConsistencyState.COMPUTED, Fraction(1, 1), _meta(2, 2, 2, 1, 1, 1, 0, 1, 0, 0, 0, 0, True)),
    CorpusCase("RC-QB-008", DOMAIN, (D_NORM_1, D_NORM_2), (_result("R001", "R002", W),), (), QbConsistencyState.COMPUTED, Fraction(1, 1), _meta(2, 2, 2, 1, 1, 1, 0, 1, 0, 0, 0, 0, True)),
    CorpusCase("RC-QB-009", DOMAIN, (D_U2_S, D_SYN_U2), (_result("R001", "R002", O, outside=(OutsideApplicabilityReason.METRIC_MISMATCH,)),), (), QbConsistencyState.NOT_APPLICABLE, None, _meta(2, 2, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, True)),
    CorpusCase("RC-QB-010", DOMAIN, (D_U2_S, D_CTX_U2), (_result("R001", "R002", O, outside=(OutsideApplicabilityReason.CONTEXT_MISMATCH,)),), (), QbConsistencyState.NOT_APPLICABLE, None, _meta(2, 2, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, True)),
    CorpusCase("RC-QB-011", END_TO_END, (E_U2_S_C, E_U1_M_C), (_result("R001", "R002", O, outside=(OutsideApplicabilityReason.UNIT_MISMATCH,)),), (), QbConsistencyState.NOT_APPLICABLE, None, _meta(2, 2, 0, 1, 1, 0, 0, 0, 0, 1, 2, 0, True, material=0, non_material=2)),
    CorpusCase("RC-QB-012", DOMAIN, (D_U2_S, D_U1_M), (_result("R001", "R002", O, outside=(OutsideApplicabilityReason.UNIT_MISMATCH,)),), (), QbConsistencyState.NOT_APPLICABLE, None, _meta(2, 2, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, True)),
    CorpusCase("RC-QB-013", END_TO_END, (E_U2_S_NM, E_U5_S_NM), (_result("R001", "R002", U, unresolved=MM),), (), QbConsistencyState.UNKNOWN, None, _meta(2, 2, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, False)),
    CorpusCase("RC-QB-014", END_TO_END, (E_U2_S_NC, E_U5_S_NC), (_result("R001", "R002", U, unresolved=MC),), (), QbConsistencyState.UNKNOWN, None, _meta(2, 2, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, False)),
    CorpusCase("RC-QB-015", DOMAIN, (D_U2_S, D_UNRES_M, D_UNRES_C), (_result("R001", "R002", U, unresolved=(CrossUnresolvedReason.UNRESOLVED_METRIC,)), _result("R001", "R003", U, unresolved=UC), _result("R002", "R003", U, unresolved=(CrossUnresolvedReason.UNRESOLVED_METRIC, CrossUnresolvedReason.UNRESOLVED_CONTEXT))), (), QbConsistencyState.UNKNOWN, None, _meta(3, 3, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, False)),
    CorpusCase("RC-QB-016", END_TO_END, (E_UPPER, E_U2_S_NM), (_result("R001", "R002", U, unresolved=(CrossUnresolvedReason.MISSING_METRIC, CrossUnresolvedReason.MISSING_CONTEXT, CrossUnresolvedReason.MISSING_UNIT, CrossUnresolvedReason.UNRESOLVED_INCLUSIVITY)),), (), QbConsistencyState.UNKNOWN, None, _meta(2, 2, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, False)),
    CorpusCase("RC-QB-017", DOMAIN, (D_FREQ, D_U5_S), (_result("R001", "R002", O, outside=(OutsideApplicabilityReason.COMPARATOR_OUTSIDE_PROFILE,)),), (), QbConsistencyState.NOT_APPLICABLE, None, _meta(2, 2, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, True)),
    CorpusCase("RC-QB-018", END_TO_END, (E_MULTI, E_U3_S_NM), (_result("R001", "R002", U, indexes=(0, 0), unresolved=MM), _result("R001", "R002", U, indexes=(1, 0), unresolved=MM)), (), QbConsistencyState.UNKNOWN, None, _meta(2, 2, 0, 1, 2, 0, 0, 0, 2, 0, 0, 0, False)),
    CorpusCase("RC-QB-019", DOMAIN, (D_U2_S, D_U5_S, _upper("8")), (_result("R001", "R002", W), _result("R001", "R003", W), _result("R002", "R003", W)), (), QbConsistencyState.COMPUTED, Fraction(1, 1), _meta(3, 3, 3, 3, 3, 3, 0, 3, 0, 0, 0, 0, True)),
    CorpusCase("RC-QB-020", DOMAIN, (D_U2_S, D_L5_S, D_U1_M), (_result("R001", "R002", C), _result("R001", "R003", O, outside=(OutsideApplicabilityReason.UNIT_MISMATCH,)), _result("R002", "R003", O, outside=(OutsideApplicabilityReason.UNIT_MISMATCH,))), ("R001", "R002"), QbConsistencyState.COMPUTED, Fraction(1, 3), _meta(3, 3, 2, 3, 3, 1, 1, 0, 0, 2, 0, 2, True)),
    CorpusCase("RC-QB-021", DOMAIN, (D_U2_S, D_L5_S, D_NONE), (_result("R001", "R002", C),), ("R001", "R002"), QbConsistencyState.COMPUTED, Fraction(1, 3), _meta(3, 2, 2, 3, 1, 1, 1, 0, 0, 0, 0, 2, True)),
    CorpusCase("RC-QB-022", DOMAIN, (D_U2_S, D_L5_S, D_UNRES_C_ONE), (_result("R001", "R002", C), _result("R001", "R003", U, unresolved=UC), _result("R002", "R003", U, unresolved=UC)), ("R001", "R002"), QbConsistencyState.UNKNOWN, None, _meta(3, 3, 2, 3, 3, 1, 1, 0, 2, 0, 0, 2, False)),
    CorpusCase("RC-QB-023", DOMAIN, (D_U5_S, D_L2_S, D_UNRES_C_ONE), (_result("R001", "R002", W), _result("R001", "R003", U, unresolved=UC), _result("R002", "R003", U, unresolved=UC)), (), QbConsistencyState.UNKNOWN, None, _meta(3, 3, 2, 3, 3, 1, 0, 1, 2, 0, 0, 0, False)),
    CorpusCase("RC-QB-024", END_TO_END, (E_X95, E_NONE_1), (), (), QbConsistencyState.UNKNOWN, None, _meta(2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, False)),
    CorpusCase("RC-QB-025", END_TO_END, (), (), (), QbConsistencyState.NOT_APPLICABLE, None, _meta(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True)),
    CorpusCase("RC-QB-026", END_TO_END, (E_NONE_1,), (), (), QbConsistencyState.NOT_APPLICABLE, None, _meta(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True)),
    CorpusCase("RC-QB-027", END_TO_END, (E_NONE_1, E_NONE_2), (), (), QbConsistencyState.NOT_APPLICABLE, None, _meta(2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, True)),
)


def _observation_from_expected(expected: ObservationExpected):
    scalar_refs = (expected.scalar_id,)
    return QuantitativeConstraintObservation(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        metric=(
            None
            if expected.metric_id is None
            else TextComponent((expected.metric_id,))
        ),
        comparator=ComparatorComponent(
            expected.comparator,
            expected.inclusivity,
            scalar_refs,
        ),
        value=NumericValueComponent(expected.value, scalar_refs),
        unit=(
            None
            if expected.unit is None
            else UnitComponent(expected.unit, scalar_refs)
        ),
        context=(
            None
            if expected.context_id is None
            else TextComponent((expected.context_id,))
        ),
        unresolved_components=expected.unresolved,
        evidence_refs=expected.evidence_ids,
    )


def _domain_record(
    requirement_id: str,
    source_line: int,
    expected: InputExpected,
) -> RequirementAssessmentRecord:
    requirement = Requirement(requirement_id, source_line, expected.text)
    extraction = BaselineFeatureExtractor().extract(requirement)
    quantitative = FeatureDetectionOutcome(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        observations=tuple(
            _observation_from_expected(item) for item in expected.observations
        ),
        processing_status=expected.processing,
        diagnostics=(),
    )
    evidence = tuple(
        Evidence(
            item.evidence_id,
            requirement_id,
            FeatureId.QUANTITATIVE_CONSTRAINT,
            item.text,
            item.start,
            item.end,
            item.rule_id,
        )
        for item in expected.evidence
    )
    extraction = replace(
        extraction,
        features=replace(extraction.features, quantitative_constraints=quantitative),
        evidence=tuple(
            item
            for item in extraction.evidence
            if item.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT
        )
        + evidence,
    )
    return RequirementQualityAssessor().assess_record(extraction)


def _run_case(case: CorpusCase, tmp_path):
    if case.boundary == DOMAIN:
        records = tuple(
            _domain_record(f"R{index:03d}", index, item)
            for index, item in enumerate(case.inputs, start=1)
        )
    else:
        source = tmp_path / f"{case.case_id}.txt"
        source.write_text(
            "" if not case.inputs else "\n".join(item.text for item in case.inputs) + "\n",
            encoding="utf-8",
        )
        requirements = RequirementReader().read(source)
        extractor = BaselineFeatureExtractor()
        assessor = RequirementQualityAssessor()
        records = tuple(
            assessor.assess_record(extractor.extract(requirement))
            for requirement in requirements
        )
    return SpecificationAssessmentService().assess(records)


def _component_text(manifest, refs):
    if not refs:
        return None
    ref, = refs
    evidence, = (item for item in manifest.evidence if item.ref == ref)
    return evidence.text


def _expected_cross_evidence(result, projection):
    refs = []
    for observation_ref in result.observation_refs:
        requirement = next(
            item
            for item in projection.requirements
            if item.requirement_id == observation_ref.requirement_id
        )
        observation = requirement.observations[observation_ref.observation_index]
        evidence = {
            item.ref: item
            for item in requirement.evidence
        }
        refs.extend(
            sorted(
                observation.evidence_refs,
                key=lambda ref: (
                    evidence[ref].start_offset,
                    evidence[ref].end_offset,
                    ref.evidence_id,
                ),
            )
        )
    return tuple(refs)


def _observability_tuple(observability):
    return (
        observability.total_requirement_count,
        observability.requirements_with_observations_count,
        observability.requirements_in_applicable_comparisons_count,
        observability.total_requirement_pair_count,
        observability.total_observation_pair_count,
        observability.confirmed_conflict_count,
        observability.compatible_count,
        observability.unresolved_count,
        observability.outside_applicability_count,
        observability.applicable_comparison_count,
        observability.global_unresolved_extraction_count,
        observability.qb_material_unresolved_count,
        observability.qb_non_material_diagnostic_count,
        observability.observed_rconf_count,
        observability.rconf_complete,
    )


@pytest.mark.parametrize("case", CASES, ids=lambda item: item.case_id)
def test_binding_reference_corpus(case: CorpusCase, tmp_path) -> None:
    result = _run_case(case, tmp_path)
    assessment = result.specification_assessment.qb_consistency

    assert [item.extraction_result.requirement.id for item in result.records] == [
        f"R{index:03d}" for index in range(1, len(case.inputs) + 1)
    ]
    assert [item.extraction_result.requirement.source_line for item in result.records] == list(
        range(1, len(case.inputs) + 1)
    )

    for source_order, (expected_input, manifest, record) in enumerate(
        zip(case.inputs, result.projection.requirements, result.records, strict=True)
    ):
        assert manifest.source_order == source_order
        assert manifest.text == expected_input.text
        assert manifest.processing_status is expected_input.processing
        assert len(manifest.observations) == len(expected_input.observations)
        assert [
            (
                item.ref.evidence_id,
                item.rule_id,
                item.text,
                item.start_offset,
                item.end_offset,
            )
            for item in manifest.evidence
        ] == [
            (item.evidence_id, item.rule_id, item.text, item.start, item.end)
            for item in expected_input.evidence
        ]
        assert [
            (
                item.code,
                item.rule_id,
                item.candidate_text,
                item.start_offset,
                item.end_offset,
            )
            for item in manifest.diagnostics
        ] == [
            (
                "QUANT_UNRESOLVED_NUMERIC_CANDIDATE",
                "QUANT-001",
                item.text,
                item.start,
                item.end,
            )
            for item in expected_input.diagnostics
        ]
        outcome = record.extraction_result.features.quantitative_constraints
        assert outcome.status is (
            DetectionStatus.DETECTED
            if expected_input.observations
            else DetectionStatus.UNRESOLVED
            if expected_input.processing is DetectionProcessingStatus.INCOMPLETE
            else DetectionStatus.NOT_DETECTED
        )

        for expected_observation, observation in zip(
            expected_input.observations,
            manifest.observations,
            strict=True,
        ):
            assert _component_text(manifest, observation.metric_evidence_refs) == (
                None
                if expected_observation.metric_id is None
                else next(
                    item.text
                    for item in expected_input.evidence
                    if item.evidence_id == expected_observation.metric_id
                )
            )
            assert _component_text(manifest, observation.context_evidence_refs) == (
                None
                if expected_observation.context_id is None
                else next(
                    item.text
                    for item in expected_input.evidence
                    if item.evidence_id == expected_observation.context_id
                )
            )
            assert observation.comparator is expected_observation.comparator
            assert observation.inclusivity is expected_observation.inclusivity
            assert observation.value == expected_observation.value
            assert observation.unit is expected_observation.unit
            assert observation.unresolved_components == expected_observation.unresolved
            assert tuple(item.evidence_id for item in observation.evidence_refs) == (
                expected_observation.evidence_ids
            )

    assert len(result.cross_results) == len(case.results)
    for actual, expected in zip(result.cross_results, case.results, strict=True):
        assert tuple(item.requirement_id for item in actual.participants) == (
            expected.participants
        )
        assert tuple(item.observation_index for item in actual.observation_refs) == (
            expected.observation_indexes
        )
        assert actual.state is expected.state
        assert actual.unresolved_reasons == expected.unresolved
        assert actual.outside_reasons == expected.outside
        assert actual.evidence_refs == _expected_cross_evidence(actual, result.projection)
        assert {item.requirement_id for item in actual.evidence_refs} == set(
            expected.participants
        )
        for evidence_ref in actual.evidence_refs:
            evidence = result.resolver.resolve_evidence(
                evidence_ref,
                snapshot_id=result.snapshot_id,
            )
            owner = result.resolver.resolve_requirement(evidence_ref.requirement_id)
            assert owner.text[evidence.start_offset:evidence.end_offset] == evidence.text
        if expected.state is C:
            assert actual.conflict_class is ConflictClass.LOGICAL_CONFLICT
            assert actual.conflict_subtype is (
                BoundedConflictSubtype.DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY
            )
        else:
            assert actual.conflict_class is None
            assert actual.conflict_subtype is None
        if expected.state in {C, W}:
            assert actual.comparison_key is not None
            assert actual.comparison_key.normalized_metric == (
                actual.operands.left.normalized_metric
            )
            assert actual.comparison_key.normalized_context == (
                actual.operands.left.normalized_context
            )
            assert actual.comparison_key.unit is actual.operands.left.unit
        else:
            assert actual.comparison_key is None
        assert actual.non_claim_keys == (BoundedNonClaimKey.NC_QB_BASE,)

        left_manifest = next(
            item
            for item in result.projection.requirements
            if item.requirement_id == expected.participants[0]
        )
        right_manifest = next(
            item
            for item in result.projection.requirements
            if item.requirement_id == expected.participants[1]
        )
        left_expected = case.inputs[int(expected.participants[0][1:]) - 1].observations[
            expected.observation_indexes[0]
        ]
        right_expected = case.inputs[int(expected.participants[1][1:]) - 1].observations[
            expected.observation_indexes[1]
        ]
        expected_operands = (
            (left_manifest, left_expected, actual.operands.left),
            (right_manifest, right_expected, actual.operands.right),
        )
        for manifest, expected_observation, operand in expected_operands:
            metric_text = _component_text(manifest, manifest.observations[operand.observation_ref.observation_index].metric_evidence_refs)
            context_text = _component_text(manifest, manifest.observations[operand.observation_ref.observation_index].context_evidence_refs)
            assert operand.normalized_metric == (
                None if metric_text is None else normalize_qb_identity_text(metric_text)
            )
            assert operand.normalized_context == (
                None if context_text is None else normalize_qb_identity_text(context_text)
            )
            assert operand.comparator is expected_observation.comparator
            assert operand.inclusivity is expected_observation.inclusivity
            assert operand.value == expected_observation.value
            assert operand.unit is expected_observation.unit

    assert assessment.rconf_participant_ids == case.rconf
    assert assessment.rconf_complete is bool(case.metadata[-1])
    assert assessment.state is case.aggregate_state
    assert assessment.value == case.aggregate_value
    if case.aggregate_value is None:
        assert assessment.value is None
    else:
        assert isinstance(assessment.value, Fraction)
    assert _observability_tuple(assessment.observability) == case.metadata
    assert assessment.non_claim_keys == (BoundedNonClaimKey.NC_QB_BASE,)
    assert tuple(item.result_id for item in result.cross_results) == assessment.cross_result_ids

    assert tuple(
        item.diagnostic_ref for item in result.materiality.audit_records
    ) == assessment.materiality_diagnostic_refs
    assert [item.requirement_source_order for item in result.materiality.audit_records] == list(
        range(len(result.materiality.audit_records))
    )
    if case.metadata[12]:
        assert all(
            item.disposition is QbMaterialityDisposition.QB_NON_MATERIAL
            and item.gate_outcomes.all_passed
            and item.matched_context_evidence_ref is not None
            and item.matched_allowlist_contract is not None
            for item in result.materiality.audit_records
        )
    elif case.metadata[11]:
        assert all(
            item.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED
            and not item.gate_outcomes.all_passed
            for item in result.materiality.audit_records
        )


FUTURE_TARGET = CorpusCase(
    "QB-ER-D013-IMP-11",
    END_TO_END,
    (
        E_U2_S_C,
        _input(
            "Час відгуку не нижче 5 с при 500 одночасних користувачах",
            (
                _e("QUANT-LB-METRIC-001:E001", "Час відгуку", 0, 11, "QUANT-LB-METRIC-001"),
                _e("QUANT-UK-001:E001", "не нижче 5 с", 12, 24, "QUANT-UK-001"),
                _e("QUANT-LB-CONTEXT-001:E001", STD_CONTEXT, 25, 56, "QUANT-LB-CONTEXT-001"),
            ),
            (
                _obs(
                    "QUANT-LB-METRIC-001:E001",
                    "QUANT-UK-001:E001",
                    "QUANT-LB-CONTEXT-001:E001",
                    ComparatorLabel.GREATER_THAN_OR_EQUAL,
                    "5",
                ),
            ),
            processing=DetectionProcessingStatus.INCOMPLETE,
            diagnostics=(DiagnosticExpected("500", 29, 32),),
        ),
    ),
    (_result("R001", "R002", C),),
    ("R001", "R002"),
    QbConsistencyState.COMPUTED,
    Fraction(0, 1),
    _meta(2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 2, 2, True, material=0, non_material=2),
)


class _PreBridgeQuantitativeDetector:
    """Test-only frozen view of R002 before the approved LB-M-C0 enrichment."""

    def detect(self, requirement: Requirement):
        from requirements_quality_assessment.detectors.quantitative import (
            QuantitativeBaselineDetector,
        )

        outcome, evidence = QuantitativeBaselineDetector().detect(requirement)
        observations = tuple(
            replace(
                observation,
                metric=None,
                context=None,
                evidence_refs=tuple(
                    ref
                    for ref in observation.evidence_refs
                    if not ref.startswith("QUANT-LB-")
                ),
            )
            for observation in outcome.observations
        )
        return (
            replace(outcome, observations=observations),
            tuple(
                item
                for item in evidence
                if item.rule_id
                not in {QUANT_LB_METRIC_RULE_ID, QUANT_LB_CONTEXT_RULE_ID}
            ),
        )


def _future_target_result(tmp_path):
    return _run_case(FUTURE_TARGET, tmp_path)


def test_exact_future_target_end_to_end_and_reporting(tmp_path) -> None:
    result = _future_target_result(tmp_path)
    assessment = result.specification_assessment.qb_consistency
    upper, lower = result.projection.requirements
    conflict, = result.cross_results

    assert [item.text for item in (upper, lower)] == [
        item.text for item in FUTURE_TARGET.inputs
    ]
    assert [len(item.observations) for item in (upper, lower)] == [1, 1]
    assert [item.processing_status for item in (upper, lower)] == [
        DetectionProcessingStatus.INCOMPLETE,
        DetectionProcessingStatus.INCOMPLETE,
    ]
    assert [
        [(item.text, item.start_offset, item.end_offset) for item in manifest.evidence]
        for manifest in (upper, lower)
    ] == [
        [(item.text, item.start, item.end) for item in expected.evidence]
        for expected in FUTURE_TARGET.inputs
    ]
    assert [
        [(item.candidate_text, item.start_offset, item.end_offset) for item in manifest.diagnostics]
        for manifest in (upper, lower)
    ] == [[("500", 22, 25)], [("500", 29, 32)]]
    assert conflict.state is C
    assert tuple(item.requirement_id for item in conflict.participants) == ("R001", "R002")
    assert conflict.conflict_class is ConflictClass.LOGICAL_CONFLICT
    assert conflict.conflict_subtype is (
        BoundedConflictSubtype.DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY
    )
    assert len(result.cross_results) == 1
    assert conflict.operands.left.normalized_metric == "час відгуку"
    assert conflict.operands.right.normalized_metric == "час відгуку"
    assert conflict.operands.left.normalized_context == STD_CONTEXT
    assert conflict.operands.right.normalized_context == STD_CONTEXT
    assert conflict.operands.left.unit is UnitLabel.SECOND
    assert conflict.operands.right.unit is UnitLabel.SECOND
    assert conflict.operands.left.value == Decimal("2")
    assert conflict.operands.right.value == Decimal("5")
    assert assessment.rconf_participant_ids == ("R001", "R002")
    assert assessment.rconf_complete is True
    assert assessment.state is QbConsistencyState.COMPUTED
    assert assessment.value == Fraction(0, 1)
    assert type(assessment.value) is Fraction
    assert _observability_tuple(assessment.observability) == FUTURE_TARGET.metadata
    assert [item.disposition for item in result.materiality.audit_records] == [
        QbMaterialityDisposition.QB_NON_MATERIAL,
        QbMaterialityDisposition.QB_NON_MATERIAL,
    ]
    assert all(item.gate_outcomes.all_passed for item in result.materiality.audit_records)
    assert [
        (
            item.requirement_id,
            item.requirement_source_order,
            item.diagnostic_code,
            item.diagnostic_rule_id,
            item.candidate_text,
            item.diagnostic_start_offset,
            item.diagnostic_end_offset,
            item.matched_context_evidence_ref.evidence_id,
            item.matched_allowlist_contract.contract_id,
            item.matched_allowlist_contract.version,
        )
        for item in result.materiality.audit_records
    ] == [
        (
            "R001",
            0,
            "QUANT_UNRESOLVED_NUMERIC_CANDIDATE",
            "QUANT-001",
            "500",
            22,
            25,
            "QUANT-CONTEXT-001:E001",
            "QUANT-CONTEXT-001",
            "1",
        ),
        (
            "R002",
            1,
            "QUANT_UNRESOLVED_NUMERIC_CANDIDATE",
            "QUANT-001",
            "500",
            29,
            32,
            "QUANT-LB-CONTEXT-001:E001",
            "QUANT-LB-CONTEXT-001",
            "1",
        ),
    ]
    assert conflict.evidence_refs == _expected_cross_evidence(conflict, result.projection)
    assert [item.requirement_id for item in conflict.evidence_refs] == [
        "R001", "R001", "R001", "R002", "R002", "R002"
    ]
    assert not conflict.diagnostic_refs
    for ref in conflict.evidence_refs:
        evidence = result.resolver.resolve_evidence(ref, snapshot_id=result.snapshot_id)
        requirement = result.resolver.resolve_requirement(ref.requirement_id)
        assert requirement.text[evidence.start_offset:evidence.end_offset] == evidence.text

    audit = ConsoleReporter().render_assessment(result)
    user = UserConsoleReporter().render_assessment(result)
    for token in (
        "CONFIRMED_CONFLICT",
        "state: COMPUTED",
        "value: 0",
        "observed_R_conf: R001, R002",
        "rconf_complete: yes",
        "R001: INCOMPLETE",
        "R002: INCOMPLETE",
        "QB-CONSISTENCY-001 / 1",
        "QB-NON-CLAIMS-001 / 1",
        "NC-QB-BASE",
    ):
        assert token in audit
    assert audit.count("disposition: QB_NON_MATERIAL") == 2
    assert audit.count("    - ", audit.index("Bounded non-claims:")) == 14
    for expected in FUTURE_TARGET.inputs:
        for evidence in expected.evidence:
            assert f"text: {evidence.text}" in audit
            assert f"range: [{evidence.start},{evidence.end})" in audit
    for token in (
        "[CONFIRMED_CONFLICT] R001 ↔ R002",
        "R001: «Час відгуку»",
        "R001: «≤ 2 с»",
        f"R001: «{STD_CONTEXT}»",
        "R002: «Час відгуку»",
        "R002: «не нижче 5 с»",
        f"R002: «{STD_CONTEXT}»",
        "Узгодженість у межах QB-v0.1: 0",
        "серйозність, ризик",
        "коригувальна дія",
        "якість програмного продукту",
        "не означає універсальної узгодженості",
    ):
        assert token in user


def test_exact_future_target_preserves_frozen_local_semantics(tmp_path) -> None:
    result = _future_target_result(tmp_path)
    lower_record = result.records[1]
    lower_requirement = lower_record.extraction_result.requirement
    pre_bridge_extraction = BaselineFeatureExtractor(
        quantitative_detector=_PreBridgeQuantitativeDetector()
    ).extract(lower_requirement)
    pre_bridge_record = RequirementQualityAssessor().assess_record(
        pre_bridge_extraction
    )

    enriched_outcome = lower_record.extraction_result.features.quantitative_constraints
    pre_bridge_outcome = pre_bridge_extraction.features.quantitative_constraints
    assert len(enriched_outcome.observations) == len(pre_bridge_outcome.observations) == 1
    assert enriched_outcome.processing_status is pre_bridge_outcome.processing_status is (
        DetectionProcessingStatus.INCOMPLETE
    )
    assert enriched_outcome.diagnostics == pre_bridge_outcome.diagnostics
    enriched_scalar = enriched_outcome.observations[0]
    pre_bridge_scalar = pre_bridge_outcome.observations[0]
    assert (
        enriched_scalar.comparator,
        enriched_scalar.value,
        enriched_scalar.unit,
    ) == (
        pre_bridge_scalar.comparator,
        pre_bridge_scalar.value,
        pre_bridge_scalar.unit,
    )
    assert enriched_scalar.metric is not None and enriched_scalar.context is not None
    assert pre_bridge_scalar.metric is None and pre_bridge_scalar.context is None
    assert lower_record.quality_profile == pre_bridge_record.quality_profile
    assert lower_record.trace == pre_bridge_record.trace
    assert (
        lower_record.quality_profile.completeness.value,
        lower_record.quality_profile.verifiability.value,
        lower_record.quality_profile.unambiguity.value,
    ) == (
        pre_bridge_record.quality_profile.completeness.value,
        pre_bridge_record.quality_profile.verifiability.value,
        pre_bridge_record.quality_profile.unambiguity.value,
    )

    aggregator = SpecificationQualityAggregator()
    enriched_profile = aggregator.aggregate(
        tuple(item.quality_profile for item in result.records)
    )
    pre_bridge_profile = aggregator.aggregate(
        (result.records[0].quality_profile, pre_bridge_record.quality_profile)
    )
    assert enriched_profile == pre_bridge_profile
    assert result.specification_assessment.quality_profile == enriched_profile
    assert {
        item.aggregation_rule_id
        for item in (
            enriched_profile.completeness,
            enriched_profile.verifiability,
            enriched_profile.unambiguity,
        )
    } == {"AGG-MVP-001"}


@pytest.mark.parametrize("case_id", ("RC-QB-003", "RC-QB-005", "RC-QB-018"))
def test_reference_corpus_identity_and_order_are_deterministic(case_id, tmp_path) -> None:
    case = next(item for item in CASES if item.case_id == case_id)
    first = _run_case(case, tmp_path)
    second = _run_case(case, tmp_path)
    assert first.snapshot_id == second.snapshot_id
    assert first.cross_results == second.cross_results
    assert first.materiality == second.materiality
    assert first.specification_assessment == second.specification_assessment


def test_future_target_reports_and_provenance_are_deterministic(tmp_path) -> None:
    first = _future_target_result(tmp_path)
    second = _future_target_result(tmp_path)
    assert first.snapshot_id == second.snapshot_id
    assert tuple(item.result_id for item in first.cross_results) == tuple(
        item.result_id for item in second.cross_results
    )
    assert first.cross_results == second.cross_results
    assert first.materiality == second.materiality
    assert first.specification_assessment == second.specification_assessment
    assert ConsoleReporter().render_assessment(first) == ConsoleReporter().render_assessment(
        second
    )
    assert UserConsoleReporter().render_assessment(
        first
    ) == UserConsoleReporter().render_assessment(second)


def test_corpus_inventory_and_required_state_coverage() -> None:
    assert [item.case_id for item in CASES] == [
        f"RC-QB-{index:03d}" for index in range(1, 28)
    ]
    assert sum(item.boundary == DOMAIN for item in CASES) == 17
    assert sum(item.boundary == END_TO_END for item in CASES) == 10
    assert {
        result.state for case in CASES for result in case.results
    } == set(CrossResultState)
    assert {item.aggregate_state for item in CASES} == set(QbConsistencyState)
    assert {
        item.aggregate_value
        for item in CASES
        if item.aggregate_state is QbConsistencyState.COMPUTED
    } >= {Fraction(0, 1), Fraction(1, 1), Fraction(1, 3)}
    assert all(
        item.aggregate_value is None
        for item in CASES
        if item.aggregate_state
        in {QbConsistencyState.UNKNOWN, QbConsistencyState.NOT_APPLICABLE}
    )

"""Binding QUANT-CONTEXT-001 behavior from model-spec §7.14.6.8."""

from dataclasses import dataclass
from decimal import Decimal

import pytest

from requirements_quality_assessment.detectors import (
    AcceptanceCriterionBaselineDetector,
    ConditionContextBaselineDetector,
    QuantitativeBaselineDetector,
)
from requirements_quality_assessment.detectors.expected_result import (
    RULE_ID as RESULT_RULE_ID,
)
from requirements_quality_assessment.detectors.quantitative import (
    QUANT_CONTEXT_RULE_ID,
    QUANT_METRIC_RULE_ID,
    QUANT_RULE_ID,
    QUANT_UK_RULE_ID,
    UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorLabel,
    DetectionProcessingStatus,
    DetectionStatus,
    Evidence,
    FeatureDetectionOutcome,
    FeatureId,
    FeatureObservation,
    Requirement,
    TextComponent,
    UnitLabel,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor


SOURCE_TEXT = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
CONTEXT_TEXT = "при 500 одночасних користувачах"


def detect(text: str):
    requirement = Requirement("R073", 7, text)
    outcome, evidence = QuantitativeBaselineDetector().detect(requirement)
    return requirement, outcome, evidence


def test_exact_source_positive_enriches_the_existing_observation() -> None:
    requirement, outcome, evidence = detect(SOURCE_TEXT)

    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert len(outcome.observations) == 1
    assert [
        (
            source.evidence_id,
            source.rule_id,
            source.text,
            source.start_offset,
            source.end_offset,
            source.feature_id,
        )
        for source in evidence
    ] == [
        (
            "QUANT-METRIC-001:E001",
            QUANT_METRIC_RULE_ID,
            "Час відгуку",
            0,
            11,
            FeatureId.QUANTITATIVE_CONSTRAINT,
        ),
        (
            "QUANT-001:E001",
            QUANT_RULE_ID,
            "≤ 2 с",
            12,
            17,
            FeatureId.QUANTITATIVE_CONSTRAINT,
        ),
        (
            "QUANT-CONTEXT-001:E001",
            QUANT_CONTEXT_RULE_ID,
            CONTEXT_TEXT,
            18,
            49,
            FeatureId.QUANTITATIVE_CONSTRAINT,
        ),
    ]
    assert all(
        requirement.text[source.start_offset:source.end_offset] == source.text
        for source in evidence
    )

    observation = outcome.observations[0]
    assert observation.metric == TextComponent(("QUANT-METRIC-001:E001",))
    assert observation.comparator.label is ComparatorLabel.LESS_THAN_OR_EQUAL
    assert observation.comparator.inclusivity is BoundaryInclusivity.INCLUSIVE
    assert observation.comparator.evidence_refs == ("QUANT-001:E001",)
    assert observation.value.decimal_value == Decimal("2")
    assert observation.value.evidence_refs == ("QUANT-001:E001",)
    assert observation.unit.label is UnitLabel.SECOND
    assert observation.unit.evidence_refs == ("QUANT-001:E001",)
    assert observation.context == TextComponent(("QUANT-CONTEXT-001:E001",))
    assert observation.unresolved_components == ()
    assert observation.evidence_refs == (
        "QUANT-METRIC-001:E001",
        "QUANT-001:E001",
        "QUANT-CONTEXT-001:E001",
    )

    assert [
        (
            item.code,
            item.rule_id,
            item.candidate_span.text,
            item.candidate_span.start_offset,
            item.candidate_span.end_offset,
        )
        for item in outcome.diagnostics
    ] == [
        (UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE, QUANT_RULE_ID, "500", 22, 25)
    ]


@pytest.mark.parametrize(
    ("scalar", "value", "unit"),
    [
        ("≤ 3 с", Decimal("3"), UnitLabel.SECOND),
        ("≤ 2,5 с", Decimal("2.5"), UnitLabel.SECOND),
        ("≤ 2 с", Decimal("2"), UnitLabel.SECOND),
        ("≤ 2 секунд", Decimal("2"), UnitLabel.SECOND),
        ("≤ 2 хв", Decimal("2"), UnitLabel.MINUTE),
        ("≤ 2 хвилин", Decimal("2"), UnitLabel.MINUTE),
    ],
)
def test_approved_primary_scalar_variants_compose_with_context(
    scalar: str,
    value: Decimal,
    unit: UnitLabel,
) -> None:
    _, outcome, evidence = detect(f"Час відгуку {scalar} {CONTEXT_TEXT}")

    observation, = outcome.observations
    assert observation.value.decimal_value == value
    assert observation.unit.label is unit
    assert observation.context == TextComponent(("QUANT-CONTEXT-001:E001",))
    assert [source.rule_id for source in evidence] == [
        QUANT_METRIC_RULE_ID,
        QUANT_RULE_ID,
        QUANT_CONTEXT_RULE_ID,
    ]
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.candidate_span.text for item in outcome.diagnostics] == ["500"]


@pytest.mark.parametrize(
    ("text", "evidence_rules", "diagnostic_texts"),
    [
        ("Час відгуку ≤ 2 с при одночасних користувачах",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ()),
        ("Час відгуку ≤ 2 с при 600 одночасних користувачах",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("600",)),
        ("Час відгуку ≤ 2 с при 500",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку ≤ 2 с при 500 одночасних клієнтах",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку ≤ 2 с за 500 одночасних користувачів",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку ≤ 2 с При 500 одночасних користувачах",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку ≤ 2 с  при 500 одночасних користувачах",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку ≤ 2 с при 500  одночасних користувачах",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку ≤ 2 с при\t500 одночасних користувачах",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку ≤ 2 с при 500 одночасних користувачах.",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку ≤ 2 с. при 500 одночасних користувачах",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку та Час відгуку ≤ 2 с при 500 одночасних користувачах",
         (QUANT_RULE_ID,), ("500",)),
        ("Час відгуку ≤ 2 с та ≤ 3 с при 500 одночасних користувачах",
         (QUANT_RULE_ID, QUANT_RULE_ID), ("500",)),
        ("Час відгуку ≤ 2 с та не більше 3 с при 500 одночасних користувачах",
         (QUANT_RULE_ID, QUANT_UK_RULE_ID), ("500",)),
        (f"Час відгуку ≤ 2 с {CONTEXT_TEXT} при піковому навантаженні",
         (QUANT_METRIC_RULE_ID, QUANT_RULE_ID), ("500",)),
        (f"Час відгуку не більше 2 с {CONTEXT_TEXT}",
         (QUANT_UK_RULE_ID,), ("500",)),
        (f"Час відгуку ≤ 2.5 с {CONTEXT_TEXT}", (), ("500",)),
        ("TLS 1.3", (), ()),
        ("OAuth 2.0/OIDC", (), ()),
    ],
)
def test_c0_negative_cases_preserve_baseline_behavior(
    text: str,
    evidence_rules: tuple[str, ...],
    diagnostic_texts: tuple[str, ...],
) -> None:
    _, outcome, evidence = detect(text)

    assert [source.rule_id for source in evidence] == list(evidence_rules)
    assert all(source.rule_id != QUANT_CONTEXT_RULE_ID for source in evidence)
    assert all(observation.context is None for observation in outcome.observations)
    assert [
        item.candidate_span.text for item in outcome.diagnostics
    ] == list(diagnostic_texts)


@pytest.mark.parametrize("population", ["500,5", "500.0", "+500", "1 000", "5e2"])
def test_unsupported_population_numeric_forms_do_not_inherit_scalar_grammar(
    population: str,
) -> None:
    text = f"Час відгуку ≤ 2 с при {population} одночасних користувачах"
    _, outcome, evidence = detect(text)

    assert [source.rule_id for source in evidence] == [
        QUANT_METRIC_RULE_ID,
        QUANT_RULE_ID,
    ]
    assert outcome.observations[0].context is None
    assert all(source.rule_id != QUANT_CONTEXT_RULE_ID for source in evidence)


def test_same_span_condition_and_quantitative_context_evidence_stay_distinct() -> None:
    requirement = Requirement("R073", 7, SOURCE_TEXT)
    condition_outcome, condition_evidence = ConditionContextBaselineDetector().detect(
        requirement
    )
    quantitative_outcome, quantitative_evidence = QuantitativeBaselineDetector().detect(
        requirement
    )

    condition_source, = condition_evidence
    context_source = next(
        source
        for source in quantitative_evidence
        if source.rule_id == QUANT_CONTEXT_RULE_ID
    )
    assert condition_outcome.status is DetectionStatus.DETECTED
    assert (condition_source.evidence_id, condition_source.feature_id) == (
        "COND-UK-001:E001",
        FeatureId.CONDITION_CONTEXT,
    )
    assert (context_source.evidence_id, context_source.feature_id) == (
        "QUANT-CONTEXT-001:E001",
        FeatureId.QUANTITATIVE_CONSTRAINT,
    )
    assert (
        condition_source.text,
        condition_source.start_offset,
        condition_source.end_offset,
    ) == (CONTEXT_TEXT, 18, 49)
    assert (
        context_source.text,
        context_source.start_offset,
        context_source.end_offset,
    ) == (CONTEXT_TEXT, 18, 49)
    assert quantitative_outcome.observations[0].context == TextComponent(
        (context_source.evidence_id,)
    )


@dataclass
class _FakeDetector:
    result: tuple[FeatureDetectionOutcome, tuple[Evidence, ...]]

    def detect(self, requirement: Requirement):
        return self.result


def test_acceptance_uses_only_scalar_evidence_for_containment() -> None:
    requirement = Requirement("R073", 7, SOURCE_TEXT)
    result_source = Evidence(
        "RESULT-UK-001:E001",
        requirement.id,
        FeatureId.EXPECTED_RESULT,
        requirement.text[:17],
        0,
        17,
        RESULT_RULE_ID,
    )
    expected = FeatureDetectionOutcome(
        FeatureId.EXPECTED_RESULT,
        (FeatureObservation(FeatureId.EXPECTED_RESULT, (result_source.evidence_id,)),),
        DetectionProcessingStatus.COMPLETE,
        (),
    )
    detector = AcceptanceCriterionBaselineDetector(
        expected_result_detector=_FakeDetector((expected, (result_source,))),
        quantitative_detector=QuantitativeBaselineDetector(),
    )

    outcome, evidence = detector.detect(requirement)

    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert len(outcome.observations) == len(evidence) == 1
    assert (evidence[0].text, evidence[0].start_offset, evidence[0].end_offset) == (
        requirement.text[:17],
        0,
        17,
    )


def test_public_extractor_preserves_integrity_and_global_evidence_order() -> None:
    requirement = Requirement("R073", 7, SOURCE_TEXT)
    result = BaselineFeatureExtractor().extract(requirement)
    observation, = result.features.quantitative_constraints.observations
    by_id = {source.evidence_id: source for source in result.evidence}

    assert len(observation.evidence_refs) == 3
    assert observation.evidence_refs == (
        "QUANT-METRIC-001:E001",
        "QUANT-001:E001",
        "QUANT-CONTEXT-001:E001",
    )
    assert len(result.features.quantitative_constraints.observations) == 1
    assert len(by_id) == len(result.evidence)
    assert set(observation.evidence_refs) <= by_id.keys()
    assert all(
        by_id[reference].feature_id is FeatureId.QUANTITATIVE_CONSTRAINT
        for reference in observation.evidence_refs
    )
    assert all(
        requirement.text[source.start_offset:source.end_offset] == source.text
        for source in result.evidence
    )
    assert [source.evidence_id for source in result.evidence] == [
        "QUANT-METRIC-001:E001",
        "QUANT-001:E001",
        "COND-UK-001:E001",
        "QUANT-CONTEXT-001:E001",
    ]

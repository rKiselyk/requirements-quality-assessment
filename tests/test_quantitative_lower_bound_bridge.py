"""Issue #116 IMP-02 exact atomic LB-M-C0 extraction bridge."""

from dataclasses import replace
from decimal import Decimal

import pytest

from requirements_quality_assessment.aggregator import SpecificationQualityAggregator
from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.detectors.quantitative import (
    QUANT_CONTEXT_RULE_ID,
    QUANT_LB_CONTEXT_RULE_ID,
    QUANT_LB_METRIC_RULE_ID,
    QUANT_METRIC_RULE_ID,
    QUANT_RULE_ID,
    QUANT_UK_RULE_ID,
    UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
    QuantitativeBaselineDetector,
)
from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorLabel,
    DetectionProcessingStatus,
    DetectionStatus,
    FeatureId,
    Requirement,
    TextComponent,
    UnitLabel,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor


SOURCE_TEXT = "Час відгуку не нижче 5 с при 500 одночасних користувачах"
LB_RULE_IDS = frozenset({QUANT_LB_METRIC_RULE_ID, QUANT_LB_CONTEXT_RULE_ID})


def detect(text: str):
    requirement = Requirement("R002", 2, text)
    outcome, evidence = QuantitativeBaselineDetector().detect(requirement)
    return requirement, outcome, evidence


def test_exact_envelope_atomically_enriches_the_existing_lower_observation() -> None:
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
            "QUANT-LB-METRIC-001:E001",
            QUANT_LB_METRIC_RULE_ID,
            "Час відгуку",
            0,
            11,
            FeatureId.QUANTITATIVE_CONSTRAINT,
        ),
        (
            "QUANT-UK-001:E001",
            QUANT_UK_RULE_ID,
            "не нижче 5 с",
            12,
            24,
            FeatureId.QUANTITATIVE_CONSTRAINT,
        ),
        (
            "QUANT-LB-CONTEXT-001:E001",
            QUANT_LB_CONTEXT_RULE_ID,
            "при 500 одночасних користувачах",
            25,
            56,
            FeatureId.QUANTITATIVE_CONSTRAINT,
        ),
    ]
    assert all(
        requirement.text[source.start_offset:source.end_offset] == source.text
        for source in evidence
    )

    observation = outcome.observations[0]
    scalar_ref = ("QUANT-UK-001:E001",)
    assert observation.metric == TextComponent(("QUANT-LB-METRIC-001:E001",))
    assert observation.comparator.label is ComparatorLabel.GREATER_THAN_OR_EQUAL
    assert observation.comparator.inclusivity is BoundaryInclusivity.INCLUSIVE
    assert observation.comparator.evidence_refs == scalar_ref
    assert observation.value.decimal_value == Decimal("5")
    assert observation.value.evidence_refs == scalar_ref
    assert observation.unit.label is UnitLabel.SECOND
    assert observation.unit.evidence_refs == scalar_ref
    assert observation.context == TextComponent(("QUANT-LB-CONTEXT-001:E001",))
    assert observation.unresolved_components == ()
    assert observation.evidence_refs == (
        "QUANT-LB-METRIC-001:E001",
        "QUANT-UK-001:E001",
        "QUANT-LB-CONTEXT-001:E001",
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
        (UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE, QUANT_RULE_ID, "500", 29, 32)
    ]


@pytest.mark.parametrize(
    ("value", "unit_surface", "unit"),
    [
        ("5", "с", UnitLabel.SECOND),
        ("2,5", "с", UnitLabel.SECOND),
        ("5", "секунд", UnitLabel.SECOND),
        ("5", "хв", UnitLabel.MINUTE),
        ("2,5", "хвилин", UnitLabel.MINUTE),
    ],
)
def test_all_approved_scalar_surfaces_receive_both_owned_contributions(
    value: str,
    unit_surface: str,
    unit: UnitLabel,
) -> None:
    text = (
        f"Час відгуку не нижче {value} {unit_surface} "
        "при 500 одночасних користувачах"
    )
    _, outcome, evidence = detect(text)

    observation, = outcome.observations
    assert {source.rule_id for source in evidence} & LB_RULE_IDS == LB_RULE_IDS
    assert observation.metric is not None
    assert observation.context is not None
    assert observation.value.decimal_value == Decimal(value.replace(",", "."))
    assert observation.unit.label is unit


@pytest.mark.parametrize(
    "text",
    [
        "Час відгуку не нижче 5 с",
        "Час відповіді не нижче 5 с при 500 одночасних користувачах",
        "час відгуку не нижче 5 с при 500 одночасних користувачах",
        "Час  відгуку не нижче 5 с при 500 одночасних користувачах",
        "Час відгуку Не нижче 5 с при 500 одночасних користувачах",
        "Час відгуку не  нижче 5 с при 500 одночасних користувачах",
        "Час відгуку не нижче 5 с при 600 одночасних користувачах",
        "Час відгуку не нижче 5 с при 500 одночасних клієнтах",
        "Час відгуку не нижче 5 с При 500 одночасних користувачах",
        "Час відгуку не нижче 5 с при 500  одночасних користувачах",
        "Час відгуку не нижче 5 с при\t500 одночасних користувачах",
        "Час відгуку не нижче 5 с при 500 одночасних користувачах.",
        "Час відгуку не нижче 5 с при 500 одночасних користувачах у піку",
        "Час відгуку (не нижче 5 с) при 500 одночасних користувачах",
        "Час відгуку не нижче 5 с та не нижче 6 с при 500 одночасних користувачах",
        "Час відгуку не більше 5 с при 500 одночасних користувачах",
        "Час відгуку ≥ 5 с при 500 одночасних користувачах",
        "Час відгуку не нижче 5.0 с при 500 одночасних користувачах",
        "Час відгуку не нижче 5 % при 500 одночасних користувачах",
    ],
)
def test_excluded_boundaries_preserve_baseline_without_partial_enrichment(
    text: str,
) -> None:
    _, outcome, evidence = detect(text)

    applied_rule_ids = {source.rule_id for source in evidence} & LB_RULE_IDS
    assert applied_rule_ids == set()
    assert all(observation.metric is None for observation in outcome.observations)
    assert all(observation.context is None for observation in outcome.observations)
    assert all(
        not (set(observation.evidence_refs) & {
            "QUANT-LB-METRIC-001:E001",
            "QUANT-LB-CONTEXT-001:E001",
        })
        for observation in outcome.observations
    )


@pytest.mark.parametrize(
    ("text", "enriched"),
    [
        (SOURCE_TEXT, True),
        ("Час відгуку не нижче 2,5 хв при 500 одночасних користувачах", True),
        ("Час відгуку не нижче 5 с", False),
        ("Час відповіді не нижче 5 с при 500 одночасних користувачах", False),
        ("Час відгуку не нижче 5 с при 501 одночасних користувачах", False),
        (f"{SOURCE_TEXT}.", False),
    ],
)
def test_metric_and_context_enrichment_are_observably_atomic(
    text: str,
    enriched: bool,
) -> None:
    _, outcome, evidence = detect(text)

    rules = {source.rule_id for source in evidence}
    assert (QUANT_LB_METRIC_RULE_ID in rules) is enriched
    assert (QUANT_LB_CONTEXT_RULE_ID in rules) is enriched
    for observation in outcome.observations:
        assert (observation.metric is not None) is (observation.context is not None)


class _PreBridgeQuantitativeDetector:
    """Test-only projection of the frozen quantitative result before IMP-02."""

    def detect(self, requirement: Requirement):
        outcome, evidence = QuantitativeBaselineDetector().detect(requirement)
        observations = tuple(
            replace(
                observation,
                metric=None,
                context=None,
                evidence_refs=tuple(
                    reference
                    for reference in observation.evidence_refs
                    if not reference.startswith("QUANT-LB-")
                ),
            )
            for observation in outcome.observations
        )
        return (
            replace(outcome, observations=observations),
            tuple(source for source in evidence if source.rule_id not in LB_RULE_IDS),
        )


def test_frozen_local_quality_trace_and_specification_aggregate_are_unchanged() -> None:
    requirement = Requirement("R002", 2, SOURCE_TEXT)
    enriched = BaselineFeatureExtractor().extract(requirement)
    pre_bridge = BaselineFeatureExtractor(
        quantitative_detector=_PreBridgeQuantitativeDetector()
    ).extract(requirement)

    assert enriched.features.condition_contexts == pre_bridge.features.condition_contexts
    assert enriched.features.expected_results == pre_bridge.features.expected_results
    assert enriched.features.acceptance_criteria == pre_bridge.features.acceptance_criteria
    assert enriched.features.verification_methods == pre_bridge.features.verification_methods
    assert enriched.features.vague_term_occurrences == pre_bridge.features.vague_term_occurrences

    assessor = RequirementQualityAssessor()
    enriched_record = assessor.assess_record(enriched)
    pre_bridge_record = assessor.assess_record(pre_bridge)
    assert enriched_record.quality_profile == pre_bridge_record.quality_profile
    assert enriched_record.trace == pre_bridge_record.trace
    assert (
        enriched_record.quality_profile.completeness.findings,
        enriched_record.quality_profile.verifiability.findings,
        enriched_record.quality_profile.unambiguity.findings,
    ) == (
        pre_bridge_record.quality_profile.completeness.findings,
        pre_bridge_record.quality_profile.verifiability.findings,
        pre_bridge_record.quality_profile.unambiguity.findings,
    )
    aggregator = SpecificationQualityAggregator()
    assert aggregator.aggregate((enriched_record.quality_profile,)) == aggregator.aggregate(
        (pre_bridge_record.quality_profile,)
    )


def test_existing_upper_c0_contract_is_unchanged() -> None:
    text = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
    _, outcome, evidence = detect(text)

    observation, = outcome.observations
    assert [source.rule_id for source in evidence] == [
        QUANT_METRIC_RULE_ID,
        QUANT_RULE_ID,
        QUANT_CONTEXT_RULE_ID,
    ]
    assert observation.metric == TextComponent(("QUANT-METRIC-001:E001",))
    assert observation.context == TextComponent(("QUANT-CONTEXT-001:E001",))
    assert not ({source.rule_id for source in evidence} & LB_RULE_IDS)

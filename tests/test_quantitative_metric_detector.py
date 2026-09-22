"""Binding QUANT-METRIC-001 behavior from model-spec §7.14.6.7."""

from dataclasses import dataclass
from decimal import Decimal

import pytest

from requirements_quality_assessment.detectors import (
    AcceptanceCriterionBaselineDetector,
    QuantitativeBaselineDetector,
)
from requirements_quality_assessment.detectors.expected_result import (
    RULE_ID as RESULT_RULE_ID,
)
from requirements_quality_assessment.detectors.quantitative import (
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
from requirements_quality_assessment.extractor import (
    BaselineFeatureExtractor,
    FeatureExtractor,
)


def detect(text: str):
    requirement = Requirement("R073", 7, text)
    outcome, evidence = QuantitativeBaselineDetector().detect(requirement)
    return requirement, outcome, evidence


@pytest.mark.parametrize(
    ("text", "value", "unit"),
    [
        ("Час відгуку ≤ 2 с", Decimal("2"), UnitLabel.SECOND),
        ("Час відгуку ≤ 3 с", Decimal("3"), UnitLabel.SECOND),
        ("Час відгуку ≤ 2,5 с", Decimal("2.5"), UnitLabel.SECOND),
        ("Час відгуку ≤ 2 хв", Decimal("2"), UnitLabel.MINUTE),
        ("Час відгуку ≤ 2 секунд", Decimal("2"), UnitLabel.SECOND),
        ("Час відгуку ≤ 2 хвилин", Decimal("2"), UnitLabel.MINUTE),
    ],
)
def test_binding_metric_prefix_enriches_existing_scalar_observation(text, value, unit):
    requirement, outcome, evidence = detect(text)

    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert len(outcome.observations) == 1
    assert [
        (source.evidence_id, source.rule_id, source.text,
         source.start_offset, source.end_offset, source.feature_id)
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
            text[12:],
            12,
            len(text),
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
    assert observation.value.decimal_value == value
    assert observation.unit.label is unit
    assert observation.context is None
    assert observation.unresolved_components == ()
    assert observation.comparator.evidence_refs == ("QUANT-001:E001",)
    assert observation.value.evidence_refs == ("QUANT-001:E001",)
    assert observation.unit.evidence_refs == ("QUANT-001:E001",)
    assert observation.evidence_refs == (
        "QUANT-METRIC-001:E001",
        "QUANT-001:E001",
    )


def test_trailing_numeric_context_preserves_metric_link_and_baseline_diagnostic():
    text = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
    _, outcome, evidence = detect(text)

    assert len(outcome.observations) == 1
    assert [source.text for source in evidence] == ["Час відгуку", "≤ 2 с"]
    assert outcome.observations[0].evidence_refs == (
        "QUANT-METRIC-001:E001",
        "QUANT-001:E001",
    )
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert [
        (item.code, item.rule_id, item.candidate_span.text,
         item.candidate_span.start_offset, item.candidate_span.end_offset)
        for item in outcome.diagnostics
    ] == [
        (UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE, QUANT_RULE_ID, "500", 22, 25)
    ]


def test_competing_lexical_scalar_bound_prevents_metric_attachment():
    text = "Час відгуку ≤ 2 с та не більше 3 с."
    _, outcome, evidence = detect(text)

    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert len(outcome.observations) == 2
    assert [
        (source.evidence_id, source.rule_id, source.text)
        for source in evidence
    ] == [
        ("QUANT-001:E001", QUANT_RULE_ID, "≤ 2 с"),
        ("QUANT-UK-001:E001", QUANT_UK_RULE_ID, "не більше 3 с"),
    ]
    assert [observation.metric for observation in outcome.observations] == [None, None]
    assert [observation.evidence_refs for observation in outcome.observations] == [
        ("QUANT-001:E001",),
        ("QUANT-UK-001:E001",),
    ]


@pytest.mark.parametrize(
    ("text", "scalar_texts", "diagnostic_texts"),
    [
        ("Час відгуку ≤ 95 %", ("≤ 95 %",), ()),
        ("Час відгуку ≤ 2", ("≤ 2",), ()),
        ("Затримка ≤ 2 с", ("≤ 2 с",), ()),
        ("час відгуку ≤ 2 с", ("≤ 2 с",), ()),
        ("Час  відгуку ≤ 2 с", ("≤ 2 с",), ()),
        ("Час відгуку\t≤ 2 с", ("≤ 2 с",), ()),
        ("Час відгуку не більше 2 с", ("не більше 2 с",), ()),
        ("Час відгуку та Час відгуку ≤ 2 с", ("≤ 2 с",), ()),
        ("Час відгуку ≤ 2 с та ≤ 3 с.", ("≤ 2 с", "≤ 3 с"), ()),
        ("Час відгуку системи ≤ 2 с", ("≤ 2 с",), ()),
        ("≤ 2 с", ("≤ 2 с",), ()),
        ("TLS 1.3", (), ()),
        ("OAuth 2.0", (), ()),
    ],
)
def test_ineligible_inputs_preserve_scalar_observations_and_diagnostics(
    text, scalar_texts, diagnostic_texts,
):
    _, outcome, evidence = detect(text)

    assert all(source.rule_id != QUANT_METRIC_RULE_ID for source in evidence)
    assert all(
        source.rule_id in {QUANT_RULE_ID, QUANT_UK_RULE_ID}
        for source in evidence
    )
    assert all(observation.metric is None for observation in outcome.observations)
    assert tuple(source.text for source in evidence) == scalar_texts
    assert tuple(
        item.candidate_span.text for item in outcome.diagnostics
    ) == diagnostic_texts
    assert len(outcome.observations) == len(scalar_texts)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is (
        DetectionStatus.DETECTED if scalar_texts else DetectionStatus.NOT_DETECTED
    )
    counters = {QUANT_RULE_ID: 0, QUANT_UK_RULE_ID: 0}
    expected_ids = []
    for source in evidence:
        counters[source.rule_id] += 1
        expected_ids.append(f"{source.rule_id}:E{counters[source.rule_id]:03d}")
    assert [source.evidence_id for source in evidence] == expected_ids
    assert [observation.evidence_refs for observation in outcome.observations] == [
        (source.evidence_id,) for source in evidence
    ]


@pytest.mark.parametrize("boundary", [".", ";", "?", "!"])
def test_hard_boundary_cannot_separate_metric_and_bound(boundary):
    _, outcome, evidence = detect(f"Час відгуку{boundary} ≤ 2 с")

    assert [source.text for source in evidence] == ["≤ 2 с"]
    assert len(outcome.observations) == 1
    assert outcome.observations[0].metric is None
    assert outcome.diagnostics == ()


def test_public_extraction_path_resolves_metric_and_scalar_evidence():
    requirement = Requirement("R073", 7, "Час відгуку ≤ 2 с")
    extractor: FeatureExtractor = BaselineFeatureExtractor()
    result = extractor.extract(requirement)
    outcome = result.features.quantitative_constraints
    observation, = outcome.observations
    by_id = {source.evidence_id: source for source in result.evidence}

    assert observation.evidence_refs == (
        "QUANT-METRIC-001:E001",
        "QUANT-001:E001",
    )
    assert set(observation.evidence_refs) <= by_id.keys()
    assert all(
        by_id[reference].feature_id is FeatureId.QUANTITATIVE_CONSTRAINT
        for reference in observation.evidence_refs
    )
    assert all(
        requirement.text[source.start_offset:source.end_offset] == source.text
        for source in by_id.values()
    )


@dataclass
class _FakeDetector:
    result: tuple[FeatureDetectionOutcome, tuple[Evidence, ...]]

    def detect(self, requirement: Requirement):
        return self.result


def test_metric_enrichment_does_not_change_acceptance_composition():
    requirement = Requirement("R073", 7, "Час відгуку ≤ 2 с")
    result_source = Evidence(
        "RESULT-UK-001:E001",
        requirement.id,
        FeatureId.EXPECTED_RESULT,
        requirement.text,
        0,
        len(requirement.text),
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
    assert evidence[0].text == requirement.text


def test_lexical_comparator_remains_owned_by_quant_uk_001():
    _, outcome, evidence = detect("Час відгуку не більше 2 с")

    assert [source.rule_id for source in evidence] == [QUANT_UK_RULE_ID]
    assert outcome.observations[0].metric is None

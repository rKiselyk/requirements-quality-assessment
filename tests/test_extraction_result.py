"""Issue #25 extraction-result graph tests; no production detectors."""

from dataclasses import FrozenInstanceError, fields
from decimal import Decimal

import pytest

from requirements_quality_assessment.domain import (
    BoundaryInclusivity, ComparatorComponent, ComparatorLabel,
    DetectionDiagnostic, DetectionProcessingStatus, DiagnosticSpan, Evidence,
    FeatureDetectionOutcome, FeatureId, FeatureObservation,
    NumericValueComponent, QuantitativeConstraintObservation, Requirement,
    RequirementExtractionResult, RequirementFeatures, TextComponent,
    UnitComponent, UnitLabel, VagueTermOccurrence,
)
from requirements_quality_assessment.domain.extraction import _accepted_evidence_refs


SOURCE = "Швидко і швидко: ≤ 2 с."


def _outcome(feature_id, observations=(), diagnostics=()):
    return FeatureDetectionOutcome(
        feature_id, observations,
        DetectionProcessingStatus.INCOMPLETE if diagnostics else DetectionProcessingStatus.COMPLETE,
        diagnostics,
    )


def _features(*, family=FeatureId.CONDITION_CONTEXT, observation=None, diagnostics=()):
    outcomes = {
        feature_id: _outcome(
            feature_id, (observation,) if family is feature_id and observation else (),
            diagnostics if family is feature_id else (),
        ) for feature_id in FeatureId
    }
    return RequirementFeatures(
        outcomes[FeatureId.CONDITION_CONTEXT], outcomes[FeatureId.EXPECTED_RESULT],
        outcomes[FeatureId.ACCEPTANCE_CRITERION],
        outcomes[FeatureId.QUANTITATIVE_CONSTRAINT],
        outcomes[FeatureId.VERIFICATION_METHOD],
        outcomes[FeatureId.VAGUE_TERM_OCCURRENCE],
    )


def _evidence(evidence_id="E1", *, start=0, end=6, requirement_id="R001",
              text=None, feature_id=FeatureId.CONDITION_CONTEXT):
    return Evidence(
        evidence_id, requirement_id, feature_id,
        SOURCE[start:end] if text is None else text, start, end, "TEST-001",
    )


def _result(features=None, evidence=(), requirement=None):
    return RequirementExtractionResult(
        requirement if requirement is not None else Requirement("R001", 1, SOURCE),
        features if features is not None else _features(), evidence,
    )


def test_valid_empty_result_is_immutable_and_preserves_six_families():
    result = _result()
    assert result.evidence == ()
    assert {field.name for field in fields(RequirementExtractionResult)} == {
        "requirement", "features", "evidence",
    }
    assert tuple(field.name for field in fields(RequirementFeatures)) == (
        "condition_contexts", "expected_results", "acceptance_criteria",
        "quantitative_constraints", "verification_methods", "vague_term_occurrences",
    )
    with pytest.raises(FrozenInstanceError):
        result.evidence = ()


@pytest.mark.parametrize("requirement,features,evidence", [
    ("R001", None, ()), (None, "features", ()), (None, None, []),
    (None, None, ("not Evidence",)),
])
def test_rejects_wrong_boundary_types(requirement, features, evidence):
    with pytest.raises(TypeError):
        _result(features=features, evidence=evidence, requirement=requirement)


def test_exact_evidence_span_and_repeated_identical_occurrences_are_distinct():
    first = _evidence("UK-VAGUE-001:E001", feature_id=FeatureId.VAGUE_TERM_OCCURRENCE)
    second = _evidence("UK-VAGUE-001:E002", start=9, end=15,
                       feature_id=FeatureId.VAGUE_TERM_OCCURRENCE)
    observation = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE, "uk_vague_terms_v1", "швидко",
        (first.evidence_id, second.evidence_id),
    )
    result = _result(_features(family=FeatureId.VAGUE_TERM_OCCURRENCE,
                               observation=observation), (first, second))
    assert first.text != second.text  # original case is retained
    assert first.text.casefold() == second.text.casefold()
    assert first.start_offset != second.start_offset
    assert result.evidence == (first, second)


def test_repeated_identical_source_literals_keep_separate_evidence_ids():
    requirement = Requirement("R001", 1, "швидко і швидко")
    items = (
        Evidence("E1", "R001", FeatureId.VAGUE_TERM_OCCURRENCE,
                 "швидко", 0, 6, "UK-VAGUE-001"),
        Evidence("E2", "R001", FeatureId.VAGUE_TERM_OCCURRENCE,
                 "швидко", 9, 15, "UK-VAGUE-001"),
    )
    observation = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE, "uk_vague_terms_v1", "швидко",
        ("E1", "E2"),
    )
    result = _result(_features(family=FeatureId.VAGUE_TERM_OCCURRENCE,
                               observation=observation), items, requirement)
    assert result.evidence[0].text == result.evidence[1].text
    assert result.evidence[0].evidence_id != result.evidence[1].evidence_id


def test_duplicate_evidence_id_is_rejected_even_for_distinct_spans():
    with pytest.raises(ValueError, match="duplicate evidence_id"):
        _result(evidence=(_evidence(), _evidence(start=9, end=15)))


def test_evidence_for_other_requirement_is_rejected():
    with pytest.raises(ValueError, match="requirement_id"):
        _result(evidence=(_evidence(requirement_id="R002"),))


@pytest.mark.parametrize("start,end,text", [
    (0, 6, "швидко"),  # length is valid, source spelling differs
    (len(SOURCE) + 1, len(SOURCE) + 2, "x"),  # extent-valid but beyond source
])
def test_source_round_trip_rejects_mismatched_substring(start, end, text):
    with pytest.raises(ValueError, match="round-trip"):
        _result(evidence=(_evidence(start=start, end=end, text=text),))


@pytest.mark.parametrize("family", [
    FeatureId.CONDITION_CONTEXT, FeatureId.EXPECTED_RESULT,
    FeatureId.ACCEPTANCE_CRITERION, FeatureId.VERIFICATION_METHOD,
])
def test_simple_observation_ref_must_resolve(family):
    observation = FeatureObservation(family, ("missing",))
    with pytest.raises(ValueError, match="dangling accepted evidence_ref"):
        _result(_features(family=family, observation=observation))


def test_vague_occurrence_ref_must_resolve():
    observation = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE, "uk_vague_terms_v1", "швидко", ("missing",),
    )
    with pytest.raises(ValueError, match="dangling accepted evidence_ref"):
        _result(_features(family=FeatureId.VAGUE_TERM_OCCURRENCE, observation=observation))


def _quantitative(*, metric=None, comparator=None, value=None, unit=None, context=None):
    comparator = comparator if comparator is not None else ComparatorComponent(
        ComparatorLabel.UPPER_BOUND, BoundaryInclusivity.UNRESOLVED, ("E1",),
    )
    value = value if value is not None else NumericValueComponent(Decimal("2"), ("E2",))
    refs = tuple(dict.fromkeys(
        ref for component in (metric, comparator, value, unit, context)
        if component is not None for ref in component.evidence_refs
    ))
    return QuantitativeConstraintObservation(
        FeatureId.QUANTITATIVE_CONSTRAINT, metric, comparator, value, unit,
        context, (), refs,
    )


def test_quantitative_top_level_refs_are_traversed_and_must_resolve():
    observation = _quantitative()
    features = _features(family=FeatureId.QUANTITATIVE_CONSTRAINT,
                         observation=observation)
    assert tuple(_accepted_evidence_refs(features))[:2] == observation.evidence_refs
    with pytest.raises(ValueError, match="dangling accepted evidence_ref"):
        _result(features, (_evidence("E1"),))


@pytest.mark.parametrize("component", ["metric", "comparator", "value", "unit", "context"])
def test_every_populated_quantitative_component_ref_is_traversed(component):
    parts = {
        "metric": TextComponent(("E3",)),
        "comparator": ComparatorComponent(
            ComparatorLabel.UPPER_BOUND, BoundaryInclusivity.UNRESOLVED, ("E3",)),
        "value": NumericValueComponent(Decimal("2"), ("E3",)),
        "unit": UnitComponent(UnitLabel.SECOND, ("E3",)),
        "context": TextComponent(("E3",)),
    }
    observation = _quantitative(**{component: parts[component]})
    features = _features(family=FeatureId.QUANTITATIVE_CONSTRAINT,
                         observation=observation)
    refs = tuple(_accepted_evidence_refs(features))
    assert "E3" in refs[:len(observation.evidence_refs)]
    assert refs.count("E3") >= 2  # top-level and component are both visited
    with pytest.raises(ValueError, match="dangling accepted evidence_ref"):
        _result(features, (_evidence("E1"), _evidence("E2", start=9, end=15)))


def test_diagnostics_are_not_accepted_evidence_refs():
    diagnostic = DetectionDiagnostic(
        "RULE_UNRESOLVED", "candidate only", "TEST-001",
        DiagnosticSpan(SOURCE[:6], 0, 6),
    )
    result = _result(_features(diagnostics=(diagnostic,)))
    assert result.evidence == ()
    assert result.features.condition_contexts.diagnostics == (diagnostic,)

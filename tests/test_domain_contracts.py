"""Construction tests for the researcher-approved Section 7.15 subset."""

from dataclasses import FrozenInstanceError, fields
from decimal import Decimal
import importlib
import sys

import pytest

from requirements_quality_assessment.domain import (
    BoundaryInclusivity, ComparatorComponent, ComparatorLabel,
    CriterionApplicability, DetectionDiagnostic, DetectionProcessingStatus,
    DetectionStatus, DiagnosticSpan, Evidence, FeatureDetectionOutcome, FeatureId,
    FeatureObservation, MorphFeature, NumericValueComponent, ParsedRequirement,
    ParserDiagnostic, ParserDiagnosticCode, ParserMetadata, ParserOutcome,
    QuantitativeComponentName, QuantitativeConstraintObservation, Requirement,
    RequirementFeatures, SentenceAnnotation, TextComponent, TokenAnnotation,
    UnitComponent, UnitLabel, VagueTermOccurrence,
)


def test_requirement_preserves_already_trimmed_text_and_source_line() -> None:
    requirement = Requirement("R001", 3, "Час ≤ 2 с.")
    assert (requirement.id, requirement.source_line, requirement.text) == (
        "R001", 3, "Час ≤ 2 с."
    )
    with pytest.raises(ValueError):
        Requirement("R002", 0, "текст")
    with pytest.raises(ValueError):
        Requirement("R002", 1, " текст ")
    with pytest.raises(FrozenInstanceError):
        requirement.text = "changed"


def test_registry_and_applicability_are_distinct() -> None:
    assert len(FeatureId) == 6
    assert {feature.value for feature in FeatureId} == {
        "condition_context", "expected_result", "acceptance_criterion",
        "quantitative_constraint", "verification_method", "vague_term_occurrence",
    }
    assert len(CriterionApplicability) == 3
    assert len({item.value for item in CriterionApplicability}) == 3
    assert CriterionApplicability.UNKNOWN is not CriterionApplicability.NOT_APPLICABLE


def test_evidence_span_checks_code_point_extent_without_normalization() -> None:
    source = "Час ≤ 2 с."
    evidence = Evidence("E1", "R001", FeatureId.QUANTITATIVE_CONSTRAINT,
                        source[4:5], 4, 5, "QUANT-001")
    assert evidence.text == "≤"
    assert source[evidence.start_offset:evidence.end_offset] == evidence.text
    for start, end, text in ((-1, 1, "ab"), (2, 1, ""), (0, 2, "a")):
        with pytest.raises(ValueError):
            Evidence("E1", "R001", FeatureId.CONDITION_CONTEXT,
                     text, start, end, "COND-UK-001")


def _diagnostic() -> DetectionDiagnostic:
    return DetectionDiagnostic("RULE_UNRESOLVED", "candidate unresolved", "COND-UK-001",
                               DiagnosticSpan("до", 2, 4))


def _outcome(feature: FeatureId, observations: tuple = (), *,
             incomplete: bool = False) -> FeatureDetectionOutcome:
    return FeatureDetectionOutcome(
        feature, observations,
        DetectionProcessingStatus.INCOMPLETE if incomplete else DetectionProcessingStatus.COMPLETE,
        (_diagnostic(),) if incomplete else (),
    )


def test_detection_status_is_derived_and_preserves_mixed_state() -> None:
    observation = FeatureObservation(FeatureId.CONDITION_CONTEXT, ("E1",))
    assert _outcome(FeatureId.CONDITION_CONTEXT, (observation,)).status is DetectionStatus.DETECTED
    assert _outcome(FeatureId.CONDITION_CONTEXT).status is DetectionStatus.NOT_DETECTED
    assert _outcome(FeatureId.CONDITION_CONTEXT, incomplete=True).status is DetectionStatus.UNRESOLVED
    mixed = _outcome(FeatureId.CONDITION_CONTEXT, (observation,), incomplete=True)
    assert mixed.status is DetectionStatus.DETECTED
    assert mixed.diagnostics == (_diagnostic(),)
    assert "status" not in {field.name for field in fields(FeatureDetectionOutcome)}


def test_detection_processing_invariants_and_diagnostic_separation() -> None:
    with pytest.raises(ValueError):
        FeatureDetectionOutcome(FeatureId.CONDITION_CONTEXT, (),
                                DetectionProcessingStatus.COMPLETE, (_diagnostic(),))
    with pytest.raises(ValueError):
        FeatureDetectionOutcome(FeatureId.CONDITION_CONTEXT, (),
                                DetectionProcessingStatus.INCOMPLETE, ())
    assert not isinstance(_diagnostic().candidate_span, Evidence)
    assert {field.name for field in fields(DiagnosticSpan)} == {
        "text", "start_offset", "end_offset"
    }
    with pytest.raises(ValueError):
        DiagnosticSpan("bad", 0, 2)


def _token(token_id: int, sentence_id: int, text: str, start: int, end: int,
           head: int | None = None) -> TokenAnnotation:
    return TokenAnnotation(token_id, sentence_id, text, start, end, None, "NOUN",
                           (MorphFeature("Case", ("Nom",)),), head, "root")


def _parsed(tokens: tuple[TokenAnnotation, ...] | None = None) -> ParsedRequirement:
    text = "Кіт біжить. Пес спить."
    return ParsedRequirement(
        "R001", text, (SentenceAnnotation(0, 0, 11), SentenceAnnotation(1, 12, len(text))),
        tokens if tokens is not None else (
            _token(0, 0, "Кіт", 0, 3), _token(1, 0, "біжить", 4, 10, 0),
            _token(2, 1, "Пес", 12, 15), _token(3, 1, "спить", 16, 21, 2),
        ), ParserMetadata("provider", "1", "model", "1", "uk"),
    )


def test_parser_outcome_success_degradation_and_failure() -> None:
    parsed = _parsed()
    assert ParserOutcome(parsed, ()).parsed_requirement is parsed
    incomplete = ParserDiagnostic(ParserDiagnosticCode.ANNOTATION_INCOMPLETE, "missing annotation")
    assert ParserOutcome(parsed, (incomplete,)).diagnostics == (incomplete,)
    unavailable = ParserDiagnostic(ParserDiagnosticCode.PARSER_UNAVAILABLE, "unavailable")
    assert ParserOutcome(None, (unavailable,)).parsed_requirement is None
    with pytest.raises(ValueError):
        ParserOutcome(parsed, (unavailable,))
    with pytest.raises(ValueError):
        ParserOutcome(None, ())


def test_parser_offsets_round_trip_and_heads_remain_in_sentence() -> None:
    parsed = _parsed()
    assert all(parsed.text[t.start_offset:t.end_offset] == t.text for t in parsed.tokens)
    with pytest.raises(ValueError):
        _token(0, 0, "Кіт", -1, 2)
    with pytest.raises(ValueError):
        _parsed((_token(0, 0, "Кит", 0, 3),))
    with pytest.raises(ValueError):
        _parsed((_token(0, 0, "Кіт", 0, 3, 2), _token(2, 1, "Пес", 12, 15)))
    with pytest.raises(ValueError):
        _parsed((_token(0, 0, "Кіт", 0, 3), _token(0, 0, "біжить", 4, 10)))
    with pytest.raises(ValueError):
        _parsed((_token(1, 0, "Кіт", 0, 3),))
    with pytest.raises(ValueError):
        MorphFeature("Case", ("Nom", "Acc"))


def test_parser_neutral_root_rejects_self_head() -> None:
    with pytest.raises(ValueError, match="self-referential"):
        _token(0, 0, "Кіт", 0, 3, 0)


def _partial() -> QuantitativeConstraintObservation:
    return QuantitativeConstraintObservation(
        FeatureId.QUANTITATIVE_CONSTRAINT, None,
        ComparatorComponent(ComparatorLabel.UPPER_BOUND, BoundaryInclusivity.UNRESOLVED, ("E1",)),
        NumericValueComponent(Decimal("99.9"), ("E2",)), None, None,
        (QuantitativeComponentName.METRIC, QuantitativeComponentName.CONTEXT), ("E1", "E2"),
    )


def test_quantitative_components_and_partial_observation() -> None:
    partial = _partial()
    assert partial.metric is None
    assert partial.comparator.label is ComparatorLabel.UPPER_BOUND
    assert partial.comparator.inclusivity is BoundaryInclusivity.UNRESOLVED
    assert isinstance(partial.value.decimal_value, Decimal)
    with pytest.raises(TypeError):
        NumericValueComponent(99.9, ("E2",))
    with pytest.raises(ValueError):
        ComparatorComponent(ComparatorLabel.UPPER_BOUND, BoundaryInclusivity.INCLUSIVE, ("E1",))
    with pytest.raises(ValueError):
        QuantitativeConstraintObservation(
            FeatureId.QUANTITATIVE_CONSTRAINT, TextComponent(("E3",)), partial.comparator,
            partial.value, UnitComponent(UnitLabel.SECOND, ("E4",)), None,
            (QuantitativeComponentName.METRIC,), ("E1", "E2", "E3", "E4"),
        )
    with pytest.raises(ValueError):
        QuantitativeConstraintObservation(
            FeatureId.QUANTITATIVE_CONSTRAINT, None, partial.comparator, partial.value,
            None, None, partial.unresolved_components, ("E1", "E1", "E2"),
        )
    with pytest.raises(ValueError):
        QuantitativeConstraintObservation(
            FeatureId.QUANTITATIVE_CONSTRAINT, None, partial.comparator, partial.value,
            None, None, partial.unresolved_components, ("E1",),
        )


@pytest.mark.parametrize("construct", [
    lambda: FeatureObservation(FeatureId.CONDITION_CONTEXT, ()),
    lambda: VagueTermOccurrence(FeatureId.VAGUE_TERM_OCCURRENCE,
                                "uk_vague_terms_v1", "швидко", ()),
    lambda: TextComponent(()),
    lambda: ComparatorComponent(ComparatorLabel.UPPER_BOUND,
                                BoundaryInclusivity.UNRESOLVED, ()),
    lambda: NumericValueComponent(Decimal("2"), ()),
    lambda: UnitComponent(UnitLabel.SECOND, ()),
], ids=["simple", "vague", "text", "comparator", "numeric", "unit"])
def test_accepted_observations_and_populated_components_require_evidence(construct) -> None:
    with pytest.raises(ValueError, match="requires evidence_refs"):
        construct()


def test_quantitative_approved_anchors_allow_both_partial_shapes() -> None:
    assert _partial().value.decimal_value == Decimal("99.9")  # comparator + value
    value_and_unit = QuantitativeConstraintObservation(
        FeatureId.QUANTITATIVE_CONSTRAINT, None, None,
        NumericValueComponent(Decimal("2"), ("E1",)),
        UnitComponent(UnitLabel.SECOND, ("E2",)), None,
        (QuantitativeComponentName.COMPARATOR,), ("E1", "E2"),
    )
    assert value_and_unit.comparator is None
    assert value_and_unit.unit.label is UnitLabel.SECOND


def test_quantitative_observation_rejects_empty_and_unanchored_components() -> None:
    with pytest.raises(ValueError, match=r"comparator \+ value or value \+ unit"):
        QuantitativeConstraintObservation(
            FeatureId.QUANTITATIVE_CONSTRAINT, None, None, None, None, None,
            (), (),
        )
    with pytest.raises(ValueError, match=r"comparator \+ value or value \+ unit"):
        QuantitativeConstraintObservation(
            FeatureId.QUANTITATIVE_CONSTRAINT, TextComponent(("E1",)),
            ComparatorComponent(ComparatorLabel.LESS_THAN_OR_EQUAL,
                                BoundaryInclusivity.INCLUSIVE, ("E2",)),
            None, None, None, (), ("E1", "E2"),
        )
    with pytest.raises(ValueError, match=r"comparator \+ value or value \+ unit"):
        QuantitativeConstraintObservation(
            FeatureId.QUANTITATIVE_CONSTRAINT, None, None,
            NumericValueComponent(Decimal("2"), ("E1",)), None, None,
            (), ("E1",),
        )


def test_six_typed_feature_families_and_wrong_wrapper_assignment() -> None:
    features = RequirementFeatures(
        _outcome(FeatureId.CONDITION_CONTEXT), _outcome(FeatureId.EXPECTED_RESULT),
        _outcome(FeatureId.ACCEPTANCE_CRITERION),
        _outcome(FeatureId.QUANTITATIVE_CONSTRAINT, (_partial(),)),
        _outcome(FeatureId.VERIFICATION_METHOD),
        _outcome(FeatureId.VAGUE_TERM_OCCURRENCE, (
            VagueTermOccurrence(FeatureId.VAGUE_TERM_OCCURRENCE, "uk_vague_terms_v1", "швидко", ("E5",)),
        )),
    )
    assert len(fields(RequirementFeatures)) == 6
    assert features.quantitative_constraints.observations == (_partial(),)
    with pytest.raises(ValueError):
        RequirementFeatures(_outcome(FeatureId.EXPECTED_RESULT), *tuple(
            getattr(features, field.name) for field in fields(RequirementFeatures)[1:]
        ))
    with pytest.raises(TypeError):
        RequirementFeatures(features.condition_contexts, features.expected_results,
                            features.acceptance_criteria,
                            _outcome(FeatureId.QUANTITATIVE_CONSTRAINT),
                            features.verification_methods,
                            _outcome(FeatureId.VAGUE_TERM_OCCURRENCE, (Evidence(
                                "E5", "R001", FeatureId.VAGUE_TERM_OCCURRENCE,
                                "швидко", 0, 6, "UK-VAGUE-001"),)))


def test_domain_import_has_no_nlp_runtime_requirement() -> None:
    importlib.import_module("requirements_quality_assessment.domain")
    assert "spacy" not in sys.modules
    assert "stanza" not in sys.modules


def test_vague_literal_is_canonical_not_unapproved_variant() -> None:
    with pytest.raises(ValueError):
        VagueTermOccurrence(FeatureId.VAGUE_TERM_OCCURRENCE,
                            "uk_vague_terms_v1", "Швидко", ("E1",))

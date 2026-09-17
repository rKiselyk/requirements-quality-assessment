"""MVP-09D AGG-MVP-001 SpecificationQualityAggregator tests.

SpecificationQualityAggregator is exercised only against manually constructed
RequirementQualityProfile instances; no calculator, extractor, reader, or
CLI involved.
"""

from fractions import Fraction

from requirements_quality_assessment.aggregator import SpecificationQualityAggregator
from requirements_quality_assessment.domain import (
    CharacteristicAssessment, CharacteristicAssessmentState, CharacteristicId,
    RequirementQualityProfile, SpecificationQualityProfile,
)
from requirements_quality_assessment.domain.specification_profile import (
    AGGREGATION_RULE_ID,
)


def _computed(characteristic_id, value, rule_id="TEST-RULE"):
    return CharacteristicAssessment(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.COMPUTED,
        value=value,
        assessment_rule_id=rule_id,
        findings=(),
        explanation="test fixture",
    )


def _unknown(characteristic_id):
    return CharacteristicAssessment(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.UNKNOWN,
        value=None,
        assessment_rule_id=None,
        findings=(),
        explanation="test fixture",
    )


def _not_applicable(characteristic_id):
    return CharacteristicAssessment(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.NOT_APPLICABLE,
        value=None,
        assessment_rule_id=None,
        findings=(),
        explanation="test fixture",
    )


def _profile(completeness=None, verifiability=None, unambiguity=None):
    return RequirementQualityProfile(
        completeness=completeness or _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1)),
        verifiability=verifiability or _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1)),
        unambiguity=unambiguity or _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1)),
    )


# -- AGG-MVP-001 eight-case decision matrix (exercised via verifiability) -------

def test_all_computed_yields_computed_state_with_exact_mean() -> None:
    profiles = [
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1))),
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(1, 2))),
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(0, 1))),
    ]

    result = SpecificationQualityAggregator().aggregate(profiles)

    assert result.verifiability.state is CharacteristicAssessmentState.COMPUTED
    assert result.verifiability.value == Fraction(1, 2)
    assert result.verifiability.computed_count == 3
    assert result.verifiability.unknown_count == 0
    assert result.verifiability.not_applicable_count == 0
    assert result.verifiability.total_count == 3


def test_computed_and_unknown_yields_computed_state_excluding_unknown() -> None:
    profiles = [
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1))),
        _profile(verifiability=_unknown(CharacteristicId.VERIFIABILITY)),
    ]

    result = SpecificationQualityAggregator().aggregate(profiles)

    assert result.verifiability.state is CharacteristicAssessmentState.COMPUTED
    assert result.verifiability.value == Fraction(1, 1)
    assert result.verifiability.computed_count == 1
    assert result.verifiability.unknown_count == 1
    assert result.verifiability.total_count == 2


def test_computed_and_not_applicable_yields_computed_state_excluding_not_applicable() -> None:
    profiles = [
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(1, 2))),
        _profile(verifiability=_not_applicable(CharacteristicId.VERIFIABILITY)),
    ]

    result = SpecificationQualityAggregator().aggregate(profiles)

    assert result.verifiability.state is CharacteristicAssessmentState.COMPUTED
    assert result.verifiability.value == Fraction(1, 2)
    assert result.verifiability.computed_count == 1
    assert result.verifiability.not_applicable_count == 1
    assert result.verifiability.total_count == 2


def test_computed_unknown_and_not_applicable_yields_computed_state() -> None:
    """Task Example 1: values 1, 1/2, UNKNOWN, 0, NOT_APPLICABLE -> 1/2, counts 3/1/1/5."""
    profiles = [
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1))),
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(1, 2))),
        _profile(verifiability=_unknown(CharacteristicId.VERIFIABILITY)),
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(0, 1))),
        _profile(verifiability=_not_applicable(CharacteristicId.VERIFIABILITY)),
    ]

    result = SpecificationQualityAggregator().aggregate(profiles)

    assert result.verifiability.state is CharacteristicAssessmentState.COMPUTED
    assert result.verifiability.value == Fraction(1, 2)
    assert result.verifiability.computed_count == 3
    assert result.verifiability.unknown_count == 1
    assert result.verifiability.not_applicable_count == 1
    assert result.verifiability.total_count == 5


def test_all_unknown_yields_unknown_state_with_none_value() -> None:
    profiles = [
        _profile(verifiability=_unknown(CharacteristicId.VERIFIABILITY)),
        _profile(verifiability=_unknown(CharacteristicId.VERIFIABILITY)),
    ]

    result = SpecificationQualityAggregator().aggregate(profiles)

    assert result.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert result.verifiability.value is None
    assert result.verifiability.computed_count == 0
    assert result.verifiability.unknown_count == 2
    assert result.verifiability.total_count == 2


def test_unknown_and_not_applicable_with_no_computed_yields_unknown_state() -> None:
    """Task Example 2: UNKNOWN, UNKNOWN, NOT_APPLICABLE -> UNKNOWN, counts 0/2/1/3."""
    profiles = [
        _profile(verifiability=_unknown(CharacteristicId.VERIFIABILITY)),
        _profile(verifiability=_unknown(CharacteristicId.VERIFIABILITY)),
        _profile(verifiability=_not_applicable(CharacteristicId.VERIFIABILITY)),
    ]

    result = SpecificationQualityAggregator().aggregate(profiles)

    assert result.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert result.verifiability.value is None
    assert result.verifiability.computed_count == 0
    assert result.verifiability.unknown_count == 2
    assert result.verifiability.not_applicable_count == 1
    assert result.verifiability.total_count == 3


def test_all_not_applicable_yields_not_applicable_state() -> None:
    """Task Example 3: NOT_APPLICABLE, NOT_APPLICABLE, NOT_APPLICABLE."""
    profiles = [
        _profile(verifiability=_not_applicable(CharacteristicId.VERIFIABILITY)),
        _profile(verifiability=_not_applicable(CharacteristicId.VERIFIABILITY)),
        _profile(verifiability=_not_applicable(CharacteristicId.VERIFIABILITY)),
    ]

    result = SpecificationQualityAggregator().aggregate(profiles)

    assert result.verifiability.state is CharacteristicAssessmentState.NOT_APPLICABLE
    assert result.verifiability.value is None
    assert result.verifiability.computed_count == 0
    assert result.verifiability.unknown_count == 0
    assert result.verifiability.not_applicable_count == 3
    assert result.verifiability.total_count == 3


def test_empty_profile_collection_yields_not_applicable_state_with_zero_counts() -> None:
    result = SpecificationQualityAggregator().aggregate([])

    for aggregate in (result.completeness, result.verifiability, result.unambiguity):
        assert aggregate.state is CharacteristicAssessmentState.NOT_APPLICABLE
        assert aggregate.value is None
        assert aggregate.computed_count == 0
        assert aggregate.unknown_count == 0
        assert aggregate.not_applicable_count == 0
        assert aggregate.total_count == 0


# -- Exact arithmetic ------------------------------------------------------------

def test_exact_mean_of_one_one_half_one_third_is_eleven_eighteenths() -> None:
    profiles = [
        _profile(completeness=_computed(CharacteristicId.COMPLETENESS, Fraction(1, 1))),
        _profile(completeness=_computed(CharacteristicId.COMPLETENESS, Fraction(1, 2))),
        _profile(completeness=_computed(CharacteristicId.COMPLETENESS, Fraction(1, 3))),
    ]

    result = SpecificationQualityAggregator().aggregate(profiles)

    assert result.completeness.value == Fraction(11, 18)


# -- Cross-cutting behavior --------------------------------------------------------

def test_each_characteristic_is_aggregated_independently_from_its_own_column() -> None:
    profiles = [
        _profile(
            completeness=_computed(CharacteristicId.COMPLETENESS, Fraction(1, 1)),
            verifiability=_unknown(CharacteristicId.VERIFIABILITY),
            unambiguity=_not_applicable(CharacteristicId.UNAMBIGUITY),
        ),
        _profile(
            completeness=_computed(CharacteristicId.COMPLETENESS, Fraction(0, 1)),
            verifiability=_unknown(CharacteristicId.VERIFIABILITY),
            unambiguity=_not_applicable(CharacteristicId.UNAMBIGUITY),
        ),
    ]

    result = SpecificationQualityAggregator().aggregate(profiles)

    assert result.completeness.state is CharacteristicAssessmentState.COMPUTED
    assert result.completeness.value == Fraction(1, 2)
    assert result.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert result.verifiability.value is None
    assert result.unambiguity.state is CharacteristicAssessmentState.NOT_APPLICABLE
    assert result.unambiguity.value is None


def test_generator_input_is_materialized_correctly() -> None:
    profiles = [
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1))),
        _profile(verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(0, 1))),
        _profile(verifiability=_unknown(CharacteristicId.VERIFIABILITY)),
    ]

    result = SpecificationQualityAggregator().aggregate(profile for profile in profiles)

    assert result.verifiability.total_count == 3
    assert result.verifiability.computed_count == 2
    assert result.verifiability.unknown_count == 1
    assert result.verifiability.value == Fraction(1, 2)


def test_result_type_has_no_scalar_score() -> None:
    result = SpecificationQualityAggregator().aggregate([_profile()])

    assert type(result) is SpecificationQualityProfile
    assert not hasattr(result, "score")
    assert not hasattr(result, "file_score")
    assert not hasattr(result, "overall")


def test_aggregation_rule_id_is_agg_mvp_001_on_every_characteristic() -> None:
    result = SpecificationQualityAggregator().aggregate([_profile()])

    assert result.completeness.aggregation_rule_id == AGGREGATION_RULE_ID == "AGG-MVP-001"
    assert result.verifiability.aggregation_rule_id == AGGREGATION_RULE_ID
    assert result.unambiguity.aggregation_rule_id == AGGREGATION_RULE_ID


def test_repeated_calls_on_the_same_input_are_deterministic() -> None:
    profiles = [_profile(), _profile()]
    aggregator = SpecificationQualityAggregator()

    first = aggregator.aggregate(profiles)
    second = aggregator.aggregate(profiles)

    assert first.completeness == second.completeness
    assert first.verifiability == second.verifiability
    assert first.unambiguity == second.unambiguity

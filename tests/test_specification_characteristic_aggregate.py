"""MVP-09D AGG-MVP-001 SpecificationCharacteristicAggregate contract tests."""

from dataclasses import FrozenInstanceError, fields
from fractions import Fraction

import pytest

from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState, CharacteristicId,
    SpecificationCharacteristicAggregate,
)
from requirements_quality_assessment.domain.specification_profile import (
    AGGREGATION_RULE_ID,
)


def _aggregate(*, characteristic_id=CharacteristicId.COMPLETENESS,
               state=CharacteristicAssessmentState.COMPUTED, value=Fraction(1, 2),
               computed_count=1, unknown_count=0, not_applicable_count=0,
               total_count=1, aggregation_rule_id=AGGREGATION_RULE_ID):
    return SpecificationCharacteristicAggregate(
        characteristic_id, state, value, computed_count, unknown_count,
        not_applicable_count, total_count, aggregation_rule_id,
    )


def test_valid_computed_aggregate_constructs_with_exact_fraction_value() -> None:
    aggregate = _aggregate(value=Fraction(11, 18), computed_count=3, total_count=3)

    assert aggregate.state is CharacteristicAssessmentState.COMPUTED
    assert aggregate.value == Fraction(11, 18)
    assert aggregate.aggregation_rule_id == "AGG-MVP-001"


def test_valid_unknown_aggregate_constructs_with_none_value() -> None:
    aggregate = _aggregate(state=CharacteristicAssessmentState.UNKNOWN, value=None,
                            computed_count=0, unknown_count=2, total_count=2)

    assert aggregate.state is CharacteristicAssessmentState.UNKNOWN
    assert aggregate.value is None


def test_valid_not_applicable_aggregate_constructs_with_none_value() -> None:
    aggregate = _aggregate(state=CharacteristicAssessmentState.NOT_APPLICABLE, value=None,
                            computed_count=0, unknown_count=0,
                            not_applicable_count=3, total_count=3)

    assert aggregate.state is CharacteristicAssessmentState.NOT_APPLICABLE
    assert aggregate.value is None


def test_valid_not_applicable_aggregate_from_empty_collection_all_counts_zero() -> None:
    aggregate = _aggregate(state=CharacteristicAssessmentState.NOT_APPLICABLE, value=None,
                            computed_count=0, unknown_count=0,
                            not_applicable_count=0, total_count=0)

    assert aggregate.state is CharacteristicAssessmentState.NOT_APPLICABLE
    assert aggregate.computed_count == 0
    assert aggregate.unknown_count == 0
    assert aggregate.not_applicable_count == 0
    assert aggregate.total_count == 0


@pytest.mark.parametrize(
    "count_field",
    ["computed_count", "unknown_count", "not_applicable_count", "total_count"],
)
def test_negative_count_is_rejected(count_field) -> None:
    with pytest.raises(ValueError):
        _aggregate(**{count_field: -1})


def test_total_count_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(computed_count=1, unknown_count=1, not_applicable_count=0, total_count=5)


def test_computed_state_with_none_value_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.COMPUTED, value=None)


def test_computed_state_with_non_fraction_value_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.COMPUTED, value=0.5)


def test_computed_state_with_value_outside_zero_one_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.COMPUTED, value=Fraction(3, 2))
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.COMPUTED, value=Fraction(-1, 2))


def test_computed_state_with_zero_computed_count_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.COMPUTED, value=Fraction(1, 2),
                    computed_count=0, total_count=0)


def test_unknown_state_with_numeric_value_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.UNKNOWN, value=Fraction(1, 2),
                    computed_count=0, unknown_count=1, total_count=1)


def test_unknown_state_with_computed_count_greater_than_zero_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.UNKNOWN, value=None,
                    computed_count=1, unknown_count=1, total_count=2)


def test_unknown_state_with_zero_unknown_count_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.UNKNOWN, value=None,
                    computed_count=0, unknown_count=0, total_count=0)


def test_not_applicable_state_with_numeric_value_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.NOT_APPLICABLE, value=Fraction(1, 2),
                    computed_count=0, unknown_count=0, not_applicable_count=1, total_count=1)


def test_not_applicable_state_with_computed_count_greater_than_zero_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.NOT_APPLICABLE, value=None,
                    computed_count=1, unknown_count=0, not_applicable_count=1, total_count=2)


def test_not_applicable_state_with_unknown_count_greater_than_zero_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(state=CharacteristicAssessmentState.NOT_APPLICABLE, value=None,
                    computed_count=0, unknown_count=1, not_applicable_count=1, total_count=2)


def test_wrong_aggregation_rule_id_is_rejected() -> None:
    with pytest.raises(ValueError):
        _aggregate(aggregation_rule_id="NOT-A-REAL-RULE")


def test_wrong_type_characteristic_id_is_rejected() -> None:
    with pytest.raises(TypeError):
        _aggregate(characteristic_id="COMPLETENESS")


def test_wrong_type_state_is_rejected() -> None:
    with pytest.raises(TypeError):
        _aggregate(state="COMPUTED")


def test_aggregate_is_immutable() -> None:
    aggregate = _aggregate()

    with pytest.raises(FrozenInstanceError):
        aggregate.value = Fraction(0, 1)


def test_aggregate_has_exactly_the_approved_fields() -> None:
    assert {field.name for field in fields(SpecificationCharacteristicAggregate)} == {
        "characteristic_id", "state", "value", "computed_count", "unknown_count",
        "not_applicable_count", "total_count", "aggregation_rule_id",
    }
    for forbidden in ("findings", "explanation"):
        assert not hasattr(SpecificationCharacteristicAggregate, forbidden)

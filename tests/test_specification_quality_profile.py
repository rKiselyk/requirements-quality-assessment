"""MVP-09D AGG-MVP-001 SpecificationQualityProfile contract tests."""

from dataclasses import FrozenInstanceError, fields
from fractions import Fraction

import pytest

from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState, CharacteristicId,
    SpecificationCharacteristicAggregate, SpecificationQualityProfile,
)
from requirements_quality_assessment.domain.specification_profile import (
    AGGREGATION_RULE_ID,
)


def _computed_aggregate(characteristic_id, value):
    return SpecificationCharacteristicAggregate(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.COMPUTED,
        value=value,
        computed_count=1,
        unknown_count=0,
        not_applicable_count=0,
        total_count=1,
        aggregation_rule_id=AGGREGATION_RULE_ID,
    )


def _unknown_aggregate(characteristic_id):
    return SpecificationCharacteristicAggregate(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.UNKNOWN,
        value=None,
        computed_count=0,
        unknown_count=1,
        not_applicable_count=0,
        total_count=1,
        aggregation_rule_id=AGGREGATION_RULE_ID,
    )


def _not_applicable_aggregate(characteristic_id):
    return SpecificationCharacteristicAggregate(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.NOT_APPLICABLE,
        value=None,
        computed_count=0,
        unknown_count=0,
        not_applicable_count=1,
        total_count=1,
        aggregation_rule_id=AGGREGATION_RULE_ID,
    )


def test_three_valid_aggregates_construct_a_valid_profile() -> None:
    completeness = _computed_aggregate(CharacteristicId.COMPLETENESS, Fraction(1, 3))
    verifiability = _computed_aggregate(CharacteristicId.VERIFIABILITY, Fraction(1, 2))
    unambiguity = _computed_aggregate(CharacteristicId.UNAMBIGUITY, Fraction(1, 1))

    profile = SpecificationQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness is completeness
    assert profile.verifiability is verifiability
    assert profile.unambiguity is unambiguity


def test_profile_preserves_exact_fraction_values_and_counts_without_mutation() -> None:
    completeness = _computed_aggregate(CharacteristicId.COMPLETENESS, Fraction(11, 18))
    verifiability = _computed_aggregate(CharacteristicId.VERIFIABILITY, Fraction(1, 2))
    unambiguity = _computed_aggregate(CharacteristicId.UNAMBIGUITY, Fraction(1, 1))

    profile = SpecificationQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.value == Fraction(11, 18)
    assert profile.verifiability.value == Fraction(1, 2)
    assert profile.unambiguity.value == Fraction(1, 1)
    assert profile.completeness.computed_count == 1
    assert type(profile.completeness.value) is Fraction


def test_mixed_states_across_characteristics_are_preserved_independently() -> None:
    completeness = _computed_aggregate(CharacteristicId.COMPLETENESS, Fraction(1, 1))
    verifiability = _unknown_aggregate(CharacteristicId.VERIFIABILITY)
    unambiguity = _not_applicable_aggregate(CharacteristicId.UNAMBIGUITY)

    profile = SpecificationQualityProfile(completeness, verifiability, unambiguity)

    assert profile.completeness.state is CharacteristicAssessmentState.COMPUTED
    assert profile.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert profile.unambiguity.state is CharacteristicAssessmentState.NOT_APPLICABLE
    assert not hasattr(profile, "state")
    assert not hasattr(profile, "value")


def test_wrong_characteristic_in_completeness_slot_is_rejected() -> None:
    wrong = _computed_aggregate(CharacteristicId.VERIFIABILITY, Fraction(1, 1))
    verifiability = _computed_aggregate(CharacteristicId.VERIFIABILITY, Fraction(1, 1))
    unambiguity = _computed_aggregate(CharacteristicId.UNAMBIGUITY, Fraction(1, 1))

    with pytest.raises(ValueError):
        SpecificationQualityProfile(wrong, verifiability, unambiguity)


def test_wrong_characteristic_in_verifiability_slot_is_rejected() -> None:
    completeness = _computed_aggregate(CharacteristicId.COMPLETENESS, Fraction(1, 1))
    wrong = _computed_aggregate(CharacteristicId.UNAMBIGUITY, Fraction(1, 1))
    unambiguity = _computed_aggregate(CharacteristicId.UNAMBIGUITY, Fraction(1, 1))

    with pytest.raises(ValueError):
        SpecificationQualityProfile(completeness, wrong, unambiguity)


def test_wrong_characteristic_in_unambiguity_slot_is_rejected() -> None:
    completeness = _computed_aggregate(CharacteristicId.COMPLETENESS, Fraction(1, 1))
    verifiability = _computed_aggregate(CharacteristicId.VERIFIABILITY, Fraction(1, 1))
    wrong = _computed_aggregate(CharacteristicId.COMPLETENESS, Fraction(1, 1))

    with pytest.raises(ValueError):
        SpecificationQualityProfile(completeness, verifiability, wrong)


def test_non_aggregate_component_is_rejected_with_type_error() -> None:
    completeness = _computed_aggregate(CharacteristicId.COMPLETENESS, Fraction(1, 1))
    verifiability = _computed_aggregate(CharacteristicId.VERIFIABILITY, Fraction(1, 1))
    unambiguity = _computed_aggregate(CharacteristicId.UNAMBIGUITY, Fraction(1, 1))

    with pytest.raises(TypeError):
        SpecificationQualityProfile("not an aggregate", verifiability, unambiguity)
    with pytest.raises(TypeError):
        SpecificationQualityProfile(completeness, "not an aggregate", unambiguity)
    with pytest.raises(TypeError):
        SpecificationQualityProfile(completeness, verifiability, "not an aggregate")


def test_profile_is_immutable() -> None:
    completeness = _computed_aggregate(CharacteristicId.COMPLETENESS, Fraction(1, 1))
    verifiability = _computed_aggregate(CharacteristicId.VERIFIABILITY, Fraction(1, 1))
    unambiguity = _computed_aggregate(CharacteristicId.UNAMBIGUITY, Fraction(1, 1))
    profile = SpecificationQualityProfile(completeness, verifiability, unambiguity)

    with pytest.raises(FrozenInstanceError):
        profile.completeness = completeness


def test_profile_has_exactly_three_fields_and_no_scalar_result() -> None:
    assert {field.name for field in fields(SpecificationQualityProfile)} == {
        "completeness", "verifiability", "unambiguity",
    }
    for forbidden in ("score", "value", "overall_score", "file_quality_score", "state"):
        assert not hasattr(SpecificationQualityProfile, forbidden)

    completeness = _computed_aggregate(CharacteristicId.COMPLETENESS, Fraction(1, 1))
    verifiability = _computed_aggregate(CharacteristicId.VERIFIABILITY, Fraction(1, 1))
    unambiguity = _computed_aggregate(CharacteristicId.UNAMBIGUITY, Fraction(1, 1))
    profile = SpecificationQualityProfile(completeness, verifiability, unambiguity)

    for forbidden in ("score", "value", "overall_score", "file_quality_score", "state"):
        assert not hasattr(profile, forbidden)

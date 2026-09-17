"""Replaceable boundary and production orchestration for AGG-MVP-001 specification aggregation."""

from fractions import Fraction
from typing import Iterable, Sequence, cast

from .domain import (
    CharacteristicAssessment,
    CharacteristicAssessmentState,
    CharacteristicId,
    RequirementQualityProfile,
    SpecificationCharacteristicAggregate,
    SpecificationQualityProfile,
)
from .domain.specification_profile import AGGREGATION_RULE_ID


class SpecificationQualityAggregator:
    """Apply AGG-MVP-001 identically and independently to each characteristic."""

    def aggregate(
        self, profiles: Iterable[RequirementQualityProfile]
    ) -> SpecificationQualityProfile:
        materialized = tuple(profiles)

        return SpecificationQualityProfile(
            completeness=self._aggregate_characteristic(
                CharacteristicId.COMPLETENESS,
                tuple(profile.completeness for profile in materialized),
            ),
            verifiability=self._aggregate_characteristic(
                CharacteristicId.VERIFIABILITY,
                tuple(profile.verifiability for profile in materialized),
            ),
            unambiguity=self._aggregate_characteristic(
                CharacteristicId.UNAMBIGUITY,
                tuple(profile.unambiguity for profile in materialized),
            ),
        )

    def _aggregate_characteristic(
        self,
        characteristic_id: CharacteristicId,
        assessments: Sequence[CharacteristicAssessment],
    ) -> SpecificationCharacteristicAggregate:
        computed = [
            assessment for assessment in assessments
            if assessment.state is CharacteristicAssessmentState.COMPUTED
        ]
        unknown = [
            assessment for assessment in assessments
            if assessment.state is CharacteristicAssessmentState.UNKNOWN
        ]
        not_applicable = [
            assessment for assessment in assessments
            if assessment.state is CharacteristicAssessmentState.NOT_APPLICABLE
        ]
        computed_count = len(computed)
        unknown_count = len(unknown)
        not_applicable_count = len(not_applicable)
        total_count = computed_count + unknown_count + not_applicable_count

        if computed_count >= 1:
            state = CharacteristicAssessmentState.COMPUTED
            computed_values = [cast(Fraction, assessment.value) for assessment in computed]
            value = sum(computed_values, start=Fraction(0)) / computed_count
        elif unknown_count >= 1:
            state = CharacteristicAssessmentState.UNKNOWN
            value = None
        else:
            state = CharacteristicAssessmentState.NOT_APPLICABLE
            value = None

        return SpecificationCharacteristicAggregate(
            characteristic_id=characteristic_id,
            state=state,
            value=value,
            computed_count=computed_count,
            unknown_count=unknown_count,
            not_applicable_count=not_applicable_count,
            total_count=total_count,
            aggregation_rule_id=AGGREGATION_RULE_ID,
        )

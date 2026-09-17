"""Approved Section 12 AGG-MVP-001 specification-level aggregate contract; no aggregation logic."""

from dataclasses import dataclass
from fractions import Fraction

from .assessment import CharacteristicAssessmentState, CharacteristicId

AGGREGATION_RULE_ID = "AGG-MVP-001"


@dataclass(frozen=True, slots=True)
class SpecificationCharacteristicAggregate:
    characteristic_id: CharacteristicId
    state: CharacteristicAssessmentState
    value: Fraction | None
    computed_count: int
    unknown_count: int
    not_applicable_count: int
    total_count: int
    aggregation_rule_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.characteristic_id, CharacteristicId):
            raise TypeError("characteristic_id must be an approved CharacteristicId")
        if not isinstance(self.state, CharacteristicAssessmentState):
            raise TypeError("state must be an approved CharacteristicAssessmentState")

        for name in ("computed_count", "unknown_count", "not_applicable_count", "total_count"):
            count = getattr(self, name)
            if not isinstance(count, int):
                raise TypeError(f"{name} must be an int")
            if count < 0:
                raise ValueError(f"{name} must be non-negative")

        if self.total_count != self.computed_count + self.unknown_count + self.not_applicable_count:
            raise ValueError(
                "total_count must equal computed_count + unknown_count + not_applicable_count"
            )

        if self.aggregation_rule_id != AGGREGATION_RULE_ID:
            raise ValueError(f"aggregation_rule_id must be {AGGREGATION_RULE_ID!r}")

        if self.state is CharacteristicAssessmentState.COMPUTED:
            if not isinstance(self.value, Fraction):
                raise ValueError("COMPUTED state requires a Fraction value")
            if not Fraction(0, 1) <= self.value <= Fraction(1, 1):
                raise ValueError("COMPUTED value must fall within [0, 1]")
            if self.computed_count < 1:
                raise ValueError("COMPUTED state requires computed_count >= 1")
        elif self.state is CharacteristicAssessmentState.UNKNOWN:
            if self.value is not None:
                raise ValueError("UNKNOWN state requires value to be None")
            if self.computed_count != 0:
                raise ValueError("UNKNOWN state requires computed_count == 0")
            if self.unknown_count < 1:
                raise ValueError("UNKNOWN state requires unknown_count >= 1")
        else:
            if self.value is not None:
                raise ValueError("NOT_APPLICABLE state requires value to be None")
            if self.computed_count != 0:
                raise ValueError("NOT_APPLICABLE state requires computed_count == 0")
            if self.unknown_count != 0:
                raise ValueError("NOT_APPLICABLE state requires unknown_count == 0")


@dataclass(frozen=True, slots=True)
class SpecificationQualityProfile:
    completeness: SpecificationCharacteristicAggregate
    verifiability: SpecificationCharacteristicAggregate
    unambiguity: SpecificationCharacteristicAggregate

    def __post_init__(self) -> None:
        for field_name, characteristic_id, value in (
            ("completeness", CharacteristicId.COMPLETENESS, self.completeness),
            ("verifiability", CharacteristicId.VERIFIABILITY, self.verifiability),
            ("unambiguity", CharacteristicId.UNAMBIGUITY, self.unambiguity),
        ):
            if not isinstance(value, SpecificationCharacteristicAggregate):
                raise TypeError(f"{field_name} must be a SpecificationCharacteristicAggregate")
            if value.characteristic_id is not characteristic_id:
                raise ValueError(
                    f"{field_name} must carry characteristic_id={characteristic_id.value}"
                )

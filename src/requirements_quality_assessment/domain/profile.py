"""Approved Section 11 requirement quality profile contract; no aggregation logic."""

from dataclasses import dataclass

from .assessment import CharacteristicAssessment, CharacteristicId


@dataclass(frozen=True, slots=True)
class RequirementQualityProfile:
    completeness: CharacteristicAssessment
    verifiability: CharacteristicAssessment
    unambiguity: CharacteristicAssessment

    def __post_init__(self) -> None:
        for field_name, characteristic_id, value in (
            ("completeness", CharacteristicId.COMPLETENESS, self.completeness),
            ("verifiability", CharacteristicId.VERIFIABILITY, self.verifiability),
            ("unambiguity", CharacteristicId.UNAMBIGUITY, self.unambiguity),
        ):
            if not isinstance(value, CharacteristicAssessment):
                raise TypeError(f"{field_name} must be a CharacteristicAssessment")
            if value.characteristic_id is not characteristic_id:
                raise ValueError(
                    f"{field_name} must carry characteristic_id={characteristic_id.value}"
                )

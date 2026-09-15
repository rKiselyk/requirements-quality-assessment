"""Partial, linked quantitative observation data without parsing or conversion."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from .core import FeatureId


class QuantitativeComponentName(str, Enum):
    METRIC = "METRIC"
    COMPARATOR = "COMPARATOR"
    VALUE = "VALUE"
    UNIT = "UNIT"
    CONTEXT = "CONTEXT"


class ComparatorLabel(str, Enum):
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    NOT_LESS_FREQUENT = "NOT_LESS_FREQUENT"
    UPPER_BOUND = "UPPER_BOUND"


class BoundaryInclusivity(str, Enum):
    INCLUSIVE = "INCLUSIVE"
    UNRESOLVED = "UNRESOLVED"


class UnitLabel(str, Enum):
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    PERCENT = "PERCENT"


def _check_refs(refs: tuple[str, ...], *, allow_empty: bool = False) -> None:
    if not isinstance(refs, tuple) or any(not isinstance(ref, str) for ref in refs):
        raise TypeError("evidence_refs must be a tuple of strings")
    if not allow_empty and not refs:
        raise ValueError("accepted observation or populated component requires evidence_refs")


@dataclass(frozen=True, slots=True)
class TextComponent:
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_refs(self.evidence_refs)


@dataclass(frozen=True, slots=True)
class ComparatorComponent:
    label: ComparatorLabel
    inclusivity: BoundaryInclusivity | None
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_refs(self.evidence_refs)
        if not isinstance(self.label, ComparatorLabel):
            raise TypeError("label must be a ComparatorLabel")
        required = {
            ComparatorLabel.LESS_THAN_OR_EQUAL: BoundaryInclusivity.INCLUSIVE,
            ComparatorLabel.GREATER_THAN_OR_EQUAL: BoundaryInclusivity.INCLUSIVE,
            ComparatorLabel.NOT_LESS_FREQUENT: None,
            ComparatorLabel.UPPER_BOUND: BoundaryInclusivity.UNRESOLVED,
        }[self.label]
        if self.inclusivity is not required:
            raise ValueError("inclusivity does not match the approved comparator meaning")


@dataclass(frozen=True, slots=True)
class NumericValueComponent:
    decimal_value: Decimal
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_refs(self.evidence_refs)
        if not isinstance(self.decimal_value, Decimal):
            raise TypeError("decimal_value must be a Decimal")


@dataclass(frozen=True, slots=True)
class UnitComponent:
    label: UnitLabel
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_refs(self.evidence_refs)
        if not isinstance(self.label, UnitLabel):
            raise TypeError("label must be an approved UnitLabel")


@dataclass(frozen=True, slots=True)
class QuantitativeConstraintObservation:
    feature_id: FeatureId
    metric: TextComponent | None
    comparator: ComparatorComponent | None
    value: NumericValueComponent | None
    unit: UnitComponent | None
    context: TextComponent | None
    unresolved_components: tuple[QuantitativeComponentName, ...]
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
            raise ValueError("quantitative observation requires quantitative_constraint feature_id")
        _check_refs(self.evidence_refs, allow_empty=True)
        if not isinstance(self.unresolved_components, tuple) or any(
            not isinstance(name, QuantitativeComponentName) for name in self.unresolved_components
        ):
            raise TypeError("unresolved_components must be a tuple of component names")
        if len(set(self.unresolved_components)) != len(self.unresolved_components):
            raise ValueError("unresolved component names must be unique")
        components = {
            QuantitativeComponentName.METRIC: (self.metric, TextComponent),
            QuantitativeComponentName.COMPARATOR: (self.comparator, ComparatorComponent),
            QuantitativeComponentName.VALUE: (self.value, NumericValueComponent),
            QuantitativeComponentName.UNIT: (self.unit, UnitComponent),
            QuantitativeComponentName.CONTEXT: (self.context, TextComponent),
        }
        for name, (component, expected_type) in components.items():
            if component is not None and not isinstance(component, expected_type):
                raise TypeError(f"{name.value} must be a {expected_type.__name__} or None")
            if component is not None and name in self.unresolved_components:
                raise ValueError(f"populated {name.value} cannot also be unresolved")
        if self.value is None or (self.comparator is None and self.unit is None):
            raise ValueError("accepted quantitative observation requires comparator + value or value + unit")
        component_refs = {
            ref for component, _ in components.values() if component is not None
            for ref in component.evidence_refs
        }
        if len(set(self.evidence_refs)) != len(self.evidence_refs) or set(self.evidence_refs) != component_refs:
            raise ValueError("top-level evidence_refs must be the de-duplicated component union")

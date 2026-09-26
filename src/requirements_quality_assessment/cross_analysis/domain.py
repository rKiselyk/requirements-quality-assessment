"""Immutable domain vocabulary for cross-requirement QB-v0.1 analysis.

``QB-SNAPSHOT-CANONICAL-001`` is the snapshot identity encoding.  It is a
UTF-8 JSON byte sequence made only from ordered, explicitly tagged arrays.
Every value has a type tag; enums use their exact value; and ``Decimal`` uses
its lossless ``as_tuple()`` sign, digit tuple, and exponent.  JSON is emitted
with no insignificant whitespace and with non-ASCII text preserved.  The
SHA-256 digest of those bytes is the snapshot ID.

The encoded input is limited to the ordered QB source/extraction/provenance
manifest, its validated count/order manifest, and the QB contract manifest.
Local C/V/U values and profiles, traces, explanation/report prose, paths,
timestamps, UUIDs, process data, and Python object identities are absent by
construction.  ``QB-RESULT-CANONICAL-001`` applies the same encoding rules to
stable cross-result identity.

This module validates supplied domain values.  It intentionally performs no
projection, resolution, normalization, comparison, conflict mathematics, or
aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from hashlib import sha256
import json
from typing import Any, ClassVar

from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorLabel,
    DetectionProcessingStatus,
    FeatureId,
    QuantitativeComponentName,
    UnitLabel,
)


SNAPSHOT_CANONICAL_VERSION = "QB-SNAPSHOT-CANONICAL-001"
RESULT_CANONICAL_VERSION = "QB-RESULT-CANONICAL-001"


def _require_identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


def _require_index(value: object, name: str, *, positive: bool = False) -> int:
    minimum = 1 if positive else 0
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        qualifier = "positive" if positive else "nonnegative"
        raise ValueError(f"{name} must be {qualifier}")
    return value


def _require_tuple(value: object, item_type: type, name: str) -> tuple[Any, ...]:
    if not isinstance(value, tuple) or any(not isinstance(item, item_type) for item in value):
        raise TypeError(f"{name} must be a tuple of {item_type.__name__}")
    return value


def _require_unique(value: tuple[Any, ...], name: str) -> None:
    if len(set(value)) != len(value):
        raise ValueError(f"{name} must not contain duplicates")


def _require_enum_order(value: tuple[Enum, ...], enum_type: type[Enum], name: str) -> None:
    rank = {item: index for index, item in enumerate(enum_type)}
    if tuple(rank[item] for item in value) != tuple(sorted(rank[item] for item in value)):
        raise ValueError(f"{name} must use approved deterministic order")


def _validate_comparator_shape(
    comparator: ComparatorLabel | None,
    inclusivity: BoundaryInclusivity | None,
) -> None:
    if comparator is None:
        if inclusivity is not None:
            raise ValueError("missing comparator cannot carry inclusivity")
        return
    required = {
        ComparatorLabel.LESS_THAN_OR_EQUAL: BoundaryInclusivity.INCLUSIVE,
        ComparatorLabel.GREATER_THAN_OR_EQUAL: BoundaryInclusivity.INCLUSIVE,
        ComparatorLabel.NOT_LESS_FREQUENT: None,
        ComparatorLabel.UPPER_BOUND: BoundaryInclusivity.UNRESOLVED,
    }[comparator]
    if inclusivity is not required:
        raise ValueError("inclusivity does not match the approved comparator meaning")


def _string(value: str) -> list[Any]:
    return ["string", value]


def _integer(value: int) -> list[Any]:
    return ["integer", str(value)]


def _optional(value: Any, encode: Any) -> list[Any]:
    return ["none"] if value is None else ["some", encode(value)]


def _enum(value: Enum) -> list[Any]:
    return ["enum", type(value).__name__, value.value]


def _decimal(value: Decimal) -> list[Any]:
    parts = value.as_tuple()
    return [
        "decimal",
        ["sign", str(parts.sign)],
        ["digits", *[str(digit) for digit in parts.digits]],
        ["exponent", str(parts.exponent)],
    ]


def _tuple(items: tuple[Any, ...], encode: Any) -> list[Any]:
    return ["tuple", *[encode(item) for item in items]]


def _record(name: str, *fields: tuple[str, Any]) -> list[Any]:
    return ["record", name, *[[field_name, value] for field_name, value in fields]]


def _canonical_bytes(root: list[Any]) -> bytes:
    return json.dumps(
        root,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


@dataclass(frozen=True, slots=True, order=True)
class AssessmentSnapshotId:
    value: str

    PREFIX: ClassVar[str] = "qb-snapshot-sha256:"

    def __post_init__(self) -> None:
        _validate_digest_id(self.value, self.PREFIX, "snapshot ID")

    @classmethod
    def from_bytes(cls, value: bytes) -> AssessmentSnapshotId:
        return cls(cls.PREFIX + sha256(value).hexdigest())

    def _canonical_node(self) -> list[Any]:
        return _record(type(self).__name__, ("value", _string(self.value)))


@dataclass(frozen=True, slots=True, order=True)
class CrossResultId:
    value: str

    PREFIX: ClassVar[str] = "qb-result-sha256:"

    def __post_init__(self) -> None:
        _validate_digest_id(self.value, self.PREFIX, "result ID")

    @classmethod
    def from_bytes(cls, value: bytes) -> CrossResultId:
        return cls(cls.PREFIX + sha256(value).hexdigest())

    def _canonical_node(self) -> list[Any]:
        return _record(type(self).__name__, ("value", _string(self.value)))


def _validate_digest_id(value: object, prefix: str, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    digest = value.removeprefix(prefix)
    if not value.startswith(prefix) or len(digest) != 64 or any(
        char not in "0123456789abcdef" for char in digest
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 identifier")


@dataclass(frozen=True, slots=True, order=True)
class ContractVersionDescriptor:
    contract_id: str
    version: str

    def __post_init__(self) -> None:
        _require_identifier(self.contract_id, "contract_id")
        _require_identifier(self.version, "version")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("contract_id", _string(self.contract_id)),
            ("version", _string(self.version)),
        )


@dataclass(frozen=True, slots=True)
class CrossAnalysisContractManifest:
    projection: ContractVersionDescriptor
    normalization: ContractVersionDescriptor
    comparison: ContractVersionDescriptor
    materiality: ContractVersionDescriptor
    aggregation: ContractVersionDescriptor
    coverage_profile: ContractVersionDescriptor

    def __post_init__(self) -> None:
        values = (
            self.projection,
            self.normalization,
            self.comparison,
            self.materiality,
            self.aggregation,
            self.coverage_profile,
        )
        if any(not isinstance(value, ContractVersionDescriptor) for value in values):
            raise TypeError("every contract manifest field must be a ContractVersionDescriptor")
        if len({value.contract_id for value in values}) != len(values):
            raise ValueError("contract manifest contract IDs must be unique")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("projection", self.projection._canonical_node()),
            ("normalization", self.normalization._canonical_node()),
            ("comparison", self.comparison._canonical_node()),
            ("materiality", self.materiality._canonical_node()),
            ("aggregation", self.aggregation._canonical_node()),
            ("coverage_profile", self.coverage_profile._canonical_node()),
        )


@dataclass(frozen=True, slots=True)
class CrossObservationRef:
    requirement_id: str
    feature_id: FeatureId
    observation_index: int

    def __post_init__(self) -> None:
        _require_identifier(self.requirement_id, "requirement_id")
        if self.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
            raise ValueError("cross observation refs require the quantitative feature")
        _require_index(self.observation_index, "observation_index")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("requirement_id", _string(self.requirement_id)),
            ("feature_id", _enum(self.feature_id)),
            ("observation_index", _integer(self.observation_index)),
        )


@dataclass(frozen=True, slots=True)
class CrossEvidenceRef:
    requirement_id: str
    evidence_id: str

    def __post_init__(self) -> None:
        _require_identifier(self.requirement_id, "requirement_id")
        _require_identifier(self.evidence_id, "evidence_id")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("requirement_id", _string(self.requirement_id)),
            ("evidence_id", _string(self.evidence_id)),
        )


@dataclass(frozen=True, slots=True)
class CrossDiagnosticRef:
    requirement_id: str
    feature_id: FeatureId
    diagnostic_index: int

    def __post_init__(self) -> None:
        _require_identifier(self.requirement_id, "requirement_id")
        if self.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
            raise ValueError("cross diagnostic refs require the quantitative feature")
        _require_index(self.diagnostic_index, "diagnostic_index")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("requirement_id", _string(self.requirement_id)),
            ("feature_id", _enum(self.feature_id)),
            ("diagnostic_index", _integer(self.diagnostic_index)),
        )


@dataclass(frozen=True, slots=True, order=True)
class RequirementOrderKey:
    source_order: int
    requirement_id: str

    def __post_init__(self) -> None:
        _require_index(self.source_order, "source_order")
        _require_identifier(self.requirement_id, "requirement_id")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("source_order", _integer(self.source_order)),
            ("requirement_id", _string(self.requirement_id)),
        )


@dataclass(frozen=True, slots=True, order=True)
class CrossObservationOrderKey:
    participant: RequirementOrderKey
    observation_index: int

    def __post_init__(self) -> None:
        if not isinstance(self.participant, RequirementOrderKey):
            raise TypeError("participant must be a RequirementOrderKey")
        _require_index(self.observation_index, "observation_index")


@dataclass(frozen=True, slots=True, order=True)
class CrossEvidenceOrderKey:
    participant_order: int
    start_offset: int
    end_offset: int
    evidence_id: str

    def __post_init__(self) -> None:
        _require_index(self.participant_order, "participant_order")
        _require_index(self.start_offset, "start_offset")
        _require_index(self.end_offset, "end_offset")
        if self.end_offset < self.start_offset:
            raise ValueError("evidence offsets must be ordered")
        _require_identifier(self.evidence_id, "evidence_id")


class CrossResultState(str, Enum):
    CONFIRMED_CONFLICT = "CONFIRMED_CONFLICT"
    COMPATIBLE_WITHIN_RULE = "COMPATIBLE_WITHIN_RULE"
    ASSESSMENT_UNRESOLVED = "ASSESSMENT_UNRESOLVED"
    OUTSIDE_V0_1_APPLICABILITY = "OUTSIDE_V0_1_APPLICABILITY"


class CrossUnresolvedReason(str, Enum):
    MISSING_METRIC = "MISSING_METRIC"
    UNRESOLVED_METRIC = "UNRESOLVED_METRIC"
    MISSING_CONTEXT = "MISSING_CONTEXT"
    UNRESOLVED_CONTEXT = "UNRESOLVED_CONTEXT"
    MISSING_UNIT = "MISSING_UNIT"
    MISSING_VALUE = "MISSING_VALUE"
    MISSING_COMPARATOR = "MISSING_COMPARATOR"
    UNRESOLVED_INCLUSIVITY = "UNRESOLVED_INCLUSIVITY"
    MATERIAL_UNRESOLVED_EXTRACTION = "MATERIAL_UNRESOLVED_EXTRACTION"


class OutsideApplicabilityReason(str, Enum):
    METRIC_MISMATCH = "METRIC_MISMATCH"
    CONTEXT_MISMATCH = "CONTEXT_MISMATCH"
    UNIT_MISMATCH = "UNIT_MISMATCH"
    COMPARATOR_OUTSIDE_PROFILE = "COMPARATOR_OUTSIDE_PROFILE"


class ConflictClass(str, Enum):
    LOGICAL_CONFLICT = "LOGICAL_CONFLICT"


class BoundedConflictSubtype(str, Enum):
    DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY = (
        "DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY"
    )


class CrossRelationKind(str, Enum):
    QUANTITATIVE_BOUND = "QUANTITATIVE_BOUND"


class BoundedNonClaimKey(str, Enum):
    NC_QB_BASE = "NC-QB-BASE"


@dataclass(frozen=True, slots=True)
class SnapshotEvidenceManifest:
    ref: CrossEvidenceRef
    feature_id: FeatureId
    text: str
    start_offset: int
    end_offset: int
    rule_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.ref, CrossEvidenceRef):
            raise TypeError("ref must be a CrossEvidenceRef")
        if self.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
            raise ValueError("QB snapshot Evidence must be quantitative")
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        _require_index(self.start_offset, "start_offset")
        _require_index(self.end_offset, "end_offset")
        if self.end_offset < self.start_offset or len(self.text) != self.end_offset - self.start_offset:
            raise ValueError("Evidence text and offsets must describe one ordered span")
        _require_identifier(self.rule_id, "rule_id")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("ref", self.ref._canonical_node()),
            ("feature_id", _enum(self.feature_id)),
            ("text", _string(self.text)),
            ("start_offset", _integer(self.start_offset)),
            ("end_offset", _integer(self.end_offset)),
            ("rule_id", _string(self.rule_id)),
        )


@dataclass(frozen=True, slots=True)
class SnapshotObservationManifest:
    ref: CrossObservationRef
    metric_evidence_refs: tuple[CrossEvidenceRef, ...]
    comparator: ComparatorLabel | None
    inclusivity: BoundaryInclusivity | None
    comparator_evidence_refs: tuple[CrossEvidenceRef, ...]
    value: Decimal | None
    value_evidence_refs: tuple[CrossEvidenceRef, ...]
    unit: UnitLabel | None
    unit_evidence_refs: tuple[CrossEvidenceRef, ...]
    context_evidence_refs: tuple[CrossEvidenceRef, ...]
    unresolved_components: tuple[QuantitativeComponentName, ...]
    evidence_refs: tuple[CrossEvidenceRef, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.ref, CrossObservationRef):
            raise TypeError("ref must be a CrossObservationRef")
        groups = (
            self.metric_evidence_refs,
            self.comparator_evidence_refs,
            self.value_evidence_refs,
            self.unit_evidence_refs,
            self.context_evidence_refs,
            self.evidence_refs,
        )
        for refs in groups:
            _require_tuple(refs, CrossEvidenceRef, "observation Evidence refs")
            _require_unique(refs, "observation Evidence refs")
            if any(ref.requirement_id != self.ref.requirement_id for ref in refs):
                raise ValueError("observation Evidence refs must have the observation owner")
        if self.comparator is not None and not isinstance(self.comparator, ComparatorLabel):
            raise TypeError("comparator must be a ComparatorLabel or None")
        if self.inclusivity is not None and not isinstance(self.inclusivity, BoundaryInclusivity):
            raise TypeError("inclusivity must be a BoundaryInclusivity or None")
        _validate_comparator_shape(self.comparator, self.inclusivity)
        if self.value is not None and not isinstance(self.value, Decimal):
            raise TypeError("value must be a Decimal or None")
        if self.unit is not None and not isinstance(self.unit, UnitLabel):
            raise TypeError("unit must be a UnitLabel or None")
        component_shapes = (
            (self.comparator, self.comparator_evidence_refs, "comparator"),
            (self.value, self.value_evidence_refs, "value"),
            (self.unit, self.unit_evidence_refs, "unit"),
        )
        for component, refs, name in component_shapes:
            if (component is None) != (not refs):
                raise ValueError(f"{name} and its Evidence refs must be present together")
        if self.value is None or (self.comparator is None and self.unit is None):
            raise ValueError(
                "snapshot observation requires value and either comparator or unit"
            )
        _require_tuple(
            self.unresolved_components,
            QuantitativeComponentName,
            "unresolved_components",
        )
        _require_unique(self.unresolved_components, "unresolved_components")
        populated = {
            QuantitativeComponentName.METRIC: bool(self.metric_evidence_refs),
            QuantitativeComponentName.COMPARATOR: self.comparator is not None,
            QuantitativeComponentName.VALUE: self.value is not None,
            QuantitativeComponentName.UNIT: self.unit is not None,
            QuantitativeComponentName.CONTEXT: bool(self.context_evidence_refs),
        }
        if any(populated[name] for name in self.unresolved_components):
            raise ValueError("a populated observation component cannot also be unresolved")
        component_union = {
            ref
            for refs in groups[:-1]
            for ref in refs
        }
        if set(self.evidence_refs) != component_union:
            raise ValueError("top-level Evidence refs must equal the component Evidence union")

    def _canonical_node(self) -> list[Any]:
        refs = lambda value: _tuple(value, lambda item: item._canonical_node())
        return _record(
            type(self).__name__,
            ("ref", self.ref._canonical_node()),
            ("metric_evidence_refs", refs(self.metric_evidence_refs)),
            ("comparator", _optional(self.comparator, _enum)),
            ("inclusivity", _optional(self.inclusivity, _enum)),
            ("comparator_evidence_refs", refs(self.comparator_evidence_refs)),
            ("value", _optional(self.value, _decimal)),
            ("value_evidence_refs", refs(self.value_evidence_refs)),
            ("unit", _optional(self.unit, _enum)),
            ("unit_evidence_refs", refs(self.unit_evidence_refs)),
            ("context_evidence_refs", refs(self.context_evidence_refs)),
            (
                "unresolved_components",
                _tuple(self.unresolved_components, _enum),
            ),
            ("evidence_refs", refs(self.evidence_refs)),
        )


@dataclass(frozen=True, slots=True)
class SnapshotDiagnosticManifest:
    ref: CrossDiagnosticRef
    code: str
    rule_id: str
    candidate_text: str | None
    start_offset: int | None
    end_offset: int | None

    def __post_init__(self) -> None:
        if not isinstance(self.ref, CrossDiagnosticRef):
            raise TypeError("ref must be a CrossDiagnosticRef")
        _require_identifier(self.code, "diagnostic code")
        _require_identifier(self.rule_id, "diagnostic rule_id")
        span = (self.candidate_text, self.start_offset, self.end_offset)
        if all(value is None for value in span):
            return
        if any(value is None for value in span):
            raise ValueError("diagnostic candidate text and offsets are all present or all absent")
        if not isinstance(self.candidate_text, str):
            raise TypeError("candidate_text must be a string or None")
        _require_index(self.start_offset, "diagnostic start_offset")
        _require_index(self.end_offset, "diagnostic end_offset")
        if self.end_offset < self.start_offset or len(self.candidate_text) != self.end_offset - self.start_offset:
            raise ValueError("diagnostic text and offsets must describe one ordered span")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("ref", self.ref._canonical_node()),
            ("code", _string(self.code)),
            ("rule_id", _string(self.rule_id)),
            ("candidate_text", _optional(self.candidate_text, _string)),
            ("start_offset", _optional(self.start_offset, _integer)),
            ("end_offset", _optional(self.end_offset, _integer)),
        )


@dataclass(frozen=True, slots=True)
class SnapshotRequirementManifest:
    requirement_id: str
    source_order: int
    source_line: int
    text: str
    processing_status: DetectionProcessingStatus
    observations: tuple[SnapshotObservationManifest, ...]
    evidence: tuple[SnapshotEvidenceManifest, ...]
    diagnostics: tuple[SnapshotDiagnosticManifest, ...]

    def __post_init__(self) -> None:
        _require_identifier(self.requirement_id, "requirement_id")
        _require_index(self.source_order, "source_order")
        _require_index(self.source_line, "source_line", positive=True)
        if not isinstance(self.text, str) or not self.text or self.text != self.text.strip():
            raise ValueError("requirement text must be non-empty and trimmed")
        if not isinstance(self.processing_status, DetectionProcessingStatus):
            raise TypeError("processing_status must be a DetectionProcessingStatus")
        _require_tuple(self.observations, SnapshotObservationManifest, "observations")
        _require_tuple(self.evidence, SnapshotEvidenceManifest, "evidence")
        _require_tuple(self.diagnostics, SnapshotDiagnosticManifest, "diagnostics")
        if self.processing_status is DetectionProcessingStatus.COMPLETE and self.diagnostics:
            raise ValueError("complete quantitative processing cannot have diagnostics")
        if self.processing_status is DetectionProcessingStatus.INCOMPLETE and not self.diagnostics:
            raise ValueError("incomplete quantitative processing requires diagnostics")
        if tuple(item.ref.observation_index for item in self.observations) != tuple(
            range(len(self.observations))
        ):
            raise ValueError("observation indexes must be contiguous source order")
        if tuple(item.ref.diagnostic_index for item in self.diagnostics) != tuple(
            range(len(self.diagnostics))
        ):
            raise ValueError("diagnostic indexes must be contiguous source order")
        children = (
            *(item.ref.requirement_id for item in self.observations),
            *(item.ref.requirement_id for item in self.evidence),
            *(item.ref.requirement_id for item in self.diagnostics),
        )
        if any(owner != self.requirement_id for owner in children):
            raise ValueError("snapshot child manifests must have the requirement owner")
        evidence_refs = tuple(item.ref for item in self.evidence)
        _require_unique(evidence_refs, "snapshot Evidence refs")
        evidence_set = set(evidence_refs)
        for item in self.evidence:
            if not 0 <= item.start_offset <= item.end_offset <= len(self.text):
                raise ValueError("Evidence span must be inside requirement text")
            if self.text[item.start_offset:item.end_offset] != item.text:
                raise ValueError("Evidence text must round-trip to requirement text")
        for observation in self.observations:
            if not set(observation.evidence_refs) <= evidence_set:
                raise ValueError("observation contains a dangling Evidence ref")
        for item in self.diagnostics:
            if item.candidate_text is not None and (
                item.end_offset > len(self.text)
                or self.text[item.start_offset:item.end_offset] != item.candidate_text
            ):
                raise ValueError("diagnostic text must round-trip to requirement text")

    @property
    def order_key(self) -> RequirementOrderKey:
        return RequirementOrderKey(self.source_order, self.requirement_id)

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("requirement_id", _string(self.requirement_id)),
            ("source_order", _integer(self.source_order)),
            ("source_line", _integer(self.source_line)),
            ("text", _string(self.text)),
            ("processing_status", _enum(self.processing_status)),
            (
                "observations",
                _tuple(self.observations, lambda item: item._canonical_node()),
            ),
            ("evidence", _tuple(self.evidence, lambda item: item._canonical_node())),
            (
                "diagnostics",
                _tuple(self.diagnostics, lambda item: item._canonical_node()),
            ),
        )


@dataclass(frozen=True, slots=True)
class RequirementCountManifest:
    requirement_id: str
    source_order: int
    observation_count: int
    evidence_count: int
    diagnostic_count: int

    def __post_init__(self) -> None:
        _require_identifier(self.requirement_id, "requirement_id")
        for name in (
            "source_order",
            "observation_count",
            "evidence_count",
            "diagnostic_count",
        ):
            _require_index(getattr(self, name), name)

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("requirement_id", _string(self.requirement_id)),
            ("source_order", _integer(self.source_order)),
            ("observation_count", _integer(self.observation_count)),
            ("evidence_count", _integer(self.evidence_count)),
            ("diagnostic_count", _integer(self.diagnostic_count)),
        )


@dataclass(frozen=True, slots=True)
class SnapshotCountManifest:
    requirement_count: int
    observation_count: int
    evidence_count: int
    diagnostic_count: int
    requirements: tuple[RequirementCountManifest, ...]

    def __post_init__(self) -> None:
        for name in (
            "requirement_count",
            "observation_count",
            "evidence_count",
            "diagnostic_count",
        ):
            _require_index(getattr(self, name), name)
        _require_tuple(self.requirements, RequirementCountManifest, "requirements")
        if self.requirement_count != len(self.requirements):
            raise ValueError("requirement_count must match requirement count entries")
        if tuple(item.source_order for item in self.requirements) != tuple(
            range(len(self.requirements))
        ):
            raise ValueError("count manifest source order must be contiguous")
        totals = (
            sum(item.observation_count for item in self.requirements),
            sum(item.evidence_count for item in self.requirements),
            sum(item.diagnostic_count for item in self.requirements),
        )
        if totals != (self.observation_count, self.evidence_count, self.diagnostic_count):
            raise ValueError("count manifest totals must match requirement entries")

    @classmethod
    def from_requirements(
        cls,
        requirements: tuple[SnapshotRequirementManifest, ...],
    ) -> SnapshotCountManifest:
        _require_tuple(requirements, SnapshotRequirementManifest, "requirements")
        entries = tuple(
            RequirementCountManifest(
                requirement_id=item.requirement_id,
                source_order=item.source_order,
                observation_count=len(item.observations),
                evidence_count=len(item.evidence),
                diagnostic_count=len(item.diagnostics),
            )
            for item in requirements
        )
        return cls(
            requirement_count=len(entries),
            observation_count=sum(item.observation_count for item in entries),
            evidence_count=sum(item.evidence_count for item in entries),
            diagnostic_count=sum(item.diagnostic_count for item in entries),
            requirements=entries,
        )

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("requirement_count", _integer(self.requirement_count)),
            ("observation_count", _integer(self.observation_count)),
            ("evidence_count", _integer(self.evidence_count)),
            ("diagnostic_count", _integer(self.diagnostic_count)),
            (
                "requirements",
                _tuple(self.requirements, lambda item: item._canonical_node()),
            ),
        )


@dataclass(frozen=True, slots=True)
class AssessmentSnapshot:
    requirements: tuple[SnapshotRequirementManifest, ...]
    contracts: CrossAnalysisContractManifest
    counts: SnapshotCountManifest
    snapshot_id: AssessmentSnapshotId = field(init=False)

    def __post_init__(self) -> None:
        _require_tuple(self.requirements, SnapshotRequirementManifest, "requirements")
        if not isinstance(self.contracts, CrossAnalysisContractManifest):
            raise TypeError("contracts must be a CrossAnalysisContractManifest")
        if not isinstance(self.counts, SnapshotCountManifest):
            raise TypeError("counts must be a SnapshotCountManifest")
        if tuple(item.source_order for item in self.requirements) != tuple(
            range(len(self.requirements))
        ):
            raise ValueError("snapshot requirements must be in contiguous source order")
        requirement_ids = tuple(item.requirement_id for item in self.requirements)
        _require_unique(requirement_ids, "snapshot requirement IDs")
        if self.counts != SnapshotCountManifest.from_requirements(self.requirements):
            raise ValueError("snapshot count/order manifest does not match requirements")
        object.__setattr__(
            self,
            "snapshot_id",
            AssessmentSnapshotId.from_bytes(self.canonical_bytes()),
        )

    def canonical_bytes(self) -> bytes:
        root = _record(
            SNAPSHOT_CANONICAL_VERSION,
            (
                "requirements",
                _tuple(self.requirements, lambda item: item._canonical_node()),
            ),
            ("contracts", self.contracts._canonical_node()),
            ("counts", self.counts._canonical_node()),
        )
        return _canonical_bytes(root)


@dataclass(frozen=True, slots=True)
class ComparisonOperand:
    snapshot_id: AssessmentSnapshotId
    observation_ref: CrossObservationRef
    normalized_metric: str | None
    normalized_context: str | None
    comparator: ComparatorLabel | None
    inclusivity: BoundaryInclusivity | None
    value: Decimal | None
    unit: UnitLabel | None

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, AssessmentSnapshotId):
            raise TypeError("snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.observation_ref, CrossObservationRef):
            raise TypeError("observation_ref must be a CrossObservationRef")
        for name in ("normalized_metric", "normalized_context"):
            value = getattr(self, name)
            if value is not None:
                _require_identifier(value, name)
        if self.comparator is not None and not isinstance(self.comparator, ComparatorLabel):
            raise TypeError("comparator must be a ComparatorLabel or None")
        if self.inclusivity is not None and not isinstance(self.inclusivity, BoundaryInclusivity):
            raise TypeError("inclusivity must be a BoundaryInclusivity or None")
        _validate_comparator_shape(self.comparator, self.inclusivity)
        if self.value is not None and not isinstance(self.value, Decimal):
            raise TypeError("value must be a Decimal or None")
        if self.unit is not None and not isinstance(self.unit, UnitLabel):
            raise TypeError("unit must be a UnitLabel or None")

    @property
    def complete(self) -> bool:
        return all(
            value is not None
            for value in (
                self.normalized_metric,
                self.normalized_context,
                self.comparator,
                self.inclusivity,
                self.value,
                self.unit,
            )
        )

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("snapshot_id", self.snapshot_id._canonical_node()),
            ("observation_ref", self.observation_ref._canonical_node()),
            ("normalized_metric", _optional(self.normalized_metric, _string)),
            ("normalized_context", _optional(self.normalized_context, _string)),
            ("comparator", _optional(self.comparator, _enum)),
            ("inclusivity", _optional(self.inclusivity, _enum)),
            ("value", _optional(self.value, _decimal)),
            ("unit", _optional(self.unit, _enum)),
        )


@dataclass(frozen=True, slots=True)
class ComparisonOperands:
    left: ComparisonOperand
    right: ComparisonOperand

    def __post_init__(self) -> None:
        if not isinstance(self.left, ComparisonOperand) or not isinstance(
            self.right, ComparisonOperand
        ):
            raise TypeError("left and right must be ComparisonOperand values")
        if self.left.snapshot_id != self.right.snapshot_id:
            raise ValueError("comparison operands cannot cross snapshots")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("left", self.left._canonical_node()),
            ("right", self.right._canonical_node()),
        )


@dataclass(frozen=True, slots=True)
class ComparisonKey:
    normalized_metric: str
    normalized_context: str
    unit: UnitLabel

    def __post_init__(self) -> None:
        _require_identifier(self.normalized_metric, "normalized_metric")
        _require_identifier(self.normalized_context, "normalized_context")
        if not isinstance(self.unit, UnitLabel):
            raise TypeError("unit must be a UnitLabel")

    def _canonical_node(self) -> list[Any]:
        return _record(
            type(self).__name__,
            ("normalized_metric", _string(self.normalized_metric)),
            ("normalized_context", _string(self.normalized_context)),
            ("unit", _enum(self.unit)),
        )


@dataclass(frozen=True, slots=True, order=True)
class CrossResultOrderKey:
    earlier_requirement_order: int
    later_requirement_order: int
    left_observation_index: int
    right_observation_index: int
    relation_kind: str
    comparison_contract_id: str
    result_id: str

    def __post_init__(self) -> None:
        for name in (
            "earlier_requirement_order",
            "later_requirement_order",
            "left_observation_index",
            "right_observation_index",
        ):
            _require_index(getattr(self, name), name)
        if self.earlier_requirement_order >= self.later_requirement_order:
            raise ValueError("result requirement order must be canonical and distinct")
        _require_identifier(self.relation_kind, "relation_kind")
        _require_identifier(self.comparison_contract_id, "comparison_contract_id")
        _validate_digest_id(self.result_id, CrossResultId.PREFIX, "result ID")


@dataclass(frozen=True, slots=True)
class CrossRequirementResult:
    snapshot_id: AssessmentSnapshotId
    participants: tuple[RequirementOrderKey, RequirementOrderKey]
    observation_refs: tuple[CrossObservationRef, CrossObservationRef]
    operands: ComparisonOperands
    state: CrossResultState
    comparison_contract: ContractVersionDescriptor
    coverage_profile: ContractVersionDescriptor
    relation_kind: CrossRelationKind
    evidence_refs: tuple[CrossEvidenceRef, ...]
    diagnostic_refs: tuple[CrossDiagnosticRef, ...]
    comparison_key: ComparisonKey | None
    conflict_class: ConflictClass | None
    conflict_subtype: BoundedConflictSubtype | None
    unresolved_reasons: tuple[CrossUnresolvedReason, ...]
    outside_reasons: tuple[OutsideApplicabilityReason, ...]
    non_claim_keys: tuple[BoundedNonClaimKey, ...]
    result_id: CrossResultId = field(init=False)

    def __post_init__(self) -> None:
        self._validate_common()
        self._validate_state_matrix()
        object.__setattr__(
            self,
            "result_id",
            CrossResultId.from_bytes(self.canonical_identity_bytes()),
        )

    def _validate_common(self) -> None:
        if not isinstance(self.snapshot_id, AssessmentSnapshotId):
            raise TypeError("snapshot_id must be an AssessmentSnapshotId")
        if (
            not isinstance(self.participants, tuple)
            or len(self.participants) != 2
            or any(not isinstance(item, RequirementOrderKey) for item in self.participants)
        ):
            raise TypeError("participants must contain two RequirementOrderKey values")
        left_participant, right_participant = self.participants
        if left_participant.source_order >= right_participant.source_order:
            raise ValueError("participants must be distinct and canonically source ordered")
        if left_participant.requirement_id == right_participant.requirement_id:
            raise ValueError("cross results cannot contain a self-pair")
        if (
            not isinstance(self.observation_refs, tuple)
            or len(self.observation_refs) != 2
            or any(not isinstance(item, CrossObservationRef) for item in self.observation_refs)
        ):
            raise TypeError("observation_refs must contain two CrossObservationRef values")
        if tuple(item.requirement_id for item in self.observation_refs) != tuple(
            item.requirement_id for item in self.participants
        ):
            raise ValueError("observation owners must match canonical participants")
        if not isinstance(self.operands, ComparisonOperands):
            raise TypeError("operands must be ComparisonOperands")
        if self.operands.left.snapshot_id != self.snapshot_id:
            raise ValueError("result and operands cannot cross snapshots")
        if (self.operands.left.observation_ref, self.operands.right.observation_ref) != (
            self.observation_refs
        ):
            raise ValueError("operand refs must match result observation refs")
        if not isinstance(self.state, CrossResultState):
            raise TypeError("state must be a CrossResultState")
        if not isinstance(self.comparison_contract, ContractVersionDescriptor):
            raise TypeError("comparison_contract must be a ContractVersionDescriptor")
        if not isinstance(self.coverage_profile, ContractVersionDescriptor):
            raise TypeError("coverage_profile must be a ContractVersionDescriptor")
        if not isinstance(self.relation_kind, CrossRelationKind):
            raise TypeError("relation_kind must be a CrossRelationKind")
        _require_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        _require_tuple(self.diagnostic_refs, CrossDiagnosticRef, "diagnostic_refs")
        _require_unique(self.evidence_refs, "evidence_refs")
        _require_unique(self.diagnostic_refs, "diagnostic_refs")
        owners = {item.requirement_id for item in self.participants}
        if any(item.requirement_id not in owners for item in self.evidence_refs):
            raise ValueError("Evidence refs must be owned by a participant")
        if any(item.requirement_id not in owners for item in self.diagnostic_refs):
            raise ValueError("diagnostic refs must be owned by a participant")
        if {item.requirement_id for item in self.evidence_refs} != owners:
            raise ValueError("every cross result requires Evidence from both participants")
        owner_rank = {item.requirement_id: index for index, item in enumerate(self.participants)}
        if tuple(owner_rank[item.requirement_id] for item in self.evidence_refs) != tuple(
            sorted(owner_rank[item.requirement_id] for item in self.evidence_refs)
        ):
            raise ValueError("Evidence refs must be grouped in participant order")
        diagnostic_order = tuple(
            (owner_rank[item.requirement_id], item.diagnostic_index)
            for item in self.diagnostic_refs
        )
        if diagnostic_order != tuple(sorted(diagnostic_order)):
            raise ValueError("diagnostic refs must be in participant/source order")
        if self.comparison_key is not None and not isinstance(self.comparison_key, ComparisonKey):
            raise TypeError("comparison_key must be a ComparisonKey or None")
        if self.conflict_class is not None and not isinstance(self.conflict_class, ConflictClass):
            raise TypeError("conflict_class must be a ConflictClass or None")
        if self.conflict_subtype is not None and not isinstance(
            self.conflict_subtype, BoundedConflictSubtype
        ):
            raise TypeError("conflict_subtype must be a BoundedConflictSubtype or None")
        _require_tuple(self.unresolved_reasons, CrossUnresolvedReason, "unresolved_reasons")
        _require_tuple(self.outside_reasons, OutsideApplicabilityReason, "outside_reasons")
        _require_tuple(self.non_claim_keys, BoundedNonClaimKey, "non_claim_keys")
        _require_unique(self.unresolved_reasons, "unresolved_reasons")
        _require_unique(self.outside_reasons, "outside_reasons")
        _require_enum_order(
            self.unresolved_reasons,
            CrossUnresolvedReason,
            "unresolved_reasons",
        )
        _require_enum_order(
            self.outside_reasons,
            OutsideApplicabilityReason,
            "outside_reasons",
        )
        if self.non_claim_keys != (BoundedNonClaimKey.NC_QB_BASE,):
            raise ValueError("QB-v0.1 results require exactly NC-QB-BASE")

    def _validate_state_matrix(self) -> None:
        complete = self.state in {
            CrossResultState.CONFIRMED_CONFLICT,
            CrossResultState.COMPATIBLE_WITHIN_RULE,
        }
        if complete:
            if self.comparison_key is None or not self.operands.left.complete or not self.operands.right.complete:
                raise ValueError("confirmed or compatible results require complete operands and key")
            if self.unresolved_reasons or self.outside_reasons:
                raise ValueError("complete results cannot carry unresolved or outside reasons")
            supported = {
                ComparatorLabel.LESS_THAN_OR_EQUAL,
                ComparatorLabel.GREATER_THAN_OR_EQUAL,
            }
            if (
                self.operands.left.comparator not in supported
                or self.operands.right.comparator not in supported
            ):
                raise ValueError("confirmed or compatible results require supported comparators")
        elif self.comparison_key is not None:
            raise ValueError("unresolved or outside results cannot carry a complete comparison key")

        if self.state is CrossResultState.CONFIRMED_CONFLICT:
            if self.conflict_class is not ConflictClass.LOGICAL_CONFLICT:
                raise ValueError("confirmed conflict requires the logical conflict class")
            if self.conflict_subtype is not BoundedConflictSubtype.DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY:
                raise ValueError("confirmed conflict requires the bounded conflict subtype")
        elif self.conflict_class is not None or self.conflict_subtype is not None:
            raise ValueError("only confirmed conflicts may carry conflict classification")

        if self.state is CrossResultState.ASSESSMENT_UNRESOLVED:
            if not self.unresolved_reasons or self.outside_reasons:
                raise ValueError("unresolved results require only typed unresolved reasons")
            if CrossUnresolvedReason.MATERIAL_UNRESOLVED_EXTRACTION in self.unresolved_reasons:
                raise ValueError(
                    "material unresolved extraction is aggregate-level, not pair-result evidence"
                )
        elif self.unresolved_reasons:
            raise ValueError("unresolved reasons belong only to ASSESSMENT_UNRESOLVED")

        if self.state is CrossResultState.OUTSIDE_V0_1_APPLICABILITY:
            if not self.outside_reasons or self.unresolved_reasons:
                raise ValueError("outside results require only typed outside reasons")
        elif self.outside_reasons:
            raise ValueError("outside reasons belong only to OUTSIDE_V0_1_APPLICABILITY")

    @classmethod
    def confirmed_conflict(cls, **values: Any) -> CrossRequirementResult:
        return cls(
            state=CrossResultState.CONFIRMED_CONFLICT,
            conflict_class=ConflictClass.LOGICAL_CONFLICT,
            conflict_subtype=BoundedConflictSubtype.DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY,
            unresolved_reasons=(),
            outside_reasons=(),
            **values,
        )

    @classmethod
    def compatible_within_rule(cls, **values: Any) -> CrossRequirementResult:
        return cls(
            state=CrossResultState.COMPATIBLE_WITHIN_RULE,
            conflict_class=None,
            conflict_subtype=None,
            unresolved_reasons=(),
            outside_reasons=(),
            **values,
        )

    @classmethod
    def assessment_unresolved(
        cls,
        *,
        unresolved_reasons: tuple[CrossUnresolvedReason, ...],
        **values: Any,
    ) -> CrossRequirementResult:
        return cls(
            state=CrossResultState.ASSESSMENT_UNRESOLVED,
            comparison_key=None,
            conflict_class=None,
            conflict_subtype=None,
            unresolved_reasons=unresolved_reasons,
            outside_reasons=(),
            **values,
        )

    @classmethod
    def outside_v0_1_applicability(
        cls,
        *,
        outside_reasons: tuple[OutsideApplicabilityReason, ...],
        **values: Any,
    ) -> CrossRequirementResult:
        return cls(
            state=CrossResultState.OUTSIDE_V0_1_APPLICABILITY,
            comparison_key=None,
            conflict_class=None,
            conflict_subtype=None,
            unresolved_reasons=(),
            outside_reasons=outside_reasons,
            **values,
        )

    def canonical_identity_bytes(self) -> bytes:
        enum_tuple = lambda value: _tuple(value, _enum)
        root = _record(
            RESULT_CANONICAL_VERSION,
            ("snapshot_id", self.snapshot_id._canonical_node()),
            (
                "participants",
                _tuple(self.participants, lambda item: item._canonical_node()),
            ),
            (
                "observation_refs",
                _tuple(self.observation_refs, lambda item: item._canonical_node()),
            ),
            ("operands", self.operands._canonical_node()),
            ("state", _enum(self.state)),
            ("comparison_contract", self.comparison_contract._canonical_node()),
            ("coverage_profile", self.coverage_profile._canonical_node()),
            ("relation_kind", _enum(self.relation_kind)),
            (
                "evidence_refs",
                _tuple(self.evidence_refs, lambda item: item._canonical_node()),
            ),
            (
                "diagnostic_refs",
                _tuple(self.diagnostic_refs, lambda item: item._canonical_node()),
            ),
            (
                "comparison_key",
                _optional(self.comparison_key, lambda item: item._canonical_node()),
            ),
            ("conflict_class", _optional(self.conflict_class, _enum)),
            ("conflict_subtype", _optional(self.conflict_subtype, _enum)),
            ("unresolved_reasons", enum_tuple(self.unresolved_reasons)),
            ("outside_reasons", enum_tuple(self.outside_reasons)),
            ("non_claim_keys", enum_tuple(self.non_claim_keys)),
        )
        return _canonical_bytes(root)

    @property
    def order_key(self) -> CrossResultOrderKey:
        left, right = self.participants
        left_ref, right_ref = self.observation_refs
        return CrossResultOrderKey(
            earlier_requirement_order=left.source_order,
            later_requirement_order=right.source_order,
            left_observation_index=left_ref.observation_index,
            right_observation_index=right_ref.observation_index,
            relation_kind=self.relation_kind.value,
            comparison_contract_id=self.comparison_contract.contract_id,
            result_id=self.result_id.value,
        )

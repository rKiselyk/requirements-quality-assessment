"""Immutable Full Model v0.1 dynamic-evidence domain contracts."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from ..domain import (
    BoundaryInclusivity, ComparatorLabel, DetectionProcessingStatus, UnitLabel,
)
from ..metrics import (
    ArtifactRef, AssessmentRef, AssessmentSnapshotId, ContractRef,
    CrossDiagnosticRef, CrossEvidenceRef, CrossObservationRef,
    RequirementSubjectRef, RuleRef, RuleVersionAuthority,
)


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


def _typed_tuple(value: object, item_type: type, name: str) -> None:
    if not isinstance(value, tuple) or any(not isinstance(item, item_type) for item in value):
        raise TypeError(f"{name} must be a tuple of {item_type.__name__} values")


class FullModelStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"
    UNRESOLVED = "UNRESOLVED"
    UNSUPPORTED = "UNSUPPORTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Applicability(str, Enum):
    APPLICABLE = "APPLICABLE"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class DynamicMetricId(str, Enum):
    RESPONSE_TIME = "DYN.RESPONSE_TIME"


class ObservationSourceKind(str, Enum):
    DETERMINISTIC_FIXTURE = "DETERMINISTIC_FIXTURE"


class DynamicNumericRepresentation(str, Enum):
    EXACT_DECIMAL = "EXACT_DECIMAL"


class ConformanceOutcome(str, Enum):
    CONFORMS = "CONFORMS"
    DOES_NOT_CONFORM = "DOES_NOT_CONFORM"


class DynamicEvidenceReason(str, Enum):
    NO_APPLICABLE_RESPONSE_TIME_CRITERION = "NO_APPLICABLE_RESPONSE_TIME_CRITERION"
    SOURCE_ASSESSMENT_UNAVAILABLE = "SOURCE_ASSESSMENT_UNAVAILABLE"
    SOURCE_OBSERVATION_SELECTION_UNRESOLVED = "SOURCE_OBSERVATION_SELECTION_UNRESOLVED"
    METRIC_IDENTITY_UNRESOLVED = "METRIC_IDENTITY_UNRESOLVED"
    COMPARATOR_UNRESOLVED = "COMPARATOR_UNRESOLVED"
    UNIT_UNRESOLVED = "UNIT_UNRESOLVED"
    CONTEXT_IDENTITY_UNRESOLVED = "CONTEXT_IDENTITY_UNRESOLVED"
    PROVENANCE_UNRESOLVED = "PROVENANCE_UNRESOLVED"
    COMPARATOR_UNSUPPORTED = "COMPARATOR_UNSUPPORTED"
    UNIT_UNSUPPORTED = "UNIT_UNSUPPORTED"
    CONTEXT_UNSUPPORTED = "CONTEXT_UNSUPPORTED"
    OBSERVATION_NOT_COLLECTED = "OBSERVATION_NOT_COLLECTED"
    OBSERVATION_IDENTITY_UNRESOLVED = "OBSERVATION_IDENTITY_UNRESOLVED"
    OBSERVATION_SOURCE_UNRESOLVED = "OBSERVATION_SOURCE_UNRESOLVED"
    OBSERVATION_NUMERIC_UNSUPPORTED = "OBSERVATION_NUMERIC_UNSUPPORTED"


FULL_MODEL_CONTRACT_REF = ContractRef("FULL-MODEL-V0.1-CONTRACT", "1")
DYNAMIC_CONTRACT_REF = ContractRef("FULL-MODEL-V0.1-DYNAMIC-EVIDENCE", "1")
DYNAMIC_METRIC_REGISTRY_REF = ContractRef("FULL-MODEL-V0.1-DYNAMIC-METRICS", "1")
QB_NORMALIZATION_CONTRACT_REF = ContractRef("QB-NORMALIZATION", "1")
BINDING_RULE_REF = RuleRef(
    "DYN-CRITERION-RESPONSE-TIME-001", "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)
EVALUATOR_RULE_REF = RuleRef(
    "DYN-CONFORMANCE-RESPONSE-TIME-001", "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)
SUPPORTED_METRIC_TEXT = "час відгуку"
SUPPORTED_CONTEXT_TEXT = "при 500 одночасних користувачах"


@dataclass(frozen=True, slots=True, order=True)
class ProductRef:
    product_id: str
    product_version: str

    def __post_init__(self) -> None:
        _identifier(self.product_id, "product_id")
        _identifier(self.product_version, "product_version")


@dataclass(frozen=True, slots=True, order=True)
class EnvironmentRef:
    environment_id: str
    environment_version: str

    def __post_init__(self) -> None:
        _identifier(self.environment_id, "environment_id")
        _identifier(self.environment_version, "environment_version")


@dataclass(frozen=True, slots=True, order=True)
class ObservationCollectionRef:
    collection_id: str
    collection_version: str
    product_ref: ProductRef
    environment_ref: EnvironmentRef
    source_kind: ObservationSourceKind

    def __post_init__(self) -> None:
        _identifier(self.collection_id, "collection_id")
        _identifier(self.collection_version, "collection_version")
        if not isinstance(self.product_ref, ProductRef):
            raise TypeError("product_ref must be a ProductRef")
        if not isinstance(self.environment_ref, EnvironmentRef):
            raise TypeError("environment_ref must be an EnvironmentRef")
        if not isinstance(self.source_kind, ObservationSourceKind):
            raise TypeError("source_kind must be an ObservationSourceKind")


@dataclass(frozen=True, slots=True, order=True)
class ObservationSlotRef:
    collection_ref: ObservationCollectionRef
    fixture_sequence: int

    def __post_init__(self) -> None:
        if not isinstance(self.collection_ref, ObservationCollectionRef):
            raise TypeError("collection_ref must be an ObservationCollectionRef")
        if type(self.fixture_sequence) is not int or self.fixture_sequence < 0:
            raise ValueError("fixture_sequence must be a non-negative integer")


@dataclass(frozen=True, slots=True, order=True)
class CriterionContextIdentity:
    normalization_contract_ref: ContractRef
    normalized_text: str

    def __post_init__(self) -> None:
        if self.normalization_contract_ref != QB_NORMALIZATION_CONTRACT_REF:
            raise ValueError("context identity requires QB-NORMALIZATION / 1")
        _identifier(self.normalized_text, "normalized_text")


@dataclass(frozen=True, slots=True, order=True)
class DynamicMetricRef:
    registry_ref: ContractRef
    metric_id: str
    normalization_contract_ref: ContractRef
    normalized_source_metric: str

    def __post_init__(self) -> None:
        if not isinstance(self.registry_ref, ContractRef):
            raise TypeError("registry_ref must be a ContractRef")
        _identifier(self.metric_id, "metric_id")
        if self.normalization_contract_ref != QB_NORMALIZATION_CONTRACT_REF:
            raise ValueError("metric identity requires QB-NORMALIZATION / 1")
        _identifier(self.normalized_source_metric, "normalized_source_metric")


RESPONSE_TIME_METRIC_REF = DynamicMetricRef(
    DYNAMIC_METRIC_REGISTRY_REF, DynamicMetricId.RESPONSE_TIME.value,
    QB_NORMALIZATION_CONTRACT_REF, SUPPORTED_METRIC_TEXT,
)
SUPPORTED_CONTEXT_IDENTITY = CriterionContextIdentity(
    QB_NORMALIZATION_CONTRACT_REF, SUPPORTED_CONTEXT_TEXT,
)


@dataclass(frozen=True, slots=True, order=True)
class CriterionBindingId:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    requirement_subject_ref: RequirementSubjectRef
    source_snapshot_id: AssessmentSnapshotId
    source_observation_ref: CrossObservationRef | None
    binding_rule_ref: RuleRef

    def __post_init__(self) -> None:
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("source assessment must name the binding artifact")
        if self.requirement_subject_ref.artifact_ref != self.artifact_ref:
            raise ValueError("requirement subject must name the binding artifact")
        if self.source_observation_ref is not None and (
            self.source_observation_ref.requirement_id
            != self.requirement_subject_ref.requirement_id
        ):
            raise ValueError("source observation must name the binding requirement")
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.binding_rule_ref, RuleRef):
            raise TypeError("binding_rule_ref must be a RuleRef")


@dataclass(frozen=True, slots=True, order=True)
class CriterionId:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    requirement_subject_ref: RequirementSubjectRef
    source_snapshot_id: AssessmentSnapshotId
    source_observation_ref: CrossObservationRef
    binding_rule_ref: RuleRef

    def __post_init__(self) -> None:
        CriterionBindingId(
            self.artifact_ref, self.source_assessment_ref,
            self.requirement_subject_ref, self.source_snapshot_id,
            self.source_observation_ref, self.binding_rule_ref,
        )


@dataclass(frozen=True, slots=True)
class CriterionProvenance:
    requirement_subject_ref: RequirementSubjectRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    source_observation_ref: CrossObservationRef
    source_processing_status: DetectionProcessingStatus
    source_component_refs: tuple[CrossEvidenceRef, ...]
    evidence_refs: tuple[CrossEvidenceRef, ...]
    diagnostic_refs: tuple[CrossDiagnosticRef, ...]
    source_rule_refs: tuple[RuleRef, ...]
    normalization_contract_ref: ContractRef
    binding_rule_ref: RuleRef

    def __post_init__(self) -> None:
        _typed_tuple(self.source_component_refs, CrossEvidenceRef, "source_component_refs")
        _typed_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        _typed_tuple(self.diagnostic_refs, CrossDiagnosticRef, "diagnostic_refs")
        _typed_tuple(self.source_rule_refs, RuleRef, "source_rule_refs")
        if not self.source_component_refs or not self.evidence_refs:
            raise ValueError("criterion provenance requires source evidence")
        if len(set(self.evidence_refs)) != len(self.evidence_refs):
            raise ValueError("criterion evidence_refs must be unique")
        if self.normalization_contract_ref != QB_NORMALIZATION_CONTRACT_REF:
            raise ValueError("criterion provenance requires QB normalization")


@dataclass(frozen=True, slots=True)
class CriterionBindingProvenance:
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    requirement_subject_ref: RequirementSubjectRef
    source_observation_ref: CrossObservationRef | None
    binding_rule_ref: RuleRef
    evidence_refs: tuple[CrossEvidenceRef, ...] = ()
    diagnostic_refs: tuple[CrossDiagnosticRef, ...] = ()

    def __post_init__(self) -> None:
        _typed_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        _typed_tuple(self.diagnostic_refs, CrossDiagnosticRef, "diagnostic_refs")


@dataclass(frozen=True, slots=True)
class QuantitativeCriterion:
    criterion_id: CriterionId
    requirement_subject_ref: RequirementSubjectRef
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    source_observation_ref: CrossObservationRef
    metric_ref: DynamicMetricRef
    comparator: ComparatorLabel
    inclusivity: BoundaryInclusivity
    bound: Decimal
    unit: UnitLabel
    context_identity: CriterionContextIdentity
    provenance: CriterionProvenance
    binding_rule_ref: RuleRef

    def __post_init__(self) -> None:
        expected = CriterionId(
            self.artifact_ref, self.source_assessment_ref,
            self.requirement_subject_ref, self.source_snapshot_id,
            self.source_observation_ref, self.binding_rule_ref,
        )
        if self.criterion_id != expected:
            raise ValueError("criterion_id must match the criterion source identity")
        if not isinstance(self.metric_ref, DynamicMetricRef):
            raise TypeError("metric_ref must be a DynamicMetricRef")
        if not isinstance(self.comparator, ComparatorLabel):
            raise TypeError("comparator must be a ComparatorLabel")
        if not isinstance(self.inclusivity, BoundaryInclusivity):
            raise TypeError("inclusivity must be a BoundaryInclusivity")
        if not isinstance(self.bound, Decimal):
            raise TypeError("bound must be a Decimal")
        if not isinstance(self.unit, UnitLabel):
            raise TypeError("unit must be a UnitLabel")
        if not isinstance(self.context_identity, CriterionContextIdentity):
            raise TypeError("context_identity must be a CriterionContextIdentity")
        if self.provenance.source_observation_ref != self.source_observation_ref:
            raise ValueError("criterion provenance must name its source observation")


_NONVALUE_APPLICABILITY = {
    FullModelStatus.UNAVAILABLE: {Applicability.APPLICABLE, Applicability.UNKNOWN},
    FullModelStatus.UNKNOWN: {Applicability.APPLICABLE, Applicability.UNKNOWN},
    FullModelStatus.UNRESOLVED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
    FullModelStatus.UNSUPPORTED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
    FullModelStatus.NOT_APPLICABLE: {Applicability.NOT_APPLICABLE},
}


@dataclass(frozen=True, slots=True)
class CriterionBindingResult:
    binding_id: CriterionBindingId
    status: FullModelStatus
    applicability: Applicability
    criterion: QuantitativeCriterion | None
    source_observation_ref: CrossObservationRef | None
    reasons: tuple[DynamicEvidenceReason, ...]
    provenance: CriterionBindingProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.status, FullModelStatus):
            raise TypeError("status must be a FullModelStatus")
        if not isinstance(self.applicability, Applicability):
            raise TypeError("applicability must be an Applicability")
        _typed_tuple(self.reasons, DynamicEvidenceReason, "reasons")
        if self.source_observation_ref != self.binding_id.source_observation_ref:
            raise ValueError("binding source observation references must agree")
        if self.status is FullModelStatus.AVAILABLE:
            if self.applicability is not Applicability.APPLICABLE or self.criterion is None:
                raise ValueError("available binding requires an applicable criterion")
            if self.reasons:
                raise ValueError("available binding cannot carry non-value reasons")
        else:
            if self.applicability not in _NONVALUE_APPLICABILITY[self.status]:
                raise ValueError("binding status/applicability combination is invalid")
            if self.status is not FullModelStatus.UNSUPPORTED and self.criterion is not None:
                raise ValueError("only an unsupported binding may preserve a criterion")


@dataclass(frozen=True, slots=True, order=True)
class DynamicObservationId:
    collection_ref: ObservationCollectionRef
    fixture_sequence: int

    def __post_init__(self) -> None:
        ObservationSlotRef(self.collection_ref, self.fixture_sequence)


@dataclass(frozen=True, slots=True)
class DynamicObservationProvenance:
    product_ref: ProductRef
    source_kind: ObservationSourceKind
    collection_ref: ObservationCollectionRef
    environment_ref: EnvironmentRef
    fixture_sequence: int
    source_record_ref: str
    declared_metric_ref: DynamicMetricRef
    declared_unit: UnitLabel
    declared_context_identity: CriterionContextIdentity
    numeric_representation: DynamicNumericRepresentation

    def __post_init__(self) -> None:
        _identifier(self.source_record_ref, "source_record_ref")
        if self.collection_ref.product_ref != self.product_ref:
            raise ValueError("provenance product must match collection")
        if self.collection_ref.environment_ref != self.environment_ref:
            raise ValueError("provenance environment must match collection")
        if self.collection_ref.source_kind is not self.source_kind:
            raise ValueError("provenance source kind must match collection")
        ObservationSlotRef(self.collection_ref, self.fixture_sequence)


@dataclass(frozen=True, slots=True)
class DynamicObservation:
    observation_id: DynamicObservationId
    slot_ref: ObservationSlotRef
    product_ref: ProductRef
    metric_ref: DynamicMetricRef
    observed_value: Decimal
    unit: UnitLabel
    context_identity: CriterionContextIdentity
    source_kind: ObservationSourceKind
    collection_ref: ObservationCollectionRef
    fixture_sequence: int
    collected_at: None
    provenance: DynamicObservationProvenance

    def __post_init__(self) -> None:
        expected_slot = ObservationSlotRef(self.collection_ref, self.fixture_sequence)
        expected_id = DynamicObservationId(self.collection_ref, self.fixture_sequence)
        if self.slot_ref != expected_slot or self.observation_id != expected_id:
            raise ValueError("observation ID and slot must match collection and sequence")
        if self.collection_ref.product_ref != self.product_ref:
            raise ValueError("observation product must match collection product")
        if self.collection_ref.source_kind is not self.source_kind:
            raise ValueError("observation source kind must match collection source")
        if not isinstance(self.observed_value, Decimal):
            raise TypeError("observed_value must be a Decimal")
        if not isinstance(self.unit, UnitLabel):
            raise TypeError("unit must be a UnitLabel")
        if self.collected_at is not None:
            raise ValueError("deterministic fixtures require collected_at=None")
        if self.provenance.product_ref != self.product_ref:
            raise ValueError("observation provenance must name its product")
        if self.provenance.fixture_sequence != self.fixture_sequence:
            raise ValueError("observation provenance must name its sequence")
        if self.provenance.declared_metric_ref != self.metric_ref:
            raise ValueError("observation provenance must preserve metric")
        if self.provenance.declared_unit is not self.unit:
            raise ValueError("observation provenance must preserve unit")
        if self.provenance.declared_context_identity != self.context_identity:
            raise ValueError("observation provenance must preserve context")


@dataclass(frozen=True, slots=True)
class ObservationResolution:
    slot_ref: ObservationSlotRef
    status: FullModelStatus
    applicability: Applicability
    observation: DynamicObservation | None
    reasons: tuple[DynamicEvidenceReason, ...]
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _typed_tuple(self.reasons, DynamicEvidenceReason, "reasons")
        if not isinstance(self.provenance_refs, tuple) or any(
            not isinstance(item, str) for item in self.provenance_refs
        ):
            raise TypeError("provenance_refs must be a tuple of strings")
        if self.status is FullModelStatus.AVAILABLE:
            if self.applicability is not Applicability.APPLICABLE or self.observation is None:
                raise ValueError("available resolution requires an applicable observation")
            if self.observation.slot_ref != self.slot_ref:
                raise ValueError("resolved observation must occupy the declared slot")
            if self.reasons:
                raise ValueError("available resolution cannot carry non-value reasons")
        else:
            if self.applicability not in _NONVALUE_APPLICABILITY[self.status]:
                raise ValueError("resolution status/applicability combination is invalid")
            if self.observation is not None:
                raise ValueError("non-available resolution cannot contain an observation")


@dataclass(frozen=True, slots=True, order=True)
class DynamicEvidenceAssessmentRef:
    assessment_id: str
    assessment_version: str
    artifact_ref: ArtifactRef
    product_ref: ProductRef
    collection_ref: ObservationCollectionRef

    def __post_init__(self) -> None:
        _identifier(self.assessment_id, "assessment_id")
        _identifier(self.assessment_version, "assessment_version")
        if self.collection_ref.product_ref != self.product_ref:
            raise ValueError("dynamic assessment product must match collection")


@dataclass(frozen=True, slots=True, order=True)
class ConformanceAssessmentId:
    dynamic_assessment_ref: DynamicEvidenceAssessmentRef
    criterion_binding_id: CriterionBindingId
    observation_slot_ref: ObservationSlotRef | None
    evaluator_rule_ref: RuleRef

    def __post_init__(self) -> None:
        if self.dynamic_assessment_ref.artifact_ref != self.criterion_binding_id.artifact_ref:
            raise ValueError("dynamic assessment artifact must match criterion binding")
        if self.observation_slot_ref is not None and (
            self.observation_slot_ref.collection_ref != self.dynamic_assessment_ref.collection_ref
        ):
            raise ValueError("conformance slot must belong to assessment collection")


@dataclass(frozen=True, slots=True, order=True)
class CriterionRef:
    criterion_id: CriterionId


@dataclass(frozen=True, slots=True, order=True)
class DynamicObservationRef:
    observation_id: DynamicObservationId


@dataclass(frozen=True, slots=True)
class ConformanceOperands:
    comparator: ComparatorLabel
    inclusivity: BoundaryInclusivity
    criterion_bound: Decimal
    criterion_unit: UnitLabel
    criterion_context_identity: CriterionContextIdentity
    observed_value: Decimal
    observation_unit: UnitLabel
    observation_context_identity: CriterionContextIdentity


@dataclass(frozen=True, slots=True)
class ConformanceProvenance:
    criterion_ref: CriterionRef | None
    observation_ref: DynamicObservationRef | ObservationSlotRef | None
    direct_criterion_evidence_refs: tuple[CrossEvidenceRef, ...]
    dynamic_observation_provenance_ref: str | None
    evaluator_rule_ref: RuleRef
    dynamic_contract_ref: ContractRef
    full_model_contract_ref: ContractRef
    exact_operands: ConformanceOperands | None
    absence_reasons: tuple[DynamicEvidenceReason, ...]

    def __post_init__(self) -> None:
        _typed_tuple(self.direct_criterion_evidence_refs, CrossEvidenceRef, "evidence_refs")
        _typed_tuple(self.absence_reasons, DynamicEvidenceReason, "absence_reasons")
        if self.dynamic_contract_ref != DYNAMIC_CONTRACT_REF:
            raise ValueError("provenance requires the dynamic contract")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("provenance requires the Full Model contract")
        if self.exact_operands is not None and self.absence_reasons:
            raise ValueError("available provenance cannot carry absence reasons")


@dataclass(frozen=True, slots=True)
class ConformanceAssessment:
    conformance_id: ConformanceAssessmentId
    dynamic_assessment_ref: DynamicEvidenceAssessmentRef
    criterion_binding_id: CriterionBindingId
    criterion_id: CriterionId | None
    observation_slot_ref: ObservationSlotRef | None
    observation_id: DynamicObservationId | None
    status: FullModelStatus
    applicability: Applicability
    outcome: ConformanceOutcome | None
    explanation: str
    reasons: tuple[DynamicEvidenceReason, ...]
    criterion_ref: CriterionRef | None
    observation_ref: DynamicObservationRef | None
    evidence_refs: tuple[CrossEvidenceRef, ...]
    provenance: ConformanceProvenance
    evaluator_rule_ref: RuleRef

    def __post_init__(self) -> None:
        _identifier(self.explanation, "explanation")
        expected = ConformanceAssessmentId(
            self.dynamic_assessment_ref, self.criterion_binding_id,
            self.observation_slot_ref, self.evaluator_rule_ref,
        )
        if self.conformance_id != expected:
            raise ValueError("conformance_id must match exact assessment inputs")
        _typed_tuple(self.reasons, DynamicEvidenceReason, "reasons")
        _typed_tuple(self.evidence_refs, CrossEvidenceRef, "evidence_refs")
        if self.status is FullModelStatus.AVAILABLE:
            if self.applicability is not Applicability.APPLICABLE:
                raise ValueError("available conformance must be applicable")
            if not isinstance(self.outcome, ConformanceOutcome):
                raise ValueError("available conformance requires exactly one outcome")
            if self.criterion_id is None or self.observation_id is None:
                raise ValueError("available conformance requires both exact input IDs")
            if self.reasons:
                raise ValueError("available conformance cannot carry reasons")
        else:
            if self.applicability not in _NONVALUE_APPLICABILITY[self.status]:
                raise ValueError("conformance status/applicability combination is invalid")
            if self.outcome is not None:
                raise ValueError("non-available conformance cannot carry an outcome")


@dataclass(frozen=True, slots=True)
class ConformanceEvaluationContext:
    dynamic_assessment_ref: DynamicEvidenceAssessmentRef
    evaluator_rule_ref: RuleRef = EVALUATOR_RULE_REF
    dynamic_contract_ref: ContractRef = DYNAMIC_CONTRACT_REF
    full_model_contract_ref: ContractRef = FULL_MODEL_CONTRACT_REF

    def __post_init__(self) -> None:
        if self.evaluator_rule_ref != EVALUATOR_RULE_REF:
            raise ValueError("unsupported conformance evaluator rule")
        if self.dynamic_contract_ref != DYNAMIC_CONTRACT_REF:
            raise ValueError("unsupported dynamic evidence contract")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("unsupported Full Model contract")


def serialize_decimal(value: Decimal) -> dict[str, object]:
    """Return the contract's lossless finite Decimal representation."""
    if not isinstance(value, Decimal):
        raise TypeError("value must be a Decimal")
    decimal_tuple = value.as_tuple()
    if not isinstance(decimal_tuple.exponent, int):
        raise ValueError("non-finite Decimal values have no finite serialization")
    return {
        "kind": "DECIMAL", "sign": decimal_tuple.sign,
        "digits": list(decimal_tuple.digits), "exponent": decimal_tuple.exponent,
    }

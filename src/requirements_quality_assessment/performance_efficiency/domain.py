"""Typed ``X_PE`` records for the Full Model v0.1 reference slice.

These immutable values package completed requirement, QB, and dynamic-evidence
results. They do not calculate product quality or transform numeric values.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from fractions import Fraction

from ..cross_analysis.domain import (
    AssessmentSnapshotId,
    ComparisonKey,
    CrossDiagnosticRef,
    CrossEvidenceRef,
    CrossResultId,
    QbConsistencyReason,
)
from ..domain import BoundaryInclusivity, ComparatorLabel, UnitLabel
from ..dynamic_evidence import (
    Applicability,
    ConformanceAssessmentId,
    ConformanceOutcome,
    CriterionBindingId,
    CriterionContextIdentity,
    DynamicEvidenceAssessmentRef,
    DynamicEvidenceReason,
    DynamicMetricRef,
    EnvironmentRef,
    FullModelStatus,
    ObservationCollectionRef,
    ObservationSlotRef,
    ProductRef,
)
from ..dynamic_evidence.domain import CriterionRef, DynamicObservationRef
from ..metrics import (
    FULL_MODEL_CONTRACT_REF,
    ArtifactRef,
    AssessmentRef,
    ContractRef,
    MetricApplicability,
    MetricEntryId,
    MetricProfileId,
    MetricStatus,
    NumericRepresentation,
    RequirementDiagnosticRef,
    RequirementEvidenceRef,
    RequirementFindingRef,
    RequirementSubjectRef,
    RequirementTraceRef,
    RuleRef,
    RuleVersionAuthority,
    SourceStatusRef,
)


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


def _typed_tuple(value: object, item_types: type | tuple[type, ...], name: str) -> None:
    if not isinstance(value, tuple) or any(
        not isinstance(item, item_types) for item in value
    ):
        raise TypeError(f"{name} must be a tuple of approved values")


class ProductQualityCharacteristicId(str, Enum):
    PERFORMANCE_EFFICIENCY = "PERFORMANCE_EFFICIENCY"


class PerformanceEfficiencyFeatureId(str, Enum):
    CRITERION_RESPONSE_TIME = "PE.CRITERION.RESPONSE_TIME"
    REQUIREMENT_COMPLETENESS = "PE.REQ.C"
    REQUIREMENT_VERIFIABILITY = "PE.REQ.V"
    REQUIREMENT_UNAMBIGUITY = "PE.REQ.U"
    SPECIFICATION_QB = "PE.SPEC.QB"
    OBSERVATION_RESPONSE_TIME = "PE.OBS.RESPONSE_TIME"
    CONFORMANCE_RESPONSE_TIME = "PE.CONFORMANCE.RESPONSE_TIME"


PE_FEATURE_REGISTRY = tuple(PerformanceEfficiencyFeatureId)


class FeatureEffect(str, Enum):
    REQUIRED_INPUT = "REQUIRED_INPUT"
    CONTEXT_ONLY = "CONTEXT_ONLY"
    ELIGIBILITY_GATE = "ELIGIBILITY_GATE"
    DIRECT_RESULT_INPUT = "DIRECT_RESULT_INPUT"


PE_FEATURE_EFFECTS = (
    FeatureEffect.REQUIRED_INPUT,
    FeatureEffect.CONTEXT_ONLY,
    FeatureEffect.CONTEXT_ONLY,
    FeatureEffect.CONTEXT_ONLY,
    FeatureEffect.ELIGIBILITY_GATE,
    FeatureEffect.REQUIRED_INPUT,
    FeatureEffect.DIRECT_RESULT_INPUT,
)


class QbTargetGateDecision(str, Enum):
    TARGET_CLEAR = "TARGET_CLEAR"
    TARGET_CONFLICT = "TARGET_CONFLICT"
    TARGET_UNRESOLVED = "TARGET_UNRESOLVED"
    TARGET_NOT_APPLICABLE = "TARGET_NOT_APPLICABLE"


class AvailabilityPoint(str, Enum):
    SOURCE_ASSESSMENT_AVAILABLE = "SOURCE_ASSESSMENT_AVAILABLE"
    CRITERION_BINDING_AVAILABLE = "CRITERION_BINDING_AVAILABLE"
    DYNAMIC_COLLECTION_AVAILABLE = "DYNAMIC_COLLECTION_AVAILABLE"
    CONFORMANCE_ASSESSMENT_AVAILABLE = "CONFORMANCE_ASSESSMENT_AVAILABLE"


class ProcessStage(str, Enum):
    REFERENCE_VERIFICATION = "REFERENCE_VERIFICATION"


class FeatureReason(str, Enum):
    CRITERION_SUBJECT_UNRESOLVED = "CRITERION_SUBJECT_UNRESOLVED"
    QB_TARGET_CONFLICT = "QB_TARGET_CONFLICT"
    QB_TARGET_UNRESOLVED = "QB_TARGET_UNRESOLVED"
    QB_TARGET_NOT_APPLICABLE = "QB_TARGET_NOT_APPLICABLE"


FEATURE_CONTRACT_REF = ContractRef(
    "FULL-MODEL-V0.1-PRODUCT-QUALITY-FEATURE", "1"
)
METRIC_PROFILE_CONTRACT_REF = ContractRef(
    "FULL-MODEL-V0.1-METRIC-PROFILE", "1"
)
FEATURE_REGISTRY_REF = ContractRef("FULL-MODEL-V0.1-PE-FEATURES", "1")
MAPPING_RULE_REF = RuleRef(
    "P-M-E-TO-X-PE-001", "1", RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION
)


@dataclass(frozen=True, slots=True, order=True)
class ProcessStateRef:
    process_state_id: str
    process_state_version: str
    stage: ProcessStage

    def __post_init__(self) -> None:
        _identifier(self.process_state_id, "process_state_id")
        _identifier(self.process_state_version, "process_state_version")
        if self.stage is not ProcessStage.REFERENCE_VERIFICATION:
            raise ValueError("Full Model v0.1 supports REFERENCE_VERIFICATION only")


@dataclass(frozen=True, slots=True, order=True)
class ExternalDynamicSourceRef:
    collection_ref: ObservationCollectionRef
    source_record_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.collection_ref, ObservationCollectionRef):
            raise TypeError("collection_ref must be an ObservationCollectionRef")
        _identifier(self.source_record_ref, "source_record_ref")


@dataclass(frozen=True, slots=True)
class PerformanceEfficiencyFeatureConstructionContext:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    metric_profile_ref: MetricProfileId
    dynamic_assessment_ref: DynamicEvidenceAssessmentRef
    product_ref: ProductRef
    process_state_ref: ProcessStateRef
    full_model_contract_ref: ContractRef = FULL_MODEL_CONTRACT_REF
    feature_contract_ref: ContractRef = FEATURE_CONTRACT_REF
    feature_registry_ref: ContractRef = FEATURE_REGISTRY_REF
    mapping_rule_ref: RuleRef = MAPPING_RULE_REF

    def __post_init__(self) -> None:
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("source assessment must name the context artifact")
        if self.metric_profile_ref.artifact_ref != self.artifact_ref:
            raise ValueError("metric profile must name the context artifact")
        if self.metric_profile_ref.assessment_ref != self.source_assessment_ref:
            raise ValueError("metric profile must name the source assessment")
        if self.dynamic_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("dynamic assessment must name the context artifact")
        if self.dynamic_assessment_ref.product_ref != self.product_ref:
            raise ValueError("dynamic assessment must name the context product")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("unsupported Full Model contract")
        if self.feature_contract_ref != FEATURE_CONTRACT_REF:
            raise ValueError("unsupported product-quality feature contract")
        if self.feature_registry_ref != FEATURE_REGISTRY_REF:
            raise ValueError("unsupported Performance Efficiency feature registry")
        if self.mapping_rule_ref != MAPPING_RULE_REF:
            raise ValueError("unsupported Performance Efficiency mapping rule")


@dataclass(frozen=True, slots=True, order=True)
class PerformanceEfficiencyFeatureProfileId:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    metric_profile_ref: MetricProfileId
    dynamic_assessment_ref: DynamicEvidenceAssessmentRef
    product_ref: ProductRef
    process_state_ref: ProcessStateRef
    feature_registry_ref: ContractRef
    mapping_rule_ref: RuleRef

    def __post_init__(self) -> None:
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("profile identity cannot mix artifact assessments")
        if self.metric_profile_ref.artifact_ref != self.artifact_ref:
            raise ValueError("profile identity cannot mix metric artifacts")
        if self.metric_profile_ref.assessment_ref != self.source_assessment_ref:
            raise ValueError("profile identity cannot mix source assessments")
        if self.dynamic_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("profile identity cannot mix dynamic artifacts")
        if self.dynamic_assessment_ref.product_ref != self.product_ref:
            raise ValueError("profile identity cannot mix products")
        if self.feature_registry_ref != FEATURE_REGISTRY_REF:
            raise ValueError("profile identity requires the approved registry")
        if self.mapping_rule_ref != MAPPING_RULE_REF:
            raise ValueError("profile identity requires the approved mapping rule")


@dataclass(frozen=True, slots=True, order=True)
class PerformanceEfficiencyFeatureEntryId:
    profile_id: PerformanceEfficiencyFeatureProfileId
    feature_id: PerformanceEfficiencyFeatureId

    def __post_init__(self) -> None:
        if not isinstance(self.profile_id, PerformanceEfficiencyFeatureProfileId):
            raise TypeError("profile_id must be a PerformanceEfficiencyFeatureProfileId")
        if not isinstance(self.feature_id, PerformanceEfficiencyFeatureId):
            raise TypeError("feature_id must be a PerformanceEfficiencyFeatureId")


@dataclass(frozen=True, slots=True)
class CriterionFeatureValue:
    criterion_ref: CriterionRef
    metric_ref: DynamicMetricRef
    comparator: ComparatorLabel
    inclusivity: BoundaryInclusivity
    exact_decimal_bound: Decimal
    unit: UnitLabel
    context_identity: CriterionContextIdentity

    def __post_init__(self) -> None:
        if not isinstance(self.criterion_ref, CriterionRef):
            raise TypeError("criterion_ref must be a CriterionRef")
        if not isinstance(self.metric_ref, DynamicMetricRef):
            raise TypeError("metric_ref must be a DynamicMetricRef")
        if not isinstance(self.comparator, ComparatorLabel):
            raise TypeError("comparator must be a ComparatorLabel")
        if not isinstance(self.inclusivity, BoundaryInclusivity):
            raise TypeError("inclusivity must be a BoundaryInclusivity")
        if not isinstance(self.exact_decimal_bound, Decimal):
            raise TypeError("criterion bound must remain an exact Decimal")
        if not isinstance(self.unit, UnitLabel):
            raise TypeError("unit must be a UnitLabel")
        if not isinstance(self.context_identity, CriterionContextIdentity):
            raise TypeError("context_identity must be a CriterionContextIdentity")


@dataclass(frozen=True, slots=True)
class RequirementMetricFeatureValue:
    metric_entry_ref: MetricEntryId
    exact_fraction_or_none: Fraction | None
    numeric_representation: NumericRepresentation
    source_status: SourceStatusRef

    def __post_init__(self) -> None:
        if not isinstance(self.metric_entry_ref, MetricEntryId):
            raise TypeError("metric_entry_ref must be a MetricEntryId")
        if not isinstance(self.exact_fraction_or_none, Fraction):
            raise TypeError("available requirement metrics require an exact Fraction")
        if self.numeric_representation is not NumericRepresentation.EXACT_FRACTION:
            raise ValueError("available requirement metrics require EXACT_FRACTION")
        if not isinstance(self.source_status, SourceStatusRef):
            raise TypeError("source_status must be a SourceStatusRef")


@dataclass(frozen=True, slots=True)
class QbTargetGateFeatureValue:
    qb_metric_entry_ref: MetricEntryId
    source_metric_status: MetricStatus
    source_metric_applicability: MetricApplicability
    source_exact_fraction_or_none: Fraction | None
    gate_decision: QbTargetGateDecision
    target_key: ComparisonKey
    ordered_cross_result_refs: tuple[CrossResultId, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.qb_metric_entry_ref, MetricEntryId):
            raise TypeError("qb_metric_entry_ref must be a MetricEntryId")
        if not isinstance(self.source_metric_status, MetricStatus):
            raise TypeError("source_metric_status must be a MetricStatus")
        if not isinstance(self.source_metric_applicability, MetricApplicability):
            raise TypeError("source metric applicability must be MetricApplicability")
        if self.source_exact_fraction_or_none is not None and not isinstance(
            self.source_exact_fraction_or_none, Fraction
        ):
            raise TypeError("QB metric values must remain exact Fractions")
        if not isinstance(self.target_key, ComparisonKey):
            raise TypeError("target_key must be a ComparisonKey")
        _typed_tuple(self.ordered_cross_result_refs, CrossResultId, "cross result refs")
        if self.gate_decision not in {
            QbTargetGateDecision.TARGET_CLEAR,
            QbTargetGateDecision.TARGET_CONFLICT,
        }:
            raise ValueError("only available gate decisions have typed values")


@dataclass(frozen=True, slots=True)
class ObservationFeatureValue:
    observation_ref: DynamicObservationRef
    metric_ref: DynamicMetricRef
    exact_decimal_value: Decimal
    unit: UnitLabel
    context_identity: CriterionContextIdentity

    def __post_init__(self) -> None:
        if not isinstance(self.observation_ref, DynamicObservationRef):
            raise TypeError("observation_ref must be a DynamicObservationRef")
        if not isinstance(self.metric_ref, DynamicMetricRef):
            raise TypeError("metric_ref must be a DynamicMetricRef")
        if not isinstance(self.exact_decimal_value, Decimal):
            raise TypeError("observation values must remain exact Decimals")
        if not isinstance(self.unit, UnitLabel):
            raise TypeError("unit must be a UnitLabel")
        if not isinstance(self.context_identity, CriterionContextIdentity):
            raise TypeError("context_identity must be a CriterionContextIdentity")


@dataclass(frozen=True, slots=True)
class ConformanceFeatureValue:
    conformance_ref: ConformanceAssessmentId
    outcome: ConformanceOutcome

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, ConformanceOutcome):
            raise TypeError("conformance outcome must remain categorical")


PeFeatureValue = (
    CriterionFeatureValue
    | RequirementMetricFeatureValue
    | QbTargetGateFeatureValue
    | ObservationFeatureValue
    | ConformanceFeatureValue
)

FeatureSourceRef = (
    CriterionBindingId
    | MetricEntryId
    | CrossResultId
    | ObservationSlotRef
    | DynamicObservationRef
    | ConformanceAssessmentId
)
FeatureEvidenceRef = RequirementEvidenceRef | CrossEvidenceRef
FeatureProvenanceRef = (
    RequirementTraceRef
    | RequirementDiagnosticRef
    | RequirementFindingRef
    | CrossDiagnosticRef
    | CrossResultId
    | ExternalDynamicSourceRef
)
FeatureSourceReason = DynamicEvidenceReason | QbConsistencyReason | FeatureReason


@dataclass(frozen=True, slots=True)
class PerformanceEfficiencyFeature:
    feature_entry_id: PerformanceEfficiencyFeatureEntryId
    feature_id: PerformanceEfficiencyFeatureId
    characteristic_id: ProductQualityCharacteristicId
    effect: FeatureEffect
    status: FullModelStatus
    applicability: Applicability
    typed_value: PeFeatureValue | None
    source_refs: tuple[FeatureSourceRef, ...]
    evidence_refs: tuple[FeatureEvidenceRef, ...]
    provenance_refs: tuple[FeatureProvenanceRef, ...]
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    product_ref: ProductRef | None
    availability_point: AvailabilityPoint
    rule_refs: tuple[RuleRef, ...]
    reasons: tuple[FeatureSourceReason, ...]
    explanation: str

    def __post_init__(self) -> None:
        if not isinstance(self.feature_entry_id, PerformanceEfficiencyFeatureEntryId):
            raise TypeError("feature_entry_id must be a feature entry identity")
        if not isinstance(self.feature_id, PerformanceEfficiencyFeatureId):
            raise TypeError("feature_id must be a PerformanceEfficiencyFeatureId")
        if self.feature_entry_id.feature_id is not self.feature_id:
            raise ValueError("feature entry identity must name its feature")
        if self.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
            raise ValueError("X_PE supports Performance Efficiency only")
        ordinal = PE_FEATURE_REGISTRY.index(self.feature_id)
        if self.effect is not PE_FEATURE_EFFECTS[ordinal]:
            raise ValueError("feature effect must match the closed registry")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("feature assessment and artifact refs must agree")
        if not isinstance(self.status, FullModelStatus):
            raise TypeError("status must be a FullModelStatus")
        if not isinstance(self.applicability, Applicability):
            raise TypeError("applicability must be an Applicability")
        if not isinstance(self.availability_point, AvailabilityPoint):
            raise TypeError("availability_point must be an AvailabilityPoint")
        _typed_tuple(
            self.source_refs,
            (
                CriterionBindingId,
                MetricEntryId,
                CrossResultId,
                ObservationSlotRef,
                DynamicObservationRef,
                ConformanceAssessmentId,
            ),
            "source_refs",
        )
        _typed_tuple(
            self.evidence_refs,
            (RequirementEvidenceRef, CrossEvidenceRef),
            "evidence_refs",
        )
        _typed_tuple(
            self.provenance_refs,
            (
                RequirementTraceRef,
                RequirementDiagnosticRef,
                RequirementFindingRef,
                CrossDiagnosticRef,
                CrossResultId,
                ExternalDynamicSourceRef,
            ),
            "provenance_refs",
        )
        _typed_tuple(self.rule_refs, RuleRef, "rule_refs")
        _typed_tuple(
            self.reasons,
            (DynamicEvidenceReason, QbConsistencyReason, FeatureReason),
            "reasons",
        )
        _identifier(self.explanation, "explanation")
        if not self.source_refs:
            raise ValueError("every feature requires at least one typed source ref")
        if not self.rule_refs:
            raise ValueError("every feature requires at least one rule ref")
        for values, name in (
            (self.source_refs, "source_refs"),
            (self.evidence_refs, "evidence_refs"),
            (self.provenance_refs, "provenance_refs"),
            (self.rule_refs, "rule_refs"),
        ):
            if len(values) != len(set(values)):
                raise ValueError(f"{name} must not contain duplicates")
        allowed = {
            FullModelStatus.AVAILABLE: {Applicability.APPLICABLE},
            FullModelStatus.NOT_APPLICABLE: {Applicability.NOT_APPLICABLE},
            FullModelStatus.UNKNOWN: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNRESOLVED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNAVAILABLE: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNSUPPORTED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
        }[self.status]
        if self.applicability not in allowed:
            raise ValueError("feature status/applicability combination is invalid")
        if self.status is FullModelStatus.AVAILABLE:
            if self.typed_value is None:
                raise ValueError("AVAILABLE features require a typed value")
        elif self.typed_value is not None:
            raise ValueError("non-AVAILABLE features cannot carry typed values")
        expected_types = {
            PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME: CriterionFeatureValue,
            PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS: RequirementMetricFeatureValue,
            PerformanceEfficiencyFeatureId.REQUIREMENT_VERIFIABILITY: RequirementMetricFeatureValue,
            PerformanceEfficiencyFeatureId.REQUIREMENT_UNAMBIGUITY: RequirementMetricFeatureValue,
            PerformanceEfficiencyFeatureId.SPECIFICATION_QB: QbTargetGateFeatureValue,
            PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME: ObservationFeatureValue,
            PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME: ConformanceFeatureValue,
        }
        if self.typed_value is not None and not isinstance(
            self.typed_value, expected_types[self.feature_id]
        ):
            raise TypeError("typed feature value does not match the registry slot")


@dataclass(frozen=True, slots=True)
class FeatureProfileProvenance:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    metric_profile_ref: MetricProfileId
    criterion_binding_ref: CriterionBindingId
    observation_resolution_ref: ObservationSlotRef
    conformance_assessment_ref: ConformanceAssessmentId
    dynamic_assessment_ref: DynamicEvidenceAssessmentRef
    product_ref: ProductRef
    environment_ref_or_none: EnvironmentRef | None
    collection_ref_or_none: ObservationCollectionRef | None
    process_state_ref: ProcessStateRef
    ordered_feature_entry_refs: tuple[PerformanceEfficiencyFeatureEntryId, ...]
    source_contract_refs: tuple[ContractRef, ...]
    rule_refs: tuple[RuleRef, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        _typed_tuple(
            self.ordered_feature_entry_refs,
            PerformanceEfficiencyFeatureEntryId,
            "ordered_feature_entry_refs",
        )
        _typed_tuple(self.source_contract_refs, ContractRef, "source_contract_refs")
        _typed_tuple(self.rule_refs, RuleRef, "rule_refs")
        if not self.source_contract_refs or not self.rule_refs:
            raise ValueError("profile provenance requires contracts and rules")
        if len(self.source_contract_refs) != len(set(self.source_contract_refs)):
            raise ValueError("source_contract_refs must not contain duplicates")
        if len(self.rule_refs) != len(set(self.rule_refs)):
            raise ValueError("rule_refs must not contain duplicates")
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("profile provenance cannot mix artifact assessments")
        if self.dynamic_assessment_ref.product_ref != self.product_ref:
            raise ValueError("profile provenance cannot mix products")
        if self.collection_ref_or_none is not None:
            if self.collection_ref_or_none != self.dynamic_assessment_ref.collection_ref:
                raise ValueError("profile provenance cannot mix collections")
            if self.environment_ref_or_none != self.collection_ref_or_none.environment_ref:
                raise ValueError("profile provenance cannot mix environments")


@dataclass(frozen=True, slots=True)
class PerformanceEfficiencyFeatureProfile:
    profile_id: PerformanceEfficiencyFeatureProfileId
    characteristic_id: ProductQualityCharacteristicId
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    metric_profile_ref: MetricProfileId
    dynamic_assessment_ref: DynamicEvidenceAssessmentRef
    product_ref: ProductRef
    process_state_ref: ProcessStateRef
    criterion_subject_ref: RequirementSubjectRef | None
    target_key: ComparisonKey | None
    status: FullModelStatus
    applicability: Applicability
    features: tuple[PerformanceEfficiencyFeature, ...]
    provenance: FeatureProfileProvenance
    registry_ref: ContractRef
    mapping_rule_ref: RuleRef

    def __post_init__(self) -> None:
        expected_id = PerformanceEfficiencyFeatureProfileId(
            self.artifact_ref,
            self.source_assessment_ref,
            self.metric_profile_ref,
            self.dynamic_assessment_ref,
            self.product_ref,
            self.process_state_ref,
            self.registry_ref,
            self.mapping_rule_ref,
        )
        if self.profile_id != expected_id:
            raise ValueError("profile_id must be the structured profile identity")
        if self.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
            raise ValueError("X_PE supports Performance Efficiency only")
        _typed_tuple(self.features, PerformanceEfficiencyFeature, "features")
        if tuple(item.feature_id for item in self.features) != PE_FEATURE_REGISTRY:
            raise ValueError("profile must contain exactly the closed seven-slot registry")
        if tuple(item.effect for item in self.features) != PE_FEATURE_EFFECTS:
            raise ValueError("profile feature effects must match the registry")
        expected_entry_ids = tuple(
            PerformanceEfficiencyFeatureEntryId(self.profile_id, feature_id)
            for feature_id in PE_FEATURE_REGISTRY
        )
        if tuple(item.feature_entry_id for item in self.features) != expected_entry_ids:
            raise ValueError("profile feature identities must be deterministic and ordered")
        if self.provenance.ordered_feature_entry_refs != expected_entry_ids:
            raise ValueError("profile provenance must preserve feature registry order")
        if (
            self.provenance.artifact_ref != self.artifact_ref
            or self.provenance.source_assessment_ref != self.source_assessment_ref
            or self.provenance.metric_profile_ref != self.metric_profile_ref
            or self.provenance.dynamic_assessment_ref != self.dynamic_assessment_ref
            or self.provenance.product_ref != self.product_ref
            or self.provenance.process_state_ref != self.process_state_ref
        ):
            raise ValueError("profile and provenance identities must agree")
        if any(
            item.feature_entry_id.profile_id != self.profile_id
            or item.artifact_ref != self.artifact_ref
            or item.source_assessment_ref != self.source_assessment_ref
            for item in self.features
        ):
            raise ValueError("every feature must share the profile context")
        if any(
            item.product_ref != self.product_ref
            for item in (self.features[5], self.features[6])
        ) or any(item.product_ref is not None for item in self.features[:5]):
            raise ValueError("static and product feature subjects must remain distinct")
        if self.registry_ref != FEATURE_REGISTRY_REF or self.mapping_rule_ref != MAPPING_RULE_REF:
            raise ValueError("profile must use the approved registry and mapping rule")
        allowed = {
            FullModelStatus.AVAILABLE: {Applicability.APPLICABLE},
            FullModelStatus.NOT_APPLICABLE: {Applicability.NOT_APPLICABLE},
            FullModelStatus.UNKNOWN: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNRESOLVED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNAVAILABLE: {Applicability.APPLICABLE, Applicability.UNKNOWN},
            FullModelStatus.UNSUPPORTED: {Applicability.APPLICABLE, Applicability.UNKNOWN},
        }[self.status]
        if self.applicability not in allowed:
            raise ValueError("profile status/applicability combination is invalid")


__all__ = [
    "AvailabilityPoint",
    "ConformanceFeatureValue",
    "CriterionFeatureValue",
    "ExternalDynamicSourceRef",
    "FEATURE_CONTRACT_REF",
    "FEATURE_REGISTRY_REF",
    "FeatureEffect",
    "FeatureProfileProvenance",
    "FeatureReason",
    "MAPPING_RULE_REF",
    "METRIC_PROFILE_CONTRACT_REF",
    "ObservationFeatureValue",
    "PE_FEATURE_EFFECTS",
    "PE_FEATURE_REGISTRY",
    "PerformanceEfficiencyFeature",
    "PerformanceEfficiencyFeatureConstructionContext",
    "PerformanceEfficiencyFeatureEntryId",
    "PerformanceEfficiencyFeatureId",
    "PerformanceEfficiencyFeatureProfile",
    "PerformanceEfficiencyFeatureProfileId",
    "ProcessStage",
    "ProcessStateRef",
    "ProductQualityCharacteristicId",
    "QbTargetGateDecision",
    "QbTargetGateFeatureValue",
    "RequirementMetricFeatureValue",
]

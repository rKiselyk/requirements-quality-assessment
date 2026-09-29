"""Immutable Full Model v0.1 metric-profile domain contracts.

These values describe the lossless ``P -> M`` representation only. They do
not calculate, aggregate, normalize, round, rank, or interpret source results.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from ..cross_analysis.domain import (
    AssessmentSnapshotId,
    BoundedNonClaimKey,
    CrossDiagnosticRef,
    CrossEvidenceRef,
    CrossResultId,
    QbConsistencyFormulaOperands,
    QbConsistencyObservability,
    QbConsistencyReason,
    QbConsistencyState,
)
from ..domain import (
    CharacteristicAssessmentState,
    CharacteristicId,
    FeatureId,
    FeatureInputTrace,
    TraceDecisionCode,
)


def _require_identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip() or any(ord(char) < 32 for char in value):
        raise ValueError(f"{name} must be non-empty, trimmed, and contain no controls")
    return value


def _require_typed_tuple(
    value: object, item_types: type | tuple[type, ...], name: str
) -> None:
    if not isinstance(value, tuple) or any(
        not isinstance(item, item_types) for item in value
    ):
        raise TypeError(f"{name} must be a tuple of approved values")


def _require_unique(value: tuple[object, ...], name: str) -> None:
    if len(value) != len(set(value)):
        raise ValueError(f"{name} must not contain duplicates")


class MetricId(str, Enum):
    RQ_COMPLETENESS = "RQ.COMPLETENESS"
    RQ_VERIFIABILITY = "RQ.VERIFIABILITY"
    RQ_UNAMBIGUITY = "RQ.UNAMBIGUITY"
    SPEC_MEAN_COMPLETENESS = "SPEC.MEAN_COMPLETENESS"
    SPEC_MEAN_VERIFIABILITY = "SPEC.MEAN_VERIFIABILITY"
    SPEC_MEAN_UNAMBIGUITY = "SPEC.MEAN_UNAMBIGUITY"
    SPEC_QB_CONSISTENCY = "SPEC.QB_CONSISTENCY"


class MetricScope(str, Enum):
    REQUIREMENT = "REQUIREMENT"
    SPECIFICATION = "SPECIFICATION"


class MetricStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNRESOLVED = "UNRESOLVED"
    UNAVAILABLE = "UNAVAILABLE"
    UNSUPPORTED = "UNSUPPORTED"


class MetricApplicability(str, Enum):
    APPLICABLE = "APPLICABLE"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class NumericRepresentation(str, Enum):
    EXACT_FRACTION = "EXACT_FRACTION"
    NONE = "NONE"


class RuleVersionAuthority(str, Enum):
    STABLE_RULE_ID_POLICY = "STABLE_RULE_ID_POLICY"
    EXPLICIT_CONTRACT_VERSION = "EXPLICIT_CONTRACT_VERSION"


class MetricSourceKind(str, Enum):
    REQUIREMENT_CHARACTERISTIC = "REQUIREMENT_CHARACTERISTIC"
    SPECIFICATION_AGGREGATE = "SPECIFICATION_AGGREGATE"
    QB_CONSISTENCY = "QB_CONSISTENCY"


@dataclass(frozen=True, slots=True, order=True)
class ArtifactRef:
    artifact_id: str
    artifact_version: str

    def __post_init__(self) -> None:
        _require_identifier(self.artifact_id, "artifact_id")
        _require_identifier(self.artifact_version, "artifact_version")


@dataclass(frozen=True, slots=True, order=True)
class AssessmentRef:
    assessment_id: str
    assessment_version: str
    artifact_ref: ArtifactRef

    def __post_init__(self) -> None:
        _require_identifier(self.assessment_id, "assessment_id")
        _require_identifier(self.assessment_version, "assessment_version")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")


@dataclass(frozen=True, slots=True, order=True)
class ContractRef:
    contract_id: str
    version: str

    def __post_init__(self) -> None:
        _require_identifier(self.contract_id, "contract_id")
        _require_identifier(self.version, "version")


@dataclass(frozen=True, slots=True, order=True)
class RuleRef:
    rule_id: str
    explicit_version: str | None
    version_authority: RuleVersionAuthority

    def __post_init__(self) -> None:
        _require_identifier(self.rule_id, "rule_id")
        if not isinstance(self.version_authority, RuleVersionAuthority):
            raise TypeError("version_authority must be a RuleVersionAuthority")
        if self.version_authority is RuleVersionAuthority.STABLE_RULE_ID_POLICY:
            if self.explicit_version is not None:
                raise ValueError(
                    "stable rule IDs cannot carry a fabricated explicit version"
                )
        else:
            _require_identifier(self.explicit_version, "explicit_version")


FULL_MODEL_CONTRACT_REF = ContractRef("FULL-MODEL-V0.1-CONTRACT", "1")
METRIC_REGISTRY_REF = ContractRef("FULL-MODEL-V0.1-METRICS", "1")
ADAPTER_RULE_REF = RuleRef(
    "P-TO-M-V0.1-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)


@dataclass(frozen=True, slots=True)
class MetricConstructionContext:
    artifact_ref: ArtifactRef
    assessment_ref: AssessmentRef
    full_model_contract_ref: ContractRef = FULL_MODEL_CONTRACT_REF
    metric_registry_ref: ContractRef = METRIC_REGISTRY_REF
    adapter_rule_ref: RuleRef = ADAPTER_RULE_REF

    def __post_init__(self) -> None:
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if not isinstance(self.assessment_ref, AssessmentRef):
            raise TypeError("assessment_ref must be an AssessmentRef")
        if self.assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("assessment_ref must name the context artifact_ref")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError(
                "full_model_contract_ref must be FULL-MODEL-V0.1-CONTRACT / 1"
            )
        if self.metric_registry_ref != METRIC_REGISTRY_REF:
            raise ValueError(
                "metric_registry_ref must be FULL-MODEL-V0.1-METRICS / 1"
            )
        if self.adapter_rule_ref != ADAPTER_RULE_REF:
            raise ValueError("adapter_rule_ref must be P-TO-M-V0.1-001 / 1")


@dataclass(frozen=True, slots=True, order=True)
class RequirementSubjectRef:
    artifact_ref: ArtifactRef
    requirement_id: str
    source_line: int

    def __post_init__(self) -> None:
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        _require_identifier(self.requirement_id, "requirement_id")
        if type(self.source_line) is not int or self.source_line < 1:
            raise ValueError("source_line must be a positive integer")


@dataclass(frozen=True, slots=True, order=True)
class SpecificationSubjectRef:
    artifact_ref: ArtifactRef

    def __post_init__(self) -> None:
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")


MetricSubjectRef = RequirementSubjectRef | SpecificationSubjectRef


@dataclass(frozen=True, slots=True, order=True)
class MetricProfileId:
    artifact_ref: ArtifactRef
    assessment_ref: AssessmentRef
    registry_ref: ContractRef

    def __post_init__(self) -> None:
        if self.assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("profile assessment and artifact refs must agree")
        if self.registry_ref != METRIC_REGISTRY_REF:
            raise ValueError("profile IDs require the Full Model v0.1 metric registry")


@dataclass(frozen=True, slots=True)
class MetricEntryId:
    profile_id: MetricProfileId
    scope: MetricScope
    subject_ref: MetricSubjectRef
    metric_id: MetricId

    def __post_init__(self) -> None:
        if not isinstance(self.profile_id, MetricProfileId):
            raise TypeError("profile_id must be a MetricProfileId")
        if not isinstance(self.scope, MetricScope):
            raise TypeError("scope must be a MetricScope")
        if not isinstance(self.metric_id, MetricId):
            raise TypeError("metric_id must be a MetricId")
        expected_type = (
            RequirementSubjectRef
            if self.scope is MetricScope.REQUIREMENT
            else SpecificationSubjectRef
        )
        if not isinstance(self.subject_ref, expected_type):
            raise TypeError("subject_ref type must match metric scope")


@dataclass(frozen=True, slots=True, eq=False)
class SourceStatusRef:
    state: CharacteristicAssessmentState | QbConsistencyState | MetricStatus

    def __post_init__(self) -> None:
        if not isinstance(
            self.state,
            (CharacteristicAssessmentState, QbConsistencyState, MetricStatus),
        ):
            raise TypeError("state must be an approved source or metric status")

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, SourceStatusRef)
            and type(self.state) is type(other.state)
            and self.state is other.state
        )

    def __hash__(self) -> int:
        return hash((type(self.state), self.state.value))


@dataclass(frozen=True, slots=True)
class RequirementCharacteristicRef:
    assessment_ref: AssessmentRef
    requirement_subject_ref: RequirementSubjectRef
    characteristic_id: CharacteristicId

    def __post_init__(self) -> None:
        if not isinstance(self.assessment_ref, AssessmentRef):
            raise TypeError("assessment_ref must be an AssessmentRef")
        if not isinstance(self.requirement_subject_ref, RequirementSubjectRef):
            raise TypeError("requirement_subject_ref must be a RequirementSubjectRef")
        if not isinstance(self.characteristic_id, CharacteristicId):
            raise TypeError("characteristic_id must be a CharacteristicId")
        if self.assessment_ref.artifact_ref != self.requirement_subject_ref.artifact_ref:
            raise ValueError("source assessment and requirement artifact refs must agree")


@dataclass(frozen=True, slots=True)
class SpecificationAggregateRef:
    assessment_ref: AssessmentRef
    artifact_ref: ArtifactRef
    characteristic_id: CharacteristicId
    aggregation_rule_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.assessment_ref, AssessmentRef):
            raise TypeError("assessment_ref must be an AssessmentRef")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if self.assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("source assessment and aggregate artifact refs must agree")
        if not isinstance(self.characteristic_id, CharacteristicId):
            raise TypeError("characteristic_id must be a CharacteristicId")
        _require_identifier(self.aggregation_rule_id, "aggregation_rule_id")


@dataclass(frozen=True, slots=True)
class QbConsistencyAssessmentRef:
    assessment_ref: AssessmentRef
    artifact_ref: ArtifactRef
    snapshot_id: AssessmentSnapshotId
    aggregation_contract: ContractRef
    coverage_profile: ContractRef

    def __post_init__(self) -> None:
        if not isinstance(self.assessment_ref, AssessmentRef):
            raise TypeError("assessment_ref must be an AssessmentRef")
        if not isinstance(self.artifact_ref, ArtifactRef):
            raise TypeError("artifact_ref must be an ArtifactRef")
        if self.assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("source assessment and QB artifact refs must agree")
        if not isinstance(self.snapshot_id, AssessmentSnapshotId):
            raise TypeError("snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.aggregation_contract, ContractRef):
            raise TypeError("aggregation_contract must be a ContractRef")
        if not isinstance(self.coverage_profile, ContractRef):
            raise TypeError("coverage_profile must be a ContractRef")


SourceAssessmentRef = (
    RequirementCharacteristicRef
    | SpecificationAggregateRef
    | QbConsistencyAssessmentRef
)


@dataclass(frozen=True, slots=True)
class RequirementTraceRef:
    requirement_subject_ref: RequirementSubjectRef
    characteristic_id: CharacteristicId
    characteristic_index: int
    coverage_profile_id: str
    governing_rule_id: str
    decision_code: TraceDecisionCode
    feature_inputs: tuple[FeatureInputTrace, ...]
    finding_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.requirement_subject_ref, RequirementSubjectRef):
            raise TypeError("requirement_subject_ref must be a RequirementSubjectRef")
        if not isinstance(self.characteristic_id, CharacteristicId):
            raise TypeError("characteristic_id must be a CharacteristicId")
        if type(self.characteristic_index) is not int or self.characteristic_index < 0:
            raise ValueError("characteristic_index must be a nonnegative integer")
        _require_identifier(self.coverage_profile_id, "coverage_profile_id")
        _require_identifier(self.governing_rule_id, "governing_rule_id")
        if not isinstance(self.decision_code, TraceDecisionCode):
            raise TypeError("decision_code must be a TraceDecisionCode")
        _require_typed_tuple(self.feature_inputs, FeatureInputTrace, "feature_inputs")
        _require_typed_tuple(self.finding_refs, str, "finding_refs")


@dataclass(frozen=True, slots=True)
class RequirementEvidenceRef:
    requirement_subject_ref: RequirementSubjectRef
    evidence_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.requirement_subject_ref, RequirementSubjectRef):
            raise TypeError("requirement_subject_ref must be a RequirementSubjectRef")
        _require_identifier(self.evidence_id, "evidence_id")


@dataclass(frozen=True, slots=True)
class RequirementDiagnosticRef:
    requirement_subject_ref: RequirementSubjectRef
    feature_id: FeatureId
    diagnostic_index: int

    def __post_init__(self) -> None:
        if not isinstance(self.requirement_subject_ref, RequirementSubjectRef):
            raise TypeError("requirement_subject_ref must be a RequirementSubjectRef")
        if not isinstance(self.feature_id, FeatureId):
            raise TypeError("feature_id must be a FeatureId")
        if type(self.diagnostic_index) is not int or self.diagnostic_index < 0:
            raise ValueError("diagnostic_index must be a nonnegative integer")


@dataclass(frozen=True, slots=True)
class RequirementFindingRef:
    requirement_subject_ref: RequirementSubjectRef
    finding_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.requirement_subject_ref, RequirementSubjectRef):
            raise TypeError("requirement_subject_ref must be a RequirementSubjectRef")
        _require_identifier(self.finding_id, "finding_id")


@dataclass(frozen=True, slots=True)
class SpecificationAggregateCounts:
    computed_count: int
    unknown_count: int
    not_applicable_count: int
    total_count: int

    def __post_init__(self) -> None:
        for name in (
            "computed_count",
            "unknown_count",
            "not_applicable_count",
            "total_count",
        ):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer")
        if self.total_count != (
            self.computed_count + self.unknown_count + self.not_applicable_count
        ):
            raise ValueError("aggregate counts must sum to total_count")


@dataclass(frozen=True, slots=True)
class MetricProvenance:
    source_kind: MetricSourceKind
    source_status: SourceStatusRef
    source_explanation: str | None
    source_assessment_refs: tuple[SourceAssessmentRef, ...]
    source_trace_refs: tuple[RequirementTraceRef, ...] = ()
    evidence_refs: tuple[RequirementEvidenceRef | CrossEvidenceRef, ...] = ()
    diagnostic_refs: tuple[RequirementDiagnosticRef | CrossDiagnosticRef, ...] = ()
    finding_refs: tuple[RequirementFindingRef, ...] = ()
    cross_result_refs: tuple[CrossResultId, ...] = ()
    source_reasons: tuple[QbConsistencyReason, ...] = ()
    source_counts_or_observability: (
        SpecificationAggregateCounts | QbConsistencyObservability | None
    ) = None
    source_formula_operands: QbConsistencyFormulaOperands | None = None
    source_contract_refs: tuple[ContractRef, ...] = ()
    source_non_claim_refs: tuple[BoundedNonClaimKey, ...] = ()
    rconf_participant_ids: tuple[str, ...] = ()
    rconf_complete: bool | None = None
    materiality_diagnostic_refs: tuple[CrossDiagnosticRef, ...] = ()
    source_metric_label: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_kind, MetricSourceKind):
            raise TypeError("source_kind must be a MetricSourceKind")
        if not isinstance(self.source_status, SourceStatusRef):
            raise TypeError("source_status must be a SourceStatusRef")
        if self.source_explanation is not None:
            _require_identifier(self.source_explanation, "source_explanation")
        _require_typed_tuple(
            self.source_assessment_refs,
            (
                RequirementCharacteristicRef,
                SpecificationAggregateRef,
                QbConsistencyAssessmentRef,
            ),
            "source_assessment_refs",
        )
        if not self.source_assessment_refs:
            raise ValueError("provenance requires at least one source assessment ref")
        _require_typed_tuple(
            self.source_trace_refs, RequirementTraceRef, "source_trace_refs"
        )
        _require_typed_tuple(
            self.evidence_refs,
            (RequirementEvidenceRef, CrossEvidenceRef),
            "evidence_refs",
        )
        _require_typed_tuple(
            self.diagnostic_refs,
            (RequirementDiagnosticRef, CrossDiagnosticRef),
            "diagnostic_refs",
        )
        _require_typed_tuple(
            self.finding_refs, RequirementFindingRef, "finding_refs"
        )
        _require_typed_tuple(
            self.cross_result_refs, CrossResultId, "cross_result_refs"
        )
        _require_typed_tuple(
            self.source_reasons, QbConsistencyReason, "source_reasons"
        )
        _require_typed_tuple(
            self.source_contract_refs, ContractRef, "source_contract_refs"
        )
        _require_typed_tuple(
            self.source_non_claim_refs,
            BoundedNonClaimKey,
            "source_non_claim_refs",
        )
        _require_typed_tuple(
            self.rconf_participant_ids, str, "rconf_participant_ids"
        )
        _require_typed_tuple(
            self.materiality_diagnostic_refs,
            CrossDiagnosticRef,
            "materiality_diagnostic_refs",
        )
        for values, name in (
            (self.evidence_refs, "evidence_refs"),
            (self.diagnostic_refs, "diagnostic_refs"),
            (self.finding_refs, "finding_refs"),
            (self.cross_result_refs, "cross_result_refs"),
            (self.source_contract_refs, "source_contract_refs"),
            (self.rconf_participant_ids, "rconf_participant_ids"),
            (self.materiality_diagnostic_refs, "materiality_diagnostic_refs"),
        ):
            _require_unique(values, name)
        if self.rconf_complete is not None and type(self.rconf_complete) is not bool:
            raise TypeError("rconf_complete must be a boolean or None")
        if self.source_metric_label is not None:
            _require_identifier(self.source_metric_label, "source_metric_label")


REQUIREMENT_METRICS = (
    MetricId.RQ_COMPLETENESS,
    MetricId.RQ_VERIFIABILITY,
    MetricId.RQ_UNAMBIGUITY,
)
SPECIFICATION_METRICS = (
    MetricId.SPEC_MEAN_COMPLETENESS,
    MetricId.SPEC_MEAN_VERIFIABILITY,
    MetricId.SPEC_MEAN_UNAMBIGUITY,
    MetricId.SPEC_QB_CONSISTENCY,
)


@dataclass(frozen=True, slots=True)
class MetricEntry:
    entry_id: MetricEntryId
    metric_id: MetricId
    scope: MetricScope
    subject_ref: MetricSubjectRef
    status: MetricStatus
    applicability: MetricApplicability
    value: Fraction | None
    numeric_representation: NumericRepresentation
    source_status: SourceStatusRef
    source_assessment_refs: tuple[SourceAssessmentRef, ...]
    provenance: MetricProvenance
    rule_refs: tuple[RuleRef, ...]
    artifact_ref: ArtifactRef
    assessment_ref: AssessmentRef
    registry_ref: ContractRef
    adapter_rule_ref: RuleRef
    full_model_contract_ref: ContractRef

    def __post_init__(self) -> None:
        if not isinstance(self.entry_id, MetricEntryId):
            raise TypeError("entry_id must be a MetricEntryId")
        if not isinstance(self.metric_id, MetricId):
            raise TypeError("metric_id must be a MetricId")
        if not isinstance(self.scope, MetricScope):
            raise TypeError("scope must be a MetricScope")
        if not isinstance(self.status, MetricStatus):
            raise TypeError("status must be a MetricStatus")
        if not isinstance(self.applicability, MetricApplicability):
            raise TypeError("applicability must be a MetricApplicability")
        if not isinstance(self.numeric_representation, NumericRepresentation):
            raise TypeError("numeric_representation must be a NumericRepresentation")
        if not isinstance(self.source_status, SourceStatusRef):
            raise TypeError("source_status must be a SourceStatusRef")
        if not isinstance(self.provenance, MetricProvenance):
            raise TypeError("provenance must be MetricProvenance")
        _require_typed_tuple(
            self.source_assessment_refs,
            (
                RequirementCharacteristicRef,
                SpecificationAggregateRef,
                QbConsistencyAssessmentRef,
            ),
            "source_assessment_refs",
        )
        if not self.source_assessment_refs:
            raise ValueError("every metric entry requires a source assessment ref")
        _require_typed_tuple(self.rule_refs, RuleRef, "rule_refs")
        if not self.rule_refs:
            raise ValueError("every metric entry requires at least one rule ref")
        _require_unique(self.rule_refs, "rule_refs")

        if self.metric_id in REQUIREMENT_METRICS:
            if self.scope is not MetricScope.REQUIREMENT:
                raise ValueError("RQ metrics require REQUIREMENT scope")
            if not isinstance(self.subject_ref, RequirementSubjectRef):
                raise TypeError("requirement metrics require RequirementSubjectRef")
            if len(self.source_assessment_refs) != 1 or not isinstance(
                self.source_assessment_refs[0], RequirementCharacteristicRef
            ):
                raise ValueError(
                    "requirement metrics require exactly one characteristic ref"
                )
        else:
            if self.scope is not MetricScope.SPECIFICATION:
                raise ValueError("SPEC metrics require SPECIFICATION scope")
            if not isinstance(self.subject_ref, SpecificationSubjectRef):
                raise TypeError("specification metrics require SpecificationSubjectRef")
            if self.metric_id is MetricId.SPEC_QB_CONSISTENCY:
                if len(self.source_assessment_refs) != 1 or not isinstance(
                    self.source_assessment_refs[0], QbConsistencyAssessmentRef
                ):
                    raise ValueError("QB metric requires exactly one QB assessment ref")
            elif not isinstance(
                self.source_assessment_refs[0], SpecificationAggregateRef
            ):
                raise ValueError(
                    "specification mean metrics require an aggregate ref first"
                )

        allowed_applicability = {
            MetricStatus.AVAILABLE: {MetricApplicability.APPLICABLE},
            MetricStatus.UNKNOWN: {
                MetricApplicability.APPLICABLE,
                MetricApplicability.UNKNOWN,
            },
            MetricStatus.NOT_APPLICABLE: {MetricApplicability.NOT_APPLICABLE},
            MetricStatus.UNRESOLVED: {
                MetricApplicability.APPLICABLE,
                MetricApplicability.UNKNOWN,
            },
            MetricStatus.UNAVAILABLE: {
                MetricApplicability.APPLICABLE,
                MetricApplicability.UNKNOWN,
            },
            MetricStatus.UNSUPPORTED: {
                MetricApplicability.APPLICABLE,
                MetricApplicability.UNKNOWN,
            },
        }[self.status]
        if self.applicability not in allowed_applicability:
            raise ValueError("status/applicability combination is not allowed")
        if self.status is MetricStatus.AVAILABLE:
            if not isinstance(self.value, Fraction):
                raise ValueError("AVAILABLE requires an exact Fraction value")
            if (
                self.numeric_representation
                is not NumericRepresentation.EXACT_FRACTION
            ):
                raise ValueError("AVAILABLE requires EXACT_FRACTION representation")
        elif (
            self.value is not None
            or self.numeric_representation is not NumericRepresentation.NONE
        ):
            raise ValueError(
                "non-AVAILABLE metrics require value=None and representation NONE"
            )

        if self.assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("entry assessment and artifact refs must agree")
        if self.subject_ref.artifact_ref != self.artifact_ref:
            raise ValueError("entry subject and artifact refs must agree")
        expected_profile_id = MetricProfileId(
            self.artifact_ref,
            self.assessment_ref,
            self.registry_ref,
        )
        expected_entry_id = MetricEntryId(
            expected_profile_id,
            self.scope,
            self.subject_ref,
            self.metric_id,
        )
        if self.entry_id != expected_entry_id:
            raise ValueError("entry_id must be the structured identity of the entry")
        if self.registry_ref != METRIC_REGISTRY_REF:
            raise ValueError(
                "entry registry_ref must be FULL-MODEL-V0.1-METRICS / 1"
            )
        if self.adapter_rule_ref != ADAPTER_RULE_REF:
            raise ValueError("entry adapter_rule_ref must be P-TO-M-V0.1-001 / 1")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError(
                "entry full_model_contract_ref must be the v0.1 parent contract"
            )
        if self.source_status != self.provenance.source_status:
            raise ValueError("entry and provenance source statuses must agree")
        if self.source_assessment_refs != self.provenance.source_assessment_refs:
            raise ValueError(
                "entry and provenance source assessment refs must agree"
            )
        if any(
            source_ref.assessment_ref != self.assessment_ref
            for source_ref in self.source_assessment_refs
        ):
            raise ValueError("source assessment refs cannot cross assessments")

        source_state = self.source_status.state
        if type(source_state) is CharacteristicAssessmentState:
            expected_status, source_applicability = {
                CharacteristicAssessmentState.COMPUTED: (
                    MetricStatus.AVAILABLE,
                    {MetricApplicability.APPLICABLE},
                ),
                CharacteristicAssessmentState.UNKNOWN: (
                    MetricStatus.UNKNOWN,
                    {MetricApplicability.APPLICABLE},
                ),
                CharacteristicAssessmentState.NOT_APPLICABLE: (
                    MetricStatus.NOT_APPLICABLE,
                    {MetricApplicability.NOT_APPLICABLE},
                ),
            }[source_state]
            if (
                self.status is not expected_status
                or self.applicability not in source_applicability
            ):
                raise ValueError("metric status must preserve the exact source state")
        elif type(source_state) is QbConsistencyState:
            expected_status, source_applicability = {
                QbConsistencyState.COMPUTED: (
                    MetricStatus.AVAILABLE,
                    {MetricApplicability.APPLICABLE},
                ),
                QbConsistencyState.UNKNOWN: (
                    MetricStatus.UNKNOWN,
                    {
                        MetricApplicability.APPLICABLE,
                        MetricApplicability.UNKNOWN,
                    },
                ),
                QbConsistencyState.NOT_APPLICABLE: (
                    MetricStatus.NOT_APPLICABLE,
                    {MetricApplicability.NOT_APPLICABLE},
                ),
            }[source_state]
            if (
                self.status is not expected_status
                or self.applicability not in source_applicability
            ):
                raise ValueError("metric status must preserve the exact source state")
        elif source_state is not self.status:
            raise ValueError("partial/future source status must match metric status")


@dataclass(frozen=True, slots=True)
class MetricProfile:
    profile_id: MetricProfileId
    artifact_ref: ArtifactRef
    assessment_ref: AssessmentRef
    full_model_contract_ref: ContractRef
    registry_ref: ContractRef
    adapter_rule_ref: RuleRef
    source_snapshot_id: AssessmentSnapshotId
    entries: tuple[MetricEntry, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.profile_id, MetricProfileId):
            raise TypeError("profile_id must be a MetricProfileId")
        if self.profile_id != MetricProfileId(
            self.artifact_ref,
            self.assessment_ref,
            self.registry_ref,
        ):
            raise ValueError("profile_id must be the structured identity of the profile")
        if self.full_model_contract_ref != FULL_MODEL_CONTRACT_REF:
            raise ValueError("profile requires the Full Model v0.1 parent contract")
        if self.registry_ref != METRIC_REGISTRY_REF:
            raise ValueError("profile requires the Full Model v0.1 metric registry")
        if self.adapter_rule_ref != ADAPTER_RULE_REF:
            raise ValueError("profile requires the Full Model v0.1 adapter rule")
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        _require_typed_tuple(self.entries, MetricEntry, "entries")
        if len(self.entries) < 4 or (len(self.entries) - 4) % 3:
            raise ValueError("profile cardinality must be exactly 3n + 4")

        requirement_entry_count = len(self.entries) - 4
        requirement_subjects: list[RequirementSubjectRef] = []
        for start in range(0, requirement_entry_count, 3):
            group = self.entries[start : start + 3]
            subject = group[0].subject_ref
            if not isinstance(subject, RequirementSubjectRef):
                raise ValueError(
                    "requirement entries must precede specification entries"
                )
            if tuple(item.metric_id for item in group) != REQUIREMENT_METRICS:
                raise ValueError(
                    "requirement metrics must use fixed C, V, U registry order"
                )
            if any(
                item.scope is not MetricScope.REQUIREMENT
                or item.subject_ref != subject
                for item in group
            ):
                raise ValueError("each requirement must have one C/V/U metric group")
            requirement_subjects.append(subject)
        if len(requirement_subjects) != len(set(requirement_subjects)):
            raise ValueError("requirement subjects must be unique")
        if tuple(item.source_line for item in requirement_subjects) != tuple(
            sorted(item.source_line for item in requirement_subjects)
        ):
            raise ValueError("requirements must preserve source order")

        specification_entries = self.entries[requirement_entry_count:]
        if (
            tuple(item.metric_id for item in specification_entries)
            != SPECIFICATION_METRICS
        ):
            raise ValueError(
                "specification metrics must use the fixed registry order"
            )
        specification_subject = SpecificationSubjectRef(self.artifact_ref)
        if any(
            item.scope is not MetricScope.SPECIFICATION
            or item.subject_ref != specification_subject
            for item in specification_entries
        ):
            raise ValueError(
                "all specification metrics require the profile artifact subject"
            )

        entry_ids = tuple(item.entry_id for item in self.entries)
        _require_unique(entry_ids, "entry IDs")
        if any(
            item.entry_id.profile_id != self.profile_id
            or item.artifact_ref != self.artifact_ref
            or item.assessment_ref != self.assessment_ref
            or item.registry_ref != self.registry_ref
            or item.adapter_rule_ref != self.adapter_rule_ref
            or item.full_model_contract_ref != self.full_model_contract_ref
            for item in self.entries
        ):
            raise ValueError("every entry must share the profile context")

        characteristic_order = tuple(CharacteristicId)
        for group_index, subject in enumerate(requirement_subjects):
            start = group_index * 3
            for entry, characteristic_id in zip(
                self.entries[start : start + 3],
                characteristic_order,
                strict=True,
            ):
                source_ref = entry.source_assessment_refs[0]
                if not isinstance(source_ref, RequirementCharacteristicRef) or (
                    source_ref.requirement_subject_ref != subject
                    or source_ref.characteristic_id is not characteristic_id
                ):
                    raise ValueError(
                        "requirement source refs must match subject and registry slot"
                    )

        for entry, characteristic_id in zip(
            specification_entries[:3],
            characteristic_order,
            strict=True,
        ):
            aggregate_ref = entry.source_assessment_refs[0]
            member_refs = entry.source_assessment_refs[1:]
            if not isinstance(aggregate_ref, SpecificationAggregateRef) or (
                aggregate_ref.artifact_ref != self.artifact_ref
                or aggregate_ref.characteristic_id is not characteristic_id
            ):
                raise ValueError(
                    "specification aggregate ref must match artifact and registry slot"
                )
            if tuple(
                (
                    member.requirement_subject_ref,
                    member.characteristic_id,
                )
                for member in member_refs
                if isinstance(member, RequirementCharacteristicRef)
            ) != tuple(
                (subject, characteristic_id) for subject in requirement_subjects
            ) or any(
                not isinstance(member, RequirementCharacteristicRef)
                for member in member_refs
            ):
                raise ValueError(
                    "specification member refs must be complete and source ordered"
                )

        qb_entry = specification_entries[-1]
        qb_ref = qb_entry.source_assessment_refs[0]
        if not isinstance(qb_ref, QbConsistencyAssessmentRef) or (
            qb_ref.artifact_ref != self.artifact_ref
            or qb_ref.snapshot_id != self.source_snapshot_id
        ):
            raise ValueError("QB source ref must match profile artifact and snapshot")
        if qb_entry.provenance.source_non_claim_refs != (
            BoundedNonClaimKey.NC_QB_BASE,
        ):
            raise ValueError("QB metric must preserve exactly NC-QB-BASE")


def serialize_metric_value(value: Fraction | None) -> dict[str, str | int] | None:
    """Return the sole approved machine representation for a metric value."""

    if value is None:
        return None
    if not isinstance(value, Fraction):
        raise TypeError("metric values must be exact Fraction values or None")
    return {
        "kind": "FRACTION",
        "numerator": value.numerator,
        "denominator": value.denominator,
    }


__all__ = [
    "ADAPTER_RULE_REF",
    "FULL_MODEL_CONTRACT_REF",
    "METRIC_REGISTRY_REF",
    "REQUIREMENT_METRICS",
    "SPECIFICATION_METRICS",
    "ArtifactRef",
    "AssessmentRef",
    "ContractRef",
    "MetricApplicability",
    "MetricConstructionContext",
    "MetricEntry",
    "MetricEntryId",
    "MetricId",
    "MetricProfile",
    "MetricProfileId",
    "MetricProvenance",
    "MetricScope",
    "MetricSourceKind",
    "MetricStatus",
    "NumericRepresentation",
    "QbConsistencyAssessmentRef",
    "RequirementCharacteristicRef",
    "RequirementDiagnosticRef",
    "RequirementEvidenceRef",
    "RequirementFindingRef",
    "RequirementSubjectRef",
    "RequirementTraceRef",
    "RuleRef",
    "RuleVersionAuthority",
    "SourceStatusRef",
    "SpecificationAggregateCounts",
    "SpecificationAggregateRef",
    "SpecificationSubjectRef",
    "serialize_metric_value",
]

"""Pure construction and evaluation services for bounded dynamic evidence."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import unicodedata

from ..detectors.quantitative import (
    QUANT_CONTEXT_RULE_ID, QUANT_METRIC_RULE_ID,
)
from ..domain import (
    BoundaryInclusivity, ComparatorLabel, FeatureId, QuantitativeComponentName,
    RequirementExtractionResult, UnitLabel,
)
from ..metrics import (
    ArtifactRef, AssessmentRef, AssessmentSnapshotId, CrossDiagnosticRef,
    CrossEvidenceRef, CrossObservationRef, RequirementSubjectRef, RuleRef,
    RuleVersionAuthority,
)
from .domain import (
    Applicability, BINDING_RULE_REF, ConformanceAssessment,
    ConformanceAssessmentId, ConformanceEvaluationContext, ConformanceOperands,
    ConformanceOutcome, ConformanceProvenance, CriterionBindingId,
    CriterionBindingProvenance, CriterionBindingResult, CriterionContextIdentity,
    CriterionId, CriterionProvenance, CriterionRef,
    DynamicEvidenceReason, DynamicMetricRef, DynamicNumericRepresentation,
    DynamicObservation, DynamicObservationId, DynamicObservationProvenance,
    DynamicObservationRef, FullModelStatus,
    ObservationCollectionRef, ObservationResolution, ObservationSlotRef,
    QB_NORMALIZATION_CONTRACT_REF, QuantitativeCriterion,
    RESPONSE_TIME_METRIC_REF, SUPPORTED_CONTEXT_IDENTITY,
)


def normalize_qb_identity(text: str) -> str:
    """Apply exactly QB-NORMALIZATION / 1 to textual identity."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


@dataclass(frozen=True, slots=True)
class CriterionBindingContext:
    artifact_ref: ArtifactRef
    source_assessment_ref: AssessmentRef
    source_snapshot_id: AssessmentSnapshotId
    binding_rule_ref: RuleRef = BINDING_RULE_REF

    def __post_init__(self) -> None:
        if self.source_assessment_ref.artifact_ref != self.artifact_ref:
            raise ValueError("source assessment must name the binding artifact")
        if not isinstance(self.source_snapshot_id, AssessmentSnapshotId):
            raise TypeError("source_snapshot_id must be an AssessmentSnapshotId")
        if self.binding_rule_ref != BINDING_RULE_REF:
            raise ValueError("unsupported criterion binding rule")


def _stable_rule_ref(rule_id: str) -> RuleRef:
    return RuleRef(rule_id, None, RuleVersionAuthority.STABLE_RULE_ID_POLICY)


def _binding_shell(
    source: RequirementExtractionResult,
    selected_ref: CrossObservationRef | None,
    context: CriterionBindingContext,
) -> tuple[CriterionBindingId, CriterionBindingProvenance, RequirementSubjectRef]:
    requirement = source.requirement
    subject = RequirementSubjectRef(
        context.artifact_ref, requirement.id, requirement.source_line,
    )
    binding_id = CriterionBindingId(
        context.artifact_ref, context.source_assessment_ref, subject,
        context.source_snapshot_id, selected_ref, context.binding_rule_ref,
    )
    evidence_refs = tuple(
        CrossEvidenceRef(requirement.id, item.evidence_id) for item in source.evidence
    )
    outcome = source.features.quantitative_constraints
    diagnostic_refs = tuple(
        CrossDiagnosticRef(requirement.id, FeatureId.QUANTITATIVE_CONSTRAINT, index)
        for index, _ in enumerate(outcome.diagnostics)
    )
    provenance = CriterionBindingProvenance(
        context.source_assessment_ref, context.source_snapshot_id, subject,
        selected_ref, context.binding_rule_ref, evidence_refs, diagnostic_refs,
    )
    return binding_id, provenance, subject


def _nonvalue_binding(
    binding_id: CriterionBindingId,
    provenance: CriterionBindingProvenance,
    status: FullModelStatus,
    applicability: Applicability,
    *reasons: DynamicEvidenceReason,
) -> CriterionBindingResult:
    return CriterionBindingResult(
        binding_id, status, applicability, None,
        binding_id.source_observation_ref, tuple(reasons), provenance,
    )


def bind_quantitative_criterion(
    source: RequirementExtractionResult,
    source_observation_ref: CrossObservationRef | None,
    context: CriterionBindingContext,
) -> CriterionBindingResult:
    """Bind one explicitly selected accepted quantitative observation."""
    if not isinstance(source, RequirementExtractionResult):
        raise TypeError("source must be a RequirementExtractionResult")
    if source_observation_ref is not None and not isinstance(
        source_observation_ref, CrossObservationRef
    ):
        raise TypeError("source_observation_ref must be a CrossObservationRef or None")
    binding_id, binding_provenance, subject = _binding_shell(
        source, source_observation_ref, context,
    )
    observations = source.features.quantitative_constraints.observations
    if source_observation_ref is None:
        if not observations and source.features.quantitative_constraints.processing_status.value == "COMPLETE":
            return _nonvalue_binding(
                binding_id, binding_provenance, FullModelStatus.NOT_APPLICABLE,
                Applicability.NOT_APPLICABLE,
                DynamicEvidenceReason.NO_APPLICABLE_RESPONSE_TIME_CRITERION,
            )
        return _nonvalue_binding(
            binding_id, binding_provenance, FullModelStatus.UNRESOLVED,
            Applicability.UNKNOWN,
            DynamicEvidenceReason.SOURCE_OBSERVATION_SELECTION_UNRESOLVED,
        )
    if (
        source_observation_ref.requirement_id != source.requirement.id
        or source_observation_ref.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT
        or source_observation_ref.observation_index >= len(observations)
    ):
        return _nonvalue_binding(
            binding_id, binding_provenance, FullModelStatus.UNRESOLVED,
            Applicability.UNKNOWN,
            DynamicEvidenceReason.SOURCE_OBSERVATION_SELECTION_UNRESOLVED,
        )
    observation = observations[source_observation_ref.observation_index]
    evidence_by_id = {item.evidence_id: item for item in source.evidence}
    if observation.metric is None or QuantitativeComponentName.METRIC in observation.unresolved_components:
        return _nonvalue_binding(
            binding_id, binding_provenance, FullModelStatus.UNRESOLVED,
            Applicability.UNKNOWN, DynamicEvidenceReason.METRIC_IDENTITY_UNRESOLVED,
        )
    metric_sources = tuple(evidence_by_id.get(ref) for ref in observation.metric.evidence_refs)
    if any(item is None for item in metric_sources):
        return _nonvalue_binding(
            binding_id, binding_provenance, FullModelStatus.UNRESOLVED,
            Applicability.UNKNOWN, DynamicEvidenceReason.PROVENANCE_UNRESOLVED,
        )
    if (
        len(metric_sources) != 1
        or metric_sources[0].rule_id != QUANT_METRIC_RULE_ID
        or normalize_qb_identity(metric_sources[0].text)
        != RESPONSE_TIME_METRIC_REF.normalized_source_metric
    ):
        return _nonvalue_binding(
            binding_id, binding_provenance, FullModelStatus.NOT_APPLICABLE,
            Applicability.NOT_APPLICABLE,
            DynamicEvidenceReason.NO_APPLICABLE_RESPONSE_TIME_CRITERION,
        )
    unresolved = set(observation.unresolved_components)
    if observation.comparator is None or QuantitativeComponentName.COMPARATOR in unresolved:
        return _nonvalue_binding(
            binding_id, binding_provenance, FullModelStatus.UNRESOLVED,
            Applicability.APPLICABLE, DynamicEvidenceReason.COMPARATOR_UNRESOLVED,
        )
    if observation.unit is None or QuantitativeComponentName.UNIT in unresolved:
        return _nonvalue_binding(
            binding_id, binding_provenance, FullModelStatus.UNRESOLVED,
            Applicability.APPLICABLE, DynamicEvidenceReason.UNIT_UNRESOLVED,
        )
    if observation.context is None or QuantitativeComponentName.CONTEXT in unresolved:
        return _nonvalue_binding(
            binding_id, binding_provenance, FullModelStatus.UNRESOLVED,
            Applicability.APPLICABLE,
            DynamicEvidenceReason.CONTEXT_IDENTITY_UNRESOLVED,
        )
    context_sources = tuple(evidence_by_id.get(ref) for ref in observation.context.evidence_refs)
    if (
        len(context_sources) != 1 or context_sources[0] is None
        or context_sources[0].rule_id != QUANT_CONTEXT_RULE_ID
    ):
        return _nonvalue_binding(
            binding_id, binding_provenance, FullModelStatus.UNRESOLVED,
            Applicability.APPLICABLE, DynamicEvidenceReason.PROVENANCE_UNRESOLVED,
        )
    context_identity = CriterionContextIdentity(
        QB_NORMALIZATION_CONTRACT_REF,
        normalize_qb_identity(context_sources[0].text),
    )
    source_refs = tuple(
        CrossEvidenceRef(source.requirement.id, ref) for ref in observation.evidence_refs
    )
    component_ref_ids = tuple(
        ref
        for component in (
            observation.metric, observation.comparator, observation.value,
            observation.unit, observation.context,
        )
        if component is not None
        for ref in component.evidence_refs
    )
    component_refs = tuple(
        CrossEvidenceRef(source.requirement.id, ref)
        for ref in dict.fromkeys(component_ref_ids)
    )
    diagnostic_refs = binding_provenance.diagnostic_refs
    source_rule_ids = tuple(dict.fromkeys(
        [evidence_by_id[ref].rule_id for ref in observation.evidence_refs]
        + [item.rule_id for item in source.features.quantitative_constraints.diagnostics]
    ))
    criterion_provenance = CriterionProvenance(
        subject, context.source_assessment_ref, context.source_snapshot_id,
        source_observation_ref,
        source.features.quantitative_constraints.processing_status,
        component_refs, source_refs, diagnostic_refs,
        tuple(_stable_rule_ref(item) for item in source_rule_ids),
        QB_NORMALIZATION_CONTRACT_REF, context.binding_rule_ref,
    )
    criterion_id = CriterionId(
        context.artifact_ref, context.source_assessment_ref, subject,
        context.source_snapshot_id, source_observation_ref,
        context.binding_rule_ref,
    )
    criterion = QuantitativeCriterion(
        criterion_id, subject, context.artifact_ref,
        context.source_assessment_ref, context.source_snapshot_id,
        source_observation_ref, RESPONSE_TIME_METRIC_REF,
        observation.comparator.label, observation.comparator.inclusivity,
        observation.value.decimal_value, observation.unit.label,
        context_identity, criterion_provenance, context.binding_rule_ref,
    )
    reasons: list[DynamicEvidenceReason] = []
    if (
        criterion.comparator is not ComparatorLabel.LESS_THAN_OR_EQUAL
        or criterion.inclusivity is not BoundaryInclusivity.INCLUSIVE
    ):
        reasons.append(DynamicEvidenceReason.COMPARATOR_UNSUPPORTED)
    if criterion.unit is not UnitLabel.SECOND:
        reasons.append(DynamicEvidenceReason.UNIT_UNSUPPORTED)
    if criterion.context_identity != SUPPORTED_CONTEXT_IDENTITY:
        reasons.append(DynamicEvidenceReason.CONTEXT_UNSUPPORTED)
    if not criterion.bound.is_finite():
        reasons.append(DynamicEvidenceReason.OBSERVATION_NUMERIC_UNSUPPORTED)
    if reasons:
        return CriterionBindingResult(
            binding_id, FullModelStatus.UNSUPPORTED, Applicability.APPLICABLE,
            criterion, source_observation_ref, tuple(reasons), binding_provenance,
        )
    return CriterionBindingResult(
        binding_id, FullModelStatus.AVAILABLE, Applicability.APPLICABLE,
        criterion, source_observation_ref, (), binding_provenance,
    )


def make_dynamic_observation(
    slot_ref: ObservationSlotRef,
    metric_ref: DynamicMetricRef,
    observed_value: Decimal,
    unit: UnitLabel,
    context_identity: CriterionContextIdentity,
    source_record_ref: str,
) -> DynamicObservation:
    """Construct one lossless controlled fixture observation."""
    collection = slot_ref.collection_ref
    provenance = DynamicObservationProvenance(
        collection.product_ref, collection.source_kind, collection,
        collection.environment_ref, slot_ref.fixture_sequence,
        source_record_ref, metric_ref, unit, context_identity,
        DynamicNumericRepresentation.EXACT_DECIMAL,
    )
    return DynamicObservation(
        DynamicObservationId(collection, slot_ref.fixture_sequence), slot_ref,
        collection.product_ref, metric_ref, observed_value, unit,
        context_identity, collection.source_kind, collection,
        slot_ref.fixture_sequence, None, provenance,
    )


def resolve_dynamic_observation(
    expected_slot: ObservationSlotRef,
    supplied_observation: DynamicObservation | None,
) -> ObservationResolution:
    """Resolve an externally supplied record without collecting a measurement."""
    if supplied_observation is None:
        return ObservationResolution(
            expected_slot, FullModelStatus.UNAVAILABLE, Applicability.APPLICABLE,
            None, (DynamicEvidenceReason.OBSERVATION_NOT_COLLECTED,), (),
        )
    if not isinstance(supplied_observation, DynamicObservation):
        raise TypeError("supplied_observation must be DynamicObservation or None")
    provenance_refs = (supplied_observation.provenance.source_record_ref,)
    if supplied_observation.slot_ref != expected_slot:
        return ObservationResolution(
            expected_slot, FullModelStatus.UNRESOLVED, Applicability.UNKNOWN,
            None, (DynamicEvidenceReason.OBSERVATION_IDENTITY_UNRESOLVED,),
            provenance_refs,
        )
    if not supplied_observation.observed_value.is_finite():
        return ObservationResolution(
            expected_slot, FullModelStatus.UNSUPPORTED, Applicability.APPLICABLE,
            None, (DynamicEvidenceReason.OBSERVATION_NUMERIC_UNSUPPORTED,),
            provenance_refs,
        )
    return ObservationResolution(
        expected_slot, FullModelStatus.AVAILABLE, Applicability.APPLICABLE,
        supplied_observation, (), provenance_refs,
    )


def resolve_dynamic_observations(
    collection_ref: ObservationCollectionRef,
    supplied: tuple[DynamicObservation, ...],
) -> tuple[ObservationResolution, ...]:
    """Validate collection-local uniqueness and resolve in sequence order."""
    if not isinstance(supplied, tuple) or any(
        not isinstance(item, DynamicObservation) for item in supplied
    ):
        raise TypeError("supplied must be a tuple of DynamicObservation values")
    if any(item.collection_ref != collection_ref for item in supplied):
        raise ValueError("every observation must belong to collection_ref")
    sequences = [item.fixture_sequence for item in supplied]
    if len(sequences) != len(set(sequences)):
        raise ValueError("fixture sequences must be unique within a collection")
    return tuple(
        resolve_dynamic_observation(item.slot_ref, item)
        for item in sorted(supplied, key=lambda item: item.fixture_sequence)
    )


def _conformance(
    binding: CriterionBindingResult,
    resolution: ObservationResolution,
    context: ConformanceEvaluationContext,
    status: FullModelStatus,
    applicability: Applicability,
    outcome: ConformanceOutcome | None,
    explanation: str,
    reasons: tuple[DynamicEvidenceReason, ...],
    operands: ConformanceOperands | None,
) -> ConformanceAssessment:
    criterion = binding.criterion
    observation = resolution.observation
    criterion_ref = CriterionRef(criterion.criterion_id) if criterion is not None else None
    observation_ref = (
        DynamicObservationRef(observation.observation_id)
        if observation is not None else None
    )
    evidence_refs = criterion.provenance.evidence_refs if criterion is not None else ()
    provenance = ConformanceProvenance(
        criterion_ref,
        observation_ref if observation_ref is not None else resolution.slot_ref,
        evidence_refs,
        observation.provenance.source_record_ref if observation is not None else None,
        context.evaluator_rule_ref, context.dynamic_contract_ref,
        context.full_model_contract_ref, operands, reasons,
    )
    conformance_id = ConformanceAssessmentId(
        context.dynamic_assessment_ref, binding.binding_id,
        resolution.slot_ref, context.evaluator_rule_ref,
    )
    return ConformanceAssessment(
        conformance_id, context.dynamic_assessment_ref, binding.binding_id,
        criterion.criterion_id if criterion is not None else None,
        resolution.slot_ref,
        observation.observation_id if observation is not None else None,
        status, applicability, outcome, explanation, reasons,
        criterion_ref, observation_ref, evidence_refs, provenance,
        context.evaluator_rule_ref,
    )


def assess_conformance(
    criterion_binding: CriterionBindingResult,
    observation_resolution: ObservationResolution,
    context: ConformanceEvaluationContext,
) -> ConformanceAssessment:
    """Apply the exact supported response-time comparison and status precedence."""
    if context.dynamic_assessment_ref.artifact_ref != criterion_binding.binding_id.artifact_ref:
        raise ValueError("dynamic assessment artifact must match criterion binding")
    if context.dynamic_assessment_ref.collection_ref != observation_resolution.slot_ref.collection_ref:
        raise ValueError("observation slot must belong to the assessment collection")
    if criterion_binding.status is not FullModelStatus.AVAILABLE:
        return _conformance(
            criterion_binding, observation_resolution, context,
            criterion_binding.status, criterion_binding.applicability, None,
            "Criterion binding did not provide an evaluator-ready criterion.",
            criterion_binding.reasons, None,
        )
    if observation_resolution.status is not FullModelStatus.AVAILABLE:
        return _conformance(
            criterion_binding, observation_resolution, context,
            observation_resolution.status, observation_resolution.applicability,
            None, "Observation resolution did not provide an available observation.",
            observation_resolution.reasons, None,
        )
    criterion = criterion_binding.criterion
    observation = observation_resolution.observation
    if criterion is None or observation is None:
        raise ValueError("available inputs must contain criterion and observation")
    reasons: list[DynamicEvidenceReason] = []
    metric_unsupported = criterion.metric_ref != observation.metric_ref
    if criterion.unit is not UnitLabel.SECOND or observation.unit is not UnitLabel.SECOND:
        reasons.append(DynamicEvidenceReason.UNIT_UNSUPPORTED)
    if (
        criterion.context_identity != SUPPORTED_CONTEXT_IDENTITY
        or observation.context_identity != criterion.context_identity
    ):
        reasons.append(DynamicEvidenceReason.CONTEXT_UNSUPPORTED)
    if not criterion.bound.is_finite() or not observation.observed_value.is_finite():
        reasons.append(DynamicEvidenceReason.OBSERVATION_NUMERIC_UNSUPPORTED)
    if metric_unsupported or reasons:
        return _conformance(
            criterion_binding, observation_resolution, context,
            FullModelStatus.UNSUPPORTED, Applicability.APPLICABLE, None,
            "Resolved criterion and observation are outside the closed evaluator.",
            tuple(dict.fromkeys(reasons)), None,
        )
    operands = ConformanceOperands(
        criterion.comparator, criterion.inclusivity, criterion.bound,
        criterion.unit, criterion.context_identity, observation.observed_value,
        observation.unit, observation.context_identity,
    )
    outcome = (
        ConformanceOutcome.CONFORMS
        if observation.observed_value <= criterion.bound
        else ConformanceOutcome.DOES_NOT_CONFORM
    )
    return _conformance(
        criterion_binding, observation_resolution, context,
        FullModelStatus.AVAILABLE, Applicability.APPLICABLE, outcome,
        "Exact response-time observation compared with the requirement's own bound.",
        (), operands,
    )

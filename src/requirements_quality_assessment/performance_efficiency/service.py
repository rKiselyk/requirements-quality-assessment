"""Deterministic construction of the bounded Performance Efficiency profile."""

from __future__ import annotations

from dataclasses import dataclass

from ..cross_analysis.domain import (
    ComparisonKey,
    ComparisonOperand,
    CrossRequirementResult,
    CrossResultState,
)
from ..cross_analysis.specification import SpecificationAssessmentResult
from ..dynamic_evidence import (
    Applicability,
    BINDING_RULE_REF,
    ConformanceAssessment,
    CriterionBindingResult,
    DYNAMIC_CONTRACT_REF,
    DYNAMIC_METRIC_REGISTRY_REF,
    EVALUATOR_RULE_REF,
    FullModelStatus,
    ObservationResolution,
    QB_NORMALIZATION_CONTRACT_REF,
    RESPONSE_TIME_METRIC_REF,
    SUPPORTED_CONTEXT_IDENTITY,
)
from ..dynamic_evidence.domain import CriterionRef, DynamicObservationRef
from ..metrics import (
    ADAPTER_RULE_REF,
    METRIC_REGISTRY_REF,
    MetricApplicability,
    MetricEntry,
    MetricId,
    MetricProfile,
    MetricStatus,
    RequirementDiagnosticRef,
    RequirementEvidenceRef,
    RequirementFindingRef,
    RequirementSubjectRef,
    RequirementTraceRef,
)
from .domain import (
    AvailabilityPoint,
    ConformanceFeatureValue,
    CriterionFeatureValue,
    ExternalDynamicSourceRef,
    FeatureProfileProvenance,
    FeatureReason,
    METRIC_PROFILE_CONTRACT_REF,
    ObservationFeatureValue,
    PE_FEATURE_EFFECTS,
    PE_FEATURE_REGISTRY,
    PerformanceEfficiencyFeature,
    PerformanceEfficiencyFeatureConstructionContext,
    PerformanceEfficiencyFeatureEntryId,
    PerformanceEfficiencyFeatureId,
    PerformanceEfficiencyFeatureProfile,
    PerformanceEfficiencyFeatureProfileId,
    ProductQualityCharacteristicId,
    QbTargetGateDecision,
    QbTargetGateFeatureValue,
    RequirementMetricFeatureValue,
)


_REQUIREMENT_FEATURES = (
    (
        PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS,
        MetricId.RQ_COMPLETENESS,
    ),
    (
        PerformanceEfficiencyFeatureId.REQUIREMENT_VERIFIABILITY,
        MetricId.RQ_VERIFIABILITY,
    ),
    (
        PerformanceEfficiencyFeatureId.REQUIREMENT_UNAMBIGUITY,
        MetricId.RQ_UNAMBIGUITY,
    ),
)


def _metric_status(status: MetricStatus) -> FullModelStatus:
    return FullModelStatus(status.value)


def _metric_applicability(value: MetricApplicability) -> Applicability:
    return Applicability(value.value)


def _operand_could_match(operand: ComparisonOperand, target: ComparisonKey) -> bool:
    return all(
        actual is None or actual == expected
        for actual, expected in (
            (operand.normalized_metric, target.normalized_metric),
            (operand.normalized_context, target.normalized_context),
            (operand.unit, target.unit),
        )
    )


@dataclass(frozen=True, slots=True)
class _GateProjection:
    decision: QbTargetGateDecision
    relevant_results: tuple[CrossRequirementResult, ...]


def _project_qb_gate(
    source: SpecificationAssessmentResult,
    target: ComparisonKey,
) -> _GateProjection:
    conflicts = tuple(
        result
        for result in source.cross_results
        if result.state is CrossResultState.CONFIRMED_CONFLICT
        and result.comparison_key == target
    )
    unresolved = tuple(
        result
        for result in source.cross_results
        if result.state is CrossResultState.ASSESSMENT_UNRESOLVED
        and _operand_could_match(result.operands.left, target)
        and _operand_could_match(result.operands.right, target)
    )
    compatible = tuple(
        result
        for result in source.cross_results
        if result.state is CrossResultState.COMPATIBLE_WITHIN_RULE
        and result.comparison_key == target
    )
    relevant_ids = {
        result.result_id for result in (*conflicts, *unresolved, *compatible)
    }
    relevant = tuple(
        result for result in source.cross_results if result.result_id in relevant_ids
    )
    if conflicts:
        decision = QbTargetGateDecision.TARGET_CONFLICT
    elif unresolved or source.materiality.qb_material_count > 0:
        # A QB-material unresolved extraction cannot be proven unrelated to the
        # target without inventing a new identity heuristic.
        decision = QbTargetGateDecision.TARGET_UNRESOLVED
    elif compatible:
        decision = QbTargetGateDecision.TARGET_CLEAR
    else:
        decision = QbTargetGateDecision.TARGET_NOT_APPLICABLE
    return _GateProjection(decision, relevant)


class PerformanceEfficiencyFeatureProfileBuilder:
    """Map completed ``M + E_stat + E_dyn`` records to immutable ``X_PE``."""

    def build(
        self,
        metric_profile: MetricProfile,
        qb_source: SpecificationAssessmentResult,
        criterion_binding: CriterionBindingResult,
        observation_resolution: ObservationResolution,
        conformance: ConformanceAssessment,
        context: PerformanceEfficiencyFeatureConstructionContext,
    ) -> PerformanceEfficiencyFeatureProfile:
        self._validate_inputs(
            metric_profile,
            qb_source,
            criterion_binding,
            observation_resolution,
            conformance,
            context,
        )
        profile_id = PerformanceEfficiencyFeatureProfileId(
            context.artifact_ref,
            context.source_assessment_ref,
            context.metric_profile_ref,
            context.dynamic_assessment_ref,
            context.product_ref,
            context.process_state_ref,
            context.feature_registry_ref,
            context.mapping_rule_ref,
        )
        subject = criterion_binding.binding_id.requirement_subject_ref
        criterion = criterion_binding.criterion
        target_key = (
            None
            if criterion_binding.status is not FullModelStatus.AVAILABLE
            else ComparisonKey(
                criterion.metric_ref.normalized_source_metric,
                criterion.context_identity.normalized_text,
                criterion.unit,
            )
        )

        requirement_entries = tuple(
            self._requirement_entry(metric_profile, subject, metric_id)
            for _, metric_id in _REQUIREMENT_FEATURES
        )
        qb_entry = self._metric_entry(metric_profile, MetricId.SPEC_QB_CONSISTENCY)
        gate = None if target_key is None else _project_qb_gate(qb_source, target_key)

        features = (
            self._criterion_feature(profile_id, criterion_binding, context),
            *(
                self._requirement_feature(
                    profile_id, feature_id, entry, criterion_binding, context
                )
                for (feature_id, _), entry in zip(
                    _REQUIREMENT_FEATURES, requirement_entries, strict=True
                )
            ),
            self._qb_feature(
                profile_id,
                qb_entry,
                gate,
                target_key,
                criterion_binding,
                context,
            ),
            self._observation_feature(
                profile_id, observation_resolution, context
            ),
            self._conformance_feature(profile_id, conformance, context),
        )
        status, applicability = self._profile_state(features, gate)
        entry_ids = tuple(item.feature_entry_id for item in features)
        collection = context.dynamic_assessment_ref.collection_ref
        provenance = FeatureProfileProvenance(
            artifact_ref=context.artifact_ref,
            source_assessment_ref=context.source_assessment_ref,
            source_snapshot_id=metric_profile.source_snapshot_id,
            metric_profile_ref=metric_profile.profile_id,
            criterion_binding_ref=criterion_binding.binding_id,
            observation_resolution_ref=observation_resolution.slot_ref,
            conformance_assessment_ref=conformance.conformance_id,
            dynamic_assessment_ref=context.dynamic_assessment_ref,
            product_ref=context.product_ref,
            environment_ref_or_none=collection.environment_ref,
            collection_ref_or_none=collection,
            process_state_ref=context.process_state_ref,
            ordered_feature_entry_refs=entry_ids,
            source_contract_refs=tuple(
                dict.fromkeys(
                    (
                        context.full_model_contract_ref,
                        METRIC_PROFILE_CONTRACT_REF,
                        context.feature_contract_ref,
                        metric_profile.registry_ref,
                        *qb_entry.provenance.source_contract_refs,
                        DYNAMIC_CONTRACT_REF,
                        DYNAMIC_METRIC_REGISTRY_REF,
                        QB_NORMALIZATION_CONTRACT_REF,
                        context.feature_registry_ref,
                    )
                )
            ),
            rule_refs=tuple(
                dict.fromkeys(
                    (
                        metric_profile.adapter_rule_ref,
                        *(rule for feature in features for rule in feature.rule_refs),
                        criterion_binding.binding_id.binding_rule_ref,
                        conformance.evaluator_rule_ref,
                        context.mapping_rule_ref,
                    )
                )
            ),
        )
        return PerformanceEfficiencyFeatureProfile(
            profile_id=profile_id,
            characteristic_id=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
            artifact_ref=context.artifact_ref,
            source_assessment_ref=context.source_assessment_ref,
            metric_profile_ref=metric_profile.profile_id,
            dynamic_assessment_ref=context.dynamic_assessment_ref,
            product_ref=context.product_ref,
            process_state_ref=context.process_state_ref,
            criterion_subject_ref=subject,
            target_key=target_key,
            status=status,
            applicability=applicability,
            features=features,
            provenance=provenance,
            registry_ref=context.feature_registry_ref,
            mapping_rule_ref=context.mapping_rule_ref,
        )

    @staticmethod
    def _validate_inputs(
        metric_profile: MetricProfile,
        qb_source: SpecificationAssessmentResult,
        binding: CriterionBindingResult,
        resolution: ObservationResolution,
        conformance: ConformanceAssessment,
        context: PerformanceEfficiencyFeatureConstructionContext,
    ) -> None:
        if not isinstance(metric_profile, MetricProfile):
            raise TypeError("metric_profile must be a MetricProfile")
        if not isinstance(qb_source, SpecificationAssessmentResult):
            raise TypeError("qb_source must be a SpecificationAssessmentResult")
        if not isinstance(binding, CriterionBindingResult):
            raise TypeError("criterion_binding must be a CriterionBindingResult")
        if not isinstance(resolution, ObservationResolution):
            raise TypeError("observation_resolution must be an ObservationResolution")
        if not isinstance(conformance, ConformanceAssessment):
            raise TypeError("conformance must be a ConformanceAssessment")
        if not isinstance(context, PerformanceEfficiencyFeatureConstructionContext):
            raise TypeError("context must be a feature construction context")

        if metric_profile.profile_id != context.metric_profile_ref:
            raise ValueError("metric profile identity does not match construction context")
        if metric_profile.artifact_ref != context.artifact_ref:
            raise ValueError("metric profile and feature context cannot cross artifacts")
        if metric_profile.assessment_ref != context.source_assessment_ref:
            raise ValueError("metric profile and feature context cannot cross assessments")
        if metric_profile.registry_ref != METRIC_REGISTRY_REF:
            raise ValueError("metric profile uses an unsupported registry")
        if metric_profile.adapter_rule_ref != ADAPTER_RULE_REF:
            raise ValueError("metric profile uses an unsupported adapter rule")
        if metric_profile.source_snapshot_id != qb_source.snapshot_id:
            raise ValueError("metric profile and QB source cannot cross snapshots")

        qb_entry = PerformanceEfficiencyFeatureProfileBuilder._metric_entry(
            metric_profile, MetricId.SPEC_QB_CONSISTENCY
        )
        expected_cross_refs = tuple(item.result_id for item in qb_source.cross_results)
        if qb_entry.provenance.cross_result_refs != expected_cross_refs:
            raise ValueError("QB metric provenance and QB source results must agree")
        qb_ref = qb_entry.source_assessment_refs[0]
        if qb_ref.snapshot_id != qb_source.snapshot_id:
            raise ValueError("QB metric source ref and QB source cannot cross snapshots")
        if qb_ref.assessment_ref != context.source_assessment_ref:
            raise ValueError("QB metric source ref and context cannot cross assessments")
        if (
            qb_entry.provenance.materiality_diagnostic_refs
            != qb_source.specification_assessment.qb_consistency.materiality_diagnostic_refs
        ):
            raise ValueError("QB materiality provenance must match its source")

        binding_id = binding.binding_id
        if binding_id.artifact_ref != context.artifact_ref:
            raise ValueError("criterion binding and context cannot cross artifacts")
        if binding_id.source_assessment_ref != context.source_assessment_ref:
            raise ValueError("criterion binding and context cannot cross assessments")
        if binding_id.source_snapshot_id != metric_profile.source_snapshot_id:
            raise ValueError("criterion binding and metric profile cannot cross snapshots")
        if binding_id.binding_rule_ref != BINDING_RULE_REF:
            raise ValueError("criterion binding uses an unsupported rule")
        if binding_id.requirement_subject_ref not in {
            item.subject_ref
            for item in metric_profile.entries
            if isinstance(item.subject_ref, RequirementSubjectRef)
        }:
            raise ValueError("criterion subject is absent from the metric profile")
        criterion = binding.criterion
        if binding.status is FullModelStatus.AVAILABLE:
            if criterion is None:
                raise ValueError("available criterion binding has no criterion")
            if (
                criterion.metric_ref != RESPONSE_TIME_METRIC_REF
                or criterion.context_identity != SUPPORTED_CONTEXT_IDENTITY
                or criterion.binding_rule_ref != BINDING_RULE_REF
            ):
                raise ValueError("available criterion is outside the closed feature contract")
            if criterion.requirement_subject_ref != binding_id.requirement_subject_ref:
                raise ValueError("criterion and binding subjects must agree")

        dynamic_ref = context.dynamic_assessment_ref
        if conformance.dynamic_assessment_ref != dynamic_ref:
            raise ValueError("conformance and context cannot cross dynamic assessments")
        if dynamic_ref.collection_ref != resolution.slot_ref.collection_ref:
            raise ValueError("observation resolution and context cannot cross collections")
        if dynamic_ref.product_ref != context.product_ref:
            raise ValueError("dynamic assessment and context cannot cross products")
        if conformance.criterion_binding_id != binding.binding_id:
            raise ValueError("conformance must reference the selected criterion binding")
        if conformance.observation_slot_ref != resolution.slot_ref:
            raise ValueError("conformance must reference the selected observation slot")
        if conformance.evaluator_rule_ref != EVALUATOR_RULE_REF:
            raise ValueError("conformance uses an unsupported evaluator rule")
        expected_criterion_id = None if criterion is None else criterion.criterion_id
        if conformance.criterion_id != expected_criterion_id:
            raise ValueError("conformance criterion identity does not match the binding")
        observation = resolution.observation
        expected_observation_id = (
            None if observation is None else observation.observation_id
        )
        if conformance.observation_id != expected_observation_id:
            raise ValueError("conformance observation identity does not match resolution")
        if observation is not None:
            if observation.product_ref != context.product_ref:
                raise ValueError("observation and context cannot cross products")
            if observation.collection_ref != dynamic_ref.collection_ref:
                raise ValueError("observation and context cannot cross collections")

    @staticmethod
    def _metric_entry(profile: MetricProfile, metric_id: MetricId) -> MetricEntry:
        matches = tuple(item for item in profile.entries if item.metric_id is metric_id)
        if len(matches) != 1:
            raise ValueError(f"metric profile must contain exactly one {metric_id.value}")
        return matches[0]

    @staticmethod
    def _requirement_entry(
        profile: MetricProfile,
        subject: RequirementSubjectRef,
        metric_id: MetricId,
    ) -> MetricEntry:
        matches = tuple(
            item
            for item in profile.entries
            if item.metric_id is metric_id and item.subject_ref == subject
        )
        if len(matches) != 1:
            raise ValueError(
                f"metric profile must contain exactly one {metric_id.value} for criterion subject"
            )
        return matches[0]

    @staticmethod
    def _feature(
        profile_id: PerformanceEfficiencyFeatureProfileId,
        feature_id: PerformanceEfficiencyFeatureId,
        *,
        status: FullModelStatus,
        applicability: Applicability,
        typed_value,
        source_refs: tuple,
        evidence_refs: tuple,
        provenance_refs: tuple,
        product_ref,
        availability_point: AvailabilityPoint,
        rule_refs: tuple,
        reasons: tuple,
        explanation: str,
        context: PerformanceEfficiencyFeatureConstructionContext,
    ) -> PerformanceEfficiencyFeature:
        ordinal = PE_FEATURE_REGISTRY.index(feature_id)
        return PerformanceEfficiencyFeature(
            feature_entry_id=PerformanceEfficiencyFeatureEntryId(
                profile_id, feature_id
            ),
            feature_id=feature_id,
            characteristic_id=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
            effect=PE_FEATURE_EFFECTS[ordinal],
            status=status,
            applicability=applicability,
            typed_value=typed_value,
            source_refs=source_refs,
            evidence_refs=evidence_refs,
            provenance_refs=provenance_refs,
            artifact_ref=context.artifact_ref,
            source_assessment_ref=context.source_assessment_ref,
            product_ref=product_ref,
            availability_point=availability_point,
            rule_refs=rule_refs,
            reasons=reasons,
            explanation=explanation,
        )

    def _criterion_feature(
        self,
        profile_id: PerformanceEfficiencyFeatureProfileId,
        binding: CriterionBindingResult,
        context: PerformanceEfficiencyFeatureConstructionContext,
    ) -> PerformanceEfficiencyFeature:
        criterion = binding.criterion
        value = None
        if binding.status is FullModelStatus.AVAILABLE:
            value = CriterionFeatureValue(
                criterion_ref=CriterionRef(criterion.criterion_id),
                metric_ref=criterion.metric_ref,
                comparator=criterion.comparator,
                inclusivity=criterion.inclusivity,
                exact_decimal_bound=criterion.bound,
                unit=criterion.unit,
                context_identity=criterion.context_identity,
            )
        evidence = (
            binding.provenance.evidence_refs
            if criterion is None
            else criterion.provenance.evidence_refs
        )
        diagnostics = (
            binding.provenance.diagnostic_refs
            if criterion is None
            else criterion.provenance.diagnostic_refs
        )
        return self._feature(
            profile_id,
            PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME,
            status=binding.status,
            applicability=binding.applicability,
            typed_value=value,
            source_refs=(binding.binding_id,),
            evidence_refs=evidence,
            provenance_refs=diagnostics,
            product_ref=None,
            availability_point=AvailabilityPoint.CRITERION_BINDING_AVAILABLE,
            rule_refs=(binding.binding_id.binding_rule_ref,),
            reasons=binding.reasons,
            explanation=(
                "Source-backed response-time criterion selected without reparsing."
                if value is not None
                else "Criterion binding state preserved without manufacturing a target."
            ),
            context=context,
        )

    def _requirement_feature(
        self,
        profile_id: PerformanceEfficiencyFeatureProfileId,
        feature_id: PerformanceEfficiencyFeatureId,
        entry: MetricEntry,
        binding: CriterionBindingResult,
        context: PerformanceEfficiencyFeatureConstructionContext,
    ) -> PerformanceEfficiencyFeature:
        status = _metric_status(entry.status)
        applicability = _metric_applicability(entry.applicability)
        value = (
            RequirementMetricFeatureValue(
                entry.entry_id,
                entry.value,
                entry.numeric_representation,
                entry.source_status,
            )
            if status is FullModelStatus.AVAILABLE
            else None
        )
        evidence = tuple(
            item
            for item in entry.provenance.evidence_refs
            if isinstance(item, RequirementEvidenceRef)
        )
        provenance = (
            *entry.provenance.source_trace_refs,
            *(
                item
                for item in entry.provenance.diagnostic_refs
                if isinstance(item, RequirementDiagnosticRef)
            ),
            *entry.provenance.finding_refs,
        )
        return self._feature(
            profile_id,
            feature_id,
            status=status,
            applicability=applicability,
            typed_value=value,
            source_refs=(entry.entry_id,),
            evidence_refs=evidence,
            provenance_refs=provenance,
            product_ref=None,
            availability_point=AvailabilityPoint.SOURCE_ASSESSMENT_AVAILABLE,
            rule_refs=entry.rule_refs,
            reasons=(),
            explanation=(
                "Requirement-quality metric retained as context and audit provenance only."
            ),
            context=context,
        )

    def _qb_feature(
        self,
        profile_id: PerformanceEfficiencyFeatureProfileId,
        entry: MetricEntry,
        gate: _GateProjection | None,
        target_key: ComparisonKey | None,
        binding: CriterionBindingResult,
        context: PerformanceEfficiencyFeatureConstructionContext,
    ) -> PerformanceEfficiencyFeature:
        source_refs = (entry.entry_id,)
        reasons: tuple = ()
        value = None
        if gate is None:
            status = binding.status
            applicability = binding.applicability
            source_refs = (*source_refs, binding.binding_id)
            reasons = binding.reasons
            explanation = "No justified criterion target exists; the controlling criterion state is preserved."
        else:
            relevant_refs = tuple(item.result_id for item in gate.relevant_results)
            source_refs = (*source_refs, *relevant_refs)
            if gate.decision in {
                QbTargetGateDecision.TARGET_CLEAR,
                QbTargetGateDecision.TARGET_CONFLICT,
            }:
                status = FullModelStatus.AVAILABLE
                applicability = Applicability.APPLICABLE
                value = QbTargetGateFeatureValue(
                    entry.entry_id,
                    entry.status,
                    entry.applicability,
                    entry.value,
                    gate.decision,
                    target_key,
                    relevant_refs,
                )
                if gate.decision is QbTargetGateDecision.TARGET_CONFLICT:
                    reasons = (FeatureReason.QB_TARGET_CONFLICT,)
                    explanation = "A confirmed QB conflict has the exact response-time target key; no bound was selected."
                else:
                    explanation = "Target-local QB comparisons are complete and compatible."
            elif gate.decision is QbTargetGateDecision.TARGET_UNRESOLVED:
                status = FullModelStatus.UNRESOLVED
                applicability = Applicability.APPLICABLE
                reasons = (FeatureReason.QB_TARGET_UNRESOLVED,)
                explanation = "Target-local QB evidence cannot establish a single consistent target."
            else:
                status = FullModelStatus.NOT_APPLICABLE
                applicability = Applicability.NOT_APPLICABLE
                reasons = (FeatureReason.QB_TARGET_NOT_APPLICABLE,)
                explanation = "No cross-requirement QB comparison applies to the selected target."
        evidence = tuple(
            item
            for item in entry.provenance.evidence_refs
            if not isinstance(item, RequirementEvidenceRef)
        )
        provenance = (
            *entry.provenance.cross_result_refs,
            *(
                item
                for item in entry.provenance.diagnostic_refs
                if not isinstance(item, RequirementDiagnosticRef)
            ),
        )
        return self._feature(
            profile_id,
            PerformanceEfficiencyFeatureId.SPECIFICATION_QB,
            status=status,
            applicability=applicability,
            typed_value=value,
            source_refs=source_refs,
            evidence_refs=evidence,
            provenance_refs=provenance,
            product_ref=None,
            availability_point=AvailabilityPoint.SOURCE_ASSESSMENT_AVAILABLE,
            rule_refs=entry.rule_refs,
            reasons=reasons,
            explanation=explanation,
            context=context,
        )

    def _observation_feature(
        self,
        profile_id: PerformanceEfficiencyFeatureProfileId,
        resolution: ObservationResolution,
        context: PerformanceEfficiencyFeatureConstructionContext,
    ) -> PerformanceEfficiencyFeature:
        observation = resolution.observation
        value = None
        source_refs: tuple = (resolution.slot_ref,)
        provenance_refs: tuple = ()
        if resolution.status is FullModelStatus.AVAILABLE:
            observation_ref = DynamicObservationRef(observation.observation_id)
            source_refs = (observation_ref,)
            value = ObservationFeatureValue(
                observation_ref,
                observation.metric_ref,
                observation.observed_value,
                observation.unit,
                observation.context_identity,
            )
            provenance_refs = (
                ExternalDynamicSourceRef(
                    observation.collection_ref,
                    observation.provenance.source_record_ref,
                ),
            )
        return self._feature(
            profile_id,
            PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME,
            status=resolution.status,
            applicability=resolution.applicability,
            typed_value=value,
            source_refs=source_refs,
            evidence_refs=(),
            provenance_refs=provenance_refs,
            product_ref=context.product_ref,
            availability_point=AvailabilityPoint.DYNAMIC_COLLECTION_AVAILABLE,
            rule_refs=(context.mapping_rule_ref,),
            reasons=resolution.reasons,
            explanation=(
                "Exact product observation retained with collection provenance."
                if value is not None
                else "Observation availability state preserved without a fallback value."
            ),
            context=context,
        )

    def _conformance_feature(
        self,
        profile_id: PerformanceEfficiencyFeatureProfileId,
        conformance: ConformanceAssessment,
        context: PerformanceEfficiencyFeatureConstructionContext,
    ) -> PerformanceEfficiencyFeature:
        value = (
            ConformanceFeatureValue(conformance.conformance_id, conformance.outcome)
            if conformance.status is FullModelStatus.AVAILABLE
            else None
        )
        return self._feature(
            profile_id,
            PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME,
            status=conformance.status,
            applicability=conformance.applicability,
            typed_value=value,
            source_refs=(conformance.conformance_id,),
            evidence_refs=conformance.evidence_refs,
            provenance_refs=(),
            product_ref=context.product_ref,
            availability_point=AvailabilityPoint.CONFORMANCE_ASSESSMENT_AVAILABLE,
            rule_refs=(conformance.evaluator_rule_ref,),
            reasons=conformance.reasons,
            explanation=(
                "Categorical criterion-observation conformance retained without numeric conversion."
                if value is not None
                else conformance.explanation
            ),
            context=context,
        )

    @staticmethod
    def _profile_state(
        features: tuple[PerformanceEfficiencyFeature, ...],
        gate: _GateProjection | None,
    ) -> tuple[FullModelStatus, Applicability]:
        criterion = features[0]
        observation = features[5]
        conformance = features[6]
        if criterion.status is FullModelStatus.NOT_APPLICABLE:
            return FullModelStatus.NOT_APPLICABLE, Applicability.NOT_APPLICABLE
        if criterion.status is not FullModelStatus.AVAILABLE:
            return criterion.status, criterion.applicability
        if gate is not None and gate.decision in {
            QbTargetGateDecision.TARGET_CONFLICT,
            QbTargetGateDecision.TARGET_UNRESOLVED,
        }:
            return FullModelStatus.UNRESOLVED, Applicability.APPLICABLE
        if observation.status is not FullModelStatus.AVAILABLE:
            return observation.status, observation.applicability
        if conformance.status is not FullModelStatus.AVAILABLE:
            return conformance.status, conformance.applicability
        return FullModelStatus.AVAILABLE, Applicability.APPLICABLE


def build_performance_efficiency_feature_profile(
    metric_profile: MetricProfile,
    qb_source: SpecificationAssessmentResult,
    criterion_binding: CriterionBindingResult,
    observation_resolution: ObservationResolution,
    conformance: ConformanceAssessment,
    context: PerformanceEfficiencyFeatureConstructionContext,
) -> PerformanceEfficiencyFeatureProfile:
    """Build the deterministic seven-slot ``X_PE`` profile."""

    return PerformanceEfficiencyFeatureProfileBuilder().build(
        metric_profile,
        qb_source,
        criterion_binding,
        observation_resolution,
        conformance,
        context,
    )


__all__ = [
    "PerformanceEfficiencyFeatureProfileBuilder",
    "build_performance_efficiency_feature_profile",
]

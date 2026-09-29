"""Pure lossless adapter from accepted property assessments to metrics."""

from __future__ import annotations

from fractions import Fraction
from typing import TypeVar

from ..cross_analysis.domain import (
    ContractVersionDescriptor,
    QbConsistencyState,
)
from ..cross_analysis.specification import SpecificationAssessmentResult
from ..domain import (
    CharacteristicAssessment,
    CharacteristicAssessmentState,
    CharacteristicId,
    RequirementAssessmentRecord,
    SpecificationCharacteristicAggregate,
)
from ..domain.trace import outcome_for_feature
from .domain import (
    ArtifactRef,
    ContractRef,
    MetricApplicability,
    MetricConstructionContext,
    MetricEntry,
    MetricEntryId,
    MetricId,
    MetricProfile,
    MetricProfileId,
    MetricProvenance,
    MetricScope,
    MetricSourceKind,
    MetricStatus,
    NumericRepresentation,
    QbConsistencyAssessmentRef,
    RequirementCharacteristicRef,
    RequirementDiagnosticRef,
    RequirementEvidenceRef,
    RequirementFindingRef,
    RequirementSubjectRef,
    RequirementTraceRef,
    RuleRef,
    RuleVersionAuthority,
    SourceStatusRef,
    SpecificationAggregateCounts,
    SpecificationAggregateRef,
    SpecificationSubjectRef,
)


_T = TypeVar("_T")


def _ordered_unique(values: tuple[_T, ...]) -> tuple[_T, ...]:
    retained: list[_T] = []
    for value in values:
        if value not in retained:
            retained.append(value)
    return tuple(retained)


def _stable_rule_ref(rule_id: str) -> RuleRef:
    return RuleRef(
        rule_id=rule_id,
        explicit_version=None,
        version_authority=RuleVersionAuthority.STABLE_RULE_ID_POLICY,
    )


def _explicit_rule_ref(descriptor: ContractVersionDescriptor) -> RuleRef:
    return RuleRef(
        rule_id=descriptor.contract_id,
        explicit_version=descriptor.version,
        version_authority=RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
    )


def _contract_ref(descriptor: ContractVersionDescriptor) -> ContractRef:
    return ContractRef(descriptor.contract_id, descriptor.version)


def _mapped_characteristic_state(
    state: CharacteristicAssessmentState,
) -> tuple[MetricStatus, MetricApplicability]:
    return {
        CharacteristicAssessmentState.COMPUTED: (
            MetricStatus.AVAILABLE,
            MetricApplicability.APPLICABLE,
        ),
        CharacteristicAssessmentState.UNKNOWN: (
            MetricStatus.UNKNOWN,
            MetricApplicability.APPLICABLE,
        ),
        CharacteristicAssessmentState.NOT_APPLICABLE: (
            MetricStatus.NOT_APPLICABLE,
            MetricApplicability.NOT_APPLICABLE,
        ),
    }[state]


def _numeric_representation(status: MetricStatus) -> NumericRepresentation:
    return (
        NumericRepresentation.EXACT_FRACTION
        if status is MetricStatus.AVAILABLE
        else NumericRepresentation.NONE
    )


_REQUIREMENT_SLOTS = (
    (
        "completeness",
        CharacteristicId.COMPLETENESS,
        MetricId.RQ_COMPLETENESS,
    ),
    (
        "verifiability",
        CharacteristicId.VERIFIABILITY,
        MetricId.RQ_VERIFIABILITY,
    ),
    (
        "unambiguity",
        CharacteristicId.UNAMBIGUITY,
        MetricId.RQ_UNAMBIGUITY,
    ),
)

_SPECIFICATION_SLOTS = (
    (
        "completeness",
        CharacteristicId.COMPLETENESS,
        MetricId.SPEC_MEAN_COMPLETENESS,
    ),
    (
        "verifiability",
        CharacteristicId.VERIFIABILITY,
        MetricId.SPEC_MEAN_VERIFIABILITY,
    ),
    (
        "unambiguity",
        CharacteristicId.UNAMBIGUITY,
        MetricId.SPEC_MEAN_UNAMBIGUITY,
    ),
)


class MetricProfileBuilder:
    """Build ``FULL-MODEL-V0.1-METRICS / 1`` without recalculation."""

    def build(
        self,
        source: SpecificationAssessmentResult,
        context: MetricConstructionContext,
    ) -> MetricProfile:
        if not isinstance(source, SpecificationAssessmentResult):
            raise TypeError("source must be a SpecificationAssessmentResult")
        if not isinstance(context, MetricConstructionContext):
            raise TypeError("context must be a MetricConstructionContext")

        profile_id = MetricProfileId(
            artifact_ref=context.artifact_ref,
            assessment_ref=context.assessment_ref,
            registry_ref=context.metric_registry_ref,
        )
        requirement_subjects = tuple(
            RequirementSubjectRef(
                artifact_ref=context.artifact_ref,
                requirement_id=record.extraction_result.requirement.id,
                source_line=record.extraction_result.requirement.source_line,
            )
            for record in source.records
        )

        entries: list[MetricEntry] = []
        for record, subject_ref in zip(
            source.records, requirement_subjects, strict=True
        ):
            for attribute, characteristic_id, metric_id in _REQUIREMENT_SLOTS:
                assessment = getattr(record.quality_profile, attribute)
                entries.append(
                    self._requirement_entry(
                        profile_id,
                        record,
                        subject_ref,
                        characteristic_id,
                        metric_id,
                        assessment,
                        context,
                    )
                )

        quality_profile = source.specification_assessment.quality_profile
        specification_subject = SpecificationSubjectRef(context.artifact_ref)
        for attribute, characteristic_id, metric_id in _SPECIFICATION_SLOTS:
            aggregate = getattr(quality_profile, attribute)
            entries.append(
                self._specification_aggregate_entry(
                    profile_id,
                    aggregate,
                    characteristic_id,
                    metric_id,
                    requirement_subjects,
                    specification_subject,
                    context,
                )
            )

        entries.append(
            self._qb_entry(
                profile_id,
                source,
                specification_subject,
                context,
            )
        )

        return MetricProfile(
            profile_id=profile_id,
            artifact_ref=context.artifact_ref,
            assessment_ref=context.assessment_ref,
            full_model_contract_ref=context.full_model_contract_ref,
            registry_ref=context.metric_registry_ref,
            adapter_rule_ref=context.adapter_rule_ref,
            source_snapshot_id=source.snapshot_id,
            entries=tuple(entries),
        )

    def _requirement_entry(
        self,
        profile_id: MetricProfileId,
        record: RequirementAssessmentRecord,
        subject_ref: RequirementSubjectRef,
        characteristic_id: CharacteristicId,
        metric_id: MetricId,
        assessment: CharacteristicAssessment,
        context: MetricConstructionContext,
    ) -> MetricEntry:
        trace_index, trace = next(
            (index, item)
            for index, item in enumerate(record.trace.characteristics)
            if item.characteristic_id is characteristic_id
        )
        if trace.governing_rule_id != (
            assessment.assessment_rule_id or trace.governing_rule_id
        ):
            raise ValueError("source assessment and trace rule identities disagree")

        source_ref = RequirementCharacteristicRef(
            assessment_ref=context.assessment_ref,
            requirement_subject_ref=subject_ref,
            characteristic_id=characteristic_id,
        )
        source_refs = (source_ref,)
        source_status = SourceStatusRef(assessment.state)
        status, applicability = _mapped_characteristic_state(assessment.state)
        evidence_ids: list[str] = []
        diagnostic_refs: list[RequirementDiagnosticRef] = []
        for input_trace in trace.inputs:
            outcome = outcome_for_feature(record.extraction_result, input_trace.feature_id)
            for observation_index in input_trace.observation_indexes:
                evidence_ids.extend(outcome.observations[observation_index].evidence_refs)
            diagnostic_refs.extend(
                RequirementDiagnosticRef(
                    requirement_subject_ref=subject_ref,
                    feature_id=input_trace.feature_id,
                    diagnostic_index=diagnostic_index,
                )
                for diagnostic_index in input_trace.diagnostic_indexes
            )
        for finding in assessment.findings:
            evidence_ids.extend(finding.evidence_refs)
        evidence_ids_tuple = _ordered_unique(tuple(evidence_ids))

        evidence_by_id = {
            evidence.evidence_id: evidence
            for evidence in record.extraction_result.evidence
        }
        if any(evidence_id not in evidence_by_id for evidence_id in evidence_ids_tuple):
            raise ValueError("metric provenance contains an unresolved Evidence ref")
        evidence_refs = tuple(
            RequirementEvidenceRef(subject_ref, evidence_id)
            for evidence_id in evidence_ids_tuple
        )
        finding_refs = tuple(
            RequirementFindingRef(subject_ref, finding.finding_id)
            for finding in assessment.findings
        )
        trace_ref = RequirementTraceRef(
            requirement_subject_ref=subject_ref,
            characteristic_id=characteristic_id,
            characteristic_index=trace_index,
            coverage_profile_id=record.trace.coverage_profile_id,
            governing_rule_id=trace.governing_rule_id,
            decision_code=trace.decision_code,
            feature_inputs=trace.inputs,
            finding_refs=trace.finding_refs,
        )
        rule_refs = _ordered_unique(
            (
                _stable_rule_ref(trace.governing_rule_id),
                *(
                    _stable_rule_ref(evidence_by_id[ref.evidence_id].rule_id)
                    for ref in evidence_refs
                ),
                *(
                    _stable_rule_ref(finding.rule_id)
                    for finding in assessment.findings
                ),
            )
        )
        provenance = MetricProvenance(
            source_kind=MetricSourceKind.REQUIREMENT_CHARACTERISTIC,
            source_status=source_status,
            source_explanation=assessment.explanation,
            source_assessment_refs=source_refs,
            source_trace_refs=(trace_ref,),
            evidence_refs=evidence_refs,
            diagnostic_refs=tuple(diagnostic_refs),
            finding_refs=finding_refs,
        )
        return self._entry(
            profile_id=profile_id,
            metric_id=metric_id,
            scope=MetricScope.REQUIREMENT,
            subject_ref=subject_ref,
            status=status,
            applicability=applicability,
            value=assessment.value,
            source_status=source_status,
            source_refs=source_refs,
            provenance=provenance,
            rule_refs=rule_refs,
            context=context,
        )

    def _specification_aggregate_entry(
        self,
        profile_id: MetricProfileId,
        aggregate: SpecificationCharacteristicAggregate,
        characteristic_id: CharacteristicId,
        metric_id: MetricId,
        requirement_subjects: tuple[RequirementSubjectRef, ...],
        subject_ref: SpecificationSubjectRef,
        context: MetricConstructionContext,
    ) -> MetricEntry:
        aggregate_ref = SpecificationAggregateRef(
            assessment_ref=context.assessment_ref,
            artifact_ref=context.artifact_ref,
            characteristic_id=characteristic_id,
            aggregation_rule_id=aggregate.aggregation_rule_id,
        )
        member_refs = tuple(
            RequirementCharacteristicRef(
                assessment_ref=context.assessment_ref,
                requirement_subject_ref=requirement_subject,
                characteristic_id=characteristic_id,
            )
            for requirement_subject in requirement_subjects
        )
        source_refs = (aggregate_ref, *member_refs)
        source_status = SourceStatusRef(aggregate.state)
        status, applicability = _mapped_characteristic_state(aggregate.state)
        provenance = MetricProvenance(
            source_kind=MetricSourceKind.SPECIFICATION_AGGREGATE,
            source_status=source_status,
            source_explanation=None,
            source_assessment_refs=source_refs,
            source_counts_or_observability=SpecificationAggregateCounts(
                computed_count=aggregate.computed_count,
                unknown_count=aggregate.unknown_count,
                not_applicable_count=aggregate.not_applicable_count,
                total_count=aggregate.total_count,
            ),
        )
        return self._entry(
            profile_id=profile_id,
            metric_id=metric_id,
            scope=MetricScope.SPECIFICATION,
            subject_ref=subject_ref,
            status=status,
            applicability=applicability,
            value=aggregate.value,
            source_status=source_status,
            source_refs=source_refs,
            provenance=provenance,
            rule_refs=(_stable_rule_ref(aggregate.aggregation_rule_id),),
            context=context,
        )

    def _qb_entry(
        self,
        profile_id: MetricProfileId,
        source: SpecificationAssessmentResult,
        subject_ref: SpecificationSubjectRef,
        context: MetricConstructionContext,
    ) -> MetricEntry:
        qb = source.specification_assessment.qb_consistency
        source_status = SourceStatusRef(qb.state)
        if qb.state is QbConsistencyState.COMPUTED:
            status = MetricStatus.AVAILABLE
            applicability = MetricApplicability.APPLICABLE
        elif qb.state is QbConsistencyState.NOT_APPLICABLE:
            status = MetricStatus.NOT_APPLICABLE
            applicability = MetricApplicability.NOT_APPLICABLE
        else:
            status = MetricStatus.UNKNOWN
            applicability = (
                MetricApplicability.APPLICABLE
                if qb.observability.applicable_comparison_count > 0
                else MetricApplicability.UNKNOWN
            )

        aggregation_contract = _contract_ref(qb.aggregation_rule)
        coverage_profile = _contract_ref(qb.coverage_profile)
        source_ref = QbConsistencyAssessmentRef(
            assessment_ref=context.assessment_ref,
            artifact_ref=context.artifact_ref,
            snapshot_id=qb.snapshot_id,
            aggregation_contract=aggregation_contract,
            coverage_profile=coverage_profile,
        )
        source_refs = (source_ref,)
        evidence_refs = _ordered_unique(
            tuple(
                evidence_ref
                for result in source.cross_results
                for evidence_ref in result.evidence_refs
            )
        )
        diagnostic_refs = _ordered_unique(
            (
                *(
                    diagnostic_ref
                    for result in source.cross_results
                    for diagnostic_ref in result.diagnostic_refs
                ),
                *qb.materiality_diagnostic_refs,
            )
        )
        provenance = MetricProvenance(
            source_kind=MetricSourceKind.QB_CONSISTENCY,
            source_status=source_status,
            source_explanation=None,
            source_assessment_refs=source_refs,
            evidence_refs=evidence_refs,
            diagnostic_refs=diagnostic_refs,
            cross_result_refs=qb.cross_result_ids,
            source_reasons=qb.reasons,
            source_counts_or_observability=qb.observability,
            source_formula_operands=qb.formula_operands,
            source_contract_refs=(
                coverage_profile,
                aggregation_contract,
                _contract_ref(qb.non_claim_contract),
            ),
            source_non_claim_refs=qb.non_claim_keys,
            rconf_participant_ids=qb.rconf_participant_ids,
            rconf_complete=qb.rconf_complete,
            materiality_diagnostic_refs=qb.materiality_diagnostic_refs,
            source_metric_label="M_cons[QB-v0.1]",
        )
        return self._entry(
            profile_id=profile_id,
            metric_id=MetricId.SPEC_QB_CONSISTENCY,
            scope=MetricScope.SPECIFICATION,
            subject_ref=subject_ref,
            status=status,
            applicability=applicability,
            value=qb.value,
            source_status=source_status,
            source_refs=source_refs,
            provenance=provenance,
            rule_refs=(_explicit_rule_ref(qb.aggregation_rule),),
            context=context,
        )

    @staticmethod
    def _entry(
        *,
        profile_id: MetricProfileId,
        metric_id: MetricId,
        scope: MetricScope,
        subject_ref: RequirementSubjectRef | SpecificationSubjectRef,
        status: MetricStatus,
        applicability: MetricApplicability,
        value: Fraction | None,
        source_status: SourceStatusRef,
        source_refs: tuple,
        provenance: MetricProvenance,
        rule_refs: tuple[RuleRef, ...],
        context: MetricConstructionContext,
    ) -> MetricEntry:
        return MetricEntry(
            entry_id=MetricEntryId(profile_id, scope, subject_ref, metric_id),
            metric_id=metric_id,
            scope=scope,
            subject_ref=subject_ref,
            status=status,
            applicability=applicability,
            value=value,
            numeric_representation=_numeric_representation(status),
            source_status=source_status,
            source_assessment_refs=source_refs,
            provenance=provenance,
            rule_refs=rule_refs,
            artifact_ref=context.artifact_ref,
            assessment_ref=context.assessment_ref,
            registry_ref=context.metric_registry_ref,
            adapter_rule_ref=context.adapter_rule_ref,
            full_model_contract_ref=context.full_model_contract_ref,
        )


def build_metric_profile(
    source: SpecificationAssessmentResult,
    context: MetricConstructionContext,
) -> MetricProfile:
    """Build the deterministic Full Model v0.1 metric profile."""

    return MetricProfileBuilder().build(source, context)


__all__ = ["MetricProfileBuilder", "build_metric_profile"]

"""Validated anti-corruption boundary for cross-requirement QB analysis.

Only :class:`CrossRequirementProjector` reads ``RequirementAssessmentRecord``
internals.  It copies the QB-relevant values into the immutable IMP-01 snapshot
manifests and builds a snapshot-scoped resolver over the original frozen
provenance values.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable
from typing import TypeAlias

from requirements_quality_assessment.domain import (
    DetectionDiagnostic,
    Evidence,
    FeatureId,
    QuantitativeComponentName,
    QuantitativeConstraintObservation,
    Requirement,
    RequirementAssessmentRecord,
)

from .domain import (
    AssessmentSnapshot,
    AssessmentSnapshotId,
    ContractVersionDescriptor,
    CrossAnalysisContractManifest,
    CrossDiagnosticRef,
    CrossEvidenceRef,
    CrossObservationRef,
    SnapshotCountManifest,
    SnapshotDiagnosticManifest,
    SnapshotEvidenceManifest,
    SnapshotObservationManifest,
    SnapshotRequirementManifest,
)


# The first six descriptors are architecture contract slots and versions frozen
# by IMP-01.  They are not production scientific Rule IDs.  In particular they
# do not allocate QB-MATERIALITY-001, QB-COMPARE-001, or QB-CONSISTENCY-001.
# The ordered extraction dependencies separately preserve the two production
# contracts allocated by IMP-02, including when neither contract fires.
IMP_02_EXTRACTION_CONTRACTS = (
    ContractVersionDescriptor("QUANT-LB-METRIC-001", "1"),
    ContractVersionDescriptor("QUANT-LB-CONTEXT-001", "1"),
)


QB_CONTRACT_MANIFEST = CrossAnalysisContractManifest(
    projection=ContractVersionDescriptor("QB-PROJECTION", "1"),
    normalization=ContractVersionDescriptor("QB-NORMALIZATION", "1"),
    comparison=ContractVersionDescriptor("QB-COMPARISON", "1"),
    materiality=ContractVersionDescriptor("QB-MATERIALITY", "1"),
    aggregation=ContractVersionDescriptor("QB-AGGREGATION", "1"),
    coverage_profile=ContractVersionDescriptor("QB-v0.1", "1"),
    extraction_contracts=IMP_02_EXTRACTION_CONTRACTS,
)


_SnapshotScope: TypeAlias = AssessmentSnapshotId | AssessmentSnapshot | None


def _component_refs(
    observation: QuantitativeConstraintObservation,
    component: QuantitativeComponentName,
) -> tuple[str, ...]:
    value = {
        QuantitativeComponentName.METRIC: observation.metric,
        QuantitativeComponentName.COMPARATOR: observation.comparator,
        QuantitativeComponentName.VALUE: observation.value,
        QuantitativeComponentName.UNIT: observation.unit,
        QuantitativeComponentName.CONTEXT: observation.context,
    }[component]
    return () if value is None else value.evidence_refs


def _qualified_refs(
    requirement_id: str,
    evidence_ids: tuple[str, ...],
) -> tuple[CrossEvidenceRef, ...]:
    return tuple(CrossEvidenceRef(requirement_id, item) for item in evidence_ids)


@dataclass(frozen=True, slots=True)
class CrossEvidenceResolver:
    """Resolve exact frozen provenance within one assessment snapshot.

    References deliberately do not contain a snapshot ID.  Callers composing
    snapshot-associated objects can pass ``snapshot_id=`` to every lookup; a
    mismatch fails before any reference is resolved.
    """

    snapshot_id: AssessmentSnapshotId
    _requirements: tuple[tuple[str, Requirement], ...]
    _evidence: tuple[tuple[CrossEvidenceRef, Evidence], ...]
    _observations: tuple[
        tuple[CrossObservationRef, QuantitativeConstraintObservation], ...
    ]
    _diagnostics: tuple[tuple[CrossDiagnosticRef, DetectionDiagnostic], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, AssessmentSnapshotId):
            raise TypeError("snapshot_id must be an AssessmentSnapshotId")
        requirement_ids = tuple(item[0] for item in self._requirements)
        if len(requirement_ids) != len(set(requirement_ids)):
            raise ValueError("resolver requirement IDs must be unique")
        for entries, name in (
            (self._evidence, "Evidence"),
            (self._observations, "observation"),
            (self._diagnostics, "diagnostic"),
        ):
            refs = tuple(item[0] for item in entries)
            if len(refs) != len(set(refs)):
                raise ValueError(f"resolver {name} refs must be unique")

    def assert_snapshot(self, snapshot: AssessmentSnapshotId | AssessmentSnapshot) -> None:
        """Fail when a caller attempts to compose provenance across snapshots."""
        candidate = snapshot.snapshot_id if isinstance(snapshot, AssessmentSnapshot) else snapshot
        if not isinstance(candidate, AssessmentSnapshotId):
            raise TypeError("snapshot must be an AssessmentSnapshot or AssessmentSnapshotId")
        if candidate != self.snapshot_id:
            raise ValueError("provenance cannot be resolved across assessment snapshots")

    def _check_scope(self, snapshot_id: _SnapshotScope) -> None:
        if snapshot_id is not None:
            self.assert_snapshot(snapshot_id)

    def resolve_requirement(
        self,
        requirement_id: str,
        *,
        snapshot_id: _SnapshotScope = None,
    ) -> Requirement:
        self._check_scope(snapshot_id)
        matches = tuple(value for key, value in self._requirements if key == requirement_id)
        if len(matches) != 1:
            raise ValueError("requirement ref must resolve exactly once in this snapshot")
        return matches[0]

    def resolve_observation(
        self,
        ref: CrossObservationRef,
        *,
        snapshot_id: _SnapshotScope = None,
    ) -> QuantitativeConstraintObservation:
        self._check_scope(snapshot_id)
        if not isinstance(ref, CrossObservationRef):
            raise TypeError("ref must be a CrossObservationRef")
        matches = tuple(value for key, value in self._observations if key == ref)
        if len(matches) != 1:
            raise ValueError("observation ref is outside the snapshot or out of range")
        return matches[0]

    def resolve_diagnostic(
        self,
        ref: CrossDiagnosticRef,
        *,
        snapshot_id: _SnapshotScope = None,
    ) -> DetectionDiagnostic:
        self._check_scope(snapshot_id)
        if not isinstance(ref, CrossDiagnosticRef):
            raise TypeError("ref must be a CrossDiagnosticRef")
        matches = tuple(value for key, value in self._diagnostics if key == ref)
        if len(matches) != 1:
            raise ValueError("diagnostic ref is outside the snapshot or out of range")
        return matches[0]

    def resolve_evidence(
        self,
        ref: CrossEvidenceRef,
        *,
        observation_ref: CrossObservationRef | None = None,
        component: QuantitativeComponentName | None = None,
        snapshot_id: _SnapshotScope = None,
    ) -> Evidence:
        """Resolve Evidence and optionally prove an observation/component edge."""
        self._check_scope(snapshot_id)
        if not isinstance(ref, CrossEvidenceRef):
            raise TypeError("ref must be a CrossEvidenceRef")
        if component is not None and not isinstance(component, QuantitativeComponentName):
            raise TypeError("component must be a QuantitativeComponentName or None")
        if component is not None and observation_ref is None:
            raise ValueError("component validation requires an observation_ref")
        matches = tuple(value for key, value in self._evidence if key == ref)
        if len(matches) != 1:
            raise ValueError("Evidence ref must resolve exactly once in this snapshot")
        evidence = matches[0]
        if evidence.requirement_id != ref.requirement_id:
            raise ValueError("Evidence does not belong to the qualified requirement")
        if evidence.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
            raise ValueError("QB Evidence must belong to the quantitative feature family")
        requirement = self.resolve_requirement(
            ref.requirement_id,
            snapshot_id=self.snapshot_id,
        )
        if (
            not 0 <= evidence.start_offset <= evidence.end_offset <= len(requirement.text)
            or requirement.text[evidence.start_offset:evidence.end_offset] != evidence.text
        ):
            raise ValueError("Evidence span must round-trip to exact requirement text")
        if observation_ref is not None:
            observation = self.resolve_observation(
                observation_ref,
                snapshot_id=self.snapshot_id,
            )
            if observation_ref.requirement_id != ref.requirement_id:
                raise ValueError("Evidence and observation must have the same owner")
            used_refs = (
                observation.evidence_refs
                if component is None
                else _component_refs(observation, component)
            )
            if ref.evidence_id not in used_refs:
                qualifier = "observation" if component is None else component.value
                raise ValueError(f"Evidence is not legitimately used by the {qualifier}")
        return evidence

    # Evidence is the resolver's primary value, so ``resolve`` is a concise,
    # unambiguous alias useful to reporting consumers.
    resolve = resolve_evidence


@dataclass(frozen=True, slots=True)
class CrossRequirementProjection:
    """One immutable snapshot paired with its exact scoped provenance resolver."""

    snapshot: AssessmentSnapshot
    resolver: CrossEvidenceResolver

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot, AssessmentSnapshot):
            raise TypeError("snapshot must be an AssessmentSnapshot")
        if not isinstance(self.resolver, CrossEvidenceResolver):
            raise TypeError("resolver must be a CrossEvidenceResolver")
        if self.snapshot.snapshot_id != self.resolver.snapshot_id:
            raise ValueError("snapshot and resolver must share one snapshot identity")

    @property
    def snapshot_id(self) -> AssessmentSnapshotId:
        return self.snapshot.snapshot_id

    @property
    def requirements(self) -> tuple[SnapshotRequirementManifest, ...]:
        return self.snapshot.requirements


class CrossRequirementProjector:
    """Project ordered local assessment records into the bounded QB contract."""

    def project(
        self,
        records: Iterable[RequirementAssessmentRecord],
        contracts: CrossAnalysisContractManifest = QB_CONTRACT_MANIFEST,
    ) -> CrossRequirementProjection:
        try:
            materialized = tuple(records)
        except TypeError as error:
            raise TypeError("records must be an ordered iterable") from error
        if any(not isinstance(item, RequirementAssessmentRecord) for item in materialized):
            raise TypeError("records must contain RequirementAssessmentRecord values")
        if not isinstance(contracts, CrossAnalysisContractManifest):
            raise TypeError("contracts must be a CrossAnalysisContractManifest")

        requirements = tuple(
            record.extraction_result.requirement for record in materialized
        )
        requirement_ids = tuple(item.id for item in requirements)
        if len(requirement_ids) != len(set(requirement_ids)):
            raise ValueError("projection requires unique requirement IDs")
        source_lines = tuple(item.source_line for item in requirements)
        if any(right <= left for left, right in zip(source_lines, source_lines[1:])):
            raise ValueError("records must be in strict source-line order")

        projected_requirements: list[SnapshotRequirementManifest] = []
        resolver_requirements: list[tuple[str, Requirement]] = []
        resolver_evidence: list[tuple[CrossEvidenceRef, Evidence]] = []
        resolver_observations: list[
            tuple[CrossObservationRef, QuantitativeConstraintObservation]
        ] = []
        resolver_diagnostics: list[tuple[CrossDiagnosticRef, DetectionDiagnostic]] = []

        for source_order, record in enumerate(materialized):
            result = record.extraction_result
            requirement = result.requirement
            outcome = result.features.quantitative_constraints
            if outcome.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
                raise ValueError("quantitative outcome has the wrong feature family")

            evidence_by_id: dict[str, Evidence] = {}
            for evidence in result.evidence:
                if evidence.evidence_id in evidence_by_id:
                    raise ValueError("duplicate Evidence ID in owning requirement")
                evidence_by_id[evidence.evidence_id] = evidence
                if evidence.requirement_id != requirement.id:
                    raise ValueError("Evidence belongs to a foreign requirement")
                if (
                    not 0 <= evidence.start_offset <= evidence.end_offset <= len(requirement.text)
                    or requirement.text[evidence.start_offset:evidence.end_offset]
                    != evidence.text
                ):
                    raise ValueError("Evidence span must round-trip to exact source text")

            observations: list[SnapshotObservationManifest] = []
            used_evidence_ids: set[str] = set()
            for observation_index, observation in enumerate(outcome.observations):
                if observation.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
                    raise ValueError("observation has the wrong feature family")
                observation_ref = CrossObservationRef(
                    requirement.id,
                    FeatureId.QUANTITATIVE_CONSTRAINT,
                    observation_index,
                )
                component_ids = {
                    component: _component_refs(observation, component)
                    for component in QuantitativeComponentName
                }
                component_union = {
                    evidence_id
                    for refs in component_ids.values()
                    for evidence_id in refs
                }
                if set(observation.evidence_refs) != component_union or len(
                    observation.evidence_refs
                ) != len(set(observation.evidence_refs)):
                    raise ValueError(
                        "observation top-level Evidence refs must be the component union"
                    )
                for component, refs in component_ids.items():
                    if len(refs) != len(set(refs)):
                        raise ValueError(
                            f"{component.value} component Evidence refs must be unique"
                        )
                    for evidence_id in refs:
                        evidence = evidence_by_id.get(evidence_id)
                        if evidence is None:
                            raise ValueError("component contains a dangling Evidence ref")
                        if evidence.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
                            raise ValueError(
                                "component Evidence must belong to the quantitative feature family"
                            )
                for evidence_id in observation.evidence_refs:
                    evidence = evidence_by_id.get(evidence_id)
                    if evidence is None:
                        raise ValueError("observation contains a dangling Evidence ref")
                    if evidence.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT:
                        raise ValueError(
                            "observation Evidence must belong to the quantitative feature family"
                        )
                used_evidence_ids.update(observation.evidence_refs)

                observations.append(
                    SnapshotObservationManifest(
                        ref=observation_ref,
                        metric_evidence_refs=_qualified_refs(
                            requirement.id,
                            component_ids[QuantitativeComponentName.METRIC],
                        ),
                        comparator=(
                            None
                            if observation.comparator is None
                            else observation.comparator.label
                        ),
                        inclusivity=(
                            None
                            if observation.comparator is None
                            else observation.comparator.inclusivity
                        ),
                        comparator_evidence_refs=_qualified_refs(
                            requirement.id,
                            component_ids[QuantitativeComponentName.COMPARATOR],
                        ),
                        value=(
                            None if observation.value is None else observation.value.decimal_value
                        ),
                        value_evidence_refs=_qualified_refs(
                            requirement.id,
                            component_ids[QuantitativeComponentName.VALUE],
                        ),
                        unit=None if observation.unit is None else observation.unit.label,
                        unit_evidence_refs=_qualified_refs(
                            requirement.id,
                            component_ids[QuantitativeComponentName.UNIT],
                        ),
                        context_evidence_refs=_qualified_refs(
                            requirement.id,
                            component_ids[QuantitativeComponentName.CONTEXT],
                        ),
                        unresolved_components=observation.unresolved_components,
                        evidence_refs=_qualified_refs(
                            requirement.id,
                            observation.evidence_refs,
                        ),
                    )
                )
                resolver_observations.append((observation_ref, observation))

            quantitative_evidence = tuple(
                evidence
                for evidence in result.evidence
                if evidence.feature_id is FeatureId.QUANTITATIVE_CONSTRAINT
            )
            projected_evidence = tuple(
                SnapshotEvidenceManifest(
                    ref=CrossEvidenceRef(requirement.id, evidence.evidence_id),
                    feature_id=evidence.feature_id,
                    text=evidence.text,
                    start_offset=evidence.start_offset,
                    end_offset=evidence.end_offset,
                    rule_id=evidence.rule_id,
                )
                for evidence in quantitative_evidence
            )
            projected_evidence_ids = {item.ref.evidence_id for item in projected_evidence}
            if not used_evidence_ids <= projected_evidence_ids:
                raise ValueError("every observation Evidence ref must exist in the QB projection")

            diagnostics: list[SnapshotDiagnosticManifest] = []
            for diagnostic_index, diagnostic in enumerate(outcome.diagnostics):
                diagnostic_ref = CrossDiagnosticRef(
                    requirement.id,
                    FeatureId.QUANTITATIVE_CONSTRAINT,
                    diagnostic_index,
                )
                span = diagnostic.candidate_span
                if span is not None and (
                    not 0 <= span.start_offset <= span.end_offset <= len(requirement.text)
                    or requirement.text[span.start_offset:span.end_offset] != span.text
                ):
                    raise ValueError("diagnostic span must round-trip to exact source text")
                diagnostics.append(
                    SnapshotDiagnosticManifest(
                        ref=diagnostic_ref,
                        code=diagnostic.code,
                        rule_id=diagnostic.rule_id,
                        candidate_text=None if span is None else span.text,
                        start_offset=None if span is None else span.start_offset,
                        end_offset=None if span is None else span.end_offset,
                    )
                )
                resolver_diagnostics.append((diagnostic_ref, diagnostic))

            projected_requirements.append(
                SnapshotRequirementManifest(
                    requirement_id=requirement.id,
                    source_order=source_order,
                    source_line=requirement.source_line,
                    text=requirement.text,
                    processing_status=outcome.processing_status,
                    observations=tuple(observations),
                    evidence=projected_evidence,
                    diagnostics=tuple(diagnostics),
                )
            )
            resolver_requirements.append((requirement.id, requirement))
            resolver_evidence.extend(
                (CrossEvidenceRef(requirement.id, evidence.evidence_id), evidence)
                for evidence in quantitative_evidence
            )

        requirement_manifests = tuple(projected_requirements)
        snapshot = AssessmentSnapshot(
            requirements=requirement_manifests,
            contracts=contracts,
            counts=SnapshotCountManifest.from_requirements(requirement_manifests),
        )
        resolver = CrossEvidenceResolver(
            snapshot_id=snapshot.snapshot_id,
            _requirements=tuple(resolver_requirements),
            _evidence=tuple(resolver_evidence),
            _observations=tuple(resolver_observations),
            _diagnostics=tuple(resolver_diagnostics),
        )

        # Exercise every projected edge through the public resolver.  This is
        # intentionally a construction invariant, not a scientific disposition.
        for requirement_manifest in snapshot.requirements:
            for observation_manifest in requirement_manifest.observations:
                resolver.resolve_observation(
                    observation_manifest.ref,
                    snapshot_id=snapshot.snapshot_id,
                )
                groups = (
                    (QuantitativeComponentName.METRIC, observation_manifest.metric_evidence_refs),
                    (
                        QuantitativeComponentName.COMPARATOR,
                        observation_manifest.comparator_evidence_refs,
                    ),
                    (QuantitativeComponentName.VALUE, observation_manifest.value_evidence_refs),
                    (QuantitativeComponentName.UNIT, observation_manifest.unit_evidence_refs),
                    (
                        QuantitativeComponentName.CONTEXT,
                        observation_manifest.context_evidence_refs,
                    ),
                )
                for component, refs in groups:
                    for evidence_ref in refs:
                        resolver.resolve_evidence(
                            evidence_ref,
                            observation_ref=observation_manifest.ref,
                            component=component,
                            snapshot_id=snapshot.snapshot_id,
                        )
                for evidence_ref in observation_manifest.evidence_refs:
                    resolver.resolve_evidence(
                        evidence_ref,
                        observation_ref=observation_manifest.ref,
                        snapshot_id=snapshot.snapshot_id,
                    )
            for evidence_manifest in requirement_manifest.evidence:
                resolver.resolve_evidence(
                    evidence_manifest.ref,
                    snapshot_id=snapshot.snapshot_id,
                )
            for diagnostic_manifest in requirement_manifest.diagnostics:
                resolver.resolve_diagnostic(
                    diagnostic_manifest.ref,
                    snapshot_id=snapshot.snapshot_id,
                )

        return CrossRequirementProjection(snapshot=snapshot, resolver=resolver)

"""Fail-closed CRA-D067 materiality classification for QB-v0.1.

This module interprets preserved quantitative diagnostics for QB only.  It
does not change detector outcomes, Evidence, observations, or local quality
assessment values.
"""

from __future__ import annotations

from dataclasses import dataclass

from requirements_quality_assessment.domain import (
    FeatureId,
    QuantitativeComponentName,
)

from .domain import (
    AssessmentSnapshotId,
    ContractVersionDescriptor,
    SnapshotDiagnosticManifest,
    SnapshotEvidenceManifest,
    SnapshotObservationManifest,
    SnapshotRequirementManifest,
    QbMaterialityAllowlistDescriptor,
    QbMaterialityAuditRecord,
    QbMaterialityDisposition,
    QbMaterialityGateOutcomes,
    QbMaterialityResult,
    SnapshotCountManifest,
)
from .projection import CrossRequirementProjection


QB_MATERIALITY_RULE = ContractVersionDescriptor("QB-MATERIALITY-001", "1")

_SNAPSHOT_MATERIALITY_CONTRACT = ContractVersionDescriptor("QB-MATERIALITY", "1")
_EXACT_C0_CONTEXT = "при 500 одночасних користувачах"
_EXACT_CANDIDATE = "500"

# QUANT-CONTEXT-001 predates the explicit extraction dependency manifest, so
# its approved version is fixed here with the exception itself.  The lower C0
# contract was allocated with that manifest and must be present there exactly.
QB_NON_MATERIAL_CONTEXT_ALLOWLIST = (
    QbMaterialityAllowlistDescriptor(
        contract=ContractVersionDescriptor("QUANT-CONTEXT-001", "1"),
        context_text=_EXACT_C0_CONTEXT,
        candidate_text=_EXACT_CANDIDATE,
        non_independent_role_guaranteed=True,
        snapshot_manifest_required=False,
    ),
    QbMaterialityAllowlistDescriptor(
        contract=ContractVersionDescriptor("QUANT-LB-CONTEXT-001", "1"),
        context_text=_EXACT_C0_CONTEXT,
        candidate_text=_EXACT_CANDIDATE,
        non_independent_role_guaranteed=True,
        snapshot_manifest_required=True,
    ),
)

_UNRESOLVED_NUMERIC_CODE = "QUANT_UNRESOLVED_NUMERIC_CANDIDATE"
_UNRESOLVED_NUMERIC_RULE = "QUANT-001"


@dataclass(frozen=True, slots=True)
class _Eligibility:
    snapshot_id: AssessmentSnapshotId
    requirement: SnapshotRequirementManifest
    diagnostic: SnapshotDiagnosticManifest
    context: SnapshotEvidenceManifest | None
    observation: SnapshotObservationManifest | None
    allowlist: QbMaterialityAllowlistDescriptor | None
    exact_code: bool
    exact_rule: bool
    exact_text: bool
    inside_context: bool
    same_observation: bool
    contract_guarantee: bool
    provenance_integrity: bool

    @property
    def locally_eligible(self) -> bool:
        return all(
            (
                self.exact_code,
                self.exact_rule,
                self.exact_text,
                self.inside_context,
                self.same_observation,
                self.contract_guarantee,
                self.provenance_integrity,
            )
        )


def _context_matches(
    requirement: SnapshotRequirementManifest,
    diagnostic: SnapshotDiagnosticManifest,
) -> tuple[SnapshotEvidenceManifest, ...]:
    if (
        diagnostic.candidate_text is None
        or diagnostic.start_offset is None
        or diagnostic.end_offset is None
    ):
        return ()
    return tuple(
        evidence
        for evidence in requirement.evidence
        if evidence.text == _EXACT_C0_CONTEXT
        and evidence.start_offset <= diagnostic.start_offset
        and diagnostic.end_offset <= evidence.end_offset
        and requirement.text[diagnostic.start_offset:diagnostic.end_offset]
        == diagnostic.candidate_text
    )


def _observation_matches(
    requirement: SnapshotRequirementManifest,
    context: SnapshotEvidenceManifest | None,
) -> tuple[SnapshotObservationManifest, ...]:
    if context is None:
        return ()
    return tuple(
        observation
        for observation in requirement.observations
        if context.ref in observation.context_evidence_refs
        and observation.ref.requirement_id == requirement.requirement_id
    )


def _allowlist_match(
    context: SnapshotEvidenceManifest | None,
) -> QbMaterialityAllowlistDescriptor | None:
    if context is None:
        return None
    matches = tuple(
        item
        for item in QB_NON_MATERIAL_CONTEXT_ALLOWLIST
        if item.contract.contract_id == context.rule_id
        and item.context_text == context.text
        and item.candidate_text == _EXACT_CANDIDATE
    )
    return matches[0] if len(matches) == 1 else None


def _contract_guarantee_passes(
    projection: CrossRequirementProjection,
    descriptor: QbMaterialityAllowlistDescriptor | None,
) -> bool:
    if descriptor is None or not descriptor.non_independent_role_guaranteed:
        return False
    same_id = tuple(
        item
        for item in projection.snapshot.contracts.extraction_contracts
        if item.contract_id == descriptor.contract.contract_id
    )
    if descriptor.snapshot_manifest_required:
        return same_id == (descriptor.contract,)
    # The legacy upper contract has no IMP-02 manifest entry.  If a caller
    # nevertheless supplies one, it must be the one approved version.
    return not same_id or same_id == (descriptor.contract,)


def _snapshot_integrity(projection: CrossRequirementProjection) -> bool:
    try:
        snapshot = projection.snapshot
        if projection.resolver.snapshot_id != snapshot.snapshot_id:
            return False
        projection.resolver.assert_snapshot(snapshot)
        if snapshot.contracts.materiality != _SNAPSHOT_MATERIALITY_CONTRACT:
            return False
        if snapshot.counts != SnapshotCountManifest.from_requirements(
            snapshot.requirements
        ):
            return False
        if AssessmentSnapshotId.from_bytes(snapshot.canonical_bytes()) != snapshot.snapshot_id:
            return False
        return True
    except (AttributeError, TypeError, ValueError):
        return False


def _diagnostic_integrity(
    projection: CrossRequirementProjection,
    requirement: SnapshotRequirementManifest,
    diagnostic: SnapshotDiagnosticManifest,
) -> bool:
    try:
        source_requirement = projection.resolver.resolve_requirement(
            requirement.requirement_id,
            snapshot_id=projection.snapshot_id,
        )
        if (
            source_requirement.id != requirement.requirement_id
            or source_requirement.source_line != requirement.source_line
            or source_requirement.text != requirement.text
        ):
            return False
        source = projection.resolver.resolve_diagnostic(
            diagnostic.ref,
            snapshot_id=projection.snapshot_id,
        )
        source_span = source.candidate_span
        source_values = (
            source.code,
            source.rule_id,
            None if source_span is None else source_span.text,
            None if source_span is None else source_span.start_offset,
            None if source_span is None else source_span.end_offset,
        )
        manifest_values = (
            diagnostic.code,
            diagnostic.rule_id,
            diagnostic.candidate_text,
            diagnostic.start_offset,
            diagnostic.end_offset,
        )
        if source_values != manifest_values:
            return False
        if diagnostic.candidate_text is not None and (
            diagnostic.start_offset is None
            or diagnostic.end_offset is None
            or not 0 <= diagnostic.start_offset <= diagnostic.end_offset <= len(requirement.text)
            or requirement.text[diagnostic.start_offset:diagnostic.end_offset]
            != diagnostic.candidate_text
        ):
            return False
        return True
    except (AttributeError, TypeError, ValueError):
        return False


def _context_integrity(
    projection: CrossRequirementProjection,
    requirement: SnapshotRequirementManifest,
    context: SnapshotEvidenceManifest | None,
    observation: SnapshotObservationManifest | None,
) -> bool:
    if context is None or observation is None:
        return False
    try:
        source = projection.resolver.resolve_evidence(
            context.ref,
            observation_ref=observation.ref,
            component=QuantitativeComponentName.CONTEXT,
            snapshot_id=projection.snapshot_id,
        )
        source_values = (
            source.requirement_id,
            source.feature_id,
            source.text,
            source.start_offset,
            source.end_offset,
            source.rule_id,
            source.evidence_id,
        )
        manifest_values = (
            context.ref.requirement_id,
            context.feature_id,
            context.text,
            context.start_offset,
            context.end_offset,
            context.rule_id,
            context.ref.evidence_id,
        )
        if source_values != manifest_values:
            return False
        if (
            context.ref.requirement_id != requirement.requirement_id
            or context.feature_id is not FeatureId.QUANTITATIVE_CONSTRAINT
            or not 0 <= context.start_offset <= context.end_offset <= len(requirement.text)
            or requirement.text[context.start_offset:context.end_offset] != context.text
        ):
            return False
        projection.resolver.resolve_observation(
            observation.ref,
            snapshot_id=projection.snapshot_id,
        )
        return True
    except (AttributeError, TypeError, ValueError):
        return False


def _first_pass(
    projection: CrossRequirementProjection,
    requirement: SnapshotRequirementManifest,
    diagnostic: SnapshotDiagnosticManifest,
    snapshot_integrity: bool,
) -> _Eligibility:
    contexts = _context_matches(requirement, diagnostic)
    context = contexts[0] if len(contexts) == 1 else None
    observations = _observation_matches(requirement, context)
    observation = observations[0] if len(observations) == 1 else None
    allowlist = _allowlist_match(context)
    diagnostic_integrity = _diagnostic_integrity(
        projection,
        requirement,
        diagnostic,
    )
    context_integrity = _context_integrity(
        projection,
        requirement,
        context,
        observation,
    )
    return _Eligibility(
        snapshot_id=projection.snapshot_id,
        requirement=requirement,
        diagnostic=diagnostic,
        context=context,
        observation=observation,
        allowlist=allowlist,
        exact_code=diagnostic.code == _UNRESOLVED_NUMERIC_CODE,
        exact_rule=diagnostic.rule_id == _UNRESOLVED_NUMERIC_RULE,
        exact_text=diagnostic.candidate_text == _EXACT_CANDIDATE,
        inside_context=len(contexts) == 1,
        same_observation=len(observations) == 1,
        contract_guarantee=_contract_guarantee_passes(projection, allowlist),
        provenance_integrity=(
            snapshot_integrity and diagnostic_integrity and context_integrity
        ),
    )


def _no_competition(
    projection: CrossRequirementProjection,
    candidate: _Eligibility,
    eligibilities: tuple[_Eligibility, ...],
) -> bool:
    """Second pass over the complete snapshot, excluding the candidate itself."""
    if any(
        observation.unresolved_components
        for requirement in projection.requirements
        for observation in requirement.observations
    ):
        return False
    if any(item is not candidate and not item.locally_eligible for item in eligibilities):
        return False
    return not any(
        len(item.requirement.diagnostics) != 1
        or len(item.requirement.observations) != 1
        for item in eligibilities
    )


class QbMaterialityClassifier:
    """Classify all preserved quantitative diagnostics in two passes."""

    def classify(self, projection: CrossRequirementProjection) -> QbMaterialityResult:
        if not isinstance(projection, CrossRequirementProjection):
            raise TypeError("projection must be a CrossRequirementProjection")

        snapshot_integrity = _snapshot_integrity(projection)
        first_pass = tuple(
            _first_pass(projection, requirement, diagnostic, snapshot_integrity)
            for requirement in projection.requirements
            for diagnostic in requirement.diagnostics
        )

        records = tuple(
            self._audit(
                item,
                no_competition=_no_competition(projection, item, first_pass),
            )
            for item in first_pass
        )
        material_count = sum(
            item.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED
            for item in records
        )
        non_material_count = sum(
            item.disposition is QbMaterialityDisposition.QB_NON_MATERIAL
            for item in records
        )
        return QbMaterialityResult(
            snapshot_id=projection.snapshot_id,
            materiality_rule=QB_MATERIALITY_RULE,
            audit_records=records,
            global_unresolved_diagnostic_count=len(records),
            qb_material_count=material_count,
            qb_non_material_count=non_material_count,
        )

    @staticmethod
    def _audit(
        item: _Eligibility,
        *,
        no_competition: bool,
    ) -> QbMaterialityAuditRecord:
        gates = QbMaterialityGateOutcomes(
            exact_diagnostic_code=item.exact_code,
            exact_diagnostic_rule=item.exact_rule,
            exact_candidate_text=item.exact_text,
            candidate_inside_context=item.inside_context,
            same_observation=item.same_observation,
            allowlisted_contract_guarantee=item.contract_guarantee,
            no_qb_competition=no_competition,
            provenance_integrity=item.provenance_integrity,
        )
        return QbMaterialityAuditRecord(
            snapshot_id=item.snapshot_id,
            requirement_id=item.requirement.requirement_id,
            requirement_source_order=item.requirement.source_order,
            diagnostic_ref=item.diagnostic.ref,
            diagnostic_code=item.diagnostic.code,
            diagnostic_rule_id=item.diagnostic.rule_id,
            candidate_text=item.diagnostic.candidate_text,
            diagnostic_start_offset=item.diagnostic.start_offset,
            diagnostic_end_offset=item.diagnostic.end_offset,
            matched_context_evidence_ref=(
                None if item.context is None else item.context.ref
            ),
            matched_allowlist_contract=(
                None if item.allowlist is None else item.allowlist.contract
            ),
            materiality_rule=QB_MATERIALITY_RULE,
            gate_outcomes=gates,
            disposition=(
                QbMaterialityDisposition.QB_NON_MATERIAL
                if gates.all_passed
                else QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED
            ),
        )

"""Observed QB-v0.1 conflict-participant set construction.

This module performs set union and validation only.  Pair applicability,
normalization, comparison, and conflict confirmation belong to IMP-06.
Numeric Consistency aggregation belongs to IMP-08.
"""

from __future__ import annotations

from dataclasses import dataclass

from .domain import (
    AssessmentSnapshot,
    AssessmentSnapshotId,
    CrossRequirementResult,
    CrossResultId,
    CrossResultState,
    QbMaterialityDisposition,
    QbMaterialityResult,
    RequirementOrderKey,
)


@dataclass(frozen=True, slots=True)
class QbConflictSet:
    """Source-ordered observed ``R_conf[QB-v0.1]`` membership."""

    snapshot_id: AssessmentSnapshotId
    participant_ids: tuple[str, ...]
    rconf_complete: bool

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, AssessmentSnapshotId):
            raise TypeError("snapshot_id must be an AssessmentSnapshotId")
        if not isinstance(self.participant_ids, tuple) or any(
            not isinstance(item, str) for item in self.participant_ids
        ):
            raise TypeError("participant_ids must be a tuple of strings")
        if any(not item or item != item.strip() for item in self.participant_ids):
            raise ValueError("participant IDs must be non-empty and trimmed")
        if len(set(self.participant_ids)) != len(self.participant_ids):
            raise ValueError("participant_ids must not contain duplicates")
        if type(self.rconf_complete) is not bool:
            raise TypeError("rconf_complete must be a boolean")

    @property
    def participants(self) -> tuple[str, ...]:
        """Return the observed participant IDs using the concise domain name."""

        return self.participant_ids


def _snapshot_requirements(
    snapshot: AssessmentSnapshot,
) -> tuple[dict[str, RequirementOrderKey], set[object], set[object], set[object]]:
    if not isinstance(snapshot, AssessmentSnapshot):
        raise TypeError("snapshot must be an AssessmentSnapshot")
    if AssessmentSnapshotId.from_bytes(snapshot.canonical_bytes()) != snapshot.snapshot_id:
        raise ValueError("snapshot identity does not match its canonical content")

    requirements = {
        item.requirement_id: item.order_key for item in snapshot.requirements
    }
    observations = {
        observation.ref
        for requirement in snapshot.requirements
        for observation in requirement.observations
    }
    evidence = {
        item.ref
        for requirement in snapshot.requirements
        for item in requirement.evidence
    }
    diagnostics = {
        item.ref
        for requirement in snapshot.requirements
        for item in requirement.diagnostics
    }
    return requirements, observations, evidence, diagnostics


def _validate_materiality(
    snapshot: AssessmentSnapshot,
    materiality: QbMaterialityResult,
    requirements: dict[str, RequirementOrderKey],
    diagnostics: set[object],
) -> bool:
    if not isinstance(materiality, QbMaterialityResult):
        raise TypeError("materiality must be a QbMaterialityResult")
    if materiality.snapshot_id != snapshot.snapshot_id:
        raise ValueError("materiality result and snapshot cannot cross snapshots")

    material_count = 0
    non_material_count = 0
    seen_diagnostics: set[object] = set()
    for audit in materiality.audit_records:
        if audit.snapshot_id != materiality.snapshot_id:
            raise ValueError("materiality audit and result cannot cross snapshots")
        if audit.materiality_rule != materiality.materiality_rule:
            raise ValueError("materiality audit and result must use the same rule")
        expected_participant = requirements.get(audit.requirement_id)
        if expected_participant is None:
            raise ValueError("materiality audit has an unknown requirement owner")
        if audit.requirement_source_order != expected_participant.source_order:
            raise ValueError("materiality audit has foreign requirement ownership")
        if audit.diagnostic_ref not in diagnostics:
            raise ValueError("materiality audit has a foreign diagnostic reference")
        if audit.diagnostic_ref in seen_diagnostics:
            raise ValueError("materiality audits must not repeat a diagnostic reference")
        seen_diagnostics.add(audit.diagnostic_ref)
        if audit.disposition is QbMaterialityDisposition.QB_MATERIAL_UNRESOLVED:
            material_count += 1
        elif audit.disposition is QbMaterialityDisposition.QB_NON_MATERIAL:
            non_material_count += 1
        else:  # Defensive against post-construction mutation of frozen values.
            raise ValueError("materiality audit has an invalid disposition")

    if seen_diagnostics != diagnostics:
        raise ValueError("materiality audits must cover every snapshot diagnostic exactly once")
    if materiality.global_unresolved_diagnostic_count != len(materiality.audit_records):
        raise ValueError("materiality global count does not match its audit records")
    if materiality.qb_material_count != material_count:
        raise ValueError("materiality QB-material count does not match its audits")
    if materiality.qb_non_material_count != non_material_count:
        raise ValueError("materiality non-material count does not match its audits")
    if materiality.global_unresolved_diagnostic_count != material_count + non_material_count:
        raise ValueError("materiality completeness counts are inconsistent")

    return material_count == 0


def _validate_result(
    snapshot: AssessmentSnapshot,
    result: CrossRequirementResult,
    requirements: dict[str, RequirementOrderKey],
    observations: set[object],
    evidence: set[object],
    diagnostics: set[object],
) -> None:
    if not isinstance(result, CrossRequirementResult):
        raise TypeError("results must contain CrossRequirementResult values")
    if result.snapshot_id != snapshot.snapshot_id:
        raise ValueError("cross result and snapshot cannot cross snapshots")
    if result.coverage_profile != snapshot.contracts.coverage_profile:
        raise ValueError("cross result has foreign coverage-profile ownership")
    if not isinstance(result.participants, tuple) or len(result.participants) != 2:
        raise TypeError("cross-result participants must contain two order keys")
    if any(not isinstance(item, RequirementOrderKey) for item in result.participants):
        raise TypeError("cross-result participants must be RequirementOrderKey values")

    left, right = result.participants
    if left.requirement_id == right.requirement_id:
        raise ValueError("cross result cannot contain a self-pair")
    for participant in result.participants:
        expected = requirements.get(participant.requirement_id)
        if expected is None:
            raise ValueError("cross result contains an unknown participant")
        if participant != expected:
            raise ValueError("cross result has foreign participant ownership")
    if left.source_order >= right.source_order:
        raise ValueError("cross-result participants must use canonical source order")

    if any(item not in observations for item in result.observation_refs):
        raise ValueError("cross result has a foreign observation reference")
    if any(item not in evidence for item in result.evidence_refs):
        raise ValueError("cross result has a foreign Evidence reference")
    if any(item not in diagnostics for item in result.diagnostic_refs):
        raise ValueError("cross result has a foreign diagnostic reference")
    if CrossResultId.from_bytes(result.canonical_identity_bytes()) != result.result_id:
        raise ValueError("cross result identity does not match its canonical content")


class QbConflictSetBuilder:
    """Build unique confirmed-conflict participants without reassessing pairs."""

    def build(
        self,
        snapshot: AssessmentSnapshot,
        results: tuple[CrossRequirementResult, ...],
        materiality: QbMaterialityResult,
    ) -> QbConflictSet:
        requirements, observations, evidence, diagnostics = _snapshot_requirements(
            snapshot
        )
        if not isinstance(results, tuple):
            raise TypeError("results must be a tuple of CrossRequirementResult values")
        materiality_complete = _validate_materiality(
            snapshot, materiality, requirements, diagnostics
        )

        seen_result_ids: set[CrossResultId] = set()
        confirmed_participants: set[str] = set()
        unresolved_pair_exists = False
        for result in results:
            _validate_result(
                snapshot,
                result,
                requirements,
                observations,
                evidence,
                diagnostics,
            )
            if result.result_id in seen_result_ids:
                raise ValueError("cross-result IDs must not contain duplicates")
            seen_result_ids.add(result.result_id)

            if result.state is CrossResultState.CONFIRMED_CONFLICT:
                confirmed_participants.update(
                    participant.requirement_id for participant in result.participants
                )
            elif result.state is CrossResultState.ASSESSMENT_UNRESOLVED:
                unresolved_pair_exists = True

        ordered_participants = tuple(
            requirement.requirement_id
            for requirement in snapshot.requirements
            if requirement.requirement_id in confirmed_participants
        )
        return QbConflictSet(
            snapshot_id=snapshot.snapshot_id,
            participant_ids=ordered_participants,
            rconf_complete=materiality_complete and not unresolved_pair_exists,
        )


__all__ = ["QbConflictSet", "QbConflictSetBuilder"]

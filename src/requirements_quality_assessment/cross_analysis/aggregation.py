"""Observed QB-v0.1 conflict-set construction and bounded aggregation.

Pair applicability, normalization, comparison, and conflict confirmation
belong to IMP-06.  This module trusts those validated states, reuses the
IMP-07 conflict-set builder, and applies only the approved IMP-08 aggregate
gates and exact cardinality formula.
"""

from __future__ import annotations

from dataclasses import dataclass

from .domain import (
    AssessmentSnapshot,
    AssessmentSnapshotId,
    BoundedNonClaimKey,
    ContractVersionDescriptor,
    CrossObservationRef,
    CrossRequirementResult,
    CrossResultId,
    CrossResultState,
    QbConsistencyAssessment,
    QbConsistencyFormulaOperands,
    QbConsistencyObservability,
    QbConsistencyReason,
    QbConsistencyState,
    QbMaterialityDisposition,
    QbMaterialityResult,
    RequirementOrderKey,
)
from .comparison import QB_COMPARISON_RULE, QB_COVERAGE_PROFILE
from .materiality import QB_MATERIALITY_RULE


QB_CONSISTENCY_RULE = ContractVersionDescriptor("QB-CONSISTENCY-001", "1")
QB_NON_CLAIMS = ContractVersionDescriptor("QB-NON-CLAIMS-001", "1")


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


def _expected_observation_pairs(
    snapshot: AssessmentSnapshot,
) -> set[tuple[CrossObservationRef, CrossObservationRef]]:
    """Return the exhaustive cross-requirement observation-pair universe."""

    return {
        (left_observation.ref, right_observation.ref)
        for left_index, left_requirement in enumerate(snapshot.requirements)
        for right_requirement in snapshot.requirements[left_index + 1 :]
        for left_observation in left_requirement.observations
        for right_observation in right_requirement.observations
    }


class QbConsistencyAggregator:
    """Aggregate validated exhaustive pair results into ``M_cons[QB-v0.1]``."""

    def aggregate(
        self,
        snapshot: AssessmentSnapshot,
        results: tuple[CrossRequirementResult, ...],
        materiality: QbMaterialityResult,
        conflict_set: QbConflictSet | None = None,
    ) -> QbConsistencyAssessment:
        if not isinstance(snapshot, AssessmentSnapshot):
            raise TypeError("snapshot must be an AssessmentSnapshot")
        if not isinstance(results, tuple):
            raise TypeError("results must be a tuple of CrossRequirementResult values")
        if not isinstance(materiality, QbMaterialityResult):
            raise TypeError("materiality must be a QbMaterialityResult")
        if snapshot.contracts.coverage_profile != QB_COVERAGE_PROFILE:
            raise ValueError("snapshot must use QB-v0.1 / 1 coverage")
        if materiality.materiality_rule != QB_MATERIALITY_RULE:
            raise ValueError("materiality result must use QB-MATERIALITY-001 / 1")
        if any(result.comparison_contract != QB_COMPARISON_RULE for result in results):
            raise ValueError("cross results must use QB-COMPARE-001 / 1")

        built_conflict_set = QbConflictSetBuilder().build(
            snapshot,
            results,
            materiality,
        )
        if conflict_set is None:
            conflict_set = built_conflict_set
        elif not isinstance(conflict_set, QbConflictSet):
            raise TypeError("conflict_set must be a QbConflictSet")
        elif conflict_set.snapshot_id != snapshot.snapshot_id:
            raise ValueError("conflict set and snapshot cannot cross snapshots")
        elif conflict_set != built_conflict_set:
            raise ValueError(
                "conflict set does not match the accepted IMP-07 builder output"
            )

        expected_pairs = _expected_observation_pairs(snapshot)
        actual_pairs = tuple(result.observation_refs for result in results)
        if len(set(actual_pairs)) != len(actual_pairs):
            raise ValueError("observation-pair results must not contain duplicates")
        if set(actual_pairs) != expected_pairs:
            raise ValueError(
                "results must cover the exhaustive observation-pair universe exactly once"
            )

        state_counts = {
            state: sum(result.state is state for result in results)
            for state in CrossResultState
        }
        confirmed_count = state_counts[CrossResultState.CONFIRMED_CONFLICT]
        compatible_count = state_counts[CrossResultState.COMPATIBLE_WITHIN_RULE]
        unresolved_count = state_counts[CrossResultState.ASSESSMENT_UNRESOLVED]
        outside_count = state_counts[CrossResultState.OUTSIDE_V0_1_APPLICABILITY]
        applicable_count = confirmed_count + compatible_count

        applicable_requirement_ids = {
            participant.requirement_id
            for result in results
            if result.state
            in {
                CrossResultState.CONFIRMED_CONFLICT,
                CrossResultState.COMPATIBLE_WITHIN_RULE,
            }
            for participant in result.participants
        }
        requirement_count = len(snapshot.requirements)

        # The first decision gate establishes that an empty/single-requirement
        # R_conf is complete even if global extraction diagnostics are present:
        # no cross-requirement conflict participant can exist in that universe.
        aggregate_conflict_set = (
            QbConflictSet(snapshot.snapshot_id, (), True)
            if requirement_count < 2
            else conflict_set
        )

        observability = QbConsistencyObservability(
            total_requirement_count=requirement_count,
            requirements_with_observations_count=sum(
                bool(requirement.observations)
                for requirement in snapshot.requirements
            ),
            requirements_in_applicable_comparisons_count=len(
                applicable_requirement_ids
            ),
            total_requirement_pair_count=requirement_count
            * (requirement_count - 1)
            // 2,
            total_observation_pair_count=len(results),
            confirmed_conflict_count=confirmed_count,
            compatible_count=compatible_count,
            unresolved_count=unresolved_count,
            outside_applicability_count=outside_count,
            applicable_comparison_count=applicable_count,
            global_unresolved_extraction_count=(
                materiality.global_unresolved_diagnostic_count
            ),
            qb_material_unresolved_count=materiality.qb_material_count,
            qb_non_material_diagnostic_count=materiality.qb_non_material_count,
            observed_rconf_count=len(aggregate_conflict_set.participant_ids),
            rconf_complete=aggregate_conflict_set.rconf_complete,
        )

        if requirement_count < 2:
            state = QbConsistencyState.NOT_APPLICABLE
            reasons = (QbConsistencyReason.FEWER_THAN_TWO_REQUIREMENTS,)
        elif materiality.qb_material_count > 0 or unresolved_count > 0:
            state = QbConsistencyState.UNKNOWN
            reasons = tuple(
                reason
                for present, reason in (
                    (
                        materiality.qb_material_count > 0,
                        QbConsistencyReason.QB_MATERIAL_UNRESOLVED_EXTRACTION,
                    ),
                    (
                        unresolved_count > 0,
                        QbConsistencyReason.ASSESSMENT_UNRESOLVED_PAIR,
                    ),
                )
                if present
            )
        elif applicable_count == 0:
            state = QbConsistencyState.NOT_APPLICABLE
            reasons = (QbConsistencyReason.NO_APPLICABLE_COMPARISONS,)
        else:
            state = QbConsistencyState.COMPUTED
            reasons = ()

        operands = QbConsistencyFormulaOperands(
            total_requirement_count=requirement_count,
            observed_rconf_count=len(aggregate_conflict_set.participant_ids),
        )
        value = operands.exact_value() if state is QbConsistencyState.COMPUTED else None

        return QbConsistencyAssessment(
            snapshot_id=snapshot.snapshot_id,
            state=state,
            value=value,
            rconf_participant_ids=aggregate_conflict_set.participant_ids,
            rconf_complete=aggregate_conflict_set.rconf_complete,
            observability=observability,
            coverage_profile=QB_COVERAGE_PROFILE,
            aggregation_rule=QB_CONSISTENCY_RULE,
            cross_result_ids=tuple(
                result.result_id
                for result in sorted(results, key=lambda item: item.order_key)
            ),
            materiality_diagnostic_refs=tuple(
                audit.diagnostic_ref for audit in materiality.audit_records
            ),
            reasons=reasons,
            formula_operands=operands,
            non_claim_contract=QB_NON_CLAIMS,
            non_claim_keys=(BoundedNonClaimKey.NC_QB_BASE,),
        )


__all__ = [
    "QB_CONSISTENCY_RULE",
    "QB_NON_CLAIMS",
    "QbConflictSet",
    "QbConflictSetBuilder",
    "QbConsistencyAggregator",
]

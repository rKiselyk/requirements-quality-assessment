"""Pure QB-v0.1 assessment of one validated observation-pair candidate.

The module deliberately contains no candidate selection, materiality,
aggregation, reporting, or general interval machinery.  It validates one
IMP-05 candidate against its immutable projection, applies the approved
four-state decision chain, and delegates result invariants and stable identity
to the IMP-01 domain factories.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
import unicodedata

from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorLabel,
    QuantitativeComponentName,
)

from .domain import (
    AssessmentSnapshotId,
    BoundedNonClaimKey,
    ComparisonKey,
    ComparisonOperand,
    ComparisonOperands,
    ContractVersionDescriptor,
    CrossEvidenceRef,
    CrossRelationKind,
    CrossRequirementResult,
    CrossResultState,
    CrossUnresolvedReason,
    OutsideApplicabilityReason,
    SnapshotCountManifest,
    SnapshotEvidenceManifest,
    SnapshotObservationManifest,
    SnapshotRequirementManifest,
)
from .projection import CrossRequirementProjection
from .selection import CrossCandidateOrderKey, CrossObservationPairCandidate


QB_COMPARISON_RULE = ContractVersionDescriptor("QB-COMPARE-001", "1")
QB_COVERAGE_PROFILE = ContractVersionDescriptor("QB-v0.1", "1")

_SNAPSHOT_NORMALIZATION_CONTRACT = ContractVersionDescriptor(
    "QB-NORMALIZATION", "1"
)
_SNAPSHOT_COMPARISON_CONTRACT = ContractVersionDescriptor("QB-COMPARISON", "1")
_SUPPORTED_COMPARATORS = frozenset(
    {
        ComparatorLabel.LESS_THAN_OR_EQUAL,
        ComparatorLabel.GREATER_THAN_OR_EQUAL,
    }
)


def normalize_qb_identity_text(text: str) -> str:
    """Apply the complete and only approved QB metric/context normalization."""

    if not isinstance(text, str):
        raise TypeError("QB identity text must be a string")
    # ``str.split`` without a separator recognizes Unicode whitespace, drops
    # leading/trailing runs, and lets the ASCII join token perform the exact
    # approved collapse.  The operation order is intentionally visible here.
    normalized = unicodedata.normalize("NFC", text)
    folded = normalized.casefold()
    return " ".join(folded.split())


@dataclass(frozen=True, slots=True)
class QbApplicabilityDecision:
    """The terminal applicability decision, or ``None`` for predicate-ready."""

    state: CrossResultState | None
    unresolved_reasons: tuple[CrossUnresolvedReason, ...] = ()
    outside_reasons: tuple[OutsideApplicabilityReason, ...] = ()

    def __post_init__(self) -> None:
        if self.state not in {
            None,
            CrossResultState.ASSESSMENT_UNRESOLVED,
            CrossResultState.OUTSIDE_V0_1_APPLICABILITY,
        }:
            raise ValueError("applicability decision has an invalid terminal state")
        if self.state is None and (self.unresolved_reasons or self.outside_reasons):
            raise ValueError("predicate-ready decisions cannot carry reasons")
        if self.state is CrossResultState.ASSESSMENT_UNRESOLVED:
            if not self.unresolved_reasons or self.outside_reasons:
                raise ValueError("unresolved decisions require only unresolved reasons")
        if self.state is CrossResultState.OUTSIDE_V0_1_APPLICABILITY:
            if not self.outside_reasons or self.unresolved_reasons:
                raise ValueError("outside decisions require only outside reasons")

    @property
    def predicate_ready(self) -> bool:
        return self.state is None


def _ordered_unique_enums(values: list[Enum], enum_type: type[Enum]) -> tuple:
    present = set(values)
    return tuple(item for item in enum_type if item in present)


class QbApplicabilityEvaluator:
    """Apply the approved comparator/mismatch/unresolved precedence."""

    def evaluate(
        self,
        operands: ComparisonOperands,
        *,
        left_unresolved_components: tuple[QuantitativeComponentName, ...] = (),
        right_unresolved_components: tuple[QuantitativeComponentName, ...] = (),
    ) -> QbApplicabilityDecision:
        if not isinstance(operands, ComparisonOperands):
            raise TypeError("operands must be ComparisonOperands")
        for value in (left_unresolved_components, right_unresolved_components):
            if not isinstance(value, tuple) or any(
                not isinstance(item, QuantitativeComponentName) for item in value
            ):
                raise TypeError(
                    "unresolved components must be tuples of QuantitativeComponentName"
                )

        pair = (operands.left, operands.right)

        # 1. A resolved comparator outside the profile is conclusive and is
        # never reinterpreted as missing or unresolved.
        if any(
            operand.comparator is not None
            and operand.comparator not in _SUPPORTED_COMPARATORS
            and operand.comparator is not ComparatorLabel.UPPER_BOUND
            for operand in pair
        ):
            return QbApplicabilityDecision(
                state=CrossResultState.OUTSIDE_V0_1_APPLICABILITY,
                outside_reasons=(
                    OutsideApplicabilityReason.COMPARATOR_OUTSIDE_PROFILE,
                ),
            )

        # 2. Any resolved identity inequality has precedence over unrelated
        # missing identity fields.  Preserve every resolved mismatch in enum
        # order, but do not attach unresolved reasons to an outside result.
        mismatches: list[OutsideApplicabilityReason] = []
        left, right = pair
        if (
            left.normalized_metric is not None
            and right.normalized_metric is not None
            and left.normalized_metric != right.normalized_metric
        ):
            mismatches.append(OutsideApplicabilityReason.METRIC_MISMATCH)
        if (
            left.normalized_context is not None
            and right.normalized_context is not None
            and left.normalized_context != right.normalized_context
        ):
            mismatches.append(OutsideApplicabilityReason.CONTEXT_MISMATCH)
        if left.unit is not None and right.unit is not None and left.unit is not right.unit:
            mismatches.append(OutsideApplicabilityReason.UNIT_MISMATCH)
        if mismatches:
            return QbApplicabilityDecision(
                state=CrossResultState.OUTSIDE_V0_1_APPLICABILITY,
                outside_reasons=_ordered_unique_enums(
                    mismatches, OutsideApplicabilityReason
                ),
            )

        # 3 and 4. Retain all applicable missing/unresolved reasons.  Step 3
        # decides the state before step 4, but UPPER_BOUND's unresolved
        # inclusivity is still preserved alongside missing identity inputs.
        reasons: list[CrossUnresolvedReason] = []
        for operand, explicit in zip(
            pair,
            (left_unresolved_components, right_unresolved_components),
            strict=True,
        ):
            explicit_set = set(explicit)
            if operand.normalized_metric is None:
                reasons.append(
                    CrossUnresolvedReason.UNRESOLVED_METRIC
                    if QuantitativeComponentName.METRIC in explicit_set
                    else CrossUnresolvedReason.MISSING_METRIC
                )
            if operand.normalized_context is None:
                reasons.append(
                    CrossUnresolvedReason.UNRESOLVED_CONTEXT
                    if QuantitativeComponentName.CONTEXT in explicit_set
                    else CrossUnresolvedReason.MISSING_CONTEXT
                )
            if operand.unit is None:
                reasons.append(CrossUnresolvedReason.MISSING_UNIT)
            if operand.value is None:
                reasons.append(CrossUnresolvedReason.MISSING_VALUE)
            if operand.comparator is None:
                reasons.append(CrossUnresolvedReason.MISSING_COMPARATOR)
            elif (
                operand.comparator is ComparatorLabel.UPPER_BOUND
                or operand.comparator in _SUPPORTED_COMPARATORS
                and operand.inclusivity is not BoundaryInclusivity.INCLUSIVE
            ):
                reasons.append(CrossUnresolvedReason.UNRESOLVED_INCLUSIVITY)

        if reasons:
            return QbApplicabilityDecision(
                state=CrossResultState.ASSESSMENT_UNRESOLVED,
                unresolved_reasons=_ordered_unique_enums(
                    reasons, CrossUnresolvedReason
                ),
            )
        return QbApplicabilityDecision(state=None)


class QbComparisonKeyBuilder:
    """Build exact bounded textual identity without semantic enrichment."""

    normalize = staticmethod(normalize_qb_identity_text)

    def build(self, operands: ComparisonOperands) -> ComparisonKey:
        if not isinstance(operands, ComparisonOperands):
            raise TypeError("operands must be ComparisonOperands")
        left, right = operands.left, operands.right
        if (
            left.normalized_metric is None
            or right.normalized_metric is None
            or left.normalized_context is None
            or right.normalized_context is None
            or left.unit is None
            or right.unit is None
        ):
            raise ValueError("comparison key requires resolved metric, context, and unit")
        if left.normalized_metric != right.normalized_metric:
            raise ValueError("comparison key requires equal normalized metrics")
        if left.normalized_context != right.normalized_context:
            raise ValueError("comparison key requires equal normalized contexts")
        if left.unit is not right.unit:
            raise ValueError("comparison key requires exact equal UnitLabel values")
        return ComparisonKey(
            normalized_metric=left.normalized_metric,
            normalized_context=left.normalized_context,
            unit=left.unit,
        )


class SupportedBoundDirection(str, Enum):
    UPPER = "UPPER"
    LOWER = "LOWER"


@dataclass(frozen=True, slots=True)
class SupportedInclusiveBound:
    direction: SupportedBoundDirection
    value: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.direction, SupportedBoundDirection):
            raise TypeError("direction must be a SupportedBoundDirection")
        if not isinstance(self.value, Decimal):
            raise TypeError("value must be an exact Decimal")


class QbSupportedBoundValidator:
    """Admit only the two approved resolved inclusive bound forms."""

    def validate(self, operand: ComparisonOperand) -> SupportedInclusiveBound:
        if not isinstance(operand, ComparisonOperand):
            raise TypeError("operand must be a ComparisonOperand")
        if operand.comparator not in _SUPPORTED_COMPARATORS:
            raise ValueError("comparator is not a supported QB-v0.1 bound")
        if operand.inclusivity is not BoundaryInclusivity.INCLUSIVE:
            raise ValueError("supported QB-v0.1 bounds must be inclusive")
        if not isinstance(operand.value, Decimal):
            raise ValueError("supported QB-v0.1 bounds require an exact Decimal value")
        direction = (
            SupportedBoundDirection.UPPER
            if operand.comparator is ComparatorLabel.LESS_THAN_OR_EQUAL
            else SupportedBoundDirection.LOWER
        )
        return SupportedInclusiveBound(direction=direction, value=operand.value)


def direct_bound_conflict(
    left: SupportedInclusiveBound,
    right: SupportedInclusiveBound,
) -> bool:
    """Return whether two approved inclusive half-lines have empty intersection."""

    if not isinstance(left, SupportedInclusiveBound) or not isinstance(
        right, SupportedInclusiveBound
    ):
        raise TypeError("direct bound predicate requires supported inclusive bounds")
    if left.direction is right.direction:
        return False
    lower = left if left.direction is SupportedBoundDirection.LOWER else right
    upper = left if left.direction is SupportedBoundDirection.UPPER else right
    return lower.value > upper.value


class QbConflictPredicate:
    """Named callable boundary for the approved direct predicate."""

    def conflicts(
        self,
        left: SupportedInclusiveBound,
        right: SupportedInclusiveBound,
    ) -> bool:
        return direct_bound_conflict(left, right)

    __call__ = conflicts


class CrossResultFactory:
    """Construct one state-valid IMP-01 result from assessed pair data."""

    def create(
        self,
        *,
        candidate: CrossObservationPairCandidate,
        operands: ComparisonOperands,
        evidence_refs: tuple[CrossEvidenceRef, ...],
        decision: QbApplicabilityDecision,
        comparison_key: ComparisonKey | None = None,
        conflict: bool | None = None,
    ) -> CrossRequirementResult:
        if not isinstance(candidate, CrossObservationPairCandidate):
            raise TypeError("candidate must be a CrossObservationPairCandidate")
        if not isinstance(operands, ComparisonOperands):
            raise TypeError("operands must be ComparisonOperands")
        if not isinstance(decision, QbApplicabilityDecision):
            raise TypeError("decision must be a QbApplicabilityDecision")
        if candidate.snapshot_id != operands.left.snapshot_id:
            raise ValueError("candidate and operands cannot cross snapshots")
        if candidate.observation_refs != (
            operands.left.observation_ref,
            operands.right.observation_ref,
        ):
            raise ValueError("result operands must match the candidate exactly")

        common = {
            "snapshot_id": candidate.snapshot_id,
            "participants": candidate.participants,
            "observation_refs": candidate.observation_refs,
            "operands": operands,
            "comparison_contract": QB_COMPARISON_RULE,
            "coverage_profile": QB_COVERAGE_PROFILE,
            "relation_kind": CrossRelationKind.QUANTITATIVE_BOUND,
            "evidence_refs": evidence_refs,
            "diagnostic_refs": (),
            "non_claim_keys": (BoundedNonClaimKey.NC_QB_BASE,),
        }
        if decision.state is CrossResultState.OUTSIDE_V0_1_APPLICABILITY:
            if comparison_key is not None or conflict is not None:
                raise ValueError("outside results cannot carry predicate output")
            return CrossRequirementResult.outside_v0_1_applicability(
                outside_reasons=decision.outside_reasons,
                **common,
            )
        if decision.state is CrossResultState.ASSESSMENT_UNRESOLVED:
            if comparison_key is not None or conflict is not None:
                raise ValueError("unresolved results cannot carry predicate output")
            return CrossRequirementResult.assessment_unresolved(
                unresolved_reasons=decision.unresolved_reasons,
                **common,
            )
        if not decision.predicate_ready or comparison_key is None or type(conflict) is not bool:
            raise ValueError("complete results require a key and boolean predicate output")
        complete = {**common, "comparison_key": comparison_key}
        if conflict:
            return CrossRequirementResult.confirmed_conflict(**complete)
        return CrossRequirementResult.compatible_within_rule(**complete)


def _snapshot_integrity(projection: CrossRequirementProjection) -> None:
    snapshot = projection.snapshot
    if projection.snapshot_id != projection.resolver.snapshot_id:
        raise ValueError("projection snapshot and resolver identities must match")
    projection.resolver.assert_snapshot(snapshot)
    if snapshot.contracts.normalization != _SNAPSHOT_NORMALIZATION_CONTRACT:
        raise ValueError("projection does not use the approved normalization contract")
    if snapshot.contracts.comparison != _SNAPSHOT_COMPARISON_CONTRACT:
        raise ValueError("projection does not use the approved comparison contract slot")
    if snapshot.contracts.coverage_profile != QB_COVERAGE_PROFILE:
        raise ValueError("projection does not use QB-v0.1 / 1 coverage")
    if snapshot.counts != SnapshotCountManifest.from_requirements(snapshot.requirements):
        raise ValueError("projection count/order manifest is corrupt")
    if AssessmentSnapshotId.from_bytes(snapshot.canonical_bytes()) != snapshot.snapshot_id:
        raise ValueError("projection snapshot identity does not match canonical content")


def _candidate_requirement(
    projection: CrossRequirementProjection,
    order_key,
) -> SnapshotRequirementManifest:
    matches = tuple(
        item
        for item in projection.requirements
        if item.requirement_id == order_key.requirement_id
        and item.source_order == order_key.source_order
    )
    if len(matches) != 1:
        raise ValueError("candidate participant must resolve exactly once in the snapshot")
    return matches[0]


def _manifest_evidence(
    requirement: SnapshotRequirementManifest,
    ref: CrossEvidenceRef,
) -> SnapshotEvidenceManifest:
    matches = tuple(item for item in requirement.evidence if item.ref == ref)
    if len(matches) != 1:
        raise ValueError("observation Evidence ref must resolve exactly once in the snapshot")
    return matches[0]


def _source_observation_values(source) -> tuple:
    component_refs = lambda component: () if component is None else component.evidence_refs
    return (
        component_refs(source.metric),
        None if source.comparator is None else source.comparator.label,
        None if source.comparator is None else source.comparator.inclusivity,
        component_refs(source.comparator),
        None if source.value is None else source.value.decimal_value,
        component_refs(source.value),
        None if source.unit is None else source.unit.label,
        component_refs(source.unit),
        component_refs(source.context),
        source.unresolved_components,
        source.evidence_refs,
    )


def _manifest_observation_values(manifest: SnapshotObservationManifest) -> tuple:
    ids = lambda refs: tuple(item.evidence_id for item in refs)
    return (
        ids(manifest.metric_evidence_refs),
        manifest.comparator,
        manifest.inclusivity,
        ids(manifest.comparator_evidence_refs),
        manifest.value,
        ids(manifest.value_evidence_refs),
        manifest.unit,
        ids(manifest.unit_evidence_refs),
        ids(manifest.context_evidence_refs),
        manifest.unresolved_components,
        ids(manifest.evidence_refs),
    )


def _validate_and_resolve_observation(
    projection: CrossRequirementProjection,
    requirement: SnapshotRequirementManifest,
    ref,
) -> SnapshotObservationManifest:
    if ref.requirement_id != requirement.requirement_id:
        raise ValueError("candidate observation owner does not match its participant")
    if ref.observation_index >= len(requirement.observations):
        raise ValueError("candidate observation ref is outside the snapshot")
    manifest = requirement.observations[ref.observation_index]
    if manifest.ref != ref:
        raise ValueError("candidate observation ref does not match projected source order")

    source_requirement = projection.resolver.resolve_requirement(
        requirement.requirement_id,
        snapshot_id=projection.snapshot_id,
    )
    if (
        source_requirement.id,
        source_requirement.source_line,
        source_requirement.text,
    ) != (
        requirement.requirement_id,
        requirement.source_line,
        requirement.text,
    ):
        raise ValueError("projected requirement does not match resolved provenance")

    source = projection.resolver.resolve_observation(
        ref,
        snapshot_id=projection.snapshot_id,
    )
    if _source_observation_values(source) != _manifest_observation_values(manifest):
        raise ValueError("projected observation does not match resolved provenance")

    groups = (
        (QuantitativeComponentName.METRIC, manifest.metric_evidence_refs),
        (QuantitativeComponentName.COMPARATOR, manifest.comparator_evidence_refs),
        (QuantitativeComponentName.VALUE, manifest.value_evidence_refs),
        (QuantitativeComponentName.UNIT, manifest.unit_evidence_refs),
        (QuantitativeComponentName.CONTEXT, manifest.context_evidence_refs),
    )
    for component, refs in groups:
        for evidence_ref in refs:
            source_evidence = projection.resolver.resolve_evidence(
                evidence_ref,
                observation_ref=ref,
                component=component,
                snapshot_id=projection.snapshot_id,
            )
            evidence = _manifest_evidence(requirement, evidence_ref)
            if (
                source_evidence.requirement_id,
                source_evidence.feature_id,
                source_evidence.text,
                source_evidence.start_offset,
                source_evidence.end_offset,
                source_evidence.rule_id,
                source_evidence.evidence_id,
            ) != (
                evidence.ref.requirement_id,
                evidence.feature_id,
                evidence.text,
                evidence.start_offset,
                evidence.end_offset,
                evidence.rule_id,
                evidence.ref.evidence_id,
            ):
                raise ValueError("projected Evidence does not match resolved provenance")
    for evidence_ref in manifest.evidence_refs:
        projection.resolver.resolve_evidence(
            evidence_ref,
            observation_ref=ref,
            snapshot_id=projection.snapshot_id,
        )
    return manifest


def _component_text(
    requirement: SnapshotRequirementManifest,
    refs: tuple[CrossEvidenceRef, ...],
    name: str,
) -> str | None:
    if not refs:
        return None
    if len(refs) != 1:
        raise ValueError(
            f"resolved {name} requires exactly one approved source Evidence item"
        )
    return _manifest_evidence(requirement, refs[0]).text


def _operand(
    snapshot_id: AssessmentSnapshotId,
    requirement: SnapshotRequirementManifest,
    observation: SnapshotObservationManifest,
) -> ComparisonOperand:
    metric = _component_text(
        requirement, observation.metric_evidence_refs, "metric"
    )
    context = _component_text(
        requirement, observation.context_evidence_refs, "context"
    )
    return ComparisonOperand(
        snapshot_id=snapshot_id,
        observation_ref=observation.ref,
        normalized_metric=(
            None if metric is None else normalize_qb_identity_text(metric)
        ),
        normalized_context=(
            None if context is None else normalize_qb_identity_text(context)
        ),
        comparator=observation.comparator,
        inclusivity=observation.inclusivity,
        value=observation.value,
        unit=observation.unit,
    )


def _ordered_result_evidence(
    left_requirement: SnapshotRequirementManifest,
    left_observation: SnapshotObservationManifest,
    right_requirement: SnapshotRequirementManifest,
    right_observation: SnapshotObservationManifest,
) -> tuple[CrossEvidenceRef, ...]:
    ordered: list[CrossEvidenceRef] = []
    for requirement, observation in (
        (left_requirement, left_observation),
        (right_requirement, right_observation),
    ):
        evidence = tuple(
            sorted(
                (_manifest_evidence(requirement, ref) for ref in observation.evidence_refs),
                key=lambda item: (
                    item.start_offset,
                    item.end_offset,
                    item.ref.evidence_id,
                ),
            )
        )
        ordered.extend(item.ref for item in evidence)
    return tuple(ordered)


class QbObservationPairAssessor:
    """Convert exactly one validated IMP-05 candidate into exactly one result."""

    def __init__(
        self,
        *,
        applicability: QbApplicabilityEvaluator | None = None,
        key_builder: QbComparisonKeyBuilder | None = None,
        bound_validator: QbSupportedBoundValidator | None = None,
        predicate: QbConflictPredicate | None = None,
        result_factory: CrossResultFactory | None = None,
    ) -> None:
        self._applicability = applicability or QbApplicabilityEvaluator()
        self._key_builder = key_builder or QbComparisonKeyBuilder()
        self._bound_validator = bound_validator or QbSupportedBoundValidator()
        self._predicate = predicate or QbConflictPredicate()
        self._result_factory = result_factory or CrossResultFactory()

    def assess(
        self,
        candidate: CrossObservationPairCandidate,
        projection: CrossRequirementProjection,
    ) -> CrossRequirementResult:
        if not isinstance(candidate, CrossObservationPairCandidate):
            raise TypeError("candidate must be a CrossObservationPairCandidate")
        if not isinstance(projection, CrossRequirementProjection):
            raise TypeError("projection must be a CrossRequirementProjection")
        _snapshot_integrity(projection)
        if candidate.snapshot_id != projection.snapshot_id:
            raise ValueError("candidate and projection cannot cross snapshots")
        expected_key = CrossCandidateOrderKey(
            earlier_requirement=candidate.earlier_requirement,
            later_requirement=candidate.later_requirement,
            left_observation_index=candidate.left.observation_index,
            right_observation_index=candidate.right.observation_index,
        )
        if candidate.order_key != expected_key:
            raise ValueError("candidate order key is corrupt")

        left_requirement = _candidate_requirement(
            projection, candidate.earlier_requirement
        )
        right_requirement = _candidate_requirement(
            projection, candidate.later_requirement
        )
        left_observation = _validate_and_resolve_observation(
            projection, left_requirement, candidate.left
        )
        right_observation = _validate_and_resolve_observation(
            projection, right_requirement, candidate.right
        )
        operands = ComparisonOperands(
            left=_operand(
                projection.snapshot_id, left_requirement, left_observation
            ),
            right=_operand(
                projection.snapshot_id, right_requirement, right_observation
            ),
        )
        evidence_refs = _ordered_result_evidence(
            left_requirement,
            left_observation,
            right_requirement,
            right_observation,
        )
        decision = self._applicability.evaluate(
            operands,
            left_unresolved_components=left_observation.unresolved_components,
            right_unresolved_components=right_observation.unresolved_components,
        )
        if not decision.predicate_ready:
            return self._result_factory.create(
                candidate=candidate,
                operands=operands,
                evidence_refs=evidence_refs,
                decision=decision,
            )

        comparison_key = self._key_builder.build(operands)
        left_bound = self._bound_validator.validate(operands.left)
        right_bound = self._bound_validator.validate(operands.right)
        conflict = self._predicate(left_bound, right_bound)
        return self._result_factory.create(
            candidate=candidate,
            operands=operands,
            evidence_refs=evidence_refs,
            decision=decision,
            comparison_key=comparison_key,
            conflict=conflict,
        )


# Concise aliases make the service useful to callers that use either the
# architecture's pair-assessor term or the issue's pair-assessment wording.
QbPairAssessor = QbObservationPairAssessor


__all__ = [
    "QB_COMPARISON_RULE",
    "QB_COVERAGE_PROFILE",
    "CrossResultFactory",
    "QbApplicabilityDecision",
    "QbApplicabilityEvaluator",
    "QbComparisonKeyBuilder",
    "QbConflictPredicate",
    "QbObservationPairAssessor",
    "QbPairAssessor",
    "QbSupportedBoundValidator",
    "SupportedBoundDirection",
    "SupportedInclusiveBound",
    "direct_bound_conflict",
    "normalize_qb_identity_text",
]

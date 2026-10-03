"""Compatibility-gated exact comparison under COMPARE-FULL-MODEL-001 / 1."""

from __future__ import annotations

from .domain import (
    COMPARISON_RULE_REF,
    MANDATORY_COMPARISON_NON_CLAIMS,
    ComparableResult,
    ComparisonClaim,
    ComparisonKind,
    ComparisonReason,
    ComparisonRequest,
    ComparisonSubject,
    ComparisonValueKind,
    CompatibilityComponentKind,
    CompatibilityDisposition,
    ResultComparison,
    ResultStateAndValue,
    SemanticCompatibilityDeclaration,
)
from ..dynamic_evidence import FullModelStatus
from ..performance_efficiency import ProcessStage
from ..product_quality import CalibrationStatus


def _state(result: ComparableResult | None) -> ResultStateAndValue | None:
    if result is None:
        return None
    return ResultStateAndValue(
        result.status,
        result.applicability,
        result.exact_value,
        result.categorical_state,
    )


def _contains_missing_identity(subject: ComparisonSubject) -> bool:
    def missing(value: object) -> bool:
        if value is None:
            return True
        if isinstance(value, tuple):
            return any(missing(item) for item in value)
        return False

    return (
        not subject.stable_subject_identity
        or missing(subject.stable_subject_identity)
        or missing(subject.ordered_lineage_population)
        or missing(subject.scope_identity)
        or missing(subject.evidence_context)
    )


def _declaration_for(
    before_ref: object,
    after_ref: object,
    kind: CompatibilityComponentKind,
    subject: ComparisonSubject,
    declarations: tuple[SemanticCompatibilityDeclaration, ...],
) -> SemanticCompatibilityDeclaration | None:
    return next(
        (
            item
            for item in declarations
            if item.component_kind is kind
            and item.before_ref == before_ref
            and item.after_ref == after_ref
            and item.comparison_scope == subject
            and item.disposition
            is CompatibilityDisposition.COMPATIBLE_FOR_COMPARISON
        ),
        None,
    )


def _semantics_compatible(
    before: tuple[object, ...],
    after: tuple[object, ...],
    kind: CompatibilityComponentKind,
    subject: ComparisonSubject,
    declarations: tuple[SemanticCompatibilityDeclaration, ...],
) -> tuple[bool, tuple[str, ...]]:
    if before == after:
        return True, ()
    if len(before) != len(after):
        return False, ()
    used: list[str] = []
    for before_ref, after_ref in zip(before, after, strict=True):
        if before_ref == after_ref:
            continue
        declaration = _declaration_for(
            before_ref,
            after_ref,
            kind,
            subject,
            declarations,
        )
        if declaration is None:
            return False, ()
        used.append(declaration.declaration_id)
    return True, tuple(used)


def _calibration(
    before: ComparableResult,
    after: ComparableResult,
) -> CalibrationStatus | None:
    values = tuple(
        value
        for value in (
            before.calibration_status_or_none,
            after.calibration_status_or_none,
        )
        if value is not None
    )
    if CalibrationStatus.PROVISIONAL_NOT_CALIBRATED in values:
        return CalibrationStatus.PROVISIONAL_NOT_CALIBRATED
    return values[0] if values and len(set(values)) == 1 else None


def _result(
    request: ComparisonRequest,
    *,
    status: FullModelStatus,
    kind: ComparisonKind | None,
    reasons: tuple[ComparisonReason, ...],
    subject: ComparisonSubject | None,
    explanation: str,
    declaration_refs: tuple[str, ...] = (),
) -> ResultComparison:
    before = request.before
    after = request.after
    parameter_refs = tuple(
        dict.fromkeys(
            (
                *(() if before is None else before.parameter_set_refs),
                *(() if after is None else after.parameter_set_refs),
            )
        )
    )
    calibration = (
        None if before is None or after is None else _calibration(before, after)
    )
    provenance = (
        request.ref,
        *((request.artifact_transition.transition_id,) if request.artifact_transition else ()),
        *((before.result_ref,) if before else ()),
        *((after.result_ref,) if after else ()),
        *declaration_refs,
        COMPARISON_RULE_REF,
    )
    return ResultComparison(
        comparison_id=request.comparison_id,
        comparison_version=request.comparison_version,
        before_result_ref=None if before is None else before.result_ref,
        after_result_ref=None if after is None else after.result_ref,
        comparison_subject=subject,
        status=status,
        comparison_kind=kind,
        before_state_and_value=_state(before),
        after_state_and_value=_state(after),
        reason_codes=reasons,
        rule_ref=COMPARISON_RULE_REF,
        compatibility_declaration_refs=declaration_refs,
        parameter_set_refs=parameter_refs,
        calibration_status_or_none=calibration,
        explanation=explanation,
        provenance=provenance,
        claims=(ComparisonClaim.STRUCTURED_CHANGE_ONLY,),
        non_claims=MANDATORY_COMPARISON_NON_CLAIMS,
    )


def compare(request: ComparisonRequest) -> ResultComparison:
    """Describe typed change only; never assign quality polarity or causality."""

    if not isinstance(request, ComparisonRequest):
        raise TypeError("request must be a ComparisonRequest")
    before = request.before
    after = request.after
    if before is None or after is None:
        return _result(
            request,
            status=FullModelStatus.UNAVAILABLE,
            kind=None,
            reasons=(ComparisonReason.REQUIRED_RESULT_UNAVAILABLE,),
            subject=None,
            explanation="A required result record is absent; no comparison conclusion exists.",
        )
    if before.subject is None or after.subject is None:
        return _result(
            request,
            status=FullModelStatus.UNRESOLVED,
            kind=None,
            reasons=(ComparisonReason.RESULT_IDENTITY_UNRESOLVED,),
            subject=before.subject or after.subject,
            explanation="Stable subject identity is missing, so comparability cannot be decided.",
        )
    if _contains_missing_identity(before.subject) or _contains_missing_identity(after.subject):
        return _result(
            request,
            status=FullModelStatus.UNRESOLVED,
            kind=None,
            reasons=(ComparisonReason.RESULT_IDENTITY_UNRESOLVED,),
            subject=before.subject,
            explanation="Stable lineage or scope identity is incomplete, so comparability is unresolved.",
        )

    reasons: list[ComparisonReason] = []
    if before.subject.result_family is not after.subject.result_family:
        reasons.append(ComparisonReason.RESULT_FAMILY_MISMATCH)
    if before.value_kind is not after.value_kind:
        reasons.append(ComparisonReason.VALUE_KIND_OR_SCALE_MISMATCH)
    if (
        before.value_kind is ComparisonValueKind.EXACT_FRACTION
        and before.numeric_scale_or_none != after.numeric_scale_or_none
    ):
        reasons.append(ComparisonReason.VALUE_KIND_OR_SCALE_MISMATCH)
    if (
        before.subject.metric_or_characteristic_id
        != after.subject.metric_or_characteristic_id
    ):
        reasons.append(ComparisonReason.METRIC_OR_CHARACTERISTIC_MISMATCH)
    if before.subject.stable_subject_identity != after.subject.stable_subject_identity:
        reasons.append(ComparisonReason.SUBJECT_LINEAGE_MISSING_OR_MISMATCH)
    transition = request.artifact_transition
    if (
        transition is None
        or transition.parent_artifact_ref != before.result_ref.artifact_ref
        or transition.child_artifact_ref != after.result_ref.artifact_ref
    ):
        reasons.append(ComparisonReason.ARTIFACT_ANCESTRY_MISSING_OR_MISMATCH)
    if (
        before.subject.ordered_lineage_population
        != after.subject.ordered_lineage_population
        or before.subject.scope_identity != after.subject.scope_identity
    ):
        reasons.append(ComparisonReason.SCOPE_OR_POPULATION_MISMATCH)
    if before.subject.evidence_context != after.subject.evidence_context:
        reasons.append(ComparisonReason.EVIDENCE_CONTEXT_MISMATCH)
    if (
        before.process_stage is not ProcessStage.REFERENCE_VERIFICATION
        or after.process_stage is not ProcessStage.REFERENCE_VERIFICATION
        or before.process_stage is not after.process_stage
    ):
        reasons.append(ComparisonReason.PROCESS_STAGE_MISMATCH)
    if before.source_contract_ref != after.source_contract_ref:
        reasons.append(ComparisonReason.APPLICABILITY_SEMANTICS_INCOMPATIBLE)

    declaration_refs: list[str] = []
    for before_refs, after_refs, component_kind, reason in (
        (
            before.rule_refs,
            after.rule_refs,
            CompatibilityComponentKind.RULE,
            ComparisonReason.RULE_SEMANTICS_INCOMPATIBLE,
        ),
        (
            before.model_refs,
            after.model_refs,
            CompatibilityComponentKind.MODEL,
            ComparisonReason.MODEL_SEMANTICS_INCOMPATIBLE,
        ),
        (
            before.parameter_set_refs,
            after.parameter_set_refs,
            CompatibilityComponentKind.PARAMETER_SET,
            ComparisonReason.PARAMETER_SEMANTICS_INCOMPATIBLE,
        ),
    ):
        compatible, used = _semantics_compatible(
            before_refs,
            after_refs,
            component_kind,
            before.subject,
            request.compatibility_declarations,
        )
        if not compatible:
            reasons.append(reason)
        declaration_refs.extend(used)

    if reasons:
        ordered = tuple(dict.fromkeys(reasons))
        return _result(
            request,
            status=FullModelStatus.AVAILABLE,
            kind=ComparisonKind.NOT_COMPARABLE,
            reasons=ordered,
            subject=before.subject,
            explanation=(
                "The typed records are not semantically compatible under "
                "COMPARE-FULL-MODEL-001 / 1. No value relation is calculated."
            ),
            declaration_refs=tuple(dict.fromkeys(declaration_refs)),
        )

    if (
        before.value_kind is ComparisonValueKind.EXACT_FRACTION
        and before.status is FullModelStatus.AVAILABLE
        and after.status is FullModelStatus.AVAILABLE
    ):
        if before.exact_value == after.exact_value:
            kind = ComparisonKind.UNCHANGED
            reason = ComparisonReason.EXACT_VALUES_EQUAL
        elif before.exact_value < after.exact_value:
            kind = ComparisonKind.INCREASED
            reason = ComparisonReason.EXACT_VALUE_INCREASED
        else:
            kind = ComparisonKind.DECREASED
            reason = ComparisonReason.EXACT_VALUE_DECREASED
        explanation = f"The exact Fraction relation is {kind.value}."
    else:
        before_state = _state(before)
        after_state = _state(after)
        if before_state == after_state:
            kind = ComparisonKind.UNCHANGED
            reason = ComparisonReason.STRUCTURED_STATE_UNCHANGED
        else:
            kind = ComparisonKind.STATE_CHANGED
            reason = ComparisonReason.STRUCTURED_STATE_CHANGED
        explanation = f"The bounded typed state relation is {kind.value}."

    return _result(
        request,
        status=FullModelStatus.AVAILABLE,
        kind=kind,
        reasons=(reason,),
        subject=before.subject,
        explanation=explanation,
        declaration_refs=tuple(dict.fromkeys(declaration_refs)),
    )


__all__ = ["compare"]

"""Additive, calculation-free presentation of finished QB-v0.1 results."""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum

from .cross_analysis.domain import (
    ComparisonOperand,
    ContractVersionDescriptor,
    CrossDiagnosticRef,
    CrossEvidenceRef,
    CrossObservationRef,
    CrossRequirementResult,
    CrossResultState,
    AssessmentSnapshotId,
    QbConsistencyReason,
    QbConsistencyState,
    QbMaterialityAuditRecord,
    QbMaterialityResult,
)
from .cross_analysis.projection import CrossEvidenceResolver, CrossRequirementProjection
from .cross_analysis.specification import (
    SpecificationAssessment,
    SpecificationAssessmentResult,
)
from .domain import Evidence, RequirementAssessmentRecord


_QB_NON_CLAIMS = (
    "absence of a detected conflict is not proof of universal semantic consistency",
    "only the supported bounded quantitative constructions were evaluated",
    "COMPATIBLE_WITHIN_RULE applies only to the supported observation pair and rule; "
    "it is not a general absence-of-conflict claim",
    "unsupported semantic equivalence is not inferred",
    "no synonym, terminology, ontology, embedding, or fuzzy-match equivalence is "
    "assumed",
    "no unit conversion or dimensional equivalence is inferred",
    "no context overlap beyond exact normalized identity is inferred",
    "no implicit domain knowledge or common-sense knowledge is supplied",
    "no general claim is made about logical consistency outside the supported bounded "
    "rule, terminological consistency, resource consistency, duplication, coverage, or "
    "traceability",
    "no severity, risk, probability, confidence score, priority, or corrective action "
    "is inferred",
    "no software-product quality or defect-probability conclusion is produced",
    "M_cons[QB-v0.1] is not a combined specification-quality score",
    "the unqualified full-source M_cons remains non-executable",
    "UNKNOWN and NOT_APPLICABLE are not numeric values and never mean zero",
)

_USER_AGGREGATE_REASONS = {
    QbConsistencyReason.FEWER_THAN_TWO_REQUIREMENTS: (
        "у специфікації менше двох вимог"
    ),
    QbConsistencyReason.QB_MATERIAL_UNRESOLVED_EXTRACTION: (
        "наявні невирішені дані видобування, істотні для QB-v0.1"
    ),
    QbConsistencyReason.ASSESSMENT_UNRESOLVED_PAIR: (
        "принаймні одну пару не вдалося однозначно оцінити за QB-v0.1"
    ),
    QbConsistencyReason.NO_APPLICABLE_COMPARISONS: (
        "немає порівнянь, застосовних у межах QB-v0.1"
    ),
}

_USER_UNRESOLVED_REASONS = {
    "MISSING_METRIC": "відсутня метрика",
    "UNRESOLVED_METRIC": "метрика лишилася невирішеною",
    "MISSING_CONTEXT": "відсутній контекст",
    "UNRESOLVED_CONTEXT": "контекст лишився невирішеним",
    "MISSING_UNIT": "відсутня одиниця вимірювання",
    "MISSING_VALUE": "відсутнє кількісне значення",
    "MISSING_COMPARATOR": "відсутній компаратор",
    "UNRESOLVED_INCLUSIVITY": "межа включності лишилася невирішеною",
    "MATERIAL_UNRESOLVED_EXTRACTION": (
        "наявні істотні невирішені дані видобування"
    ),
}

_USER_OUTSIDE_REASONS = {
    "METRIC_MISMATCH": "метрики не збігаються",
    "CONTEXT_MISMATCH": "контексти не збігаються",
    "UNIT_MISMATCH": "одиниці вимірювання не збігаються",
    "COMPARATOR_OUTSIDE_PROFILE": "компаратор не входить до профілю QB-v0.1",
}


@dataclass(frozen=True, slots=True)
class AssessmentReportBundle:
    """Validated report boundary over one authoritative IMP-09 result.

    The wrapper retains the completed result by reference.  Its properties do
    not copy or recreate scientific values, Evidence, diagnostics, or source
    objects.
    """

    assessment_result: SpecificationAssessmentResult

    def __post_init__(self) -> None:
        if not isinstance(self.assessment_result, SpecificationAssessmentResult):
            raise TypeError(
                "assessment_result must be a SpecificationAssessmentResult"
            )

        result = self.assessment_result
        # Reapply the immutable IMP-09 composition invariant at the reporting
        # boundary.  This validates ownership/association only; it performs no
        # extraction, assessment, projection, classification, or aggregation.
        SpecificationAssessmentResult(
            records=result.records,
            specification_assessment=result.specification_assessment,
            projection=result.projection,
            cross_results=result.cross_results,
            materiality=result.materiality,
        )
        resolver = result.resolver
        for cross_result in result.cross_results:
            observations_by_owner = {
                ref.requirement_id: ref for ref in cross_result.observation_refs
            }
            for observation_ref in cross_result.observation_refs:
                resolver.resolve_observation(
                    observation_ref,
                    snapshot_id=result.snapshot_id,
                )
            for evidence_ref in cross_result.evidence_refs:
                resolver.resolve_evidence(
                    evidence_ref,
                    observation_ref=observations_by_owner[
                        evidence_ref.requirement_id
                    ],
                    snapshot_id=result.snapshot_id,
                )
            for diagnostic_ref in cross_result.diagnostic_refs:
                resolver.resolve_diagnostic(
                    diagnostic_ref,
                    snapshot_id=result.snapshot_id,
                )
        for audit in result.materiality.audit_records:
            resolver.resolve_diagnostic(
                audit.diagnostic_ref,
                snapshot_id=result.snapshot_id,
            )
            if audit.matched_context_evidence_ref is not None:
                resolver.resolve_evidence(
                    audit.matched_context_evidence_ref,
                    snapshot_id=result.snapshot_id,
                )

    @classmethod
    def from_result(
        cls, result: SpecificationAssessmentResult
    ) -> AssessmentReportBundle:
        return cls(result)

    @property
    def records(self) -> tuple[RequirementAssessmentRecord, ...]:
        return self.assessment_result.records

    @property
    def specification_assessment(self) -> SpecificationAssessment:
        return self.assessment_result.specification_assessment

    @property
    def cross_results(self) -> tuple[CrossRequirementResult, ...]:
        return self.assessment_result.cross_results

    @property
    def materiality(self) -> QbMaterialityResult:
        return self.assessment_result.materiality

    @property
    def resolver(self) -> CrossEvidenceResolver:
        return self.assessment_result.resolver

    @property
    def snapshot_id(self) -> AssessmentSnapshotId:
        return self.assessment_result.snapshot_id

    @property
    def projection(self) -> CrossRequirementProjection:
        return self.assessment_result.projection


def _descriptor(value: ContractVersionDescriptor) -> str:
    return f"{value.contract_id} / {value.version}"


def _bool_token(value: bool) -> str:
    return "yes" if value else "no"


def _enum_or_none(value: Enum | None) -> str:
    return "none" if value is None else value.value


def _ref(value: CrossEvidenceRef | CrossDiagnosticRef | CrossObservationRef) -> str:
    if isinstance(value, CrossEvidenceRef):
        return f"{value.requirement_id}:{value.evidence_id}"
    if isinstance(value, CrossDiagnosticRef):
        return (
            f"{value.requirement_id}:{value.feature_id.value}:"
            f"diagnostic[{value.diagnostic_index}]"
        )
    return (
        f"{value.requirement_id}:{value.feature_id.value}:"
        f"observation[{value.observation_index}]"
    )


def _resolved_evidence(
    bundle: AssessmentReportBundle,
    refs: tuple[CrossEvidenceRef, ...],
) -> tuple[tuple[CrossEvidenceRef, Evidence], ...]:
    return tuple(
        (
            ref,
            bundle.resolver.resolve_evidence(
                ref,
                snapshot_id=bundle.snapshot_id,
            ),
        )
        for ref in refs
    )


class AuditCrossRequirementReporter:
    """Render the complete technical cross-requirement audit section."""

    def render(self, bundle: AssessmentReportBundle) -> str:
        if not isinstance(bundle, AssessmentReportBundle):
            raise TypeError("audit cross reporter requires AssessmentReportBundle")

        assessment = bundle.specification_assessment.qb_consistency
        observability = assessment.observability
        value = assessment.value if assessment.value is not None else assessment.state.value
        reasons = (
            ", ".join(reason.value for reason in assessment.reasons)
            if assessment.reasons
            else "none"
        )
        rconf = (
            ", ".join(assessment.rconf_participant_ids)
            if assessment.rconf_participant_ids
            else "none"
        )

        lines = [
            "Cross-Requirement Consistency",
            f"snapshot_id: {assessment.snapshot_id.value}",
            f"coverage_profile: {_descriptor(assessment.coverage_profile)}",
            f"aggregation_rule: {_descriptor(assessment.aggregation_rule)}",
            f"non_claim_contract: {_descriptor(assessment.non_claim_contract)}",
            "non_claim_keys: "
            + ", ".join(item.value for item in assessment.non_claim_keys),
            f"state: {assessment.state.value}",
            f"value: {value}",
            f"observed_R_conf: {rconf}",
            f"rconf_complete: {_bool_token(assessment.rconf_complete)}",
            f"aggregate_reasons: {reasons}",
            "formula_operands:",
            "  total_requirement_count: "
            f"{assessment.formula_operands.total_requirement_count}",
            "  observed_rconf_count: "
            f"{assessment.formula_operands.observed_rconf_count}",
            "observability:",
        ]
        for field in fields(observability):
            field_value = getattr(observability, field.name)
            rendered = _bool_token(field_value) if type(field_value) is bool else field_value
            lines.append(f"  {field.name}: {rendered}")

        lines.extend(("quantitative_extraction_status:",))
        if bundle.projection.requirements:
            for manifest in bundle.projection.requirements:
                lines.append(
                    f"  - {manifest.requirement_id}: {manifest.processing_status.value}"
                )
        else:
            lines.append("  none")

        lines.extend(("", "Cross-result audit:"))
        if not bundle.cross_results:
            lines.append("  none")
        else:
            for index, result in enumerate(bundle.cross_results, start=1):
                if index > 1:
                    lines.append("")
                lines.extend(self._render_result(index, result, bundle))

        lines.extend(("", *self._render_materiality(bundle)))
        lines.extend(
            (
                "",
                "Bounded non-claims:",
                "  QB-v0.1 does not establish:",
                *(f"    - {claim}" for claim in _QB_NON_CLAIMS),
            )
        )
        return "\n".join(lines)

    def _render_result(
        self,
        index: int,
        result: CrossRequirementResult,
        bundle: AssessmentReportBundle,
    ) -> list[str]:
        participant_ids = tuple(item.requirement_id for item in result.participants)
        lines = [
            f"  Result {index}",
            f"    result_id: {result.result_id.value}",
            f"    participants: {', '.join(participant_ids)}",
            f"    state: {result.state.value}",
            f"    relation_kind: {result.relation_kind.value}",
            f"    comparison_contract: {_descriptor(result.comparison_contract)}",
            f"    coverage_profile: {_descriptor(result.coverage_profile)}",
            "    observation_refs: "
            + ", ".join(_ref(item) for item in result.observation_refs),
        ]
        if result.comparison_key is None:
            lines.append("    comparison_key: none")
        else:
            lines.extend(
                (
                    "    comparison_key:",
                    f"      normalized_metric: {result.comparison_key.normalized_metric}",
                    f"      normalized_context: {result.comparison_key.normalized_context}",
                    f"      unit: {result.comparison_key.unit.value}",
                )
            )
        lines.extend(("    operands:", *self._render_operand("left", result.operands.left)))
        lines.extend(self._render_operand("right", result.operands.right))
        lines.append(
            "    unresolved_reasons: "
            + (
                ", ".join(item.value for item in result.unresolved_reasons)
                if result.unresolved_reasons
                else "none"
            )
        )
        lines.append(
            "    outside_reasons: "
            + (
                ", ".join(item.value for item in result.outside_reasons)
                if result.outside_reasons
                else "none"
            )
        )
        lines.extend(
            (
                f"    conflict_class: {_enum_or_none(result.conflict_class)}",
                f"    conflict_subtype: {_enum_or_none(result.conflict_subtype)}",
                "    non_claim_keys: "
                + ", ".join(item.value for item in result.non_claim_keys),
                "    diagnostic_refs: "
                + (
                    ", ".join(_ref(item) for item in result.diagnostic_refs)
                    if result.diagnostic_refs
                    else "none"
                ),
                "    resolved_evidence:",
            )
        )
        for ref, evidence in _resolved_evidence(bundle, result.evidence_refs):
            lines.extend(
                (
                    f"      - ref: {_ref(ref)}",
                    f"        owner_requirement: {ref.requirement_id}",
                    f"        evidence_id: {evidence.evidence_id}",
                    f"        text: {evidence.text}",
                    f"        range: [{evidence.start_offset},{evidence.end_offset})",
                    f"        feature_id: {evidence.feature_id.value}",
                    f"        detector_rule_id: {evidence.rule_id}",
                )
            )
        return lines

    @staticmethod
    def _render_operand(label: str, operand: ComparisonOperand) -> tuple[str, ...]:
        return (
            f"      {label}:",
            f"        observation_ref: {_ref(operand.observation_ref)}",
            f"        normalized_metric: {operand.normalized_metric or 'none'}",
            f"        normalized_context: {operand.normalized_context or 'none'}",
            f"        comparator: {_enum_or_none(operand.comparator)}",
            f"        inclusivity: {_enum_or_none(operand.inclusivity)}",
            f"        value: {operand.value if operand.value is not None else 'none'}",
            f"        unit: {_enum_or_none(operand.unit)}",
        )

    def _render_materiality(self, bundle: AssessmentReportBundle) -> list[str]:
        materiality = bundle.materiality
        lines = [
            "Materiality audit:",
            f"  materiality_rule: {_descriptor(materiality.materiality_rule)}",
            "  global_unresolved_diagnostic_count: "
            f"{materiality.global_unresolved_diagnostic_count}",
            f"  qb_material_count: {materiality.qb_material_count}",
            f"  qb_non_material_count: {materiality.qb_non_material_count}",
            "  audit_records:",
        ]
        if not materiality.audit_records:
            lines.append("    none")
            return lines

        for record in materiality.audit_records:
            lines.extend(self._render_materiality_record(record, bundle))
        return lines

    @staticmethod
    def _render_materiality_record(
        record: QbMaterialityAuditRecord,
        bundle: AssessmentReportBundle,
    ) -> list[str]:
        diagnostic = bundle.resolver.resolve_diagnostic(
            record.diagnostic_ref,
            snapshot_id=bundle.snapshot_id,
        )
        lines = [
            f"    - diagnostic_ref: {_ref(record.diagnostic_ref)}",
            f"      owner_requirement: {record.requirement_id}",
            f"      diagnostic_code: {record.diagnostic_code}",
            f"      diagnostic_rule_id: {record.diagnostic_rule_id}",
            f"      diagnostic_explanation: {diagnostic.explanation}",
            f"      disposition: {record.disposition.value}",
            f"      candidate_text: {record.candidate_text or 'none'}",
            "      candidate_range: "
            + (
                "none"
                if record.diagnostic_start_offset is None
                else f"[{record.diagnostic_start_offset},{record.diagnostic_end_offset})"
            ),
            "      gate_outcomes:",
        ]
        for field in fields(record.gate_outcomes):
            lines.append(
                f"        {field.name}: "
                f"{_bool_token(getattr(record.gate_outcomes, field.name))}"
            )

        if record.matched_context_evidence_ref is None:
            lines.append("      matched_context_evidence: none")
        else:
            ref = record.matched_context_evidence_ref
            evidence = bundle.resolver.resolve_evidence(
                ref,
                snapshot_id=bundle.snapshot_id,
            )
            lines.extend(
                (
                    f"      matched_context_evidence_ref: {_ref(ref)}",
                    f"      matched_context_text: {evidence.text}",
                    "      matched_context_range: "
                    f"[{evidence.start_offset},{evidence.end_offset})",
                )
            )
        lines.append(
            "      matched_allowlist_contract: "
            + (
                "none"
                if record.matched_allowlist_contract is None
                else _descriptor(record.matched_allowlist_contract)
            )
        )
        return lines


class UserCrossRequirementReporter:
    """Render the concise Ukrainian cross-requirement section."""

    def render(self, bundle: AssessmentReportBundle) -> str:
        if not isinstance(bundle, AssessmentReportBundle):
            raise TypeError("user cross reporter requires AssessmentReportBundle")

        assessment = bundle.specification_assessment.qb_consistency
        lines = ["Узгодженість вимог", f"Стан: {assessment.state.value}"]
        if assessment.state is QbConsistencyState.COMPUTED:
            lines.extend(
                (
                    f"Узгодженість у межах QB-v0.1: {assessment.value}",
                    "Значення стосується лише виконуваного обмеженого правила "
                    "QB-v0.1 і не означає універсальної узгодженості.",
                )
            )
        elif assessment.state is QbConsistencyState.UNKNOWN:
            lines.extend(
                (
                    "Узгодженість у межах QB-v0.1: UNKNOWN",
                    "Причини: " + self._aggregate_reasons(assessment.reasons),
                    "Числове значення не обчислено через невирішені QB-входи.",
                )
            )
        else:
            lines.extend(
                (
                    "Узгодженість у межах QB-v0.1: NOT_APPLICABLE",
                    "Причина: " + self._aggregate_reasons(assessment.reasons),
                    "За затвердженими умовами числове значення не застосовне.",
                )
            )

        if assessment.rconf_participant_ids:
            lines.append(
                "Підтверджені учасники конфліктів: "
                + ", ".join(assessment.rconf_participant_ids)
            )
        elif assessment.state is QbConsistencyState.UNKNOWN:
            lines.append("Підтверджені учасники конфліктів: немає")
        lines.append(f"R_conf complete: {_bool_token(assessment.rconf_complete)}")

        lines.append("")
        lines.append("Результати попарного аналізу:")
        if not bundle.cross_results:
            lines.append("  - Немає пар кількісних спостережень для відображення.")
        else:
            for result in bundle.cross_results:
                lines.extend(self._render_result(result, bundle))

        lines.extend(
            (
                "",
                "Межі QB-v0.1:",
                "  Оцінено лише підтримувані обмежені кількісні конструкції. "
                "Відсутність виявленого конфлікту не доводить універсальної "
                "семантичної узгодженості. COMPATIBLE_WITHIN_RULE стосується лише "
                "підтримуваної пари спостережень і правила та не є загальним "
                "твердженням про відсутність конфлікту.",
                "  Непідтримувана семантична еквівалентність не виводиться; не "
                "припускається еквівалентність за синонімами, термінологією, "
                "онтологіями, вбудовуваннями (embedding) чи нечітким зіставленням.",
                "  Не виводяться перетворення одиниць чи розмірнісна еквівалентність, "
                "а також перетин контекстів поза точною нормалізованою ідентичністю. "
                "Не додаються неявні предметні знання чи знання здорового глузду.",
                "  Не робиться загальних тверджень про логічну узгодженість поза "
                "підтримуваним обмеженим правилом, термінологічну або ресурсну "
                "узгодженість, дублювання, покриття чи простежуваність.",
                "  Не виводяться серйозність, ризик, імовірність, показник упевненості, "
                "пріоритет чи коригувальна дія; не робляться висновки про якість "
                "програмного продукту або ймовірність дефекту.",
                "  M_cons[QB-v0.1] не є об'єднаною оцінкою якості специфікації; "
                "повний M_cons без кваліфікатора лишається невиконуваним. UNKNOWN і "
                "NOT_APPLICABLE не є числовими значеннями й ніколи не означають нуль.",
            )
        )
        return "\n".join(lines)

    @staticmethod
    def _aggregate_reasons(reasons: tuple[QbConsistencyReason, ...]) -> str:
        return "; ".join(_USER_AGGREGATE_REASONS[item] for item in reasons)

    def _render_result(
        self,
        result: CrossRequirementResult,
        bundle: AssessmentReportBundle,
    ) -> list[str]:
        left_id, right_id = (item.requirement_id for item in result.participants)
        prefix = f"  - [{result.state.value}] {left_id} ↔ {right_id}: "
        if result.state is CrossResultState.CONFIRMED_CONFLICT:
            lines = [
                prefix
                + "підтримані кількісні межі несумісні в межах правила QB-v0.1.",
                "    Структуровані значення: "
                + self._user_operand(left_id, result.operands.left)
                + "; "
                + self._user_operand(right_id, result.operands.right)
                + ".",
                "    Джерельні фрагменти:",
            ]
            for ref, evidence in _resolved_evidence(bundle, result.evidence_refs):
                lines.append(f"      - {ref.requirement_id}: «{evidence.text}»")
            return lines

        if result.state is CrossResultState.COMPATIBLE_WITHIN_RULE:
            return [
                prefix
                + "підтримані кількісні обмеження спільно здійсненні лише в "
                "межах цього правила QB-v0.1."
            ]
        if result.state is CrossResultState.ASSESSMENT_UNRESOLVED:
            reasons = "; ".join(
                _USER_UNRESOLVED_REASONS[item.value]
                for item in result.unresolved_reasons
            )
            return [
                prefix
                + "пару не вдалося однозначно оцінити за QB-v0.1; "
                + reasons
                + "."
            ]

        reasons = "; ".join(
            _USER_OUTSIDE_REASONS[item.value] for item in result.outside_reasons
        )
        return [
            prefix
            + "пара перебуває поза межами чинного правила QB-v0.1; "
            + reasons
            + "."
        ]

    @staticmethod
    def _user_operand(requirement_id: str, operand: ComparisonOperand) -> str:
        return (
            f"{requirement_id} [метрика={operand.normalized_metric}; "
            f"контекст={operand.normalized_context}; "
            f"компаратор={_enum_or_none(operand.comparator)}; "
            f"включність={_enum_or_none(operand.inclusivity)}; "
            f"значення={operand.value if operand.value is not None else 'none'}; "
            f"одиниця={_enum_or_none(operand.unit)}]"
        )


__all__ = [
    "AssessmentReportBundle",
    "AuditCrossRequirementReporter",
    "UserCrossRequirementReporter",
]

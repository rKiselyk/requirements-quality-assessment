"""Approved record-based ConsoleReporter presentation boundary; no calculation."""

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Iterable

from .domain import (
    CharacteristicAssessment,
    CharacteristicAssessmentState,
    CharacteristicId,
    CharacteristicTrace,
    DetectionDiagnostic,
    DetectionProcessingStatus,
    Evidence,
    FeatureId,
    FeatureInputTrace,
    Finding,
    FindingKind,
    Requirement,
    RequirementAssessmentRecord,
    RequirementQualityProfile,
    SpecificationCharacteristicAggregate,
    SpecificationQualityProfile,
    TraceDecisionCode,
    TraceEffectCode,
)
from .domain.trace import outcome_for_feature

_CHARACTERISTIC_FIELDS = ("completeness", "verifiability", "unambiguity")

_COVERAGE_DISCLOSURES = (
    "Coverage is limited to the implemented bounded six-family extraction and "
    "approved C/V/U rules; it is not exhaustive Ukrainian linguistic or semantic analysis.",
    "NOT_DETECTED and completed absence mean no accepted observation under completed "
    "implemented rules; they do not establish universal semantic absence.",
    "C/V values, including low values or zero, are rule outputs and are not confirmed defects.",
    "U=1 means absence of the supported signal class, not proof of unique interpretation; "
    "U=1/2 means signal presence, not confirmed ambiguity; the current U rule never produces 0.",
    "FIND-U-VAGUE-001 is SIGNAL only; no current QUALITY_PROBLEM, severity, confidence, "
    "risk, or corrective action exists.",
    "R3 and F1-A are researcher-approved but unimplemented and are not claimed as runtime coverage.",
    "This is a multidimensional C/V/U profile, not a scalar requirement score or "
    "product-quality prediction.",
)

_DECISION_INTERPRETATIONS = {
    TraceDecisionCode.C_CRITERION_RATIO_COMPUTED: (
        "The exact Completeness value is the approved ratio of observed required feature "
        "families; repeated observations do not add weight."
    ),
    TraceDecisionCode.C_REQUIRED_INPUT_UNRESOLVED: (
        "Completeness is UNKNOWN because at least one required feature family is unresolved."
    ),
    TraceDecisionCode.V_FULL_ACCEPTANCE_TIER: (
        "Accepted acceptance-criterion evidence fixes the approved full Verifiability tier."
    ),
    TraceDecisionCode.V_PARTIAL_LOWER_TIER: (
        "With acceptance processing complete and absent, accepted quantitative or verification-"
        "method evidence fixes the approved lower Verifiability tier."
    ),
    TraceDecisionCode.V_COMPLETED_NO_EVIDENCE_TIER: (
        "All three Verifiability paths completed without an accepted observation, producing "
        "the approved zero tier without creating absence Evidence."
    ),
    TraceDecisionCode.V_MATERIAL_INPUT_UNRESOLVED: (
        "Verifiability is UNKNOWN because an unresolved material candidate could change its tier."
    ),
    TraceDecisionCode.U_SUPPORTED_SIGNAL_TIER: (
        "Accepted supported vague-term occurrence(s) produce the approved U=1/2 signal tier; "
        "the count is not cumulative."
    ),
    TraceDecisionCode.U_COMPLETED_SIGNAL_ABSENCE_TIER: (
        "The supported vague-term scan completed without an accepted occurrence, producing U=1 "
        "without creating absence Evidence."
    ),
    TraceDecisionCode.U_MATERIAL_INPUT_UNRESOLVED: (
        "Unambiguity is UNKNOWN because unresolved processing could still surface a supported signal."
    ),
    TraceDecisionCode.CHARACTERISTIC_NOT_APPLICABLE: (
        "The named governing rule established non-applicability."
    ),
}

_EFFECT_INTERPRETATIONS = {
    TraceEffectCode.C_PRESENT_1: "observed; contributes exactly 1 to the three-family ratio",
    TraceEffectCode.C_COMPLETED_ABSENCE_0: "completed absence; contributes exactly 0",
    TraceEffectCode.C_REQUIRED_UNRESOLVED: "unresolved required input; withholds the result",
    TraceEffectCode.V_SELECTS_FULL_TIER: "observed; selects the full tier",
    TraceEffectCode.V_SELECTS_LOWER_TIER: "observed; selects the lower tier",
    TraceEffectCode.V_PRESENT_NONSELECTING: "observed; accepted but does not select the final tier",
    TraceEffectCode.V_COMPLETED_ABSENCE: "completed absence; supplies no accepted V evidence",
    TraceEffectCode.V_UNRESOLVED_MATERIAL: "unresolved and material; resolution could change the tier",
    TraceEffectCode.V_UNRESOLVED_NON_MATERIAL: "unresolved but non-material",
    TraceEffectCode.U_SIGNAL_PRESENT: "observed; establishes the supported signal tier",
    TraceEffectCode.U_COMPLETED_SIGNAL_ABSENCE: "completed absence of the supported signal class",
    TraceEffectCode.U_UNRESOLVED_MATERIAL: (
        "unresolved and material; resolution could surface a supported signal"
    ),
}

_LegacyResult = tuple[Requirement, RequirementQualityProfile]


class ConsoleReporter:
    """Format already-computed quality results; performs no scoring or aggregation."""

    def render(
        self,
        requirement_results: Iterable[RequirementAssessmentRecord | _LegacyResult],
        specification_profile: SpecificationQualityProfile,
    ) -> str:
        materialized = tuple(requirement_results)

        sections = [
            self._render_record(item)
            if isinstance(item, RequirementAssessmentRecord)
            else self._render_requirement(*item)
            for item in materialized
        ]
        sections.append(
            self._render_specification_summary(len(materialized), specification_profile)
        )
        return "\n\n".join(sections)

    def _render_requirement(
        self, requirement: Requirement, profile: RequirementQualityProfile
    ) -> str:
        lines = [f"Requirement {requirement.id}", f"Text: {requirement.text}"]
        for field_name in _CHARACTERISTIC_FIELDS:
            lines.append("")
            lines.extend(
                self._render_characteristic_assessment(getattr(profile, field_name))
            )
        return "\n".join(lines)

    def _render_record(self, record: RequirementAssessmentRecord) -> str:
        result = record.extraction_result
        lines = [
            f"Requirement {result.requirement.id}",
            f"Text: {result.requirement.text}",
            "",
            "FORMAL RESULT",
        ]
        assessments = tuple(
            getattr(record.quality_profile, name) for name in _CHARACTERISTIC_FIELDS
        )
        for assessment, trace in zip(
            assessments, record.trace.characteristics, strict=True
        ):
            lines.append("")
            lines.extend(self._render_record_characteristic(record, assessment, trace))

        lines.extend(("", "HUMAN-READABLE INTERPRETATION"))
        for assessment, trace in zip(
            assessments, record.trace.characteristics, strict=True
        ):
            lines.append("")
            lines.extend(self._render_interpretation(record, assessment, trace))

        lines.extend(
            (
                "",
                f"Coverage disclosures ({record.trace.coverage_profile_id}):",
                *(f"  {index}. {text}" for index, text in enumerate(_COVERAGE_DISCLOSURES, 1)),
            )
        )
        return "\n".join(lines)

    def _render_record_characteristic(
        self,
        record: RequirementAssessmentRecord,
        assessment: CharacteristicAssessment,
        trace: CharacteristicTrace,
    ) -> list[str]:
        lines = [f"{assessment.characteristic_id.value.capitalize()}:"]
        lines.append(f"  state: {assessment.state.value}")
        lines.append(f"  value: {self._render_value(assessment.state, assessment.value)}")
        if assessment.state is CharacteristicAssessmentState.COMPUTED:
            lines.append(f"  assessment_rule_id: {assessment.assessment_rule_id}")
        lines.append(f"  governing_rule_id: {trace.governing_rule_id}")
        lines.append(f"  decision_code: {trace.decision_code.value}")
        lines.append("  feature_inputs:")
        for input_trace in trace.inputs:
            lines.extend(self._render_input(record, input_trace))
        lines.extend(self._render_resolved_findings(record, assessment.findings))
        lines.append(f"  assessment_explanation: {assessment.explanation}")
        return lines

    def _render_input(
        self, record: RequirementAssessmentRecord, input_trace: FeatureInputTrace
    ) -> list[str]:
        outcome = outcome_for_feature(record.extraction_result, input_trace.feature_id)
        applicability = (
            input_trace.applicability.value
            if input_trace.applicability is not None
            else "none"
        )
        lines = [
            f"    - feature_id: {input_trace.feature_id.value}",
            f"      applicability: {applicability}",
            f"      processing_status: {outcome.processing_status.value}",
            f"      detection_status: {outcome.status.value}",
            f"      effect_code: {input_trace.effect_code.value}",
        ]
        if input_trace.observation_indexes:
            lines.append("      accepted_observations:")
            for index in input_trace.observation_indexes:
                observation = outcome.observations[index]
                lines.extend(
                    (
                        f"        - observation_index: {index}",
                        f"          observation_type: {type(observation).__name__}",
                        f"          observation: {self._render_domain_value(observation)}",
                        "          resolved_evidence:",
                    )
                )
                for evidence in self._resolve_evidence(
                    record, observation.evidence_refs
                ):
                    lines.extend(self._render_evidence(evidence, indent="            "))
        else:
            lines.append("      accepted_observations: none")

        if input_trace.diagnostic_indexes:
            lines.append("      unresolved_diagnostics (not accepted Evidence):")
            for index in input_trace.diagnostic_indexes:
                diagnostic = outcome.diagnostics[index]
                lines.extend(
                    (
                        f"        - diagnostic_index: {index}",
                        f"          code: {diagnostic.code}",
                        f"          rule_id: {diagnostic.rule_id}",
                        f"          explanation: {diagnostic.explanation}",
                    )
                )
                if diagnostic.candidate_span is None:
                    lines.append("          candidate_span: none")
                else:
                    span = diagnostic.candidate_span
                    lines.extend(
                        (
                            "          candidate_span (not accepted Evidence):",
                            f"            text: {span.text}",
                            f"            range: [{span.start_offset},{span.end_offset})",
                        )
                    )
        else:
            lines.append("      unresolved_diagnostics: none")

        if (
            outcome.processing_status is DetectionProcessingStatus.COMPLETE
            and not outcome.observations
        ):
            lines.append(
                "      completed_absence: no accepted observation; no Evidence was created for absence"
            )
        return lines

    def _render_resolved_findings(
        self, record: RequirementAssessmentRecord, findings: tuple[Finding, ...]
    ) -> list[str]:
        if not findings:
            return ["  findings: none"]
        lines = ["  findings:"]
        for finding in findings:
            lines.extend(self._render_finding(finding))
            lines.append("      resolved_evidence:")
            for evidence in self._resolve_evidence(record, finding.evidence_refs):
                lines.extend(self._render_evidence(evidence, indent="        "))
        return lines

    @staticmethod
    def _resolve_evidence(
        record: RequirementAssessmentRecord, references: tuple[str, ...]
    ) -> tuple[Evidence, ...]:
        evidence_by_id = {
            item.evidence_id: item for item in record.extraction_result.evidence
        }
        return tuple(evidence_by_id[reference] for reference in references)

    @staticmethod
    def _render_evidence(evidence: Evidence, *, indent: str) -> list[str]:
        return [
            f"{indent}- evidence_id: {evidence.evidence_id}",
            f"{indent}  text: {evidence.text}",
            f"{indent}  range: [{evidence.start_offset},{evidence.end_offset})",
            f"{indent}  feature_id: {evidence.feature_id.value}",
            f"{indent}  detector_rule_id: {evidence.rule_id}",
        ]

    def _render_interpretation(
        self,
        record: RequirementAssessmentRecord,
        assessment: CharacteristicAssessment,
        trace: CharacteristicTrace,
    ) -> list[str]:
        lines = [
            f"{assessment.characteristic_id.value.capitalize()}:",
            f"  decision: {_DECISION_INTERPRETATIONS[trace.decision_code]}",
            f"  approved explanation: {assessment.explanation}",
            "  input interpretation:",
        ]
        for input_trace in trace.inputs:
            outcome = outcome_for_feature(record.extraction_result, input_trace.feature_id)
            interpretation = _EFFECT_INTERPRETATIONS[input_trace.effect_code]
            if input_trace.effect_code is TraceEffectCode.V_UNRESOLVED_NON_MATERIAL:
                if trace.decision_code is TraceDecisionCode.V_FULL_ACCEPTANCE_TIER:
                    interpretation += "; accepted acceptance evidence fixes the computed V=1 class"
                elif trace.decision_code is TraceDecisionCode.V_PARTIAL_LOWER_TIER:
                    interpretation += (
                        "; accepted lower-tier evidence fixes the computed V=1/2 class"
                    )
                elif trace.decision_code is TraceDecisionCode.V_MATERIAL_INPUT_UNRESOLVED:
                    interpretation += (
                        "; accepted lower-tier evidence establishes the provisional lower "
                        "tier, so this unresolved lower-tier input cannot improve it; the "
                        "final result remains UNKNOWN because unresolved acceptance may "
                        "change the tier to V=1"
                    )
            if (
                input_trace.effect_code is TraceEffectCode.V_PRESENT_NONSELECTING
                and trace.decision_code is TraceDecisionCode.V_MATERIAL_INPUT_UNRESOLVED
            ):
                interpretation += (
                    "; this accepted lower-tier evidence is provisional while the "
                    "material acceptance candidate remains unresolved"
                )
            if input_trace.observation_indexes and input_trace.diagnostic_indexes:
                interpretation += (
                    "; accepted Evidence remains observed while the separate diagnostic "
                    "candidate remains unresolved"
                )
            if not input_trace.observation_indexes and not input_trace.diagnostic_indexes:
                interpretation += (
                    "; this is no accepted observation under completed implemented rules, "
                    "not universal semantic absence, and no absence Evidence exists"
                )
            lines.append(f"    - {input_trace.feature_id.value}: {interpretation}.")
        if any(finding.kind is FindingKind.SIGNAL for finding in assessment.findings):
            lines.append(
                "  SIGNAL meaning: a supported indicator only; it is not a confirmed "
                "ambiguity, defect, QUALITY_PROBLEM, severity, confidence, or risk."
            )
        return lines

    def _render_domain_value(self, value) -> str:
        if isinstance(value, Enum):
            return value.value
        if value is None:
            return "none"
        if isinstance(value, tuple):
            return "[" + ", ".join(self._render_domain_value(item) for item in value) + "]"
        if is_dataclass(value):
            content = ", ".join(
                f"{field.name}={self._render_domain_value(getattr(value, field.name))}"
                for field in fields(value)
            )
            return f"{type(value).__name__}({content})"
        return str(value)

    def _render_characteristic_assessment(
        self, assessment: CharacteristicAssessment
    ) -> list[str]:
        lines = [f"{assessment.characteristic_id.value.capitalize()}:"]
        lines.append(f"  state: {assessment.state.value}")
        lines.append(f"  value: {self._render_value(assessment.state, assessment.value)}")
        if assessment.assessment_rule_id is not None:
            lines.append(f"  assessment_rule_id: {assessment.assessment_rule_id}")
        lines.extend(self._render_findings(assessment.findings))
        lines.append(f"  explanation: {assessment.explanation}")
        return lines

    def _render_findings(self, findings: tuple[Finding, ...]) -> list[str]:
        if not findings:
            return ["  findings: none"]
        lines = ["  findings:"]
        for finding in findings:
            lines.extend(self._render_finding(finding))
        return lines

    def _render_finding(self, finding: Finding) -> list[str]:
        lines = [
            f"    - kind: {finding.kind.value}",
            f"      code: {finding.code}",
            f"      rule_id: {finding.rule_id}",
        ]
        if finding.criterion_id is not None:
            lines.append(f"      criterion_id: {finding.criterion_id}")
        evidence_refs = ", ".join(finding.evidence_refs) if finding.evidence_refs else "none"
        lines.append(f"      evidence_refs: {evidence_refs}")
        lines.append(f"      explanation: {finding.explanation}")
        return lines

    def _render_specification_summary(
        self, analyzed_count: int, specification_profile: SpecificationQualityProfile
    ) -> str:
        lines = ["Specification summary", f"Analyzed requirements: {analyzed_count}"]
        for field_name in _CHARACTERISTIC_FIELDS:
            lines.append("")
            lines.extend(
                self._render_aggregate(getattr(specification_profile, field_name))
            )
        return "\n".join(lines)

    def _render_aggregate(
        self, aggregate: SpecificationCharacteristicAggregate
    ) -> list[str]:
        return [
            f"{aggregate.characteristic_id.value.capitalize()}:",
            f"  state: {aggregate.state.value}",
            f"  value: {self._render_value(aggregate.state, aggregate.value)}",
            f"  computed_count: {aggregate.computed_count}",
            f"  unknown_count: {aggregate.unknown_count}",
            f"  not_applicable_count: {aggregate.not_applicable_count}",
            f"  total_count: {aggregate.total_count}",
            f"  aggregation_rule_id: {aggregate.aggregation_rule_id}",
        ]

    def _render_value(self, state, value) -> str:
        if value is not None:
            return str(value)
        return state.value


_USER_CHARACTERISTICS = (
    ("completeness", "Повнота"),
    ("verifiability", "Перевірюваність"),
    ("unambiguity", "Однозначність"),
)

_USER_FEATURE_ACCUSATIVE = {
    FeatureId.CONDITION_CONTEXT: "умову/контекст",
    FeatureId.EXPECTED_RESULT: "очікуваний результат",
    FeatureId.ACCEPTANCE_CRITERION: "критерій приймання",
    FeatureId.QUANTITATIVE_CONSTRAINT: "кількісне обмеження",
    FeatureId.VERIFICATION_METHOD: "метод перевірки",
    FeatureId.VAGUE_TERM_OCCURRENCE: "підтримуваний SIGNAL",
}

_USER_FEATURE_GENITIVE = {
    FeatureId.CONDITION_CONTEXT: "умови/контексту",
    FeatureId.EXPECTED_RESULT: "очікуваного результату",
    FeatureId.ACCEPTANCE_CRITERION: "критерію приймання",
    FeatureId.QUANTITATIVE_CONSTRAINT: "кількісного обмеження",
    FeatureId.VERIFICATION_METHOD: "методу перевірки",
    FeatureId.VAGUE_TERM_OCCURRENCE: "підтримуваного SIGNAL",
}

_USER_CHARACTERISTIC_ACCUSATIVE = {
    CharacteristicId.COMPLETENESS: "Повноту",
    CharacteristicId.VERIFIABILITY: "Перевірюваність",
    CharacteristicId.UNAMBIGUITY: "Однозначність",
}

_MATERIAL_EFFECTS = frozenset(
    {
        TraceEffectCode.C_REQUIRED_UNRESOLVED,
        TraceEffectCode.V_UNRESOLVED_MATERIAL,
        TraceEffectCode.U_UNRESOLVED_MATERIAL,
    }
)

_USER_COVERAGE_DISCLOSURES = (
    "Покриття обмежене реалізованими правилами для шести сімейств ознак і C/V/U; "
    "це не вичерпний аналіз української мови або змісту вимог.",
    "NOT_DETECTED і завершена відсутність означають лише, що завершені реалізовані "
    "правила не прийняли спостереження; це не універсальна семантична відсутність.",
    "Значення C/V, зокрема низькі або нульові, є результатами правил, а не "
    "підтвердженими дефектами.",
    "U=1 означає відсутність підтримуваного класу SIGNAL, а не доказ єдиного "
    "тлумачення; U=1/2 означає наявність SIGNAL, а не підтверджену неоднозначність; "
    "чинне правило U не повертає 0.",
    "FIND-U-VAGUE-001 створює лише SIGNAL; чинна модель не створює QUALITY_PROBLEM, "
    "рівень серйозності, упевненість, ризик або коригувальну дію.",
    "R3 і F1-A затверджені дослідником, але не реалізовані й не належать до "
    "заявленого покриття виконання.",
    "Це багатовимірний профіль C/V/U, а не скалярна оцінка вимоги чи прогноз "
    "якості програмного продукту.",
)


class UserConsoleReporter:
    """Render the approved concise Ukrainian view over completed records."""

    def render(
        self,
        requirement_results: Iterable[RequirementAssessmentRecord],
        specification_profile: SpecificationQualityProfile,
    ) -> str:
        materialized = tuple(requirement_results)
        if any(not isinstance(item, RequirementAssessmentRecord) for item in materialized):
            raise TypeError("user view requires RequirementAssessmentRecord inputs")

        sections = ["Звіт про якість вимог"]
        sections.extend(self._render_record(record) for record in materialized)
        sections.append(
            self._render_specification_summary(len(materialized), specification_profile)
        )
        sections.append(self._render_disclosures())
        return "\n\n".join(sections)

    def _render_record(self, record: RequirementAssessmentRecord) -> str:
        requirement = record.extraction_result.requirement
        lines = [f"Вимога {requirement.id}", f"Текст: {requirement.text}", ""]

        for field_name, label in _USER_CHARACTERISTICS:
            assessment = getattr(record.quality_profile, field_name)
            lines.append(f"{label}: {self._render_value(assessment)}")

        lines.extend(("", "Чому така оцінка:"))
        for trace, (_, label) in zip(
            record.trace.characteristics, _USER_CHARACTERISTICS, strict=True
        ):
            lines.append(f"  - {label}: {self._render_explanation(record, trace)}")

        attention, shown_ranges = self._render_attention(record)
        if attention:
            lines.extend(("", "Звернути увагу:", *attention))

        source_basis = self._render_source_basis(record, shown_ranges)
        if source_basis:
            lines.extend(("", "Підстава в тексті:", *source_basis))

        return "\n".join(lines)

    def _render_explanation(
        self, record: RequirementAssessmentRecord, trace: CharacteristicTrace
    ) -> str:
        assessment = self._assessment_for(record, trace.characteristic_id)
        if assessment.state is CharacteristicAssessmentState.NOT_APPLICABLE:
            return (
                "Стан NOT_APPLICABLE встановлено чинним керівним правилом; "
                "числового значення немає."
            )
        if trace.characteristic_id is CharacteristicId.COMPLETENESS:
            return self._render_completeness_explanation(record, trace)
        if trace.characteristic_id is CharacteristicId.VERIFIABILITY:
            return self._render_verifiability_explanation(record, trace)
        return self._render_unambiguity_explanation(record, trace)

    def _render_completeness_explanation(
        self, record: RequirementAssessmentRecord, trace: CharacteristicTrace
    ) -> str:
        present: list[str] = []
        absent: list[str] = []
        unresolved: list[str] = []
        repeated = False
        for input_trace in trace.inputs:
            count = len(input_trace.observation_indexes)
            if count:
                present.append(self._detected_completeness_label(input_trace.feature_id, count))
                repeated = repeated or count > 1
            if input_trace.effect_code is TraceEffectCode.C_COMPLETED_ABSENCE_0:
                absent.append(_USER_FEATURE_ACCUSATIVE[input_trace.feature_id])
            elif input_trace.effect_code is TraceEffectCode.C_REQUIRED_UNRESOLVED:
                unresolved.append(_USER_FEATURE_ACCUSATIVE[input_trace.feature_id])

        if trace.decision_code is TraceDecisionCode.C_REQUIRED_INPUT_UNRESOLVED:
            return (
                f"Виявлено: {self._join_ukrainian(present)}; за реалізованими "
                f"правилами не виявлено: {self._join_ukrainian(absent)}; "
                f"невирішено: {self._join_ukrainian(unresolved)}. Через невирішений "
                "обов'язковий складник результат UNKNOWN."
            )

        repeated_suffix = (
            ", тому повторні спостереження одного складника не збільшують оцінку"
            if repeated
            else ""
        )
        return (
            f"Виявлено: {self._join_ukrainian(present)}; за реалізованими правилами "
            f"не виявлено: {self._join_ukrainian(absent)}. Кожен із трьох "
            f"складників враховується один раз{repeated_suffix}."
        )

    def _render_verifiability_explanation(
        self, record: RequirementAssessmentRecord, trace: CharacteristicTrace
    ) -> str:
        if trace.decision_code is TraceDecisionCode.V_FULL_ACCEPTANCE_TIER:
            lower_has_content = any(
                input_trace.observation_indexes or input_trace.diagnostic_indexes
                for input_trace in trace.inputs[1:]
            )
            suffix = (
                " Інші прийняті або невирішені нижчі шляхи не змінюють цього рівня."
                if lower_has_content
                else ""
            )
            return (
                "Виявлено прийнятий критерій приймання, тому застосовано повний "
                f"затверджений рівень.{suffix}"
            )

        if trace.decision_code is TraceDecisionCode.V_PARTIAL_LOWER_TIER:
            accepted = [
                _USER_FEATURE_ACCUSATIVE[input_trace.feature_id]
                for input_trace in trace.inputs[1:]
                if input_trace.observation_indexes
            ]
            return (
                "Критерій приймання завершено без прийнятого спостереження; "
                f"виявлено {self._join_ukrainian(accepted)}, тому застосовано "
                "нижчий затверджений рівень."
            )

        if trace.decision_code is TraceDecisionCode.V_COMPLETED_NO_EVIDENCE_TIER:
            return (
                "Критерій приймання, кількісне обмеження та метод перевірки "
                "завершено без прийнятих спостережень. Це завершена відсутність "
                "за реалізованими правилами, а не підтверджений дефект."
            )

        present: list[str] = []
        absent: list[str] = []
        unresolved: list[str] = []
        for input_trace in trace.inputs:
            if input_trace.observation_indexes:
                present.append(_USER_FEATURE_ACCUSATIVE[input_trace.feature_id])
            if input_trace.effect_code is TraceEffectCode.V_COMPLETED_ABSENCE:
                absent.append(_USER_FEATURE_ACCUSATIVE[input_trace.feature_id])
            elif input_trace.effect_code is TraceEffectCode.V_UNRESOLVED_MATERIAL:
                unresolved.append(_USER_FEATURE_ACCUSATIVE[input_trace.feature_id])
        return (
            f"Виявлено: {self._join_ukrainian(present)}; за реалізованими правилами "
            f"не виявлено: {self._join_ukrainian(absent)}; невирішено: "
            f"{self._join_ukrainian(unresolved)}. Невирішений істотний кандидат "
            "може змінити рівень, тому результат UNKNOWN."
        )

    def _render_unambiguity_explanation(
        self, record: RequirementAssessmentRecord, trace: CharacteristicTrace
    ) -> str:
        outcome = outcome_for_feature(
            record.extraction_result, FeatureId.VAGUE_TERM_OCCURRENCE
        )
        if trace.decision_code is TraceDecisionCode.U_SUPPORTED_SIGNAL_TIER:
            count = len(outcome.observations)
            agreement = "підтримуваний" if count == 1 else "підтримуваних"
            return (
                f"Виявлено {count} {agreement} SIGNAL, тому значення 1/2; кількість "
                "сигналів не накопичує оцінку. SIGNAL є потенційним індикатором, "
                "а не підтвердженою неоднозначністю чи дефектом."
            )
        if trace.decision_code is TraceDecisionCode.U_COMPLETED_SIGNAL_ABSENCE_TIER:
            return (
                "Пошук підтримуваного класу SIGNAL завершено без прийнятих "
                "входжень, тому значення 1. Це не доводить єдиність тлумачення."
            )
        return (
            "Пошук підтримуваного класу SIGNAL не завершено: невирішена обробка "
            "ще може виявити індикатор. Тому результат UNKNOWN."
        )

    def _render_attention(
        self, record: RequirementAssessmentRecord
    ) -> tuple[list[str], set[tuple[int, int]]]:
        evidence_by_id = {
            evidence.evidence_id: evidence
            for evidence in record.extraction_result.evidence
        }
        items: list[tuple[int, int, str, set[tuple[int, int]]]] = []
        sequence = 0

        unambiguity = record.quality_profile.unambiguity
        for finding in unambiguity.findings:
            if finding.kind is not FindingKind.SIGNAL:
                continue
            evidence = tuple(evidence_by_id[ref] for ref in finding.evidence_refs)
            ranges = {(item.start_offset, item.end_offset) for item in evidence}
            start = min(item.start_offset for item in evidence)
            text = (
                f"SIGNAL: {self._quote_evidence(evidence)} — підтримуваний індикатор "
                "потенційної неоднозначності, а не підтверджений дефект."
            )
            items.append((start, sequence, text, ranges))
            sequence += 1

        diagnostics: dict[
            tuple[FeatureId, int],
            tuple[DetectionDiagnostic, FeatureId, list[CharacteristicId]],
        ] = {}
        for trace in record.trace.characteristics:
            for input_trace in trace.inputs:
                if input_trace.effect_code not in _MATERIAL_EFFECTS:
                    continue
                outcome = outcome_for_feature(
                    record.extraction_result, input_trace.feature_id
                )
                for index in input_trace.diagnostic_indexes:
                    key = (input_trace.feature_id, index)
                    diagnostic = outcome.diagnostics[index]
                    if key not in diagnostics:
                        diagnostics[key] = (
                            diagnostic,
                            input_trace.feature_id,
                            [trace.characteristic_id],
                        )
                    elif trace.characteristic_id not in diagnostics[key][2]:
                        diagnostics[key][2].append(trace.characteristic_id)

        requirement_text_length = len(record.extraction_result.requirement.text)
        for diagnostic, feature_id, characteristic_ids in diagnostics.values():
            affected = self._join_affected(characteristic_ids)
            span = diagnostic.candidate_span
            ranges: set[tuple[int, int]] = set()
            if span is None:
                start = requirement_text_length + 1
                text = (
                    "Невирішений кандидат без окремого джерельного фрагмента "
                    "(не прийняте Evidence). Він може змінити "
                    f"{affected}, тому відповідний результат лишається UNKNOWN."
                )
            else:
                start = span.start_offset
                ranges.add((span.start_offset, span.end_offset))
                same_range_evidence = tuple(
                    evidence
                    for evidence in record.extraction_result.evidence
                    if evidence.feature_id is not feature_id
                    and evidence.start_offset == span.start_offset
                    and evidence.end_offset == span.end_offset
                )
                if same_range_evidence:
                    accepted_features = self._join_ukrainian(
                        list(
                            dict.fromkeys(
                                _USER_FEATURE_GENITIVE[evidence.feature_id]
                                for evidence in same_range_evidence
                            )
                        )
                    )
                    text = (
                        f"Невирішений кандидат {_USER_FEATURE_GENITIVE[feature_id]} "
                        f"(не прийняте Evidence): «{span.text}». Цей самий фрагмент "
                        f"окремо прийнято як Evidence {accepted_features}; невирішений "
                        f"кандидат може змінити {affected}, тому відповідний результат "
                        "лишається UNKNOWN."
                    )
                else:
                    text = (
                        f"Невирішений кандидат (не прийняте Evidence): «{span.text}». "
                        f"Він може змінити {affected}, тому відповідний результат "
                        "лишається UNKNOWN."
                    )
            items.append((start, sequence, text, ranges))
            sequence += 1

        items.sort(key=lambda item: (item[0], item[1]))
        shown_ranges = {source_range for item in items for source_range in item[3]}
        return [f"  - {item[2]}" for item in items], shown_ranges

    def _render_source_basis(
        self,
        record: RequirementAssessmentRecord,
        shown_ranges: set[tuple[int, int]],
    ) -> list[str]:
        evidence_by_id = {
            evidence.evidence_id: evidence
            for evidence in record.extraction_result.evidence
        }
        seen_ranges = set(shown_ranges)
        lines: list[str] = []

        completeness_trace = record.trace.characteristics[0]
        for input_trace in completeness_trace.inputs:
            if len(input_trace.observation_indexes) < 2:
                continue
            outcome = outcome_for_feature(record.extraction_result, input_trace.feature_id)
            for ordinal, observation_index in enumerate(
                input_trace.observation_indexes, start=1
            ):
                observation = outcome.observations[observation_index]
                evidence = tuple(
                    evidence_by_id[reference]
                    for reference in observation.evidence_refs
                    if (
                        evidence_by_id[reference].start_offset,
                        evidence_by_id[reference].end_offset,
                    )
                    not in seen_ranges
                )
                if not evidence:
                    continue
                prefix = self._ordinal_prefix(ordinal)
                lines.append(
                    f"  - {prefix} прийняте спостереження "
                    f"{_USER_FEATURE_GENITIVE[input_trace.feature_id]}: "
                    f"{self._quote_evidence(evidence)}."
                )
                seen_ranges.update(
                    (item.start_offset, item.end_offset) for item in evidence
                )

        verifiability_trace = record.trace.characteristics[1]
        selecting_effects = {
            TraceEffectCode.V_SELECTS_FULL_TIER,
            TraceEffectCode.V_SELECTS_LOWER_TIER,
        }
        for input_trace in verifiability_trace.inputs:
            if input_trace.effect_code not in selecting_effects:
                continue
            outcome = outcome_for_feature(record.extraction_result, input_trace.feature_id)
            for observation_index in input_trace.observation_indexes:
                observation = outcome.observations[observation_index]
                evidence = tuple(
                    evidence_by_id[reference]
                    for reference in observation.evidence_refs
                    if (
                        evidence_by_id[reference].start_offset,
                        evidence_by_id[reference].end_offset,
                    )
                    not in seen_ranges
                )
                if not evidence:
                    continue
                lines.append(
                    f"  - Прийняте Evidence "
                    f"{_USER_FEATURE_GENITIVE[input_trace.feature_id]}: "
                    f"{self._quote_evidence(evidence)}."
                )
                seen_ranges.update(
                    (item.start_offset, item.end_offset) for item in evidence
                )

        return lines

    def _render_specification_summary(
        self, analyzed_count: int, specification_profile: SpecificationQualityProfile
    ) -> str:
        lines = ["Підсумок специфікації", f"Вимог: {analyzed_count}"]
        for field_name, label in _USER_CHARACTERISTICS:
            aggregate = getattr(specification_profile, field_name)
            value = aggregate.value if aggregate.value is not None else aggregate.state.value
            lines.append(
                f"{label}: {value} (обчислено: {aggregate.computed_count}; "
                f"UNKNOWN: {aggregate.unknown_count}; NOT_APPLICABLE: "
                f"{aggregate.not_applicable_count}; усього: {aggregate.total_count})"
            )
        return "\n".join(lines)

    @staticmethod
    def _render_disclosures() -> str:
        return "\n".join(
            [
                "Межі звіту",
                *(
                    f"  {index}. {disclosure}"
                    for index, disclosure in enumerate(_USER_COVERAGE_DISCLOSURES, 1)
                ),
            ]
        )

    @staticmethod
    def _assessment_for(
        record: RequirementAssessmentRecord, characteristic_id: CharacteristicId
    ) -> CharacteristicAssessment:
        return {
            CharacteristicId.COMPLETENESS: record.quality_profile.completeness,
            CharacteristicId.VERIFIABILITY: record.quality_profile.verifiability,
            CharacteristicId.UNAMBIGUITY: record.quality_profile.unambiguity,
        }[characteristic_id]

    @staticmethod
    def _render_value(assessment: CharacteristicAssessment) -> str:
        if assessment.value is not None:
            return str(assessment.value)
        return assessment.state.value

    @staticmethod
    def _detected_completeness_label(feature_id: FeatureId, count: int) -> str:
        if count == 1:
            return _USER_FEATURE_ACCUSATIVE[feature_id]
        if feature_id is FeatureId.EXPECTED_RESULT and count == 2:
            return "два очікувані результати"
        return f"{count} спостереження {_USER_FEATURE_GENITIVE[feature_id]}"

    @staticmethod
    def _join_ukrainian(items: list[str]) -> str:
        if not items:
            return "немає"
        if len(items) == 1:
            return items[0]
        return ", ".join(items[:-1]) + " і " + items[-1]

    @staticmethod
    def _join_affected(characteristic_ids: list[CharacteristicId]) -> str:
        labels = [
            _USER_CHARACTERISTIC_ACCUSATIVE[characteristic_id]
            for characteristic_id in characteristic_ids
        ]
        if len(labels) == 1:
            return labels[0]
        return ", ".join(labels[:-1]) + " й " + labels[-1]

    @staticmethod
    def _quote_evidence(evidence: tuple[Evidence, ...]) -> str:
        return " + ".join(f"«{item.text}»" for item in evidence)

    @staticmethod
    def _ordinal_prefix(ordinal: int) -> str:
        return {1: "Перше", 2: "Друге", 3: "Третє"}.get(
            ordinal, f"{ordinal}-те"
        )

"""Approved record-based ConsoleReporter presentation boundary; no calculation."""

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Iterable

from .domain import (
    CharacteristicAssessment,
    CharacteristicAssessmentState,
    CharacteristicTrace,
    DetectionProcessingStatus,
    Evidence,
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

"""Section 19 (MVP-10A) approved ConsoleReporter presentation boundary; no calculation."""

from typing import Iterable

from .domain import (
    CharacteristicAssessment,
    Finding,
    Requirement,
    RequirementQualityProfile,
    SpecificationCharacteristicAggregate,
    SpecificationQualityProfile,
)

_CHARACTERISTIC_FIELDS = ("completeness", "verifiability", "unambiguity")


class ConsoleReporter:
    """Format already-computed quality results; performs no scoring or aggregation."""

    def render(
        self,
        requirement_results: Iterable[tuple[Requirement, RequirementQualityProfile]],
        specification_profile: SpecificationQualityProfile,
    ) -> str:
        materialized = tuple(requirement_results)

        sections = [
            self._render_requirement(requirement, profile)
            for requirement, profile in materialized
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

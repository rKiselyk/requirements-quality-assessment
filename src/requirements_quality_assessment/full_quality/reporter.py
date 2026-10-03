"""Calculation-free USER and AUDIT projections for TC-01 full profiles."""

from .domain import (
    ExternalAssessmentState,
    FullRequirementQualityProfile,
    PropertyAssessmentOrigin,
    RequirementPropertyAssessment,
    RequirementQualityPropertyId,
)


_USER_LABELS = {
    RequirementQualityPropertyId.COMPLETENESS: "Completeness",
    RequirementQualityPropertyId.VERIFIABILITY: "Verifiability",
    RequirementQualityPropertyId.UNAMBIGUITY: "Unambiguity",
    RequirementQualityPropertyId.SINGULARITY: "Singularity / Atomicity",
    RequirementQualityPropertyId.PRESENTATION_CONFORMANCE: "Presentation Conformance",
    RequirementQualityPropertyId.CORRECTNESS: "Correctness",
    RequirementQualityPropertyId.FEASIBILITY: "Feasibility",
    RequirementQualityPropertyId.NECESSITY: "Necessity",
    RequirementQualityPropertyId.RELEVANCE: "Relevance",
}


class UserFullRequirementQualityReporter:
    def render(self, profile: FullRequirementQualityProfile) -> str:
        if not isinstance(profile, FullRequirementQualityProfile):
            raise TypeError("profile must be a FullRequirementQualityProfile")
        automatic = tuple(
            item
            for item in profile.properties
            if item.origin is PropertyAssessmentOrigin.AUTOMATIC
        )
        external = tuple(
            item
            for item in profile.properties
            if item.origin is PropertyAssessmentOrigin.EXTERNAL_EXPERT
        )
        lines = [
            f"Full requirement-quality profile: {profile.requirement_ref.requirement_id}",
            "Automatic properties (authoritative C/V/U)",
            *(self._line(item) for item in automatic),
            "External/expert properties",
            *(self._line(item) for item in external),
            "No integrated scalar requirement-quality score is calculated.",
        ]
        return "\n".join(lines)

    @staticmethod
    def _line(item: RequirementPropertyAssessment) -> str:
        label = _USER_LABELS[item.property_id]
        if item.origin is PropertyAssessmentOrigin.AUTOMATIC:
            assessment = item.automatic_assessment
            assert assessment is not None
            rendered = assessment.value if assessment.value is not None else assessment.state.value
        else:
            assessment = item.external_assessment
            assert assessment is not None
            rendered = (
                assessment.judgment.judgment_id
                if assessment.state is ExternalAssessmentState.AVAILABLE
                else assessment.state.value
            )
        return f"  - {label} [{item.origin.value}]: {rendered}"


class AuditFullRequirementQualityReporter:
    def render(self, profile: FullRequirementQualityProfile) -> str:
        if not isinstance(profile, FullRequirementQualityProfile):
            raise TypeError("profile must be a FullRequirementQualityProfile")
        lines = [
            "FULL NINE-PROPERTY REQUIREMENT-QUALITY PROFILE",
            f"requirement_id: {profile.requirement_ref.requirement_id}",
            f"source_line: {profile.requirement_ref.source_line}",
            f"artifact_id: {profile.artifact_ref.artifact_id}",
            f"artifact_version: {profile.artifact_ref.artifact_version}",
            f"assessment_id: {profile.assessment_ref.assessment_id}",
            f"assessment_version: {profile.assessment_ref.assessment_version}",
            "properties:",
        ]
        for item in profile.properties:
            lines.extend(self._property_lines(item))
        lines.append(
            "non_claim: no integrated scalar requirement-quality score is defined"
        )
        return "\n".join(lines)

    @staticmethod
    def _property_lines(item: RequirementPropertyAssessment) -> list[str]:
        lines = [
            f"  - property_id: {item.property_id.value}",
            f"    origin: {item.origin.value}",
        ]
        if item.origin is PropertyAssessmentOrigin.AUTOMATIC:
            assessment = item.automatic_assessment
            trace = item.automatic_trace
            assert assessment is not None and trace is not None
            value = assessment.value if assessment.value is not None else assessment.state.value
            finding_ids = ", ".join(item.finding_id for item in assessment.findings) or "none"
            lines.extend(
                (
                    f"    state: {assessment.state.value}",
                    f"    value: {value}",
                    f"    assessment_rule_id: {assessment.assessment_rule_id or 'none'}",
                    f"    governing_rule_id: {trace.governing_rule_id}",
                    f"    decision_code: {trace.decision_code.value}",
                    f"    finding_ids: {finding_ids}",
                    f"    explanation: {assessment.explanation}",
                )
            )
            return lines

        assessment = item.external_assessment
        assert assessment is not None
        provenance = assessment.provenance
        judgment = assessment.judgment.judgment_id if assessment.judgment else "none"
        rule = provenance.assessment_rule_ref
        rule_version = rule.explicit_version or rule.version_authority.value
        lines.extend(
            (
                f"    state: {assessment.state.value}",
                f"    judgment: {judgment}",
                f"    source_id: {provenance.source_ref.source_id}",
                f"    source_version: {provenance.source_ref.source_version}",
                f"    provenance_requirement_id: {provenance.requirement_ref.requirement_id}",
                f"    provenance_artifact_id: {provenance.artifact_ref.artifact_id}",
                f"    provenance_artifact_version: {provenance.artifact_ref.artifact_version}",
                f"    assessment_contract_id: {provenance.assessment_contract_ref.contract_id}",
                f"    assessment_contract_version: {provenance.assessment_contract_ref.version}",
                f"    assessment_rule_id: {rule.rule_id}",
                f"    assessment_rule_version: {rule_version}",
                f"    explanation: {assessment.explanation}",
            )
        )
        return lines

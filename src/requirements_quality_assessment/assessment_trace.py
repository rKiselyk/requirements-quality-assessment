"""Construct the approved SRM-10 trace from existing extraction/profile values."""

from .domain import (
    CharacteristicId,
    CharacteristicTrace,
    CriterionApplicability,
    FeatureInputTrace,
    RequirementAssessmentRecord,
    RequirementAssessmentTrace,
    RequirementExtractionResult,
    RequirementQualityProfile,
)
from .domain.trace import (
    _INPUT_FAMILIES,
    _RULE_IDS,
    expected_characteristic_semantics,
    outcome_for_feature,
)


class RequirementAssessmentTraceBuilder:
    """Build local tuple-index trace references without copying source data."""

    def build(
        self,
        result: RequirementExtractionResult,
        profile: RequirementQualityProfile,
    ) -> RequirementAssessmentRecord:
        characteristics = tuple(
            self._characteristic_trace(result, profile, characteristic_id)
            for characteristic_id in CharacteristicId
        )
        trace = RequirementAssessmentTrace(
            requirement_id=result.requirement.id,
            characteristics=characteristics,
        )
        return RequirementAssessmentRecord(result, profile, trace)

    @staticmethod
    def _characteristic_trace(
        result: RequirementExtractionResult,
        profile: RequirementQualityProfile,
        characteristic_id: CharacteristicId,
    ) -> CharacteristicTrace:
        feature_ids = _INPUT_FAMILIES[characteristic_id]
        outcomes = tuple(outcome_for_feature(result, feature_id) for feature_id in feature_ids)
        decision_code, effect_codes, _, _ = expected_characteristic_semantics(
            characteristic_id, outcomes
        )
        assessment = {
            CharacteristicId.COMPLETENESS: profile.completeness,
            CharacteristicId.VERIFIABILITY: profile.verifiability,
            CharacteristicId.UNAMBIGUITY: profile.unambiguity,
        }[characteristic_id]
        inputs = tuple(
            FeatureInputTrace(
                feature_id=feature_id,
                applicability=(
                    CriterionApplicability.APPLICABLE
                    if characteristic_id is CharacteristicId.COMPLETENESS
                    else None
                ),
                observation_indexes=tuple(range(len(outcome.observations))),
                diagnostic_indexes=tuple(range(len(outcome.diagnostics))),
                effect_code=effect_code,
            )
            for feature_id, outcome, effect_code in zip(
                feature_ids, outcomes, effect_codes, strict=True
            )
        )
        return CharacteristicTrace(
            characteristic_id=characteristic_id,
            governing_rule_id=_RULE_IDS[characteristic_id],
            decision_code=decision_code,
            inputs=inputs,
            finding_refs=tuple(finding.finding_id for finding in assessment.findings),
        )

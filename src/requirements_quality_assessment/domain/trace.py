"""SRM-10 immutable assessment-trace contracts and joint validation."""

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from .assessment import (
    CharacteristicAssessment,
    CharacteristicAssessmentState,
    CharacteristicId,
    FindingKind,
)
from .core import CriterionApplicability, FeatureId
from .detection import DetectionProcessingStatus, FeatureDetectionOutcome
from .extraction import RequirementExtractionResult, _accepted_evidence_refs
from .profile import RequirementQualityProfile


COVERAGE_PROFILE_ID = "MVP-V0.1-BOUNDED-CVU-001"


class TraceDecisionCode(str, Enum):
    C_CRITERION_RATIO_COMPUTED = "C_CRITERION_RATIO_COMPUTED"
    C_REQUIRED_INPUT_UNRESOLVED = "C_REQUIRED_INPUT_UNRESOLVED"
    V_FULL_ACCEPTANCE_TIER = "V_FULL_ACCEPTANCE_TIER"
    V_PARTIAL_LOWER_TIER = "V_PARTIAL_LOWER_TIER"
    V_COMPLETED_NO_EVIDENCE_TIER = "V_COMPLETED_NO_EVIDENCE_TIER"
    V_MATERIAL_INPUT_UNRESOLVED = "V_MATERIAL_INPUT_UNRESOLVED"
    U_SUPPORTED_SIGNAL_TIER = "U_SUPPORTED_SIGNAL_TIER"
    U_COMPLETED_SIGNAL_ABSENCE_TIER = "U_COMPLETED_SIGNAL_ABSENCE_TIER"
    U_MATERIAL_INPUT_UNRESOLVED = "U_MATERIAL_INPUT_UNRESOLVED"
    CHARACTERISTIC_NOT_APPLICABLE = "CHARACTERISTIC_NOT_APPLICABLE"


class TraceEffectCode(str, Enum):
    C_PRESENT_1 = "C_PRESENT_1"
    C_COMPLETED_ABSENCE_0 = "C_COMPLETED_ABSENCE_0"
    C_REQUIRED_UNRESOLVED = "C_REQUIRED_UNRESOLVED"
    V_SELECTS_FULL_TIER = "V_SELECTS_FULL_TIER"
    V_SELECTS_LOWER_TIER = "V_SELECTS_LOWER_TIER"
    V_PRESENT_NONSELECTING = "V_PRESENT_NONSELECTING"
    V_COMPLETED_ABSENCE = "V_COMPLETED_ABSENCE"
    V_UNRESOLVED_MATERIAL = "V_UNRESOLVED_MATERIAL"
    V_UNRESOLVED_NON_MATERIAL = "V_UNRESOLVED_NON_MATERIAL"
    U_SIGNAL_PRESENT = "U_SIGNAL_PRESENT"
    U_COMPLETED_SIGNAL_ABSENCE = "U_COMPLETED_SIGNAL_ABSENCE"
    U_UNRESOLVED_MATERIAL = "U_UNRESOLVED_MATERIAL"


def _validate_indexes(name: str, indexes: tuple[int, ...]) -> None:
    if not isinstance(indexes, tuple) or any(type(index) is not int for index in indexes):
        raise TypeError(f"{name} must be a tuple of integers")
    if any(index < 0 for index in indexes):
        raise ValueError(f"{name} cannot contain negative indexes")
    if indexes != tuple(sorted(set(indexes))):
        raise ValueError(f"{name} must contain unique ascending indexes")


@dataclass(frozen=True, slots=True)
class FeatureInputTrace:
    feature_id: FeatureId
    applicability: CriterionApplicability | None
    observation_indexes: tuple[int, ...]
    diagnostic_indexes: tuple[int, ...]
    effect_code: TraceEffectCode

    def __post_init__(self) -> None:
        if not isinstance(self.feature_id, FeatureId):
            raise TypeError("feature_id must be an approved FeatureId")
        if self.applicability is not None and not isinstance(
            self.applicability, CriterionApplicability
        ):
            raise TypeError("applicability must be CriterionApplicability or None")
        _validate_indexes("observation_indexes", self.observation_indexes)
        _validate_indexes("diagnostic_indexes", self.diagnostic_indexes)
        if not isinstance(self.effect_code, TraceEffectCode):
            raise TypeError("effect_code must be an approved TraceEffectCode")


@dataclass(frozen=True, slots=True)
class CharacteristicTrace:
    characteristic_id: CharacteristicId
    governing_rule_id: str
    decision_code: TraceDecisionCode
    inputs: tuple[FeatureInputTrace, ...]
    finding_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.characteristic_id, CharacteristicId):
            raise TypeError("characteristic_id must be an approved CharacteristicId")
        if not isinstance(self.governing_rule_id, str) or not self.governing_rule_id:
            raise ValueError("governing_rule_id must be a non-empty string")
        if not isinstance(self.decision_code, TraceDecisionCode):
            raise TypeError("decision_code must be an approved TraceDecisionCode")
        if not isinstance(self.inputs, tuple) or any(
            not isinstance(item, FeatureInputTrace) for item in self.inputs
        ):
            raise TypeError("inputs must be a tuple of FeatureInputTrace")
        if not isinstance(self.finding_refs, tuple) or any(
            not isinstance(item, str) for item in self.finding_refs
        ):
            raise TypeError("finding_refs must be a tuple of strings")


@dataclass(frozen=True, slots=True)
class RequirementAssessmentTrace:
    requirement_id: str
    characteristics: tuple[CharacteristicTrace, ...]
    coverage_profile_id: str = COVERAGE_PROFILE_ID

    def __post_init__(self) -> None:
        if not isinstance(self.requirement_id, str) or not self.requirement_id:
            raise ValueError("requirement_id must be a non-empty string")
        if not isinstance(self.characteristics, tuple) or any(
            not isinstance(item, CharacteristicTrace) for item in self.characteristics
        ):
            raise TypeError("characteristics must be a tuple of CharacteristicTrace")
        if self.coverage_profile_id != COVERAGE_PROFILE_ID:
            raise ValueError(f"coverage_profile_id must be {COVERAGE_PROFILE_ID!r}")


@dataclass(frozen=True, slots=True)
class RequirementAssessmentRecord:
    extraction_result: RequirementExtractionResult
    quality_profile: RequirementQualityProfile
    trace: RequirementAssessmentTrace

    def __post_init__(self) -> None:
        if not isinstance(self.extraction_result, RequirementExtractionResult):
            raise TypeError("extraction_result must be a RequirementExtractionResult")
        if not isinstance(self.quality_profile, RequirementQualityProfile):
            raise TypeError("quality_profile must be a RequirementQualityProfile")
        if not isinstance(self.trace, RequirementAssessmentTrace):
            raise TypeError("trace must be a RequirementAssessmentTrace")
        _validate_record(self.extraction_result, self.quality_profile, self.trace)


_RULE_IDS = {
    CharacteristicId.COMPLETENESS: "CALC-C-MVP-001",
    CharacteristicId.VERIFIABILITY: "CALC-V-MVP-001",
    CharacteristicId.UNAMBIGUITY: "CALC-U-MVP-001",
}

_INPUT_FAMILIES = {
    CharacteristicId.COMPLETENESS: (
        FeatureId.CONDITION_CONTEXT,
        FeatureId.EXPECTED_RESULT,
        FeatureId.ACCEPTANCE_CRITERION,
    ),
    CharacteristicId.VERIFIABILITY: (
        FeatureId.ACCEPTANCE_CRITERION,
        FeatureId.QUANTITATIVE_CONSTRAINT,
        FeatureId.VERIFICATION_METHOD,
    ),
    CharacteristicId.UNAMBIGUITY: (FeatureId.VAGUE_TERM_OCCURRENCE,),
}


def outcome_for_feature(
    result: RequirementExtractionResult, feature_id: FeatureId
) -> FeatureDetectionOutcome:
    """Return the one approved outcome selected by a FeatureId."""
    attribute = {
        FeatureId.CONDITION_CONTEXT: "condition_contexts",
        FeatureId.EXPECTED_RESULT: "expected_results",
        FeatureId.ACCEPTANCE_CRITERION: "acceptance_criteria",
        FeatureId.QUANTITATIVE_CONSTRAINT: "quantitative_constraints",
        FeatureId.VERIFICATION_METHOD: "verification_methods",
        FeatureId.VAGUE_TERM_OCCURRENCE: "vague_term_occurrences",
    }[feature_id]
    return getattr(result.features, attribute)


def _assessment_for(
    profile: RequirementQualityProfile, characteristic_id: CharacteristicId
) -> CharacteristicAssessment:
    return {
        CharacteristicId.COMPLETENESS: profile.completeness,
        CharacteristicId.VERIFIABILITY: profile.verifiability,
        CharacteristicId.UNAMBIGUITY: profile.unambiguity,
    }[characteristic_id]


def _expected_c(
    outcomes: tuple[FeatureDetectionOutcome, ...],
) -> tuple[
    TraceDecisionCode,
    tuple[TraceEffectCode, ...],
    CharacteristicAssessmentState,
    Fraction | None,
]:
    effects = tuple(
        TraceEffectCode.C_REQUIRED_UNRESOLVED
        if outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
        else TraceEffectCode.C_PRESENT_1
        if outcome.observations
        else TraceEffectCode.C_COMPLETED_ABSENCE_0
        for outcome in outcomes
    )
    if any(
        outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
        for outcome in outcomes
    ):
        return (
            TraceDecisionCode.C_REQUIRED_INPUT_UNRESOLVED,
            effects,
            CharacteristicAssessmentState.UNKNOWN,
            None,
        )
    return (
        TraceDecisionCode.C_CRITERION_RATIO_COMPUTED,
        effects,
        CharacteristicAssessmentState.COMPUTED,
        Fraction(sum(bool(outcome.observations) for outcome in outcomes), 3),
    )


def _expected_v(
    outcomes: tuple[FeatureDetectionOutcome, ...],
) -> tuple[
    TraceDecisionCode,
    tuple[TraceEffectCode, ...],
    CharacteristicAssessmentState,
    Fraction | None,
]:
    acceptance, quantitative, method = outcomes
    lower = (quantitative, method)

    if acceptance.observations:
        effects = (TraceEffectCode.V_SELECTS_FULL_TIER,) + tuple(
            TraceEffectCode.V_PRESENT_NONSELECTING
            if outcome.observations
            else TraceEffectCode.V_COMPLETED_ABSENCE
            if outcome.processing_status is DetectionProcessingStatus.COMPLETE
            else TraceEffectCode.V_UNRESOLVED_NON_MATERIAL
            for outcome in lower
        )
        return (
            TraceDecisionCode.V_FULL_ACCEPTANCE_TIER,
            effects,
            CharacteristicAssessmentState.COMPUTED,
            Fraction(1, 1),
        )

    if acceptance.processing_status is DetectionProcessingStatus.INCOMPLETE:
        lower_tier_established = any(outcome.observations for outcome in lower)
        effects = (TraceEffectCode.V_UNRESOLVED_MATERIAL,) + tuple(
            TraceEffectCode.V_PRESENT_NONSELECTING
            if outcome.observations
            else TraceEffectCode.V_COMPLETED_ABSENCE
            if outcome.processing_status is DetectionProcessingStatus.COMPLETE
            else TraceEffectCode.V_UNRESOLVED_NON_MATERIAL
            if lower_tier_established
            else TraceEffectCode.V_UNRESOLVED_MATERIAL
            for outcome in lower
        )
        return (
            TraceDecisionCode.V_MATERIAL_INPUT_UNRESOLVED,
            effects,
            CharacteristicAssessmentState.UNKNOWN,
            None,
        )

    if any(outcome.observations for outcome in lower):
        effects = (TraceEffectCode.V_COMPLETED_ABSENCE,) + tuple(
            TraceEffectCode.V_SELECTS_LOWER_TIER
            if outcome.observations
            else TraceEffectCode.V_COMPLETED_ABSENCE
            if outcome.processing_status is DetectionProcessingStatus.COMPLETE
            else TraceEffectCode.V_UNRESOLVED_NON_MATERIAL
            for outcome in lower
        )
        return (
            TraceDecisionCode.V_PARTIAL_LOWER_TIER,
            effects,
            CharacteristicAssessmentState.COMPUTED,
            Fraction(1, 2),
        )

    if any(
        outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
        for outcome in lower
    ):
        effects = (TraceEffectCode.V_COMPLETED_ABSENCE,) + tuple(
            TraceEffectCode.V_COMPLETED_ABSENCE
            if outcome.processing_status is DetectionProcessingStatus.COMPLETE
            else TraceEffectCode.V_UNRESOLVED_MATERIAL
            for outcome in lower
        )
        return (
            TraceDecisionCode.V_MATERIAL_INPUT_UNRESOLVED,
            effects,
            CharacteristicAssessmentState.UNKNOWN,
            None,
        )

    return (
        TraceDecisionCode.V_COMPLETED_NO_EVIDENCE_TIER,
        (TraceEffectCode.V_COMPLETED_ABSENCE,) * 3,
        CharacteristicAssessmentState.COMPUTED,
        Fraction(0, 1),
    )


def _expected_u(
    outcomes: tuple[FeatureDetectionOutcome, ...],
) -> tuple[
    TraceDecisionCode,
    tuple[TraceEffectCode, ...],
    CharacteristicAssessmentState,
    Fraction | None,
]:
    outcome = outcomes[0]
    if outcome.observations:
        return (
            TraceDecisionCode.U_SUPPORTED_SIGNAL_TIER,
            (TraceEffectCode.U_SIGNAL_PRESENT,),
            CharacteristicAssessmentState.COMPUTED,
            Fraction(1, 2),
        )
    if outcome.processing_status is DetectionProcessingStatus.COMPLETE:
        return (
            TraceDecisionCode.U_COMPLETED_SIGNAL_ABSENCE_TIER,
            (TraceEffectCode.U_COMPLETED_SIGNAL_ABSENCE,),
            CharacteristicAssessmentState.COMPUTED,
            Fraction(1, 1),
        )
    return (
        TraceDecisionCode.U_MATERIAL_INPUT_UNRESOLVED,
        (TraceEffectCode.U_UNRESOLVED_MATERIAL,),
        CharacteristicAssessmentState.UNKNOWN,
        None,
    )


def expected_characteristic_semantics(
    characteristic_id: CharacteristicId,
    outcomes: tuple[FeatureDetectionOutcome, ...],
) -> tuple[
    TraceDecisionCode,
    tuple[TraceEffectCode, ...],
    CharacteristicAssessmentState,
    Fraction | None,
]:
    """Derive the approved trace branch and authoritative expected result."""
    if characteristic_id is CharacteristicId.COMPLETENESS:
        return _expected_c(outcomes)
    if characteristic_id is CharacteristicId.VERIFIABILITY:
        return _expected_v(outcomes)
    return _expected_u(outcomes)


def _validate_record(
    result: RequirementExtractionResult,
    profile: RequirementQualityProfile,
    trace: RequirementAssessmentTrace,
) -> None:
    if trace.requirement_id != result.requirement.id:
        raise ValueError("trace requirement_id must match extraction requirement.id")

    expected_characteristics = tuple(CharacteristicId)
    actual_characteristics = tuple(item.characteristic_id for item in trace.characteristics)
    if actual_characteristics != expected_characteristics:
        raise ValueError("trace characteristics must contain exactly C, V, U in order")

    evidence_by_id = {item.evidence_id: item for item in result.evidence}
    for evidence in result.evidence:
        if evidence.requirement_id != trace.requirement_id:
            raise ValueError("Evidence requirement_id must match trace requirement_id")
    for _, evidence_ref in _accepted_evidence_refs(result.features):
        if evidence_ref not in evidence_by_id:
            raise ValueError("every accepted evidence reference must resolve exactly once")

    for feature_id in FeatureId:
        outcome = outcome_for_feature(result, feature_id)
        for diagnostic in outcome.diagnostics:
            span = diagnostic.candidate_span
            if span is not None and (
                span.end_offset > len(result.requirement.text)
                or result.requirement.text[span.start_offset:span.end_offset] != span.text
            ):
                raise ValueError("diagnostic candidate span must round-trip to Requirement.text")

    for characteristic_trace in trace.characteristics:
        characteristic_id = characteristic_trace.characteristic_id
        assessment = _assessment_for(profile, characteristic_id)
        governing_rule_id = _RULE_IDS[characteristic_id]
        if characteristic_trace.governing_rule_id != governing_rule_id:
            raise ValueError("trace governing_rule_id does not match the characteristic")
        if assessment.state is CharacteristicAssessmentState.NOT_APPLICABLE:
            raise ValueError("NOT_APPLICABLE is unreachable under current C/V/U rules")
        if (
            assessment.assessment_rule_id is not None
            and assessment.assessment_rule_id != governing_rule_id
        ):
            raise ValueError("assessment_rule_id must match the trace governing rule")
        if (
            assessment.state is CharacteristicAssessmentState.COMPUTED
            and assessment.assessment_rule_id != characteristic_trace.governing_rule_id
        ):
            raise ValueError("computed assessment_rule_id must equal governing_rule_id")

        expected_families = _INPUT_FAMILIES[characteristic_id]
        actual_families = tuple(item.feature_id for item in characteristic_trace.inputs)
        if actual_families != expected_families:
            raise ValueError("trace inputs must contain the required feature families in order")

        outcomes = tuple(outcome_for_feature(result, item) for item in expected_families)
        decision, effects, state, value = expected_characteristic_semantics(
            characteristic_id, outcomes
        )
        if characteristic_trace.decision_code is not decision:
            raise ValueError("trace decision_code is inconsistent with extraction outcomes")
        if assessment.state is not state or assessment.value != value:
            raise ValueError("quality profile is inconsistent with extraction outcomes and trace")

        for input_trace, outcome, effect in zip(
            characteristic_trace.inputs, outcomes, effects, strict=True
        ):
            expected_applicability = (
                CriterionApplicability.APPLICABLE
                if characteristic_id is CharacteristicId.COMPLETENESS
                else None
            )
            if input_trace.applicability is not expected_applicability:
                raise ValueError("trace input applicability is invalid for the characteristic")
            if input_trace.observation_indexes != tuple(range(len(outcome.observations))):
                raise ValueError("observation indexes must reference every observation in order")
            if input_trace.diagnostic_indexes != tuple(range(len(outcome.diagnostics))):
                raise ValueError("diagnostic indexes must reference every diagnostic in order")
            if input_trace.effect_code is not effect:
                raise ValueError("trace effect_code is inconsistent with the rule branch")

        expected_finding_refs = tuple(item.finding_id for item in assessment.findings)
        if characteristic_trace.finding_refs != expected_finding_refs:
            raise ValueError("finding_refs must reference every assessment Finding in order")
        if characteristic_id is not CharacteristicId.UNAMBIGUITY:
            if assessment.findings:
                raise ValueError("current Completeness and Verifiability cannot carry Findings")
        else:
            _validate_unambiguity_findings(result, assessment)


def _validate_unambiguity_findings(
    result: RequirementExtractionResult, assessment: CharacteristicAssessment
) -> None:
    occurrences = result.features.vague_term_occurrences.observations
    if not occurrences:
        if assessment.findings:
            raise ValueError("Unambiguity absence or unresolved state cannot carry Findings")
        return

    evidence_by_id = {item.evidence_id: item for item in result.evidence}
    ordered_occurrences = tuple(
        occurrence
        for _, occurrence in sorted(
            enumerate(occurrences),
            key=lambda indexed: (
                min(evidence_by_id[ref].start_offset for ref in indexed[1].evidence_refs),
                indexed[0],
            ),
        )
    )
    if len(assessment.findings) != len(ordered_occurrences):
        raise ValueError("each vague-term occurrence must map to exactly one Finding")
    for finding, occurrence in zip(assessment.findings, ordered_occurrences, strict=True):
        if (
            finding.requirement_id != result.requirement.id
            or finding.characteristic_id is not CharacteristicId.UNAMBIGUITY
            or finding.kind is not FindingKind.SIGNAL
            or finding.code != "VAGUE_TERM_SIGNAL"
            or finding.rule_id != "FIND-U-VAGUE-001"
            or finding.criterion_id is not None
            or finding.evidence_refs != occurrence.evidence_refs
        ):
            raise ValueError("Unambiguity Finding provenance must match its vague occurrence")

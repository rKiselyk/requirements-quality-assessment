"""Pure evaluator for the bounded observed Performance Efficiency indicator."""

from __future__ import annotations

from fractions import Fraction

from ..dynamic_evidence import (
    Applicability,
    ConformanceOutcome,
    CriterionBindingId,
    FullModelStatus,
    RESPONSE_TIME_METRIC_REF,
)
from ..metrics import MetricEntryId, NumericRepresentation
from ..performance_efficiency import (
    FEATURE_CONTRACT_REF,
    FEATURE_REGISTRY_REF,
    MAPPING_RULE_REF,
    PE_FEATURE_EFFECTS,
    PE_FEATURE_REGISTRY,
    ConformanceFeatureValue,
    CriterionFeatureValue,
    FeatureReason,
    FeatureDiagnosticRef,
    ObservationFeatureValue,
    PerformanceEfficiencyFeature,
    PerformanceEfficiencyFeatureId,
    PerformanceEfficiencyFeatureProfile,
    ProductQualityCharacteristicId,
    QbCrossResultRef,
    QbTargetGateDecision,
    QbTargetGateFeatureValue,
)
from .domain import (
    MANDATORY_NON_CLAIMS,
    MODEL_REF,
    PARAMETER_SET_REF,
    PROCEDURE_RULE_REF,
    BoundedEvidenceCoverage,
    BoundedProcedureState,
    CalibrationStatus,
    EvidenceChannelId,
    EvidenceCoverageItem,
    EvidenceCoverageKind,
    EvidenceProcedureScope,
    EvidenceRole,
    FullCharacteristicCoverage,
    ModelRef,
    ParameterSetRef,
    ProductQualityAssessment,
    ProductQualityAssessmentContext,
    ProductQualityAssessmentId,
    ProductQualityAssessmentProvenance,
    ProductQualityResultKind,
    ProductQualityScope,
    ProductQualityScopeKind,
)


_COVERAGE_SLOTS = (
    (
        EvidenceChannelId.RESPONSE_TIME_CRITERION,
        EvidenceRole.REQUIRED,
        PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME,
    ),
    (
        EvidenceChannelId.TARGET_QB_GATE,
        EvidenceRole.GATE,
        PerformanceEfficiencyFeatureId.SPECIFICATION_QB,
    ),
    (
        EvidenceChannelId.RESPONSE_TIME_OBSERVATION,
        EvidenceRole.REQUIRED,
        PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME,
    ),
    (
        EvidenceChannelId.RESPONSE_TIME_CONFORMANCE,
        EvidenceRole.REQUIRED,
        PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME,
    ),
    (
        EvidenceChannelId.REQUIREMENT_C_CONTEXT,
        EvidenceRole.CONTEXT_ONLY,
        PerformanceEfficiencyFeatureId.REQUIREMENT_COMPLETENESS,
    ),
    (
        EvidenceChannelId.REQUIREMENT_V_CONTEXT,
        EvidenceRole.CONTEXT_ONLY,
        PerformanceEfficiencyFeatureId.REQUIREMENT_VERIFIABILITY,
    ),
    (
        EvidenceChannelId.REQUIREMENT_U_CONTEXT,
        EvidenceRole.CONTEXT_ONLY,
        PerformanceEfficiencyFeatureId.REQUIREMENT_UNAMBIGUITY,
    ),
)


def _feature(
    profile: PerformanceEfficiencyFeatureProfile,
    feature_id: PerformanceEfficiencyFeatureId,
) -> PerformanceEfficiencyFeature:
    return profile.features[PE_FEATURE_REGISTRY.index(feature_id)]


def _deduplicate(values: tuple) -> tuple:
    return tuple(dict.fromkeys(values))


def _gate_decision(feature: PerformanceEfficiencyFeature) -> QbTargetGateDecision:
    if feature.status is FullModelStatus.AVAILABLE:
        if not isinstance(feature.typed_value, QbTargetGateFeatureValue):
            raise ValueError("available QB gate requires its categorical value")
        return feature.typed_value.gate_decision
    if (
        feature.status is FullModelStatus.NOT_APPLICABLE
        and FeatureReason.QB_TARGET_NOT_APPLICABLE in feature.reasons
    ):
        return QbTargetGateDecision.TARGET_NOT_APPLICABLE
    if (
        feature.status is FullModelStatus.UNRESOLVED
        and FeatureReason.QB_TARGET_UNRESOLVED in feature.reasons
    ):
        return QbTargetGateDecision.TARGET_UNRESOLVED
    raise ValueError("QB feature does not represent an approved target-gate decision")


def _expected_profile_state(
    profile: PerformanceEfficiencyFeatureProfile,
) -> tuple[FullModelStatus, Applicability]:
    criterion = _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    )
    observation = _feature(
        profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME
    )
    conformance = _feature(
        profile, PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME
    )
    qb = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)
    if criterion.status is FullModelStatus.NOT_APPLICABLE:
        return FullModelStatus.NOT_APPLICABLE, Applicability.NOT_APPLICABLE
    if criterion.status is not FullModelStatus.AVAILABLE:
        return criterion.status, criterion.applicability
    gate = _gate_decision(qb)
    if gate in {
        QbTargetGateDecision.TARGET_CONFLICT,
        QbTargetGateDecision.TARGET_UNRESOLVED,
    }:
        return FullModelStatus.UNRESOLVED, Applicability.APPLICABLE
    if observation.status is not FullModelStatus.AVAILABLE:
        return observation.status, observation.applicability
    if conformance.status is not FullModelStatus.AVAILABLE:
        return conformance.status, conformance.applicability
    return FullModelStatus.AVAILABLE, Applicability.APPLICABLE


def _validate_profile(
    profile: PerformanceEfficiencyFeatureProfile,
    context: ProductQualityAssessmentContext,
) -> None:
    if not isinstance(profile, PerformanceEfficiencyFeatureProfile):
        raise TypeError("feature_profile must be a PerformanceEfficiencyFeatureProfile")
    if not isinstance(context, ProductQualityAssessmentContext):
        raise TypeError("assessment_context must be a ProductQualityAssessmentContext")
    if profile.profile_id != context.feature_profile_ref:
        raise ValueError("feature profile identity does not match assessment context")
    if profile.artifact_ref != context.artifact_ref:
        raise ValueError("feature profile and assessment context cannot cross artifacts")
    if profile.source_assessment_ref != context.source_assessment_ref:
        raise ValueError("feature profile and context cannot cross source assessments")
    if profile.product_ref != context.product_ref:
        raise ValueError("feature profile and context cannot cross products")
    if profile.process_state_ref != context.process_state_ref:
        raise ValueError("feature profile and context cannot cross process states")
    if profile.characteristic_id is not ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY:
        raise ValueError("only Performance Efficiency is supported")
    if profile.registry_ref != FEATURE_REGISTRY_REF:
        raise ValueError("feature profile uses an unsupported registry")
    if profile.mapping_rule_ref != MAPPING_RULE_REF:
        raise ValueError("feature profile uses an unsupported mapping rule")
    if FEATURE_CONTRACT_REF not in profile.provenance.source_contract_refs:
        raise ValueError("feature profile provenance omits its approved contract")
    if tuple(item.feature_id for item in profile.features) != PE_FEATURE_REGISTRY:
        raise ValueError("feature profile must contain the exact seven-slot registry")
    if tuple(item.effect for item in profile.features) != PE_FEATURE_EFFECTS:
        raise ValueError("feature profile roles do not match the approved registry")
    if profile.provenance.ordered_feature_entry_refs != tuple(
        item.feature_entry_id for item in profile.features
    ):
        raise ValueError("feature profile provenance order is inconsistent")
    if (profile.status, profile.applicability) != _expected_profile_state(profile):
        raise ValueError("feature profile status is inconsistent with approved precedence")

    criterion = _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    )
    observation = _feature(
        profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME
    )
    conformance = _feature(
        profile, PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME
    )
    if criterion.status is FullModelStatus.AVAILABLE:
        if not isinstance(criterion.typed_value, CriterionFeatureValue):
            raise ValueError("available criterion feature has no criterion value")
        if criterion.typed_value.metric_ref != RESPONSE_TIME_METRIC_REF:
            raise ValueError("criterion feature does not use response time")
        criterion_id = criterion.typed_value.criterion_ref.criterion_id
        expected_binding = CriterionBindingId(
            criterion_id.artifact_ref,
            criterion_id.source_assessment_ref,
            criterion_id.requirement_subject_ref,
            criterion_id.source_snapshot_id,
            criterion_id.source_observation_ref,
            criterion_id.binding_rule_ref,
        )
        if expected_binding != profile.provenance.criterion_binding_ref:
            raise ValueError("criterion feature and profile provenance do not agree")
        if criterion.source_refs != (expected_binding,):
            raise ValueError("criterion feature must retain its binding reference")
    if observation.status is FullModelStatus.AVAILABLE:
        if not isinstance(observation.typed_value, ObservationFeatureValue):
            raise ValueError("available observation feature has no observation value")
        if observation.typed_value.metric_ref != RESPONSE_TIME_METRIC_REF:
            raise ValueError("observation feature does not use response time")
        if observation.source_refs != (observation.typed_value.observation_ref,):
            raise ValueError("observation feature must retain its observation reference")
    if conformance.status is FullModelStatus.AVAILABLE:
        if not isinstance(conformance.typed_value, ConformanceFeatureValue):
            raise ValueError("available conformance feature has no categorical value")
        if conformance.typed_value.conformance_ref != profile.provenance.conformance_assessment_ref:
            raise ValueError("conformance feature and profile provenance do not agree")
        if conformance.source_refs != (conformance.typed_value.conformance_ref,):
            raise ValueError("conformance feature must retain its assessment reference")
        if conformance.typed_value.outcome not in {
            ConformanceOutcome.CONFORMS,
            ConformanceOutcome.DOES_NOT_CONFORM,
        }:
            raise ValueError("unsupported conformance outcome")
    if profile.status is FullModelStatus.AVAILABLE:
        gate = _gate_decision(
            _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)
        )
        if gate not in {
            QbTargetGateDecision.TARGET_CLEAR,
            QbTargetGateDecision.TARGET_NOT_APPLICABLE,
        }:
            raise ValueError("available profile requires an eligible QB target gate")


def _procedure_state(status: FullModelStatus) -> BoundedProcedureState:
    if status is FullModelStatus.AVAILABLE:
        return BoundedProcedureState.COMPLETE
    return BoundedProcedureState(status.value)


def _coverage(
    profile: PerformanceEfficiencyFeatureProfile,
) -> BoundedEvidenceCoverage:
    items = tuple(
        EvidenceCoverageItem(
            channel_id=channel_id,
            role=role,
            feature_ref=_feature(profile, feature_id).feature_entry_id,
            status=_feature(profile, feature_id).status,
            applicability=_feature(profile, feature_id).applicability,
            source_refs=_feature(profile, feature_id).source_refs,
        )
        for channel_id, role, feature_id in _COVERAGE_SLOTS
    )
    return BoundedEvidenceCoverage(
        coverage_kind=EvidenceCoverageKind.BOUNDED_REQUIRED_CHANNEL_INVENTORY,
        procedure_scope=EvidenceProcedureScope.SINGLE_RESPONSE_TIME_CRITERION,
        items=items,
        bounded_procedure_state=_procedure_state(profile.status),
        full_performance_efficiency_coverage=FullCharacteristicCoverage.NOT_ESTABLISHED,
        numeric_coverage=None,
    )


def _scope(profile: PerformanceEfficiencyFeatureProfile) -> ProductQualityScope:
    criterion = _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    ).typed_value
    observation = _feature(
        profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME
    ).typed_value
    criterion_value = criterion if isinstance(criterion, CriterionFeatureValue) else None
    observation_value = (
        observation if isinstance(observation, ObservationFeatureValue) else None
    )
    context_identity = (
        criterion_value.context_identity
        if criterion_value is not None
        else (
            observation_value.context_identity
            if observation_value is not None
            else None
        )
    )
    unit = (
        criterion_value.unit
        if criterion_value is not None
        else observation_value.unit if observation_value is not None else None
    )
    return ProductQualityScope(
        scope_kind=ProductQualityScopeKind.SINGLE_CRITERION_SINGLE_OBSERVATION,
        characteristic_id=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
        dynamic_metric_ref=RESPONSE_TIME_METRIC_REF,
        criterion_ref=(
            None if criterion_value is None else criterion_value.criterion_ref
        ),
        requirement_subject_ref=profile.criterion_subject_ref,
        observation_ref=(
            None if observation_value is None else observation_value.observation_ref
        ),
        conformance_ref=profile.provenance.conformance_assessment_ref,
        product_ref=profile.product_ref,
        environment_ref=profile.provenance.environment_ref_or_none,
        collection_ref=profile.provenance.collection_ref_or_none,
        context_identity=context_identity,
        unit=unit,
        process_stage=profile.process_state_ref.stage,
        full_characteristic_coverage=FullCharacteristicCoverage.NOT_ESTABLISHED,
    )


def _qb_description(profile: PerformanceEfficiencyFeatureProfile) -> str:
    qb = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)
    try:
        return _gate_decision(qb).value
    except ValueError:
        return qb.status.value


def _reasons(profile: PerformanceEfficiencyFeatureProfile) -> str:
    values = tuple(
        reason.value
        for feature in profile.features
        for reason in feature.reasons
    )
    return ", ".join(dict.fromkeys(values)) if values else "no typed reason supplied"


def _scope_statement(profile: PerformanceEfficiencyFeatureProfile) -> str:
    collection = profile.provenance.collection_ref_or_none
    environment = profile.provenance.environment_ref_or_none
    criterion = _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    ).typed_value
    context = (
        criterion.context_identity.normalized_text
        if isinstance(criterion, CriterionFeatureValue)
        else "unavailable"
    )
    statement = (
        "Observed conformance of one response-time criterion for product "
        f"{profile.product_ref.product_id} version {profile.product_ref.product_version} "
        f"in collection {collection.collection_id if collection else 'unavailable'} "
        f"version {collection.collection_version if collection else 'unavailable'} and "
        f"environment {environment.environment_id if environment else 'unavailable'} "
        f"version {environment.environment_version if environment else 'unavailable'} "
        f"in exact criterion context {context!r}. This covers one criterion and "
        "observation; it is not complete Performance Efficiency and is not a prediction."
    )
    if profile.status is not FullModelStatus.AVAILABLE:
        statement += (
            f" The bounded procedure status is {profile.status.value}: {_reasons(profile)}."
        )
    return statement


def _explanation(
    profile: PerformanceEfficiencyFeatureProfile,
    outcome: ConformanceOutcome | None,
    value: Fraction | None,
) -> str:
    criterion = _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    ).typed_value
    observation = _feature(
        profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME
    ).typed_value
    parts = [
        "Result kind OBSERVED_REFERENCE_INDICATOR covers one response-time criterion and one observation.",
    ]
    if isinstance(criterion, CriterionFeatureValue):
        parts.append(
            "Criterion "
            f"{criterion.criterion_ref.criterion_id!r} uses comparator "
            f"{criterion.comparator.value}, bound {criterion.exact_decimal_bound}, "
            f"unit {criterion.unit.value}, and context {criterion.context_identity.normalized_text!r}."
        )
    if isinstance(observation, ObservationFeatureValue):
        collection = profile.provenance.collection_ref_or_none
        environment = profile.provenance.environment_ref_or_none
        parts.append(
            "Observation "
            f"{observation.observation_ref.observation_id!r} has exact value "
            f"{observation.exact_decimal_value} for product {profile.product_ref.product_id} "
            f"version {profile.product_ref.product_version}, collection "
            f"{collection.collection_id if collection else 'unavailable'} version "
            f"{collection.collection_version if collection else 'unavailable'}, and environment "
            f"{environment.environment_id if environment else 'unavailable'} version "
            f"{environment.environment_version if environment else 'unavailable'}."
        )
    if outcome is None:
        parts.append(
            f"No indicator is produced because the controlling state is {profile.status.value}: {_reasons(profile)}."
        )
    else:
        parts.append(
            f"Categorical conformance {outcome.value} maps exactly to Fraction({value.numerator}, {value.denominator})."
        )
    parts.extend(
        (
            f"The target-scoped QB gate is {_qb_description(profile)} and its Fraction is not an assessment operand.",
            "Completeness, Verifiability, and Unambiguity remain requirement-artifact context only.",
            "Prediction, reliability, and uncertainty are absent; calibration status is PROVISIONAL_NOT_CALIBRATED.",
            "This result is not complete Performance Efficiency.",
        )
    )
    return " ".join(parts)


def _provenance(
    profile: PerformanceEfficiencyFeatureProfile,
    context: ProductQualityAssessmentContext,
    model_ref: ModelRef,
    parameter_set_ref: ParameterSetRef,
) -> ProductQualityAssessmentProvenance:
    criterion = _feature(
        profile, PerformanceEfficiencyFeatureId.CRITERION_RESPONSE_TIME
    ).typed_value
    observation = _feature(
        profile, PerformanceEfficiencyFeatureId.OBSERVATION_RESPONSE_TIME
    ).typed_value
    qb = _feature(profile, PerformanceEfficiencyFeatureId.SPECIFICATION_QB)
    if not isinstance(qb.source_refs[0], MetricEntryId):
        raise ValueError("QB feature must reference its metric entry first")
    qb_cross_refs = tuple(
        item for item in qb.provenance_refs if isinstance(item, QbCrossResultRef)
    )
    evidence_refs = _deduplicate(
        tuple(ref for feature in profile.features for ref in feature.evidence_refs)
    )
    diagnostic_refs = _deduplicate(
        tuple(
            ref
            for feature in profile.features
            for ref in feature.provenance_refs
            if isinstance(ref, FeatureDiagnosticRef)
        )
    )
    contracts = _deduplicate(
        (*profile.provenance.source_contract_refs, context.assessment_contract_ref)
    )
    rules = _deduplicate((*profile.provenance.rule_refs, PROCEDURE_RULE_REF))
    return ProductQualityAssessmentProvenance(
        feature_profile_ref=profile.profile_id,
        ordered_feature_refs=tuple(
            item.feature_entry_id for item in profile.features
        ),
        criterion_ref_or_none=(
            criterion.criterion_ref
            if isinstance(criterion, CriterionFeatureValue)
            else None
        ),
        requirement_subject_ref_or_none=profile.criterion_subject_ref,
        metric_profile_ref=profile.metric_profile_ref,
        qb_metric_entry_ref=qb.source_refs[0],
        ordered_qb_cross_result_refs=qb_cross_refs,
        observation_ref_or_none=(
            observation.observation_ref
            if isinstance(observation, ObservationFeatureValue)
            else None
        ),
        conformance_ref_or_none=profile.provenance.conformance_assessment_ref,
        product_ref=profile.product_ref,
        environment_ref_or_none=profile.provenance.environment_ref_or_none,
        collection_ref_or_none=profile.provenance.collection_ref_or_none,
        process_state_ref=profile.process_state_ref,
        source_evidence_refs=evidence_refs,
        source_diagnostic_refs=diagnostic_refs,
        source_assessment_refs=(
            profile.source_assessment_ref,
            profile.dynamic_assessment_ref,
        ),
        contract_refs=contracts,
        rule_refs=rules,
        model_ref=model_ref,
        parameter_set_ref=parameter_set_ref,
    )


class PerformanceEfficiencyQualityAssessor:
    """Interpret one validated ``X_PE`` without rebuilding upstream evidence."""

    def assess(
        self,
        feature_profile: PerformanceEfficiencyFeatureProfile,
        model_ref: ModelRef,
        parameter_set_ref: ParameterSetRef,
        assessment_context: ProductQualityAssessmentContext,
    ) -> ProductQualityAssessment:
        if not isinstance(model_ref, ModelRef):
            raise TypeError("model_ref must be a ModelRef")
        if not isinstance(parameter_set_ref, ParameterSetRef):
            raise TypeError("parameter_set_ref must be a ParameterSetRef")
        if model_ref != MODEL_REF:
            raise ValueError("unsupported product-quality model identity/version")
        if parameter_set_ref != PARAMETER_SET_REF:
            raise ValueError("unsupported product-quality parameter-set identity/version")
        _validate_profile(feature_profile, assessment_context)

        outcome = None
        value = None
        representation = NumericRepresentation.NONE
        if feature_profile.status is FullModelStatus.AVAILABLE:
            conformance_value = _feature(
                feature_profile,
                PerformanceEfficiencyFeatureId.CONFORMANCE_RESPONSE_TIME,
            ).typed_value
            if not isinstance(conformance_value, ConformanceFeatureValue):
                raise ValueError("available profile requires categorical conformance")
            outcome = conformance_value.outcome
            value = {
                ConformanceOutcome.CONFORMS: Fraction(1, 1),
                ConformanceOutcome.DOES_NOT_CONFORM: Fraction(0, 1),
            }[outcome]
            representation = NumericRepresentation.EXACT_FRACTION

        result_kind = ProductQualityResultKind.OBSERVED_REFERENCE_INDICATOR
        assessment_id = ProductQualityAssessmentId(
            assessment_context.assessment_event_ref,
            feature_profile.profile_id,
            ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
            result_kind,
            model_ref,
            PROCEDURE_RULE_REF,
            parameter_set_ref,
        )
        provenance = _provenance(
            feature_profile, assessment_context, model_ref, parameter_set_ref
        )
        feature_refs = tuple(
            item.feature_entry_id for item in feature_profile.features
        )
        return ProductQualityAssessment(
            assessment_id=assessment_id,
            assessment_event_ref=assessment_context.assessment_event_ref,
            characteristic_id=ProductQualityCharacteristicId.PERFORMANCE_EFFICIENCY,
            product_ref=feature_profile.product_ref,
            artifact_ref=feature_profile.artifact_ref,
            feature_profile_ref=feature_profile.profile_id,
            scope=_scope(feature_profile),
            scope_statement=_scope_statement(feature_profile),
            result_kind=result_kind,
            status=feature_profile.status,
            applicability=feature_profile.applicability,
            source_conformance_outcome=outcome,
            value=value,
            prediction_value=None,
            observed_value=value,
            numeric_representation=representation,
            evidence_coverage=_coverage(feature_profile),
            reliability=None,
            uncertainty=None,
            explanation=_explanation(feature_profile, outcome, value),
            feature_refs=feature_refs,
            evidence_refs=provenance.source_evidence_refs,
            provenance=provenance,
            model_ref=model_ref,
            procedure_rule_ref=PROCEDURE_RULE_REF,
            parameter_set_ref=parameter_set_ref,
            calibration_status=CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
            artifact_version=feature_profile.artifact_ref.artifact_version,
            source_assessment_version=(
                feature_profile.source_assessment_ref.assessment_version
            ),
            product_version=feature_profile.product_ref.product_version,
            product_quality_assessment_version=(
                assessment_context.assessment_event_ref.assessment_event_version
            ),
            non_claims=MANDATORY_NON_CLAIMS,
        )


def assess_product_quality(
    feature_profile: PerformanceEfficiencyFeatureProfile,
    model_ref: ModelRef,
    parameter_set_ref: ParameterSetRef,
    assessment_context: ProductQualityAssessmentContext,
) -> ProductQualityAssessment:
    """Return the exact bounded observed indicator for one validated ``X_PE``."""

    return PerformanceEfficiencyQualityAssessor().assess(
        feature_profile,
        model_ref,
        parameter_set_ref,
        assessment_context,
    )


__all__ = ["PerformanceEfficiencyQualityAssessor", "assess_product_quality"]

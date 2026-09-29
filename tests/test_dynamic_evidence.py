"""Contract tests for the Full Model v0.1 minimal dynamic-evidence path."""

from dataclasses import fields, replace
from decimal import Decimal

import pytest

from requirements_quality_assessment.cross_analysis.domain import (
    AssessmentSnapshotId, CrossObservationRef,
)
from requirements_quality_assessment.detectors.quantitative import (
    QuantitativeBaselineDetector, UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE,
)
from requirements_quality_assessment.domain import (
    DetectionProcessingStatus, FeatureDetectionOutcome, FeatureId, Requirement,
    RequirementExtractionResult, RequirementFeatures, UnitLabel,
)
from requirements_quality_assessment.dynamic_evidence import (
    Applicability, ConformanceEvaluationContext, ConformanceOutcome,
    CriterionBindingContext, CriterionContextIdentity,
    DYNAMIC_METRIC_REGISTRY_REF, DynamicEvidenceAssessmentRef,
    DynamicEvidenceReason, DynamicMetricRef, EnvironmentRef, FullModelStatus,
    ObservationCollectionRef, ObservationSlotRef, ObservationSourceKind,
    ProductRef, QB_NORMALIZATION_CONTRACT_REF, RESPONSE_TIME_METRIC_REF,
    SUPPORTED_CONTEXT_IDENTITY, assess_conformance,
    bind_quantitative_criterion, make_dynamic_observation,
    resolve_dynamic_observation, resolve_dynamic_observations, serialize_decimal,
)
from requirements_quality_assessment.metrics import ArtifactRef, AssessmentRef


SOURCE_TEXT = "Час відгуку ≤ 2 с при 500 одночасних користувачах"


def _empty(feature_id: FeatureId):
    return FeatureDetectionOutcome(
        feature_id, (), DetectionProcessingStatus.COMPLETE, (),
    )


def _source(text: str = SOURCE_TEXT) -> RequirementExtractionResult:
    requirement = Requirement("R001", 1, text)
    quantitative, evidence = QuantitativeBaselineDetector().detect(requirement)
    features = RequirementFeatures(
        _empty(FeatureId.CONDITION_CONTEXT),
        _empty(FeatureId.EXPECTED_RESULT),
        _empty(FeatureId.ACCEPTANCE_CRITERION),
        quantitative,
        _empty(FeatureId.VERIFICATION_METHOD),
        _empty(FeatureId.VAGUE_TERM_OCCURRENCE),
    )
    return RequirementExtractionResult(requirement, features, evidence)


def _binding(artifact_id: str = "SPEC-DYN-REF"):
    source = _source()
    artifact = ArtifactRef(artifact_id, "1")
    source_assessment = AssessmentRef("ASSESS-DYN-SOURCE", "1", artifact)
    context = CriterionBindingContext(
        artifact, source_assessment, AssessmentSnapshotId.from_bytes(artifact_id.encode()),
    )
    selected = CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0)
    return source, bind_quantitative_criterion(source, selected, context)


def _collection() -> ObservationCollectionRef:
    return ObservationCollectionRef(
        "DYN-REF-COLLECTION", "1", ProductRef("PRODUCT-DYN-REF", "1"),
        EnvironmentRef("ENV-DYN-REF", "1"),
        ObservationSourceKind.DETERMINISTIC_FIXTURE,
    )


def _observation(
    value: Decimal = Decimal("1.5"),
    *,
    sequence: int = 0,
    unit: UnitLabel = UnitLabel.SECOND,
    context_identity: CriterionContextIdentity = SUPPORTED_CONTEXT_IDENTITY,
    metric_ref: DynamicMetricRef = RESPONSE_TIME_METRIC_REF,
    collection: ObservationCollectionRef | None = None,
):
    collection = collection or _collection()
    slot = ObservationSlotRef(collection, sequence)
    return make_dynamic_observation(
        slot, metric_ref, value, unit, context_identity, f"DYN-RF-{sequence:03d}",
    )


def _assess(binding, observation=None, *, sequence: int = 0):
    collection = observation.collection_ref if observation is not None else _collection()
    slot = ObservationSlotRef(collection, sequence)
    resolution = resolve_dynamic_observation(slot, observation)
    dynamic_ref = DynamicEvidenceAssessmentRef(
        "ASSESS-DYN-CONFORMANCE", "1", binding.binding_id.artifact_ref,
        collection.product_ref, collection,
    )
    return assess_conformance(
        binding, resolution, ConformanceEvaluationContext(dynamic_ref),
    )


def test_valid_response_time_criterion_is_lossless_and_source_backed() -> None:
    source, binding = _binding()

    assert binding.status is FullModelStatus.AVAILABLE
    assert binding.applicability is Applicability.APPLICABLE
    criterion = binding.criterion
    source_observation = source.features.quantitative_constraints.observations[0]
    assert criterion is not None
    assert criterion.bound is source_observation.value.decimal_value
    assert criterion.bound.as_tuple() == Decimal("2").as_tuple()
    assert criterion.metric_ref == RESPONSE_TIME_METRIC_REF
    assert criterion.context_identity == SUPPORTED_CONTEXT_IDENTITY
    assert criterion.requirement_subject_ref.requirement_id == source.requirement.id
    assert all(
        source.requirement.text[item.start_offset:item.end_offset] == item.text
        for item in source.evidence
    )
    assert [item.evidence_id for item in criterion.provenance.evidence_refs] == [
        "QUANT-METRIC-001:E001", "QUANT-001:E001", "QUANT-CONTEXT-001:E001",
    ]
    assert source.features.quantitative_constraints.diagnostics[0].code == (
        UNRESOLVED_NUMERIC_DIAGNOSTIC_CODE
    )
    assert criterion.provenance.diagnostic_refs[0].diagnostic_index == 0


def test_observation_identity_is_criterion_independent() -> None:
    _, first = _binding("SPEC-A")
    _, second = _binding("SPEC-B")
    observation = _observation()

    assert "criterion_id" not in {item.name for item in fields(type(observation.slot_ref))}
    assert "criterion_id" not in {item.name for item in fields(type(observation))}
    assert _assess(first, observation).outcome is ConformanceOutcome.CONFORMS
    assert _assess(second, observation).outcome is ConformanceOutcome.CONFORMS
    assert observation.observation_id == _observation().observation_id


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Decimal("1.5"), ConformanceOutcome.CONFORMS),
        (Decimal("2.00"), ConformanceOutcome.CONFORMS),
        (Decimal("2.01"), ConformanceOutcome.DOES_NOT_CONFORM),
    ],
)
def test_exact_decimal_comparison_including_boundary(value, expected) -> None:
    _, binding = _binding()
    observation = _observation(value)

    assessment = _assess(binding, observation)

    assert assessment.status is FullModelStatus.AVAILABLE
    assert assessment.outcome is expected
    assert assessment.provenance.exact_operands.observed_value is value
    assert observation.observed_value.as_tuple() == value.as_tuple()


@pytest.mark.parametrize(
    "observation",
    [
        _observation(
            metric_ref=DynamicMetricRef(
                DYNAMIC_METRIC_REGISTRY_REF, "DYN.OTHER",
                QB_NORMALIZATION_CONTRACT_REF, "інша метрика",
            )
        ),
        _observation(unit=UnitLabel.MINUTE),
        _observation(
            context_identity=CriterionContextIdentity(
                QB_NORMALIZATION_CONTRACT_REF, "під час пікового навантаження",
            )
        ),
    ],
)
def test_incompatible_metric_unit_or_context_is_unsupported(observation) -> None:
    _, binding = _binding()

    assessment = _assess(binding, observation)

    assert assessment.status is FullModelStatus.UNSUPPORTED
    assert assessment.applicability is Applicability.APPLICABLE
    assert assessment.outcome is None


def test_missing_observation_is_unavailable_not_nonconformance() -> None:
    _, binding = _binding()

    assessment = _assess(binding, None)

    assert assessment.status is FullModelStatus.UNAVAILABLE
    assert assessment.outcome is None
    assert assessment.observation_id is None
    assert assessment.reasons == (DynamicEvidenceReason.OBSERVATION_NOT_COLLECTED,)


def test_unknown_criterion_precedes_observation_and_propagates() -> None:
    _, available = _binding()
    unknown = replace(
        available, status=FullModelStatus.UNKNOWN,
        applicability=Applicability.UNKNOWN, criterion=None, reasons=(),
    )

    assessment = _assess(unknown, _observation(Decimal("3")))

    assert assessment.status is FullModelStatus.UNKNOWN
    assert assessment.applicability is Applicability.UNKNOWN
    assert assessment.outcome is None


def test_unknown_and_unresolved_observation_states_propagate() -> None:
    _, binding = _binding()
    collection = _collection()
    slot = ObservationSlotRef(collection, 0)
    base = resolve_dynamic_observation(slot, None)
    dynamic_ref = DynamicEvidenceAssessmentRef(
        "ASSESS-DYN-CONFORMANCE", "1", binding.binding_id.artifact_ref,
        collection.product_ref, collection,
    )
    context = ConformanceEvaluationContext(dynamic_ref)

    unknown = replace(
        base, status=FullModelStatus.UNKNOWN,
        applicability=Applicability.UNKNOWN, reasons=(),
    )
    unresolved = replace(
        base, status=FullModelStatus.UNRESOLVED,
        applicability=Applicability.UNKNOWN,
        reasons=(DynamicEvidenceReason.OBSERVATION_IDENTITY_UNRESOLVED,),
    )

    assert assess_conformance(binding, unknown, context).status is FullModelStatus.UNKNOWN
    assert assess_conformance(binding, unresolved, context).status is FullModelStatus.UNRESOLVED
    assert assess_conformance(binding, unresolved, context).outcome is None


def test_unsupported_criterion_precedes_unavailable_observation() -> None:
    source = _source("Час відгуку ≤ 2 хв при 500 одночасних користувачах")
    artifact = ArtifactRef("SPEC-DYN-REF", "1")
    context = CriterionBindingContext(
        artifact, AssessmentRef("ASSESS-DYN-SOURCE", "1", artifact),
        AssessmentSnapshotId.from_bytes(b"minute"),
    )
    selected = CrossObservationRef("R001", FeatureId.QUANTITATIVE_CONSTRAINT, 0)
    binding = bind_quantitative_criterion(source, selected, context)

    assessment = _assess(binding, None)

    assert binding.status is FullModelStatus.UNSUPPORTED
    assert assessment.status is FullModelStatus.UNSUPPORTED
    assert assessment.outcome is None


def test_deterministic_structured_identities_and_provenance() -> None:
    _, first = _binding()
    _, second = _binding()
    observation = _observation(Decimal("1.50"))
    a = _assess(first, observation)
    b = _assess(second, observation)

    assert first.binding_id == second.binding_id
    assert first.criterion.criterion_id == second.criterion.criterion_id
    assert a.conformance_id == b.conformance_id
    assert a.criterion_ref.criterion_id == first.criterion.criterion_id
    assert a.observation_ref.observation_id == observation.observation_id
    assert a.provenance.dynamic_observation_provenance_ref == "DYN-RF-000"
    assert a.evidence_refs == first.criterion.provenance.evidence_refs


def test_decimal_serialization_preserves_tuple_and_rejects_float() -> None:
    value = Decimal("2.00")

    assert serialize_decimal(value) == {
        "kind": "DECIMAL", "sign": 0, "digits": [2, 0, 0], "exponent": -2,
    }
    with pytest.raises(TypeError):
        _observation(2.0)  # type: ignore[arg-type]


def test_nonfinite_decimal_is_unsupported_before_comparison() -> None:
    _, binding = _binding()
    observation = _observation(Decimal("NaN"))
    resolution = resolve_dynamic_observation(observation.slot_ref, observation)

    assert resolution.status is FullModelStatus.UNSUPPORTED
    assert resolution.observation is None
    assert _assess(binding, observation).outcome is None


def test_collection_rejects_duplicate_fixture_sequences() -> None:
    collection = _collection()
    first = _observation(collection=collection)
    second = replace(
        first,
        provenance=replace(first.provenance, source_record_ref="DYN-RF-DUPLICATE"),
    )

    with pytest.raises(ValueError, match="unique"):
        resolve_dynamic_observations(collection, (first, second))


def test_binding_without_explicit_selection_does_not_guess() -> None:
    source, _ = _binding()
    artifact = ArtifactRef("SPEC-DYN-REF", "1")
    context = CriterionBindingContext(
        artifact, AssessmentRef("ASSESS-DYN-SOURCE", "1", artifact),
        AssessmentSnapshotId.from_bytes(b"selection"),
    )

    result = bind_quantitative_criterion(source, None, context)

    assert result.status is FullModelStatus.UNRESOLVED
    assert result.criterion is None
    assert result.reasons == (
        DynamicEvidenceReason.SOURCE_OBSERVATION_SELECTION_UNRESOLVED,
    )


def test_completed_absence_is_not_applicable_not_zero() -> None:
    source = _source("Система зберігає дані.")
    artifact = ArtifactRef("SPEC-DYN-REF", "1")
    context = CriterionBindingContext(
        artifact, AssessmentRef("ASSESS-DYN-SOURCE", "1", artifact),
        AssessmentSnapshotId.from_bytes(b"not-applicable"),
    )

    result = bind_quantitative_criterion(source, None, context)

    assert result.status is FullModelStatus.NOT_APPLICABLE
    assert result.applicability is Applicability.NOT_APPLICABLE
    assert result.criterion is None
    assessment = _assess(result, None)
    assert assessment.status is FullModelStatus.NOT_APPLICABLE
    assert assessment.outcome is None

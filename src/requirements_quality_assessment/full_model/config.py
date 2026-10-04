"""Strict stdlib JSON adapter for the programmatic FullModelRequest boundary."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from ..corrective_action import (
    ActionCreatorSource, ApplicationIdentityContext, ExternalProviderRef,
    ExternalRevisionProviderKind, RevisionRef,
)
from ..cross_analysis import CrossObservationRef
from ..domain import FeatureId, UnitLabel
from ..dynamic_evidence import (
    Applicability, CriterionContextIdentity, DynamicEvidenceAssessmentRef,
    EnvironmentRef, ObservationCollectionRef, ObservationSlotRef,
    ObservationSourceKind, ProductRef, RESPONSE_TIME_METRIC_REF,
    make_dynamic_observation,
)
from ..metrics import ArtifactRef, AssessmentRef, ContractRef
from ..performance_efficiency import ProcessStage, ProcessStateRef
from ..product_quality import ProductQualityAssessmentEventRef
from ..reassessment import (
    ComponentVersionSet, EvidenceReuseDisposition, EvidenceReuseReason,
    ExactIdentityCheck, ReassessmentIdentityContext, VersionedComponentRef,
)
from ..risk import RiskAssessmentEventRef
from .domain import (
    EvidenceReuseInput, ExternalRequirementReplacement, ExternalRevisionInput,
    FullModelRequest,
)


def _obj(value, name):
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _text(obj, key):
    value = obj[key]
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{key} must be a non-empty trimmed string")
    return value


def _ref(cls, value, name):
    obj = _obj(value, name)
    return cls(_text(obj, "id"), _text(obj, "version"))


def load_full_model_request(path: str | Path, requirements: tuple) -> FullModelRequest:
    """Load explicit core inputs; TC-01/02/03 remain programmatic-only in TC-05."""
    with Path(path).open("r", encoding="utf-8") as stream:
        root = json.load(stream, parse_float=lambda _: (_ for _ in ()).throw(
            ValueError("JSON floating-point values are forbidden; use strings for exact numbers")
        ))
    root = _obj(root, "config")
    artifact1 = _ref(ArtifactRef, root["artifact_v1"], "artifact_v1")
    artifact2 = _ref(ArtifactRef, root["artifact_v2"], "artifact_v2")
    a1 = _obj(root["assessment_v1"], "assessment_v1")
    a2 = _obj(root["assessment_v2"], "assessment_v2")
    assessment1 = AssessmentRef(_text(a1, "id"), _text(a1, "version"), artifact1)
    assessment2 = AssessmentRef(_text(a2, "id"), _text(a2, "version"), artifact2)
    process = _obj(root["process"], "process")
    stage = ProcessStage(_text(process, "stage"))
    process1 = ProcessStateRef(_text(process, "id"), _text(process, "v1_version"), stage)
    process2 = ProcessStateRef(_text(process, "id"), _text(process, "v2_version"), stage)
    product = _ref(ProductRef, root["product"], "product")
    environment = _ref(EnvironmentRef, root["environment"], "environment")
    collection_obj = _obj(root["collection"], "collection")
    source_kind = ObservationSourceKind(_text(collection_obj, "source_kind"))
    collection = ObservationCollectionRef(
        _text(collection_obj, "id"), _text(collection_obj, "version"), product,
        environment, source_kind,
    )
    criterion = _obj(root["selected_criterion"], "selected_criterion")
    selected_requirement_id = _text(criterion, "requirement_id")
    selected = CrossObservationRef(
        selected_requirement_id,
        FeatureId(_text(criterion, "feature_id")),
        criterion["occurrence"],
    )
    observation_obj = _obj(root["observation"], "observation")
    context_obj = _obj(observation_obj["context"], "observation.context")
    normalization = _obj(context_obj["normalization_contract"], "normalization_contract")
    criterion_context = CriterionContextIdentity(
        ContractRef(_text(normalization, "id"), _text(normalization, "version")),
        _text(context_obj, "normalized_text"),
    )
    observed_value = Decimal(_text(observation_obj, "value"))
    unit = UnitLabel(_text(observation_obj, "unit"))
    slot_index = observation_obj["slot_index"]
    observation_id = _text(observation_obj, "id")
    slot = ObservationSlotRef(collection, slot_index)
    observation = make_dynamic_observation(
        slot, RESPONSE_TIME_METRIC_REF, observed_value, unit, criterion_context,
        observation_id,
    )
    events = _obj(root["events"], "events")
    dynamic1 = DynamicEvidenceAssessmentRef(
        _text(events, "dynamic_id"), _text(events, "v1_version"), artifact1,
        product, collection,
    )
    dynamic2 = DynamicEvidenceAssessmentRef(
        _text(events, "dynamic_id"), _text(events, "v2_version"), artifact2,
        product, collection,
    )
    quality1 = ProductQualityAssessmentEventRef(
        _text(events, "product_quality_id"), _text(events, "v1_version"),
        product, artifact1,
    )
    quality2 = ProductQualityAssessmentEventRef(
        _text(events, "product_quality_id"), _text(events, "v2_version"),
        product, artifact2,
    )
    risk1 = RiskAssessmentEventRef(
        _text(events, "risk_id"), _text(events, "v1_version"), artifact1, process1
    )
    risk2 = RiskAssessmentEventRef(
        _text(events, "risk_id"), _text(events, "v2_version"), artifact2, process2
    )
    action = _obj(root["action"], "action")
    creator = _obj(action["creator"], "action.creator")
    revision_obj = _obj(root["revision"], "revision")
    revision_ref = _ref(RevisionRef, revision_obj["identity"], "revision.identity")
    provider = _obj(revision_obj["provider"], "revision.provider")
    application = _obj(revision_obj["application"], "revision.application")
    replacements = tuple(
        ExternalRequirementReplacement(_text(_obj(item, "replacement"), "requirement_id"),
                                       _text(item, "text"))
        for item in revision_obj["replacements"]
    )
    revision = ExternalRevisionInput(
        artifact2, revision_ref,
        ExternalRevisionProviderKind(_text(revision_obj, "provider_kind")),
        ExternalProviderRef(_text(provider, "id"), _text(provider, "version")),
        replacements, _text(revision_obj, "reason"),
        ApplicationIdentityContext(
            _text(application, "id"), _text(application, "version"),
            _text(application, "child_version"), _text(application, "transition_id"),
        ),
    )
    reuse_obj = _obj(root["evidence_reuse"], "evidence_reuse")
    if reuse_obj["source_contract_permission"] is not True:
        raise ValueError("evidence_reuse.source_contract_permission must be explicitly true")
    values = (
        ("product_ref", observation.product_ref),
        ("observation_source_kind", observation.source_kind),
        ("collection_ref", observation.collection_ref),
        ("metric_ref", observation.metric_ref),
        ("unit", observation.unit),
        ("context_identity", observation.context_identity),
        ("applicability", Applicability.APPLICABLE),
        ("process_stage", process2.stage),
        ("source_contract_permission", True),
    )
    reuse = EvidenceReuseInput(
        EvidenceReuseDisposition(_text(reuse_obj, "disposition")),
        tuple(ExactIdentityCheck(name, value, value, True) for name, value in values),
        tuple(EvidenceReuseReason(item) for item in reuse_obj["reasons"]),
    )
    reassessment_obj = _obj(root["reassessment"], "reassessment")
    versions = ComponentVersionSet(tuple(
        VersionedComponentRef(_text(item, "kind"), _text(item, "id"),
                              _text(item, "version"))
        for item in root["component_versions"]
    ))
    comparisons = _obj(root["comparisons"], "comparisons")
    ids = tuple(comparisons["ids"])
    return FullModelRequest(
        requirements, artifact1, assessment1, process1, selected,
        selected_requirement_id, product, environment, collection, source_kind,
        slot_index, observation_id, observed_value, unit, criterion_context,
        dynamic1, quality1, risk1, _text(action, "id"),
        ActionCreatorSource(_text(creator, "id"), _text(creator, "version")),
        revision, process2, assessment2, reuse, dynamic2, quality2, risk2,
        ReassessmentIdentityContext(
            _text(reassessment_obj, "id"), _text(reassessment_obj, "version"),
            process2,
        ),
        versions, ids, _text(comparisons, "version"),
        _text(process, "transition_id"),
    )


__all__ = ["load_full_model_request"]

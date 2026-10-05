import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactValueData } from "../../components/scientific";
import { selectSectionAvailability } from "../results/projection";
import { selectCurrentResultRecords } from "../results/currentVersion";

export const peFeatureIds = [
  "PE.CRITERION.RESPONSE_TIME",
  "PE.REQ.C",
  "PE.REQ.V",
  "PE.REQ.U",
  "PE.SPEC.QB",
  "PE.OBS.RESPONSE_TIME",
  "PE.CONFORMANCE.RESPONSE_TIME",
] as const;

export const peFeatureEffects = [
  "REQUIRED_INPUT",
  "CONTEXT_ONLY",
  "CONTEXT_ONLY",
  "CONTEXT_ONLY",
  "ELIGIBILITY_GATE",
  "REQUIRED_INPUT",
  "DIRECT_RESULT_INPUT",
] as const;

export const productQualityNonClaims = [
  "NC-PE-001", "NC-PE-002", "NC-PE-003", "NC-PE-004", "NC-PE-005",
  "NC-PE-006", "NC-PE-007", "NC-PE-008", "NC-PE-009",
] as const;

const statuses = new Set(["AVAILABLE", "UNAVAILABLE", "UNKNOWN", "UNRESOLVED", "UNSUPPORTED", "NOT_APPLICABLE"]);
const applicabilities = new Set(["APPLICABLE", "UNKNOWN", "NOT_APPLICABLE"]);

type JsonRecord = Record<string, unknown>;
type ScientificState = { status: string; applicability: string; reasons: string[] };

export interface CriterionProjection extends ScientificState {
  raw: JsonRecord;
  bindingId: JsonRecord;
  criterion: JsonRecord | null;
  requirementId: string | null;
  metricId: string | null;
  comparator: string | null;
  inclusivity: string | null;
  bound: string | null;
  unit: string | null;
  contextIdentity: string | null;
  sourceObservationRef: JsonRecord | null;
  bindingRuleRef: JsonRecord | null;
  evidenceRefs: unknown[];
}

export interface ObservationProjection extends ScientificState {
  raw: JsonRecord;
  slotRef: JsonRecord;
  observation: JsonRecord | null;
  observationId: JsonRecord | null;
  observedValue: string | null;
  metricId: string | null;
  unit: string | null;
  contextIdentity: string | null;
  productRef: JsonRecord | null;
  environmentRef: JsonRecord | null;
  collectionRef: JsonRecord | null;
  sourceKind: string | null;
  sourceRecordRef: string | null;
  provenanceRefs: string[];
}

export interface ConformanceProjection extends ScientificState {
  raw: JsonRecord;
  conformanceId: JsonRecord;
  outcome: string | null;
  explanation: string;
  criterionId: JsonRecord | null;
  observationId: JsonRecord | null;
  evidenceRefs: unknown[];
  evaluatorRuleRef: JsonRecord;
}

export interface FeatureProjection extends ScientificState {
  raw: JsonRecord;
  featureId: string;
  effect: string;
  typedValue: JsonRecord | null;
  availabilityPoint: string;
  explanation: string;
  sourceRefs: unknown[];
  evidenceRefs: unknown[];
  provenanceRefs: unknown[];
  ruleRefs: unknown[];
}

export interface FeatureProfileProjection extends ScientificState {
  raw: JsonRecord;
  profileId: JsonRecord;
  characteristicId: string;
  criterionSubjectRef: JsonRecord | null;
  targetKey: JsonRecord | null;
  registryRef: JsonRecord;
  mappingRuleRef: JsonRecord;
  artifactRef: JsonRecord;
  productRef: JsonRecord;
  processStateRef: JsonRecord;
  features: FeatureProjection[];
}

export interface ObservedProjection extends ScientificState {
  raw: JsonRecord;
  resultKind: string;
  characteristicId: string;
  value: ExactValueData | null;
  observedValue: ExactValueData | null;
  numericRepresentation: string;
  sourceConformanceOutcome: string | null;
  scopeStatement: string;
  calibrationStatus: string;
  nonClaims: string[];
}

export interface PredictionProjection extends ScientificState {
  raw: JsonRecord;
  resultKind: string;
  characteristicId: string;
  predictedValue: ExactValueData | null;
  numericRepresentation: string;
  predictorRef: JsonRecord;
  parameterSetRef: JsonRecord;
  calibrationStatus: string;
  explanation: string;
  withheldReason: string | null;
}

export type PredictionPresentation =
  | { kind: "PRESENT"; value: PredictionProjection }
  | { kind: "ABSENT" }
  | { kind: "MALFORMED" };

export type ProductQualityProjection =
  | { kind: "UNAVAILABLE"; reasonCode: string }
  | { kind: "MALFORMED" }
  | {
      kind: "AVAILABLE";
      revision: "CONTROLLED_DEMO_V1" | "REASSESSMENT_V2";
      criterion: CriterionProjection | null;
      observation: ObservationProjection | null;
      conformance: ConformanceProjection | null;
      featureProfile: FeatureProfileProjection | null;
      observed: ObservedProjection | null;
      prediction: PredictionPresentation;
    };

function record(value: unknown): JsonRecord | null {
  return typeof value === "object" && value !== null && !Array.isArray(value) ? value as JsonRecord : null;
}

function text(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function array(value: unknown): unknown[] | null {
  return Array.isArray(value) ? [...value] : null;
}

function strings(value: unknown): string[] | null {
  return Array.isArray(value) && value.every((item) => typeof item === "string" && item.length > 0) ? [...value] : null;
}

function state(value: JsonRecord, reasonsRequired = false): ScientificState | null {
  const status = text(value.status);
  const applicability = text(value.applicability);
  const reasons = value.reasons === undefined && !reasonsRequired ? [] : strings(value.reasons);
  if (!status || !statuses.has(status) || !applicability || !applicabilities.has(applicability) || reasons === null) return null;
  const accepted = status === "AVAILABLE"
    ? applicability === "APPLICABLE"
    : status === "NOT_APPLICABLE"
      ? applicability === "NOT_APPLICABLE"
      : applicability === "APPLICABLE" || applicability === "UNKNOWN";
  return accepted ? { status, applicability, reasons } : null;
}

function exactFraction(value: unknown): ExactValueData | null {
  const candidate = record(value);
  const numerator = candidate?.numerator;
  const denominator = candidate?.denominator;
  return typeof numerator === "number" && Number.isSafeInteger(numerator)
    && typeof denominator === "number" && Number.isSafeInteger(denominator) && denominator !== 0
    ? { numerator: String(numerator), denominator: String(denominator) }
    : null;
}

function fractionInUnitInterval(value: unknown): boolean {
  const candidate = record(value);
  const numerator = candidate?.numerator;
  const denominator = candidate?.denominator;
  return typeof numerator === "number" && Number.isSafeInteger(numerator)
    && typeof denominator === "number" && Number.isSafeInteger(denominator)
    && denominator > 0 && numerator >= 0 && numerator <= denominator;
}

function hasOwn(value: JsonRecord, field: string): boolean {
  return Object.prototype.hasOwnProperty.call(value, field);
}

function optionalIdentity(value: JsonRecord, field: string, expected: unknown): boolean {
  return !hasOwn(value, field) || deepEqual(value[field], expected);
}

function deepEqual(left: unknown, right: unknown): boolean {
  if (left === right) return true;
  if (Array.isArray(left) && Array.isArray(right)) {
    return left.length === right.length && left.every((item, index) => deepEqual(item, right[index]));
  }
  const leftRecord = record(left);
  const rightRecord = record(right);
  if (!leftRecord || !rightRecord) return false;
  const leftKeys = Object.keys(leftRecord);
  const rightKeys = Object.keys(rightRecord);
  return leftKeys.length === rightKeys.length
    && leftKeys.every((key) => Object.prototype.hasOwnProperty.call(rightRecord, key) && deepEqual(leftRecord[key], rightRecord[key]));
}

function criterionProjection(value: unknown): CriterionProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate, true);
  const bindingId = candidate && record(candidate.binding_id);
  const sourceObservationRef = candidate && record(candidate.source_observation_ref);
  const provenance = candidate && record(candidate.provenance);
  const evidenceRefs = provenance && array(provenance.evidence_refs);
  if (!candidate || !currentState || !bindingId || !provenance || evidenceRefs === null) return null;
  const criterion = candidate.criterion === null ? null : record(candidate.criterion);
  if (candidate.criterion !== null && !criterion) return null;
  if (currentState.status === "AVAILABLE" && (currentState.applicability !== "APPLICABLE" || !criterion || currentState.reasons.length || !sourceObservationRef)) return null;
  if (currentState.status !== "AVAILABLE" && currentState.status !== "UNSUPPORTED" && criterion !== null) return null;
  if (!criterion) return {
    ...currentState, raw: candidate, bindingId, criterion: null, requirementId: null, metricId: null,
    comparator: null, inclusivity: null, bound: null, unit: null, contextIdentity: null,
    sourceObservationRef, bindingRuleRef: record(bindingId.binding_rule_ref), evidenceRefs,
  };
  const requirementRef = record(criterion.requirement_subject_ref);
  const criterionId = record(criterion.criterion_id);
  const metricRef = record(criterion.metric_ref);
  const context = record(criterion.context_identity);
  const bindingRuleRef = record(criterion.binding_rule_ref);
  const requirementId = requirementRef && text(requirementRef.requirement_id);
  const metricId = metricRef && text(metricRef.metric_id);
  const comparator = text(criterion.comparator);
  const inclusivity = text(criterion.inclusivity);
  const bound = text(criterion.bound);
  const unit = text(criterion.unit);
  const contextIdentity = context && text(context.normalized_text);
  const bindingRequirementRef = record(bindingId.requirement_subject_ref);
  const bindingSourceObservationRef = record(bindingId.source_observation_ref);
  const bindingRuleIdentity = record(bindingId.binding_rule_ref);
  if (!criterionId || !requirementId || !metricId || !comparator || !inclusivity || !bound || !unit || !contextIdentity || !bindingRuleRef
    || !bindingRequirementRef || !bindingSourceObservationRef || !bindingRuleIdentity
    || !deepEqual(criterionId, bindingId)
    || !deepEqual(requirementRef, bindingRequirementRef)
    || !deepEqual(criterion.source_observation_ref, bindingSourceObservationRef)
    || !deepEqual(sourceObservationRef, bindingSourceObservationRef)
    || !deepEqual(bindingRuleRef, bindingRuleIdentity)
    || !optionalIdentity(provenance, "requirement_subject_ref", bindingRequirementRef)
    || !optionalIdentity(provenance, "source_observation_ref", bindingSourceObservationRef)
    || !optionalIdentity(provenance, "binding_rule_ref", bindingRuleIdentity)) return null;
  return { ...currentState, raw: candidate, bindingId, criterion, requirementId, metricId, comparator, inclusivity, bound, unit, contextIdentity, sourceObservationRef, bindingRuleRef, evidenceRefs };
}

function observationProjection(value: unknown): ObservationProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate, true);
  const slotRef = candidate && record(candidate.slot_ref);
  const provenanceRefs = candidate && strings(candidate.provenance_refs);
  if (!candidate || !currentState || !slotRef || !provenanceRefs) return null;
  const observation = candidate.observation === null ? null : record(candidate.observation);
  if (candidate.observation !== null && !observation) return null;
  if (currentState.status === "AVAILABLE" && (currentState.applicability !== "APPLICABLE" || !observation || currentState.reasons.length)) return null;
  if (currentState.status !== "AVAILABLE" && observation !== null) return null;
  if (!observation) return { ...currentState, raw: candidate, slotRef, observation: null, observationId: null, observedValue: null, metricId: null, unit: null, contextIdentity: null, productRef: null, environmentRef: null, collectionRef: null, sourceKind: null, sourceRecordRef: null, provenanceRefs };
  const observationId = record(observation.observation_id);
  const metricRef = record(observation.metric_ref);
  const context = record(observation.context_identity);
  const productRef = record(observation.product_ref);
  const collectionRef = record(observation.collection_ref);
  const environmentRef = collectionRef && record(collectionRef.environment_ref);
  const provenance = record(observation.provenance);
  const observedValue = text(observation.observed_value);
  const metricId = metricRef && text(metricRef.metric_id);
  const unit = text(observation.unit);
  const contextIdentity = context && text(context.normalized_text);
  const sourceKind = text(observation.source_kind);
  const sourceRecordRef = provenance && text(provenance.source_record_ref);
  const slotCollectionRef = record(slotRef.collection_ref);
  const observationIdCollectionRef = observationId && record(observationId.collection_ref);
  const collectionProductRef = record(collectionRef?.product_ref);
  if (!observationId || !observedValue || !metricId || !unit || !contextIdentity || !productRef || !collectionRef || !environmentRef || !sourceKind || !sourceRecordRef
    || !slotCollectionRef || !observationIdCollectionRef || !collectionProductRef
    || !deepEqual(observation.slot_ref, slotRef)
    || !deepEqual(collectionRef, slotCollectionRef)
    || !deepEqual(observation.fixture_sequence, slotRef.fixture_sequence)
    || !deepEqual(observationIdCollectionRef, collectionRef)
    || !deepEqual(observationId.fixture_sequence, observation.fixture_sequence)
    || !deepEqual(productRef, collectionProductRef)
    || !deepEqual(sourceKind, collectionRef.source_kind)
    || !provenance
    || !optionalIdentity(provenance, "product_ref", productRef)
    || !optionalIdentity(provenance, "collection_ref", collectionRef)
    || !optionalIdentity(provenance, "fixture_sequence", observation.fixture_sequence)
    || !optionalIdentity(provenance, "declared_metric_ref", metricRef)
    || !optionalIdentity(provenance, "declared_unit", observation.unit)
    || !optionalIdentity(provenance, "declared_context_identity", context)
    || !optionalIdentity(provenance, "source_kind", sourceKind)) return null;
  return { ...currentState, raw: candidate, slotRef, observation, observationId, observedValue, metricId, unit, contextIdentity, productRef, environmentRef, collectionRef, sourceKind, sourceRecordRef, provenanceRefs };
}

function conformanceProjection(
  value: unknown,
  criterion: CriterionProjection | null,
  observation: ObservationProjection | null,
): ConformanceProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate, true);
  const conformanceId = candidate && record(candidate.conformance_id);
  const evaluatorRuleRef = candidate && record(candidate.evaluator_rule_ref);
  const evidenceRefs = candidate && array(candidate.evidence_refs);
  const explanation = candidate && text(candidate.explanation);
  const provenance = candidate && record(candidate.provenance);
  if (!candidate || !currentState || !conformanceId || !evaluatorRuleRef || evidenceRefs === null || !explanation || !provenance) return null;
  const outcome = candidate.outcome === null ? null : text(candidate.outcome);
  const criterionId = candidate.criterion_id === null ? null : record(candidate.criterion_id);
  const observationId = candidate.observation_id === null ? null : record(candidate.observation_id);
  if (candidate.criterion_id !== null && !criterionId || candidate.observation_id !== null && !observationId) return null;
  if (currentState.status === "AVAILABLE" && (currentState.applicability !== "APPLICABLE" || !criterionId || !observationId || currentState.reasons.length || !outcome || !["CONFORMS", "DOES_NOT_CONFORM"].includes(outcome))) return null;
  if (currentState.status !== "AVAILABLE" && outcome !== null) return null;
  const criterionBindingId = record(candidate.criterion_binding_id);
  const observationSlotRef = record(candidate.observation_slot_ref);
  const criterionRef = record(candidate.criterion_ref);
  const observationRef = record(candidate.observation_ref);
  if (!["dynamic_assessment_ref", "criterion_binding_id", "observation_slot_ref", "evaluator_rule_ref"].every((field) => hasOwn(conformanceId, field))
    || !hasOwn(provenance, "evaluator_rule_ref")
    || !deepEqual(conformanceId.dynamic_assessment_ref, candidate.dynamic_assessment_ref)
    || !deepEqual(conformanceId.criterion_binding_id, candidate.criterion_binding_id)
    || !deepEqual(conformanceId.observation_slot_ref, candidate.observation_slot_ref)
    || !deepEqual(conformanceId.evaluator_rule_ref, evaluatorRuleRef)
    || !deepEqual(provenance.evaluator_rule_ref, evaluatorRuleRef)) return null;
  if (criterion?.status === "AVAILABLE") {
    const selectedCriterionId = criterion.criterion && record(criterion.criterion.criterion_id);
    if (!criterionBindingId || !criterionId || !criterionRef || !selectedCriterionId
      || !deepEqual(criterionBindingId, criterion.bindingId)
      || !deepEqual(criterionId, selectedCriterionId)
      || !deepEqual(criterionRef.criterion_id, selectedCriterionId)
      || !hasOwn(provenance, "criterion_ref")
      || !deepEqual(provenance.criterion_ref, criterionRef)) return null;
  }
  if (observation?.status === "AVAILABLE") {
    const selectedObservationId = observation.observationId;
    if (!observationSlotRef || !observationId || !observationRef || !selectedObservationId
      || !deepEqual(observationSlotRef, observation.slotRef)
      || !deepEqual(observationId, selectedObservationId)
      || !deepEqual(observationRef.observation_id, selectedObservationId)
      || !hasOwn(provenance, "observation_ref")
      || !deepEqual(provenance.observation_ref, observationRef)) return null;
  }
  return { ...currentState, raw: candidate, conformanceId, outcome, explanation, criterionId, observationId, evidenceRefs, evaluatorRuleRef };
}

function featureProjection(
  value: unknown,
  index: number,
  profileId: JsonRecord,
  artifactRef: JsonRecord,
  sourceAssessmentRef: unknown,
  productRef: JsonRecord,
  targetKey: JsonRecord | null,
  criterion: CriterionProjection,
  observation: ObservationProjection,
  conformance: ConformanceProjection,
): FeatureProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate, true);
  const featureId = candidate && text(candidate.feature_id);
  const effect = candidate && text(candidate.effect);
  const availabilityPoint = candidate && text(candidate.availability_point);
  const explanation = candidate && text(candidate.explanation);
  const sourceRefs = candidate && array(candidate.source_refs);
  const evidenceRefs = candidate && array(candidate.evidence_refs);
  const provenanceRefs = candidate && array(candidate.provenance_refs);
  const ruleRefs = candidate && array(candidate.rule_refs);
  const featureEntryId = candidate && record(candidate.feature_entry_id);
  if (!candidate || !currentState || featureId !== peFeatureIds[index] || effect !== peFeatureEffects[index]
    || candidate.characteristic_id !== "PERFORMANCE_EFFICIENCY"
    || !featureEntryId || !availabilityPoint || !explanation || sourceRefs === null || evidenceRefs === null || provenanceRefs === null || ruleRefs === null
    || featureEntryId.feature_id !== featureId
    || !deepEqual(featureEntryId.profile_id, profileId)
    || !deepEqual(candidate.artifact_ref, artifactRef)
    || !deepEqual(candidate.source_assessment_ref, sourceAssessmentRef)
    || (index < 5 ? candidate.product_ref !== null : !deepEqual(candidate.product_ref, productRef))) return null;
  const typedValue = candidate.typed_value === null ? null : record(candidate.typed_value);
  if (candidate.typed_value !== null && !typedValue) return null;
  if (currentState.status === "AVAILABLE" && (currentState.applicability !== "APPLICABLE" || !typedValue)) return null;
  if (currentState.status !== "AVAILABLE" && typedValue !== null) return null;
  if (typedValue && !validFeatureValue(index, typedValue, targetKey, criterion, observation, conformance)) return null;
  return { ...currentState, raw: candidate, featureId, effect, typedValue, availabilityPoint, explanation, sourceRefs, evidenceRefs, provenanceRefs, ruleRefs };
}

function validFeatureValue(
  index: number,
  value: JsonRecord,
  targetKey: JsonRecord | null,
  criterion: CriterionProjection,
  observation: ObservationProjection,
  conformance: ConformanceProjection,
): boolean {
  if (index === 0) {
    const criterionRef = record(value.criterion_ref);
    const metricRef = record(value.metric_ref);
    const contextIdentity = record(value.context_identity);
    const selected = criterion.criterion;
    const selectedCriterionId = selected && record(selected.criterion_id);
    return !!criterionRef && !!metricRef && !!contextIdentity && !!selected && !!selectedCriterionId
      && !!text(value.comparator) && !!text(value.inclusivity) && !!text(value.exact_decimal_bound) && !!text(value.unit)
      && deepEqual(criterionRef.criterion_id, selectedCriterionId)
      && deepEqual(metricRef, selected.metric_ref)
      && value.comparator === selected.comparator
      && value.inclusivity === selected.inclusivity
      && value.exact_decimal_bound === selected.bound
      && value.unit === selected.unit
      && deepEqual(contextIdentity, selected.context_identity);
  }
  if (index >= 1 && index <= 3) {
    return !!record(value.metric_entry_ref)
      && exactFraction(value.exact_fraction_or_none) !== null
      && value.numeric_representation === "EXACT_FRACTION"
      && !!record(value.source_status);
  }
  if (index === 4) {
    const exactSource = value.source_exact_fraction_or_none;
    const valueTargetKey = record(value.target_key);
    return !!record(value.qb_metric_entry_ref)
      && !!text(value.source_metric_status)
      && !!text(value.source_metric_applicability)
      && (exactSource === null || exactFraction(exactSource) !== null)
      && (value.gate_decision === "TARGET_CLEAR" || value.gate_decision === "TARGET_CONFLICT")
      && !!valueTargetKey
      && Array.isArray(value.ordered_cross_result_refs)
      && (targetKey === null || deepEqual(valueTargetKey, targetKey));
  }
  if (index === 5) {
    const observationRef = record(value.observation_ref);
    const metricRef = record(value.metric_ref);
    const contextIdentity = record(value.context_identity);
    const selected = observation.observation;
    return !!observationRef && !!metricRef && !!contextIdentity && !!selected && !!observation.observationId
      && !!text(value.exact_decimal_value) && !!text(value.unit)
      && deepEqual(observationRef.observation_id, observation.observationId)
      && deepEqual(metricRef, selected.metric_ref)
      && value.exact_decimal_value === selected.observed_value
      && value.unit === selected.unit
      && deepEqual(contextIdentity, selected.context_identity);
  }
  if (index === 6) {
    const conformanceRef = record(value.conformance_ref);
    return !!conformanceRef
      && (value.outcome === "CONFORMS" || value.outcome === "DOES_NOT_CONFORM")
      && deepEqual(conformanceRef, conformance.conformanceId)
      && value.outcome === conformance.outcome;
  }
  return false;
}

function featureProfileProjection(
  value: unknown,
  criterion: CriterionProjection | null,
  observation: ObservationProjection | null,
  conformance: ConformanceProjection | null,
): FeatureProfileProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate);
  const profileId = candidate && record(candidate.profile_id);
  const characteristicId = candidate && text(candidate.characteristic_id);
  const registryRef = candidate && record(candidate.registry_ref);
  const mappingRuleRef = candidate && record(candidate.mapping_rule_ref);
  const artifactRef = candidate && record(candidate.artifact_ref);
  const sourceAssessmentRef = candidate && record(candidate.source_assessment_ref);
  const metricProfileRef = candidate && record(candidate.metric_profile_ref);
  const dynamicAssessmentRef = candidate && record(candidate.dynamic_assessment_ref);
  const productRef = candidate && record(candidate.product_ref);
  const processStateRef = candidate && record(candidate.process_state_ref);
  const featureValues = candidate && array(candidate.features);
  const provenance = candidate && record(candidate.provenance);
  if (!candidate || !currentState || !criterion || !observation || !conformance || !profileId || characteristicId !== "PERFORMANCE_EFFICIENCY"
    || !registryRef || !mappingRuleRef || !artifactRef || !sourceAssessmentRef || !metricProfileRef || !dynamicAssessmentRef
    || !productRef || !processStateRef || !featureValues || featureValues.length !== peFeatureIds.length || !provenance) return null;
  const identityPairs: Array<[unknown, unknown]> = [
    [profileId.artifact_ref, artifactRef],
    [profileId.source_assessment_ref, candidate.source_assessment_ref],
    [profileId.metric_profile_ref, candidate.metric_profile_ref],
    [profileId.dynamic_assessment_ref, candidate.dynamic_assessment_ref],
    [profileId.product_ref, productRef],
    [profileId.process_state_ref, processStateRef],
    [profileId.feature_registry_ref, registryRef],
    [profileId.mapping_rule_ref, mappingRuleRef],
  ];
  if (identityPairs.some(([left, right]) => !deepEqual(left, right))) return null;
  const criterionSubjectRef = candidate.criterion_subject_ref === null ? null : record(candidate.criterion_subject_ref);
  const targetKey = candidate.target_key === null ? null : record(candidate.target_key);
  if (candidate.criterion_subject_ref !== null && !criterionSubjectRef || candidate.target_key !== null && !targetKey) return null;
  if (criterion.status === "AVAILABLE" && (!deepEqual(criterion.bindingId.artifact_ref, artifactRef) || !deepEqual(criterion.criterion?.requirement_subject_ref, criterionSubjectRef))) return null;
  if (observation.status === "AVAILABLE" && !deepEqual(observation.productRef, productRef)) return null;
  if (!deepEqual(conformance.raw.dynamic_assessment_ref, dynamicAssessmentRef) || !deepEqual(conformance.raw.criterion_binding_id, criterion.bindingId)) return null;
  const features = featureValues.map((feature, index) => featureProjection(
    feature, index, profileId, artifactRef, sourceAssessmentRef, productRef, targetKey, criterion, observation, conformance,
  ));
  if (features.some((item) => item === null)) return null;
  const featureEntryRefs = (features as FeatureProjection[]).map((feature) => feature.raw.feature_entry_id);
  const provenancePairs: Array<[unknown, unknown]> = [
    [provenance.artifact_ref, artifactRef],
    [provenance.source_assessment_ref, sourceAssessmentRef],
    [provenance.metric_profile_ref, metricProfileRef],
    [provenance.dynamic_assessment_ref, dynamicAssessmentRef],
    [provenance.product_ref, productRef],
    [provenance.process_state_ref, processStateRef],
    [provenance.criterion_binding_ref, criterion.bindingId],
    [provenance.observation_resolution_ref, observation.slotRef],
    [provenance.conformance_assessment_ref, conformance.conformanceId],
    [provenance.ordered_feature_entry_refs, featureEntryRefs],
  ];
  if (provenancePairs.some(([left, right]) => !deepEqual(left, right))) return null;
  return { ...currentState, raw: candidate, profileId, characteristicId, criterionSubjectRef, targetKey, registryRef, mappingRuleRef, artifactRef, productRef, processStateRef, features: features as FeatureProjection[] };
}

function observedProjection(
  value: unknown,
  featureProfile: FeatureProfileProjection | null,
  criterion: CriterionProjection | null,
  observation: ObservationProjection | null,
  conformance: ConformanceProjection | null,
): ObservedProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate);
  const resultKind = candidate && text(candidate.result_kind);
  const characteristicId = candidate && text(candidate.characteristic_id);
  const numericRepresentation = candidate && text(candidate.numeric_representation);
  const scopeStatement = candidate && text(candidate.scope_statement);
  const calibrationStatus = candidate && text(candidate.calibration_status);
  const nonClaims = candidate && strings(candidate.non_claims);
  const provenance = candidate && record(candidate.provenance);
  const scope = candidate && record(candidate.scope);
  const assessmentId = candidate && record(candidate.assessment_id);
  const assessmentEventRef = candidate && record(candidate.assessment_event_ref);
  if (!candidate || !currentState || resultKind !== "OBSERVED_REFERENCE_INDICATOR" || characteristicId !== "PERFORMANCE_EFFICIENCY" || !numericRepresentation || !scopeStatement || !calibrationStatus || !nonClaims || !deepEqual(nonClaims, productQualityNonClaims) || !provenance || !scope || !assessmentId || !assessmentEventRef || !featureProfile) return null;
  if (candidate.prediction_value !== null || candidate.reliability !== null || candidate.uncertainty !== null) return null;
  const valueProjection = exactFraction(candidate.value);
  const observedValue = exactFraction(candidate.observed_value);
  const sourceConformanceOutcome = candidate.source_conformance_outcome === null ? null : text(candidate.source_conformance_outcome);
  if (currentState.status === "AVAILABLE" && (!valueProjection || !observedValue
    || !fractionInUnitInterval(candidate.value) || !fractionInUnitInterval(candidate.observed_value)
    || !deepEqual(candidate.value, candidate.observed_value)
    || numericRepresentation !== "EXACT_FRACTION" || !sourceConformanceOutcome)) return null;
  if (currentState.status !== "AVAILABLE" && (candidate.value !== null || candidate.observed_value !== null || sourceConformanceOutcome !== null || numericRepresentation !== "NONE")) return null;
  if (!deepEqual(candidate.feature_profile_ref, featureProfile.profileId)
    || !deepEqual(candidate.artifact_ref, featureProfile.artifactRef)
    || !deepEqual(candidate.product_ref, featureProfile.productRef)
    || !deepEqual(provenance.feature_profile_ref, featureProfile.profileId)
    || !deepEqual(provenance.product_ref, featureProfile.productRef)
    || !deepEqual(provenance.process_state_ref, featureProfile.processStateRef)
    || scope.characteristic_id !== "PERFORMANCE_EFFICIENCY"
    || scope.full_characteristic_coverage !== "NOT_ESTABLISHED"
    || !deepEqual(scope.product_ref, featureProfile.productRef)
    || !deepEqual(candidate.model_ref, provenance.model_ref)
    || !deepEqual(candidate.parameter_set_ref, provenance.parameter_set_ref)
    || !deepEqual(candidate.feature_refs, provenance.ordered_feature_refs)
    || !deepEqual(candidate.evidence_refs, provenance.source_evidence_refs)) return null;
  const eventArtifactRef = record(assessmentEventRef.artifact_ref);
  const eventProductRef = record(assessmentEventRef.product_ref);
  const sourceAssessmentRef = record(featureProfile.raw.source_assessment_ref);
  const artifactVersion = text(candidate.artifact_version);
  const productVersion = text(candidate.product_version);
  const assessmentVersion = text(candidate.product_quality_assessment_version);
  const sourceAssessmentVersion = text(candidate.source_assessment_version);
  if (!eventArtifactRef || !eventProductRef || !sourceAssessmentRef || !artifactVersion || !productVersion || !assessmentVersion || !sourceAssessmentVersion
    || !deepEqual(assessmentId.assessment_event_ref, assessmentEventRef)
    || !deepEqual(eventArtifactRef, candidate.artifact_ref)
    || !deepEqual(eventProductRef, candidate.product_ref)
    || artifactVersion !== record(candidate.artifact_ref)?.artifact_version
    || productVersion !== record(candidate.product_ref)?.product_version
    || assessmentVersion !== assessmentEventRef.assessment_event_version
    || sourceAssessmentVersion !== sourceAssessmentRef.assessment_version) return null;
  const provenanceRules = array(provenance.rule_refs);
  if (!provenanceRules || !provenanceRules.some((item) => deepEqual(item, candidate.procedure_rule_ref))) return null;
  const assessmentIdentityPairs: Array<[unknown, unknown]> = [
    [assessmentId.feature_profile_ref, featureProfile.profileId],
    [assessmentId.characteristic_id, characteristicId],
    [assessmentId.result_kind, resultKind],
    [assessmentId.model_ref, candidate.model_ref],
    [assessmentId.procedure_rule_ref, candidate.procedure_rule_ref],
    [assessmentId.parameter_set_ref, candidate.parameter_set_ref],
  ];
  if (assessmentIdentityPairs.some(([left, right]) => !deepEqual(left, right))) return null;
  if (criterion?.status === "AVAILABLE") {
    const selectedCriterionId = criterion.criterion && record(criterion.criterion.criterion_id);
    if (!selectedCriterionId || !deepEqual(record(scope.criterion_ref)?.criterion_id, selectedCriterionId)
      || !optionalIdentity(scope, "dynamic_metric_ref", criterion.criterion?.metric_ref)
      || !optionalIdentity(scope, "context_identity", criterion.criterion?.context_identity)
      || !optionalIdentity(scope, "unit", criterion.criterion?.unit)) return null;
  }
  if (observation?.status === "AVAILABLE" && (!deepEqual(record(scope.observation_ref)?.observation_id, observation.observationId)
    || !optionalIdentity(scope, "dynamic_metric_ref", observation.observation?.metric_ref)
    || !optionalIdentity(scope, "context_identity", observation.observation?.context_identity)
    || !optionalIdentity(scope, "unit", observation.observation?.unit)
    || !optionalIdentity(scope, "collection_ref", observation.collectionRef)
    || !optionalIdentity(scope, "environment_ref", observation.environmentRef))) return null;
  if (conformance?.status === "AVAILABLE" && (!deepEqual(scope.conformance_ref, conformance.conformanceId) || sourceConformanceOutcome !== conformance.outcome)) return null;
  return { ...currentState, raw: candidate, resultKind, characteristicId, value: valueProjection, observedValue, numericRepresentation, sourceConformanceOutcome, scopeStatement, calibrationStatus, nonClaims };
}

function predictionProjection(value: unknown, featureProfile: FeatureProfileProjection | null): PredictionProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate);
  const resultKind = candidate && text(candidate.result_kind);
  const characteristicId = candidate && text(candidate.characteristic_id);
  const numericRepresentation = candidate && text(candidate.numeric_representation);
  const predictorRef = candidate && record(candidate.predictor_ref);
  const parameterSetRef = candidate && record(candidate.parameter_set_ref);
  const calibrationStatus = candidate && text(candidate.calibration_status);
  const explanation = candidate && text(candidate.explanation);
  const provenance = candidate && record(candidate.provenance);
  const definition = provenance && record(provenance.predictor_definition);
  const provenanceParameterSet = provenance && record(provenance.parameter_set_ref);
  const inputTraces = provenance && array(provenance.input_traces);
  const selectedInputRefs = candidate && array(candidate.selected_input_refs);
  const contextInputs = candidate && array(candidate.context_inputs);
  const provenanceContext = provenance && array(provenance.context_inputs);
  const provenanceProfile = provenance && record(provenance.feature_profile_ref);
  const withheld = provenance?.withheld_reason_or_none === null ? null : text(provenance?.withheld_reason_or_none);
  if (!candidate || !currentState || resultKind !== "PREDICTED_PERFORMANCE_EFFICIENCY" || characteristicId !== "PERFORMANCE_EFFICIENCY" || !numericRepresentation || !predictorRef || !parameterSetRef || !calibrationStatus || !explanation || !provenance || !definition || !provenanceParameterSet || !inputTraces || !selectedInputRefs || !contextInputs || !provenanceContext || !provenanceProfile || !featureProfile || !hasOwn(provenance, "withheld_reason_or_none")) return null;
  const traceRefs = inputTraces.map((item) => record(item)?.feature_ref);
  if (!deepEqual(predictorRef, definition.predictor_ref) || !deepEqual(parameterSetRef, provenanceParameterSet)
    || calibrationStatus !== definition.calibration_status || !deepEqual(selectedInputRefs, traceRefs)
    || !deepEqual(contextInputs, provenanceContext) || !deepEqual(provenanceProfile, featureProfile.profileId)
    || !deepEqual(candidate.artifact_ref, featureProfile.artifactRef)
    || !deepEqual(candidate.product_ref, featureProfile.productRef)
    || !deepEqual(candidate.process_state_ref, featureProfile.processStateRef)
    || !deepEqual(provenanceProfile.artifact_ref, candidate.artifact_ref)
    || !deepEqual(provenanceProfile.product_ref, candidate.product_ref)
    || !deepEqual(provenanceProfile.process_state_ref, candidate.process_state_ref)
    || !deepEqual(parameterSetRef.predictor_ref, definition.predictor_ref)
    || !deepEqual(record(parameterSetRef.identity), definition.parameter_set_identity)
    || inputTraces.some((item) => {
      const featureRef = record(record(item)?.feature_ref);
      return !featureRef || !deepEqual(featureRef.profile_id, featureProfile.profileId);
    })) return null;
  const predictedValue = exactFraction(candidate.predicted_value);
  if (currentState.status === "AVAILABLE" && (currentState.applicability !== "APPLICABLE" || !predictedValue || !fractionInUnitInterval(candidate.predicted_value) || numericRepresentation !== "EXACT_FRACTION" || withheld !== null)) return null;
  if (currentState.status !== "AVAILABLE" && (candidate.predicted_value !== null || numericRepresentation !== "NONE" || withheld === null)) return null;
  return { ...currentState, raw: candidate, resultKind, characteristicId, predictedValue, numericRepresentation, predictorRef, parameterSetRef, calibrationStatus, explanation, withheldReason: withheld };
}

export function selectProductQualityPage(response: CanonicalAnalyzeResponse): ProductQualityProjection {
  const availability = selectSectionAvailability(response, "product_quality");
  if (!availability) return { kind: "MALFORMED" };
  if (availability.availability === "UNAVAILABLE") {
    return availability.reasonCode ? { kind: "UNAVAILABLE", reasonCode: availability.reasonCode } : { kind: "MALFORMED" };
  }
  const selected = selectCurrentResultRecords(response);
  if (!selected) return { kind: "MALFORMED" };
  const criterion = criterionProjection(selected.records.criterion_binding);
  const observation = observationProjection(selected.records.observation_resolution);
  const conformance = conformanceProjection(selected.records.conformance, criterion, observation);
  const featureProfile = featureProfileProjection(selected.records.feature_profile, criterion, observation, conformance);
  const observed = observedProjection(
    selected.revision === "REASSESSMENT_V2" ? selected.records.product_quality_assessment : selected.records.observed_product_quality,
    featureProfile,
    criterion,
    observation,
    conformance,
  );
  let prediction: PredictionPresentation = { kind: "ABSENT" };
  if (selected.revision === "CONTROLLED_DEMO_V1" && selected.records.prediction !== null) {
    const projectedPrediction = predictionProjection(selected.records.prediction, featureProfile);
    prediction = projectedPrediction ? { kind: "PRESENT", value: projectedPrediction } : { kind: "MALFORMED" };
  }
  return {
    kind: "AVAILABLE",
    revision: selected.revision,
    criterion,
    observation,
    conformance,
    featureProfile,
    observed,
    prediction,
  };
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

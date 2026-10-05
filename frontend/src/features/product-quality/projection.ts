import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactValueData } from "../../components/scientific";
import { selectSectionAvailability } from "../results/projection";

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
      prediction: PredictionProjection | null;
      predictionCurrent: boolean;
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
  return status && statuses.has(status) && applicability && applicabilities.has(applicability) && reasons !== null
    ? { status, applicability, reasons }
    : null;
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
  if (!candidate || !currentState || !bindingId || evidenceRefs === null) return null;
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
  if (!requirementId || !metricId || !comparator || !inclusivity || !bound || !unit || !contextIdentity || !bindingRuleRef) return null;
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
  if (!observationId || !observedValue || !metricId || !unit || !contextIdentity || !productRef || !collectionRef || !environmentRef || !sourceKind || !sourceRecordRef) return null;
  return { ...currentState, raw: candidate, slotRef, observation, observationId, observedValue, metricId, unit, contextIdentity, productRef, environmentRef, collectionRef, sourceKind, sourceRecordRef, provenanceRefs };
}

function conformanceProjection(value: unknown): ConformanceProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate, true);
  const conformanceId = candidate && record(candidate.conformance_id);
  const evaluatorRuleRef = candidate && record(candidate.evaluator_rule_ref);
  const evidenceRefs = candidate && array(candidate.evidence_refs);
  const explanation = candidate && text(candidate.explanation);
  if (!candidate || !currentState || !conformanceId || !evaluatorRuleRef || evidenceRefs === null || !explanation) return null;
  const outcome = candidate.outcome === null ? null : text(candidate.outcome);
  const criterionId = candidate.criterion_id === null ? null : record(candidate.criterion_id);
  const observationId = candidate.observation_id === null ? null : record(candidate.observation_id);
  if (candidate.criterion_id !== null && !criterionId || candidate.observation_id !== null && !observationId) return null;
  if (currentState.status === "AVAILABLE" && (currentState.applicability !== "APPLICABLE" || !criterionId || !observationId || currentState.reasons.length || !outcome || !["CONFORMS", "DOES_NOT_CONFORM"].includes(outcome))) return null;
  if (currentState.status !== "AVAILABLE" && outcome !== null) return null;
  return { ...currentState, raw: candidate, conformanceId, outcome, explanation, criterionId, observationId, evidenceRefs, evaluatorRuleRef };
}

function featureProjection(value: unknown, index: number): FeatureProjection | null {
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
  if (!candidate || !currentState || featureId !== peFeatureIds[index] || effect !== peFeatureEffects[index]
    || !availabilityPoint || !explanation || sourceRefs === null || evidenceRefs === null || provenanceRefs === null || ruleRefs === null) return null;
  const typedValue = candidate.typed_value === null ? null : record(candidate.typed_value);
  if (candidate.typed_value !== null && !typedValue) return null;
  if (currentState.status === "AVAILABLE" && (currentState.applicability !== "APPLICABLE" || !typedValue)) return null;
  if (currentState.status !== "AVAILABLE" && typedValue !== null) return null;
  return { ...currentState, raw: candidate, featureId, effect, typedValue, availabilityPoint, explanation, sourceRefs, evidenceRefs, provenanceRefs, ruleRefs };
}

function featureProfileProjection(value: unknown): FeatureProfileProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate);
  const profileId = candidate && record(candidate.profile_id);
  const characteristicId = candidate && text(candidate.characteristic_id);
  const registryRef = candidate && record(candidate.registry_ref);
  const mappingRuleRef = candidate && record(candidate.mapping_rule_ref);
  const artifactRef = candidate && record(candidate.artifact_ref);
  const productRef = candidate && record(candidate.product_ref);
  const processStateRef = candidate && record(candidate.process_state_ref);
  const featureValues = candidate && array(candidate.features);
  if (!candidate || !currentState || !profileId || characteristicId !== "PERFORMANCE_EFFICIENCY" || !registryRef || !mappingRuleRef || !artifactRef || !productRef || !processStateRef || !featureValues || featureValues.length !== peFeatureIds.length) return null;
  const features = featureValues.map(featureProjection);
  if (features.some((item) => item === null)) return null;
  const criterionSubjectRef = candidate.criterion_subject_ref === null ? null : record(candidate.criterion_subject_ref);
  const targetKey = candidate.target_key === null ? null : record(candidate.target_key);
  if (candidate.criterion_subject_ref !== null && !criterionSubjectRef || candidate.target_key !== null && !targetKey) return null;
  return { ...currentState, raw: candidate, profileId, characteristicId, criterionSubjectRef, targetKey, registryRef, mappingRuleRef, artifactRef, productRef, processStateRef, features: features as FeatureProjection[] };
}

function observedProjection(value: unknown): ObservedProjection | null {
  const candidate = record(value);
  const currentState = candidate && state(candidate);
  const resultKind = candidate && text(candidate.result_kind);
  const characteristicId = candidate && text(candidate.characteristic_id);
  const numericRepresentation = candidate && text(candidate.numeric_representation);
  const scopeStatement = candidate && text(candidate.scope_statement);
  const calibrationStatus = candidate && text(candidate.calibration_status);
  const nonClaims = candidate && strings(candidate.non_claims);
  if (!candidate || !currentState || resultKind !== "OBSERVED_REFERENCE_INDICATOR" || characteristicId !== "PERFORMANCE_EFFICIENCY" || !numericRepresentation || !scopeStatement || !calibrationStatus || !nonClaims || !deepEqual(nonClaims, productQualityNonClaims)) return null;
  if (candidate.prediction_value !== null || candidate.reliability !== null || candidate.uncertainty !== null) return null;
  const valueProjection = exactFraction(candidate.value);
  const observedValue = exactFraction(candidate.observed_value);
  const sourceConformanceOutcome = candidate.source_conformance_outcome === null ? null : text(candidate.source_conformance_outcome);
  if (currentState.status === "AVAILABLE" && (currentState.applicability !== "APPLICABLE" || !valueProjection || !observedValue || numericRepresentation !== "EXACT_FRACTION" || !sourceConformanceOutcome)) return null;
  if (currentState.status !== "AVAILABLE" && (candidate.value !== null || candidate.observed_value !== null || sourceConformanceOutcome !== null || numericRepresentation !== "NONE")) return null;
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
  if (!candidate || !currentState || resultKind !== "PREDICTED_PERFORMANCE_EFFICIENCY" || characteristicId !== "PERFORMANCE_EFFICIENCY" || !numericRepresentation || !predictorRef || !parameterSetRef || !calibrationStatus || !explanation || !provenance || !definition || !provenanceParameterSet || !inputTraces || !selectedInputRefs || !contextInputs || !provenanceContext || !provenanceProfile || !featureProfile) return null;
  const traceRefs = inputTraces.map((item) => record(item)?.feature_ref);
  if (!deepEqual(predictorRef, definition.predictor_ref) || !deepEqual(parameterSetRef, provenanceParameterSet)
    || calibrationStatus !== definition.calibration_status || !deepEqual(selectedInputRefs, traceRefs)
    || !deepEqual(contextInputs, provenanceContext) || !deepEqual(provenanceProfile, featureProfile.profileId)) return null;
  const predictedValue = exactFraction(candidate.predicted_value);
  if (currentState.status === "AVAILABLE" && (currentState.applicability !== "APPLICABLE" || !predictedValue || !fractionInUnitInterval(candidate.predicted_value) || numericRepresentation !== "EXACT_FRACTION" || withheld !== null)) return null;
  if (currentState.status !== "AVAILABLE" && (candidate.predicted_value !== null || numericRepresentation !== "NONE" || withheld === null)) return null;
  return { ...currentState, raw: candidate, resultKind, characteristicId, predictedValue, numericRepresentation, predictorRef, parameterSetRef, calibrationStatus, explanation, withheldReason: withheld };
}

function currentRecords(response: CanonicalAnalyzeResponse): { revision: "CONTROLLED_DEMO_V1" | "REASSESSMENT_V2"; records: JsonRecord; predictionCurrent: boolean } | null {
  const fullModel = record(response.full_model);
  if (!fullModel) return null;
  if (response.analysis_case === "CONTROLLED_DEMO") return { revision: "CONTROLLED_DEMO_V1", records: fullModel, predictionCurrent: true };
  if (response.analysis_case !== "REASSESSMENT") return null;
  const reassessment = record(fullModel.reassessment);
  const refs = reassessment && array(reassessment.produced_result_refs);
  const results = reassessment && array(reassessment.produced_results);
  const context = reassessment && record(reassessment.context);
  const provenance = reassessment && record(reassessment.provenance);
  const childArtifact = context && record(context.child_artifact_ref);
  const provenanceChild = provenance && record(provenance.child_artifact_ref);
  if (!reassessment || !refs || !results || refs.length !== results.length || !childArtifact || !provenanceChild || !deepEqual(childArtifact, provenanceChild)) return null;
  const indexes = refs.flatMap((item, index) => record(item)?.result_family === "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH" ? [index] : []);
  if (indexes.length !== 1) return null;
  const ref = record(refs[indexes[0]]);
  const result = record(results[indexes[0]]);
  const refArtifact = ref && record(ref.artifact_ref);
  const resultArtifact = result && record(result.artifact_ref);
  if (!ref || !result || !refArtifact || !resultArtifact || !deepEqual(refArtifact, resultArtifact) || !deepEqual(resultArtifact, childArtifact)) return null;
  return { revision: "REASSESSMENT_V2", records: result, predictionCurrent: false };
}

export function selectProductQualityPage(response: CanonicalAnalyzeResponse): ProductQualityProjection {
  const availability = selectSectionAvailability(response, "product_quality");
  if (!availability) return { kind: "MALFORMED" };
  if (availability.availability === "UNAVAILABLE") {
    return availability.reasonCode ? { kind: "UNAVAILABLE", reasonCode: availability.reasonCode } : { kind: "MALFORMED" };
  }
  const selected = currentRecords(response);
  if (!selected) return { kind: "MALFORMED" };
  const featureProfile = featureProfileProjection(selected.records.feature_profile);
  return {
    kind: "AVAILABLE",
    revision: selected.revision,
    criterion: criterionProjection(selected.records.criterion_binding),
    observation: observationProjection(selected.records.observation_resolution),
    conformance: conformanceProjection(selected.records.conformance),
    featureProfile,
    observed: observedProjection(selected.revision === "REASSESSMENT_V2" ? selected.records.product_quality_assessment : selected.records.observed_product_quality),
    prediction: selected.predictionCurrent && selected.records.prediction !== null
      ? predictionProjection(selected.records.prediction, featureProfile)
      : null,
    predictionCurrent: selected.predictionCurrent,
  };
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

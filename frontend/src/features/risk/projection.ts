import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactValueData } from "../../components/scientific";
import { selectProductQualityPage } from "../product-quality/projection";
import { selectCurrentResultRecords, type JsonRecord } from "../results/currentVersion";
import { selectSectionAvailability } from "../results/projection";

const fullModelStatuses = new Set([
  "AVAILABLE", "NOT_APPLICABLE", "UNAVAILABLE", "UNKNOWN", "UNRESOLVED", "UNSUPPORTED",
]);
const problemNonClaims = ["NC-D-001", "NC-D-002", "NC-D-003", "NC-D-004", "NC-D-005", "NC-D-006"];
export const relationNonClaims = ["NC-RDQ-001", "NC-RDQ-002", "NC-RDQ-003", "NC-RDQ-004", "NC-RDQ-005"] as const;
export const categoricalRiskNonClaims = [
  "NC-RISK-001", "NC-RISK-002", "NC-RISK-003", "NC-RISK-004", "NC-RISK-005",
  "NC-RISK-006", "NC-RISK-007", "NC-RISK-008", "NC-RISK-009",
] as const;
export const quantitativeRiskNonClaims = [
  "NC-Q-RISK-001", "NC-Q-RISK-002", "NC-Q-RISK-003",
  "NC-Q-RISK-004", "NC-Q-RISK-005", "NC-Q-RISK-006",
] as const;
export const operandKinds = ["RHO", "PROBABILITY", "IMPACT", "CONTEXT_FACTOR"] as const;

interface ScientificState {
  status: string;
  applicability: string;
}

export interface ProblemProjection extends ScientificState {
  raw: JsonRecord;
  problemId: JsonRecord;
  problemKind: string;
  defectType: string;
  conflictClass: string;
  conflictSubtype: string;
  participantRefs: JsonRecord[];
  sourceObservationRefs: JsonRecord[];
  comparisonKey: JsonRecord;
  operandRefs: JsonRecord[];
  evidenceRefs: unknown[];
  diagnosticRefs: unknown[];
  explanation: string;
  nonClaims: string[];
}

export interface ResolutionProjection extends ScientificState {
  raw: JsonRecord;
  resolutionId: JsonRecord;
  sourceClaimRef: JsonRecord;
  disposition: string | null;
  problem: ProblemProjection | null;
  explanation: string;
  reason: string;
  evidenceRefs: unknown[];
  provenanceRefs: unknown[];
}

export interface PopulationProjection extends ScientificState {
  raw: JsonRecord;
  populationId: JsonRecord;
  members: unknown[];
  populationComplete: boolean;
  problemResolutionRefs: unknown[];
  unresolvedResolutionRefs: unknown[];
}

export interface RelationProjection extends ScientificState {
  raw: JsonRecord;
  relationId: JsonRecord;
  problemResolutionRef: JsonRecord;
  problemRef: JsonRecord | null;
  characteristicId: string;
  relationKind: string | null;
  rationale: string;
  reason: string;
  calibrationStatus: string;
  nonClaims: string[];
}

export interface CategoricalRiskProjection extends ScientificState {
  raw: JsonRecord;
  riskAssessmentId: JsonRecord;
  assessmentEventRef: JsonRecord;
  subject: JsonRecord;
  characteristicId: string;
  classification: string | null;
  riskStatement: string;
  explanation: string;
  productQualityContext: JsonRecord;
  calibrationStatus: string;
  nonClaims: string[];
}

export interface OperandProjection {
  raw: JsonRecord;
  operandId: JsonRecord;
  kind: string;
  state: string;
  value: ExactValueData | null;
  sourceRef: JsonRecord;
  sourceOrRationale: string;
  calibrationStatus: string;
  governingContractRef: JsonRecord;
  contextRef: JsonRecord | null;
}

export interface QuantitativeRiskProjection {
  raw: JsonRecord;
  assessmentId: JsonRecord;
  resultKind: string;
  state: "AVAILABLE" | "CALCULATION_WITHHELD";
  scope: string;
  characteristicId: string;
  operands: OperandProjection[];
  numericRepresentation: string;
  localRisk: ExactValueData | null;
  calibrationStatuses: string[];
  governingContractRef: JsonRecord;
  calculationRuleRef: JsonRecord;
  calculationRule: string;
  explanation: string;
  nonClaims: string[];
}

export type ProjectedRecord<T> = { kind: "VALID"; value: T } | { kind: "MALFORMED"; raw: unknown };
export type QuantitativePresentation =
  | { kind: "REASSESSMENT_ABSENT" }
  | { kind: "RECORDS"; records: ProjectedRecord<QuantitativeRiskProjection>[] };

export type RiskPageProjection =
  | { kind: "UNAVAILABLE"; reasonCode: string }
  | { kind: "MALFORMED" }
  | {
    kind: "AVAILABLE";
    revision: "CONTROLLED_DEMO_V1" | "REASSESSMENT_V2";
    resolutions: ProjectedRecord<ResolutionProjection>[];
    population: ProjectedRecord<PopulationProjection>;
    relations: ProjectedRecord<RelationProjection>[];
    categorical: ProjectedRecord<CategoricalRiskProjection>[];
    quantitative: QuantitativePresentation;
  };

function record(value: unknown): JsonRecord | null {
  return typeof value === "object" && value !== null && !Array.isArray(value) ? value as JsonRecord : null;
}

function array(value: unknown): unknown[] | null {
  return Array.isArray(value) ? value : null;
}

function text(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function strings(value: unknown): string[] | null {
  return Array.isArray(value) && value.every((item) => typeof item === "string") ? value : null;
}

function deepEqual(left: unknown, right: unknown): boolean {
  return JSON.stringify(left) === JSON.stringify(right);
}

function hasOwn(value: JsonRecord, key: string): boolean {
  return Object.prototype.hasOwnProperty.call(value, key);
}

function state(value: JsonRecord): ScientificState | null {
  const status = text(value.status);
  const applicability = text(value.applicability);
  if (!status || !applicability || !fullModelStatuses.has(status)) return null;
  if (status === "AVAILABLE" && applicability !== "APPLICABLE") return null;
  if (status === "NOT_APPLICABLE" && applicability !== "NOT_APPLICABLE") return null;
  if (!["AVAILABLE", "NOT_APPLICABLE"].includes(status) && !["APPLICABLE", "UNKNOWN"].includes(applicability)) return null;
  return { status, applicability };
}

function exactFraction(value: unknown): ExactValueData | null {
  const candidate = record(value);
  const numerator = candidate?.numerator;
  const denominator = candidate?.denominator;
  if (!Number.isSafeInteger(numerator) || !Number.isSafeInteger(denominator)
    || (denominator as number) <= 0 || (numerator as number) < 0 || (numerator as number) > (denominator as number)) return null;
  return { numerator: String(numerator), denominator: String(denominator) };
}

function contextMatches(value: JsonRecord, artifactRef: unknown, assessmentRef: unknown, snapshotId: unknown): boolean {
  return deepEqual(value.artifact_ref, artifactRef)
    && deepEqual(value.source_assessment_ref, assessmentRef)
    && deepEqual(value.source_snapshot_id, snapshotId)
    && deepEqual(record(value.source_assessment_ref)?.artifact_ref, artifactRef);
}

function projectProblem(value: unknown): ProblemProjection | null {
  const raw = record(value);
  const currentState = raw && state(raw);
  const problemId = raw && record(raw.problem_id);
  const targetRef = raw && record(raw.target_ref);
  const participants = raw && array(raw.participant_refs)?.map(record);
  const observations = raw && array(raw.source_observation_refs)?.map(record);
  const operands = raw && array(raw.operand_refs)?.map(record);
  const comparisonKey = raw && record(raw.comparison_key);
  const provenance = raw && record(raw.provenance);
  const evidenceRefs = raw && array(raw.evidence_refs);
  const diagnosticRefs = raw && array(raw.diagnostic_refs);
  const nonClaims = raw && strings(raw.non_claims);
  const explanation = raw && text(raw.explanation);
  if (!raw || !currentState || currentState.status !== "AVAILABLE" || currentState.applicability !== "APPLICABLE"
    || !problemId || !targetRef || !comparisonKey || !provenance || !evidenceRefs || !diagnosticRefs || !nonClaims || !explanation
    || !participants || participants.length !== 2 || participants.some((item) => item === null)
    || !observations || observations.length !== 2 || observations.some((item) => item === null)
    || !operands || operands.length !== 2 || operands.some((item) => item === null)
    || raw.problem_kind !== "CONFIRMED_SUPPORTED_PROBLEM"
    || raw.defect_type !== "SPECIFICATION_INCONSISTENCY"
    || raw.conflict_class !== "LOGICAL_CONFLICT"
    || raw.conflict_subtype !== "DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY"
    || !deepEqual(nonClaims, problemNonClaims)) return null;
  const participantRecords = participants as JsonRecord[];
  const observationRecords = observations as JsonRecord[];
  const operandRecords = operands as JsonRecord[];
  if (!deepEqual(targetRef.artifact_ref, raw.artifact_ref)
    || !contextMatches(raw, raw.artifact_ref, raw.source_assessment_ref, raw.source_snapshot_id)
    || !deepEqual(problemId.artifact_ref, raw.artifact_ref)
    || !deepEqual(problemId.source_assessment_ref, raw.source_assessment_ref)
    || !deepEqual(problemId.source_snapshot_id, raw.source_snapshot_id)
    || !deepEqual(problemId.source_cross_result_ref, raw.source_cross_result_ref)
    || !deepEqual(problemId.problem_rule_ref, raw.rule_ref)
    || participantRecords.some((item) => !deepEqual(item.artifact_ref, raw.artifact_ref))
    || observationRecords.some((item, index) => item.requirement_id !== participantRecords[index].requirement_id)
    || operandRecords[0].position !== "LEFT" || operandRecords[1].position !== "RIGHT"
    || operandRecords.some((item, index) => !deepEqual(item.source_cross_result_ref, raw.source_cross_result_ref)
      || !deepEqual(item.source_observation_ref, observationRecords[index]))) return null;
  const provenancePairs: Array<[unknown, unknown]> = [
    [provenance.source_cross_result_ref, raw.source_cross_result_ref],
    [provenance.source_snapshot_id, raw.source_snapshot_id],
    [provenance.participant_refs, raw.participant_refs],
    [provenance.source_observation_refs, raw.source_observation_refs],
    [provenance.comparison_key, raw.comparison_key],
    [provenance.exact_operand_refs, raw.operand_refs],
    [provenance.ordered_cross_evidence_refs, raw.evidence_refs],
    [provenance.diagnostic_refs, raw.diagnostic_refs],
    [provenance.problem_rule_ref, raw.rule_ref],
  ];
  if (provenancePairs.some(([left, right]) => !deepEqual(left, right))) return null;
  return {
    ...currentState, raw, problemId, problemKind: raw.problem_kind as string, defectType: raw.defect_type as string,
    conflictClass: raw.conflict_class as string, conflictSubtype: raw.conflict_subtype as string,
    participantRefs: participantRecords, sourceObservationRefs: observationRecords, comparisonKey,
    operandRefs: operandRecords, evidenceRefs, diagnosticRefs, explanation, nonClaims,
  };
}

export function projectResolution(value: unknown): ResolutionProjection | null {
  const raw = record(value);
  const currentState = raw && state(raw);
  const resolutionId = raw && record(raw.resolution_id);
  const sourceClaimRef = raw && record(raw.source_claim_ref);
  const reasons = raw && strings(raw.reasons);
  const evidenceRefs = raw && array(raw.evidence_refs);
  const provenanceRefs = raw && array(raw.provenance_refs);
  const explanation = raw && text(raw.explanation);
  if (!raw || !currentState || !resolutionId || !sourceClaimRef || !reasons || reasons.length !== 1
    || !evidenceRefs || !provenanceRefs || !explanation || !hasOwn(raw, "disposition") || !hasOwn(raw, "problem")
    || !deepEqual(resolutionId.artifact_ref, raw.artifact_ref)
    || !deepEqual(resolutionId.source_assessment_ref, raw.source_assessment_ref)
    || !deepEqual(resolutionId.source_snapshot_id, raw.source_snapshot_id)
    || !deepEqual(resolutionId.source_claim_ref, sourceClaimRef)
    || !deepEqual(resolutionId.problem_rule_ref, raw.rule_ref)
    || !contextMatches(raw, raw.artifact_ref, raw.source_assessment_ref, raw.source_snapshot_id)) return null;

  const disposition = raw.disposition === null ? null : text(raw.disposition);
  let problem: ProblemProjection | null = null;
  if (currentState.status === "AVAILABLE") {
    if (disposition === "CONFIRMED_SUPPORTED_PROBLEM") {
      problem = projectProblem(raw.problem);
      if (!problem || !contextMatches(problem.raw, raw.artifact_ref, raw.source_assessment_ref, raw.source_snapshot_id)
        || !deepEqual(problem.raw.rule_ref, raw.rule_ref)) return null;
    } else if (disposition === "NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE") {
      if (raw.problem !== null) return null;
    } else return null;
  } else if (raw.disposition !== null || raw.problem !== null) return null;
  return { ...currentState, raw, resolutionId, sourceClaimRef, disposition, problem, explanation, reason: reasons[0], evidenceRefs, provenanceRefs };
}

export function projectPopulation(value: unknown, resolutions: ResolutionProjection[]): PopulationProjection | null {
  const raw = record(value);
  const currentState = raw && state(raw);
  const populationId = raw && record(raw.population_id);
  const members = raw && array(raw.members);
  const resolutionRefs = raw && array(raw.problem_resolution_refs);
  const unresolvedRefs = raw && array(raw.unresolved_resolution_refs);
  const sourceQb = raw && record(raw.source_qb_assessment_ref);
  if (!raw || !currentState || !populationId || !members || !resolutionRefs || !unresolvedRefs || !sourceQb
    || typeof raw.population_complete !== "boolean"
    || !contextMatches(raw, raw.artifact_ref, raw.source_assessment_ref, raw.source_snapshot_id)
    || !deepEqual(populationId.artifact_ref, raw.artifact_ref)
    || !deepEqual(populationId.source_assessment_ref, raw.source_assessment_ref)
    || !deepEqual(populationId.source_snapshot_id, raw.source_snapshot_id)
    || !deepEqual(populationId.problem_rule_ref, raw.rule_ref)
    || !deepEqual(sourceQb.artifact_ref, raw.artifact_ref)
    || !deepEqual(sourceQb.assessment_ref, raw.source_assessment_ref)
    || !deepEqual(sourceQb.snapshot_id, raw.source_snapshot_id)) return null;
  if (currentState.status === "AVAILABLE" && raw.population_complete !== true) return null;
  if (currentState.status === "NOT_APPLICABLE" && (raw.population_complete !== true || members.length !== 0)) return null;
  if (["UNKNOWN", "UNRESOLVED"].includes(currentState.status) && raw.population_complete !== false) return null;
  const expectedResolutionRefs = resolutions.map((item) => ({ resolution_id: item.resolutionId }));
  if (!deepEqual(resolutionRefs, expectedResolutionRefs)) return null;
  const confirmedRefs = resolutions.flatMap((item) => item.problem ? [{ problem_id: item.problem.problemId }] : []);
  if (members.some((item) => !confirmedRefs.some((candidate) => deepEqual(candidate, item)))) return null;
  const unresolvedCandidates = resolutions.filter((item) => item.status !== "AVAILABLE").map((item) => ({ resolution_id: item.resolutionId }));
  if (unresolvedRefs.some((item) => !unresolvedCandidates.some((candidate) => deepEqual(candidate, item)))) return null;
  return { ...currentState, raw, populationId, members, populationComplete: raw.population_complete, problemResolutionRefs: resolutionRefs, unresolvedResolutionRefs: unresolvedRefs };
}

export function projectRelation(value: unknown, resolutions: ResolutionProjection[], population: PopulationProjection): RelationProjection | null {
  const raw = record(value);
  const currentState = raw && state(raw);
  const relationId = raw && record(raw.relation_id);
  const resolutionRef = raw && record(raw.problem_resolution_ref);
  const problemRef = raw?.problem_ref === null ? null : record(raw?.problem_ref);
  const provenance = raw && record(raw.provenance);
  const reasons = raw && strings(raw.reasons);
  const rationale = raw && text(raw.rationale);
  const calibration = raw && text(raw.calibration_status);
  const nonClaims = raw && strings(raw.non_claims);
  const resolution = resolutionRef && resolutions.find((item) => deepEqual(resolutionRef, { resolution_id: item.resolutionId }));
  if (!raw || !currentState || !relationId || !resolutionRef || raw.problem_ref !== null && !problemRef || !provenance
    || !reasons || reasons.length !== 1 || !rationale || !calibration || !nonClaims || !resolution
    || raw.characteristic_id !== "PERFORMANCE_EFFICIENCY"
    || calibration !== "PROVISIONAL_NOT_CALIBRATED" || !deepEqual(nonClaims, relationNonClaims)
    || !contextMatches(raw, population.raw.artifact_ref, population.raw.source_assessment_ref, population.raw.source_snapshot_id)
    || !deepEqual(relationId.problem_resolution_ref, resolutionRef)
    || !deepEqual(relationId.problem_ref, problemRef)
    || relationId.characteristic_id !== raw.characteristic_id
    || !deepEqual(relationId.relation_rule_ref, raw.rule_ref)) return null;
  const relationKind = raw.relation_kind === null ? null : text(raw.relation_kind);
  if (currentState.status === "AVAILABLE") {
    if (currentState.applicability !== "APPLICABLE" || relationKind !== "BOUNDED_RISK_RELEVANCE" || !problemRef
      || !resolution.problem || !deepEqual(problemRef, { problem_id: resolution.problem.problemId })) return null;
  } else if (raw.relation_kind !== null) return null;
  const provenancePairs: Array<[unknown, unknown]> = [
    [provenance.problem_resolution_ref, resolutionRef], [provenance.problem_ref, problemRef],
    [provenance.characteristic_id, raw.characteristic_id], [provenance.relation_rule_ref, raw.rule_ref],
    [provenance.rationale_code, reasons[0]], [provenance.evidence_refs, raw.evidence_refs],
  ];
  if (provenancePairs.some(([left, right]) => !deepEqual(left, right))) return null;
  return { ...currentState, raw, relationId, problemResolutionRef: resolutionRef, problemRef, characteristicId: raw.characteristic_id, relationKind, rationale, reason: reasons[0], calibrationStatus: calibration, nonClaims };
}

function expectedProductQualityContext(response: CanonicalAnalyzeResponse, selected: ReturnType<typeof selectCurrentResultRecords>): JsonRecord | null {
  const productQuality = selectProductQualityPage(response);
  if (!selected || productQuality.kind !== "AVAILABLE" || !productQuality.featureProfile) return null;
  const raw = record(selected.revision === "REASSESSMENT_V2"
    ? selected.records.product_quality_assessment
    : selected.records.observed_product_quality);
  const currentState = raw && state(raw);
  const assessmentId = raw && record(raw.assessment_id);
  const scope = raw && record(raw.scope);
  const productRef = raw && record(raw.product_ref);
  if (!raw || !currentState || !assessmentId || !scope || !productRef
    || raw.result_kind !== "OBSERVED_REFERENCE_INDICATOR"
    || scope.characteristic_id !== "PERFORMANCE_EFFICIENCY"
    || !deepEqual(scope.product_ref, productRef)
    || !deepEqual(raw.artifact_ref, productQuality.featureProfile.artifactRef)
    || !deepEqual(productRef, productQuality.featureProfile.productRef)
    || !deepEqual(raw.feature_profile_ref, productQuality.featureProfile.profileId)) return null;
  return {
    assessment_ref: { assessment_id: assessmentId, product_quality_assessment_version: raw.product_quality_assessment_version },
    status: currentState.status,
    applicability: currentState.applicability,
    result_kind: raw.result_kind,
    scope_ref: scope,
    product_ref: productRef,
  };
}

export function projectCategoricalRisk(
  value: unknown,
  resolutions: ResolutionProjection[],
  population: PopulationProjection,
  relations: RelationProjection[],
  productQualityContext: JsonRecord | null,
): CategoricalRiskProjection | null {
  const raw = record(value);
  const currentState = raw && state(raw);
  const riskId = raw && record(raw.risk_assessment_id);
  const event = raw && record(raw.assessment_event_ref);
  const subject = raw && record(raw.subject);
  const provenance = raw && record(raw.provenance);
  const riskStatement = raw && text(raw.risk_statement);
  const explanation = raw && text(raw.explanation);
  const calibration = raw && text(raw.calibration_status);
  const nonClaims = raw && strings(raw.non_claims);
  const resolution = raw && resolutions.find((item) => deepEqual(raw.problem_resolution_ref, { resolution_id: item.resolutionId }));
  const relation = raw && relations.find((item) => deepEqual(raw.relation_ref, { relation_id: item.relationId }));
  if (!raw || !currentState || !riskId || !event || !subject || !provenance || !riskStatement || !explanation || !calibration || !nonClaims
    || !resolution || !relation || !productQualityContext
    || raw.characteristic_id !== "PERFORMANCE_EFFICIENCY"
    || subject.affected_characteristic_id !== raw.characteristic_id
    || !deepEqual(subject.artifact_ref, raw.artifact_ref)
    || !deepEqual(raw.defect_population_ref, { population_id: population.populationId })
    || raw.defect_population_status !== population.status
    || !deepEqual(raw.product_quality_context, productQualityContext)
    || calibration !== "PROVISIONAL_NOT_CALIBRATED" || !deepEqual(nonClaims, categoricalRiskNonClaims)
    || !contextMatches(raw, population.raw.artifact_ref, population.raw.source_assessment_ref, population.raw.source_snapshot_id)
    || !deepEqual(event.artifact_ref, raw.artifact_ref) || !deepEqual(event.process_state_ref, raw.process_state_ref)) return null;
  const classification = raw.classification === null ? null : text(raw.classification);
  if (currentState.status === "AVAILABLE") {
    if (currentState.applicability !== "APPLICABLE" || classification !== "RISK_IDENTIFIED" || raw.problem_ref === null
      || !resolution.problem || !deepEqual(raw.problem_ref, { problem_id: resolution.problem.problemId })
      || !deepEqual(subject.participant_refs, resolution.problem.participantRefs)) return null;
  } else if (raw.classification !== null) return null;
  const expectedId: JsonRecord = {
    assessment_event_ref: event, subject, problem_resolution_ref: raw.problem_resolution_ref,
    defect_population_ref: raw.defect_population_ref, relation_ref: raw.relation_ref,
    product_quality_assessment_ref: productQualityContext.assessment_ref,
    model_ref: raw.model_ref, rule_ref: raw.rule_ref, parameter_set_ref: raw.parameter_set_ref,
  };
  if (!deepEqual(riskId, expectedId)) return null;
  const provenancePairs: Array<[unknown, unknown]> = [
    [provenance.problem_resolution_ref, raw.problem_resolution_ref], [provenance.problem_ref_or_none, raw.problem_ref],
    [provenance.defect_population_ref, raw.defect_population_ref], [provenance.defect_population_status, raw.defect_population_status],
    [provenance.relation_ref, raw.relation_ref], [provenance.product_quality_context, raw.product_quality_context],
    [provenance.participant_refs, subject.participant_refs], [provenance.ordered_evidence_refs, raw.evidence_refs],
    [provenance.artifact_ref, raw.artifact_ref], [provenance.source_snapshot_id, raw.source_snapshot_id],
    [provenance.process_state_ref, raw.process_state_ref], [provenance.model_ref, raw.model_ref],
    [provenance.rule_ref, raw.rule_ref], [provenance.parameter_set_ref, raw.parameter_set_ref],
  ];
  if (provenancePairs.some(([left, right]) => !deepEqual(left, right))) return null;
  return { ...currentState, raw, riskAssessmentId: riskId, assessmentEventRef: event, subject, characteristicId: raw.characteristic_id, classification, riskStatement, explanation, productQualityContext, calibrationStatus: calibration, nonClaims };
}

function projectOperand(value: unknown, index: number, result: JsonRecord): OperandProjection | null {
  const raw = record(value);
  const operandId = raw && record(raw.operand_id);
  const provenance = raw && record(raw.provenance);
  const sourceRef = provenance && record(provenance.source_ref);
  const stateCode = raw && text(raw.state);
  const kind = raw && text(raw.kind);
  const sourceOrRationale = provenance && text(provenance.source_or_rationale);
  const calibration = provenance && text(provenance.calibration_status);
  const governing = provenance && record(provenance.governing_contract_ref);
  const contextRef = provenance?.context_ref === null ? null : record(provenance?.context_ref);
  if (!raw || !operandId || !provenance || !sourceRef || !stateCode || !fullModelStatuses.has(stateCode)
    || !kind || kind !== operandKinds[index] || operandId.kind !== kind || !sourceOrRationale || !calibration || !governing
    || provenance.context_ref !== null && !contextRef
    || !deepEqual(provenance.problem_ref, result.problem_ref)
    || !deepEqual(provenance.relation_ref, result.relation_ref)
    || !deepEqual(provenance.artifact_ref, result.artifact_ref)
    || !deepEqual(provenance.process_state_ref, result.process_state_ref)
    || provenance.characteristic_id !== result.characteristic_id
    || !deepEqual(governing, result.governing_contract_ref)) return null;
  if (kind === "CONTEXT_FACTOR" ? contextRef === null : contextRef !== null) return null;
  const exact = raw.value === null ? null : exactFraction(raw.value);
  if (stateCode === "AVAILABLE" ? exact === null : raw.value !== null) return null;
  return { raw, operandId, kind, state: stateCode, value: exact, sourceRef, sourceOrRationale, calibrationStatus: calibration, governingContractRef: governing, contextRef };
}

export function projectQuantitativeRisk(value: unknown, problems: ProblemProjection[], relations: RelationProjection[], context: PopulationProjection): QuantitativeRiskProjection | null {
  const raw = record(value);
  const assessmentId = raw && record(raw.assessment_id);
  const provenance = raw && record(raw.provenance);
  const rawOperands = raw && array(raw.operands);
  const calibrationStatuses = raw && strings(raw.calibration_statuses);
  const governing = raw && record(raw.governing_contract_ref);
  const ruleRef = raw && record(raw.calculation_rule_ref);
  const ruleText = raw && text(raw.calculation_rule);
  const explanation = raw && text(raw.explanation);
  const nonClaims = raw && strings(raw.non_claims);
  const stateCode = raw && text(raw.state);
  const problem = raw && problems.find((item) => deepEqual(raw.problem_ref, { problem_id: item.problemId }));
  const relation = raw && relations.find((item) => deepEqual(raw.relation_ref, { relation_id: item.relationId }));
  if (!raw || !assessmentId || !provenance || !rawOperands || rawOperands.length !== 4 || !calibrationStatuses || !governing || !ruleRef
    || !ruleText || !explanation || !nonClaims || !stateCode || !["AVAILABLE", "CALCULATION_WITHHELD"].includes(stateCode)
    || !problem || !relation || raw.result_kind !== "LOCAL_RISK_R_IJ"
    || raw.scope !== "EXTERNALLY_PARAMETERIZED_BOUNDED_PE_REFERENCE"
    || raw.characteristic_id !== "PERFORMANCE_EFFICIENCY" || !deepEqual(nonClaims, quantitativeRiskNonClaims)
    || !contextMatches(raw, context.raw.artifact_ref, context.raw.source_assessment_ref, context.raw.source_snapshot_id)
    || !deepEqual(provenance.problem_ref, raw.problem_ref) || !deepEqual(provenance.relation_ref, raw.relation_ref)
    || !deepEqual(provenance.artifact_ref, raw.artifact_ref) || !deepEqual(provenance.source_assessment_ref, raw.source_assessment_ref)
    || !deepEqual(provenance.source_snapshot_id, raw.source_snapshot_id) || !deepEqual(provenance.process_state_ref, raw.process_state_ref)
    || provenance.characteristic_id !== raw.characteristic_id || !deepEqual(provenance.operands, raw.operands)
    || !deepEqual(provenance.governing_contract_ref, governing) || !deepEqual(provenance.calculation_rule_ref, ruleRef)
    || provenance.calculation_rule !== ruleText) return null;
  const operands = rawOperands.map((item, index) => projectOperand(item, index, raw));
  if (operands.some((item) => item === null)) return null;
  const validOperands = operands as OperandProjection[];
  if (!deepEqual(assessmentId.problem_ref, raw.problem_ref) || !deepEqual(assessmentId.relation_ref, raw.relation_ref)
    || !deepEqual(assessmentId.operand_refs, validOperands.map((item) => item.operandId))
    || !deepEqual(assessmentId.rule_ref, ruleRef)
    || !deepEqual(calibrationStatuses, validOperands.map((item) => item.calibrationStatus))) return null;
  const localRisk = raw.local_risk === null ? null : exactFraction(raw.local_risk);
  if (stateCode === "AVAILABLE") {
    if (!localRisk || raw.numeric_representation !== "EXACT_FRACTION" || validOperands.some((item) => item.state !== "AVAILABLE")) return null;
  } else if (raw.local_risk !== null || raw.numeric_representation !== "NONE" || validOperands.every((item) => item.state === "AVAILABLE")) return null;
  return {
    raw, assessmentId, resultKind: raw.result_kind as string, state: stateCode as "AVAILABLE" | "CALCULATION_WITHHELD",
    scope: raw.scope as string, characteristicId: raw.characteristic_id as string, operands: validOperands,
    numericRepresentation: raw.numeric_representation as string, localRisk, calibrationStatuses, governingContractRef: governing,
    calculationRuleRef: ruleRef, calculationRule: ruleText, explanation, nonClaims,
  };
}

function projected<T>(raw: unknown, value: T | null): ProjectedRecord<T> {
  return value ? { kind: "VALID", value } : { kind: "MALFORMED", raw };
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

export function selectRiskPage(response: CanonicalAnalyzeResponse): RiskPageProjection {
  const availability = selectSectionAvailability(response, "risk");
  if (!availability) return { kind: "MALFORMED" };
  if (availability.availability === "UNAVAILABLE") {
    return availability.reasonCode ? { kind: "UNAVAILABLE", reasonCode: availability.reasonCode } : { kind: "MALFORMED" };
  }
  const selected = selectCurrentResultRecords(response);
  if (!selected) return { kind: "MALFORMED" };
  const resolutionValues = array(selected.records.problem_resolutions);
  if (!resolutionValues) return { kind: "MALFORMED" };
  const resolutionValuesProjected = resolutionValues.map(projectResolution);
  const resolutions = resolutionValues.map((raw, index) => projected(raw, resolutionValuesProjected[index]));
  const validResolutions = resolutionValuesProjected.filter((item): item is ResolutionProjection => item !== null);
  const sourceGraphReady = validResolutions.length === resolutionValues.length;
  if (selected.revision === "REASSESSMENT_V2" && (!sourceGraphReady
    || !validResolutions.some((item) => deepEqual(item.raw, selected.records.target_problem_resolution)))) return { kind: "MALFORMED" };

  const populationValue = projectPopulation(selected.records.defect_population, sourceGraphReady ? validResolutions : []);
  const population = projected(selected.records.defect_population, populationValue);
  const relationValues = selected.revision === "REASSESSMENT_V2"
    ? [selected.records.defect_quality_relation]
    : array(selected.records.defect_quality_relations);
  const riskValues = selected.revision === "REASSESSMENT_V2"
    ? [selected.records.risk_assessment]
    : array(selected.records.risk_assessments);
  if (!relationValues || !riskValues) return { kind: "MALFORMED" };
  const validRelations = relationValues.map((raw) => populationValue && sourceGraphReady ? projectRelation(raw, validResolutions, populationValue) : null);
  const relations = relationValues.map((raw, index) => projected(raw, validRelations[index]));
  const productQualityContext = expectedProductQualityContext(response, selected);
  const allRelations = validRelations.filter((item): item is RelationProjection => item !== null);
  const categoricalValues = riskValues.map((raw) => populationValue && sourceGraphReady && allRelations.length === relationValues.length
    ? projectCategoricalRisk(raw, validResolutions, populationValue, allRelations, productQualityContext) : null);
  const categorical = riskValues.map((raw, index) => projected(raw, categoricalValues[index]));

  let quantitative: QuantitativePresentation = { kind: "REASSESSMENT_ABSENT" };
  if (selected.revision === "CONTROLLED_DEMO_V1") {
    const values = array(selected.records.quantitative_risk_assessments);
    if (!values) return { kind: "MALFORMED" };
    const problems = validResolutions.flatMap((item) => item.problem ? [item.problem] : []);
    quantitative = {
      kind: "RECORDS",
      records: values.map((raw) => projected(raw, populationValue && allRelations.length === relationValues.length
        ? projectQuantitativeRisk(raw, problems, allRelations, populationValue) : null)),
    };
  }
  return { kind: "AVAILABLE", revision: selected.revision, resolutions, population, relations, categorical, quantitative };
}

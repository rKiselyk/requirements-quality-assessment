import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactValueData } from "../../components/scientific";
import { selectRequirements } from "../requirements/projection";

export const specificationCharacteristicKeys = ["completeness", "verifiability", "unambiguity"] as const;
export type SpecificationCharacteristicKey = (typeof specificationCharacteristicKeys)[number];
export type AssessmentState = "COMPUTED" | "UNKNOWN" | "NOT_APPLICABLE";

export interface AggregateProjection {
  characteristicId: string;
  state: AssessmentState;
  value: ExactValueData | null;
  computedCount: number;
  unknownCount: number;
  notApplicableCount: number;
  totalCount: number;
  aggregationRuleId: string;
}

export interface RequirementContributionProjection {
  requirementId: string;
  sourceLine: number;
  characteristics: Record<SpecificationCharacteristicKey, CharacteristicValueProjection>;
}

export interface CharacteristicValueProjection {
  characteristicId: string;
  state: AssessmentState;
  value: ExactValueData | null;
}

export type ContributionEntry =
  | { kind: "VALID"; position: number; value: RequirementContributionProjection; navigable: boolean }
  | { kind: "MALFORMED"; position: number };

export interface ContractProjection {
  contractId: string;
  version: string;
}

export interface ObservabilityProjection {
  totalRequirementCount: number;
  requirementsWithObservationsCount: number;
  requirementsInApplicableComparisonsCount: number;
  totalRequirementPairCount: number;
  totalObservationPairCount: number;
  confirmedConflictCount: number;
  compatibleCount: number;
  unresolvedCount: number;
  outsideApplicabilityCount: number;
  applicableComparisonCount: number;
  globalUnresolvedExtractionCount: number;
  qbMaterialUnresolvedCount: number;
  qbNonMaterialDiagnosticCount: number;
  observedRconfCount: number;
  rconfComplete: boolean;
}

export interface FormulaOperandsProjection {
  totalRequirementCount: number;
  observedRconfCount: number;
}

export interface DiagnosticRefProjection {
  requirementId: string;
  featureId: string;
  diagnosticIndex: number;
}

export interface ObservationRefProjection {
  requirementId: string;
  featureId: string;
  observationIndex: number;
}

export interface ComparisonOperandProjection {
  snapshotId: string;
  observationRef: ObservationRefProjection;
  normalizedMetric: string | null;
  normalizedContext: string | null;
  comparator: string | null;
  inclusivity: string | null;
  value: string | null;
  unit: string | null;
}

export interface ComparisonKeyProjection {
  normalizedMetric: string;
  normalizedContext: string;
  unit: string;
}

export interface QbProjection {
  snapshotId: string;
  state: AssessmentState;
  value: ExactValueData | null;
  reasons: string[];
  rconfParticipantIds: string[];
  rconfComplete: boolean;
  observability: ObservabilityProjection | null;
  coverageProfile: ContractProjection | null;
  aggregationRule: ContractProjection | null;
  crossResultIds: Array<string | null>;
  materialityDiagnosticRefs: Array<DiagnosticRefProjection | null>;
  formulaOperands: FormulaOperandsProjection | null;
  nonClaimContract: ContractProjection | null;
  nonClaimKeys: Array<string | null>;
}

export interface ParticipantProjection {
  requirementId: string;
  sourceOrder: number;
  matchesCanonicalPopulation: boolean;
}

export interface EvidenceRefProjection {
  requirementId: string;
  evidenceId: string;
}

export interface CrossResultProjection {
  resultId: string;
  snapshotId: string;
  state: "CONFIRMED_CONFLICT" | "COMPATIBLE_WITHIN_RULE" | "ASSESSMENT_UNRESOLVED" | "OUTSIDE_V0_1_APPLICABILITY";
  participants: [ParticipantProjection, ParticipantProjection];
  observationRefs: [ObservationRefProjection, ObservationRefProjection];
  operands: { left: ComparisonOperandProjection; right: ComparisonOperandProjection };
  diagnosticRefs: DiagnosticRefProjection[];
  comparisonKey: ComparisonKeyProjection | null;
  relationKind: string;
  conflictClass: string | null;
  conflictSubtype: string | null;
  unresolvedReasons: string[];
  outsideReasons: string[];
  evidenceRefs: Array<EvidenceRefProjection | null>;
  comparisonContract: ContractProjection | null;
  coverageProfile: ContractProjection | null;
  nonClaimKeys: Array<string | null>;
}

export interface MaterialityAuditProjection {
  snapshotId: string;
  requirementId: string;
  requirementSourceOrder: number;
  diagnosticRef: DiagnosticRefProjection;
  diagnosticCode: string;
  diagnosticRuleId: string;
  candidateText: string | null;
  startOffset: number | null;
  endOffset: number | null;
  disposition: string;
  materialityRule: ContractProjection | null;
  matchedContextEvidenceRef: EvidenceRefProjection | null;
  matchedAllowlistContract: ContractProjection | null;
  gateOutcomes: Record<MaterialityGateKey, boolean>;
}

export const materialityGateKeys = [
  "exact_diagnostic_code",
  "exact_diagnostic_rule",
  "exact_candidate_text",
  "candidate_inside_context",
  "same_observation",
  "allowlisted_contract_guarantee",
  "no_qb_competition",
  "provenance_integrity",
] as const;
export type MaterialityGateKey = (typeof materialityGateKeys)[number];

export interface MaterialityProjection {
  snapshotId: string;
  materialityRule: ContractProjection;
  globalUnresolvedDiagnosticCount: number;
  qbMaterialCount: number;
  qbNonMaterialCount: number;
  auditRecords: MaterialityAuditProjection[];
}

export interface ProjectionTraceProjection {
  snapshotId: string;
  contracts: Array<{ slot: string; value: ContractProjection | null }>;
  requirementCount: number;
  observationCount: number;
  evidenceCount: number;
  diagnosticCount: number;
}

export interface SpecificationPageProjection {
  snapshotId: string | null;
  aggregates: Record<SpecificationCharacteristicKey, AggregateProjection | null>;
  qb: QbProjection | null;
  contributions: ContributionEntry[];
  crossResults: Array<CrossResultProjection | null>;
  materiality: MaterialityProjection | null;
  projectionTrace: ProjectionTraceProjection | null;
}

function record(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function text(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function stringValue(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function nonNegativeInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value >= 0 ? value : null;
}

function positiveInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value > 0 ? value : null;
}

function exactRational(value: unknown): ExactValueData | null {
  const candidate = record(value);
  if (!candidate) return null;
  const numerator = typeof candidate.numerator === "number" && Number.isSafeInteger(candidate.numerator)
    ? candidate.numerator
    : null;
  const denominator = typeof candidate.denominator === "number" && Number.isSafeInteger(candidate.denominator)
    ? candidate.denominator
    : null;
  return numerator !== null && denominator !== null && denominator !== 0
    ? { numerator: String(numerator), denominator: String(denominator) }
    : null;
}

function exactUnitRational(value: unknown): ExactValueData | null {
  const candidate = record(value);
  if (!candidate) return null;
  const numerator = typeof candidate.numerator === "number" && Number.isSafeInteger(candidate.numerator)
    ? candidate.numerator
    : null;
  const denominator = typeof candidate.denominator === "number" && Number.isSafeInteger(candidate.denominator)
    ? candidate.denominator
    : null;
  return numerator !== null && denominator !== null && denominator > 0 && numerator >= 0 && numerator <= denominator
    ? { numerator: String(numerator), denominator: String(denominator) }
    : null;
}

function stateValue(value: unknown): { state: AssessmentState; value: ExactValueData | null } | null {
  const candidate = record(value);
  if (!candidate) return null;
  const state = candidate.state;
  if (state !== "COMPUTED" && state !== "UNKNOWN" && state !== "NOT_APPLICABLE") return null;
  const projectedValue = exactRational(candidate.value);
  if (state === "COMPUTED" && projectedValue === null) return null;
  if (state !== "COMPUTED" && candidate.value !== null) return null;
  return { state, value: projectedValue };
}

function stringArray(value: unknown): string[] | null {
  return Array.isArray(value) && value.every((item) => typeof item === "string" && item.length > 0)
    ? [...value]
    : null;
}

function identifier(value: unknown): string | null {
  const direct = text(value);
  if (direct) return direct;
  const candidate = record(value);
  return candidate ? text(candidate.value) : null;
}

function contract(value: unknown): ContractProjection | null {
  const candidate = record(value);
  const contractId = candidate && text(candidate.contract_id);
  const version = candidate && text(candidate.version);
  return contractId && version ? { contractId, version } : null;
}

function sameContract(left: ContractProjection, right: ContractProjection): boolean {
  return left.contractId === right.contractId && left.version === right.version;
}

function characteristic(value: unknown, expectedCharacteristicId: string): CharacteristicValueProjection | null {
  const candidate = record(value);
  const projected = stateValue(value);
  const characteristicId = candidate && text(candidate.characteristic_id);
  return candidate && projected && characteristicId === expectedCharacteristicId
    ? { characteristicId, ...projected }
    : null;
}

function aggregate(value: unknown, expectedCharacteristicId: string): AggregateProjection | null {
  const candidate = record(value);
  const projected = characteristic(value, expectedCharacteristicId);
  if (!candidate || !projected) return null;
  const computedCount = nonNegativeInteger(candidate.computed_count);
  const unknownCount = nonNegativeInteger(candidate.unknown_count);
  const notApplicableCount = nonNegativeInteger(candidate.not_applicable_count);
  const totalCount = nonNegativeInteger(candidate.total_count);
  const aggregationRuleId = text(candidate.aggregation_rule_id);
  if (computedCount === null || unknownCount === null || notApplicableCount === null || totalCount === null
    || aggregationRuleId !== "AGG-MVP-001"
    || totalCount !== computedCount + unknownCount + notApplicableCount) return null;
  if (projected.state === "COMPUTED" && (computedCount < 1 || exactUnitRational(candidate.value) === null)) return null;
  if (projected.state === "UNKNOWN" && (computedCount !== 0 || unknownCount < 1)) return null;
  if (projected.state === "NOT_APPLICABLE" && (computedCount !== 0 || unknownCount !== 0)) return null;
  return { ...projected, computedCount, unknownCount, notApplicableCount, totalCount, aggregationRuleId };
}

function contribution(value: unknown): RequirementContributionProjection | null {
  const candidate = record(value);
  const identity = candidate && record(candidate.requirement);
  const profile = candidate && record(candidate.quality_profile);
  const requirementId = identity && text(identity.id);
  const sourceLine = identity && positiveInteger(identity.source_line);
  if (!profile || !requirementId || sourceLine === null) return null;
  const completeness = characteristic(profile.completeness, "COMPLETENESS");
  const verifiability = characteristic(profile.verifiability, "VERIFIABILITY");
  const unambiguity = characteristic(profile.unambiguity, "UNAMBIGUITY");
  if (!completeness || !verifiability || !unambiguity) return null;
  return { requirementId, sourceLine, characteristics: { completeness, verifiability, unambiguity } };
}

function observability(value: unknown): ObservabilityProjection | null {
  const candidate = record(value);
  if (!candidate || typeof candidate.rconf_complete !== "boolean") return null;
  const names = [
    "total_requirement_count", "requirements_with_observations_count", "requirements_in_applicable_comparisons_count",
    "total_requirement_pair_count", "total_observation_pair_count", "confirmed_conflict_count", "compatible_count",
    "unresolved_count", "outside_applicability_count", "applicable_comparison_count", "global_unresolved_extraction_count",
    "qb_material_unresolved_count", "qb_non_material_diagnostic_count", "observed_rconf_count",
  ] as const;
  const counts = names.map((name) => nonNegativeInteger(candidate[name]));
  if (counts.some((item) => item === null)) return null;
  const [totalRequirementCount, requirementsWithObservationsCount, requirementsInApplicableComparisonsCount,
    totalRequirementPairCount, totalObservationPairCount, confirmedConflictCount, compatibleCount, unresolvedCount,
    outsideApplicabilityCount, applicableComparisonCount, globalUnresolvedExtractionCount, qbMaterialUnresolvedCount,
    qbNonMaterialDiagnosticCount, observedRconfCount] = counts as number[];
  return {
    totalRequirementCount, requirementsWithObservationsCount, requirementsInApplicableComparisonsCount,
    totalRequirementPairCount, totalObservationPairCount, confirmedConflictCount, compatibleCount, unresolvedCount,
    outsideApplicabilityCount, applicableComparisonCount, globalUnresolvedExtractionCount, qbMaterialUnresolvedCount,
    qbNonMaterialDiagnosticCount, observedRconfCount, rconfComplete: candidate.rconf_complete,
  };
}

function formulaOperands(value: unknown): FormulaOperandsProjection | null {
  const candidate = record(value);
  const totalRequirementCount = candidate && nonNegativeInteger(candidate.total_requirement_count);
  const observedRconfCount = candidate && nonNegativeInteger(candidate.observed_rconf_count);
  return candidate && totalRequirementCount !== null && observedRconfCount !== null
    ? { totalRequirementCount, observedRconfCount }
    : null;
}

function diagnosticRef(value: unknown): DiagnosticRefProjection | null {
  const candidate = record(value);
  const requirementId = candidate && text(candidate.requirement_id);
  const featureId = candidate && text(candidate.feature_id);
  const diagnosticIndex = candidate && nonNegativeInteger(candidate.diagnostic_index);
  return requirementId && featureId && diagnosticIndex !== null
    ? { requirementId, featureId, diagnosticIndex }
    : null;
}

function observationRef(value: unknown): ObservationRefProjection | null {
  const candidate = record(value);
  const requirementId = candidate && text(candidate.requirement_id);
  const featureId = candidate && text(candidate.feature_id);
  const observationIndex = candidate && nonNegativeInteger(candidate.observation_index);
  return requirementId && featureId && observationIndex !== null
    ? { requirementId, featureId, observationIndex }
    : null;
}

function sameObservationRef(left: ObservationRefProjection, right: ObservationRefProjection): boolean {
  return left.requirementId === right.requirementId
    && left.featureId === right.featureId
    && left.observationIndex === right.observationIndex;
}

function sameDiagnosticRef(left: DiagnosticRefProjection, right: DiagnosticRefProjection): boolean {
  return left.requirementId === right.requirementId
    && left.featureId === right.featureId
    && left.diagnosticIndex === right.diagnosticIndex;
}

function nullableCanonicalText(value: unknown): { valid: boolean; value: string | null } {
  if (value === null) return { valid: true, value: null };
  const projected = text(value);
  return { valid: projected !== null, value: projected };
}

function comparisonOperand(value: unknown, expectedSnapshotId: string): ComparisonOperandProjection | null {
  const candidate = record(value);
  const snapshotId = candidate && identifier(candidate.snapshot_id);
  const projectedObservationRef = candidate && observationRef(candidate.observation_ref);
  if (!candidate || snapshotId !== expectedSnapshotId || !projectedObservationRef) return null;
  const normalizedMetric = nullableCanonicalText(candidate.normalized_metric);
  const normalizedContext = nullableCanonicalText(candidate.normalized_context);
  const comparator = nullableCanonicalText(candidate.comparator);
  const inclusivity = nullableCanonicalText(candidate.inclusivity);
  const unit = nullableCanonicalText(candidate.unit);
  const exactValue = candidate.value === null
    ? { valid: true, value: null }
    : { valid: typeof candidate.value === "string", value: typeof candidate.value === "string" ? candidate.value : null };
  if (![normalizedMetric, normalizedContext, comparator, inclusivity, unit, exactValue].every((item) => item.valid)) return null;
  return {
    snapshotId,
    observationRef: projectedObservationRef,
    normalizedMetric: normalizedMetric.value,
    normalizedContext: normalizedContext.value,
    comparator: comparator.value,
    inclusivity: inclusivity.value,
    value: exactValue.value,
    unit: unit.value,
  };
}

function comparisonKey(value: unknown): ComparisonKeyProjection | null {
  const candidate = record(value);
  const normalizedMetric = candidate && text(candidate.normalized_metric);
  const normalizedContext = candidate && text(candidate.normalized_context);
  const unit = candidate && text(candidate.unit);
  return normalizedMetric && normalizedContext && unit ? { normalizedMetric, normalizedContext, unit } : null;
}

function completeComparisonOperand(value: ComparisonOperandProjection): boolean {
  return value.normalizedMetric !== null
    && value.normalizedContext !== null
    && value.comparator !== null
    && value.inclusivity !== null
    && value.value !== null
    && value.unit !== null;
}

function qb(value: unknown, expectedSnapshotId: string, expectedRequirementCount: number): QbProjection | null {
  const candidate = record(value);
  const projected = stateValue(value);
  const snapshotId = candidate && identifier(candidate.snapshot_id);
  const reasons = candidate && stringArray(candidate.reasons);
  const rconfParticipantIds = candidate && stringArray(candidate.rconf_participant_ids);
  if (!candidate || !projected || snapshotId !== expectedSnapshotId || reasons === null || rconfParticipantIds === null || typeof candidate.rconf_complete !== "boolean") return null;
  const crossResultIds = Array.isArray(candidate.cross_result_ids)
    ? candidate.cross_result_ids.map(identifier)
    : [null];
  const materialityDiagnosticRefs = Array.isArray(candidate.materiality_diagnostic_refs)
    ? candidate.materiality_diagnostic_refs.map(diagnosticRef)
    : [null];
  const nonClaimKeys = Array.isArray(candidate.non_claim_keys)
    ? candidate.non_claim_keys.map((item) => text(item))
    : [null];
  const projectedObservability = observability(candidate.observability);
  const projectedFormulaOperands = formulaOperands(candidate.formula_operands);
  if (!projectedObservability || !projectedFormulaOperands
    || crossResultIds.some((item) => item === null)
    || materialityDiagnosticRefs.some((item) => item === null)
    || nonClaimKeys.some((item) => item === null)
    || candidate.rconf_complete !== projectedObservability.rconfComplete
    || projectedObservability.observedRconfCount !== rconfParticipantIds.length
    || projectedFormulaOperands.totalRequirementCount !== projectedObservability.totalRequirementCount
    || projectedFormulaOperands.observedRconfCount !== projectedObservability.observedRconfCount
    || crossResultIds.length !== projectedObservability.totalObservationPairCount
    || materialityDiagnosticRefs.length !== projectedObservability.globalUnresolvedExtractionCount
    || projectedObservability.totalRequirementCount !== expectedRequirementCount
    || (projected.state === "COMPUTED" && reasons.length > 0)) return null;
  return {
    snapshotId,
    ...projected,
    reasons,
    rconfParticipantIds,
    rconfComplete: candidate.rconf_complete,
    observability: projectedObservability,
    coverageProfile: contract(candidate.coverage_profile),
    aggregationRule: contract(candidate.aggregation_rule),
    crossResultIds,
    materialityDiagnosticRefs,
    formulaOperands: projectedFormulaOperands,
    nonClaimContract: contract(candidate.non_claim_contract),
    nonClaimKeys,
  };
}

function participant(value: unknown, requirementPopulation: Map<number, string>): ParticipantProjection | null {
  const candidate = record(value);
  const requirementId = candidate && text(candidate.requirement_id);
  const sourceOrder = candidate && nonNegativeInteger(candidate.source_order);
  return requirementId && sourceOrder !== null
    ? { requirementId, sourceOrder, matchesCanonicalPopulation: requirementPopulation.get(sourceOrder) === requirementId }
    : null;
}

function evidenceRef(value: unknown): EvidenceRefProjection | null {
  const candidate = record(value);
  const requirementId = candidate && text(candidate.requirement_id);
  const evidenceId = candidate && text(candidate.evidence_id);
  return requirementId && evidenceId ? { requirementId, evidenceId } : null;
}

function crossResult(value: unknown, expectedSnapshotId: string, requirementPopulation: Map<number, string>): CrossResultProjection | null {
  const candidate = record(value);
  if (!candidate) return null;
  const resultId = identifier(candidate.result_id);
  const snapshotId = identifier(candidate.snapshot_id);
  const state = candidate.state;
  const relationKind = text(candidate.relation_kind);
  const participants = Array.isArray(candidate.participants) ? candidate.participants.map((item) => participant(item, requirementPopulation)) : [];
  const observationRefs = Array.isArray(candidate.observation_refs) ? candidate.observation_refs.map(observationRef) : [];
  const operandsRecord = record(candidate.operands);
  const leftOperand = operandsRecord && comparisonOperand(operandsRecord.left, expectedSnapshotId);
  const rightOperand = operandsRecord && comparisonOperand(operandsRecord.right, expectedSnapshotId);
  const evidenceRefs = Array.isArray(candidate.evidence_refs) ? candidate.evidence_refs.map(evidenceRef) : [null];
  const diagnosticRefs = Array.isArray(candidate.diagnostic_refs) ? candidate.diagnostic_refs.map(diagnosticRef) : [null];
  const unresolvedReasons = stringArray(candidate.unresolved_reasons);
  const outsideReasons = stringArray(candidate.outside_reasons);
  const conflictClass = candidate.conflict_class === null ? null : text(candidate.conflict_class);
  const conflictSubtype = candidate.conflict_subtype === null ? null : text(candidate.conflict_subtype);
  const projectedComparisonKey = candidate.comparison_key === null ? null : comparisonKey(candidate.comparison_key);
  if (!resultId || snapshotId !== expectedSnapshotId || !relationKind
    || participants.length !== 2 || participants.some((item) => item === null)
    || observationRefs.length !== 2 || observationRefs.some((item) => item === null)
    || !leftOperand || !rightOperand
    || evidenceRefs.some((item) => item === null)
    || diagnosticRefs.some((item) => item === null)
    || unresolvedReasons === null || outsideReasons === null
    || (candidate.conflict_class !== null && conflictClass === null)
    || (candidate.conflict_subtype !== null && conflictSubtype === null)
    || (candidate.comparison_key !== null && projectedComparisonKey === null)
    || (state !== "CONFIRMED_CONFLICT" && state !== "COMPATIBLE_WITHIN_RULE"
      && state !== "ASSESSMENT_UNRESOLVED" && state !== "OUTSIDE_V0_1_APPLICABILITY")) return null;
  const typedParticipants = participants as [ParticipantProjection, ParticipantProjection];
  const typedObservationRefs = observationRefs as [ObservationRefProjection, ObservationRefProjection];
  const participantIds = new Set(typedParticipants.map((item) => item.requirementId));
  const typedEvidenceRefs = evidenceRefs as EvidenceRefProjection[];
  const typedDiagnosticRefs = diagnosticRefs as DiagnosticRefProjection[];
  if (typedParticipants[0].requirementId === typedParticipants[1].requirementId
    || typedParticipants[0].sourceOrder >= typedParticipants[1].sourceOrder
    || typedObservationRefs[0].requirementId !== typedParticipants[0].requirementId
    || typedObservationRefs[1].requirementId !== typedParticipants[1].requirementId
    || !sameObservationRef(leftOperand.observationRef, typedObservationRefs[0])
    || !sameObservationRef(rightOperand.observationRef, typedObservationRefs[1])
    || typedEvidenceRefs.some((item) => !participantIds.has(item.requirementId))
    || typedParticipants.some((item) => !typedEvidenceRefs.some((ref) => ref.requirementId === item.requirementId))
    || typedDiagnosticRefs.some((item) => !participantIds.has(item.requirementId))) return null;
  const completeComparison = projectedComparisonKey !== null
    && completeComparisonOperand(leftOperand)
    && completeComparisonOperand(rightOperand);
  const stateMatrixValid = state === "CONFIRMED_CONFLICT"
    ? conflictClass !== null && conflictSubtype !== null && unresolvedReasons.length === 0 && outsideReasons.length === 0 && completeComparison
    : state === "COMPATIBLE_WITHIN_RULE"
      ? conflictClass === null && conflictSubtype === null && unresolvedReasons.length === 0 && outsideReasons.length === 0 && completeComparison
      : state === "ASSESSMENT_UNRESOLVED"
        ? conflictClass === null && conflictSubtype === null && unresolvedReasons.length > 0 && outsideReasons.length === 0 && projectedComparisonKey === null
        : conflictClass === null && conflictSubtype === null && unresolvedReasons.length === 0 && outsideReasons.length > 0 && projectedComparisonKey === null;
  if (!stateMatrixValid) return null;
  return {
    resultId,
    snapshotId,
    state,
    participants: typedParticipants,
    observationRefs: typedObservationRefs,
    operands: { left: leftOperand, right: rightOperand },
    diagnosticRefs: typedDiagnosticRefs,
    comparisonKey: projectedComparisonKey,
    relationKind,
    conflictClass,
    conflictSubtype,
    unresolvedReasons,
    outsideReasons,
    evidenceRefs: typedEvidenceRefs,
    comparisonContract: contract(candidate.comparison_contract),
    coverageProfile: contract(candidate.coverage_profile),
    nonClaimKeys: Array.isArray(candidate.non_claim_keys) ? candidate.non_claim_keys.map((item) => text(item)) : [null],
  };
}

function materialityAudit(
  value: unknown,
  expectedSnapshotId: string,
  requirementPopulation: Map<number, string>,
  expectedMaterialityRule: ContractProjection,
): MaterialityAuditProjection | null {
  const candidate = record(value);
  if (!candidate) return null;
  const snapshotId = identifier(candidate.snapshot_id);
  const requirementId = text(candidate.requirement_id);
  const requirementSourceOrder = nonNegativeInteger(candidate.requirement_source_order);
  const projectedDiagnosticRef = diagnosticRef(candidate.diagnostic_ref);
  const diagnosticCode = text(candidate.diagnostic_code);
  const diagnosticRuleId = text(candidate.diagnostic_rule_id);
  const disposition = text(candidate.disposition);
  const candidateText = candidate.candidate_text === null ? null : stringValue(candidate.candidate_text);
  const startOffset = candidate.diagnostic_start_offset === null ? null : nonNegativeInteger(candidate.diagnostic_start_offset);
  const endOffset = candidate.diagnostic_end_offset === null ? null : nonNegativeInteger(candidate.diagnostic_end_offset);
  const spanValues = [candidateText, startOffset, endOffset];
  const spanAbsent = spanValues.every((item) => item === null);
  const spanPresent = candidateText !== null && startOffset !== null && endOffset !== null;
  const validSpan = spanAbsent || (spanPresent
    && endOffset >= startOffset
    && Array.from(candidateText).length === endOffset - startOffset);
  const matchedContextEvidenceRef = candidate.matched_context_evidence_ref === null ? null : evidenceRef(candidate.matched_context_evidence_ref);
  const matchedAllowlistContract = candidate.matched_allowlist_contract === null ? null : contract(candidate.matched_allowlist_contract);
  const materialityRule = contract(candidate.materiality_rule);
  const gates = record(candidate.gate_outcomes);
  const gateEntries = gates && materialityGateKeys.map((key) => [key, gates[key]] as const);
  const allGatesTrue = gateEntries?.every(([, gate]) => gate === true) ?? false;
  if (snapshotId !== expectedSnapshotId || !requirementId || requirementSourceOrder === null || !projectedDiagnosticRef
    || requirementPopulation.get(requirementSourceOrder) !== requirementId
    || projectedDiagnosticRef.requirementId !== requirementId || !diagnosticCode || !diagnosticRuleId
    || (disposition !== "QB_MATERIAL_UNRESOLVED" && disposition !== "QB_NON_MATERIAL") || !validSpan
    || (candidate.matched_context_evidence_ref !== null && matchedContextEvidenceRef === null)
    || (matchedContextEvidenceRef !== null && matchedContextEvidenceRef.requirementId !== requirementId)
    || (candidate.matched_allowlist_contract !== null && matchedAllowlistContract === null)
    || !materialityRule || !sameContract(materialityRule, expectedMaterialityRule)
    || !gateEntries || gateEntries.some(([, gate]) => typeof gate !== "boolean")
    || (disposition === "QB_NON_MATERIAL"
      && (!allGatesTrue || !spanPresent || matchedContextEvidenceRef === null || matchedAllowlistContract === null))
    || (disposition === "QB_MATERIAL_UNRESOLVED" && allGatesTrue)) return null;
  return {
    snapshotId,
    requirementId,
    requirementSourceOrder,
    diagnosticRef: projectedDiagnosticRef,
    diagnosticCode,
    diagnosticRuleId,
    candidateText,
    startOffset,
    endOffset,
    disposition,
    materialityRule,
    matchedContextEvidenceRef,
    matchedAllowlistContract,
    gateOutcomes: Object.fromEntries(gateEntries) as Record<MaterialityGateKey, boolean>,
  };
}

function materiality(value: unknown, expectedSnapshotId: string, requirementPopulation: Map<number, string>): MaterialityProjection | null {
  const candidate = record(value);
  const snapshotId = candidate && identifier(candidate.snapshot_id);
  const materialityRule = candidate && contract(candidate.materiality_rule);
  const globalUnresolvedDiagnosticCount = candidate && nonNegativeInteger(candidate.global_unresolved_diagnostic_count);
  const qbMaterialCount = candidate && nonNegativeInteger(candidate.qb_material_count);
  const qbNonMaterialCount = candidate && nonNegativeInteger(candidate.qb_non_material_count);
  if (!candidate || snapshotId !== expectedSnapshotId || !materialityRule
    || globalUnresolvedDiagnosticCount === null || qbMaterialCount === null || qbNonMaterialCount === null) return null;
  const auditRecords = Array.isArray(candidate.audit_records)
    ? candidate.audit_records.map((item) => materialityAudit(
      item,
      expectedSnapshotId,
      requirementPopulation,
      materialityRule,
    ))
    : [null];
  if (auditRecords.some((item) => item === null)
    || globalUnresolvedDiagnosticCount !== auditRecords.length
    || globalUnresolvedDiagnosticCount !== qbMaterialCount + qbNonMaterialCount
    || auditRecords.filter((item) => item?.disposition === "QB_MATERIAL_UNRESOLVED").length !== qbMaterialCount
    || auditRecords.filter((item) => item?.disposition === "QB_NON_MATERIAL").length !== qbNonMaterialCount) return null;
  return {
    snapshotId,
    materialityRule,
    globalUnresolvedDiagnosticCount,
    qbMaterialCount,
    qbNonMaterialCount,
    auditRecords: auditRecords as MaterialityAuditProjection[],
  };
}

function projectionTrace(value: unknown, expectedSnapshotId: string): ProjectionTraceProjection | null {
  const candidate = record(value);
  const snapshotId = candidate && identifier(candidate.snapshot_id);
  const contracts = candidate && record(candidate.contracts);
  const counts = candidate && record(candidate.counts);
  if (!candidate || snapshotId !== expectedSnapshotId || !contracts || !counts) return null;
  const requirementCount = nonNegativeInteger(counts.requirement_count);
  const observationCount = nonNegativeInteger(counts.observation_count);
  const evidenceCount = nonNegativeInteger(counts.evidence_count);
  const diagnosticCount = nonNegativeInteger(counts.diagnostic_count);
  if (requirementCount === null || observationCount === null || evidenceCount === null || diagnosticCount === null) return null;
  const slots = ["projection", "normalization", "comparison", "materiality", "aggregation", "coverage_profile"];
  return {
    snapshotId,
    contracts: slots.map((slot) => ({ slot, value: contract(contracts[slot]) })),
    requirementCount,
    observationCount,
    evidenceCount,
    diagnosticCount,
  };
}

export function selectSpecificationPage(response: CanonicalAnalyzeResponse): SpecificationPageProjection {
  const specification = record(response.specification);
  const profile = specification && record(specification.quality_profile);
  const snapshotId = specification ? text(specification.snapshot_id) : null;
  let aggregates: SpecificationPageProjection["aggregates"] = {
    completeness: aggregate(profile?.completeness, "COMPLETENESS"),
    verifiability: aggregate(profile?.verifiability, "VERIFIABILITY"),
    unambiguity: aggregate(profile?.unambiguity, "UNAMBIGUITY"),
  };
  const validAggregates = specificationCharacteristicKeys.map((key) => aggregates[key]);
  const aggregatePopulation = validAggregates.every((item): item is AggregateProjection => item !== null)
    && new Set(validAggregates.map((item) => item.totalCount)).size === 1
    ? validAggregates[0].totalCount
    : null;
  if (aggregatePopulation === null && validAggregates.every((item) => item !== null)) {
    aggregates = { completeness: null, verifiability: null, unambiguity: null };
  }

  const requirementsProjection = selectRequirements(response);
  const requirementPopulation = new Map<number, string>();
  response.requirements.forEach((item, index) => {
    const candidate = record(item);
    const identity = candidate && record(candidate.requirement);
    const requirementId = identity && text(identity.id);
    if (requirementId) requirementPopulation.set(index, requirementId);
  });
  const contributions: ContributionEntry[] = response.requirements.map((item, index) => {
    const projected = contribution(item);
    if (!projected) return { kind: "MALFORMED" as const, position: index + 1 };
    const requirementEntry = requirementsProjection[index];
    const navigable = requirementEntry?.kind === "VALID"
      && requirementEntry.value.requirement.id === projected.requirementId
      && requirementEntry.value.requirement.sourceLine === projected.sourceLine;
    return { kind: "VALID" as const, position: index + 1, value: projected, navigable };
  });

  let crossResults = snapshotId && Array.isArray(specification?.cross_results)
    ? specification.cross_results.map((item) => crossResult(item, snapshotId, requirementPopulation))
    : [null];
  let projectedQb = snapshotId !== null && aggregatePopulation !== null
    ? qb(specification?.qb_consistency, snapshotId, aggregatePopulation)
    : null;
  let projectedMateriality = snapshotId !== null ? materiality(specification?.materiality, snapshotId, requirementPopulation) : null;
  const projectedTrace = snapshotId !== null ? projectionTrace(specification?.projection_snapshot, snapshotId) : null;

  if (projectedQb && crossResults.every((item): item is CrossResultProjection => item !== null)) {
    const ids = crossResults.map((item) => item.resultId);
    if (ids.length !== projectedQb.crossResultIds.length || ids.some((id, index) => id !== projectedQb?.crossResultIds[index])) {
      projectedQb = null;
      crossResults = crossResults.map(() => null);
    }
  }
  if (projectedQb && projectedMateriality) {
    const auditRefs = projectedMateriality.auditRecords.map((item) => item.diagnosticRef);
    const qbRefs = projectedQb.materialityDiagnosticRefs;
    if (auditRefs.length !== qbRefs.length || auditRefs.some((item, index) => {
      const qbRef = qbRefs[index];
      return qbRef === null || !sameDiagnosticRef(item, qbRef);
    })) {
      projectedQb = null;
      projectedMateriality = null;
    }
  }
  return {
    snapshotId,
    aggregates,
    qb: projectedQb,
    contributions,
    crossResults,
    materiality: projectedMateriality,
    projectionTrace: projectedTrace,
  };
}

import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactValueData } from "../../components/scientific";

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
  | { kind: "VALID"; position: number; value: RequirementContributionProjection }
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
}

export interface EvidenceRefProjection {
  requirementId: string;
  evidenceId: string;
}

export interface CrossResultProjection {
  resultId: string;
  state: "CONFIRMED_CONFLICT" | "COMPATIBLE_WITHIN_RULE" | "ASSESSMENT_UNRESOLVED" | "OUTSIDE_V0_1_APPLICABILITY";
  participants: [ParticipantProjection, ParticipantProjection];
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
  requirementId: string;
  requirementSourceOrder: number;
  diagnosticCode: string;
  diagnosticRuleId: string;
  candidateText: string | null;
  startOffset: number | null;
  endOffset: number | null;
  disposition: string;
  materialityRule: ContractProjection | null;
}

export interface MaterialityProjection {
  snapshotId: string;
  materialityRule: ContractProjection;
  globalUnresolvedDiagnosticCount: number;
  qbMaterialCount: number;
  qbNonMaterialCount: number;
  auditRecords: Array<MaterialityAuditProjection | null>;
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

function characteristic(value: unknown): CharacteristicValueProjection | null {
  const candidate = record(value);
  const projected = stateValue(value);
  const characteristicId = candidate && text(candidate.characteristic_id);
  return candidate && projected && characteristicId
    ? { characteristicId, ...projected }
    : null;
}

function aggregate(value: unknown): AggregateProjection | null {
  const candidate = record(value);
  const projected = characteristic(value);
  if (!candidate || !projected) return null;
  const computedCount = nonNegativeInteger(candidate.computed_count);
  const unknownCount = nonNegativeInteger(candidate.unknown_count);
  const notApplicableCount = nonNegativeInteger(candidate.not_applicable_count);
  const totalCount = nonNegativeInteger(candidate.total_count);
  const aggregationRuleId = text(candidate.aggregation_rule_id);
  if (computedCount === null || unknownCount === null || notApplicableCount === null || totalCount === null || !aggregationRuleId) return null;
  return { ...projected, computedCount, unknownCount, notApplicableCount, totalCount, aggregationRuleId };
}

function contribution(value: unknown): RequirementContributionProjection | null {
  const candidate = record(value);
  const identity = candidate && record(candidate.requirement);
  const profile = candidate && record(candidate.quality_profile);
  const requirementId = identity && text(identity.id);
  const sourceLine = identity && positiveInteger(identity.source_line);
  if (!profile || !requirementId || sourceLine === null) return null;
  const completeness = characteristic(profile.completeness);
  const verifiability = characteristic(profile.verifiability);
  const unambiguity = characteristic(profile.unambiguity);
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

function qb(value: unknown): QbProjection | null {
  const candidate = record(value);
  const projected = stateValue(value);
  const snapshotId = candidate && identifier(candidate.snapshot_id);
  const reasons = candidate && stringArray(candidate.reasons);
  const rconfParticipantIds = candidate && stringArray(candidate.rconf_participant_ids);
  if (!candidate || !projected || !snapshotId || reasons === null || rconfParticipantIds === null || typeof candidate.rconf_complete !== "boolean") return null;
  const crossResultIds = Array.isArray(candidate.cross_result_ids)
    ? candidate.cross_result_ids.map(identifier)
    : [null];
  const materialityDiagnosticRefs = Array.isArray(candidate.materiality_diagnostic_refs)
    ? candidate.materiality_diagnostic_refs.map(diagnosticRef)
    : [null];
  const nonClaimKeys = Array.isArray(candidate.non_claim_keys)
    ? candidate.non_claim_keys.map((item) => text(item))
    : [null];
  return {
    snapshotId,
    ...projected,
    reasons,
    rconfParticipantIds,
    rconfComplete: candidate.rconf_complete,
    observability: observability(candidate.observability),
    coverageProfile: contract(candidate.coverage_profile),
    aggregationRule: contract(candidate.aggregation_rule),
    crossResultIds,
    materialityDiagnosticRefs,
    formulaOperands: formulaOperands(candidate.formula_operands),
    nonClaimContract: contract(candidate.non_claim_contract),
    nonClaimKeys,
  };
}

function participant(value: unknown): ParticipantProjection | null {
  const candidate = record(value);
  const requirementId = candidate && text(candidate.requirement_id);
  const sourceOrder = candidate && nonNegativeInteger(candidate.source_order);
  return requirementId && sourceOrder !== null ? { requirementId, sourceOrder } : null;
}

function evidenceRef(value: unknown): EvidenceRefProjection | null {
  const candidate = record(value);
  const requirementId = candidate && text(candidate.requirement_id);
  const evidenceId = candidate && text(candidate.evidence_id);
  return requirementId && evidenceId ? { requirementId, evidenceId } : null;
}

function crossResult(value: unknown): CrossResultProjection | null {
  const candidate = record(value);
  if (!candidate) return null;
  const resultId = identifier(candidate.result_id);
  const state = candidate.state;
  const relationKind = text(candidate.relation_kind);
  const participants = Array.isArray(candidate.participants) ? candidate.participants.map(participant) : [];
  const unresolvedReasons = stringArray(candidate.unresolved_reasons);
  const outsideReasons = stringArray(candidate.outside_reasons);
  const conflictClass = candidate.conflict_class === null ? null : text(candidate.conflict_class);
  const conflictSubtype = candidate.conflict_subtype === null ? null : text(candidate.conflict_subtype);
  if (!resultId || !relationKind || participants.length !== 2 || participants.some((item) => item === null)
    || unresolvedReasons === null || outsideReasons === null
    || (candidate.conflict_class !== null && conflictClass === null)
    || (candidate.conflict_subtype !== null && conflictSubtype === null)
    || (state !== "CONFIRMED_CONFLICT" && state !== "COMPATIBLE_WITHIN_RULE"
      && state !== "ASSESSMENT_UNRESOLVED" && state !== "OUTSIDE_V0_1_APPLICABILITY")) return null;
  return {
    resultId,
    state,
    participants: participants as [ParticipantProjection, ParticipantProjection],
    relationKind,
    conflictClass,
    conflictSubtype,
    unresolvedReasons,
    outsideReasons,
    evidenceRefs: Array.isArray(candidate.evidence_refs) ? candidate.evidence_refs.map(evidenceRef) : [null],
    comparisonContract: contract(candidate.comparison_contract),
    coverageProfile: contract(candidate.coverage_profile),
    nonClaimKeys: Array.isArray(candidate.non_claim_keys) ? candidate.non_claim_keys.map((item) => text(item)) : [null],
  };
}

function materialityAudit(value: unknown): MaterialityAuditProjection | null {
  const candidate = record(value);
  if (!candidate) return null;
  const requirementId = text(candidate.requirement_id);
  const requirementSourceOrder = nonNegativeInteger(candidate.requirement_source_order);
  const diagnosticCode = text(candidate.diagnostic_code);
  const diagnosticRuleId = text(candidate.diagnostic_rule_id);
  const disposition = text(candidate.disposition);
  const candidateText = candidate.candidate_text === null ? null : stringValue(candidate.candidate_text);
  const startOffset = candidate.diagnostic_start_offset === null ? null : nonNegativeInteger(candidate.diagnostic_start_offset);
  const endOffset = candidate.diagnostic_end_offset === null ? null : nonNegativeInteger(candidate.diagnostic_end_offset);
  const spanValues = [candidateText, startOffset, endOffset];
  const validSpan = spanValues.every((item) => item === null) || spanValues.every((item) => item !== null);
  if (!requirementId || requirementSourceOrder === null || !diagnosticCode || !diagnosticRuleId || !disposition || !validSpan) return null;
  return { requirementId, requirementSourceOrder, diagnosticCode, diagnosticRuleId, candidateText, startOffset, endOffset, disposition, materialityRule: contract(candidate.materiality_rule) };
}

function materiality(value: unknown): MaterialityProjection | null {
  const candidate = record(value);
  const snapshotId = candidate && identifier(candidate.snapshot_id);
  const materialityRule = candidate && contract(candidate.materiality_rule);
  const globalUnresolvedDiagnosticCount = candidate && nonNegativeInteger(candidate.global_unresolved_diagnostic_count);
  const qbMaterialCount = candidate && nonNegativeInteger(candidate.qb_material_count);
  const qbNonMaterialCount = candidate && nonNegativeInteger(candidate.qb_non_material_count);
  if (!candidate || !snapshotId || !materialityRule || globalUnresolvedDiagnosticCount === null || qbMaterialCount === null || qbNonMaterialCount === null) return null;
  return {
    snapshotId,
    materialityRule,
    globalUnresolvedDiagnosticCount,
    qbMaterialCount,
    qbNonMaterialCount,
    auditRecords: Array.isArray(candidate.audit_records) ? candidate.audit_records.map(materialityAudit) : [null],
  };
}

function projectionTrace(value: unknown): ProjectionTraceProjection | null {
  const candidate = record(value);
  const snapshotId = candidate && identifier(candidate.snapshot_id);
  const contracts = candidate && record(candidate.contracts);
  const counts = candidate && record(candidate.counts);
  if (!candidate || !snapshotId || !contracts || !counts) return null;
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
  return {
    snapshotId: specification ? text(specification.snapshot_id) : null,
    aggregates: {
      completeness: aggregate(profile?.completeness),
      verifiability: aggregate(profile?.verifiability),
      unambiguity: aggregate(profile?.unambiguity),
    },
    qb: qb(specification?.qb_consistency),
    contributions: response.requirements.map((item, index) => {
      const projected = contribution(item);
      return projected
        ? { kind: "VALID" as const, position: index + 1, value: projected }
        : { kind: "MALFORMED" as const, position: index + 1 };
    }),
    crossResults: Array.isArray(specification?.cross_results) ? specification.cross_results.map(crossResult) : [null],
    materiality: materiality(specification?.materiality),
    projectionTrace: projectionTrace(specification?.projection_snapshot),
  };
}

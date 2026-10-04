import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactValueData } from "../../components/scientific";

export const characteristicKeys = ["completeness", "verifiability", "unambiguity"] as const;
export type CharacteristicKey = (typeof characteristicKeys)[number];

export const featureKeys = [
  "condition_contexts",
  "expected_results",
  "acceptance_criteria",
  "quantitative_constraints",
  "verification_methods",
  "vague_term_occurrences",
] as const;
export type FeatureKey = (typeof featureKeys)[number];

export const externalPropertySlots = [
  ["singularity", "SINGULARITY"],
  ["presentation_conformance", "PRESENTATION_CONFORMANCE"],
  ["correctness", "CORRECTNESS"],
  ["feasibility", "FEASIBILITY"],
  ["necessity", "NECESSITY"],
  ["relevance", "RELEVANCE"],
] as const;

export interface RequirementIdentityProjection {
  id: string;
  sourceLine: number;
  text: string;
}

export interface EvidenceProjection {
  evidenceId: string;
  requirementId: string;
  featureId: string;
  text: string;
  startOffset: number;
  endOffset: number;
  ruleId: string;
}

export interface FindingProjection {
  findingId: string;
  requirementId: string;
  characteristicId: string;
  kind: string;
  code: string;
  ruleId: string;
  criterionId: string | null;
  evidenceRefs: string[];
  explanation: string;
}

export interface CharacteristicProjection {
  characteristicId: string;
  state: "COMPUTED" | "UNKNOWN" | "NOT_APPLICABLE";
  value: ExactValueData | null;
  assessmentRuleId: string | null;
  explanation: string;
  findings: Array<FindingProjection | null>;
}

export interface DiagnosticProjection {
  code: string;
  explanation: string;
  ruleId: string;
  candidateSpan: { text: string; startOffset: number; endOffset: number } | null;
}

export interface FeatureProjection {
  featureId: string;
  diagnostics: Array<DiagnosticProjection | null>;
}

export interface FeatureInputTraceProjection {
  featureId: string;
  applicability: string | null;
  observationIndexes: number[];
  diagnosticIndexes: number[];
  effectCode: string;
}

export interface CharacteristicTraceProjection {
  characteristicId: string;
  governingRuleId: string;
  decisionCode: string;
  inputs: FeatureInputTraceProjection[];
  findingRefs: string[];
}

export interface RequirementTraceProjection {
  requirementId: string;
  coverageProfileId: string;
  characteristics: CharacteristicTraceProjection[];
}

export interface RequirementProjection {
  requirement: RequirementIdentityProjection;
  characteristics: Record<CharacteristicKey, CharacteristicProjection | null>;
  evidence: Array<EvidenceProjection | null>;
  features: Record<FeatureKey, FeatureProjection | null>;
  trace: RequirementTraceProjection | null;
}

export type RequirementListEntry =
  | { kind: "VALID"; position: number; value: RequirementProjection }
  | { kind: "MALFORMED"; position: number };

export interface ExternalPropertyProjection {
  propertyId: string;
  state: "AVAILABLE" | "UNKNOWN" | "UNAVAILABLE" | "NOT_APPLICABLE" | "UNRESOLVED";
  judgmentId: string | null;
  provenance: Record<string, unknown>;
  explanation: string;
}

export type FullProfileProjection =
  | { kind: "ABSENT" }
  | { kind: "MALFORMED" }
  | { kind: "PRESENT"; external: ExternalPropertyProjection[] };

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

function positiveInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value > 0 ? value : null;
}

function nonNegativeInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value >= 0 ? value : null;
}

function stringArray(value: unknown): string[] | null {
  return Array.isArray(value) && value.every((item) => typeof item === "string" && item.length > 0)
    ? [...value]
    : null;
}

function integerArray(value: unknown): number[] | null {
  if (!Array.isArray(value)) return null;
  const projected = value.map(nonNegativeInteger);
  return projected.every((item): item is number => item !== null) ? projected : null;
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

function finding(value: unknown, parentRequirementId: string, parentCharacteristicId: string): FindingProjection | null {
  const candidate = record(value);
  if (!candidate) return null;
  const findingId = text(candidate.finding_id);
  const requirementId = text(candidate.requirement_id);
  const characteristicId = text(candidate.characteristic_id);
  const kind = text(candidate.kind);
  const code = text(candidate.code);
  const ruleId = text(candidate.rule_id);
  const criterionId = candidate.criterion_id === null ? null : text(candidate.criterion_id);
  const evidenceRefs = stringArray(candidate.evidence_refs);
  const explanation = stringValue(candidate.explanation);
  if (!findingId || requirementId !== parentRequirementId || characteristicId !== parentCharacteristicId || !kind || !code || !ruleId
    || (candidate.criterion_id !== null && criterionId === null) || evidenceRefs === null || explanation === null) return null;
  return { findingId, requirementId, characteristicId, kind, code, ruleId, criterionId, evidenceRefs, explanation };
}

function characteristic(value: unknown, expectedId: string, parentRequirementId: string): CharacteristicProjection | null {
  const candidate = record(value);
  if (!candidate || candidate.characteristic_id !== expectedId) return null;
  const state = candidate.state;
  if (state !== "COMPUTED" && state !== "UNKNOWN" && state !== "NOT_APPLICABLE") return null;
  const projectedValue = exactRational(candidate.value);
  if (state === "COMPUTED" && projectedValue === null) return null;
  if (state !== "COMPUTED" && candidate.value !== null) return null;
  const assessmentRuleId = candidate.assessment_rule_id === null ? null : text(candidate.assessment_rule_id);
  const explanation = stringValue(candidate.explanation);
  if ((candidate.assessment_rule_id !== null && assessmentRuleId === null)
    || (state === "COMPUTED" && assessmentRuleId === null)
    || explanation === null || !Array.isArray(candidate.findings)) return null;
  return {
    characteristicId: expectedId,
    state,
    value: projectedValue,
    assessmentRuleId,
    explanation,
    findings: candidate.findings.map((item) => finding(item, parentRequirementId, expectedId)),
  };
}

function evidence(value: unknown, parentRequirementId: string): EvidenceProjection | null {
  const candidate = record(value);
  if (!candidate) return null;
  const evidenceId = text(candidate.evidence_id);
  const requirementId = text(candidate.requirement_id);
  const featureId = text(candidate.feature_id);
  const evidenceText = stringValue(candidate.text);
  const startOffset = nonNegativeInteger(candidate.start_offset);
  const endOffset = nonNegativeInteger(candidate.end_offset);
  const ruleId = text(candidate.rule_id);
  if (!evidenceId || requirementId !== parentRequirementId || !featureId || evidenceText === null || startOffset === null
    || endOffset === null || endOffset < startOffset || !ruleId) return null;
  return { evidenceId, requirementId, featureId, text: evidenceText, startOffset, endOffset, ruleId };
}

function diagnostic(value: unknown): DiagnosticProjection | null {
  const candidate = record(value);
  if (!candidate) return null;
  const code = text(candidate.code);
  const explanation = stringValue(candidate.explanation);
  const ruleId = text(candidate.rule_id);
  if (!code || explanation === null || !ruleId) return null;
  if (candidate.candidate_span === null) return { code, explanation, ruleId, candidateSpan: null };
  const span = record(candidate.candidate_span);
  const spanText = span && stringValue(span.text);
  const startOffset = span && nonNegativeInteger(span.start_offset);
  const endOffset = span && nonNegativeInteger(span.end_offset);
  if (!span || spanText === null || startOffset === null || endOffset === null || endOffset < startOffset) return null;
  return { code, explanation, ruleId, candidateSpan: { text: spanText, startOffset, endOffset } };
}

function feature(value: unknown, expectedFeatureId: string): FeatureProjection | null {
  const candidate = record(value);
  const featureId = candidate && text(candidate.feature_id);
  if (!candidate || featureId !== expectedFeatureId || !Array.isArray(candidate.diagnostics)) return null;
  return { featureId, diagnostics: candidate.diagnostics.map(diagnostic) };
}

function inputTrace(value: unknown): FeatureInputTraceProjection | null {
  const candidate = record(value);
  if (!candidate) return null;
  const featureId = text(candidate.feature_id);
  const applicability = candidate.applicability === null ? null : text(candidate.applicability);
  const observationIndexes = integerArray(candidate.observation_indexes);
  const diagnosticIndexes = integerArray(candidate.diagnostic_indexes);
  const effectCode = text(candidate.effect_code);
  if (!featureId || (candidate.applicability !== null && applicability === null)
    || observationIndexes === null || diagnosticIndexes === null || !effectCode) return null;
  return { featureId, applicability, observationIndexes, diagnosticIndexes, effectCode };
}

function characteristicTrace(value: unknown): CharacteristicTraceProjection | null {
  const candidate = record(value);
  if (!candidate || !Array.isArray(candidate.inputs)) return null;
  const characteristicId = text(candidate.characteristic_id);
  const governingRuleId = text(candidate.governing_rule_id);
  const decisionCode = text(candidate.decision_code);
  const inputs = candidate.inputs.map(inputTrace);
  const findingRefs = stringArray(candidate.finding_refs);
  if (!characteristicId || !governingRuleId || !decisionCode
    || inputs.some((item) => item === null) || findingRefs === null) return null;
  return { characteristicId, governingRuleId, decisionCode, inputs: inputs as FeatureInputTraceProjection[], findingRefs };
}

function trace(value: unknown): RequirementTraceProjection | null {
  const candidate = record(value);
  if (!candidate || !Array.isArray(candidate.characteristics)) return null;
  const requirementId = text(candidate.requirement_id);
  const coverageProfileId = text(candidate.coverage_profile_id);
  const characteristics = candidate.characteristics.map(characteristicTrace);
  if (!requirementId || !coverageProfileId || characteristics.some((item) => item === null)) return null;
  return { requirementId, coverageProfileId, characteristics: characteristics as CharacteristicTraceProjection[] };
}

function requirement(value: unknown): RequirementProjection | null {
  const candidate = record(value);
  const identity = candidate && record(candidate.requirement);
  const qualityProfile = candidate && record(candidate.quality_profile);
  const features = candidate && record(candidate.features);
  if (!candidate || !identity || !qualityProfile || !features || !Array.isArray(candidate.evidence)) return null;
  const id = text(identity.id);
  const sourceLine = positiveInteger(identity.source_line);
  const requirementText = stringValue(identity.text);
  if (!id || sourceLine === null || requirementText === null) return null;
  const projectedTrace = trace(candidate.trace);
  return {
    requirement: { id, sourceLine, text: requirementText },
    characteristics: {
      completeness: characteristic(qualityProfile.completeness, "COMPLETENESS", id),
      verifiability: characteristic(qualityProfile.verifiability, "VERIFIABILITY", id),
      unambiguity: characteristic(qualityProfile.unambiguity, "UNAMBIGUITY", id),
    },
    evidence: candidate.evidence.map((item) => evidence(item, id)),
    features: {
      condition_contexts: feature(features.condition_contexts, "condition_context"),
      expected_results: feature(features.expected_results, "expected_result"),
      acceptance_criteria: feature(features.acceptance_criteria, "acceptance_criterion"),
      quantitative_constraints: feature(features.quantitative_constraints, "quantitative_constraint"),
      verification_methods: feature(features.verification_methods, "verification_method"),
      vague_term_occurrences: feature(features.vague_term_occurrences, "vague_term_occurrence"),
    },
    trace: projectedTrace?.requirementId === id ? projectedTrace : null,
  };
}

export function selectRequirements(response: CanonicalAnalyzeResponse): RequirementListEntry[] {
  return response.requirements.map((item, index) => {
    const projected = requirement(item);
    return projected
      ? { kind: "VALID" as const, position: index + 1, value: projected }
      : { kind: "MALFORMED" as const, position: index + 1 };
  });
}

function externalProperty(
  value: unknown,
  expectedPropertyId: string,
  expectedRequirement: RequirementIdentityProjection,
): ExternalPropertyProjection | null {
  const candidate = record(value);
  if (!candidate || candidate.property_id !== expectedPropertyId) return null;
  const state = candidate.state;
  if (state !== "AVAILABLE" && state !== "UNKNOWN" && state !== "UNAVAILABLE"
    && state !== "NOT_APPLICABLE" && state !== "UNRESOLVED") return null;
  const judgment = candidate.judgment === null ? null : record(candidate.judgment);
  const judgmentId = judgment && text(judgment.judgment_id);
  if ((state === "AVAILABLE" && !judgmentId) || (state !== "AVAILABLE" && candidate.judgment !== null)) return null;
  const provenance = record(candidate.provenance);
  const explanation = stringValue(candidate.explanation);
  const provenanceRequirement = provenance && record(provenance.requirement_ref);
  if (!provenance || !provenanceRequirement
    || provenanceRequirement.requirement_id !== expectedRequirement.id
    || provenanceRequirement.source_line !== expectedRequirement.sourceLine
    || explanation === null) return null;
  return { propertyId: expectedPropertyId, state, judgmentId: judgmentId ?? null, provenance, explanation };
}

function profileIdentity(value: Record<string, unknown>) {
  const ref = record(value.requirement_ref);
  return ref ? { requirementId: text(ref.requirement_id), sourceLine: positiveInteger(ref.source_line) } : null;
}

export function selectFullProfile(response: CanonicalAnalyzeResponse, selected: RequirementIdentityProjection): FullProfileProjection {
  if (response.full_model === null) return { kind: "ABSENT" };
  const profiles = response.full_model.full_quality_profiles;
  if (!Array.isArray(profiles)) return { kind: "MALFORMED" };
  let malformedIdentityMatch = false;
  for (const value of profiles) {
    const candidate = record(value);
    if (!candidate) continue;
    const identity = profileIdentity(candidate);
    if (!identity || identity.requirementId !== selected.id) continue;
    if (identity.sourceLine !== selected.sourceLine) continue;

    const automatic = record(candidate.automatic_record);
    const extraction = automatic && record(automatic.extraction_result);
    const automaticRequirement = extraction && record(extraction.requirement);
    if (!automaticRequirement || automaticRequirement.id !== selected.id || automaticRequirement.source_line !== selected.sourceLine) {
      malformedIdentityMatch = true;
      continue;
    }

    const projected = externalPropertySlots.map(([slot, propertyId]) => externalProperty(candidate[slot], propertyId, selected));
    if (projected.some((item) => item === null)) return { kind: "MALFORMED" };
    return { kind: "PRESENT", external: projected as ExternalPropertyProjection[] };
  }
  return malformedIdentityMatch ? { kind: "MALFORMED" } : { kind: "ABSENT" };
}

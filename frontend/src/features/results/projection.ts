import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactValueData } from "../../components/scientific";

export type ResultSectionId =
  | "overview"
  | "requirements"
  | "specification"
  | "product_quality"
  | "risk"
  | "corrective_actions"
  | "process"
  | "audit";

export const resultSectionIds: readonly ResultSectionId[] = [
  "overview",
  "requirements",
  "specification",
  "product_quality",
  "risk",
  "corrective_actions",
  "process",
  "audit",
];

export interface SectionAvailabilityProjection {
  section: string;
  availability: "AVAILABLE" | "UNAVAILABLE";
  reasonCode: string | null;
}

export interface MetricProjection {
  state: "COMPUTED" | "UNKNOWN" | "NOT_APPLICABLE";
  value: ExactValueData | null;
  computedCount: number | null;
  unknownCount: number | null;
  notApplicableCount: number | null;
  totalCount: number | null;
}

export interface QbProjection {
  state: "COMPUTED" | "UNKNOWN" | "NOT_APPLICABLE";
  value: ExactValueData | null;
  reasons: string[];
}

export interface ScientificRecordProjection {
  status: string | null;
  applicability: string | null;
  kind: string | null;
  value: ExactValueData | null;
  reasonCodes: string[];
}

export interface RiskProjection {
  categorical: ScientificRecordProjection[];
  quantitative: ScientificRecordProjection[];
}

export interface ProcessProjection {
  states: Array<{ id: string; version: string; stage: string }>;
  checkpoints: Array<{ id: string; version: string; outcome: string; reasonCodes: string[] }>;
}

function record(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function text(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function integer(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) ? value : null;
}

function nonNegativeInteger(value: unknown): number | null {
  const projected = integer(value);
  return projected !== null && projected >= 0 ? projected : null;
}

export function exactValue(value: unknown): ExactValueData | null {
  if (typeof value === "string" && value.length > 0) return value;
  const candidate = record(value);
  if (!candidate) return null;
  const numerator = integer(candidate.numerator);
  const denominator = integer(candidate.denominator);
  if (numerator !== null && denominator !== null && denominator !== 0) {
    return { numerator: String(numerator), denominator: String(denominator) };
  }
  const exact = text(candidate.exact);
  return exact === null ? null : { exact };
}

function exactRational(value: unknown): ExactValueData | null {
  const candidate = record(value);
  if (!candidate) return null;
  const numerator = integer(candidate.numerator);
  const denominator = integer(candidate.denominator);
  return numerator !== null && denominator !== null && denominator !== 0
    ? { numerator: String(numerator), denominator: String(denominator) }
    : null;
}

function stringArray(value: unknown): string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string")
    ? [...value]
    : [];
}

function canonicalCodeArray(value: unknown): string[] | null {
  return Array.isArray(value)
    && value.every((item) => typeof item === "string" && item.length > 0)
    ? [...value]
    : null;
}

export function selectSectionAvailability(
  response: CanonicalAnalyzeResponse,
  section: string,
): SectionAvailabilityProjection | null {
  for (const item of response.section_availability) {
    const candidate = record(item);
    if (!candidate || candidate.section !== section) continue;
    if (candidate.availability !== "AVAILABLE" && candidate.availability !== "UNAVAILABLE") return null;
    if (candidate.reason_code !== null && text(candidate.reason_code) === null) return null;
    return {
      section,
      availability: candidate.availability,
      reasonCode: candidate.reason_code === null ? null : text(candidate.reason_code),
    };
  }
  return null;
}

function stateAndValue(value: unknown): Pick<MetricProjection, "state" | "value"> | null {
  const candidate = record(value);
  if (!candidate) return null;
  const state = candidate.state;
  if (state !== "COMPUTED" && state !== "UNKNOWN" && state !== "NOT_APPLICABLE") return null;
  const projectedValue = exactRational(candidate.value);
  if (state === "COMPUTED" && projectedValue === null) return null;
  if ((state === "UNKNOWN" || state === "NOT_APPLICABLE") && candidate.value !== null) return null;
  return { state, value: projectedValue };
}

function aggregateMetric(value: unknown): MetricProjection | null {
  const candidate = record(value);
  const stateValue = stateAndValue(value);
  if (!candidate || !stateValue) return null;
  const computedCount = nonNegativeInteger(candidate.computed_count);
  const unknownCount = nonNegativeInteger(candidate.unknown_count);
  const notApplicableCount = nonNegativeInteger(candidate.not_applicable_count);
  const totalCount = nonNegativeInteger(candidate.total_count);
  if (computedCount === null || unknownCount === null || notApplicableCount === null || totalCount === null) return null;
  return {
    ...stateValue,
    computedCount,
    unknownCount,
    notApplicableCount,
    totalCount,
  };
}

export function selectSpecificationMetrics(response: CanonicalAnalyzeResponse) {
  const qualityProfile = record(response.specification.quality_profile);
  return {
    completeness: aggregateMetric(qualityProfile?.completeness),
    verifiability: aggregateMetric(qualityProfile?.verifiability),
    unambiguity: aggregateMetric(qualityProfile?.unambiguity),
  };
}

export function selectQbConsistency(response: CanonicalAnalyzeResponse): QbProjection | null {
  const candidate = record(response.specification.qb_consistency);
  const stateValue = stateAndValue(response.specification.qb_consistency);
  const reasons = candidate && canonicalCodeArray(candidate.reasons);
  return stateValue === null || reasons === null
    ? null
    : { ...stateValue, reasons };
}

function scientificRecord(value: unknown, valueField: string, kindField: string): ScientificRecordProjection | null {
  const candidate = record(value);
  if (!candidate) return null;
  const status = text(candidate.status) ?? text(candidate.state);
  const kind = text(candidate[kindField]);
  const applicability = text(candidate.applicability);
  if (!status && !kind && !applicability) return null;
  return {
    status,
    applicability,
    kind,
    value: exactValue(candidate[valueField]),
    reasonCodes: stringArray(candidate.reason_codes),
  };
}

export function selectProductQuality(response: CanonicalAnalyzeResponse) {
  const fullModel = response.full_model;
  return {
    observed: scientificRecord(fullModel?.observed_product_quality, "observed_value", "result_kind"),
    predicted: scientificRecord(fullModel?.prediction, "predicted_value", "result_kind"),
  };
}

export function selectRisk(response: CanonicalAnalyzeResponse): RiskProjection {
  const fullModel = response.full_model;
  const categorical = Array.isArray(fullModel?.risk_assessments)
    ? fullModel.risk_assessments.map((item) => scientificRecord(item, "value", "classification")).filter((item): item is ScientificRecordProjection => item !== null)
    : [];
  const quantitative = Array.isArray(fullModel?.quantitative_risk_assessments)
    ? fullModel.quantitative_risk_assessments.map((item) => scientificRecord(item, "local_risk", "result_kind")).filter((item): item is ScientificRecordProjection => item !== null)
    : [];
  return { categorical, quantitative };
}

export function selectCorrectiveAction(response: CanonicalAnalyzeResponse): ScientificRecordProjection | null {
  return scientificRecord(response.full_model?.corrective_action_resolution, "value", "action_kind");
}

export function selectProcess(response: CanonicalAnalyzeResponse): ProcessProjection {
  const states: ProcessProjection["states"] = [];
  for (const value of [response.full_model?.process_v1, response.full_model?.process_v2]) {
    const candidate = record(value);
    const id = candidate && text(candidate.process_state_id);
    const version = candidate && text(candidate.process_state_version);
    const stage = candidate && text(candidate.stage);
    if (id && version && stage) states.push({ id, version, stage });
  }
  const checkpoints = Array.isArray(response.full_model?.checkpoint_evaluations)
    ? response.full_model.checkpoint_evaluations.flatMap((value) => {
        const candidate = record(value);
        const id = candidate && text(candidate.checkpoint_id);
        const version = candidate && text(candidate.checkpoint_version);
        const outcome = candidate && text(candidate.outcome);
        return id && version && outcome
          ? [{ id, version, outcome, reasonCodes: stringArray(candidate.reason_codes) }]
          : [];
      })
    : [];
  return { states, checkpoints };
}

export function selectSnapshotId(response: CanonicalAnalyzeResponse): string | null {
  return text(response.specification.snapshot_id);
}

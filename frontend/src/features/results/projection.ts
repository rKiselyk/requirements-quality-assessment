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
  state: string;
  value: ExactValueData | null;
  computedCount: number | null;
  unknownCount: number | null;
  notApplicableCount: number | null;
  totalCount: number | null;
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

function stringArray(value: unknown): string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string")
    ? [...value]
    : [];
}

export function selectSectionAvailability(
  response: CanonicalAnalyzeResponse,
  section: string,
): SectionAvailabilityProjection | null {
  for (const item of response.section_availability) {
    const candidate = record(item);
    if (!candidate || candidate.section !== section) continue;
    if (candidate.availability !== "AVAILABLE" && candidate.availability !== "UNAVAILABLE") return null;
    return {
      section,
      availability: candidate.availability,
      reasonCode: candidate.reason_code === null ? null : text(candidate.reason_code),
    };
  }
  return null;
}

function metric(value: unknown): MetricProjection | null {
  const candidate = record(value);
  const state = candidate && text(candidate.state);
  if (!candidate || !state) return null;
  return {
    state,
    value: exactValue(candidate.value),
    computedCount: integer(candidate.computed_count),
    unknownCount: integer(candidate.unknown_count),
    notApplicableCount: integer(candidate.not_applicable_count),
    totalCount: integer(candidate.total_count),
  };
}

export function selectSpecificationMetrics(response: CanonicalAnalyzeResponse) {
  const qualityProfile = record(response.specification.quality_profile);
  return {
    completeness: metric(qualityProfile?.completeness),
    verifiability: metric(qualityProfile?.verifiability),
    unambiguity: metric(qualityProfile?.unambiguity),
  };
}

export function selectQbConsistency(response: CanonicalAnalyzeResponse): MetricProjection | null {
  return metric(response.specification.qb_consistency);
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

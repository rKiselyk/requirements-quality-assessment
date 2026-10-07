import type { CanonicalAnalyzeResponse } from "../../api/analyze";

export type AuditAvailability =
  | { kind: "AVAILABLE" }
  | { kind: "UNAVAILABLE"; reasonCode: string | null }
  | { kind: "MALFORMED" };

export interface AuditGroup {
  id: "response" | "assessment" | "fullModel" | "reassessmentContext";
  canonicalKey: string | null;
  path: string;
  value: unknown;
}

function record(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

export function selectAuditAvailability(response: CanonicalAnalyzeResponse): AuditAvailability {
  const matches = response.section_availability.filter((value) => record(value)?.section === "audit");
  if (matches.length !== 1) return { kind: "MALFORMED" };
  const entry = record(matches[0]);
  if (entry?.availability === "AVAILABLE") return { kind: "AVAILABLE" };
  if (entry?.availability === "UNAVAILABLE") {
    return { kind: "UNAVAILABLE", reasonCode: typeof entry.reason_code === "string" ? entry.reason_code : null };
  }
  return { kind: "MALFORMED" };
}

/**
 * Groups the response for presentation while retaining every own response key
 * exactly once. Values are never copied, normalized, sorted, or interpreted.
 */
export function buildAuditGroups(response: CanonicalAnalyzeResponse): AuditGroup[] {
  const responseFields: Record<string, unknown> = {};
  const assessmentFields: Record<string, unknown> = {};
  let fullModel: unknown = null;
  let reassessmentContext: unknown = null;

  for (const [key, value] of Object.entries(response)) {
    if (key === "requirements" || key === "specification") {
      assessmentFields[key] = value;
    } else if (key === "full_model") {
      fullModel = value;
    } else if (key === "reassessment_context" && value !== null) {
      reassessmentContext = value;
    } else {
      responseFields[key] = value;
    }
  }

  const groups: AuditGroup[] = [
    { id: "response", canonicalKey: null, path: "$", value: responseFields },
    { id: "assessment", canonicalKey: null, path: "$", value: assessmentFields },
    {
      id: "fullModel",
      canonicalKey: "full_model",
      path: "$.full_model",
      value: fullModel,
    },
  ];
  if (reassessmentContext !== null) {
    groups.push({
      id: "reassessmentContext",
      canonicalKey: "reassessment_context",
      path: "$.reassessment_context",
      value: reassessmentContext,
    });
  }
  return groups;
}

export function isPlainRecord(value: unknown): value is Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

export function isCanonicalFraction(value: unknown): value is { numerator: number; denominator: number } {
  if (!isPlainRecord(value)) return false;
  const keys = Object.keys(value);
  return keys.length === 2
    && keys.includes("numerator")
    && keys.includes("denominator")
    && Number.isSafeInteger(value.numerator)
    && Number.isSafeInteger(value.denominator)
    && value.denominator !== 0;
}

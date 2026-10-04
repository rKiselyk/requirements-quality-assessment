import type { Rui05AnalyzeRequest } from "../features/specification-input/model";
import { apiErrorCodes, type ApiErrorCode } from "../i18n";

export interface CanonicalAnalyzeResponse extends Record<string, unknown> {
  contract_version: "research-api-v1";
  analysis_case: "INITIAL" | "CONTROLLED_DEMO" | "REASSESSMENT";
  controlled_scenario: Record<string, unknown> | null;
  requirements: unknown[];
  specification: Record<string, unknown>;
  section_availability: unknown[];
  full_model: Record<string, unknown> | null;
  reassessment_context: Record<string, unknown> | null;
  limitations: unknown[];
}

export interface SafeAnalyzeError {
  code: ApiErrorCode | null;
  kind: "API" | "NETWORK" | "MALFORMED_RESPONSE";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isKnownErrorCode(value: unknown): value is ApiErrorCode {
  return typeof value === "string" && apiErrorCodes.some((code) => code === value);
}

function safeErrorFromPayload(payload: unknown): SafeAnalyzeError {
  if (!isRecord(payload) || !isRecord(payload.error)) {
    return { code: null, kind: "MALFORMED_RESPONSE" };
  }
  return {
    code: isKnownErrorCode(payload.error.code) ? payload.error.code : null,
    kind: "API",
  };
}

function isCanonicalResponse(
  value: unknown,
  expectedCase: Rui05AnalyzeRequest["case"],
): value is CanonicalAnalyzeResponse {
  return isRecord(value)
    && value.contract_version === "research-api-v1"
    && value.analysis_case === expectedCase
    && (value.controlled_scenario === null || isRecord(value.controlled_scenario))
    && Array.isArray(value.requirements)
    && isRecord(value.specification)
    && Array.isArray(value.section_availability)
    && (value.full_model === null || isRecord(value.full_model))
    && (value.reassessment_context === null || isRecord(value.reassessment_context))
    && Array.isArray(value.limitations);
}

export class AnalyzeRequestError extends Error {
  readonly safe: SafeAnalyzeError;

  constructor(safe: SafeAnalyzeError) {
    super("The analysis request failed.");
    this.name = "AnalyzeRequestError";
    this.safe = safe;
  }
}

async function readJson(response: Response): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    throw new AnalyzeRequestError({ code: null, kind: "MALFORMED_RESPONSE" });
  }
}

export async function analyzeSpecification(
  request: Rui05AnalyzeRequest,
  fetchImplementation: typeof fetch = fetch,
): Promise<CanonicalAnalyzeResponse> {
  let response: Response;
  try {
    response = await fetchImplementation("/api/v1/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
  } catch {
    throw new AnalyzeRequestError({ code: null, kind: "NETWORK" });
  }

  const payload = await readJson(response);
  if (!response.ok) throw new AnalyzeRequestError(safeErrorFromPayload(payload));
  if (!isCanonicalResponse(payload, request.case)) {
    throw new AnalyzeRequestError({ code: null, kind: "MALFORMED_RESPONSE" });
  }

  return payload;
}

export function toSafeAnalyzeError(error: unknown): SafeAnalyzeError {
  return error instanceof AnalyzeRequestError
    ? error.safe
    : { code: null, kind: "NETWORK" };
}

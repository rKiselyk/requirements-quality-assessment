import type { Rui05AnalyzeRequest } from "../features/specification-input/model";
import { apiErrorCodes, type ApiErrorCode } from "../i18n";

export interface CanonicalAnalyzeResponse extends Record<string, unknown> {
  contract_version: string;
  analysis_case: "INITIAL" | "CONTROLLED_DEMO" | "REASSESSMENT";
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

function isCanonicalResponse(value: unknown): value is CanonicalAnalyzeResponse {
  if (!isRecord(value) || typeof value.contract_version !== "string") return false;
  return value.analysis_case === "INITIAL"
    || value.analysis_case === "CONTROLLED_DEMO"
    || value.analysis_case === "REASSESSMENT";
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
  if (!isCanonicalResponse(payload)) {
    throw new AnalyzeRequestError({ code: null, kind: "MALFORMED_RESPONSE" });
  }

  return payload;
}

export function toSafeAnalyzeError(error: unknown): SafeAnalyzeError {
  return error instanceof AnalyzeRequestError
    ? error.safe
    : { code: null, kind: "NETWORK" };
}

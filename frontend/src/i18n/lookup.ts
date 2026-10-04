export type ApiErrorCode =
  | "EMPTY_SPECIFICATION"
  | "MALFORMED_REQUIREMENT_INPUT"
  | "INVALID_REASSESSMENT_CONTEXT"
  | "INVALID_CONTROLLED_DEMO_REQUEST"
  | "ANALYSIS_VALIDATION_FAILED"
  | "ANALYSIS_INTERNAL_FAILURE";

export type LimitationCode =
  | "NO_VALUE_INFERRED"
  | "OBSERVED_NOT_PREDICTED"
  | "CATEGORICAL_NOT_QUANTITATIVE"
  | "NO_CAUSAL_PROOF";

/** Presentation lookup keys only; callers must continue to retain and display canonical codes where relevant. */
export const apiErrorTranslationKey = (code: ApiErrorCode) => `codes.${code}` as const;
export const limitationTranslationKey = (code: LimitationCode) => `codes.${code}` as const;

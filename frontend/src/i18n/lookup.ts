export const apiErrorCodes = [
  "EMPTY_SPECIFICATION",
  "MALFORMED_REQUIREMENT_INPUT",
  "INVALID_REASSESSMENT_CONTEXT",
  "INVALID_CONTROLLED_DEMO_REQUEST",
  "ANALYSIS_VALIDATION_FAILED",
  "ANALYSIS_INTERNAL_FAILURE",
] as const;

export type ApiErrorCode = (typeof apiErrorCodes)[number];

export const limitationCodes = [
  "NO_COMBINED_QUALITY_SCORE",
  "TEXT_ONLY_INITIAL_ASSESSMENT",
  "UKRAINIAN_LANGUAGE_PROFILE",
  "BOUNDED_RESEARCH_MODEL",
  "CONTROLLED_RESEARCH_FIXTURE_DATA",
  "PROVISIONAL_NOT_CALIBRATED",
  "NO_CAUSAL_OR_RELEASE_CLAIM",
  "NO_ARBITRARY_V1_V2_COMPARISON",
] as const;

export type LimitationCode = (typeof limitationCodes)[number];

/** Presentation lookup keys only; callers must continue to retain and display canonical codes where relevant. */
export const apiErrorTranslationKey = (code: ApiErrorCode) => `codes.${code}` as const;
export const limitationTranslationKey = (code: LimitationCode) => `codes.${code}` as const;

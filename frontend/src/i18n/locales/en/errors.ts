export const errors = {
  unknown: "The analysis request could not be completed.",
  codes: {
    EMPTY_SPECIFICATION: "The specification contains no non-empty requirements.",
    MALFORMED_REQUIREMENT_INPUT: "The requirement input could not be read.",
    INVALID_REASSESSMENT_CONTEXT: "The reassessment context is missing or invalid.",
    INVALID_CONTROLLED_DEMO_REQUEST: "The controlled demonstration request is invalid.",
    ANALYSIS_VALIDATION_FAILED: "Analysis validation failed.",
    ANALYSIS_INTERNAL_FAILURE: "An unexpected analysis failure occurred.",
  },
} as const;

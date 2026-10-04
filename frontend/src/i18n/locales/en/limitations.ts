export const limitations = {
  unknown: "A limitation applies; see its canonical code.",
  codes: {
    NO_COMBINED_QUALITY_SCORE: "The assessment does not provide a combined quality score.",
    TEXT_ONLY_INITIAL_ASSESSMENT: "The initial assessment uses specification text only.",
    UKRAINIAN_LANGUAGE_PROFILE: "Language-dependent detection uses the Ukrainian language profile.",
    BOUNDED_RESEARCH_MODEL: "Results are limited to the scope of the bounded research model.",
    CONTROLLED_RESEARCH_FIXTURE_DATA: "Additional inputs are controlled research fixture data.",
    PROVISIONAL_NOT_CALIBRATED: "Applicable results are provisional and not calibrated.",
    NO_CAUSAL_OR_RELEASE_CLAIM: "The result does not establish causal effectiveness or authorize release.",
    NO_ARBITRARY_V1_V2_COMPARISON: "Arbitrary specification-only v1/v2 comparison is not supported.",
  },
} as const;

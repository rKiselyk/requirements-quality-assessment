export const limitations = {
  unknown: "A limitation applies; see its canonical code.",
  codes: {
    NO_VALUE_INFERRED: "No value was inferred from unavailable evidence.",
    OBSERVED_NOT_PREDICTED: "Observed and predicted product quality are distinct records.",
    CATEGORICAL_NOT_QUANTITATIVE: "Categorical and quantitative risk are distinct records.",
    NO_CAUSAL_PROOF: "A before/after change does not prove causal effectiveness.",
  },
} as const;

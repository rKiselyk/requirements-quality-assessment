export const lifecycle = {
  actions: {
    newSpecification: "New specification",
    tryAgain: "Try again",
  },
  analyzing: {
    title: "Analyzing specification",
    description: "The model is evaluating the supplied specification.",
    progressLabel: "Analysis in progress",
    resultNotice: "Results will appear when the analysis is complete.",
  },
  error: {
    title: "Analysis could not be completed",
  },
  result: {
    title: "Analysis result ready",
    subtitle: "The canonical response is retained for the Research UI result pages.",
    completed: "Analysis completed",
    boundary: "Detailed result presentation is deferred to RUI-07.",
    metadataTitle: "Canonical response metadata",
    analysisCase: "Analysis case",
    contractVersion: "Contract version",
  },
} as const;

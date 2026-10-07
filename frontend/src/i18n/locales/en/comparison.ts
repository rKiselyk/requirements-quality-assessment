export const comparison = {
  title: "Comparison",
  subtitle: "Model-produced ResultComparison records",
  before: "Before",
  after: "After",
  beforeAfter: "Before and after canonical values",
  none: "No canonical value",
  artifactIdentity: "Before / After artifact identity",
  records: {
    title: "Model-produced comparisons", resultFamily: "Result family", metric: "Metric / characteristic",
    identity: "Comparison record", status: "Status", kind: "Kind", beforeRef: "Before result ref", afterRef: "After result ref",
    rule: "Comparison rule", calibration: "Calibration", reasons: "Reasons", claims: "Claim", nonClaims: "Non-claims",
    compatibility: "Compatibility declarations", technical: "Technical detail", subject: "Comparison subject", parameters: "Parameter-set refs", provenance: "Provenance",
  },
  limitation: {
    title: "Scientific limitation",
    structured: "The comparison describes structured change only.",
    direction: "INCREASED is not automatically improvement, and DECREASED is not automatically deterioration.",
    causality: "The comparison does not prove that the corrective action caused the observed change.",
    action: "An APPLIED action state does not demonstrate action effectiveness, stakeholder intent, release readiness, or safety.",
  },
} as const;

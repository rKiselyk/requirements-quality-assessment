export const productQuality = {
  title: "Product Quality",
  subtitle: "Selected criterion, dynamic evidence, X_PE, and distinct observed and predicted results",
  revision: { CONTROLLED_DEMO_V1: "Current controlled-demo v1 result", REASSESSMENT_V2: "Current reassessed v2 result" },
  unavailable: {
    title: "Not available for this analysis",
    reasonCode: "Canonical reason code",
    noValue: "No observation, conformance, X_PE value, observed indicator, or prediction was inferred.",
    unknownReason: "The section is unavailable for the canonical reason shown below. No value was inferred.",
    reasons: { EXTERNAL_EVIDENCE_NOT_SUPPLIED: "Runtime observation evidence was not supplied. This is a valid specification-only result, not a failed assessment." },
  },
  malformed: { title: "Product Quality cannot be safely presented", description: "The canonical section is marked available, but the current-version records or required identities are malformed.", record: "Canonical record cannot be safely presented" },
  technical: { details: "Canonical technical details", reference: "View canonical reference", none: "None", noNumericValue: "No numeric value" },
  criterion: { title: "Selected criterion", requirement: "Requirement identity", openRequirement: "Open {{id}}", expressionLabel: "Canonical quantitative criterion", inclusivity: "Inclusivity", context: "Normalized context identity", sourceObservation: "Source observation reference", bindingRule: "Binding rule", noValue: "No criterion value is present for this canonical state." },
  observationConformance: { title: "Observation & conformance" },
  observation: { title: "Dynamic observation", observedValue: "Exact observed decimal", metric: "Metric", context: "Context", sourceKind: "Source kind", sourceRecord: "Fixture/source record", product: "Product identity", environment: "Environment", collection: "Collection identity", fixtureBoundary: "DETERMINISTIC_FIXTURE is controlled fixture evidence, not live or production telemetry.", noValue: "No observation value is present for this canonical state." },
  conformance: { title: "Criterion conformance", outcome: "Canonical outcome", noOutcome: "No conformance outcome is present for this canonical state." },
  features: {
    title: "Performance Efficiency feature profile (X_PE)", description: "A bounded seven-slot feature profile; it is not a combined score or complete Performance Efficiency coverage.", caption: "Canonical X_PE feature registry", id: "Feature ID", effect: "Effect", state: "Status / applicability", value: "Typed value", availabilityPoint: "Availability / trace", characteristic: "Bounded characteristic", registry: "Registry identity", mappingRule: "Mapping rule", processState: "Process state", noTypedValue: "No typed value", structuredValue: "Structured canonical value", typedValueDetails: "View typed value", profileDetails: "View complete profile record",
    effects: { REQUIRED_INPUT: "Required input", CONTEXT_ONLY: "Context only", ELIGIBILITY_GATE: "Eligibility gate", DIRECT_RESULT_INPUT: "Direct result input" },
  },
  observed: { title: "Observed product-quality evidence", resultKind: "Canonical result kind", exactValue: "Exact bounded indicator", characteristic: "Characteristic", numericRepresentation: "Numeric representation", conformanceOutcome: "Source conformance outcome", calibration: "Calibration status" },
  prediction: { title: "Predicted product quality", resultKind: "Canonical result kind", exactValue: "Exact predicted value", predictor: "Predictor identity/version", parameterSet: "Parameter-set identity/version", calibration: "Calibration status", numericRepresentation: "Numeric representation", withheldReason: "Canonical withheld reason", noCurrentTitle: "No current prediction record", noCurrentDescription: "No prediction record was produced for this current result. A prior-version prediction is not reused as a current result.", calibrationBoundary: "Calibration is scientific metadata. It is not interpreted as confidence, reliability, uncertainty, accuracy, or validity." },
  nonClaims: {
    title: "Canonical observed-result non-claims",
    items: {
      "NC-PE-001": "Not complete Performance Efficiency.", "NC-PE-002": "Not predicted product quality.", "NC-PE-003": "Not an actual aggregated y_PE.", "NC-PE-004": "Not probability, confidence, reliability, or accuracy.", "NC-PE-005": "No model uncertainty estimate.", "NC-PE-006": "No causal claim from requirement quality.", "NC-PE-007": "No validation of the requirement target or stakeholder need.", "NC-PE-008": "No other Performance Efficiency metrics or contexts were assessed.", "NC-PE-009": "No scalar overall product or requirement quality.",
    },
  },
  limitations: { title: "Scientific limitations", observedPredictedTitle: "Observed result ≠ predicted result", observedPredicted: "The bounded observed reference indicator and predicted Performance Efficiency are different scientific result families and are never combined.", bounded: "A bounded single-criterion indicator is not complete Performance Efficiency.", prediction: "Prediction does not imply confidence, empirical validation, reliability, uncertainty, accuracy, causality, or universal predictive validity." },
} as const;

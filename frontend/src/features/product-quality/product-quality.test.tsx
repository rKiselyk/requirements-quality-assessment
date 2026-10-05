import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../../App";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { i18n } from "../../i18n";
import { ProductQualityPage } from "./ProductQualityPage";
import { peFeatureEffects, peFeatureIds, productQualityNonClaims, selectProductQualityPage } from "./projection";

const artifactV1 = { artifact_id: "SPEC-PQ", artifact_version: "1" };
const artifactV2 = { artifact_id: "SPEC-PQ", artifact_version: "2" };
const rule = { rule_id: "RULE", rule_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };

function featureProfile(artifact = artifactV1) {
  const profileId = {
    artifact_ref: artifact,
    source_assessment_ref: { assessment_id: "ASSESS", assessment_version: artifact.artifact_version, artifact_ref: artifact },
    metric_profile_ref: { profile_id: "METRICS", profile_version: artifact.artifact_version, artifact_ref: artifact },
    dynamic_assessment_ref: { assessment_id: "DYN", assessment_version: artifact.artifact_version, artifact_ref: artifact },
    product_ref: { product_id: "PRODUCT", product_version: "1" },
    process_state_ref: { process_state_id: "PROCESS", process_state_version: artifact.artifact_version, stage: "REFERENCE_VERIFICATION" },
    feature_registry_ref: { contract_id: "FULL-MODEL-V0.1-PE-FEATURES", contract_version: "1" },
    mapping_rule_ref: rule,
  };
  const typedValues = [
    { exact_decimal_bound: "2.0", metric_ref: { metric_id: "DYN.RESPONSE_TIME" } },
    { exact_fraction_or_none: { numerator: 1, denominator: 1 } },
    { exact_fraction_or_none: { numerator: 2, denominator: 3 } },
    { exact_fraction_or_none: { numerator: 1, denominator: 2 } },
    { source_exact_fraction_or_none: { numerator: 4, denominator: 5 }, gate_decision: "TARGET_CLEAR" },
    { exact_decimal_value: "1.80", metric_ref: { metric_id: "DYN.RESPONSE_TIME" } },
    { outcome: "CONFORMS" },
  ];
  return {
    profile_id: profileId,
    characteristic_id: "PERFORMANCE_EFFICIENCY",
    artifact_ref: artifact,
    source_assessment_ref: profileId.source_assessment_ref,
    metric_profile_ref: profileId.metric_profile_ref,
    dynamic_assessment_ref: profileId.dynamic_assessment_ref,
    product_ref: profileId.product_ref,
    process_state_ref: profileId.process_state_ref,
    criterion_subject_ref: { requirement_id: "R001", artifact_ref: artifact },
    target_key: { key: "response-time" },
    status: "AVAILABLE",
    applicability: "APPLICABLE",
    features: peFeatureIds.map((featureId, index) => ({
      feature_entry_id: { profile_id: profileId, feature_id: featureId },
      feature_id: featureId,
      characteristic_id: "PERFORMANCE_EFFICIENCY",
      effect: peFeatureEffects[index],
      status: "AVAILABLE",
      applicability: "APPLICABLE",
      typed_value: typedValues[index],
      source_refs: [{ source: featureId }],
      evidence_refs: [],
      provenance_refs: [],
      artifact_ref: artifact,
      source_assessment_ref: profileId.source_assessment_ref,
      product_ref: index >= 5 ? profileId.product_ref : null,
      availability_point: "SOURCE_ASSESSMENT_AVAILABLE",
      rule_refs: [rule],
      reasons: [],
      explanation: `Canonical ${featureId}`,
    })),
    provenance: { ordered_feature_entry_refs: [] },
    registry_ref: profileId.feature_registry_ref,
    mapping_rule_ref: rule,
  };
}

function currentRecords(artifact = artifactV1, marker = "CURRENT") {
  const profile = featureProfile(artifact);
  const predictorRef = { predictor_id: `PREDICTOR-${marker}`, predictor_version: "1" };
  const parameterSetRef = { identity: { parameter_set_id: `THETA-${marker}`, parameter_set_version: "1" }, predictor_ref: predictorRef };
  const selectedInputRefs = profile.features.map((feature) => feature.feature_entry_id);
  const contextInputs = [{ field: "PRODUCT", value_or_none: profile.product_ref }];
  const requirementSubjectRef = profile.criterion_subject_ref;
  const sourceObservationRef = { requirement_id: "R001", feature_id: "quantitative_constraint", observation_index: 0 };
  const sourceSnapshotId = { value: `SNAPSHOT-${artifact.artifact_version}` };
  const bindingId = {
    artifact_ref: artifact,
    source_assessment_ref: profile.source_assessment_ref,
    requirement_subject_ref: requirementSubjectRef,
    source_snapshot_id: sourceSnapshotId,
    source_observation_ref: sourceObservationRef,
    binding_rule_ref: rule,
  };
  const collectionRef = {
    collection_id: "COLLECTION", collection_version: "1", product_ref: profile.product_ref,
    environment_ref: { environment_id: "ENV", environment_version: "1" }, source_kind: "DETERMINISTIC_FIXTURE",
  };
  const slotRef = { collection_ref: collectionRef, fixture_sequence: 0 };
  const observationId = { collection_ref: collectionRef, fixture_sequence: 0 };
  const metricRef = { metric_id: "DYN.RESPONSE_TIME" };
  const criterionContext = { normalized_text: "500 concurrent users" };
  const dynamicAssessmentRef = profile.dynamic_assessment_ref;
  const conformanceId = {
    dynamic_assessment_ref: dynamicAssessmentRef,
    criterion_binding_id: bindingId,
    observation_slot_ref: slotRef,
    evaluator_rule_ref: rule,
  };
  const criterionRef = { criterion_id: bindingId };
  const observationRef = { observation_id: observationId };
  const sourceStatus = { status: "COMPUTED", applicability: "APPLICABLE" };
  const metricEntry = (metricId: string) => ({ metric_profile_ref: profile.metric_profile_ref, metric_id: metricId });
  const typedValues = [
    { criterion_ref: criterionRef, metric_ref: metricRef, comparator: "LESS_THAN_OR_EQUAL", inclusivity: "INCLUSIVE", exact_decimal_bound: marker === "STALE" ? "99" : "2.0", unit: "SECOND", context_identity: criterionContext },
    { metric_entry_ref: metricEntry("C"), exact_fraction_or_none: { numerator: 1, denominator: 1 }, numeric_representation: "EXACT_FRACTION", source_status: sourceStatus },
    { metric_entry_ref: metricEntry("V"), exact_fraction_or_none: { numerator: 2, denominator: 3 }, numeric_representation: "EXACT_FRACTION", source_status: sourceStatus },
    { metric_entry_ref: metricEntry("U"), exact_fraction_or_none: { numerator: 1, denominator: 2 }, numeric_representation: "EXACT_FRACTION", source_status: sourceStatus },
    { qb_metric_entry_ref: metricEntry("QB"), source_metric_status: "COMPUTED", source_metric_applicability: "APPLICABLE", source_exact_fraction_or_none: { numerator: 4, denominator: 5 }, gate_decision: "TARGET_CLEAR", target_key: profile.target_key, ordered_cross_result_refs: [] },
    { observation_ref: observationRef, metric_ref: metricRef, exact_decimal_value: marker === "STALE" ? "88" : "1.80", unit: "SECOND", context_identity: criterionContext },
    { conformance_ref: conformanceId, outcome: "CONFORMS" },
  ];
  profile.features.forEach((feature, index) => { Object.assign(feature, { typed_value: typedValues[index] }); });
  Object.assign(profile.provenance, {
    artifact_ref: artifact,
    source_assessment_ref: profile.source_assessment_ref,
    source_snapshot_id: sourceSnapshotId,
    metric_profile_ref: profile.metric_profile_ref,
    criterion_binding_ref: bindingId,
    observation_resolution_ref: slotRef,
    conformance_assessment_ref: conformanceId,
    dynamic_assessment_ref: dynamicAssessmentRef,
    product_ref: profile.product_ref,
    environment_ref_or_none: collectionRef.environment_ref,
    collection_ref_or_none: collectionRef,
    process_state_ref: profile.process_state_ref,
    ordered_feature_entry_refs: profile.features.map((feature) => feature.feature_entry_id),
    source_contract_refs: [{ contract_id: "FULL-MODEL-V0.1", contract_version: "1" }],
    rule_refs: [rule],
  });
  return {
    criterion_binding: {
      binding_id: bindingId, status: "AVAILABLE", applicability: "APPLICABLE",
      criterion: { criterion_id: bindingId, requirement_subject_ref: requirementSubjectRef, artifact_ref: artifact, source_assessment_ref: profile.source_assessment_ref, source_snapshot_id: sourceSnapshotId, source_observation_ref: sourceObservationRef, metric_ref: metricRef, comparator: "LESS_THAN_OR_EQUAL", inclusivity: "INCLUSIVE", bound: marker === "STALE" ? "99" : "2.0", unit: "SECOND", context_identity: criterionContext, provenance: {}, binding_rule_ref: rule },
      source_observation_ref: sourceObservationRef, reasons: [], provenance: { requirement_subject_ref: requirementSubjectRef, source_observation_ref: sourceObservationRef, binding_rule_ref: rule, evidence_refs: [{ requirement_id: "R001", evidence_id: "E003" }] },
    },
    observation_resolution: {
      slot_ref: slotRef, status: "AVAILABLE", applicability: "APPLICABLE",
      observation: { observation_id: observationId, slot_ref: slotRef, product_ref: profile.product_ref, metric_ref: metricRef, observed_value: marker === "STALE" ? "88" : "1.80", unit: "SECOND", context_identity: criterionContext, source_kind: "DETERMINISTIC_FIXTURE", collection_ref: collectionRef, fixture_sequence: 0, collected_at: null, provenance: { product_ref: profile.product_ref, collection_ref: collectionRef, fixture_sequence: 0, declared_metric_ref: metricRef, declared_unit: "SECOND", declared_context_identity: criterionContext, source_kind: "DETERMINISTIC_FIXTURE", source_record_ref: `FIXTURE-${marker}` } },
      reasons: [], provenance_refs: [`FIXTURE-${marker}`],
    },
    conformance: { conformance_id: conformanceId, dynamic_assessment_ref: dynamicAssessmentRef, criterion_binding_id: bindingId, criterion_id: bindingId, observation_slot_ref: slotRef, observation_id: observationId, status: "AVAILABLE", applicability: "APPLICABLE", outcome: "CONFORMS", explanation: "Canonical backend conformance result.", reasons: [], criterion_ref: criterionRef, observation_ref: observationRef, evidence_refs: [{ evidence_id: "E003" }], provenance: { criterion_ref: criterionRef, observation_ref: observationRef, evaluator_rule_ref: rule }, evaluator_rule_ref: rule },
    feature_profile: profile,
    observed_product_quality: observed(artifact, profile, marker, bindingId, observationId, conformanceId),
    product_quality_assessment: observed(artifact, profile, marker, bindingId, observationId, conformanceId),
    prediction: prediction(profile, predictorRef, parameterSetRef, selectedInputRefs, contextInputs, marker),
  };
}

function observed(artifact: typeof artifactV1, profile: ReturnType<typeof featureProfile>, marker: string, criterionId: Record<string, unknown>, observationId: Record<string, unknown>, conformanceId: Record<string, unknown>) {
  const modelRef = { model_id: "FULL-MODEL-V0.1-M-QUALITY-PE", model_version: "1" };
  const parameterSetRef = { parameter_set_id: "PE-OBS-CONFORMANCE-001-PARAMETERS", parameter_set_version: "1" };
  const featureRefs = profile.features.map((feature) => feature.feature_entry_id);
  const evidenceRefs: unknown[] = [];
  const assessmentEventRef = { assessment_event_id: `EVENT-${marker}`, assessment_event_version: "1", product_ref: profile.product_ref, artifact_ref: artifact };
  const assessmentId = { assessment_event_ref: assessmentEventRef, feature_profile_ref: profile.profile_id, characteristic_id: "PERFORMANCE_EFFICIENCY", result_kind: "OBSERVED_REFERENCE_INDICATOR", model_ref: modelRef, procedure_rule_ref: rule, parameter_set_ref: parameterSetRef };
  return {
    assessment_id: assessmentId, assessment_event_ref: assessmentEventRef, characteristic_id: "PERFORMANCE_EFFICIENCY", product_ref: profile.product_ref, artifact_ref: artifact, feature_profile_ref: profile.profile_id,
    scope: { scope_kind: "SINGLE_CRITERION_SINGLE_OBSERVATION", characteristic_id: "PERFORMANCE_EFFICIENCY", dynamic_metric_ref: { metric_id: "DYN.RESPONSE_TIME" }, criterion_ref: { criterion_id: criterionId }, observation_ref: { observation_id: observationId }, conformance_ref: conformanceId, product_ref: profile.product_ref, environment_ref: (profile.provenance as Record<string, unknown>).environment_ref_or_none, collection_ref: (profile.provenance as Record<string, unknown>).collection_ref_or_none, context_identity: { normalized_text: "500 concurrent users" }, unit: "SECOND", process_stage: "REFERENCE_VERIFICATION", full_characteristic_coverage: "NOT_ESTABLISHED" }, scope_statement: "One response-time criterion and one observation.", result_kind: "OBSERVED_REFERENCE_INDICATOR", status: "AVAILABLE", applicability: "APPLICABLE", source_conformance_outcome: "CONFORMS", value: { numerator: 1, denominator: 1 }, prediction_value: null, observed_value: { numerator: 1, denominator: 1 }, numeric_representation: "EXACT_FRACTION", evidence_coverage: { coverage_kind: "BOUNDED_REQUIRED_CHANNEL_INVENTORY" }, reliability: null, uncertainty: null, explanation: "Bounded observed indicator.", feature_refs: featureRefs, evidence_refs: evidenceRefs, provenance: { feature_profile_ref: profile.profile_id, product_ref: profile.product_ref, process_state_ref: profile.process_state_ref, model_ref: modelRef, parameter_set_ref: parameterSetRef, ordered_feature_refs: featureRefs, source_evidence_refs: evidenceRefs, rule_refs: [rule] }, model_ref: modelRef, procedure_rule_ref: rule, parameter_set_ref: parameterSetRef, calibration_status: "PROVISIONAL_NOT_CALIBRATED", artifact_version: artifact.artifact_version, source_assessment_version: profile.source_assessment_ref.assessment_version, product_version: profile.product_ref.product_version, product_quality_assessment_version: assessmentEventRef.assessment_event_version, non_claims: [...productQualityNonClaims],
  };
}

function prediction(profile: ReturnType<typeof featureProfile>, predictorRef: Record<string, unknown>, parameterSetRef: Record<string, unknown>, selectedInputRefs: unknown[], contextInputs: unknown[], marker: string) {
  return {
    event_ref: { prediction_event_id: `PREDICTION-${marker}`, prediction_event_version: "1" }, result_kind: "PREDICTED_PERFORMANCE_EFFICIENCY", characteristic_id: "PERFORMANCE_EFFICIENCY", status: "AVAILABLE", applicability: "APPLICABLE", predicted_value: { numerator: 5, denominator: 6 }, numeric_representation: "EXACT_FRACTION", predictor_ref: predictorRef, parameter_set_ref: parameterSetRef, calibration_status: "PROVISIONAL_NOT_CALIBRATED", selected_input_refs: selectedInputRefs, context_inputs: contextInputs, artifact_ref: profile.artifact_ref, product_ref: profile.product_ref, process_state_ref: profile.process_state_ref, governing_contract_ref: {}, rule_refs: [rule], explanation: "Fixture-only bounded prediction.",
    provenance: { feature_profile_ref: profile.profile_id, input_traces: selectedInputRefs.map((feature_ref) => ({ feature_ref })), context_inputs: contextInputs, predictor_definition: { predictor_ref: predictorRef, parameter_set_identity: parameterSetRef.identity, calibration_status: "PROVISIONAL_NOT_CALIBRATED", source_or_rationale: "Fixture-only rationale." }, parameter_set_ref: parameterSetRef, parameter_entries: [{ name: "alpha", exact_value: { numerator: 1, denominator: 2 } }], parameter_source_or_rationale: "Controlled fixture parameter source.", contract_refs: [], rule_refs: [rule], withheld_reason_or_none: null },
  };
}

function requirementResult() {
  const feature = (featureId: string) => ({ feature_id: featureId, observations: [], diagnostics: [] });
  return {
    requirement: { id: "R001", source_line: 1, text: "Canonical requirement text." },
    quality_profile: {},
    evidence: [],
    features: {
      condition_contexts: feature("condition_context"),
      expected_results: feature("expected_result"),
      acceptance_criteria: feature("acceptance_criterion"),
      quantitative_constraints: feature("quantitative_constraint"),
      verification_methods: feature("verification_method"),
      vague_term_occurrences: feature("vague_term_occurrence"),
    },
    trace: null,
  };
}

function response(caseName: CanonicalAnalyzeResponse["analysis_case"] = "CONTROLLED_DEMO"): CanonicalAnalyzeResponse {
  return {
    contract_version: "research-api-v1", analysis_case: caseName, controlled_scenario: caseName === "INITIAL" ? null : { id: "SCENARIO", version: "1" },
    requirements: [requirementResult()], specification: { snapshot_id: "SNAPSHOT" },
    section_availability: [{ section: "product_quality", availability: caseName === "INITIAL" ? "UNAVAILABLE" : "AVAILABLE", reason_code: caseName === "INITIAL" ? "EXTERNAL_EVIDENCE_NOT_SUPPLIED" : null }],
    full_model: caseName === "INITIAL" ? null : currentRecords(), reassessment_context: null, limitations: [],
  };
}

function reassessmentResponse(mismatch = false): CanonicalAnalyzeResponse {
  const stale = currentRecords(artifactV1, "STALE");
  const riskAssessmentId = { assessment: "RISK", artifact_ref: artifactV2 };
  const current = { artifact_ref: artifactV2, ...currentRecords(artifactV2, "CURRENT"), risk_assessment: { risk_assessment_id: riskAssessmentId } };
  return {
    ...response("REASSESSMENT"),
    full_model: {
      ...stale,
      reassessment: {
        context: { child_artifact_ref: artifactV2 },
        provenance: { child_artifact_ref: artifactV2 },
        produced_result_refs: [
          { result_family: "CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH", result_id: "CORE", artifact_ref: artifactV2 },
          { result_family: "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH", result_id: riskAssessmentId, artifact_ref: mismatch ? artifactV1 : artifactV2 },
        ],
        produced_results: [{ artifact_ref: artifactV2, core: true }, current],
      },
    },
  };
}

describe("RUI-10 Product Quality", () => {
  beforeEach(async () => { window.sessionStorage.clear(); await i18n.changeLanguage("en"); });
  afterEach(() => { cleanup(); vi.restoreAllMocks(); });

  it("renders INITIAL as a readable unavailable page without fabricated values", () => {
    render(<ProductQualityPage result={response("INITIAL")} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Product Quality" })).toBeTruthy();
    expect(screen.getByText("EXTERNAL_EVIDENCE_NOT_SUPPLIED")).toBeTruthy();
    expect(screen.getByText(/No observation, conformance, X_PE value/)).toBeTruthy();
    expect(screen.queryByText(/1\.80|5\/6|0\/1/)).toBeNull();
  });

  it("opens Product Quality and switches locale without another analysis request or response mutation", async () => {
    const payload = response("INITIAL");
    payload.section_availability = [
      { section: "overview", availability: "AVAILABLE", reason_code: null },
      { section: "requirements", availability: "AVAILABLE", reason_code: null },
      { section: "specification", availability: "AVAILABLE", reason_code: null },
      ...payload.section_availability,
    ];
    payload.specification = { snapshot_id: "SNAPSHOT", quality_profile: {}, qb_consistency: {} };
    const before = JSON.stringify(payload);
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ ok: true, json: async () => payload } as Response);
    const client = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
    render(<QueryClientProvider client={client}><App /></QueryClientProvider>);
    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    await screen.findByRole("heading", { name: "Overview" });
    fireEvent.click(screen.getByRole("button", { name: "Product Quality" }));
    await screen.findByText("EXTERNAL_EVIDENCE_NOT_SUPPLIED");
    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));
    expect(await screen.findByRole("heading", { name: "Якість продукту" })).toBeTruthy();
    expect(globalThis.fetch).toHaveBeenCalledTimes(1);
    expect(JSON.stringify(payload)).toBe(before);
    fireEvent.click(screen.getByRole("button", { name: "Нова специфікація" }));
    expect(await screen.findByRole("heading", { name: "Аналіз специфікації" })).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "Якість продукту" })).toBeNull();
    expect(globalThis.fetch).toHaveBeenCalledTimes(1);
  });

  it("selects controlled-demo v1 records and preserves decimals, registry order, effects, exact fractions, and identities", () => {
    const projected = selectProductQualityPage(response());
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.revision).toBe("CONTROLLED_DEMO_V1");
    expect(projected.criterion?.bound).toBe("2.0");
    expect(projected.observation?.observedValue).toBe("1.80");
    expect(projected.observation?.sourceKind).toBe("DETERMINISTIC_FIXTURE");
    expect(projected.conformance?.outcome).toBe("CONFORMS");
    expect(projected.featureProfile?.features.map((item) => item.featureId)).toEqual(peFeatureIds);
    expect(projected.featureProfile?.features.map((item) => item.effect)).toEqual(peFeatureEffects);
    expect(projected.observed?.observedValue).toEqual({ numerator: "1", denominator: "1" });
    expect(projected.prediction.kind === "PRESENT" && projected.prediction.value.predictedValue).toEqual({ numerator: "5", denominator: "6" });
    expect(projected.prediction.kind === "PRESENT" && projected.prediction.value.calibrationStatus).toBe("PROVISIONAL_NOT_CALIBRATED");
  });

  it("renders observed and predicted results separately without telemetry, percentage, reliability, or overall-score claims", () => {
    render(<ProductQualityPage result={response()} onSelectRequirement={vi.fn()} />);
    const observedSection = screen.getByRole("heading", { name: "Observed product-quality evidence" }).closest("section")!;
    const predictionSection = screen.getByRole("heading", { name: "Predicted product quality" }).closest("section")!;
    expect(within(observedSection).getByText("OBSERVED_REFERENCE_INDICATOR")).toBeTruthy();
    expect(within(observedSection).getByLabelText("Exact value: 1/1")).toBeTruthy();
    expect(within(predictionSection).getByText("PREDICTED_PERFORMANCE_EFFICIENCY")).toBeTruthy();
    expect(within(predictionSection).getByLabelText("Exact value: 5/6")).toBeTruthy();
    expect(screen.getByText(/not live or production telemetry/)).toBeTruthy();
    expect(screen.getAllByText("PROVISIONAL_NOT_CALIBRATED").length).toBeGreaterThan(0);
    expect(document.body.textContent).not.toMatch(/overall product-quality score|% quality|confidence meter/i);
    expect(Array.from(observedSection.querySelectorAll(".non-claims code"), (node) => node.textContent)).toEqual(productQualityNonClaims);
  });

  it("presents the backend conformance outcome without reevaluating the comparator", () => {
    const value = response();
    const model = value.full_model as Record<string, unknown>;
    const binding = model.criterion_binding as Record<string, unknown>;
    (binding.criterion as Record<string, unknown>).bound = "0.01";
    const resolution = model.observation_resolution as Record<string, unknown>;
    (resolution.observation as Record<string, unknown>).observed_value = "999.0";
    render(<ProductQualityPage result={value} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Criterion conformance" }).closest("section")?.textContent).toContain("CONFORMS");
    expect(screen.queryByText("DOES_NOT_CONFORM")).toBeNull();
  });

  it("keeps an unavailable feature value absent and rejects a contradictory non-available feature value", () => {
    const valid = response();
    const model = valid.full_model as Record<string, unknown>;
    const profile = model.feature_profile as ReturnType<typeof featureProfile>;
    profile.features[1] = { ...profile.features[1], status: "UNAVAILABLE", applicability: "APPLICABLE", typed_value: null, reasons: ["SOURCE_ASSESSMENT_UNAVAILABLE"] } as unknown as typeof profile.features[number];
    const validProjection = selectProductQualityPage(valid);
    expect(validProjection.kind === "AVAILABLE" && validProjection.featureProfile).not.toBeNull();
    const invalid = structuredClone(valid);
    const invalidProfile = (invalid.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    invalidProfile.features[1].typed_value = { exact_fraction_or_none: { numerator: 0, denominator: 1 } };
    const projected = selectProductQualityPage(invalid);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it.each([
    ["available prediction missing value", (value: Record<string, unknown>) => { value.predicted_value = null; }],
    ["available prediction with non-applicable applicability", (value: Record<string, unknown>) => { value.applicability = "NOT_APPLICABLE"; }],
    ["predictor identity mismatch", (value: Record<string, unknown>) => { value.predictor_ref = { predictor_id: "OTHER", predictor_version: "1" }; }],
  ])("uses the malformed boundary for %s", (_label, mutate) => {
    const value = response();
    mutate((value.full_model as Record<string, unknown>).prediction as Record<string, unknown>);
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.prediction).toEqual({ kind: "MALFORMED" });
    render(<ProductQualityPage result={value} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Predicted product quality" }).closest("section")?.textContent).toContain("Canonical record cannot be safely presented");
  });

  it("preserves a withheld prediction reason and renders no numeric value", () => {
    const value = response();
    const predictionRecord = (value.full_model as Record<string, unknown>).prediction as Record<string, unknown>;
    predictionRecord.status = "UNAVAILABLE";
    predictionRecord.predicted_value = null;
    predictionRecord.numeric_representation = "NONE";
    ((predictionRecord.provenance as Record<string, unknown>)).withheld_reason_or_none = "REQUIRED_X_PE_INPUT_NOT_AVAILABLE";
    render(<ProductQualityPage result={value} onSelectRequirement={vi.fn()} />);
    const section = screen.getByRole("heading", { name: "Predicted product quality" }).closest("section")!;
    expect(within(section).getByText("REQUIRED_X_PE_INPUT_NOT_AVAILABLE")).toBeTruthy();
    expect(within(section).getByText("No numeric value")).toBeTruthy();
    expect(within(section).queryByText("0")).toBeNull();
  });

  it("rejects a non-available prediction that carries a numeric value", () => {
    const value = response();
    const predictionRecord = (value.full_model as Record<string, unknown>).prediction as Record<string, unknown>;
    predictionRecord.status = "UNAVAILABLE";
    predictionRecord.numeric_representation = "NONE";
    ((predictionRecord.provenance as Record<string, unknown>)).withheld_reason_or_none = "REQUIRED_CONTEXT_INPUT_NOT_AVAILABLE";
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.prediction).toEqual({ kind: "MALFORMED" });
  });

  it("selects the paired reassessment v2 dynamic result and never reuses top-level v1 records or prediction", () => {
    const projected = selectProductQualityPage(reassessmentResponse());
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.revision).toBe("REASSESSMENT_V2");
    expect(projected.criterion?.bound).toBe("2.0");
    expect(projected.criterion?.raw).not.toEqual((reassessmentResponse().full_model as Record<string, unknown>).criterion_binding);
    expect(projected.observed?.raw.artifact_ref).toEqual(artifactV2);
    expect(projected.prediction).toEqual({ kind: "ABSENT" });
    render(<ProductQualityPage result={reassessmentResponse()} onSelectRequirement={vi.fn()} />);
    expect(screen.getByText(/No prediction record was produced for this current result/)).toBeTruthy();
    expect(screen.queryByText("PREDICTOR-STALE")).toBeNull();
  });

  it("fails safely when the paired produced-result artifact does not match the reassessment child", () => {
    expect(selectProductQualityPage(reassessmentResponse(true))).toEqual({ kind: "MALFORMED" });
    render(<ProductQualityPage result={reassessmentResponse(true)} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Product Quality cannot be safely presented" })).toBeTruthy();
  });

  it.each([
    ["criterion NOT_APPLICABLE + APPLICABLE", "criterion_binding", "NOT_APPLICABLE", "APPLICABLE", "criterion"],
    ["observation UNAVAILABLE + NOT_APPLICABLE", "observation_resolution", "UNAVAILABLE", "NOT_APPLICABLE", "observation"],
    ["observed NOT_APPLICABLE + APPLICABLE", "observed_product_quality", "NOT_APPLICABLE", "APPLICABLE", "observed"],
  ])("rejects invalid status/applicability: %s", (_label, recordName, status, applicability, projectionName) => {
    const value = response();
    const scientificRecord = (value.full_model as Record<string, unknown>)[recordName] as Record<string, unknown>;
    scientificRecord.status = status;
    scientificRecord.applicability = applicability;
    const projected = selectProductQualityPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind === "AVAILABLE") expect(projected[projectionName as "criterion" | "observation" | "observed"]).toBeNull();
  });

  it("rejects an invalid X_PE feature status/applicability pair", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    profile.features[0].status = "UNAVAILABLE";
    profile.features[0].applicability = "NOT_APPLICABLE";
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects an invalid prediction status/applicability pair", () => {
    const value = response();
    const predictionRecord = (value.full_model as Record<string, unknown>).prediction as Record<string, unknown>;
    predictionRecord.status = "UNAVAILABLE";
    predictionRecord.applicability = "NOT_APPLICABLE";
    predictionRecord.predicted_value = null;
    predictionRecord.numeric_representation = "NONE";
    (predictionRecord.provenance as Record<string, unknown>).withheld_reason_or_none = "REQUIRED_X_PE_INPUT_NOT_AVAILABLE";
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.prediction).toEqual({ kind: "MALFORMED" });
  });

  it.each([
    ["binding requirement subject", (binding: Record<string, unknown>) => {
      const bindingId = binding.binding_id as Record<string, unknown>;
      binding.binding_id = { ...bindingId, requirement_subject_ref: { ...(bindingId.requirement_subject_ref as Record<string, unknown>), requirement_id: "R999" } };
    }],
    ["criterion source observation", (binding: Record<string, unknown>) => {
      const criterion = binding.criterion as Record<string, unknown>;
      criterion.source_observation_ref = { ...(criterion.source_observation_ref as Record<string, unknown>), observation_index: 9 };
    }],
  ])("rejects criterion identity mismatch: %s", (_label, mutate) => {
    const value = response();
    mutate((value.full_model as Record<string, unknown>).criterion_binding as Record<string, unknown>);
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.criterion).toBeNull();
  });

  it("rejects a resolved observation slot mismatch", () => {
    const value = response();
    const resolution = (value.full_model as Record<string, unknown>).observation_resolution as Record<string, unknown>;
    ((resolution.observation as Record<string, unknown>).slot_ref as Record<string, unknown>).fixture_sequence = 7;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.observation).toBeNull();
  });

  it.each([
    ["metric", "declared_metric_ref", { metric_id: "OTHER" }],
    ["unit", "declared_unit", "MILLISECOND"],
    ["context", "declared_context_identity", { normalized_text: "other context" }],
  ])("rejects observation provenance %s mismatch", (_label, field, replacement) => {
    const value = response();
    const resolution = (value.full_model as Record<string, unknown>).observation_resolution as Record<string, unknown>;
    const observationRecord = resolution.observation as Record<string, unknown>;
    (observationRecord.provenance as Record<string, unknown>)[field] = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.observation).toBeNull();
  });

  it.each([
    ["binding", "criterion_binding_id", { wrong: "binding" }],
    ["criterion", "criterion_id", { wrong: "criterion" }],
    ["observation", "observation_id", { wrong: "observation" }],
  ])("rejects conformance %s identity mismatch", (_label, field, replacement) => {
    const value = response();
    const conformanceRecord = (value.full_model as Record<string, unknown>).conformance as Record<string, unknown>;
    conformanceRecord[field] = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.conformance).toBeNull();
  });

  it("rejects an X_PE profile identity mismatch", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    profile.profile_id.product_ref = { product_id: "OTHER", product_version: "1" };
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects an X_PE feature entry that names another profile", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    profile.features[2].feature_entry_id.profile_id = { ...profile.profile_id, artifact_ref: artifactV2 };
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it.each([
    ["feature profile", "feature_profile_ref", { stale: "profile" }],
    ["product", "product_ref", { product_id: "OTHER", product_version: "1" }],
  ])("rejects observed %s mismatch", (_label, field, replacement) => {
    const value = response();
    const observedRecord = (value.full_model as Record<string, unknown>).observed_product_quality as Record<string, unknown>;
    observedRecord[field] = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.observed).toBeNull();
  });

  it("rejects a stale v1 observed artifact inside a valid v2 downstream container", () => {
    const value = reassessmentResponse();
    const reassessment = (value.full_model as Record<string, unknown>).reassessment as Record<string, unknown>;
    const downstream = (reassessment.produced_results as unknown[])[1] as Record<string, unknown>;
    (downstream.product_quality_assessment as Record<string, unknown>).artifact_ref = artifactV1;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.observed).toBeNull();
  });

  it("rejects a stale v1 X_PE profile inside a valid v2 downstream container", () => {
    const value = reassessmentResponse();
    const reassessment = (value.full_model as Record<string, unknown>).reassessment as Record<string, unknown>;
    const downstream = (reassessment.produced_results as unknown[])[1] as Record<string, unknown>;
    downstream.feature_profile = (value.full_model as Record<string, unknown>).feature_profile;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
    expect(projected.kind === "AVAILABLE" && projected.observed).toBeNull();
  });

  it("rejects observed conformance-outcome disagreement without recomputing either result", () => {
    const value = response();
    const observedRecord = (value.full_model as Record<string, unknown>).observed_product_quality as Record<string, unknown>;
    observedRecord.source_conformance_outcome = "DOES_NOT_CONFORM";
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.conformance?.outcome).toBe("CONFORMS");
    expect(projected.kind === "AVAILABLE" && projected.observed).toBeNull();
  });

  it.each([
    ["value differs from observed_value", { numerator: 0, denominator: 1 }],
    ["fraction exceeds one", { numerator: 2, denominator: 1 }],
  ])("rejects observed exact-value inconsistency: %s", (_label, replacement) => {
    const value = response();
    const observedRecord = (value.full_model as Record<string, unknown>).observed_product_quality as Record<string, unknown>;
    observedRecord.value = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.observed).toBeNull();
  });

  it("renders a null controlled-demo prediction as neutral absence", () => {
    const value = response();
    (value.full_model as Record<string, unknown>).prediction = null;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.prediction).toEqual({ kind: "ABSENT" });
    render(<ProductQualityPage result={value} onSelectRequirement={vi.fn()} />);
    const section = screen.getByRole("heading", { name: "Predicted product quality" }).closest("section")!;
    expect(within(section).getByText(/No prediction record was produced for this current result/)).toBeTruthy();
    expect(within(section).queryByText("Canonical record cannot be safely presented")).toBeNull();
  });

  it.each([
    ["artifact", "artifact_ref", artifactV2],
    ["product", "product_ref", { product_id: "OTHER", product_version: "1" }],
    ["process", "process_state_ref", { process_state_id: "OTHER", process_state_version: "1", stage: "REFERENCE_VERIFICATION" }],
  ])("rejects prediction %s mismatch with X_PE", (_label, field, replacement) => {
    const value = response();
    const predictionRecord = (value.full_model as Record<string, unknown>).prediction as Record<string, unknown>;
    predictionRecord[field] = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.prediction).toEqual({ kind: "MALFORMED" });
  });

  it("rejects a prediction input trace naming another X_PE profile", () => {
    const value = response();
    const predictionRecord = (value.full_model as Record<string, unknown>).prediction as Record<string, unknown>;
    const provenance = predictionRecord.provenance as Record<string, unknown>;
    const trace = (provenance.input_traces as Array<Record<string, unknown>>)[0];
    (trace.feature_ref as Record<string, unknown>).profile_id = { wrong: "profile" };
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.prediction).toEqual({ kind: "MALFORMED" });
  });

  it("treats missing withheld_reason_or_none as malformed and explicit null as valid", () => {
    const missing = response();
    const missingPrediction = (missing.full_model as Record<string, unknown>).prediction as Record<string, unknown>;
    delete (missingPrediction.provenance as Record<string, unknown>).withheld_reason_or_none;
    const missingProjection = selectProductQualityPage(missing);
    expect(missingProjection.kind === "AVAILABLE" && missingProjection.prediction).toEqual({ kind: "MALFORMED" });

    const validProjection = selectProductQualityPage(response());
    expect(validProjection.kind === "AVAILABLE" && validProjection.prediction.kind).toBe("PRESENT");
  });

  it.each([
    ["criterion", "criterion_binding", (record: Record<string, unknown>) => { record.criterion = null; }],
    ["observation", "observation_resolution", (record: Record<string, unknown>) => { record.observation = null; }],
    ["conformance", "conformance", (record: Record<string, unknown>) => { record.outcome = "INVALID_OUTCOME"; }],
  ])("fails X_PE closed when the %s projection is malformed", (_label, field, mutate) => {
    const value = response();
    const model = value.full_model as Record<string, unknown>;
    mutate(model[field] as Record<string, unknown>);
    const projected = selectProductQualityPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.featureProfile).toBeNull();
    expect(projected.observed).toBeNull();
    expect(projected.prediction).toEqual({ kind: "MALFORMED" });
  });

  it("does not allow malformed X_PE to leave observed or a non-null prediction valid", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    (profile.provenance as Record<string, unknown>).criterion_binding_ref = { wrong: "binding" };
    const projected = selectProductQualityPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.featureProfile).toBeNull();
    expect(projected.observed).toBeNull();
    expect(projected.prediction).toEqual({ kind: "MALFORMED" });
  });

  it.each([
    ["criterion binding", "criterion_binding_ref", { wrong: "binding" }],
    ["observation resolution", "observation_resolution_ref", { wrong: "slot" }],
    ["conformance", "conformance_assessment_ref", { wrong: "conformance" }],
  ])("rejects X_PE provenance %s mismatch", (_label, field, replacement) => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    (profile.provenance as Record<string, unknown>)[field] = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it.each([
    ["artifact", "artifact_ref", artifactV2],
    ["product", "product_ref", { product_id: "OTHER", product_version: "1" }],
    ["process", "process_state_ref", { process_state_id: "OTHER", process_state_version: "1", stage: "REFERENCE_VERIFICATION" }],
  ])("rejects X_PE provenance %s identity mismatch", (_label, field, replacement) => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    (profile.provenance as Record<string, unknown>)[field] = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects X_PE provenance feature-entry refs in the wrong registry order", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    const provenance = profile.provenance as Record<string, unknown>;
    provenance.ordered_feature_entry_refs = [...(provenance.ordered_feature_entry_refs as unknown[])].reverse();
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects a static X_PE feature carrying a product subject", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    profile.features[0].product_ref = profile.product_ref;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it.each([[5, "observation"], [6, "conformance"]])("rejects dynamic %s feature with the wrong product subject", (index) => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    profile.features[index].product_ref = { product_id: "OTHER", product_version: "1" };
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects another typed-value family in the criterion registry slot", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    profile.features[0].typed_value = profile.features[1].typed_value;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it.each([1, 2, 3])("rejects requirement metric slot %s without an exact fraction", (index) => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    (profile.features[index].typed_value as Record<string, unknown>).exact_fraction_or_none = null;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects a requirement metric feature without EXACT_FRACTION representation", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    (profile.features[1].typed_value as Record<string, unknown>).numeric_representation = "DECIMAL";
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects a malformed typed-value family in the QB slot", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    profile.features[4].typed_value = profile.features[1].typed_value;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects a QB typed-value target-key mismatch", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    (profile.features[4].typed_value as Record<string, unknown>).target_key = { key: "other-target" };
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects an observation feature that names another observation", () => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    (profile.features[5].typed_value as Record<string, unknown>).observation_ref = { observation_id: { wrong: "observation" } };
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("preserves the observation feature exact decimal as an untouched string", () => {
    const projected = selectProductQualityPage(response());
    expect(projected.kind === "AVAILABLE" && projected.featureProfile?.features[5].typedValue?.exact_decimal_value).toBe("1.80");
  });

  it.each([
    ["reference", "conformance_ref", { wrong: "conformance" }],
    ["outcome", "outcome", "DOES_NOT_CONFORM"],
  ])("rejects conformance feature %s mismatch without recomputing conformance", (_label, field, replacement) => {
    const value = response();
    const profile = (value.full_model as Record<string, unknown>).feature_profile as ReturnType<typeof featureProfile>;
    (profile.features[6].typed_value as Record<string, unknown>)[field] = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.conformance?.outcome).toBe("CONFORMS");
    expect(projected.kind === "AVAILABLE" && projected.featureProfile).toBeNull();
  });

  it("rejects an observed assessment ID/event mismatch", () => {
    const value = response();
    const observedRecord = (value.full_model as Record<string, unknown>).observed_product_quality as Record<string, unknown>;
    (observedRecord.assessment_id as Record<string, unknown>).assessment_event_ref = { wrong: "event" };
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.observed).toBeNull();
  });

  it.each([
    ["artifact", "artifact_ref", artifactV2],
    ["product", "product_ref", { product_id: "OTHER", product_version: "1" }],
  ])("rejects an observed event %s mismatch", (_label, field, replacement) => {
    const value = response();
    const observedRecord = (value.full_model as Record<string, unknown>).observed_product_quality as Record<string, unknown>;
    const event = { ...(observedRecord.assessment_event_ref as Record<string, unknown>), [field]: replacement };
    observedRecord.assessment_event_ref = event;
    (observedRecord.assessment_id as Record<string, unknown>).assessment_event_ref = event;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.observed).toBeNull();
  });

  it.each([
    ["artifact", "artifact_version", "99"],
    ["product", "product_version", "99"],
    ["assessment", "product_quality_assessment_version", "99"],
    ["source assessment", "source_assessment_version", "99"],
  ])("rejects observed %s version mismatch", (_label, field, replacement) => {
    const value = response();
    const observedRecord = (value.full_model as Record<string, unknown>).observed_product_quality as Record<string, unknown>;
    observedRecord[field] = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.observed).toBeNull();
  });

  it.each([
    ["metric", "dynamic_metric_ref", { metric_id: "OTHER" }],
    ["context", "context_identity", { normalized_text: "other context" }],
    ["unit", "unit", "MILLISECOND"],
    ["collection", "collection_ref", { wrong: "collection" }],
    ["environment", "environment_ref", { wrong: "environment" }],
  ])("rejects observed scope %s mismatch", (_label, field, replacement) => {
    const value = response();
    const observedRecord = (value.full_model as Record<string, unknown>).observed_product_quality as Record<string, unknown>;
    (observedRecord.scope as Record<string, unknown>)[field] = replacement;
    const projected = selectProductQualityPage(value);
    expect(projected.kind === "AVAILABLE" && projected.observed).toBeNull();
  });

  it("disables criterion navigation when RUI-08 marks the matching requirement malformed", () => {
    const value = response();
    value.requirements = [{ requirement: { id: "R001", source_line: 1, text: "Malformed outer record" } }];
    render(<ProductQualityPage result={value} onSelectRequirement={vi.fn()} />);
    expect(screen.queryByRole("button", { name: "Open R001" })).toBeNull();
  });

  it("navigates to RUI-08 only when the canonical criterion requirement resolves", () => {
    const onSelect = vi.fn();
    render(<ProductQualityPage result={response()} onSelectRequirement={onSelect} />);
    fireEvent.click(screen.getByRole("button", { name: "Open R001" }));
    expect(onSelect).toHaveBeenCalledWith("R001");
  });
});

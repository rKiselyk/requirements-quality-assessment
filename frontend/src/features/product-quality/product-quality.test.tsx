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
  return {
    criterion_binding: {
      binding_id: { artifact_ref: artifact, binding_rule_ref: rule }, status: "AVAILABLE", applicability: "APPLICABLE",
      criterion: { criterion_id: { id: `CRITERION-${marker}` }, requirement_subject_ref: { requirement_id: "R001", artifact_ref: artifact }, artifact_ref: artifact, source_assessment_ref: {}, source_snapshot_id: {}, source_observation_ref: { requirement_id: "R001", observation_index: 0 }, metric_ref: { metric_id: "DYN.RESPONSE_TIME" }, comparator: "LESS_THAN_OR_EQUAL", inclusivity: "INCLUSIVE", bound: marker === "STALE" ? "99" : "2.0", unit: "SECOND", context_identity: { normalized_text: "500 concurrent users" }, provenance: {}, binding_rule_ref: rule },
      source_observation_ref: { requirement_id: "R001", observation_index: 0 }, reasons: [], provenance: { evidence_refs: [{ requirement_id: "R001", evidence_id: "E003" }] },
    },
    observation_resolution: {
      slot_ref: { collection_ref: { collection_id: "COLLECTION" }, fixture_sequence: 0 }, status: "AVAILABLE", applicability: "APPLICABLE",
      observation: { observation_id: { collection_ref: { collection_id: "COLLECTION" }, fixture_sequence: 0 }, slot_ref: {}, product_ref: profile.product_ref, metric_ref: { metric_id: "DYN.RESPONSE_TIME" }, observed_value: marker === "STALE" ? "88" : "1.80", unit: "SECOND", context_identity: { normalized_text: "500 concurrent users" }, source_kind: "DETERMINISTIC_FIXTURE", collection_ref: { collection_id: "COLLECTION", collection_version: "1", product_ref: profile.product_ref, environment_ref: { environment_id: "ENV", environment_version: "1" }, source_kind: "DETERMINISTIC_FIXTURE" }, fixture_sequence: 0, collected_at: null, provenance: { source_record_ref: `FIXTURE-${marker}` } },
      reasons: [], provenance_refs: [`FIXTURE-${marker}`],
    },
    conformance: { conformance_id: { artifact_ref: artifact }, dynamic_assessment_ref: { artifact_ref: artifact }, criterion_binding_id: {}, criterion_id: { id: `CRITERION-${marker}` }, observation_slot_ref: {}, observation_id: { id: `OBS-${marker}` }, status: "AVAILABLE", applicability: "APPLICABLE", outcome: "CONFORMS", explanation: "Canonical backend conformance result.", reasons: [], criterion_ref: {}, observation_ref: {}, evidence_refs: [{ evidence_id: "E003" }], provenance: {}, evaluator_rule_ref: rule },
    feature_profile: profile,
    observed_product_quality: observed(artifact, profile, marker),
    product_quality_assessment: observed(artifact, profile, marker),
    prediction: prediction(profile, predictorRef, parameterSetRef, selectedInputRefs, contextInputs, marker),
  };
}

function observed(artifact: typeof artifactV1, profile: ReturnType<typeof featureProfile>, marker: string) {
  return {
    assessment_id: { id: `PQ-${marker}` }, assessment_event_ref: { assessment_event_id: `EVENT-${marker}`, assessment_event_version: "1" }, characteristic_id: "PERFORMANCE_EFFICIENCY", product_ref: profile.product_ref, artifact_ref: artifact, feature_profile_ref: profile.profile_id,
    scope: { scope_kind: "SINGLE_CRITERION_SINGLE_OBSERVATION" }, scope_statement: "One response-time criterion and one observation.", result_kind: "OBSERVED_REFERENCE_INDICATOR", status: "AVAILABLE", applicability: "APPLICABLE", source_conformance_outcome: "CONFORMS", value: { numerator: 1, denominator: 1 }, prediction_value: null, observed_value: { numerator: 1, denominator: 1 }, numeric_representation: "EXACT_FRACTION", evidence_coverage: { coverage_kind: "BOUNDED_REQUIRED_CHANNEL_INVENTORY" }, reliability: null, uncertainty: null, explanation: "Bounded observed indicator.", feature_refs: [], evidence_refs: [], provenance: {}, model_ref: { model_id: "FULL-MODEL-V0.1-M-QUALITY-PE", model_version: "1" }, procedure_rule_ref: rule, parameter_set_ref: { parameter_set_id: "PE-OBS-CONFORMANCE-001-PARAMETERS", parameter_set_version: "1" }, calibration_status: "PROVISIONAL_NOT_CALIBRATED", artifact_version: artifact.artifact_version, source_assessment_version: artifact.artifact_version, product_version: "1", product_quality_assessment_version: "1", non_claims: [...productQualityNonClaims],
  };
}

function prediction(profile: ReturnType<typeof featureProfile>, predictorRef: Record<string, unknown>, parameterSetRef: Record<string, unknown>, selectedInputRefs: unknown[], contextInputs: unknown[], marker: string) {
  return {
    event_ref: { prediction_event_id: `PREDICTION-${marker}`, prediction_event_version: "1" }, result_kind: "PREDICTED_PERFORMANCE_EFFICIENCY", characteristic_id: "PERFORMANCE_EFFICIENCY", status: "AVAILABLE", applicability: "APPLICABLE", predicted_value: { numerator: 5, denominator: 6 }, numeric_representation: "EXACT_FRACTION", predictor_ref: predictorRef, parameter_set_ref: parameterSetRef, calibration_status: "PROVISIONAL_NOT_CALIBRATED", selected_input_refs: selectedInputRefs, context_inputs: contextInputs, artifact_ref: profile.artifact_ref, product_ref: profile.product_ref, process_state_ref: profile.process_state_ref, governing_contract_ref: {}, rule_refs: [rule], explanation: "Fixture-only bounded prediction.",
    provenance: { feature_profile_ref: profile.profile_id, input_traces: selectedInputRefs.map((feature_ref) => ({ feature_ref })), context_inputs: contextInputs, predictor_definition: { predictor_ref: predictorRef, calibration_status: "PROVISIONAL_NOT_CALIBRATED", source_or_rationale: "Fixture-only rationale." }, parameter_set_ref: parameterSetRef, parameter_entries: [{ name: "alpha", exact_value: { numerator: 1, denominator: 2 } }], parameter_source_or_rationale: "Controlled fixture parameter source.", contract_refs: [], rule_refs: [rule], withheld_reason_or_none: null },
  };
}

function response(caseName: CanonicalAnalyzeResponse["analysis_case"] = "CONTROLLED_DEMO"): CanonicalAnalyzeResponse {
  return {
    contract_version: "research-api-v1", analysis_case: caseName, controlled_scenario: caseName === "INITIAL" ? null : { id: "SCENARIO", version: "1" },
    requirements: [{ requirement: { id: "R001", source_line: 1, text: "Canonical requirement text." } }], specification: { snapshot_id: "SNAPSHOT" },
    section_availability: [{ section: "product_quality", availability: caseName === "INITIAL" ? "UNAVAILABLE" : "AVAILABLE", reason_code: caseName === "INITIAL" ? "EXTERNAL_EVIDENCE_NOT_SUPPLIED" : null }],
    full_model: caseName === "INITIAL" ? null : currentRecords(), reassessment_context: null, limitations: [],
  };
}

function reassessmentResponse(mismatch = false): CanonicalAnalyzeResponse {
  const stale = currentRecords(artifactV1, "STALE");
  const current = { artifact_ref: artifactV2, ...currentRecords(artifactV2, "CURRENT") };
  return {
    ...response("REASSESSMENT"),
    full_model: {
      ...stale,
      reassessment: {
        context: { child_artifact_ref: artifactV2 },
        provenance: { child_artifact_ref: artifactV2 },
        produced_result_refs: [
          { result_family: "CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH", result_id: "CORE", artifact_ref: artifactV2 },
          { result_family: "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH", result_id: "RISK", artifact_ref: mismatch ? artifactV1 : artifactV2 },
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
    expect(projected.prediction?.predictedValue).toEqual({ numerator: "5", denominator: "6" });
    expect(projected.prediction?.calibrationStatus).toBe("PROVISIONAL_NOT_CALIBRATED");
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
    expect(projected.kind === "AVAILABLE" && projected.prediction).toBeNull();
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
    expect(projected.kind === "AVAILABLE" && projected.prediction).toBeNull();
  });

  it("selects the paired reassessment v2 dynamic result and never reuses top-level v1 records or prediction", () => {
    const projected = selectProductQualityPage(reassessmentResponse());
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.revision).toBe("REASSESSMENT_V2");
    expect(projected.criterion?.bound).toBe("2.0");
    expect(projected.criterion?.raw).not.toEqual((reassessmentResponse().full_model as Record<string, unknown>).criterion_binding);
    expect(projected.observed?.raw.artifact_ref).toEqual(artifactV2);
    expect(projected.predictionCurrent).toBe(false);
    expect(projected.prediction).toBeNull();
    render(<ProductQualityPage result={reassessmentResponse()} onSelectRequirement={vi.fn()} />);
    expect(screen.getByText(/No prediction record was produced for the current reassessed revision/)).toBeTruthy();
    expect(screen.queryByText("PREDICTOR-STALE")).toBeNull();
  });

  it("fails safely when the paired produced-result artifact does not match the reassessment child", () => {
    expect(selectProductQualityPage(reassessmentResponse(true))).toEqual({ kind: "MALFORMED" });
    render(<ProductQualityPage result={reassessmentResponse(true)} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Product Quality cannot be safely presented" })).toBeTruthy();
  });

  it("navigates to RUI-08 only when the canonical criterion requirement resolves", () => {
    const onSelect = vi.fn();
    render(<ProductQualityPage result={response()} onSelectRequirement={onSelect} />);
    fireEvent.click(screen.getByRole("button", { name: "Open R001" }));
    expect(onSelect).toHaveBeenCalledWith("R001");
  });
});

import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../../App";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { i18n } from "../../i18n";
import { ModelPipeline } from "./ModelPipeline";
import { OverviewPage } from "./OverviewPage";
import { exactValue, selectQbConsistency, selectSpecificationMetrics } from "./projection";

const aggregate = (characteristic: string, numerator: number | null, denominator: number | null, state = "COMPUTED") => ({
  characteristic_id: characteristic,
  state,
  value: numerator === null || denominator === null ? null : { numerator, denominator },
  computed_count: state === "COMPUTED" ? 2 : 0,
  unknown_count: state === "UNKNOWN" ? 2 : 0,
  not_applicable_count: state === "NOT_APPLICABLE" ? 2 : 0,
  total_count: 2,
  aggregation_rule_id: "AGG-MVP-001",
});

const sections = [
  ["overview", "AVAILABLE", null],
  ["requirements", "AVAILABLE", null],
  ["specification", "AVAILABLE", null],
  ["audit", "AVAILABLE", null],
  ["product_quality", "UNAVAILABLE", "EXTERNAL_EVIDENCE_NOT_SUPPLIED"],
  ["risk", "UNAVAILABLE", "CONFIRMED_PROBLEM_AND_RISK_INPUTS_NOT_AVAILABLE"],
  ["corrective_actions", "UNAVAILABLE", "CONFIRMED_PROBLEM_NOT_AVAILABLE"],
  ["process", "UNAVAILABLE", "FULL_MODEL_LIFECYCLE_NOT_INVOKED"],
  ["reassessment", "UNAVAILABLE", "INITIAL_ASSESSMENT_HAS_NO_REASSESSMENT"],
  ["comparison", "UNAVAILABLE", "INITIAL_ASSESSMENT_HAS_NO_COMPARISON"],
].map(([section, availability, reason_code]) => ({ section, availability, reason_code }));

function initialResult(overrides: Partial<CanonicalAnalyzeResponse> = {}): CanonicalAnalyzeResponse {
  return {
    contract_version: "research-api-v1",
    analysis_case: "INITIAL",
    controlled_scenario: null,
    requirements: [
      { requirement: { id: "R001" }, quality_profile: { completeness: { value: { numerator: 0, denominator: 1 } } } },
      { requirement: { id: "R002" }, quality_profile: { completeness: { value: { numerator: 0, denominator: 1 } } } },
    ],
    specification: {
      snapshot_id: "qb-snapshot-sha256:accepted",
      quality_profile: {
        completeness: aggregate("COMPLETENESS", 2, 3),
        verifiability: aggregate("VERIFIABILITY", 5, 7),
        unambiguity: aggregate("UNAMBIGUITY", null, null, "UNKNOWN"),
      },
      qb_consistency: {
        state: "NOT_APPLICABLE",
        value: null,
        observability: { total_requirement_count: 2 },
        reasons: ["NO_APPLICABLE_COMPARISONS"],
      },
    },
    section_availability: sections,
    full_model: null,
    reassessment_context: null,
    limitations: ["NO_COMBINED_QUALITY_SCORE"],
    ...overrides,
  };
}

function controlledResult(): CanonicalAnalyzeResponse {
  return initialResult({
    analysis_case: "CONTROLLED_DEMO",
    controlled_scenario: { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" },
    section_availability: sections.map((item) => ["product_quality", "risk", "corrective_actions", "process"].includes(String(item.section))
      ? { section: item.section, availability: "AVAILABLE", reason_code: null }
      : item),
    full_model: {
      observed_product_quality: { status: "UNRESOLVED", applicability: "APPLICABLE", result_kind: "OBSERVED_REFERENCE_INDICATOR", observed_value: null },
      prediction: { status: "AVAILABLE", applicability: "APPLICABLE", result_kind: "PREDICTED_PERFORMANCE_EFFICIENCY", predicted_value: { numerator: 5, denominator: 6 } },
      risk_assessments: [{ status: "AVAILABLE", applicability: "APPLICABLE", classification: "RISK_IDENTIFIED" }],
      quantitative_risk_assessments: [{ state: "AVAILABLE", result_kind: "LOCAL_RISK_R_IJ", local_risk: { numerator: 1, denominator: 16 } }],
      corrective_action_resolution: { status: "AVAILABLE", applicability: "APPLICABLE", reason_codes: ["ELIGIBLE_RISK_IDENTIFIED"] },
      process_v1: { process_state_id: "PROCESS-REFERENCE", process_state_version: "v1", stage: "REFERENCE_VERIFICATION" },
      process_v2: { process_state_id: "PROCESS-REFERENCE", process_state_version: "v2", stage: "REFERENCE_VERIFICATION" },
      checkpoint_evaluations: [
        { checkpoint_id: "CHECKPOINT-V1", checkpoint_version: "1", outcome: "NOT_SATISFIED", reason_codes: ["PREDICATE_FALSE"] },
        { checkpoint_id: "CHECKPOINT-V2", checkpoint_version: "1", outcome: "SATISFIED", reason_codes: ["PREDICATE_TRUE"] },
      ],
    },
    limitations: ["NO_COMBINED_QUALITY_SCORE", "CONTROLLED_RESEARCH_FIXTURE_DATA", "NO_CAUSAL_OR_RELEASE_CLAIM"],
  });
}

function withCompleteness(value: Record<string, unknown>): CanonicalAnalyzeResponse {
  const result = initialResult();
  const qualityProfile = result.specification.quality_profile as Record<string, unknown>;
  return { ...result, specification: { ...result.specification, quality_profile: { ...qualityProfile, completeness: value } } };
}

function withQb(value: unknown): CanonicalAnalyzeResponse {
  const result = initialResult();
  return { ...result, specification: { ...result.specification, qb_consistency: value } };
}

function response(payload: unknown): Response {
  return { ok: true, json: async () => payload } as Response;
}

function renderApp(payload: CanonicalAnalyzeResponse) {
  vi.spyOn(globalThis, "fetch").mockResolvedValue(response(payload));
  const client = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
  return render(<QueryClientProvider client={client}><App /></QueryClientProvider>);
}

async function analyze() {
  fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
  fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
  await screen.findByRole("heading", { name: "Overview" });
}

describe("RUI-07 results workspace", () => {
  beforeEach(async () => {
    window.sessionStorage.clear();
    await i18n.changeLanguage("en");
  });

  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("defaults a successful result to Overview with exactly eight standard sections", async () => {
    renderApp(initialResult());
    await analyze();

    const navigation = screen.getByRole("navigation", { name: "Research result sections" });
    expect(within(navigation).getAllByRole("button").map((button) => button.textContent)).toEqual([
      "Overview", "Requirements", "Specification", "Product Quality", "Risk", "Corrective Actions", "Process", "Audit",
    ]);
    expect(within(navigation).queryByText("Reassessment")).toBeNull();
    expect(within(navigation).queryByText("Comparison")).toBeNull();
    expect(within(navigation).getByRole("button", { name: "Overview" }).getAttribute("aria-current")).toBe("page");
  });

  it("changes result views and locale without rerunning analysis", async () => {
    renderApp(initialResult());
    await analyze();
    const fetchSpy = vi.mocked(globalThis.fetch);

    fireEvent.click(screen.getByRole("button", { name: "Risk" }));
    expect(await screen.findByRole("heading", { name: "Risk" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));
    expect(await screen.findByRole("heading", { name: "Ризик" })).toBeTruthy();
    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  it("resets result and selected view for a new specification while retaining locale", async () => {
    renderApp(initialResult());
    await analyze();
    fireEvent.click(screen.getByRole("button", { name: "Risk" }));
    await screen.findByRole("heading", { name: "Risk" });
    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));
    fireEvent.click(await screen.findByRole("button", { name: "Нова специфікація" }));

    expect(screen.getByRole("heading", { name: "Аналіз специфікації" })).toBeTruthy();
    expect(screen.queryByRole("navigation", { name: "Розділи результатів дослідження" })).toBeNull();
    expect(document.documentElement.lang).toBe("uk");
  });

  it("uses canonical requirement length and specification aggregates without recalculation", () => {
    render(<OverviewPage result={initialResult()} />);
    expect(screen.getByText("2")).toBeTruthy();
    expect(screen.getByLabelText("Exact value: 2/3")).toBeTruthy();
    expect(screen.getByLabelText("Exact value: 5/7")).toBeTruthy();
    expect(screen.queryByLabelText("Exact value: 0/1")).toBeNull();
  });

  it("keeps exact fractions lossless and does not fabricate values for UNKNOWN or NOT_APPLICABLE", () => {
    const result = initialResult();
    const metrics = selectSpecificationMetrics(result);
    const qb = selectQbConsistency(result);
    expect(exactValue({ numerator: 2, denominator: 3 })).toEqual({ numerator: "2", denominator: "3" });
    expect(metrics.completeness?.value).toEqual({ numerator: "2", denominator: "3" });
    expect(metrics.unambiguity?.state).toBe("UNKNOWN");
    expect(metrics.unambiguity?.value).toBeNull();
    expect(qb?.state).toBe("NOT_APPLICABLE");
    expect(qb?.value).toBeNull();
  });

  it("does not fabricate UNAVAILABLE for missing or malformed pipeline availability", () => {
    const missing = initialResult({ section_availability: sections.filter((item) => item.section !== "process") });
    const malformed = initialResult({ section_availability: sections.map((item) => item.section === "risk" ? { ...item, availability: "BROKEN" } : item) });
    const first = render(<ModelPipeline result={missing} />);
    const processStage = screen.getByText("Process").closest("li")!;
    expect(within(processStage).getByText("Availability cannot be safely presented")).toBeTruthy();
    expect(within(processStage).queryByText("UNAVAILABLE")).toBeNull();
    first.unmount();

    render(<ModelPipeline result={malformed} />);
    const riskStage = screen.getByText("Risk").closest("li")!;
    expect(within(riskStage).getByText("Availability cannot be safely presented")).toBeTruthy();
    expect(within(riskStage).queryByText("UNAVAILABLE")).toBeNull();
  });

  it("continues to display valid canonical pipeline UNAVAILABLE", () => {
    render(<ModelPipeline result={initialResult()} />);
    const productQualityStage = screen.getByText("Product Quality").closest("li")!;
    expect(within(productQualityStage).getByText("Unavailable")).toBeTruthy();
    expect(within(productQualityStage).getByText("UNAVAILABLE")).toBeTruthy();
  });

  it.each([
    ["COMPUTED with null", { ...aggregate("COMPLETENESS", 2, 3), state: "COMPUTED", value: null }],
    ["COMPUTED with malformed rational", { ...aggregate("COMPLETENESS", 2, 3), state: "COMPUTED", value: { numerator: "2", denominator: 3 } }],
    ["UNKNOWN with numeric value", { ...aggregate("COMPLETENESS", 2, 3), state: "UNKNOWN", value: { numerator: 2, denominator: 3 } }],
    ["NOT_APPLICABLE with numeric value", { ...aggregate("COMPLETENESS", 2, 3), state: "NOT_APPLICABLE", value: { numerator: 2, denominator: 3 } }],
  ])("rejects contradictory C/V/U presentation: %s", (_label, completeness) => {
    const result = withCompleteness(completeness);
    expect(selectSpecificationMetrics(result).completeness).toBeNull();
    render(<OverviewPage result={result} />);
    const card = screen.getByRole("heading", { name: "Completeness" }).closest("article")!;
    expect(within(card).getByText("Canonical record cannot be safely presented")).toBeTruthy();
    expect(within(card).queryByText(/COMPUTED|UNKNOWN|NOT_APPLICABLE/)).toBeNull();
  });

  it("keeps a valid COMPUTED C/V/U fraction exact", () => {
    const result = withCompleteness(aggregate("COMPLETENESS", 13, 17));
    expect(selectSpecificationMetrics(result).completeness?.value).toEqual({ numerator: "13", denominator: "17" });
    render(<OverviewPage result={result} />);
    expect(screen.getByLabelText("Exact value: 13/17")).toBeTruthy();
  });

  it.each([
    ["negative", { ...aggregate("COMPLETENESS", 2, 3), unknown_count: -1 }],
    ["malformed", { ...aggregate("COMPLETENESS", 2, 3), total_count: "2" }],
    ["missing", (() => { const value = { ...aggregate("COMPLETENESS", 2, 3) } as Record<string, unknown>; delete value.computed_count; return value; })()],
  ])("rejects %s aggregate counts rather than substituting zero", (_label, completeness) => {
    const result = withCompleteness(completeness);
    expect(selectSpecificationMetrics(result).completeness).toBeNull();
    render(<OverviewPage result={result} />);
    const card = screen.getByRole("heading", { name: "Completeness" }).closest("article")!;
    expect(within(card).getByText("Canonical record cannot be safely presented")).toBeTruthy();
    expect(within(card).queryByText(/Computed 0/)).toBeNull();
  });

  it.each([
    ["COMPUTED without value", { state: "COMPUTED", value: null }],
    ["COMPUTED with malformed value", { state: "COMPUTED", value: { numerator: 1, denominator: 0 } }],
    ["UNKNOWN with value", { state: "UNKNOWN", value: { numerator: 1, denominator: 2 } }],
    ["NOT_APPLICABLE with value", { state: "NOT_APPLICABLE", value: { numerator: 1, denominator: 2 } }],
  ])("rejects contradictory QB presentation: %s", (_label, qb) => {
    const result = withQb(qb);
    expect(selectQbConsistency(result)).toBeNull();
    render(<OverviewPage result={result} />);
    const qbCard = screen.getByRole("heading", { name: "QB consistency" }).closest("section")!;
    expect(within(qbCard).getByText("Canonical record cannot be safely presented")).toBeTruthy();
    expect(within(qbCard).queryByText(/COMPUTED|UNKNOWN|NOT_APPLICABLE/)).toBeNull();
  });

  it("presents QB separately from C/V/U", () => {
    render(<OverviewPage result={initialResult()} />);
    const quality = screen.getByRole("heading", { name: "Requirement quality" }).parentElement!;
    expect(within(quality).queryByText("QB consistency")).toBeNull();
    expect(screen.getByRole("heading", { name: "QB consistency" })).toBeTruthy();
  });

  it.each([
    ["Product Quality", "EXTERNAL_EVIDENCE_NOT_SUPPLIED"],
    ["Risk", "CONFIRMED_PROBLEM_AND_RISK_INPUTS_NOT_AVAILABLE"],
    ["Corrective Actions", "CONFIRMED_PROBLEM_NOT_AVAILABLE"],
    ["Process / Checkpoint", "FULL_MODEL_LIFECYCLE_NOT_INVOKED"],
  ])("shows INITIAL %s as unavailable from its canonical reason", (title, code) => {
    render(<OverviewPage result={initialResult()} />);
    const card = screen.getByRole("heading", { name: title }).closest("section")!;
    expect(within(card).getByText("Not available for this analysis")).toBeTruthy();
    expect(within(card).getByText(code)).toBeTruthy();
    expect(within(card).queryByText("0")).toBeNull();
  });

  it("distinguishes controlled-demo observed and predicted Product Quality", () => {
    render(<OverviewPage result={controlledResult()} />);
    expect(screen.getByRole("heading", { name: "Observed product-quality record" })).toBeTruthy();
    expect(screen.getByText("OBSERVED_REFERENCE_INDICATOR")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Prediction record" })).toBeTruthy();
    expect(screen.getByText("PREDICTED_PERFORMANCE_EFFICIENCY")).toBeTruthy();
    expect(screen.getByLabelText("Exact value: 5/6")).toBeTruthy();
  });

  it("presents applicability with localized applicability semantics and its canonical code", async () => {
    render(<OverviewPage result={controlledResult()} />);
    const productQuality = screen.getByRole("heading", { name: "Product Quality" }).closest("section")!;
    expect(within(productQuality).getAllByText("Applicable").length).toBeGreaterThan(0);
    expect(within(productQuality).getAllByText("APPLICABLE").length).toBeGreaterThan(0);

    await i18n.changeLanguage("uk");
    expect(within(productQuality).getAllByText("Застосовне").length).toBeGreaterThan(0);
    expect(within(productQuality).getAllByText("APPLICABLE").length).toBeGreaterThan(0);
  });

  it("uses malformed-presentation wording for an AVAILABLE section with a malformed nested record", () => {
    const result = controlledResult();
    const fullModel = { ...result.full_model, observed_product_quality: null };
    render(<OverviewPage result={{ ...result, full_model: fullModel }} />);
    const productQuality = screen.getByRole("heading", { name: "Product Quality" }).closest("section")!;
    expect(within(productQuality).getByText("Canonical record cannot be safely presented")).toBeTruthy();
    expect(within(productQuality).queryByText("Not available for this analysis")).toBeNull();
  });

  it("distinguishes controlled-demo categorical and quantitative Risk", () => {
    render(<OverviewPage result={controlledResult()} />);
    expect(screen.getByRole("heading", { name: "Categorical risk assessments" })).toBeTruthy();
    expect(screen.getByText("RISK_IDENTIFIED")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Quantitative risk assessments" })).toBeTruthy();
    expect(screen.getByText("LOCAL_RISK_R_IJ")).toBeTruthy();
    expect(screen.getByLabelText("Exact value: 1/16")).toBeTruthy();
  });

  it("projects action status without an effectiveness claim and checkpoints without release approval", () => {
    render(<OverviewPage result={controlledResult()} />);
    const action = screen.getByRole("heading", { name: "Corrective Actions" }).closest("section")!;
    expect(within(action).getByText("ELIGIBLE_RISK_IDENTIFIED")).toBeTruthy();
    expect(within(action).queryByText(/effective|optimal|successful/i)).toBeNull();
    const process = screen.getByRole("heading", { name: "Process / Checkpoint" }).closest("section")!;
    expect(within(process).getByText("SATISFIED")).toBeTruthy();
    expect(within(process).getByText("NOT_SATISFIED")).toBeTruthy();
    expect(within(process).getByText(/do not authorize release or approval/i)).toBeTruthy();
  });

  it("presents accepted limitations and no overall score, gauge, or percentage", () => {
    render(<OverviewPage result={controlledResult()} />);
    expect(screen.getByText("NO_COMBINED_QUALITY_SCORE")).toBeTruthy();
    expect(screen.getByText("CONTROLLED_RESEARCH_FIXTURE_DATA")).toBeTruthy();
    expect(screen.queryByText(/overall quality score/i)).toBeNull();
    expect(document.querySelector("meter, progress, svg")).toBeNull();
    expect(document.body.textContent).not.toMatch(/\d+(?:\.\d+)?%/);
  });

  it("degrades unknown availability reasons visibly without inventing meaning", () => {
    const result = initialResult({ section_availability: sections.map((item) => item.section === "risk" ? { ...item, reason_code: "FUTURE_CANONICAL_REASON" } : item) });
    render(<OverviewPage result={result} />);
    expect(screen.getAllByText("FUTURE_CANONICAL_REASON").length).toBeGreaterThan(0);
    expect(screen.getByText(/No localized explanation is registered/)).toBeTruthy();
  });

  it("renders malformed nested records safely and does not mutate the canonical response", () => {
    const result = initialResult({ specification: { snapshot_id: "accepted", quality_profile: { completeness: { state: "COMPUTED", value: { numerator: "bad", denominator: 3 } } }, qb_consistency: [] } });
    const before = JSON.stringify(result);
    render(<OverviewPage result={result} />);
    expect(JSON.stringify(result)).toBe(before);
    expect(screen.getAllByText(/No value was inferred|cannot be safely presented/).length).toBeGreaterThan(0);
    expect(screen.queryByText("0")).toBeNull();
  });

  it("preserves the canonical response object while navigating", async () => {
    const result = initialResult();
    const before = JSON.stringify(result);
    renderApp(result);
    await analyze();
    fireEvent.click(screen.getByRole("button", { name: "Specification" }));
    await waitFor(() => expect(screen.getByRole("heading", { name: "Specification" })).toBeTruthy());
    expect(JSON.stringify(result)).toBe(before);
  });
});

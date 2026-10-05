import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../../App";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { i18n } from "../../i18n";
import { SpecificationPage } from "./SpecificationPage";
import { selectSpecificationPage } from "./projection";

const characteristic = (id: string, numerator: number | null, denominator: number | null, state = "COMPUTED") => ({
  characteristic_id: id,
  state,
  value: numerator === null || denominator === null ? null : { numerator, denominator },
  assessment_rule_id: `RULE-${id}`,
  findings: [],
  explanation: `Canonical ${id} explanation`,
});

const aggregate = (id: string, numerator: number | null, denominator: number | null, state = "COMPUTED", counts = [2, 0, 0, 2]) => ({
  characteristic_id: id,
  state,
  value: numerator === null || denominator === null ? null : { numerator, denominator },
  computed_count: counts[0], unknown_count: counts[1], not_applicable_count: counts[2], total_count: counts[3],
  aggregation_rule_id: "AGG-MVP-001",
});

const emptyFeature = (featureId: string) => ({ feature_id: featureId, status: "NOT_DETECTED", processing_status: "COMPLETE", observations: [], diagnostics: [] });

function requirement(id: string, sourceLine: number, values: [number, number, number]) {
  const profile = {
    completeness: characteristic("COMPLETENESS", values[0], 10),
    verifiability: characteristic("VERIFIABILITY", values[1], 10),
    unambiguity: characteristic("UNAMBIGUITY", values[2], 10),
  };
  return {
    requirement: { id, source_line: sourceLine, text: `${id} canonical requirement text.` },
    features: {
      condition_contexts: emptyFeature("condition_context"), expected_results: emptyFeature("expected_result"),
      acceptance_criteria: emptyFeature("acceptance_criterion"), quantitative_constraints: emptyFeature("quantitative_constraint"),
      verification_methods: emptyFeature("verification_method"), vague_term_occurrences: emptyFeature("vague_term_occurrence"),
    },
    evidence: [],
    quality_profile: profile,
    trace: {
      requirement_id: id,
      coverage_profile_id: "MVP-V0.1-BOUNDED-CVU-001",
      characteristics: Object.values(profile).map((item) => ({ characteristic_id: item.characteristic_id, governing_rule_id: item.assessment_rule_id, decision_code: "CANONICAL", inputs: [], finding_refs: [] })),
    },
  };
}

const contract = (contractId: string) => ({ contract_id: contractId, version: "1" });

function qb(overrides: Record<string, unknown> = {}) {
  return {
    snapshot_id: { value: "qb-snapshot-sha256:canonical" },
    state: "COMPUTED",
    value: { numerator: 7, denominator: 11 },
    reasons: ["QB_MATERIAL_UNRESOLVED_EXTRACTION", "FUTURE_REASON"],
    rconf_participant_ids: ["R001", "R002"],
    rconf_complete: true,
    observability: {
      total_requirement_count: 2, requirements_with_observations_count: 2, requirements_in_applicable_comparisons_count: 2,
      total_requirement_pair_count: 1, total_observation_pair_count: 4, confirmed_conflict_count: 1, compatible_count: 1,
      unresolved_count: 1, outside_applicability_count: 1, applicable_comparison_count: 2, global_unresolved_extraction_count: 3,
      qb_material_unresolved_count: 1, qb_non_material_diagnostic_count: 2, observed_rconf_count: 2, rconf_complete: true,
    },
    coverage_profile: contract("QB-v0.1"), aggregation_rule: contract("QB-CONSISTENCY-001"),
    cross_result_ids: [{ value: "CR-1" }, { value: "CR-2" }],
    materiality_diagnostic_refs: [],
    formula_operands: { total_requirement_count: 99, observed_rconf_count: 98 },
    non_claim_contract: contract("QB-NON-CLAIMS-001"), non_claim_keys: ["NC-QB-BASE"],
    ...overrides,
  };
}

function crossResult(resultId: string, state: string, left = "R001", right = "R002") {
  return {
    result_id: { value: resultId }, state,
    participants: [{ source_order: 0, requirement_id: left }, { source_order: 1, requirement_id: right }],
    relation_kind: "QUANTITATIVE_BOUND",
    conflict_class: state === "CONFIRMED_CONFLICT" ? "LOGICAL_CONFLICT" : null,
    conflict_subtype: state === "CONFIRMED_CONFLICT" ? "DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY" : null,
    unresolved_reasons: state === "ASSESSMENT_UNRESOLVED" ? ["MISSING_VALUE"] : [],
    outside_reasons: state === "OUTSIDE_V0_1_APPLICABILITY" ? ["METRIC_MISMATCH"] : [],
    evidence_refs: [{ requirement_id: left, evidence_id: "E-LEFT" }, { requirement_id: right, evidence_id: "E-RIGHT" }],
    comparison_contract: contract("QB-COMPARISON"), coverage_profile: contract("QB-v0.1"), non_claim_keys: ["NC-QB-BASE"],
  };
}

function result(overrides: Partial<CanonicalAnalyzeResponse> = {}): CanonicalAnalyzeResponse {
  return {
    contract_version: "research-api-v1", analysis_case: "INITIAL", controlled_scenario: null,
    requirements: [requirement("R001", 3, [1, 2, 3]), requirement("R002", 8, [9, 8, 7])],
    specification: {
      snapshot_id: "qb-snapshot-sha256:canonical",
      quality_profile: {
        completeness: aggregate("COMPLETENESS", 13, 17, "COMPUTED", [1, 1, 0, 2]),
        verifiability: aggregate("VERIFIABILITY", null, null, "UNKNOWN", [0, 2, 0, 2]),
        unambiguity: aggregate("UNAMBIGUITY", null, null, "NOT_APPLICABLE", [0, 0, 2, 2]),
      },
      qb_consistency: qb(),
      cross_results: [
        crossResult("CR-1", "CONFIRMED_CONFLICT"), crossResult("CR-2", "COMPATIBLE_WITHIN_RULE"),
        crossResult("CR-3", "ASSESSMENT_UNRESOLVED"), crossResult("CR-4", "OUTSIDE_V0_1_APPLICABILITY"),
      ],
      materiality: {
        snapshot_id: { value: "qb-snapshot-sha256:canonical" }, materiality_rule: contract("QB-MATERIALITY"),
        global_unresolved_diagnostic_count: 5, qb_material_count: 2, qb_non_material_count: 3,
        audit_records: [{ requirement_id: "R001", requirement_source_order: 0, diagnostic_code: "NUMERIC_CANDIDATE", diagnostic_rule_id: "DIAG-001", candidate_text: "500", diagnostic_start_offset: 10, diagnostic_end_offset: 13, disposition: "QB_NON_MATERIAL", materiality_rule: contract("QB-MATERIALITY") }],
      },
      projection_snapshot: {
        snapshot_id: { value: "qb-snapshot-sha256:canonical" },
        contracts: { projection: contract("QB-PROJECTION"), normalization: contract("QB-NORMALIZATION"), comparison: contract("QB-COMPARISON"), materiality: contract("QB-MATERIALITY"), aggregation: contract("QB-AGGREGATION"), coverage_profile: contract("QB-v0.1") },
        counts: { requirement_count: 2, observation_count: 4, evidence_count: 4, diagnostic_count: 5 },
      },
    },
    section_availability: ["overview", "requirements", "specification", "audit", "product_quality", "risk", "corrective_actions", "process"].map((section) => ({ section, availability: "AVAILABLE", reason_code: null })),
    full_model: null, reassessment_context: null,
    limitations: ["NO_COMBINED_QUALITY_SCORE", "BOUNDED_RESEARCH_MODEL"],
    ...overrides,
  };
}

function renderPage(payload = result(), onSelectRequirement = vi.fn()) {
  return { onSelectRequirement, ...render(<SpecificationPage result={payload} onSelectRequirement={onSelectRequirement} />) };
}

function response(payload: unknown): Response { return { ok: true, json: async () => payload } as Response; }

async function renderApp(payload = result()) {
  vi.spyOn(globalThis, "fetch").mockResolvedValue(response(payload));
  const client = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
  render(<QueryClientProvider client={client}><App /></QueryClientProvider>);
  fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
  fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
  await screen.findByRole("heading", { name: "Overview" });
}

describe("RUI-09 Specification page", () => {
  beforeEach(async () => { window.sessionStorage.clear(); await i18n.changeLanguage("en"); });
  afterEach(() => { cleanup(); vi.restoreAllMocks(); });

  it("opens from result navigation without another analysis request and keeps the response immutable", async () => {
    const payload = result();
    const before = JSON.stringify(payload);
    await renderApp(payload);
    fireEvent.click(screen.getByRole("button", { name: "Specification" }));
    expect(await screen.findByRole("heading", { name: "Specification" })).toBeTruthy();
    expect(vi.mocked(globalThis.fetch)).toHaveBeenCalledTimes(1);
    expect(JSON.stringify(payload)).toBe(before);
  });

  it("uses API specification aggregates, preserves exact fractions, counts, and rule IDs", () => {
    renderPage();
    const completeness = screen.getByRole("heading", { name: "Completeness" }).closest("article")!;
    expect(within(completeness).getByLabelText("Exact value: 13/17")).toBeTruthy();
    expect(within(completeness).getAllByText("1")).toHaveLength(2);
    expect(within(completeness).getByText("AGG-MVP-001")).toBeTruthy();
    expect(within(completeness).queryByText("1/10")).toBeNull();
  });

  it("shows UNKNOWN and NOT_APPLICABLE without numeric zero", () => {
    renderPage();
    const verifiability = screen.getByRole("heading", { name: "Verifiability" }).closest("article")!;
    const unambiguity = screen.getByRole("heading", { name: "Unambiguity" }).closest("article")!;
    expect(within(verifiability).getByText("No numeric value")).toBeTruthy();
    expect(within(unambiguity).getByText("No numeric value")).toBeTruthy();
    expect(within(verifiability).queryByLabelText("Exact value: 0")).toBeNull();
    expect(within(unambiguity).queryByLabelText("Exact value: 0")).toBeNull();
  });

  it.each([[-1, "negative"] as const, ["2", "malformed"] as const])("does not replace %s aggregate count with zero (%s)", (badCount, _label) => {
    const payload = result();
    const profile = payload.specification.quality_profile as Record<string, Record<string, unknown>>;
    profile.completeness.computed_count = badCount;
    renderPage(payload);
    const completeness = screen.getByRole("heading", { name: "Completeness" }).closest("article")!;
    expect(within(completeness).getByText("Malformed canonical presentation data")).toBeTruthy();
    expect(within(completeness).queryByText("AGG-MVP-001")).toBeNull();
  });

  it("keeps QB separate, exact, reason-ordered, and does not calculate it from operands", () => {
    renderPage();
    const qbSection = screen.getByRole("heading", { name: "QB consistency" }).closest("section")!;
    expect(within(qbSection).getByLabelText("Exact value: 7/11")).toBeTruthy();
    const reasons = within(qbSection).getByRole("heading", { name: "Canonical reasons" }).nextElementSibling!;
    expect(Array.from(reasons.querySelectorAll("code")).map((item) => item.textContent)).toEqual(["QB_MATERIAL_UNRESOLVED_EXTRACTION", "FUTURE_REASON"]);
    expect(within(qbSection).queryByText("1/99")).toBeNull();
    expect(within(qbSection).getByText("99")).toBeTruthy();
    expect(within(qbSection).getByText("98")).toBeTruthy();
  });

  it.each(["UNKNOWN", "NOT_APPLICABLE"])("withholds a QB numeric value for %s", (state) => {
    const payload = result();
    payload.specification = { ...payload.specification, qb_consistency: qb({ state, value: null }) };
    renderPage(payload);
    const qbSection = screen.getByRole("heading", { name: "QB consistency" }).closest("section")!;
    expect(within(qbSection).getByText("No numeric value")).toBeTruthy();
    expect(within(qbSection).queryByLabelText("Exact value: 0")).toBeNull();
  });

  it("shows independent observability counts and unchanged contract/non-claim identities", () => {
    renderPage();
    expect(screen.getByText("99")).toBeTruthy();
    expect(screen.getAllByText("QB-v0.1").length).toBeGreaterThan(0);
    expect(screen.getByText("QB-CONSISTENCY-001")).toBeTruthy();
    expect(screen.getAllByText("QB-NON-CLAIMS-001").length).toBeGreaterThan(0);
    expect(screen.getAllByText("NC-QB-BASE").length).toBeGreaterThan(0);
    expect(screen.queryByText(/%/)).toBeNull();
    expect(screen.getByText(/not overall specification completeness or quality/i)).toBeTruthy();
  });

  it("preserves contribution order and direct requirement values without an overall column", () => {
    renderPage();
    const table = screen.getByRole("table", { name: "Requirement-level C/V/U contributions" });
    expect(within(table).getAllByRole("row").slice(1).map((row) => within(row).getAllByRole("code")[0].textContent)).toEqual(["R001", "R002"]);
    expect(within(table).getByLabelText("Exact value: 1/10")).toBeTruthy();
    expect(within(table).getByLabelText("Exact value: 9/10")).toBeTruthy();
    expect(within(table).queryByText(/average|overall/i)).toBeNull();
  });

  it("keeps a malformed top-level requirement position visible and non-navigable", () => {
    const payload = result();
    payload.requirements.splice(1, 0, { requirement: { id: "BROKEN" }, quality_profile: null });
    renderPage(payload);
    const table = screen.getByRole("table", { name: "Requirement-level C/V/U contributions" });
    expect(within(table).getByText("Response position 2")).toBeTruthy();
    expect(within(table).getByText("No canonical identity")).toBeTruthy();
  });

  it("navigates from R002 contribution to the exact Requirement without an API call and preserves selection across locale", async () => {
    await renderApp();
    fireEvent.click(screen.getByRole("button", { name: "Specification" }));
    fireEvent.click(await screen.findByRole("button", { name: "Open R002" }));
    expect(await screen.findByRole("heading", { name: "R002" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));
    expect(await screen.findByRole("heading", { name: "R002" })).toBeTruthy();
    expect(vi.mocked(globalThis.fetch)).toHaveBeenCalledTimes(1);
  });

  it("clears selected requirement on reset before the next analysis", async () => {
    await renderApp();
    fireEvent.click(screen.getByRole("button", { name: "Specification" }));
    fireEvent.click(await screen.findByRole("button", { name: "Open R002" }));
    expect(await screen.findByRole("heading", { name: "R002" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "New specification" }));
    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    await screen.findByRole("heading", { name: "Overview" });
    fireEvent.click(screen.getByRole("button", { name: "Requirements" }));
    expect(await screen.findByRole("heading", { name: "R001" })).toBeTruthy();
  });

  it("preserves cross-result order, distinct states, evidence refs, and bounded non-claims", () => {
    renderPage();
    const cards = document.querySelectorAll(".cross-result-card");
    expect(Array.from(cards).map((card) => card.querySelector("code")?.textContent)).toEqual(["CR-1", "CR-2", "CR-3", "CR-4"]);
    expect(screen.getByText(/not an overall specification failure/i)).toBeTruthy();
    expect(screen.getByText(/not proof of global consistency/i)).toBeTruthy();
    expect(screen.getByText(/remains unresolved/i)).toBeTruthy();
    expect(screen.getByText(/outside v0.1 applicability/i)).toBeTruthy();
    expect(screen.getAllByText("E-LEFT").length).toBe(4);
  });

  it("navigates only resolvable cross-result participants", () => {
    const payload = result();
    const specification = payload.specification as Record<string, unknown>;
    specification.cross_results = [crossResult("CR-DANGLING", "COMPATIBLE_WITHIN_RULE", "R001", "R999")];
    const onSelect = vi.fn();
    renderPage(payload, onSelect);
    fireEvent.click(screen.getByRole("button", { name: "R001" }));
    expect(onSelect).toHaveBeenCalledWith("R001");
    expect(screen.queryByRole("button", { name: "R999" })).toBeNull();
    expect(screen.getByText(/does not resolve to a canonical requirement/)).toBeTruthy();
  });

  it("keeps malformed cross-result positions visible", () => {
    const payload = result();
    const specification = payload.specification as Record<string, unknown>;
    specification.cross_results = [crossResult("CR-1", "CONFIRMED_CONFLICT"), { result_id: "broken" }, crossResult("CR-3", "ASSESSMENT_UNRESOLVED")];
    renderPage(payload);
    expect(screen.getByText("Response position 2")).toBeTruthy();
    expect(document.querySelectorAll(".cross-result-card")).toHaveLength(3);
  });

  it("presents distinct materiality counts and keeps candidate spans out of Evidence", () => {
    renderPage();
    const materialitySection = screen.getByRole("heading", { name: "Materiality trace" }).closest("section")!;
    const summary = materialitySection.querySelector(".materiality-summary")!;
    expect(within(summary as HTMLElement).getByText("5")).toBeTruthy();
    expect(within(summary as HTMLElement).getByText("2")).toBeTruthy();
    expect(within(summary as HTMLElement).getByText("3")).toBeTruthy();
    fireEvent.click(screen.getByText("Diagnostic audit records (1)"));
    expect(screen.getByText("500")).toBeTruthy();
    expect(screen.getByText("A diagnostic candidate is not accepted Evidence.")).toBeTruthy();
    expect(screen.queryByRole("button", { name: /500/ })).toBeNull();
  });

  it("projects malformed nested data through neutral boundaries without inventing state", () => {
    const payload = result();
    const specification = payload.specification as Record<string, unknown>;
    specification.qb_consistency = { ...qb(), observability: { total_requirement_count: -1 } };
    specification.materiality = { global_unresolved_diagnostic_count: -1 };
    renderPage(payload);
    expect(screen.getAllByText("Malformed canonical presentation data").length).toBeGreaterThan(0);
    expect(screen.queryByText("-1")).toBeNull();
  });

  it("does not expose a combined specification quality score", () => {
    renderPage();
    expect(screen.queryByText("Overall specification quality score")).toBeNull();
    expect(screen.getByText("NO_COMBINED_QUALITY_SCORE")).toBeTruthy();
  });

  it("projection preserves exact API values and response positions without mutating input", () => {
    const payload = result();
    const before = JSON.stringify(payload);
    const projected = selectSpecificationPage(payload);
    expect(projected.aggregates.completeness?.value).toEqual({ numerator: "13", denominator: "17" });
    expect(projected.qb?.value).toEqual({ numerator: "7", denominator: "11" });
    expect(projected.contributions.map((entry) => entry.position)).toEqual([1, 2]);
    expect(JSON.stringify(payload)).toBe(before);
  });
});

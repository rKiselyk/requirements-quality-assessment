import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../../App";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { i18n } from "../../i18n";
import { RequirementsPage } from "../requirements/RequirementsPage";
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
    reasons: [],
    rconf_participant_ids: ["R001", "R002"],
    rconf_complete: true,
    observability: {
      total_requirement_count: 2, requirements_with_observations_count: 2, requirements_in_applicable_comparisons_count: 2,
      total_requirement_pair_count: 1, total_observation_pair_count: 4, confirmed_conflict_count: 1, compatible_count: 1,
      unresolved_count: 1, outside_applicability_count: 1, applicable_comparison_count: 2, global_unresolved_extraction_count: 1,
      qb_material_unresolved_count: 0, qb_non_material_diagnostic_count: 1, observed_rconf_count: 2, rconf_complete: true,
    },
    coverage_profile: contract("QB-v0.1"), aggregation_rule: contract("QB-CONSISTENCY-001"),
    cross_result_ids: [{ value: "CR-1" }, { value: "CR-2" }, { value: "CR-3" }, { value: "CR-4" }],
    materiality_diagnostic_refs: [{ requirement_id: "R001", feature_id: "quantitative_constraint", diagnostic_index: 0 }],
    formula_operands: { total_requirement_count: 2, observed_rconf_count: 2 },
    non_claim_contract: contract("QB-NON-CLAIMS-001"), non_claim_keys: ["NC-QB-BASE"],
    ...overrides,
  };
}

function crossResult(resultId: string, state: string, left = "R001", right = "R002") {
  const leftObservation = { requirement_id: left, feature_id: "quantitative_constraint", observation_index: 0 };
  const rightObservation = { requirement_id: right, feature_id: "quantitative_constraint", observation_index: 1 };
  return {
    result_id: { value: resultId }, snapshot_id: { value: "qb-snapshot-sha256:canonical" }, state,
    participants: [{ source_order: 0, requirement_id: left }, { source_order: 1, requirement_id: right }],
    observation_refs: [leftObservation, rightObservation],
    operands: {
      left: { snapshot_id: { value: "qb-snapshot-sha256:canonical" }, observation_ref: leftObservation, normalized_metric: "response_time", normalized_context: "normal_load", comparator: "LESS_THAN_OR_EQUAL", inclusivity: "INCLUSIVE", value: "2.500", unit: "SECOND" },
      right: { snapshot_id: { value: "qb-snapshot-sha256:canonical" }, observation_ref: rightObservation, normalized_metric: "response_time", normalized_context: "normal_load", comparator: "GREATER_THAN_OR_EQUAL", inclusivity: "INCLUSIVE", value: "5", unit: "SECOND" },
    },
    relation_kind: "QUANTITATIVE_BOUND",
    conflict_class: state === "CONFIRMED_CONFLICT" ? "LOGICAL_CONFLICT" : null,
    conflict_subtype: state === "CONFIRMED_CONFLICT" ? "DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY" : null,
    unresolved_reasons: state === "ASSESSMENT_UNRESOLVED" ? ["MISSING_VALUE"] : [],
    outside_reasons: state === "OUTSIDE_V0_1_APPLICABILITY" ? ["METRIC_MISMATCH"] : [],
    evidence_refs: [{ requirement_id: left, evidence_id: "E-LEFT" }, { requirement_id: right, evidence_id: "E-RIGHT" }],
    diagnostic_refs: [{ requirement_id: left, feature_id: "quantitative_constraint", diagnostic_index: 0 }],
    comparison_key: { normalized_metric: "response_time", normalized_context: "normal_load", unit: "SECOND" },
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
        global_unresolved_diagnostic_count: 1, qb_material_count: 0, qb_non_material_count: 1,
        audit_records: [{
          snapshot_id: { value: "qb-snapshot-sha256:canonical" }, requirement_id: "R001", requirement_source_order: 0,
          diagnostic_ref: { requirement_id: "R001", feature_id: "quantitative_constraint", diagnostic_index: 0 },
          diagnostic_code: "NUMERIC_CANDIDATE", diagnostic_rule_id: "DIAG-001", candidate_text: "500", diagnostic_start_offset: 10, diagnostic_end_offset: 13,
          matched_context_evidence_ref: { requirement_id: "R001", evidence_id: "E-CONTEXT" }, matched_allowlist_contract: contract("QB-MATERIALITY-ALLOWLIST"),
          disposition: "QB_NON_MATERIAL", materiality_rule: contract("QB-MATERIALITY"),
          gate_outcomes: { exact_diagnostic_code: true, exact_diagnostic_rule: true, exact_candidate_text: true, candidate_inside_context: true, same_observation: true, allowlisted_contract_guarantee: true, no_qb_competition: true, provenance_integrity: true },
        }],
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

  it("keeps QB separate, exact, and does not calculate it from operands", () => {
    renderPage();
    const qbSection = screen.getByRole("heading", { name: "QB consistency" }).closest("section")!;
    expect(within(qbSection).getByLabelText("Exact value: 7/11")).toBeTruthy();
    expect(within(qbSection).queryByText("0/2")).toBeNull();
  });

  it("preserves canonical QB reason order for a domain-consistent withholding state", () => {
    const payload = result();
    payload.specification = { ...payload.specification, qb_consistency: qb({ state: "UNKNOWN", value: null, reasons: ["QB_MATERIAL_UNRESOLVED_EXTRACTION", "FUTURE_REASON"] }) };
    renderPage(payload);
    const qbSection = screen.getByRole("heading", { name: "QB consistency" }).closest("section")!;
    const reasons = within(qbSection).getByRole("heading", { name: "Canonical reasons" }).nextElementSibling!;
    expect(Array.from(reasons.querySelectorAll("code")).map((item) => item.textContent)).toEqual(["QB_MATERIAL_UNRESOLVED_EXTRACTION", "FUTURE_REASON"]);
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
    const currentQb = qb();
    specification.qb_consistency = { ...currentQb, cross_result_ids: [{ value: "CR-DANGLING" }], observability: { ...(currentQb.observability as Record<string, unknown>), total_observation_pair_count: 1 } };
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
    expect(Array.from(summary.querySelectorAll("strong")).map((item) => item.textContent)).toEqual(["1", "0", "1"]);
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

  it("rejects an aggregate in the wrong characteristic slot", () => {
    const payload = result();
    const profile = payload.specification.quality_profile as Record<string, Record<string, unknown>>;
    profile.completeness.characteristic_id = "VERIFIABILITY";
    expect(selectSpecificationPage(payload).aggregates.completeness).toBeNull();
  });

  it("rejects a contribution characteristic in the wrong slot", () => {
    const payload = result();
    const r2 = payload.requirements[1] as Record<string, Record<string, Record<string, unknown>>>;
    r2.quality_profile.completeness.characteristic_id = "UNAMBIGUITY";
    expect(selectSpecificationPage(payload).contributions[1].kind).toBe("MALFORMED");
  });

  it("rejects aggregate count sums and rule identities that contradict the contract", () => {
    const countPayload = result();
    const countProfile = countPayload.specification.quality_profile as Record<string, Record<string, unknown>>;
    countProfile.completeness.total_count = 3;
    expect(selectSpecificationPage(countPayload).aggregates.completeness).toBeNull();

    const rulePayload = result();
    const ruleProfile = rulePayload.specification.quality_profile as Record<string, Record<string, unknown>>;
    ruleProfile.verifiability.aggregation_rule_id = "FUTURE-RULE";
    expect(selectSpecificationPage(rulePayload).aggregates.verifiability).toBeNull();
  });

  it.each([
    ["COMPUTED without computed population", { state: "COMPUTED", value: { numerator: 1, denominator: 2 }, computed_count: 0, unknown_count: 2, not_applicable_count: 0, total_count: 2 }],
    ["UNKNOWN with computed population", { state: "UNKNOWN", value: null, computed_count: 1, unknown_count: 1, not_applicable_count: 0, total_count: 2 }],
    ["NOT_APPLICABLE with unknown population", { state: "NOT_APPLICABLE", value: null, computed_count: 0, unknown_count: 1, not_applicable_count: 1, total_count: 2 }],
    ["COMPUTED outside the exact unit interval", { state: "COMPUTED", value: { numerator: 3, denominator: 2 }, computed_count: 2, unknown_count: 0, not_applicable_count: 0, total_count: 2 }],
  ])("rejects invalid aggregate state/count matrix: %s", (_label, overrides) => {
    const payload = result();
    const profile = payload.specification.quality_profile as Record<string, Record<string, unknown>>;
    Object.assign(profile.completeness, overrides);
    expect(selectSpecificationPage(payload).aggregates.completeness).toBeNull();
  });

  it("does not present three different aggregate populations as one coherent profile", () => {
    const payload = result();
    const profile = payload.specification.quality_profile as Record<string, Record<string, unknown>>;
    Object.assign(profile.unambiguity, { not_applicable_count: 3, total_count: 3 });
    expect(selectSpecificationPage(payload).aggregates).toEqual({ completeness: null, verifiability: null, unambiguity: null });
  });

  it("disables contribution navigation when RUI-08 cannot safely resolve the displayed requirement", () => {
    const payload = result();
    delete (payload.requirements[1] as Record<string, unknown>).features;
    renderPage(payload);
    expect(screen.queryByRole("button", { name: "Open R002" })).toBeNull();
    expect(screen.getByText("Requirement detail is not safely resolvable")).toBeTruthy();
  });

  it("never substitutes R001 for an explicitly requested unresolvable requirement", () => {
    render(<RequirementsPage result={result()} selectedRequirementId="R999" />);
    expect(screen.getByText("Requested requirement cannot be safely presented")).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "R001" })).toBeNull();
    expect(screen.getByText(/No other requirement was substituted/)).toBeTruthy();
  });

  it("preserves observation refs, operands, comparison key, diagnostic refs, and exact decimal strings", () => {
    renderPage();
    const firstCard = document.querySelectorAll(".cross-result-card")[0] as HTMLElement;
    fireEvent.click(within(firstCard).getByText("Show canonical comparison trace"));
    expect(within(firstCard).getAllByText(/R001 \/ quantitative_constraint \/ 0/).length).toBeGreaterThan(0);
    expect(within(firstCard).getByText("2.500")).toBeTruthy();
    expect(within(firstCard).getAllByText("response_time").length).toBeGreaterThan(0);
    expect(within(firstCard).getAllByText("normal_load").length).toBeGreaterThan(0);
    expect(within(firstCard).getAllByText("SECOND").length).toBeGreaterThan(0);
  });

  it.each([
    ["CONFIRMED_CONFLICT", { conflict_class: null }],
    ["COMPATIBLE_WITHIN_RULE", { unresolved_reasons: ["MISSING_VALUE"] }],
    ["ASSESSMENT_UNRESOLVED", { unresolved_reasons: [] }],
    ["OUTSIDE_V0_1_APPLICABILITY", { conflict_subtype: "DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY" }],
  ])("renders contradictory cross-result state data as malformed: %s", (state, contradiction) => {
    const payload = result();
    const specification = payload.specification as Record<string, unknown>;
    specification.cross_results = [{ ...crossResult("CR-1", state), ...contradiction }, ...((specification.cross_results as unknown[]).slice(1))];
    expect(selectSpecificationPage(payload).crossResults[0]).toBeNull();
  });

  it("disables participant navigation when source-order identity disagrees with the requirement population", () => {
    const payload = result();
    const mismatch = crossResult("CR-1", "CONFIRMED_CONFLICT");
    mismatch.participants = [{ source_order: 0, requirement_id: "R002" }, { source_order: 1, requirement_id: "R001" }];
    const specification = payload.specification as Record<string, unknown>;
    specification.cross_results = [mismatch, ...((specification.cross_results as unknown[]).slice(1))];
    renderPage(payload);
    const firstCard = document.querySelectorAll(".cross-result-card")[0] as HTMLElement;
    expect(within(firstCard).queryByRole("button", { name: "R001" })).toBeNull();
    expect(within(firstCard).queryByRole("button", { name: "R002" })).toBeNull();
  });

  it("keeps valid cross participants navigable", () => {
    const onSelect = vi.fn();
    renderPage(result(), onSelect);
    const firstCard = document.querySelectorAll(".cross-result-card")[0] as HTMLElement;
    fireEvent.click(within(firstCard).getByRole("button", { name: "R002" }));
    expect(onSelect).toHaveBeenCalledWith("R002");
  });

  it("shows the complete canonical materiality proof and all eight gate outcomes", () => {
    renderPage();
    fireEvent.click(screen.getByText("Diagnostic audit records (1)"));
    const materiality = screen.getByRole("heading", { name: "Materiality trace" }).closest("section")!;
    expect(within(materiality).getAllByText(/R001 \/ quantitative_constraint \/ 0/).length).toBeGreaterThan(0);
    expect(within(materiality).getByText("E-CONTEXT")).toBeTruthy();
    expect(within(materiality).getByText("QB-MATERIALITY-ALLOWLIST")).toBeTruthy();
    const gates = materiality.querySelector(".materiality-gates")!;
    expect(gates.querySelectorAll("dt")).toHaveLength(8);
    expect(Array.from(gates.querySelectorAll("dd code")).map((item) => item.textContent)).toEqual(Array(8).fill("true"));
  });

  it.each([
    ["count sum", { global_unresolved_diagnostic_count: 2, qb_material_count: 0, qb_non_material_count: 1 }],
    ["audit cardinality", { global_unresolved_diagnostic_count: 2, qb_material_count: 0, qb_non_material_count: 2 }],
    ["disposition count", { global_unresolved_diagnostic_count: 1, qb_material_count: 1, qb_non_material_count: 0 }],
  ])("rejects inconsistent materiality %s", (_label, countOverrides) => {
    const payload = result();
    const specification = payload.specification as Record<string, Record<string, unknown>>;
    Object.assign(specification.materiality, countOverrides);
    expect(selectSpecificationPage(payload).materiality).toBeNull();
  });

  it("rejects QB/specification snapshot and direct cardinality contradictions", () => {
    const snapshotPayload = result();
    const snapshotSpec = snapshotPayload.specification as Record<string, unknown>;
    snapshotSpec.qb_consistency = qb({ snapshot_id: { value: "qb-snapshot-sha256:other" } });
    expect(selectSpecificationPage(snapshotPayload).qb).toBeNull();

    const rconfPayload = result();
    const rconfSpec = rconfPayload.specification as Record<string, unknown>;
    const current = qb();
    rconfSpec.qb_consistency = { ...current, rconf_complete: false };
    expect(selectSpecificationPage(rconfPayload).qb).toBeNull();

    const operandPayload = result();
    const operandSpec = operandPayload.specification as Record<string, unknown>;
    operandSpec.qb_consistency = { ...current, formula_operands: { total_requirement_count: 2, observed_rconf_count: 1 } };
    expect(selectSpecificationPage(operandPayload).qb).toBeNull();
  });

  it("rejects COMPUTED QB with withholding reasons without calculating a replacement", () => {
    const payload = result();
    const specification = payload.specification as Record<string, unknown>;
    specification.qb_consistency = qb({ reasons: ["ASSESSMENT_UNRESOLVED_PAIR"] });
    expect(selectSpecificationPage(payload).qb).toBeNull();
  });

  it("uses a domain-consistent valid COMPUTED QB fixture", () => {
    const projection = selectSpecificationPage(result());
    expect(projection.qb).not.toBeNull();
    expect(projection.qb?.reasons).toEqual([]);
    expect(projection.qb?.crossResultIds).toHaveLength(4);
    expect(projection.qb?.materialityDiagnosticRefs).toHaveLength(1);
  });

  it("degrades materiality, projection, cross, and audit snapshot mismatches independently", () => {
    const materialityPayload = result();
    const materialitySpec = materialityPayload.specification as Record<string, Record<string, unknown>>;
    materialitySpec.materiality.snapshot_id = { value: "qb-snapshot-sha256:other" };
    expect(selectSpecificationPage(materialityPayload).materiality).toBeNull();

    const projectionPayload = result();
    const projectionSpec = projectionPayload.specification as Record<string, Record<string, unknown>>;
    projectionSpec.projection_snapshot.snapshot_id = { value: "qb-snapshot-sha256:other" };
    expect(selectSpecificationPage(projectionPayload).projectionTrace).toBeNull();

    const crossPayload = result();
    const crossSpec = crossPayload.specification as Record<string, unknown>;
    const cross = crossResult("CR-1", "CONFIRMED_CONFLICT");
    cross.snapshot_id = { value: "qb-snapshot-sha256:other" };
    crossSpec.cross_results = [cross, ...((crossSpec.cross_results as unknown[]).slice(1))];
    expect(selectSpecificationPage(crossPayload).crossResults[0]).toBeNull();

    const auditPayload = result();
    const auditSpec = auditPayload.specification as Record<string, Record<string, unknown>>;
    const audits = auditSpec.materiality.audit_records as Array<Record<string, unknown>>;
    audits[0].snapshot_id = { value: "qb-snapshot-sha256:other" };
    expect(selectSpecificationPage(auditPayload).materiality).toBeNull();
  });

  it("requires ordered QB cross-result IDs to match ordered result records", () => {
    const payload = result();
    const specification = payload.specification as Record<string, unknown>;
    specification.qb_consistency = qb({ cross_result_ids: [{ value: "CR-2" }, { value: "CR-1" }, { value: "CR-3" }, { value: "CR-4" }] });
    const projection = selectSpecificationPage(payload);
    expect(projection.qb).toBeNull();
    expect(projection.crossResults.every((item) => item === null)).toBe(true);
  });

  it("requires ordered QB materiality refs to match ordered audit refs", () => {
    const payload = result();
    const specification = payload.specification as Record<string, unknown>;
    specification.qb_consistency = qb({ materiality_diagnostic_refs: [{ requirement_id: "R002", feature_id: "quantitative_constraint", diagnostic_index: 0 }] });
    const projection = selectSpecificationPage(payload);
    expect(projection.qb).toBeNull();
    expect(projection.materiality).toBeNull();
  });
});

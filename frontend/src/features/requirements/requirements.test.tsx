import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../../App";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { validateEvidenceSpan } from "../../components/scientific";
import { i18n } from "../../i18n";
import { RequirementsPage } from "./RequirementsPage";
import { selectFullProfile, selectRequirements } from "./projection";

const feature = (featureId: string, diagnostics: unknown[] = []) => ({
  feature_id: featureId,
  status: diagnostics.length ? "UNRESOLVED" : "DETECTED",
  processing_status: diagnostics.length ? "INCOMPLETE" : "COMPLETE",
  observations: [],
  diagnostics,
});

const finding = (evidenceRefs = ["E-EMOJI"]) => ({
  finding_id: "F-SIGNAL-1",
  requirement_id: "R001",
  characteristic_id: "UNAMBIGUITY",
  kind: "SIGNAL",
  code: "VAGUE_TERM_SIGNAL",
  rule_id: "CALC-U-MVP-001",
  criterion_id: "U-VAGUE-TERM",
  evidence_refs: evidenceRefs,
  explanation: "A bounded detector supplied a signal; this is not automatically a quality problem.",
});

const assessment = (id: string, numerator: number | null, denominator: number | null, state = "COMPUTED", findings: unknown[] = []) => ({
  characteristic_id: id,
  state,
  value: numerator === null || denominator === null ? null : { numerator, denominator },
  assessment_rule_id: `RULE-${id}`,
  findings,
  explanation: `Canonical ${id} explanation.`,
});

const traces = (id: string) => ({
  characteristic_id: id,
  governing_rule_id: `RULE-${id}`,
  decision_code: `${id}_DECISION`,
  inputs: [{ feature_id: "condition_context", applicability: "APPLICABLE", observation_indexes: [0], diagnostic_indexes: [], effect_code: `${id}_INPUT` }],
  finding_refs: id === "UNAMBIGUITY" ? ["F-SIGNAL-1"] : [],
});

function requirement(id: string, sourceLine: number, text: string, evidence: unknown[], withSignal = false) {
  return {
    requirement: { id, source_line: sourceLine, text },
    features: {
      condition_contexts: feature("condition_context"),
      expected_results: feature("expected_result"),
      acceptance_criteria: feature("acceptance_criterion"),
      quantitative_constraints: feature("quantitative_constraint", id === "R001" ? [{
        code: "NUMERIC_CANDIDATE",
        explanation: "A candidate was observed but not accepted as Evidence.",
        rule_id: "DIAG-001",
        candidate_span: { text: "500", start_offset: 10, end_offset: 13 },
      }] : []),
      verification_methods: feature("verification_method"),
      vague_term_occurrences: feature("vague_term_occurrence"),
    },
    evidence: evidence.map((item) => ({ ...(item as Record<string, unknown>) })),
    quality_profile: {
      completeness: assessment("COMPLETENESS", 13, 17),
      verifiability: assessment("VERIFIABILITY", null, null, "UNKNOWN"),
      unambiguity: assessment("UNAMBIGUITY", 1, 2, "COMPUTED", withSignal ? [finding()] : []),
    },
    trace: {
      requirement_id: id,
      coverage_profile_id: "MVP-V0.1-BOUNDED-CVU-001",
      characteristics: [traces("COMPLETENESS"), traces("VERIFIABILITY"), traces("UNAMBIGUITY")],
    },
  };
}

const r1Text = "😀 Швидко відповісти за 500 мс.";
const r2Text = "Система зберігає журнал без змін!";
const r1Evidence = [
  { evidence_id: "E-EMOJI", requirement_id: "R001", feature_id: "vague_term_occurrence", text: "Швидко", start_offset: 2, end_offset: 8, rule_id: "VAGUE-001" },
  { evidence_id: "E-NUMBER", requirement_id: "R001", feature_id: "quantitative_constraint", text: "500 мс", start_offset: 22, end_offset: 28, rule_id: "QUANT-001" },
];
const r2Evidence = [
  { evidence_id: "E-R002", requirement_id: "R002", feature_id: "expected_result", text: "зберігає журнал", start_offset: 8, end_offset: 23, rule_id: "RESULT-001" },
];

const externalSlots = [
  ["singularity", "SINGULARITY"], ["presentation_conformance", "PRESENTATION_CONFORMANCE"], ["correctness", "CORRECTNESS"],
  ["feasibility", "FEASIBILITY"], ["necessity", "NECESSITY"], ["relevance", "RELEVANCE"],
] as const;

function fullProfile(id: string, sourceLine: number) {
  const profile: Record<string, unknown> = {
    requirement_ref: { requirement_id: id, source_line: sourceLine },
    automatic_record: { extraction_result: { requirement: { id, source_line: sourceLine } } },
  };
  for (const [slot, propertyId] of externalSlots) {
    profile[slot] = {
      property_id: propertyId,
      state: "AVAILABLE",
      judgment: { judgment_id: `${id}-${propertyId}-JUDGMENT` },
      provenance: { source_ref: { source_id: `${id}-EXPERT`, source_version: "1" }, requirement_ref: { requirement_id: id, source_line: sourceLine } },
      explanation: `Canonical expert explanation for ${id} ${propertyId}.`,
    };
  }
  return profile;
}

function result(overrides: Partial<CanonicalAnalyzeResponse> = {}): CanonicalAnalyzeResponse {
  return {
    contract_version: "research-api-v1",
    analysis_case: "INITIAL",
    controlled_scenario: null,
    requirements: [requirement("R001", 3, r1Text, r1Evidence, true), requirement("R002", 8, r2Text, r2Evidence)],
    specification: {},
    section_availability: [],
    full_model: null,
    reassessment_context: null,
    limitations: [],
    ...overrides,
  };
}

function renderPage(payload = result()) {
  return render(<RequirementsPage result={payload} />);
}

function appResponse(payload: CanonicalAnalyzeResponse): Response {
  return { ok: true, json: async () => payload } as Response;
}

describe("RUI-08 Requirements page", () => {
  beforeEach(async () => {
    window.sessionStorage.clear();
    await i18n.changeLanguage("en");
  });

  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("selects the first canonical requirement by default and preserves server order", () => {
    renderPage();
    expect(screen.getByRole("heading", { name: "R001" })).toBeTruthy();
    const navigator = screen.getByRole("navigation", { name: "Canonical requirements" });
    expect(within(navigator).getAllByRole("button").map((button) => button.querySelector("strong")?.textContent)).toEqual(["R001", "R002"]);
    expect(screen.getAllByText(r1Text)).toHaveLength(2);
  });

  it("selects R002 as presentation state and displays its exact identity, line, and text", () => {
    renderPage();
    fireEvent.click(screen.getByRole("button", { name: /R002/ }));
    expect(screen.getByRole("heading", { name: "R002" })).toBeTruthy();
    expect(screen.getAllByText(r2Text)).toHaveLength(2);
    expect(document.querySelector(".requirement-source-card__identity")?.textContent).toContain("8");
  });

  it("projects C/V/U exact values and absence directly without displaying zero", () => {
    renderPage();
    expect(screen.getAllByLabelText("Exact value: 13/17").length).toBeGreaterThan(0);
    expect(screen.getAllByLabelText("Exact value: 1/2").length).toBeGreaterThan(0);
    const verifiability = screen.getByRole("heading", { name: "Verifiability" }).closest("article")!;
    expect(within(verifiability).getByText("UNKNOWN")).toBeTruthy();
    expect(within(verifiability).getByText("No numeric value")).toBeTruthy();
    expect(within(verifiability).queryByText("0")).toBeNull();
    expect(screen.getAllByText("RULE-COMPLETENESS").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Canonical COMPLETENESS explanation.").length).toBeGreaterThan(0);
  });

  it("uses presentation-malformed behavior for contradictory characteristic state/value", () => {
    const payload = result();
    const first = payload.requirements[0] as Record<string, unknown>;
    const quality = first.quality_profile as Record<string, unknown>;
    quality.completeness = assessment("COMPLETENESS", null, null, "COMPUTED");
    renderPage(payload);
    const completeness = screen.getByRole("heading", { name: "Completeness" }).closest("article")!;
    expect(within(completeness).getByText(/Nothing was inferred/)).toBeTruthy();
    expect(within(completeness).queryByText("COMPUTED")).toBeNull();
  });

  it("keeps NOT_APPLICABLE separate from zero", () => {
    const payload = result();
    const first = payload.requirements[0] as Record<string, unknown>;
    const quality = first.quality_profile as Record<string, unknown>;
    quality.verifiability = assessment("VERIFIABILITY", null, null, "NOT_APPLICABLE");
    renderPage(payload);
    const verifiability = screen.getByRole("heading", { name: "Verifiability" }).closest("article")!;
    expect(within(verifiability).getByText("NOT_APPLICABLE")).toBeTruthy();
    expect(within(verifiability).getByText("No numeric value")).toBeTruthy();
    expect(within(verifiability).queryByText("0")).toBeNull();
  });

  it("preserves every evidence record in canonical response order", () => {
    renderPage();
    const ids = Array.from(document.querySelectorAll(".evidence-list .evidence-badge code"), (node) => node.textContent);
    expect(ids).toEqual(["E-EMOJI", "E-NUMBER"]);
  });

  it("highlights Unicode code-point offsets exactly and opens the evidence drawer", () => {
    renderPage();
    fireEvent.click(screen.getAllByRole("button", { name: /E-EMOJI/ })[0]);
    const mark = document.querySelector("mark[data-evidence-id='E-EMOJI']")!;
    expect(mark.textContent).toBe("Швидко");
    expect(mark.parentElement?.textContent).toBe(r1Text);
    const drawer = screen.getByRole("dialog");
    expect(within(drawer).getByText("E-EMOJI")).toBeTruthy();
    expect(within(drawer).getByText("vague_term_occurrence")).toBeTruthy();
    expect(within(drawer).getByText("VAGUE-001")).toBeTruthy();
    expect(within(drawer).getByText("2")).toBeTruthy();
    expect(within(drawer).getByText("8")).toBeTruthy();
    expect(within(drawer).getByText("Швидко")).toBeTruthy();
  });

  it("proves the accepted emoji offset is not interpreted as a UTF-16 index", () => {
    const projected = selectRequirements(result())[0].evidence[0]!;
    expect(r1Text.substring(projected.startOffset, projected.endOffset)).not.toBe(projected.text);
    expect(validateEvidenceSpan(r1Text, projected)).toMatchObject({ valid: true, selected: "Швидко" });
  });

  it("does not fuzzy-search or approximate an evidence mismatch", () => {
    const payload = result();
    const first = payload.requirements[0] as Record<string, unknown>;
    (first.evidence as Array<Record<string, unknown>>)[0] = { ...r1Evidence[0], start_offset: 3, end_offset: 9 };
    renderPage(payload);
    fireEvent.click(screen.getAllByRole("button", { name: /E-EMOJI/ })[0]);
    expect(document.querySelector("mark")).toBeNull();
    expect(screen.getByText(/no approximate highlight was applied/)).toBeTruthy();
    expect(screen.getAllByText("Швидко").length).toBeGreaterThan(0);
  });

  it("closes the drawer, clears the highlight, and returns focus to the evidence badge", () => {
    renderPage();
    const badge = screen.getAllByRole("button", { name: /E-EMOJI/ })[0];
    fireEvent.click(badge);
    fireEvent.click(screen.getByRole("button", { name: "Close evidence drawer" }));
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.querySelector("mark")).toBeNull();
    expect(document.activeElement).toBe(badge);
  });

  it("keeps SIGNAL explicit and degrades dangling finding evidence safely", () => {
    const payload = result();
    const first = payload.requirements[0] as Record<string, unknown>;
    const quality = first.quality_profile as Record<string, unknown>;
    quality.unambiguity = assessment("UNAMBIGUITY", 1, 2, "COMPUTED", [finding(["E-EMOJI", "E-MISSING"])]);
    renderPage(payload);
    expect(screen.getByText("Signal")).toBeTruthy();
    expect(screen.getByText("SIGNAL")).toBeTruthy();
    expect(screen.queryByText("QUALITY_PROBLEM")).toBeNull();
    expect(screen.getByText("E-MISSING")).toBeTruthy();
    expect(screen.getByText(/Referenced evidence is not present/)).toBeTruthy();
  });

  it("keeps diagnostics distinct and never turns a candidate span into Evidence", () => {
    renderPage();
    fireEvent.click(screen.getByRole("tab", { name: "Diagnostics (1)" }));
    expect(screen.getByText("NUMERIC_CANDIDATE")).toBeTruthy();
    expect(screen.getByText("500")).toBeTruthy();
    expect(screen.getByText(/not accepted Evidence/)).toBeTruthy();
    expect(Array.from(document.querySelectorAll(".evidence-badge code"), (node) => node.textContent)).not.toContain("NUMERIC_CANDIDATE");
  });

  it("presents automatic C/V/U but no fabricated six-property records for INITIAL", () => {
    renderPage();
    expect(screen.getAllByText("AUTOMATIC")).toHaveLength(3);
    expect(screen.getByText("No canonical extended external/expert profile is present")).toBeTruthy();
    expect(screen.queryByText("EXTERNAL_EXPERT")).toBeNull();
  });

  it("matches a controlled full profile by requirement identity rather than list position", () => {
    const payload = result({
      analysis_case: "CONTROLLED_DEMO",
      controlled_scenario: { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" },
      full_model: { full_quality_profiles: [fullProfile("R002", 8), fullProfile("R001", 3)] },
    });
    renderPage(payload);
    expect(screen.getAllByText("EXTERNAL_EXPERT")).toHaveLength(6);
    expect(screen.getByText("R001-SINGULARITY-JUDGMENT")).toBeTruthy();
    expect(screen.queryByText("R002-SINGULARITY-JUDGMENT")).toBeNull();
    expect(screen.getAllByText("AUTOMATIC")).toHaveLength(3);
    expect(document.body.textContent).not.toMatch(/overall requirement score/i);
    expect(selectFullProfile(payload, selectRequirements(payload)[0].requirement).kind).toBe("PRESENT");
  });

  it("keeps external UNKNOWN, UNAVAILABLE, and NOT_APPLICABLE states non-numeric", () => {
    const profile = fullProfile("R001", 3);
    for (const [slot, , state] of [
      ["singularity", "SINGULARITY", "UNKNOWN"],
      ["presentation_conformance", "PRESENTATION_CONFORMANCE", "UNAVAILABLE"],
      ["correctness", "CORRECTNESS", "NOT_APPLICABLE"],
    ] as const) {
      profile[slot] = { ...(profile[slot] as Record<string, unknown>), state, judgment: null };
    }
    renderPage(result({ analysis_case: "CONTROLLED_DEMO", full_model: { full_quality_profiles: [profile] } }));
    const propertyProfile = document.querySelector(".property-profile") as HTMLElement;
    expect(within(propertyProfile).getAllByText("UNKNOWN").length).toBeGreaterThan(0);
    expect(within(propertyProfile).getByText("UNAVAILABLE")).toBeTruthy();
    expect(within(propertyProfile).getByText("NOT_APPLICABLE")).toBeTruthy();
    expect(within(propertyProfile).getAllByText("No judgment value")).toHaveLength(3);
    expect(propertyProfile.textContent).not.toMatch(/(?:^|\s)0(?:\s|$)/);
  });

  it("keeps selected requirement and source/evidence text unchanged across locale switching", async () => {
    renderPage();
    fireEvent.click(screen.getByRole("button", { name: /R002/ }));
    fireEvent.click(screen.getAllByRole("button", { name: /E-R002/ })[0]);
    await i18n.changeLanguage("uk");
    expect(screen.getByRole("heading", { name: "R002" })).toBeTruthy();
    expect(screen.getByText(r2Text)).toBeTruthy();
    expect(screen.getAllByText("зберігає журнал").length).toBeGreaterThan(0);
    expect(screen.getByRole("dialog")).toBeTruthy();
  });

  it("does not mutate the canonical response through selection, tabs, evidence, or locale", async () => {
    const payload = result();
    const before = JSON.stringify(payload);
    renderPage(payload);
    fireEvent.click(screen.getByRole("button", { name: /R002/ }));
    fireEvent.click(screen.getAllByRole("button", { name: /E-R002/ })[0]);
    fireEvent.click(screen.getByRole("button", { name: "Close evidence drawer" }));
    fireEvent.click(screen.getByRole("tab", { name: "Diagnostics (0)" }));
    await i18n.changeLanguage("uk");
    expect(JSON.stringify(payload)).toBe(before);
  });

  it("renders a safe empty state for a malformed constructed requirements fixture", () => {
    renderPage(result({ requirements: [{ requirement: null }] }));
    expect(screen.getByText("No canonical requirements")).toBeTruthy();
    expect(screen.queryByRole("navigation", { name: "Canonical requirements" })).toBeNull();
  });

  it("opens Requirements through result navigation without another analysis call", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(appResponse(result()));
    const client = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
    render(<QueryClientProvider client={client}><App /></QueryClientProvider>);
    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    await screen.findByRole("heading", { name: "Overview" });
    fireEvent.click(screen.getByRole("button", { name: "Requirements" }));
    await screen.findByRole("heading", { name: "Requirements" });
    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  it("does not analyze on tab changes and a new specification clears requirement/evidence presentation state", async () => {
    const payload = result();
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(appResponse(payload));
    const client = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
    render(<QueryClientProvider client={client}><App /></QueryClientProvider>);
    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    await screen.findByRole("heading", { name: "Overview" });
    fireEvent.click(screen.getByRole("button", { name: "Requirements" }));
    fireEvent.click(screen.getByRole("button", { name: /R002/ }));
    fireEvent.click(screen.getAllByRole("button", { name: /E-R002/ })[0]);
    fireEvent.click(screen.getByRole("tab", { name: "Diagnostics (0)" }));
    expect(fetchSpy).toHaveBeenCalledTimes(1);

    fireEvent.click(screen.getByRole("button", { name: "New specification" }));
    expect(screen.queryByRole("dialog")).toBeNull();
    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement again" } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    await screen.findByRole("heading", { name: "Overview" });
    fireEvent.click(screen.getByRole("button", { name: "Requirements" }));
    expect(screen.getByRole("heading", { name: "R001" })).toBeTruthy();
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(fetchSpy).toHaveBeenCalledTimes(2);
  });
});

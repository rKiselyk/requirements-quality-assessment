import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { i18n } from "../../i18n";
import { ResultWorkspace } from "../results/ResultWorkspace";
import { AuditPage } from "./AuditPage";
import { buildEvidenceIndex } from "./evidenceIndex";
import { buildAuditGroups, isCanonicalFraction, selectAuditAvailability } from "./tree";

const sourceText = "A 😀 вимога має 2 с.";
const evidenceStart = Array.from(sourceText).findIndex((_, index, all) => all.slice(index, index + 3).join("") === "має");

function evidence(id = "E-1") {
  return {
    evidence_id: id,
    requirement_id: "R001",
    feature_id: "quantitative_constraint",
    text: "має",
    start_offset: evidenceStart,
    end_offset: evidenceStart + 3,
    rule_id: "RULE-1",
  };
}

function requirementRecord(text = sourceText, id = "E-1") {
  const recordEvidence = evidence(id);
  const start = Array.from(text).findIndex((_, index, all) => all.slice(index, index + 3).join("") === "має");
  if (start >= 0) Object.assign(recordEvidence, { start_offset: start, end_offset: start + 3 });
  return {
    requirement: { id: "R001", source_line: 7, text },
    features: {},
    evidence: [recordEvidence],
    quality_profile: {
      completeness: {
        findings: [{
          finding_id: "F-1", characteristic_id: "COMPLETENESS", kind: "ISSUE", code: "MISSING",
          rule_id: "FINDING-RULE", explanation: "Canonical finding", evidence_refs: [id],
        }],
      },
    },
    trace: null,
  };
}

function requirementRecordFor(requirementId: string, sourceLine: number, evidenceId: string, text = sourceText) {
  const record = requirementRecord(text, evidenceId);
  record.requirement.id = requirementId;
  record.requirement.source_line = sourceLine;
  record.evidence[0].requirement_id = requirementId;
  return record;
}

function artifactRef(version = "v1") {
  return { artifact_id: "SPEC", artifact_version: version };
}

function withArtifact(record: ReturnType<typeof requirementRecordFor>, version = "v1") {
  return { artifact_ref: artifactRef(version), automatic_record: record };
}

function requirementEvidenceRef(requirementId: string, sourceLine: number, evidenceId: string, version = "v1") {
  return {
    requirement_subject_ref: {
      artifact_ref: artifactRef(version),
      requirement_id: requirementId,
      source_line: sourceLine,
    },
    evidence_id: evidenceId,
  };
}

const fullModelKeys = [
  "initial_specification_assessment", "metric_profile", "criterion_binding", "observation_resolution", "conformance",
  "feature_profile", "observed_product_quality", "problem_resolutions", "defect_population", "defect_quality_relations",
  "risk_assessments", "corrective_action_resolution", "initial_specification", "revised_specification", "external_revision",
  "action_application", "reassessment", "comparisons", "process_v1", "process_v2", "process_transition",
  "full_quality_profiles", "prediction", "quantitative_risk_assessments", "checkpoint_evaluations",
] as const;

function fullModel(): Record<string, unknown> {
  return Object.fromEntries(fullModelKeys.map((key) => [key, key === "checkpoint_evaluations"
    ? [{ checkpoint_id: "CP-2" }, { checkpoint_id: "CP-1" }]
    : key === "comparisons" ? [{ comparison_kind: "INCREASED" }]
      : key === "reassessment" ? { produced_result_refs: ["REF-B", "REF-A"], produced_results: [{ id: "B" }, { id: "A" }] }
        : key === "initial_specification_assessment" ? { records: [{ extraction_result: requirementRecord() }] }
          : key === "metric_profile" ? { calibration: "PROVISIONAL", provenance: { model_id: "MODEL-1" } }
            : { status: "AVAILABLE", value: null }]));
}

function response(overrides: Partial<CanonicalAnalyzeResponse> = {}): CanonicalAnalyzeResponse {
  return {
    contract_version: "research-api-v1",
    analysis_case: "INITIAL",
    controlled_scenario: null,
    requirements: [requirementRecord()],
    specification: { snapshot_id: "SNAPSHOT-1", exact: { numerator: 2, denominator: 3 } },
    section_availability: [{ section: "audit", availability: "AVAILABLE", reason_code: null }],
    full_model: null,
    reassessment_context: null,
    limitations: ["NO_COMBINED_QUALITY_SCORE"],
    ...overrides,
  };
}

function renderAudit(value = response()) {
  return render(<AuditPage result={value} />);
}

function expandAll(container: HTMLElement) {
  let remaining = [...container.querySelectorAll<HTMLDetailsElement>("details:not([open])")];
  while (remaining.length > 0) {
    for (const detail of remaining) {
      detail.open = true;
      fireEvent(detail, new Event("toggle"));
    }
    remaining = [...container.querySelectorAll<HTMLDetailsElement>("details:not([open])")];
  }
}

describe("RUI-14 Audit availability and integration", () => {
  beforeEach(async () => { window.sessionStorage.clear(); await i18n.changeLanguage("en"); });
  afterEach(() => { cleanup(); vi.restoreAllMocks(); });

  it("requires exactly one canonical Audit availability record", () => {
    expect(selectAuditAvailability(response()).kind).toBe("AVAILABLE");
    expect(selectAuditAvailability(response({ section_availability: [] })).kind).toBe("MALFORMED");
    expect(selectAuditAvailability(response({ section_availability: [
      { section: "audit", availability: "AVAILABLE" }, { section: "audit", availability: "AVAILABLE" },
    ] })).kind).toBe("MALFORMED");
  });

  it("renders an unavailable state with the exact reason and no fabricated tree", () => {
    renderAudit(response({ section_availability: [{ section: "audit", availability: "UNAVAILABLE", reason_code: "FUTURE_AUDIT_REASON" }] }));
    expect(screen.getByText("FUTURE_AUDIT_REASON")).toBeTruthy();
    expect(document.querySelector(".audit-tree")).toBeNull();
  });

  it("accepts only canonical AVAILABLE plus null reason", () => {
    expect(selectAuditAvailability(response({ section_availability: [{ section: "audit", availability: "AVAILABLE", reason_code: null }] }))).toEqual({ kind: "AVAILABLE" });
    expect(selectAuditAvailability(response({ section_availability: [{ section: "audit", availability: "AVAILABLE", reason_code: "CONTRADICTORY" }] })).kind).toBe("MALFORMED");
  });

  it("accepts only canonical UNAVAILABLE plus a non-empty reason", () => {
    expect(selectAuditAvailability(response({ section_availability: [{ section: "audit", availability: "UNAVAILABLE", reason_code: "EXACT_REASON" }] }))).toEqual({ kind: "UNAVAILABLE", reasonCode: "EXACT_REASON" });
    expect(selectAuditAvailability(response({ section_availability: [{ section: "audit", availability: "UNAVAILABLE", reason_code: null }] })).kind).toBe("MALFORMED");
    expect(selectAuditAvailability(response({ section_availability: [{ section: "audit", availability: "UNAVAILABLE", reason_code: "" }] })).kind).toBe("MALFORMED");
    expect(selectAuditAvailability(response({ section_availability: [{ section: "audit", availability: "UNAVAILABLE", reason_code: "   " }] })).kind).toBe("MALFORMED");
    expect(selectAuditAvailability(response({ section_availability: [{ section: "audit", availability: "UNAVAILABLE", reason_code: 7 }] })).kind).toBe("MALFORMED");
  });

  it("routes Audit to the real page without making an Analyze request", () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    render(<ResultWorkspace result={response()} activeView="audit" selectedRequirementId={null} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Full Model Audit" })).toBeTruthy();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("switches locale without analysis and preserves canonical identities", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const view = renderAudit(response());
    expect(screen.getByText("research-api-v1")).toBeTruthy();
    await i18n.changeLanguage("uk");
    view.rerender(<AuditPage result={response()} />);
    expandAll(view.container);
    expect(screen.getByRole("heading", { name: "Аудит повної моделі" })).toBeTruthy();
    expect(screen.getByText("research-api-v1")).toBeTruthy();
    expect(screen.getByText("NO_COMBINED_QUALITY_SCORE")).toBeTruthy();
    expect(fetchSpy).not.toHaveBeenCalled();
  });
});

describe("RUI-14 INITIAL and response coverage", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(cleanup);

  it("renders INITIAL requirement records, specification assessment, metadata, and limitations", () => {
    const view = renderAudit(); expandAll(view.container);
    expect(screen.getByText("Requirement records")).toBeTruthy();
    expect(screen.getByText("Specification assessment")).toBeTruthy();
    expect(screen.getByText("INITIAL")).toBeTruthy();
    expect(screen.getByText("SNAPSHOT-1")).toBeTruthy();
    expect(screen.getByText("NO_COMBINED_QUALITY_SCORE")).toBeTruthy();
  });

  it("shows full_model null neutrally and fabricates no downstream records", () => {
    const view = renderAudit(); expandAll(view.container);
    const fullModelNode = view.container.querySelector('[data-audit-path="$.full_model"]');
    expect(fullModelNode?.textContent).toContain("null");
    expect(view.container.querySelector('[data-audit-path="$.full_model.risk_assessments"]')).toBeNull();
    expect(view.container.querySelector('[data-audit-path="$.full_model.reassessment"]')).toBeNull();
  });

  it("represents all accepted top-level response fields exactly once", () => {
    const groups = buildAuditGroups(response());
    const responseKeys = groups.flatMap((group) => group.canonicalKey ? [group.canonicalKey] : Object.keys(group.value as object));
    expect(responseKeys).toEqual([
      "contract_version", "analysis_case", "controlled_scenario", "section_availability", "reassessment_context", "limitations",
      "requirements", "specification", "full_model",
    ]);
    expect(new Set(responseKeys).size).toBe(responseKeys.length);
  });
});

describe("RUI-14 generic AuditTree preservation", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(cleanup);

  it("renders nested objects as accessible expandable details", () => {
    const view = renderAudit(response({ specification: { outer: { inner: "VALUE" } } }));
    expandAll(view.container);
    const outer = view.container.querySelector('[data-audit-path="$.specification.outer"]');
    expect(outer?.tagName).toBe("DETAILS");
    expect(outer?.querySelector("summary")?.getAttribute("aria-label")).toContain("outer");
  });

  it("preserves object field order and array order with explicit indexes", () => {
    const value = response({ specification: { zebra: "first", alpha: "second", ordered: ["B", "A", "B"] } });
    const groups = buildAuditGroups(value);
    expect(Object.keys((groups[1].value as Record<string, unknown>).specification as object)).toEqual(["zebra", "alpha", "ordered"]);
    const view = renderAudit(value); expandAll(view.container);
    expect([...view.container.querySelectorAll('[data-audit-path]')].filter((node) => node.getAttribute("data-audit-path")?.startsWith("$.specification.ordered[")).map((node) => node.textContent)).toEqual([
      expect.stringContaining("[0]"), expect.stringContaining("[1]"), expect.stringContaining("[2]"),
    ]);
    expect(view.container.querySelector('[data-audit-path="$.specification.ordered[0]"]')?.textContent).toContain("B");
    expect(view.container.querySelector('[data-audit-path="$.specification.ordered[1]"]')?.textContent).toContain("A");
  });

  it("keeps null, zero, false, and empty string distinct", () => {
    const view = renderAudit(response({ specification: { nullish: null, zero: 0, disabled: false, blank: "" } })); expandAll(view.container);
    expect(view.container.querySelector('[data-audit-path="$.specification.nullish"]')?.textContent).toContain("null");
    expect(view.container.querySelector('[data-audit-path="$.specification.zero"]')?.textContent).toContain("0");
    expect(view.container.querySelector('[data-audit-path="$.specification.disabled"]')?.textContent).toContain("false");
    expect(view.container.querySelector('[data-audit-path="$.specification.blank"]')?.textContent).toContain('"" (empty string)');
  });

  it("keeps empty arrays and empty objects distinct with zero counts", () => {
    const view = renderAudit(response({ specification: { empty_array: [], empty_object: {} } })); expandAll(view.container);
    expect(view.container.querySelector('[data-audit-path="$.specification.empty_array"]')?.textContent).toContain("Array0 items");
    expect(view.container.querySelector('[data-audit-path="$.specification.empty_object"]')?.textContent).toContain("Object0 fields");
  });

  it("renders an unsupported constructed value locally without dropping neighbors", () => {
    const value = response({ specification: { before: "BEFORE", unsupported: () => undefined, after: "AFTER" } });
    const view = renderAudit(value); expandAll(view.container);
    expect(screen.getByText("BEFORE")).toBeTruthy();
    expect(screen.getByText("AFTER")).toBeTruthy();
    expect(view.container.querySelector('[data-audit-path="$.specification.unsupported"]')?.textContent).toContain("Unsupported transport value");
  });

  it("keeps a reporter-looking string as one string leaf", () => {
    const reporter = "AUDIT REPORT\nRisk: AVAILABLE\nCheckpoint: SATISFIED";
    const view = renderAudit(response({ specification: { arbitrary_text: reporter } })); expandAll(view.container);
    const node = view.container.querySelector('[data-audit-path="$.specification.arbitrary_text"]');
    expect(node?.querySelectorAll(".audit-node")).toHaveLength(0);
    expect(node?.textContent).toContain(reporter);
  });
});

describe("RUI-14 exact values and Full Model coverage", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(cleanup);

  it("recognizes only the exact canonical Fraction shape", () => {
    expect(isCanonicalFraction({ numerator: 2, denominator: 3 })).toBe(true);
    expect(isCanonicalFraction({ denominator: 3, numerator: 2 })).toBe(true);
    expect(isCanonicalFraction({ numerator: 2, denominator: 3, rounded: 0.67 })).toBe(false);
  });

  it("renders positive and negative Fractions exactly without decimal conversion while retaining both fields", () => {
    const view = renderAudit(response({ specification: { positive: { numerator: 2, denominator: 3 }, negative: { numerator: -1, denominator: 4 } } })); expandAll(view.container);
    expect(screen.getByText("2/3")).toBeTruthy();
    expect(screen.getByText("-1/4")).toBeTruthy();
    expect(screen.queryByText("0.6666666666666666")).toBeNull();
    expect(view.container.querySelector('[data-audit-path="$.specification.positive.numerator"]')?.textContent).toContain("2");
    expect(view.container.querySelector('[data-audit-path="$.specification.positive.denominator"]')?.textContent).toContain("3");
  });

  it("keeps numeric-looking and Decimal-like strings as exact strings", () => {
    const view = renderAudit(response({ specification: { numeric: "001.2300", decimal: "0.333333333333333333" } })); expandAll(view.container);
    expect(view.container.querySelector('[data-audit-path="$.specification.numeric"]')?.textContent).toContain("string001.2300");
    expect(screen.getByText("0.333333333333333333")).toBeTruthy();
  });

  it("renders every actual Full Model own key including a future field", () => {
    const model = fullModel(); model.future_structured_field = { future_nested_field: "EXACT-FUTURE" };
    const view = renderAudit(response({ analysis_case: "CONTROLLED_DEMO", full_model: model })); expandAll(view.container);
    for (const key of Object.keys(model)) expect(view.container.querySelector(`[data-audit-path="$.full_model.${key}"]`)).not.toBeNull();
    expect(screen.getByText("EXACT-FUTURE")).toBeTruthy();
  });

  it("keeps distinct Full Model families and lifecycle records separate", () => {
    const view = renderAudit(response({ analysis_case: "CONTROLLED_DEMO", full_model: fullModel() })); expandAll(view.container);
    for (const key of [
      "criterion_binding", "observation_resolution", "conformance", "feature_profile", "observed_product_quality", "prediction",
      "risk_assessments", "quantitative_risk_assessments", "corrective_action_resolution", "external_revision", "action_application",
      "process_v1", "process_v2", "process_transition",
    ]) expect(view.container.querySelector(`[data-audit-path="$.full_model.${key}"]`)).not.toBeNull();
  });

  it("preserves checkpoint order, calibration, provenance, and omits report_bundle reconstruction", () => {
    const view = renderAudit(response({ analysis_case: "CONTROLLED_DEMO", full_model: fullModel() })); expandAll(view.container);
    expect(view.container.querySelector('[data-audit-path="$.full_model.checkpoint_evaluations[0].checkpoint_id"]')?.textContent).toContain("CP-2");
    expect(view.container.querySelector('[data-audit-path="$.full_model.checkpoint_evaluations[1].checkpoint_id"]')?.textContent).toContain("CP-1");
    expect(screen.getByText("PROVISIONAL")).toBeTruthy();
    expect(screen.getByText("MODEL-1")).toBeTruthy();
    expect(view.container.querySelector('[data-audit-path="$.full_model.report_bundle"]')).toBeNull();
  });
});

describe("RUI-14 reassessment trace", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(cleanup);

  it("keeps current top-level assessment, historical initial assessment, reassessment, comparison, and context distinct", () => {
    const model = fullModel();
    const value = response({
      analysis_case: "REASSESSMENT",
      requirements: [{ requirement: { id: "CURRENT-R" }, evidence: [] }],
      specification: { snapshot_id: "CURRENT-SPEC" },
      full_model: model,
      reassessment_context: { context_digest: "sha256:verbatim", prior: "PRIOR" },
    });
    const view = renderAudit(value); expandAll(view.container);
    expect(view.container.querySelector('[data-audit-path="$.requirements"]')?.textContent).toContain("CURRENT-R");
    expect(view.container.querySelector('[data-audit-path="$.full_model.initial_specification_assessment"]')).not.toBeNull();
    expect(view.container.querySelector('[data-audit-path="$.full_model.reassessment"]')).not.toBeNull();
    expect(view.container.querySelector('[data-audit-path="$.full_model.comparisons"]')?.textContent).toContain("INCREASED");
    expect(screen.getByText("sha256:verbatim")).toBeTruthy();
    expect(screen.queryByText(/improved|worsened/i)).toBeNull();
  });

  it("preserves produced refs and results order literally", () => {
    const view = renderAudit(response({ analysis_case: "REASSESSMENT", full_model: fullModel() })); expandAll(view.container);
    expect(view.container.querySelector('[data-audit-path="$.full_model.reassessment.produced_result_refs[0]"]')?.textContent).toContain("REF-B");
    expect(view.container.querySelector('[data-audit-path="$.full_model.reassessment.produced_results[0].id"]')?.textContent).toContain("B");
  });

  it("does not add dedicated Reassessment or Comparison result navigation", () => {
    expect(document.body.textContent).not.toContain("n/a");
    const value = response({ analysis_case: "REASSESSMENT", full_model: fullModel() });
    render(<ResultWorkspace result={value} activeView="audit" selectedRequirementId={null} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Full Model Audit" })).toBeTruthy();
  });
});

describe("RUI-14 EvidenceDrawer resolution", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(() => { cleanup(); vi.restoreAllMocks(); });

  it("indexes a complete Evidence object with Unicode code-point offsets and linked findings", () => {
    const record = requirementRecord();
    const index = buildEvidenceIndex({ record });
    const target = index.resolve(record.evidence[0], "evidence");
    expect(target?.evidence.text).toBe("має");
    expect(target?.evidence.startOffset).toBe(evidenceStart);
    expect(target?.sourceLine).toBe(7);
    expect(target?.linkedFindings.map((item) => item.findingId)).toEqual(["F-1"]);
  });

  it("resolves a canonical CrossEvidenceRef only when its requirement and evidence identity is unique", () => {
    const first = requirementRecordFor("R001", 2, "SHARED");
    const second = requirementRecordFor("R002", 4, "SHARED");
    const index = buildEvidenceIndex({ first, second });
    expect(index.resolve({ requirement_id: "R002", evidence_id: "SHARED" }, "evidence_refs")?.sourceLine).toBe(4);
    expect(index.resolve("SHARED", "evidence_refs")).toBeNull();
  });

  it("keeps the same CrossEvidenceRef ambiguous across v1 and v2", () => {
    const v1 = requirementRecordFor("R001", 2, "SHARED");
    const v2 = requirementRecordFor("R001", 2, "SHARED");
    const index = buildEvidenceIndex({ v1: withArtifact(v1, "v1"), v2: withArtifact(v2, "v2") });
    expect(index.resolve({ requirement_id: "R001", evidence_id: "SHARED" }, "evidence_refs")).toBeNull();
  });

  it("resolves canonical RequirementEvidenceRef through its nested subject", () => {
    const first = requirementRecordFor("R001", 2, "SHARED");
    const second = requirementRecordFor("R002", 2, "SHARED");
    const index = buildEvidenceIndex({ first: withArtifact(first), second: withArtifact(second) });
    expect(index.resolve(requirementEvidenceRef("R002", 2, "SHARED"), "evidence_ref")?.evidence.requirementId).toBe("R002");
  });

  it("uses RequirementEvidenceRef source_line to narrow otherwise matching candidates", () => {
    const line2 = requirementRecordFor("R001", 2, "SHARED");
    const line9 = requirementRecordFor("R001", 9, "SHARED");
    const index = buildEvidenceIndex({ line2: withArtifact(line2), line9: withArtifact(line9) });
    expect(index.resolve(requirementEvidenceRef("R001", 9, "SHARED"), "evidence_ref")?.sourceLine).toBe(9);
  });

  it("rejects malformed nested requirement subjects", () => {
    const record = requirementRecordFor("R001", 2, "E-1");
    const index = buildEvidenceIndex({ record: withArtifact(record) });
    expect(index.resolve({ requirement_subject_ref: { requirement_id: "R001", source_line: 2 }, evidence_id: "E-1" }, "evidence_ref")).toBeNull();
    expect(index.resolve({ requirement_subject_ref: { artifact_ref: {}, requirement_id: "R001", source_line: 0 }, evidence_id: "E-1" }, "evidence_ref")).toBeNull();
  });

  it("keeps a still-ambiguous RequirementEvidenceRef technical only", () => {
    const v1 = requirementRecordFor("R001", 2, "SHARED");
    const alternate = requirementRecordFor("R001", 2, "SHARED", "Інша має вимога.");
    const index = buildEvidenceIndex({ v1: withArtifact(v1), alternate: withArtifact(alternate) });
    expect(index.resolve(requirementEvidenceRef("R001", 2, "SHARED"), "evidence_ref")).toBeNull();
  });

  it.each([
    "evidence_refs", "ordered_evidence_refs", "ordered_cross_evidence_refs", "direct_criterion_evidence_refs",
    "source_component_refs", "metric_evidence_refs", "comparator_evidence_refs", "value_evidence_refs",
    "unit_evidence_refs", "context_evidence_refs", "matched_context_evidence_ref", "ref",
  ])(
    "%s resolves an unambiguous CrossEvidenceRef",
    (fieldKey) => {
      const record = requirementRecordFor("R001", 2, "E-1");
      const index = buildEvidenceIndex({ record });
      expect(index.resolve({ requirement_id: "R001", evidence_id: "E-1" }, fieldKey)?.evidence.evidenceId).toBe("E-1");
    },
  );

  it("source_evidence_refs independently resolves CrossEvidenceRef and RequirementEvidenceRef shapes", () => {
    const record = requirementRecordFor("R001", 2, "E-1");
    const index = buildEvidenceIndex({ profile: withArtifact(record) });
    expect(index.resolve({ requirement_id: "R001", evidence_id: "E-1" }, "source_evidence_refs")?.evidence.evidenceId).toBe("E-1");
    expect(index.resolve(requirementEvidenceRef("R001", 2, "E-1"), "source_evidence_refs")?.artifactRef).toEqual({ artifactId: "SPEC", artifactVersion: "v1" });
  });

  it("exposes drawer actions at actual CrossEvidenceRef field locations without replacing raw refs", () => {
    const model = fullModel();
    model.initial_specification_assessment = { records: [] };
    model.criterion_binding = {
      provenance: {
        direct_criterion_evidence_refs: [{ requirement_id: "R001", evidence_id: "E-1" }],
        source_component_refs: [{ requirement_id: "R001", evidence_id: "E-1" }],
      },
    };
    const view = renderAudit(response({ analysis_case: "CONTROLLED_DEMO", full_model: model })); expandAll(view.container);
    for (const path of [
      "$.full_model.criterion_binding.provenance.direct_criterion_evidence_refs[0]",
      "$.full_model.criterion_binding.provenance.source_component_refs[0]",
    ]) {
      const node = view.container.querySelector(`[data-audit-path="${path}"]`);
      expect(node?.textContent).toContain("R001");
      expect(node?.textContent).toContain("E-1");
      expect(node?.querySelector(".audit-evidence-action")).not.toBeNull();
    }
  });

  it.each(["diagnostic_ref", "diagnostic_refs", "observation_ref", "observation_refs", "criterion_ref", "criterion_refs", "process_ref", "dynamic_observation_ref", "arbitrary_refs"])(
    "does not route unrelated %s values to base Evidence",
    (fieldKey) => {
      const record = requirementRecordFor("R001", 2, "E-1");
      const index = buildEvidenceIndex({ record });
      expect(index.resolve({ requirement_id: "R001", evidence_id: "E-1" }, fieldKey)).toBeNull();
    },
  );

  it("shape-gates source_evidence_ref to a canonical structured base Evidence identity", () => {
    const record = requirementRecordFor("R001", 2, "E-1");
    const index = buildEvidenceIndex({ record });
    expect(index.resolve({ requirement_id: "R001", evidence_id: "E-1" }, "source_evidence_ref")?.evidence.evidenceId).toBe("E-1");
    expect(index.resolve("E-1", "source_evidence_ref")).toBeNull();
    expect(index.resolve({ observation_id: "E-1", evidence_id: "E-1" }, "source_evidence_ref")).toBeNull();
    expect(index.resolve({ requirement_id: "R001", evidence_id: "E-1", observation_id: "OTHER-TYPE" }, "source_evidence_ref")).toBeNull();
  });

  it("leaves dangling canonical reference shapes non-interactive", () => {
    const index = buildEvidenceIndex({ record: requirementRecordFor("R001", 2, "E-1") });
    expect(index.resolve({ requirement_id: "R001", evidence_id: "MISSING" }, "direct_criterion_evidence_refs")).toBeNull();
    expect(index.resolve(requirementEvidenceRef("R001", 2, "MISSING"), "evidence_ref")).toBeNull();
  });

  it("uses canonical artifact identity to keep v1 and v2 candidates distinct", () => {
    const v1 = requirementRecordFor("R001", 2, "SHARED");
    const v2 = structuredClone(v1);
    const root = {
      initial_specification: { artifact_ref: artifactRef("v1") },
      initial_specification_assessment: { records: [{ extraction_result: v1 }] },
      reassessment: {
        produced_results: [{
          specification_version: { artifact_ref: artifactRef("v2") },
          requirement_records: [v2],
        }],
      },
    };
    const index = buildEvidenceIndex(root);
    expect(index.resolve(requirementEvidenceRef("R001", 2, "SHARED", "v1"), "source_evidence_refs")?.artifactRef).toEqual({ artifactId: "SPEC", artifactVersion: "v1" });
    expect(index.resolve(requirementEvidenceRef("R001", 2, "SHARED", "v2"), "source_evidence_refs")?.artifactRef).toEqual({ artifactId: "SPEC", artifactVersion: "v2" });
    expect(index.resolve({ requirement_id: "R001", evidence_id: "SHARED" }, "evidence_refs")).toBeNull();
  });

  it("deduplicates repeated projections of the same complete artifact/source identity for lookup only", () => {
    const first = requirementRecordFor("R001", 2, "SHARED");
    const repeated = structuredClone(first);
    const root = {
      full_model: {
        initial_specification: { artifact_ref: artifactRef("v1") },
        initial_specification_assessment: { records: [{ extraction_result: first }] },
      },
      reassessment_context: {
        initial_specification: { artifact_ref: artifactRef("v1") },
        initial_specification_assessment: { records: [{ extraction_result: repeated }] },
      },
    };
    const index = buildEvidenceIndex(root);
    expect(index.resolve(requirementEvidenceRef("R001", 2, "SHARED", "v1"), "source_evidence_refs")).not.toBeNull();
    expect(index.resolve({ requirement_id: "R001", evidence_id: "SHARED" }, "evidence_refs")).not.toBeNull();
    expect(index.resolve(first.evidence[0], "evidence")).not.toBeNull();
    expect(index.resolve(repeated.evidence[0], "evidence")).not.toBeNull();
  });

  it("does not assign an artifact to a candidate without directly provable artifact context", () => {
    const record = requirementRecordFor("R001", 2, "E-1");
    const target = buildEvidenceIndex({ record }).resolve(record.evidence[0], "evidence");
    expect(target?.artifactRef).toBeNull();
    expect(buildEvidenceIndex({ record }).resolve(requirementEvidenceRef("R001", 2, "E-1"), "source_evidence_refs")).toBeNull();
  });

  it("rejects malformed RequirementEvidenceRef artifact identity", () => {
    const record = requirementRecordFor("R001", 2, "E-1");
    const index = buildEvidenceIndex({ profile: withArtifact(record) });
    const malformed = requirementEvidenceRef("R001", 2, "E-1");
    malformed.requirement_subject_ref.artifact_ref.artifact_version = "";
    expect(index.resolve(malformed, "source_evidence_refs")).toBeNull();
  });

  it("handles a realistic repeated lifecycle transport without changing raw Audit occurrences", () => {
    const v1 = requirementRecordFor("R001", 2, "LIFECYCLE-E");
    const repeatedV1 = structuredClone(v1);
    const v2 = structuredClone(v1);
    const v1Ref = requirementEvidenceRef("R001", 2, "LIFECYCLE-E", "v1");
    const v2Ref = requirementEvidenceRef("R001", 2, "LIFECYCLE-E", "v2");
    const crossRef = { requirement_id: "R001", evidence_id: "LIFECYCLE-E" };
    const model = fullModel();
    Object.assign(model, {
      initial_specification: { artifact_ref: artifactRef("v1") },
      initial_specification_assessment: { records: [{ extraction_result: v1 }] },
      metric_profile: { artifact_ref: artifactRef("v1"), provenance: { source_evidence_refs: [v1Ref] } },
      observed_product_quality: { provenance: { source_evidence_refs: [v1Ref, v2Ref] } },
      observation_resolution: {
        snapshot_observation_manifest: {
          metric_evidence_refs: [crossRef], comparator_evidence_refs: [crossRef], value_evidence_refs: [crossRef],
          unit_evidence_refs: [crossRef], context_evidence_refs: [crossRef], evidence_refs: [crossRef],
        },
      },
      reassessment: {
        produced_results: [{ specification_version: { artifact_ref: artifactRef("v2") }, requirement_records: [v2] }],
      },
    });
    const value = response({
      analysis_case: "REASSESSMENT",
      requirements: [structuredClone(v2)],
      full_model: model,
      reassessment_context: {
        initial_specification: { artifact_ref: artifactRef("v1") },
        initial_specification_assessment: { records: [{ extraction_result: repeatedV1 }] },
      },
    });
    const index = buildEvidenceIndex(value);
    expect(index.resolve(v1Ref, "source_evidence_refs")?.artifactRef?.artifactVersion).toBe("v1");
    expect(index.resolve(v2Ref, "source_evidence_refs")?.artifactRef?.artifactVersion).toBe("v2");
    expect(index.resolve(crossRef, "metric_evidence_refs")).toBeNull();

    const view = renderAudit(value); expandAll(view.container);
    for (const path of [
      "$.requirements[0].evidence[0]",
      "$.full_model.initial_specification_assessment.records[0].extraction_result.evidence[0]",
      "$.full_model.reassessment.produced_results[0].requirement_records[0].evidence[0]",
      "$.reassessment_context.initial_specification_assessment.records[0].extraction_result.evidence[0]",
    ]) expect(view.container.querySelector(`[data-audit-path="${path}"]`)).not.toBeNull();

    const v1Node = view.container.querySelector('[data-audit-path="$.full_model.metric_profile.provenance.source_evidence_refs[0]"]');
    const v2Node = view.container.querySelector('[data-audit-path="$.full_model.observed_product_quality.provenance.source_evidence_refs[1]"]');
    const ambiguousNode = view.container.querySelector('[data-audit-path="$.full_model.observation_resolution.snapshot_observation_manifest.metric_evidence_refs[0]"]');
    expect(v1Node?.querySelector(".audit-evidence-action")).not.toBeNull();
    expect(v2Node?.querySelector(".audit-evidence-action")).not.toBeNull();
    expect(ambiguousNode?.querySelector(".audit-evidence-action")).toBeNull();
    fireEvent.click(v1Node?.querySelector(".audit-evidence-action") as HTMLButtonElement);
    expect(screen.getByRole("dialog")).toBeTruthy();
  });

  it("rejects a mismatched source slice instead of creating a drawer target", () => {
    const record = requirementRecord("Different source");
    expect(buildEvidenceIndex({ record }).resolve(record.evidence[0], "evidence")).toBeNull();
  });

  it("does not shift offsets when a non-BMP character precedes Evidence", () => {
    const record = requirementRecord();
    const target = buildEvidenceIndex({ record }).resolve(record.evidence[0], "evidence");
    expect(target?.evidence.startOffset).toBe(evidenceStart);
    expect(sourceText.slice(target?.evidence.startOffset, target?.evidence.endOffset)).not.toBe("має");
  });

  it("resolves historical and current full Evidence objects to their own source contexts", () => {
    const v1 = requirementRecord(sourceText, "SHARED");
    const v2Text = "Нова вимога має результат.";
    const v2 = requirementRecord(v2Text, "SHARED");
    const start = Array.from(v2Text).findIndex((_, index, all) => all.slice(index, index + 3).join("") === "має");
    Object.assign(v2.evidence[0], { start_offset: start, end_offset: start + 3 });
    const index = buildEvidenceIndex({ initial: { extraction_result: v1 }, reassessment: { extraction_result: v2 } });
    expect(index.resolve(v1.evidence[0], "evidence")?.requirementText).toBe(sourceText);
    expect(index.resolve(v2.evidence[0], "evidence")?.requirementText).toBe(v2Text);
    expect(index.resolve("SHARED", "evidence_ref")).toBeNull();
  });

  it("keeps ambiguous, dangling, and dynamic references as technical values only", () => {
    const v1 = requirementRecord(sourceText, "SHARED");
    const v2 = requirementRecord(sourceText.replace("2", "3"), "SHARED");
    const index = buildEvidenceIndex({ v1, v2 });
    expect(index.resolve("SHARED", "evidence_ref")).toBeNull();
    expect(index.resolve("MISSING", "evidence_ref")).toBeNull();
    expect(index.resolve("E-1", "dynamic_evidence_ref")).toBeNull();
  });

  it("does not collapse identical evidence occurrences from distinct lifecycle contexts", () => {
    const v1 = requirementRecord(sourceText, "SAME");
    const v2 = structuredClone(v1);
    const index = buildEvidenceIndex({ v1: withArtifact(v1, "v1"), v2: withArtifact(v2, "v2") });
    expect(index.resolve("SAME", "evidence_ref")).toBeNull();
    expect(index.resolve(v1.evidence[0], "evidence")).not.toBeNull();
    expect(index.resolve(v2.evidence[0], "evidence")).not.toBeNull();
  });

  it("opens the existing EvidenceDrawer, displays canonical data, and restores trigger focus on close", () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const view = renderAudit(); expandAll(view.container);
    const trigger = screen.getAllByRole("button", { name: /Open evidence/ })[0];
    fireEvent.click(trigger);
    const dialog = screen.getByRole("dialog");
    expect(within(dialog).getByText("має")).toBeTruthy();
    expect(within(dialog).getByText(String(evidenceStart))).toBeTruthy();
    expect(within(dialog).getByText(String(evidenceStart + 3))).toBeTruthy();
    expect(within(dialog).getByText("R001")).toBeTruthy();
    expect(within(dialog).getByText("7")).toBeTruthy();
    fireEvent.click(within(dialog).getByRole("button", { name: "Close evidence drawer" }));
    expect(document.activeElement).toBe(trigger);
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("closes through the existing drawer Escape behavior", () => {
    const view = renderAudit(); expandAll(view.container);
    fireEvent.click(screen.getAllByRole("button", { name: /Open evidence/ })[0]);
    expect(screen.getByRole("dialog")).toBeTruthy();
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  it("does not translate canonical source, evidence, IDs, codes, or rules", async () => {
    const view = renderAudit(); expandAll(view.container);
    await i18n.changeLanguage("uk");
    view.rerender(<AuditPage result={response()} />); expandAll(view.container);
    expect(screen.getByText(sourceText)).toBeTruthy();
    expect(screen.getAllByText("має").length).toBeGreaterThan(0);
    expect(screen.getAllByText("R001").length).toBeGreaterThan(0);
    expect(screen.getAllByText("RULE-1").length).toBeGreaterThan(0);
  });
});

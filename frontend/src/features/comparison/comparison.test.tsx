import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { i18n } from "../../i18n";
import { lifecycleFixture } from "../reassessment/testFixture";
import { ComparisonPage } from "./ComparisonPage";
import { selectComparisonProjection } from "./projection";

function full(response: any) { return response.full_model as Record<string, any>; }
function comparisons(response: any) { return full(response).comparisons as Array<Record<string, any>>; }
function syncComparisons(response: any) {
  response.reassessment_context.comparisons = structuredClone(comparisons(response));
}

describe("RUI-15 canonical ResultComparison presentation", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(cleanup);

  it("preserves canonical comparison order and current families", () => {
    expect(selectComparisonProjection(lifecycleFixture())?.comparisons.map((item) => item.family)).toEqual(["QB_CONSISTENCY", "CONFIRMED_PROBLEM", "BOUNDED_RISK", "PRODUCT_QUALITY"]);
  });

  it.each([
    ["rule", (r: any) => { r.full_model.comparisons[0].rule_ref.rule_id = "OTHER"; }],
    ["available kind", (r: any) => { r.full_model.comparisons[0].comparison_kind = null; }],
    ["reason", (r: any) => { r.full_model.comparisons[0].reason_codes = ["FABRICATED"]; }],
    ["before artifact", (r: any) => { r.full_model.comparisons[0].before_result_ref.artifact_ref.artifact_version = "v2"; }],
    ["non-claim", (r: any) => { r.full_model.comparisons[0].non_claims.pop(); }],
  ])("fails closed for malformed %s", (_label, mutate) => {
    const response = structuredClone(lifecycleFixture());
    mutate(response);
    expect(selectComparisonProjection(response)).toBeNull();
  });

  it("does not recalculate kind when exact values change", () => {
    const response: any = lifecycleFixture();
    (response.full_model as any).comparisons[0].before_state_and_value.exact_value = { numerator: 50, denominator: 1 };
    (response.full_model as any).comparisons[0].after_state_and_value.exact_value = { numerator: 1, denominator: 50 };
    syncComparisons(response);
    expect(selectComparisonProjection(response)?.comparisons[0].kind).toBe("INCREASED");
  });

  it("renders exact values, kinds, reasons, calibration, claims, non-claims, and visible causality limits", () => {
    render(<ComparisonPage result={lifecycleFixture()} />);
    expect(screen.getAllByText("INCREASED").length).toBeGreaterThan(0);
    expect(screen.getByText("EXACT_VALUE_INCREASED")).toBeTruthy();
    expect(screen.getAllByText("PROVISIONAL_NOT_CALIBRATED").length).toBeGreaterThan(0);
    expect(screen.getAllByText("STRUCTURED_CHANGE_ONLY").length).toBe(4);
    expect(screen.getAllByText("NO_CAUSAL_EFFECT_INFERENCE").length).toBe(4);
    expect(screen.getByText(/does not prove that the corrective action caused/i)).toBeTruthy();
    expect(screen.queryByText(/^Action effectiveness$|^Risk improved$|^Worsened$/i)).toBeNull();
  });

  it("keeps comparable-ref family separate from scientific subject family", () => {
    const projected = selectComparisonProjection(lifecycleFixture());
    expect(projected?.comparisons[0].beforeResultRef?.result_family).toBe("FULL-MODEL-SERVICE-COMPARABLE");
    expect(projected?.comparisons[0].afterResultRef?.result_family).toBe("FULL-MODEL-SERVICE-COMPARABLE");
    expect(projected?.comparisons[0].family).toBe("QB_CONSISTENCY");
  });

  it.each([
    ["request ref", (item: any) => { item.provenance[0].comparison_id = "OTHER"; }],
    ["transition", (item: any) => { item.provenance[1] = { transition_instance_id: "OTHER" }; }],
    ["before ref", (item: any) => { item.provenance[2] = { result_family: "OTHER" }; }],
    ["after ref", (item: any) => { item.provenance[3] = { result_family: "OTHER" }; }],
    ["compatibility order", (item: any) => { [item.provenance[4], item.provenance[5]] = [item.provenance[5], item.provenance[4]]; }],
    ["final rule", (item: any) => { item.provenance[item.provenance.length - 1] = { rule_id: "OTHER" }; }],
  ])("fails closed for %s provenance mismatch", (_label, mutate) => {
    const response: any = lifecycleFixture();
    const item = _label === "compatibility order" ? comparisons(response)[1] : comparisons(response)[0];
    mutate(item);
    syncComparisons(response);
    expect(selectComparisonProjection(response)).toBeNull();
  });

  it("requires the canonical non-claim order exactly", () => {
    const response: any = lifecycleFixture();
    comparisons(response)[0].non_claims.reverse();
    syncComparisons(response);
    expect(selectComparisonProjection(response)).toBeNull();
  });

  it("preserves parameter refs, compatibility refs, calibration, and provenance order", () => {
    const projected = selectComparisonProjection(lifecycleFixture())?.comparisons[1];
    expect(projected?.parameterSetRefs).toEqual([{ parameter_set_id: "PARAMETERS-A" }, { parameter_set_id: "PARAMETERS-B" }]);
    expect(projected?.compatibilityDeclarationRefs).toEqual(["DECLARATION-A", "DECLARATION-B"]);
    expect(projected?.calibrationStatus).toBe("PROVISIONAL_NOT_CALIBRATED");
    expect(projected?.provenance[4]).toBe("DECLARATION-A");
    expect(projected?.provenance[5]).toBe("DECLARATION-B");
  });

  it("accepts NOT_COMPARABLE as an AVAILABLE canonical conclusion", () => {
    const response: any = lifecycleFixture();
    comparisons(response)[0].comparison_kind = "NOT_COMPARABLE";
    comparisons(response)[0].reason_codes = ["RULE_SEMANTICS_INCOMPATIBLE"];
    syncComparisons(response);
    expect(selectComparisonProjection(response)?.comparisons[0]).toMatchObject({ status: "AVAILABLE", kind: "NOT_COMPARABLE" });
  });

  it("rejects a non-AVAILABLE comparison carrying a kind", () => {
    const response: any = lifecycleFixture();
    comparisons(response)[0].status = "UNAVAILABLE";
    syncComparisons(response);
    expect(selectComparisonProjection(response)).toBeNull();
  });

  it("does not synthesize quantitative-risk, action-effectiveness, or C/V/U comparisons", () => {
    const families = selectComparisonProjection(lifecycleFixture())?.comparisons.map((item) => item.family);
    expect(families).toEqual(["QB_CONSISTENCY", "CONFIRMED_PROBLEM", "BOUNDED_RISK", "PRODUCT_QUALITY"]);
    expect(families).not.toContain("QUANTITATIVE_RISK");
    expect(families).not.toContain("ACTION_EFFECTIVENESS");
    expect(families).not.toContain("REQUIREMENT_METRIC");
    expect(families).not.toContain("SPECIFICATION_METRIC");
  });

  it("renders Ukrainian labels while preserving canonical kinds, reasons, and all non-claims", async () => {
    await i18n.changeLanguage("uk");
    render(<ComparisonPage result={lifecycleFixture()} />);
    expect(screen.getByRole("heading", { name: "Порівняння" })).toBeTruthy();
    expect(screen.getAllByText("INCREASED").length).toBeGreaterThan(0);
    expect(screen.getByText("EXACT_VALUE_INCREASED")).toBeTruthy();
    for (const code of ["NO_DIRECTIONAL_QUALITY_INTERPRETATION", "NO_CAUSAL_EFFECT_INFERENCE", "NO_ACTION_SUCCESS_INFERENCE", "NO_STAKEHOLDER_INTENT_VALIDATION"]) {
      expect(screen.getAllByText(code).length).toBe(4);
    }
    expect(screen.queryByText(/^Improved$|^Worsened$|^Successful fix$/i)).toBeNull();
  });
});

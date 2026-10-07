import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { i18n } from "../../i18n";
import { lifecycleFixture } from "../reassessment/testFixture";
import { ComparisonPage } from "./ComparisonPage";
import { selectComparisonProjection } from "./projection";

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
    const response = structuredClone(lifecycleFixture());
    (response.full_model as any).comparisons[0].before_state_and_value.exact_value = { numerator: 50, denominator: 1 };
    (response.full_model as any).comparisons[0].after_state_and_value.exact_value = { numerator: 1, denominator: 50 };
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
});

import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { i18n } from "../../i18n";
import { selectVisibleResultSections } from "../results/projection";
import { ReassessmentPage } from "./ReassessmentPage";
import { selectReassessmentProjection } from "./projection";
import { lifecycleFixture } from "./testFixture";

describe("RUI-15 reassessment projection", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(cleanup);

  it("never exposes lifecycle pages for INITIAL, including stray records", () => {
    const response = lifecycleFixture("INITIAL");
    expect(selectVisibleResultSections(response)).toHaveLength(8);
    expect(selectReassessmentProjection(response)).toBeNull();
  });

  it.each(["CONTROLLED_DEMO", "REASSESSMENT"] as const)("accepts canonical %s lifecycle", (analysisCase) => {
    const projected = selectReassessmentProjection(lifecycleFixture(analysisCase));
    expect(projected?.producedResults.map((item) => item.family)).toEqual(["CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH", "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH"]);
    expect(projected?.comparisonRequestRefs).toEqual([]);
    expect(projected?.requirements.map((item) => item.changed)).toEqual([false, true]);
  });

  it.each([
    ["rule", (r: any) => { r.full_model.reassessment.rule_ref.rule_id = "OTHER"; }],
    ["provenance", (r: any) => { r.full_model.reassessment.provenance.child_artifact_ref = { artifact_id: "SPEC", artifact_version: "other" }; }],
    ["process lineage", (r: any) => { r.full_model.process_v2.process_state_id = "OTHER"; }],
    ["result pairing", (r: any) => { r.full_model.reassessment.produced_results.pop(); }],
    ["core family", (r: any) => { r.full_model.reassessment.produced_result_refs[0].result_family = "OTHER"; }],
    ["lineage", (r: any) => { r.full_model.reassessment.produced_results[0].specification_version.requirements[0].lineage_id.origin_requirement_id = "OTHER"; }],
    ["reuse check", (r: any) => { r.full_model.reassessment.context.evidence_reuse_decisions[0].exact_identity_checks[0].matches = false; r.full_model.reassessment.provenance.evidence_reuse_decisions[0].exact_identity_checks[0].matches = false; }],
  ])("fails closed for malformed %s", (_label, mutate) => {
    const response = structuredClone(lifecycleFixture());
    mutate(response);
    expect(selectReassessmentProjection(response)).toBeNull();
    expect(selectVisibleResultSections(response)).not.toContain("reassessment");
  });

  it("uses core v2 snapshots, preserves source text, exact fractions, and changed_subjects", () => {
    render(<ReassessmentPage result={lifecycleFixture()} />);
    expect(screen.getByText("Original two")).toBeTruthy();
    expect(screen.getByText("Revised two")).toBeTruthy();
    expect(screen.getByText("Changed by external revision")).toBeTruthy();
    expect(screen.getAllByText("2/3").length).toBeGreaterThan(0);
    expect(screen.queryByText(/^Improved$|^Worsened$/i)).toBeNull();
  });
});

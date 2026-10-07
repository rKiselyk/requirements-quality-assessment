import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { i18n } from "../../i18n";
import { selectVisibleResultSections } from "../results/projection";
import { ReassessmentPage } from "./ReassessmentPage";
import { selectReassessmentProjection } from "./projection";
import { lifecycleFixture } from "./testFixture";

function model(response: any) { return response.full_model as Record<string, any>; }
function prior(response: any) { return response.reassessment_context as Record<string, any>; }
function reassessment(response: any) { return model(response).reassessment as Record<string, any>; }
function syncEnvelope(response: any) {
  const full = model(response);
  Object.assign(prior(response), {
    initial_specification: structuredClone(full.initial_specification),
    initial_specification_assessment: structuredClone(full.initial_specification_assessment),
    predecessor_process_state: structuredClone(full.process_v1),
    corrective_action_resolution: structuredClone(full.corrective_action_resolution),
    action_application: structuredClone(full.action_application),
    external_revision: structuredClone(full.external_revision),
    revised_specification: structuredClone(full.revised_specification),
    successor_process_state: structuredClone(full.process_v2),
    process_transition: structuredClone(full.process_transition),
    comparisons: structuredClone(full.comparisons),
    evidence_reuse_decisions: structuredClone(full.reassessment.context.evidence_reuse_decisions),
  });
  prior(response).reassessment_identity = {
    reassessment_id: full.reassessment.reassessment_id,
    reassessment_version: full.reassessment.reassessment_version,
    child_process_state_ref: structuredClone(full.reassessment.child_process_state_ref),
    component_version_set: structuredClone(full.reassessment.context.component_version_set),
  };
}

describe("RUI-15 reassessment projection", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

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

  it.each([
    ["wrong scenario ID", (r: any) => { r.controlled_scenario.id = "OTHER"; }],
    ["wrong scenario version", (r: any) => { r.controlled_scenario.version = "2"; }],
    ["null controlled scenario", (r: any) => { r.controlled_scenario = null; }],
    ["prior scenario mismatch", (r: any) => { prior(r).scenario = { id: "OTHER", version: "1" }; }],
    ["missing prior context", (r: any) => { r.reassessment_context = null; }],
    ["missing digest", (r: any) => { delete prior(r).context_digest; }],
    ["empty digest", (r: any) => { prior(r).context_digest = ""; }],
    ["wrong contract", (r: any) => { r.contract_version = "research-api-v2"; }],
    ["AVAILABLE with reason", (r: any) => { r.section_availability[0].reason_code = "CONTRADICTION"; }],
    ["UNAVAILABLE without reason", (r: any) => { r.section_availability[0].availability = "UNAVAILABLE"; }],
    ["duplicate section", (r: any) => { r.section_availability.push(structuredClone(r.section_availability[0])); }],
  ])("hides both lifecycle pages for %s", (_label, mutate) => {
    const response: any = lifecycleFixture();
    mutate(response);
    expect(selectVisibleResultSections(response)).not.toContain("reassessment");
    expect(selectVisibleResultSections(response)).not.toContain("comparison");
  });

  it.each([
    ["initial specification", "initial_specification", "artifact_ref"],
    ["initial assessment", "initial_specification_assessment", "records"],
    ["predecessor process", "predecessor_process_state", "process_state_version"],
    ["action application", "action_application", "status"],
    ["external revision", "external_revision", "revision_version"],
    ["revised specification", "revised_specification", "artifact_ref"],
    ["successor process", "successor_process_state", "process_state_version"],
    ["process transition", "process_transition", "transition_id"],
    ["comparisons", "comparisons", "length"],
  ])("rejects prior/full-model %s mismatch", (_label, contextField, nested) => {
    const response: any = lifecycleFixture();
    const value = prior(response)[contextField];
    if (nested === "length") value.pop();
    else if (nested === "artifact_ref") value[nested] = { artifact_id: "OTHER", artifact_version: "v9" };
    else if (nested === "records") value[nested] = [];
    else if (nested === "transition_id") value[nested] = { transition_id: "OTHER" };
    else value[nested] = "OTHER";
    expect(selectReassessmentProjection(response)).toBeNull();
  });

  it.each([
    ["missing external revision", (r: any) => { delete model(r).external_revision; }],
    ["revision parent", (r: any) => { model(r).external_revision.parent_artifact_ref = { artifact_id: "SPEC", artifact_version: "other" }; }],
    ["revision child", (r: any) => { model(r).external_revision.requested_child_artifact_ref = { artifact_id: "SPEC", artifact_version: "other" }; }],
    ["empty revision ID", (r: any) => { model(r).external_revision.revision_id = ""; }],
    ["empty revision version", (r: any) => { model(r).external_revision.revision_version = ""; }],
    ["unsupported provider kind", (r: any) => { model(r).external_revision.provider_kind = "SYSTEM"; }],
    ["revision action", (r: any) => { model(r).external_revision.action_ref = { action_id: {}, action_record_version: "other" }; }],
    ["revision provenance action", (r: any) => { model(r).external_revision.provenance.action_ref = { action_id: {}, action_record_version: "other" }; }],
    ["specification revision", (r: any) => { model(r).revised_specification.provenance.revision_ref = { revision_id: "OTHER", revision_version: "1" }; }],
    ["specification application", (r: any) => { model(r).revised_specification.provenance.application_ref = { application_id: {}, application_version: "other" }; }],
    ["specification parent", (r: any) => { model(r).revised_specification.provenance.parent_artifact_ref = { artifact_id: "SPEC", artifact_version: "other" }; }],
    ["specification child", (r: any) => { model(r).revised_specification.provenance.artifact_ref = { artifact_id: "SPEC", artifact_version: "other" }; }],
    ["process contract", (r: any) => { model(r).revised_specification.provenance.process_reassessment_contract_ref.version = "2"; }],
    ["application rule", (r: any) => { model(r).revised_specification.provenance.application_rule_ref_or_none.rule_id = "OTHER"; }],
  ])("rejects malformed revision lineage: %s", (_label, mutate) => {
    const response: any = lifecycleFixture();
    mutate(response);
    const revised = model(response).revised_specification;
    if (revised) reassessment(response).produced_results[0].specification_version = structuredClone(revised);
    syncEnvelope(response);
    expect(selectReassessmentProjection(response)).toBeNull();
  });

  it("renders canonical external revision and provider identities", () => {
    render(<ReassessmentPage result={lifecycleFixture()} />);
    expect(screen.getAllByText(/REVISION-REFERENCE/).length).toBeGreaterThan(0);
    expect(screen.getByText(/CONTROLLED_REFERENCE_FIXTURE/)).toBeTruthy();
    expect(screen.getByText(/REFERENCE_FIXTURE/)).toBeTruthy();
  });

  it.each([
    ["empty components", (r: any) => { reassessment(r).context.component_version_set.components = []; }],
    ["malformed component", (r: any) => { reassessment(r).context.component_version_set.components[0].component_id = ""; }],
    ["duplicate role", (r: any) => { reassessment(r).context.component_version_set.components[1].component_role = "FULL_MODEL_CONTRACT"; }],
    ["source process", (r: any) => { reassessment(r).context.evidence_reuse_decisions[0].provenance.source_process_state_ref.process_state_version = "other"; }],
    ["target process", (r: any) => { reassessment(r).context.evidence_reuse_decisions[0].provenance.target_process_state_ref.process_state_version = "other"; }],
    ["source contract", (r: any) => { reassessment(r).context.evidence_reuse_decisions[0].provenance.source_contract_ref.version = ""; }],
    ["reuse rule", (r: any) => { reassessment(r).context.evidence_reuse_decisions[0].provenance.reassessment_rule_ref.rule_id = "OTHER"; }],
  ])("rejects malformed component/evidence identity: %s", (_label, mutate) => {
    const response: any = lifecycleFixture();
    mutate(response);
    reassessment(response).provenance.component_version_set = structuredClone(reassessment(response).context.component_version_set);
    reassessment(response).provenance.evidence_reuse_decisions = structuredClone(reassessment(response).context.evidence_reuse_decisions);
    syncEnvelope(response);
    expect(selectReassessmentProjection(response)).toBeNull();
  });

  it("keeps REBUILD_OR_RECOLLECT_REQUIRED distinct", () => {
    const response: any = lifecycleFixture();
    const decision = reassessment(response).context.evidence_reuse_decisions[0];
    decision.decision = "REBUILD_OR_RECOLLECT_REQUIRED";
    decision.reason_codes = ["IDENTITY_OR_CONTEXT_CHANGED"];
    decision.exact_identity_checks[0].actual = { product_id: "OTHER" };
    decision.exact_identity_checks[0].matches = false;
    reassessment(response).provenance.evidence_reuse_decisions = structuredClone(reassessment(response).context.evidence_reuse_decisions);
    syncEnvelope(response);
    expect(selectReassessmentProjection(response)?.evidenceReuse[0].decision).toBe("REBUILD_OR_RECOLLECT_REQUIRED");
  });

  it.each([
    ["length mismatch", (r: any) => { reassessment(r).produced_results.pop(); }],
    ["missing core", (r: any) => { reassessment(r).produced_result_refs[0].result_family = "OTHER"; }],
    ["duplicate core", (r: any) => { reassessment(r).produced_result_refs[1].result_family = "CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH"; }],
    ["missing dynamic", (r: any) => { reassessment(r).produced_result_refs[1].result_family = "OTHER"; }],
    ["duplicate dynamic", (r: any) => { reassessment(r).produced_result_refs[0].result_family = "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH"; }],
    ["core artifact", (r: any) => { reassessment(r).produced_result_refs[0].artifact_ref = { artifact_id: "SPEC", artifact_version: "v1" }; }],
    ["core assessment", (r: any) => { reassessment(r).produced_result_refs[0].result_id = { assessment_id: "OTHER", assessment_version: "v2", artifact_ref: { artifact_id: "SPEC", artifact_version: "v2" } }; }],
    ["metric artifact", (r: any) => { reassessment(r).produced_results[0].metric_profile.artifact_ref = { artifact_id: "SPEC", artifact_version: "v1" }; }],
    ["dynamic artifact", (r: any) => { reassessment(r).produced_results[1].artifact_ref = { artifact_id: "SPEC", artifact_version: "v1" }; }],
    ["nested artifact", (r: any) => { reassessment(r).produced_results[1].feature_profile.artifact_ref = { artifact_id: "SPEC", artifact_version: "v1" }; }],
    ["dynamic result ID", (r: any) => { reassessment(r).produced_result_refs[1].result_id = { id: "OTHER" }; }],
  ])("rejects malformed produced result: %s", (_label, mutate) => {
    const response: any = lifecycleFixture();
    mutate(response);
    reassessment(response).provenance.produced_result_refs = structuredClone(reassessment(response).produced_result_refs);
    expect(selectReassessmentProjection(response)).toBeNull();
  });

  it("preserves produced-result order", () => {
    expect(selectReassessmentProjection(lifecycleFixture())?.producedResults.map((item) => item.family)).toEqual(["CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH", "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH"]);
  });

  it("aligns requirement snapshots by lineage rather than array index", () => {
    const response: any = lifecycleFixture();
    const revisedRequirements = model(response).revised_specification.requirements;
    revisedRequirements[0].subject_ref.source_line = 2;
    revisedRequirements[1].subject_ref.source_line = 1;
    model(response).revised_specification.requirements = [revisedRequirements[1], revisedRequirements[0]];
    const records = reassessment(response).produced_results[0].requirement_records;
    records[0].extraction_result.requirement.source_line = 2;
    records[1].extraction_result.requirement.source_line = 1;
    syncEnvelope(response);

    expect(selectReassessmentProjection(response)?.requirements.map((item) => [
      item.beforeSubject.requirement_id,
      item.afterSubject.requirement_id,
    ])).toEqual([["R001", "R001"], ["R002", "R002"]]);
  });

  it("rejects a predecessor subject mismatch", () => {
    const response: any = lifecycleFixture();
    model(response).revised_specification.requirements[0].predecessor_subject_ref = {
      artifact_ref: { artifact_id: "SPEC", artifact_version: "v1" },
      requirement_id: "OTHER",
      source_line: 1,
    };
    syncEnvelope(response);
    expect(selectReassessmentProjection(response)).toBeNull();
  });

  it("rejects duplicate requirement lineage", () => {
    const response: any = lifecycleFixture();
    const requirements = model(response).revised_specification.requirements;
    requirements[1].lineage_id = structuredClone(requirements[0].lineage_id);
    syncEnvelope(response);
    expect(selectReassessmentProjection(response)).toBeNull();
  });

  it("accepts canonical tuple ordering with equal source lines", () => {
    const response: any = lifecycleFixture();
    const full = model(response);
    full.initial_specification.requirements[1].subject_ref.source_line = 1;
    full.initial_specification.requirements[1].lineage_id.origin_source_line = 1;
    full.revised_specification.requirements[1].subject_ref.source_line = 1;
    full.revised_specification.requirements[1].predecessor_subject_ref.source_line = 1;
    full.initial_specification_assessment.records[1].extraction_result.requirement.source_line = 1;
    reassessment(response).produced_results[0].requirement_records[1].extraction_result.requirement.source_line = 1;
    reassessment(response).produced_results[0].specification_assessment.records[1].extraction_result.requirement.source_line = 1;
    syncEnvelope(response);
    expect(selectReassessmentProjection(response)).not.toBeNull();
  });

  it("rejects noncanonical requirement-ID order when source lines are equal", () => {
    const response: any = lifecycleFixture();
    const requirements = model(response).initial_specification.requirements;
    requirements[1].subject_ref.source_line = 1;
    requirements[1].lineage_id.origin_source_line = 1;
    model(response).initial_specification.requirements = [requirements[1], requirements[0]];
    syncEnvelope(response);
    expect(selectReassessmentProjection(response)).toBeNull();
  });

  it("takes v2 page data from the produced core result, not top-level response fields", () => {
    const response: any = lifecycleFixture();
    response.requirements = [{ requirement: { id: "R999", source_line: 999, text: "Top-level decoy" } }];
    response.specification = { text: "Top-level decoy" };
    const projected = selectReassessmentProjection(response);
    expect(projected?.requirements.map((item) => item.afterText)).toEqual(["Original one", "Revised two"]);
  });

  it("accepts the exact REUSE_ALLOWED evidence path", () => {
    expect(selectReassessmentProjection(lifecycleFixture())?.evidenceReuse[0]).toMatchObject({
      decision: "REUSE_ALLOWED",
      reasonCodes: ["EXACT_IDENTITY_AND_CONTEXT_MATCH"],
    });
  });

  it("does not infer changed status from text difference", () => {
    const response: any = lifecycleFixture();
    model(response).revised_specification.changed_subjects = [];
    reassessment(response).produced_results[0].specification_version = structuredClone(model(response).revised_specification);
    syncEnvelope(response);
    expect(selectReassessmentProjection(response)?.requirements.map((item) => item.changed)).toEqual([false, false]);
  });

  it.each(["UNKNOWN", "NOT_APPLICABLE"] as const)("preserves %s without a fabricated value", (state) => {
    const response: any = lifecycleFixture();
    const assessment = reassessment(response).produced_results[0].requirement_records[0].quality_profile.completeness;
    assessment.state = state;
    assessment.value = null;
    expect(selectReassessmentProjection(response)?.requirements[0].after.completeness).toEqual({ state, value: null });
  });

  it("keeps v1/v2 QB and C/V/U snapshots separate without comparison kinds", () => {
    const projected = selectReassessmentProjection(lifecycleFixture());
    expect(projected?.specification.qbBefore.value).toEqual({ numerator: "1", denominator: "2" });
    expect(projected?.specification.qbAfter.value).toEqual({ numerator: "2", denominator: "2" });
    expect(projected?.requirements[0].before.completeness.value).toEqual({ numerator: "1", denominator: "3" });
    expect(projected?.requirements[0].after.completeness.value).toEqual({ numerator: "2", denominator: "3" });
    expect(projected?.requirements[0].after).not.toHaveProperty("comparisonKind");
  });

  it("renders Ukrainian lifecycle labels without translating canonical text or revision identity", async () => {
    await i18n.changeLanguage("uk");
    render(<ReassessmentPage result={lifecycleFixture()} />);
    expect(screen.getByRole("heading", { name: "Повторне оцінювання" })).toBeTruthy();
    expect(screen.getByText("Revised two")).toBeTruthy();
    expect(screen.getAllByText(/REVISION-REFERENCE/).length).toBeGreaterThan(0);
  });

  it("preserves lifecycle eligibility across locale switching without an analysis call", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const response = lifecycleFixture();
    const before = selectVisibleResultSections(response);

    await i18n.changeLanguage("uk");

    expect(selectVisibleResultSections(response)).toEqual(before);
    expect(before).toEqual(expect.arrayContaining(["reassessment", "comparison"]));
    expect(fetchSpy).not.toHaveBeenCalled();
  });
});

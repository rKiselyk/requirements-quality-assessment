import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../../App";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { i18n } from "../../i18n";
import { ResultWorkspace } from "../results/ResultWorkspace";
import { ProcessPage } from "./ProcessPage";
import { COMPONENT_ROLES, EVIDENCE_ROLES, selectProcessPage } from "./projection";

const fullContract = { contract_id: "FULL-MODEL-V0.1-CONTRACT", version: "1" };
const processContract = { contract_id: "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", version: "1" };
const processRule = { rule_id: "PROCESS-REFERENCE-VERIFICATION-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const checkpointContract = { contract_id: "FULL-MODEL-V1.0-SCALAR-CHECKPOINT", version: "1" };
const checkpointRule = { rule_id: "CHECKPOINT-SCALAR-PREDICATE-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const registry = { contract_id: "FULL-MODEL-V0.1-METRICS", version: "1" };

function artifact(version: string) { return { artifact_id: "SPEC-PROCESS", artifact_version: version }; }
function assessment(version: string) { return { assessment_id: "ASSESS-PROCESS", assessment_version: version, artifact_ref: artifact(version) }; }
function processRef(version: string) { return { process_state_id: "PROCESS-LINEAGE", process_state_version: version, stage: "REFERENCE_VERIFICATION" }; }
function metric(version: string) { return { artifact_ref: artifact(version), assessment_ref: assessment(version), registry_ref: registry }; }
function actionId() {
  return {
    action_instance_id: "ACTION",
    target_artifact_ref: artifact("v1"),
    originating_risk_id: { assessment_event_ref: { process_state_ref: processRef("v1") } },
  };
}
function actionRef(version: string) { return { action_id: actionId(), action_record_version: version }; }

function refs(version: string) {
  const ownArtifact = artifact(version);
  const ownAssessment = assessment(version);
  const ownProcess = processRef(version);
  const requirement = { assessment_ref: ownAssessment, requirement_subject_ref: { artifact_ref: ownArtifact, requirement_id: "R001", source_line: 1 } };
  const specification = { assessment_ref: ownAssessment, snapshot_id: { value: `snapshot-${version}` } };
  const metricProfile = metric(version);
  const feature = { artifact_ref: ownArtifact, source_assessment_ref: ownAssessment, metric_profile_ref: metricProfile, process_state_ref: ownProcess };
  const quality = { assessment_id: { assessment_event_ref: { artifact_ref: ownArtifact }, feature_profile_ref: { process_state_ref: ownProcess, source_assessment_ref: ownAssessment } }, product_quality_assessment_version: version };
  const population = { population_id: { artifact_ref: ownArtifact, source_assessment_ref: ownAssessment } };
  const problem = { problem_id: { artifact_ref: ownArtifact, source_assessment_ref: ownAssessment } };
  const relation = { relation_id: { problem_resolution_ref: { resolution_id: { artifact_ref: ownArtifact, source_assessment_ref: ownAssessment } } } };
  const risk = { risk_assessment_id: { assessment_event_ref: { artifact_ref: ownArtifact, process_state_ref: ownProcess } } };
  const action = actionRef(version);
  return { requirement, specification, metricProfile, feature, quality, population, problem, relation, risk, action };
}

function componentAssociations(version: string) {
  const value = refs(version);
  const resultByRole: Record<string, unknown> = {
    REQUIREMENT_ASSESSMENT: value.requirement,
    SPECIFICATION_ASSESSMENT: value.specification,
    METRIC_PROFILE: value.metricProfile,
    PE_FEATURE_PROFILE: value.feature,
    PRODUCT_QUALITY_ASSESSMENT: value.quality,
    DEFECT_POPULATION: value.population,
    CONFIRMED_PROBLEM: value.problem,
    DEFECT_QUALITY_RELATION: value.relation,
    BOUNDED_RISK_ASSESSMENT: value.risk,
    CORRECTIVE_ACTION: value.action,
  };
  return COMPONENT_ROLES.map((role) => ({
    role, result_ref: resultByRole[role], status: "AVAILABLE", applicability: "APPLICABLE",
    subject_or_scope_ref: artifact(version), producing_contract_or_rule_ref: fullContract,
    reason_codes: [], provenance: [{ role, version }],
  }));
}

function evidenceAssociations(version: string) {
  return EVIDENCE_ROLES.map((role) => ({
    role, evidence_ref: { evidence_id: `${role}-${version}` }, status: "AVAILABLE", applicability: "APPLICABLE",
    artifact_or_product_ref: artifact(version), source_or_collection_ref: { source_id: `SOURCE-${role}` },
    context_ref_or_none: null, reuse_decision_ref_or_none: null, reason_codes: [], provenance: [{ role, version }],
  }));
}

const componentVersions = { components: [
  { component_role: "FULL_MODEL_CONTRACT", component_id: "FULL-MODEL-V0.1-CONTRACT", component_version: "1" },
  { component_role: "PROCESS_REASSESSMENT", component_id: "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", component_version: "1" },
] };

function processState(version: "v1" | "v2") {
  const values = refs(version);
  const components = componentAssociations(version);
  const evidence = evidenceAssociations(version);
  const predecessor = version === "v1" ? null : processRef("v1");
  const transitionRef = version === "v1" ? null : { transition_id: { transition_id: "ARTIFACT-TRANSITION" } };
  const reassessmentRef = version === "v1" ? null : { reassessment_id: "REASSESSMENT", reassessment_version: "1" };
  const applicationRef = version === "v1" ? null : { application_id: { application_instance_id: "APPLICATION", action_before_ref: actionRef("v1"), revision_ref: { revision_id: "REVISION", revision_version: "1" }, child_artifact_ref: artifact("v2") }, application_version: "1" };
  const comparisons = version === "v1" ? [] : [{ comparison_id: "COMPARISON", comparison_version: "1" }];
  const state: Record<string, any> = {
    status: null, applicability: null,
    process_state_id: "PROCESS-LINEAGE", process_state_version: version, process_lineage_id: "PROCESS-LINEAGE", stage: "REFERENCE_VERIFICATION",
    artifact_ref: artifact(version), artifact_transition_ref_or_none: transitionRef, assessment_ref: assessment(version), full_model_contract_ref: fullContract,
    component_version_set: componentVersions, evidence_associations: evidence, component_associations: components,
    requirement_assessment_refs: [values.requirement], specification_assessment_ref: values.specification, metric_profile_ref: values.metricProfile,
    pe_feature_profile_ref: values.feature, product_quality_assessment_ref: values.quality, defect_population_ref: values.population,
    confirmed_problem_refs: [values.problem], defect_quality_relation_refs: [values.relation], bounded_risk_assessment_refs: [values.risk], corrective_action_refs: [values.action],
    predecessor_process_state_ref: predecessor, reassessment_ref: reassessmentRef,
  };
  state.provenance = {
    process_state_ref: processRef(version), process_lineage_id: "PROCESS-LINEAGE", artifact_ref: artifact(version), assessment_ref: assessment(version),
    predecessor_process_state_ref: predecessor, artifact_transition_ref_or_none: transitionRef, action_application_ref_or_none: applicationRef,
    reassessment_ref_or_none: reassessmentRef, comparison_refs: comparisons, evidence_associations: evidence, component_associations: components,
    component_version_set: componentVersions, full_model_contract_ref: fullContract, process_reassessment_contract_ref: processContract, rule_ref: processRule,
  };
  return state;
}

function checkpoint(version: "v1" | "v2", outcome = version === "v1" ? "NOT_SATISFIED" : "SATISFIED") {
  const process = processRef(version);
  const ownArtifact = artifact(version);
  const resultRef = { profile_id: metric(version), scope: "SPECIFICATION", subject_ref: { artifact_ref: ownArtifact }, metric_id: "SPEC.QB_CONSISTENCY" };
  const selectedProvenance = [{ source: version }];
  const selected = {
    result_ref: resultRef, result_identity: "SPEC.QB_CONSISTENCY", status: "AVAILABLE", applicability: "APPLICABLE",
    exact_value: { numerator: version === "v1" ? 0 : 1, denominator: 1 }, artifact_ref: ownArtifact, process_state_ref: process,
    governing_contract_or_rule_ref: registry, reason_codes: [], provenance: selectedProvenance,
  };
  const policy = {
    policy_id: "EXTERNAL-POLICY", policy_version: "7", source_ref: { source_id: "POLICY-SOURCE", source_version: "3" },
    provider_ref: { provider_id: "POLICY-PROVIDER", provider_version: "2" }, rationale: "Externally supplied research threshold.",
    comparator: ">=", threshold: { numerator: 1, denominator: 1 }, governing_contract_ref: { contract_id: "EXTERNAL-POLICY-CONTRACT", version: "9" },
  };
  return {
    checkpoint_id: `CHECKPOINT-${version}`, checkpoint_version: "1", selected_result: selected, threshold_policy: policy,
    process_state_ref: process, artifact_ref: ownArtifact, outcome, reason_codes: [outcome === "SATISFIED" ? "PREDICATE_TRUE" : "PREDICATE_FALSE"],
    checkpoint_contract_ref: checkpointContract, evaluator_rule_ref: checkpointRule,
    provenance: {
      selected_result_ref: resultRef, selected_result_provenance: selectedProvenance,
      threshold_policy_ref: { policy_id: "EXTERNAL-POLICY", policy_version: "7" }, policy_source_ref: policy.source_ref, policy_provider_ref: policy.provider_ref,
      process_state_ref: process, artifact_ref: ownArtifact, governing_policy_contract_ref: policy.governing_contract_ref,
      checkpoint_contract_ref: checkpointContract, evaluator_rule_ref: checkpointRule,
    },
  };
}

export function processResponse(): CanonicalAnalyzeResponse {
  const v1 = processState("v1");
  const v2 = processState("v2");
  const artifactTransition = v2.artifact_transition_ref_or_none;
  const applicationRef = v2.provenance.action_application_ref_or_none;
  const reassessmentRef = v2.reassessment_ref;
  const comparisonRefs = v2.provenance.comparison_refs;
  const transition = {
    transition_id: { transition_id: "PROCESS-TRANSITION" }, predecessor_process_state_ref: processRef("v1"), successor_process_state_ref: processRef("v2"),
    artifact_transition_ref: artifactTransition, action_application_ref: applicationRef, reassessment_ref: reassessmentRef, comparison_refs: comparisonRefs, rule_ref: processRule,
    provenance: {
      predecessor_process_state_ref: processRef("v1"), successor_process_state_ref: processRef("v2"), artifact_transition_ref: artifactTransition,
      action_application_ref: applicationRef, reassessment_ref: reassessmentRef, comparison_refs: comparisonRefs,
      process_reassessment_contract_ref: processContract, rule_ref: processRule,
    },
  };
  return {
    contract_version: "research-api-v1", analysis_case: "CONTROLLED_DEMO", controlled_scenario: { id: "SCENARIO", version: "1" },
    requirements: [], specification: {}, section_availability: [{ section: "process", availability: "AVAILABLE", reason_code: null }],
    full_model: {
      process_v1: v1, process_v2: v2, process_transition: transition,
      revised_specification: { artifact_ref: artifact("v2") },
      action_application: {
        application_id: applicationRef.application_id, application_version: applicationRef.application_version, child_artifact_ref: artifact("v2"),
        action_before_ref: actionRef("v1"), action_after_ref: actionRef("v2"),
        transition: { transition_id: { transition_id: "ARTIFACT-TRANSITION" } },
      },
      reassessment: {
        reassessment_id: "REASSESSMENT", reassessment_version: "1", child_process_state_ref: processRef("v2"),
        context: {
          predecessor_process_state_ref: processRef("v1"), action_application_ref: applicationRef,
          parent_artifact_ref: artifact("v1"), child_artifact_ref: artifact("v2"), child_assessment_ref: assessment("v2"),
          component_version_set: componentVersions, full_model_contract_ref: fullContract, stage: "REFERENCE_VERIFICATION",
        },
        provenance: {
          reassessment_ref: reassessmentRef, action_application_ref: applicationRef, predecessor_process_state_ref: processRef("v1"),
          child_process_state_ref: processRef("v2"), parent_artifact_ref: artifact("v1"), child_artifact_ref: artifact("v2"),
          child_assessment_ref: assessment("v2"), component_version_set: componentVersions,
          full_model_contract_ref: fullContract, process_reassessment_contract_ref: processContract,
        },
      },
      comparisons: [{ comparison_id: "COMPARISON", comparison_version: "1" }],
      checkpoint_evaluations: [checkpoint("v1"), checkpoint("v2")],
    },
    reassessment_context: {}, limitations: [],
  };
}

function clone() { return structuredClone(processResponse()) as CanonicalAnalyzeResponse; }
function fm(value: CanonicalAnalyzeResponse) { return value.full_model as Record<string, any>; }
function state(value: CanonicalAnalyzeResponse, name: "process_v1" | "process_v2") { return fm(value)[name] as Record<string, any>; }
function checkpoints(value: CanonicalAnalyzeResponse) { return fm(value).checkpoint_evaluations as Array<Record<string, any>>; }
function expectMalformed(value: CanonicalAnalyzeResponse) { expect(selectProcessPage(value).kind).toBe("MALFORMED"); }

describe("RUI-13 process projection", () => {
  beforeEach(async () => { window.sessionStorage.clear(); await i18n.changeLanguage("en"); });
  afterEach(() => { cleanup(); vi.restoreAllMocks(); });

  it("accepts the canonical process_v1/process_v2 graph and derives the current state only from the exact successor", () => {
    const projected = selectProcessPage(processResponse());
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.current).toBe(projected.successor);
    expect(projected.current.version).toBe("v2");
    expect(projected.predecessor.version).toBe("v1");
  });

  it.each([
    ["another artifact", (ref: Record<string, any>) => { ref.action_id.target_artifact_ref = artifact("other"); }],
    ["another process state", (ref: Record<string, any>) => { ref.action_id.originating_risk_id.assessment_event_ref.process_state_ref = processRef("other"); }],
    ["missing action_record_version", (ref: Record<string, any>) => { delete ref.action_record_version; }],
    ["blank action_record_version", (ref: Record<string, any>) => { ref.action_record_version = " "; }],
  ])("rejects a process_v1 corrective ActionRef owned by %s", (_label, mutate) => {
    const value = clone(); mutate(state(value, "process_v1").corrective_action_refs[0]); expectMalformed(value);
  });

  it("rejects process_v2 when corrective_action_refs omit the exact applied action_after_ref", () => {
    const value = clone(); const v2 = state(value, "process_v2");
    const replacement = actionRef("another-record-version");
    v2.corrective_action_refs = [replacement];
    v2.component_associations.find((item: any) => item.role === "CORRECTIVE_ACTION").result_ref = replacement;
    expectMalformed(value);
  });

  it("rejects a process_v2 corrective ActionRef from a different action_id lineage", () => {
    const value = clone(); const v2 = state(value, "process_v2");
    const replacement = actionRef("v2"); replacement.action_id.action_instance_id = "OTHER-ACTION";
    v2.corrective_action_refs = [replacement];
    v2.component_associations.find((item: any) => item.role === "CORRECTIVE_ACTION").result_ref = replacement;
    expectMalformed(value);
  });

  it("allows multiple successor ActionRefs in one lineage without requiring one record version", () => {
    const value = clone(); const v2 = state(value, "process_v2");
    const additional = actionRef("v3");
    v2.corrective_action_refs.push(additional);
    const association = structuredClone(v2.component_associations.find((item: any) => item.role === "CORRECTIVE_ACTION"));
    association.result_ref = additional;
    v2.component_associations.push(association);
    v2.provenance.component_associations = v2.component_associations;
    expect(selectProcessPage(value).kind).toBe("AVAILABLE");
  });

  it.each([
    ["target artifact", (ref: Record<string, any>) => { ref.action_id.target_artifact_ref = artifact("other"); }],
    ["origin risk process", (ref: Record<string, any>) => { ref.action_id.originating_risk_id.assessment_event_ref.process_state_ref = processRef("other"); }],
  ])("rejects application action_before_ref with a different predecessor %s", (_label, mutate) => {
    const value = clone(); mutate(fm(value).action_application.action_before_ref); expectMalformed(value);
  });

  it("rejects an arbitrary component producing source object", () => {
    const value = clone(); state(value, "process_v1").component_associations[0].producing_contract_or_rule_ref = { arbitrary: "SOURCE" }; expectMalformed(value);
  });

  it.each([
    ["ContractRef", { contract_id: "FUTURE-COMPONENT-CONTRACT", version: "3" }],
    ["explicit RuleRef", { rule_id: "FUTURE-COMPONENT-RULE", explicit_version: "4", version_authority: "EXPLICIT_CONTRACT_VERSION" }],
    ["stable RuleRef", { rule_id: "FUTURE-STABLE-RULE", explicit_version: null, version_authority: "STABLE_RULE_ID_POLICY" }],
  ])("accepts a typed component producing %s", (_label, producingRef) => {
    const value = clone(); state(value, "process_v1").component_associations[0].producing_contract_or_rule_ref = producingRef;
    expect(selectProcessPage(value).kind).toBe("AVAILABLE");
  });

  it.each([
    ["primitive result_ref", (c: Record<string, any>) => { c.selected_result.result_ref = "METRIC"; c.provenance.selected_result_ref = "METRIC"; }],
    ["arbitrary result_ref", (c: Record<string, any>) => { c.selected_result.result_ref = { arbitrary: "METRIC" }; c.provenance.selected_result_ref = c.selected_result.result_ref; }],
    ["profile mismatch", (c: Record<string, any>) => { c.selected_result.result_ref.profile_id = metric("other"); c.provenance.selected_result_ref = c.selected_result.result_ref; }],
    ["metric identity mismatch", (c: Record<string, any>) => { c.selected_result.result_ref.metric_id = "OTHER"; c.provenance.selected_result_ref = c.selected_result.result_ref; }],
    ["unsupported scope", (c: Record<string, any>) => { c.selected_result.result_ref.scope = "OTHER"; }],
    ["missing subject", (c: Record<string, any>) => { delete c.selected_result.result_ref.subject_ref; c.provenance.selected_result_ref = c.selected_result.result_ref; }],
  ])("isolates malformed typed MetricEntryId case: %s", (_label, mutate) => {
    const value = clone(); mutate(checkpoints(value)[0]);
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("MALFORMED");
  });

  it("accepts a valid REQUIREMENT-scope MetricEntryId", () => {
    const value = clone(); const entry = checkpoints(value)[0];
    entry.selected_result.result_ref.scope = "REQUIREMENT";
    entry.selected_result.result_ref.subject_ref = { artifact_ref: artifact("v1"), requirement_id: "R001", source_line: 1 };
    entry.provenance.selected_result_ref = entry.selected_result.result_ref;
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("AVAILABLE");
  });

  it.each([
    ["artifact mismatch", (subject: Record<string, any>) => { subject.artifact_ref = artifact("other"); }],
    ["missing requirement_id", (subject: Record<string, any>) => { delete subject.requirement_id; }],
    ["blank requirement_id", (subject: Record<string, any>) => { subject.requirement_id = " "; }],
    ["zero source_line", (subject: Record<string, any>) => { subject.source_line = 0; }],
    ["non-integer source_line", (subject: Record<string, any>) => { subject.source_line = 1.5; }],
  ])("rejects malformed REQUIREMENT-scope MetricEntry subject %s", (_label, mutate) => {
    const value = clone(); const entry = checkpoints(value)[0];
    entry.selected_result.result_ref.scope = "REQUIREMENT";
    entry.selected_result.result_ref.subject_ref = { artifact_ref: artifact("v1"), requirement_id: "R001", source_line: 1 };
    mutate(entry.selected_result.result_ref.subject_ref);
    entry.provenance.selected_result_ref = entry.selected_result.result_ref;
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("MALFORMED");
  });

  it("rejects a SPECIFICATION-scope MetricEntry subject artifact mismatch", () => {
    const value = clone(); const entry = checkpoints(value)[0];
    entry.selected_result.result_ref.subject_ref.artifact_ref = artifact("other");
    entry.provenance.selected_result_ref = entry.selected_result.result_ref;
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("MALFORMED");
  });

  it("rejects an arbitrary selected-result governing ref", () => {
    const value = clone(); checkpoints(value)[0].selected_result.governing_contract_or_rule_ref = { arbitrary: "GOVERNING" };
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("MALFORMED");
  });

  it.each([
    ["ContractRef", { contract_id: "FUTURE-RESULT-CONTRACT", version: "2" }],
    ["RuleRef", { rule_id: "FUTURE-RESULT-RULE", explicit_version: "2", version_authority: "EXPLICIT_CONTRACT_VERSION" }],
  ])("accepts a typed selected-result governing %s", (_label, governingRef) => {
    const value = clone(); checkpoints(value)[0].selected_result.governing_contract_or_rule_ref = governingRef;
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("AVAILABLE");
  });

  it.each([
    ["component reason_codes", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").component_associations[0].reason_codes = [null]; }],
    ["component provenance", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").component_associations[0].provenance = [null]; }],
    ["evidence reason_codes", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").evidence_associations[0].reason_codes = [null]; }],
    ["evidence provenance", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").evidence_associations[0].provenance = [null]; }],
  ])("rejects a null item inside %s", (_label, mutate) => {
    const value = clone(); mutate(value); expectMalformed(value);
  });

  it.each([
    ["selected reason_codes", (c: Record<string, any>) => { c.selected_result.reason_codes = [null]; }],
    ["selected provenance", (c: Record<string, any>) => { c.selected_result.provenance = [null]; c.provenance.selected_result_provenance = c.selected_result.provenance; }],
  ])("isolates a null item inside %s", (_label, mutate) => {
    const value = clone(); mutate(checkpoints(value)[0]);
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("MALFORMED");
  });

  it("accepts ARTIFACT_PROVENANCE_MISMATCH when both selected artifact and process differ", () => {
    const value = clone(); const entry = checkpoints(value)[0];
    entry.outcome = "UNRESOLVED"; entry.reason_codes = ["ARTIFACT_PROVENANCE_MISMATCH"];
    entry.selected_result.artifact_ref = artifact("other"); entry.selected_result.process_state_ref = processRef("other");
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE" || projected.checkpoints[0].kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].value.reasonCode).toBe("ARTIFACT_PROVENANCE_MISMATCH");
  });

  it("accepts PROCESS_STATE_PROVENANCE_MISMATCH only while selected artifact still matches", () => {
    const value = clone(); const entry = checkpoints(value)[0];
    entry.outcome = "UNRESOLVED"; entry.reason_codes = ["PROCESS_STATE_PROVENANCE_MISMATCH"];
    entry.selected_result.process_state_ref = processRef("other");
    const accepted = selectProcessPage(value);
    expect(accepted.kind).toBe("AVAILABLE");
    if (accepted.kind !== "AVAILABLE") return;
    expect(accepted.checkpoints[0].kind).toBe("AVAILABLE");
    entry.selected_result.artifact_ref = artifact("other");
    const rejected = selectProcessPage(value);
    expect(rejected.kind).toBe("AVAILABLE");
    if (rejected.kind !== "AVAILABLE") return;
    expect(rejected.checkpoints[0].kind).toBe("MALFORMED");
  });

  it.each([
    ["missing", (r: Record<string, any>) => { delete r.comparisons; }],
    ["non-array", (r: Record<string, any>) => { r.comparisons = { comparison_id: "COMPARISON", comparison_version: "1" }; }],
    ["malformed identity", (r: Record<string, any>) => { r.comparisons = [{ comparison_id: " ", comparison_version: "1" }]; }],
  ])("rejects %s full_model.comparisons", (_label, mutate) => {
    const value = clone(); mutate(fm(value)); expectMalformed(value);
  });

  it("requires comparison refs to match successor and transition exactly in source order", () => {
    const value = clone();
    fm(value).comparisons = [
      { comparison_id: "COMPARISON", comparison_version: "1" },
      { comparison_id: "COMPARISON-2", comparison_version: "1" },
    ];
    const reversed = [
      { comparison_id: "COMPARISON-2", comparison_version: "1" },
      { comparison_id: "COMPARISON", comparison_version: "1" },
    ];
    state(value, "process_v2").provenance.comparison_refs = reversed;
    fm(value).process_transition.comparison_refs = reversed;
    fm(value).process_transition.provenance.comparison_refs = reversed;
    expectMalformed(value);
  });

  it("accepts an empty canonical comparisons population only with empty process refs", () => {
    const value = clone(); fm(value).comparisons = [];
    state(value, "process_v2").provenance.comparison_refs = [];
    fm(value).process_transition.comparison_refs = [];
    fm(value).process_transition.provenance.comparison_refs = [];
    expect(selectProcessPage(value).kind).toBe("AVAILABLE");
  });

  it.each([
    ["lineage differs from state ID", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").process_lineage_id = "OTHER"; }],
    ["unsupported stage", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").stage = "OTHER"; }],
    ["assessment artifact mismatch", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").assessment_ref.artifact_ref = artifact("other"); }],
    ["Full Model contract mismatch", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").full_model_contract_ref.contract_id = "OTHER"; }],
    ["process rule mismatch", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").provenance.rule_ref.rule_id = "OTHER"; }],
    ["provenance process-state mismatch", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").provenance.process_state_ref.process_state_version = "other"; }],
    ["provenance artifact mismatch", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").provenance.artifact_ref = artifact("other"); }],
    ["provenance assessment mismatch", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").provenance.assessment_ref = assessment("other"); }],
    ["provenance component-version mismatch", (r: CanonicalAnalyzeResponse) => { const value = state(r, "process_v1"); value.provenance.component_version_set = structuredClone(value.component_version_set); value.provenance.component_version_set.components[0].component_version = "other"; }],
    ["v1 predecessor", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").predecessor_process_state_ref = processRef("v0"); }],
    ["v1 artifact transition", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").artifact_transition_ref_or_none = { transition_id: { transition_id: "OTHER" } }; }],
    ["v1 reassessment", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").reassessment_ref = { reassessment_id: "OTHER", reassessment_version: "1" }; }],
    ["v1 provenance application", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").provenance.action_application_ref_or_none = { id: "OTHER" }; }],
    ["v1 comparison refs", (r: CanonicalAnalyzeResponse) => { state(r, "process_v1").provenance.comparison_refs = [{ comparison_id: "OTHER", comparison_version: "1" }]; }],
    ["v2 predecessor mismatch", (r: CanonicalAnalyzeResponse) => { state(r, "process_v2").predecessor_process_state_ref.process_state_version = "other"; }],
    ["same state versions", (r: CanonicalAnalyzeResponse) => { state(r, "process_v2").process_state_version = "v1"; state(r, "process_v2").provenance.process_state_ref.process_state_version = "v1"; }],
    ["stable process ID changes", (r: CanonicalAnalyzeResponse) => { state(r, "process_v2").process_state_id = "OTHER"; state(r, "process_v2").process_lineage_id = "OTHER"; state(r, "process_v2").provenance.process_state_ref.process_state_id = "OTHER"; state(r, "process_v2").provenance.process_lineage_id = "OTHER"; }],
    ["revised artifact mismatch", (r: CanonicalAnalyzeResponse) => { fm(r).revised_specification.artifact_ref = artifact("other"); }],
  ])("fails the complete lifecycle graph closed for %s", (_label, mutate) => {
    const value = clone(); mutate(value); expectMalformed(value);
  });

  it("preserves component and evidence registry order including duplicate same-role entries", () => {
    const value = clone();
    const v1 = state(value, "process_v1");
    const duplicate = structuredClone(v1.component_associations[0]);
    v1.component_associations.splice(1, 0, duplicate);
    v1.requirement_assessment_refs.push(duplicate.result_ref);
    v1.provenance.component_associations = v1.component_associations;
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.predecessor.components.map((item) => item.role)).toEqual(["REQUIREMENT_ASSESSMENT", "REQUIREMENT_ASSESSMENT", ...COMPONENT_ROLES.slice(1)]);
    expect(projected.predecessor.evidence.map((item) => item.role)).toEqual(EVIDENCE_ROLES);
  });

  it.each([
    ["missing component role", (s: Record<string, any>) => { s.component_associations = s.component_associations.filter((x: any) => x.role !== "CORRECTIVE_ACTION"); s.provenance.component_associations = s.component_associations; }],
    ["component order", (s: Record<string, any>) => { s.component_associations.reverse(); s.provenance.component_associations = s.component_associations; }],
    ["invalid component state pair", (s: Record<string, any>) => { s.component_associations[0].applicability = "UNKNOWN"; }],
    ["AVAILABLE component lacks ref", (s: Record<string, any>) => { s.component_associations[0].result_ref = null; }],
    ["missing component ref lacks reason", (s: Record<string, any>) => { s.component_associations[0].result_ref = null; s.component_associations[0].status = "UNAVAILABLE"; s.component_associations[0].reason_codes = []; }],
    ["component convenience refs differ", (s: Record<string, any>) => { s.requirement_assessment_refs = []; }],
    ["missing evidence role", (s: Record<string, any>) => { s.evidence_associations.pop(); s.provenance.evidence_associations = s.evidence_associations; }],
    ["evidence order", (s: Record<string, any>) => { s.evidence_associations.reverse(); s.provenance.evidence_associations = s.evidence_associations; }],
    ["AVAILABLE evidence lacks ref", (s: Record<string, any>) => { s.evidence_associations[0].evidence_ref = null; }],
    ["reuse targets another state", (s: Record<string, any>) => { s.evidence_associations[0].reuse_decision_ref_or_none = { target_process_state_ref: processRef("other") }; }],
    ["requirement current artifact differs", (s: Record<string, any>) => { s.requirement_assessment_refs[0].requirement_subject_ref.artifact_ref = artifact("other"); }],
    ["metric current assessment differs", (s: Record<string, any>) => { s.metric_profile_ref.assessment_ref = assessment("other"); }],
  ])("rejects malformed association/current-ref case: %s", (_label, mutate) => {
    const value = clone(); const target = state(value, "process_v1"); mutate(target); expectMalformed(value);
  });

  it.each([
    ["predecessor", (r: Record<string, any>) => { r.predecessor_process_state_ref.process_state_version = "other"; }],
    ["successor", (r: Record<string, any>) => { r.successor_process_state_ref.process_state_version = "other"; }],
    ["rule", (r: Record<string, any>) => { r.rule_ref.rule_id = "OTHER"; }],
    ["artifact transition", (r: Record<string, any>) => { r.artifact_transition_ref.transition_id.transition_id = "OTHER"; }],
    ["application", (r: Record<string, any>) => { r.action_application_ref.application_version = "other"; }],
    ["reassessment", (r: Record<string, any>) => { r.reassessment_ref.reassessment_version = "other"; }],
    ["comparison order", (r: Record<string, any>) => { r.comparison_refs = [{ comparison_id: "OTHER", comparison_version: "1" }, ...r.comparison_refs]; }],
    ["provenance predecessor", (r: Record<string, any>) => { r.provenance.predecessor_process_state_ref.process_state_version = "other"; }],
    ["provenance successor", (r: Record<string, any>) => { r.provenance.successor_process_state_ref.process_state_version = "other"; }],
    ["provenance contract", (r: Record<string, any>) => { r.provenance.process_reassessment_contract_ref.contract_id = "OTHER"; }],
    ["provenance rule", (r: Record<string, any>) => { r.provenance.rule_ref.rule_id = "OTHER"; }],
  ])("rejects malformed process transition %s", (_label, mutate) => {
    const value = clone(); mutate(fm(value).process_transition); expectMalformed(value);
  });

  it("renders checkpoint absence neutrally without discarding the valid process", () => {
    const value = clone(); fm(value).checkpoint_evaluations = [];
    render(<ProcessPage result={value} />);
    expect(screen.getByRole("heading", { name: "Process timeline" })).toBeTruthy();
    expect(screen.getByText("No checkpoint evaluation records were produced.")).toBeTruthy();
    expect(screen.queryByText("UNRESOLVED")).toBeNull();
  });

  it("preserves checkpoint response order and exact process-state association", () => {
    const value = clone(); fm(value).checkpoint_evaluations.reverse();
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints.map((entry) => entry.kind === "AVAILABLE" ? entry.value.processStateVersion : "MALFORMED")).toEqual(["v2", "v1"]);
  });

  it.each([
    ["unknown checkpoint process", (c: Record<string, any>) => { c.process_state_ref = processRef("v9"); c.provenance.process_state_ref = c.process_state_ref; }],
    ["checkpoint artifact differs from state", (c: Record<string, any>) => { c.artifact_ref = artifact("other"); c.provenance.artifact_ref = c.artifact_ref; }],
    ["selected process differs", (c: Record<string, any>) => { c.selected_result.process_state_ref = processRef("other"); }],
    ["selected artifact differs", (c: Record<string, any>) => { c.selected_result.artifact_ref = artifact("other"); }],
    ["selected MetricEntry profile differs", (c: Record<string, any>) => { c.selected_result.result_ref.profile_id = metric("other"); c.provenance.selected_result_ref = c.selected_result.result_ref; }],
    ["selected metric identity differs", (c: Record<string, any>) => { c.selected_result.result_ref.metric_id = "OTHER"; c.provenance.selected_result_ref = c.selected_result.result_ref; }],
    ["invalid selected state pair", (c: Record<string, any>) => { c.selected_result.applicability = "UNKNOWN"; }],
    ["AVAILABLE selected result lacks Fraction", (c: Record<string, any>) => { c.selected_result.exact_value = null; }],
    ["non-AVAILABLE selected result has value", (c: Record<string, any>) => { c.selected_result.status = "UNKNOWN"; }],
  ])("isolates malformed checkpoint source/result: %s", (_label, mutate) => {
    const value = clone(); mutate(checkpoints(value)[0]);
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("MALFORMED");
    expect(projected.current.version).toBe("v2");
  });

  it("preserves policy identities, exact threshold, and distinct external/checkpoint contracts", () => {
    const projected = selectProcessPage(processResponse());
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE" || projected.checkpoints[0].kind !== "AVAILABLE") return;
    const item = projected.checkpoints[0].value;
    expect(item.policy.sourceRef).toEqual({ source_id: "POLICY-SOURCE", source_version: "3" });
    expect(item.policy.providerRef).toEqual({ provider_id: "POLICY-PROVIDER", provider_version: "2" });
    expect(item.policy.threshold).toEqual({ numerator: "1", denominator: "1" });
    expect(item.policy.governingContractRef).not.toEqual(item.checkpointContractRef);
  });

  it.each([
    ["empty policy source", (c: Record<string, any>) => { c.threshold_policy.source_ref.source_id = ""; }],
    ["empty policy provider", (c: Record<string, any>) => { c.threshold_policy.provider_ref.provider_id = ""; }],
    ["unsupported comparator", (c: Record<string, any>) => { c.threshold_policy.comparator = "!="; }],
    ["malformed threshold", (c: Record<string, any>) => { c.threshold_policy.threshold.denominator = 0; }],
    ["wrong checkpoint contract", (c: Record<string, any>) => { c.checkpoint_contract_ref.contract_id = "OTHER"; }],
    ["wrong evaluator rule", (c: Record<string, any>) => { c.evaluator_rule_ref.rule_id = "OTHER"; }],
    ["provenance policy ref mismatch", (c: Record<string, any>) => { c.provenance.threshold_policy_ref.policy_version = "other"; }],
    ["provenance selected ref mismatch", (c: Record<string, any>) => { c.provenance.selected_result_ref.metric_id = "OTHER"; }],
    ["provenance selected provenance mismatch", (c: Record<string, any>) => { c.provenance.selected_result_provenance = [{ other: true }]; }],
    ["provenance process mismatch", (c: Record<string, any>) => { c.provenance.process_state_ref.process_state_version = "other"; }],
    ["provenance artifact mismatch", (c: Record<string, any>) => { c.provenance.artifact_ref = artifact("other"); }],
  ])("isolates malformed checkpoint policy/provenance: %s", (_label, mutate) => {
    const value = clone(); mutate(checkpoints(value)[0]);
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("MALFORMED");
  });

  it.each([
    ["SATISFIED", "PREDICATE_TRUE", "AVAILABLE", "APPLICABLE"],
    ["NOT_SATISFIED", "PREDICATE_FALSE", "AVAILABLE", "APPLICABLE"],
    ["NOT_APPLICABLE", "SOURCE_NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE"],
    ["UNRESOLVED", "SOURCE_VALUE_UNRESOLVED", "UNKNOWN", "UNKNOWN"],
  ])("preserves canonical %s outcome with %s", (outcome, reason, status, applicability) => {
    const value = clone(); const item = checkpoints(value)[0];
    item.outcome = outcome; item.reason_codes = [reason]; item.selected_result.status = status; item.selected_result.applicability = applicability;
    if (status !== "AVAILABLE") item.selected_result.exact_value = null;
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE" || projected.checkpoints[0].kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].value.outcome).toBe(outcome);
    expect(projected.checkpoints[0].value.reasonCode).toBe(reason);
  });

  it("isolates invalid outcome/reason association", () => {
    const value = clone(); checkpoints(value)[0].outcome = "SATISFIED";
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.checkpoints[0].kind).toBe("MALFORMED");
  });

  it("never recomputes the backend outcome when threshold or selected exact value changes", () => {
    const value = clone(); const item = checkpoints(value)[1];
    item.threshold_policy.threshold = { numerator: 999, denominator: 1 };
    item.selected_result.exact_value = { numerator: -999, denominator: 1 };
    const projected = selectProcessPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE" || projected.checkpoints[1].kind !== "AVAILABLE") return;
    expect(projected.checkpoints[1].value.outcome).toBe("SATISFIED");
    expect(projected.checkpoints[1].value.policy.threshold).toEqual({ numerator: "999", denominator: "1" });
    expect(projected.checkpoints[1].value.selectedResult.exactValue).toEqual({ numerator: "-999", denominator: "1" });
  });

  it("renders the visible SATISFIED limitation without authorization wording", () => {
    render(<ProcessPage result={processResponse()} />);
    const satisfied = screen.getByText("SATISFIED").closest(".checkpoint-card") as HTMLElement;
    expect(within(satisfied).getByText(/means only that the configured predicate is true/)).toBeTruthy();
    expect(within(satisfied).getByText(/does not authorize RELEASE or PROCEED/)).toBeTruthy();
    expect(within(satisfied).queryByText(/approved|production ready|safe to deploy/i)).toBeNull();
  });

  it("renders historical v1 and successor v2 checkpoints as distinct cards", () => {
    render(<ProcessPage result={processResponse()} />);
    expect(screen.getByRole("heading", { name: /CHECKPOINT-v1/ })).toBeTruthy();
    expect(screen.getByRole("heading", { name: /CHECKPOINT-v2/ })).toBeTruthy();
  });

  it("INITIAL displays its canonical unavailable reason and fabricates no lifecycle records", () => {
    const value = clone(); value.analysis_case = "INITIAL"; value.controlled_scenario = null; value.full_model = null;
    value.section_availability = [{ section: "process", availability: "UNAVAILABLE", reason_code: "FULL_MODEL_LIFECYCLE_NOT_INVOKED" }];
    render(<ProcessPage result={value} />);
    expect(screen.getByRole("heading", { name: "Process" })).toBeTruthy();
    expect(screen.getByText("FULL_MODEL_LIFECYCLE_NOT_INVOKED")).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "Process timeline" })).toBeNull();
    expect(screen.queryByText("Current lifecycle successor")).toBeNull();
    expect(screen.queryByText("SATISFIED")).toBeNull();
  });

  it("keeps Audit deferred while Process routes to the real page", () => {
    const result = processResponse();
    const view = render(<ResultWorkspace result={result} activeView="process" selectedRequirementId={null} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Process timeline" })).toBeTruthy();
    view.rerender(<ResultWorkspace result={result} activeView="audit" selectedRequirementId={null} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Audit" })).toBeTruthy();
    expect(screen.getByText("Section implementation follows")).toBeTruthy();
  });

  it("Process navigation and locale switching perform no analysis request", async () => {
    const initial = clone(); initial.analysis_case = "INITIAL"; initial.controlled_scenario = null; initial.full_model = null;
    initial.section_availability = [{ section: "process", availability: "UNAVAILABLE", reason_code: "FULL_MODEL_LIFECYCLE_NOT_INVOKED" }];
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ ok: true, json: async () => initial } as Response);
    const client = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
    render(<QueryClientProvider client={client}><App /></QueryClientProvider>);
    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    await screen.findByRole("heading", { name: "Overview" });
    fireEvent.click(screen.getByRole("button", { name: "Process" }));
    expect(await screen.findByText("FULL_MODEL_LIFECYCLE_NOT_INVOKED")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));
    expect(await screen.findByRole("heading", { name: "Процес" })).toBeTruthy();
    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });
});

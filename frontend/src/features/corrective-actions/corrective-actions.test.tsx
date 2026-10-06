import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { i18n } from "../../i18n";
import { CorrectiveActionsPage } from "./CorrectiveActionsPage";
import { selectCorrectiveActionsPage } from "./projection";
import { createReassessmentDraft, createReassessmentRequest, matchesCanonicalRevision } from "./reassessmentDraft";

const actionRule = { rule_id: "ACTION-RECONCILE-QB-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const verificationRule = { rule_id: "REEVAL-FULL-MODEL-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const applicationRule = { rule_id: "APPLY-EXTERNAL-REVISION-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const fullModelContract = { contract_id: "FULL-MODEL-V0.1-CONTRACT", version: "1" };
const defectRiskContract = { contract_id: "FULL-MODEL-V0.1-DEFECT-QUALITY-RISK", version: "1" };
const processContract = { contract_id: "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", version: "1" };
const artifactV1 = { artifact_id: "SPEC", artifact_version: "v1" };
const artifactV2 = { artifact_id: "SPEC", artifact_version: "v2" };
const subject1v1 = { artifact_ref: artifactV1, requirement_id: "R001", source_line: 1 };
const subject2v1 = { artifact_ref: artifactV1, requirement_id: "R002", source_line: 3 };
const subject1v2 = { artifact_ref: artifactV2, requirement_id: "R001", source_line: 1 };
const subject2v2 = { artifact_ref: artifactV2, requirement_id: "R002", source_line: 3 };
const lineage1 = { artifact_id: "SPEC", origin_artifact_version: "v1", origin_requirement_id: "R001", origin_source_line: 1 };
const lineage2 = { artifact_id: "SPEC", origin_artifact_version: "v1", origin_requirement_id: "R002", origin_source_line: 3 };
const target1 = { lineage_id: lineage1, subject_ref: subject1v1 };
const target2 = { lineage_id: lineage2, subject_ref: subject2v1 };
const riskRef = { risk_assessment_id: { id: "RISK" } };
const problemRef = { problem_id: { id: "PROBLEM" } };
const relationRef = { relation_id: { id: "RELATION" } };
const actionId = { action_instance_id: "ACTION", rule_ref: actionRule, originating_risk_id: riskRef.risk_assessment_id, originating_problem_id: problemRef.problem_id, target_artifact_ref: artifactV1 };
const actionRef = { action_id: actionId, action_record_version: "1" };
const revisionRef = { revision_id: "REVISION", revision_version: "1" };
const applicationId = { application_instance_id: "APPLICATION", action_before_ref: actionRef, revision_ref: revisionRef, child_artifact_ref: artifactV2 };
const applicationRef = { application_id: applicationId, application_version: "1" };
const actionAfterRef = { action_id: actionId, action_record_version: "2" };
const comparisonKey = { normalized_metric: "response time", normalized_context: "500 users", unit: "SECOND" };
const changedSubject = { lineage_id: lineage2, before_subject_ref: subject2v1, after_subject_ref: subject2v2, change_kind: "REPLACE_TEXT" };

function ruiRequirement(id: string, sourceLine: number, requirementText: string) {
  const feature = (featureId: string) => ({ feature_id: featureId, status: "NOT_DETECTED", processing_status: "COMPLETE", observations: [], diagnostics: [] });
  const assessment = (characteristicId: string) => ({ characteristic_id: characteristicId, state: "COMPUTED", value: { numerator: 1, denominator: 1 }, assessment_rule_id: `RULE-${characteristicId}`, findings: [], explanation: "Canonical explanation." });
  const trace = (characteristicId: string) => ({ characteristic_id: characteristicId, governing_rule_id: `RULE-${characteristicId}`, decision_code: `${characteristicId}_DECISION`, inputs: [], finding_refs: [] });
  return {
    requirement: { id, source_line: sourceLine, text: requirementText },
    features: {
      condition_contexts: feature("condition_context"), expected_results: feature("expected_result"), acceptance_criteria: feature("acceptance_criterion"),
      quantitative_constraints: feature("quantitative_constraint"), verification_methods: feature("verification_method"), vague_term_occurrences: feature("vague_term_occurrence"),
    },
    evidence: [],
    quality_profile: { completeness: assessment("COMPLETENESS"), verifiability: assessment("VERIFIABILITY"), unambiguity: assessment("UNAMBIGUITY") },
    trace: { requirement_id: id, coverage_profile_id: "MVP-V0.1-BOUNDED-CVU-001", characteristics: [trace("COMPLETENESS"), trace("VERIFIABILITY"), trace("UNAMBIGUITY")] },
  };
}

function initialSpecification() {
  return {
    status: null, applicability: null,
    provenance: { artifact_ref: artifactV1, parent_artifact_ref: null, application_ref: null, revision_ref: null, process_reassessment_contract_ref: processContract, application_rule_ref_or_none: null },
    artifact_ref: artifactV1, parent_artifact_ref: null, created_by_application_ref: null,
    requirements: [
      { lineage_id: lineage1, subject_ref: subject1v1, text: "Response time <= 2 s", predecessor_subject_ref: null },
      { lineage_id: lineage2, subject_ref: subject2v1, text: "Response time >= 5 s", predecessor_subject_ref: null },
    ],
    changed_subjects: [],
  };
}

function revisedSpecification() {
  return {
    status: null, applicability: null,
    provenance: { artifact_ref: artifactV2, parent_artifact_ref: artifactV1, application_ref: applicationRef, revision_ref: revisionRef, process_reassessment_contract_ref: processContract, application_rule_ref_or_none: applicationRule },
    artifact_ref: artifactV2, parent_artifact_ref: artifactV1, created_by_application_ref: applicationRef,
    requirements: [
      { lineage_id: lineage1, subject_ref: subject1v2, text: "Response time <= 2 s", predecessor_subject_ref: subject1v1 },
      { lineage_id: lineage2, subject_ref: subject2v2, text: "Response time <= 5 s", predecessor_subject_ref: subject2v1 },
    ],
    changed_subjects: [changedSubject],
  };
}

function proposal() {
  return {
    action_id: actionId, action_record_version: "1", predecessor_action_ref: null,
    action_kind: "RECONCILE_QUANTITATIVE_BOUNDS", status: "PROPOSED", rule_ref: actionRule,
    originating_risk_ref: riskRef, originating_problem_ref: problemRef, originating_relation_ref: relationRef,
    target_artifact_ref: artifactV1, target_requirements: [target1, target2], comparison_key: comparisonKey,
    rationale: "The two target requirements contain an exact QB-v0.1 confirmed conflict on the same complete quantitative comparison key. Stakeholder reconciliation is requested because the system cannot determine which bound expresses intent.",
    proposed_change_kind: "REPLACE_REQUIREMENT_TEXT",
    expected_bounded_outcome: "A later rerun may no longer identify that exact confirmed conflict.",
    verification_rule_ref: verificationRule, external_revision_ref: null, application_ref: null, rejection_source_ref: null,
    creator_source: { source_id: "FULL_MODEL_SERVICE", source_version: "1" },
    provenance: {
      originating_risk_ref: riskRef, originating_problem_ref: problemRef, originating_relation_ref: relationRef,
      problem_resolution_ref: { id: "RESOLUTION" }, defect_population_ref: { id: "POPULATION" }, source_cross_result_ref: { id: "CROSS" },
      participant_refs: [subject1v1, subject2v1], target_requirements: [target1, target2], comparison_key: comparisonKey,
      ordered_evidence_refs: [{ requirement_id: "R001", evidence_id: "E1" }, { requirement_id: "R002", evidence_id: "E2" }],
      artifact_ref: artifactV1, source_assessment_ref: { id: "ASSESS" }, source_snapshot_id: { id: "SNAPSHOT" }, process_state_ref: { id: "PROCESS-v1" },
      full_model_contract_ref: fullModelContract, defect_risk_contract_ref: defectRiskContract, process_reassessment_contract_ref: processContract,
      problem_rule_ref: { id: "PROBLEM_RULE" }, relation_rule_ref: { id: "RELATION_RULE" }, risk_model_ref: { id: "RISK_MODEL" }, risk_rule_ref: { id: "RISK_RULE" }, risk_parameter_set_ref: { id: "PARAMETERS" },
      action_rule_ref: actionRule, verification_rule_ref: verificationRule,
    },
    non_optimality_claim: "CANDIDATE_NOT_OPTIMALITY_CLAIM",
  };
}

function fixture(caseName: CanonicalAnalyzeResponse["analysis_case"] = "CONTROLLED_DEMO"): CanonicalAnalyzeResponse {
  const initial = initialSpecification();
  const revised = revisedSpecification();
  const action = proposal();
  const resolution = {
    status: "AVAILABLE", applicability: "APPLICABLE",
    provenance: {
      source_risk_ref: riskRef, source_problem_ref: problemRef, source_relation_ref: relationRef,
      artifact_ref: artifactV1, source_assessment_ref: { id: "ASSESS" }, source_snapshot_id: { id: "SNAPSHOT" }, process_state_ref: { id: "PROCESS-v1" },
      participant_refs: [subject1v1, subject2v1], target_requirements: [target1, target2], ordered_evidence_refs: action.provenance.ordered_evidence_refs,
      full_model_contract_ref: fullModelContract, defect_risk_contract_ref: defectRiskContract, process_reassessment_contract_ref: processContract,
      source_risk_model_ref: { id: "RISK_MODEL" }, source_risk_rule_ref: { id: "RISK_RULE" }, source_risk_parameter_set_ref: { id: "PARAMETERS" }, action_rule_ref: actionRule,
    },
    resolution_id: { action_instance_id: "ACTION", source_risk_ref: riskRef, requested_action_kind: "RECONCILE_QUANTITATIVE_BOUNDS", rule_ref: actionRule },
    action_ref: actionRef, reason_codes: ["ELIGIBLE_RISK_IDENTIFIED"], source_risk_ref: riskRef, source_problem_ref: problemRef, source_relation_ref: relationRef, rule_ref: actionRule, action,
  };
  const externalRevision = {
    status: null, applicability: null,
    provenance: { revision_ref: revisionRef, action_ref: actionRef, parent_artifact_ref: artifactV1, requested_child_artifact_ref: artifactV2, provider_ref: { provider_id: "REFERENCE_FIXTURE", provider_version: "1" }, process_reassessment_contract_ref: processContract, application_rule_ref: applicationRule },
    revision_id: "REVISION", revision_version: "1", provider_kind: "CONTROLLED_REFERENCE_FIXTURE", provider_ref: { provider_id: "REFERENCE_FIXTURE", provider_version: "1" },
    action_ref: actionRef, parent_artifact_ref: artifactV1, requested_child_artifact_ref: artifactV2,
    replacements: [{ lineage_id: lineage2, expected_parent_subject_ref: subject2v1, replacement_text: "Response time <= 5 s" }], provider_rationale_or_none: "Externally supplied reference revision.",
  };
  const childSpecification = (({ status: _status, applicability: _applicability, ...rest }) => rest)(structuredClone(revised));
  const application = {
    status: "AVAILABLE", applicability: null,
    provenance: { action_before_ref: actionRef, action_after_ref: actionAfterRef, revision_ref: revisionRef, provider_ref: externalRevision.provider_ref, parent_artifact_ref: artifactV1, child_artifact_ref: artifactV2, application_rule_ref: applicationRule, process_reassessment_contract_ref: processContract },
    application_id: applicationId, application_version: "1", action_before_ref: actionRef, action_after_ref: actionAfterRef, revision_ref: revisionRef,
    parent_artifact_ref: artifactV1, child_artifact_ref: artifactV2, changed_subjects: [changedSubject], rule_ref: applicationRule,
    reason_codes: ["EXTERNAL_REVISION_MATERIALIZED"],
    applied_action: { ...action, action_record_version: "2", predecessor_action_ref: actionRef, status: "APPLIED", external_revision_ref: revisionRef, application_ref: applicationRef },
    child_specification: childSpecification,
    transition: {
      transition_id: { transition_instance_id: "TRANSITION", application_ref: applicationRef },
      parent_artifact_ref: artifactV1, child_artifact_ref: artifactV2, action_application_ref: applicationRef, revision_ref: revisionRef, changed_subjects: [changedSubject],
      provenance: { action_before_ref: actionRef, action_after_ref: actionAfterRef, application_ref: applicationRef, revision_ref: revisionRef, process_reassessment_contract_ref: processContract, application_rule_ref: applicationRule },
    },
  };
  const processV1 = { process_state_id: "PROCESS", process_state_version: "v1", stage: "REFERENCE_VERIFICATION" };
  const processV2 = { process_state_id: "PROCESS", process_state_version: "v2", stage: "REFERENCE_VERIFICATION" };
  const componentVersionSet = { components: [{ component_role: "FULL_MODEL_CONTRACT", component_id: "FULL-MODEL-V0.1-CONTRACT", component_version: "1" }] };
  const evidenceReuseDecisions = [{ id: "EVIDENCE-REUSE" }];
  const reassessmentIdentity = { reassessment_id: "REASSESSMENT", reassessment_version: "1", child_process_state_ref: processV2, component_version_set: componentVersionSet };
  const reassessment = {
    reassessment_id: "REASSESSMENT", reassessment_version: "1", child_process_state_ref: processV2,
    context: { predecessor_process_state_ref: processV1, action_application_ref: applicationRef, parent_artifact_ref: artifactV1, child_artifact_ref: artifactV2, component_version_set: componentVersionSet, evidence_reuse_decisions: evidenceReuseDecisions },
  };
  const fullModel: Record<string, unknown> = {
    initial_specification_assessment: { id: "INITIAL_ASSESSMENT" }, corrective_action_resolution: resolution,
    initial_specification: initial, revised_specification: revised, external_revision: externalRevision, action_application: application,
    risk_assessments: [{ risk_assessment_id: riskRef.risk_assessment_id }],
    problem_resolutions: [{ problem: { problem_id: problemRef.problem_id } }],
    defect_quality_relations: [{ relation_id: relationRef.relation_id }],
    process_v1: processV1, process_v2: processV2, process_transition: { id: "PROCESS-TRANSITION" }, comparisons: [{ id: "COMPARISON" }], reassessment,
  };
  const scenario = { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" };
  const context = {
    scenario, context_digest: "sha256:context", initial_specification: initial, initial_specification_assessment: fullModel.initial_specification_assessment,
    predecessor_process_state: fullModel.process_v1, corrective_action_resolution: resolution, action_application: application,
    external_revision: externalRevision, revised_specification: revised, evidence_reuse_decisions: evidenceReuseDecisions, reassessment_identity: reassessmentIdentity,
    successor_process_state: fullModel.process_v2, process_transition: fullModel.process_transition, comparisons: fullModel.comparisons,
  };
  return {
    contract_version: "research-api-v1", analysis_case: caseName, controlled_scenario: scenario,
    requirements: (caseName === "REASSESSMENT" ? revised.requirements : initial.requirements).map((item) => ruiRequirement(item.subject_ref.requirement_id, item.subject_ref.source_line, item.text)),
    specification: { snapshot_id: "snapshot", quality_profile: {}, qb_consistency: {}, cross_results: [], materiality: {}, projection_snapshot: {} },
    section_availability: [{ section: "corrective_actions", availability: "AVAILABLE", reason_code: null }],
    full_model: fullModel, reassessment_context: context, limitations: [],
  };
}

function cloneFixture(caseName: CanonicalAnalyzeResponse["analysis_case"] = "CONTROLLED_DEMO") {
  return structuredClone(fixture(caseName));
}

function fullModel(response: CanonicalAnalyzeResponse): Record<string, any> {
  return response.full_model as Record<string, any>;
}

function context(response: CanonicalAnalyzeResponse): Record<string, any> {
  return response.reassessment_context as Record<string, any>;
}

function renderPage(response: CanonicalAnalyzeResponse, props: Partial<React.ComponentProps<typeof CorrectiveActionsPage>> = {}) {
  const onSelectRequirement = vi.fn();
  const onAnalyzeReassessment = vi.fn();
  render(<CorrectiveActionsPage result={response} onSelectRequirement={onSelectRequirement} onAnalyzeReassessment={onAnalyzeReassessment} {...props} />);
  return { onSelectRequirement, onAnalyzeReassessment };
}

describe("RUI-12 corrective-action projection", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(() => { cleanup(); vi.restoreAllMocks(); });

  it("renders ordinary INITIAL unavailability without lifecycle fabrication or reassessment entry", () => {
    const response = cloneFixture("INITIAL");
    response.full_model = null;
    response.controlled_scenario = null;
    response.reassessment_context = null;
    response.section_availability = [{ section: "corrective_actions", availability: "UNAVAILABLE", reason_code: "CONFIRMED_PROBLEM_NOT_AVAILABLE" }];
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    renderPage(response);
    expect(screen.getByText("CONFIRMED_PROBLEM_NOT_AVAILABLE")).toBeTruthy();
    expect(screen.queryByText("Proposed action")).toBeNull();
    expect(screen.queryByText("External revision")).toBeNull();
    expect(screen.queryByText("Action application")).toBeNull();
    expect(screen.queryByRole("button", { name: "Reassess revised specification" })).toBeNull();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("projects the canonical proposal, revision, application, and explicit changed lineage", () => {
    const projected = selectCorrectiveActionsPage(fixture());
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.resolution.reasonCode).toBe("ELIGIBLE_RISK_IDENTIFIED");
    expect(projected.resolution.action).toMatchObject({ actionKind: "RECONCILE_QUANTITATIVE_BOUNDS", proposedChangeKind: "REPLACE_REQUIREMENT_TEXT", nonOptimalityClaim: "CANDIDATE_NOT_OPTIMALITY_CLAIM" });
    expect(projected.resolution.action?.verificationRuleRef).toEqual(verificationRule);
    expect(projected.externalRevision?.providerKind).toBe("CONTROLLED_REFERENCE_FIXTURE");
    expect(projected.application).toMatchObject({ status: "AVAILABLE", reasonCode: "EXTERNAL_REVISION_MATERIALIZED", appliedActionVersion: "2" });
    expect(projected.changedRequirements.map((item) => item.changeKind)).toEqual(["REPLACE_TEXT"]);
    expect(projected.reassessment).not.toBeNull();
  });

  it.each([
    ["AVAILABLE/UNKNOWN", (r: any) => { r.status = "AVAILABLE"; r.applicability = "UNKNOWN"; }],
    ["NOT_APPLICABLE/APPLICABLE", (r: any) => { r.status = "NOT_APPLICABLE"; r.applicability = "APPLICABLE"; }],
    ["fabricated reason", (r: any) => { r.reason_codes = ["NOTHING_NEEDS_FIXING"]; }],
    ["multiple reasons", (r: any) => { r.reason_codes.push("SOURCE_UNAVAILABLE"); }],
    ["wrong action rule", (r: any) => { r.rule_ref = { ...actionRule, rule_id: "OTHER" }; }],
    ["missing available action", (r: any) => { r.action = null; }],
  ])("rejects malformed resolution: %s", (_label, mutate) => {
    const response = cloneFixture();
    mutate(fullModel(response).corrective_action_resolution);
    expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
  });

  it("accepts non-AVAILABLE only without action/action_ref and does not reinterpret it", () => {
    const response = cloneFixture();
    const resolution = fullModel(response).corrective_action_resolution;
    resolution.status = "UNAVAILABLE";
    resolution.applicability = "UNKNOWN";
    resolution.reason_codes = ["SOURCE_UNAVAILABLE"];
    resolution.action = null;
    resolution.action_ref = null;
    const projected = selectCorrectiveActionsPage(response);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind === "AVAILABLE") expect(projected.resolution.action).toBeNull();
  });

  it.each([
    ["one target", (a: any) => { a.target_requirements = [a.target_requirements[0]]; }],
    ["revision ref on proposal", (a: any) => { a.external_revision_ref = revisionRef; }],
    ["application ref on proposal", (a: any) => { a.application_ref = applicationRef; }],
    ["predecessor on proposal", (a: any) => { a.predecessor_action_ref = actionRef; }],
    ["source risk mismatch", (a: any) => { a.originating_risk_ref = { id: "OTHER" }; }],
    ["source problem mismatch", (a: any) => { a.originating_problem_ref = { id: "OTHER" }; }],
    ["source relation mismatch", (a: any) => { a.originating_relation_ref = { id: "OTHER" }; }],
    ["provenance targets mismatch", (a: any) => { a.provenance.target_requirements.reverse(); }],
    ["provenance comparison mismatch", (a: any) => { a.provenance.comparison_key = { id: "OTHER" }; }],
    ["verification rule mismatch", (a: any) => { a.verification_rule_ref = { ...verificationRule, rule_id: "OTHER" }; }],
  ])("rejects malformed proposed action: %s", (_label, mutate) => {
    const response = cloneFixture();
    mutate(fullModel(response).corrective_action_resolution.action);
    expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
  });

  it("keeps the expected outcome bounded and renders no guaranteed quality claim", () => {
    renderPage(fixture());
    expect(screen.getByText("A later rerun may no longer identify that exact confirmed conflict.")).toBeTruthy();
    expect(screen.getByText(/not a guarantee of effectiveness/i)).toBeTruthy();
    expect(screen.queryByText(/guaranteed improvement|recommended improvement/i)).toBeNull();
  });

  it("navigates a controlled-demo v1 target only when the visible Requirement is its exact subject", () => {
    const { onSelectRequirement } = renderPage(fixture());
    fireEvent.click(screen.getByRole("button", { name: "R001" }));
    expect(onSelectRequirement).toHaveBeenCalledWith("R001");
  });

  it("does not navigate a historical v1 target from a REASSESSMENT v2 result", () => {
    renderPage(fixture("REASSESSMENT"));
    expect(screen.queryByRole("button", { name: "R001" })).toBeNull();
    expect(screen.getAllByText("R001").length).toBeGreaterThan(0);
    expect(screen.queryByRole("button", { name: "Reassess revised specification" })).toBeNull();
  });

  it.each([
    ["unsupported provider", (r: any) => { r.provider_kind = "SYSTEM"; }],
    ["wrong action", (r: any) => { r.action_ref = { id: "OTHER" }; }],
    ["wrong parent", (r: any) => { r.parent_artifact_ref = artifactV2; }],
    ["wrong child", (r: any) => { r.requested_child_artifact_ref = artifactV1; }],
    ["non-target replacement", (r: any) => { r.replacements[0].lineage_id = { id: "OTHER" }; }],
    ["duplicate lineage", (r: any) => { r.replacements.push(structuredClone(r.replacements[0])); }],
    ["wrong expected parent", (r: any) => { r.replacements[0].expected_parent_subject_ref = subject1v1; }],
  ])("rejects malformed external revision: %s", (_label, mutate) => {
    const response = cloneFixture();
    mutate(fullModel(response).external_revision);
    expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
  });

  it("preserves exact external replacement text and does not translate it", async () => {
    renderPage(fixture());
    expect(screen.getAllByText("Response time <= 5 s")).toHaveLength(2);
    await i18n.changeLanguage("uk");
    expect(await screen.findAllByText("Response time <= 5 s")).toHaveLength(2);
  });

  it.each([
    ["initial parent", (m: any) => { m.initial_specification.parent_artifact_ref = artifactV1; }],
    ["initial changed subject", (m: any) => { m.initial_specification.changed_subjects = [changedSubject]; }],
    ["revised parent", (m: any) => { m.revised_specification.parent_artifact_ref = artifactV2; }],
    ["same artifact version", (m: any) => { m.revised_specification.artifact_ref.artifact_version = "v1"; }],
    ["reordered lineage", (m: any) => { m.revised_specification.requirements.reverse(); }],
    ["unresolved changed subject", (m: any) => { m.revised_specification.changed_subjects[0].after_subject_ref = subject1v2; }],
  ])("rejects malformed specification lineage: %s", (_label, mutate) => {
    const response = cloneFixture();
    mutate(fullModel(response));
    expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
  });

  it("uses changed_subjects as authority rather than inferring by text comparison", () => {
    const response = cloneFixture();
    fullModel(response).revised_specification.requirements[1].text = "Response time >= 5 s";
    fullModel(response).external_revision.replacements[0].replacement_text = "Response time >= 5 s";
    fullModel(response).action_application.child_specification.requirements[1].text = "Response time >= 5 s";
    const projected = selectCorrectiveActionsPage(response);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind === "AVAILABLE") expect(projected.changedRequirements).toHaveLength(1);
  });

  it.each([
    ["wrong application rule", (a: any) => { a.rule_ref = { ...applicationRule, rule_id: "OTHER" }; }],
    ["non-AVAILABLE application", (a: any) => { a.status = "UNRESOLVED"; }],
    ["wrong reason", (a: any) => { a.reason_codes = ["ACTION_EFFECTIVE"]; }],
    ["wrong action before", (a: any) => { a.action_before_ref = actionAfterRef; }],
    ["wrong applied predecessor", (a: any) => { a.applied_action.predecessor_action_ref = actionAfterRef; }],
    ["wrong child specification", (a: any) => { a.child_specification.requirements[1].text = "Other"; }],
    ["changed-subject disagreement", (a: any) => { a.transition.changed_subjects = []; }],
  ])("rejects malformed ActionApplication: %s", (_label, mutate) => {
    const response = cloneFixture();
    mutate(fullModel(response).action_application);
    expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
  });

  it("renders APPLIED as materialization without causal effectiveness semantics", () => {
    renderPage(fixture());
    expect(screen.getByText("EXTERNAL_REVISION_MATERIALIZED")).toBeTruthy();
    expect(screen.getByText(/means only that the external revision was materialized/i)).toBeTruthy();
  });

  it.each([
    ["context digest", (r: CanonicalAnalyzeResponse) => { context(r).context_digest = ""; }],
    ["predecessor process", (r: CanonicalAnalyzeResponse) => { delete context(r).predecessor_process_state; }],
    ["action application", (r: CanonicalAnalyzeResponse) => { delete context(r).action_application; }],
    ["external revision", (r: CanonicalAnalyzeResponse) => { delete context(r).external_revision; }],
    ["evidence decisions", (r: CanonicalAnalyzeResponse) => { context(r).evidence_reuse_decisions = {}; }],
    ["reassessment identity", (r: CanonicalAnalyzeResponse) => { delete context(r).reassessment_identity; }],
    ["revised counterpart", (r: CanonicalAnalyzeResponse) => { context(r).revised_specification = { id: "OTHER" }; }],
    ["application counterpart", (r: CanonicalAnalyzeResponse) => { context(r).action_application = { id: "OTHER" }; }],
    ["scenario identity", (r: CanonicalAnalyzeResponse) => { context(r).scenario = { id: "OTHER", version: "1" }; }],
  ])("disables formal reassessment when %s is invalid", (_label, mutate) => {
    const response = cloneFixture();
    mutate(response);
    const projected = selectCorrectiveActionsPage(response);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind === "AVAILABLE") expect(projected.reassessment).toBeNull();
  });

  describe("final lifecycle identity hardening", () => {
    it.each([
      ["initial subject artifact", (m: any) => { m.initial_specification.requirements[0].subject_ref.artifact_ref = artifactV2; }],
      ["revised subject still v1", (m: any) => { m.revised_specification.requirements[0].subject_ref.artifact_ref = artifactV1; }],
      ["initial source order", (m: any) => { m.initial_specification.requirements.reverse(); }],
      ["revised source order", (m: any) => { m.revised_specification.requirements.reverse(); }],
    ])("rejects malformed SpecificationVersion ownership/order: %s", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response));
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it("rejects a structurally coherent action target absent from the initial specification", () => {
      const response = cloneFixture();
      const action = fullModel(response).corrective_action_resolution.action;
      const resolution = fullModel(response).corrective_action_resolution;
      const absentSubject = { artifact_ref: artifactV1, requirement_id: "R999", source_line: 9 };
      const absentLineage = { artifact_id: "SPEC", origin_artifact_version: "v1", origin_requirement_id: "R999", origin_source_line: 9 };
      const absentTarget = { lineage_id: absentLineage, subject_ref: absentSubject };
      action.target_requirements[0] = absentTarget;
      action.provenance.target_requirements[0] = absentTarget;
      action.provenance.participant_refs[0] = absentSubject;
      resolution.provenance.target_requirements[0] = absentTarget;
      resolution.provenance.participant_refs[0] = absentSubject;
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["source risk", (id: any) => { id.source_risk_ref = { risk_assessment_id: { id: "OTHER" } }; }],
      ["action kind", (id: any) => { id.requested_action_kind = "OTHER"; }],
      ["rule", (id: any) => { id.rule_ref = { ...actionRule, rule_id: "OTHER" }; }],
    ])("rejects contradictory resolution_id %s", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response).corrective_action_resolution.resolution_id);
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it("validates provenance sources for a non-AVAILABLE resolution", () => {
      const response = cloneFixture();
      const resolution = fullModel(response).corrective_action_resolution;
      resolution.status = "UNAVAILABLE";
      resolution.applicability = "UNKNOWN";
      resolution.reason_codes = ["SOURCE_UNAVAILABLE"];
      resolution.action = null;
      resolution.action_ref = null;
      resolution.provenance.source_risk_ref = { risk_assessment_id: { id: "OTHER" } };
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["missing", (action: any) => { delete action.rejection_source_ref; }],
      ["non-null", (action: any) => { action.rejection_source_ref = { source_id: "REJECTION" }; }],
    ])("rejects a PROPOSED action with %s rejection_source_ref", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response).corrective_action_resolution.action);
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["missing", (action: any) => { delete action.rejection_source_ref; }],
      ["non-null", (action: any) => { action.rejection_source_ref = { source_id: "REJECTION" }; }],
    ])("rejects an APPLIED action with %s rejection_source_ref", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response).action_application.applied_action);
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["null", null],
      ["malformed", "RELATION"],
    ])("rejects a non-AVAILABLE resolution with %s source_relation_ref", (_label, value) => {
      const response = cloneFixture();
      const resolution = fullModel(response).corrective_action_resolution;
      resolution.status = "UNAVAILABLE";
      resolution.applicability = "UNKNOWN";
      resolution.reason_codes = ["SOURCE_UNAVAILABLE"];
      resolution.action = null;
      resolution.action_ref = null;
      resolution.source_relation_ref = value;
      resolution.provenance.source_relation_ref = value;
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["risk", (resolution: any) => {
        const unknown = { risk_assessment_id: { id: "OTHER" } };
        resolution.source_risk_ref = unknown;
        resolution.resolution_id.source_risk_ref = unknown;
        resolution.provenance.source_risk_ref = unknown;
      }],
      ["relation", (resolution: any) => {
        const unknown = { relation_id: { id: "OTHER" } };
        resolution.source_relation_ref = unknown;
        resolution.provenance.source_relation_ref = unknown;
      }],
      ["problem", (resolution: any) => {
        const unknown = { problem_id: { id: "OTHER" } };
        resolution.source_problem_ref = unknown;
        resolution.provenance.source_problem_ref = unknown;
      }],
    ])("rejects a non-AVAILABLE resolution with an unknown %s reference", (_label, mutate) => {
      const response = cloneFixture();
      const resolution = fullModel(response).corrective_action_resolution;
      resolution.status = "UNAVAILABLE";
      resolution.applicability = "UNKNOWN";
      resolution.reason_codes = ["SOURCE_UNAVAILABLE"];
      resolution.action = null;
      resolution.action_ref = null;
      mutate(resolution);
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["risk", (model: any) => { model.risk_assessments.push(structuredClone(model.risk_assessments[0])); }],
      ["relation", (model: any) => { model.defect_quality_relations.push(structuredClone(model.defect_quality_relations[0])); }],
      ["problem", (model: any) => { model.problem_resolutions.push(structuredClone(model.problem_resolutions[0])); }],
    ])("rejects a resolution whose %s reference has multiple top-level matches", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response));
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it("accepts canonical non-AVAILABLE resolution sources with an explicit null problem", () => {
      const response = cloneFixture();
      const resolution = fullModel(response).corrective_action_resolution;
      resolution.status = "UNAVAILABLE";
      resolution.applicability = "UNKNOWN";
      resolution.reason_codes = ["SOURCE_UNAVAILABLE"];
      resolution.action = null;
      resolution.action_ref = null;
      resolution.source_problem_ref = null;
      resolution.provenance.source_problem_ref = null;
      const projected = selectCorrectiveActionsPage(response);
      expect(projected.kind).toBe("AVAILABLE");
      if (projected.kind === "AVAILABLE") {
        expect(projected.resolution.sourceProblemRef).toBeNull();
        expect(projected.resolution.sourceRiskRef).toEqual(riskRef);
        expect(projected.resolution.sourceRelationRef).toEqual(relationRef);
        expect(projected.resolution.action).toBeNull();
      }
    });

    it("accepts the canonical AVAILABLE chain with explicit null rejection references", () => {
      const projected = selectCorrectiveActionsPage(fixture());
      expect(projected.kind).toBe("AVAILABLE");
      if (projected.kind === "AVAILABLE") {
        expect(projected.resolution.action?.raw.rejection_source_ref).toBeNull();
        expect(projected.application).not.toBeNull();
      }
    });

    it.each([
      ["risk", (id: any) => { id.originating_risk_id = { id: "OTHER" }; }],
      ["problem", (id: any) => { id.originating_problem_id = { id: "OTHER" }; }],
      ["target artifact", (id: any) => { id.target_artifact_ref = artifactV2; }],
    ])("rejects contradictory structured action_id %s identity", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response).corrective_action_resolution.action.action_id);
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it("rejects proposal participant order differing from target order", () => {
      const response = cloneFixture();
      fullModel(response).corrective_action_resolution.action.provenance.participant_refs.reverse();
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["empty population", (m: any) => { m.external_revision.replacements = []; }],
      ["line break", (m: any) => { m.external_revision.replacements[0].replacement_text = "Line one\nLine two"; }],
      ["text differs from child", (m: any) => { m.external_revision.replacements[0].replacement_text = "Other text"; }],
      ["non-replaced child text changed", (m: any) => { m.revised_specification.requirements[0].text = "Changed without replacement"; }],
    ])("rejects malformed revision replacement coherence: %s", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response));
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it("rejects replacement population that does not explain canonical changed subjects", () => {
      const response = cloneFixture();
      fullModel(response).external_revision.replacements = [{ lineage_id: lineage1, expected_parent_subject_ref: subject1v1, replacement_text: "Response time <= 2 s" }];
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it("rejects a changed subject without a corresponding replacement", () => {
      const response = cloneFixture();
      const extra = { lineage_id: lineage1, before_subject_ref: subject1v1, after_subject_ref: subject1v2, change_kind: "REPLACE_TEXT" };
      fullModel(response).revised_specification.changed_subjects.unshift(extra);
      fullModel(response).action_application.changed_subjects.unshift(extra);
      fullModel(response).action_application.transition.changed_subjects.unshift(extra);
      fullModel(response).action_application.child_specification.changed_subjects.unshift(extra);
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["action-before", (id: any) => { id.action_before_ref = actionAfterRef; }],
      ["revision", (id: any) => { id.revision_ref = { revision_id: "OTHER", revision_version: "1" }; }],
      ["child", (id: any) => { id.child_artifact_ref = artifactV1; }],
    ])("rejects contradictory ActionApplicationId %s identity", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response).action_application.application_id);
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["targets", (applied: any) => { applied.target_requirements.reverse(); }],
      ["comparison key", (applied: any) => { applied.comparison_key = { id: "OTHER" }; }],
      ["rationale", (applied: any) => { applied.rationale = "Other rationale"; }],
    ])("rejects APPLIED action with changed %s", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response).action_application.applied_action);
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it("rejects application provenance from another provider", () => {
      const response = cloneFixture();
      fullModel(response).action_application.provenance.provider_ref = { provider_id: "OTHER", provider_version: "1" };
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it.each([
      ["transition ID application", (a: any) => { a.transition.transition_id.application_ref = { id: "OTHER" }; }],
      ["provenance action-before", (a: any) => { a.transition.provenance.action_before_ref = actionAfterRef; }],
      ["provenance action-after", (a: any) => { a.transition.provenance.action_after_ref = actionRef; }],
      ["provenance contract", (a: any) => { a.transition.provenance.process_reassessment_contract_ref = { contract_id: "OTHER", version: "1" }; }],
      ["provenance rule", (a: any) => { a.transition.provenance.application_rule_ref = { ...applicationRule, rule_id: "OTHER" }; }],
    ])("rejects malformed ArtifactTransition %s", (_label, mutate) => {
      const response = cloneFixture();
      mutate(fullModel(response).action_application);
      expect(selectCorrectiveActionsPage(response).kind).toBe("MALFORMED");
    });

    it("keeps a malformed RUI-08 entry non-navigable", () => {
      const response = cloneFixture();
      delete (response.requirements[0] as any).quality_profile;
      renderPage(response);
      expect(screen.queryByRole("button", { name: "R001" })).toBeNull();
      expect(screen.getByRole("button", { name: "R002" })).toBeTruthy();
    });

    it.each([
      ["evidence reuse", (r: CanonicalAnalyzeResponse) => { context(r).evidence_reuse_decisions = [{ id: "OTHER" }]; }],
      ["identity ID", (r: CanonicalAnalyzeResponse) => { context(r).reassessment_identity.reassessment_id = "OTHER"; }],
      ["identity version", (r: CanonicalAnalyzeResponse) => { context(r).reassessment_identity.reassessment_version = "2"; }],
      ["child process", (r: CanonicalAnalyzeResponse) => { context(r).reassessment_identity.child_process_state_ref = { id: "OTHER" }; }],
      ["component versions", (r: CanonicalAnalyzeResponse) => { context(r).reassessment_identity.component_version_set = { components: [] }; }],
      ["controlled scenario", (r: CanonicalAnalyzeResponse) => {
        r.controlled_scenario = { id: "UNKNOWN", version: "1" };
        context(r).scenario = { id: "UNKNOWN", version: "1" };
      }],
    ])("disables reassessment entry for mismatched %s", (_label, mutate) => {
      const response = cloneFixture();
      mutate(response);
      const projected = selectCorrectiveActionsPage(response);
      expect(projected.kind).toBe("AVAILABLE");
      if (projected.kind === "AVAILABLE") expect(projected.reassessment).toBeNull();
    });

    it("keeps the complete canonical controlled lifecycle eligible", () => {
      const projected = selectCorrectiveActionsPage(fixture());
      expect(projected.kind).toBe("AVAILABLE");
      if (projected.kind === "AVAILABLE") expect(projected.reassessment).not.toBeNull();
    });
  });
});

describe("RUI-12 canonical revised-specification editor", () => {
  beforeEach(async () => { await i18n.changeLanguage("en"); });
  afterEach(() => { cleanup(); vi.restoreAllMocks(); });

  it("reconstructs blank source-line gaps without silently renumbering", () => {
    const requirements = [{ text: "First", source_line: 1 }, { text: "Third", source_line: 3 }];
    expect(createReassessmentDraft(requirements)).toBe("First\n\nThird");
    expect(matchesCanonicalRevision("First\n\nThird", requirements)).toBe(true);
    expect(matchesCanonicalRevision("First\nThird", requirements)).toBe(false);
  });

  it("opens and cancels the editor without an API request while retaining the result", () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    renderPage(fixture());
    fireEvent.click(screen.getByRole("button", { name: "Reassess revised specification" }));
    expect(screen.getByText("Corrective-action resolution")).toBeTruthy();
    expect((screen.getByRole("textbox", { name: "Revised specification" }) as HTMLTextAreaElement).value).toBe("Response time <= 2 s\n\nResponse time <= 5 s");
    fireEvent.click(screen.getByRole("button", { name: "Cancel" }));
    expect(screen.queryByRole("textbox", { name: "Revised specification" })).toBeNull();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("preserves the draft across locale switching without submitting", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    renderPage(fixture());
    fireEvent.click(screen.getByRole("button", { name: "Reassess revised specification" }));
    const editor = screen.getByRole("textbox", { name: "Revised specification" }) as HTMLTextAreaElement;
    fireEvent.change(editor, { target: { value: "Draft text" } });
    await i18n.changeLanguage("uk");
    expect((screen.getByRole("textbox", { name: "Переглянута специфікація" }) as HTMLTextAreaElement).value).toBe("Draft text");
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("blocks a modified non-canonical draft locally and does not mutate prior_context", () => {
    const response = fixture();
    const prior = response.reassessment_context;
    const snapshot = structuredClone(prior);
    const { onAnalyzeReassessment } = renderPage(response);
    fireEvent.click(screen.getByRole("button", { name: "Reassess revised specification" }));
    const editor = screen.getByRole("textbox", { name: "Revised specification" });
    fireEvent.change(editor, { target: { value: "Different revision" } });
    expect(screen.getByText(/not the canonical external revision/i)).toBeTruthy();
    expect((screen.getByRole("button", { name: "Analyze revised specification" }) as HTMLButtonElement).disabled).toBe(true);
    expect(onAnalyzeReassessment).not.toHaveBeenCalled();
    expect(response.reassessment_context).toEqual(snapshot);
  });

  it("submits exactly one REASSESSMENT request only after explicit second Analyze", () => {
    const response = fixture();
    const { onAnalyzeReassessment } = renderPage(response);
    fireEvent.click(screen.getByRole("button", { name: "Reassess revised specification" }));
    expect(onAnalyzeReassessment).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "Analyze revised specification" }));
    expect(onAnalyzeReassessment).toHaveBeenCalledTimes(1);
    const request = onAnalyzeReassessment.mock.calls[0][0];
    expect(Object.keys(request)).toEqual(["case", "requirements", "prior_context"]);
    expect(request).toEqual({ case: "REASSESSMENT", requirements: [{ text: "Response time <= 2 s", source_line: 1 }, { text: "Response time <= 5 s", source_line: 3 }], prior_context: response.reassessment_context });
    expect((request as any).prior_context).toBe(response.reassessment_context);
    expect(request).not.toHaveProperty("locale");
    expect(request).not.toHaveProperty("ui_state");
  });

  it("constructs the request without mutation or frontend lifecycle identities", () => {
    const prior = { scenario: { id: "SCENARIO", version: "1" }, opaque: { lifecycle: true } };
    const requirements = [{ text: "Canonical", source_line: 4 }];
    const request = createReassessmentRequest(requirements, prior);
    expect(request.prior_context).toBe(prior);
    expect(request.requirements).toBe(requirements);
    expect(Object.keys(request)).toEqual(["case", "requirements", "prior_context"]);
  });

  it("uses the exact failed request retry until a draft change invalidates it", () => {
    const retry = vi.fn();
    const invalidate = vi.fn();
    const { onAnalyzeReassessment } = renderPage(fixture(), { reassessmentErrorMessage: "Request failed", onRetryReassessment: retry, onReassessmentDraftChange: invalidate });
    fireEvent.click(screen.getByRole("button", { name: "Reassess revised specification" }));
    fireEvent.click(screen.getByRole("button", { name: "Retry revised specification" }));
    expect(retry).toHaveBeenCalledTimes(1);
    expect(onAnalyzeReassessment).not.toHaveBeenCalled();
    fireEvent.change(screen.getByRole("textbox", { name: "Revised specification" }), { target: { value: "Changed" } });
    expect(invalidate).toHaveBeenCalled();
  });
});

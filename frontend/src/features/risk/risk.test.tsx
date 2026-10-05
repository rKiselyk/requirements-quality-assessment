import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../../App";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { i18n } from "../../i18n";
import { risk as enRisk } from "../../i18n/locales/en/risk";
import { risk as ukRisk } from "../../i18n/locales/uk/risk";
import { RiskPage } from "./RiskPage";
import {
  categoricalRiskNonClaims,
  operandKinds,
  projectCategoricalRisk,
  projectPopulation,
  projectQuantitativeRisk,
  projectRelation,
  projectResolution,
  quantitativeRiskNonClaims,
  relationNonClaims,
  selectRiskPage,
} from "./projection";

const artifact = { artifact_id: "SPEC-RISK", artifact_version: "v1" };
const assessment = { assessment_id: "ASSESS-RISK", assessment_version: "v1", artifact_ref: artifact };
const snapshot = { value: "SNAPSHOT-RISK" };
const processState = { process_state_id: "PROCESS-RISK", process_state_version: "v1", stage: "REFERENCE_VERIFICATION" };
const problemRule = { rule_id: "D-QB-CONFLICT-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const relationRule = { rule_id: "R_DQ-PE-QB-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const riskRule = { rule_id: "RISK-PE-QB-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const calculationRule = { rule_id: "R-IJ-PE-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const sourceClaim = { source_kind: "QB_CROSS_REQUIREMENT_RESULT", source_id: "CROSS-1", source_version: "1" };
const crossResult = { value: "CROSS-1" };
const participants = [
  { artifact_ref: artifact, requirement_id: "R001", source_line: 1 },
  { artifact_ref: artifact, requirement_id: "R002", source_line: 2 },
];
const observations = [
  { requirement_id: "R001", feature_id: "quantitative_constraint", observation_index: 0 },
  { requirement_id: "R002", feature_id: "quantitative_constraint", observation_index: 0 },
];
const operandRefs = observations.map((source_observation_ref, index) => ({ source_cross_result_ref: crossResult, position: index === 0 ? "LEFT" : "RIGHT", source_observation_ref }));
const evidence = [{ requirement_id: "R001", evidence_id: "E1" }, { requirement_id: "R002", evidence_id: "E2" }];
const comparisonKey = { normalized_metric: "response time", normalized_context: "load", unit: "SECOND" };
const resolutionId = { artifact_ref: artifact, source_assessment_ref: assessment, source_snapshot_id: snapshot, source_claim_ref: sourceClaim, problem_rule_ref: problemRule };
const problemId = { artifact_ref: artifact, source_assessment_ref: assessment, source_snapshot_id: snapshot, source_cross_result_ref: crossResult, problem_rule_ref: problemRule };
const problemRef = { problem_id: problemId };
const resolutionRef = { resolution_id: resolutionId };
const populationId = { artifact_ref: artifact, source_assessment_ref: assessment, source_snapshot_id: snapshot, problem_rule_ref: problemRule };
const populationRef = { population_id: populationId };
const relationId = { problem_resolution_ref: resolutionRef, problem_ref: problemRef, characteristic_id: "PERFORMANCE_EFFICIENCY", relation_rule_ref: relationRule };
const relationRef = { relation_id: relationId };
const productRef = { product_id: "PRODUCT", product_version: "1" };
const pqAssessmentId = { identity: "PQ-ASSESSMENT", artifact_ref: artifact };
const pqScope = { scope_kind: "SINGLE_CRITERION_SINGLE_OBSERVATION", characteristic_id: "PERFORMANCE_EFFICIENCY", product_ref: productRef };
const productQualityContext = {
  assessment_ref: { assessment_id: pqAssessmentId, product_quality_assessment_version: "v1" },
  status: "AVAILABLE", applicability: "APPLICABLE", result_kind: "OBSERVED_REFERENCE_INDICATOR", scope_ref: pqScope, product_ref: productRef,
};

const expectedEnglishRelationNonClaims = {
  "NC-RDQ-001": "R_DQ does not supply a numeric rho.",
  "NC-RDQ-002": "R_DQ does not establish causality.",
  "NC-RDQ-003": "R_DQ does not supply probability or impact.",
  "NC-RDQ-004": "R_DQ is not proof of poor product performance.",
  "NC-RDQ-005": "R_DQ does not establish a mapping beyond the exact supported response-time key.",
} as const;

const expectedUkrainianRelationNonClaims = {
  "NC-RDQ-001": "R_DQ не задає числового rho.",
  "NC-RDQ-002": "R_DQ не встановлює причинного зв’язку.",
  "NC-RDQ-003": "R_DQ не задає ймовірність або вплив.",
  "NC-RDQ-004": "R_DQ не є доказом низької продуктивності продукту.",
  "NC-RDQ-005": "R_DQ не встановлює відображення за межами точного підтримуваного ключа часу відгуку.",
} as const;

const expectedEnglishCategoricalNonClaims = {
  "NC-RISK-001": "The classification identifies bounded risk presence, not risk magnitude.",
  "NC-RISK-002": "No probability or likelihood is supplied.",
  "NC-RISK-003": "No impact, severity, or criticality is supplied.",
  "NC-RISK-004": "No weight, threshold, or aggregate risk is supplied.",
  "NC-RISK-005": "No priority or rank is supplied.",
  "NC-RISK-006": "The bounded risk classification is neither a product-failure result nor a product-quality score.",
  "NC-RISK-007": "No causal claim is established.",
  "NC-RISK-008": "Absence of this bounded risk classification does not establish absence of risk.",
  "NC-RISK-009": "The categorical risk model is provisional and not calibrated.",
} as const;

const expectedUkrainianCategoricalNonClaims = {
  "NC-RISK-001": "Класифікація встановлює обмежену наявність ризику, а не його величину.",
  "NC-RISK-002": "Ймовірність або правдоподібність не задаються.",
  "NC-RISK-003": "Вплив, тяжкість або критичність не задаються.",
  "NC-RISK-004": "Вага, поріг або агрегований ризик не задаються.",
  "NC-RISK-005": "Пріоритет або ранг не задаються.",
  "NC-RISK-006": "Обмежена класифікація ризику не є ані результатом відмови продукту, ані оцінкою якості продукту.",
  "NC-RISK-007": "Причинне твердження не встановлюється.",
  "NC-RISK-008": "Відсутність цієї обмеженої класифікації ризику не встановлює відсутність ризику.",
  "NC-RISK-009": "Модель категорійного ризику є попередньою та некаліброваною.",
} as const;

function clone<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

vi.mock("../product-quality/projection", () => ({
  selectProductQualityPage: () => ({
    kind: "AVAILABLE",
    featureProfile: {
      artifactRef: { artifact_id: "SPEC-RISK", artifact_version: "v1" },
      productRef: { product_id: "PRODUCT", product_version: "1" },
      profileId: { profile_id: "PQ-PROFILE" },
      processStateRef: { process_state_id: "PROCESS-RISK", process_state_version: "v1", stage: "REFERENCE_VERIFICATION" },
    },
    observed: { raw: {
      assessment_id: { identity: "PQ-ASSESSMENT", artifact_ref: { artifact_id: "SPEC-RISK", artifact_version: "v1" } },
      product_quality_assessment_version: "v1", status: "AVAILABLE", applicability: "APPLICABLE", result_kind: "OBSERVED_REFERENCE_INDICATOR",
      scope: { scope_kind: "SINGLE_CRITERION_SINGLE_OBSERVATION", characteristic_id: "PERFORMANCE_EFFICIENCY", product_ref: { product_id: "PRODUCT", product_version: "1" } },
      product_ref: { product_id: "PRODUCT", product_version: "1" },
    } },
  }),
}));

function confirmedResolution(marker = "CURRENT") {
  const problem = {
    problem_id: problemId, problem_kind: "CONFIRMED_SUPPORTED_PROBLEM", defect_type: "SPECIFICATION_INCONSISTENCY",
    conflict_class: "LOGICAL_CONFLICT", conflict_subtype: "DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY",
    target_ref: { artifact_ref: artifact }, participant_refs: participants, source_cross_result_ref: crossResult,
    source_observation_refs: observations, comparison_key: comparisonKey, operand_refs: operandRefs,
    status: "AVAILABLE", applicability: "APPLICABLE", evidence_refs: evidence, diagnostic_refs: [], explanation: `Confirmed ${marker} problem.`,
    provenance: {
      source_cross_result_ref: crossResult, source_snapshot_id: snapshot, participant_refs: participants, source_observation_refs: observations,
      comparison_key: comparisonKey, exact_operand_refs: operandRefs, ordered_cross_evidence_refs: evidence, diagnostic_refs: [], problem_rule_ref: problemRule,
    },
    artifact_ref: artifact, source_assessment_ref: assessment, source_snapshot_id: snapshot, process_state_ref: processState, rule_ref: problemRule,
    non_claims: ["NC-D-001", "NC-D-002", "NC-D-003", "NC-D-004", "NC-D-005", "NC-D-006"],
  };
  return clone({
    resolution_id: resolutionId, source_claim_ref: sourceClaim, status: "AVAILABLE", applicability: "APPLICABLE",
    disposition: "CONFIRMED_SUPPORTED_PROBLEM", problem, explanation: `Resolution ${marker}.`, reasons: ["CONFIRMED_QB_CONFLICT"],
    evidence_refs: evidence, provenance_refs: [sourceClaim], artifact_ref: artifact, source_assessment_ref: assessment, source_snapshot_id: snapshot, rule_ref: problemRule,
  });
}

function population() {
  return clone({
    population_id: populationId, artifact_ref: artifact, source_assessment_ref: assessment, source_snapshot_id: snapshot,
    status: "AVAILABLE", applicability: "APPLICABLE", members: [problemRef], population_complete: true,
    problem_resolution_refs: [resolutionRef], unresolved_resolution_refs: [],
    source_qb_assessment_ref: { assessment_ref: assessment, artifact_ref: artifact, snapshot_id: snapshot }, provenance_refs: [], rule_ref: problemRule,
  });
}

function relation() {
  return clone({
    relation_id: relationId, problem_resolution_ref: resolutionRef, problem_ref: problemRef, characteristic_id: "PERFORMANCE_EFFICIENCY",
    relation_kind: "BOUNDED_RISK_RELEVANCE", status: "AVAILABLE", applicability: "APPLICABLE", rationale: "Bounded relevance only.",
    reasons: ["EXACT_RESPONSE_TIME_KEY"], source_result_refs: [sourceClaim], evidence_refs: evidence,
    provenance: {
      problem_resolution_ref: resolutionRef, problem_ref: problemRef, source_cross_result_ref: crossResult, comparison_key: comparisonKey,
      characteristic_id: "PERFORMANCE_EFFICIENCY", relation_rule_ref: relationRule,
      rationale_code: "EXACT_RESPONSE_TIME_KEY", evidence_refs: evidence, source_contract_refs: [],
    },
    artifact_ref: artifact, source_assessment_ref: assessment, source_snapshot_id: snapshot, process_state_ref: processState,
    rule_ref: relationRule, calibration_status: "PROVISIONAL_NOT_CALIBRATED", non_claims: [...relationNonClaims],
  });
}

function categoricalRisk() {
  const event = { event_id: "RISK-EVENT", event_version: "v1", artifact_ref: artifact, process_state_ref: processState };
  const subject = { artifact_ref: artifact, participant_refs: participants, affected_characteristic_id: "PERFORMANCE_EFFICIENCY" };
  const modelRef = { model_id: "FULL-MODEL-V0.1-M-RISK-PE-QB", model_version: "1" };
  const parameterSetRef = { parameter_set_id: "RISK-PE-QB-001-PARAMETERS", parameter_set_version: "1" };
  const riskId = { assessment_event_ref: event, subject, problem_resolution_ref: resolutionRef, defect_population_ref: populationRef, relation_ref: relationRef, product_quality_assessment_ref: productQualityContext.assessment_ref, model_ref: modelRef, rule_ref: riskRule, parameter_set_ref: parameterSetRef };
  return clone({
    risk_assessment_id: riskId, assessment_event_ref: event, subject, characteristic_id: "PERFORMANCE_EFFICIENCY",
    status: "AVAILABLE", applicability: "APPLICABLE", classification: "RISK_IDENTIFIED", risk_statement: "Bounded risk presence.", explanation: "Categorical only.",
    problem_resolution_ref: resolutionRef, problem_ref: problemRef, defect_population_ref: populationRef, defect_population_status: "AVAILABLE",
    relation_ref: relationRef, product_quality_context: productQualityContext, evidence_refs: evidence,
    provenance: {
      problem_resolution_ref: resolutionRef, problem_ref_or_none: problemRef, defect_population_ref: populationRef, defect_population_status: "AVAILABLE",
      relation_ref: relationRef, product_quality_context: productQualityContext, participant_refs: participants, ordered_evidence_refs: evidence,
      source_cross_result_ref_or_none: crossResult, source_assessment_refs: [assessment, productQualityContext.assessment_ref],
      artifact_ref: artifact, source_snapshot_id: snapshot, process_state_ref: processState, model_ref: modelRef, rule_ref: riskRule, parameter_set_ref: parameterSetRef,
      full_model_contract_ref: { contract_id: "FULL-MODEL-V0.1-CONTRACT", version: "1" },
      defect_risk_contract_ref: { contract_id: "FULL-MODEL-V0.1-DEFECT-QUALITY-RISK", version: "1" },
    },
    model_ref: modelRef, rule_ref: riskRule, parameter_set_ref: parameterSetRef, calibration_status: "PROVISIONAL_NOT_CALIBRATED",
    artifact_ref: artifact, source_assessment_ref: assessment, source_snapshot_id: snapshot, process_state_ref: processState, non_claims: [...categoricalRiskNonClaims],
  });
}

function quantitativeRisk() {
  const contract = { contract_id: "FULL-MODEL-V0.1-QUANTITATIVE-LOCAL-RISK", version: "1" };
  const values = [{ numerator: 1, denominator: 2 }, { numerator: 1, denominator: 4 }, { numerator: 3, denominator: 4 }, { numerator: 2, denominator: 3 }];
  const operands = operandKinds.map((kind, index) => ({
    operand_id: { kind, operand_id: `OPERAND-${kind}`, operand_version: "1" }, kind, state: "AVAILABLE", value: values[index],
    provenance: {
      source_ref: { source_id: `SOURCE-${kind}`, source_version: "1", provider_id: "CONTROLLED-PROVIDER", provider_version: "1" }, source_or_rationale: `Externally supplied ${kind}.`,
      calibration_status: "PROVISIONAL_NOT_CALIBRATED", governing_contract_ref: contract, artifact_ref: artifact,
      problem_ref: problemRef, relation_ref: relationRef, characteristic_id: "PERFORMANCE_EFFICIENCY", process_state_ref: processState,
      context_ref: kind === "CONTEXT_FACTOR" ? { context_id: "CONTEXT", context_version: "1" } : null,
    },
  }));
  const assessmentId = { calculation_id: "CALC", calculation_version: "1", problem_ref: problemRef, relation_ref: relationRef, operand_refs: operands.map((item) => item.operand_id), rule_ref: calculationRule };
  const base = {
    assessment_id: assessmentId, result_kind: "LOCAL_RISK_R_IJ", state: "AVAILABLE", scope: "EXTERNALLY_PARAMETERIZED_BOUNDED_PE_REFERENCE",
    problem_ref: problemRef, relation_ref: relationRef, characteristic_id: "PERFORMANCE_EFFICIENCY", artifact_ref: artifact,
    source_assessment_ref: assessment, source_snapshot_id: snapshot, process_state_ref: processState, operands,
    numeric_representation: "EXACT_FRACTION", local_risk: { numerator: 1, denominator: 16 },
    calibration_statuses: operands.map((item) => item.provenance.calibration_status), governing_contract_ref: contract,
    calculation_rule_ref: calculationRule, calculation_rule: "r_ij = rho_ij * p_ij * I_ij * kappa_j(C)", explanation: "Backend supplied exact local result.",
    non_claims: [...quantitativeRiskNonClaims],
  };
  return clone({ ...base, provenance: { problem_ref: problemRef, relation_ref: relationRef, artifact_ref: artifact, source_assessment_ref: assessment, source_snapshot_id: snapshot, process_state_ref: processState, characteristic_id: "PERFORMANCE_EFFICIENCY", operands, governing_contract_ref: contract, calculation_rule_ref: calculationRule, calculation_rule: base.calculation_rule } });
}

function requirement(id: string, sourceLine: number) {
  const feature = (feature_id: string) => ({ feature_id, observations: [], diagnostics: [] });
  return { requirement: { id, source_line: sourceLine, text: `Requirement ${id}` }, quality_profile: {}, evidence: [], features: { condition_contexts: feature("condition_context"), expected_results: feature("expected_result"), acceptance_criteria: feature("acceptance_criterion"), quantitative_constraints: feature("quantitative_constraint"), verification_methods: feature("verification_method"), vague_term_occurrences: feature("vague_term_occurrence") }, trace: null };
}

function controlledResponse(): CanonicalAnalyzeResponse {
  const observed = {
    assessment_id: pqAssessmentId, product_quality_assessment_version: "v1", status: "AVAILABLE", applicability: "APPLICABLE",
    result_kind: "OBSERVED_REFERENCE_INDICATOR", scope: pqScope, product_ref: productRef, artifact_ref: artifact,
    feature_profile_ref: { profile_id: "PQ-PROFILE" },
  };
  return {
    contract_version: "research-api-v1", analysis_case: "CONTROLLED_DEMO", controlled_scenario: { id: "SCENARIO", version: "1" },
    requirements: [requirement("R001", 1), requirement("R002", 2)], specification: { snapshot_id: "SNAPSHOT" },
    section_availability: [{ section: "risk", availability: "AVAILABLE", reason_code: null }],
    full_model: { observed_product_quality: observed, problem_resolutions: [confirmedResolution()], defect_population: population(), defect_quality_relations: [relation()], risk_assessments: [categoricalRisk()], quantitative_risk_assessments: [quantitativeRisk()] },
    reassessment_context: null, limitations: [],
  } as unknown as CanonicalAnalyzeResponse;
}

function initialResponse(): CanonicalAnalyzeResponse {
  return { ...controlledResponse(), analysis_case: "INITIAL", controlled_scenario: null, full_model: null, section_availability: [{ section: "risk", availability: "UNAVAILABLE", reason_code: "CONFIRMED_PROBLEM_AND_RISK_INPUTS_NOT_AVAILABLE" }] };
}

function reassessmentResponse(options: { mismatch?: boolean; duplicate?: boolean; missing?: boolean } = {}): CanonicalAnalyzeResponse {
  const current = { artifact_ref: artifact, product_quality_assessment: (controlledResponse().full_model as Record<string, unknown>).observed_product_quality, problem_resolutions: [confirmedResolution("V2")], defect_population: population(), target_problem_resolution: confirmedResolution("V2"), defect_quality_relation: relation(), risk_assessment: categoricalRisk() };
  const dynamicRef = { result_family: "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH", result_id: (current.risk_assessment as Record<string, unknown>).risk_assessment_id, artifact_ref: options.mismatch ? { ...artifact, artifact_version: "wrong" } : artifact };
  const refs = [{ result_family: "CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH", result_id: "CORE", artifact_ref: artifact }, ...(options.missing ? [] : [dynamicRef]), ...(options.duplicate ? [dynamicRef] : [])];
  const results = [{ artifact_ref: artifact, core: true }, ...(options.missing ? [] : [current]), ...(options.duplicate ? [current] : [])];
  const stale = controlledResponse().full_model as Record<string, unknown>;
  return { ...controlledResponse(), analysis_case: "REASSESSMENT", full_model: { ...stale, problem_resolutions: [{ ...confirmedResolution("STALE"), explanation: "STALE V1" }], reassessment: { context: { child_artifact_ref: artifact }, provenance: { child_artifact_ref: artifact }, produced_result_refs: refs, produced_results: results } } } as unknown as CanonicalAnalyzeResponse;
}

function validGraph() {
  const projectedResolution = projectResolution(confirmedResolution())!;
  const projectedPopulation = projectPopulation(population(), [projectedResolution])!;
  const projectedRelation = projectRelation(relation(), [projectedResolution], projectedPopulation)!;
  return { projectedResolution, projectedPopulation, projectedRelation, problem: projectedResolution.problem! };
}

function identifiedResolution(marker: string, suffix: string) {
  const value = confirmedResolution(marker) as Record<string, unknown>;
  const claim = { ...sourceClaim, source_id: `CROSS-${suffix}` };
  const cross = { value: `CROSS-${suffix}` };
  value.source_claim_ref = claim;
  (value.resolution_id as Record<string, unknown>).source_claim_ref = claim;
  const problem = value.problem as Record<string, unknown>;
  problem.source_cross_result_ref = cross;
  (problem.problem_id as Record<string, unknown>).source_cross_result_ref = cross;
  (problem.operand_refs as Record<string, unknown>[]).forEach((item) => { item.source_cross_result_ref = cross; });
  const provenance = problem.provenance as Record<string, unknown>;
  provenance.source_cross_result_ref = cross;
  provenance.exact_operand_refs = problem.operand_refs;
  return value;
}

function unresolvedResolution(status: "UNKNOWN" | "UNRESOLVED" | "NOT_APPLICABLE" | "UNAVAILABLE" | "UNSUPPORTED", suffix: string) {
  const value = identifiedResolution(status, suffix);
  value.status = status;
  value.applicability = status === "NOT_APPLICABLE" ? "NOT_APPLICABLE" : "UNKNOWN";
  value.disposition = null;
  value.problem = null;
  value.reasons = [status === "NOT_APPLICABLE" ? "QB_OUTSIDE_V0_1_APPLICABILITY" : status === "UNAVAILABLE" ? "SUPPORTED_SOURCE_UNAVAILABLE" : status === "UNSUPPORTED" ? "SOURCE_KIND_UNSUPPORTED" : status === "UNKNOWN" ? "SOURCE_STATE_UNKNOWN" : "QB_ASSESSMENT_UNRESOLVED"];
  return value;
}

function categoricalRecord(value = controlledResponse()) {
  return ((value.full_model as Record<string, unknown>).risk_assessments as Record<string, unknown>[])[0];
}

function setRiskProcess(risk: Record<string, unknown>, process: Record<string, unknown>) {
  risk.process_state_ref = process;
  (risk.assessment_event_ref as Record<string, unknown>).process_state_ref = process;
  (risk.provenance as Record<string, unknown>).process_state_ref = process;
}

describe("RUI-11 Risk", () => {
  beforeEach(async () => { window.sessionStorage.clear(); await i18n.changeLanguage("en"); });
  afterEach(() => { cleanup(); vi.restoreAllMocks(); });

  it("renders canonical INITIAL unavailability without fabricating risk, defects, or operands", () => {
    render(<RiskPage result={initialResponse()} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Risk" })).toBeTruthy();
    expect(screen.getByText("CONFIRMED_PROBLEM_AND_RISK_INPUTS_NOT_AVAILABLE")).toBeTruthy();
    expect(screen.getByText(/No defect absence, safety verdict, zero risk, or quantitative operand was inferred/)).toBeTruthy();
    expect(screen.queryByText("RISK_IDENTIFIED")).toBeNull();
    expect(screen.queryByText("RHO")).toBeNull();
  });

  it("opens Risk and switches locale without another API call or response mutation", async () => {
    const payload = initialResponse();
    payload.section_availability = [{ section: "overview", availability: "AVAILABLE", reason_code: null }, { section: "requirements", availability: "AVAILABLE", reason_code: null }, { section: "specification", availability: "AVAILABLE", reason_code: null }, { section: "product_quality", availability: "UNAVAILABLE", reason_code: "EXTERNAL_EVIDENCE_NOT_SUPPLIED" }, ...payload.section_availability];
    payload.specification = { snapshot_id: "SNAPSHOT", quality_profile: {}, qb_consistency: {} } as never;
    const before = JSON.stringify(payload);
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ ok: true, json: async () => payload } as Response);
    const client = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
    render(<QueryClientProvider client={client}><App /></QueryClientProvider>);
    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    await screen.findByRole("heading", { name: "Overview" });
    fireEvent.click(screen.getByRole("button", { name: "Risk" }));
    await screen.findByText("CONFIRMED_PROBLEM_AND_RISK_INPUTS_NOT_AVAILABLE");
    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));
    expect(await screen.findByRole("heading", { name: "Ризик" })).toBeTruthy();
    expect(globalThis.fetch).toHaveBeenCalledTimes(1);
    expect(JSON.stringify(payload)).toBe(before);
    fireEvent.click(screen.getByRole("button", { name: "Нова специфікація" }));
    expect(await screen.findByRole("heading", { name: "Аналіз специфікації" })).toBeTruthy();
    expect(globalThis.fetch).toHaveBeenCalledTimes(1);
  });

  it("preserves controlled-demo v1 record order and renders distinct categorical and quantitative layers", () => {
    const value = controlledResponse();
    const second = confirmedResolution("SECOND");
    const first = (value.full_model as Record<string, unknown>).problem_resolutions as unknown[];
    first.push(second);
    const pop = (value.full_model as Record<string, unknown>).defect_population as Record<string, unknown>;
    (pop.problem_resolution_refs as unknown[]).push({ resolution_id: second.resolution_id });
    (pop.members as unknown[]).push({ problem_id: (second.problem as Record<string, unknown>).problem_id });
    const projected = selectRiskPage(value);
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.revision).toBe("CONTROLLED_DEMO_V1");
    expect(projected.resolutions.map((entry) => entry.kind === "VALID" ? entry.value.explanation : "MALFORMED")).toEqual(["Resolution CURRENT.", "Resolution SECOND."]);
    expect(projected.quantitative.kind).toBe("RECORDS");
    render(<RiskPage result={value} onSelectRequirement={vi.fn()} />);
    expect(screen.getByRole("heading", { name: "Categorical bounded risk" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Quantitative local risk" })).toBeTruthy();
    expect(screen.getByText("RISK_IDENTIFIED")).toBeTruthy();
    expect(screen.getByText("1/16")).toBeTruthy();
  });

  it("selects the paired v2 dynamic-through-risk result and withholds stale v1 quantitative presentation", () => {
    const projected = selectRiskPage(reassessmentResponse());
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.revision).toBe("REASSESSMENT_V2");
    expect(projected.resolutions[0].kind === "VALID" && projected.resolutions[0].value.explanation).toBe("Resolution V2.");
    expect(projected.quantitative).toEqual({ kind: "REASSESSMENT_ABSENT" });
    render(<RiskPage result={reassessmentResponse()} onSelectRequirement={vi.fn()} />);
    expect(screen.getByText("No quantitative local-risk record was produced for the current reassessed revision.")).toBeTruthy();
    expect(screen.queryByText("1/16")).toBeNull();
    expect(screen.queryByText("STALE V1")).toBeNull();
  });

  it.each([
    ["artifact mismatch", { mismatch: true }], ["duplicate result", { duplicate: true }], ["missing result", { missing: true }],
  ])("fails malformed reassessment selection safely: %s", (_label, options) => {
    expect(selectRiskPage(reassessmentResponse(options as never))).toEqual({ kind: "MALFORMED" });
  });

  it("rejects a dynamic-through-risk ref whose result_id differs from the nested risk assessment identity", () => {
    const value = reassessmentResponse();
    const reassessment = ((value.full_model as Record<string, unknown>).reassessment as Record<string, unknown>);
    const refs = reassessment.produced_result_refs as Record<string, unknown>[];
    refs[1].result_id = { mismatched: true };
    expect(selectRiskPage(value)).toEqual({ kind: "MALFORMED" });
  });

  it("accepts structurally equal current-result identities regardless of object key order", () => {
    const value = reassessmentResponse();
    const reassessment = ((value.full_model as Record<string, unknown>).reassessment as Record<string, unknown>);
    const refs = reassessment.produced_result_refs as Record<string, unknown>[];
    const resultId = refs[1].result_id as Record<string, unknown>;
    refs[1].result_id = Object.fromEntries(Object.entries(resultId).reverse());
    expect(selectRiskPage(value).kind).toBe("AVAILABLE");
  });

  it.each([
    ["confirmed without problem", (value: Record<string, unknown>) => { value.problem = null; }],
    ["no-confirmed with problem", (value: Record<string, unknown>) => { value.disposition = "NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE"; }],
    ["non-available with disposition", (value: Record<string, unknown>) => { value.status = "UNKNOWN"; value.applicability = "UNKNOWN"; }],
    ["multiple reasons", (value: Record<string, unknown>) => { value.reasons = ["ONE", "TWO"]; }],
  ])("rejects malformed problem resolution: %s", (_label, mutate) => {
    const value = confirmedResolution() as Record<string, unknown>; mutate(value); expect(projectResolution(value)).toBeNull();
  });

  it.each([
    ["fabricated problem rule", (value: Record<string, unknown>) => { value.rule_ref = { ...problemRule, rule_id: "FABRICATED" }; }],
    ["fabricated resolution reason", (value: Record<string, unknown>) => { value.reasons = ["REASON-CURRENT"]; }],
  ])("rejects non-canonical problem-resolution contract data: %s", (_label, mutate) => {
    const value = confirmedResolution() as Record<string, unknown>; mutate(value); expect(projectResolution(value)).toBeNull();
  });

  it.each([
    ["participant ownership", (problem: Record<string, unknown>) => { ((problem.source_observation_refs as Record<string, unknown>[])[0]).requirement_id = "OTHER"; }],
    ["operand order", (problem: Record<string, unknown>) => { ((problem.operand_refs as Record<string, unknown>[])[0]).position = "RIGHT"; }],
    ["provenance graph", (problem: Record<string, unknown>) => { (problem.provenance as Record<string, unknown>).comparison_key = { other: true }; }],
    ["problem status", (problem: Record<string, unknown>) => { problem.status = "UNKNOWN"; }],
  ])("rejects malformed confirmed problem: %s", (_label, mutate) => {
    const value = confirmedResolution() as Record<string, unknown>; mutate(value.problem as Record<string, unknown>); expect(projectResolution(value)).toBeNull();
  });

  it("navigates only exact valid participant requirements", () => {
    const onSelect = vi.fn(); render(<RiskPage result={controlledResponse()} onSelectRequirement={onSelect} />);
    fireEvent.click(screen.getByRole("button", { name: "Open R001" }));
    expect(onSelect).toHaveBeenCalledWith("R001");
    const malformed = controlledResponse(); malformed.requirements[0] = { requirement: { id: "R001", source_line: 1, text: "Malformed" } } as never;
    cleanup(); render(<RiskPage result={malformed} onSelectRequirement={onSelect} />);
    expect(screen.queryByRole("button", { name: "Open R001" })).toBeNull();
  });

  it.each([
    ["available incomplete", (value: Record<string, unknown>) => { value.population_complete = false; }],
    ["not-applicable nonempty", (value: Record<string, unknown>) => { value.status = "NOT_APPLICABLE"; value.applicability = "NOT_APPLICABLE"; }],
    ["unknown complete", (value: Record<string, unknown>) => { value.status = "UNKNOWN"; value.applicability = "UNKNOWN"; }],
    ["unknown member", (value: Record<string, unknown>) => { value.members = [{ problem_id: { other: true } }]; }],
    ["resolution mismatch", (value: Record<string, unknown>) => { value.problem_resolution_refs = []; }],
  ])("rejects malformed defect population: %s", (_label, mutate) => {
    const resolution = projectResolution(confirmedResolution())!; const value = population() as Record<string, unknown>; mutate(value);
    expect(projectPopulation(value, [resolution])).toBeNull();
  });

  it("requires the exact ordered confirmed-problem member population", () => {
    const first = projectResolution(identifiedResolution("FIRST", "A"))!;
    const second = projectResolution(identifiedResolution("SECOND", "B"))!;
    const value = population() as Record<string, unknown>;
    value.problem_resolution_refs = [{ resolution_id: first.resolutionId }, { resolution_id: second.resolutionId }];
    value.members = [{ problem_id: first.problem!.problemId }];
    expect(projectPopulation(value, [first, second])).toBeNull();
    value.members = [{ problem_id: second.problem!.problemId }, { problem_id: first.problem!.problemId }];
    expect(projectPopulation(value, [first, second])).toBeNull();
  });

  it("requires the exact ordered UNKNOWN/UNRESOLVED resolution population", () => {
    const unknown = projectResolution(unresolvedResolution("UNKNOWN", "UNKNOWN"))!;
    const unresolved = projectResolution(unresolvedResolution("UNRESOLVED", "UNRESOLVED"))!;
    const value = population() as Record<string, unknown>;
    value.status = "UNRESOLVED"; value.applicability = "UNKNOWN"; value.population_complete = false;
    value.members = []; value.problem_resolution_refs = [{ resolution_id: unknown.resolutionId }, { resolution_id: unresolved.resolutionId }];
    value.unresolved_resolution_refs = [{ resolution_id: unknown.resolutionId }];
    expect(projectPopulation(value, [unknown, unresolved])).toBeNull();
  });

  it.each(["NOT_APPLICABLE", "UNAVAILABLE", "UNSUPPORTED"] as const)("does not classify %s resolutions as unresolved", (status) => {
    const resolution = projectResolution(unresolvedResolution(status, status))!;
    const value = population() as Record<string, unknown>;
    value.status = "UNKNOWN"; value.applicability = "UNKNOWN"; value.population_complete = false;
    value.members = []; value.problem_resolution_refs = [{ resolution_id: resolution.resolutionId }]; value.unresolved_resolution_refs = [];
    expect(projectPopulation(value, [resolution])).not.toBeNull();
  });

  it("rejects a NOT_APPLICABLE population with a contradictory resolution universe", () => {
    const resolution = projectResolution(unresolvedResolution("NOT_APPLICABLE", "NA"))!;
    const value = population() as Record<string, unknown>;
    value.status = "NOT_APPLICABLE"; value.applicability = "NOT_APPLICABLE"; value.members = [];
    value.problem_resolution_refs = [{ resolution_id: resolution.resolutionId }]; value.unresolved_resolution_refs = [];
    expect(projectPopulation(value, [resolution])).toBeNull();
  });

  it.each([
    ["available wrong kind", (value: Record<string, unknown>) => { value.relation_kind = "OTHER"; }],
    ["available no problem", (value: Record<string, unknown>) => { value.problem_ref = null; }],
    ["non-available kind", (value: Record<string, unknown>) => { value.status = "UNKNOWN"; value.applicability = "UNKNOWN"; }],
    ["wrong characteristic", (value: Record<string, unknown>) => { value.characteristic_id = "OTHER"; }],
    ["provenance mismatch", (value: Record<string, unknown>) => { (value.provenance as Record<string, unknown>).rationale_code = "OTHER"; }],
  ])("rejects malformed R_DQ relation: %s", (_label, mutate) => {
    const graph = validGraph(); const value = relation() as Record<string, unknown>; mutate(value);
    expect(projectRelation(value, [graph.projectedResolution], graph.projectedPopulation)).toBeNull();
  });

  it.each([
    ["fabricated relation rule", (value: Record<string, unknown>) => { value.rule_ref = { ...relationRule, rule_id: "FABRICATED" }; }],
    ["fabricated relation reason", (value: Record<string, unknown>) => { value.reasons = ["CONFIRMED_PROBLEM_RELEVANT_TO_PERFORMANCE_EFFICIENCY"]; }],
    ["problem process mismatch", (value: Record<string, unknown>) => { value.process_state_ref = { ...processState, process_state_version: "v2" }; }],
  ])("rejects non-canonical R_DQ contract data: %s", (_label, mutate) => {
    const graph = validGraph(); const value = relation() as Record<string, unknown>; mutate(value);
    expect(projectRelation(value, [graph.projectedResolution], graph.projectedPopulation)).toBeNull();
  });

  it("preserves relation and categorical non-claim order and neutral calibration", () => {
    const projected = selectRiskPage(controlledResponse()); expect(projected.kind).toBe("AVAILABLE"); if (projected.kind !== "AVAILABLE") return;
    expect(projected.relations[0].kind === "VALID" && projected.relations[0].value.nonClaims).toEqual(relationNonClaims);
    expect(projected.categorical[0].kind === "VALID" && projected.categorical[0].value.nonClaims).toEqual(categoricalRiskNonClaims);
    expect(projected.categorical[0].kind === "VALID" && projected.categorical[0].value.calibrationStatus).toBe("PROVISIONAL_NOT_CALIBRATED");
  });

  it.each(Object.entries(expectedEnglishRelationNonClaims))("maps English %s to its canonical R_DQ meaning", (code, explanation) => {
    expect(enRisk.nonClaims.relation[code as keyof typeof enRisk.nonClaims.relation]).toBe(explanation);
  });

  it.each(Object.entries(expectedUkrainianRelationNonClaims))("maps Ukrainian %s to its canonical R_DQ meaning", (code, explanation) => {
    expect(ukRisk.nonClaims.relation[code as keyof typeof ukRisk.nonClaims.relation]).toBe(explanation);
  });

  it.each(Object.entries(expectedEnglishCategoricalNonClaims))("maps English %s to its canonical categorical Risk meaning", (code, explanation) => {
    expect(enRisk.nonClaims.categorical[code as keyof typeof enRisk.nonClaims.categorical]).toBe(explanation);
  });

  it.each(Object.entries(expectedUkrainianCategoricalNonClaims))("maps Ukrainian %s to its canonical categorical Risk meaning", (code, explanation) => {
    expect(ukRisk.nonClaims.categorical[code as keyof typeof ukRisk.nonClaims.categorical]).toBe(explanation);
  });

  it("keeps localized non-claim codes in canonical order", () => {
    expect(Object.keys(enRisk.nonClaims.relation)).toEqual(relationNonClaims);
    expect(Object.keys(ukRisk.nonClaims.relation)).toEqual(relationNonClaims);
    expect(Object.keys(enRisk.nonClaims.categorical)).toEqual(categoricalRiskNonClaims);
    expect(Object.keys(ukRisk.nonClaims.categorical)).toEqual(categoricalRiskNonClaims);
  });

  it("renders canonical R_DQ and categorical Risk codes visibly with their English explanations", () => {
    render(<RiskPage result={controlledResponse()} onSelectRequirement={vi.fn()} />);
    const summaries = screen.getAllByText("Canonical non-claims");
    fireEvent.click(summaries[1]);
    fireEvent.click(summaries[2]);
    const relationDetails = within(summaries[1].closest("details")!);
    const categoricalDetails = within(summaries[2].closest("details")!);
    relationNonClaims.forEach((code) => expect(relationDetails.getByText(code)).toBeTruthy());
    categoricalRiskNonClaims.forEach((code) => expect(categoricalDetails.getByText(code)).toBeTruthy());
    Object.values(expectedEnglishRelationNonClaims).forEach((explanation) => expect(relationDetails.getByText(explanation)).toBeTruthy());
    Object.values(expectedEnglishCategoricalNonClaims).forEach((explanation) => expect(categoricalDetails.getByText(explanation)).toBeTruthy());
  });

  it("renders canonical R_DQ and categorical Risk codes visibly with their Ukrainian explanations", async () => {
    await i18n.changeLanguage("uk");
    render(<RiskPage result={controlledResponse()} onSelectRequirement={vi.fn()} />);
    const summaries = screen.getAllByText("Канонічні не-твердження");
    fireEvent.click(summaries[1]);
    fireEvent.click(summaries[2]);
    const relationDetails = within(summaries[1].closest("details")!);
    const categoricalDetails = within(summaries[2].closest("details")!);
    relationNonClaims.forEach((code) => expect(relationDetails.getByText(code)).toBeTruthy());
    categoricalRiskNonClaims.forEach((code) => expect(categoricalDetails.getByText(code)).toBeTruthy());
    Object.values(expectedUkrainianRelationNonClaims).forEach((explanation) => expect(relationDetails.getByText(explanation)).toBeTruthy());
    Object.values(expectedUkrainianCategoricalNonClaims).forEach((explanation) => expect(categoricalDetails.getByText(explanation)).toBeTruthy());
  });

  it.each([
    ["available wrong classification", (value: Record<string, unknown>) => { value.classification = "LOW"; }],
    ["non-available classification", (value: Record<string, unknown>) => { value.status = "UNKNOWN"; value.applicability = "UNKNOWN"; }],
    ["population ref", (value: Record<string, unknown>) => { value.defect_population_ref = { other: true }; }],
    ["event process", (value: Record<string, unknown>) => { (value.assessment_event_ref as Record<string, unknown>).process_state_ref = { other: true }; }],
    ["product quality", (value: Record<string, unknown>) => { value.product_quality_context = { stale: true }; }],
    ["model provenance", (value: Record<string, unknown>) => { (value.provenance as Record<string, unknown>).model_ref = { other: true }; }],
  ])("fails categorical risk closed: %s", (_label, mutate) => {
    const value = controlledResponse(); const risk = ((value.full_model as Record<string, unknown>).risk_assessments as Record<string, unknown>[])[0]; mutate(risk);
    const projected = selectRiskPage(value); expect(projected.kind === "AVAILABLE" && projected.categorical[0].kind).toBe("MALFORMED");
  });

  it.each([
    ["legacy model", "model_ref", { model_id: "M-RISK", model_version: "1" }],
    ["legacy parameter set", "parameter_set_ref", { parameter_set_id: "RISK-PARAMETERS", parameter_set_version: "1" }],
  ])("rejects a self-consistent non-canonical categorical %s", (_label, field, replacement) => {
    const value = controlledResponse(); const risk = categoricalRecord(value);
    risk[field] = replacement;
    (risk.provenance as Record<string, unknown>)[field] = replacement;
    (risk.risk_assessment_id as Record<string, unknown>)[field] = replacement;
    const projected = selectRiskPage(value);
    expect(projected.kind === "AVAILABLE" && projected.categorical[0].kind).toBe("MALFORMED");
  });

  it("accepts the canonical categorical model, rule, parameter set, and calibration identities", () => {
    const projected = selectRiskPage(controlledResponse());
    expect(projected.kind).toBe("AVAILABLE");
    if (projected.kind !== "AVAILABLE") return;
    expect(projected.categorical[0].kind).toBe("VALID");
  });

  it("rejects categorical risk whose relation belongs to another selected resolution", () => {
    const value = controlledResponse(); const fm = value.full_model as Record<string, unknown>;
    const secondRaw = identifiedResolution("SECOND", "SECOND");
    const second = projectResolution(secondRaw)!;
    (fm.problem_resolutions as unknown[]).push(secondRaw);
    const pop = fm.defect_population as Record<string, unknown>;
    (pop.problem_resolution_refs as unknown[]).push({ resolution_id: second.resolutionId });
    (pop.members as unknown[]).push({ problem_id: second.problem!.problemId });
    const risk = categoricalRecord(value); const riskId = risk.risk_assessment_id as Record<string, unknown>;
    const provenance = risk.provenance as Record<string, unknown>;
    risk.problem_resolution_ref = { resolution_id: second.resolutionId };
    risk.problem_ref = { problem_id: second.problem!.problemId };
    riskId.problem_resolution_ref = risk.problem_resolution_ref;
    provenance.problem_resolution_ref = risk.problem_resolution_ref;
    provenance.problem_ref_or_none = risk.problem_ref;
    provenance.source_cross_result_ref_or_none = second.problem!.raw.source_cross_result_ref;
    const projected = selectRiskPage(value);
    expect(projected.kind === "AVAILABLE" && projected.categorical[0].kind).toBe("MALFORMED");
  });

  it.each([
    ["relation problem", (risk: Record<string, unknown>) => {
      const other = { problem_id: { ...problemId, source_cross_result_ref: { value: "OTHER" } } };
      risk.problem_ref = other; (risk.provenance as Record<string, unknown>).problem_ref_or_none = other;
    }],
    ["confirmed-problem evidence", (risk: Record<string, unknown>) => {
      risk.evidence_refs = [{ evidence_id: "OTHER" }]; (risk.provenance as Record<string, unknown>).ordered_evidence_refs = risk.evidence_refs;
    }],
    ["source cross result", (risk: Record<string, unknown>) => { (risk.provenance as Record<string, unknown>).source_cross_result_ref_or_none = { value: "OTHER" }; }],
    ["source assessment order", (risk: Record<string, unknown>) => { (risk.provenance as Record<string, unknown>).source_assessment_refs = [productQualityContext.assessment_ref, assessment]; }],
    ["Full Model provenance contract", (risk: Record<string, unknown>) => { (risk.provenance as Record<string, unknown>).full_model_contract_ref = { contract_id: "OTHER", version: "1" }; }],
    ["defect/risk provenance contract", (risk: Record<string, unknown>) => { (risk.provenance as Record<string, unknown>).defect_risk_contract_ref = { contract_id: "OTHER", version: "1" }; }],
  ])("rejects categorical risk with a mismatched exact source graph: %s", (_label, mutate) => {
    const value = controlledResponse(); mutate(categoricalRecord(value));
    const projected = selectRiskPage(value);
    expect(projected.kind === "AVAILABLE" && projected.categorical[0].kind).toBe("MALFORMED");
  });

  it("rejects categorical risk whose process differs from the R_DQ relation", () => {
    const value = controlledResponse();
    setRiskProcess(categoricalRecord(value), { ...processState, process_state_version: "v2" });
    const projected = selectRiskPage(value);
    expect(projected.kind === "AVAILABLE" && projected.categorical[0].kind).toBe("MALFORMED");
  });

  it("rejects categorical risk whose process differs from its confirmed problem", () => {
    const graph = validGraph(); const risk = categoricalRisk() as Record<string, unknown>;
    const nextProcess = { ...processState, process_state_version: "v2" };
    setRiskProcess(risk, nextProcess);
    graph.projectedRelation.raw.process_state_ref = nextProcess;
    expect(projectCategoricalRisk(risk, [graph.projectedResolution], graph.projectedPopulation, [graph.projectedRelation], {
      context: productQualityContext, processStateRef: nextProcess,
    } as never)).toBeNull();
  });

  it("rejects current risk tied to a stale Product Quality process state", () => {
    const graph = validGraph();
    expect(projectCategoricalRisk(categoricalRisk(), [graph.projectedResolution], graph.projectedPopulation, [graph.projectedRelation], {
      context: productQualityContext, processStateRef: { ...processState, process_state_version: "stale-v1" },
    } as never)).toBeNull();
  });

  it("never maps RISK_IDENTIFIED to severity or a numeric magnitude", () => {
    render(<RiskPage result={controlledResponse()} onSelectRequirement={vi.fn()} />);
    const section = screen.getByRole("heading", { name: "Categorical bounded risk" }).closest("section")!;
    expect(within(section).getByText("RISK_IDENTIFIED")).toBeTruthy();
    expect(within(section).queryByText(/high|medium|low|%/i)).toBeNull();
    expect(within(section).queryByText("1/16")).toBeNull();
  });

  it("preserves quantitative identity, scope, operand order, exact values, and non-claim order", () => {
    const projected = selectRiskPage(controlledResponse()); expect(projected.kind).toBe("AVAILABLE"); if (projected.kind !== "AVAILABLE" || projected.quantitative.kind !== "RECORDS") return;
    const entry = projected.quantitative.records[0]; expect(entry.kind).toBe("VALID"); if (entry.kind !== "VALID") return;
    expect(entry.value.resultKind).toBe("LOCAL_RISK_R_IJ");
    expect(entry.value.scope).toBe("EXTERNALLY_PARAMETERIZED_BOUNDED_PE_REFERENCE");
    expect(entry.value.operands.map((item) => item.kind)).toEqual(operandKinds);
    expect(entry.value.operands.map((item) => item.value)).toEqual([{ numerator: "1", denominator: "2" }, { numerator: "1", denominator: "4" }, { numerator: "3", denominator: "4" }, { numerator: "2", denominator: "3" }]);
    expect(entry.value.localRisk).toEqual({ numerator: "1", denominator: "16" });
    expect(entry.value.nonClaims).toEqual(quantitativeRiskNonClaims);
  });

  it.each([
    ["operand missing exact fraction", (value: Record<string, unknown>) => { ((value.operands as Record<string, unknown>[])[0]).value = null; }],
    ["operand outside unit interval", (value: Record<string, unknown>) => { ((value.operands as Record<string, unknown>[])[0]).value = { numerator: 2, denominator: 1 }; }],
    ["non-available operand has value", (value: Record<string, unknown>) => { ((value.operands as Record<string, unknown>[])[0]).state = "UNKNOWN"; }],
    ["context on rho", (value: Record<string, unknown>) => { (((value.operands as Record<string, unknown>[])[0]).provenance as Record<string, unknown>).context_ref = { context_id: "OTHER" }; }],
    ["missing context factor context", (value: Record<string, unknown>) => { (((value.operands as Record<string, unknown>[])[3]).provenance as Record<string, unknown>).context_ref = null; }],
    ["wrong operand order", (value: Record<string, unknown>) => { (value.operands as unknown[]).reverse(); }],
    ["operand graph mismatch", (value: Record<string, unknown>) => { (((value.operands as Record<string, unknown>[])[1]).provenance as Record<string, unknown>).problem_ref = { other: true }; }],
    ["provenance operands mismatch", (value: Record<string, unknown>) => { (value.provenance as Record<string, unknown>).operands = []; }],
    ["calibration order mismatch", (value: Record<string, unknown>) => { value.calibration_statuses = ["OTHER", "PROVISIONAL_NOT_CALIBRATED", "PROVISIONAL_NOT_CALIBRATED", "PROVISIONAL_NOT_CALIBRATED"]; }],
    ["local risk outside interval", (value: Record<string, unknown>) => { value.local_risk = { numerator: 2, denominator: 1 }; }],
    ["available none representation", (value: Record<string, unknown>) => { value.numeric_representation = "NONE"; }],
  ])("rejects malformed quantitative local risk: %s", (_label, mutate) => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>; mutate(value);
    expect(projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation)).toBeNull();
  });

  it("rejects quantitative risk whose selected R_DQ relation is not AVAILABLE/APPLICABLE", () => {
    const graph = validGraph(); const unavailable = { ...graph.projectedRelation, status: "UNKNOWN", applicability: "UNKNOWN", relationKind: null };
    expect(projectQuantitativeRisk(quantitativeRisk(), [graph.problem], [unavailable], graph.projectedPopulation)).toBeNull();
  });

  it("rejects quantitative risk whose relation names a different problem", () => {
    const graph = validGraph(); const mismatched = { ...graph.projectedRelation, problemRef: { problem_id: { other: true } } };
    expect(projectQuantitativeRisk(quantitativeRisk(), [graph.problem], [mismatched], graph.projectedPopulation)).toBeNull();
  });

  it("rejects quantitative risk crossing the relation/problem process version", () => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>;
    const other = { ...processState, process_state_version: "v2" };
    value.process_state_ref = other;
    (value.provenance as Record<string, unknown>).process_state_ref = other;
    (value.operands as Record<string, unknown>[]).forEach((operand) => { (operand.provenance as Record<string, unknown>).process_state_ref = other; });
    ((value.provenance as Record<string, unknown>).operands as Record<string, unknown>[]).forEach((operand) => { (operand.provenance as Record<string, unknown>).process_state_ref = other; });
    expect(projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation)).toBeNull();
  });

  it.each([
    ["governing contract", (value: Record<string, unknown>) => {
      const wrong = { contract_id: "OTHER", version: "1" }; value.governing_contract_ref = wrong;
      (value.provenance as Record<string, unknown>).governing_contract_ref = wrong;
      (value.operands as Record<string, unknown>[]).forEach((operand) => { (operand.provenance as Record<string, unknown>).governing_contract_ref = wrong; });
      ((value.provenance as Record<string, unknown>).operands as Record<string, unknown>[]).forEach((operand) => { (operand.provenance as Record<string, unknown>).governing_contract_ref = wrong; });
    }],
    ["calculation rule ref", (value: Record<string, unknown>) => {
      const wrong = { ...calculationRule, rule_id: "OTHER" }; value.calculation_rule_ref = wrong;
      (value.provenance as Record<string, unknown>).calculation_rule_ref = wrong;
      (value.assessment_id as Record<string, unknown>).rule_ref = wrong;
    }],
    ["calculation rule text", (value: Record<string, unknown>) => {
      value.calculation_rule = "modified trace text"; (value.provenance as Record<string, unknown>).calculation_rule = "modified trace text";
    }],
  ])("rejects a non-canonical quantitative %s", (_label, mutate) => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>; mutate(value);
    expect(projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation)).toBeNull();
  });

  it.each(["operand_id", "operand_version"])("rejects an operand ID missing %s", (field) => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>;
    delete (((value.operands as Record<string, unknown>[])[0].operand_id as Record<string, unknown>)[field]);
    expect(projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation)).toBeNull();
  });

  it.each(["provider_id", "provider_version"])("rejects an operand source ref missing %s", (field) => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>;
    const provenance = (value.operands as Record<string, unknown>[])[0].provenance as Record<string, unknown>;
    delete ((provenance.source_ref as Record<string, unknown>)[field]);
    expect(projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation)).toBeNull();
  });

  it("rejects arbitrary operand calibration even when result ordering agrees", () => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>;
    const operands = value.operands as Record<string, unknown>[];
    (operands[0].provenance as Record<string, unknown>).calibration_status = "HIGH_CONFIDENCE";
    (((value.provenance as Record<string, unknown>).operands as Record<string, unknown>[])[0].provenance as Record<string, unknown>).calibration_status = "HIGH_CONFIDENCE";
    (value.calibration_statuses as unknown[])[0] = "HIGH_CONFIDENCE";
    expect(projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation)).toBeNull();
  });

  it.each(["PROVISIONAL_NOT_CALIBRATED", "EXPERIMENTAL_CALIBRATION_REQUIRED"])("accepts canonical operand calibration %s", (calibration) => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>;
    const operands = value.operands as Record<string, unknown>[];
    (operands[0].provenance as Record<string, unknown>).calibration_status = calibration;
    (((value.provenance as Record<string, unknown>).operands as Record<string, unknown>[])[0].provenance as Record<string, unknown>).calibration_status = calibration;
    (value.calibration_statuses as unknown[])[0] = calibration;
    expect(projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation)).not.toBeNull();
  });

  it.each(["calculation_id", "calculation_version"])("rejects a quantitative assessment ID missing %s", (field) => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>;
    delete ((value.assessment_id as Record<string, unknown>)[field]);
    expect(projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation)).toBeNull();
  });

  it("accepts canonical CALCULATION_WITHHELD and never converts absence to zero", () => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>;
    value.state = "CALCULATION_WITHHELD"; value.numeric_representation = "NONE"; value.local_risk = null;
    const operands = value.operands as Record<string, unknown>[]; operands[0].state = "UNKNOWN"; operands[0].value = null;
    (value.provenance as Record<string, unknown>).operands = operands;
    const projected = projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation);
    expect(projected?.localRisk).toBeNull(); expect(projected?.operands[0].value).toBeNull();
  });

  it.each([
    ["withheld numeric result", (value: Record<string, unknown>) => { value.state = "CALCULATION_WITHHELD"; value.numeric_representation = "NONE"; }],
    ["withheld all operands available", (value: Record<string, unknown>) => { value.state = "CALCULATION_WITHHELD"; value.numeric_representation = "NONE"; value.local_risk = null; }],
  ])("rejects contradictory withheld state: %s", (_label, mutate) => {
    const graph = validGraph(); const value = quantitativeRisk() as Record<string, unknown>; mutate(value);
    expect(projectQuantitativeRisk(value, [graph.problem], [graph.projectedRelation], graph.projectedPopulation)).toBeNull();
  });

  it("does not recompute backend local risk when an operand value changes", () => {
    const value = controlledResponse(); const quantitative = ((value.full_model as Record<string, unknown>).quantitative_risk_assessments as Record<string, unknown>[])[0];
    const operands = quantitative.operands as Record<string, unknown>[]; operands[0].value = { numerator: 1, denominator: 3 };
    (quantitative.provenance as Record<string, unknown>).operands = operands;
    const projected = selectRiskPage(value); expect(projected.kind).toBe("AVAILABLE"); if (projected.kind !== "AVAILABLE" || projected.quantitative.kind !== "RECORDS") return;
    const entry = projected.quantitative.records[0]; expect(entry.kind === "VALID" && entry.value.localRisk).toEqual({ numerator: "1", denominator: "16" });
  });

  it("renders an empty bounded population without a universal zero-defect claim", () => {
    const value = controlledResponse(); const resolution = confirmedResolution() as Record<string, unknown>;
    resolution.disposition = "NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE"; resolution.problem = null;
    const fm = value.full_model as Record<string, unknown>; fm.problem_resolutions = [resolution];
    const pop = population() as Record<string, unknown>; pop.members = []; fm.defect_population = pop;
    fm.defect_quality_relations = []; fm.risk_assessments = []; fm.quantitative_risk_assessments = [];
    render(<RiskPage result={value} onSelectRequirement={vi.fn()} />);
    expect(screen.getAllByText(/does not establish absence of defects/).length).toBeGreaterThan(0);
    expect(screen.queryByText(/no defects|defect free/i)).toBeNull();
  });
});

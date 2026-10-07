import type { CanonicalAnalyzeResponse } from "../../api/analyze";

const reassessmentRule = { rule_id: "REEVAL-FULL-MODEL-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const comparisonRule = { rule_id: "COMPARE-FULL-MODEL-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const fullModelContract = { contract_id: "FULL-MODEL-V0.1-CONTRACT", version: "1" };
const processContract = { contract_id: "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", version: "1" };
const parentArtifact = { artifact_id: "SPEC", artifact_version: "v1" };
const childArtifact = { artifact_id: "SPEC", artifact_version: "v2" };
const processV1 = { process_state_id: "PROCESS", process_state_version: "v1", stage: "REFERENCE_VERIFICATION" };
const processV2 = { process_state_id: "PROCESS", process_state_version: "v2", stage: "REFERENCE_VERIFICATION" };
const childAssessment = { assessment_id: "ASSESS", assessment_version: "v2", artifact_ref: childArtifact };
const applicationRef = { application_id: { application_instance_id: "APPLICATION" }, application_version: "1" };
const componentVersionSet = { components: [{ component_role: "FULL_MODEL_CONTRACT", component_id: "FULL-MODEL-V0.1-CONTRACT", component_version: "1" }] };

function requirement(id: string, sourceLine: number, text: string, numerator: number) {
  const assessment = (characteristicId: string) => ({ characteristic_id: characteristicId, state: "COMPUTED", value: { numerator, denominator: 3 }, assessment_rule_id: `RULE-${characteristicId}`, findings: [], explanation: "Canonical." });
  return { extraction_result: { requirement: { id, source_line: sourceLine, text } }, quality_profile: { completeness: assessment("COMPLETENESS"), verifiability: assessment("VERIFIABILITY"), unambiguity: assessment("UNAMBIGUITY") } };
}

function metric(numerator: number) {
  return { state: "COMPUTED", value: { numerator, denominator: 3 }, computed_count: 2, unknown_count: 0, not_applicable_count: 0, total_count: 2 };
}

function specificationResult(records: unknown[], numerator: number) {
  return { records, specification_assessment: { quality_profile: { completeness: metric(numerator), verifiability: metric(numerator), unambiguity: metric(numerator) }, qb_consistency: { state: "COMPUTED", value: { numerator, denominator: 2 }, reasons: [] } } };
}

function comparison(family: string, index: number) {
  const beforeRef = { result_family: family, result_id: { id: `BEFORE-${index}` }, artifact_ref: parentArtifact };
  const afterRef = { result_family: family, result_id: { id: `AFTER-${index}` }, artifact_ref: childArtifact };
  return {
    comparison_id: `COMPARISON-${index}`, comparison_version: "1", before_result_ref: beforeRef, after_result_ref: afterRef,
    comparison_subject: { result_family: family, metric_or_characteristic_id: `METRIC-${index}`, stable_subject_identity: ["SUBJECT"], ordered_lineage_population: [], scope_identity: ["SCOPE"], evidence_context: ["EVIDENCE"] },
    status: "AVAILABLE", comparison_kind: index === 1 ? "INCREASED" : index === 2 ? "DECREASED" : index === 3 ? "STATE_CHANGED" : "UNCHANGED",
    before_state_and_value: { status: "AVAILABLE", applicability: "APPLICABLE", exact_value: index === 1 ? { numerator: 1, denominator: 2 } : null, categorical_state: index === 1 ? null : "BEFORE_STATE" },
    after_state_and_value: { status: "AVAILABLE", applicability: "APPLICABLE", exact_value: index === 1 ? { numerator: 1, denominator: 1 } : null, categorical_state: index === 1 ? null : index === 4 ? "BEFORE_STATE" : "AFTER_STATE" },
    reason_codes: [index === 1 ? "EXACT_VALUE_INCREASED" : index === 2 ? "STRUCTURED_STATE_CHANGED" : index === 3 ? "STRUCTURED_STATE_CHANGED" : "STRUCTURED_STATE_UNCHANGED"],
    rule_ref: comparisonRule, compatibility_declaration_refs: [], parameter_set_refs: [{ id: "PARAMETERS" }], calibration_status_or_none: "PROVISIONAL_NOT_CALIBRATED",
    explanation: "Canonical structured comparison.", provenance: [{ comparison_id: `COMPARISON-${index}`, comparison_version: "1" }, beforeRef, afterRef, comparisonRule],
    claims: ["STRUCTURED_CHANGE_ONLY"], non_claims: ["NO_DIRECTIONAL_QUALITY_INTERPRETATION", "NO_CAUSAL_EFFECT_INFERENCE", "NO_ACTION_SUCCESS_INFERENCE", "NO_STAKEHOLDER_INTENT_VALIDATION"],
  };
}

export function lifecycleFixture(analysisCase: CanonicalAnalyzeResponse["analysis_case"] = "CONTROLLED_DEMO"): CanonicalAnalyzeResponse {
  const lineage1 = { artifact_id: "SPEC", origin_artifact_version: "v1", origin_requirement_id: "R001", origin_source_line: 1 };
  const lineage2 = { artifact_id: "SPEC", origin_artifact_version: "v1", origin_requirement_id: "R002", origin_source_line: 2 };
  const subject1v1 = { artifact_ref: parentArtifact, requirement_id: "R001", source_line: 1 };
  const subject2v1 = { artifact_ref: parentArtifact, requirement_id: "R002", source_line: 2 };
  const subject1v2 = { artifact_ref: childArtifact, requirement_id: "R001", source_line: 1 };
  const subject2v2 = { artifact_ref: childArtifact, requirement_id: "R002", source_line: 2 };
  const initial = { artifact_ref: parentArtifact, parent_artifact_ref: null, created_by_application_ref: null, requirements: [
    { lineage_id: lineage1, subject_ref: subject1v1, text: "Original one", predecessor_subject_ref: null },
    { lineage_id: lineage2, subject_ref: subject2v1, text: "Original two", predecessor_subject_ref: null },
  ], changed_subjects: [] };
  const changed = { lineage_id: lineage2, before_subject_ref: subject2v1, after_subject_ref: subject2v2, change_kind: "REPLACE_TEXT" };
  const revised = { artifact_ref: childArtifact, parent_artifact_ref: parentArtifact, created_by_application_ref: applicationRef, requirements: [
    { lineage_id: lineage1, subject_ref: subject1v2, text: "Original one", predecessor_subject_ref: subject1v1 },
    { lineage_id: lineage2, subject_ref: subject2v2, text: "Revised two", predecessor_subject_ref: subject2v1 },
  ], changed_subjects: [changed] };
  const v1Records = [requirement("R001", 1, "Original one", 1), requirement("R002", 2, "Original two", 1)];
  const v2Records = [requirement("R001", 1, "Original one", 2), requirement("R002", 2, "Revised two", 2)];
  const initialAssessment = specificationResult(v1Records, 1);
  const core = { specification_version: revised, requirement_records: v2Records, specification_assessment: specificationResult(v2Records, 2), metric_profile: { artifact_ref: childArtifact, assessment_ref: childAssessment } };
  const childRecord = { artifact_ref: childArtifact };
  const dynamic = {
    artifact_ref: childArtifact,
    criterion_binding: { binding_id: { artifact_ref: childArtifact } },
    observation_resolution: {},
    conformance: { dynamic_assessment_ref: { artifact_ref: childArtifact } },
    feature_profile: childRecord,
    product_quality_assessment: childRecord,
    problem_resolutions: [childRecord],
    defect_population: childRecord,
    target_problem_resolution: childRecord,
    defect_quality_relation: childRecord,
    risk_assessment: { risk_assessment_id: { id: "RISK-v2" }, artifact_ref: childArtifact },
  };
  const evidenceReuseDecisions = [{
    source_evidence_ref: { evidence_id: "OBSERVATION" }, target_process_state_ref: processV2, decision: "REUSE_ALLOWED",
    exact_identity_checks: [{ field_name: "product_ref", expected: { id: "PRODUCT" }, actual: { id: "PRODUCT" }, matches: true }],
    reason_codes: ["EXACT_IDENTITY_AND_CONTEXT_MATCH"], provenance: { source_process_state_ref: processV1, target_process_state_ref: processV2, source_contract_ref: fullModelContract, reassessment_rule_ref: reassessmentRule },
  }];
  const refs = [
    { result_family: "CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH", result_id: childAssessment, artifact_ref: childArtifact },
    { result_family: "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH", result_id: { id: "RISK-v2" }, artifact_ref: childArtifact },
  ];
  const context = { predecessor_process_state_ref: processV1, action_application_ref: applicationRef, parent_artifact_ref: parentArtifact, child_artifact_ref: childArtifact, child_assessment_ref: childAssessment, full_model_contract_ref: fullModelContract, component_version_set: componentVersionSet, evidence_reuse_decisions: evidenceReuseDecisions, stage: "REFERENCE_VERIFICATION" };
  const reassessmentRef = { reassessment_id: "REASSESSMENT", reassessment_version: "1" };
  const reassessment = {
    ...reassessmentRef, context, status: "AVAILABLE", child_process_state_ref: processV2, produced_result_refs: refs, comparison_request_refs: [], reason_codes: ["FULL_MODEL_PATH_REBUILT"], rule_ref: reassessmentRule,
    provenance: { reassessment_ref: reassessmentRef, action_application_ref: applicationRef, predecessor_process_state_ref: processV1, child_process_state_ref: processV2, parent_artifact_ref: parentArtifact, child_artifact_ref: childArtifact, child_assessment_ref: childAssessment, produced_result_refs: refs, component_version_set: componentVersionSet, evidence_reuse_decisions: evidenceReuseDecisions, full_model_contract_ref: fullModelContract, process_reassessment_contract_ref: processContract, rule_ref: reassessmentRule },
    produced_results: [core, dynamic],
  };
  const comparisons = [comparison("QB_CONSISTENCY", 1), comparison("CONFIRMED_PROBLEM", 2), comparison("BOUNDED_RISK", 3), comparison("PRODUCT_QUALITY", 4)];
  return {
    contract_version: "research-api-v1", analysis_case: analysisCase, controlled_scenario: { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" },
    requirements: [], specification: {}, section_availability: [
      { section: "reassessment", availability: "AVAILABLE", reason_code: null },
      { section: "comparison", availability: "AVAILABLE", reason_code: null },
    ],
    full_model: { initial_specification: initial, revised_specification: revised, initial_specification_assessment: initialAssessment, action_application: { ...applicationRef }, process_v1: processV1, process_v2: processV2, reassessment, comparisons },
    reassessment_context: {}, limitations: [],
  };
}

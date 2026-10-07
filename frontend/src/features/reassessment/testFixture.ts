import type { CanonicalAnalyzeResponse } from "../../api/analyze";

const reassessmentRule = { rule_id: "REEVAL-FULL-MODEL-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const comparisonRule = { rule_id: "COMPARE-FULL-MODEL-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const applicationRule = { rule_id: "APPLY-EXTERNAL-REVISION-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const fullModelContract = { contract_id: "FULL-MODEL-V0.1-CONTRACT", version: "1" };
const processContract = { contract_id: "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", version: "1" };
const scenario = { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" };
const parentArtifact = { artifact_id: "SPEC", artifact_version: "v1" };
const childArtifact = { artifact_id: "SPEC", artifact_version: "v2" };
const processV1 = { process_state_id: "PROCESS", process_state_version: "v1", process_lineage_id: "PROCESS", stage: "REFERENCE_VERIFICATION", artifact_ref: parentArtifact };
const processV2 = { process_state_id: "PROCESS", process_state_version: "v2", process_lineage_id: "PROCESS", stage: "REFERENCE_VERIFICATION", artifact_ref: childArtifact };
const processRefV1 = { process_state_id: "PROCESS", process_state_version: "v1", stage: "REFERENCE_VERIFICATION" };
const processRefV2 = { process_state_id: "PROCESS", process_state_version: "v2", stage: "REFERENCE_VERIFICATION" };
const childAssessment = { assessment_id: "ASSESS", assessment_version: "v2", artifact_ref: childArtifact };
const revisionRef = { revision_id: "REVISION-REFERENCE", revision_version: "1" };
const providerRef = { provider_id: "REFERENCE_FIXTURE", provider_version: "1" };
const applicationRef = { application_id: { application_instance_id: "APPLICATION", revision_ref: revisionRef, child_artifact_ref: childArtifact }, application_version: "1" };
const transitionId = { transition_instance_id: "ARTIFACT-TRANSITION", application_ref: applicationRef };
const componentVersionSet = { components: [
  { component_role: "FULL_MODEL_CONTRACT", component_id: "FULL-MODEL-V0.1-CONTRACT", component_version: "1" },
  { component_role: "REASSESSMENT_RULE", component_id: "REEVAL-FULL-MODEL-001", component_version: "1" },
] };

function requirement(id: string, sourceLine: number, text: string, state: "COMPUTED" | "UNKNOWN" | "NOT_APPLICABLE", numerator: number | null) {
  const assessment = (characteristicId: string) => ({ characteristic_id: characteristicId, state, value: numerator === null ? null : { numerator, denominator: 3 }, assessment_rule_id: state === "COMPUTED" ? `RULE-${characteristicId}` : null, findings: [], explanation: "Canonical." });
  return { extraction_result: { requirement: { id, source_line: sourceLine, text } }, quality_profile: { completeness: assessment("COMPLETENESS"), verifiability: assessment("VERIFIABILITY"), unambiguity: assessment("UNAMBIGUITY") } };
}

function metric(state: "COMPUTED" | "UNKNOWN" | "NOT_APPLICABLE", numerator: number | null) {
  return { state, value: numerator === null ? null : { numerator, denominator: 3 }, computed_count: state === "COMPUTED" ? 2 : 0, unknown_count: state === "UNKNOWN" ? 2 : 0, not_applicable_count: state === "NOT_APPLICABLE" ? 2 : 0, total_count: 2 };
}

function specificationResult(records: unknown[], state: "COMPUTED" | "UNKNOWN" | "NOT_APPLICABLE", numerator: number | null) {
  return { records, specification_assessment: { quality_profile: { completeness: metric(state, numerator), verifiability: metric(state, numerator), unambiguity: metric(state, numerator) }, qb_consistency: { state, value: numerator === null ? null : { numerator, denominator: 2 }, reasons: state === "COMPUTED" ? [] : ["CANONICAL_ABSENCE"] } } };
}

function modelComparison(family: string, index: number, canonicalTransitionId: unknown) {
  const beforeRef = { result_family: "FULL-MODEL-SERVICE-COMPARABLE", result_id: { id: `BEFORE-${index}` }, artifact_ref: parentArtifact };
  const afterRef = { result_family: "FULL-MODEL-SERVICE-COMPARABLE", result_id: { id: `AFTER-${index}` }, artifact_ref: childArtifact };
  const compatibility = index === 2 ? ["DECLARATION-A", "DECLARATION-B"] : [];
  const kind = index === 1 ? "INCREASED" : index === 2 ? "DECREASED" : index === 3 ? "STATE_CHANGED" : "UNCHANGED";
  return {
    comparison_id: `COMPARISON-${index}`, comparison_version: "1", before_result_ref: beforeRef, after_result_ref: afterRef,
    comparison_subject: { result_family: family, metric_or_characteristic_id: `METRIC-${index}`, stable_subject_identity: ["SUBJECT"], ordered_lineage_population: [], scope_identity: ["SCOPE"], evidence_context: ["EVIDENCE"] },
    status: "AVAILABLE", comparison_kind: kind,
    before_state_and_value: { status: "AVAILABLE", applicability: "APPLICABLE", exact_value: index === 1 ? { numerator: 1, denominator: 2 } : null, categorical_state: index === 1 ? null : "BEFORE_STATE" },
    after_state_and_value: { status: "AVAILABLE", applicability: "APPLICABLE", exact_value: index === 1 ? { numerator: 1, denominator: 1 } : null, categorical_state: index === 1 ? null : index === 4 ? "BEFORE_STATE" : "AFTER_STATE" },
    reason_codes: [index === 1 ? "EXACT_VALUE_INCREASED" : index === 4 ? "STRUCTURED_STATE_UNCHANGED" : "STRUCTURED_STATE_CHANGED"],
    rule_ref: comparisonRule, compatibility_declaration_refs: compatibility, parameter_set_refs: [{ parameter_set_id: "PARAMETERS-A" }, { parameter_set_id: "PARAMETERS-B" }], calibration_status_or_none: "PROVISIONAL_NOT_CALIBRATED",
    explanation: "Canonical structured comparison.", provenance: [{ comparison_id: `COMPARISON-${index}`, comparison_version: "1" }, canonicalTransitionId, beforeRef, afterRef, ...compatibility, comparisonRule],
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
  const initial = {
    artifact_ref: parentArtifact, parent_artifact_ref: null, created_by_application_ref: null,
    requirements: [{ lineage_id: lineage1, subject_ref: subject1v1, text: "Original one", predecessor_subject_ref: null }, { lineage_id: lineage2, subject_ref: subject2v1, text: "Original two", predecessor_subject_ref: null }], changed_subjects: [],
    provenance: { artifact_ref: parentArtifact, parent_artifact_ref: null, application_ref: null, revision_ref: null, process_reassessment_contract_ref: processContract, application_rule_ref_or_none: null },
  };
  const changed = { lineage_id: lineage2, before_subject_ref: subject2v1, after_subject_ref: subject2v2, change_kind: "REPLACE_TEXT" };
  const revised = {
    artifact_ref: childArtifact, parent_artifact_ref: parentArtifact, created_by_application_ref: applicationRef,
    requirements: [{ lineage_id: lineage1, subject_ref: subject1v2, text: "Original one", predecessor_subject_ref: subject1v1 }, { lineage_id: lineage2, subject_ref: subject2v2, text: "Revised two", predecessor_subject_ref: subject2v1 }], changed_subjects: [changed],
    provenance: { artifact_ref: childArtifact, parent_artifact_ref: parentArtifact, application_ref: applicationRef, revision_ref: revisionRef, process_reassessment_contract_ref: processContract, application_rule_ref_or_none: applicationRule },
  };
  const v1Records = [requirement("R001", 1, "Original one", "COMPUTED", 1), requirement("R002", 2, "Original two", "COMPUTED", 1)];
  const v2Records = [requirement("R001", 1, "Original one", "COMPUTED", 2), requirement("R002", 2, "Revised two", "COMPUTED", 2)];
  const initialAssessment = specificationResult(v1Records, "COMPUTED", 1);
  const core = { specification_version: revised, requirement_records: v2Records, specification_assessment: specificationResult(v2Records, "COMPUTED", 2), metric_profile: { artifact_ref: childArtifact, assessment_ref: childAssessment } };
  const childRecord = { artifact_ref: childArtifact };
  const dynamic = { artifact_ref: childArtifact, criterion_binding: { binding_id: { artifact_ref: childArtifact } }, observation_resolution: {}, conformance: { dynamic_assessment_ref: { artifact_ref: childArtifact } }, feature_profile: childRecord, product_quality_assessment: childRecord, problem_resolutions: [childRecord], defect_population: childRecord, target_problem_resolution: childRecord, defect_quality_relation: childRecord, risk_assessment: { risk_assessment_id: { id: "RISK-v2" }, artifact_ref: childArtifact } };
  const evidenceReuseDecisions = [{ source_evidence_ref: { observation_id: "OBSERVATION" }, target_process_state_ref: processRefV2, decision: "REUSE_ALLOWED", exact_identity_checks: [{ field_name: "product_ref", expected: { product_id: "PRODUCT" }, actual: { product_id: "PRODUCT" }, matches: true }], reason_codes: ["EXACT_IDENTITY_AND_CONTEXT_MATCH"], provenance: { source_process_state_ref: processRefV1, target_process_state_ref: processRefV2, source_contract_ref: { contract_id: "FULL-MODEL-V0.1-DYNAMIC-EVIDENCE", version: "1" }, reassessment_rule_ref: reassessmentRule } }];
  const refs = [{ result_family: "CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH", result_id: childAssessment, artifact_ref: childArtifact }, { result_family: "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH", result_id: { id: "RISK-v2" }, artifact_ref: childArtifact }];
  const reassessmentContext = { predecessor_process_state_ref: processRefV1, action_application_ref: applicationRef, parent_artifact_ref: parentArtifact, child_artifact_ref: childArtifact, child_assessment_ref: childAssessment, full_model_contract_ref: fullModelContract, component_version_set: componentVersionSet, evidence_reuse_decisions: evidenceReuseDecisions, stage: "REFERENCE_VERIFICATION" };
  const reassessmentRef = { reassessment_id: "REASSESSMENT", reassessment_version: "1" };
  const reassessment = { ...reassessmentRef, context: reassessmentContext, status: "AVAILABLE", child_process_state_ref: processRefV2, produced_result_refs: refs, comparison_request_refs: [], reason_codes: ["FULL_MODEL_PATH_REBUILT"], rule_ref: reassessmentRule, provenance: { reassessment_ref: reassessmentRef, action_application_ref: applicationRef, predecessor_process_state_ref: processRefV1, child_process_state_ref: processRefV2, parent_artifact_ref: parentArtifact, child_artifact_ref: childArtifact, child_assessment_ref: childAssessment, produced_result_refs: refs, component_version_set: componentVersionSet, evidence_reuse_decisions: evidenceReuseDecisions, full_model_contract_ref: fullModelContract, process_reassessment_contract_ref: processContract, rule_ref: reassessmentRule }, produced_results: [core, dynamic] };
  const actionRef = { action_id: { action_instance_id: "ACTION" }, action_record_version: "1" };
  const externalRevision = { revision_id: revisionRef.revision_id, revision_version: revisionRef.revision_version, provider_kind: "CONTROLLED_REFERENCE_FIXTURE", provider_ref: providerRef, action_ref: actionRef, parent_artifact_ref: parentArtifact, requested_child_artifact_ref: childArtifact, replacements: [{ lineage_id: lineage2, expected_parent_subject_ref: subject2v1, replacement_text: "Revised two" }], provider_rationale_or_none: "Externally supplied reference revision.", status: null, applicability: null, provenance: { revision_ref: revisionRef, action_ref: actionRef, parent_artifact_ref: parentArtifact, requested_child_artifact_ref: childArtifact, provider_ref: providerRef, process_reassessment_contract_ref: processContract, application_rule_ref: applicationRule } };
  const actionApplication = { ...applicationRef, status: "AVAILABLE", parent_artifact_ref: parentArtifact, child_artifact_ref: childArtifact, revision_ref: revisionRef, transition: { transition_id: transitionId, parent_artifact_ref: parentArtifact, child_artifact_ref: childArtifact, action_application_ref: applicationRef, revision_ref: revisionRef, changed_subjects: [changed] } };
  const comparisons = [modelComparison("QB_CONSISTENCY", 1, transitionId), modelComparison("CONFIRMED_PROBLEM", 2, transitionId), modelComparison("BOUNDED_RISK", 3, transitionId), modelComparison("PRODUCT_QUALITY", 4, transitionId)];
  const processTransition = { transition_id: { transition_id: "PROCESS-TRANSITION" }, predecessor_process_state_ref: processRefV1, successor_process_state_ref: processRefV2, artifact_transition_ref: { transition_id: transitionId }, action_application_ref: applicationRef, reassessment_ref: reassessmentRef };
  const correctiveActionResolution = { status: "AVAILABLE", action_ref: actionRef };
  const fullModel = { initial_specification: initial, initial_specification_assessment: initialAssessment, corrective_action_resolution: correctiveActionResolution, action_application: actionApplication, external_revision: externalRevision, revised_specification: revised, process_v1: processV1, process_v2: processV2, process_transition: processTransition, reassessment, comparisons };
  const priorContext = {
    scenario: structuredClone(scenario), initial_specification: structuredClone(initial), initial_specification_assessment: structuredClone(initialAssessment), predecessor_process_state: structuredClone(processV1), corrective_action_resolution: structuredClone(correctiveActionResolution), action_application: structuredClone(actionApplication), external_revision: structuredClone(externalRevision), revised_specification: structuredClone(revised), evidence_reuse_decisions: structuredClone(evidenceReuseDecisions), reassessment_identity: { ...reassessmentRef, child_process_state_ref: structuredClone(processRefV2), component_version_set: structuredClone(componentVersionSet) }, successor_process_state: structuredClone(processV2), process_transition: structuredClone(processTransition), comparisons: structuredClone(comparisons), context_digest: "sha256:opaque-canonical-lifecycle-context-digest",
  };
  return structuredClone({ contract_version: "research-api-v1", analysis_case: analysisCase, controlled_scenario: structuredClone(scenario), requirements: analysisCase === "CONTROLLED_DEMO" ? [] : structuredClone(v2Records), specification: {}, section_availability: [{ section: "reassessment", availability: "AVAILABLE", reason_code: null }, { section: "comparison", availability: "AVAILABLE", reason_code: null }], full_model: fullModel, reassessment_context: priorContext, limitations: [] }) as CanonicalAnalyzeResponse;
}

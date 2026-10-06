import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactRational } from "../../components/scientific/ExactValue";
import { structuralEqual } from "../results/structuralIdentity";

const FULL_MODEL_CONTRACT = { contract_id: "FULL-MODEL-V0.1-CONTRACT", version: "1" };
const PROCESS_CONTRACT = { contract_id: "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", version: "1" };
const PROCESS_RULE = { rule_id: "PROCESS-REFERENCE-VERIFICATION-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const CHECKPOINT_CONTRACT = { contract_id: "FULL-MODEL-V1.0-SCALAR-CHECKPOINT", version: "1" };
const CHECKPOINT_RULE = { rule_id: "CHECKPOINT-SCALAR-PREDICATE-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const PROCESS_STAGE = "REFERENCE_VERIFICATION";

export const COMPONENT_ROLES = [
  "REQUIREMENT_ASSESSMENT",
  "SPECIFICATION_ASSESSMENT",
  "METRIC_PROFILE",
  "PE_FEATURE_PROFILE",
  "PRODUCT_QUALITY_ASSESSMENT",
  "DEFECT_POPULATION",
  "CONFIRMED_PROBLEM",
  "DEFECT_QUALITY_RELATION",
  "BOUNDED_RISK_ASSESSMENT",
  "CORRECTIVE_ACTION",
] as const;

export const EVIDENCE_ROLES = [
  "STATIC_REQUIREMENT",
  "QB",
  "DYNAMIC_CRITERION",
  "DYNAMIC_OBSERVATION",
  "CONFORMANCE",
] as const;

const FULL_MODEL_STATUSES = ["AVAILABLE", "NOT_APPLICABLE", "UNAVAILABLE", "UNKNOWN", "UNRESOLVED", "UNSUPPORTED"] as const;
const APPLICABILITIES = ["APPLICABLE", "UNKNOWN", "NOT_APPLICABLE"] as const;
const COMPARATORS = [">=", ">", "<=", "<", "=="] as const;
const OUTCOMES = ["SATISFIED", "NOT_SATISFIED", "UNRESOLVED", "NOT_APPLICABLE"] as const;
const REASONS = [
  "PREDICATE_TRUE",
  "PREDICATE_FALSE",
  "SOURCE_NOT_APPLICABLE",
  "SOURCE_VALUE_UNRESOLVED",
  "ARTIFACT_PROVENANCE_MISMATCH",
  "PROCESS_STATE_PROVENANCE_MISMATCH",
] as const;

type RecordValue = Record<string, unknown>;
type FullModelStatus = typeof FULL_MODEL_STATUSES[number];
type Applicability = typeof APPLICABILITIES[number];

export interface ProcessAssociationProjection {
  role: string;
  ref: unknown | null;
  status: FullModelStatus;
  applicability: Applicability;
  subjectOrScope: unknown;
  source: unknown;
  reasonCodes: unknown[];
  provenance: unknown[];
  raw: RecordValue;
}

export interface EvidenceAssociationProjection {
  role: string;
  ref: unknown | null;
  status: FullModelStatus;
  applicability: Applicability;
  artifactOrProduct: unknown;
  sourceOrCollection: unknown;
  context: unknown | null;
  reuseDecision: unknown | null;
  reasonCodes: unknown[];
  provenance: unknown[];
  raw: RecordValue;
}

export interface ProcessStateProjection {
  id: string;
  version: string;
  lineageId: string;
  stage: typeof PROCESS_STAGE;
  ref: RecordValue;
  artifactRef: RecordValue;
  assessmentRef: RecordValue;
  predecessorRef: RecordValue | null;
  artifactTransitionRef: RecordValue | null;
  reassessmentRef: RecordValue | null;
  metricProfileRef: RecordValue;
  componentVersionSet: RecordValue;
  components: ProcessAssociationProjection[];
  evidence: EvidenceAssociationProjection[];
  provenance: RecordValue;
  raw: RecordValue;
}

export interface ProcessTransitionProjection {
  transitionId: string;
  predecessorRef: RecordValue;
  successorRef: RecordValue;
  artifactTransitionRef: RecordValue;
  actionApplicationRef: RecordValue;
  reassessmentRef: RecordValue;
  comparisonRefs: unknown[];
  ruleRef: RecordValue;
  provenance: RecordValue;
  raw: RecordValue;
}

export interface CheckpointProjection {
  checkpointId: string;
  checkpointVersion: string;
  processStateRef: RecordValue;
  artifactRef: RecordValue;
  processStateVersion: string;
  selectedResult: {
    identity: string;
    status: FullModelStatus;
    applicability: Applicability;
    exactValue: ExactRational | null;
    resultRef: unknown;
    governingRef: RecordValue;
    reasonCodes: unknown[];
    provenance: unknown[];
  };
  policy: {
    policyId: string;
    policyVersion: string;
    sourceRef: RecordValue;
    providerRef: RecordValue;
    rationale: string;
    comparator: typeof COMPARATORS[number];
    threshold: ExactRational;
    governingContractRef: RecordValue;
  };
  outcome: typeof OUTCOMES[number];
  reasonCode: typeof REASONS[number];
  checkpointContractRef: RecordValue;
  evaluatorRuleRef: RecordValue;
  provenance: RecordValue;
  raw: RecordValue;
}

export type CheckpointPresentation =
  | { kind: "AVAILABLE"; value: CheckpointProjection; raw: unknown }
  | { kind: "MALFORMED"; raw: unknown };

export type ProcessPageProjection =
  | { kind: "UNAVAILABLE"; reasonCode: string }
  | { kind: "MALFORMED" }
  | {
      kind: "AVAILABLE";
      predecessor: ProcessStateProjection;
      transition: ProcessTransitionProjection;
      successor: ProcessStateProjection;
      current: ProcessStateProjection;
      checkpoints: CheckpointPresentation[];
      checkpointPopulationMalformed: boolean;
    };

function record(value: unknown): RecordValue | null {
  return typeof value === "object" && value !== null && !Array.isArray(value) ? value as RecordValue : null;
}

function array(value: unknown): unknown[] | null {
  return Array.isArray(value) ? value : null;
}

function canonicalString(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 && value === value.trim() && !/[\u0000-\u001f]/u.test(value) ? value : null;
}

function member<T extends readonly string[]>(value: unknown, values: T): T[number] | null {
  return typeof value === "string" && values.includes(value) ? value as T[number] : null;
}

function exactFraction(value: unknown): ExactRational | null {
  const candidate = record(value);
  if (!candidate || !Number.isSafeInteger(candidate.numerator) || !Number.isSafeInteger(candidate.denominator) || Number(candidate.denominator) <= 0) return null;
  return { numerator: String(candidate.numerator), denominator: String(candidate.denominator) };
}

function canonicalObject(value: unknown): RecordValue | null {
  const candidate = record(value);
  if (!candidate || Object.values(candidate).some((entry) => typeof entry === "string" && canonicalString(entry) === null)) return null;
  return candidate;
}

function artifactRef(value: unknown): RecordValue | null {
  const candidate = record(value);
  return candidate && canonicalString(candidate.artifact_id) && canonicalString(candidate.artifact_version) ? candidate : null;
}

function assessmentRef(value: unknown): RecordValue | null {
  const candidate = record(value);
  return candidate && canonicalString(candidate.assessment_id) && canonicalString(candidate.assessment_version) && artifactRef(candidate.artifact_ref) ? candidate : null;
}

function processRef(value: unknown): RecordValue | null {
  const candidate = record(value);
  return candidate
    && canonicalString(candidate.process_state_id)
    && canonicalString(candidate.process_state_version)
    && candidate.stage === PROCESS_STAGE
    ? candidate : null;
}

function contractRef(value: unknown): RecordValue | null {
  const candidate = record(value);
  return candidate && canonicalString(candidate.contract_id) && canonicalString(candidate.version) ? candidate : null;
}

function statusApplicability(statusValue: unknown, applicabilityValue: unknown): { status: FullModelStatus; applicability: Applicability } | null {
  const status = member(statusValue, FULL_MODEL_STATUSES);
  const applicability = member(applicabilityValue, APPLICABILITIES);
  if (!status || !applicability) return null;
  const allowed: Record<FullModelStatus, readonly Applicability[]> = {
    AVAILABLE: ["APPLICABLE"],
    NOT_APPLICABLE: ["NOT_APPLICABLE"],
    UNAVAILABLE: ["APPLICABLE", "UNKNOWN"],
    UNKNOWN: ["APPLICABLE", "UNKNOWN"],
    UNRESOLVED: ["APPLICABLE", "UNKNOWN"],
    UNSUPPORTED: ["APPLICABLE", "UNKNOWN"],
  };
  return allowed[status].includes(applicability) ? { status, applicability } : null;
}

function canonicalReasonArray(value: unknown, requireNonEmpty = false): unknown[] | null {
  const values = array(value);
  if (!values || (requireNonEmpty && values.length === 0) || values.some((entry) => typeof entry === "string" && canonicalString(entry) === null)) return null;
  return values;
}

function validateComponentVersions(value: unknown): RecordValue | null {
  const candidate = record(value);
  const components = candidate && array(candidate.components);
  if (!candidate || !components || components.length === 0) return null;
  const roles = new Set<string>();
  for (const value of components) {
    const component = record(value);
    const role = component && canonicalString(component.component_role);
    if (!component || !role || !canonicalString(component.component_id) || !canonicalString(component.component_version) || roles.has(role)) return null;
    roles.add(role);
  }
  return candidate;
}

function projectComponents(value: unknown): ProcessAssociationProjection[] | null {
  const values = array(value);
  if (!values) return null;
  const projected: ProcessAssociationProjection[] = [];
  let previousOrder = -1;
  const seen = new Set<string>();
  for (const value of values) {
    const candidate = record(value);
    const role = candidate && canonicalString(candidate.role);
    const order = role ? COMPONENT_ROLES.indexOf(role as typeof COMPONENT_ROLES[number]) : -1;
    const state = candidate && statusApplicability(candidate.status, candidate.applicability);
    const reasons = candidate && canonicalReasonArray(candidate.reason_codes, candidate.result_ref == null);
    const provenance = candidate && array(candidate.provenance);
    if (!candidate || !role || order < 0 || order < previousOrder || !state || !reasons || !provenance || provenance.length === 0
      || candidate.subject_or_scope_ref == null || !canonicalObject(candidate.producing_contract_or_rule_ref)
      || (state.status === "AVAILABLE" && candidate.result_ref == null)) return null;
    previousOrder = order;
    seen.add(role);
    projected.push({
      role, ref: candidate.result_ref ?? null, ...state,
      subjectOrScope: candidate.subject_or_scope_ref,
      source: candidate.producing_contract_or_rule_ref,
      reasonCodes: reasons, provenance, raw: candidate,
    });
  }
  if (COMPONENT_ROLES.some((role) => !seen.has(role))) return null;
  return projected;
}

function projectEvidence(value: unknown, ownArtifact: RecordValue, ownProcessRef: RecordValue): EvidenceAssociationProjection[] | null {
  const values = array(value);
  if (!values) return null;
  const projected: EvidenceAssociationProjection[] = [];
  let previousOrder = -1;
  const seen = new Set<string>();
  for (const value of values) {
    const candidate = record(value);
    const role = candidate && canonicalString(candidate.role);
    const order = role ? EVIDENCE_ROLES.indexOf(role as typeof EVIDENCE_ROLES[number]) : -1;
    const state = candidate && statusApplicability(candidate.status, candidate.applicability);
    const reasons = candidate && canonicalReasonArray(candidate.reason_codes, candidate.evidence_ref == null);
    const provenance = candidate && array(candidate.provenance);
    const owner = candidate && canonicalObject(candidate.artifact_or_product_ref);
    const source = candidate && canonicalObject(candidate.source_or_collection_ref);
    const reuse = candidate?.reuse_decision_ref_or_none == null ? null : record(candidate.reuse_decision_ref_or_none);
    if (!candidate || !role || order < 0 || order < previousOrder || !state || !reasons || !provenance || provenance.length === 0 || !owner || !source
      || (state.status === "AVAILABLE" && candidate.evidence_ref == null)
      || ("artifact_id" in owner && !structuralEqual(owner, ownArtifact))
      || (candidate.reuse_decision_ref_or_none != null && (!reuse || !structuralEqual(reuse.target_process_state_ref, ownProcessRef)))) return null;
    previousOrder = order;
    seen.add(role);
    projected.push({
      role, ref: candidate.evidence_ref ?? null, ...state,
      artifactOrProduct: owner, sourceOrCollection: source,
      context: candidate.context_ref_or_none ?? null,
      reuseDecision: candidate.reuse_decision_ref_or_none ?? null,
      reasonCodes: reasons, provenance, raw: candidate,
    });
  }
  if (EVIDENCE_ROLES.some((role) => !seen.has(role))) return null;
  return projected;
}

function associationRefs(components: ProcessAssociationProjection[], role: string): unknown[] {
  return components.filter((item) => item.role === role && item.ref !== null).map((item) => item.ref);
}

function optionalArray(value: unknown): unknown[] | null {
  return value == null ? [] : [value];
}

function validateConvenienceRefs(state: RecordValue, components: ProcessAssociationProjection[]): boolean {
  const requirements = array(state.requirement_assessment_refs);
  const confirmed = array(state.confirmed_problem_refs);
  const relations = array(state.defect_quality_relation_refs);
  const risks = array(state.bounded_risk_assessment_refs);
  const actions = array(state.corrective_action_refs);
  if (!requirements || !confirmed || !relations || !risks || !actions) return false;
  const expected: Array<[string, unknown[] | null]> = [
    ["REQUIREMENT_ASSESSMENT", requirements],
    ["SPECIFICATION_ASSESSMENT", [state.specification_assessment_ref]],
    ["METRIC_PROFILE", [state.metric_profile_ref]],
    ["PE_FEATURE_PROFILE", optionalArray(state.pe_feature_profile_ref)],
    ["PRODUCT_QUALITY_ASSESSMENT", optionalArray(state.product_quality_assessment_ref)],
    ["DEFECT_POPULATION", [state.defect_population_ref]],
    ["CONFIRMED_PROBLEM", confirmed],
    ["DEFECT_QUALITY_RELATION", relations],
    ["BOUNDED_RISK_ASSESSMENT", risks],
    ["CORRECTIVE_ACTION", actions],
  ];
  return expected.every(([role, refs]) => refs !== null && structuralEqual(associationRefs(components, role), refs));
}

function validateCurrentRefs(state: RecordValue, ownRef: RecordValue, ownArtifact: RecordValue, ownAssessment: RecordValue): boolean {
  const requirementRefs = array(state.requirement_assessment_refs);
  const specification = record(state.specification_assessment_ref);
  const metric = record(state.metric_profile_ref);
  const feature = state.pe_feature_profile_ref == null ? null : record(state.pe_feature_profile_ref);
  const quality = state.product_quality_assessment_ref == null ? null : record(state.product_quality_assessment_ref);
  const population = record(record(state.defect_population_ref)?.population_id);
  const problems = array(state.confirmed_problem_refs);
  const relations = array(state.defect_quality_relation_refs);
  const risks = array(state.bounded_risk_assessment_refs);
  if (!requirementRefs || !specification || !metric || !population || !problems || !relations || !risks) return false;
  if (requirementRefs.some((value) => {
    const item = record(value);
    const subject = item && record(item.requirement_subject_ref);
    return !item || !subject || !structuralEqual(item.assessment_ref, ownAssessment) || !structuralEqual(subject.artifact_ref, ownArtifact);
  })) return false;
  if (!structuralEqual(specification.assessment_ref, ownAssessment)
    || !structuralEqual(metric.artifact_ref, ownArtifact) || !structuralEqual(metric.assessment_ref, ownAssessment)) return false;
  if (feature && (!structuralEqual(feature.artifact_ref, ownArtifact)
    || !structuralEqual(feature.source_assessment_ref, ownAssessment)
    || !structuralEqual(feature.metric_profile_ref, metric)
    || !structuralEqual(feature.process_state_ref, ownRef))) return false;
  const qualityId = quality && record(quality.assessment_id);
  const qualityEvent = qualityId && record(qualityId.assessment_event_ref);
  const qualityFeature = qualityId && record(qualityId.feature_profile_ref);
  if (quality && (!qualityId || !qualityEvent || !qualityFeature
    || !structuralEqual(qualityEvent.artifact_ref, ownArtifact)
    || !structuralEqual(qualityFeature.process_state_ref, ownRef)
    || !structuralEqual(qualityFeature.source_assessment_ref, ownAssessment))) return false;
  if (!structuralEqual(population.artifact_ref, ownArtifact) || !structuralEqual(population.source_assessment_ref, ownAssessment)) return false;
  if (problems.some((value) => {
    const problem = record(record(value)?.problem_id);
    return !problem || !structuralEqual(problem.artifact_ref, ownArtifact) || !structuralEqual(problem.source_assessment_ref, ownAssessment);
  })) return false;
  if (relations.some((value) => {
    const resolution = record(record(record(record(value)?.relation_id)?.problem_resolution_ref)?.resolution_id);
    return !resolution || !structuralEqual(resolution.artifact_ref, ownArtifact) || !structuralEqual(resolution.source_assessment_ref, ownAssessment);
  })) return false;
  if (risks.some((value) => {
    const event = record(record(record(value)?.risk_assessment_id)?.assessment_event_ref);
    return !event || !structuralEqual(event.artifact_ref, ownArtifact) || !structuralEqual(event.process_state_ref, ownRef);
  })) return false;
  return true;
}

function projectState(value: unknown): ProcessStateProjection | null {
  const candidate = record(value);
  const id = candidate && canonicalString(candidate.process_state_id);
  const version = candidate && canonicalString(candidate.process_state_version);
  const lineageId = candidate && canonicalString(candidate.process_lineage_id);
  if (!candidate || !id || !version || lineageId !== id || candidate.stage !== PROCESS_STAGE) return null;
  const ref = { process_state_id: id, process_state_version: version, stage: PROCESS_STAGE };
  const artifact = artifactRef(candidate.artifact_ref);
  const assessment = assessmentRef(candidate.assessment_ref);
  const provenance = record(candidate.provenance);
  const versions = validateComponentVersions(candidate.component_version_set);
  if (!artifact || !assessment || !provenance || !versions || !structuralEqual(assessment.artifact_ref, artifact)
    || !structuralEqual(candidate.full_model_contract_ref, FULL_MODEL_CONTRACT)
    || !structuralEqual(provenance.process_state_ref, ref)
    || provenance.process_lineage_id !== lineageId
    || !structuralEqual(provenance.artifact_ref, artifact)
    || !structuralEqual(provenance.assessment_ref, assessment)
    || !structuralEqual(provenance.predecessor_process_state_ref, candidate.predecessor_process_state_ref)
    || !structuralEqual(provenance.artifact_transition_ref_or_none, candidate.artifact_transition_ref_or_none)
    || !structuralEqual(provenance.reassessment_ref_or_none, candidate.reassessment_ref)
    || !structuralEqual(provenance.component_version_set, versions)
    || !structuralEqual(provenance.full_model_contract_ref, FULL_MODEL_CONTRACT)
    || !structuralEqual(provenance.process_reassessment_contract_ref, PROCESS_CONTRACT)
    || !structuralEqual(provenance.rule_ref, PROCESS_RULE)) return null;
  const components = projectComponents(candidate.component_associations);
  const evidence = projectEvidence(candidate.evidence_associations, artifact, ref);
  if (!components || !evidence
    || !structuralEqual(provenance.component_associations, candidate.component_associations)
    || !structuralEqual(provenance.evidence_associations, candidate.evidence_associations)
    || !validateConvenienceRefs(candidate, components)
    || !validateCurrentRefs(candidate, ref, artifact, assessment)) return null;
  const predecessor = candidate.predecessor_process_state_ref == null ? null : processRef(candidate.predecessor_process_state_ref);
  const artifactTransition = candidate.artifact_transition_ref_or_none == null ? null : record(candidate.artifact_transition_ref_or_none);
  const reassessment = candidate.reassessment_ref == null ? null : record(candidate.reassessment_ref);
  const metric = record(candidate.metric_profile_ref);
  if ((candidate.predecessor_process_state_ref != null && !predecessor)
    || (candidate.artifact_transition_ref_or_none != null && !artifactTransition)
    || (candidate.reassessment_ref != null && !reassessment) || !metric) return null;
  return {
    id, version, lineageId, stage: PROCESS_STAGE, ref, artifactRef: artifact,
    assessmentRef: assessment, predecessorRef: predecessor,
    artifactTransitionRef: artifactTransition, reassessmentRef: reassessment,
    metricProfileRef: metric, componentVersionSet: versions,
    components, evidence, provenance, raw: candidate,
  };
}

function refFromApplication(value: unknown): RecordValue | null {
  const application = record(value);
  const applicationId = application && record(application.application_id);
  return application && applicationId && canonicalString(applicationId.application_instance_id) && canonicalString(application.application_version)
    ? { application_id: applicationId, application_version: application.application_version } : null;
}

function refFromReassessment(value: unknown): RecordValue | null {
  const reassessment = record(value);
  return reassessment && canonicalString(reassessment.reassessment_id) && canonicalString(reassessment.reassessment_version)
    ? { reassessment_id: reassessment.reassessment_id, reassessment_version: reassessment.reassessment_version } : null;
}

function projectTransition(value: unknown, predecessor: ProcessStateProjection, successor: ProcessStateProjection): ProcessTransitionProjection | null {
  const candidate = record(value);
  const transitionIdentity = candidate && record(candidate.transition_id);
  const transitionId = transitionIdentity && canonicalString(transitionIdentity.transition_id);
  const provenance = candidate && record(candidate.provenance);
  const comparisonRefs = candidate && array(candidate.comparison_refs);
  const artifactTransition = candidate && record(candidate.artifact_transition_ref);
  const actionApplication = candidate && record(candidate.action_application_ref);
  const reassessment = candidate && record(candidate.reassessment_ref);
  if (!candidate || !transitionId || !provenance || !comparisonRefs || !artifactTransition || !actionApplication || !reassessment
    || !structuralEqual(candidate.predecessor_process_state_ref, predecessor.ref)
    || !structuralEqual(candidate.successor_process_state_ref, successor.ref)
    || !structuralEqual(candidate.rule_ref, PROCESS_RULE)
    || !structuralEqual(provenance.predecessor_process_state_ref, candidate.predecessor_process_state_ref)
    || !structuralEqual(provenance.successor_process_state_ref, candidate.successor_process_state_ref)
    || !structuralEqual(provenance.artifact_transition_ref, artifactTransition)
    || !structuralEqual(provenance.action_application_ref, actionApplication)
    || !structuralEqual(provenance.reassessment_ref, reassessment)
    || !structuralEqual(provenance.comparison_refs, comparisonRefs)
    || !structuralEqual(provenance.process_reassessment_contract_ref, PROCESS_CONTRACT)
    || !structuralEqual(provenance.rule_ref, PROCESS_RULE)) return null;
  return {
    transitionId, predecessorRef: predecessor.ref, successorRef: successor.ref,
    artifactTransitionRef: artifactTransition, actionApplicationRef: actionApplication,
    reassessmentRef: reassessment, comparisonRefs, ruleRef: candidate.rule_ref as RecordValue,
    provenance, raw: candidate,
  };
}

function validateLifecycleGraph(fullModel: RecordValue, predecessor: ProcessStateProjection, successor: ProcessStateProjection, transition: ProcessTransitionProjection): boolean {
  if (predecessor.id !== successor.id || predecessor.version === successor.version || predecessor.stage !== successor.stage) return false;
  const predecessorProvenance = predecessor.provenance;
  const successorProvenance = successor.provenance;
  if (predecessor.predecessorRef !== null || predecessor.artifactTransitionRef !== null || predecessor.reassessmentRef !== null
    || predecessorProvenance.predecessor_process_state_ref !== null
    || predecessorProvenance.artifact_transition_ref_or_none !== null
    || predecessorProvenance.action_application_ref_or_none !== null
    || predecessorProvenance.reassessment_ref_or_none !== null
    || !structuralEqual(predecessorProvenance.comparison_refs, [])) return false;
  const successorComparisons = array(successorProvenance.comparison_refs);
  const successorAction = record(successorProvenance.action_application_ref_or_none);
  if (!structuralEqual(successor.predecessorRef, predecessor.ref) || !successor.artifactTransitionRef || !successor.reassessmentRef
    || !successorAction || !successorComparisons) return false;
  const revisedSpecification = record(fullModel.revised_specification);
  const application = record(fullModel.action_application);
  const applicationTransition = application && record(application.transition);
  const applicationTransitionId = applicationTransition && record(applicationTransition.transition_id);
  const applicationRef = refFromApplication(application);
  const reassessmentRecord = record(fullModel.reassessment);
  const reassessmentRef = refFromReassessment(reassessmentRecord);
  const reassessmentContext = reassessmentRecord && record(reassessmentRecord.context);
  const reassessmentProvenance = reassessmentRecord && record(reassessmentRecord.provenance);
  const expectedArtifactTransition = applicationTransitionId ? { transition_id: applicationTransitionId } : null;
  if (!revisedSpecification || !application || !applicationTransition || !applicationRef || !reassessmentRecord || !reassessmentRef || !reassessmentContext || !reassessmentProvenance || !expectedArtifactTransition
    || !structuralEqual(revisedSpecification.artifact_ref, successor.artifactRef)
    || !structuralEqual(application.child_artifact_ref, successor.artifactRef)
    || !structuralEqual(reassessmentRecord.child_process_state_ref, successor.ref)
    || !structuralEqual(reassessmentContext.predecessor_process_state_ref, predecessor.ref)
    || !structuralEqual(reassessmentContext.action_application_ref, applicationRef)
    || !structuralEqual(reassessmentContext.parent_artifact_ref, predecessor.artifactRef)
    || !structuralEqual(reassessmentContext.child_artifact_ref, successor.artifactRef)
    || !structuralEqual(reassessmentContext.child_assessment_ref, successor.assessmentRef)
    || !structuralEqual(reassessmentContext.component_version_set, successor.componentVersionSet)
    || !structuralEqual(reassessmentContext.full_model_contract_ref, FULL_MODEL_CONTRACT)
    || reassessmentContext.stage !== PROCESS_STAGE
    || !structuralEqual(reassessmentProvenance.reassessment_ref, reassessmentRef)
    || !structuralEqual(reassessmentProvenance.action_application_ref, applicationRef)
    || !structuralEqual(reassessmentProvenance.predecessor_process_state_ref, predecessor.ref)
    || !structuralEqual(reassessmentProvenance.child_artifact_ref, successor.artifactRef)
    || !structuralEqual(reassessmentProvenance.child_process_state_ref, successor.ref)
    || !structuralEqual(reassessmentProvenance.parent_artifact_ref, predecessor.artifactRef)
    || !structuralEqual(reassessmentProvenance.child_assessment_ref, successor.assessmentRef)
    || !structuralEqual(reassessmentProvenance.component_version_set, successor.componentVersionSet)
    || !structuralEqual(reassessmentProvenance.full_model_contract_ref, FULL_MODEL_CONTRACT)
    || !structuralEqual(reassessmentProvenance.process_reassessment_contract_ref, PROCESS_CONTRACT)
    || !structuralEqual(successor.artifactTransitionRef, expectedArtifactTransition)
    || !structuralEqual(successorAction, applicationRef)
    || !structuralEqual(successor.reassessmentRef, reassessmentRef)
    || !structuralEqual(transition.artifactTransitionRef, successor.artifactTransitionRef)
    || !structuralEqual(transition.actionApplicationRef, successorAction)
    || !structuralEqual(transition.reassessmentRef, successor.reassessmentRef)
    || !structuralEqual(transition.comparisonRefs, successorComparisons)) return false;
  const comparisons = array(fullModel.comparisons);
  if (comparisons) {
    const refs = comparisons.map((value) => {
      const comparison = record(value);
      return comparison && canonicalString(comparison.comparison_id) && canonicalString(comparison.comparison_version)
        ? { comparison_id: comparison.comparison_id, comparison_version: comparison.comparison_version } : null;
    });
    if (refs.some((value) => value === null) || !structuralEqual(refs, transition.comparisonRefs)) return false;
  }
  return true;
}

function projectCheckpoint(value: unknown, states: ProcessStateProjection[]): CheckpointProjection | null {
  const candidate = record(value);
  const checkpointId = candidate && canonicalString(candidate.checkpoint_id);
  const checkpointVersion = candidate && canonicalString(candidate.checkpoint_version);
  const checkpointProcess = candidate && processRef(candidate.process_state_ref);
  const checkpointArtifact = candidate && artifactRef(candidate.artifact_ref);
  const selected = candidate && record(candidate.selected_result);
  const policy = candidate && record(candidate.threshold_policy);
  const provenance = candidate && record(candidate.provenance);
  const outcome = candidate && member(candidate.outcome, OUTCOMES);
  const reasons = candidate && array(candidate.reason_codes);
  if (!candidate || !checkpointId || !checkpointVersion || !checkpointProcess || !checkpointArtifact || !selected || !policy || !provenance || !outcome || !reasons || reasons.length !== 1) return null;
  const reason = member(reasons[0], REASONS);
  const state = states.find((item) => structuralEqual(item.ref, checkpointProcess));
  if (!reason || !state || !structuralEqual(state.artifactRef, checkpointArtifact)) return null;

  const selectedState = statusApplicability(selected.status, selected.applicability);
  const identity = canonicalString(selected.result_identity);
  const selectedArtifact = artifactRef(selected.artifact_ref);
  const selectedProcess = processRef(selected.process_state_ref);
  const selectedReasons = canonicalReasonArray(selected.reason_codes);
  const selectedProvenance = array(selected.provenance);
  const governingResultRef = canonicalObject(selected.governing_contract_or_rule_ref);
  if (selected.result_ref == null || !selectedState || !identity || !selectedArtifact || !selectedProcess || !selectedReasons || !selectedProvenance || selectedProvenance.length === 0 || !governingResultRef) return null;
  const fraction = selected.exact_value == null ? null : exactFraction(selected.exact_value);
  if ((selectedState.status === "AVAILABLE" && (!fraction || selectedState.applicability !== "APPLICABLE"))
    || (selectedState.status !== "AVAILABLE" && selected.exact_value !== null)) return null;
  const artifactMatches = structuralEqual(selectedArtifact, checkpointArtifact);
  const processMatches = structuralEqual(selectedProcess, checkpointProcess);
  if (reason === "ARTIFACT_PROVENANCE_MISMATCH" ? artifactMatches : !artifactMatches) return null;
  if (reason === "PROCESS_STATE_PROVENANCE_MISMATCH" ? processMatches : !processMatches) return null;
  const resultRef = record(selected.result_ref);
  if (resultRef && "profile_id" in resultRef) {
    if (!structuralEqual(resultRef.profile_id, state.metricProfileRef) || resultRef.metric_id !== identity) return null;
  }

  const policyId = canonicalString(policy.policy_id);
  const policyVersion = canonicalString(policy.policy_version);
  const sourceRef = record(policy.source_ref);
  const providerRef = record(policy.provider_ref);
  const rationale = canonicalString(policy.rationale);
  const comparator = member(policy.comparator, COMPARATORS);
  const threshold = exactFraction(policy.threshold);
  const governingPolicyContract = contractRef(policy.governing_contract_ref);
  if (!policyId || !policyVersion || !sourceRef || !canonicalString(sourceRef.source_id) || !canonicalString(sourceRef.source_version)
    || !providerRef || !canonicalString(providerRef.provider_id) || !canonicalString(providerRef.provider_version)
    || !rationale || !comparator || !threshold || !governingPolicyContract
    || !structuralEqual(candidate.checkpoint_contract_ref, CHECKPOINT_CONTRACT)
    || !structuralEqual(candidate.evaluator_rule_ref, CHECKPOINT_RULE)) return null;

  const outcomeValid = (
    (outcome === "SATISFIED" && reason === "PREDICATE_TRUE" && selectedState.status === "AVAILABLE" && fraction !== null)
    || (outcome === "NOT_SATISFIED" && reason === "PREDICATE_FALSE" && selectedState.status === "AVAILABLE" && fraction !== null)
    || (outcome === "NOT_APPLICABLE" && reason === "SOURCE_NOT_APPLICABLE" && selectedState.status === "NOT_APPLICABLE")
    || (outcome === "UNRESOLVED" && reason === "SOURCE_VALUE_UNRESOLVED" && selectedState.status !== "AVAILABLE" && selectedState.status !== "NOT_APPLICABLE")
    || (outcome === "UNRESOLVED" && reason === "ARTIFACT_PROVENANCE_MISMATCH" && !artifactMatches)
    || (outcome === "UNRESOLVED" && reason === "PROCESS_STATE_PROVENANCE_MISMATCH" && !processMatches)
  );
  if (!outcomeValid
    || !structuralEqual(provenance.selected_result_ref, selected.result_ref)
    || !structuralEqual(provenance.selected_result_provenance, selected.provenance)
    || !structuralEqual(provenance.threshold_policy_ref, { policy_id: policyId, policy_version: policyVersion })
    || !structuralEqual(provenance.policy_source_ref, sourceRef)
    || !structuralEqual(provenance.policy_provider_ref, providerRef)
    || !structuralEqual(provenance.process_state_ref, checkpointProcess)
    || !structuralEqual(provenance.artifact_ref, checkpointArtifact)
    || !structuralEqual(provenance.governing_policy_contract_ref, governingPolicyContract)
    || !structuralEqual(provenance.checkpoint_contract_ref, CHECKPOINT_CONTRACT)
    || !structuralEqual(provenance.evaluator_rule_ref, CHECKPOINT_RULE)) return null;

  return {
    checkpointId, checkpointVersion, processStateRef: checkpointProcess,
    artifactRef: checkpointArtifact, processStateVersion: state.version,
    selectedResult: {
      identity, ...selectedState, exactValue: fraction, resultRef: selected.result_ref,
      governingRef: governingResultRef, reasonCodes: selectedReasons, provenance: selectedProvenance,
    },
    policy: {
      policyId, policyVersion, sourceRef, providerRef, rationale,
      comparator, threshold, governingContractRef: governingPolicyContract,
    },
    outcome, reasonCode: reason,
    checkpointContractRef: candidate.checkpoint_contract_ref as RecordValue,
    evaluatorRuleRef: candidate.evaluator_rule_ref as RecordValue,
    provenance, raw: candidate,
  };
}

function sectionAvailability(response: CanonicalAnalyzeResponse): { availability: "AVAILABLE" | "UNAVAILABLE"; reasonCode: string | null } | null {
  const matches = response.section_availability.filter((value) => record(value)?.section === "process");
  if (matches.length !== 1) return null;
  const candidate = record(matches[0]);
  if (!candidate || (candidate.availability !== "AVAILABLE" && candidate.availability !== "UNAVAILABLE")) return null;
  if (candidate.availability === "UNAVAILABLE") {
    const reasonCode = canonicalString(candidate.reason_code);
    return reasonCode ? { availability: "UNAVAILABLE", reasonCode } : null;
  }
  return candidate.reason_code === null ? { availability: "AVAILABLE", reasonCode: null } : null;
}

export function selectProcessPage(response: CanonicalAnalyzeResponse): ProcessPageProjection {
  const availability = sectionAvailability(response);
  if (!availability) return { kind: "MALFORMED" };
  if (availability.availability === "UNAVAILABLE") return { kind: "UNAVAILABLE", reasonCode: availability.reasonCode! };
  const fullModel = record(response.full_model);
  if (!fullModel) return { kind: "MALFORMED" };
  const predecessor = projectState(fullModel.process_v1);
  const successor = projectState(fullModel.process_v2);
  if (!predecessor || !successor) return { kind: "MALFORMED" };
  const transition = projectTransition(fullModel.process_transition, predecessor, successor);
  if (!transition || !validateLifecycleGraph(fullModel, predecessor, successor, transition)) return { kind: "MALFORMED" };
  const rawCheckpoints = array(fullModel.checkpoint_evaluations);
  if (!rawCheckpoints) return {
    kind: "AVAILABLE", predecessor, transition, successor, current: successor,
    checkpoints: [], checkpointPopulationMalformed: true,
  };
  const checkpoints = rawCheckpoints.map((raw): CheckpointPresentation => {
    const value = projectCheckpoint(raw, [predecessor, successor]);
    return value ? { kind: "AVAILABLE", value, raw } : { kind: "MALFORMED", raw };
  });
  return {
    kind: "AVAILABLE", predecessor, transition, successor, current: successor,
    checkpoints, checkpointPopulationMalformed: false,
  };
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactValueData } from "../../components/scientific";
import { structuralEqual } from "../results/structuralIdentity";

export type JsonRecord = Record<string, unknown>;

const REASSESSMENT_RULE = {
  rule_id: "REEVAL-FULL-MODEL-001",
  explicit_version: "1",
  version_authority: "EXPLICIT_CONTRACT_VERSION",
};
const FULL_MODEL_CONTRACT = { contract_id: "FULL-MODEL-V0.1-CONTRACT", version: "1" };
const PROCESS_CONTRACT = { contract_id: "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", version: "1" };
const APPLICATION_RULE = {
  rule_id: "APPLY-EXTERNAL-REVISION-001",
  explicit_version: "1",
  version_authority: "EXPLICIT_CONTRACT_VERSION",
};
const APPROVED_SCENARIO = { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" };
const PROVIDER_KINDS = new Set(["STAKEHOLDER", "CONTROLLED_REFERENCE_FIXTURE"]);
const CORE_FAMILY = "CORE_REQUIREMENT_SPECIFICATION_METRIC_PATH";
const DYNAMIC_FAMILY = "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH";
const characteristicFields = ["completeness", "verifiability", "unambiguity"] as const;

export type CharacteristicField = (typeof characteristicFields)[number];

export interface SnapshotValue {
  state: "COMPUTED" | "UNKNOWN" | "NOT_APPLICABLE";
  value: ExactValueData | null;
  computedCount: number | null;
  unknownCount: number | null;
  notApplicableCount: number | null;
  totalCount: number | null;
  reasons: string[];
}

export interface RequirementSnapshot {
  state: SnapshotValue["state"];
  value: ExactValueData | null;
}

export interface RequirementBeforeAfter {
  lineage: JsonRecord;
  beforeSubject: JsonRecord;
  afterSubject: JsonRecord;
  beforeArtifact: JsonRecord;
  afterArtifact: JsonRecord;
  beforeText: string;
  afterText: string;
  changed: boolean;
  before: Record<CharacteristicField, RequirementSnapshot>;
  after: Record<CharacteristicField, RequirementSnapshot>;
}

export interface EvidenceCheckProjection {
  fieldName: string;
  expected: unknown;
  actual: unknown;
  matches: boolean;
}

export interface EvidenceReuseProjection {
  sourceEvidenceRef: unknown;
  targetProcessStateRef: JsonRecord;
  decision: "REUSE_ALLOWED" | "REBUILD_OR_RECOLLECT_REQUIRED";
  exactIdentityChecks: EvidenceCheckProjection[];
  reasonCodes: string[];
  provenance: JsonRecord;
}

export interface ProducedResultProjection {
  family: string;
  resultId: unknown;
  artifactRef: JsonRecord;
  result: JsonRecord;
}

export interface ExternalRevisionProjection {
  revisionId: string;
  revisionVersion: string;
  revisionRef: JsonRecord;
  providerKind: string;
  providerRef: JsonRecord;
  raw: JsonRecord;
}

export interface ReassessmentProjection {
  reassessmentId: string;
  reassessmentVersion: string;
  status: "AVAILABLE";
  reasonCodes: string[];
  ruleRef: JsonRecord;
  parentArtifactRef: JsonRecord;
  childArtifactRef: JsonRecord;
  actionApplicationRef: JsonRecord;
  predecessorProcessStateRef: JsonRecord;
  childProcessStateRef: JsonRecord;
  childAssessmentRef: JsonRecord;
  componentVersionSet: JsonRecord;
  externalRevision: ExternalRevisionProjection;
  comparisonRequestRefs: JsonRecord[];
  producedResults: ProducedResultProjection[];
  requirements: RequirementBeforeAfter[];
  specification: {
    before: Record<CharacteristicField, SnapshotValue>;
    after: Record<CharacteristicField, SnapshotValue>;
    qbBefore: SnapshotValue;
    qbAfter: SnapshotValue;
  };
  evidenceReuse: EvidenceReuseProjection[];
  provenance: JsonRecord;
  raw: JsonRecord;
}

export function record(value: unknown): JsonRecord | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? value as JsonRecord
    : null;
}

function withoutTransportState(value: JsonRecord): JsonRecord {
  const { status: _status, applicability: _applicability, ...canonical } = value;
  return canonical;
}

export function nonEmptyText(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 && value === value.trim() ? value : null;
}

function nonNegativeInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value >= 0 ? value : null;
}

function positiveInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value > 0 ? value : null;
}

export function canonicalStringArray(value: unknown): string[] | null {
  return Array.isArray(value) && value.every((item) => nonEmptyText(item) !== null)
    ? [...value] as string[]
    : null;
}

function exactFraction(value: unknown): ExactValueData | null {
  const candidate = record(value);
  if (!candidate) return null;
  const numerator = typeof candidate.numerator === "number" && Number.isSafeInteger(candidate.numerator)
    ? candidate.numerator
    : null;
  const denominator = typeof candidate.denominator === "number" && Number.isSafeInteger(candidate.denominator)
    ? candidate.denominator
    : null;
  return numerator !== null && denominator !== null && denominator !== 0
    ? { numerator: String(numerator), denominator: String(denominator) }
    : null;
}

function artifactRef(value: unknown): JsonRecord | null {
  const candidate = record(value);
  return candidate && nonEmptyText(candidate.artifact_id) && nonEmptyText(candidate.artifact_version)
    ? candidate
    : null;
}

function processRef(value: unknown): JsonRecord | null {
  const candidate = record(value);
  return candidate
    && nonEmptyText(candidate.process_state_id)
    && nonEmptyText(candidate.process_state_version)
    && candidate.stage === "REFERENCE_VERIFICATION"
    ? candidate
    : null;
}

function processStateRef(value: unknown): JsonRecord | null {
  const candidate = record(value);
  if (!candidate) return null;
  return processRef({
    process_state_id: candidate.process_state_id,
    process_state_version: candidate.process_state_version,
    stage: candidate.stage,
  });
}

function assessmentRef(value: unknown, expectedArtifact: JsonRecord): JsonRecord | null {
  const candidate = record(value);
  return candidate
    && nonEmptyText(candidate.assessment_id)
    && nonEmptyText(candidate.assessment_version)
    && structuralEqual(candidate.artifact_ref, expectedArtifact)
    ? candidate
    : null;
}

function contractRef(value: unknown): JsonRecord | null {
  const candidate = record(value);
  return candidate && nonEmptyText(candidate.contract_id) && nonEmptyText(candidate.version) ? candidate : null;
}

function sectionAvailable(response: CanonicalAnalyzeResponse, section: string): boolean {
  const matches = response.section_availability.filter((item) => record(item)?.section === section);
  if (matches.length !== 1) return false;
  const candidate = record(matches[0]);
  if (!candidate || (candidate.availability !== "AVAILABLE" && candidate.availability !== "UNAVAILABLE")) return false;
  return candidate.availability === "AVAILABLE"
    ? candidate.reason_code === null
    : nonEmptyText(candidate.reason_code) !== null && false;
}

function characteristic(value: unknown): RequirementSnapshot | null {
  const candidate = record(value);
  if (!candidate || (candidate.state !== "COMPUTED" && candidate.state !== "UNKNOWN" && candidate.state !== "NOT_APPLICABLE")) return null;
  const exact = exactFraction(candidate.value);
  if ((candidate.state === "COMPUTED" && exact === null) || (candidate.state !== "COMPUTED" && candidate.value !== null)) return null;
  return { state: candidate.state, value: exact };
}

function characteristics(value: unknown): Record<CharacteristicField, RequirementSnapshot> | null {
  const candidate = record(value);
  if (!candidate) return null;
  const completeness = characteristic(candidate.completeness);
  const verifiability = characteristic(candidate.verifiability);
  const unambiguity = characteristic(candidate.unambiguity);
  return completeness && verifiability && unambiguity
    ? { completeness, verifiability, unambiguity }
    : null;
}

function snapshotValue(value: unknown, includeCounts: boolean): SnapshotValue | null {
  const candidate = record(value);
  const base = characteristic(value);
  if (!candidate || !base) return null;
  const reasons = candidate.reasons === undefined ? [] : canonicalStringArray(candidate.reasons);
  if (reasons === null) return null;
  if (!includeCounts) return { ...base, computedCount: null, unknownCount: null, notApplicableCount: null, totalCount: null, reasons };
  const computedCount = nonNegativeInteger(candidate.computed_count);
  const unknownCount = nonNegativeInteger(candidate.unknown_count);
  const notApplicableCount = nonNegativeInteger(candidate.not_applicable_count);
  const totalCount = nonNegativeInteger(candidate.total_count);
  return computedCount !== null && unknownCount !== null && notApplicableCount !== null && totalCount !== null
    ? { ...base, computedCount, unknownCount, notApplicableCount, totalCount, reasons }
    : null;
}

function specificationSnapshot(value: unknown) {
  const result = record(value);
  const assessment = result && record(result.specification_assessment);
  const profile = assessment && record(assessment.quality_profile);
  if (!result || !assessment || !profile) return null;
  const completeness = snapshotValue(profile.completeness, true);
  const verifiability = snapshotValue(profile.verifiability, true);
  const unambiguity = snapshotValue(profile.unambiguity, true);
  const qb = snapshotValue(assessment.qb_consistency, false);
  return completeness && verifiability && unambiguity && qb
    ? { metrics: { completeness, verifiability, unambiguity }, qb }
    : null;
}

interface VersionedRequirementProjection {
  lineage: JsonRecord;
  subject: JsonRecord;
  text: string;
  predecessor: JsonRecord | null;
}

function subjectRef(value: unknown, expectedArtifact: JsonRecord): JsonRecord | null {
  const candidate = record(value);
  return candidate
    && structuralEqual(candidate.artifact_ref, expectedArtifact)
    && nonEmptyText(candidate.requirement_id)
    && positiveInteger(candidate.source_line) !== null
    ? candidate
    : null;
}

function lineage(value: unknown, stableArtifactId: string): JsonRecord | null {
  const candidate = record(value);
  return candidate
    && candidate.artifact_id === stableArtifactId
    && nonEmptyText(candidate.origin_artifact_version)
    && nonEmptyText(candidate.origin_requirement_id)
    && positiveInteger(candidate.origin_source_line) !== null
    ? candidate
    : null;
}

function versionRequirements(value: unknown, expectedArtifact: JsonRecord, initial: boolean): VersionedRequirementProjection[] | null {
  if (!Array.isArray(value) || value.length === 0) return null;
  const stableId = nonEmptyText(expectedArtifact.artifact_id);
  if (!stableId) return null;
  const projected = value.map((item) => {
    const candidate = record(item);
    const projectedLineage = candidate && lineage(candidate.lineage_id, stableId);
    const subject = candidate && subjectRef(candidate.subject_ref, expectedArtifact);
    const requirementText = candidate && typeof candidate.text === "string" ? candidate.text : null;
    const predecessor = candidate?.predecessor_subject_ref === null
      ? null
      : candidate && record(candidate.predecessor_subject_ref);
    if (!candidate || !projectedLineage || !subject || requirementText === null
      || (initial ? predecessor !== null : predecessor === null)) return null;
    if (initial && (projectedLineage.origin_artifact_version !== expectedArtifact.artifact_version
      || projectedLineage.origin_requirement_id !== subject.requirement_id
      || projectedLineage.origin_source_line !== subject.source_line)) return null;
    return { lineage: projectedLineage, subject, text: requirementText, predecessor };
  });
  if (projected.some((item) => item === null)) return null;
  const typed = projected as VersionedRequirementProjection[];
  if (typed.some((item, index) => {
    if (index === 0) return false;
    const previous = typed[index - 1].subject;
    const currentLine = Number(item.subject.source_line);
    const previousLine = Number(previous.source_line);
    return currentLine < previousLine
      || (currentLine === previousLine && String(item.subject.requirement_id) <= String(previous.requirement_id));
  })) return null;
  if (typed.some((item, index) => typed.some((other, otherIndex) => otherIndex !== index
    && structuralEqual(item.lineage, other.lineage)))) return null;
  return typed;
}

function requirementRecords(value: unknown, versioned: VersionedRequirementProjection[]): Array<Record<CharacteristicField, RequirementSnapshot>> | null {
  if (!Array.isArray(value) || value.length !== versioned.length) return null;
  const projected = value.map((item, index) => {
    const candidate = record(item);
    const extraction = candidate && record(candidate.extraction_result);
    const requirement = extraction && record(extraction.requirement);
    const expected = versioned[index];
    if (!candidate || !requirement
      || requirement.id !== expected.subject.requirement_id
      || requirement.source_line !== expected.subject.source_line
      || requirement.text !== expected.text) return null;
    return characteristics(candidate.quality_profile);
  });
  return projected.some((item) => item === null)
    ? null
    : projected as Array<Record<CharacteristicField, RequirementSnapshot>>;
}

function changedPopulation(value: unknown, before: VersionedRequirementProjection[], after: VersionedRequirementProjection[]): JsonRecord[] | null {
  if (!Array.isArray(value)) return null;
  const projected: JsonRecord[] = [];
  for (const item of value) {
    const candidate = record(item);
    if (!candidate || candidate.change_kind !== "REPLACE_TEXT") return null;
    const beforeIndex = before.findIndex((entry) => structuralEqual(entry.lineage, candidate.lineage_id));
    const afterIndex = after.findIndex((entry) => structuralEqual(entry.lineage, candidate.lineage_id));
    if (beforeIndex < 0 || afterIndex < 0
      || !structuralEqual(candidate.before_subject_ref, before[beforeIndex].subject)
      || !structuralEqual(candidate.after_subject_ref, after[afterIndex].subject)) return null;
    projected.push(candidate);
  }
  return projected;
}

function evidenceReuse(value: unknown, predecessorProcess: JsonRecord, childProcess: JsonRecord): EvidenceReuseProjection[] | null {
  if (!Array.isArray(value)) return null;
  const projected = value.map((item) => {
    const candidate = record(item);
    const provenance = candidate && record(candidate.provenance);
    const target = candidate && processRef(candidate.target_process_state_ref);
    const reasons = candidate && canonicalStringArray(candidate.reason_codes);
    if (!candidate || !provenance || !target || !reasons || reasons.length === 0
      || !structuralEqual(target, childProcess)
      || !structuralEqual(provenance.source_process_state_ref, predecessorProcess)
      || !structuralEqual(provenance.target_process_state_ref, childProcess)
      || !structuralEqual(provenance.reassessment_rule_ref, REASSESSMENT_RULE)
      || !contractRef(provenance.source_contract_ref)
      || (candidate.decision !== "REUSE_ALLOWED" && candidate.decision !== "REBUILD_OR_RECOLLECT_REQUIRED")
      || !Array.isArray(candidate.exact_identity_checks)) return null;
    const checks = candidate.exact_identity_checks.map((check) => {
      const checkRecord = record(check);
      if (!checkRecord || !nonEmptyText(checkRecord.field_name) || typeof checkRecord.matches !== "boolean"
        || checkRecord.matches !== structuralEqual(checkRecord.expected, checkRecord.actual)) return null;
      return { fieldName: checkRecord.field_name as string, expected: checkRecord.expected, actual: checkRecord.actual, matches: checkRecord.matches };
    });
    if (checks.some((check) => check === null)) return null;
    if (candidate.decision === "REUSE_ALLOWED"
      && (checks.length === 0 || checks.some((check) => !check?.matches)
        || reasons.length !== 1 || reasons[0] !== "EXACT_IDENTITY_AND_CONTEXT_MATCH")) return null;
    if (candidate.decision === "REBUILD_OR_RECOLLECT_REQUIRED"
      && reasons.some((reason) => reason !== "IDENTITY_OR_CONTEXT_CHANGED" && reason !== "VALIDITY_NOT_ESTABLISHED")) return null;
    return {
      sourceEvidenceRef: candidate.source_evidence_ref,
      targetProcessStateRef: target,
      decision: candidate.decision,
      exactIdentityChecks: checks as EvidenceCheckProjection[],
      reasonCodes: reasons,
      provenance,
    };
  });
  return projected.some((item) => item === null) ? null : projected as EvidenceReuseProjection[];
}

function applicationRef(value: unknown): JsonRecord | null {
  const candidate = record(value);
  return candidate && record(candidate.application_id) && nonEmptyText(candidate.application_version)
    ? { application_id: candidate.application_id, application_version: candidate.application_version }
    : null;
}

function componentVersionSet(value: unknown): JsonRecord | null {
  const candidate = record(value);
  if (!candidate || !Array.isArray(candidate.components) || candidate.components.length === 0) return null;
  const roles = new Set<string>();
  for (const item of candidate.components) {
    const component = record(item);
    const role = component && nonEmptyText(component.component_role);
    if (!component || !role || !nonEmptyText(component.component_id) || !nonEmptyText(component.component_version)
      || roles.has(role)) return null;
    roles.add(role);
  }
  return candidate;
}

function externalRevision(
  value: unknown,
  revisedVersion: JsonRecord,
  parentArtifact: JsonRecord,
  childArtifact: JsonRecord,
  canonicalApplicationRef: JsonRecord,
  canonicalActionRef: JsonRecord,
): ExternalRevisionProjection | null {
  const candidate = record(value);
  const revisionId = candidate && nonEmptyText(candidate.revision_id);
  const revisionVersion = candidate && nonEmptyText(candidate.revision_version);
  const providerKind = candidate && nonEmptyText(candidate.provider_kind);
  const providerRef = candidate && record(candidate.provider_ref);
  const actionRef = candidate && record(candidate.action_ref);
  const revisionProvenance = candidate && record(candidate.provenance);
  const specificationProvenance = record(revisedVersion.provenance);
  if (!candidate || !revisionId || !revisionVersion || !providerKind || !PROVIDER_KINDS.has(providerKind)
    || !providerRef || !actionRef
    || !nonEmptyText(providerRef.provider_id) || !nonEmptyText(providerRef.provider_version)
    || !revisionProvenance || !specificationProvenance) return null;
  const revisionRef = { revision_id: revisionId, revision_version: revisionVersion };
  if (!structuralEqual(candidate.parent_artifact_ref, parentArtifact)
    || !structuralEqual(candidate.requested_child_artifact_ref, childArtifact)
    || !structuralEqual(revisionProvenance.revision_ref, revisionRef)
    || !structuralEqual(actionRef, canonicalActionRef)
    || !structuralEqual(revisionProvenance.action_ref, actionRef)
    || !structuralEqual(revisionProvenance.parent_artifact_ref, parentArtifact)
    || !structuralEqual(revisionProvenance.requested_child_artifact_ref, childArtifact)
    || !structuralEqual(revisionProvenance.provider_ref, providerRef)
    || !structuralEqual(revisionProvenance.process_reassessment_contract_ref, PROCESS_CONTRACT)
    || !structuralEqual(revisionProvenance.application_rule_ref, APPLICATION_RULE)
    || !structuralEqual(specificationProvenance.artifact_ref, childArtifact)
    || !structuralEqual(specificationProvenance.parent_artifact_ref, parentArtifact)
    || !structuralEqual(specificationProvenance.application_ref, canonicalApplicationRef)
    || !structuralEqual(specificationProvenance.revision_ref, revisionRef)
    || !structuralEqual(specificationProvenance.process_reassessment_contract_ref, PROCESS_CONTRACT)
    || !structuralEqual(specificationProvenance.application_rule_ref_or_none, APPLICATION_RULE)) return null;
  return { revisionId, revisionVersion, revisionRef, providerKind, providerRef, raw: candidate };
}

export function selectReassessmentProjection(response: CanonicalAnalyzeResponse): ReassessmentProjection | null {
  if (response.contract_version !== "research-api-v1"
    || (response.analysis_case !== "CONTROLLED_DEMO" && response.analysis_case !== "REASSESSMENT")
    || !sectionAvailable(response, "reassessment")) return null;
  const scenario = record(response.controlled_scenario);
  const priorContext = record(response.reassessment_context);
  const priorScenario = priorContext && record(priorContext.scenario);
  if (!scenario || !priorContext || !priorScenario
    || !structuralEqual(scenario, APPROVED_SCENARIO)
    || !structuralEqual(priorScenario, scenario)
    || !nonEmptyText(priorContext.context_digest)) return null;
  const fullModel = record(response.full_model);
  const reassessment = fullModel && record(fullModel.reassessment);
  const context = reassessment && record(reassessment.context);
  const provenance = reassessment && record(reassessment.provenance);
  const priorPairs: Array<[string, string]> = [
    ["initial_specification", "initial_specification"],
    ["initial_specification_assessment", "initial_specification_assessment"],
    ["predecessor_process_state", "process_v1"],
    ["corrective_action_resolution", "corrective_action_resolution"],
    ["action_application", "action_application"],
    ["external_revision", "external_revision"],
    ["revised_specification", "revised_specification"],
    ["successor_process_state", "process_v2"],
    ["process_transition", "process_transition"],
    ["comparisons", "comparisons"],
  ];
  if (!fullModel || priorPairs.some(([priorField, modelField]) => priorContext[priorField] === undefined
    || fullModel[modelField] === undefined || !structuralEqual(priorContext[priorField], fullModel[modelField]))) return null;
  if (!reassessment || !context || !provenance
    || reassessment.status !== "AVAILABLE"
    || !nonEmptyText(reassessment.reassessment_id)
    || !nonEmptyText(reassessment.reassessment_version)
    || !structuralEqual(reassessment.rule_ref, REASSESSMENT_RULE)
    || !structuralEqual(context.full_model_contract_ref, FULL_MODEL_CONTRACT)
    || !structuralEqual(provenance.full_model_contract_ref, FULL_MODEL_CONTRACT)
    || !structuralEqual(provenance.process_reassessment_contract_ref, PROCESS_CONTRACT)
    || !structuralEqual(provenance.rule_ref, REASSESSMENT_RULE)
    || context.stage !== "REFERENCE_VERIFICATION") return null;

  const parentArtifact = artifactRef(context.parent_artifact_ref);
  const childArtifact = artifactRef(context.child_artifact_ref);
  const predecessor = processRef(context.predecessor_process_state_ref);
  const childProcess = processRef(reassessment.child_process_state_ref);
  const processV1 = processStateRef(fullModel.process_v1);
  const processV2 = processStateRef(fullModel.process_v2);
  const childAssessment = childArtifact && assessmentRef(context.child_assessment_ref, childArtifact);
  const initialVersion = record(fullModel.initial_specification);
  const revisedVersion = record(fullModel.revised_specification);
  const canonicalApplicationRef = applicationRef(fullModel.action_application);
  const correctiveResolution = record(fullModel.corrective_action_resolution);
  const canonicalActionRef = correctiveResolution && record(correctiveResolution.action_ref);
  if (!parentArtifact || !childArtifact || !predecessor || !childProcess || !processV1 || !processV2 || !childAssessment
    || !initialVersion || !revisedVersion || !canonicalApplicationRef || !canonicalActionRef
    || parentArtifact.artifact_id !== childArtifact.artifact_id
    || parentArtifact.artifact_version === childArtifact.artifact_version
    || predecessor.process_state_id !== childProcess.process_state_id
    || predecessor.process_state_version === childProcess.process_state_version
    || !structuralEqual(predecessor, processV1)
    || !structuralEqual(childProcess, processV2)
    || !structuralEqual(context.action_application_ref, canonicalApplicationRef)
    || !structuralEqual(context.parent_artifact_ref, initialVersion.artifact_ref)
    || !structuralEqual(context.child_artifact_ref, revisedVersion.artifact_ref)
    || !structuralEqual(revisedVersion.parent_artifact_ref, parentArtifact)
    || !structuralEqual(revisedVersion.created_by_application_ref, canonicalApplicationRef)) return null;

  const projectedRevision = externalRevision(
    fullModel.external_revision,
    revisedVersion,
    parentArtifact,
    childArtifact,
    canonicalApplicationRef,
    canonicalActionRef,
  );
  const priorIdentity = record(priorContext.reassessment_identity);
  if (!projectedRevision || !priorIdentity
    || priorIdentity.reassessment_id !== reassessment.reassessment_id
    || priorIdentity.reassessment_version !== reassessment.reassessment_version
    || !structuralEqual(priorIdentity.child_process_state_ref, reassessment.child_process_state_ref)
    || !structuralEqual(priorIdentity.component_version_set, context.component_version_set)
    || !structuralEqual(priorContext.evidence_reuse_decisions, context.evidence_reuse_decisions)) return null;

  const identity = { reassessment_id: reassessment.reassessment_id, reassessment_version: reassessment.reassessment_version };
  const equalityPairs: Array<[unknown, unknown]> = [
    [provenance.reassessment_ref, identity],
    [provenance.action_application_ref, context.action_application_ref],
    [provenance.predecessor_process_state_ref, context.predecessor_process_state_ref],
    [provenance.child_process_state_ref, reassessment.child_process_state_ref],
    [provenance.parent_artifact_ref, context.parent_artifact_ref],
    [provenance.child_artifact_ref, context.child_artifact_ref],
    [provenance.child_assessment_ref, context.child_assessment_ref],
    [provenance.component_version_set, context.component_version_set],
    [provenance.evidence_reuse_decisions, context.evidence_reuse_decisions],
    [provenance.produced_result_refs, reassessment.produced_result_refs],
  ];
  if (equalityPairs.some(([left, right]) => !structuralEqual(left, right))) return null;
  const componentSet = componentVersionSet(context.component_version_set);
  if (!componentSet) return null;

  const decisions = evidenceReuse(context.evidence_reuse_decisions, predecessor, childProcess);
  const reasonCodes = canonicalStringArray(reassessment.reason_codes);
  const requestRefs = Array.isArray(reassessment.comparison_request_refs)
    && reassessment.comparison_request_refs.every((item) => {
      const candidate = record(item);
      return candidate && nonEmptyText(candidate.comparison_id) && nonEmptyText(candidate.comparison_version);
    }) ? reassessment.comparison_request_refs as JsonRecord[] : null;
  if (!decisions || !reasonCodes || reasonCodes.length !== 1 || reasonCodes[0] !== "FULL_MODEL_PATH_REBUILT" || requestRefs === null) return null;

  const refs = Array.isArray(reassessment.produced_result_refs) ? reassessment.produced_result_refs : null;
  const results = Array.isArray(reassessment.produced_results) ? reassessment.produced_results : null;
  if (!refs || !results || refs.length !== results.length) return null;
  const pairs: ProducedResultProjection[] = [];
  for (let index = 0; index < refs.length; index += 1) {
    const ref = record(refs[index]);
    const result = record(results[index]);
    const family = ref && nonEmptyText(ref.result_family);
    const refArtifact = ref && artifactRef(ref.artifact_ref);
    if (!ref || !result || !family || !refArtifact || ref.result_id == null || !structuralEqual(refArtifact, childArtifact)) return null;
    pairs.push({ family, resultId: ref.result_id, artifactRef: refArtifact, result });
  }
  const corePairs = pairs.filter((pair) => pair.family === CORE_FAMILY);
  const dynamicPairs = pairs.filter((pair) => pair.family === DYNAMIC_FAMILY);
  if (corePairs.length !== 1 || dynamicPairs.length !== 1) return null;
  const core = corePairs[0];
  const dynamic = dynamicPairs[0];
  const coreVersion = record(core.result.specification_version);
  const metricProfile = record(core.result.metric_profile);
  const dynamicArtifact = artifactRef(dynamic.result.artifact_ref);
  const riskAssessment = record(dynamic.result.risk_assessment);
  const dynamicArtifactRecords = [
    record(record(dynamic.result.criterion_binding)?.binding_id)?.artifact_ref,
    record(dynamic.result.conformance)?.dynamic_assessment_ref && record(record(dynamic.result.conformance)?.dynamic_assessment_ref)?.artifact_ref,
    record(dynamic.result.feature_profile)?.artifact_ref,
    record(dynamic.result.product_quality_assessment)?.artifact_ref,
    record(dynamic.result.defect_population)?.artifact_ref,
    record(dynamic.result.target_problem_resolution)?.artifact_ref,
    record(dynamic.result.defect_quality_relation)?.artifact_ref,
    riskAssessment?.artifact_ref,
  ];
  const problemResolutions = Array.isArray(dynamic.result.problem_resolutions) ? dynamic.result.problem_resolutions : null;
  if (!coreVersion || !metricProfile || !dynamicArtifact || !riskAssessment || !problemResolutions
    || !structuralEqual(core.resultId, childAssessment)
    || !structuralEqual(coreVersion, withoutTransportState(revisedVersion))
    || !structuralEqual(coreVersion.artifact_ref, childArtifact)
    || !structuralEqual(metricProfile.artifact_ref, childArtifact)
    || !structuralEqual(metricProfile.assessment_ref, childAssessment)
    || !structuralEqual(dynamicArtifact, childArtifact)
    || !structuralEqual(dynamic.resultId, riskAssessment.risk_assessment_id)
    || dynamicArtifactRecords.some((value) => !structuralEqual(value, childArtifact))
    || problemResolutions.some((value) => !structuralEqual(record(value)?.artifact_ref, childArtifact))) return null;

  const beforeRequirements = versionRequirements(initialVersion.requirements, parentArtifact, true);
  const afterRequirements = versionRequirements(coreVersion.requirements, childArtifact, false);
  if (!beforeRequirements || !afterRequirements || beforeRequirements.length !== afterRequirements.length) return null;
  const alignedAfter = beforeRequirements.map((before) => afterRequirements.filter((after) => structuralEqual(after.lineage, before.lineage)));
  if (alignedAfter.some((matches) => matches.length !== 1)) return null;
  const orderedAfter = alignedAfter.map((matches) => matches[0]);
  if (orderedAfter.some((after, index) => !structuralEqual(after.predecessor, beforeRequirements[index].subject))) return null;
  const initialAssessment = record(fullModel.initial_specification_assessment);
  const coreAssessment = record(core.result.specification_assessment);
  const beforeCharacteristicRecords = initialAssessment && requirementRecords(initialAssessment.records, beforeRequirements);
  const afterCharacteristicRecords = requirementRecords(core.result.requirement_records, orderedAfter);
  const beforeSpecification = specificationSnapshot(initialAssessment);
  const afterSpecification = specificationSnapshot(coreAssessment);
  const changed = changedPopulation(revisedVersion.changed_subjects, beforeRequirements, orderedAfter);
  if (!beforeCharacteristicRecords || !afterCharacteristicRecords || !beforeSpecification || !afterSpecification || !changed) return null;

  const requirementProjection = beforeRequirements.map((before, index) => ({
    lineage: before.lineage,
    beforeSubject: before.subject,
    afterSubject: orderedAfter[index].subject,
    beforeArtifact: parentArtifact,
    afterArtifact: childArtifact,
    beforeText: before.text,
    afterText: orderedAfter[index].text,
    changed: changed.some((item) => structuralEqual(item.lineage_id, before.lineage)),
    before: beforeCharacteristicRecords[index],
    after: afterCharacteristicRecords[index],
  }));

  return {
    reassessmentId: reassessment.reassessment_id as string,
    reassessmentVersion: reassessment.reassessment_version as string,
    status: "AVAILABLE",
    reasonCodes,
    ruleRef: reassessment.rule_ref as JsonRecord,
    parentArtifactRef: parentArtifact,
    childArtifactRef: childArtifact,
    actionApplicationRef: canonicalApplicationRef,
    predecessorProcessStateRef: predecessor,
    childProcessStateRef: childProcess,
    childAssessmentRef: childAssessment,
    componentVersionSet: componentSet,
    externalRevision: projectedRevision,
    comparisonRequestRefs: requestRefs,
    producedResults: pairs,
    requirements: requirementProjection,
    specification: {
      before: beforeSpecification.metrics,
      after: afterSpecification.metrics,
      qbBefore: beforeSpecification.qb,
      qbAfter: afterSpecification.qb,
    },
    evidenceReuse: decisions,
    provenance,
    raw: reassessment,
  };
}

export function hasAvailableLifecycleSection(response: CanonicalAnalyzeResponse, section: "reassessment" | "comparison") {
  return sectionAvailable(response, section);
}

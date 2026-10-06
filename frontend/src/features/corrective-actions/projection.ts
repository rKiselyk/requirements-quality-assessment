import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { RequirementInput } from "../specification-input/model";
import { selectSectionAvailability } from "../results/projection";
import { structuralEqual } from "../results/structuralIdentity";

export type JsonRecord = Record<string, unknown>;

const canonicalActionRule = { rule_id: "ACTION-RECONCILE-QB-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const canonicalVerificationRule = { rule_id: "REEVAL-FULL-MODEL-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const canonicalApplicationRule = { rule_id: "APPLY-EXTERNAL-REVISION-001", explicit_version: "1", version_authority: "EXPLICIT_CONTRACT_VERSION" };
const canonicalFullModelContract = { contract_id: "FULL-MODEL-V0.1-CONTRACT", version: "1" };
const canonicalDefectRiskContract = { contract_id: "FULL-MODEL-V0.1-DEFECT-QUALITY-RISK", version: "1" };
const canonicalProcessContract = { contract_id: "FULL-MODEL-V0.1-PROCESS-REASSESSMENT", version: "1" };
const canonicalRationale = "The two target requirements contain an exact QB-v0.1 confirmed conflict on the same complete quantitative comparison key. Stakeholder reconciliation is requested because the system cannot determine which bound expresses intent.";
const canonicalOutcome = "A later rerun may no longer identify that exact confirmed conflict.";
const resolutionReasons = new Set([
  "ELIGIBLE_RISK_IDENTIFIED",
  "NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE",
  "SOURCE_UNAVAILABLE",
  "SOURCE_ASSESSMENT_UNKNOWN",
  "SOURCE_IDENTITY_OR_COHERENCE_UNRESOLVED",
  "SOURCE_UNSUPPORTED",
  "REQUESTED_ACTION_KIND_UNSUPPORTED",
]);
const providerKinds = new Set(["STAKEHOLDER", "CONTROLLED_REFERENCE_FIXTURE"]);
const fullModelStatuses = new Set(["AVAILABLE", "NOT_APPLICABLE", "UNAVAILABLE", "UNKNOWN", "UNRESOLVED", "UNSUPPORTED"]);

export interface ScientificState {
  status: string;
  applicability: string;
}

export interface TargetRequirementProjection {
  lineage: JsonRecord;
  subject: JsonRecord;
  requirementId: string;
  sourceLine: number;
  navigationRequirementId: string | null;
}

export interface ActionProjection {
  raw: JsonRecord;
  actionRef: JsonRecord;
  actionRecordVersion: string;
  actionKind: "RECONCILE_QUANTITATIVE_BOUNDS";
  status: "PROPOSED";
  ruleRef: JsonRecord;
  targetArtifactRef: JsonRecord;
  targets: TargetRequirementProjection[];
  comparisonKey: JsonRecord;
  rationale: string;
  proposedChangeKind: "REPLACE_REQUIREMENT_TEXT";
  expectedBoundedOutcome: string;
  verificationRuleRef: JsonRecord;
  creatorSource: JsonRecord;
  nonOptimalityClaim: "CANDIDATE_NOT_OPTIMALITY_CLAIM";
  orderedEvidenceRefs: unknown[];
}

export interface ResolutionProjection extends ScientificState {
  raw: JsonRecord;
  resolutionId: JsonRecord;
  actionRef: JsonRecord | null;
  reasonCode: string;
  sourceRiskRef: JsonRecord | null;
  sourceProblemRef: JsonRecord | null;
  sourceRelationRef: JsonRecord | null;
  ruleRef: JsonRecord;
  action: ActionProjection | null;
}

interface VersionedRequirementProjection {
  raw: JsonRecord;
  lineage: JsonRecord;
  subject: JsonRecord;
  text: string;
  predecessorSubject: JsonRecord | null;
}

interface SpecificationProjection {
  raw: JsonRecord;
  artifactRef: JsonRecord;
  parentArtifactRef: JsonRecord | null;
  applicationRef: JsonRecord | null;
  requirements: VersionedRequirementProjection[];
  changedSubjects: JsonRecord[];
}

export interface RevisionReplacementProjection {
  lineage: JsonRecord;
  expectedParentSubject: JsonRecord;
  replacementText: string;
}

export interface ExternalRevisionProjection {
  raw: JsonRecord;
  revisionRef: JsonRecord;
  providerKind: string;
  providerRef: JsonRecord;
  actionRef: JsonRecord;
  parentArtifactRef: JsonRecord;
  childArtifactRef: JsonRecord;
  replacements: RevisionReplacementProjection[];
  providerRationale: string | null;
}

export interface ApplicationProjection {
  status: "AVAILABLE";
  raw: JsonRecord;
  applicationRef: JsonRecord;
  actionBeforeRef: JsonRecord;
  actionAfterRef: JsonRecord;
  revisionRef: JsonRecord;
  parentArtifactRef: JsonRecord;
  childArtifactRef: JsonRecord;
  changedSubjects: JsonRecord[];
  ruleRef: JsonRecord;
  reasonCode: "EXTERNAL_REVISION_MATERIALIZED";
  appliedActionVersion: string;
}

export interface ChangedRequirementProjection {
  lineage: JsonRecord;
  beforeSubject: JsonRecord;
  afterSubject: JsonRecord;
  beforeText: string;
  afterText: string;
  changeKind: "REPLACE_TEXT";
}

export interface ReassessmentEntryProjection {
  priorContext: JsonRecord;
  requirements: RequirementInput[];
}

export type CorrectiveActionsPageProjection =
  | { kind: "UNAVAILABLE"; reasonCode: string }
  | { kind: "MALFORMED" }
  | {
    kind: "AVAILABLE";
    resolution: ResolutionProjection;
    externalRevision: ExternalRevisionProjection | null;
    application: ApplicationProjection | null;
    changedRequirements: ChangedRequirementProjection[];
    reassessment: ReassessmentEntryProjection | null;
  };

function record(value: unknown): JsonRecord | null {
  return typeof value === "object" && value !== null && !Array.isArray(value) ? value as JsonRecord : null;
}

function array(value: unknown): unknown[] | null {
  return Array.isArray(value) ? value : null;
}

function text(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function positiveInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value > 0 ? value : null;
}

function hasOwn(value: JsonRecord, key: string): boolean {
  return Object.prototype.hasOwnProperty.call(value, key);
}

function state(value: JsonRecord): ScientificState | null {
  const status = text(value.status);
  const applicability = text(value.applicability);
  if (!status || !applicability || !fullModelStatuses.has(status)) return null;
  if (status === "AVAILABLE" && applicability !== "APPLICABLE") return null;
  if (status === "NOT_APPLICABLE" && applicability !== "NOT_APPLICABLE") return null;
  if (!["AVAILABLE", "NOT_APPLICABLE"].includes(status) && !["APPLICABLE", "UNKNOWN"].includes(applicability)) return null;
  return { status, applicability };
}

function identifiers(value: JsonRecord, ...keys: string[]): boolean {
  return keys.every((key) => text(value[key]) !== null);
}

function withoutScientificWrapper(value: JsonRecord): JsonRecord {
  const { status: _status, applicability: _applicability, ...rest } = value;
  return rest;
}

function exactRef(parent: JsonRecord, idKey: string, versionKey: string): JsonRecord | null {
  const identity = parent[idKey];
  const version = text(parent[versionKey]);
  return record(identity) && version ? { [idKey]: identity, [versionKey]: version } : null;
}

function projectVersionedRequirement(value: unknown): VersionedRequirementProjection | null {
  const raw = record(value);
  const lineage = raw && record(raw.lineage_id);
  const subject = raw && record(raw.subject_ref);
  const artifact = subject && record(subject.artifact_ref);
  const sourceLine = subject && positiveInteger(subject.source_line);
  const requirementId = subject && text(subject.requirement_id);
  const requirementText = raw && text(raw.text);
  const predecessor = raw?.predecessor_subject_ref === null ? null : record(raw?.predecessor_subject_ref);
  if (!raw || !lineage || !subject || !artifact || !sourceLine || !requirementId || !requirementText
    || (!hasOwn(raw, "predecessor_subject_ref") || (raw.predecessor_subject_ref !== null && !predecessor))
    || lineage.artifact_id !== artifact.artifact_id
    || lineage.origin_requirement_id !== requirementId
    || lineage.origin_source_line !== sourceLine
    || !identifiers(lineage, "artifact_id", "origin_artifact_version", "origin_requirement_id")) return null;
  return { raw, lineage, subject, text: requirementText, predecessorSubject: predecessor };
}

function projectSpecification(value: unknown, initial: boolean): SpecificationProjection | null {
  const raw = record(value);
  const artifactRef = raw && record(raw.artifact_ref);
  const provenance = raw && record(raw.provenance);
  const requirementsRaw = raw && array(raw.requirements);
  const changedRaw = raw && array(raw.changed_subjects);
  if (!raw || !artifactRef || !identifiers(artifactRef, "artifact_id", "artifact_version") || !provenance || !requirementsRaw || !changedRaw
    || !structuralEqual(provenance.artifact_ref, artifactRef)
    || !structuralEqual(provenance.process_reassessment_contract_ref, canonicalProcessContract)) return null;
  const requirements = requirementsRaw.map(projectVersionedRequirement);
  const changedSubjects = changedRaw.map(record);
  if (requirements.some((item) => item === null) || changedSubjects.some((item) => item === null)) return null;
  const projectedRequirements = requirements as VersionedRequirementProjection[];
  const projectedChanged = changedSubjects as JsonRecord[];
  if (projectedRequirements.some((item, index) => projectedRequirements.slice(0, index).some((prior) => structuralEqual(prior.lineage, item.lineage)))) return null;

  if (initial) {
    if (raw.parent_artifact_ref !== null || raw.created_by_application_ref !== null || projectedChanged.length !== 0
      || provenance.parent_artifact_ref !== null || provenance.application_ref !== null || provenance.revision_ref !== null
      || provenance.application_rule_ref_or_none !== null
      || projectedRequirements.some((item) => item.predecessorSubject !== null)) return null;
    return { raw, artifactRef, parentArtifactRef: null, applicationRef: null, requirements: projectedRequirements, changedSubjects: [] };
  }
  const parent = record(raw.parent_artifact_ref);
  const application = record(raw.created_by_application_ref);
  if (!parent || !application || projectedChanged.length === 0
    || !structuralEqual(provenance.parent_artifact_ref, parent)
    || !structuralEqual(provenance.application_ref, application)
    || !record(provenance.revision_ref)
    || !structuralEqual(provenance.application_rule_ref_or_none, canonicalApplicationRule)) return null;
  return { raw, artifactRef, parentArtifactRef: parent, applicationRef: application, requirements: projectedRequirements, changedSubjects: projectedChanged };
}

function targetProjection(value: unknown): Omit<TargetRequirementProjection, "navigationRequirementId"> | null {
  const raw = record(value);
  const lineage = raw && record(raw.lineage_id);
  const subject = raw && record(raw.subject_ref);
  const artifact = subject && record(subject.artifact_ref);
  const requirementId = subject && text(subject.requirement_id);
  const sourceLine = subject && positiveInteger(subject.source_line);
  if (!raw || !lineage || !subject || !artifact || !requirementId || !sourceLine
    || lineage.artifact_id !== artifact.artifact_id
    || lineage.origin_artifact_version !== artifact.artifact_version
    || lineage.origin_requirement_id !== requirementId
    || lineage.origin_source_line !== sourceLine) return null;
  return { lineage, subject, requirementId, sourceLine };
}

function projectAction(value: unknown, actionRef: JsonRecord, resolution: JsonRecord): ActionProjection | null {
  const raw = record(value);
  const ruleRef = raw && record(raw.rule_ref);
  const verification = raw && record(raw.verification_rule_ref);
  const targetArtifact = raw && record(raw.target_artifact_ref);
  const targetsRaw = raw && array(raw.target_requirements);
  const comparisonKey = raw && record(raw.comparison_key);
  const creator = raw && record(raw.creator_source);
  const provenance = raw && record(raw.provenance);
  const rationale = raw && text(raw.rationale);
  const outcome = raw && text(raw.expected_bounded_outcome);
  const version = raw && text(raw.action_record_version);
  const orderedEvidence = provenance && array(provenance.ordered_evidence_refs);
  const ownRef = raw && record(raw.action_id) && version ? { action_id: raw.action_id, action_record_version: version } : null;
  if (!raw || !ruleRef || !verification || !targetArtifact || !targetsRaw || targetsRaw.length !== 2 || !comparisonKey || !creator || !provenance
    || !rationale || !outcome || !version || !orderedEvidence || !ownRef
    || !structuralEqual(ownRef, actionRef)
    || raw.predecessor_action_ref !== null || raw.external_revision_ref !== null || raw.application_ref !== null
    || raw.action_kind !== "RECONCILE_QUANTITATIVE_BOUNDS" || raw.status !== "PROPOSED"
    || raw.proposed_change_kind !== "REPLACE_REQUIREMENT_TEXT"
    || raw.non_optimality_claim !== "CANDIDATE_NOT_OPTIMALITY_CLAIM"
    || rationale !== canonicalRationale || outcome !== canonicalOutcome
    || !structuralEqual(ruleRef, canonicalActionRule) || !structuralEqual(verification, canonicalVerificationRule)
    || !structuralEqual(resolution.source_risk_ref, raw.originating_risk_ref)
    || !structuralEqual(resolution.source_problem_ref, raw.originating_problem_ref)
    || !structuralEqual(resolution.source_relation_ref, raw.originating_relation_ref)
    || !structuralEqual(provenance.originating_risk_ref, raw.originating_risk_ref)
    || !structuralEqual(provenance.originating_problem_ref, raw.originating_problem_ref)
    || !structuralEqual(provenance.originating_relation_ref, raw.originating_relation_ref)
    || !structuralEqual(provenance.artifact_ref, targetArtifact)
    || !structuralEqual(provenance.target_requirements, targetsRaw)
    || !structuralEqual(provenance.comparison_key, comparisonKey)
    || !structuralEqual(provenance.action_rule_ref, canonicalActionRule)
    || !structuralEqual(provenance.verification_rule_ref, canonicalVerificationRule)
    || !structuralEqual(provenance.full_model_contract_ref, canonicalFullModelContract)
    || !structuralEqual(provenance.defect_risk_contract_ref, canonicalDefectRiskContract)
    || !structuralEqual(provenance.process_reassessment_contract_ref, canonicalProcessContract)
    || !identifiers(creator, "source_id", "source_version")) return null;
  const targets = targetsRaw.map(targetProjection);
  if (targets.some((item) => item === null) || structuralEqual(targets[0]?.lineage, targets[1]?.lineage)) return null;
  return {
    raw, actionRef, actionRecordVersion: version, actionKind: "RECONCILE_QUANTITATIVE_BOUNDS", status: "PROPOSED",
    ruleRef, targetArtifactRef: targetArtifact, targets: (targets as Omit<TargetRequirementProjection, "navigationRequirementId">[]).map((item) => ({ ...item, navigationRequirementId: null })),
    comparisonKey, rationale, proposedChangeKind: "REPLACE_REQUIREMENT_TEXT", expectedBoundedOutcome: outcome,
    verificationRuleRef: verification, creatorSource: creator, nonOptimalityClaim: "CANDIDATE_NOT_OPTIMALITY_CLAIM", orderedEvidenceRefs: orderedEvidence,
  };
}

function sourceGraphResolves(fullModel: JsonRecord, resolution: JsonRecord): boolean {
  const risks = array(fullModel.risk_assessments);
  const problems = array(fullModel.problem_resolutions);
  const relations = array(fullModel.defect_quality_relations);
  return Boolean(risks && problems && relations
    && risks.some((item) => structuralEqual({ risk_assessment_id: record(item)?.risk_assessment_id }, resolution.source_risk_ref))
    && problems.some((item) => structuralEqual({ problem_id: record(record(item)?.problem)?.problem_id }, resolution.source_problem_ref))
    && relations.some((item) => structuralEqual({ relation_id: record(item)?.relation_id }, resolution.source_relation_ref)));
}

function projectResolution(value: unknown, fullModel: JsonRecord): ResolutionProjection | null {
  const raw = record(value);
  const currentState = raw && state(raw);
  const resolutionId = raw && record(raw.resolution_id);
  const ruleRef = raw && record(raw.rule_ref);
  const reasons = raw && array(raw.reason_codes);
  const provenance = raw && record(raw.provenance);
  if (!raw || !currentState || !resolutionId || !ruleRef || !reasons || reasons.length !== 1 || typeof reasons[0] !== "string"
    || !resolutionReasons.has(reasons[0]) || !provenance || !structuralEqual(ruleRef, canonicalActionRule)
    || !structuralEqual(provenance.action_rule_ref, canonicalActionRule)
    || !structuralEqual(provenance.full_model_contract_ref, canonicalFullModelContract)
    || !structuralEqual(provenance.defect_risk_contract_ref, canonicalDefectRiskContract)
    || !structuralEqual(provenance.process_reassessment_contract_ref, canonicalProcessContract)) return null;
  if (currentState.status !== "AVAILABLE") {
    if (raw.action_ref !== null || raw.action !== null) return null;
    return { ...currentState, raw, resolutionId, actionRef: null, reasonCode: reasons[0], sourceRiskRef: record(raw.source_risk_ref), sourceProblemRef: record(raw.source_problem_ref), sourceRelationRef: record(raw.source_relation_ref), ruleRef, action: null };
  }
  const actionRef = record(raw.action_ref);
  const sourceRiskRef = record(raw.source_risk_ref);
  const sourceProblemRef = record(raw.source_problem_ref);
  const sourceRelationRef = record(raw.source_relation_ref);
  if (!actionRef || !sourceRiskRef || !sourceProblemRef || !sourceRelationRef
    || !structuralEqual(provenance.source_risk_ref, sourceRiskRef)
    || !structuralEqual(provenance.source_problem_ref, sourceProblemRef)
    || !structuralEqual(provenance.source_relation_ref, sourceRelationRef)
    || !sourceGraphResolves(fullModel, raw)) return null;
  const action = projectAction(raw.action, actionRef, raw);
  if (!action) return null;
  return { ...currentState, raw, resolutionId, actionRef, reasonCode: reasons[0], sourceRiskRef, sourceProblemRef, sourceRelationRef, ruleRef, action };
}

function projectExternalRevision(value: unknown, action: ActionProjection, initial: SpecificationProjection, revised: SpecificationProjection): ExternalRevisionProjection | null {
  const raw = record(value);
  const revisionId = raw && text(raw.revision_id);
  const revisionVersion = raw && text(raw.revision_version);
  const revisionRef = revisionId && revisionVersion ? { revision_id: revisionId, revision_version: revisionVersion } : null;
  const providerRef = raw && record(raw.provider_ref);
  const actionRef = raw && record(raw.action_ref);
  const parent = raw && record(raw.parent_artifact_ref);
  const child = raw && record(raw.requested_child_artifact_ref);
  const replacementsRaw = raw && array(raw.replacements);
  const provenance = raw && record(raw.provenance);
  if (!raw || raw.status !== null || raw.applicability !== null || !revisionRef || !providerRef || !actionRef || !parent || !child || !replacementsRaw || !provenance
    || !providerKinds.has(String(raw.provider_kind)) || !identifiers(providerRef, "provider_id", "provider_version")
    || !structuralEqual(actionRef, action.actionRef) || !structuralEqual(parent, initial.artifactRef) || !structuralEqual(child, revised.artifactRef)
    || !structuralEqual(provenance.revision_ref, revisionRef) || !structuralEqual(provenance.action_ref, actionRef)
    || !structuralEqual(provenance.parent_artifact_ref, parent) || !structuralEqual(provenance.requested_child_artifact_ref, child)
    || !structuralEqual(provenance.provider_ref, providerRef) || !structuralEqual(provenance.process_reassessment_contract_ref, canonicalProcessContract)
    || !structuralEqual(provenance.application_rule_ref, canonicalApplicationRule)
    || (raw.provider_rationale_or_none !== null && typeof raw.provider_rationale_or_none !== "string")) return null;
  const replacements = replacementsRaw.map((item) => {
    const replacement = record(item);
    const lineage = replacement && record(replacement.lineage_id);
    const expected = replacement && record(replacement.expected_parent_subject_ref);
    const replacementText = replacement && text(replacement.replacement_text);
    const target = lineage && action.targets.find((candidate) => structuralEqual(candidate.lineage, lineage));
    const parentRequirement = lineage && initial.requirements.find((candidate) => structuralEqual(candidate.lineage, lineage));
    return replacement && lineage && expected && replacementText && target && parentRequirement && structuralEqual(expected, parentRequirement.subject)
      ? { lineage, expectedParentSubject: expected, replacementText }
      : null;
  });
  if (replacements.some((item) => item === null)
    || replacements.some((item, index) => replacements.slice(0, index).some((prior) => structuralEqual(prior?.lineage, item?.lineage)))) return null;
  return {
    raw, revisionRef, providerKind: raw.provider_kind as string, providerRef, actionRef,
    parentArtifactRef: parent, childArtifactRef: child, replacements: replacements as RevisionReplacementProjection[],
    providerRationale: raw.provider_rationale_or_none as string | null,
  };
}

function projectApplication(value: unknown, action: ActionProjection, revision: ExternalRevisionProjection, initial: SpecificationProjection, revised: SpecificationProjection): ApplicationProjection | null {
  const raw = record(value);
  const applicationRef = raw && exactRef(raw, "application_id", "application_version");
  const actionBefore = raw && record(raw.action_before_ref);
  const actionAfter = raw && record(raw.action_after_ref);
  const revisionRef = raw && record(raw.revision_ref);
  const parent = raw && record(raw.parent_artifact_ref);
  const child = raw && record(raw.child_artifact_ref);
  const changed = raw && array(raw.changed_subjects);
  const ruleRef = raw && record(raw.rule_ref);
  const reasons = raw && array(raw.reason_codes);
  const provenance = raw && record(raw.provenance);
  const applied = raw && record(raw.applied_action);
  const transition = raw && record(raw.transition);
  const appliedVersion = applied && text(applied.action_record_version);
  const appliedRef = applied && appliedVersion ? { action_id: applied.action_id, action_record_version: appliedVersion } : null;
  if (!raw || raw.status !== "AVAILABLE" || raw.applicability !== null || !applicationRef || !actionBefore || !actionAfter || !revisionRef || !parent || !child
    || !changed || !ruleRef || !reasons || reasons.length !== 1 || reasons[0] !== "EXTERNAL_REVISION_MATERIALIZED"
    || !provenance || !applied || !appliedVersion || !appliedRef || !transition
    || !structuralEqual(ruleRef, canonicalApplicationRule) || !structuralEqual(actionBefore, action.actionRef)
    || !structuralEqual(actionAfter, appliedRef) || !structuralEqual(revisionRef, revision.revisionRef)
    || !structuralEqual(parent, initial.artifactRef) || !structuralEqual(child, revised.artifactRef)
    || !structuralEqual(changed, revised.changedSubjects)
    || !structuralEqual(withoutScientificWrapper(revised.raw), raw.child_specification)
    || applied.status !== "APPLIED" || appliedVersion === action.actionRecordVersion
    || !structuralEqual(applied.action_id, action.raw.action_id) || !structuralEqual(applied.predecessor_action_ref, action.actionRef)
    || !structuralEqual(applied.external_revision_ref, revision.revisionRef) || !structuralEqual(applied.application_ref, applicationRef)
    || !structuralEqual(provenance.action_before_ref, actionBefore) || !structuralEqual(provenance.action_after_ref, actionAfter)
    || !structuralEqual(provenance.revision_ref, revisionRef) || !structuralEqual(provenance.parent_artifact_ref, parent)
    || !structuralEqual(provenance.child_artifact_ref, child) || !structuralEqual(provenance.application_rule_ref, canonicalApplicationRule)
    || !structuralEqual(provenance.process_reassessment_contract_ref, canonicalProcessContract)
    || !structuralEqual(transition.parent_artifact_ref, parent) || !structuralEqual(transition.child_artifact_ref, child)
    || !structuralEqual(transition.action_application_ref, applicationRef) || !structuralEqual(transition.revision_ref, revisionRef)
    || !structuralEqual(transition.changed_subjects, changed)) return null;
  return {
    status: "AVAILABLE", raw, applicationRef, actionBeforeRef: actionBefore, actionAfterRef: actionAfter, revisionRef,
    parentArtifactRef: parent, childArtifactRef: child, changedSubjects: changed as JsonRecord[], ruleRef,
    reasonCode: "EXTERNAL_REVISION_MATERIALIZED", appliedActionVersion: appliedVersion,
  };
}

function lineageIsCoherent(initial: SpecificationProjection, revised: SpecificationProjection, application: ApplicationProjection): boolean {
  if (!revised.parentArtifactRef || !revised.applicationRef
    || !structuralEqual(revised.parentArtifactRef, initial.artifactRef)
    || !structuralEqual(revised.applicationRef, application.applicationRef)
    || initial.artifactRef.artifact_id !== revised.artifactRef.artifact_id
    || initial.artifactRef.artifact_version === revised.artifactRef.artifact_version
    || initial.requirements.length !== revised.requirements.length) return false;
  return revised.requirements.every((item, index) => structuralEqual(item.lineage, initial.requirements[index]?.lineage)
    && structuralEqual(item.predecessorSubject, initial.requirements[index]?.subject));
}

function changedRequirements(initial: SpecificationProjection, revised: SpecificationProjection): ChangedRequirementProjection[] | null {
  const projected = revised.changedSubjects.map((changed) => {
    const lineage = record(changed.lineage_id);
    const before = record(changed.before_subject_ref);
    const after = record(changed.after_subject_ref);
    const beforeRequirement = lineage && before && initial.requirements.find((item) => structuralEqual(item.lineage, lineage) && structuralEqual(item.subject, before));
    const afterRequirement = lineage && after && revised.requirements.find((item) => structuralEqual(item.lineage, lineage) && structuralEqual(item.subject, after));
    return lineage && before && after && changed.change_kind === "REPLACE_TEXT" && beforeRequirement && afterRequirement
      ? { lineage, beforeSubject: before, afterSubject: after, beforeText: beforeRequirement.text, afterText: afterRequirement.text, changeKind: "REPLACE_TEXT" as const }
      : null;
  });
  return projected.some((item) => item === null) ? null : projected as ChangedRequirementProjection[];
}

function topRequirement(value: unknown): { id: string; sourceLine: number; text: string } | null {
  const container = record(value);
  const requirement = container && record(container.requirement);
  const id = requirement && text(requirement.id);
  const sourceLine = requirement && positiveInteger(requirement.source_line);
  const requirementText = requirement && text(requirement.text);
  return id && sourceLine && requirementText ? { id, sourceLine, text: requirementText } : null;
}

function withNavigation(response: CanonicalAnalyzeResponse, action: ActionProjection, initial: SpecificationProjection, revised: SpecificationProjection): ActionProjection {
  const current = response.analysis_case === "REASSESSMENT" ? revised : initial;
  const top = response.requirements.map(topRequirement);
  return {
    ...action,
    targets: action.targets.map((target) => {
      const versioned = current.requirements.find((item) => structuralEqual(item.subject, target.subject));
      const visible = top.find((item) => item?.id === target.requirementId && item.sourceLine === target.sourceLine && item.text === versioned?.text);
      return { ...target, navigationRequirementId: versioned && visible ? target.requirementId : null };
    }),
  };
}

function eligibleReassessment(response: CanonicalAnalyzeResponse, fullModel: JsonRecord, revised: SpecificationProjection): ReassessmentEntryProjection | null {
  if (response.analysis_case !== "CONTROLLED_DEMO") return null;
  const context = record(response.reassessment_context);
  const scenario = context && record(context.scenario);
  if (!context || !scenario || !structuralEqual(scenario, response.controlled_scenario) || !text(context.context_digest)) return null;
  const recordFields = [
    "initial_specification", "initial_specification_assessment", "predecessor_process_state", "corrective_action_resolution",
    "action_application", "external_revision", "revised_specification", "reassessment_identity", "successor_process_state", "process_transition",
  ];
  if (recordFields.some((field) => !record(context[field])) || !array(context.evidence_reuse_decisions) || !array(context.comparisons)) return null;
  const pairs = [
    ["initial_specification", "initial_specification"], ["initial_specification_assessment", "initial_specification_assessment"],
    ["corrective_action_resolution", "corrective_action_resolution"], ["action_application", "action_application"],
    ["external_revision", "external_revision"], ["revised_specification", "revised_specification"],
    ["predecessor_process_state", "process_v1"], ["successor_process_state", "process_v2"],
    ["process_transition", "process_transition"], ["comparisons", "comparisons"],
  ];
  if (pairs.some(([contextField, modelField]) => !structuralEqual(context[contextField], fullModel[modelField]))) return null;
  const contextRevised = record(context.revised_specification);
  const requirementsRaw = contextRevised && array(contextRevised.requirements);
  if (!contextRevised || !requirementsRaw || !structuralEqual(contextRevised, revised.raw)) return null;
  const requirements = requirementsRaw.map((item) => {
    const requirement = record(item);
    const subject = requirement && record(requirement.subject_ref);
    const sourceLine = subject && positiveInteger(subject.source_line);
    const requirementText = requirement && text(requirement.text);
    return sourceLine && requirementText ? { text: requirementText, source_line: sourceLine } : null;
  });
  if (requirements.some((item) => item === null)
    || requirements.some((item, index) => index > 0 && (item?.source_line ?? 0) <= (requirements[index - 1]?.source_line ?? 0))) return null;
  return { priorContext: context, requirements: requirements as RequirementInput[] };
}

export function selectCorrectiveActionsPage(response: CanonicalAnalyzeResponse): CorrectiveActionsPageProjection {
  const availability = selectSectionAvailability(response, "corrective_actions");
  if (!availability) return { kind: "MALFORMED" };
  if (availability.availability === "UNAVAILABLE") {
    return availability.reasonCode ? { kind: "UNAVAILABLE", reasonCode: availability.reasonCode } : { kind: "MALFORMED" };
  }
  const fullModel = record(response.full_model);
  if (!fullModel) return { kind: "MALFORMED" };
  const resolution = projectResolution(fullModel.corrective_action_resolution, fullModel);
  if (!resolution) return { kind: "MALFORMED" };
  if (!resolution.action) return { kind: "AVAILABLE", resolution, externalRevision: null, application: null, changedRequirements: [], reassessment: null };

  const initial = projectSpecification(fullModel.initial_specification, true);
  const revised = projectSpecification(fullModel.revised_specification, false);
  if (!initial || !revised) return { kind: "MALFORMED" };
  const revision = projectExternalRevision(fullModel.external_revision, resolution.action, initial, revised);
  if (!revision) return { kind: "MALFORMED" };
  const application = projectApplication(fullModel.action_application, resolution.action, revision, initial, revised);
  if (!application || !lineageIsCoherent(initial, revised, application)) return { kind: "MALFORMED" };
  const changed = changedRequirements(initial, revised);
  if (!changed) return { kind: "MALFORMED" };
  const action = withNavigation(response, resolution.action, initial, revised);
  const projectedResolution = { ...resolution, action };
  return {
    kind: "AVAILABLE",
    resolution: projectedResolution,
    externalRevision: revision,
    application,
    changedRequirements: changed,
    reassessment: eligibleReassessment(response, fullModel, revised),
  };
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

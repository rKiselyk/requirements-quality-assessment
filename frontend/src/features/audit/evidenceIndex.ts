import type { EvidenceDrawerFinding, EvidenceDrawerRecord } from "../../components/scientific";
import { isPlainRecord } from "./tree";

export interface AuditEvidenceTarget {
  evidence: EvidenceDrawerRecord;
  sourceLine: number | null;
  requirementText: string;
  linkedFindings: EvidenceDrawerFinding[];
  artifactRef: AuditArtifactRef | null;
}

export interface AuditArtifactRef {
  artifactId: string;
  artifactVersion: string;
}

export interface AuditEvidenceIndex {
  resolve(value: unknown, fieldKey: string | null): AuditEvidenceTarget | null;
}

const referenceFields = new Set([
  "evidence_ref",
  "evidence_refs",
  "ordered_evidence_refs",
  "ordered_cross_evidence_refs",
  "direct_criterion_evidence_refs",
  "source_component_refs",
  "source_evidence_ref",
  "source_evidence_refs",
  "metric_evidence_refs",
  "comparator_evidence_refs",
  "value_evidence_refs",
  "unit_evidence_refs",
  "context_evidence_refs",
  "matched_context_evidence_ref",
  "ref",
]);

const stringReferenceFields = new Set([
  "evidence_ref",
  "evidence_refs",
  "ordered_evidence_refs",
]);

interface EvidenceReferenceIdentity {
  evidenceId: string;
  requirementId?: string;
  sourceLine?: number;
  artifactRef?: AuditArtifactRef;
}

function nonEmptyText(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function integer(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) ? value : null;
}

function hasExactKeys(value: Record<string, unknown>, keys: readonly string[]): boolean {
  const actual = Object.keys(value);
  return actual.length === keys.length && keys.every((key) => actual.includes(key));
}

function artifactRef(value: unknown): AuditArtifactRef | null {
  if (!isPlainRecord(value) || !hasExactKeys(value, ["artifact_id", "artifact_version"])) return null;
  const artifactId = nonEmptyText(value.artifact_id);
  const artifactVersion = nonEmptyText(value.artifact_version);
  return artifactId && artifactVersion ? { artifactId, artifactVersion } : null;
}

function sameArtifact(left: AuditArtifactRef, right: AuditArtifactRef): boolean {
  return left.artifactId === right.artifactId && left.artifactVersion === right.artifactVersion;
}

function artifactKey(value: AuditArtifactRef): string {
  return JSON.stringify([value.artifactId, value.artifactVersion]);
}

function sourceRequirement(value: unknown) {
  if (!isPlainRecord(value)) return null;
  const id = nonEmptyText(value.id);
  const text = typeof value.text === "string" ? value.text : null;
  const sourceLine = value.source_line === undefined ? null : integer(value.source_line);
  if (!id || text === null || (value.source_line !== undefined && (sourceLine === null || sourceLine < 1))) return null;
  return { id, text, sourceLine };
}

function canonicalEvidence(value: unknown, requirementId: string, requirementText: string): EvidenceDrawerRecord | null {
  if (!isPlainRecord(value)) return null;
  const evidenceId = nonEmptyText(value.evidence_id);
  const evidenceRequirementId = nonEmptyText(value.requirement_id);
  const featureId = nonEmptyText(value.feature_id);
  const text = typeof value.text === "string" ? value.text : null;
  const startOffset = integer(value.start_offset);
  const endOffset = integer(value.end_offset);
  const ruleId = nonEmptyText(value.rule_id);
  if (!evidenceId || evidenceRequirementId !== requirementId || !featureId || text === null
    || startOffset === null || startOffset < 0 || endOffset === null || endOffset < startOffset || !ruleId) return null;
  const sourceSlice = Array.from(requirementText).slice(startOffset, endOffset).join("");
  if (sourceSlice !== text) return null;
  return { evidenceId, requirementId: evidenceRequirementId, featureId, text, startOffset, endOffset, ruleId };
}

function collectFindings(value: unknown, evidenceId: string): EvidenceDrawerFinding[] {
  const findings: EvidenceDrawerFinding[] = [];
  const visited = new WeakSet<object>();
  const visit = (candidate: unknown) => {
    if (Array.isArray(candidate)) {
      for (const item of candidate) visit(item);
      return;
    }
    if (!isPlainRecord(candidate) || visited.has(candidate)) return;
    visited.add(candidate);
    if (Array.isArray(candidate.evidence_refs) && candidate.evidence_refs.includes(evidenceId)) {
      const findingId = nonEmptyText(candidate.finding_id);
      const characteristicId = nonEmptyText(candidate.characteristic_id);
      const kind = nonEmptyText(candidate.kind);
      const code = nonEmptyText(candidate.code);
      const ruleId = nonEmptyText(candidate.rule_id);
      const explanation = typeof candidate.explanation === "string" ? candidate.explanation : null;
      if (findingId && characteristicId && kind && code && ruleId && explanation !== null) {
        findings.push({ findingId, characteristicId, kind, code, ruleId, explanation });
      }
    }
    for (const nested of Object.values(candidate)) visit(nested);
  };
  visit(value);
  return findings;
}

export function buildEvidenceIndex(root: unknown): AuditEvidenceIndex {
  const byObject = new WeakMap<object, AuditEvidenceTarget>();
  const byId = new Map<string, AuditEvidenceTarget[]>();
  const visited = new WeakSet<object>();

  const indexAssessment = (
    assessment: Record<string, unknown>,
    findingsOwner: unknown,
    inheritedArtifactRef: AuditArtifactRef | null,
  ) => {
    const requirement = sourceRequirement(assessment.requirement);
    if (!requirement || !Array.isArray(assessment.evidence)) return;
    for (const item of assessment.evidence) {
      const evidence = canonicalEvidence(item, requirement.id, requirement.text);
      if (!evidence || !isPlainRecord(item)) continue;
      const target: AuditEvidenceTarget = {
        evidence,
        sourceLine: requirement.sourceLine,
        requirementText: requirement.text,
        linkedFindings: collectFindings(findingsOwner, evidence.evidenceId),
        artifactRef: inheritedArtifactRef,
      };
      const existing = byObject.get(item);
      if (existing) {
        if (!existing.linkedFindings.length && target.linkedFindings.length) existing.linkedFindings = target.linkedFindings;
        continue;
      }
      byObject.set(item, target);
      const candidates = byId.get(evidence.evidenceId) ?? [];
      candidates.push(target);
      byId.set(evidence.evidenceId, candidates);
    }
  };

  const directlyContainedArtifact = (value: Record<string, unknown>, inherited: AuditArtifactRef | null) => {
    if (Object.hasOwn(value, "artifact_ref")) return artifactRef(value.artifact_ref);
    if (Object.hasOwn(value, "specification_version")) {
      const specificationVersion = isPlainRecord(value.specification_version) ? value.specification_version : null;
      return specificationVersion && Object.hasOwn(specificationVersion, "artifact_ref")
        ? artifactRef(specificationVersion.artifact_ref)
        : null;
    }
    return inherited;
  };

  const artifactForChild = (
    parent: Record<string, unknown>,
    key: string,
    inherited: AuditArtifactRef | null,
  ) => {
    if (key === "initial_specification_assessment") {
      const initialSpecification = isPlainRecord(parent.initial_specification) ? parent.initial_specification : null;
      return initialSpecification && Object.hasOwn(initialSpecification, "artifact_ref")
        ? artifactRef(initialSpecification.artifact_ref)
        : inherited;
    }
    return inherited;
  };

  const visit = (value: unknown, inheritedArtifactRef: AuditArtifactRef | null = null) => {
    if (Array.isArray(value)) {
      if (visited.has(value)) return;
      visited.add(value);
      for (const item of value) visit(item, inheritedArtifactRef);
      return;
    }
    if (!isPlainRecord(value) || visited.has(value)) return;
    visited.add(value);
    const currentArtifactRef = directlyContainedArtifact(value, inheritedArtifactRef);
    indexAssessment(value, value.quality_profile ?? value, currentArtifactRef);
    if (isPlainRecord(value.extraction_result)) {
      indexAssessment(value.extraction_result, value.quality_profile ?? value, currentArtifactRef);
    }
    for (const [key, nested] of Object.entries(value)) {
      visit(nested, artifactForChild(value, key, currentArtifactRef));
    }
  };
  visit(root);

  const referenceIdentity = (value: unknown, fieldKey: string): EvidenceReferenceIdentity | null => {
    if (typeof value === "string") {
      return stringReferenceFields.has(fieldKey) && value.length > 0 ? { evidenceId: value } : null;
    }
    if (!isPlainRecord(value)) return null;
    const evidenceId = nonEmptyText(value.evidence_id);
    if (!evidenceId) return null;

    if (Object.hasOwn(value, "requirement_subject_ref")) {
      if (!hasExactKeys(value, ["requirement_subject_ref", "evidence_id"])) return null;
      const subject = isPlainRecord(value.requirement_subject_ref) ? value.requirement_subject_ref : null;
      const requirementId = subject && nonEmptyText(subject.requirement_id);
      const sourceLine = subject && integer(subject.source_line);
      const subjectArtifactRef = subject && artifactRef(subject.artifact_ref);
      if (!subject || !subjectArtifactRef || !requirementId || sourceLine === null || sourceLine < 1) return null;
      return { evidenceId, requirementId, sourceLine, artifactRef: subjectArtifactRef };
    }

    if (!hasExactKeys(value, ["requirement_id", "evidence_id"])) return null;
    const requirementId = nonEmptyText(value.requirement_id);
    return requirementId ? { evidenceId, requirementId } : null;
  };

  const resolveReference = (value: unknown, fieldKey: string): AuditEvidenceTarget | null => {
    const reference = referenceIdentity(value, fieldKey);
    if (!reference) return null;
    let candidates = [...(byId.get(reference.evidenceId) ?? [])];
    if (reference.requirementId) candidates = candidates.filter((item) => item.evidence.requirementId === reference.requirementId);
    if (reference.sourceLine !== undefined) candidates = candidates.filter((item) => item.sourceLine === reference.sourceLine);
    if (reference.artifactRef) {
      candidates = candidates.filter((item) => item.artifactRef !== null && sameArtifact(item.artifactRef, reference.artifactRef as AuditArtifactRef));
    }

    const bySourceIdentity = new Map<string, AuditEvidenceTarget[]>();
    for (const candidate of candidates) {
      const evidence = candidate.evidence;
      const key = JSON.stringify([
        evidence.requirementId, candidate.sourceLine, candidate.requirementText, evidence.evidenceId,
        evidence.featureId, evidence.text, evidence.startOffset, evidence.endOffset, evidence.ruleId,
      ]);
      const group = bySourceIdentity.get(key) ?? [];
      group.push(candidate);
      bySourceIdentity.set(key, group);
    }

    const distinct: AuditEvidenceTarget[] = [];
    for (const group of bySourceIdentity.values()) {
      const knownArtifacts = new Map<string, AuditEvidenceTarget>();
      const unknownArtifacts: AuditEvidenceTarget[] = [];
      for (const candidate of group) {
        if (candidate.artifactRef) {
          const key = artifactKey(candidate.artifactRef);
          if (!knownArtifacts.has(key)) knownArtifacts.set(key, candidate);
        }
        else unknownArtifacts.push(candidate);
      }
      distinct.push(...knownArtifacts.values());
      if (knownArtifacts.size === 0 && unknownArtifacts.length) distinct.push(unknownArtifacts[0]);
      else if (knownArtifacts.size > 1 && unknownArtifacts.length) distinct.push(unknownArtifacts[0]);
    }
    return distinct.length === 1 ? distinct[0] : null;
  };

  return {
    resolve(value, fieldKey) {
      if (typeof value === "object" && value !== null) {
        const exact = byObject.get(value);
        if (exact) return exact;
      }
      if (!fieldKey || !referenceFields.has(fieldKey)) return null;
      return resolveReference(value, fieldKey);
    },
  };
}

import type { EvidenceDrawerFinding, EvidenceDrawerRecord } from "../../components/scientific";
import { isPlainRecord } from "./tree";

export interface AuditEvidenceTarget {
  evidence: EvidenceDrawerRecord;
  sourceLine: number | null;
  requirementText: string;
  linkedFindings: EvidenceDrawerFinding[];
}

export interface AuditEvidenceIndex {
  resolve(value: unknown, fieldKey: string | null): AuditEvidenceTarget | null;
}

const referenceFields = new Set([
  "evidence_ref",
  "evidence_refs",
  "ordered_evidence_refs",
  "source_evidence_ref",
]);

function nonEmptyText(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function integer(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) ? value : null;
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

  const indexAssessment = (assessment: Record<string, unknown>, findingsOwner: unknown) => {
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

  const visit = (value: unknown) => {
    if (Array.isArray(value)) {
      if (visited.has(value)) return;
      visited.add(value);
      for (const item of value) visit(item);
      return;
    }
    if (!isPlainRecord(value) || visited.has(value)) return;
    visited.add(value);
    indexAssessment(value, value.quality_profile ?? value);
    if (isPlainRecord(value.extraction_result)) {
      indexAssessment(value.extraction_result, value.quality_profile ?? value);
    }
    for (const nested of Object.values(value)) visit(nested);
  };
  visit(root);

  const resolveReference = (value: unknown): AuditEvidenceTarget | null => {
    const reference = typeof value === "string" ? { evidenceId: value } : isPlainRecord(value)
      ? {
          evidenceId: nonEmptyText(value.evidence_id),
          requirementId: nonEmptyText(value.requirement_id),
          featureId: nonEmptyText(value.feature_id),
          text: typeof value.text === "string" ? value.text : null,
          startOffset: integer(value.start_offset),
          endOffset: integer(value.end_offset),
          ruleId: nonEmptyText(value.rule_id),
          sourceLine: integer(value.source_line),
        }
      : null;
    if (!reference?.evidenceId) return null;
    let candidates = [...(byId.get(reference.evidenceId) ?? [])];
    if ("requirementId" in reference && reference.requirementId) candidates = candidates.filter((item) => item.evidence.requirementId === reference.requirementId);
    if ("featureId" in reference && reference.featureId) candidates = candidates.filter((item) => item.evidence.featureId === reference.featureId);
    if ("text" in reference && reference.text !== null) candidates = candidates.filter((item) => item.evidence.text === reference.text);
    if ("startOffset" in reference && reference.startOffset !== null) candidates = candidates.filter((item) => item.evidence.startOffset === reference.startOffset);
    if ("endOffset" in reference && reference.endOffset !== null) candidates = candidates.filter((item) => item.evidence.endOffset === reference.endOffset);
    if ("ruleId" in reference && reference.ruleId) candidates = candidates.filter((item) => item.evidence.ruleId === reference.ruleId);
    if ("sourceLine" in reference && reference.sourceLine !== null) candidates = candidates.filter((item) => item.sourceLine === reference.sourceLine);
    return candidates.length === 1 ? candidates[0] : null;
  };

  return {
    resolve(value, fieldKey) {
      if (typeof value === "object" && value !== null) {
        const exact = byObject.get(value);
        if (exact) return exact;
      }
      if (!fieldKey || fieldKey.includes("dynamic") || !referenceFields.has(fieldKey)) return null;
      return resolveReference(value);
    },
  };
}

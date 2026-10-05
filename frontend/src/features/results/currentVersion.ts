import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { structuralEqual } from "./structuralIdentity";

export type JsonRecord = Record<string, unknown>;

export interface CurrentResultRecords {
  revision: "CONTROLLED_DEMO_V1" | "REASSESSMENT_V2";
  records: JsonRecord;
}

function record(value: unknown): JsonRecord | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? value as JsonRecord
    : null;
}

function array(value: unknown): unknown[] | null {
  return Array.isArray(value) ? value : null;
}

/**
 * Selects the one canonical current downstream result used by presentation.
 * Pairing is positional because produced_result_refs and produced_results form
 * one ordered canonical pair population in the reassessment contract.
 */
export function selectCurrentResultRecords(response: CanonicalAnalyzeResponse): CurrentResultRecords | null {
  const fullModel = record(response.full_model);
  if (!fullModel) return null;
  if (response.analysis_case === "CONTROLLED_DEMO") {
    return { revision: "CONTROLLED_DEMO_V1", records: fullModel };
  }
  if (response.analysis_case !== "REASSESSMENT") return null;

  const reassessment = record(fullModel.reassessment);
  const refs = reassessment && array(reassessment.produced_result_refs);
  const results = reassessment && array(reassessment.produced_results);
  const context = reassessment && record(reassessment.context);
  const provenance = reassessment && record(reassessment.provenance);
  const childArtifact = context && record(context.child_artifact_ref);
  const provenanceChild = provenance && record(provenance.child_artifact_ref);
  if (!reassessment || !refs || !results || refs.length !== results.length || !childArtifact || !provenanceChild
    || !structuralEqual(childArtifact, provenanceChild)) return null;

  const indexes = refs.flatMap((item, index) =>
    record(item)?.result_family === "FULL_MODEL_DYNAMIC_THROUGH_RISK_PATH" ? [index] : []);
  if (indexes.length !== 1) return null;

  const ref = record(refs[indexes[0]]);
  const result = record(results[indexes[0]]);
  const refArtifact = ref && record(ref.artifact_ref);
  const resultArtifact = result && record(result.artifact_ref);
  const riskAssessment = result && record(result.risk_assessment);
  const refResultId = ref && record(ref.result_id);
  const riskAssessmentId = riskAssessment && record(riskAssessment.risk_assessment_id);
  if (!ref || !result || !refArtifact || !resultArtifact
    || !riskAssessment || !refResultId || !riskAssessmentId
    || !structuralEqual(refResultId, riskAssessmentId)
    || !structuralEqual(refArtifact, resultArtifact)
    || !structuralEqual(resultArtifact, childArtifact)) return null;
  return { revision: "REASSESSMENT_V2", records: result };
}

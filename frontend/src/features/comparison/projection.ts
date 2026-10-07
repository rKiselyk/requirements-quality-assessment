import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import type { ExactValueData } from "../../components/scientific";
import { structuralEqual } from "../results/structuralIdentity";
import {
  canonicalStringArray,
  hasAvailableLifecycleSection,
  nonEmptyText,
  record,
  selectReassessmentProjection,
  type JsonRecord,
  type ReassessmentProjection,
} from "../reassessment/projection";

const COMPARISON_RULE = {
  rule_id: "COMPARE-FULL-MODEL-001",
  explicit_version: "1",
  version_authority: "EXPLICIT_CONTRACT_VERSION",
};
const families = [
  "REQUIREMENT_METRIC", "SPECIFICATION_METRIC", "QB_CONSISTENCY",
  "CRITERION_CONFORMANCE", "PERFORMANCE_EFFICIENCY_FEATURE", "PRODUCT_QUALITY",
  "CONFIRMED_PROBLEM", "DEFECT_QUALITY_RELATION", "BOUNDED_RISK",
] as const;
const kinds = ["UNCHANGED", "INCREASED", "DECREASED", "STATE_CHANGED", "NOT_COMPARABLE"] as const;
const statuses = ["AVAILABLE", "UNAVAILABLE", "UNKNOWN", "UNRESOLVED", "UNSUPPORTED", "NOT_APPLICABLE"] as const;
const applicabilityValues = ["APPLICABLE", "UNKNOWN", "NOT_APPLICABLE"] as const;
const reasons = [
  "EXACT_VALUES_EQUAL", "EXACT_VALUE_INCREASED", "EXACT_VALUE_DECREASED",
  "STRUCTURED_STATE_UNCHANGED", "STRUCTURED_STATE_CHANGED", "REQUIRED_RESULT_UNAVAILABLE",
  "RESULT_IDENTITY_UNRESOLVED", "RESULT_FAMILY_MISMATCH", "VALUE_KIND_OR_SCALE_MISMATCH",
  "METRIC_OR_CHARACTERISTIC_MISMATCH", "SUBJECT_LINEAGE_MISSING_OR_MISMATCH",
  "ARTIFACT_ANCESTRY_MISSING_OR_MISMATCH", "SCOPE_OR_POPULATION_MISMATCH",
  "RULE_SEMANTICS_INCOMPATIBLE", "MODEL_SEMANTICS_INCOMPATIBLE",
  "PARAMETER_SEMANTICS_INCOMPATIBLE", "EVIDENCE_CONTEXT_MISMATCH",
  "PROCESS_STAGE_MISMATCH", "APPLICABILITY_SEMANTICS_INCOMPATIBLE",
  "RESULT_FAMILY_UNSUPPORTED",
] as const;
const mandatoryNonClaims = [
  "NO_DIRECTIONAL_QUALITY_INTERPRETATION",
  "NO_CAUSAL_EFFECT_INFERENCE",
  "NO_ACTION_SUCCESS_INFERENCE",
  "NO_STAKEHOLDER_INTENT_VALIDATION",
] as const;

type ComparisonKind = (typeof kinds)[number];

export interface StateAndValueProjection {
  status: string;
  applicability: string;
  exactValue: ExactValueData | null;
  categoricalState: string | null;
}

export interface ComparisonRecordProjection {
  comparisonId: string;
  comparisonVersion: string;
  family: string;
  metricOrCharacteristicId: string;
  status: string;
  kind: ComparisonKind | null;
  beforeResultRef: JsonRecord | null;
  afterResultRef: JsonRecord | null;
  subject: JsonRecord | null;
  before: StateAndValueProjection | null;
  after: StateAndValueProjection | null;
  reasonCodes: string[];
  ruleRef: JsonRecord;
  compatibilityDeclarationRefs: string[];
  parameterSetRefs: unknown[];
  calibrationStatus: string | null;
  explanation: string;
  provenance: unknown[];
  claims: string[];
  nonClaims: string[];
  raw: JsonRecord;
}

export interface ComparisonProjection {
  lifecycle: ReassessmentProjection;
  comparisons: ComparisonRecordProjection[];
}

function exactFraction(value: unknown): ExactValueData | null {
  const candidate = record(value);
  if (!candidate) return null;
  const numerator = typeof candidate.numerator === "number" && Number.isSafeInteger(candidate.numerator) ? candidate.numerator : null;
  const denominator = typeof candidate.denominator === "number" && Number.isSafeInteger(candidate.denominator) ? candidate.denominator : null;
  return numerator !== null && denominator !== null && denominator !== 0
    ? { numerator: String(numerator), denominator: String(denominator) }
    : null;
}

function stateAndValue(value: unknown): StateAndValueProjection | null {
  const candidate = record(value);
  if (!candidate || !statuses.includes(candidate.status as never)
    || !applicabilityValues.includes(candidate.applicability as never)) return null;
  const exactValue = candidate.exact_value === null ? null : exactFraction(candidate.exact_value);
  const categoricalState = candidate.categorical_state === null ? null : nonEmptyText(candidate.categorical_state);
  if ((candidate.exact_value !== null && exactValue === null)
    || (candidate.categorical_state !== null && categoricalState === null)
    || (exactValue !== null && categoricalState !== null)
    || (candidate.status === "AVAILABLE" && candidate.applicability !== "APPLICABLE")
    || (candidate.status === "NOT_APPLICABLE" && candidate.applicability !== "NOT_APPLICABLE")
    || (candidate.status !== "AVAILABLE" && candidate.status !== "NOT_APPLICABLE" && candidate.applicability === "NOT_APPLICABLE")
    || (candidate.status === "AVAILABLE" && exactValue === null && categoricalState === null)
    || (candidate.status !== "AVAILABLE" && (exactValue !== null || categoricalState !== null))) return null;
  return {
    status: candidate.status as string,
    applicability: candidate.applicability as string,
    exactValue,
    categoricalState,
  };
}

function resultRef(value: unknown, expectedArtifact: JsonRecord): JsonRecord | null {
  const candidate = record(value);
  return candidate
    && nonEmptyText(candidate.result_family)
    && candidate.result_id != null
    && structuralEqual(candidate.artifact_ref, expectedArtifact)
    ? candidate
    : null;
}

function subject(value: unknown): JsonRecord | null {
  const candidate = record(value);
  return candidate
    && families.includes(candidate.result_family as never)
    && nonEmptyText(candidate.metric_or_characteristic_id)
    && Array.isArray(candidate.stable_subject_identity)
    && Array.isArray(candidate.ordered_lineage_population)
    && Array.isArray(candidate.scope_identity)
    && Array.isArray(candidate.evidence_context)
    ? candidate
    : null;
}

function comparison(value: unknown, lifecycle: ReassessmentProjection, transitionId: JsonRecord): ComparisonRecordProjection | null {
  const candidate = record(value);
  if (!candidate || !nonEmptyText(candidate.comparison_id) || !nonEmptyText(candidate.comparison_version)
    || !statuses.includes(candidate.status as never)
    || !structuralEqual(candidate.rule_ref, COMPARISON_RULE)) return null;
  const kind = candidate.comparison_kind === null ? null : candidate.comparison_kind;
  if ((candidate.status === "AVAILABLE" && !kinds.includes(kind as never))
    || (candidate.status !== "AVAILABLE" && kind !== null)) return null;
  const reasonCodes = canonicalStringArray(candidate.reason_codes);
  if (!reasonCodes || reasonCodes.length === 0 || reasonCodes.some((reason) => !reasons.includes(reason as never))) return null;
  const projectedSubject = candidate.comparison_subject === null ? null : subject(candidate.comparison_subject);
  const beforeRef = candidate.before_result_ref === null ? null : resultRef(candidate.before_result_ref, lifecycle.parentArtifactRef);
  const afterRef = candidate.after_result_ref === null ? null : resultRef(candidate.after_result_ref, lifecycle.childArtifactRef);
  const before = candidate.before_state_and_value === null ? null : stateAndValue(candidate.before_state_and_value);
  const after = candidate.after_state_and_value === null ? null : stateAndValue(candidate.after_state_and_value);
  if ((candidate.comparison_subject !== null && !projectedSubject)
    || (candidate.before_result_ref !== null && !beforeRef)
    || (candidate.after_result_ref !== null && !afterRef)
    || (candidate.before_state_and_value !== null && !before)
    || (candidate.after_state_and_value !== null && !after)
    || (candidate.status === "AVAILABLE" && (!projectedSubject || !beforeRef || !afterRef || !before || !after))
    || (beforeRef && beforeRef.result_family !== "FULL-MODEL-SERVICE-COMPARABLE")
    || (afterRef && afterRef.result_family !== "FULL-MODEL-SERVICE-COMPARABLE")
    || (beforeRef && afterRef && structuralEqual(beforeRef, afterRef))) return null;
  const family = projectedSubject?.result_family as string | undefined;

  const declarationRefs = canonicalStringArray(candidate.compatibility_declaration_refs);
  const claims = canonicalStringArray(candidate.claims);
  const nonClaims = canonicalStringArray(candidate.non_claims);
  const explanation = typeof candidate.explanation === "string" ? candidate.explanation : null;
  const calibration = candidate.calibration_status_or_none === null ? null : nonEmptyText(candidate.calibration_status_or_none);
  const requestRef = { comparison_id: candidate.comparison_id, comparison_version: candidate.comparison_version };
  const expectedProvenance = [
    requestRef,
    transitionId,
    ...(beforeRef ? [beforeRef] : []),
    ...(afterRef ? [afterRef] : []),
    ...(declarationRefs ?? []),
    COMPARISON_RULE,
  ];
  if (!declarationRefs || !claims || !nonClaims || explanation === null || !Array.isArray(candidate.parameter_set_refs)
    || !Array.isArray(candidate.provenance) || (candidate.calibration_status_or_none !== null && !calibration)
    || claims.length !== 1 || claims[0] !== "STRUCTURED_CHANGE_ONLY"
    || !structuralEqual(nonClaims, mandatoryNonClaims)
    || !structuralEqual(candidate.provenance, expectedProvenance)) return null;

  return {
    comparisonId: candidate.comparison_id as string,
    comparisonVersion: candidate.comparison_version as string,
    family: family ?? "",
    metricOrCharacteristicId: projectedSubject?.metric_or_characteristic_id as string ?? "",
    status: candidate.status as string,
    kind: kind as ComparisonKind | null,
    beforeResultRef: beforeRef,
    afterResultRef: afterRef,
    subject: projectedSubject,
    before,
    after,
    reasonCodes,
    ruleRef: candidate.rule_ref as JsonRecord,
    compatibilityDeclarationRefs: declarationRefs,
    parameterSetRefs: [...candidate.parameter_set_refs],
    calibrationStatus: calibration,
    explanation,
    provenance: [...candidate.provenance],
    claims,
    nonClaims,
    raw: candidate,
  };
}

export function selectComparisonProjection(response: CanonicalAnalyzeResponse): ComparisonProjection | null {
  const lifecycle = selectReassessmentProjection(response);
  const fullModel = record(response.full_model);
  const actionApplication = fullModel && record(fullModel.action_application);
  const transition = actionApplication && record(actionApplication.transition);
  const transitionId = transition && record(transition.transition_id);
  if (!lifecycle || !fullModel || !hasAvailableLifecycleSection(response, "comparison")
    || !transitionId || !Array.isArray(fullModel.comparisons) || fullModel.comparisons.length === 0) return null;
  const projected = fullModel.comparisons.map((item) => comparison(item, lifecycle, transitionId));
  return projected.some((item) => item === null)
    ? null
    : { lifecycle, comparisons: projected as ComparisonRecordProjection[] };
}

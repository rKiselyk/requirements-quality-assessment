import type { ReassessmentAnalyzeRequest, RequirementInput } from "../specification-input/model";
import { parseSpecificationText } from "../specification-input/model";
import { structuralEqual } from "../results/structuralIdentity";

export function createReassessmentDraft(requirements: readonly RequirementInput[]): string {
  const finalLine = requirements.at(-1)?.source_line ?? 0;
  const lines = Array.from({ length: finalLine }, () => "");
  for (const requirement of requirements) lines[requirement.source_line - 1] = requirement.text;
  return lines.join("\n");
}

export function matchesCanonicalRevision(draft: string, requirements: readonly RequirementInput[]): boolean {
  return structuralEqual(parseSpecificationText(draft), requirements);
}

export function createReassessmentRequest(
  requirements: RequirementInput[],
  priorContext: Record<string, unknown>,
): ReassessmentAnalyzeRequest {
  return { case: "REASSESSMENT", requirements, prior_context: priorContext };
}

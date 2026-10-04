export interface EvidenceSpan {
  evidenceId: string;
  text: string;
  startOffset: number;
  endOffset: number;
}

export function validateEvidenceSpan(requirementText: string, selected: EvidenceSpan | null) {
  if (selected === null) return { valid: true as const, before: requirementText, selected: "", after: "" };
  const codePoints = Array.from(requirementText);
  const { startOffset, endOffset } = selected;
  if (startOffset < 0 || endOffset < startOffset || endOffset > codePoints.length) return { valid: false as const };
  const selectedText = codePoints.slice(startOffset, endOffset).join("");
  if (selectedText !== selected.text) return { valid: false as const };
  return {
    valid: true as const,
    before: codePoints.slice(0, startOffset).join(""),
    selected: selectedText,
    after: codePoints.slice(endOffset).join(""),
  };
}

export interface EvidenceHighlighterProps {
  requirementText: string;
  evidence: EvidenceSpan | null;
  mismatchMessage: string;
}

/** Highlights only a validated Unicode code-point span and always preserves the full source text. */
export function EvidenceHighlighter({ requirementText, evidence, mismatchMessage }: EvidenceHighlighterProps) {
  const span = validateEvidenceSpan(requirementText, evidence);
  if (!span.valid) {
    return (
      <>
        <p className="evidence-source-text">{requirementText}</p>
        <p className="evidence-span-error" role="status">{mismatchMessage}</p>
      </>
    );
  }
  return (
    <p className="evidence-source-text">
      {span.before}
      {evidence ? <mark data-evidence-id={evidence.evidenceId}>{span.selected}</mark> : null}
      {span.after}
    </p>
  );
}

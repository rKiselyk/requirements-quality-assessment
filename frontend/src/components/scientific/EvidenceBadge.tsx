import type { ButtonHTMLAttributes } from "react";

export interface EvidenceBadgeProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  evidenceId: string;
  kind: string;
  sourceText?: string;
}

export function EvidenceBadge({ evidenceId, kind, sourceText, className = "", ...props }: EvidenceBadgeProps) {
  const label = `${kind} evidence ${evidenceId}${sourceText ? `: ${sourceText}` : ""}`;
  return <button type="button" className={`evidence-badge ${className}`.trim()} aria-label={label} {...props}><span aria-hidden="true">⌁</span>{kind}<code>{evidenceId}</code></button>;
}

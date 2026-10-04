export type ScientificCode =
  | "COMPUTED"
  | "AVAILABLE"
  | "SATISFIED"
  | "UNKNOWN"
  | "UNRESOLVED"
  | "UNSUPPORTED"
  | "NOT_APPLICABLE"
  | "UNAVAILABLE"
  | "RISK_IDENTIFIED"
  | (string & {});

export type ApplicabilityCode = "APPLICABLE" | "UNKNOWN" | "NOT_APPLICABLE" | (string & {});
export type DisplayTone = "neutral";

/** Raw scientific codes receive no positive, negative, or severity interpretation. */
export function statusDisplayTone(_code: ScientificCode | ApplicabilityCode): DisplayTone {
  return "neutral";
}

export function StatusBadge({ code, label }: { code: ScientificCode; label?: string }) {
  return <span className={`status-badge status-badge--${statusDisplayTone(code)}`}><span className="status-badge__marker" aria-hidden="true" />{label ?? code}</span>;
}

export function ApplicabilityBadge({ code, label }: { code: ApplicabilityCode; label?: string }) {
  return <span className={`status-badge status-badge--${statusDisplayTone(code)}`}><span className="status-badge__marker" aria-hidden="true" />{label ?? code}</span>;
}

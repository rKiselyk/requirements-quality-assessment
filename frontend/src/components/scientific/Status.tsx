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
export type DisplayTone = "accent" | "warning" | "muted" | "critical" | "neutral";

/** Presentation mapping only. It does not derive or reinterpret a scientific state. */
export function statusDisplayTone(code: ScientificCode | ApplicabilityCode): DisplayTone {
  if (code === "COMPUTED" || code === "AVAILABLE" || code === "SATISFIED" || code === "APPLICABLE") return "accent";
  if (code === "UNKNOWN" || code === "UNRESOLVED" || code === "UNSUPPORTED") return "warning";
  if (code === "NOT_APPLICABLE" || code === "UNAVAILABLE") return "muted";
  if (code === "RISK_IDENTIFIED") return "critical";
  return "neutral";
}

export function StatusBadge({ code, label }: { code: ScientificCode; label?: string }) {
  return <span className={`status-badge status-badge--${statusDisplayTone(code)}`}><span className="status-badge__marker" aria-hidden="true" />{label ?? code}</span>;
}

export function ApplicabilityBadge({ code, label }: { code: ApplicabilityCode; label?: string }) {
  return <span className={`status-badge status-badge--${statusDisplayTone(code)}`}><span className="status-badge__marker" aria-hidden="true" />{label ?? code}</span>;
}

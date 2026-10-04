export interface ExactRational {
  numerator: string;
  denominator: string;
}

export interface ExactDecimal {
  exact: string;
}

export type ExactValueData = string | ExactRational | ExactDecimal;

function isRational(value: ExactValueData): value is ExactRational {
  return typeof value === "object" && "numerator" in value && "denominator" in value;
}

function exactText(value: ExactValueData): string {
  if (typeof value === "string") return value;
  if (isRational(value)) return `${value.numerator}/${value.denominator}`;
  return value.exact;
}

export interface ExactValueProps {
  value?: ExactValueData | null;
  fallback?: string;
  label?: string;
  compact?: boolean;
}

/** Renders canonical exact data as text; it never parses, divides, or rounds it. */
export function ExactValue({ value, fallback = "Unavailable", label = "Exact value", compact = false }: ExactValueProps) {
  return (
    <span className={`exact-value ${compact ? "exact-value--compact" : ""}`} aria-label={`${label}: ${value == null ? fallback : exactText(value)}`}>
      {value == null ? fallback : exactText(value)}
    </span>
  );
}

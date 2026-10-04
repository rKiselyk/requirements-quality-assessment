import type { HTMLAttributes, ReactNode } from "react";
import { ExactValue, type ExactValueData } from "../scientific/ExactValue";
import { StatusBadge, type ScientificCode } from "../scientific/Status";

export interface CardProps extends HTMLAttributes<HTMLElement> {
  title?: string;
  description?: string;
  children: ReactNode;
}

export function Card({ title, description, children, className = "", ...props }: CardProps) {
  return (
    <section className={`card ${className}`.trim()} {...props}>
      {title || description ? <header className="card__header">{title ? <h2 className="card__title">{title}</h2> : null}{description ? <p>{description}</p> : null}</header> : null}
      <div className="card__body">{children}</div>
    </section>
  );
}

export interface MetricCardProps {
  label: string;
  value?: ExactValueData | null;
  status: ScientificCode;
  detail?: string;
}

export function MetricCard({ label, value, status, detail }: MetricCardProps) {
  return (
    <article className="metric-card">
      <h3>{label}</h3>
      <ExactValue value={value} fallback="No value" />
      <StatusBadge code={status} />
      {detail ? <p>{detail}</p> : null}
    </article>
  );
}

import type { HTMLAttributes, ReactNode } from "react";
import { useTranslation } from "react-i18next";

export type CalloutTone = "information" | "warning" | "critical";

export interface CalloutProps {
  title: string;
  children: ReactNode;
  tone?: CalloutTone;
}

export function Callout({ title, children, tone = "information" }: CalloutProps) {
  const role = tone === "critical" ? "alert" : "note";
  return (
    <div className={`callout callout--${tone}`} role={role}>
      <span className="callout__icon" aria-hidden="true">{tone === "critical" ? "!" : "i"}</span>
      <div><strong className="callout__title">{title}</strong><div className="callout__body">{children}</div></div>
    </div>
  );
}

export function LoadingProgress({ label }: { label?: string }) {
  const { t } = useTranslation("common");
  return (
    <div className="loading" role="status" aria-live="polite">
      <span>{label ?? t("states.loading")}</span>
      <span className="loading__track" aria-hidden="true"><span className="loading__bar" /></span>
    </div>
  );
}

interface StateProps {
  title: string;
  description: string;
  action?: ReactNode;
}

export function EmptyState({ title, description, action }: StateProps) {
  return <div className="state-panel state-panel--empty"><div className="state-panel__symbol" aria-hidden="true">◇</div><h3>{title}</h3><p>{description}</p>{action}</div>;
}

export function UnavailableState({ title, description, action }: StateProps) {
  return <div className="state-panel state-panel--unavailable"><div className="state-panel__symbol" aria-hidden="true">—</div><h3>{title}</h3><p>{description}</p>{action}</div>;
}

export function InlineValidation({ children, ...props }: HTMLAttributes<HTMLParagraphElement>) {
  return <p className="inline-validation" role="alert" {...props}><span aria-hidden="true">!</span>{children}</p>;
}

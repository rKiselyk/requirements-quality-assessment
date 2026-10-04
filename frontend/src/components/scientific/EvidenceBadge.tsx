import type { ButtonHTMLAttributes } from "react";
import { useTranslation } from "react-i18next";

export interface EvidenceBadgeProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  evidenceId: string;
  kind: string;
  sourceText?: string;
}

export function EvidenceBadge({ evidenceId, kind, sourceText, className = "", ...props }: EvidenceBadgeProps) {
  const { t } = useTranslation("common");
  const sourceSuffix = sourceText ? t("evidence.sourceSuffix", { sourceText }) : "";
  const label = t("evidence.accessibleLabel", { kind, evidenceId, sourceSuffix });
  return <button type="button" className={`evidence-badge ${className}`.trim()} aria-label={label} {...props}><span aria-hidden="true">⌁</span>{kind}<code>{evidenceId}</code></button>;
}

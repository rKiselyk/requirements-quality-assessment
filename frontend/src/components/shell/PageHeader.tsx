import type { ReactNode } from "react";

export function PageHeader({ title, subtitle, metadata, actions }: { title: string; subtitle?: string; metadata?: ReactNode; actions?: ReactNode }) {
  return (
    <div className="page-header">
      <div><h1>{title}</h1>{subtitle ? <p>{subtitle}</p> : null}{metadata ? <div className="page-header__metadata">{metadata}</div> : null}</div>
      {actions ? <div className="page-header__actions">{actions}</div> : null}
    </div>
  );
}

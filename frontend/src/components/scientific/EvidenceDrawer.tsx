import { useEffect, useRef } from "react";

export interface EvidenceDrawerRecord {
  evidenceId: string;
  requirementId: string;
  featureId: string;
  text: string;
  startOffset: number;
  endOffset: number;
  ruleId: string;
}

export interface EvidenceDrawerLabels {
  heading: string;
  close: string;
  requirement: string;
  sourceLine: string;
  feature: string;
  exactText: string;
  startOffset: string;
  endOffset: string;
  rule: string;
  linkedFindings: string;
}

export function EvidenceDrawer({
  evidence,
  sourceLine,
  linkedFindingIds,
  labels,
  onClose,
}: {
  evidence: EvidenceDrawerRecord | null;
  sourceLine: number | null;
  linkedFindingIds: readonly string[];
  labels: EvidenceDrawerLabels;
  onClose: () => void;
}) {
  const closeButton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!evidence) return;
    closeButton.current?.focus();
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => document.removeEventListener("keydown", closeOnEscape);
  }, [evidence, onClose]);

  if (!evidence) return null;
  return (
    <div className="evidence-drawer-layer">
      <div className="evidence-drawer__backdrop" aria-hidden="true" onMouseDown={onClose} />
      <aside className="evidence-drawer" role="dialog" aria-modal="true" aria-labelledby="evidence-drawer-heading">
        <header className="evidence-drawer__header">
          <div>
            <span className="primitive-label">{labels.heading}</span>
            <h2 id="evidence-drawer-heading"><code>{evidence.evidenceId}</code></h2>
          </div>
          <button ref={closeButton} className="icon-button" type="button" aria-label={labels.close} onClick={onClose}>×</button>
        </header>
        <div className="evidence-drawer__body">
          <dl className="evidence-metadata">
            <div><dt>{labels.requirement}</dt><dd><code>{evidence.requirementId}</code></dd></div>
            {sourceLine !== null ? <div><dt>{labels.sourceLine}</dt><dd>{sourceLine}</dd></div> : null}
            <div><dt>{labels.feature}</dt><dd><code>{evidence.featureId}</code></dd></div>
            <div><dt>{labels.startOffset}</dt><dd>{evidence.startOffset}</dd></div>
            <div><dt>{labels.endOffset}</dt><dd>{evidence.endOffset}</dd></div>
            <div><dt>{labels.rule}</dt><dd><code>{evidence.ruleId}</code></dd></div>
          </dl>
          <section>
            <h3>{labels.exactText}</h3>
            <blockquote className="evidence-drawer__quote">{evidence.text}</blockquote>
          </section>
          {linkedFindingIds.length ? (
            <section>
              <h3>{labels.linkedFindings}</h3>
              <ul className="technical-code-list">{linkedFindingIds.map((id) => <li key={id}><code>{id}</code></li>)}</ul>
            </section>
          ) : null}
        </div>
      </aside>
    </div>
  );
}

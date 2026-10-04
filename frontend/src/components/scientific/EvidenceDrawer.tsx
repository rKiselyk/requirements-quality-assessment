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

export interface EvidenceDrawerFinding {
  findingId: string;
  characteristicId: string;
  kind: string;
  code: string;
  ruleId: string;
  explanation: string;
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
  findingKind: string;
  findingCode: string;
  findingRule: string;
  findingCharacteristic: string;
  findingExplanation: string;
}

export function EvidenceDrawer({
  evidence,
  sourceLine,
  linkedFindings,
  labels,
  onClose,
}: {
  evidence: EvidenceDrawerRecord | null;
  sourceLine: number | null;
  linkedFindings: readonly EvidenceDrawerFinding[];
  labels: EvidenceDrawerLabels;
  onClose: () => void;
}) {
  const closeButton = useRef<HTMLButtonElement>(null);
  const drawer = useRef<HTMLElement>(null);

  useEffect(() => {
    if (!evidence) return;
    closeButton.current?.focus();
    const containFocus = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
        return;
      }
      if (event.key !== "Tab" || !drawer.current) return;
      const focusable = Array.from(drawer.current.querySelectorAll<HTMLElement>(
        "button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex='-1'])",
      )).filter((item) => item.getAttribute("aria-hidden") !== "true");
      if (!focusable.length) {
        event.preventDefault();
        drawer.current.focus();
        return;
      }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      const active = document.activeElement;
      if (event.shiftKey && (active === first || !drawer.current.contains(active))) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && (active === last || !drawer.current.contains(active))) {
        event.preventDefault();
        first.focus();
      }
    };
    document.addEventListener("keydown", containFocus);
    return () => document.removeEventListener("keydown", containFocus);
  }, [evidence, onClose]);

  if (!evidence) return null;
  return (
    <div className="evidence-drawer-layer">
      <div className="evidence-drawer__backdrop" aria-hidden="true" onMouseDown={onClose} />
      <aside ref={drawer} className="evidence-drawer" role="dialog" aria-modal="true" aria-labelledby="evidence-drawer-heading" tabIndex={-1}>
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
          {linkedFindings.length ? (
            <section className="evidence-drawer__findings">
              <h3>{labels.linkedFindings}</h3>
              <ul>{linkedFindings.map((finding) => (
                <li key={finding.findingId}>
                  <h4><code>{finding.findingId}</code></h4>
                  <dl className="compact-metadata">
                    <div><dt>{labels.findingKind}</dt><dd><code>{finding.kind}</code></dd></div>
                    <div><dt>{labels.findingCode}</dt><dd><code>{finding.code}</code></dd></div>
                    <div><dt>{labels.findingRule}</dt><dd><code>{finding.ruleId}</code></dd></div>
                    <div><dt>{labels.findingCharacteristic}</dt><dd><code>{finding.characteristicId}</code></dd></div>
                    <div><dt>{labels.findingExplanation}</dt><dd>{finding.explanation}</dd></div>
                  </dl>
                </li>
              ))}</ul>
            </section>
          ) : null}
        </div>
      </aside>
    </div>
  );
}

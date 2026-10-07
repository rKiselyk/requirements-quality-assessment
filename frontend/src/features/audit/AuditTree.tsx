import { EvidenceBadge, ExactValue } from "../../components/scientific";
import type { AuditEvidenceIndex, AuditEvidenceTarget } from "./evidenceIndex";
import { isCanonicalFraction, isPlainRecord } from "./tree";

export interface AuditTreeLabels {
  array: string;
  object: string;
  fields: string;
  items: string;
  canonicalField: string;
  value: string;
  nullValue: string;
  emptyString: string;
  unsupported: string;
  openEvidence: string;
  fieldLabel: (key: string) => string;
}

interface AuditTreeProps {
  value: unknown;
  path: string;
  labels: AuditTreeLabels;
  evidenceIndex: AuditEvidenceIndex;
  onOpenEvidence: (target: AuditEvidenceTarget, trigger: HTMLButtonElement) => void;
}

function safeUnsupportedText(value: unknown, fallback: string): string {
  try {
    if (typeof value === "symbol") return value.description ? `Symbol(${value.description})` : "Symbol()";
    if (typeof value === "bigint") return `${value.toString()}n`;
    if (typeof value === "function") return `[function ${value.name || "anonymous"}]`;
    if (typeof value === "undefined") return "undefined";
  } catch {
    return fallback;
  }
  return fallback;
}

function childPath(path: string, key: string, isIndex: boolean) {
  return isIndex ? `${path}${key}` : `${path}.${key}`;
}

function ValueType({ children }: { children: string }) {
  return <span className="audit-node__type">{children}</span>;
}

function OpenEvidence({ target, labels, onOpenEvidence }: {
  target: AuditEvidenceTarget;
  labels: AuditTreeLabels;
  onOpenEvidence: AuditTreeProps["onOpenEvidence"];
}) {
  return (
    <EvidenceBadge
      className="audit-evidence-action"
      evidenceId={target.evidence.evidenceId}
      kind={labels.openEvidence}
      sourceText={target.evidence.text}
      onClick={(event) => onOpenEvidence(target, event.currentTarget)}
    />
  );
}

function AuditTreeNode({
  value,
  fieldKey,
  presentationKey,
  path,
  semanticKey,
  labels,
  evidenceIndex,
  onOpenEvidence,
  ancestors,
}: {
  value: unknown;
  fieldKey: string;
  presentationKey: string;
  path: string;
  semanticKey: string;
  labels: AuditTreeLabels;
  evidenceIndex: AuditEvidenceIndex;
  onOpenEvidence: AuditTreeProps["onOpenEvidence"];
  ancestors: ReadonlySet<object>;
}) {
  const friendlyLabel = presentationKey.startsWith("[") ? presentationKey : labels.fieldLabel(fieldKey);
  const referenceTarget = evidenceIndex.resolve(value, semanticKey);
  const isArray = Array.isArray(value);
  const structured = isArray || isPlainRecord(value);

  if (structured) {
    if (ancestors.has(value)) {
      return (
        <div className="audit-node audit-node--leaf audit-node--unsupported" data-audit-path={path}>
          <span className="audit-node__label">{friendlyLabel}</span>
          <code className="audit-node__key">{presentationKey}</code>
          <ValueType>{labels.unsupported}</ValueType>
          <code className="audit-node__value">{labels.unsupported}</code>
        </div>
      );
    }
    const entries = isArray ? value.map((item, index) => [`[${index}]`, item] as const) : Object.entries(value);
    const fraction = isCanonicalFraction(value) ? value : null;
    const nextAncestors = new Set(ancestors);
    nextAncestors.add(value);
    return (
      <details className="audit-node audit-node--branch" data-audit-path={path}>
        <summary aria-label={`${friendlyLabel}, ${path}`}>
          <span className="audit-node__label">{friendlyLabel}</span>
          <code className="audit-node__key" title={`${labels.canonicalField}: ${fieldKey}`}>{presentationKey}</code>
          <ValueType>{isArray ? labels.array : labels.object}</ValueType>
          <span className="audit-node__count">{entries.length} {isArray ? labels.items : labels.fields}</span>
          {fraction ? <ExactValue compact value={{ numerator: String(fraction.numerator), denominator: String(fraction.denominator) }} /> : null}
        </summary>
        <div className="audit-node__children">
          {referenceTarget ? <OpenEvidence target={referenceTarget} labels={labels} onOpenEvidence={onOpenEvidence} /> : null}
          {entries.map(([key, child], index) => {
            const item = isArray;
            return (
              <AuditTreeNode
                key={`${path}-${key}-${index}`}
                value={child}
                fieldKey={key}
                presentationKey={key}
                path={childPath(path, key, item)}
                semanticKey={item ? semanticKey : key}
                labels={labels}
                evidenceIndex={evidenceIndex}
                onOpenEvidence={onOpenEvidence}
                ancestors={nextAncestors}
              />
            );
          })}
        </div>
      </details>
    );
  }

  let type: string = typeof value;
  let rendered: string;
  if (value === null) {
    type = "null";
    rendered = labels.nullValue;
  } else if (typeof value === "string") {
    rendered = value.length ? value : labels.emptyString;
  } else if (typeof value === "number" || typeof value === "boolean") {
    rendered = String(value);
  } else {
    type = labels.unsupported;
    rendered = safeUnsupportedText(value, labels.unsupported);
  }
  return (
    <div className={`audit-node audit-node--leaf${type === labels.unsupported ? " audit-node--unsupported" : ""}`} data-audit-path={path}>
      <span className="audit-node__label">{friendlyLabel}</span>
      <code className="audit-node__key" title={`${labels.canonicalField}: ${fieldKey}`}>{presentationKey}</code>
      <ValueType>{type}</ValueType>
      <code className="audit-node__value" aria-label={`${labels.value}: ${rendered}`}>{rendered}</code>
      {referenceTarget ? <OpenEvidence target={referenceTarget} labels={labels} onOpenEvidence={onOpenEvidence} /> : null}
    </div>
  );
}

export function AuditTree({ value, path, labels, evidenceIndex, onOpenEvidence }: AuditTreeProps) {
  if (Array.isArray(value)) {
    return (
      <div className="audit-tree">
        {value.map((item, index) => (
          <AuditTreeNode key={`${path}-${index}`} value={item} fieldKey={`[${index}]`} presentationKey={`[${index}]`} path={`${path}[${index}]`} semanticKey="" labels={labels} evidenceIndex={evidenceIndex} onOpenEvidence={onOpenEvidence} ancestors={new Set()} />
        ))}
      </div>
    );
  }
  if (isPlainRecord(value)) {
    return (
      <div className="audit-tree">
        {Object.entries(value).map(([key, item], index) => (
          <AuditTreeNode key={`${path}-${key}-${index}`} value={item} fieldKey={key} presentationKey={key} path={`${path}.${key}`} semanticKey={key} labels={labels} evidenceIndex={evidenceIndex} onOpenEvidence={onOpenEvidence} ancestors={new Set()} />
        ))}
      </div>
    );
  }
  return (
    <div className="audit-tree">
      <AuditTreeNode value={value} fieldKey={path.split(".").at(-1) ?? path} presentationKey={path.split(".").at(-1) ?? path} path={path} semanticKey={path.split(".").at(-1) ?? path} labels={labels} evidenceIndex={evidenceIndex} onOpenEvidence={onOpenEvidence} ancestors={new Set()} />
    </div>
  );
}

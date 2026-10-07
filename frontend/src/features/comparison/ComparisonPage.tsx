import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { Callout, Card } from "../../components/ui";
import { PageHeader } from "../../components/shell";
import { BeforeAfterComparison } from "./BeforeAfterComparison";
import { selectComparisonProjection } from "./projection";

function technical(value: unknown) {
  if (value === null || value === undefined) return "—";
  return typeof value === "string" ? value : JSON.stringify(value);
}

function TechnicalList({ values }: { values: readonly unknown[] }) {
  return values.length ? <ol className="technical-code-list">{values.map((value, index) => <li key={index}><code>{technical(value)}</code></li>)}</ol> : <span>—</span>;
}

export function ComparisonPage({ result }: { result: CanonicalAnalyzeResponse }) {
  const { t } = useTranslation("comparison");
  const projection = useMemo(() => selectComparisonProjection(result), [result]);
  if (!projection) return null;
  return <section className="lifecycle-page comparison-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} />
    <Card title={t("artifactIdentity")}><div className="before-after">
      <section><h3>{t("before")}</h3><code>{technical(projection.lifecycle.parentArtifactRef)}</code></section>
      <section><h3>{t("after")}</h3><code>{technical(projection.lifecycle.childArtifactRef)}</code></section>
    </div></Card>

    <section className="lifecycle-section" aria-labelledby="comparison-records"><h2 id="comparison-records">{t("records.title")}</h2>
      <div className="comparison-records">{projection.comparisons.map((item, index) => <Card key={`${item.comparisonId}-${index}`} className="comparison-record">
        <div className="comparison-record__heading"><div><span>{t("records.resultFamily")}</span><code>{item.family}</code><span>{t("records.metric")}</span><code>{item.metricOrCharacteristicId}</code></div><code className="comparison-kind">{item.kind ?? item.status}</code></div>
        <BeforeAfterComparison before={item.before} after={item.after} />
        <dl className="lifecycle-metadata">
          <div><dt>{t("records.identity")}</dt><dd><code>{item.comparisonId} / {item.comparisonVersion}</code></dd></div>
          <div><dt>{t("records.status")}</dt><dd><code>{item.status}</code></dd></div>
          <div><dt>{t("records.kind")}</dt><dd><code>{item.kind ?? "—"}</code></dd></div>
          <div><dt>{t("records.beforeRef")}</dt><dd><code>{technical(item.beforeResultRef)}</code></dd></div>
          <div><dt>{t("records.afterRef")}</dt><dd><code>{technical(item.afterResultRef)}</code></dd></div>
          <div><dt>{t("records.rule")}</dt><dd><code>{technical(item.ruleRef)}</code></dd></div>
          <div><dt>{t("records.calibration")}</dt><dd><code>{item.calibrationStatus ?? "—"}</code></dd></div>
        </dl>
        <p>{item.explanation}</p>
        <div className="comparison-detail-grid">
          <section><h4>{t("records.reasons")}</h4><TechnicalList values={item.reasonCodes} /></section>
          <section><h4>{t("records.claims")}</h4><TechnicalList values={item.claims} /></section>
          <section><h4>{t("records.nonClaims")}</h4><TechnicalList values={item.nonClaims} /></section>
          <section><h4>{t("records.compatibility")}</h4><TechnicalList values={item.compatibilityDeclarationRefs} /></section>
        </div>
        <details><summary>{t("records.technical")}</summary>
          <h4>{t("records.subject")}</h4><pre className="technical-json">{technical(item.subject)}</pre>
          <h4>{t("records.parameters")}</h4><pre className="technical-json">{technical(item.parameterSetRefs)}</pre>
          <h4>{t("records.provenance")}</h4><pre className="technical-json">{technical(item.provenance)}</pre>
        </details>
      </Card>)}</div>
    </section>
    <Callout title={t("limitation.title")}><p>{t("limitation.structured")}</p><p>{t("limitation.direction")}</p><p>{t("limitation.causality")}</p><p>{t("limitation.action")}</p></Callout>
  </section>;
}

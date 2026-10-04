import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { ExactValue, StatusBadge } from "../../components/scientific";
import { PageHeader } from "../../components/shell";
import { Callout, Card, MetricCard, UnavailableState } from "../../components/ui";
import { limitationCodes, limitationTranslationKey, type LimitationCode } from "../../i18n";
import { ModelPipeline } from "./ModelPipeline";
import {
  selectCorrectiveAction,
  selectProcess,
  selectProductQuality,
  selectQbConsistency,
  selectRisk,
  selectSectionAvailability,
  selectSnapshotId,
  selectSpecificationMetrics,
  type MetricProjection,
  type ScientificRecordProjection,
} from "./projection";

function knownLimitation(code: unknown): code is LimitationCode {
  return typeof code === "string" && limitationCodes.some((item) => item === code);
}

function Metric({ label, metric }: { label: string; metric: MetricProjection | null }) {
  const { t } = useTranslation("overview");
  if (!metric) return <MetricCard label={label} value={null} status="UNAVAILABLE" detail={t("malformedProjection")} />;
  const detail = metric.computedCount === null
    ? undefined
    : t("metrics.counts", {
        computed: metric.computedCount,
        unknown: metric.unknownCount ?? "—",
        notApplicable: metric.notApplicableCount ?? "—",
        total: metric.totalCount ?? "—",
      });
  return <MetricCard label={label} value={metric.value} status={metric.state} detail={detail} />;
}

const availabilityReasonCodes = new Set([
  "EXTERNAL_EVIDENCE_NOT_SUPPLIED",
  "CONFIRMED_PROBLEM_AND_RISK_INPUTS_NOT_AVAILABLE",
  "CONFIRMED_PROBLEM_NOT_AVAILABLE",
  "FULL_MODEL_LIFECYCLE_NOT_INVOKED",
  "INITIAL_ASSESSMENT_HAS_NO_REASSESSMENT",
  "INITIAL_ASSESSMENT_HAS_NO_COMPARISON",
  "REASSESSMENT_NOT_PRODUCED",
  "COMPARISONS_NOT_PRODUCED",
]);

function reasonText(reasonCode: string | null, t: (key: string, options?: Record<string, unknown>) => string) {
  if (!reasonCode) return t("availability.missingReason");
  return availabilityReasonCodes.has(reasonCode)
    ? t(`availability.reasons.${reasonCode}`)
    : t("availability.unknownReason", { code: reasonCode });
}

function SectionUnavailable({ section, result }: { section: string; result: CanonicalAnalyzeResponse }) {
  const { t } = useTranslation("overview");
  const availability = selectSectionAvailability(result, section);
  return (
    <UnavailableState
      title={t("availability.title")}
      description={availability?.availability === "UNAVAILABLE"
        ? reasonText(availability.reasonCode, t)
        : t("malformedProjection")}
      action={availability?.reasonCode ? <code>{availability.reasonCode}</code> : undefined}
    />
  );
}

function RecordItem({ label, item }: { label: string; item: ScientificRecordProjection | null }) {
  const { t } = useTranslation("overview");
  return (
    <div className="record-item">
      <h3>{label}</h3>
      {item ? (
        <>
          <div className="record-item__states">
            {item.status ? <StatusBadge code={item.status} /> : null}
            {item.applicability ? <StatusBadge code={item.applicability} /> : null}
          </div>
          {item.value ? <ExactValue value={item.value} /> : <span className="record-item__no-value">{t("noCanonicalValue")}</span>}
          {item.kind ? <code>{item.kind}</code> : null}
          {item.reasonCodes.map((code) => <code key={code}>{code}</code>)}
        </>
      ) : <UnavailableState title={t("availability.title")} description={t("malformedProjection")} />}
    </div>
  );
}

function isAvailable(result: CanonicalAnalyzeResponse, section: string) {
  return selectSectionAvailability(result, section)?.availability === "AVAILABLE";
}

export function OverviewPage({ result }: { result: CanonicalAnalyzeResponse }) {
  const { t } = useTranslation("overview");
  const { t: limitationText } = useTranslation("limitations");
  const metrics = selectSpecificationMetrics(result);
  const qb = selectQbConsistency(result);
  const productQuality = selectProductQuality(result);
  const risk = selectRisk(result);
  const correctiveAction = selectCorrectiveAction(result);
  const process = selectProcess(result);
  const snapshotId = selectSnapshotId(result);

  return (
    <section className="overview-page">
      <PageHeader
        title={t("title")}
        subtitle={t("subtitle")}
        metadata={<>
          <span>{t("metadata.analysisCase")}: <code>{result.analysis_case}</code></span>
          <span>{t("metadata.contractVersion")}: <code>{result.contract_version}</code></span>
          {result.controlled_scenario ? <span>{t("metadata.scenario")}: <code>{String(result.controlled_scenario.id ?? "—")} / {String(result.controlled_scenario.version ?? "—")}</code></span> : null}
          {snapshotId ? <span>{t("metadata.snapshot")}: <code>{snapshotId}</code></span> : null}
        </>}
      />

      <Card className="requirement-count-card" title={t("requirements.title")}>
        <strong className="requirement-count">{result.requirements.length}</strong>
        <span>{t("requirements.count", { count: result.requirements.length })}</span>
      </Card>

      <section className="overview-section" aria-labelledby="requirement-quality-title">
        <h2 id="requirement-quality-title">{t("quality.title")}</h2>
        <div className="metric-grid">
          <Metric label={t("quality.completeness")} metric={metrics.completeness} />
          <Metric label={t("quality.verifiability")} metric={metrics.verifiability} />
          <Metric label={t("quality.unambiguity")} metric={metrics.unambiguity} />
        </div>
      </section>

      <section className="overview-section" aria-labelledby="specification-title">
        <h2 id="specification-title">{t("specification.title")}</h2>
        <Card className="qb-card">
          <div><h3>{t("specification.qb")}</h3><p>{t("specification.qbDescription")}</p></div>
          {qb ? <><ExactValue value={qb.value} /><StatusBadge code={qb.state} /></> : <UnavailableState title={t("availability.title")} description={t("malformedProjection")} />}
        </Card>
      </section>

      <section className="overview-section" aria-labelledby="model-surface-title">
        <h2 id="model-surface-title">{t("surface.title")}</h2>
        <div className="model-surface-grid">
          <Card title={t("surface.productQuality")}>{isAvailable(result, "product_quality")
            ? <div className="record-grid"><RecordItem label={t("surface.observed")} item={productQuality.observed} /><RecordItem label={t("surface.predicted")} item={productQuality.predicted} /></div>
            : <SectionUnavailable section="product_quality" result={result} />}</Card>
          <Card title={t("surface.risk")}>{isAvailable(result, "risk")
            ? <div className="record-grid"><div><h3>{t("surface.categoricalRisk")}</h3>{risk.categorical.length ? risk.categorical.map((item, index) => <RecordItem key={index} label={t("surface.record", { number: index + 1 })} item={item} />) : <SectionUnavailable section="risk" result={result} />}</div><div><h3>{t("surface.quantitativeRisk")}</h3>{risk.quantitative.length ? risk.quantitative.map((item, index) => <RecordItem key={index} label={t("surface.record", { number: index + 1 })} item={item} />) : <SectionUnavailable section="risk" result={result} />}</div></div>
            : <SectionUnavailable section="risk" result={result} />}</Card>
          <Card title={t("surface.correctiveActions")}>{isAvailable(result, "corrective_actions")
            ? <RecordItem label={t("surface.resolution")} item={correctiveAction} />
            : <SectionUnavailable section="corrective_actions" result={result} />}</Card>
          <Card title={t("surface.process")}>{isAvailable(result, "process")
            ? <div className="process-summary">
                <h3>{t("surface.processStates")}</h3>
                {process.states.length ? process.states.map((state) => <p key={`${state.id}-${state.version}`}><code>{state.id}</code> <code>{state.version}</code> <StatusBadge code={state.stage} /></p>) : <p>{t("malformedProjection")}</p>}
                <h3>{t("surface.checkpoints", { count: process.checkpoints.length })}</h3>
                {process.checkpoints.map((checkpoint) => <p key={`${checkpoint.id}-${checkpoint.version}`}><code>{checkpoint.id}</code> <StatusBadge code={checkpoint.outcome} /> {checkpoint.reasonCodes.map((code) => <code key={code}>{code}</code>)}</p>)}
                <p className="scientific-boundary">{t("surface.checkpointBoundary")}</p>
              </div>
            : <SectionUnavailable section="process" result={result} />}</Card>
        </div>
      </section>

      <ModelPipeline result={result} />

      <section className="overview-limitations" aria-labelledby="limitations-title">
        <h2 id="limitations-title">{t("limitations.title")}</h2>
        {result.limitations.map((code, index) => {
          const canonicalCode = typeof code === "string" ? code : null;
          const explanation = knownLimitation(code) ? limitationText(limitationTranslationKey(code)) : limitationText("unknown");
          return <Callout key={`${canonicalCode ?? "malformed"}-${index}`} title={canonicalCode ?? t("limitations.malformed")}><p>{explanation}</p></Callout>;
        })}
      </section>
    </section>
  );
}

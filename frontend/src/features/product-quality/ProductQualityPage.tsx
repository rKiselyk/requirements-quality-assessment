import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { ApplicabilityBadge, ExactValue, StatusBadge, type ExactValueData } from "../../components/scientific";
import { PageHeader } from "../../components/shell";
import { Button, Callout, Card, DataTable, UnavailableState } from "../../components/ui";
import {
  canonicalJson,
  selectProductQualityPage,
  type CriterionProjection,
  type FeatureProjection,
  type ObservationProjection,
} from "./projection";

function Malformed({ compact = false }: { compact?: boolean }) {
  const { t } = useTranslation("productQuality");
  return <p className={`malformed-record${compact ? " malformed-record--compact" : ""}`}>{t("malformed.record")}</p>;
}

function TechnicalDetails({ value, label }: { value: unknown; label?: string }) {
  const { t } = useTranslation("productQuality");
  return <details className="product-quality-technical"><summary>{label ?? t("technical.details")}</summary><pre>{canonicalJson(value)}</pre></details>;
}

function CodeList({ values, empty }: { values: readonly string[]; empty: string }) {
  return values.length ? <ul className="technical-code-list">{values.map((value, index) => <li key={`${value}-${index}`}><code>{value}</code></li>)}</ul> : <p className="empty-records">{empty}</p>;
}

function StatePair({ status, applicability }: { status: string; applicability: string }) {
  return <div className="product-quality-state"><StatusBadge code={status} /><ApplicabilityBadge code={applicability} /></div>;
}

function Metadata({ children }: { children: ReactNode }) {
  return <dl className="compact-metadata product-quality-metadata">{children}</dl>;
}

function MetadataItem({ label, value }: { label: string; value: ReactNode }) {
  return <div><dt>{label}</dt><dd>{value}</dd></div>;
}

function SelectedCriterion({ value, navigable, onSelectRequirement }: { value: CriterionProjection | null; navigable: boolean; onSelectRequirement: (id: string) => void }) {
  const { t } = useTranslation("productQuality");
  if (!value) return <Card title={t("criterion.title")}><Malformed /></Card>;
  return <Card title={t("criterion.title")} className="product-quality-record">
    <StatePair status={value.status} applicability={value.applicability} />
    {value.criterion ? <>
      <div className="product-quality-primary-row">
        <div><span className="primitive-label">{t("criterion.requirement")}</span><strong className="technical-primary">{value.requirementId}</strong></div>
        {value.requirementId && navigable ? <Button type="button" variant="quiet" onClick={() => onSelectRequirement(value.requirementId!)}>{t("criterion.openRequirement", { id: value.requirementId })}</Button> : null}
      </div>
      <div className="criterion-expression" aria-label={t("criterion.expressionLabel")}>
        <code>{value.metricId}</code><code>{value.comparator}</code><ExactValue value={value.bound} compact /><code>{value.unit}</code>
      </div>
      <Metadata>
        <MetadataItem label={t("criterion.inclusivity")} value={<code>{value.inclusivity}</code>} />
        <MetadataItem label={t("criterion.context")} value={<code>{value.contextIdentity}</code>} />
        <MetadataItem label={t("criterion.sourceObservation")} value={<TechnicalDetails value={value.sourceObservationRef} label={t("technical.reference")} />} />
        <MetadataItem label={t("criterion.bindingRule")} value={<TechnicalDetails value={value.bindingRuleRef} label={t("technical.reference")} />} />
      </Metadata>
    </> : <p className="scientific-boundary">{t("criterion.noValue")}</p>}
    {value.reasons.length ? <CodeList values={value.reasons} empty={t("technical.none")} /> : null}
    <TechnicalDetails value={value.raw} />
  </Card>;
}

function ObservationCard({ value }: { value: ObservationProjection | null }) {
  const { t } = useTranslation("productQuality");
  if (!value) return <Card title={t("observation.title")}><Malformed /></Card>;
  return <Card title={t("observation.title")} className="product-quality-record">
    <StatePair status={value.status} applicability={value.applicability} />
    {value.observation ? <>
      <div className="product-quality-exact"><span>{t("observation.observedValue")}</span><ExactValue value={value.observedValue} /><code>{value.unit}</code></div>
      <Metadata>
        <MetadataItem label={t("observation.metric")} value={<code>{value.metricId}</code>} />
        <MetadataItem label={t("observation.context")} value={<code>{value.contextIdentity}</code>} />
        <MetadataItem label={t("observation.sourceKind")} value={<code>{value.sourceKind}</code>} />
        <MetadataItem label={t("observation.sourceRecord")} value={<code>{value.sourceRecordRef}</code>} />
        <MetadataItem label={t("observation.product")} value={<TechnicalDetails value={value.productRef} label={t("technical.reference")} />} />
        <MetadataItem label={t("observation.environment")} value={<TechnicalDetails value={value.environmentRef} label={t("technical.reference")} />} />
        <MetadataItem label={t("observation.collection")} value={<TechnicalDetails value={value.collectionRef} label={t("technical.reference")} />} />
      </Metadata>
      {value.sourceKind === "DETERMINISTIC_FIXTURE" ? <p className="fixture-boundary">{t("observation.fixtureBoundary")}</p> : null}
    </> : <p className="scientific-boundary">{t("observation.noValue")}</p>}
    {value.reasons.length ? <CodeList values={value.reasons} empty={t("technical.none")} /> : null}
    <TechnicalDetails value={value.raw} />
  </Card>;
}

function ConformanceCard({ value }: { value: ReturnType<typeof selectProductQualityPage> extends infer _T ? import("./projection").ConformanceProjection | null : never }) {
  const { t } = useTranslation("productQuality");
  if (!value) return <Card title={t("conformance.title")}><Malformed /></Card>;
  return <Card title={t("conformance.title")} className="product-quality-record">
    <StatePair status={value.status} applicability={value.applicability} />
    {value.outcome ? <div className="conformance-outcome"><span>{t("conformance.outcome")}</span><code>{value.outcome}</code></div> : <p className="scientific-boundary">{t("conformance.noOutcome")}</p>}
    <p className="record-explanation">{value.explanation}</p>
    {value.reasons.length ? <CodeList values={value.reasons} empty={t("technical.none")} /> : null}
    <TechnicalDetails value={value.raw} />
  </Card>;
}

function fractionValue(value: unknown): ExactValueData | null {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return null;
  const candidate = value as Record<string, unknown>;
  return typeof candidate.numerator === "number" && Number.isSafeInteger(candidate.numerator)
    && typeof candidate.denominator === "number" && Number.isSafeInteger(candidate.denominator) && candidate.denominator !== 0
    ? { numerator: String(candidate.numerator), denominator: String(candidate.denominator) }
    : null;
}

function FeatureTypedValue({ feature }: { feature: FeatureProjection }) {
  const { t } = useTranslation("productQuality");
  if (!feature.typedValue) return <span className="scientific-boundary">{t("features.noTypedValue")}</span>;
  const value = feature.typedValue;
  const decimal = [value.exact_decimal_bound, value.exact_decimal_value].find((item) => typeof item === "string") as string | undefined;
  const fraction = fractionValue(value.exact_fraction_or_none) ?? fractionValue(value.source_exact_fraction_or_none);
  const category = typeof value.outcome === "string" ? value.outcome : typeof value.gate_decision === "string" ? value.gate_decision : null;
  return <div className="feature-value">
    {decimal ? <ExactValue value={decimal} compact /> : fraction ? <ExactValue value={fraction} compact /> : category ? <code>{category}</code> : <code>{t("features.structuredValue")}</code>}
    <TechnicalDetails value={value} label={t("features.typedValueDetails")} />
  </div>;
}

function FeatureProfile({ value }: { value: import("./projection").FeatureProfileProjection | null }) {
  const { t } = useTranslation("productQuality");
  if (!value) return <section className="product-quality-section"><h2>{t("features.title")}</h2><Card><Malformed /></Card></section>;
  return <section className="product-quality-section" aria-labelledby="pe-profile-heading">
    <div className="section-heading-row"><div><h2 id="pe-profile-heading">{t("features.title")}</h2><p>{t("features.description")}</p></div><StatePair status={value.status} applicability={value.applicability} /></div>
    <Card className="feature-profile-card">
      <Metadata>
        <MetadataItem label={t("features.characteristic")} value={<code>{value.characteristicId}</code>} />
        <MetadataItem label={t("features.registry")} value={<TechnicalDetails value={value.registryRef} label={t("technical.reference")} />} />
        <MetadataItem label={t("features.mappingRule")} value={<TechnicalDetails value={value.mappingRuleRef} label={t("technical.reference")} />} />
        <MetadataItem label={t("features.processState")} value={<TechnicalDetails value={value.processStateRef} label={t("technical.reference")} />} />
      </Metadata>
      <DataTable
        caption={t("features.caption")}
        rows={value.features}
        rowKey={(feature) => feature.featureId}
        columns={[
          { key: "id", header: t("features.id"), render: (feature) => <code>{feature.featureId}</code> },
          { key: "effect", header: t("features.effect"), render: (feature) => <div><span>{t(`features.effects.${feature.effect}`)}</span><code className="block-code">{feature.effect}</code></div> },
          { key: "state", header: t("features.state"), render: (feature) => <StatePair status={feature.status} applicability={feature.applicability} /> },
          { key: "value", header: t("features.value"), render: (feature) => <FeatureTypedValue feature={feature} /> },
          { key: "availability", header: t("features.availabilityPoint"), render: (feature) => <div><code>{feature.availabilityPoint}</code>{feature.reasons.length ? <CodeList values={feature.reasons} empty={t("technical.none")} /> : null}<TechnicalDetails value={feature.raw} /></div> },
        ]}
      />
      <TechnicalDetails value={value.raw} label={t("features.profileDetails")} />
    </Card>
  </section>;
}

function ObservedSection({ value }: { value: import("./projection").ObservedProjection | null }) {
  const { t } = useTranslation("productQuality");
  return <section className="product-quality-section" aria-labelledby="observed-heading">
    <h2 id="observed-heading">{t("observed.title")}</h2>
    {!value ? <Card><Malformed /></Card> : <Card className="observed-quality-card product-quality-record">
      <StatePair status={value.status} applicability={value.applicability} />
      <div className="product-quality-result-heading"><div><span className="primitive-label">{t("observed.resultKind")}</span><code>{value.resultKind}</code></div><div><span className="primitive-label">{t("observed.exactValue")}</span><ExactValue value={value.observedValue} fallback={t("technical.noNumericValue")} /></div></div>
      <Metadata>
        <MetadataItem label={t("observed.characteristic")} value={<code>{value.characteristicId}</code>} />
        <MetadataItem label={t("observed.numericRepresentation")} value={<code>{value.numericRepresentation}</code>} />
        <MetadataItem label={t("observed.conformanceOutcome")} value={value.sourceConformanceOutcome ? <code>{value.sourceConformanceOutcome}</code> : <span>{t("technical.none")}</span>} />
        <MetadataItem label={t("observed.calibration")} value={<code>{value.calibrationStatus}</code>} />
      </Metadata>
      <p className="scope-statement">{value.scopeStatement}</p>
      <div className="null-scientific-fields"><span><code>prediction_value</code>: {t("technical.none")}</span><span><code>reliability</code>: {t("technical.none")}</span><span><code>uncertainty</code>: {t("technical.none")}</span></div>
      <details className="non-claims"><summary>{t("nonClaims.title")}</summary><ol>{value.nonClaims.map((claim) => <li key={claim}><code>{claim}</code><span>{t(`nonClaims.items.${claim}`)}</span></li>)}</ol></details>
      <TechnicalDetails value={value.raw} />
    </Card>}
  </section>;
}

function PredictionSection({ value, current }: { value: import("./projection").PredictionProjection | null; current: boolean }) {
  const { t } = useTranslation("productQuality");
  return <section className="product-quality-section" aria-labelledby="prediction-heading">
    <h2 id="prediction-heading">{t("prediction.title")}</h2>
    {!current ? <Card className="prediction-quality-card"><div className="neutral-note"><strong>{t("prediction.noCurrentTitle")}</strong><p>{t("prediction.noCurrentDescription")}</p></div></Card>
      : !value ? <Card className="prediction-quality-card"><Malformed /></Card>
      : <Card className="prediction-quality-card product-quality-record">
        <StatePair status={value.status} applicability={value.applicability} />
        <div className="product-quality-result-heading"><div><span className="primitive-label">{t("prediction.resultKind")}</span><code>{value.resultKind}</code></div><div><span className="primitive-label">{t("prediction.exactValue")}</span><ExactValue value={value.predictedValue} fallback={t("technical.noNumericValue")} /></div></div>
        <Metadata>
          <MetadataItem label={t("prediction.predictor")} value={<TechnicalDetails value={value.predictorRef} label={t("technical.reference")} />} />
          <MetadataItem label={t("prediction.parameterSet")} value={<TechnicalDetails value={value.parameterSetRef} label={t("technical.reference")} />} />
          <MetadataItem label={t("prediction.calibration")} value={<code>{value.calibrationStatus}</code>} />
          <MetadataItem label={t("prediction.numericRepresentation")} value={<code>{value.numericRepresentation}</code>} />
        </Metadata>
        {value.withheldReason ? <div className="withheld-reason"><span>{t("prediction.withheldReason")}</span><code>{value.withheldReason}</code></div> : null}
        <p className="record-explanation">{value.explanation}</p>
        <p className="fixture-boundary">{t("prediction.calibrationBoundary")}</p>
        <TechnicalDetails value={value.raw} />
      </Card>}
  </section>;
}

export function ProductQualityPage({ result, onSelectRequirement }: { result: CanonicalAnalyzeResponse; onSelectRequirement: (requirementId: string) => void }) {
  const { t, i18n } = useTranslation("productQuality");
  const projection = selectProductQualityPage(result);
  const requirementIds = new Set(result.requirements.flatMap((item) => {
    const requirement = typeof item === "object" && item !== null && !Array.isArray(item) ? (item as Record<string, unknown>).requirement : null;
    const id = typeof requirement === "object" && requirement !== null && !Array.isArray(requirement) ? (requirement as Record<string, unknown>).id : null;
    return typeof id === "string" ? [id] : [];
  }));

  if (projection.kind === "UNAVAILABLE") {
    const reasonKey = `unavailable.reasons.${projection.reasonCode}`;
    return <section className="product-quality-page"><PageHeader title={t("title")} subtitle={t("subtitle")} /><UnavailableState title={t("unavailable.title")} description={i18n.exists(reasonKey, { ns: "productQuality" }) ? t(reasonKey) : t("unavailable.unknownReason")} action={<div className="availability-reason"><span>{t("unavailable.reasonCode")}</span><code>{projection.reasonCode}</code><p>{t("unavailable.noValue")}</p></div>} /></section>;
  }
  if (projection.kind === "MALFORMED") {
    return <section className="product-quality-page"><PageHeader title={t("title")} subtitle={t("subtitle")} /><UnavailableState title={t("malformed.title")} description={t("malformed.description")} /></section>;
  }

  return <section className="product-quality-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} metadata={<code>{t(`revision.${projection.revision}`)}</code>} />
    <SelectedCriterion value={projection.criterion} navigable={Boolean(projection.criterion?.requirementId && requirementIds.has(projection.criterion.requirementId))} onSelectRequirement={onSelectRequirement} />
    <section className="product-quality-section" aria-labelledby="observation-conformance-heading"><h2 id="observation-conformance-heading">{t("observationConformance.title")}</h2><div className="observation-conformance-grid"><ObservationCard value={projection.observation} /><ConformanceCard value={projection.conformance} /></div></section>
    <FeatureProfile value={projection.featureProfile} />
    <ObservedSection value={projection.observed} />
    <PredictionSection value={projection.prediction} current={projection.predictionCurrent} />
    <section className="product-quality-section product-quality-limitations" aria-labelledby="product-quality-limitations-heading">
      <h2 id="product-quality-limitations-heading">{t("limitations.title")}</h2>
      <Callout title={t("limitations.observedPredictedTitle")}><p>{t("limitations.observedPredicted")}</p><p>{t("limitations.bounded")}</p><p>{t("limitations.prediction")}</p></Callout>
    </section>
  </section>;
}

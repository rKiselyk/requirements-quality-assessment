import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { ApplicabilityBadge, ExactValue, StatusBadge } from "../../components/scientific";
import { PageHeader } from "../../components/shell";
import { Button, Callout, Card, UnavailableState } from "../../components/ui";
import { selectRequirements } from "../requirements/projection";
import {
  canonicalJson,
  selectRiskPage,
  type CategoricalRiskProjection,
  type PopulationProjection,
  type ProjectedRecord,
  type QuantitativeRiskProjection,
  type RelationProjection,
  type ResolutionProjection,
} from "./projection";

function Malformed() {
  const { t } = useTranslation("risk");
  return <p className="malformed-record">{t("malformed.record")}</p>;
}

function TechnicalDetails({ value, label }: { value: unknown; label?: string }) {
  const { t } = useTranslation("risk");
  return <details className="product-quality-technical"><summary>{label ?? t("technical.details")}</summary><pre>{canonicalJson(value)}</pre></details>;
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

function NonClaims({ values, family }: { values: string[]; family: "problem" | "relation" | "categorical" | "quantitative" }) {
  const { t, i18n } = useTranslation("risk");
  return <details className="non-claims"><summary>{t("nonClaims.title")}</summary><ol>{values.map((code) => {
    const key = `nonClaims.${family}.${code}`;
    return <li key={code}><code>{code}</code><span>{i18n.exists(key, { ns: "risk" }) ? t(key) : t("nonClaims.canonical")}</span></li>;
  })}</ol></details>;
}

function ResolutionCard({ entry, validRequirements, onSelectRequirement, index }: {
  entry: ProjectedRecord<ResolutionProjection>;
  validRequirements: Set<string>;
  onSelectRequirement: (requirementId: string) => void;
  index: number;
}) {
  const { t } = useTranslation("risk");
  if (entry.kind === "MALFORMED") return <Card title={t("resolutions.item", { index: index + 1 })}><Malformed /><TechnicalDetails value={entry.raw} /></Card>;
  const resolution = entry.value;
  return <Card title={t("resolutions.item", { index: index + 1 })} className="risk-record">
    <StatePair status={resolution.status} applicability={resolution.applicability} />
    <Metadata>
      <MetadataItem label={t("resolutions.disposition")} value={resolution.disposition ? <code>{resolution.disposition}</code> : <span>{t("technical.none")}</span>} />
      <MetadataItem label={t("resolutions.reason")} value={<code>{resolution.reason}</code>} />
      <MetadataItem label={t("resolutions.sourceClaim")} value={<TechnicalDetails value={resolution.sourceClaimRef} label={t("technical.reference")} />} />
      <MetadataItem label={t("resolutions.identity")} value={<TechnicalDetails value={resolution.resolutionId} label={t("technical.reference")} />} />
    </Metadata>
    <p className="record-explanation">{resolution.explanation}</p>
    {resolution.problem ? <section className="confirmed-problem" aria-label={t("problem.title")}>
      <h3>{t("problem.title")}</h3>
      <StatePair status={resolution.problem.status} applicability={resolution.problem.applicability} />
      <div className="risk-code-grid">
        <div><span>{t("problem.kind")}</span><code>{resolution.problem.problemKind}</code></div>
        <div><span>{t("problem.defectType")}</span><code>{resolution.problem.defectType}</code></div>
        <div><span>{t("problem.conflictClass")}</span><code>{resolution.problem.conflictClass}</code></div>
        <div><span>{t("problem.conflictSubtype")}</span><code>{resolution.problem.conflictSubtype}</code></div>
      </div>
      <h4>{t("problem.participants")}</h4>
      <div className="participant-links">{resolution.problem.participantRefs.map((participant, participantIndex) => {
        const requirementId = typeof participant.requirement_id === "string" ? participant.requirement_id : null;
        return requirementId && validRequirements.has(requirementId)
          ? <Button key={participantIndex} type="button" variant="quiet" onClick={() => onSelectRequirement(requirementId)}>{t("problem.openRequirement", { id: requirementId })}</Button>
          : <code key={participantIndex}>{canonicalJson(participant)}</code>;
      })}</div>
      <p className="record-explanation">{resolution.problem.explanation}</p>
      <NonClaims values={resolution.problem.nonClaims} family="problem" />
      <TechnicalDetails value={resolution.problem.raw} label={t("problem.trace")} />
    </section> : <p className="scientific-boundary">{t("problem.noConfirmedBoundary")}</p>}
    <TechnicalDetails value={resolution.raw} />
  </Card>;
}

function PopulationCard({ entry }: { entry: ProjectedRecord<PopulationProjection> }) {
  const { t } = useTranslation("risk");
  if (entry.kind === "MALFORMED") return <Card title={t("population.title")}><Malformed /><TechnicalDetails value={entry.raw} /></Card>;
  const value = entry.value;
  return <Card title={t("population.title")} description={t("population.description")} className="risk-record risk-population">
    <StatePair status={value.status} applicability={value.applicability} />
    <div className="risk-summary-row">
      <div><span>{t("population.members")}</span><strong>{value.members.length}</strong></div>
      <div><span>{t("population.complete")}</span><code>{String(value.populationComplete)}</code></div>
      <div><span>{t("population.unresolved")}</span><strong>{value.unresolvedResolutionRefs.length}</strong></div>
    </div>
    <p className="scientific-boundary">{t("population.boundary")}</p>
    <TechnicalDetails value={value.raw} />
  </Card>;
}

function RelationCard({ entry, index }: { entry: ProjectedRecord<RelationProjection>; index: number }) {
  const { t } = useTranslation("risk");
  if (entry.kind === "MALFORMED") return <Card title={t("relation.item", { index: index + 1 })}><Malformed /><TechnicalDetails value={entry.raw} /></Card>;
  const value = entry.value;
  return <Card title={t("relation.item", { index: index + 1 })} className="risk-record risk-relation">
    <StatePair status={value.status} applicability={value.applicability} />
    <Metadata>
      <MetadataItem label={t("relation.kind")} value={value.relationKind ? <code>{value.relationKind}</code> : <span>{t("technical.none")}</span>} />
      <MetadataItem label={t("relation.characteristic")} value={<code>{value.characteristicId}</code>} />
      <MetadataItem label={t("relation.reason")} value={<code>{value.reason}</code>} />
      <MetadataItem label={t("relation.calibration")} value={<code>{value.calibrationStatus}</code>} />
    </Metadata>
    <p className="record-explanation">{value.rationale}</p>
    <p className="fixture-boundary">{t("relation.calibrationBoundary")}</p>
    <NonClaims values={value.nonClaims} family="relation" />
    <TechnicalDetails value={value.raw} />
  </Card>;
}

function CategoricalCard({ entry, index }: { entry: ProjectedRecord<CategoricalRiskProjection>; index: number }) {
  const { t } = useTranslation("risk");
  if (entry.kind === "MALFORMED") return <Card><Malformed /><TechnicalDetails value={entry.raw} /></Card>;
  const value = entry.value;
  return <Card className="risk-record categorical-risk-card" aria-label={t("categorical.item", { index: index + 1 })}>
    <StatePair status={value.status} applicability={value.applicability} />
    <div className="risk-result-heading">
      <div><span>{t("categorical.classification")}</span>{value.classification ? <StatusBadge code={value.classification} /> : <span>{t("technical.none")}</span>}</div>
      <div><span>{t("categorical.characteristic")}</span><code>{value.characteristicId}</code></div>
    </div>
    <p className="risk-statement">{value.riskStatement}</p>
    <details className="product-quality-technical categorical-explanation"><summary>{t("categorical.explanation")}</summary><p className="record-explanation">{value.explanation}</p></details>
    <Metadata>
      <MetadataItem label={t("categorical.calibration")} value={<code>{value.calibrationStatus}</code>} />
      <MetadataItem label={t("categorical.productQualityContext")} value={<TechnicalDetails value={value.productQualityContext} label={t("technical.reference")} />} />
      <MetadataItem label={t("categorical.event")} value={<TechnicalDetails value={value.assessmentEventRef} label={t("technical.reference")} />} />
      <MetadataItem label={t("categorical.identity")} value={<TechnicalDetails value={value.riskAssessmentId} label={t("technical.reference")} />} />
    </Metadata>
    <NonClaims values={value.nonClaims} family="categorical" />
    <TechnicalDetails value={value.raw} />
  </Card>;
}

function QuantitativeCard({ entry, index }: { entry: ProjectedRecord<QuantitativeRiskProjection>; index: number }) {
  const { t } = useTranslation("risk");
  if (entry.kind === "MALFORMED") return <Card><Malformed /><TechnicalDetails value={entry.raw} /></Card>;
  const value = entry.value;
  return <Card className="risk-record quantitative-risk-card" aria-label={t("quantitative.item", { index: index + 1 })}>
    <div className="quantitative-heading"><div><span>{t("quantitative.resultKind")}</span><code>{value.resultKind}</code></div><StatusBadge code={value.state} /></div>
    <div className="local-risk-value"><span>{t("quantitative.localRisk")}</span><ExactValue value={value.localRisk} fallback={t("quantitative.noValue")} /></div>
    <Metadata>
      <MetadataItem label={t("quantitative.scope")} value={<code>{value.scope}</code>} />
      <MetadataItem label={t("quantitative.numericRepresentation")} value={<code>{value.numericRepresentation}</code>} />
      <MetadataItem label={t("quantitative.characteristic")} value={<code>{value.characteristicId}</code>} />
      <MetadataItem label={t("quantitative.calculationRuleRef")} value={<TechnicalDetails value={value.calculationRuleRef} label={t("technical.reference")} />} />
    </Metadata>
    <div className="operand-grid">{value.operands.map((operand) => <article className="operand-card" key={operand.kind}>
      <header><code>{operand.kind}</code><StatusBadge code={operand.state} /></header>
      <ExactValue value={operand.value} fallback={t("quantitative.noOperandValue")} compact />
      <span className="operand-calibration"><code>{operand.calibrationStatus}</code></span>
      <p>{operand.sourceOrRationale}</p>
      <TechnicalDetails value={operand.raw} label={t("quantitative.operandTrace")} />
    </article>)}</div>
    <p className="record-explanation">{value.explanation}</p>
    <details className="formula-trace"><summary>{t("quantitative.formulaTrace")}</summary><code>{value.calculationRule}</code><p>{t("quantitative.formulaBoundary")}</p></details>
    <NonClaims values={value.nonClaims} family="quantitative" />
    <TechnicalDetails value={value.raw} />
  </Card>;
}

export function RiskPage({ result, onSelectRequirement }: { result: CanonicalAnalyzeResponse; onSelectRequirement: (requirementId: string) => void }) {
  const { t, i18n } = useTranslation("risk");
  const projection = selectRiskPage(result);
  const validRequirements = new Set(selectRequirements(result).flatMap((entry) => entry.kind === "VALID" ? [entry.value.requirement.id] : []));
  if (projection.kind === "UNAVAILABLE") {
    const reasonKey = `unavailable.reasons.${projection.reasonCode}`;
    return <section className="risk-page"><PageHeader title={t("title")} subtitle={t("subtitle")} /><UnavailableState title={t("unavailable.title")} description={i18n.exists(reasonKey, { ns: "risk" }) ? t(reasonKey) : t("unavailable.unknownReason")} action={<div className="availability-reason"><span>{t("unavailable.reasonCode")}</span><code>{projection.reasonCode}</code><p>{t("unavailable.boundary")}</p></div>} /></section>;
  }
  if (projection.kind === "MALFORMED") return <section className="risk-page"><PageHeader title={t("title")} subtitle={t("subtitle")} /><UnavailableState title={t("malformed.title")} description={t("malformed.description")} /></section>;
  return <section className="risk-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} metadata={<code>{t(`revision.${projection.revision}`)}</code>} />
    <section className="risk-layer" aria-labelledby="supported-problem-heading"><div className="section-heading-row"><div><h2 id="supported-problem-heading">{t("supported.title")}</h2><p>{t("supported.description")}</p></div><span className="layer-index">01</span></div>
      <div className="risk-card-stack">{projection.resolutions.map((entry, index) => <ResolutionCard key={index} entry={entry} index={index} validRequirements={validRequirements} onSelectRequirement={onSelectRequirement} />)}</div>
      <PopulationCard entry={projection.population} />
      <div className="risk-card-stack">{projection.relations.map((entry, index) => <RelationCard key={index} entry={entry} index={index} />)}</div>
    </section>
    <section className="risk-layer risk-layer--categorical" aria-labelledby="categorical-risk-heading"><div className="section-heading-row"><div><h2 id="categorical-risk-heading">{t("categorical.title")}</h2><p>{t("categorical.description")}</p></div><span className="layer-index">02</span></div>
      <div className="risk-card-stack">{projection.categorical.map((entry, index) => <CategoricalCard key={index} entry={entry} index={index} />)}</div>
    </section>
    <section className="risk-layer risk-layer--quantitative" aria-labelledby="quantitative-risk-heading"><div className="section-heading-row"><div><h2 id="quantitative-risk-heading">{t("quantitative.title")}</h2><p>{t("quantitative.description")}</p></div><span className="layer-index">03</span></div>
      {projection.quantitative.kind === "REASSESSMENT_ABSENT" ? <Card><div className="neutral-note"><strong>{t("quantitative.currentAbsenceTitle")}</strong><p>{t("quantitative.currentAbsence")}</p></div></Card>
        : <div className="risk-card-stack">{projection.quantitative.records.length ? projection.quantitative.records.map((entry, index) => <QuantitativeCard key={index} entry={entry} index={index} />) : <Card><div className="neutral-note"><strong>{t("quantitative.noRecordsTitle")}</strong><p>{t("quantitative.noRecords")}</p></div></Card>}</div>}
    </section>
    <section className="risk-guardrails" aria-labelledby="risk-guardrails-heading"><h2 id="risk-guardrails-heading">{t("guardrails.title")}</h2><Callout title={t("guardrails.calloutTitle")}><p>{t("guardrails.categoricalQuantitative")}</p><p>{t("guardrails.localGlobal")}</p><p>{t("guardrails.absence")}</p></Callout></section>
  </section>;
}

import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { ExactValue, StatusBadge } from "../../components/scientific";
import { PageHeader } from "../../components/shell";
import { Button, Callout, Card, DataTable } from "../../components/ui";
import { limitationCodes, limitationTranslationKey, type LimitationCode } from "../../i18n";
import {
  selectSpecificationPage,
  specificationCharacteristicKeys,
  materialityGateKeys,
  type AggregateProjection,
  type ComparisonOperandProjection,
  type ContributionEntry,
  type ContractProjection,
  type CrossResultProjection,
  type MaterialityProjection,
  type QbProjection,
} from "./projection";

function Malformed({ compact = false }: { compact?: boolean }) {
  const { t } = useTranslation("specification");
  return <span className={compact ? "malformed-record malformed-record--compact" : "malformed-record"}>{t("malformed.record")}</span>;
}

function ContractIdentity({ value }: { value: ContractProjection | null }) {
  return value
    ? <span className="contract-identity"><code>{value.contractId}</code><code>{value.version}</code></span>
    : <Malformed compact />;
}

function AggregateCard({ characteristicKey, aggregate }: { characteristicKey: string; aggregate: AggregateProjection | null }) {
  const { t } = useTranslation("specification");
  return (
    <article className="specification-aggregate-card">
      <h3>{t(`quality.${characteristicKey}`)}</h3>
      {aggregate ? <>
        <ExactValue value={aggregate.value} fallback={t("quality.noNumericValue")} />
        <StatusBadge code={aggregate.state} />
        <dl className="aggregate-counts">
          <div><dt>{t("quality.computedCount")}</dt><dd>{aggregate.computedCount}</dd></div>
          <div><dt>{t("quality.unknownCount")}</dt><dd>{aggregate.unknownCount}</dd></div>
          <div><dt>{t("quality.notApplicableCount")}</dt><dd>{aggregate.notApplicableCount}</dd></div>
          <div><dt>{t("quality.totalCount")}</dt><dd>{aggregate.totalCount}</dd></div>
        </dl>
        <dl className="compact-metadata">
          <div><dt>{t("quality.characteristicId")}</dt><dd><code>{aggregate.characteristicId}</code></dd></div>
          <div><dt>{t("quality.aggregationRule")}</dt><dd><code>{aggregate.aggregationRuleId}</code></dd></div>
        </dl>
      </> : <Malformed />}
    </article>
  );
}

const observabilityFields = [
  "totalRequirementCount", "requirementsWithObservationsCount", "requirementsInApplicableComparisonsCount",
  "totalRequirementPairCount", "totalObservationPairCount", "confirmedConflictCount", "compatibleCount",
  "unresolvedCount", "outsideApplicabilityCount", "applicableComparisonCount", "globalUnresolvedExtractionCount",
  "qbMaterialUnresolvedCount", "qbNonMaterialDiagnosticCount", "observedRconfCount",
] as const;

function QbSection({ qb }: { qb: QbProjection | null }) {
  const { t, i18n } = useTranslation("specification");
  if (!qb) return <Card className="specification-qb-card"><Malformed /></Card>;
  return (
    <Card className="specification-qb-card">
      <div className="specification-qb-card__primary">
        <div>
          <span className="primitive-label">{t("qb.exactValue")}</span>
          <ExactValue value={qb.value} fallback={t("qb.noNumericValue")} />
        </div>
        <StatusBadge code={qb.state} />
        <dl className="compact-metadata">
          <div><dt>{t("qb.snapshot")}</dt><dd><code>{qb.snapshotId}</code></dd></div>
          <div><dt>{t("qb.rconfComplete")}</dt><dd><code>{String(qb.rconfComplete)}</code><span className="field-explanation">{t("qb.rconfCompleteBoundary")}</span></dd></div>
        </dl>
      </div>

      <div className="specification-qb-card__reasons">
        <h3>{t("qb.reasons")}</h3>
        {qb.reasons.length ? <ol>{qb.reasons.map((reason, index) => {
          const key = `qb.reasonExplanations.${reason}`;
          return <li key={`${reason}-${index}`}><code>{reason}</code><span>{i18n.exists(key, { ns: "specification" }) ? t(key) : t("qb.unknownReason")}</span></li>;
        })}</ol> : <p className="empty-records">{t("qb.noReasons")}</p>}
      </div>

      <section className="qb-detail-section" aria-labelledby="qb-observability-heading">
        <h3 id="qb-observability-heading">{t("qb.observability.title")}</h3>
        <p className="section-description">{t("qb.observability.description")}</p>
        {qb.observability ? <dl className="scope-count-grid">
          {observabilityFields.map((field) => <div key={field}><dt>{t(`qb.observability.${field}`)}</dt><dd>{qb.observability?.[field]}</dd></div>)}
          <div><dt>{t("qb.observability.rconfComplete")}</dt><dd><code>{String(qb.observability.rconfComplete)}</code></dd></div>
        </dl> : <Malformed />}
      </section>

      <section className="qb-detail-section" aria-labelledby="qb-trace-heading">
        <h3 id="qb-trace-heading">{t("qb.trace.title")}</h3>
        <div className="qb-contract-grid">
          <div><span>{t("qb.trace.coverageProfile")}</span><ContractIdentity value={qb.coverageProfile} /></div>
          <div><span>{t("qb.trace.aggregationRule")}</span><ContractIdentity value={qb.aggregationRule} /></div>
          <div><span>{t("qb.trace.nonClaimContract")}</span><ContractIdentity value={qb.nonClaimContract} /></div>
        </div>
        <dl className="scope-count-grid scope-count-grid--small">
          <div><dt>{t("qb.trace.totalRequirementCount")}</dt><dd>{qb.formulaOperands?.totalRequirementCount ?? <Malformed compact />}</dd></div>
          <div><dt>{t("qb.trace.observedRconfCount")}</dt><dd>{qb.formulaOperands?.observedRconfCount ?? <Malformed compact />}</dd></div>
        </dl>
        <p className="scientific-boundary">{t("qb.trace.operandsBoundary")}</p>
        <div className="technical-list-block"><strong>{t("qb.trace.rconfParticipants")}</strong>{qb.rconfParticipantIds.length ? qb.rconfParticipantIds.map((id) => <code key={id}>{id}</code>) : <span>{t("none")}</span>}</div>
        <div className="technical-list-block"><strong>{t("qb.trace.crossResultIds")}</strong>{qb.crossResultIds.length ? qb.crossResultIds.map((id, index) => id ? <code key={`${id}-${index}`}>{id}</code> : <Malformed key={`malformed-${index}`} compact />) : <span>{t("none")}</span>}</div>
        <div className="technical-list-block"><strong>{t("qb.trace.materialityDiagnosticRefs")}</strong>{qb.materialityDiagnosticRefs.length ? qb.materialityDiagnosticRefs.map((ref, index) => ref ? <code key={`${ref.requirementId}-${ref.diagnosticIndex}-${index}`}>{ref.requirementId} / {ref.featureId} / {ref.diagnosticIndex}</code> : <Malformed key={`malformed-${index}`} compact />) : <span>{t("none")}</span>}</div>
        <div className="technical-list-block"><strong>{t("qb.trace.nonClaimKeys")}</strong>{qb.nonClaimKeys.length ? qb.nonClaimKeys.map((key, index) => key ? <code key={`${key}-${index}`}>{key}</code> : <Malformed key={`malformed-${index}`} compact />) : <span>{t("none")}</span>}</div>
      </section>
    </Card>
  );
}

function ContributionTable({ entries, onSelectRequirement }: { entries: ContributionEntry[]; onSelectRequirement: (id: string) => void }) {
  const { t } = useTranslation("specification");
  return <DataTable
    caption={t("contributions.caption")}
    rows={entries}
    rowKey={(entry) => `${entry.kind}-${entry.position}`}
    columns={[
      { key: "requirement", header: t("contributions.requirement"), render: (entry) => entry.kind === "VALID" ? <div className="contribution-identity"><code>{entry.value.requirementId}</code><span>{t("contributions.sourceLine", { line: entry.value.sourceLine })}</span></div> : <div><Malformed compact /><span className="malformed-position">{t("malformed.position", { position: entry.position })}</span></div> },
      ...specificationCharacteristicKeys.map((key) => ({ key, header: t(`quality.${key}`), render: (entry: ContributionEntry) => entry.kind === "VALID" ? <div className="contribution-value"><ExactValue compact value={entry.value.characteristics[key].value} fallback={t(`states.${entry.value.characteristics[key].state}`)} /><StatusBadge code={entry.value.characteristics[key].state} /></div> : <span aria-hidden="true">—</span> })),
      { key: "action", header: t("contributions.action"), render: (entry) => entry.kind === "VALID" && entry.navigable ? <Button variant="quiet" type="button" onClick={() => onSelectRequirement(entry.value.requirementId)}>{t("contributions.openRequirement", { id: entry.value.requirementId })}</Button> : <span className="scientific-boundary">{entry.kind === "VALID" ? t("contributions.requirementUnavailable") : t("contributions.notNavigable")}</span> },
    ]}
  />;
}

function ParticipantButton({ participant, navigableIds, onSelectRequirement }: { participant: CrossResultProjection["participants"][number]; navigableIds: Set<string>; onSelectRequirement: (id: string) => void }) {
  const { t } = useTranslation("specification");
  return participant.matchesCanonicalPopulation && navigableIds.has(participant.requirementId)
    ? <Button type="button" variant="quiet" onClick={() => onSelectRequirement(participant.requirementId)}>{participant.requirementId}</Button>
    : <span className="dangling-reference"><code>{participant.requirementId}</code> {t("crossResults.danglingParticipant")}</span>;
}

function OperandTrace({ label, operand }: { label: string; operand: ComparisonOperandProjection }) {
  const { t } = useTranslation("specification");
  const technical = (value: string | null) => value === null ? <span className="scientific-boundary">{t("none")}</span> : <code>{value}</code>;
  return <section className="operand-trace">
    <h4>{label}</h4>
    <dl className="compact-metadata">
      <div><dt>{t("crossResults.trace.snapshot")}</dt><dd><code>{operand.snapshotId}</code></dd></div>
      <div><dt>{t("crossResults.trace.observationRef")}</dt><dd><code>{operand.observationRef.requirementId} / {operand.observationRef.featureId} / {operand.observationRef.observationIndex}</code></dd></div>
      <div><dt>{t("crossResults.trace.normalizedMetric")}</dt><dd>{technical(operand.normalizedMetric)}</dd></div>
      <div><dt>{t("crossResults.trace.normalizedContext")}</dt><dd>{technical(operand.normalizedContext)}</dd></div>
      <div><dt>{t("crossResults.trace.comparator")}</dt><dd>{technical(operand.comparator)}</dd></div>
      <div><dt>{t("crossResults.trace.inclusivity")}</dt><dd>{technical(operand.inclusivity)}</dd></div>
      <div><dt>{t("crossResults.trace.exactValue")}</dt><dd>{technical(operand.value)}</dd></div>
      <div><dt>{t("crossResults.trace.unit")}</dt><dd>{technical(operand.unit)}</dd></div>
    </dl>
  </section>;
}

function CrossResultCard({ item, position, navigableIds, onSelectRequirement }: { item: CrossResultProjection | null; position: number; navigableIds: Set<string>; onSelectRequirement: (id: string) => void }) {
  const { t } = useTranslation("specification");
  if (!item) return <Card className="cross-result-card"><Malformed /><span className="malformed-position">{t("malformed.position", { position })}</span></Card>;
  return (
    <Card className="cross-result-card">
      <div className="cross-result-card__heading"><code>{item.resultId}</code><StatusBadge code={item.state} /></div>
      <p className="scientific-boundary">{t(`crossResults.stateBoundaries.${item.state}`)}</p>
      <div className="participant-list"><strong>{t("crossResults.participants")}</strong>{item.participants.map((participant) => <ParticipantButton key={`${participant.sourceOrder}-${participant.requirementId}`} participant={participant} navigableIds={navigableIds} onSelectRequirement={onSelectRequirement} />)}</div>
      <dl className="compact-metadata cross-result-metadata">
        <div><dt>{t("crossResults.relationKind")}</dt><dd><code>{item.relationKind}</code></dd></div>
        {item.conflictClass ? <div><dt>{t("crossResults.conflictClass")}</dt><dd><code>{item.conflictClass}</code></dd></div> : null}
        {item.conflictSubtype ? <div><dt>{t("crossResults.conflictSubtype")}</dt><dd><code>{item.conflictSubtype}</code></dd></div> : null}
        <div><dt>{t("crossResults.comparisonContract")}</dt><dd><ContractIdentity value={item.comparisonContract} /></dd></div>
        <div><dt>{t("crossResults.coverageProfile")}</dt><dd><ContractIdentity value={item.coverageProfile} /></dd></div>
      </dl>
      {item.unresolvedReasons.length ? <div className="technical-list-block"><strong>{t("crossResults.unresolvedReasons")}</strong>{item.unresolvedReasons.map((reason) => <code key={reason}>{reason}</code>)}</div> : null}
      {item.outsideReasons.length ? <div className="technical-list-block"><strong>{t("crossResults.outsideReasons")}</strong>{item.outsideReasons.map((reason) => <code key={reason}>{reason}</code>)}</div> : null}
      <div className="technical-list-block"><strong>{t("crossResults.evidenceRefs")}</strong>{item.evidenceRefs.length ? item.evidenceRefs.map((ref, index) => ref ? <span key={`${ref.requirementId}-${ref.evidenceId}-${index}`}><code>{ref.requirementId}</code> → <code>{ref.evidenceId}</code></span> : <Malformed key={`malformed-${index}`} compact />) : <span>{t("none")}</span>}</div>
      <p className="scientific-boundary">{t("crossResults.evidenceBoundary")}</p>
      <details className="cross-comparison-trace">
        <summary>{t("crossResults.trace.title")}</summary>
        <dl className="compact-metadata cross-result-metadata">
          <div><dt>{t("crossResults.trace.snapshot")}</dt><dd><code>{item.snapshotId}</code></dd></div>
          <div><dt>{t("crossResults.trace.observationRefs")}</dt><dd>{item.observationRefs.map((ref) => <code key={`${ref.requirementId}-${ref.observationIndex}`}>{ref.requirementId} / {ref.featureId} / {ref.observationIndex}</code>)}</dd></div>
          <div><dt>{t("crossResults.trace.diagnosticRefs")}</dt><dd>{item.diagnosticRefs.length ? item.diagnosticRefs.map((ref) => <code key={`${ref.requirementId}-${ref.diagnosticIndex}`}>{ref.requirementId} / {ref.featureId} / {ref.diagnosticIndex}</code>) : <span className="scientific-boundary">{t("none")}</span>}</dd></div>
          <div><dt>{t("crossResults.trace.comparisonKey")}</dt><dd>{item.comparisonKey ? <><code>{item.comparisonKey.normalizedMetric}</code><code>{item.comparisonKey.normalizedContext}</code><code>{item.comparisonKey.unit}</code></> : <span className="scientific-boundary">{t("none")}</span>}</dd></div>
        </dl>
        <div className="operand-trace-grid"><OperandTrace label={t("crossResults.trace.leftOperand")} operand={item.operands.left} /><OperandTrace label={t("crossResults.trace.rightOperand")} operand={item.operands.right} /></div>
      </details>
    </Card>
  );
}

function MaterialitySection({ value }: { value: MaterialityProjection | null }) {
  const { t } = useTranslation("specification");
  if (!value) return <Malformed />;
  return <>
    <div className="materiality-summary">
      <div><span>{t("materiality.globalUnresolved")}</span><strong>{value.globalUnresolvedDiagnosticCount}</strong></div>
      <div><span>{t("materiality.qbMaterial")}</span><strong>{value.qbMaterialCount}</strong></div>
      <div><span>{t("materiality.qbNonMaterial")}</span><strong>{value.qbNonMaterialCount}</strong></div>
    </div>
    <dl className="compact-metadata">
      <div><dt>{t("materiality.snapshot")}</dt><dd><code>{value.snapshotId}</code></dd></div>
      <div><dt>{t("materiality.rule")}</dt><dd><ContractIdentity value={value.materialityRule} /></dd></div>
    </dl>
    {value.auditRecords.length ? <details className="materiality-audits"><summary>{t("materiality.audits", { count: value.auditRecords.length })}</summary><ol>{value.auditRecords.map((audit, index) => audit ? <li key={`${audit.requirementId}-${audit.diagnosticCode}-${index}`}>
      <div className="record-heading"><code>{audit.requirementId}</code><code>{audit.disposition}</code></div>
      <p><code>{audit.diagnosticCode}</code> <code>{audit.diagnosticRuleId}</code></p>
      <dl className="compact-metadata materiality-proof-metadata">
        <div><dt>{t("materiality.auditSnapshot")}</dt><dd><code>{audit.snapshotId}</code></dd></div>
        <div><dt>{t("materiality.sourceOrder")}</dt><dd>{audit.requirementSourceOrder}</dd></div>
        <div><dt>{t("materiality.diagnosticRef")}</dt><dd><code>{audit.diagnosticRef.requirementId} / {audit.diagnosticRef.featureId} / {audit.diagnosticRef.diagnosticIndex}</code></dd></div>
        <div><dt>{t("materiality.contextEvidenceRef")}</dt><dd>{audit.matchedContextEvidenceRef ? <><code>{audit.matchedContextEvidenceRef.requirementId}</code> → <code>{audit.matchedContextEvidenceRef.evidenceId}</code></> : <span className="scientific-boundary">{t("none")}</span>}</dd></div>
        <div><dt>{t("materiality.allowlistContract")}</dt><dd>{audit.matchedAllowlistContract ? <ContractIdentity value={audit.matchedAllowlistContract} /> : <span className="scientific-boundary">{t("none")}</span>}</dd></div>
        <div><dt>{t("materiality.auditRule")}</dt><dd><ContractIdentity value={audit.materialityRule} /></dd></div>
      </dl>
      {audit.candidateText !== null ? <div className="candidate-span"><strong>{t("materiality.candidate")}</strong><q>{audit.candidateText}</q><span>{audit.startOffset}–{audit.endOffset}</span><small>{t("materiality.notEvidence")}</small></div> : null}
      <div className="materiality-gates"><strong>{t("materiality.gates.title")}</strong><dl>{materialityGateKeys.map((key) => <div key={key}><dt>{t(`materiality.gates.${key}`)}</dt><dd><code>{String(audit.gateOutcomes[key])}</code></dd></div>)}</dl></div>
    </li> : <li key={`malformed-${index}`}><Malformed /></li>)}</ol></details> : null}
  </>;
}

function knownLimitation(code: unknown): code is LimitationCode {
  return typeof code === "string" && limitationCodes.some((item) => item === code);
}

export function SpecificationPage({ result, onSelectRequirement }: { result: CanonicalAnalyzeResponse; onSelectRequirement: (id: string) => void }) {
  const { t } = useTranslation("specification");
  const { t: limitationText } = useTranslation("limitations");
  const projection = useMemo(() => selectSpecificationPage(result), [result]);
  const navigableIds = useMemo(() => new Set(projection.contributions.flatMap((entry) => entry.kind === "VALID" && entry.navigable ? [entry.value.requirementId] : [])), [projection.contributions]);
  return (
    <section className="specification-page">
      <PageHeader title={t("title")} subtitle={t("subtitle")} metadata={projection.snapshotId ? <span>{t("snapshot")}: <code>{projection.snapshotId}</code></span> : <Malformed compact />} />

      <section className="specification-section" aria-labelledby="specification-quality-heading">
        <h2 id="specification-quality-heading">{t("quality.title")}</h2>
        <p className="section-description">{t("quality.description")}</p>
        <div className="specification-aggregate-grid">{specificationCharacteristicKeys.map((key) => <AggregateCard key={key} characteristicKey={key} aggregate={projection.aggregates[key]} />)}</div>
      </section>

      <section className="specification-section" aria-labelledby="qb-heading">
        <h2 id="qb-heading">{t("qb.title")}</h2>
        <p className="section-description">{t("qb.description")}</p>
        <QbSection qb={projection.qb} />
        <Callout title={t("boundaries.qbTitle")}><p>{t("boundaries.qbDescription")}</p></Callout>
      </section>

      <section className="specification-section" aria-labelledby="contributions-heading">
        <h2 id="contributions-heading">{t("contributions.title")}</h2>
        <p className="section-description">{t("contributions.description")}</p>
        <Card><ContributionTable entries={projection.contributions} onSelectRequirement={onSelectRequirement} /></Card>
      </section>

      <section className="specification-section specification-trace-section" aria-labelledby="cross-results-heading">
        <h2 id="cross-results-heading">{t("crossResults.title")}</h2>
        <p className="section-description">{t("crossResults.description")}</p>
        {projection.crossResults.length ? <div className="cross-result-list">{projection.crossResults.map((item, index) => <CrossResultCard key={item?.resultId ?? `malformed-${index}`} item={item} position={index + 1} navigableIds={navigableIds} onSelectRequirement={onSelectRequirement} />)}</div> : <p className="empty-records">{t("crossResults.empty")}</p>}
      </section>

      <section className="specification-section specification-trace-section" aria-labelledby="materiality-heading">
        <h2 id="materiality-heading">{t("materiality.title")}</h2>
        <p className="section-description">{t("materiality.description")}</p>
        <Card><MaterialitySection value={projection.materiality} /></Card>
      </section>

      <section className="specification-section specification-trace-section" aria-labelledby="projection-trace-heading">
        <h2 id="projection-trace-heading">{t("projectionTrace.title")}</h2>
        <details className="projection-trace"><summary>{t("projectionTrace.summary")}</summary>{projection.projectionTrace ? <>
          <dl className="scope-count-grid scope-count-grid--small">
            <div><dt>{t("projectionTrace.requirements")}</dt><dd>{projection.projectionTrace.requirementCount}</dd></div>
            <div><dt>{t("projectionTrace.observations")}</dt><dd>{projection.projectionTrace.observationCount}</dd></div>
            <div><dt>{t("projectionTrace.evidence")}</dt><dd>{projection.projectionTrace.evidenceCount}</dd></div>
            <div><dt>{t("projectionTrace.diagnostics")}</dt><dd>{projection.projectionTrace.diagnosticCount}</dd></div>
          </dl>
          <p><code>{projection.projectionTrace.snapshotId}</code></p>
          <div className="qb-contract-grid">{projection.projectionTrace.contracts.map((item) => <div key={item.slot}><span>{t(`projectionTrace.contracts.${item.slot}`)}</span><ContractIdentity value={item.value} /></div>)}</div>
        </> : <Malformed />}</details>
      </section>

      <section className="specification-section specification-limitations" aria-labelledby="specification-limitations-heading">
        <h2 id="specification-limitations-heading">{t("limitations.title")}</h2>
        <Callout title={t("boundaries.absenceTitle")}><p>{t("boundaries.absenceDescription")}</p></Callout>
        <Callout title={t("boundaries.consistencyTitle")}><p>{t("boundaries.consistencyDescription")}</p></Callout>
        {result.limitations.map((code, index) => {
          const canonicalCode = typeof code === "string" ? code : null;
          const explanation = knownLimitation(code) ? limitationText(limitationTranslationKey(code)) : limitationText("unknown");
          return <Callout key={`${canonicalCode ?? "malformed"}-${index}`} title={canonicalCode ?? t("malformed.limitation")}><p>{explanation}</p></Callout>;
        })}
      </section>
    </section>
  );
}

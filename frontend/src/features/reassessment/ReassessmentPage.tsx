import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { ExactValue } from "../../components/scientific";
import { Callout, Card } from "../../components/ui";
import { PageHeader } from "../../components/shell";
import { selectReassessmentProjection, type JsonRecord, type SnapshotValue } from "./projection";

function technical(value: unknown) {
  if (value === null || value === undefined) return "—";
  return typeof value === "string" ? value : JSON.stringify(value);
}

function Snapshot({ value }: { value: SnapshotValue | { state: SnapshotValue["state"]; value: SnapshotValue["value"] } }) {
  const { t } = useTranslation("reassessment");
  const detailed = "totalCount" in value ? value as SnapshotValue : null;
  return <div className="snapshot-value"><ExactValue value={value.value} fallback={value.state} /><code>{value.state}</code>
    {detailed && detailed.totalCount !== null ? <small>{t("counts", { computed: detailed.computedCount, unknown: detailed.unknownCount, notApplicable: detailed.notApplicableCount, total: detailed.totalCount })}</small> : null}
    {detailed?.reasons.length ? <span className="snapshot-reasons">{detailed.reasons.map((reason, index) => <code key={`${reason}-${index}`}>{reason}</code>)}</span> : null}
  </div>;
}

function Identity({ label, value }: { label: string; value: unknown }) {
  return <div><dt>{label}</dt><dd><code>{technical(value)}</code></dd></div>;
}

function ArtifactLabel({ value }: { value: JsonRecord }) {
  return <code>{String(value.artifact_id)} / {String(value.artifact_version)}</code>;
}

export function ReassessmentPage({ result }: { result: CanonicalAnalyzeResponse }) {
  const { t } = useTranslation("reassessment");
  const projection = useMemo(() => selectReassessmentProjection(result), [result]);
  if (!projection) return null;
  return <section className="lifecycle-page reassessment-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} metadata={<><code>{projection.reassessmentId}</code><code>{projection.reassessmentVersion}</code></>} />

    <section className="lifecycle-section" aria-labelledby="reassessment-lifecycle"><h2 id="reassessment-lifecycle">{t("lifecycle")}</h2>
      <div className="lifecycle-strip"><ArtifactLabel value={projection.parentArtifactRef} /><span>{t("externalRevision")} <code>{projection.externalRevision.revisionId} / {projection.externalRevision.revisionVersion}</code></span><ArtifactLabel value={projection.childArtifactRef} /></div>
    </section>

    <Card title={t("identity.title")}>
      <dl className="lifecycle-metadata">
        <Identity label={t("identity.reassessment")} value={{ reassessment_id: projection.reassessmentId, reassessment_version: projection.reassessmentVersion }} />
        <Identity label={t("identity.status")} value={projection.status} />
        <Identity label={t("identity.rule")} value={projection.ruleRef} />
        <Identity label={t("identity.assessment")} value={projection.childAssessmentRef} />
        <Identity label={t("identity.application")} value={projection.actionApplicationRef} />
        <Identity label={t("identity.revision")} value={projection.externalRevision.revisionRef} />
        <Identity label={t("identity.provider")} value={{ provider_kind: projection.externalRevision.providerKind, provider_ref: projection.externalRevision.providerRef }} />
        <Identity label={t("identity.processBefore")} value={projection.predecessorProcessStateRef} />
        <Identity label={t("identity.processAfter")} value={projection.childProcessStateRef} />
        <Identity label={t("identity.reasons")} value={projection.reasonCodes} />
      </dl>
      <details><summary>{t("identity.technical")}</summary><dl className="lifecycle-metadata">
        <Identity label={t("identity.components")} value={projection.componentVersionSet} />
        <Identity label={t("identity.provenance")} value={projection.provenance} />
      </dl></details>
    </Card>

    <section className="lifecycle-section" aria-labelledby="produced-results"><h2 id="produced-results">{t("produced.title")}</h2>
      <div className="produced-results">{projection.producedResults.map((item, index) => <Card key={`${item.family}-${index}`}>
        <code>{item.family}</code><dl className="compact-metadata"><Identity label={t("produced.resultId")} value={item.resultId} /><Identity label={t("produced.artifact")} value={item.artifactRef} /></dl>
      </Card>)}</div>
      <details><summary>{t("comparisonRequests.title", { count: projection.comparisonRequestRefs.length })}</summary><pre className="technical-json">{technical(projection.comparisonRequestRefs)}</pre></details>
    </section>

    <section className="lifecycle-section" aria-labelledby="requirement-snapshots"><h2 id="requirement-snapshots">{t("requirements.title")}</h2>
      <div className="requirement-snapshots">{projection.requirements.map((item, index) => <Card key={`${technical(item.lineage)}-${index}`} className="requirement-before-after">
        <div className="record-heading"><code>{technical(item.lineage)}</code>{item.changed ? <span className="neutral-label">{t("requirements.changed")}</span> : null}</div>
        <div className="before-after before-after--requirements">
          {(["before", "after"] as const).map((side) => <section key={side}><h3>{t(side)}</h3><p className="requirement-source">{item[`${side}Text`]}</p><code>{technical(item[`${side}Subject`])}</code>
            <dl className="snapshot-characteristics">{(["completeness", "verifiability", "unambiguity"] as const).map((key) => <div key={key}><dt>{t(`characteristics.${key}`)}</dt><dd><Snapshot value={item[side][key]} /></dd></div>)}</dl>
          </section>)}
        </div>
      </Card>)}</div>
    </section>

    <section className="lifecycle-section" aria-labelledby="specification-snapshot"><h2 id="specification-snapshot">{t("specification.title")}</h2>
      <Card><div className="before-after">{(["before", "after"] as const).map((side) => <section key={side}><h3>{t(side)}</h3>
        <dl className="snapshot-characteristics">{(["completeness", "verifiability", "unambiguity"] as const).map((key) => <div key={key}><dt>{t(`characteristics.${key}`)}</dt><dd><Snapshot value={projection.specification[side][key]} /></dd></div>)}
          <div><dt>{t("characteristics.qb")}</dt><dd><Snapshot value={side === "before" ? projection.specification.qbBefore : projection.specification.qbAfter} /></dd></div>
        </dl></section>)}</div></Card>
    </section>

    <section className="lifecycle-section" aria-labelledby="evidence-reuse"><h2 id="evidence-reuse">{t("evidence.title")}</h2>
      {projection.evidenceReuse.length ? projection.evidenceReuse.map((decision, index) => <Card key={index}>
        <div className="record-heading"><code>{decision.decision}</code>{decision.reasonCodes.map((reason, reasonIndex) => <code key={`${reason}-${reasonIndex}`}>{reason}</code>)}</div>
        <dl className="lifecycle-metadata"><Identity label={t("evidence.source")} value={decision.sourceEvidenceRef} /><Identity label={t("evidence.target")} value={decision.targetProcessStateRef} /><Identity label={t("evidence.provenance")} value={decision.provenance} /></dl>
        <div className="identity-checks">{decision.exactIdentityChecks.map((check, checkIndex) => <article key={`${check.fieldName}-${checkIndex}`}>
          <span><small>{t("evidence.field")}</small><strong>{check.fieldName}</strong></span>
          <span><small>{t("evidence.expected")}</small><code>{technical(check.expected)}</code></span>
          <span><small>{t("evidence.actual")}</small><code>{technical(check.actual)}</code></span>
          <span><small>{t("evidence.matches")}</small><code>{String(check.matches)}</code></span>
        </article>)}</div>
      </Card>) : <p className="scientific-boundary">{t("evidence.none")}</p>}
    </section>

    <Callout title={t("limitation.title")}><p>{t("limitation.description")}</p></Callout>
  </section>;
}

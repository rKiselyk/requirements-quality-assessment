import { useState, type ReactNode } from "react";
import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { ApplicabilityBadge, StatusBadge } from "../../components/scientific";
import { PageHeader } from "../../components/shell";
import { Button, Callout, Card, DataTable, InlineValidation, TextArea, UnavailableState } from "../../components/ui";
import type { Rui05AnalyzeRequest } from "../specification-input/model";
import { canonicalJson, selectCorrectiveActionsPage, type ActionProjection, type ChangedRequirementProjection, type ExternalRevisionProjection, type ResolutionProjection } from "./projection";
import { createReassessmentDraft, createReassessmentRequest, matchesCanonicalRevision } from "./reassessmentDraft";

function TechnicalDetails({ value, label }: { value: unknown; label?: string }) {
  const { t } = useTranslation("actions");
  return <details className="product-quality-technical"><summary>{label ?? t("technical.details")}</summary><pre>{canonicalJson(value)}</pre></details>;
}

function StatePair({ status, applicability }: { status: string; applicability: string }) {
  return <div className="product-quality-state"><StatusBadge code={status} /><ApplicabilityBadge code={applicability} /></div>;
}

function Metadata({ children }: { children: ReactNode }) {
  return <dl className="compact-metadata action-metadata">{children}</dl>;
}

function MetadataItem({ label, children }: { label: string; children: ReactNode }) {
  return <div><dt>{label}</dt><dd>{children}</dd></div>;
}

function ResolutionCard({ resolution }: { resolution: ResolutionProjection }) {
  const { t } = useTranslation("actions");
  return <Card title={t("resolution.title")} description={t("resolution.description")} className="action-record">
    <StatePair status={resolution.status} applicability={resolution.applicability} />
    <Metadata>
      <MetadataItem label={t("resolution.reason")}><code>{resolution.reasonCode}</code></MetadataItem>
      <MetadataItem label={t("resolution.rule")}><code>{String(resolution.ruleRef.rule_id)} / {String(resolution.ruleRef.explicit_version)}</code></MetadataItem>
      <MetadataItem label={t("resolution.identity")}><TechnicalDetails value={resolution.resolutionId} label={t("technical.reference")} /></MetadataItem>
      <MetadataItem label={t("resolution.sources")}><TechnicalDetails value={{ risk: resolution.sourceRiskRef, problem: resolution.sourceProblemRef, relation: resolution.sourceRelationRef }} label={t("technical.references")} /></MetadataItem>
    </Metadata>
    <TechnicalDetails value={resolution.raw} />
  </Card>;
}

function ProposalCard({ action, onSelectRequirement }: { action: ActionProjection; onSelectRequirement: (requirementId: string) => void }) {
  const { t } = useTranslation("actions");
  return <Card title={t("proposal.title")} description={t("proposal.description")} className="action-record proposal-card">
    <div className="action-heading"><StatusBadge code={action.status} /><code>{action.actionKind}</code></div>
    <Metadata>
      <MetadataItem label={t("proposal.changeKind")}><code>{action.proposedChangeKind}</code></MetadataItem>
      <MetadataItem label={t("proposal.targetArtifact")}><TechnicalDetails value={action.targetArtifactRef} label={t("technical.reference")} /></MetadataItem>
      <MetadataItem label={t("proposal.creator")}><TechnicalDetails value={action.creatorSource} label={t("technical.reference")} /></MetadataItem>
      <MetadataItem label={t("proposal.nonOptimality")}><code>{action.nonOptimalityClaim}</code></MetadataItem>
    </Metadata>
    <DataTable
      caption={t("targets.caption")}
      rows={action.targets}
      rowKey={(target) => canonicalJson(target.lineage)}
      columns={[
        { key: "requirement", header: t("targets.requirement"), render: (target) => target.navigationRequirementId
          ? <Button type="button" variant="quiet" onClick={() => onSelectRequirement(target.navigationRequirementId!)}>{target.requirementId}</Button>
          : <code>{target.requirementId}</code> },
        { key: "line", header: t("targets.sourceLine"), render: (target) => target.sourceLine },
        { key: "lineage", header: t("targets.lineage"), render: (target) => <TechnicalDetails value={target.lineage} label={t("technical.reference")} /> },
        { key: "change", header: t("targets.changeKind"), render: () => <code>{action.proposedChangeKind}</code> },
      ]}
    />
    <div className="action-copy"><h3>{t("proposal.rationale")}</h3><p>{action.rationale}</p></div>
    <div className="action-copy"><h3>{t("proposal.outcome")}</h3><p>{action.expectedBoundedOutcome}</p></div>
    <p className="scientific-boundary">{t("proposal.boundary")}</p>
    <TechnicalDetails value={{ action_ref: action.actionRef, comparison_key: action.comparisonKey, rule_ref: action.ruleRef, verification_rule_ref: action.verificationRuleRef, ordered_evidence_refs: action.orderedEvidenceRefs }} />
  </Card>;
}

function RevisionCard({ revision }: { revision: ExternalRevisionProjection }) {
  const { t } = useTranslation("actions");
  return <Card title={t("revision.title")} description={t("revision.description")} className="action-record revision-card">
    <Metadata>
      <MetadataItem label={t("revision.providerKind")}><code>{revision.providerKind}</code></MetadataItem>
      <MetadataItem label={t("revision.provider")}><TechnicalDetails value={revision.providerRef} label={t("technical.reference")} /></MetadataItem>
      <MetadataItem label={t("revision.parent")}><TechnicalDetails value={revision.parentArtifactRef} label={t("technical.reference")} /></MetadataItem>
      <MetadataItem label={t("revision.child")}><TechnicalDetails value={revision.childArtifactRef} label={t("technical.reference")} /></MetadataItem>
    </Metadata>
    <DataTable
      caption={t("revision.replacements")}
      rows={revision.replacements}
      rowKey={(replacement) => canonicalJson(replacement.lineage)}
      columns={[
        { key: "lineage", header: t("targets.lineage"), render: (replacement) => <TechnicalDetails value={replacement.lineage} label={t("technical.reference")} /> },
        { key: "parent", header: t("revision.expectedParent"), render: (replacement) => <TechnicalDetails value={replacement.expectedParentSubject} label={t("technical.reference")} /> },
        { key: "text", header: t("revision.externalText"), render: (replacement) => <span className="source-text">{replacement.replacementText}</span> },
      ]}
    />
    {revision.providerRationale ? <p className="record-explanation">{revision.providerRationale}</p> : null}
    <p className="scientific-boundary">{t("revision.boundary")}</p>
    <TechnicalDetails value={revision.raw} />
  </Card>;
}

function ChangedRequirements({ rows }: { rows: ChangedRequirementProjection[] }) {
  const { t } = useTranslation("actions");
  return <Card title={t("changed.title")} description={t("changed.description")} className="changed-requirements">
    <DataTable
      caption={t("changed.caption")}
      rows={rows}
      rowKey={(row) => canonicalJson(row.lineage)}
      columns={[
        { key: "lineage", header: t("targets.lineage"), render: (row) => <TechnicalDetails value={row.lineage} label={t("technical.reference")} /> },
        { key: "before", header: t("changed.before"), render: (row) => <div className="changed-text"><TechnicalDetails value={row.beforeSubject} label={t("technical.subject")} /><span className="source-text">{row.beforeText}</span></div> },
        { key: "after", header: t("changed.after"), render: (row) => <div className="changed-text"><TechnicalDetails value={row.afterSubject} label={t("technical.subject")} /><span className="source-text">{row.afterText}</span></div> },
        { key: "kind", header: t("targets.changeKind"), render: (row) => <code>{row.changeKind}</code> },
      ]}
    />
  </Card>;
}

export function CorrectiveActionsPage({
  result,
  onSelectRequirement,
  onAnalyzeReassessment,
  reassessmentPending = false,
  reassessmentErrorMessage = null,
  onRetryReassessment,
  onReassessmentDraftChange = () => undefined,
}: {
  result: CanonicalAnalyzeResponse;
  onSelectRequirement: (requirementId: string) => void;
  onAnalyzeReassessment: (request: Rui05AnalyzeRequest) => void;
  reassessmentPending?: boolean;
  reassessmentErrorMessage?: string | null;
  onRetryReassessment?: () => void;
  onReassessmentDraftChange?: () => void;
}) {
  const { t } = useTranslation("actions");
  const projection = selectCorrectiveActionsPage(result);
  const [editorOpen, setEditorOpen] = useState(false);
  const [draft, setDraft] = useState("");

  if (projection.kind === "UNAVAILABLE") return <section className="corrective-actions-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} />
    <UnavailableState title={t("unavailable.title")} description={t("unavailable.description")} />
    <p className="unavailable-reason"><span>{t("unavailable.reason")}</span><code>{projection.reasonCode}</code></p>
  </section>;
  if (projection.kind === "MALFORMED") return <section className="corrective-actions-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} />
    <UnavailableState title={t("malformed.title")} description={t("malformed.description")} />
  </section>;

  const entry = projection.reassessment;
  const canonicalDraft = entry ? createReassessmentDraft(entry.requirements) : "";
  const canonical = entry ? matchesCanonicalRevision(draft, entry.requirements) : false;
  const submit = () => {
    if (!entry || !canonical || reassessmentPending) return;
    if (onRetryReassessment) onRetryReassessment();
    else onAnalyzeReassessment(createReassessmentRequest(entry.requirements, entry.priorContext));
  };

  return <section className="corrective-actions-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} />
    <ResolutionCard resolution={projection.resolution} />
    {projection.resolution.action ? <ProposalCard action={projection.resolution.action} onSelectRequirement={onSelectRequirement} /> : null}
    {projection.externalRevision ? <RevisionCard revision={projection.externalRevision} /> : null}
    {projection.application ? <Card title={t("application.title")} description={t("application.description")} className="action-record application-card">
      <div className="product-quality-state"><StatusBadge code={projection.application.status} /></div>
      <div className="application-lineage"><StatusBadge code="PROPOSED" /><span aria-hidden="true">→</span><StatusBadge code="APPLIED" /></div>
      <Metadata>
        <MetadataItem label={t("application.reason")}><code>{projection.application.reasonCode}</code></MetadataItem>
        <MetadataItem label={t("application.rule")}><code>{String(projection.application.ruleRef.rule_id)} / {String(projection.application.ruleRef.explicit_version)}</code></MetadataItem>
        <MetadataItem label={t("application.version")}><code>{projection.application.appliedActionVersion}</code></MetadataItem>
        <MetadataItem label={t("application.identity")}><TechnicalDetails value={projection.application.applicationRef} label={t("technical.reference")} /></MetadataItem>
      </Metadata>
      <p className="scientific-boundary">{t("application.boundary")}</p>
      <TechnicalDetails value={projection.application.raw} />
    </Card> : null}
    {projection.changedRequirements.length ? <ChangedRequirements rows={projection.changedRequirements} /> : null}
    <Callout title={t("limitation.title")}><p>{t("limitation.body")}</p></Callout>

    {entry ? <Card title={t("reassessment.title")} description={t("reassessment.description")} className="formal-reassessment">
      {!editorOpen ? <Button type="button" variant="primary" onClick={() => { setDraft(canonicalDraft); setEditorOpen(true); }}>
        {t("reassessment.open")}
      </Button> : <div className="reassessment-editor">
        <Callout title={t("editor.boundaryTitle")}><p>{t("editor.boundary")}</p></Callout>
        <TextArea
          label={t("editor.label")}
          hint={t("editor.hint")}
          value={draft}
          rows={Math.max(6, entry.requirements.at(-1)?.source_line ?? 6)}
          onChange={(event) => { setDraft(event.currentTarget.value); onReassessmentDraftChange(); }}
          error={!canonical ? t("editor.mismatch") : undefined}
        />
        {reassessmentErrorMessage ? <InlineValidation>{reassessmentErrorMessage}</InlineValidation> : null}
        <div className="button-row reassessment-editor__actions">
          <Button type="button" variant="secondary" disabled={reassessmentPending} onClick={() => { setEditorOpen(false); onReassessmentDraftChange(); }}>{t("editor.cancel")}</Button>
          <Button type="button" variant="primary" disabled={!canonical} loading={reassessmentPending} onClick={submit}>
            {onRetryReassessment ? t("editor.retry") : t("editor.analyze")}
          </Button>
        </div>
      </div>}
    </Card> : null}
  </section>;
}

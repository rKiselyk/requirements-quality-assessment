import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { ApplicabilityBadge, ExactValue, StatusBadge } from "../../components/scientific";
import { PageHeader } from "../../components/shell";
import { Callout, Card, UnavailableState } from "../../components/ui";
import {
  canonicalJson,
  selectProcessPage,
  type CheckpointProjection,
  type EvidenceAssociationProjection,
  type ProcessAssociationProjection,
  type ProcessStateProjection,
  type ProcessTransitionProjection,
} from "./projection";

function TechnicalDetails({ value, label }: { value: unknown; label: string }) {
  return <details className="process-technical"><summary>{label}</summary><pre>{canonicalJson(value)}</pre></details>;
}

function Metadata({ children }: { children: ReactNode }) {
  return <dl className="compact-metadata process-metadata">{children}</dl>;
}

function MetadataItem({ label, children }: { label: string; children: ReactNode }) {
  return <div><dt>{label}</dt><dd>{children}</dd></div>;
}

function Identity({ value, label }: { value: unknown; label: string }) {
  return <TechnicalDetails value={value} label={label} />;
}

function StateNode({ state, position }: { state: ProcessStateProjection; position: "predecessor" | "successor" }) {
  const { t } = useTranslation("process");
  return <article className="process-timeline__node process-state-node">
    <span className="process-timeline__eyebrow">{t(`timeline.${position}`)}</span>
    <h3>{t("state.title")}</h3>
    <code>{state.id} / {state.version}</code>
    <span><strong>{t("labels.stage")}</strong> <code>{state.stage}</code></span>
    <span><strong>{t("labels.artifact")}</strong> <code>{String(state.artifactRef.artifact_id)} / {String(state.artifactRef.artifact_version)}</code></span>
    {position === "successor" ? <span className="process-current-label">{t("timeline.currentSuccessor")}</span> : null}
  </article>;
}

function TransitionNode({ transition }: { transition: ProcessTransitionProjection }) {
  const { t } = useTranslation("process");
  return <article className="process-timeline__node process-transition-node">
    <span className="process-timeline__eyebrow">{t("timeline.transition")}</span>
    <h3>{t("transition.title")}</h3>
    <code>{transition.transitionId}</code>
    <div className="process-transition-refs">
      <Identity value={transition.artifactTransitionRef} label={t("labels.artifactTransition")} />
      <Identity value={transition.actionApplicationRef} label={t("labels.actionApplication")} />
      <Identity value={transition.reassessmentRef} label={t("labels.reassessment")} />
    </div>
  </article>;
}

function AssociationState({ status, applicability }: { status: string; applicability: string }) {
  return <div className="process-association__state"><StatusBadge code={status} /><ApplicabilityBadge code={applicability} /></div>;
}

function ComponentAssociation({ association }: { association: ProcessAssociationProjection }) {
  const { t } = useTranslation("process");
  return <li className="process-association">
    <header><code>{association.role}</code><AssociationState status={association.status} applicability={association.applicability} /></header>
    <div className="process-association__refs">
      <Identity value={association.ref} label={t("associations.resultRef")} />
      <Identity value={association.subjectOrScope} label={t("associations.subjectScope")} />
      <Identity value={association.source} label={t("associations.producingRef")} />
    </div>
    {association.reasonCodes.length ? <div className="technical-code-list">{association.reasonCodes.map((reason, index) => <code key={index}>{String(reason)}</code>)}</div> : null}
    <TechnicalDetails value={association.provenance} label={t("labels.provenance")} />
  </li>;
}

function EvidenceAssociation({ association }: { association: EvidenceAssociationProjection }) {
  const { t } = useTranslation("process");
  return <li className="process-association">
    <header><code>{association.role}</code><AssociationState status={association.status} applicability={association.applicability} /></header>
    <div className="process-association__refs">
      <Identity value={association.ref} label={t("associations.evidenceRef")} />
      <Identity value={association.artifactOrProduct} label={t("associations.artifactProduct")} />
      <Identity value={association.sourceOrCollection} label={t("associations.sourceCollection")} />
      {association.context !== null ? <Identity value={association.context} label={t("associations.context")} /> : null}
      {association.reuseDecision !== null ? <Identity value={association.reuseDecision} label={t("associations.reuseDecision")} /> : null}
    </div>
    {association.reasonCodes.length ? <div className="technical-code-list">{association.reasonCodes.map((reason, index) => <code key={index}>{String(reason)}</code>)}</div> : null}
    <TechnicalDetails value={association.provenance} label={t("labels.provenance")} />
  </li>;
}

function StateTrace({ state, label }: { state: ProcessStateProjection; label: string }) {
  const { t } = useTranslation("process");
  return <Card title={label} description={`${state.id} / ${state.version}`} className="process-state-trace">
    <details className="process-association-group">
      <summary>{t("associations.components")}</summary>
      <ol>{state.components.map((association, index) => <ComponentAssociation association={association} key={`${association.role}-${index}`} />)}</ol>
    </details>
    <details className="process-association-group">
      <summary>{t("associations.evidence")}</summary>
      <ol>{state.evidence.map((association, index) => <EvidenceAssociation association={association} key={`${association.role}-${index}`} />)}</ol>
    </details>
    <TechnicalDetails value={state.componentVersionSet} label={t("associations.componentVersions")} />
    <TechnicalDetails value={state.provenance} label={t("labels.provenance")} />
  </Card>;
}

function CurrentState({ state }: { state: ProcessStateProjection }) {
  const { t } = useTranslation("process");
  return <Card title={t("current.title")} description={t("current.description")} className="current-process-state">
    <Metadata>
      <MetadataItem label={t("labels.processStateId")}><code>{state.id}</code></MetadataItem>
      <MetadataItem label={t("labels.version")}><code>{state.version}</code></MetadataItem>
      <MetadataItem label={t("labels.stage")}><code>{state.stage}</code></MetadataItem>
      <MetadataItem label={t("labels.lineage")}><code>{state.lineageId}</code></MetadataItem>
      <MetadataItem label={t("labels.artifact")}><Identity value={state.artifactRef} label={t("technical.reference")} /></MetadataItem>
      <MetadataItem label={t("labels.assessment")}><Identity value={state.assessmentRef} label={t("technical.reference")} /></MetadataItem>
      <MetadataItem label={t("labels.predecessor")}><Identity value={state.predecessorRef} label={t("technical.reference")} /></MetadataItem>
      <MetadataItem label={t("labels.rule")}><code>{String(state.provenance.rule_ref && (state.provenance.rule_ref as Record<string, unknown>).rule_id)} / {String(state.provenance.rule_ref && (state.provenance.rule_ref as Record<string, unknown>).explicit_version)}</code></MetadataItem>
    </Metadata>
    <TechnicalDetails value={state.provenance} label={t("labels.provenance")} />
  </Card>;
}

function CheckpointCard({ checkpoint }: { checkpoint: CheckpointProjection }) {
  const { t } = useTranslation("process");
  return <Card title={`${t("checkpoints.item")} — ${checkpoint.checkpointId} / ${checkpoint.checkpointVersion}`} className="checkpoint-card">
    <div className="checkpoint-context">
      <span>{t("labels.processState")}: <code>{String(checkpoint.processStateRef.process_state_id)} / {checkpoint.processStateVersion}</code></span>
      <span>{t("labels.artifact")}: <code>{String(checkpoint.artifactRef.artifact_id)} / {String(checkpoint.artifactRef.artifact_version)}</code></span>
    </div>
    <div className="checkpoint-grid">
      <section aria-label={t("checkpoints.selected.title")}>
        <h3>{t("checkpoints.selected.title")}</h3>
        <AssociationState status={checkpoint.selectedResult.status} applicability={checkpoint.selectedResult.applicability} />
        <Metadata>
          <MetadataItem label={t("checkpoints.selected.identity")}><code>{checkpoint.selectedResult.identity}</code></MetadataItem>
          <MetadataItem label={t("checkpoints.selected.value")}><ExactValue value={checkpoint.selectedResult.exactValue} /></MetadataItem>
          {checkpoint.selectedResult.reasonCodes.length > 0 ? <MetadataItem label={t("checkpoints.selected.sourceReasons")}>
            <span className="technical-code-list">{checkpoint.selectedResult.reasonCodes.map((reason, index) => <code key={index}>{String(reason)}</code>)}</span>
          </MetadataItem> : null}
          <MetadataItem label={t("checkpoints.selected.resultRef")}><Identity value={checkpoint.selectedResult.resultRef} label={t("technical.reference")} /></MetadataItem>
          <MetadataItem label={t("checkpoints.selected.governingRef")}><Identity value={checkpoint.selectedResult.governingRef} label={t("technical.reference")} /></MetadataItem>
        </Metadata>
      </section>
      <section aria-label={t("checkpoints.policy.title")}>
        <h3>{t("checkpoints.policy.title")}</h3>
        <Metadata>
          <MetadataItem label={t("checkpoints.policy.identity")}><code>{checkpoint.policy.policyId} / {checkpoint.policy.policyVersion}</code></MetadataItem>
          <MetadataItem label={t("checkpoints.policy.source")}><Identity value={checkpoint.policy.sourceRef} label={t("technical.reference")} /></MetadataItem>
          <MetadataItem label={t("checkpoints.policy.provider")}><Identity value={checkpoint.policy.providerRef} label={t("technical.reference")} /></MetadataItem>
          <MetadataItem label={t("checkpoints.policy.comparator")}><code>{checkpoint.policy.comparator}</code></MetadataItem>
          <MetadataItem label={t("checkpoints.policy.threshold")}><ExactValue value={checkpoint.policy.threshold} /></MetadataItem>
          <MetadataItem label={t("checkpoints.policy.contract")}><Identity value={checkpoint.policy.governingContractRef} label={t("technical.reference")} /></MetadataItem>
        </Metadata>
        <p className="record-explanation">{checkpoint.policy.rationale}</p>
      </section>
      <section aria-label={t("checkpoints.evaluation.title")}>
        <h3>{t("checkpoints.evaluation.title")}</h3>
        <StatusBadge code={checkpoint.outcome} />
        <Metadata>
          <MetadataItem label={t("checkpoints.evaluation.reason")}><code>{checkpoint.reasonCode}</code></MetadataItem>
          <MetadataItem label={t("checkpoints.evaluation.rule")}><Identity value={checkpoint.evaluatorRuleRef} label={t("technical.reference")} /></MetadataItem>
          <MetadataItem label={t("checkpoints.evaluation.contract")}><Identity value={checkpoint.checkpointContractRef} label={t("technical.reference")} /></MetadataItem>
        </Metadata>
      </section>
    </div>
    <Callout title={t("checkpoints.limitation.title")}>
      <p>{checkpoint.outcome === "SATISFIED" ? t("checkpoints.limitation.satisfied") : t("checkpoints.limitation.general")}</p>
    </Callout>
    <TechnicalDetails value={checkpoint.provenance} label={t("labels.provenance")} />
  </Card>;
}

export function ProcessPage({ result }: { result: CanonicalAnalyzeResponse }) {
  const { t } = useTranslation("process");
  const projection = selectProcessPage(result);
  if (projection.kind === "UNAVAILABLE") return <section className="process-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} />
    <UnavailableState title={t("unavailable.title")} description={t("unavailable.description")} />
    <p className="unavailable-reason"><span>{t("unavailable.reason")}</span><code>{projection.reasonCode}</code></p>
  </section>;
  if (projection.kind === "MALFORMED") return <section className="process-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} />
    <UnavailableState title={t("malformed.title")} description={t("malformed.description")} />
  </section>;

  return <section className="process-page">
    <PageHeader title={t("title")} subtitle={t("subtitle")} />
    <Card title={t("timeline.title")} description={t("timeline.description")} className="process-timeline-card">
      <div className="process-timeline">
        <StateNode state={projection.predecessor} position="predecessor" />
        <span className="process-timeline__arrow" aria-hidden="true">→</span>
        <TransitionNode transition={projection.transition} />
        <span className="process-timeline__arrow" aria-hidden="true">→</span>
        <StateNode state={projection.successor} position="successor" />
      </div>
      <TechnicalDetails value={projection.transition.provenance} label={t("transition.provenance")} />
    </Card>
    <CurrentState state={projection.current} />
    <div className="process-state-traces">
      <StateTrace state={projection.predecessor} label={t("timeline.predecessorTrace")} />
      <StateTrace state={projection.successor} label={t("timeline.successorTrace")} />
    </div>
    <section className="checkpoint-section" aria-labelledby="checkpoint-heading">
      <header className="section-heading-row"><div><h2 id="checkpoint-heading">{t("checkpoints.title")}</h2><p>{t("checkpoints.description")}</p></div></header>
      {projection.checkpointPopulationMalformed ? <UnavailableState title={t("checkpoints.malformedPopulation.title")} description={t("checkpoints.malformedPopulation.description")} /> : null}
      {!projection.checkpointPopulationMalformed && projection.checkpoints.length === 0
        ? <UnavailableState title={t("checkpoints.absent.title")} description={t("checkpoints.absent.description")} /> : null}
      {projection.checkpoints.map((entry, index) => entry.kind === "AVAILABLE"
        ? <CheckpointCard checkpoint={entry.value} key={`${entry.value.checkpointId}-${entry.value.checkpointVersion}-${index}`} />
        : <Card title={t("checkpoints.malformedItem.title", { index: index + 1 })} className="checkpoint-card checkpoint-card--malformed" key={index}>
            <p className="malformed-record">{t("checkpoints.malformedItem.description")}</p>
            <TechnicalDetails value={entry.raw} label={t("technical.details")} />
          </Card>)}
    </section>
  </section>;
}

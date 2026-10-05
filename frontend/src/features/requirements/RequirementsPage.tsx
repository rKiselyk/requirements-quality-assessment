import { useCallback, useMemo, useRef, useState, type MouseEvent } from "react";
import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { EvidenceBadge, EvidenceDrawer, EvidenceHighlighter, ExactValue, StatusBadge } from "../../components/scientific";
import { PageHeader } from "../../components/shell";
import { Card, EmptyState, Tabs } from "../../components/ui";
import {
  characteristicKeys,
  featureKeys,
  selectFullProfile,
  selectRequirements,
  type CharacteristicKey,
  type EvidenceProjection,
  type FindingProjection,
  type RequirementProjection,
} from "./projection";

function MalformedRecord({ compact = false }: { compact?: boolean }) {
  const { t } = useTranslation("requirements");
  return <p className={compact ? "malformed-record malformed-record--compact" : "malformed-record"}>{t("malformed.record")}</p>;
}

function technicalValue(value: string | null, absent: string) {
  return value ? <code>{value}</code> : <span className="scientific-boundary">{absent}</span>;
}

function TraceBlock({
  requirement,
  characteristicKey,
  onSelectEvidence,
}: {
  requirement: RequirementProjection;
  characteristicKey: CharacteristicKey;
  onSelectEvidence: (evidence: EvidenceProjection, event: MouseEvent<HTMLButtonElement>) => void;
}) {
  const { t } = useTranslation("requirements");
  const assessment = requirement.characteristics[characteristicKey];
  const trace = assessment && requirement.trace?.characteristics.find((item) => item.characteristicId === assessment.characteristicId);
  const evidenceById = new Map(requirement.evidence.flatMap((item) => item ? [[item.evidenceId, item] as const] : []));
  if (!requirement.trace || !trace) return <MalformedRecord compact />;
  return (
    <details className="quality-trace">
      <summary>{t("trace.heading")}</summary>
      <dl className="compact-metadata">
        <div><dt>{t("trace.governingRule")}</dt><dd><code>{trace.governingRuleId}</code></dd></div>
        <div><dt>{t("trace.decisionCode")}</dt><dd><code>{trace.decisionCode}</code></dd></div>
        <div><dt>{t("trace.coverageProfile")}</dt><dd><code>{requirement.trace.coverageProfileId}</code></dd></div>
      </dl>
      <ul className="trace-inputs">
        {trace.inputs.map((input, index) => (
          <li key={`${input.featureId}-${index}`}>
            <div className="trace-input__identity">
              <code>{input.featureId}</code>
              <code>{input.effectCode}</code>
              {input.applicability ? <code>{input.applicability}</code> : null}
            </div>
            <span>{t("trace.references", { observations: input.observationIndexes.join(", ") || "—", diagnostics: input.diagnosticIndexes.join(", ") || "—" })}</span>
            {input.observationIndexes.length ? (
              <ol className="trace-observations">
                {input.observationIndexes.map((observationIndex) => {
                  const feature = featureKeys.map((key) => requirement.features[key]).find((item) => item?.featureId === input.featureId);
                  const observation = feature?.observations[observationIndex];
                  if (!observation) return <li className="trace-observation--malformed" key={observationIndex}>{t("trace.malformedObservation", { index: observationIndex })}</li>;
                  return (
                    <li key={observationIndex}>
                      <div className="trace-observation__heading">
                        <strong>{t("trace.observation", { index: observation.index })}</strong>
                        {observation.observationId ? <code>{observation.observationId}</code> : null}
                        {observation.featureId ? <code>{observation.featureId}</code> : null}
                        {observation.kind ? <code>{observation.kind}</code> : null}
                      </div>
                      {observation.evidenceRefs.length ? (
                        <div className="trace-observation__evidence">
                          <span>{t("trace.observationEvidence")}</span>
                          {observation.evidenceRefs.map((ref) => {
                            const linked = evidenceById.get(ref);
                            return linked
                              ? <EvidenceBadge key={ref} evidenceId={linked.evidenceId} kind={linked.featureId} sourceText={linked.text} onClick={(event) => onSelectEvidence(linked, event)} />
                              : <span className="dangling-reference" key={ref}><code>{ref}</code> {t("trace.danglingEvidence")}</span>;
                          })}
                        </div>
                      ) : <span className="trace-observation__no-evidence">{t("trace.noExplicitEvidence")}</span>}
                    </li>
                  );
                })}
              </ol>
            ) : null}
          </li>
        ))}
      </ul>
      {trace.findingRefs.length ? <p>{t("trace.findingRefs")}: {trace.findingRefs.map((id) => <code key={id}>{id}</code>)}</p> : null}
    </details>
  );
}

function QualityCards({
  requirement,
  onSelectEvidence,
}: {
  requirement: RequirementProjection;
  onSelectEvidence: (evidence: EvidenceProjection, event: MouseEvent<HTMLButtonElement>) => void;
}) {
  const { t } = useTranslation("requirements");
  return (
    <section className="requirements-section" aria-labelledby="requirement-quality-heading">
      <h2 id="requirement-quality-heading">{t("quality.title")}</h2>
      <div className="requirement-quality-grid">
        {characteristicKeys.map((key) => {
          const assessment = requirement.characteristics[key];
          return (
            <article className="requirement-quality-card" key={key}>
              <h3>{t(`properties.${key}`)}</h3>
              {assessment ? (
                <>
                  <ExactValue value={assessment.value} fallback={t("quality.noNumericValue")} />
                  <StatusBadge code={assessment.state} />
                  <dl className="compact-metadata">
                    <div><dt>{t("quality.characteristicId")}</dt><dd><code>{assessment.characteristicId}</code></dd></div>
                    <div><dt>{t("quality.assessmentRule")}</dt><dd>{technicalValue(assessment.assessmentRuleId, t("quality.noRule"))}</dd></div>
                  </dl>
                  <p className="assessment-explanation">{assessment.explanation}</p>
                  <TraceBlock requirement={requirement} characteristicKey={key} onSelectEvidence={onSelectEvidence} />
                </>
              ) : <MalformedRecord />}
            </article>
          );
        })}
      </div>
    </section>
  );
}

function PropertyProfile({ result, requirement }: { result: CanonicalAnalyzeResponse; requirement: RequirementProjection }) {
  const { t } = useTranslation("requirements");
  const fullProfile = selectFullProfile(result, requirement.requirement);
  return (
    <section className="requirements-section property-profile" aria-labelledby="property-profile-heading">
      <h2 id="property-profile-heading">{t("profile.title")}</h2>
      <p className="section-description">{t("profile.description")}</p>
      <div className="table-scroll" tabIndex={0} role="region" aria-label={t("profile.tableLabel")}>
        <table className="data-table property-profile__table">
          <thead><tr><th>{t("profile.property")}</th><th>{t("profile.origin")}</th><th>{t("profile.state")}</th><th>{t("profile.result")}</th><th>{t("profile.explanation")}</th></tr></thead>
          <tbody>
            {characteristicKeys.map((key) => {
              const assessment = requirement.characteristics[key];
              return (
                <tr key={key}>
                  <th scope="row">{t(`properties.${key}`)}</th>
                  <td><span>{t("origins.automatic")}</span> <code>AUTOMATIC</code></td>
                  {assessment ? <><td><StatusBadge code={assessment.state} /></td><td><ExactValue value={assessment.value} fallback={t("quality.noNumericValue")} compact /></td><td>{assessment.explanation}</td></> : <td colSpan={3}><MalformedRecord compact /></td>}
                </tr>
              );
            })}
            {fullProfile.kind === "PRESENT" ? fullProfile.external.map((property) => (
              <tr key={property.propertyId}>
                <th scope="row">{t(`properties.${property.propertyId}`)}</th>
                <td><span>{t("origins.external")}</span> <code>EXTERNAL_EXPERT</code></td>
                <td><StatusBadge code={property.state} /></td>
                <td>{property.judgmentId ? <code>{property.judgmentId}</code> : <span className="scientific-boundary">{t("profile.noJudgment")}</span>}</td>
                <td>
                  <p>{property.explanation}</p>
                  <details className="provenance-detail"><summary>{t("profile.provenance")}</summary><pre>{JSON.stringify(property.provenance, null, 2)}</pre></details>
                </td>
              </tr>
            )) : null}
          </tbody>
        </table>
      </div>
      {fullProfile.kind === "ABSENT" ? <div className="neutral-note" role="note"><strong>{t("profile.extendedAbsentTitle")}</strong><p>{t("profile.extendedAbsentDescription")}</p></div> : null}
      {fullProfile.kind === "MALFORMED" ? <div className="neutral-note" role="note"><strong>{t("malformed.title")}</strong><p>{t("malformed.profile")}</p></div> : null}
    </section>
  );
}

function Findings({ requirement, onSelectEvidence }: { requirement: RequirementProjection; onSelectEvidence: (evidence: EvidenceProjection, event: MouseEvent<HTMLButtonElement>) => void }) {
  const { t } = useTranslation("requirements");
  const findings = characteristicKeys.flatMap((key) => requirement.characteristics[key]?.findings ?? []);
  const evidenceById = new Map(requirement.evidence.flatMap((item) => item ? [[item.evidenceId, item] as const] : []));
  if (!findings.length) return <p className="empty-records">{t("findings.empty")}</p>;
  return (
    <ol className="finding-list">
      {findings.map((finding, index) => finding ? (
        <li key={`${finding.findingId}-${index}`}>
          <div className="record-heading"><code>{finding.findingId}</code><span className="finding-kind"><span>{t(`findingKinds.${finding.kind}`, { defaultValue: finding.kind })}</span><code>{finding.kind}</code></span></div>
          <p>{finding.explanation}</p>
          <dl className="compact-metadata">
            <div><dt>{t("findings.characteristic")}</dt><dd><code>{finding.characteristicId}</code></dd></div>
            <div><dt>{t("findings.code")}</dt><dd><code>{finding.code}</code></dd></div>
            <div><dt>{t("findings.rule")}</dt><dd><code>{finding.ruleId}</code></dd></div>
            <div><dt>{t("findings.criterion")}</dt><dd>{technicalValue(finding.criterionId, t("findings.noCriterion"))}</dd></div>
          </dl>
          {finding.evidenceRefs.length ? <div className="evidence-ref-list"><strong>{t("findings.evidenceRefs")}</strong>{finding.evidenceRefs.map((ref) => {
            const linked = evidenceById.get(ref);
            return linked
              ? <EvidenceBadge key={ref} evidenceId={linked.evidenceId} kind={linked.featureId} sourceText={linked.text} onClick={(event) => onSelectEvidence(linked, event)} />
              : <span className="dangling-reference" key={ref}><code>{ref}</code> {t("findings.danglingEvidence")}</span>;
          })}</div> : null}
        </li>
      ) : <li key={`malformed-${index}`}><MalformedRecord /></li>)}
    </ol>
  );
}

function Diagnostics({ requirement }: { requirement: RequirementProjection }) {
  const { t } = useTranslation("requirements");
  const count = featureKeys.reduce((total, key) => total + (requirement.features[key]?.diagnostics.length ?? 0), 0);
  const hasMalformedFeature = featureKeys.some((key) => requirement.features[key] === null);
  if (!count && !hasMalformedFeature) return <p className="empty-records">{t("diagnostics.empty")}</p>;
  return (
    <div className="diagnostic-groups">
      {featureKeys.map((key) => {
        const feature = requirement.features[key];
        if (!feature) return <section key={key}><h3>{t(`features.${key}`)}</h3><MalformedRecord /></section>;
        if (!feature.diagnostics.length) return null;
        return (
          <section key={key}>
            <h3>{t(`features.${key}`)} <code>{feature.featureId}</code></h3>
            <ol className="diagnostic-list">
              {feature.diagnostics.map((item, index) => item ? (
                <li key={`${item.code}-${index}`}>
                  <div className="record-heading"><code>{item.code}</code><code>{item.ruleId}</code></div>
                  <p>{item.explanation}</p>
                  {item.candidateSpan ? <div className="candidate-span"><strong>{t("diagnostics.candidateSpan")}</strong><q>{item.candidateSpan.text}</q><span>{t("diagnostics.offsets", { start: item.candidateSpan.startOffset, end: item.candidateSpan.endOffset })}</span><small>{t("diagnostics.notEvidence")}</small></div> : null}
                </li>
              ) : <li key={`malformed-${index}`}><MalformedRecord /></li>)}
            </ol>
          </section>
        );
      })}
    </div>
  );
}

export function RequirementsPage({
  result,
  selectedRequirementId: requestedRequirementId = null,
  onSelectRequirement,
}: {
  result: CanonicalAnalyzeResponse;
  selectedRequirementId?: string | null;
  onSelectRequirement?: (requirementId: string) => void;
}) {
  const { t } = useTranslation("requirements");
  const requirementEntries = useMemo(() => selectRequirements(result), [result]);
  const requirements = requirementEntries.flatMap((entry) => entry.kind === "VALID" ? [entry.value] : []);
  const malformedRequirementCount = requirementEntries.length - requirements.length;
  const [localSelectedRequirementId, setLocalSelectedRequirementId] = useState<string | null>(null);
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string | null>(null);
  const evidenceTrigger = useRef<HTMLButtonElement | null>(null);
  const selectedRequirementId = requestedRequirementId ?? localSelectedRequirementId;
  const selected = requirements.find((item) => item.requirement.id === selectedRequirementId) ?? requirements[0] ?? null;
  const selectedEvidence = selected?.evidence.find((item) => item?.evidenceId === selectedEvidenceId) ?? null;

  const selectEvidence = (evidence: EvidenceProjection, event: MouseEvent<HTMLButtonElement>) => {
    evidenceTrigger.current = event.currentTarget;
    setSelectedEvidenceId(evidence.evidenceId);
  };
  const closeEvidence = useCallback(() => {
    setSelectedEvidenceId(null);
    evidenceTrigger.current?.focus();
  }, []);

  if (!selected) {
    return (
      <section className="requirements-page">
        <PageHeader title={t("title")} subtitle={t("subtitle")} metadata={<span>{t("header.count", { count: requirementEntries.length })}</span>} />
        {malformedRequirementCount ? <div className="neutral-note malformed-requirements-note" role="note"><strong>{t("malformed.requirementsTitle", { count: malformedRequirementCount })}</strong><p>{t("malformed.requirementsDescription")}</p></div> : null}
        <EmptyState title={t("empty.title")} description={t("empty.description")} />
      </section>
    );
  }

  const findingCount = characteristicKeys.reduce((total, key) => total + (selected.characteristics[key]?.findings.length ?? 0), 0);
  const diagnosticCount = featureKeys.reduce((total, key) => total + (selected.features[key]?.diagnostics.length ?? 0), 0);
  const linkedFindings = characteristicKeys.flatMap((key) => selected.characteristics[key]?.findings ?? [])
    .flatMap((finding: FindingProjection | null) => finding && selectedEvidence && finding.evidenceRefs.includes(selectedEvidence.evidenceId) ? [finding] : []);

  return (
    <section className="requirements-page">
      <PageHeader title={t("title")} subtitle={t("subtitle")} metadata={<><span>{t("header.selected")}: <code>{selected.requirement.id}</code></span><span>{t("header.count", { count: requirementEntries.length })}</span></>} />
      {malformedRequirementCount ? <div className="neutral-note malformed-requirements-note" role="note"><strong>{t("malformed.requirementsTitle", { count: malformedRequirementCount })}</strong><p>{t("malformed.requirementsDescription")}</p></div> : null}
      <div className="requirements-master-detail">
        <nav className="requirement-navigator" aria-label={t("navigator.label")}>
          <div className="requirement-navigator__heading"><h2>{t("navigator.title")}</h2><span>{requirementEntries.length}</span></div>
          <ol>
            {requirementEntries.map((entry) => entry.kind === "VALID" ? (
              <li key={`${entry.value.requirement.id}-${entry.value.requirement.sourceLine}-${entry.position}`}>
                <button
                  type="button"
                  aria-current={entry.value === selected ? "true" : undefined}
                  onClick={() => {
                    setLocalSelectedRequirementId(entry.value.requirement.id);
                    onSelectRequirement?.(entry.value.requirement.id);
                    setSelectedEvidenceId(null);
                  }}
                >
                  <strong>{entry.value.requirement.id}</strong>
                  <span>{t("navigator.sourceLine", { line: entry.value.requirement.sourceLine })}</span>
                  <small>{entry.value.requirement.text}</small>
                </button>
              </li>
            ) : (
              <li className="requirement-navigator__malformed" key={`malformed-${entry.position}`}>
                <strong>{t("malformed.requirementRow")}</strong>
                <span>{t("malformed.responsePosition", { position: entry.position })}</span>
              </li>
            ))}
          </ol>
        </nav>
        <article className="requirement-detail">
          <Card className="requirement-source-card">
            <div className="requirement-source-card__identity">
              <div><span className="primitive-label">{t("source.requirement")}</span><h2>{selected.requirement.id}</h2></div>
              <span>{t("source.sourceLine")}: <strong>{selected.requirement.sourceLine}</strong></span>
            </div>
            <EvidenceHighlighter requirementText={selected.requirement.text} evidence={selectedEvidence} mismatchMessage={t("evidence.spanMismatch")} />
          </Card>

          <QualityCards requirement={selected} onSelectEvidence={selectEvidence} />
          <PropertyProfile result={result} requirement={selected} />

          <section className="requirements-section" aria-labelledby="evidence-heading">
            <h2 id="evidence-heading">{t("evidence.title")}</h2>
            <p className="section-description">{t("evidence.description")}</p>
            {selected.evidence.length ? (
              <ol className="evidence-list">
                {selected.evidence.map((item, index) => item ? (
                  <li key={`${item.evidenceId}-${index}`}>
                    <EvidenceBadge evidenceId={item.evidenceId} kind={item.featureId} sourceText={item.text} aria-pressed={item.evidenceId === selectedEvidenceId} onClick={(event) => selectEvidence(item, event)} />
                    <q>{item.text}</q>
                    <span>{t("evidence.rule")}: <code>{item.ruleId}</code></span>
                  </li>
                ) : <li key={`malformed-${index}`}><MalformedRecord /></li>)}
              </ol>
            ) : <p className="empty-records">{t("evidence.empty")}</p>}
          </section>

          <section className="requirements-section findings-diagnostics" aria-labelledby="findings-diagnostics-heading">
            <h2 id="findings-diagnostics-heading">{t("records.title")}</h2>
            <Tabs
              label={t("records.tabsLabel")}
              items={[
                { id: "findings", label: t("records.findings", { count: findingCount }), content: <Findings requirement={selected} onSelectEvidence={selectEvidence} /> },
                { id: "diagnostics", label: t("records.diagnostics", { count: diagnosticCount }), content: <Diagnostics requirement={selected} /> },
              ]}
            />
          </section>
        </article>
      </div>
      <EvidenceDrawer
        evidence={selectedEvidence}
        sourceLine={selected.requirement.sourceLine}
        linkedFindings={linkedFindings}
        labels={{
          heading: t("drawer.heading"), close: t("drawer.close"), requirement: t("drawer.requirement"), sourceLine: t("drawer.sourceLine"),
          feature: t("drawer.feature"), exactText: t("drawer.exactText"), startOffset: t("drawer.startOffset"), endOffset: t("drawer.endOffset"),
          rule: t("drawer.rule"), linkedFindings: t("drawer.linkedFindings"), findingKind: t("drawer.findingKind"),
          findingCode: t("drawer.findingCode"), findingRule: t("drawer.findingRule"), findingCharacteristic: t("drawer.findingCharacteristic"),
          findingExplanation: t("drawer.findingExplanation"),
        }}
        onClose={closeEvidence}
      />
    </section>
  );
}

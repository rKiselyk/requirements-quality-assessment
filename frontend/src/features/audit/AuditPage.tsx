import { useCallback, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { EvidenceDrawer } from "../../components/scientific";
import { PageHeader } from "../../components/shell";
import { UnavailableState } from "../../components/ui";
import { AuditTree, type AuditTreeLabels } from "./AuditTree";
import { buildEvidenceIndex, type AuditEvidenceTarget } from "./evidenceIndex";
import { buildAuditGroups, selectAuditAvailability } from "./tree";

const friendlyFieldKeys = new Set([
  "contract_version", "analysis_case", "controlled_scenario", "requirements", "specification", "section_availability",
  "full_model", "reassessment_context", "limitations", "initial_specification_assessment", "metric_profile", "criterion_binding",
  "observation_resolution", "conformance", "feature_profile", "observed_product_quality", "prediction", "full_quality_profiles",
  "problem_resolutions", "defect_population", "defect_quality_relations", "risk_assessments", "quantitative_risk_assessments",
  "corrective_action_resolution", "initial_specification", "external_revision", "action_application", "revised_specification",
  "reassessment", "comparisons", "process_v1", "process_v2", "process_transition", "checkpoint_evaluations",
]);

export function AuditPage({ result }: { result: CanonicalAnalyzeResponse }) {
  const { t } = useTranslation("audit");
  const availability = useMemo(() => selectAuditAvailability(result), [result]);
  const groups = useMemo(() => buildAuditGroups(result), [result]);
  const evidenceIndex = useMemo(() => buildEvidenceIndex(result), [result]);
  const [openGroups, setOpenGroups] = useState(() => new Set(["response", "assessment", "fullModel", "reassessmentContext"]));
  const [selectedEvidence, setSelectedEvidence] = useState<AuditEvidenceTarget | null>(null);
  const evidenceTrigger = useRef<HTMLButtonElement | null>(null);
  const openEvidence = useCallback((target: AuditEvidenceTarget, trigger: HTMLButtonElement) => {
    evidenceTrigger.current = trigger;
    setSelectedEvidence(target);
  }, []);
  const closeEvidence = useCallback(() => {
    setSelectedEvidence(null);
    evidenceTrigger.current?.focus();
  }, []);

  const labels: AuditTreeLabels = {
    array: t("types.array"), object: t("types.object"), fields: t("types.fields"), items: t("types.items"),
    canonicalField: t("tree.canonicalField"), value: t("tree.value"), nullValue: t("tree.null"),
    emptyString: t("tree.emptyString"), unsupported: t("tree.unsupported"), openEvidence: t("tree.openEvidence"),
    fieldLabel: (key) => friendlyFieldKeys.has(key) ? t(`fields.${key}`) : key,
  };

  if (availability.kind !== "AVAILABLE") {
    const malformed = availability.kind === "MALFORMED";
    return (
      <section className="audit-page">
        <PageHeader title={t("title")} subtitle={t("subtitle")} />
        <UnavailableState
          title={malformed ? t("availability.malformedTitle") : t("availability.unavailableTitle")}
          description={malformed ? t("availability.malformedDescription") : t("availability.unavailableDescription")}
          action={!malformed && availability.reasonCode !== null ? <code className="audit-unavailable-reason">{availability.reasonCode}</code> : undefined}
        />
      </section>
    );
  }

  return (
    <section className="audit-page">
      <PageHeader title={t("title")} subtitle={t("subtitle")} />
      <h2 className="audit-page__heading">{t("fullModel")}</h2>
      <div className="audit-groups">
        {groups.map((group) => (
          <details
            className="audit-group"
            open={openGroups.has(group.id)}
            key={group.id}
            onToggle={(event) => {
              const isOpen = event.currentTarget.open;
              setOpenGroups((current) => {
                if (current.has(group.id) === isOpen) return current;
                const next = new Set(current);
                if (isOpen) next.add(group.id); else next.delete(group.id);
                return next;
              });
            }}
          >
            <summary>
              <span>{t(`groups.${group.id}`)}</span>
              {group.canonicalKey ? <code>{group.canonicalKey}</code> : null}
            </summary>
            <AuditTree
              value={group.value}
              path={group.path}
              labels={labels}
              evidenceIndex={evidenceIndex}
              onOpenEvidence={openEvidence}
            />
          </details>
        ))}
      </div>
      <EvidenceDrawer
        evidence={selectedEvidence?.evidence ?? null}
        sourceLine={selectedEvidence?.sourceLine ?? null}
        linkedFindings={selectedEvidence?.linkedFindings ?? []}
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

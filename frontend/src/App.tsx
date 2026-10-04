import { useState } from "react";
import { useTranslation } from "react-i18next";
import { AppShell, PageHeader, type NavigationItem } from "./components/shell";
import {
  Accordion, Button, Callout, Card, DataTable, EmptyState, FileDropzone,
  IconButton, InlineValidation, LoadingProgress, MetricCard, Tabs, TextArea,
  TextInput, Tooltip, UnavailableState, type DataTableColumn,
} from "./components/ui";
import { ApplicabilityBadge, EvidenceBadge, ExactValue, StatusBadge, type ScientificCode } from "./components/scientific";

export const DEMO_REQUIREMENT_SOURCE_TEXT = "Система повинна зберегти E-DEMO-001 без змін.";
export const DEMO_EVIDENCE_SOURCE_TEXT = "E-DEMO-001 без змін";

interface DemoRecord {
  id: string;
  value: { numerator: string; denominator: string } | null;
  status: ScientificCode;
}

const demoRecords: readonly DemoRecord[] = [
  { id: "DEMO-001", value: { numerator: "5", denominator: "6" }, status: "COMPUTED" },
  { id: "DEMO-002", value: null, status: "UNKNOWN" },
  { id: "DEMO-003", value: null, status: "NOT_APPLICABLE" },
];

export function App() {
  const { t } = useTranslation(["common", "input", "assessment"]);
  const [activeId, setActiveId] = useState("foundation");
  const navigation: readonly NavigationItem[] = [
    { id: "foundation", label: t("common:navigation.foundation") },
    { id: "components", label: t("common:navigation.components") },
    { id: "scientific", label: t("common:navigation.scientific") },
  ];
  const columns: readonly DataTableColumn<DemoRecord>[] = [
    { key: "id", header: t("assessment:primitives.demoRecord"), render: (row) => <code>{row.id}</code> },
    { key: "value", header: t("assessment:primitives.exactValue"), render: (row) => <ExactValue value={row.value} compact /> },
    { key: "status", header: t("assessment:primitives.canonicalState"), render: (row) => <StatusBadge code={row.status} /> },
  ];

  return (
    <AppShell
      navigation={navigation}
      activeNavigationId={activeId}
      onNavigate={(id) => {
        setActiveId(id);
        document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
      }}
      headerActions={<Button variant="quiet">{t("common:actions.demo")}</Button>}
    >
      <div className="showcase">
        <PageHeader
          title={t("common:page.title")}
          subtitle={t("common:page.subtitle")}
          metadata={<><code>FOUNDATION_DEMO</code><span>{t("common:page.notConnected")}</span></>}
          actions={<Tooltip content={t("common:page.aboutTooltip")}><IconButton label={t("common:page.about")} icon="?" /></Tooltip>}
        />

        <Callout title={t("common:showcase.title")}>{t("common:showcase.description")}</Callout>

        <section id="foundation" className="showcase__section" aria-labelledby="foundation-title">
          <div className="section-heading"><div><span className="section-heading__eyebrow">{t("common:showcase.shellEyebrow")}</span><h2 id="foundation-title">{t("common:showcase.foundation")}</h2></div></div>
          <div className="metric-grid">
            <MetricCard label={t("assessment:metrics.completenessDemo")} value={{ numerator: "5", denominator: "6" }} status="COMPUTED" detail={t("assessment:metrics.staticExactInput")} />
            <MetricCard label={t("assessment:metrics.verifiabilityDemo")} value={null} status="UNKNOWN" detail={t("assessment:metrics.noNumericValue")} />
            <MetricCard label={t("assessment:metrics.unambiguityDemo")} value={null} status="NOT_APPLICABLE" detail={t("assessment:metrics.notZero")} />
          </div>
          <Card title={t("common:showcase.sharedCard")} description={t("common:showcase.sharedCardDescription")}>
            <div className="button-row">
              <Button variant="primary">{t("common:actions.primary")}</Button>
              <Button>{t("common:actions.secondary")}</Button>
              <Button variant="quiet">{t("common:actions.quiet")}</Button>
              <IconButton label={t("common:actions.moreInformation")} icon="⋯" />
            </div>
          </Card>
        </section>

        <section id="components" className="showcase__section" aria-labelledby="components-title">
          <div className="section-heading"><div><span className="section-heading__eyebrow">{t("common:showcase.reusableEyebrow")}</span><h2 id="components-title">{t("common:showcase.genericComponents")}</h2></div></div>
          <div className="showcase-grid">
            <Card title={t("input:cardTitle")}>
              <div className="form-stack">
                <TextInput label={t("input:artifactLabel")} placeholder={t("input:artifactPlaceholder")} hint={t("input:artifactHint")} />
                <TextArea label={t("input:requirementText")} rows={4} defaultValue={DEMO_REQUIREMENT_SOURCE_TEXT} hint={t("input:requirementHint")} />
                <FileDropzone label={t("input:dropzoneLabel")} description={t("input:dropzoneDescription")} />
                <InlineValidation>{t("input:exampleValidation")}</InlineValidation>
              </div>
            </Card>
            <Card title={t("common:showcase.feedback")}>
              <div className="form-stack">
                <LoadingProgress label={t("assessment:feedback.progress")} />
                <UnavailableState title={t("assessment:feedback.unavailableTitle")} description={t("assessment:feedback.unavailableDescription")} />
                <EmptyState title={t("assessment:feedback.emptyTitle")} description={t("assessment:feedback.emptyDescription")} />
              </div>
            </Card>
          </div>
          <Card title={t("common:showcase.disclosure")}>
            <Tabs label={t("assessment:tabs.label")} items={[
              { id: "summary", label: t("assessment:tabs.summary"), content: <p>{t("assessment:tabs.summaryContent")}</p> },
              { id: "trace", label: t("assessment:tabs.trace"), content: <p><code>RULE-DEMO-001</code> {t("assessment:tabs.traceContent")}</p> },
            ]} />
            <Accordion items={[
              { id: "details", title: t("assessment:tabs.technicalDetail"), content: <p>{t("assessment:tabs.technicalDetailContent")}</p> },
              { id: "provenance", title: t("assessment:tabs.provenance"), content: <p>{t("assessment:tabs.provenanceContent")}</p> },
            ]} />
          </Card>
        </section>

        <section id="scientific" className="showcase__section" aria-labelledby="scientific-title">
          <div className="section-heading"><div><span className="section-heading__eyebrow">{t("common:showcase.presentationOnly")}</span><h2 id="scientific-title">{t("common:showcase.scientificPrimitives")}</h2></div></div>
          <Card title={t("assessment:primitives.cardTitle")}>
            <div className="primitive-row">
              <div><span className="primitive-label">{t("assessment:primitives.structuredRational")}</span><ExactValue value={{ numerator: "2", denominator: "3" }} /></div>
              <div><span className="primitive-label">{t("assessment:primitives.status")}</span><StatusBadge code="COMPUTED" /></div>
              <div><span className="primitive-label">{t("assessment:primitives.applicability")}</span><ApplicabilityBadge code="APPLICABLE" /></div>
              <div><span className="primitive-label">{t("assessment:primitives.evidenceReference")}</span><EvidenceBadge evidenceId="E-DEMO-001" kind={t("assessment:primitives.criterion")} sourceText={DEMO_EVIDENCE_SOURCE_TEXT} /></div>
            </div>
            <DataTable caption={t("assessment:primitives.tableCaption")} columns={columns} rows={demoRecords} rowKey={(row) => row.id} />
          </Card>
          <Callout title={t("assessment:primitives.boundaryTitle")} tone="warning">{t("assessment:primitives.boundaryText")}</Callout>
        </section>
      </div>
    </AppShell>
  );
}

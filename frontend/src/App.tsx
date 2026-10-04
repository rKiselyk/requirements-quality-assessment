import { useState } from "react";
import { AppShell, PageHeader, type NavigationItem } from "./components/shell";
import {
  Accordion,
  Button,
  Callout,
  Card,
  DataTable,
  EmptyState,
  FileDropzone,
  IconButton,
  InlineValidation,
  LoadingProgress,
  MetricCard,
  Tabs,
  TextArea,
  TextInput,
  Tooltip,
  UnavailableState,
  type DataTableColumn,
} from "./components/ui";
import { ApplicabilityBadge, EvidenceBadge, ExactValue, StatusBadge, type ScientificCode } from "./components/scientific";

const navigation: readonly NavigationItem[] = [
  { id: "foundation", label: "Foundation" },
  { id: "components", label: "Components" },
  { id: "scientific", label: "Scientific primitives" },
];

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

const columns: readonly DataTableColumn<DemoRecord>[] = [
  { key: "id", header: "Demo record", render: (row) => <code>{row.id}</code> },
  { key: "value", header: "Exact value", render: (row) => <ExactValue value={row.value} compact /> },
  { key: "status", header: "Canonical state", render: (row) => <StatusBadge code={row.status} /> },
];

export function App() {
  const [activeId, setActiveId] = useState("foundation");

  return (
    <AppShell
      navigation={navigation}
      activeNavigationId={activeId}
      onNavigate={(id) => {
        setActiveId(id);
        document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
      }}
      headerActions={<Button variant="quiet">Demo action</Button>}
    >
      <div className="showcase">
        <PageHeader
          title="Research UI foundation"
          subtitle="RUI-03 development showcase — static presentation data only"
          metadata={<><code>FOUNDATION_DEMO</code><span>Not connected to the analysis API</span></>}
          actions={<Tooltip content="This showcase does not submit an analysis."><IconButton label="About this demo" icon="?" /></Tooltip>}
        />

        <Callout title="Foundation-only showcase">
          Every value and state below is static demonstration content supplied to presentation components. No scientific result is calculated or inferred here.
        </Callout>

        <section id="foundation" className="showcase__section" aria-labelledby="foundation-title">
          <div className="section-heading"><div><span className="section-heading__eyebrow">Shell and surfaces</span><h2 id="foundation-title">Foundation</h2></div></div>
          <div className="metric-grid">
            <MetricCard label="Completeness demo" value={{ numerator: "5", denominator: "6" }} status="COMPUTED" detail="Static exact rational input" />
            <MetricCard label="Verifiability demo" value={null} status="UNKNOWN" detail="No numeric value is presented" />
            <MetricCard label="Unambiguity demo" value={null} status="NOT_APPLICABLE" detail="Not converted to zero" />
          </div>
          <Card title="Shared card" description="A restrained surface for grouped research information.">
            <div className="button-row">
              <Button variant="primary">Primary action</Button>
              <Button>Secondary action</Button>
              <Button variant="quiet">Quiet action</Button>
              <IconButton label="More information" icon="⋯" />
            </div>
          </Card>
        </section>

        <section id="components" className="showcase__section" aria-labelledby="components-title">
          <div className="section-heading"><div><span className="section-heading__eyebrow">Reusable controls</span><h2 id="components-title">Generic components</h2></div></div>
          <div className="showcase-grid">
            <Card title="Form controls">
              <div className="form-stack">
                <TextInput label="Artifact label" placeholder="Example label" hint="Presentation-only development field" />
                <TextArea label="Requirement text" rows={4} defaultValue="Static demonstration requirement text." hint="The component preserves supplied text." />
                <FileDropzone label="Drop a demonstration text file" description="or choose a file — no upload occurs in this showcase" />
                <InlineValidation>Example inline validation message</InlineValidation>
              </div>
            </Card>
            <Card title="Feedback and progress">
              <div className="form-stack">
                <LoadingProgress label="Example indeterminate activity" />
                <UnavailableState title="Not available for this analysis" description="External evidence was not supplied. No value was inferred." />
                <EmptyState title="No demonstration records" description="Add data to show content in this region." />
              </div>
            </Card>
          </div>
          <Card title="Disclosure patterns">
            <Tabs label="Demonstration views" items={[
              { id: "summary", label: "Summary", content: <p>Tabs expose supplied presentation content without changing scientific state.</p> },
              { id: "trace", label: "Trace", content: <p><code>RULE-DEMO-001</code> is a non-scientific placeholder identifier.</p> },
            ]} />
            <Accordion items={[
              { id: "details", title: "Expandable technical detail", content: <p>Native disclosure semantics provide keyboard-accessible expansion.</p> },
              { id: "provenance", title: "Example provenance", content: <p>Static showcase data; not produced by the backend.</p> },
            ]} />
          </Card>
        </section>

        <section id="scientific" className="showcase__section" aria-labelledby="scientific-title">
          <div className="section-heading"><div><span className="section-heading__eyebrow">Presentation only</span><h2 id="scientific-title">Scientific primitives</h2></div></div>
          <Card title="Exact values, evidence, and canonical states">
            <div className="primitive-row">
              <div><span className="primitive-label">Structured rational</span><ExactValue value={{ numerator: "2", denominator: "3" }} /></div>
              <div><span className="primitive-label">Status</span><StatusBadge code="COMPUTED" /></div>
              <div><span className="primitive-label">Applicability</span><ApplicabilityBadge code="APPLICABLE" /></div>
              <div><span className="primitive-label">Evidence reference</span><EvidenceBadge evidenceId="E-DEMO-001" kind="Criterion" sourceText="static source fragment" /></div>
            </div>
            <DataTable caption="Static exact-value presentation examples" columns={columns} rows={demoRecords} rowKey={(row) => row.id} />
          </Card>
          <Callout title="Scientific presentation boundary" tone="warning">
            COMPUTED indicates that an approved rule produced a value; this primitive does not label it good, passed, or safe.
          </Callout>
        </section>
      </div>
    </AppShell>
  );
}

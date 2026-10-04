import { useTranslation } from "react-i18next";
import { PageHeader } from "../../components/shell";
import { Callout, Card } from "../../components/ui";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";

export function ResultReadyPage({ result }: { result: CanonicalAnalyzeResponse }) {
  const { t } = useTranslation("lifecycle");
  return (
    <section className="result-ready">
      <PageHeader title={t("result.title")} subtitle={t("result.subtitle")} />
      <Callout title={t("result.completed")}> <p>{t("result.boundary")}</p> </Callout>
      <Card title={t("result.metadataTitle")}>
        <dl className="result-ready__metadata">
          <div><dt>{t("result.analysisCase")}</dt><dd><code>{result.analysis_case}</code></dd></div>
          <div><dt>{t("result.contractVersion")}</dt><dd><code>{result.contract_version}</code></dd></div>
        </dl>
      </Card>
    </section>
  );
}

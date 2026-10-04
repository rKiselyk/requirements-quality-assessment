import { useTranslation } from "react-i18next";
import { Card, LoadingProgress } from "../../components/ui";

export function AnalyzingPage() {
  const { t } = useTranslation("lifecycle");
  return (
    <section className="analysis-state" aria-labelledby="analysis-state-title">
      <Card>
        <div className="analysis-state__content">
          <div className="analysis-state__spinner" aria-hidden="true" />
          <h1 id="analysis-state-title">{t("analyzing.title")}</h1>
          <p>{t("analyzing.description")}</p>
          <LoadingProgress label={t("analyzing.progressLabel")} />
          <p className="analysis-state__note">{t("analyzing.resultNotice")}</p>
        </div>
      </Card>
    </section>
  );
}

import { useTranslation } from "react-i18next";
import { ExactValue } from "../../components/scientific";
import type { StateAndValueProjection } from "./projection";

function Value({ value }: { value: StateAndValueProjection | null }) {
  const { t } = useTranslation("comparison");
  if (!value) return <span className="scientific-boundary">{t("none")}</span>;
  return <div className="comparison-value">
    <code>{value.status}</code>
    <code>{value.applicability}</code>
    {value.exactValue ? <ExactValue value={value.exactValue} /> : null}
    {value.categoricalState ? <code>{value.categoricalState}</code> : null}
  </div>;
}

export function BeforeAfterComparison({ before, after }: { before: StateAndValueProjection | null; after: StateAndValueProjection | null }) {
  const { t } = useTranslation("comparison");
  return <div className="before-after" aria-label={t("beforeAfter") }>
    <section><h4>{t("before")}</h4><Value value={before} /></section>
    <section><h4>{t("after")}</h4><Value value={after} /></section>
  </div>;
}

import { useTranslation } from "react-i18next";
import { StatusBadge } from "../../components/scientific";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { selectSectionAvailability } from "./projection";

const stages = ["requirements", "specification", "product_quality", "risk", "corrective_actions", "process"] as const;

export function ModelPipeline({ result }: { result: CanonicalAnalyzeResponse }) {
  const { t } = useTranslation("overview");
  return (
    <section className="model-pipeline" aria-labelledby="model-pipeline-title">
      <h2 id="model-pipeline-title">{t("pipeline.title")}</h2>
      <p>{t("pipeline.description")}</p>
      <ol>
        {stages.map((stage) => {
          const availability = selectSectionAvailability(result, stage);
          return (
            <li key={stage}>
              <span>{t(`pipeline.stages.${stage}`)}</span>
              {availability
                ? <StatusBadge code={availability.availability} />
                : <span className="model-pipeline__malformed">{t("pipeline.availabilityCannotPresent")}</span>}
            </li>
          );
        })}
      </ol>
    </section>
  );
}

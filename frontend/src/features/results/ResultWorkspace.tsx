import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { PageHeader } from "../../components/shell";
import { UnavailableState } from "../../components/ui";
import { OverviewPage } from "./OverviewPage";
import type { ResultSectionId } from "./projection";
import { RequirementsPage } from "../requirements/RequirementsPage";
import { SpecificationPage } from "../specification/SpecificationPage";

export function ResultWorkspace({
  result,
  activeView,
  selectedRequirementId,
  onSelectRequirement,
}: {
  result: CanonicalAnalyzeResponse;
  activeView: ResultSectionId;
  selectedRequirementId: string | null;
  onSelectRequirement: (requirementId: string) => void;
}) {
  const { t } = useTranslation("overview");
  if (activeView === "overview") return <OverviewPage result={result} />;
  if (activeView === "requirements") return <RequirementsPage result={result} selectedRequirementId={selectedRequirementId} onSelectRequirement={onSelectRequirement} />;
  if (activeView === "specification") return <SpecificationPage result={result} onSelectRequirement={onSelectRequirement} />;
  return (
    <section className="deferred-page">
      <PageHeader title={t(`navigation.${activeView}`)} subtitle={t("deferred.subtitle")} />
      <UnavailableState title={t("deferred.title")} description={t("deferred.description")} />
    </section>
  );
}

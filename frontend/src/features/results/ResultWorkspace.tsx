import { useTranslation } from "react-i18next";
import type { CanonicalAnalyzeResponse } from "../../api/analyze";
import { PageHeader } from "../../components/shell";
import { UnavailableState } from "../../components/ui";
import { OverviewPage } from "./OverviewPage";
import type { ResultSectionId } from "./projection";
import { RequirementsPage } from "../requirements/RequirementsPage";
import { SpecificationPage } from "../specification/SpecificationPage";
import { ProductQualityPage } from "../product-quality/ProductQualityPage";
import { RiskPage } from "../risk/RiskPage";
import { CorrectiveActionsPage } from "../corrective-actions/CorrectiveActionsPage";
import type { Rui05AnalyzeRequest } from "../specification-input/model";

export function ResultWorkspace({
  result,
  activeView,
  selectedRequirementId,
  onSelectRequirement,
  onAnalyzeReassessment = () => undefined,
  reassessmentPending = false,
  reassessmentErrorMessage = null,
  onRetryReassessment,
  onReassessmentDraftChange = () => undefined,
}: {
  result: CanonicalAnalyzeResponse;
  activeView: ResultSectionId;
  selectedRequirementId: string | null;
  onSelectRequirement: (requirementId: string) => void;
  onAnalyzeReassessment?: (request: Rui05AnalyzeRequest) => void;
  reassessmentPending?: boolean;
  reassessmentErrorMessage?: string | null;
  onRetryReassessment?: () => void;
  onReassessmentDraftChange?: () => void;
}) {
  const { t } = useTranslation("overview");
  if (activeView === "overview") return <OverviewPage result={result} />;
  if (activeView === "requirements") return <RequirementsPage result={result} selectedRequirementId={selectedRequirementId} onSelectRequirement={onSelectRequirement} />;
  if (activeView === "specification") return <SpecificationPage result={result} onSelectRequirement={onSelectRequirement} />;
  if (activeView === "product_quality") return <ProductQualityPage result={result} onSelectRequirement={onSelectRequirement} />;
  if (activeView === "risk") return <RiskPage result={result} onSelectRequirement={onSelectRequirement} />;
  if (activeView === "corrective_actions") return <CorrectiveActionsPage
    result={result}
    onSelectRequirement={onSelectRequirement}
    onAnalyzeReassessment={onAnalyzeReassessment}
    reassessmentPending={reassessmentPending}
    reassessmentErrorMessage={reassessmentErrorMessage}
    onRetryReassessment={onRetryReassessment}
    onReassessmentDraftChange={onReassessmentDraftChange}
  />;
  return (
    <section className="deferred-page">
      <PageHeader title={t(`navigation.${activeView}`)} subtitle={t("deferred.subtitle")} />
      <UnavailableState title={t("deferred.title")} description={t("deferred.description")} />
    </section>
  );
}

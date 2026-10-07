import { useState } from "react";
import { useTranslation } from "react-i18next";
import { AppShell } from "./components/shell";
import { Button } from "./components/ui";
import { AnalyzingPage } from "./features/analysis-session/AnalyzingPage";
import { useAnalysisSession } from "./features/analysis-session/useAnalysisSession";
import { ResultWorkspace } from "./features/results/ResultWorkspace";
import { resultSectionIds, selectVisibleResultSections, type ResultSectionId } from "./features/results/projection";
import { SpecificationInputPage } from "./features/specification-input/SpecificationInputPage";
import { apiErrorTranslationKey } from "./i18n";

export function App() {
  const { t: lifecycleText } = useTranslation("lifecycle");
  const { t: errorText } = useTranslation("errors");
  const { t: overviewText } = useTranslation("overview");
  const [inputVersion, setInputVersion] = useState(0);
  const [selectedResultView, setSelectedResultView] = useState<ResultSectionId>("overview");
  const [selectedRequirementId, setSelectedRequirementId] = useState<string | null>(null);
  const session = useAnalysisSession();
  const errorMessage = session.error?.code
    ? errorText(apiErrorTranslationKey(session.error.code))
    : session.error
      ? errorText("unknown")
      : null;

  const reset = () => {
    session.reset();
    setSelectedResultView("overview");
    setSelectedRequirementId(null);
    setInputVersion((version) => version + 1);
  };

  const visibleSections = session.phase === "RESULT_READY" && session.latestResult
    ? selectVisibleResultSections(session.latestResult)
    : [];
  const navigation = session.phase === "RESULT_READY"
    ? visibleSections.map((id) => ({ id, label: overviewText(`navigation.${id}`) }))
    : undefined;

  return (
    <AppShell
      headerActions={session.phase === "RESULT_READY" ? (
        <Button type="button" variant="secondary" onClick={reset}>
          {lifecycleText("actions.newSpecification")}
        </Button>
      ) : undefined}
      navigation={navigation}
      activeNavigationId={selectedResultView}
      onNavigate={(id) => {
        if (visibleSections.includes(id as ResultSectionId) && resultSectionIds.includes(id as ResultSectionId)) setSelectedResultView(id as ResultSectionId);
      }}
    >
      <div hidden={session.phase !== "INPUT"}>
        <SpecificationInputPage
          key={inputVersion}
          onAnalyzeRequest={session.submit}
          onInputIdentityChange={session.invalidateFailedAttempt}
          apiErrorMessage={errorMessage}
          onRetry={session.submittedRequest ? session.retry : undefined}
        />
      </div>
      {session.phase === "ANALYZING" ? <AnalyzingPage /> : null}
      {session.phase === "RESULT_READY" && session.latestResult
          ? <ResultWorkspace
            result={session.latestResult}
            activeView={selectedResultView}
            selectedRequirementId={selectedRequirementId}
            onSelectRequirement={(requirementId) => {
              setSelectedRequirementId(requirementId);
              setSelectedResultView("requirements");
            }}
            onAnalyzeReassessment={session.submit}
            reassessmentPending={session.reassessmentPending}
            reassessmentErrorMessage={session.latestResult && session.error ? errorMessage : null}
            onRetryReassessment={session.latestResult && session.error && session.submittedRequest?.case === "REASSESSMENT" ? session.retry : undefined}
            onReassessmentDraftChange={session.invalidateFailedAttempt}
          />
        : null}
    </AppShell>
  );
}

export type { Rui05AnalyzeRequest } from "./features/specification-input/model";

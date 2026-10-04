import { useState } from "react";
import { useTranslation } from "react-i18next";
import { AppShell } from "./components/shell";
import { Button } from "./components/ui";
import { AnalyzingPage } from "./features/analysis-session/AnalyzingPage";
import { ResultReadyPage } from "./features/analysis-session/ResultReadyPage";
import { useAnalysisSession } from "./features/analysis-session/useAnalysisSession";
import { SpecificationInputPage } from "./features/specification-input/SpecificationInputPage";
import { apiErrorTranslationKey } from "./i18n";

export function App() {
  const { t: lifecycleText } = useTranslation("lifecycle");
  const { t: errorText } = useTranslation("errors");
  const [inputVersion, setInputVersion] = useState(0);
  const session = useAnalysisSession();
  const errorMessage = session.error?.code
    ? errorText(apiErrorTranslationKey(session.error.code))
    : session.error
      ? errorText("unknown")
      : null;

  const reset = () => {
    session.reset();
    setInputVersion((version) => version + 1);
  };

  return (
    <AppShell
      headerActions={session.phase === "RESULT_READY" ? (
        <Button type="button" variant="secondary" onClick={reset}>
          {lifecycleText("actions.newSpecification")}
        </Button>
      ) : undefined}
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
        ? <ResultReadyPage result={session.latestResult} />
        : null}
    </AppShell>
  );
}

export type { Rui05AnalyzeRequest } from "./features/specification-input/model";

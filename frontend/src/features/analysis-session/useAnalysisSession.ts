import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { analyzeSpecification, toSafeAnalyzeError, type CanonicalAnalyzeResponse, type SafeAnalyzeError } from "../../api/analyze";
import type { Rui05AnalyzeRequest } from "../specification-input/model";

export type AnalysisPhase = "INPUT" | "ANALYZING" | "RESULT_READY";

export interface AnalysisSession {
  phase: AnalysisPhase;
  submittedRequest: Rui05AnalyzeRequest | null;
  latestResult: CanonicalAnalyzeResponse | null;
  error: SafeAnalyzeError | null;
  submit: (request: Rui05AnalyzeRequest) => void;
  retry: () => void;
  reset: () => void;
}

export function useAnalysisSession(): AnalysisSession {
  const [phase, setPhase] = useState<AnalysisPhase>("INPUT");
  const [submittedRequest, setSubmittedRequest] = useState<Rui05AnalyzeRequest | null>(null);
  const [latestResult, setLatestResult] = useState<CanonicalAnalyzeResponse | null>(null);
  const [error, setError] = useState<SafeAnalyzeError | null>(null);

  const mutation = useMutation({
    mutationFn: (request: Rui05AnalyzeRequest) => analyzeSpecification(request),
    retry: false,
    onMutate: (request) => {
      setSubmittedRequest(request);
      setError(null);
      setPhase("ANALYZING");
    },
    onSuccess: (response) => {
      setLatestResult(response);
      setPhase("RESULT_READY");
    },
    onError: (mutationError) => {
      setError(toSafeAnalyzeError(mutationError));
      setPhase("INPUT");
    },
  });

  const submit = (request: Rui05AnalyzeRequest) => mutation.mutate(request);
  const retry = () => {
    if (submittedRequest !== null && phase === "INPUT") mutation.mutate(submittedRequest);
  };
  const reset = () => {
    mutation.reset();
    setSubmittedRequest(null);
    setLatestResult(null);
    setError(null);
    setPhase("INPUT");
  };

  return { phase, submittedRequest, latestResult, error, submit, retry, reset };
}

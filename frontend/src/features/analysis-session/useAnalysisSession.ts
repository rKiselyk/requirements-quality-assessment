import { useRef, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { analyzeSpecification, toSafeAnalyzeError, type CanonicalAnalyzeResponse, type SafeAnalyzeError } from "../../api/analyze";
import type { Rui05AnalyzeRequest } from "../specification-input/model";

export type AnalysisPhase = "INPUT" | "ANALYZING" | "RESULT_READY";

export interface AnalysisSession {
  phase: AnalysisPhase;
  submittedRequest: Rui05AnalyzeRequest | null;
  latestResult: CanonicalAnalyzeResponse | null;
  error: SafeAnalyzeError | null;
  reassessmentPending: boolean;
  submit: (request: Rui05AnalyzeRequest) => void;
  retry: () => void;
  invalidateFailedAttempt: () => void;
  reset: () => void;
}

export function useAnalysisSession(): AnalysisSession {
  const generation = useRef(0);
  const [phase, setPhase] = useState<AnalysisPhase>("INPUT");
  const [submittedRequest, setSubmittedRequest] = useState<Rui05AnalyzeRequest | null>(null);
  const [latestResult, setLatestResult] = useState<CanonicalAnalyzeResponse | null>(null);
  const [error, setError] = useState<SafeAnalyzeError | null>(null);

  const mutation = useMutation({
    mutationFn: (request: Rui05AnalyzeRequest) => analyzeSpecification(request),
    retry: false,
    onMutate: (request) => {
      const requestGeneration = generation.current;
      setSubmittedRequest(request);
      setError(null);
      setPhase(request.case === "REASSESSMENT" && latestResult !== null ? "RESULT_READY" : "ANALYZING");
      return { generation: requestGeneration };
    },
    onSuccess: (response, _request, context) => {
      if (context.generation !== generation.current) return;
      setLatestResult(response);
      setPhase("RESULT_READY");
    },
    onError: (mutationError, _request, context) => {
      if (context?.generation !== generation.current) return;
      setError(toSafeAnalyzeError(mutationError));
      setPhase(latestResult === null ? "INPUT" : "RESULT_READY");
    },
  });

  const submit = (request: Rui05AnalyzeRequest) => mutation.mutate(request);
  const retry = () => {
    if (submittedRequest !== null && error !== null && (phase === "INPUT" || latestResult !== null)) mutation.mutate(submittedRequest);
  };
  const invalidateFailedAttempt = () => {
    if (error === null) return;
    mutation.reset();
    setSubmittedRequest(null);
    setError(null);
  };
  const reset = () => {
    generation.current += 1;
    mutation.reset();
    setSubmittedRequest(null);
    setLatestResult(null);
    setError(null);
    setPhase("INPUT");
  };

  const reassessmentPending = mutation.isPending && submittedRequest?.case === "REASSESSMENT" && latestResult !== null;
  return { phase, submittedRequest, latestResult, error, reassessmentPending, submit, retry, invalidateFailedAttempt, reset };
}

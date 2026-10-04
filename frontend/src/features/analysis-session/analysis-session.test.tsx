import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../../App";
import { analyzeSpecification } from "../../api/analyze";
import { i18n } from "../../i18n";
import type { Rui05AnalyzeRequest } from "../specification-input/model";
import { useAnalysisSession, type AnalysisSession } from "./useAnalysisSession";

const canonicalResult = {
  contract_version: "research-api-v1",
  analysis_case: "INITIAL" as const,
  specification: { quality_profile: { completeness: { value: { numerator: 2, denominator: 3 } } } },
  limitations: ["TEXT_ONLY_INITIAL_ASSESSMENT"],
};

function jsonResponse(payload: unknown, ok = true): Response {
  return { ok, json: async () => payload } as Response;
}

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((resolvePromise) => { resolve = resolvePromise; });
  return { promise, resolve };
}

function renderApp() {
  const queryClient = new QueryClient({
    defaultOptions: { mutations: { retry: 4 } },
  });
  return render(<QueryClientProvider client={queryClient}><App /></QueryClientProvider>);
}

function enterRequirement(value = "  Preserve   this requirement!  ") {
  fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value } });
}

describe("RUI-06 analysis lifecycle", () => {
  beforeEach(async () => {
    window.sessionStorage.clear();
    await i18n.changeLanguage("en");
  });

  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("sends one unchanged INITIAL request and shows truthful indeterminate progress", async () => {
    const pending = deferred<Response>();
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockImplementation(() => pending.promise);
    renderApp();
    enterRequirement("First requirement\n\n Second requirement ");

    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));

    await screen.findByRole("heading", { name: "Analyzing specification" });
    expect(screen.getByRole("status").textContent).toContain("Analysis in progress");
    expect(screen.queryByText(/Extraction complete|Risk complete|Prediction complete/)).toBeNull();
    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(fetchSpy).toHaveBeenCalledWith("/api/v1/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        case: "INITIAL",
        requirements: [
          { text: "First requirement", source_line: 1 },
          { text: "Second requirement", source_line: 3 },
        ],
      }),
    });
    expect(JSON.parse(String(fetchSpy.mock.calls[0][1]?.body))).not.toHaveProperty("locale");

    pending.resolve(jsonResponse(canonicalResult));
    expect(await screen.findByRole("heading", { name: "Analysis result ready" })).toBeTruthy();
  });

  it("sends exactly one accepted controlled-demo request", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse({
      ...canonicalResult,
      analysis_case: "CONTROLLED_DEMO",
    }));
    renderApp();

    fireEvent.click(screen.getByRole("button", { name: "Load demonstration example" }));

    await screen.findByRole("heading", { name: "Analysis result ready" });
    expect(fetchSpy).toHaveBeenCalledTimes(1);
    const body = JSON.parse(String(fetchSpy.mock.calls[0][1]?.body));
    expect(body).toEqual({
      case: "CONTROLLED_DEMO",
      scenario: { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" },
    });
    expect(body).not.toHaveProperty("locale");
  });

  it("does not retry automatically, preserves input, and retries only on explicit action", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch")
      .mockRejectedValueOnce(new Error("C:\\private\\traceback secret"))
      .mockResolvedValueOnce(jsonResponse(canonicalResult));
    renderApp();
    const source = "  Preserve   this requirement!  ";
    enterRequirement(source);

    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));

    expect(await screen.findByText("The analysis request could not be completed.")).toBeTruthy();
    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect((screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement).value).toBe(source);
    expect(screen.queryByText(/private|traceback|secret/i)).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "Try again" }));
    await screen.findByRole("heading", { name: "Analysis result ready" });
    expect(fetchSpy).toHaveBeenCalledTimes(2);
  });

  it("localizes known errors without exposing details or rerunning analysis", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse({
      error: {
        code: "MALFORMED_REQUIREMENT_INPUT",
        details: { exception: "raw internal exception", path: "C:\\server\\model.py" },
        path: ["body", "requirements"],
      },
    }, false));
    renderApp();
    enterRequirement("Requirement");
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));

    expect(await screen.findByText("The requirement input could not be read.")).toBeTruthy();
    expect(screen.queryByText(/raw internal|server\\model/i)).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));

    expect(await screen.findByText("Не вдалося прочитати введені вимоги.")).toBeTruthy();
    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  it.each([
    ["unknown API code", jsonResponse({ error: { code: "SOME_NEW_CODE", details: {}, path: null } }, false)],
    ["malformed intermediary body", jsonResponse({ html: "<h1>proxy failure</h1>" }, false)],
  ])("uses the safe fallback for %s", async (_label, response) => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(response);
    renderApp();
    enterRequirement("Requirement");
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));

    expect(await screen.findByText("The analysis request could not be completed.")).toBeTruthy();
    expect(screen.queryByText(/SOME_NEW_CODE|proxy failure|<h1>/)).toBeNull();
  });

  it("switches locale without another request or mutation of result metadata", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse(canonicalResult));
    renderApp();
    enterRequirement("Requirement");
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    await screen.findByText("research-api-v1");

    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));

    expect(await screen.findByRole("heading", { name: "Результат аналізу готовий" })).toBeTruthy();
    expect(screen.getByText("research-api-v1")).toBeTruthy();
    expect(screen.getByText("INITIAL")).toBeTruthy();
    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  it("New specification clears result and draft while preserving locale", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse(canonicalResult));
    renderApp();
    enterRequirement("Requirement");
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    await screen.findByRole("heading", { name: "Analysis result ready" });
    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));
    await screen.findByRole("heading", { name: "Результат аналізу готовий" });

    fireEvent.click(screen.getByRole("button", { name: "Нова специфікація" }));

    expect(screen.getByRole("heading", { name: "Аналіз специфікації" })).toBeTruthy();
    expect((screen.getByRole("textbox", { name: "Вставте або відредагуйте вимоги" }) as HTMLTextAreaElement).value).toBe("");
    expect(screen.queryByText("research-api-v1")).toBeNull();
    expect(document.documentElement.lang).toBe("uk");
  });
});

describe("RUI-06 canonical response ownership", () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("returns and retains the complete response object unchanged", async () => {
    const payload = { ...canonicalResult, opaque_future_section: { exact: "17/19", state: null } };
    const fetchImplementation = vi.fn().mockResolvedValue(jsonResponse(payload));
    const request: Rui05AnalyzeRequest = { case: "INITIAL", requirements: [{ text: "Requirement", source_line: 1 }] };

    const response = await analyzeSpecification(request, fetchImplementation);

    expect(response).toBe(payload);
    expect(response).toEqual(payload);
  });

  it("keeps result ownership independent from presentation view selection", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse(canonicalResult));
    let session!: AnalysisSession;
    function Probe() {
      session = useAnalysisSession();
      return null;
    }
    const queryClient = new QueryClient();
    render(<QueryClientProvider client={queryClient}><Probe /></QueryClientProvider>);

    await act(async () => {
      session.submit({ case: "INITIAL", requirements: [{ text: "Requirement", source_line: 1 }] });
    });
    await waitFor(() => expect(session.phase).toBe("RESULT_READY"));
    const retained = session.latestResult;
    let selectedView = "overview";
    selectedView = "future-requirements";

    expect(selectedView).toBe("future-requirements");
    expect(session.latestResult).toBe(retained);
    expect(session.latestResult).toBe(canonicalResult);
  });
});

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { App, type Rui05AnalyzeRequest } from "./App";
import { i18n } from "./i18n";
import { createInitialAnalyzeRequest, parseSpecificationText } from "./features/specification-input/model";

function textFile(name: string, content: string, type = "text/plain"): File {
  const file = new File([content], name, { type });
  Object.defineProperty(file, "arrayBuffer", {
    configurable: true,
    value: async () => new TextEncoder().encode(content).buffer,
  });
  return file;
}

function fileInput(): HTMLInputElement {
  const input = document.querySelector('input[type="file"]');
  if (!(input instanceof HTMLInputElement)) throw new Error("File input not found");
  return input;
}

function selectFile(file: File) {
  fireEvent.change(fileInput(), {
    target: { files: { 0: file, length: 1, item: (index: number) => index === 0 ? file : null } },
  });
}

describe("RUI-05 specification input", () => {
  beforeEach(async () => {
    window.sessionStorage.clear();
    await i18n.changeLanguage("en");
  });

  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("ignores blank lines while preserving physical source lines", () => {
    expect(parseSpecificationText("First requirement\n   \nSecond requirement")).toEqual([
      { text: "First requirement", source_line: 1 },
      { text: "Second requirement", source_line: 3 },
    ]);
  });

  it("trims only line edges without rewriting internal text", () => {
    expect(parseSpecificationText("  Keep   internal punctuation: так!  \r\n\tДругий  текст\t")).toEqual([
      { text: "Keep   internal punctuation: так!", source_line: 1 },
      { text: "Другий  текст", source_line: 2 },
    ]);
  });

  it("produces the same canonical requirements from paste and file input", async () => {
    const source = "  First requirement  \n\n Second requirement ";
    const pastedRequests: Rui05AnalyzeRequest[] = [];
    const pasted = render(<App onAnalyzeRequest={(request) => pastedRequests.push(request)} />);

    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: source } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    const pastedRequest = pastedRequests[0];
    pasted.unmount();

    const fileRequests: Rui05AnalyzeRequest[] = [];
    render(<App onAnalyzeRequest={(request) => fileRequests.push(request)} />);
    selectFile(textFile("requirements.txt", source));

    await screen.findByText("Selected file: requirements.txt");
    expect((screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement).value).toBe(source);
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    expect(fileRequests[0]).toEqual(pastedRequest);
  });

  it("shows empty validation and disables Analyze", () => {
    render(<App />);

    expect(screen.getByText("Enter at least one non-empty requirement.")).toBeTruthy();
    expect((screen.getByRole("button", { name: "Analyze" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("rejects unsupported files without replacing the editor", async () => {
    render(<App />);

    selectFile(textFile("requirements.json", "[]", "application/json"));

    expect(await screen.findByText("Choose a supported UTF-8 .txt or plain-text file.")).toBeTruthy();
    expect((screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement).value).toBe("");
  });

  it("shows safe validation when a supported file cannot be read", async () => {
    const file = textFile("requirements.txt", "Requirement");
    Object.defineProperty(file, "arrayBuffer", { value: async () => { throw new Error("read failed"); } });
    render(<App />);

    selectFile(file);

    expect(await screen.findByText("The file could not be read as UTF-8 plain text. Choose another file.")).toBeTruthy();
  });

  it("constructs an INITIAL request with only case and requirements and no client IDs", () => {
    const request = createInitialAnalyzeRequest("First\n\nSecond");

    expect(Object.keys(request)).toEqual(["case", "requirements"]);
    expect(request).toEqual({
      case: "INITIAL",
      requirements: [
        { text: "First", source_line: 1 },
        { text: "Second", source_line: 3 },
      ],
    });
    expect(request.requirements.every((requirement) => !("id" in requirement))).toBe(true);
  });

  it("keeps the controlled demo opt-in and emits only the approved identity", () => {
    const requests: Rui05AnalyzeRequest[] = [];
    render(<App onAnalyzeRequest={(request) => requests.push(request)} />);

    expect(requests).toEqual([]);
    fireEvent.click(screen.getByRole("button", { name: "Load demonstration example" }));
    expect(requests).toEqual([{
      case: "CONTROLLED_DEMO",
      scenario: { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" },
    }]);
  });

  it("does not perform an HTTP request for ordinary or demonstration actions", () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    render(<App />);

    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    fireEvent.click(screen.getByRole("button", { name: "Load demonstration example" }));

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("switches locale without mutating entered requirement text", async () => {
    const source = "  Не змінювати   внутрішній текст!  ";
    render(<App />);
    const editor = screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement;
    fireEvent.change(editor, { target: { value: source } });

    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));

    await waitFor(() => expect(screen.getByRole("heading", { name: "Аналіз специфікації" })).toBeTruthy());
    expect(editor.value).toBe(source);
    expect(document.querySelector(".requirement-list__text")?.textContent).toBe("Не змінювати   внутрішній текст!");
  });
});

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { Rui05AnalyzeRequest } from "./App";
import { AppShell } from "./components/shell";
import { i18n } from "./i18n";
import { createInitialAnalyzeRequest, parseSpecificationText } from "./features/specification-input/model";
import { SpecificationInputPage } from "./features/specification-input/SpecificationInputPage";

function Rui05Harness({ onAnalyzeRequest = () => undefined }: { onAnalyzeRequest?: (request: Rui05AnalyzeRequest) => void }) {
  return <AppShell><SpecificationInputPage onAnalyzeRequest={onAnalyzeRequest} /></AppShell>;
}

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

function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((resolvePromise, rejectPromise) => {
    resolve = resolvePromise;
    reject = rejectPromise;
  });
  return { promise, resolve, reject };
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
    const pasted = render(<Rui05Harness onAnalyzeRequest={(request) => { pastedRequests.push(request); }} />);

    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: source } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    const pastedRequest = pastedRequests[0];
    pasted.unmount();

    const fileRequests: Rui05AnalyzeRequest[] = [];
    render(<Rui05Harness onAnalyzeRequest={(request) => { fileRequests.push(request); }} />);
    selectFile(textFile("requirements.txt", source));

    await screen.findByText("Selected file: requirements.txt");
    expect((screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement).value).toBe(source);
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    expect(fileRequests[0]).toEqual(pastedRequest);
  });

  it("shows empty validation and disables Analyze", () => {
    render(<Rui05Harness />);

    expect(screen.getByText("Enter at least one non-empty requirement.")).toBeTruthy();
    expect((screen.getByRole("button", { name: "Analyze" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("rejects unsupported files without replacing the editor", async () => {
    render(<Rui05Harness />);

    selectFile(textFile("requirements.json", "[]", "application/json"));

    expect(await screen.findByText("Choose a supported UTF-8 .txt or plain-text file.")).toBeTruthy();
    expect((screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement).value).toBe("");
  });

  it("shows safe validation and preserves existing text when a supported file cannot be read", async () => {
    const file = textFile("requirements.txt", "Requirement");
    Object.defineProperty(file, "arrayBuffer", { value: async () => { throw new Error("read failed"); } });
    render(<Rui05Harness />);
    const editor = screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement;
    fireEvent.change(editor, { target: { value: "Existing valid requirement" } });

    selectFile(file);

    expect(await screen.findByText("The file could not be read as UTF-8 plain text. Choose another file.")).toBeTruthy();
    expect(editor.value).toBe("Existing valid requirement");
    expect((screen.getByRole("button", { name: "Analyze" }) as HTMLButtonElement).disabled).toBe(false);
  });

  it("blocks analysis until a replacement file read completes", async () => {
    const requests: Rui05AnalyzeRequest[] = [];
    const read = deferred<ArrayBuffer>();
    const replacement = textFile("replacement.txt", "unused");
    Object.defineProperty(replacement, "arrayBuffer", { value: () => read.promise });
    render(<Rui05Harness onAnalyzeRequest={(request) => { requests.push(request); }} />);
    const editor = screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement;
    const analyze = screen.getByRole("button", { name: "Analyze" }) as HTMLButtonElement;
    fireEvent.change(editor, { target: { value: "Old requirement" } });

    selectFile(replacement);

    expect(await screen.findByText("Reading selected file: replacement.txt")).toBeTruthy();
    expect(editor.value).toBe("Old requirement");
    expect(analyze.disabled).toBe(true);
    fireEvent.click(analyze);
    expect(requests).toEqual([]);

    read.resolve(new TextEncoder().encode("New file requirement").buffer);
    await screen.findByText("Selected file: replacement.txt");
    expect(editor.value).toBe("New file requirement");
    expect(analyze.disabled).toBe(false);
    fireEvent.click(analyze);
    expect(requests).toEqual([{
      case: "INITIAL",
      requirements: [{ text: "New file requirement", source_line: 1 }],
    }]);
  });

  it("does not let a superseded file read overwrite a newer manual edit", async () => {
    const staleRead = deferred<ArrayBuffer>();
    const staleFile = textFile("stale.txt", "unused");
    Object.defineProperty(staleFile, "arrayBuffer", { value: () => staleRead.promise });
    render(<Rui05Harness />);
    const editor = screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement;

    selectFile(staleFile);
    await screen.findByText("Reading selected file: stale.txt");
    fireEvent.change(editor, { target: { value: "Newer manual requirement" } });
    staleRead.resolve(new TextEncoder().encode("Stale file requirement").buffer);

    await waitFor(() => expect(editor.value).toBe("Newer manual requirement"));
    expect(screen.queryByText("Selected file: stale.txt")).toBeNull();
    expect((screen.getByRole("button", { name: "Analyze" }) as HTMLButtonElement).disabled).toBe(false);
  });

  it("resets the file control so the same file can be selected again", async () => {
    const file = textFile("same.txt", "First file content");
    render(<Rui05Harness />);
    const input = fileInput();
    const editor = screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement;

    selectFile(file);
    await screen.findByText("Selected file: same.txt");
    expect(editor.value).toBe("First file content");
    expect(input.value).toBe("");

    fireEvent.click(screen.getByRole("button", { name: "Clear specification" }));
    Object.defineProperty(file, "arrayBuffer", {
      value: async () => new TextEncoder().encode("Reloaded same file").buffer,
    });
    selectFile(file);

    await waitFor(() => expect(editor.value).toBe("Reloaded same file"));
    expect(input.value).toBe("");
  });

  it("rejects invalid UTF-8 bytes without replacing valid input or starting analysis", async () => {
    const requests: Rui05AnalyzeRequest[] = [];
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const invalidUtf8File = new File([new Uint8Array([0xc3, 0x28])], "invalid.txt", { type: "text/plain" });
    Object.defineProperty(invalidUtf8File, "arrayBuffer", {
      value: async () => new Uint8Array([0xc3, 0x28]).buffer,
    });
    render(<Rui05Harness onAnalyzeRequest={(request) => { requests.push(request); }} />);
    const editor = screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement;
    fireEvent.change(editor, { target: { value: "Existing valid requirement" } });

    selectFile(invalidUtf8File);

    expect(await screen.findByText("The file could not be read as UTF-8 plain text. Choose another file.")).toBeTruthy();
    expect(editor.value).toBe("Existing valid requirement");
    expect(requests).toEqual([]);
    expect(fetchSpy).not.toHaveBeenCalled();
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
    render(<Rui05Harness onAnalyzeRequest={(request) => { requests.push(request); }} />);

    expect(requests).toEqual([]);
    fireEvent.click(screen.getByRole("button", { name: "Load demonstration example" }));
    expect(requests).toEqual([{
      case: "CONTROLLED_DEMO",
      scenario: { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" },
    }]);
  });

  it("does not perform an HTTP request for ordinary or demonstration actions", () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    render(<Rui05Harness />);

    fireEvent.change(screen.getByRole("textbox", { name: "Paste or edit requirements" }), { target: { value: "Requirement" } });
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    fireEvent.click(screen.getByRole("button", { name: "Load demonstration example" }));

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("switches locale without mutating entered requirement text", async () => {
    const source = "  Не змінювати   внутрішній текст!  ";
    render(<Rui05Harness />);
    const editor = screen.getByRole("textbox", { name: "Paste or edit requirements" }) as HTMLTextAreaElement;
    fireEvent.change(editor, { target: { value: source } });

    fireEvent.click(screen.getByRole("button", { name: /Ukrainian/ }));

    await waitFor(() => expect(screen.getByRole("heading", { name: "Аналіз специфікації" })).toBeTruthy());
    expect(editor.value).toBe(source);
    expect(document.querySelector(".requirement-list__text")?.textContent).toBe("Не змінювати   внутрішній текст!");
  });
});

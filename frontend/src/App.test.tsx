import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { App, DEMO_EVIDENCE_SOURCE_TEXT, DEMO_REQUIREMENT_SOURCE_TEXT } from "./App";
import { i18n, limitationCodes, limitationTranslationKey, LOCALE_SESSION_KEY } from "./i18n";

describe("presentation localization", () => {
  beforeEach(async () => {
    window.sessionStorage.clear();
    await i18n.changeLanguage("uk");
  });

  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("projects both locales without changing source or scientific identity", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    render(<App />);

    expect(screen.getByRole("heading", { name: "Основа Research UI" }).textContent).toBe("Основа Research UI");
    expect(screen.getByRole("button", { name: /англійську/ }).getAttribute("aria-pressed")).toBe("false");

    const sourceInput = screen.getByRole("textbox", { name: "Текст вимоги" }) as HTMLTextAreaElement;
    expect(sourceInput.value).toBe(DEMO_REQUIREMENT_SOURCE_TEXT);
    expect(screen.getAllByText("E-DEMO-001").length).toBeGreaterThan(0);
    expect(screen.getByRole("button", { name: new RegExp(DEMO_EVIDENCE_SOURCE_TEXT) })).toBeTruthy();
    expect(screen.getAllByText("COMPUTED").length).toBeGreaterThan(0);
    expect(screen.getAllByText("5/6").length).toBeGreaterThan(0);

    fireEvent.click(screen.getByRole("button", { name: /англійську/ }));

    expect(await screen.findByRole("heading", { name: "Research UI foundation" })).toBeTruthy();
    expect(screen.getByRole("button", { name: /Ukrainian/ }).getAttribute("aria-pressed")).toBe("false");
    expect(sourceInput.value).toBe(DEMO_REQUIREMENT_SOURCE_TEXT);
    expect(screen.getByRole("button", { name: new RegExp(DEMO_EVIDENCE_SOURCE_TEXT) })).toBeTruthy();
    expect(screen.getAllByText("COMPUTED").length).toBeGreaterThan(0);
    expect(screen.getAllByText("5/6").length).toBeGreaterThan(0);
    expect(window.sessionStorage.getItem(LOCALE_SESSION_KEY)).toBe("en");
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("makes a missing development translation visibly fail", () => {
    const consoleErrorSpy = vi.spyOn(console, "error").mockImplementation(() => undefined);

    const result = i18n.t("rui04.deliberatelyMissing", { ns: "common" });

    expect(result).toBe("⟦missing:rui04.deliberatelyMissing⟧");
    expect(result).not.toBe("rui04.deliberatelyMissing");
    expect(consoleErrorSpy).toHaveBeenCalledWith("[i18n] Missing translation: common:rui04.deliberatelyMissing");
  });

  it("translates every canonical API limitation code in both locales", async () => {
    for (const locale of ["uk", "en"] as const) {
      await i18n.changeLanguage(locale);

      for (const code of limitationCodes) {
        const key = limitationTranslationKey(code);
        const translation = i18n.t(key, { ns: "limitations" });

        expect(i18n.exists(key, { lng: locale, ns: "limitations" })).toBe(true);
        expect(translation).not.toBe(key);
        expect(translation).not.toContain("⟦missing:");
      }
    }
  });
});

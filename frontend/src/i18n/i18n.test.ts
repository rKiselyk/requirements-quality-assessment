import { afterEach, describe, expect, it, vi } from "vitest";
import { i18n, limitationCodes, limitationTranslationKey } from ".";

describe("RUI-04 localization regressions", () => {
  afterEach(() => {
    vi.restoreAllMocks();
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

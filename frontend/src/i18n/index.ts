import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import { namespaces, resources } from "./resources";

export const supportedLocales = ["uk", "en"] as const;
export type SupportedLocale = (typeof supportedLocales)[number];
export const DEFAULT_LOCALE: SupportedLocale = "uk";
export const LOCALE_SESSION_KEY = "research-ui.locale";

function isSupportedLocale(value: string | null): value is SupportedLocale {
  return value !== null && supportedLocales.some((locale) => locale === value);
}

function initialLocale(): SupportedLocale {
  if (typeof window === "undefined") return DEFAULT_LOCALE;
  const stored = window.sessionStorage.getItem(LOCALE_SESSION_KEY);
  return isSupportedLocale(stored) ? stored : DEFAULT_LOCALE;
}

void i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: initialLocale(),
    supportedLngs: supportedLocales,
    fallbackLng: false,
    defaultNS: "common",
    ns: namespaces,
    interpolation: { escapeValue: false },
    initAsync: false,
    returnNull: false,
    saveMissing: import.meta.env.DEV,
    missingKeyHandler: (_languages, namespace, key) => {
      if (import.meta.env.DEV) console.error(`[i18n] Missing translation: ${namespace}:${key}`);
    },
    parseMissingKeyHandler: (key) => import.meta.env.DEV ? `⟦missing:${key}⟧` : key,
  });

function reflectLocale(locale: string) {
  if (!isSupportedLocale(locale)) return;
  if (typeof document !== "undefined") document.documentElement.lang = locale;
  if (typeof window !== "undefined") window.sessionStorage.setItem(LOCALE_SESSION_KEY, locale);
}

reflectLocale(i18n.resolvedLanguage ?? i18n.language);
i18n.on("languageChanged", reflectLocale);

export { i18n };
export * from "./lookup";

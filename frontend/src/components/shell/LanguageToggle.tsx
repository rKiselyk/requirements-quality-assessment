import { useTranslation } from "react-i18next";
import { supportedLocales, type SupportedLocale } from "../../i18n";

export function LanguageToggle() {
  const { i18n, t } = useTranslation("common");
  const activeLocale = (i18n.resolvedLanguage ?? i18n.language) as SupportedLocale;

  return (
    <div className="language-toggle" role="group" aria-label={t("language.label")} data-active-locale={activeLocale}>
      {supportedLocales.map((locale, index) => {
        const active = locale === activeLocale;
        return (
          <span key={locale} className="language-toggle__item">
            {index > 0 ? <span aria-hidden="true">|</span> : null}
            <button
              type="button"
              lang={locale}
              className={`language-toggle__option ${active ? "language-toggle__option--active" : ""}`.trim()}
              aria-pressed={active}
              aria-label={t("language.switchTo", { language: t(`language.${locale}`) })}
              onClick={() => { if (!active) void i18n.changeLanguage(locale); }}
            >
              {locale === "uk" ? "UA" : "EN"}
            </button>
          </span>
        );
      })}
    </div>
  );
}

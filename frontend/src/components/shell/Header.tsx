import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { LanguageToggle } from "./LanguageToggle";

export function Header({ actions }: { actions?: ReactNode }) {
  const { t } = useTranslation("common");
  return (
    <header className="app-header">
      <div className="app-header__brand"><span>{t("app.brand")}</span><span className="prototype-label">{t("app.prototype")}</span></div>
      <div className="app-header__actions">{actions}<LanguageToggle /></div>
    </header>
  );
}

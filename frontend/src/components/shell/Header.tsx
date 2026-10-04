import type { ReactNode } from "react";
import { LanguageToggle } from "./LanguageToggle";

export function Header({ actions }: { actions?: ReactNode }) {
  return (
    <header className="app-header">
      <div className="app-header__brand"><span>Requirements Quality Assessment</span><span className="prototype-label">Research Prototype</span></div>
      <div className="app-header__actions">{actions}<LanguageToggle /></div>
    </header>
  );
}

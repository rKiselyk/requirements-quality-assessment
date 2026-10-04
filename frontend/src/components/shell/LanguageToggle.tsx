export function LanguageToggle() {
  return (
    <div className="language-toggle" role="group" aria-label="Presentation language placeholder">
      <button type="button" className="language-toggle__option language-toggle__option--active" aria-pressed="true" title="Localization is added in RUI-04">UA</button>
      <span aria-hidden="true">|</span>
      <button type="button" className="language-toggle__option" aria-pressed="false" title="Localization is added in RUI-04">EN</button>
    </div>
  );
}

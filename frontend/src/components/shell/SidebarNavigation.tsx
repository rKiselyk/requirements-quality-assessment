export interface NavigationItem {
  id: string;
  label: string;
}

export function SidebarNavigation({ items, activeId, onNavigate }: { items: readonly NavigationItem[]; activeId: string; onNavigate?: (id: string) => void }) {
  const { t } = useTranslation("common");
  return (
    <aside className="sidebar">
      <nav aria-label={t("navigation.label")}>
        <ul>{items.map((item) => <li key={item.id}><button type="button" className="sidebar__link" aria-current={item.id === activeId ? "page" : undefined} onClick={() => onNavigate?.(item.id)}>{item.label}</button></li>)}</ul>
      </nav>
    </aside>
  );
}
import { useTranslation } from "react-i18next";

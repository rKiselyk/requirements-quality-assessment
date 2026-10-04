export interface NavigationItem {
  id: string;
  label: string;
}

export function SidebarNavigation({ items, activeId, onNavigate }: { items: readonly NavigationItem[]; activeId: string; onNavigate?: (id: string) => void }) {
  return (
    <aside className="sidebar">
      <nav aria-label="Research result sections">
        <ul>{items.map((item) => <li key={item.id}><button type="button" className="sidebar__link" aria-current={item.id === activeId ? "page" : undefined} onClick={() => onNavigate?.(item.id)}>{item.label}</button></li>)}</ul>
      </nav>
    </aside>
  );
}

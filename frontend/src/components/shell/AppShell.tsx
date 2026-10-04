import type { ReactNode } from "react";
import { Header } from "./Header";
import { SidebarNavigation, type NavigationItem } from "./SidebarNavigation";

export interface AppShellProps {
  children: ReactNode;
  headerActions?: ReactNode;
  navigation?: readonly NavigationItem[];
  activeNavigationId?: string;
  onNavigate?: (id: string) => void;
}

export function AppShell({ children, headerActions, navigation, activeNavigationId = "", onNavigate }: AppShellProps) {
  const hasNavigation = Boolean(navigation?.length);
  return (
    <div className="app-shell">
      <Header actions={headerActions} />
      <div className={`app-shell__body ${hasNavigation ? "app-shell__body--with-sidebar" : ""}`}>
        {navigation ? <SidebarNavigation items={navigation} activeId={activeNavigationId} onNavigate={onNavigate} /> : null}
        <main id="main-content" className="main-content">{children}</main>
      </div>
    </div>
  );
}

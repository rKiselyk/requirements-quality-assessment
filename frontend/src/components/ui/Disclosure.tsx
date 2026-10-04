import { useId, useState, type ReactNode } from "react";

export interface TabsItem {
  id: string;
  label: string;
  content: ReactNode;
}

export function Tabs({ items, label }: { items: readonly TabsItem[]; label: string }) {
  const [activeId, setActiveId] = useState(items[0]?.id ?? "");
  const activeItem = items.find((item) => item.id === activeId);
  const prefix = useId();

  const move = (index: number, direction: number) => {
    if (!items.length) return;
    const next = (index + direction + items.length) % items.length;
    setActiveId(items[next].id);
    document.getElementById(`${prefix}-tab-${items[next].id}`)?.focus();
  };

  return (
    <div className="tabs">
      <div className="tabs__list" role="tablist" aria-label={label}>
        {items.map((item, index) => (
          <button
            id={`${prefix}-tab-${item.id}`}
            key={item.id}
            className="tabs__tab"
            type="button"
            role="tab"
            aria-selected={item.id === activeId}
            aria-controls={`${prefix}-panel-${item.id}`}
            tabIndex={item.id === activeId ? 0 : -1}
            onClick={() => setActiveId(item.id)}
            onKeyDown={(event) => {
              if (event.key === "ArrowRight") { event.preventDefault(); move(index, 1); }
              if (event.key === "ArrowLeft") { event.preventDefault(); move(index, -1); }
            }}
          >{item.label}</button>
        ))}
      </div>
      {activeItem ? <div id={`${prefix}-panel-${activeItem.id}`} className="tabs__panel" role="tabpanel" aria-labelledby={`${prefix}-tab-${activeItem.id}`}>{activeItem.content}</div> : null}
    </div>
  );
}

export interface AccordionItem {
  id: string;
  title: string;
  content: ReactNode;
}

export function Accordion({ items }: { items: readonly AccordionItem[] }) {
  return <div className="accordion">{items.map((item) => <details key={item.id} className="collapsible"><summary>{item.title}</summary><div className="collapsible__content">{item.content}</div></details>)}</div>;
}

export const Collapsible = Accordion;

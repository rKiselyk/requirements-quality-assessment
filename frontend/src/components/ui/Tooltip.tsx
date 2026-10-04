import { useId, type ReactElement } from "react";

export function Tooltip({ content, children }: { content: string; children: ReactElement }) {
  const id = useId();
  return <span className="tooltip" tabIndex={0} aria-describedby={id}>{children}<span id={id} className="tooltip__bubble" role="tooltip">{content}</span></span>;
}

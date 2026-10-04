import { AppShell } from "./components/shell";
import { SpecificationInputPage } from "./features/specification-input/SpecificationInputPage";
import type { Rui05AnalyzeRequest } from "./features/specification-input/model";

export interface AppProps {
  onAnalyzeRequest?: (request: Rui05AnalyzeRequest) => void;
}

export function App({ onAnalyzeRequest = () => undefined }: AppProps) {
  return (
    <AppShell>
      <SpecificationInputPage onAnalyzeRequest={onAnalyzeRequest} />
    </AppShell>
  );
}

export type { Rui05AnalyzeRequest } from "./features/specification-input/model";

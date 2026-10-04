export interface RequirementInput {
  text: string;
  source_line: number;
}

export interface InitialAnalyzeRequest {
  case: "INITIAL";
  requirements: RequirementInput[];
}

export interface ControlledDemoAnalyzeRequest {
  case: "CONTROLLED_DEMO";
  scenario: {
    id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO";
    version: "1";
  };
}

export type Rui05AnalyzeRequest = InitialAnalyzeRequest | ControlledDemoAnalyzeRequest;

export const CONTROLLED_DEMO_REQUEST: ControlledDemoAnalyzeRequest = {
  case: "CONTROLLED_DEMO",
  scenario: {
    id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO",
    version: "1",
  },
};

export function parseSpecificationText(source: string): RequirementInput[] {
  return source
    .split(/\r\n|\n|\r/)
    .map((line, index) => ({ text: line.trim(), source_line: index + 1 }))
    .filter((requirement) => requirement.text.length > 0);
}

export function createInitialAnalyzeRequest(source: string): InitialAnalyzeRequest {
  return {
    case: "INITIAL",
    requirements: parseSpecificationText(source),
  };
}

export function isSupportedSpecificationFile(file: File): boolean {
  return file.name.toLocaleLowerCase("en-US").endsWith(".txt") || file.type === "text/plain";
}

export async function readSpecificationFile(file: File): Promise<string> {
  const bytes = await file.arrayBuffer();
  return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
}

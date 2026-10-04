import { useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { PageHeader } from "../../components/shell";
import { Button, Callout, Card, FileDropzone, InlineValidation, TextArea } from "../../components/ui";
import {
  CONTROLLED_DEMO_REQUEST,
  createInitialAnalyzeRequest,
  isSupportedSpecificationFile,
  parseSpecificationText,
  readSpecificationFile,
  type Rui05AnalyzeRequest,
} from "./model";

export interface SpecificationInputPageProps {
  onAnalyzeRequest: (request: Rui05AnalyzeRequest) => void;
}

type FileValidation = "unsupported" | "unreadable" | null;

export function SpecificationInputPage({ onAnalyzeRequest }: SpecificationInputPageProps) {
  const { t } = useTranslation("input");
  const [sourceText, setSourceText] = useState("");
  const [fileName, setFileName] = useState<string | null>(null);
  const [fileValidation, setFileValidation] = useState<FileValidation>(null);
  const readSequence = useRef(0);
  const requirements = useMemo(() => parseSpecificationText(sourceText), [sourceText]);
  const isEmpty = requirements.length === 0;

  const replaceSource = (nextText: string, nextFileName: string | null) => {
    readSequence.current += 1;
    setSourceText(nextText);
    setFileName(nextFileName);
    setFileValidation(null);
  };

  const receiveFile = async (file: File) => {
    const sequence = readSequence.current + 1;
    readSequence.current = sequence;
    setFileValidation(null);

    if (!isSupportedSpecificationFile(file)) {
      setFileValidation("unsupported");
      return;
    }

    try {
      const text = await readSpecificationFile(file);
      if (readSequence.current !== sequence) return;
      setSourceText(text);
      setFileName(file.name);
    } catch {
      if (readSequence.current === sequence) setFileValidation("unreadable");
    }
  };

  const submitInitial = () => {
    if (isEmpty) return;
    onAnalyzeRequest(createInitialAnalyzeRequest(sourceText));
  };

  return (
    <div className="input-page">
      <PageHeader title={t("pageTitle")} subtitle={t("pageSubtitle")} />

      <Card title={t("ordinary.title")} description={t("ordinary.description")}>
        <div className="input-workflow">
          <FileDropzone
            label={t("file.label")}
            description={t("file.description")}
            accept=".txt,text/plain"
            onFile={(file) => { void receiveFile(file); }}
          />
          {fileName ? <p className="selected-file">{t("file.selected", { fileName })}</p> : null}
          {fileValidation ? <InlineValidation>{t(`validation.${fileValidation}`)}</InlineValidation> : null}

          <div className="input-separator" aria-hidden="true"><span>{t("ordinary.or")}</span></div>

          <TextArea
            label={t("editor.label")}
            hint={t("editor.hint")}
            placeholder={t("editor.placeholder")}
            rows={9}
            value={sourceText}
            onChange={(event) => replaceSource(event.target.value, null)}
            error={isEmpty ? t("validation.empty") : undefined}
          />

          <section className="requirement-preview" aria-labelledby="requirement-preview-title">
            <div className="requirement-preview__header">
              <div>
                <h2 id="requirement-preview-title">{t("preview.title")}</h2>
                <p aria-live="polite">{t("preview.count", { count: requirements.length })}</p>
              </div>
              <Button type="button" variant="quiet" disabled={!sourceText} onClick={() => replaceSource("", null)}>
                {t("actions.clear")}
              </Button>
            </div>
            {requirements.length > 0 ? (
              <ol className="requirement-list">
                {requirements.map((requirement) => (
                  <li key={requirement.source_line}>
                    <span className="requirement-list__line">{t("preview.sourceLine", { line: requirement.source_line })}</span>
                    <span className="requirement-list__text">{requirement.text}</span>
                  </li>
                ))}
              </ol>
            ) : <p className="requirement-preview__empty">{t("preview.empty")}</p>}
          </section>

          <div className="input-actions">
            <Button type="button" variant="primary" disabled={isEmpty} onClick={submitInitial}>
              {t("actions.analyze")}
            </Button>
          </div>
        </div>
      </Card>

      <section className="demo-entry">
        <Callout title={t("demo.title")} tone="warning">
          <p>{t("demo.description")}</p>
          <p>{t("demo.boundary")}</p>
          <Button type="button" variant="secondary" onClick={() => onAnalyzeRequest(CONTROLLED_DEMO_REQUEST)}>
            {t("actions.loadDemo")}
          </Button>
        </Callout>
      </section>
    </div>
  );
}

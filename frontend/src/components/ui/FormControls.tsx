import { useId, useState, type DragEvent, type InputHTMLAttributes, type TextareaHTMLAttributes } from "react";
import { InlineValidation } from "./Feedback";

interface FieldProps {
  label: string;
  hint?: string;
  error?: string;
}

export type TextInputProps = FieldProps & InputHTMLAttributes<HTMLInputElement>;

export function TextInput({ label, hint, error, id, className = "", ...props }: TextInputProps) {
  const generatedId = useId();
  const fieldId = id ?? generatedId;
  const hintId = `${fieldId}-hint`;
  const errorId = `${fieldId}-error`;
  return (
    <div className="field">
      <label className="field__label" htmlFor={fieldId}>{label}</label>
      <input
        id={fieldId}
        className={`field__control ${error ? "field__control--invalid" : ""} ${className}`.trim()}
        aria-invalid={Boolean(error)}
        aria-describedby={[hint ? hintId : "", error ? errorId : ""].filter(Boolean).join(" ") || undefined}
        {...props}
      />
      {hint ? <span id={hintId} className="field__hint">{hint}</span> : null}
      {error ? <InlineValidation id={errorId}>{error}</InlineValidation> : null}
    </div>
  );
}

export type TextAreaProps = FieldProps & TextareaHTMLAttributes<HTMLTextAreaElement>;

export function TextArea({ label, hint, error, id, className = "", ...props }: TextAreaProps) {
  const generatedId = useId();
  const fieldId = id ?? generatedId;
  const hintId = `${fieldId}-hint`;
  const errorId = `${fieldId}-error`;
  return (
    <div className="field">
      <label className="field__label" htmlFor={fieldId}>{label}</label>
      <textarea
        id={fieldId}
        className={`field__control field__textarea ${error ? "field__control--invalid" : ""} ${className}`.trim()}
        aria-invalid={Boolean(error)}
        aria-describedby={[hint ? hintId : "", error ? errorId : ""].filter(Boolean).join(" ") || undefined}
        {...props}
      />
      {hint ? <span id={hintId} className="field__hint">{hint}</span> : null}
      {error ? <InlineValidation id={errorId}>{error}</InlineValidation> : null}
    </div>
  );
}

export interface FileDropzoneProps {
  label: string;
  description?: string;
  accept?: string;
  disabled?: boolean;
  onFile?: (file: File) => void;
}

export function FileDropzone({ label, description, accept = ".txt,text/plain", disabled = false, onFile }: FileDropzoneProps) {
  const id = useId();
  const [dragging, setDragging] = useState(false);

  const receive = (files: FileList | null) => {
    const file = files?.item(0);
    if (file) onFile?.(file);
  };

  const onDrop = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    setDragging(false);
    if (!disabled) receive(event.dataTransfer.files);
  };

  return (
    <label
      className={`dropzone ${dragging ? "dropzone--active" : ""} ${disabled ? "dropzone--disabled" : ""}`.trim()}
      htmlFor={id}
      onDragEnter={(event) => { event.preventDefault(); if (!disabled) setDragging(true); }}
      onDragOver={(event) => event.preventDefault()}
      onDragLeave={() => setDragging(false)}
      onDrop={onDrop}
    >
      <span className="dropzone__icon" aria-hidden="true">⇧</span>
      <span className="dropzone__label">{label}</span>
      {description ? <span className="dropzone__description">{description}</span> : null}
      <input id={id} className="visually-hidden" type="file" accept={accept} disabled={disabled} onChange={(event) => receive(event.target.files)} />
    </label>
  );
}

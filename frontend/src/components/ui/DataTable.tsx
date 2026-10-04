import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";

export interface DataTableColumn<Row> {
  key: string;
  header: ReactNode;
  render: (row: Row) => ReactNode;
  headerScope?: "col" | "row";
}

export interface DataTableProps<Row> {
  caption: string;
  columns: readonly DataTableColumn<Row>[];
  rows: readonly Row[];
  rowKey: (row: Row) => string;
  emptyMessage?: string;
}

export function DataTable<Row>({ caption, columns, rows, rowKey, emptyMessage }: DataTableProps<Row>) {
  const { t } = useTranslation("common");
  const resolvedEmptyMessage = emptyMessage ?? t("table.noRecords");
  return (
    <div className="table-scroll" tabIndex={0} role="region" aria-label={t("table.scrollableRegion", { caption })}>
      <table className="data-table">
        <caption>{caption}</caption>
        <thead><tr>{columns.map((column) => <th key={column.key} scope="col">{column.header}</th>)}</tr></thead>
        <tbody>
          {rows.length ? rows.map((row) => (
            <tr key={rowKey(row)}>{columns.map((column) => <td key={column.key}>{column.render(row)}</td>)}</tr>
          )) : <tr><td colSpan={columns.length} className="data-table__empty">{resolvedEmptyMessage}</td></tr>}
        </tbody>
      </table>
    </div>
  );
}

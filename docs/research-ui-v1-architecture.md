# Research UI v1 implementation map

**Status:** non-normative implementation guide

This map is subordinate to `model-spec.md`, the accepted Full Model contracts,
and `research-ui-v1-contract.md`. It introduces no scientific rule.

## Processing boundary

```text
UTF-8 file or pasted text
→ browser input model (one trimmed non-empty physical line per requirement)
→ POST /api/v1/analyze
→ stateless FastAPI transport/application adapter
→ accepted application and scientific/domain services
→ canonical AnalyzeResponse
→ temporary React analysis session
→ defensive presentation projections
→ result pages
```

The domain/application layer remains the only scientific source of truth. The
FastAPI adapter validates one legal interaction case, calls an accepted service
boundary, and serializes canonical records. React retains only temporary
workflow state and turns canonical records into view data. Its projections are
presentation guards: they reject missing or contradictory shapes rather than
calculate, complete, normalize, compare, or reinterpret them.

## Request cases

| Case | Application path | Lifecycle meaning |
|---|---|---|
| `INITIAL` | Supplied requirements → accepted requirement/specification assessment | One specification-only result. Downstream sections requiring external evidence remain explicitly unavailable. |
| `CONTROLLED_DEMO` | Exact `CONTROLLED_RESEARCH_REFERENCE_SCENARIO / 1` → accepted `FullModelService` path | Versioned fixture with a genuine accepted two-version lifecycle and complete supported result surface. |
| `REASSESSMENT` | Canonical revised requirements + complete prior context → stateless validation and accepted reassessment path | Explicit second analysis. The returned response replaces the browser's current result atomically. |

There is no server-side history, database, account, or hidden session. Formal
reassessment carries the complete canonical prior lifecycle context. The
frontend never replaces it with a browser-generated summary and never merges
two independent analysis responses into a formal comparison.

## Page ownership

| Page | Canonical ownership |
|---|---|
| Overview | Separate requirement/specification summaries, section availability, and bounded pipeline presence. No combined score. |
| Requirements | Ordered source records, C/V/U, full property profiles when present, evidence, Findings, diagnostics, and assessment trace. |
| Specification | Separate C/V/U aggregates, QB, counts, bounded cross-results, and trace. |
| Product Quality | Criterion/observation/conformance, `X_PE`, observed result, and prediction as distinct records. |
| Risk | Confirmed-problem relations, categorical risk, and quantitative local risk as distinct records. |
| Corrective Actions | Resolution, proposal/application, external revision, and the eligible formal reassessment entry. |
| Process | Canonical states, transition, associations, checkpoint source identity, predicate outcome, and limitation. |
| Audit | Recursive inspection of structured canonical transport data; never parsed console-report text. |
| Reassessment | Canonical `ReassessmentRun`, v1/v2 snapshots, produced result families, and evidence-reuse decisions. |
| Comparison | Backend-produced compatible `ResultComparison` records only; the frontend does not calculate a comparison. |

Reassessment and Comparison are absent from ordinary `INITIAL` navigation.
They may appear immediately for `CONTROLLED_DEMO` because its approved fixture
already contains a genuine lifecycle, and remain available on a valid returned
`REASSESSMENT` response.

Exact rational values, source/evidence text, offsets, canonical identities,
states, applicability, reasons, versions, provenance, and calibration remain
unchanged across transport and presentation. Localization applies only to UI
copy.

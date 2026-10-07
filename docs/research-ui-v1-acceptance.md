# Research UI v1 acceptance evidence — phase 1

**Issue:** #186 / RUI-16

**Status:** `PENDING_FINAL_COMMITTED_SHA_ACCEPTANCE`

**Accepted main baseline:** `6b61b4b8198aaadfec1c982a4dd167faaf7c9671`

**FINAL_ACCEPTANCE_MARKER:** `PENDING`

This phase adds acceptance infrastructure and records local pre-commit evidence.
It does not self-certify the final committed PR HEAD. Final acceptance requires
independent review and a complete rerun against that exact implementation SHA.

## Authorities

1. `docs/model-spec.md` and accepted scientific/Full Model contracts;
2. `docs/research-ui-v1-contract.md`;
3. `docs/research-ui-v1-design-spec.md`;
4. `docs/assets/research-ui-v1-design.png`;
5. issue #186 acceptance wording where consistent with the frozen lifecycle.

## Implemented page matrix

| Page | `INITIAL` | `CONTROLLED_DEMO` | `REASSESSMENT` |
|---|---|---|---|
| Overview | available | available | available |
| Requirements | available | available | available |
| Specification | available | available | available |
| Product Quality | canonical unavailable presentation | available | available |
| Risk | canonical unavailable presentation | available | available |
| Corrective Actions | canonical unavailable presentation | available | available |
| Process | canonical unavailable presentation | available | available |
| Audit | available, including `full_model: null` | available | available |
| Reassessment | absent from navigation | available from genuine fixture lifecycle | available |
| Comparison | absent from navigation | available from genuine fixture lifecycle | available |

## Scenario checklists

### A — specification only

- [x] Parsed requirement count verified.
- [x] Exactly one `INITIAL` POST observed.
- [x] Exactly eight base navigation pages; no lifecycle pages.
- [x] Every base page visited.
- [x] Four required downstream unavailable reason codes verified.
- [x] Exact source text, evidence, offsets, and rational values verified.
- [x] Audit remains usable with `full_model: null`.
- [x] New specification resets the session and removes result navigation.

### B — controlled complete demonstration

- [x] Exactly one `CONTROLLED_DEMO` POST observed with scenario identity/version.
- [x] Ten legal result pages visible immediately under the frozen contract.
- [x] Representative product-quality, risk, action, process/checkpoint, audit,
      reassessment, and comparison records verified without recalculation.
- [x] Controlled fixture labels and scientific limitations remain visible.

### C — formal reassessment

- [x] Canonical revised specification explicitly shown in the editor.
- [x] Non-canonical draft disables submission; exact restoration enables it.
- [x] Second POST is `REASSESSMENT` with requirements and complete prior context.
- [x] No browser-generated scientific summary replaces prior context.
- [x] Returned response case is `REASSESSMENT` and replaces current UI state.
- [x] Reassessment uses v2 records; Comparison uses four backend-produced records.
- [x] Structured-change and non-causal/non-directional/non-success limitations verified.

## Localization checklist

- [x] Relevant controlled/reassessment paths run in `uk` and `en`.
- [x] Navigation and headings change language without another POST.
- [x] Requirement/evidence text, canonical IDs/codes, rational values, and
      lifecycle eligibility remain unchanged.

## Accessibility smoke checklist

**Automated engine:** `@axe-core/playwright` / Axe

**Required scan pages:** input, INITIAL Overview, INITIAL Requirements,
controlled-demo Overview, Process, Audit, Reassessment, Comparison.

- Serious violations: `0` in the supplemental Microsoft Edge run.
- Critical violations: `0` in the supplemental Microsoft Edge run.
- [x] Language toggle, sidebar, Analyze, Audit disclosures, EvidenceDrawer,
      and reassessment controls checked for keyboard reachability/operation.
- [x] EvidenceDrawer closes with Escape and restores trigger focus.

This is accessibility smoke acceptance only, not WCAG certification. The Audit
scan covers its visible collapsed disclosure surface and excludes recursively
hidden `.audit-node__children`; disclosure semantics and nested preservation are
covered separately by keyboard E2E and 69 Audit unit tests.

## Visual checklist

**Viewport:** `1440 × 1000` desktop, plus `900 × 1000` minimum-width smoke.

**Design authority:** `docs/assets/research-ui-v1-design.png` interpreted with
`docs/research-ui-v1-design-spec.md` and higher scientific/application contracts.

Transient screenshots are generated under `frontend/test-results/rui16-visual/`:

- `a1-initial-overview.png`
- `a2-initial-unavailable-product-quality.png`
- `b1-controlled-demo-overview.png`
- `b2-controlled-demo-risk.png`
- `b3-controlled-demo-process.png`
- `b4-controlled-demo-audit-expanded.png`
- `b5-controlled-demo-overview-uk.png`
- `c1-reassessment.png`
- `c2-comparison.png`
- `c3-comparison-uk.png`

**Semantic comparison status:** `ACCEPTED_SUPPLEMENTAL_EDGE`

The review covered header/sidebar proportions, readable content width, spacing,
hierarchy, card grouping, long technical IDs, exact values, overflow, EN/UK
labels, neutral scientific semantics, Audit, Reassessment, Comparison, and
EvidenceDrawer placement/focus. The visual implementation is semantically
consistent with the design authority. Long Reassessment and Comparison pages
remain dense because they intentionally expose canonical trace records.

## Commands and phase-1 results

| Command | Result |
|---|---|
| `python -m pytest tests/test_api.py -q` | `25 passed, 1 PytestCacheWarning in 21.75s` |
| `python -m pytest tests/test_research_ui_v1_acceptance.py -q` | `1 passed, 1 PytestCacheWarning in 5.37s` |
| `python -m pytest -q` | environment failure after `1450 passed`: 60 `WinError 5` errors from the host global pytest temp root |
| `python -m pytest -q --basetemp .pytest-basetemp-rui16-final-20261007 -p no:cacheprovider` | `1511 passed in 471.34s` |
| `cd frontend; npm install` | completed; final audit covers 243 packages with 0 vulnerabilities |
| `cd frontend; npm test` | `13` files, `804 passed` in `8.18s` |
| `cd frontend; npm run lint` | passed |
| `cd frontend; npm run typecheck` | passed |
| `cd frontend; npm run build` | passed; 191 modules; existing 677.77 kB chunk advisory |
| `cd frontend; npx playwright install chromium` | `BLOCKED_BY_ENVIRONMENT`: all CDN attempts timed out; bundled executable remains absent |
| `cd frontend; npm run test:e2e` | `BLOCKED_BY_ENVIRONMENT`: two launch failures because bundled Chromium is absent |
| `cd frontend; $env:RUI16_BROWSER_CHANNEL='msedge'; npm run test:e2e` | supplemental: `2 passed in 23.9s` |
| `cd frontend; $env:RUI16_BROWSER_CHANNEL='msedge'; npm run test:acceptance` | supplemental convenience gate passed; browser portion `2 passed in 26.0s` |

The production build's large-chunk advisory is non-blocking. The default
Chromium gate is not accepted as passed: Edge evidence is explicitly
supplemental and cannot substitute for the required bundled Chromium rerun.

## Final committed-SHA evidence placeholders

- Tested implementation SHA: `PENDING_POST_COMMIT_RERUN`
- Independent review: `PENDING`
- Exact command counts: phase-1 counts recorded above; committed-SHA rerun pending
- Accessibility smoke result: supplemental Edge passed; Chromium pending
- Visual semantic result: supplemental Edge accepted; Chromium pending
- Material deviations/blockers: bundled Chromium download/executable unavailable
- Final marker: `PENDING`

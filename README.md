# Requirements Quality Assessment

This research prototype has two explicitly bounded paths. Historical MVP v0.1
reads a UTF-8 text file, extracts six approved feature families, computes
separate Completeness, Verifiability, and Unambiguity assessments, aggregates
each characteristic across the file, and prints an explainable console report.
That historical mode does not predict software-product quality or produce an
overall scalar score. Full Model v1.0 adds a deterministic, traceable research
path without changing the historical CLI or its contracts.

[`docs/model-spec.md`](docs/model-spec.md) is the authoritative scientific
model. Its executable MVP v0.1 subset and the bounded TC-01 through TC-05 Full
Model components carry their recorded acceptance markers. TC-06 is independently
accepted under `TC06_INTEGRATED_RESEARCH_ACCEPTANCE_ACCEPTED`, making Full Model
v1.0 an accepted executable, deterministic, and traceable research realization
within its declared bounded reference scope. Constructs outside those boundaries
remain draft or unimplemented. [`docs/mvp-v0.1-baseline.md`](docs/mvp-v0.1-baseline.md)
describes the historical subset and limitations.

A stateless FastAPI adapter now exposes the accepted specification-assessment
path for the forthcoming Research UI v1. Its frozen boundary is documented in
[`docs/research-ui-v1-contract.md`](docs/research-ui-v1-contract.md), with the approved page/component baseline in [`docs/research-ui-v1-design-spec.md`](docs/research-ui-v1-design-spec.md). No web UI
recalculates scientific results or fabricates unavailable Full Model inputs.
The reusable React frontend foundation lives in [`frontend/`](frontend/).

## Requirements and installation

Python 3.11 or newer is required. The parser extra pins spaCy 3.8.16 and the Ukrainian `uk_core_news_sm` model 3.8.0. Install from the repository root in a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,parser]"
python -m pip check
```

On POSIX systems, activate with `. .venv/bin/activate`. The same `python -m pip install -e ".[dev,parser]"` command installs the package, tests, parser, and model. The model wheel is pinned in `pyproject.toml` by version and SHA-256. An internet connection or a package cache containing the pinned dependencies is needed for a fresh installation.

## Run the frontend foundation

The RUI-03 React, TypeScript, and Vite foundation is in `frontend/`. It provides
the shared shell, design tokens, reusable presentation components, and a static
development showcase. It does not yet implement the specification workflow,
API analysis integration, localization, or Research UI result pages.

Install and start the independent frontend development server:

```powershell
cd frontend
npm install
npm run dev
```

Run the TypeScript check and create a production build with:

```powershell
npm run typecheck
npm run build
```

The FastAPI backend remains the stateless scientific application boundary and
can be run separately as described below. RUI-03 configures TanStack Query for
later API integration but does not call or duplicate the backend contract.

## Run the HTTP API

The Research API is a thin, synchronous, stateless HTTP/JSON adapter over the
accepted application services. It does not define independent scoring
semantics or fabricate unavailable scientific inputs. One endpoint supports
the three frozen Research UI v1 cases: `INITIAL`, `CONTROLLED_DEMO`, and
`REASSESSMENT`.

Start the local server from the repository root:

```powershell
python -m uvicorn requirements_quality_assessment.api.app:app --reload
```

`GET /health` returns `{"status":"ok"}` without running the model. Interactive
OpenAPI documentation is available at [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs).

For an ordinary initial assessment, submit one source-ordered specification:

```json
{
  "case": "INITIAL",
  "requirements": [
    {
      "text": "Якщо сервіс недоступний, система повинна відповісти не більше ніж за 2 с.",
      "source_line": 1
    },
    {
      "text": "Система повинна швидко оновити статус.",
      "source_line": 3
    }
  ]
}
```

Scientific requirement IDs are always generated deterministically from the
one-based request position (`R001`, `R002`, ...); arbitrary client IDs are not
accepted. `source_line` is the positive physical line number in the original
source. Values must be unique and strictly increasing in request order; the
backend neither renumbers nor reorders them. Leading and trailing whitespace is
trimmed and blank requirements are rejected.

The accepted controlled demonstration is selected only by its frozen identity.
Clients cannot override its observations, parameters, policies, revision, or
other scientific fixture fields:

```json
{
  "case": "CONTROLLED_DEMO",
  "scenario": {
    "id": "CONTROLLED_RESEARCH_REFERENCE_SCENARIO",
    "version": "1"
  }
}
```

That response includes the genuine Full Model, revision, reassessment,
comparison, checkpoint, and process records produced by the accepted scenario,
plus a canonical `reassessment_context`. A formal reassessment sends that
complete context back with the externally revised specification:

```json
{
  "case": "REASSESSMENT",
  "requirements": [
    {"text": "Час відгуку ≤ 2 с при 500 одночасних користувачах", "source_line": 1},
    {"text": "Час відгуку ≤ 5 с при 500 одночасних користувачах", "source_line": 2}
  ],
  "prior_context": {"...": "canonical reassessment_context from CONTROLLED_DEMO"}
}
```

The backend stores no history. It validates the complete supplied context and
independently reruns the accepted path. An ordinary `INITIAL` response is not
sufficient prior context, and arbitrary v1/v2 analysis or comparison is not
supported.

A shortened successful response has this shape (exact rational values are
never converted to floating point):

```json
{
  "contract_version": "research-api-v1",
  "analysis_case": "INITIAL",
  "controlled_scenario": null,
  "requirements": [
    {
      "requirement": {"id": "R001", "source_line": 1, "text": "..."},
      "quality_profile": {
        "completeness": {
          "state": "COMPUTED",
          "value": {"numerator": 1, "denominator": 1},
          "assessment_rule_id": "CALC-C-MVP-001"
        }
      },
      "evidence": []
    }
  ],
  "specification": {
    "snapshot_id": "qb-snapshot-sha256:...",
    "quality_profile": {},
    "qb_consistency": {}
  },
  "section_availability": [],
  "full_model": null,
  "reassessment_context": null,
  "limitations": ["NO_COMBINED_QUALITY_SCORE"]
}
```

The complete response preserves requirement text and order, C/V/U states and
exact values, Findings, accepted Evidence and offsets, diagnostics, assessment
traces, specification aggregates, and bounded QB records. Optional downstream
sections that cannot legally be constructed from text alone are explicitly
marked `UNAVAILABLE` rather than fabricated.

OpenAPI exposes stable Full Model record families—criterion binding,
observation/conformance, product quality, problem/defect relations, categorical
and quantitative risk, corrective action, process, checkpoints, reassessment,
and comparisons. Their nested payloads remain canonical domain projections.
A reusable transport record documents shared `status`, `applicability`, and
`provenance` fields while permitting domain-specific fields, avoiding a second
scientific model in the HTTP layer.

## Run an assessment

Put one requirement on each non-empty line of a UTF-8 file, for example `requirements.txt`:

```text
Якщо сервіс недоступний, система повинна відповісти не більше ніж за 2 с.
Система повинна швидко оновити статус.
```

Run the default concise Ukrainian user view:

```powershell
python -m requirements_quality_assessment requirements.txt
```

Use the audit view when you need the complete scientific trace, including Rule
IDs, decision/effect codes, accepted observations, exact Evidence and offsets,
diagnostics, Findings, and coverage disclosures:

```powershell
python -m requirements_quality_assessment --view audit requirements.txt
```

The default command is equivalent to explicitly selecting `--view user`:

```powershell
python -m requirements_quality_assessment --view user requirements.txt
```

The Full Model v1.0 facade is available through a separate mode; it does not
change either historical command:

```powershell
python -m requirements_quality_assessment --mode full-model --config full-model.json --view user requirements.txt
```

The config has no built-in scientific fixture values. The public
`FullModelService` path composes the full nine-property requirement
representation, specification metrics and QB analysis, dynamic evidence,
observed Performance Efficiency evidence, explicitly parameterized prediction,
categorical and quantitative local risk, corrective action and externally
supplied revision, reassessment and literal comparison, an externally
parameterized checkpoint, and process-state lineage. USER and AUDIT reports are
read-only projections of those completed records. See
[`docs/full-model-config.md`](docs/full-model-config.md) for its strict JSON
shape and the programmatic-only predictor limitation, and
[`docs/full-model-v1-theory-traceability.md`](docs/full-model-v1-theory-traceability.md)
for the bounded theory-to-implementation mapping.

Leading and trailing whitespace is trimmed. Blank lines are ignored. Each remaining physical line is one requirement, even if it contains multiple sentences or clauses. The reader retains source order and line numbers, assigns IDs `R001`, `R002`, and so on, and retains punctuation in the trimmed text. The CLI reports missing files and invalid UTF-8 as errors with a nonzero exit code. An empty input produces a specification summary with zero requirements and `NOT_APPLICABLE` aggregates.

## Interpret the results

For each requirement, the concise user view shows the original text, three
separate exact results, three short Ukrainian explanations, and a conditional
`Звернути увагу` section for supported `SIGNAL` findings or material unresolved
diagnostics. Accepted Evidence and diagnostic candidates remain distinct. The
audit view exposes the complete trace behind the same already-computed results;
selecting a view does not rerun or change the assessment.

The three independent assessments are:

- **Completeness** (`CALC-C-MVP-001`) counts whether the approved condition/context, expected result, and acceptance criterion families are detected. In this MVP, all three are mandatory for each supported input; the value is their exact unweighted detected fraction.
- **Verifiability** (`CALC-V-MVP-001`) uses alternative evidence paths. An accepted acceptance criterion yields `1`; otherwise an accepted quantitative constraint or explicit verification method yields `1/2`; complete absence of all three yields `0`.
- **Unambiguity** (`CALC-U-MVP-001`) yields `1` when complete scanning finds no supported vague-term signal and `1/2` when it finds at least one. It does not produce `0`; confirmation of material ambiguity is a future research decision.

Values are displayed as exact fractions, without decimal conversion or rounding. `COMPUTED` means the approved rule produced a value. `UNKNOWN` means unresolved required detection could change the value, so no numeric value is shown. `NOT_APPLICABLE` means the approved applicability or aggregation contract has no applicable value; it is also shown for an empty specification. Neither unavailable state is zero. The current CLI supports individual input requirements for all three characteristics, so `NOT_APPLICABLE` is normally visible at specification level for empty input or in constructed domain/aggregation cases. Rule IDs and the complete contributing-feature trace are available in `--view audit`.

An accepted vague-term occurrence can create a `SIGNAL` Finding under `FIND-U-VAGUE-001`. A signal points to exact source evidence and is a potential ambiguity indicator, **not** a confirmed quality problem. No automatic `QUALITY_PROBLEM` conversion is approved for MVP v0.1. The user view shows the relevant source fragment once; the audit view additionally shows Evidence references, explanations, and Unicode code-point offsets.

`AGG-MVP-001` produces separate specification-level Completeness, Verifiability, and Unambiguity means from `COMPUTED` requirement assessments using exact fraction arithmetic. It excludes `UNKNOWN` and `NOT_APPLICABLE` from each mean and always displays computed, unknown, not-applicable, and total counts. If there are no computed values but at least one unknown value, the aggregate is `UNKNOWN`; if neither computed nor unknown values exist, it is `NOT_APPLICABLE`. There is no combined requirement or file score.

## Scope and limitations

Ukrainian is the supported language for language-dependent detection. The six
historical MVP feature families are condition/context, expected result,
acceptance criterion, quantitative constraint, explicit verification method,
and vague-term occurrence. Detectors implement only their approved baseline
grammars and vocabulary. Complex sentence and metric attachment, written-out
numbers, generic ranges, broader vague vocabulary, non-numeric acceptance
criteria, and confirmed-ambiguity rules remain research decisions. A score of
`1` means the approved bounded evidence check succeeded; it is not proof of
universal semantic completeness, verifiability, or unambiguity. The selected
parser may leave an input `UNKNOWN` where required analysis is unresolved.

Full Model v1.0 is an executable, deterministic, and traceable research
realization within a bounded reference scope. It is not exhaustive NLP
coverage, universal product-quality prediction, universal risk calibration, or
production readiness. It does not provide an English linguistic profile,
automatic requirement-type classification, a combined or integrated overall
scalar requirement or specification quality score, aggregate risk or priority,
release authorization, causal inference, or automatic rewriting. Separate
specification-level Completeness, Verifiability, and Unambiguity aggregates
remain available as documented above.

## Tests

Run the complete suite after installing both extras:

```powershell
python -m pytest -q
```

The real-parser integration tests require the pinned spaCy and Ukrainian model; inspect the pytest summary for skips rather than treating skipped parser tests as full acceptance. Acceptance evidence for a tested environment is recorded in [`docs/mvp-v0.1-acceptance.md`](docs/mvp-v0.1-acceptance.md).

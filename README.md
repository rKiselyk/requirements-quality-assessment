# Requirements Quality Assessment

This research prototype assesses the quality of individual software requirements as information artifacts. MVP v0.1 reads a UTF-8 text file, extracts six approved feature families, computes separate Completeness, Verifiability, and Unambiguity assessments, aggregates each characteristic across the file, and prints an explainable console report. It does not predict software-product quality or produce an overall scalar score.

[`docs/model-spec.md`](docs/model-spec.md) is the authoritative scientific model. Its **executable MVP v0.1 subset** is approved; the broader research specification remains a draft. [`docs/mvp-v0.1-baseline.md`](docs/mvp-v0.1-baseline.md) describes the accepted subset and limitations.

## Requirements and installation

Python 3.11 or newer is required. The parser extra pins spaCy 3.8.16 and the Ukrainian `uk_core_news_sm` model 3.8.0. Install from the repository root in a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,parser]"
python -m pip check
```

On POSIX systems, activate with `. .venv/bin/activate`. The same `python -m pip install -e ".[dev,parser]"` command installs the package, tests, parser, and model. The model wheel is pinned in `pyproject.toml` by version and SHA-256. An internet connection or a package cache containing the pinned dependencies is needed for a fresh installation.

## Run an assessment

Put one requirement on each non-empty line of a UTF-8 file, for example `requirements.txt`:

```text
Якщо сервіс недоступний, система повинна відповісти не більше ніж за 2 с.
Система повинна швидко оновити статус.
```

Run:

```powershell
python -m requirements_quality_assessment requirements.txt
```

Leading and trailing whitespace is trimmed. Blank lines are ignored. Each remaining physical line is one requirement, even if it contains multiple sentences or clauses. The reader retains source order and line numbers, assigns IDs `R001`, `R002`, and so on, and retains punctuation in the trimmed text. The CLI reports missing files and invalid UTF-8 as errors with a nonzero exit code. An empty input produces a specification summary with zero requirements and `NOT_APPLICABLE` aggregates.

## Interpret the results

For each requirement the report shows three separate assessments:

- **Completeness** (`CALC-C-MVP-001`) counts whether the approved condition/context, expected result, and acceptance criterion families are detected. In this MVP, all three are mandatory for each supported input; the value is their exact unweighted detected fraction.
- **Verifiability** (`CALC-V-MVP-001`) uses alternative evidence paths. An accepted acceptance criterion yields `1`; otherwise an accepted quantitative constraint or explicit verification method yields `1/2`; complete absence of all three yields `0`.
- **Unambiguity** (`CALC-U-MVP-001`) yields `1` when complete scanning finds no supported vague-term signal and `1/2` when it finds at least one. It does not produce `0`; confirmation of material ambiguity is a future research decision.

Values are displayed as exact fractions, without decimal conversion or rounding. Each computed assessment names its rule and explains contributing features. `COMPUTED` means the approved rule produced a value. `UNKNOWN` means unresolved required detection could change the value, so no numeric value is shown. `NOT_APPLICABLE` means the approved applicability or aggregation contract has no applicable value; it is also shown for an empty specification. Neither unavailable state is zero. The current CLI supports individual input requirements for all three characteristics, so `NOT_APPLICABLE` is normally visible at specification level for empty input or in constructed domain/aggregation cases.

An accepted vague-term occurrence can create a `SIGNAL` Finding under `FIND-U-VAGUE-001`. A signal points to exact source evidence and is a potential ambiguity indicator, **not** a confirmed quality problem. No automatic `QUALITY_PROBLEM` conversion is approved for MVP v0.1. The console report shows a Finding's evidence references and explanation; the underlying extraction result retains exact source text and Unicode code-point offsets.

`AGG-MVP-001` produces separate specification-level Completeness, Verifiability, and Unambiguity means from `COMPUTED` requirement assessments using exact fraction arithmetic. It excludes `UNKNOWN` and `NOT_APPLICABLE` from each mean and always displays computed, unknown, not-applicable, and total counts. If there are no computed values but at least one unknown value, the aggregate is `UNKNOWN`; if neither computed nor unknown values exist, it is `NOT_APPLICABLE`. There is no combined requirement or file score.

## Scope and limitations

Ukrainian is the supported language for language-dependent detection. The six feature families are condition/context, expected result, acceptance criterion, quantitative constraint, explicit verification method, and vague-term occurrence. Detectors implement only their approved baseline grammars and vocabulary. Complex sentence and metric attachment, written-out numbers, generic ranges, broader vague vocabulary, non-numeric acceptance criteria, and confirmed-ambiguity rules remain research decisions. A score of `1` means the approved MVP evidence check succeeded; it is not proof of universal semantic completeness, verifiability, or unambiguity. The selected parser may leave an input `UNKNOWN` where required analysis is unresolved. The prototype has no English linguistic profile, automatic requirement-type classification, cross-requirement consistency, risk model, or product-quality prediction.

## Tests

Run the complete suite after installing both extras:

```powershell
python -m pytest -q
```

The real-parser integration tests require the pinned spaCy and Ukrainian model; inspect the pytest summary for skips rather than treating skipped parser tests as full acceptance. Acceptance evidence for a tested environment is recorded in [`docs/mvp-v0.1-acceptance.md`](docs/mvp-v0.1-acceptance.md).

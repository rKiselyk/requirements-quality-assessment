# Requirements Quality Assessment

This repository contains a research prototype for automated assessment of
software-requirement quality.

## MVP v0.1 intent

The eventual MVP will read UTF-8 textual requirements, extract approved
deterministic features, evaluate Completeness, Verifiability, and Unambiguity,
and produce explainable console output.

The precise output contract is governed by
[`docs/model-spec.md`](docs/model-spec.md) and remains under researcher
approval. This project initialization does not approve or implement scoring or
aggregation rules.

## Development setup

Create and activate a virtual environment, install the package and development
dependencies in editable mode, then run the tests.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

### POSIX shells

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

# AGENTS.md

## Project scope

This repository contains the research prototype of the Requirements Quality
Assessment system.

For MVP v0.1, the system reads a UTF-8 text file containing one software
requirement per line, extracts deterministic textual and structural features,
calculates completeness, verifiability, and unambiguity, derives requirement-
level and file-level quality, and prints explainable results to the console.

## Research rules

- Treat `docs/model-spec.md` as the authoritative implementation model.
- Treat `docs/reference/` as research context and traceability sources, not as
  executable specifications.
- Do not invent scientific formulas.
- Do not invent coefficients or weights.
- Do not invent thresholds, score ranges, or rounding rules.
- Do not introduce undocumented quality criteria.
- Do not silently resolve contradictions or ambiguity in the theoretical
  documents.
- Do not silently introduce NLP heuristics, dictionaries, vocabularies, or
  semantic assumptions.
- If the model specification does not define a required rule or value, document
  the unresolved research decision, stop the affected task, and leave its
  implementation blocked instead of guessing.
- All quality metrics must be explainable.
- Every score must provide its contributing features and reasons.
- Every detected problem must preserve enough evidence to explain why it was
  detected.
- Every implemented numeric result must be traceable to `docs/model-spec.md`.
- Keep the mathematical model, implementation, and tests traceable to each
  other.
- Research assumptions must be documented explicitly.
- Prefer deterministic and reproducible behavior.

## Required architecture

Preserve this processing pipeline:

```text
Text file
-> RequirementReader
-> FeatureExtractor
-> RequirementFeatures
-> CharacteristicCalculators
-> RequirementQualityAggregator
-> FileQualityAggregator
-> ConsoleReporter
```

- Quality calculators depend only on domain models and the approved model
  specification.
- Quality calculators must not depend on `FeatureExtractor` or any concrete
  feature-extraction implementation.
- Quality calculators must be independently testable with manually constructed
  `RequirementFeatures`, without files, CLI code, an extractor, or an NLP
  library.
- File I/O must not be implemented inside calculators.
- CLI code must contain orchestration only and no business logic.
- Feature extraction and quality calculation must remain separate layers.
- Any NLP-library-specific implementation must stay behind the feature
  extraction boundary.
- `FeatureExtractor` accepts `Requirement` and returns `RequirementFeatures`.
  It must not calculate quality scores, and no NLP-specific object may escape
  this boundary.
- Feature extraction must preserve evidence using the representation approved
  by the domain model.
- Requirement-level and file-level aggregators operate on structured assessment
  results, not raw files, CLI state, feature-extraction implementations, or
  NLP-library-specific objects.
- `ConsoleReporter` formats completed results and must not calculate scores.

## Input policy for MVP v0.1

- Decode input as UTF-8.
- Treat each non-empty line as one requirement.
- Trim leading and trailing whitespace.
- Ignore blank and whitespace-only lines.
- Preserve original source line numbers and input order.
- Generate requirement IDs automatically in processing order.

## Engineering rules

- Use a Python `src` layout and `pytest`.
- Keep external dependencies minimal; prefer the Python standard library.
- Use explicit typed domain models at component boundaries.
- Every calculator requires unit tests.
- Add tests for every approved rule and important edge case.
- Do not silently decide unspecified behavior such as malformed-input handling,
  score presentation, or rounding.
- Do not add databases, REST APIs, web UI, authentication, Docker, cloud
  infrastructure, custom neural-network training, LLM API integrations, a risk
  model, a defect-probability model, a corrective-action engine, or advanced
  semantic consistency analysis unless an issue explicitly requests it.

## Delivery workflow

Use this workflow for each implementation issue:

```text
Issue
-> Codex implementation
-> tests
-> local review
-> commit
-> push
-> pull request
-> merge
```

- Keep one issue scoped to one pull request.
- Do not mix unrelated changes into an issue branch.
- Use stable branch names in the form `mvp/NN-short-description`, for example:
  `mvp/01-project-init`, `mvp/02-domain-models`, and `mvp/03-model-spec`.
- Ensure tests pass and perform a local review before committing.
- Keep the commit and pull-request history clear enough to trace when an
  algorithm, formula, assumption, or test changed.

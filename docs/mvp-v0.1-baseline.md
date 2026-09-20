# MVP v0.1 executable baseline

## Status and scope

This document describes the **approved executable MVP v0.1 subset** of [`model-spec.md`](model-spec.md). The wider research specification remains a draft. Acceptance evidence for a particular commit and environment belongs in [`mvp-v0.1-acceptance.md`](mvp-v0.1-acceptance.md); this document does not declare a release tag or a complete scientific model.

MVP v0.1 treats one non-empty, trimmed UTF-8 input line as one individual requirement. It assigns processing-order IDs and preserves source line numbers, order, text, punctuation, exact evidence spans, and zero-based Unicode code-point offsets. The implemented output is a three-dimensional requirement quality profile and separate specification-level property summaries. It has no scalar requirement or file score and makes no software-product-quality prediction.

## Implemented pipeline and boundaries

```text
UTF-8 text file
→ RequirementReader
→ BaselineFeatureExtractor (FeatureExtractor boundary)
→ RequirementExtractionResult (RequirementFeatures + Evidence)
→ CompletenessCalculator / VerifiabilityCalculator / UnambiguityCalculator
→ RequirementQualityAssessor → RequirementQualityProfile
→ SpecificationQualityAggregator → SpecificationQualityProfile
→ ConsoleReporter
```

The CLI wires these components and handles input errors. The reader alone performs file I/O. The selected `SpaCyRequirementParser` uses spaCy 3.8.16 and `uk_core_news_sm` 3.8.0 behind the extraction boundary; it converts parser data to typed, parser-neutral domain models. Each detector can return accepted observations and separate incomplete diagnostics. `BaselineFeatureExtractor` assembles six family outcomes and accepted Evidence without scoring. Calculators consume `RequirementExtractionResult` containing domain `RequirementFeatures` and Evidence; they do not import the extractor, parser, CLI, or file I/O. The assessor combines three assessments without calculation. The aggregator consumes profiles, and the reporter formats already computed results without scoring or aggregation.

## Feature families and traceability

The six approved families, with their baseline rule IDs, are:

| Feature family | Implemented baseline |
| --- | --- |
| Condition/context | `COND-UK-001` |
| Expected result/reaction | `RESULT-UK-001` |
| Acceptance criterion | `ACCEPT-QUANT-001` |
| Quantitative constraint | `QUANT-001`, `QUANT-UK-001` |
| Explicit verification method | `VERIFY-UK-001` |
| Ukrainian vague-term occurrence | `UK-VAGUE-001`, `uk_vague_terms_v1` |

Only the approved detector grammars and seed vocabulary are implemented. Source evidence may be shared by related observations. Detection (`DETECTED`, `NOT_DETECTED`, `UNRESOLVED`) is distinct from criterion applicability (`APPLICABLE`, `NOT_APPLICABLE`, `UNKNOWN`). No requirement type is inferred. The approved MVP Completeness rule makes its three criteria applicable to each supported input requirement; Verifiability uses alternative evidence paths instead of mandatory per-family criteria.

## Assessment and aggregation rules

| Rule | Executable behavior |
| --- | --- |
| `CALC-C-MVP-001` | Exact unweighted detected fraction over condition/context, expected result, and acceptance criterion; values `0`, `1/3`, `2/3`, `1` when all required detection is complete. |
| `CALC-V-MVP-001` | Accepted acceptance criterion → `1`; otherwise accepted quantitative constraint or verification method → `1/2`; complete absence → `0`. An unresolved candidate yields `UNKNOWN` only when it could change the class. |
| `CALC-U-MVP-001` | No supported vague signal after complete scanning → `1`; one or more accepted signals → `1/2`. Unresolved scanning with no accepted signal → `UNKNOWN`. `0` is reserved for a future confirmed-ambiguity rule. |
| `FIND-U-VAGUE-001` | Each accepted vague-term occurrence creates one Unambiguity `SIGNAL` Finding with evidence references. It is not a confirmed `QUALITY_PROBLEM`. |
| `AGG-MVP-001` | Each characteristic is aggregated independently as an exact mean of `COMPUTED` values. `UNKNOWN` and `NOT_APPLICABLE` are excluded and counted. With no computed values, any unknown yields `UNKNOWN`; otherwise the aggregate is `NOT_APPLICABLE`. |
| `RQD-015` / Section 19 | Console values use exact `Fraction` text, literal unavailable-state tokens, fixed C/V/U order, and visible aggregate observability counts. |

Computed values and explanations retain rule provenance. `UNKNOWN` and `NOT_APPLICABLE` have no numeric value; neither is silently converted to zero. The current CLI's supported individual requirements are applicable to C/V/U, while an empty file has three `NOT_APPLICABLE` specification aggregates. The `Finding` domain contract can represent more than the executable MVP creates; production calculation currently emits `SIGNAL` findings only.

## Scientific and technical limits

The executable subset does not settle broader detector grammar under `RQD-006` and `RQD-008`: complex or ambiguous attachment, non-numeric acceptance criteria, count-noun roles, nested constraints/context, written-out numbers, and generic ranges remain deferred. Broader vague-term vocabulary is outside the approved seed. Numeric detector confidence or evidence reliability (`RQD-020`) is not defined. `QUALITY_PROBLEM` conversion and a confirmed-material-ambiguity procedure (`RQD-016`, including `U_i = 0`) remain open. Neither a computed `1` nor the absence of a supported signal establishes universal semantic quality. No English linguistic profile, automatic requirement-type classifier, cross-requirement consistency, traceability, global requirements coverage, risk, or product-quality prediction is implemented.

The selected parser is an engineering backend, not a scientific authority. A missing, incompatible, or unsuccessful parser can cause required detection and downstream assessments to remain `UNKNOWN`. Reproducibility requires the pinned parser and model versions. The console presents Finding evidence references and explanations; exact evidence text and offsets are retained in `RequirementExtractionResult` for traceability. The CLI does not export that structured result to another format.

## Future v1.0 result architecture

Future SRM work must preserve two levels: **Level 1 — Scientific Assessment**, the formal approved assessments, states, rules, Findings, Evidence, and quality profiles; and **Level 2 — Human-readable Interpretation**, a separate understandable rendering of Level 1. Interpretation must not modify scientific results, invent unsupported conclusions, or turn `UNKNOWN` into a number. This is a future v1.0 requirement, not an SRM-01 implementation change.

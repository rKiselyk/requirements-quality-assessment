# MVP v0.1 acceptance evidence — SRM-01

## Release identity

[SRM-01 PR #82](https://github.com/rKiselyk/requirements-quality-assessment/pull/82) was reviewed and merged. The executable MVP v0.1 subset was verified on the merged `main` branch. The immutable annotated tag [`mvp-v0.1-baseline`](https://github.com/rKiselyk/requirements-quality-assessment/tree/mvp-v0.1-baseline), once published, identifies the accepted final commit. The tag annotation and [SRM-01 Issue #69](https://github.com/rKiselyk/requirements-quality-assessment/issues/69) record its full SHA and final verification. This document deliberately does not embed its own commit SHA, because editing that value would change it.

The pre-audit local and remote `main` HEAD were both independently verified as `f36abc8e68cbc98974e3ca925f2c71ad82554c5c` on 2026-09-20. PR #82 was squash-merged as `3a9dfa8323665149a25726c47d4b0d9c9ed21dc3`; final documentation and tag publication follow that merge. Neither the starting SHA nor the PR branch SHA is the accepted baseline identity.

## Verified environment and installation

| Check | Observed result |
| --- | --- |
| Operating system | Windows `10.0.26200` (`Windows-10-10.0.26200-SP0`) |
| Python | 3.11.9; project requirement `>=3.11` |
| Fresh isolated virtual environment | Created at a temporary path; `python -m pip install -e ".[dev,parser]"` completed successfully against the working tree. The first network-restricted attempt could not reach the package index; rerunning with network access succeeded. |
| Clean committed checkout | Local clone of branch commit `3c551837da21910bd22c3cd405cf170f03c744ca` had a clean status. A second fresh virtual environment installed that checkout with `python -m pip install -e ".[dev,parser]"`. |
| Parser packages | spaCy 3.8.16; `uk_core_news_sm` 3.8.0 |
| Model load | `spacy.load("uk_core_news_sm", disable=["ner"])` succeeded; Ukrainian pipeline contained `tok2vec`, `morphologizer`, `parser`, `attribute_ruler`, `lemmatizer`. |
| Compatibility | `python -m pip check` reported `No broken requirements found.` in the existing and fresh virtual environments. |
| Fresh-environment test suite after the CLI fix | `554 passed in 24.39s`, no skipped tests. |
| Existing-environment test suite after the CLI fix | `554 passed in 24.23s`, no skipped tests. |
| Clean-checkout test suite | `554 passed in 25.58s`, no skipped tests; pinned model loaded; `pip check` found no broken requirements. |
| Pre-merge focused real-parser and acceptance selection | `10 passed, 543 deselected in 12.12s`, no skipped tests. |
| Merged-main full suite before documentation update | `554 passed in 25.26s`, no skipped tests, on merge commit `3a9dfa8323665149a25726c47d4b0d9c9ed21dc3`. |
| Merged-main focused parser/acceptance selection | `10 passed, 544 deselected in 12.14s`, no skipped tests. |
| Merged-main model and CLI | Pinned Ukrainian model loaded; `pip check` found no broken requirements. Two production CLI runs exited 0 and produced byte-identical UTF-8 output for two Ukrainian requirements, including a `SIGNAL` and specification summary. |

The clean-checkout installation verified the committed implementation and tests. Verification after the final documentation commit is required before the baseline tag is created; the tag annotation and Issue #69 provide that final result.

## Implementation and architecture audit

The following components were inspected in source and exercised by the suite: `RequirementReader`; typed domain models; `SpaCyRequirementParser`; condition/context, expected-result, acceptance-criterion, quantitative, verification-method, and vague-term detectors; `BaselineFeatureExtractor`; `CompletenessCalculator`, `VerifiabilityCalculator`, and `UnambiguityCalculator`; `RequirementQualityAssessor`; `RequirementQualityProfile`; `SpecificationQualityAggregator`; `SpecificationQualityProfile`; `ConsoleReporter`; and the CLI. The pipeline follows the boundary sequence documented in [`mvp-v0.1-baseline.md`](mvp-v0.1-baseline.md). The CLI performs orchestration and input-error handling; the reporter formats completed assessments and aggregates. Neither contains a scientific formula. Calculators depend on domain extraction results, not on the extractor or spaCy, and are tested with manually constructed features and evidence.

The approved executable rules are `CALC-C-MVP-001`, `CALC-V-MVP-001`, `CALC-U-MVP-001`, `FIND-U-VAGUE-001`, `AGG-MVP-001`, and the exact-fraction presentation contract in Section 19 / `RQD-015` of [`model-spec.md`](model-spec.md). Detector rules and vocabularies were not changed by SRM-01.

## End-to-end acceptance observations

`tests/test_mvp_acceptance.py` uses the installed, pinned parser and a five-requirement UTF-8 file. It verifies trimming, blank-line handling, IDs `R001`–`R005`, original source lines `1, 3, 4, 5, 6`, all six feature-family types, exact evidence text and offsets, rule-derived values, Finding provenance, specification aggregation, stable report order, and byte-identical repeated CLI output. The approved positive case produced `(C,V,U)=(1,1,1)`. The vague-term case produced `(1/3,0,1/2)` and one `SIGNAL` tied to exact `швидко` evidence at offsets `[16,22)`, without `QUALITY_PROBLEM` conversion. The quantitative case produced `(2/3,1,1)`. The `до 2 с` acceptance candidate remained `UNRESOLVED`, propagating to `UNKNOWN` C and V with no numeric value. An explicit verification-method case produced V=`1/2`. The five-case aggregates were exact `C=2/3`, `V=5/8`, `U=9/10`, with computed/unknown counts `3/2`, `4/1`, and `5/0` respectively. These expected values follow only the approved rules and the observed detector outcomes.

An empty file yielded zero requirements and three `NOT_APPLICABLE` aggregates with zero counts. Existing CLI tests verify missing-file and invalid-UTF-8 errors with nonzero exit codes, multiple requirements, blank lines, Ukrainian text, and absence of scalar scores. Domain and aggregation tests verify `NOT_APPLICABLE` separately from `UNKNOWN`, exact `Fraction` arithmetic, and no zero substitution. The full suite covers detector boundary cases and manually constructed calculator inputs. Two pre-existing import-boundary tests initially failed in a full run because earlier tests had legitimately imported spaCy into the shared pytest process; SRM-01 moved those checks into isolated Python processes. They now verify the intended import property without relying on test order.

A direct Windows module invocation initially failed with `UnicodeEncodeError` when redirected stdout used `cp1252`. SRM-01 configures UTF-8 for the module entry point's stdout and stderr before orchestration. A subprocess test forces `PYTHONIOENCODING=cp1252` and verifies successful Ukrainian output; a separate direct command was rerun and returned exit code 0 with the original Ukrainian text and `SIGNAL` intact. No detector, score, or domain rule changed.

## GitHub issue reconciliation audit

GitHub issue bodies, their states at the pre-freeze audit, the merged PR history visible in Git, and the current model specification were reviewed. A merged sub-issue PR establishes the approved narrow implementation, not completion of an open research gate. Completion summaries were posted before closing #7–#12; #5 and #6 received scope comments and remain open. Issue #69 tracks the final freeze. The table records pre-freeze dispositions; later closure of #13 and #69 is recorded in GitHub.

| Issue | Observed state and merged PR evidence | Disposition and justification |
| --- | --- | --- |
| [#1](https://github.com/rKiselyk/requirements-quality-assessment/issues/1) MVP-00 | Closed; PR #15 | Initialization and guardrails are present. Keep closed. |
| [#2](https://github.com/rKiselyk/requirements-quality-assessment/issues/2) MVP-01 | Closed; PRs #19, #20 and later profile contracts | Approved typed domain subset exists and is tested. Keep closed; broader science is handled by separate decisions. |
| [#3](https://github.com/rKiselyk/requirements-quality-assessment/issues/3) MVP-02 | Closed; PR #21 | UTF-8 reader contract and error paths are tested. Keep closed. |
| [#4](https://github.com/rKiselyk/requirements-quality-assessment/issues/4) MVP-03 | Closed; PRs #22, #26 | Replaceable extraction/evidence boundary exists. Current `RequirementExtractionResult` contract supersedes old direct-return wording. Keep closed. |
| [#5](https://github.com/rKiselyk/requirements-quality-assessment/issues/5) MVP-04 | Open; parser/extraction and structural detector PRs #24, #26, #34, #38, #42, #46, #52 | Narrow approved structural baselines are implemented. A scope comment records that `RQD-006`/`RQD-008` grammar blockers remain; the issue stays open for broader research. |
| [#6](https://github.com/rKiselyk/requirements-quality-assessment/issues/6) MVP-05 | Open; vague and quantitative/verification detector PRs #28, #34, #50, #52 | Ukrainian seed matcher and approved textual baselines are implemented. A scope comment records that broader `RQD-006`/`RQD-008` grammar remains open. |
| [#7](https://github.com/rKiselyk/requirements-quality-assessment/issues/7) MVP-06 | Closed; rule PRs #54, #55 and calculator PR #56 | Approved `CALC-C-MVP-001` and tests are implemented. The completion summary clarifies the domain `RequirementExtractionResult` input with manually constructible features and Evidence. |
| [#8](https://github.com/rKiselyk/requirements-quality-assessment/issues/8) MVP-07 | Closed; rule PRs #54, #55 and calculator PR #57 | Approved `CALC-V-MVP-001`, `UNKNOWN` propagation, and independent tests are implemented; the completion summary clarifies the domain input. |
| [#9](https://github.com/rKiselyk/requirements-quality-assessment/issues/9) MVP-08 | Closed; rule PRs #54, #55 and calculator PR #58 | Automated `CALC-U-MVP-001` and vague `SIGNAL` mapping are implemented. The closing summary supersedes an old blocked paragraph for the accepted `1/2`/`1` subset and leaves confirmed-ambiguity `0` and `QUALITY_PROBLEM` rules open for future research. |
| [#10](https://github.com/rKiselyk/requirements-quality-assessment/issues/10) MVP-09 | Closed; profile/assessor/aggregation PRs #59, #60, #62, #63 | Separate profiles, `AGG-MVP-001`, exact means, observability counts, and tests satisfy the MVP scope. |
| [#11](https://github.com/rKiselyk/requirements-quality-assessment/issues/11) MVP-10 | Closed; presentation and reporter PRs #65, #66 | Reporter implements the approved Section 19 surface, including `SIGNAL`, rule IDs, evidence references, and explanations. The completion summary distinguishes that surface from unsupported confirmed problems or full evidence-text rendering. |
| [#12](https://github.com/rKiselyk/requirements-quality-assessment/issues/12) MVP-11 | Closed; CLI PR #67 | Full profile-based CLI pipeline, input errors, and integration tests satisfy the MVP scope. |
| [#13](https://github.com/rKiselyk/requirements-quality-assessment/issues/13) MVP-12 | Open at pre-freeze audit; SRM-01 PR #82 supplies acceptance and README work | Its acceptance text now requires supported `Finding`/`SIGNAL` evidence references without requiring automatic `QUALITY_PROBLEM` generation. Close only after final-main verification and baseline tagging. |
| [#14](https://github.com/rKiselyk/requirements-quality-assessment/issues/14) MVP-SPEC | Open; scientific-contract PRs #16–#19, #30, #33, #36, #41, #44, #48, #53–#55, #62, #65 | Its body now acknowledges approved C/V/U, `AGG-MVP-001`, exact `Fraction`, and presentation rules, while preserving the broader draft and `RQD-006`, `RQD-008`, `RQD-016`, `RQD-020` decisions as open. |

At the pre-freeze audit, the [Full Single Requirement Model v1.0 milestone](https://github.com/rKiselyk/requirements-quality-assessment/milestone/1) was open with 14 open issues, including SRM-00, SRM-01, and SRM-02–SRM-13. It is not the MVP v0.1 freeze record. SRM-00 and SRM-02–SRM-13 are outside SRM-01 closure scope.

## Remaining limitations and acceptance work

Scientific limits are recorded in [`mvp-v0.1-baseline.md`](mvp-v0.1-baseline.md). Technical limits include dependence on the selected parser/model for complete detection and console-only output of evidence references rather than a structured export. The broader research issues #5, #6, and #14 stay open after the executable MVP freeze. The final tag and Issue #69, rather than this document's mutable text, establish whether all freeze steps completed.

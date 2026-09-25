# SRM-13 bounded two-stage execution results

## Scope and evaluated implementation

This is an executed, bounded verification and practical demonstration of the
existing single-requirement C/V/U application. It is not the planned
independent SRM-13 validation and does not supersede the existing G1-G13
preparation records.

- Evaluated implementation commit: `0bfa03e04be187bc56fdd30dff393eb813b482aa`.
- Execution environment: Python 3.11.9, spaCy 3.8.16, `uk_core_news_sm` 3.8.0,
  Windows 10 build 26200.
- Executed cases: 40 authored requirements and 23 naturally occurring
  requirements.
- Production implementation changes made for this study: none.
- Evaluation wrapper: `scripts/run_srm13_two_stage.py`. It invokes
  `BaselineFeatureExtractor`, `RequirementQualityAssessor`, the specification
  aggregator, and the existing user/audit reporters; it does not reimplement
  the detectors or calculators.

## Stage 1: authored verification cases

The authored JSONL records a stable ID, exact text, purpose, model-spec basis,
relevant expected feature state, Evidence text, diagnostics, C/V/U state and
value, Trace decision, Findings, and stated limitations. Actual full domain
records and the explicit comparison are retained per case.

### Final comparison

| Comparison | PASS | FAIL | NOT_ASSESSABLE |
|---|---:|---:|---:|
| Case overall | 40 | 0 | 0 |
| C state/value/Trace | 40 | 0 | 0 |
| V state/value/Trace | 40 | 0 | 0 |
| U state/value/Trace | 40 | 0 | 0 |
| Evidence/features | 40 | 0 | - |
| Findings | 40 | 0 | - |

This is a conformity result for these 40 designed cases only. It is not an
accuracy estimate and the percentage must not be generalized to natural
requirements.

### Preserved first run and expectation adjudication

The first execution produced 27 PASS and 13 FAIL cases (C: 31/40, V: 39/40,
U: 40/40). The unmodified first-run comparisons and aggregate summary remain
in `authored-initial-results.jsonl` and `initial-summary.json`. That historical
summary also records the 24-line preliminary real set before the ineligible
continuation fragment was excluded; `summary.json` is the final 23-line result.

All 13 discrepancies were expectation mistakes, not silently removed cases:

- A010 incorrectly treated a postposed-condition prefix as accepted result
  Evidence despite the binding P01 production contract.
- A012 used a nonexistent shortened diagnostic code.
- A013 stopped at the RESULT-UK-002 disjunction boundary and omitted the
  required RESULT-UK-001 unresolved fall-through.
- A017, A020, A025, A027, A028, and A029 incorrectly treated finite nonmodal or
  passive result candidates as completed absence rather than `UNRESOLVED`.
- A030 ignored unresolved coordination scope between qualitative modifiers.
- A031 generalized lexical casefolding to parser morphology; the pinned parser
  cannot establish the all-uppercase infinitive graph.
- A033 ignored RESULT-UK-002's parser-visible negation exclusion for the
  comparator `не більше`; the quantitative observations remain detected, but
  result and acceptance are unresolved.
- A038 omitted the unresolved second result segment from an otherwise mixed
  detected/incomplete family.

Each corrected case has an `expectation_revision` explaining the governing
rule. The corrections were made from the frozen model's production contracts,
not by declaring the observed output to be ground truth. No scientific rule,
formula, implementation behavior, or case text was changed.

## Stage 2: practical demonstration on real requirements

### Sources and lawful representation

The 23 lines come from three pinned documents in two public repositories in
the OpenProcurement ecosystem:

1. OpenProcurement, [Вимоги до Публічного порталу доступу до бази даних державних закупівель](https://github.com/openprocurement/openprocurement.github.io/blob/b6fa56b287fe126460eb7dc1f780088c5ff399bb/_posts/ua/2015-07-16-public-procurement-portal.markdown),
   commit `b6fa56b287fe126460eb7dc1f780088c5ff399bb`, file SHA-256
   `17c54b6404de87513a211b1b5d71d35ff1f56387b82745c30b196c2692f68c2f`.
2. Prozorro, [`requestForProposal` requirements](https://github.com/ProzorroUKR/openprocurement.api/blob/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c/docs/source/features/request_for_proposal.rst),
   commit `3fec5a97c31913aefc3f05e0ad6b929fd8148b4c`, file SHA-256
   `45ba9e25bd55b44f80201436ff1985feb47a8c7e06bdaec979db98d162679c81`.
3. Prozorro, [framework-period modification requirements](https://github.com/ProzorroUKR/openprocurement.api/blob/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c/docs/source/features/modify_framework_period.rst),
   the same pinned commit, file SHA-256
   `f0f14928644913b3526146895ca8fee456175eea5ea4037053f02e4c1f993222`.

The repositories declare Apache-2.0. The dataset retains attribution, commit,
path, original line number, retrieval date (2026-09-25 Europe/Kiev), hash, and
representation note for every case. Only selected single lines are quoted.
Markdown/RST list markers and inline emphasis delimiters were omitted; visible
text otherwise remains one physical source line with no joining, paraphrasing,
or reconstruction. One initially considered line was excluded because it began
with a continuation fragment. Public accessibility was not treated as a
licence by itself.

### Observed distributions

| Characteristic | Observed states/values |
|---|---|
| C | `0`: 14; `2/3`: 1; `UNKNOWN`: 8 |
| V | `0`: 23 |
| U | `1`: 23 |
| Diagnostics | 8 cases had at least one diagnostic |
| SIGNAL Findings | 0 |

These are application outputs, not expert reference labels. In particular,
U=1 means only that the approved seed detector found no supported vague-term
signal after complete processing. It is not proof of semantic unambiguity.

### Per-case results

Source references below resolve through the three pinned document links above.
`Detected` lists only accepted feature families; `Diagnostics` lists unresolved
feature behavior. The last column is researcher interpretation, not system
output and not a correctness label. Exact requirement text and full provenance
are in `real-requirements.jsonl`.

| ID | Source line | C | V | U | Detected | Findings | Diagnostics | Researcher interpretation |
|---|---|---:|---:|---:|---|---|---|---|
| N001 | Portal L34 | 0 | 0 | 1 | - | - | - | Imperative-style directive is outside the normative-modal result grammar. |
| N002 | Portal L35 | 0 | 0 | 1 | - | - | - | Qualitative formulation is outside the frozen vague-term seed lexicon. |
| N003 | Portal L36 | 0 | 0 | 1 | - | - | - | Infinitive list item lacks the explicit actor/modal required by RESULT-UK-001. |
| N005 | Portal L52 | UNKNOWN | 0 | 1 | - | - | `RESULT_COORD_UNRESOLVED_CANDIDATE` | Complex coordination exceeds RESULT-UK-002. |
| N006 | Portal L55 | UNKNOWN | 0 | 1 | - | - | `RESULT_UNRESOLVED_CANDIDATE` | Passive normative construction is outside the narrow result grammar. |
| N007 | Portal L56 | UNKNOWN | 0 | 1 | - | - | `RESULT_COORD_UNRESOLVED_CANDIDATE` | Multi-part coordinated result is unresolved. |
| N008 | Portal L57 | UNKNOWN | 0 | 1 | - | - | `RESULT_COORD_UNRESOLVED_CANDIDATE` | Compound integration statement is unresolved by the bounded grammar. |
| N009 | Portal L58 | UNKNOWN | 0 | 1 | - | - | two `RESULT_UNRESOLVED_CANDIDATE` | Multiple clauses/sentences produce unresolved result candidates. |
| N010 | Portal L59 | UNKNOWN | 0 | 1 | - | - | `RESULT_COORD_UNRESOLVED_CANDIDATE` | Modal-capability coordination is outside the supported graph. |
| N011 | Portal L64 | 2/3 | 0 | 1 | condition, result | - | - | The result and load context are accepted; no acceptance criterion is detected. |
| N012 | Portal L65 | UNKNOWN | 0 | 1 | - | - | `RESULT_UNRESOLVED_CANDIDATE` | Passive modal plus explanatory clause is unresolved. |
| N013 | RFP L16 | 0 | 0 | 1 | - | - | - | Imperative infinitive is not a supported normative-modal result. |
| N014 | RFP L18 | 0 | 0 | 1 | - | - | - | Analogy to another module is semantically outside the bounded features. |
| N015 | RFP L19 | 0 | 0 | 1 | - | - | - | Directive with a URL has no supported modal subject. |
| N016 | RFP L20 | 0 | 0 | 1 | - | - | - | Short implementation directive is outside RESULT-UK-001. |
| N017 | RFP L27 | 0 | 0 | 1 | - | - | - | Imperative result limitation. |
| N018 | RFP L29 | UNKNOWN | 0 | 1 | - | - | `RESULT_COORD_UNRESOLVED_CANDIDATE` | Complex passive/negative coordination is unresolved. |
| N019 | RFP L30 | 0 | 0 | 1 | - | - | - | Imperative result limitation. |
| N020 | RFP L32 | 0 | 0 | 1 | - | - | - | Short implementation directive is outside RESULT-UK-001. |
| N021 | RFP L42 | 0 | 0 | 1 | - | - | - | Qualitative analogy and exception are not represented by bounded features. |
| N022 | RFP L45 | 0 | 0 | 1 | - | - | - | Short implementation directive is outside RESULT-UK-001. |
| N023 | Period L8 | 0 | 0 | 1 | - | - | - | A real day-valued bound is outside the supported seconds/minutes/percent grammar. |
| N024 | Period L10 | 0 | 0 | 1 | - | - | - | A second day-valued bound confirms the same coverage limitation. |

### Representative observations

- Straightforward supported behavior: N011 accepted exact condition and result
  Evidence and produced C=2/3, V=0, U=1. The output is explainable, but the
  qualitative word `стабільну` is not in the approved vague seed and therefore
  produces no U Finding.
- Quantitative criterion: N023 visibly contains `365 днів`, yet no quantitative
  observation is accepted because days and the nominal dash construction are
  outside the frozen rule. The resulting V=0 is an observed coverage limitation,
  not evidence that the source criterion is unverifiable.
- Qualitative/ambiguous formulation: N002 says `високий рівень якості`, but the
  bounded seed detector emits no SIGNAL and U=1. This is a concrete reminder
  that U=1 is supported-signal absence only.
- Missing supported structure: N013 is a genuine implementation directive, but
  its imperative infinitive has no explicit modal subject, so every C family is
  completed absence and C=0.
- Complex limitation: N005 contains nested and coordinated behavior. The system
  preserves a result diagnostic and returns C=`UNKNOWN` instead of repairing or
  guessing the scope.

## Conclusions and non-claims

The execution supports the claim that the frozen implementation conforms to
the explicitly recorded expectations on these 40 authored cases after visible,
model-based correction of the first-run expectation errors. It also demonstrates
that the application can preserve Evidence, diagnostics, Trace, Findings, and
defined states across 23 real source lines.

The real demonstration exposes substantial coverage limits: imperative
specification style is usually scored as completed result absence; complex,
passive, and coordinated formulations frequently make C unknown; the real
day-valued bounds are outside quantitative coverage; and the limited vague-term
seed misses conspicuous qualitative wording. No real case produced V above 0
or a U SIGNAL.

This study does **not** establish Precision, Recall, F1, accuracy,
representativeness of Ukrainian software requirements, source independence for
a holdout corpus, or validation of additional dissertation characteristics. It
does not approve either repository for an independent corpus, pass G7, close
G1/G2/G3/G7/G13, or close issues #81/#68. Source diversity is narrow: all real
documents are from the OpenProcurement ecosystem.

## Reproduction and artifacts

From the repository root with the pinned project environment installed:

```powershell
.venv\Scripts\python.exe scripts\run_srm13_two_stage.py
```

Focused checks used for the existing public interface and reporters:

```powershell
.venv\Scripts\python.exe -m pytest -q tests/test_mvp_acceptance.py tests/test_cli.py
git diff --check
```

Artifacts are under `docs/srm-13-two-stage-results/`:

- `authored-requirements.jsonl`: authored texts and final explicit expectations.
- `authored-results.jsonl`: final expected-versus-actual comparisons plus full
  executed domain records.
- `authored-initial-results.jsonl`: preserved first-run failures before
  expectation adjudication.
- `real-requirements.jsonl`: exact selected source lines and full provenance.
- `real-results.jsonl`: actual structured outputs and interpretation focus.
- `authored-user-report.txt`, `authored-audit-report.txt`,
  `real-user-report.txt`, and `real-audit-report.txt`: existing reporter views.
- `authored-input.txt` and `real-input.txt`: exact executed one-line inputs.
- `summary.json` and `initial-summary.json`: final and first-run aggregates.

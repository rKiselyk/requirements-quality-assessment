# Full Model v1.0 research acceptance

Status: `ACCEPTED`

Acceptance marker: `TC06_INTEGRATED_RESEARCH_ACCEPTANCE_ACCEPTED`

Scenario: `CONTROLLED_RESEARCH_REFERENCE_SCENARIO`

Issue: #168

Pull request: #169

Starting integration HEAD: `fcf880d8fcd3f3a6beed6b06f7f38a33637e5828`

Initial TC-06 candidate commit: `0ffb8667c3fcc4f501afe928584ec5cc36d725d4`

Accepted integration HEAD: `2971758f435be44d92d1d99dd68c45c0a56ca4ff`

Merged main SHA: `994cd473cdb80d71d322ffc8883d9de5d41fc7bc`

Independent final acceptance is recorded on closed issue #168. Within the
declared bounded reference scope, TC-06 accepts Full Model v1.0 as an
executable, deterministic, and traceable research realization. This acceptance
does not claim exhaustive NLP coverage, universal product-quality prediction,
universal risk calibration, causal effectiveness, universal release decisions,
or production readiness.

## Bounded scope and public invocation

The canonical fixture lives in `tests/reference_acceptance_data.py`; no
scientific fixture value is added to production. The dedicated acceptance test
calls `FullModelService.run(...)` exactly once with that explicit request. It
does not import or reconstruct the historical M3 `_build_scenario()` pipeline.

The service-driven report bundle uses presentation identity `v1.0`.
Historical `FullModelReportBundle` output and historical versioned component
contracts, including `FULL-MODEL-V0.1-CONTRACT` and
`FULL-MODEL-V0.1-DYNAMIC-EVIDENCE`, remain unchanged.

## Explicit controlled fixture inputs

- Requirements: R001 `Час відгуку ≤ 2 с при 500 одночасних користувачах`;
  R002 `Час відгуку не нижче 5 с при 500 одночасних користувачах`.
- Dynamic evidence: selected R001 quantitative constraint; explicit `1.8 s`
  observation; deterministic fixture collection; explicit product,
  environment, metric, unit, and normalized criterion context.
- External requirement properties: all six non-C/V/U properties for both R001
  and R002 are `AVAILABLE` opaque judgments from
  `TC06-CONTROLLED-EXPERT / 1`, governed by
  `TC06-EXTERNAL-PROPERTIES / 1` and property-specific version-1 rules.
- Prediction: fixture-only `TC06-CONTROLLED-REFERENCE-PE / 1`; theta
  `TC06-CONTROLLED-THETA / 1`; parameter `requirement_weight=1/4`;
  `PROVISIONAL_NOT_CALIBRATED`; required features are requirement completeness
  and response-time conformance; required context is product, environment, and
  response-time criterion context.
- Quantitative risk operands: `rho=1/2`, `p=1/4`, `I=3/4`,
  `kappa(C)=2/3`; every operand is `AVAILABLE`, versioned, externally sourced
  from `TC06-CONTROLLED-PROVIDER / 1`, and provisional/not calibrated.
- Checkpoint: selected `SPEC.QB_CONSISTENCY`; comparator `>=`; threshold
  `Fraction(1,1)`; the same `TC06-QB-CHECKPOINT-POLICY / 1` is supplied for v1
  and v2.
- Revision: R002 is externally replaced by
  `Час відгуку ≤ 5 с при 500 одночасних користувачах`; provider kind is
  `CONTROLLED_REFERENCE_FIXTURE`; no rewrite is inferred or generated.
- Evidence reuse: all required identities/context values and the
  `REUSE_ALLOWED` decision are explicit.

## #168 coverage

| # | Coverage item | Expected | Actual canonical evidence |
|---:|---|---|---|
| 1 | Requirement ingestion | two ordered requirements | R001/R002 text, IDs, line identities preserved |
| 2 | Automatic C/V/U | automatic typed assessments | each requirement: C=`1/3`, V=`1/2`, U=`1` |
| 3 | Full nine-property profile | nine independent slots per requirement | two profiles; 3 automatic plus 6 external/expert each; no integrated score |
| 4 | Specification metrics + QB | v1 metric profile and conflict QB | confirmed conflict; exact v1 `QB=0/1` |
| 5 | Dynamic criterion | bound quantitative criterion | R001 response-time bound is `AVAILABLE` |
| 6 | Dynamic observation | explicit observation record | exact `1.8 s`, deterministic fixture source |
| 7 | Conformance | typed outcome | `CONFORMS` |
| 8 | `X_PE` | typed feature profile | profile and feature-level states/provenance retained; aggregate profile is `UNRESOLVED`, not zero-filled |
| 9 | Observed product-quality evidence | distinct observed record | v1 `ProductQualityAssessment`, `OBSERVED_REFERENCE_INDICATOR`, `UNRESOLVED`, value absent |
| 10 | Predicted product quality | deterministic typed prediction | `PredictedPerformanceEfficiency`, exact `5/6` |
| 11 | Confirmed problem | supported v1 problem | `CONFIRMED_SUPPORTED_PROBLEM` |
| 12 | `R_DQ` | structural relation | Performance Efficiency relation; `NOT_NUMERIC_RHO` retained |
| 13 | Categorical risk | separate classification | v1 `RISK_IDENTIFIED` |
| 14 | Quantitative `r_ij` | exact externally parameterized calculation | `1/2 × 1/4 × 3/4 × 2/3 = 1/16` |
| 15 | Corrective action | typed proposal | `RECONCILE_QUANTITATIVE_BOUNDS` |
| 16 | External revision | explicit non-generated child artifact | controlled provider changes only R002 in S(v2) |
| 17 | v2 reassessment | accepted reevaluation path | v2 metric/downstream records rebuilt with explicit evidence reuse |
| 18 | Before/after comparisons | literal comparisons only | `INCREASED`, then three `STATE_CHANGED`; no improvement interpretation |
| 19 | Checkpoint evaluation | same explicit policy on both versions | v1 `NOT_SATISFIED`; v2 `SATISFIED`; neither means proceed/release |
| 20 | Process states + transition | linked typed records | v1 predecessor, v2 successor, and `PROCESS-TRANSITION-TC06` agree |
| 21 | USER report | visible semantic separation | v1.0 identity and separate requirement, observed, predicted, risk, checkpoint, reassessment/comparison/process sections |
| 22 | AUDIT report | complete typed trace | v1.0 identity and exact full-profile, prediction, risk, checkpoint, comparison, and transition records |

## Exact requirement-quality evidence

For both R001 and R002, automatic C/V/U remains the original automatic record:

| Requirement | Completeness | Verifiability | Unambiguity |
|---|---:|---:|---:|
| R001 | `COMPUTED 1/3` | `COMPUTED 1/2` | `COMPUTED 1` |
| R002 | `COMPUTED 1/3` | `COMPUTED 1/2` | `COMPUTED 1` |

Each requirement also has explicit external/expert `AVAILABLE` judgments for
Singularity, Presentation Conformance, Correctness, Feasibility, Necessity, and
Relevance. Judgment IDs use
`TC06-{requirement}-{property}-EXPERT-JUDGMENT`; provenance retains source
`TC06-CONTROLLED-EXPERT / 1`, artifact `SPEC-TC06-REFERENCE / v1`, the exact
requirement reference, assessment contract, and versioned property rule. No
external property is inferred from text and no scalar requirement-quality
field exists.

## Prediction and observed-quality distinction

The fixture evaluator computes:

`(1/4 × requirement completeness 1/3) + (3/4 × conforms 1) = 5/6`.

The exact result is `PREDICTED_PERFORMANCE_EFFICIENCY`, with predictor, theta,
selected feature/context inputs, and provisional calibration provenance. It is
a different type and record from the observed
`OBSERVED_REFERENCE_INDICATOR`. The v1 observed record is `UNRESOLVED` with no
value; the reassessed v2 observed record is `AVAILABLE` with exact value `1`.
No confidence, uncertainty, accuracy, universal validity, or full
nine-characteristic product prediction is claimed.

## Categorical and quantitative risk

The structural `R_DQ` contains no numeric rho field. The categorical record is
`RISK_IDENTIFIED`; the separate quantitative record contains the explicit
normalized rho, probability, impact, and context-factor operands and exact
`r_ij=1/16`. All operand source/provider versions and provisional calibration
states are retained. No aggregate `Risk_j`, `Ψ_j`, ranking, or priority exists.

After reassessment, the supported target problem disappears within the bounded
rule and categorical risk is `NOT_APPLICABLE`; this is not interpreted as
proved correction success or risk reduction.

## Checkpoint, reassessment, comparison, and process lineage

The same externally supplied QB policy produces:

| Version | Selected value | Predicate | Outcome |
|---|---:|---:|---|
| v1 | `0/1` | `>= 1/1` | `NOT_SATISFIED` |
| v2 | `1/1` | `>= 1/1` | `SATISFIED` |

`SATISFIED != PROCEED` and `SATISFIED != RELEASE`.

S(v1), assessment/metric identities, dynamic evidence, problem/relation/risk,
action, externally supplied revision, S(v2), reassessment, comparisons, and
the v1→v2 process transition retain exact artifact, process, requirement, and
component lineage. Requirement lineage IDs are unchanged across the revision.
The action application and later state changes do not establish causality.

## Missing-state and zero-fill evidence

The v1 observed product-quality result is `UNRESOLVED` with `value=None`; the
v2 bounded risk is `NOT_APPLICABLE` with `classification=None`. Both remain
distinct from the real exact v1 QB value `Fraction(0,1)`. No missing or
not-applicable state is converted to numeric zero.

## Deterministic report evidence

- Full Model v1.0 USER SHA-256:
  `32f1be06e5dffb85745ae222d0cd1f4bb7e1ceb3ab754fcbf92bb84df38e8789`
- Full Model v1.0 AUDIT SHA-256:
  `c8f2ed47719207fdbff1f6cfa6b2242b0f3b86692dcbcea72ec711c807b14923`
- Historical v0.1 USER SHA-256 preserved:
  `27bc841fa93e9b297419ef9af5251399100ac0f8104f870c609335d1007d9314`
- Historical v0.1 AUDIT SHA-256 preserved:
  `daa7fe519ca2b1f3fcf9119f50a6b5676938c8932f36c2d19e64559fa51dc608`

Both v1.0 views visibly separate requirement quality, observed quality,
predicted quality, categorical risk, quantitative risk, checkpoint outcome,
and reassessment/comparison/process lineage. Reporters only format completed
records. They claim no automatic improvement, successful correction, causal
effect, proved risk reduction, release approval, or proceed authorization.

## Verification record

Run on 2026-10-04 (Europe/Kiev) from the integration branch:

- Focused TC-06:
  `.venv\Scripts\python.exe -m pytest -q --disable-warnings tests\test_full_model_v1_research_acceptance.py`
  → `1 passed in 2.48s`.
- TC-01 through TC-05, process/reassessment, reporters, historical M3:
  selected requested test files → `129 passed in 129.23s`.
- Complete suite:
  `.venv\Scripts\python.exe -m pytest -q --disable-warnings`
  → `1485 passed in 403.65s`.
- `git diff --check` → passed (line-ending conversion warnings only; no
  whitespace errors).

## Non-claims and remaining boundaries

Full Model v1.0 is an executable, deterministic, traceable research
realization within this controlled reference scope. It is not exhaustive NLP
coverage, exhaustive nine-characteristic product prediction, universal
prediction, universal risk calibration, production readiness, aggregate
`Q_int`, aggregate `Risk_j / Ψ_j`, priority `Π_i`, full `K_k`, full
`Decision_j(K_k)`, a release rule, causal inference, or automatic rewriting.

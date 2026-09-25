# Cross-Requirement Consistency QB-v0.1 Implementation Plan

- Planning date: 2026-09-25
- Planning baseline: `main` at `d0acc8ced9f601673c89f859834741658f3ec85e`
- Approved research branch tip: `bc2a023cb265b309a5e3c96b9538b3c25b490eb0`
- Scope: implementation planning only
- Production code changed by this plan: none
- Tests changed by this plan: none

This plan translates the approved QB-v0.1 scientific and architecture contracts
into small implementation issues and pull requests. It does not reopen their
decisions. The authority order is the one frozen in the architecture contract:

1. `docs/model-spec.md`;
2. `docs/cross-requirement-consistency-architecture.md`;
3. `docs/cross-requirement-consistency-decision-package.md`;
4. `docs/cross-requirement-consistency-reference-cases.md`;
5. `docs/cross-requirement-qb-extraction-readiness.md`;
6. `docs/cross-requirement-analysis-research.md`;
7. accepted production contracts and the current pipeline; and
8. existing tests.

## 1. Current repository and base readiness

### 1.1 Verified local and remote state

The following state was verified on 2026-09-25. Remote facts were checked
through GitHub's public read-only API because the local GitHub CLI credential
is invalid.

| Check | Verified result | Planning consequence |
| --- | --- | --- |
| Current local branch | `feat/cross-requirement-consistency-qb-v0.1` | The proposed branch already existed before this planning document was written. It was not created, changed, pushed, or deleted in this round. |
| Working tree | Clean before this document; no production or test diff | Planning is not contaminated by implementation work. |
| Local branch base | `HEAD`, local `main`, and local `origin/main` all resolved to `d0acc8c` before this document | The pre-existing branch currently has zero implementation commits and zero diff from the merged base. |
| Local branch creation record | Created from `HEAD` at 2026-09-25 22:30:04 +0300 | Treat it as pre-existing repository state, not an action authorized by this planning round. |
| Upstream | None | The implementation branch has not been published from this checkout. |
| Remote implementation branch | GitHub returned `404` for `feat/cross-requirement-consistency-qb-v0.1` | Do not push it during planning. |
| Current remote `main` | `d0acc8ced9f601673c89f859834741658f3ec85e` | This is the implementation base as of the verification time. Re-verify immediately before IMP-01 starts. |
| Research branch | Local and remote `research/cross-requirement-analysis` at `bc2a023` | The approved package is committed and pushed. |
| Research pull request | PR #113, `cross-requirement-analysis`, merged to `main` at 2026-09-25 19:29:42 UTC | The prerequisite merge has happened; implementation planning and subsequent issue creation are not blocked by an unmerged research package. |
| Approved documents on `main` | All six authoritative inputs are reachable from merge commit `d0acc8c` | Future implementation must start from this merged history or a later verified `main`. |
| Open milestones | Only `Full Single Requirement Model v1.0` (10 open, 4 closed issues) | Create a separate implementation-only QB milestone; do not add QB implementation to the Single Requirement milestone. |
| Open Single Requirement issues | #68, #70-#78 are open in `Full Single Requirement Model v1.0`; legacy MVP issues #5, #6, and #14 are open without a milestone | QB work must not absorb or silently implement these open research/generalization scopes. |
| Open Cross Requirement issues | None | IMP-01 through IMP-11 may be created without duplicating existing Cross Requirement issues. |
| Labels | Repository has only standard labels; current open project issues are unlabeled | Use existing `enhancement` only if desired. Do not invent a QB label taxonomy as part of this milestone. |

PR #113 is the authoritative merge evidence. The remote research branch remains
available as traceability history, but implementation must not branch from it:
its approved content is already in `main`.

### 1.2 Base-readiness conclusion

The approved research/architecture package is merged, so the former
"branching must wait" condition is satisfied. The pre-existing local feature
branch happens to be based exactly on the merged `main`, but it must remain
unpublished and implementation-free until the milestone and issues are
approved/created.

At implementation kickoff:

1. fetch and verify the current remote `main` again;
2. verify that PR #113 remains an ancestor of that `main`;
3. verify that the local feature branch is still clean and contains no commit
   absent from `main`;
4. reuse the existing branch only if those checks pass; otherwise stop and
   resolve the base explicitly rather than silently rebasing or recreating it;
5. do not branch from `research/cross-requirement-analysis`; and
6. publish the feature branch only as part of the first authorized
   implementation PR workflow.

### 1.3 Current code and test boundary

The current production pipeline is:

```text
RequirementReader
-> BaselineFeatureExtractor
-> RequirementExtractionResult
-> RequirementQualityAssessor
-> RequirementAssessmentRecord
-> SpecificationQualityAggregator
-> SpecificationQualityProfile
-> ConsoleReporter or UserConsoleReporter
```

The relevant current implementation locations are:

- `domain/core.py`, `domain/detection.py`, `domain/extraction.py`,
  `domain/quantitative.py`, and `domain/trace.py` for frozen local values;
- `detectors/quantitative.py` and `extractor.py` for the quantitative
  extraction boundary;
- `assessor.py` and the three calculator modules for frozen C/V/U;
- `aggregator.py` and `domain/specification_profile.py` for `AGG-MVP-001`;
- `reporter.py` for both existing presentation views; and
- `cli.py` for orchestration.

Tests currently use a flat `tests/test_*.py` structure organized by domain
contract, detector, calculator, aggregation, reporter, and end-to-end/CLI
layer. New cross-analysis tests should follow that convention with narrowly
named files rather than creating a second test framework.

A green baseline suite could not be established in this planning environment:
`pytest` was not on `PATH`, and the available `python.exe` and `py.exe`
WindowsApps launchers could not be started. This is an environment limitation,
not evidence of a failing suite. A working Python 3.11+ environment and a full
green `python -m pytest -q` run are mandatory before IMP-01 changes begin.

## 2. Milestone proposal

Create the milestone:

`Cross-Requirement Consistency QB-v0.1`

The name follows the approved scientific/architecture package and clearly
distinguishes the bounded slice from the open `Full Single Requirement Model
v1.0` milestone. The milestone contains IMP-01 through IMP-11 only and is
implementation-only.

Recommended issue convention:

- titles start with the stable workstream key `IMP-01` through `IMP-11`;
- each issue is assigned to the proposed milestone;
- use existing label `enhancement` if a label is wanted, otherwise follow the
  repository's current unlabeled-issue convention;
- do not invent issue numbers or new labels; and
- link each issue to its prerequisite issues after GitHub assigns numbers.

The milestone excludes generic logical conflict detection, terminology and
resource conflicts, duplication/Uniqueness, unit conversion, synonym or
semantic matching, generic quantitative grammar, R3, F1-A, risk, corrective
actions, product-quality prediction, an overall quality score, and generic
refactoring.

## 3. Branch and pull-request strategy

### 3.1 Implementation branch

The approved implementation branch name is:

`feat/cross-requirement-consistency-qb-v0.1`

It must be based on the then-current `main` containing PR #113. Because a clean
local branch with this exact name already exists at the current `main`, the
recommended action is to verify and reuse it at implementation kickoff rather
than create a second branch or rewrite it. No branch action is part of this
planning round.

Use it as a rolling feature branch:

1. implement one issue;
2. run its focused tests and the full existing suite;
3. perform local review;
4. commit and push;
5. open one PR to `main` for that issue;
6. merge only after its acceptance gate passes;
7. synchronize the rolling branch with the resulting `main`; and
8. start the next issue only from that verified state.

This permits one logical issue per PR without a final mega-PR. Do not stack an
unreviewed chain of all eleven issues on the remote branch.

### 3.2 Dependency graph

The exact logical DAG is:

```text
IMP-01 ───────> IMP-03 ─> IMP-04 ─> IMP-05 ─> IMP-06 ─> IMP-07 ─> IMP-08
   │                ^         ^                                           │
   │                │         │                                           v
   └─ contract base │         │                                        IMP-09
                    │         │                                           │
IMP-02 ─ identifiers/bridge ──┘                                           v
                                                                          IMP-10
                                                                            │
                                                                            v
                                                                          IMP-11
```

IMP-02 is technically independent of IMP-01: it changes the existing
extraction boundary while IMP-01 creates new cross-domain types. It may be
developed in parallel on a separate temporary branch if repository workflow
later authorizes that. The recommended merge order is nevertheless IMP-01,
IMP-02, IMP-03. This gives projection a manifest containing the allocated
lower-bridge identifiers and gives materiality both approved allowlist entries
before it is implemented. IMP-02 must not be coupled into the cross-analysis
package.

### 3.3 PR sequence

| PR order | Issue | PR boundary and acceptance focus |
| --- | --- | --- |
| 1 | IMP-01 | New immutable cross-domain vocabulary and identity only |
| 2 | IMP-02 | Exact atomic `LB-M-C0` extraction bridge and frozen-local regression only |
| 3 | IMP-03 | Record-to-QB projection and provenance resolvers only |
| 4 | IMP-04 | Fail-closed materiality classification and audit only |
| 5 | IMP-05 | Exhaustive deterministic pair enumeration only |
| 6 | IMP-06 | Pure four-state pair assessment only |
| 7 | IMP-07 | `R_conf[QB-v0.1]` set builder only |
| 8 | IMP-08 | Consistency aggregation and observability only |
| 9 | IMP-09 | Thin specification composition and application orchestration only |
| 10 | IMP-10 | Additive audit/user reporting and final CLI wiring only |
| 11 | IMP-11 | Corpus harness, all acceptance gates, and conditional fixture promotion only |

IMP-07 and IMP-08 share an aggregation module but are not inseparable: the
first PR freezes participant-set semantics; the second consumes that frozen
builder. IMP-09 and IMP-10 are also separate: the composed assessment/service
is independently testable before presentation is changed.

## 4. Ready-to-create implementation issues

### IMP-01 — Implement cross-analysis domain primitives

**Purpose.** Add the immutable, validated vocabulary needed by later QB
algorithms without implementing comparison, selection, aggregation, or
reporting.

**Background.** CRA-A003 through CRA-A007 require stable qualified refs, a
deterministic snapshot, typed states/reasons, and one validated discriminated
cross-result. Existing local domain objects remain unchanged.

**In scope.** Create `cross_analysis/domain.py` and package exports for:

- `AssessmentSnapshot` and its immutable contract/count manifest;
- `CrossObservationRef`, `CrossEvidenceRef`, and `CrossDiagnosticRef`;
- cross-result state, unresolved-reason, outside-reason, conflict class, and
  bounded subtype enums;
- structured comparison operands and bounded non-claim keys;
- `CrossRequirementResult` with state-specific constructors/invariants;
- deterministic source/order keys and stable result identity; and
- validated contract/version descriptors used by later issues.

Adopt one documented canonical identity encoding identified as
`QB-SNAPSHOT-CANONICAL-001`: an ordered, typed standard-library data model,
canonical UTF-8 serialization, exact enum values, and exact `Decimal.as_tuple`
components, hashed with SHA-256. The identity input is exactly architecture
Section 6's QB-relevant state and contract manifest; local C/V/U, traces,
paths, timestamps, UUIDs, object identities, and reporter text are excluded.
The precise serialization fixture belongs in the issue tests and becomes
versioned behavior.

**Out of scope.** Projection from records, resolver lookup, diagnostic
materiality, pair enumeration, normalization, conflict logic, `R_conf`,
aggregation, reporting, and changes to existing domain types.

**Dependencies.** Approved documents merged to `main`; green baseline suite.
No implementation-issue dependency.

**Implementation constraints.** Frozen dataclasses/tuples only; explicit type
validation; no dictionaries as public scientific results; no random or
time-based identity; no reuse of `CharacteristicAssessment`; no scientific
reason represented only as prose. This issue allocates the snapshot canonical
encoding version, not the comparison/materiality/aggregation Rule IDs.

**Expected production files.** New `src/requirements_quality_assessment/
cross_analysis/__init__.py` and `cross_analysis/domain.py`; narrowly scoped
package exports if required. No edits to local calculators or profiles.

**Required tests.** Construction of every primitive; empty/invalid strings;
foreign or duplicate ownership; noncanonical participant order; self-pairs;
cross-snapshot composition; dangling/index-shape rejection; every legal and
illegal state/field matrix; deterministic ref/result ordering; same input gives
same snapshot/result IDs; each included manifest fact changes identity; each
explicitly excluded local/reporting fact does not; fixed canonical-encoding
golden fixture.

**Acceptance criteria.** All invalid ownership/state combinations fail fast;
stable identities and ordering are reproducible; domain objects contain no
algorithm or reporter dependency; full existing suite remains green.

**Traceability.** CRA-D011-D014, D043-D050, D060-D062; CRA-A003-A007;
architecture Sections 4-9 and 21-23.

**Expected artifacts.** Domain module, public exports, domain unit tests, and a
short in-code/README note fixing `QB-SNAPSHOT-CANONICAL-001`.

**PR gate.** Review can validate all invariants without constructing files,
detectors, calculators, CLI objects, or reports.

### IMP-02 — Implement the exact atomic LB-M-C0 extraction bridge

**Purpose.** Make only the researcher-approved exact lower-bound whole-input
envelope observable as the same enriched quantitative observation.

**Background.** The existing `QUANT-UK-001` scalar recognizes the lower bound
but lacks metric and context identity. QB-ER-D002/D005 approve both links only
together in exact `LB-M-C0`; QB-ER-D007 freezes the embedded `500` diagnostic,
global quantitative `INCOMPLETE`, and all local assessment effects.

**In scope.** Implement a narrow whole-envelope coordinator and two separately
owned enrichment contributions. Allocate these production identifiers in this
issue:

- lower metric Rule ID `QUANT-LB-METRIC-001`, Evidence IDs
  `QUANT-LB-METRIC-001:E001...` per owning requirement;
- lower C0 Rule ID `QUANT-LB-CONTEXT-001`, Evidence IDs
  `QUANT-LB-CONTEXT-001:E001...` per owning requirement.

The coordinator has no Rule ID because it is an atomic implementation
mechanism, not a third scientific rule. Match only the approved complete input
envelope; locate exactly one existing `QUANT-UK-001` scalar; construct both
component contributions for that observation; apply both or neither; preserve
observation count/order and the original scalar Evidence.

**Out of scope.** Standalone `LB-M0`; partial enrichment; variants, synonyms,
parser inference, unit-based metric inference, variable populations, generic
context grammar, R3, F1-A, new observations, and any cross-analysis code.

**Dependencies.** Logically independent of IMP-01. Merge after IMP-01 and
before IMP-03/IMP-04 so its identifiers can enter the cross contract manifest
and lower-C0 allowlist.

**Implementation constraints.** Preserve the existing comparator,
inclusivity, `Decimal`, unit, original Evidence, `500` diagnostic/span/rule,
`INCOMPLETE / DETECTED`, C/V/U states and values, findings, traces,
`SpecificationQualityProfile`, `AGG-MVP-001`, and current upper-C0 behavior.
Update only explicit accepted-rule registries that must recognize the two new
Evidence owners; do not broaden existing Rule IDs.

**Expected production files.** Primarily `detectors/quantitative.py`; package
exports and the existing quantitative-Evidence consumer allowlists in
`detectors/condition_context.py` or `detectors/acceptance_criterion.py` only if
their current explicit ownership checks require the new approved IDs.
`extractor.py` may change only for detector wiring. No calculator changes.

**Required tests.** Exact positive envelope and exact metric/context spans;
same observation cardinality; separate Rule/Evidence ownership; atomic
both-or-neither behavior; every readiness Section 3.4/4 exclusion; standalone
lower input remains unenriched; no duplicate observation; preserved `500`
diagnostic and `INCOMPLETE`; unchanged upper C0; unchanged C/V/U, traces,
aggregate profile, audit report, and user report for frozen local fixtures.

**Acceptance criteria.** The approved R002 input yields one enriched existing
observation with `Час відгуку [0,11)`, unchanged `не нижче 5 с [12,24)`, and
context `[25,56)`; negative boundaries do not enrich; all frozen-local
regressions and the full suite pass.

**Traceability.** Model-spec Section 7.14.6.11; QB-ER-D002-D007, D010-D012;
CRA-A009; architecture Section 11.

**Expected artifacts.** Two allocated Rule ID constants, deterministic
Evidence allocation, atomic coordinator, focused extraction tests, and frozen
local regression fixtures.

**PR gate.** Reviewer can prove from tests that the only behavior change is
the approved metric/context Evidence graph for exact `LB-M-C0`.

### IMP-03 — Implement CrossRequirementProjection and provenance resolvers

**Purpose.** Establish the anti-corruption boundary from an ordered
`RequirementAssessmentRecord[]` to one immutable QB snapshot.

**Background.** Only the projector may navigate arbitrary local record
internals. Later QB components consume projected values and scoped resolvers.

**In scope.** Implement the projector, projected requirement/observation/
diagnostic values, snapshot manifest assembly, `CrossEvidenceResolver`, and
diagnostic/observation resolution. Copy required scalar/enum/`Decimal` values;
retain exact frozen source/Evidence/diagnostic access only in the resolver;
qualify all refs by owner; include the IMP-02 IDs/versions in the contract
manifest.

**Out of scope.** Materiality classification, comparison, pair selection,
aggregation, C/V/U reading for science, and report formatting.

**Dependencies.** IMP-01 and IMP-02.

**Implementation constraints.** Project all and only architecture Section
3.2's required fields. Validate unique requirement IDs, strict reader/source
order, one snapshot, quantitative index bounds, exact source/span round trips,
feature-family ownership, component-to-Evidence use, diagnostic refs, and
Evidence from the correct requirement. Invalid provenance is a domain error,
never scientific `UNKNOWN`.

**Expected production files.** New `cross_analysis/projection.py`; small domain
extensions in `cross_analysis/domain.py` if the IMP-01 contract anticipated
them; package exports.

**Required tests.** Valid multi-record projection; zero/one/many observations;
stable indexes and snapshot identity; duplicate IDs; non-strict order;
foreign/dangling/duplicate Evidence; wrong feature family; component not using
the referenced Evidence; observation out of range; diagnostic and Evidence
span mismatch; resolver round trip; cross-snapshot failures; mutation-free
relationship to the input records.

**Acceptance criteria.** Downstream test doubles can obtain every approved QB
fact without reading a `RequirementAssessmentRecord`; resolver proves all
ownership/span invariants; existing records are unchanged; full suite passes.

**Traceability.** CRA-D043, D046, D048-D051, D060-D062; CRA-A001-A005;
architecture Sections 3-6, 18, and 23.

**Expected artifacts.** Projector, immutable views, resolvers, validation
tests, and a manifest fixture including all allocated contract identifiers.

**PR gate.** No comparison, classification, or aggregate state is produced.

### IMP-04 — Implement the fail-closed QB materiality classifier

**Purpose.** Implement the CRA-D067/QB-ER-D009 distinction between global
unresolved extraction and QB-material unresolved extraction.

**Background.** Only exact embedded `500` diagnostics proven to belong to the
approved upper C0 or lower C0 contracts may be non-material to QB-v0.1. The
diagnostic and global `INCOMPLETE` remain visible.

**In scope.** Add a two-pass classifier, closed two-entry allowlist, per-
diagnostic audit records, all eight gates, and the three separate counts.
Allocate materiality Rule ID/version `QB-MATERIALITY-001` / `1`.

**Out of scope.** Configurable ignored codes, wildcard allowlists, detector
changes, diagnostic suppression, observation-component reason handling,
pair-state assessment, or aggregation state selection.

**Dependencies.** IMP-01 through IMP-03; IMP-02 supplies the lower allowlist
descriptor.

**Implementation constraints.** Exact code, source Rule ID, ASCII `500`, span
containment, same observation, exact contract version, no competitor, and full
provenance must all pass. Any missing/changed/invalid fact is
`QB_MATERIAL_UNRESOLVED`. Classification is snapshot-aware and two-pass so a
later competitor invalidates an early apparent exception.

**Expected production files.** New `cross_analysis/materiality.py`; audit
values/enums in `cross_analysis/domain.py` only as already scoped by IMP-01.

**Required tests.** Both positive allowlist entries; each of the eight gates
failed individually; every readiness negative; extra candidate/observation;
version mismatch; malformed/dangling provenance; two-pass competition;
deterministic audit ordering; count equations; global diagnostic and
`INCOMPLETE` preservation.

**Acceptance criteria.** Exactly approved C0 diagnostics can be
`QB_NON_MATERIAL`; every other case fails closed; audit records identify
requirement, diagnostic, span, governing Evidence/contract/version, every gate,
and rule version; all three counts are independently observable.

**Traceability.** CRA-D067; QB-ER-D008-D011; CRA-A008; architecture Section
10; readiness Sections 5-7.

**Expected artifacts.** Classifier, fixed allowlist, materiality Rule ID,
audit records, and exhaustive gate tests.

**PR gate.** No detector state or local assessment/report meaning changes.

### IMP-05 — Implement exhaustive deterministic pair selection

**Purpose.** Materialize the architecture-approved oracle comparison universe.

**Background.** QB-v0.1 requires each unordered distinct requirement pair and
the full Cartesian product of their quantitative observations. Mismatched and
unresolved members must not be pruned.

**In scope.** Enumerate requirements in source order, each pair once with the
earlier owner first, then left/right observations in source order. Emit one
immutable candidate per Cartesian-product member and expose deterministic
counts/order.

**Out of scope.** Identity-key grouping, indexing, optimization thresholds,
applicability, state classification, conflict logic, material diagnostics with
no observation, and aggregation.

**Dependencies.** IMP-03; materiality may already exist but is not consumed by
selection.

**Implementation constraints.** No self-pairs, reverse duplicates, within-
requirement comparisons, first-observation shortcuts, or key-based pruning.
Omission or duplication is a programmer/invariant error.

**Expected production files.** New `cross_analysis/selection.py`; no changes
to projection or detector code.

**Required tests.** Empty, single-requirement, zero-observation, 1x1, 2x3,
multiple requirement pairs, no self/reverse pairs, exact source order, stable
repeat output, candidate-count formula, and retention of resolved mismatch and
unresolved observations.

**Acceptance criteria.** Produced candidates equal
`sum(i<j, O_i * O_j)` in exact approved order for every fixture; no scientific
disposition is assigned; full suite passes.

**Traceability.** CRA-D005-D010, D057, D060-D061; CRA-A010 and deferred
CRA-A016; architecture Section 12.

**Expected artifacts.** Exhaustive selector and oracle/count tests.

**PR gate.** There is no index, semantic key, or performance threshold.

### IMP-06 — Implement pure QB observation-pair assessment

**Purpose.** Apply the approved four-state QB-v0.1 decision chain to one
candidate pair.

**Background.** Applicability, bounded normalization, supported inclusive
bounds, exact `Decimal` predicate, and validated result construction are
separate pure responsibilities.

**In scope.** Implement `QbApplicabilityEvaluator`,
`QbComparisonKeyBuilder`, `QbSupportedBoundValidator`, direct bound predicate,
and result factory/service. Allocate comparison/confirmation Rule ID/version
`QB-COMPARE-001` / `1` and coverage profile ID/version `QB-v0.1` / `1`.

**Out of scope.** Candidate selection, global materiality, aggregate state,
`R_conf`, general interval algebra, open intervals, tolerance, conversion,
synonyms, semantic equivalence, and reporting prose.

**Dependencies.** IMP-01, IMP-03, and IMP-05. IMP-04 is not a pair-assessor
input; it is consumed later by aggregation.

**Implementation constraints.** Decision precedence is comparator outside
profile; resolved metric/context/unit mismatch; missing or unresolved input;
unsupported/unresolved inclusivity; supported predicate. Normalize text only
with NFC, case folding, Unicode-whitespace collapse, and trim. Units compare by
exact `UnitLabel`. Supported comparators are inclusive `LESS_THAN_OR_EQUAL`
and `GREATER_THAN_OR_EQUAL`. Two uppers and two lowers are compatible; mixed
bounds conflict iff lower `>` upper; equality is compatible. Preserve
qualified Evidence from both requirements and deterministic reasons/order.

**Expected production files.** New `cross_analysis/comparison.py`; only
pre-scoped domain constants/exports elsewhere.

**Required tests.** Every reason code and precedence combination; normalization
positive/negative boundaries; exact unit mismatch; supported/unsupported
comparators; missing values/components; unresolved inclusivity; same-direction
bounds; lower greater/equal/less than upper; exact `Decimal`; all four result
states; stable IDs; Evidence from both owners; state-construction rejection;
required decision examples and RC-QB-001/002/004/006-010/012/015/017 at their
declared unit/domain boundary.

**Acceptance criteria.** The pure assessor distinguishes
`CONFIRMED_CONFLICT`, `COMPATIBLE_WITHIN_RULE`, `ASSESSMENT_UNRESOLVED`, and
`OUTSIDE_V0_1_APPLICABILITY` exactly; it cannot access other pairs, aggregate
counts, local C/V/U, detectors, CLI, or reporters.

**Traceability.** CRA-D001-D003, D011-D013, D029-D041, D043-D047, D056-D059,
D062-D065; CRA-A006-A007, A011, and rejected A017; architecture Sections 7-9
and 13-14.

**Expected artifacts.** Pure comparison module, allocated rule/profile
versions, structured operands, and pair-rule tests.

**PR gate.** Review can execute it using manually built projected observations.

### IMP-07 — Implement the R_conf[QB-v0.1] builder

**Purpose.** Construct the unique observed conflict-participant set without
performing aggregate arithmetic.

**Background.** `R_conf` counts requirement participants, not results or
pairs. Observed membership remains useful but partial when unresolved work can
add members.

**In scope.** Add both participants from validated confirmed results, collapse
duplicates, emit source-ordered IDs, validate snapshot/result ownership, and
derive `rconf_complete` from unresolved pair/materiality facts supplied by the
caller.

**Out of scope.** Reassessing results, `Fraction`, aggregate state/value,
reporter priority, or full-source unqualified `R_conf`.

**Dependencies.** IMP-01, IMP-04, and IMP-06.

**Implementation constraints.** Consume only validated ordered results;
non-conflict states never add members. Reject unknown participants, duplicate
result IDs, snapshot mismatch, and noncanonical pair order. Partial observed
membership is audit data only.

**Expected production files.** `cross_analysis/aggregation.py` with only the
set-builder responsibility; narrow domain view if already planned.

**Required tests.** No conflicts; one conflict adds both; repeated participant
deduplication; several disjoint conflicts; source-order output independent of
result discovery order; non-conflict exclusion; invalid participant/result/
snapshot rejection; complete versus partial observed set.

**Acceptance criteria.** Output cardinality is unique requirement cardinality;
confirmed results remain represented when completeness is false; no numeric
Consistency value is produced.

**Traceability.** CRA-D015-D017, D021, D028; CRA-A012; architecture Section 15.

**Expected artifacts.** Validated builder and dedicated participant-set tests.

**PR gate.** No aggregation Rule ID or formula yet.

### IMP-08 — Implement QbConsistencyAssessment aggregation

**Purpose.** Produce the bounded specification-level Consistency assessment,
exact value when observable, and complete coverage metadata.

**Background.** QB aggregation is a direct set-cardinality formula and is not
`AGG-MVP-001`. Strict observability gates select `COMPUTED`, `UNKNOWN`, or
`NOT_APPLICABLE`.

**In scope.** Implement observability metadata, aggregate reasons,
`QbConsistencyAssessment`, state decision order, exact
`Fraction(N_R - N_Rconf, N_R)`, partial/complete `R_conf`, non-claim set, and
all metadata equations. Allocate aggregation Rule ID/version
`QB-CONSISTENCY-001` / `1` and bounded non-claim set/version
`QB-NON-CLAIMS-001` / `1`.

**Out of scope.** Full unqualified `M_cons`, mean aggregation, local profile
changes, risk/severity, report formatting, and recomputation of pair states.

**Dependencies.** IMP-04, IMP-06, and IMP-07.

**Implementation constraints.** Apply the frozen decision order: fewer than
two requirements -> NA; else any QB-material diagnostic or unresolved pair ->
UNKNOWN; else zero applicable comparisons -> NA; else COMPUTED. Preserve all
global/QB-material/QB-non-material counts and partial confirmed results.
Validate requirement-pair, observation-pair, applicable, state-total,
diagnostic-classification, and observed-set equations. A computed `1` always
retains bounded non-claims.

**Expected production files.** Extend `cross_analysis/aggregation.py` and the
already scoped assessment values in `cross_analysis/domain.py`.

**Required tests.** Empty and one requirement; complete universe with no
applicable pair; all compatible; one/multiple conflicts; isolated
non-quantitative requirements in denominator; unresolved pair; material
diagnostic with no pair; non-material upper/lower C0 diagnostics; partial
`R_conf`; exact reduced fractions; every metadata equation and invalid state/
value/count combination; RC-QB-003/005/011/018-027 at their declared boundary.

**Acceptance criteria.** Formula runs only under approved gates; UNKNOWN and
NA always have `None`; NA is never numeric `1`; partial `R_conf` is never used
as numerator; `AGG-MVP-001` and `SpecificationQualityProfile` are untouched.

**Traceability.** CRA-D018-D028, D066-D067; CRA-A013; architecture Section 16;
readiness materiality amendment.

**Expected artifacts.** Aggregator, assessment/metadata values, rule/non-claim
versions, and exhaustive state/equation tests.

**PR gate.** Manually constructed domain inputs fully test the formula without
files, detectors, CLI, or reporters.

### IMP-09 — Integrate SpecificationAssessment and orchestration

**Purpose.** Compose the unchanged local profile with the separate QB
assessment and provide the first complete application service.

**Background.** Cross-analysis enters only after all ordered
`RequirementAssessmentRecord` values exist. The local aggregator and cross
pipeline remain independent.

**In scope.** Add immutable `SpecificationAssessment(snapshot_id,
quality_profile, qb_consistency)`, cross-analysis sequencing service, and
composition validation. The service accepts completed records, computes the
existing profile through the existing aggregator, then projects, classifies,
selects, assesses, builds `R_conf`, aggregates, and composes. Expose all
ordered cross results/materiality audit data needed by IMP-10 without putting
them into the local profile.

**Out of scope.** Reporter prose/layout, scalar combination, modification of
local records/profiles, extraction inside cross-analysis, and scientific logic
inside CLI.

**Dependencies.** IMP-03 through IMP-08.

**Implementation constraints.** Existing Single Requirement code must not
import `cross_analysis`. The service is thin sequencing only. Validate the
same ordered source set and snapshot association. Keep `SpecificationQuality
Aggregator` as the sole owner of `AGG-MVP-001`. Existing CLI/report output may
remain unchanged in this intermediate PR; final CLI report-bundle wiring is
IMP-10.

**Expected production files.** New `cross_analysis/specification.py` and
`cross_analysis/service.py`; package exports. `cli.py` changes only if the new
service can be introduced while producing byte-for-byte equivalent old output;
otherwise CLI wiring is explicitly deferred to IMP-10.

**Required tests.** Composition type/state validation; snapshot mismatch;
records fully built before projection; local and cross pipelines called once;
cross UNKNOWN/NA does not affect local profile; local aggregate does not affect
cross result; empty/single/multi-requirement service runs; no overall value;
existing local pipeline regression.

**Acceptance criteria.** One application call returns the unchanged local
profile and separate QB assessment associated with the same source set;
dependency direction has no cycle; full suite passes.

**Traceability.** CRA-D051-D055; CRA-A001, A013-A014, A018; architecture
Sections 17-18, 22-23.

**Expected artifacts.** Thin composition, sequencing service, integration
tests, and an explicit dependency-direction review note.

**PR gate.** No report calculation or local-profile reinterpretation.

### IMP-10 — Add cross-requirement technical and user reporting

**Purpose.** Render the finished QB assessment and provenance as a separate
section in both existing views.

**Background.** Existing report sections and meanings are frozen. Reporting
selects and formats supplied results; it does not calculate science.

**In scope.** Add an immutable report bundle, additive cross-report sections,
and final CLI/service wiring. The audit view shows contracts, counts,
materiality audits, all states/reasons, participants, exact operands, and
Evidence from both owners. The user view concisely distinguishes conflict,
bounded compatibility, unresolved, outside, UNKNOWN, NA, and computed values.

**Out of scope.** Reassessment, aggregation, diagnostic reclassification,
risk/severity/priority, correction advice, product-quality claims, universal
Consistency language, and redesign of existing local sections.

**Dependencies.** IMP-09.

**Implementation constraints.** Preserve existing local sections and delegate
their rendering. UNKNOWN states why value was withheld. NA is never displayed
as `1`. Computed `1` carries the complete bounded non-claim. Compatible means
jointly satisfiable within this rule only. Global `INCOMPLETE` remains visible
when a diagnostic is QB-non-material. Evidence is resolved, not duplicated or
rewritten. Ordering never implies priority.

**Expected production files.** New `cross_reporter.py` (or equally separated
module), additive composition in `reporter.py`, final `cli.py` wiring, and
report-bundle values in `cross_analysis/specification.py` if appropriate.

**Required tests.** Golden/structural audit and user outputs for all four pair
states and all three aggregate states; two-owner Evidence; partial `R_conf`;
material/non-material diagnostic disclosure; exact Fraction; NA versus one;
bounded non-claims; deterministic ordering; no forbidden vocabulary/claims;
unchanged existing local sections in both views; CLI view selection and errors.

**Acceptance criteria.** Both reports expose the approved cross section from
finished objects only; current local meaning remains intact; all explanations
are traceable; full suite passes.

**Traceability.** CRA-D043, D048-D050, D059, D062-D065; CRA-A015; architecture
Section 19 and model-spec Section 19.6.

**Expected artifacts.** Report bundle, two cross-section renderers, CLI
integration, reporter/CLI regression tests.

**PR gate.** No formula, normalization, state decision, or materiality logic is
present in reporters.

### IMP-11 — Run reference-corpus and end-to-end acceptance

**Purpose.** Demonstrate conformance of the complete delivered slice and only
then promote the approved future exact upper/lower fixture.

**Background.** The 27 reference cases are binding at their declared domain or
end-to-end boundary. The upper-2/lower-5 fixture is currently non-binding until
implementation, identifier allocation, audit, and explicit corpus amendment.

**In scope.** Add one data-driven corpus harness for RC-QB-001 through
RC-QB-027; execute every case at its declared boundary; run frozen-local and
full regression; run the exact R001/R002 pipeline; audit IDs, spans, ordering,
counts, states, Evidence, `R_conf`, Fraction, diagnostics, and non-claims; then
amend the reference-cases document to promote the future fixture only after
all gates pass.

**Out of scope.** New science, grammar broadening, refactoring, performance
indexing, or weakening a reference expectation to fit implementation. Any
behavioral defect discovered here is fixed in its owning component through a
small reviewed correction, not hidden in corpus data.

**Dependencies.** IMP-01 through IMP-10.

**Implementation constraints.** Preserve case boundary/status and exact
expected data. Domain-contract cases use manually constructed values; current-
extractor cases run end to end. Promotion is a status change with traceability,
not silent replacement of an existing case.

**Expected production files.** Normally none. New corpus fixture/harness files
under `tests/`; `docs/cross-requirement-consistency-reference-cases.md` only for
the conditional promotion and implementation evidence.

**Required tests.** All 27 cases; exact future input:

```text
R001: Час відгуку ≤ 2 с при 500 одночасних користувачах
R002: Час відгуку не нижче 5 с при 500 одночасних користувачах
```

Expected result: one `CONFIRMED_CONFLICT`,
`R_conf[QB-v0.1] = {R001, R002}`, complete `R_conf`,
`M_cons[QB-v0.1] = Fraction(0, 1)`, aggregate `COMPUTED`, and both preserved
global diagnostics/`INCOMPLETE` states with non-materiality audit proof.

**Acceptance criteria.** Every binding expectation passes; the future target
passes exactly; full existing suite passes; no local profile/report regression;
promotion occurs only after recorded audit; milestone DoD evidence is linked
from the PR.

**Traceability.** CRA-D041-D042; QB-ER-D013; architecture Section 24; all 27
reference-case contracts; readiness Section 8.

**Expected artifacts.** Corpus harness, fixtures, conformance report in the PR,
conditional reference-case status amendment, and final regression evidence.

**PR gate.** Any failed binding expectation blocks milestone completion; the
test is not weakened without a new approved research/architecture amendment.

## 5. Milestone Definition of Done

The milestone is done only when all of the following are true:

1. PR #113 remains in the ancestry of the implementation base and IMP-01
   through IMP-11 have each passed review and merged through scoped PRs.
2. All existing Single Requirement behavior is preserved, including
   `RequirementAssessmentRecord`, `RequirementExtractionResult`, Evidence,
   diagnostics, C_i/V_i/U_i, traces, `SpecificationQualityProfile`,
   `SpecificationQualityAggregator`, `AGG-MVP-001`, and local reporting
   meaning.
3. A multi-requirement specification is processed only after all local records
   exist, and cross-analysis does not mutate them.
4. Exhaustive unordered distinct requirement pairs times cross-requirement
   observation pairs are constructed in deterministic source order.
5. All four pair states are produced according to the approved precedence and
   typed reason contracts.
6. The direct incompatible inclusive-bound rule detects conflict iff mixed
   lower `>` upper, using exact `Decimal` and exact bounded identity.
7. Every result preserves validated qualified Evidence from both requirements
   where required, plus any diagnostic provenance needed by its reason.
8. `R_conf[QB-v0.1]` is the source-ordered unique set of confirmed-conflict
   participants; partial observed membership remains audit-only.
9. `M_cons[QB-v0.1]` is an exact reduced `Fraction` computed only under the
   approved observability gates and never presented as unqualified `M_cons`.
10. `UNKNOWN` and `NOT_APPLICABLE` follow the approved state decision order;
    NA is never substituted by `1`, and computed `1` carries bounded
    non-claims.
11. Global unresolved diagnostics, QB-material unresolved diagnostics, and
    QB-non-material preserved diagnostics are all counted and explained
    separately; only both exact C0 contracts can pass the fail-closed exception.
12. `SpecificationAssessment` composes the unchanged local profile and
    `QbConsistencyAssessment` without an overall scalar.
13. Technical/audit and user reports contain a separate cross-requirement
    section, retain existing sections, and perform no scientific calculation.
14. All 27 binding cases pass at their declared boundaries.
15. The exact upper/lower future target produces the approved conflict,
    participant set, `Fraction(0,1)`, `COMPUTED` state, and preserved global
    diagnostic/incomplete evidence before it is promoted.
16. The complete pre-existing and new test suite passes in a documented Python
    3.11+ environment.
17. No excluded scope, speculative refactor, generic rule engine, index, unit
    conversion, semantic matcher, risk model, or product-quality claim has
    entered the milestone.

## 6. Validation strategy

### 6.1 Per-PR gates

Every PR must run:

1. focused tests for the changed responsibility;
2. cross-layer tests only for already merged dependencies;
3. the full `python -m pytest -q` suite;
4. a local review for scientific traceability, dependency direction, frozen
   contracts, and forbidden scope; and
5. deterministic repeat runs where identity/order/output is involved.

No PR may rely on IMP-11 to supply missing unit coverage for its own rule.

### 6.2 Validation layers

| Layer | Primary issues | Mandatory evidence |
| --- | --- | --- |
| Domain invariants/identity | IMP-01 | state matrices, ownership failures, cross-snapshot failures, canonical identity golden fixtures |
| Frozen extraction and local behavior | IMP-02 | exact/negative envelopes, unchanged observations/diagnostics/C/V/U/traces/aggregates/reports |
| Projection/provenance | IMP-03 | record-to-view fidelity, span round trips, foreign/dangling failures |
| Materiality | IMP-04 | all eight gates, two allowlist positives, all fail-closed negatives, count separation |
| Universe selection | IMP-05 | Cartesian oracle, count formula, stable ordering, no pruning |
| Pair science | IMP-06 | four states, precedence, normalization boundaries, exact predicate, two-owner Evidence |
| Conflict participants | IMP-07 | set union, uniqueness, source order, partial completeness |
| Aggregate science | IMP-08 | state order, exact Fraction, metadata equations, bounded non-claims |
| Composition/orchestration | IMP-09 | downstream insertion, one source set, independent local and cross paths |
| Presentation | IMP-10 | two views, immutable input consumption, local-section regression, non-claims |
| Corpus/end to end | IMP-11 | RC-QB-001..027 plus the conditional upper/lower target and full regression |

### 6.3 Failure policy

- A domain/provenance invariant failure raises a validation/programmer error;
  it is not converted to scientific `UNKNOWN`.
- A scientifically missing/unresolved component becomes a typed unresolved
  pair reason.
- A resolved boundary mismatch becomes typed outside applicability.
- An unproven diagnostic is material and withholds the aggregate.
- A binding-case mismatch blocks the owning PR or milestone; expectations are
  not edited to accommodate implementation.

## 7. Deferred post-acceptance refactoring

The following are candidates only after the first accepted end-to-end slice:

- shared state/value validation utilities;
- reusable qualified Evidence/diagnostic-ref helpers;
- a measured candidate index with exhaustive-oracle equivalence tests;
- a generic versioned rule/contract registry;
- shared ordering helpers;
- package restructuring demonstrated necessary by actual dependency pain; and
- report layout cleanup that preserves approved meanings.

None belongs to the milestone DoD unless implementation demonstrates a
specific correctness blocker. In that event, document the blocker and create a
separate narrowly scoped issue; do not hide a refactor inside an IMP PR.

## 8. Implementation risks and protections

| Risk | Protection |
| --- | --- |
| Pre-existing local feature branch masks an incorrect future base | Re-fetch and compare remote `main`, PR #113 ancestry, branch-only commits, diff, and upstream immediately before IMP-01; stop on mismatch. |
| IDs are added ad hoc or old Rule IDs are broadened | IMP-02/04/06/08 allocate explicit IDs/versions; manifests and golden tests freeze them; existing upper-C0 ID is never reused for lower semantics. |
| Snapshot IDs churn with irrelevant local/report changes | `QB-SNAPSHOT-CANONICAL-001` includes only approved QB state/manifest and has include/exclude regression tests. |
| Cross-analysis leaks into local calculators or aggregation | One-way dependency checks and IMP-09 integration tests; no import from existing Single Requirement modules into cross-analysis consumers. |
| Evidence becomes detached or IDs collide across records | Always use qualified refs plus resolver ownership, family, span, and observation-use validation. |
| Exact C0 exception hides a real unresolved operand | Closed two-entry versioned allowlist, all eight gates, two-pass competition scan, and fail-closed default. |
| Pair optimization silently changes coverage | Ship the exhaustive oracle only; indexing is deferred until measured need and exact equivalence evidence. |
| UNKNOWN, outside, compatible, and NA collapse in code or prose | Separate enums/constructors, state matrices, typed reasons, and reporter fixtures for every state. |
| Partial `R_conf` is used as a numeric numerator | IMP-07 keeps completeness explicit; IMP-08 constructor rejects a numeric value when incomplete. |
| Computed `1` is presented as universal Consistency | Versioned mandatory non-claim set and audit/user golden tests. |
| Reporters recalculate or reinterpret results | Finished immutable report bundle; reporter modules may select/format only; unit tests use prebuilt assessments. |
| IMP-02 changes frozen local behavior | Dedicated before/after local regression for observations, diagnostic, processing, C/V/U, trace, aggregate, and both reports. |
| Open Single Requirement issues leak into QB work | Treat #68 and #70-#78 plus legacy #5/#6/#14 as separate work; exact issue out-of-scope lists are review gates. |
| Test environment remains unavailable | Resolve Python 3.11+/pytest execution before IMP-01; no implementation PR opens without a green baseline. |

## 9. Decision-to-issue traceability

### 9.1 Architecture decision register

| Architecture decision | Implemented/protected by |
| --- | --- |
| CRA-A001 downstream insertion | IMP-03, IMP-09 |
| CRA-A002 immutable projection plus resolver | IMP-03 |
| CRA-A003 qualified observation identity | IMP-01, IMP-03 |
| CRA-A004 qualified Evidence refs | IMP-01, IMP-03, IMP-10 |
| CRA-A005 deterministic QB snapshot identity | IMP-01, IMP-03 |
| CRA-A006 one validated discriminated result | IMP-01, IMP-06 |
| CRA-A007 typed minimal reason vocabulary | IMP-01, IMP-06, IMP-10 |
| CRA-A008 downstream exact materiality classifier | IMP-04 |
| CRA-A009 two atomically coordinated lower enrichment rules | IMP-02 |
| CRA-A010 exhaustive selector | IMP-05 |
| CRA-A011 minimal direct inclusive-bound predicate | IMP-06 |
| CRA-A012 separate set-union `R_conf` builder | IMP-07 |
| CRA-A013 separate `QbConsistencyAssessment` | IMP-08 |
| CRA-A014 thin `SpecificationAssessment` in integrated slice | IMP-09 |
| CRA-A015 additive composed reporting | IMP-10 |
| CRA-A016 indexed selector deferred | IMP-05 non-goals; post-acceptance list |
| CRA-A017 generic interval/semantic engine rejected | IMP-06 constraints/non-goals |
| CRA-A018 responsibility-separated package | IMP-01, IMP-03-IMP-10 |

### 9.2 Scientific decision groups

| Approved decision group | Owning issues |
| --- | --- |
| CRA-D001-D010 scope, unit, universe, candidate separation | IMP-05, IMP-06 |
| CRA-D011-D014 four states, confirmation, unresolved, snapshot | IMP-01, IMP-06 |
| CRA-D015-D021 `R_conf`, empty/single/no-applicable/partial semantics | IMP-07, IMP-08 |
| CRA-D022-D028 and D066-D067 formula, exactness, observability, bounded naming/materiality | IMP-04, IMP-07, IMP-08, IMP-10 |
| CRA-D029-D041 normalization, identity, supported bounds, predicate, examples | IMP-06, IMP-11 |
| CRA-D042 binding mixed corpus | IMP-11 |
| CRA-D043-D050 result and provenance contract | IMP-01, IMP-03, IMP-06, IMP-10 |
| CRA-D051-D055 local/specification boundaries | IMP-09, IMP-10 |
| CRA-D056-D059 unresolved/outside/non-claim boundary | IMP-06, IMP-08, IMP-10 |
| CRA-D060-D065 ordering and prohibited claims | IMP-01, IMP-05-IMP-10 |
| QB-ER-D002-D007 exact lower bridge and frozen extraction behavior | IMP-02 |
| QB-ER-D008-D011 exact C0 materiality amendment | IMP-04, IMP-08 |
| QB-ER-D012 R3/F1-A non-solution/deferment | Every issue non-goal; especially IMP-02 and IMP-06 |
| QB-ER-D013 conditional end-to-end promotion | IMP-11 |
| QB-ER-D014 broader extraction/semantic scope deferred | Every issue out-of-scope gate |

## 10. Final readiness

The implementation milestone and issue set can now be created. The research
and architecture package is merged to current `main`, no duplicate Cross
Requirement milestone/issues exist, the proposed branch base is known, and
the implementation work is partitioned into reviewable PRs. Implementation
itself remains gated on issue/milestone creation, a fresh base verification,
and a working green Python test environment.

READY_TO_CREATE_IMPLEMENTATION_MILESTONE_AND_ISSUES

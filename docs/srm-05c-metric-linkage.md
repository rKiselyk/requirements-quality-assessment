# SRM-05C — Explicit Metric and Single-Bound Linkage Research

**Issue:** #73  
**Research slice:** explicit metric identification and linkage to one approved
scalar anchor  
**Document status:** `DRAFT_FOR_RESEARCHER_REVIEW`

This document is a bounded scientific decision package. It identifies one
source-attested candidate, defines the smallest linkage and Evidence proposal
that could be reviewed, and exposes every remaining approval gate. It does not
approve production grammar, allocate or reuse a Rule ID, define binding tests,
or authorize implementation.

## 1. Purpose, scope and baseline

`EXISTING_APPROVED` — The protected baseline is `main` after merged PR #92,
whose task-supplied verified merge commit is
`20b8d1395a6400ac8d5e5dbf3f778636533b117d`. No Git or GitHub operation was
performed for this package.

`PROPOSED_RESEARCH_DECISION` — This slice asks whether exactly one explicitly
written Ukrainian metric can be linked to exactly one already-accepted scalar
anchor in the same requirement clause. The candidate must preserve the
existing anchor rather than reparse, replace, enlarge, or merge it.

`DEFERRED` — Load, population, measurement-window and general
`condition_context` attachment; nested or compound constraints; ranges;
written frequency; multiple-result acceptance; general nonnumeric
judgeability; formulas; quality-problem inference; and parser upgrades remain
outside this slice.

`EXISTING_APPROVED` — The only eligible scalar anchors are those already
accepted by `QUANT-001` and `QUANT-UK-001`. Their comparator labels,
inclusivity, values, units, Evidence, precedence, diagnostics, and acceptance
interaction remain unchanged. In particular, `до` remains
`UPPER_BOUND / UNRESOLVED`; decimal-point measured values, new comparator or
unit surfaces, conversions, and written-out-number parsing are excluded.

`EXISTING_APPROVED` — `ACCEPT-QUANT-001` judgeability does not change. Linking
a metric to an observation does not by itself create a new acceptance
criterion, Finding, `QUALITY_PROBLEM`, applicability value, confidence,
severity, score, or C/V/U contribution.

## 2. Scientific and implementation sources

The audit was restricted to the requested material.

| Source | Use in this package | Classification |
| --- | --- | --- |
| [`model-spec.md` §7.6](model-spec.md) | Defines one linked, partial quantitative observation and distinguishes an unexpressed metric from an explicitly expressed but unresolved metric. | `EXISTING_APPROVED` |
| [`model-spec.md` §§7.14.6.4–7.14.6.6](model-spec.md) | Supplies attested metric expressions, the conservative same-clause linkage boundary, the non-authorizing traceability examples, and the protected `QUANT-001`/`QUANT-UK-001` scalar allocation. | `EXISTING_APPROVED` |
| [`model-spec.md` §7.15.10](model-spec.md) | Defines `TextComponent`, `unresolved_components`, component Evidence refs, and the source-ordered top-level union. | `EXISTING_APPROVED` |
| [`model-spec.md` §18, `RQD-008`](model-spec.md) | Keeps complex metric/context grammar, count-noun roles, and nested representation open. | `EXISTING_APPROVED` |
| [`srm-05-quantitative-research.md` §§3, 5–9](srm-05-quantitative-research.md) | Establishes the scalar baseline, identifies metric linkage as Slice 2, and supplies non-binding research cases and approval gates. | `EXISTING_APPROVED` |
| [`srm-05b-scalar-decisions.md`](srm-05b-scalar-decisions.md) | Concludes `NO_EXTENSION_READY` for scalar syntax and therefore freezes the anchor vocabulary used here. | `EXISTING_APPROVED` |
| [`reference/2.2_Взаємозвязок_вимог_і_якості.docx`](reference/2.2_Взаємозвязок_вимог_і_якості.docx), §2.2/Table 2.5 passage | Directly attests `Час відгуку ≤ 2 с при 500 одночасних користувачах` and separately lists response time among measurable performance quantities. | `SOURCE_ATTESTED_NOT_ALLOCATED` |
| [`reference/Приклад_застосування_моделі.docx`](reference/Приклад_застосування_моделі.docx), §8/Table 7 passages | Attests longer nominal metrics and quantitative contexts, but not another equally small metric/bound template suitable for this slice. | `SOURCE_ATTESTED_NOT_ALLOCATED` |
| [`quantitative.py`](../src/requirements_quality_assessment/domain/quantitative.py), [`detectors/quantitative.py`](../src/requirements_quality_assessment/detectors/quantitative.py), and directly related tests | Confirm that the current implementation stores partial linked observations, exact refs, scalar-anchor Evidence, and family diagnostics. Code behavior is not scientific authorization. | `EXISTING_APPROVED` as implementation confirmation only |

`SOURCE_ATTESTED_NOT_ALLOCATED` — The dissertation example supplies an
explicit metric, a symbolic scalar anchor, and a following load phrase. It
supports investigation of the metric/bound relation, but it does not itself
allocate detector grammar.

`UNSUPPORTED_BY_AVAILABLE_SOURCES` — The audited passages do not define a
general Ukrainian noun-phrase grammar, an exhaustive metric vocabulary, a
parser dependency label that is always sufficient, or a general rule for
essential complements.

## 3. Approved baseline and unresolved `RQD-008` boundary

| Topic | Protected baseline | Remaining boundary | Classification |
| --- | --- | --- | --- |
| Linked observation | `metric`, `comparator`, `value`, `unit`, `context`, `unresolved_components`, and `evidence_refs` coexist in one `QuantitativeConstraintObservation`. | Concrete metric-recognition and attachment grammar is not allocated. | `EXISTING_APPROVED` |
| Scalar anchors | Only existing `QUANT-001` and `QUANT-UK-001` observations are eligible. | SRM-05C must not extend scalar syntax. | `EXISTING_APPROVED` |
| Metric absence | A baseline anchor with no metric expression has `metric = None` and no `METRIC` unresolved entry. | Absence must not be recast as failed extraction. | `EXISTING_APPROVED` |
| Expressed ambiguity | An expressed candidate whose metric role cannot be resolved has `metric = None` and `METRIC` in `unresolved_components`. | The exact recognizing grammar, diagnostic, and trigger are unapproved. | `EXISTING_APPROVED` representation; `PROPOSED_RESEARCH_DECISION` detector semantics |
| Linkage | A metric may be linked only through a separately approved template or grammatical rule in the same clause; proximity is forbidden. | No such production metric template is currently approved. | `EXISTING_APPROVED` |
| Hard boundaries | Full stop, semicolon, question mark, and exclamation mark are hard boundaries in the lexical baseline. A comma cannot authorize linkage by itself. | Broader parser clauses are outside this slice. | `EXISTING_APPROVED` |
| Multiple anchors | Distinct anchors remain separate unless an approved range rule says otherwise. | Shared metrics, coordination, nesting, and reusable attachment identity remain open. | `EXISTING_APPROVED` separation; `DEFERRED` attachment grammar |
| Acceptance | Existing judgeability depends on the accepted scalar observation and approved result containment, not on metric population. | No new acceptance observation follows from a metric link. | `EXISTING_APPROVED` |

`EXISTING_APPROVED` — The fully linked outputs shown in model-spec
§7.14.6.5 are traceability examples. They are not an unimplemented production
contract and are not promoted to one by this package.

## 4. Candidate minimal metric grammar

### 4.1 Source-attested seed

`SOURCE_ATTESTED_NOT_ALLOCATED` — The exact source is:

```text
Час відгуку ≤ 2 с при 500 одночасних користувачах
```

For this slice only, the research subject is the prefix:

```text
Час відгуку ≤ 2 с
```

The trailing `при 500 одночасних користувачах` is neither consumed nor
classified by this candidate. Existing baseline handling of its numeric text
must remain intact.

### 4.2 Smallest candidate template

`PROPOSED_RESEARCH_DECISION` — The smallest reviewable template is:

```text
<requirement-start>
Час відгуку<U+0020><one already-accepted QUANT-001 symbolic anchor>
```

with all of these restrictions:

1. The metric surface is exactly `Час відгуку`, with exact casing and exactly
   one U+0020 SPACE between its two words.
2. Exactly one U+0020 SPACE separates the metric surface from the already
   accepted anchor.
3. The anchor must already have been accepted by `QUANT-001` through its
   symbolic `≤` construction. SRM-05C does not reparse its value or unit.
4. The metric begins at requirement offset `0`; metric and anchor are therefore
   in the same hard-bounded clause for the attested seed.
5. The candidate region must contain exactly one eligible metric surface and
   one eligible scalar anchor.
6. The metric is the explicit left operand of the symbolic relation; the
   accepted scalar anchor supplies its right-hand bound. This bounded source
   template, not proximity, establishes the proposed link.
7. The metric span ends before the separating space. The scalar Evidence span
   remains exactly the existing anchor span.
8. Text after the scalar anchor, including an attested load phrase, is outside
   the candidate and cannot help establish the link.

`PROPOSED_RESEARCH_DECISION` — Requiring the literal seed surface rather than
a generated vocabulary is intentional. A future researcher may broaden the
template only by separately approving additional metric surfaces, morphology,
capitalization, whitespace, punctuation, or grammar.

`DEFERRED` — Copular forms such as `має бути`, lexical comparator templates,
adjectival qualifiers, arbitrary nominal phrases, parser-assisted noun-phrase
selection, coordination, and anaphora are not part of the smallest candidate.

`UNSUPPORTED_BY_AVAILABLE_SOURCES` — The sources do not justify treating every
noun phrase to the left of an anchor, the nearest noun phrase, or any phrase
whose unit looks plausible as a metric.

## 5. Metric Evidence and component representation

### 5.1 Exact positive-source spans

For the 49-code-point source string, the exact spans are:

| Role | Exact original text | Unicode code-point span `[start,end)` | Classification |
| --- | --- | --- | --- |
| Candidate metric Evidence | `Час відгуку` | `[0,11)` | `PROPOSED_RESEARCH_DECISION` |
| Existing scalar-anchor Evidence | `≤ 2 с` | `[12,17)` | `EXISTING_APPROVED` |
| Excluded context text | `при 500 одночасних користувачах` | `[18,49)` | `DEFERRED` |

`EXISTING_APPROVED` — Every boundary is zero-based, start-inclusive and
end-exclusive over Unicode code points in the trimmed original requirement.
For every accepted Evidence item, `requirement.text[start:end]` must equal the
stored Evidence text exactly. No normalized matching-view text may become
Evidence.

### 5.2 Why the full metric phrase is required

`SOURCE_ATTESTED_NOT_ALLOCATED` — The cited example presents the complete
two-word surface `Час відгуку` as its explicit metric expression.

`PROPOSED_RESEARCH_DECISION` — The candidate analysis treats `Час` as the
governing noun and `відгуку` as the genitive complement that identifies which
time is measured.

`PROPOSED_RESEARCH_DECISION` — The proposed metric Evidence is therefore the
complete phrase `[0,11)`, not governing noun `Час` `[0,3)`. Dropping the
complement would turn the attested response-time metric into an underspecified
generic time expression.

`DEFERRED` — This decision applies only to the exact phrase. It does not define
a generic method for deciding which complements are essential in other noun
phrases.

### 5.3 Component and top-level references

`EXISTING_APPROVED` — The existing bound Evidence remains unchanged, including
its `QUANT-001` rule identity and source-order ordinal. In this source it is
expected to remain `QUANT-001:E001` if it is the first `QUANT-001` anchor.

`PROPOSED_RESEARCH_DECISION` — A separately accepted metric Evidence item would
have an identifier owned by the researcher-approved metric-link rule. This
document denotes it as `<METRIC_EVIDENCE_ID>` only; that token is not a Rule ID
proposal or allocation.

The candidate positive observation would use:

```text
metric.evidence_refs     = (<METRIC_EVIDENCE_ID>,)
comparator.evidence_refs = (QUANT-001:E001,)
value.evidence_refs      = (QUANT-001:E001,)
unit.evidence_refs       = (QUANT-001:E001,)
context                  = None
unresolved_components    = ()
evidence_refs            = (<METRIC_EVIDENCE_ID>, QUANT-001:E001)
```

`PROPOSED_RESEARCH_DECISION` — The top-level order is metric Evidence first,
then bound Evidence, because that is the stable de-duplicated component union
ordered by `(start_offset, end_offset, evidence_id)`. Component refs do not
duplicate the scalar anchor, and the link is represented by both components
belonging to the same `QuantitativeConstraintObservation`.

`EXISTING_APPROVED` — The comparator remains
`LESS_THAN_OR_EQUAL / INCLUSIVE`, the exact value remains `Decimal("2")`, and
the unit remains `SECOND`. The proposal neither enlarges the anchor Evidence to
include the metric nor replaces original text with normalized values.

## 6. Exact metric-to-bound linkage proposal

`PROPOSED_RESEARCH_DECISION` — Link only when all of the following predicates
are true:

1. One existing `QUANT-001` symbolic anchor has already been accepted.
2. Its start offset immediately follows the exact sequence
   `Час відгуку<U+0020>` at requirement start.
3. The metric and anchor occupy the same hard-bounded clause.
4. No second eligible metric surface competes for that anchor.
5. No second scalar anchor competes for the metric inside the candidate
   construction.
6. The metric Evidence and existing anchor Evidence are disjoint and retain
   their exact original-source spans.

If all predicates hold, populate the existing observation's `metric` with a
`TextComponent` referring to the metric Evidence, preserve every scalar field
and ref, and rebuild only the top-level source-ordered Evidence union.

`PROPOSED_RESEARCH_DECISION` — This is a bounded left-operand source-template
relation. It is sufficient for the one attested symbolic construction without
claiming that adjacency, token distance, or character distance is generally a
grammatical relation.

`EXISTING_APPROVED` — A hard boundary prevents linkage. A comma is not, by
itself, permission to cross or attach. Distinct scalar anchors are never
merged.

`DEFERRED` — Any parser-assisted generalization must separately define its
allowed dependency/constituency relation, phrase boundary, essential
complements, exclusions, multiplicity, and failure behavior. Arbitrary parser
dependency selection is not a fallback.

## 7. Multiplicity and ambiguity matrix

| Situation | Candidate behavior | Observation consequence | Processing consequence | Classification |
| --- | --- | --- | --- | --- |
| Exactly one exact metric and one accepted symbolic bound satisfy §6 | Link them in one observation. | Metric populated; scalar fields and Evidence unchanged; no merge. | `COMPLETE` if no independent diagnostics exist. | `PROPOSED_RESEARCH_DECISION` |
| Two possible metrics for one bound | Do not choose by proximity or coordination order. The smallest exact template does not accept this shape. | Existing bound remains accepted. If a future approved candidate recognizer establishes both metric candidates, use `metric = None` plus unresolved `METRIC`; otherwise metric remains simply absent. | `INCOMPLETE` only under an approved ambiguity diagnostic; otherwise existing baseline status is preserved. | `DEFERRED` recognition; `PROPOSED_RESEARCH_DECISION` representation |
| One metric and two independent bounds | Do not duplicate the metric, choose a bound, or merge anchors. The smallest template excludes the shape. | Both accepted anchors remain separate and unchanged. Any shared-metric semantics remain unrepresented. | Existing baseline status is preserved unless a future approved ambiguity diagnostic applies. | `DEFERRED` |
| Metric and bound separated by `.`, `;`, `?`, or `!` | No cross-boundary link. | Bound keeps `metric = None` without unresolved `METRIC`; the out-of-clause text is not a candidate for that observation. | No metric-link diagnostic solely because text exists across the boundary. | `PROPOSED_RESEARCH_DECISION`, consistent with `EXISTING_APPROVED` boundary policy |
| Metric-like noun belongs to another syntactic role | Do not attach it merely because it precedes a duration or bound. | Existing anchor is preserved with no inferred metric. | No new metric-link result unless a separately approved grammar recognizes an actual candidate. | `PROPOSED_RESEARCH_DECISION` exclusion |
| Accepted quantitative anchor has no explicit metric | Preserve baseline behavior. | `metric = None`; `METRIC` absent from `unresolved_components`. | Existing family status is unchanged. | `EXISTING_APPROVED` |
| Load/count phrase follows the primary bound | Do not promote `користувачах`, `запитів`, their count, or a unit-like interpretation to the metric. | Primary metric candidate, if accepted, is only `Час відгуку`; context remains unpopulated in this slice. | The existing baseline independently handles any numeric candidate in the trailing phrase. | `EXISTING_APPROVED` non-inference; `DEFERRED` context role |

`UNSUPPORTED_BY_AVAILABLE_SOURCES` — No evidence supports a general rule that
one metric distributes over two bounds, two coordinated metrics share one
bound, or the closest metric-like phrase wins.

## 8. Partial-component and uncertainty decisions

| State | Required representation | Evidence/diagnostic treatment | Family outcome | Classification |
| --- | --- | --- | --- | --- |
| Accepted metric + accepted bound | Populate `metric`; preserve comparator/value/unit; no metric unresolved entry. | Accepted metric Evidence plus unchanged bound Evidence; top-level source-ordered union. | `DETECTED`; `COMPLETE` when no diagnostics exist. | `PROPOSED_RESEARCH_DECISION` |
| Accepted bound, no expressed metric | `metric = None`; `METRIC` absent from `unresolved_components`. | Bound Evidence only; no metric diagnostic. | Existing baseline outcome unchanged. | `EXISTING_APPROVED` |
| Accepted bound, explicit metric candidate, role or attachment unresolved | `metric = None`; include `METRIC` exactly once in `unresolved_components`. | Candidate text is diagnostic span, not accepted Evidence; bound Evidence remains accepted. | `DETECTED` plus `INCOMPLETE` only when the approved diagnostic is present. | `EXISTING_APPROVED` representation; `PROPOSED_RESEARCH_DECISION` trigger |

`EXISTING_APPROVED` — An unexpressed metric is not unresolved merely because
the baseline detector does not extract one. `None` without `METRIC` means
absent/unexpressed; `None` with `METRIC` means an explicitly expressed
candidate could not be resolved.

`PROPOSED_RESEARCH_DECISION` — An unresolved metric attachment should make the
quantitative family `INCOMPLETE` only when all three conditions hold:

1. an approved metric-candidate grammar recognizes explicit source text;
2. an existing accepted scalar observation is preserved; and
3. the approved linkage rule cannot determine one metric-to-one-bound
   attachment.

The outcome is then mixed: observations remain present, derived status remains
`DETECTED`, processing is `INCOMPLETE`, and at least one diagnostic is required
by the existing outcome invariant.

`PROPOSED_RESEARCH_DECISION` — The diagnostic candidate span should preserve
the full competing metric region that caused uncertainty. It must not become
Evidence and must not remove or rewrite the accepted scalar observation.

`DEFERRED` — The diagnostic code, exact explanation text, `rule_id`, whether one
diagnostic is emitted per competing attachment or per candidate region, and
how it cites multiple affected anchors are researcher decisions. No diagnostic
code is allocated here.

`EXISTING_APPROVED` — Deterministic exclusion under the exact template does not
make processing incomplete. In particular, a hard-boundary-separated phrase
is not an unresolved metric candidate for the later anchor.

## 9. Positive, negative and unresolved illustrative cases

Every row is `ILLUSTRATIVE_NOT_APPROVED`. It is a research prompt, not a
binding test, production output, or implementation authorization.

| Kind | Exact candidate text and relevant spans | Research interpretation | Source status |
| --- | --- | --- | --- |
| `ILLUSTRATIVE_NOT_APPROVED` — positive explicit metric | `Час відгуку ≤ 2 с при 500 одночасних користувачах`; metric `[0,11)`, bound `[12,17)`, excluded context `[18,49)` | Candidate link between the complete metric phrase and unchanged `QUANT-001` anchor. The trailing phrase has no role in establishing the link. | `SOURCE_ATTESTED_NOT_ALLOCATED` |
| `ILLUSTRATIVE_NOT_APPROVED` — no inferred metric from duration | `Система повинна завершити операцію за 2 с.`; fallback anchor `2 с` `[38,41)` | The accepted duration does not authorize invented metric text such as `час виконання`; `metric = None` without unresolved `METRIC`. | Synthetic |
| `ILLUSTRATIVE_NOT_APPROVED` — ambiguous multi-metric attachment | `Час відповіді та час обробки ≤ 2 с.`; candidates `[0,13)` and `[17,28)`, bound `[29,34)` | Do not choose the nearest phrase. If future grammar recognizes both candidates, preserve the bound and mark metric attachment unresolved. | Synthetic |
| `ILLUSTRATIVE_NOT_APPROVED` — one metric, two bounds | `Час відгуку ≤ 2 с та ≤ 3 с.`; metric `[0,11)`, bounds `[12,17)` and `[21,26)` | Preserve two independent anchors; do not merge, duplicate, or select. Shared-metric semantics are deferred. | Synthetic |
| `ILLUSTRATIVE_NOT_APPROVED` — hard-boundary separation | `Час відгуку. ≤ 2 с.`; metric-like phrase `[0,11)`, bound `[13,18)` | Full stop prevents linkage. The accepted bound has an unexpressed metric for this observation, not unresolved attachment. | Synthetic |
| `ILLUSTRATIVE_NOT_APPROVED` — metric-like noun in another role | `Система реєструє час відгуку та завершує операцію за 2 с.`; object phrase `[17,28)`, fallback anchor `[53,56)` | `час відгуку` is an object of another predicate and is not attached to the duration by proximity. | Synthetic |
| `ILLUSTRATIVE_NOT_APPROVED` — context/count not promoted | `Час відгуку ≤ 2 с при 500 одночасних користувачах`; count-bearing phrase `[18,49)` | `500` and `користувачах` do not become the metric. Baseline numeric diagnostics and future context research remain independent. | `SOURCE_ATTESTED_NOT_ALLOCATED` |
| `ILLUSTRATIVE_NOT_APPROVED` — accepted anchor with no metric | `не більше 2 секунд`; anchor `[0,18)` | Preserve the approved partial observation with `metric = None` and no unresolved `METRIC`. | Authoritative baseline example |
| `ILLUSTRATIVE_NOT_APPROVED` — technical versions preserved | `Дані передаються через TLS 1.3; доступ до API — за OAuth 2.0/OIDC;`; version spans `[27,30)` and `[57,60)` | `1.3` and `2.0` remain existing bounded negatives; metric linkage cannot turn them into values or anchors. | Source-attested excerpt |

`UNSUPPORTED_BY_AVAILABLE_SOURCES` — None of the synthetic cases supplies
scientific authorization. They exist only to make exclusion and uncertainty
questions reviewable.

## 10. Existing-domain sufficiency assessment

| Need | Existing representation | Assessment | Classification |
| --- | --- | --- | --- |
| Accepted explicit metric text | `TextComponent(evidence_refs=...)` | Sufficient; exact text remains in referenced `Evidence`. | `EXISTING_APPROVED` capability |
| Metric linked to scalar fields | Co-residence in one `QuantitativeConstraintObservation` | Sufficient for the one-metric/one-bound candidate; no attachment object is needed. | `PROPOSED_RESEARCH_DECISION` |
| Separate metric and bound spans | Component refs plus de-duplicated source-ordered top-level refs | Sufficient without enlarging existing bound Evidence. | `EXISTING_APPROVED` capability |
| Unexpressed versus unresolved metric | `None` plus presence/absence of `METRIC` in `unresolved_components` | Sufficient. | `EXISTING_APPROVED` |
| Mixed accepted-bound/ambiguous-metric outcome | Observation plus family diagnostic and `INCOMPLETE` processing | Structurally sufficient, but exact diagnostic semantics are not approved. | `EXISTING_APPROVED` capability; `PROPOSED_RESEARCH_DECISION` semantics |
| One candidate related to several anchors | No reusable attachment identity or structured multi-anchor diagnostic relation | Not needed for the smallest candidate; insufficient for a general attachment model. | `DEFERRED` |

`PROPOSED_RESEARCH_DECISION` — The existing domain is sufficient for the
smallest exact positive template and for preserving a bound with an unresolved
metric component. No domain class, comparator, unit, nested relation, or
reusable attachment model should be added for this slice.

`DEFERRED` — If later research requires structured identity between one metric
candidate and several observations, the current family diagnostic may not
preserve that graph explicitly. That broader representation question must be
decided before general coordination or compound attachment is implemented.

## 11. Proposed Rule-ID disposition

`EXISTING_APPROVED` — `QUANT-001` must retain its current scalar-anchor
semantics and Evidence boundary. The candidate metric link must not overwrite,
renumber, or enlarge `QUANT-001:E001` in the source example.

`PROPOSED_RESEARCH_DECISION` — Because metric recognition introduces a new
surface, a new Evidence span, and a new linkage decision, the conservative
disposition is to require a separately approved metric-link rule identity
rather than silently treating existing `QUANT-001` as authorization. The
researcher may instead approve reuse only after explicitly finding that stable
Rule-ID semantics and Evidence boundaries remain compatible.

`DEFERRED` — No concrete Rule ID, prefix, diagnostic code, or precedence slot is
allocated in this package. `<METRIC_EVIDENCE_ID>` is documentation notation
only.

`EXISTING_APPROVED` — Whatever disposition is chosen, the scalar anchor keeps
its existing rule identity. A metric-link rule composes with an accepted anchor;
it does not create a new scalar observation or a second copy of the anchor.

## 12. Researcher approval gates

No implementation is authorized until the researcher explicitly records all
of the following decisions in the authoritative model specification:

1. **Exact source-attested grammar** — approve, reject, or revise the literal
   `Час відгуку<U+0020><QUANT-001 symbolic anchor>` candidate, including start
   position, casing, whitespace, punctuation, and hard-boundary policy.
2. **Full metric phrase boundary** — approve `[0,11)` as the complete metric and
   confirm that `відгуку` is an essential complement for this template.
3. **Unique metric-to-bound relation** — approve the left-operand template and
   explicitly reject proximity and arbitrary parser arcs as fallbacks.
4. **Exclusions and ambiguity behavior** — approve the behavior for two
   metrics, two bounds, hard boundaries, other syntactic roles, trailing
   context/count phrases, and absent metrics.
5. **Exact Evidence and component refs** — approve separate metric and anchor
   Evidence, source round-trip, IDs, component refs, and top-level ordering.
6. **Partial observation and diagnostic semantics** — approve when `METRIC` is
   unresolved, the exact diagnostic code/span/explanation/rule identity, mixed
   `DETECTED` + `INCOMPLETE` behavior, and deterministic exclusions.
7. **Existing-domain sufficiency** — confirm that `TextComponent`,
   `unresolved_components`, and the existing family outcome suffice for the
   bounded slice.
8. **Rule-ID allocation or reuse** — allocate a new rule or explicitly approve
   reuse under the stable-ID policy. This package does neither.
9. **Later implementation authorization** — state separately whether any
   production detector, test, model-spec, or other implementation work may
   begin.

`EXISTING_APPROVED` — A separate acceptance gate would be required for any
future change to judgeability. Approval of the metric link alone must leave
`ACCEPT-QUANT-001` unchanged.

## 13. Smallest candidate for later model-spec approval

`PROPOSED_RESEARCH_DECISION` — The smallest candidate is one literal,
source-attested construction only:

```text
Source form:
  Час відгуку ≤ 2 с

Candidate reusable boundary:
  Час відгуку<U+0020><one existing QUANT-001 symbolic anchor>

Metric:
  exact full phrase Час відгуку

Relation:
  unique left operand immediately governing one accepted symbolic bound
  in the same hard-bounded clause

Representation:
  add one metric TextComponent and its separate exact Evidence reference
  to the existing scalar observation; preserve all scalar fields and refs

Exclusions:
  no lexical comparators, multiple metrics, multiple bounds, hard-boundary
  crossing, context/count attachment, inferred metrics, or parser fallback
```

`SOURCE_ATTESTED_NOT_ALLOCATED` — The seed form and its metric/bound roles are
supported by the cited dissertation passage and the model-spec traceability
example.

`PROPOSED_RESEARCH_DECISION` — Generalizing the numeric value and approved unit
inside an already-accepted `QUANT-001` anchor does not propose new scalar
syntax, but the researcher must still decide whether the source supports that
bounded reuse or whether approval should initially be restricted to the exact
`≤ 2 с` seed.

`DEFERRED` — All broader metric vocabulary and nominal-phrase grammar remain a
later research slice.

## 14. Open blockers and final status

The blockers to implementation are:

1. The exact literal template has not been approved as production grammar.
2. The complete metric boundary and essential-complement interpretation have
   not been approved.
3. The unique left-operand relation and its exclusions have not been approved.
4. Metric Evidence ownership and Rule-ID disposition remain undecided.
5. No metric-ambiguity diagnostic code, span, explanation, or emission
   cardinality is approved.
6. The family-processing consequence for an explicit unresolved metric remains
   a proposal, although the existing domain can represent it.
7. The researcher has not confirmed existing-domain sufficiency.
8. No later implementation has been authorized.

`SOURCE_ATTESTED_NOT_ALLOCATED` — The available sources do justify placing one
unambiguous bounded construction before the researcher: the exact
`Час відгуку` left operand attached to the existing `≤ 2 с` anchor. Therefore
this package does not conclude `NO_EXTENSION_READY` for metric linkage.

`PROPOSED_RESEARCH_DECISION` — The candidate is ready only for researcher
decision. It is not approved, implementable, or binding until every applicable
gate in §12 is closed in `model-spec.md`.

**Final status: `DRAFT_FOR_RESEARCHER_REVIEW`.**

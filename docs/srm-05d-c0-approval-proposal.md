# SRM-05D — Bounded C0 Scientific Approval Proposal

**Issue:** #73 (`SRM-05`)  
**Proposal scope:** one exact quantitative-context extension after the accepted
`QUANT-METRIC-001` prefix  
**Final proposal status:** `PROPOSED_FOR_RESEARCHER_APPROVAL`

This document asks the researcher to approve, revise, or reject one bounded
contract. It records no scientific approval, implementation authorization, or
production change. Every proposed decision below remains pending until the
researcher explicitly approves it.

## 1. Decision requested from the researcher

The proposed C0 decision is to recognize the exact suffix
`при 500 одночасних користувачах` as the measurement/load context under which
the already accepted response-time bound is evaluated in:

```text
Час відгуку ≤ 2 с при 500 одночасних користувачах
```

The suffix would populate `context` on the existing linked quantitative
observation. It would not be an independent count constraint, would not create
a second quantitative observation, and would not assign equality, a count
unit, or judgeability to `500`.

## 2. Source basis and protected baseline

The proposal is based on:

- `docs/srm-05d-quantitative-context-linkage.md`;
- `docs/model-spec.md` §§7.5–7.7, §§7.14.6.4–7.14.6.7, §7.15.10, and
  §18 `RQD-008`;
- `docs/srm-05c-implementation-acceptance-report.md`; and
- the current quantitative, condition-context, acceptance, domain,
  extraction, calculator, reporter, and aggregation contracts.

The protected baseline is `main` after merged PR #98, verified merge commit
`d0acbb072ccd1a12637e2966a4d2c91b1b5b7092`.

`EXISTING_APPROVED` — `QUANT-METRIC-001` remains
`RESEARCHER_APPROVED` and `IMPLEMENTED_AND_ACCEPTED`. Its exact metric grammar,
scalar linkage, Evidence boundaries, component references, observation count,
diagnostic preservation, exclusions, and downstream behavior are unchanged.
`RQD-008` remains `PARTIALLY_APPROVED / OPEN`, and issue #73 remains open.

The source-attested role distinction is:

| Role | Text | Span `[start,end)` | Status |
| --- | --- | --- | --- |
| Metric | `Час відгуку` | `[0,11)` | `EXISTING_APPROVED` under `QUANT-METRIC-001` |
| Scalar | `≤ 2 с` | `[12,17)` | `EXISTING_APPROVED` under `QUANT-001` |
| Measurement/load context | `при 500 одночасних користувачах` | `[18,49)` | `SOURCE_ATTESTED`; proposed for C0 |
| Embedded numeric candidate | `500` | `[22,25)` | Existing unresolved diagnostic candidate |

## 3. Exact proposed C0 grammar

The proposed grammar is:

```text
<exactly one already accepted QUANT-METRIC-001 observation>
<U+0020>при<U+0020>500<U+0020>одночасних<U+0020>користувачах
<trimmed Requirement.text end>
```

The line wrapping is editorial; the source construction is contiguous. C0
would require all of the following:

1. Exactly one already accepted `QUANT-METRIC-001` observation.
2. Exactly one approved symbolic `QUANT-001` duration anchor already linked to
   that metric.
3. Exactly one U+0020 SPACE between the accepted scalar anchor and the suffix.
4. The exact suffix `при 500 одночасних користувачах`.
5. Exact casing and exactly one U+0020 SPACE between suffix tokens.
6. The suffix ends at the end of trimmed `Requirement.text`.
7. No intervening punctuation, conjunction, parenthesis, or arbitrary text.
8. Metric, scalar, and suffix remain within the same hard-bounded segment; no
   attachment crosses `.`, `;`, `?`, or `!`.
9. No selection among competing metrics, bounds, or context candidates.
10. A failed C0 match is only a deterministic non-match. It does not by itself
    create an ambiguity diagnostic or unresolved `CONTEXT` component.

This is an exact source template, not a general Ukrainian `при` grammar, a
nearest-context rule, or parser-based attachment.

## 4. Proposed reuse of approved primary scalars

C0 proposes compositional reuse of every primary scalar variant already
accepted by `QUANT-METRIC-001`:

- ASCII integer values;
- single-decimal-comma values; and
- duration-unit surfaces `с`, `секунд`, `хв`, and `хвилин`.

This reuse would not extend or reparse the primary scalar grammar. The suffix
would remain exact, including the population count `500`. Alternative
ASCII-integer population counts belong to a later C1 decision. Decimal-comma
count syntax and all other primary-scalar numeric forms would not be inherited
for the population count.

## 5. Proposed context Evidence and component references

For the exact source example, C0 proposes one new Evidence item:

```text
evidence_id  = <NEW_CONTEXT_EVIDENCE_ID>
feature_id   = QUANTITATIVE_CONSTRAINT
text         = при 500 одночасних користувачах
span         = [18,49)
rule_id      = <FUTURE_APPROVED_QUANTITATIVE_CONTEXT_RULE_ID>
```

The Evidence would preserve the exact trimmed-source substring and would be
separate from the existing same-span `COND-UK-001:E001` Evidence. Shared source
span is allowed; shared cross-family Evidence identity is not.

The existing observation would gain:

```text
context = TextComponent(
    evidence_refs=(<NEW_CONTEXT_EVIDENCE_ID>,)
)

evidence_refs = (
    QUANT-METRIC-001:E001,
    QUANT-001:E001,
    <NEW_CONTEXT_EVIDENCE_ID>,
)
```

That tuple is the stable, de-duplicated, source-ordered component union. C0
would preserve the metric component, comparator, numeric value, duration unit,
every existing component reference, the existing scalar Evidence ID and span,
and the single scalar-observation count. It would add no nested relation and no
new domain type.

## 6. Proposed treatment of the embedded `500`

C0 proposes preserving the existing diagnostic exactly:

```text
code              = QUANT_UNRESOLVED_NUMERIC_CANDIDATE
rule_id           = QUANT-001
candidate span    = [22,25) "500"
processing status = INCOMPLETE
derived status    = DETECTED
```

The complete suffix would be recognized as the context of the response-time
bound. The embedded `500` would remain an unresolved numeric candidate under
the existing scalar detector. The diagnostic would remain diagnostic only: it
would not become accepted Evidence or a component reference.

This treatment does not prove that `500` must be an independent quantitative
constraint, and it does not mean that the entire context is unrecognized.
Suppressing, replacing, or reinterpreting the diagnostic requires a separate
future scientific approval.

## 7. Cross-family and acceptance compatibility

Any future implementation of an approved C0 contract would be required to
preserve:

- all `COND-UK-001/002` observations, Evidence, diagnostics, and processing;
- all `QUANT-001`, `QUANT-UK-001`, and `QUANT-METRIC-001` behavior;
- `ACCEPT-QUANT-001` judgeability;
- scalar-only acceptance containment;
- acceptance-criterion count, merge order, and deduplication;
- public extraction integrity and global Evidence ordering;
- Completeness, Verifiability, and Unambiguity calculations;
- Findings and `QUALITY_PROBLEM` behavior; and
- reporter and specification-aggregation behavior.

A future quantitative-context Evidence owner may be accepted by downstream
component-owner validation so the enriched observation remains valid. That
owner must not become another scalar attachment anchor. Only unchanged
`QUANT-001`/`QUANT-UK-001` scalar Evidence may continue to drive scalar
containment and attachment. Same-span condition and quantitative Evidence must
remain independently identifiable.

## 8. Proposed binding cases

The labels mean: `SOURCE_ATTESTED` is present in the audited research source;
`SYNTHETIC_TEST_CASE` is a constructed boundary case; `EXISTING_APPROVED`
identifies protected behavior; `DEFERRED` lies outside C0; and
`UNSUPPORTED_BY_AVAILABLE_SOURCES` has no audited scientific support. Every C0
disposition below is proposed, not approved. Unless stated otherwise, a
negative means only “emit no C0 context Evidence”; existing scalar and other
family behavior remains unchanged, and no new scalar diagnostic is asserted.

| Case | Representative input | Classification | Proposed C0 disposition |
| --- | --- | --- | --- |
| Exact positive | `Час відгуку ≤ 2 с при 500 одночасних користувачах` | `SOURCE_ATTESTED`; prefix `EXISTING_APPROVED` | Match; context `[18,49)`; preserve the `500` diagnostic. |
| Integer primary value | `Час відгуку ≤ 3 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE`; scalar variant `EXISTING_APPROVED` | Match. |
| Decimal-comma primary value | `Час відгуку ≤ 2,5 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE`; scalar variant `EXISTING_APPROVED` | Match. |
| Approved duration-unit variants | The exact suffix after `≤ 2 с`, `≤ 2 секунд`, `≤ 2 хв`, or `≤ 2 хвилин` | Composite strings `SYNTHETIC_TEST_CASE`; units `EXISTING_APPROVED` | Match each already accepted prefix. |
| Missing `500` | `Час відгуку ≤ 2 с при одночасних користувачах` | `SYNTHETIC_TEST_CASE` | No C0 match. |
| Changed `500` | `Час відгуку ≤ 2 с при 600 одночасних користувачах` | `SYNTHETIC_TEST_CASE`; alternative counts `DEFERRED` to C1 | No C0 match. |
| Missing population noun phrase | `Час відгуку ≤ 2 с при 500` | `SYNTHETIC_TEST_CASE` | No C0 match. |
| Changed population noun | `Час відгуку ≤ 2 с при 500 одночасних клієнтах` | `SYNTHETIC_TEST_CASE`; vocabulary expansion `DEFERRED` | No C0 match. |
| Changed marker | `Час відгуку ≤ 2 с за 500 одночасних користувачів` | `SYNTHETIC_TEST_CASE`; general marker grammar `DEFERRED` | No C0 match. |
| Changed casing | `Час відгуку ≤ 2 с При 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | No C0 match. |
| Changed spacing | Double space or TAB anywhere in or immediately before the suffix | `SYNTHETIC_TEST_CASE` | No C0 match. |
| Punctuation after suffix | `Час відгуку ≤ 2 с при 500 одночасних користувачах.` | `SYNTHETIC_TEST_CASE`; punctuation variant `DEFERRED` | No C0 match because the exact suffix is not at trimmed-text end. |
| Hard-boundary separation | `Час відгуку ≤ 2 с. при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE`; hard boundaries `EXISTING_APPROVED` | No cross-boundary C0 attachment. |
| Competing metric | `Час відгуку та Час відгуку ≤ 2 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE`; competition exclusion `EXISTING_APPROVED` | No C0 match; do not choose a metric. |
| Competing symbolic bound | `Час відгуку ≤ 2 с та ≤ 3 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE`; competition exclusion `EXISTING_APPROVED` | No C0 match; preserve baseline observations. |
| Competing lexical bound | `Час відгуку ≤ 2 с та не більше 3 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE`; scalar rules and competition exclusion `EXISTING_APPROVED` | No C0 match; preserve baseline observations. |
| Additional context phrase | `Час відгуку ≤ 2 с при 500 одночасних користувачах при піковому навантаженні` | `SYNTHETIC_TEST_CASE`; multiple-context attachment `DEFERRED` | No C0 match; do not select or merge contexts. |
| Lexical primary comparator | `Час відгуку не більше 2 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE`; `QUANT-UK-001` scalar behavior `EXISTING_APPROVED` | No C0 match because the required `QUANT-METRIC-001` prefix is absent. |
| Unsupported primary numeric form | `Час відгуку ≤ 2.5 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE`; form `UNSUPPORTED_BY_AVAILABLE_SOURCES` | No C0 match; preserve baseline detector behavior without asserting a new diagnostic. |
| Unsupported population numeric forms | Use `500,5`, `500.0`, `+500`, `1 000`, or `5e2` instead of `500` | `SYNTHETIC_TEST_CASE`; forms `UNSUPPORTED_BY_AVAILABLE_SOURCES` | No C0 match; do not inherit primary-scalar syntax. |
| Different source load grammar | `при навантаженні до 300 одночасних запитів` | `SOURCE_ATTESTED`; broader grammar and nested role `DEFERRED` | Outside C0. |
| Independent `= 500 users` interpretation | Reinterpret the source count as a separate bound | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; independent/nested count `DEFERRED` | Forbidden in C0. |
| Protected technical versions | `TLS 1.3`; `OAuth 2.0/OIDC` | `SOURCE_ATTESTED`; negative handling `EXISTING_APPROVED` | Preserve the existing no-observation/no-diagnostic treatment for those version numbers. |

## 9. Proposed Rule-ID disposition

`QUANT-CONTEXT-001` is a proposed candidate name for the future exact C0 rule.
It is not allocated, published, or researcher-approved by this document. A
Rule ID may be allocated only after the researcher approves its semantics,
grammar, Evidence boundary, diagnostics, and compatibility contract.

Existing IDs cannot own the new context Evidence:

- `QUANT-METRIC-001` has an immutable meaning and owns only the exact metric
  recognition/link and metric Evidence; adding context would materially change
  its semantics and Evidence boundary.
- `QUANT-001` owns the scalar anchor and unresolved numeric diagnostic; using it
  for the full context would conflate accepted scalar syntax with context
  attachment and alter protected Evidence provenance.
- `COND-UK-001` owns `CONDITION_CONTEXT` Evidence for a general feature family.
  A quantitative component must reference `QUANTITATIVE_CONSTRAINT` Evidence,
  so reusing its identity would violate family ownership and erase the
  semantic distinction between general condition and linked quantitative
  context.

## 10. Explicit exclusions

C0 would not approve:

- alternative population counts, including a variable ASCII-integer count;
- generic workload vocabulary or general Ukrainian context grammar;
- context ambiguity diagnostics;
- count-unit, bare-count comparator, equality, or judgeability semantics;
- independent or nested count observations;
- shared contexts or multiple-bound attachment;
- any new numeric grammar;
- parser-based context attachment;
- new acceptance criteria or changed acceptance containment;
- new C/V/U contributions or formulas;
- new Findings or `QUALITY_PROBLEM` conversions; or
- changes to reporting, aggregation, applicability, confidence, severity,
  risk, priority, or corrective actions.

## 11. Researcher approval checklist

Every item is pending explicit researcher decision:

- [ ] Approve or revise the suffix's semantic role as measurement/load context,
  not an independent count constraint.
- [ ] Approve or revise the exact C0 casing, U+0020 spacing, adjacency,
  requirement-end, uniqueness, and hard-boundary grammar.
- [ ] Approve or revise composition with all already accepted
  `QUANT-METRIC-001` primary scalar variants.
- [ ] Approve exact population count `500` and keep alternative counts outside
  C0.
- [ ] Approve separate `QUANTITATIVE_CONSTRAINT` Evidence ownership for
  `[18,49)`.
- [ ] Approve `context = TextComponent(...)` and the source-ordered
  metric/scalar/context reference union.
- [ ] Approve preservation of the `QUANT-001` diagnostic for `500` and the
  `INCOMPLETE / DETECTED` family result.
- [ ] Approve unchanged, independently owned `COND-UK-001/002` behavior.
- [ ] Approve unchanged `ACCEPT-QUANT-001` judgeability, scalar-only
  containment, count, and deduplication.
- [ ] Confirm that the existing domain is sufficient for context-only C0 and
  that no new type is required.
- [ ] Approve a future distinct Rule ID, potentially `QUANT-CONTEXT-001`, or
  select another name; no ID is allocated here.
- [ ] Confirm all C1, general grammar, ambiguity, count/nesting, numeric,
  parser, acceptance, scoring, finding, reporting, and aggregation boundaries
  remain deferred.

## 12. Final proposal status

The exact bounded C0 contract above is ready for an explicit researcher
decision. Nothing in this document records approval or authorizes
implementation. `RQD-008` remains `PARTIALLY_APPROVED / OPEN`, and issue #73
remains open.

**Final proposal status: `PROPOSED_FOR_RESEARCHER_APPROVAL`.**

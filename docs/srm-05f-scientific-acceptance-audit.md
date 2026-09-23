# SRM-05F — Final Scientific Acceptance Audit

**Audit date:** 2026-09-23  
**Audit result:** `PASS` — all 12 scientific acceptance gates pass  
**Authoritative contract audited:** `docs/model-spec.md`  
**Approved package:** `F1-A / M-A`  
**Scientific status:** `RESEARCHER_APPROVED`  
**Production status:** `NOT_IMPLEMENTED`  
**Rule ID:** `NOT_ALLOCATED`  
**New Evidence IDs:** `NOT_ALLOCATED`

## 1. Audit scope and sources

This audit verifies that the researcher-approved exact F1-A/M-A scientific
contract is completely and consistently recorded in the authoritative model
specification. It is a documentation-only acceptance audit. It does not approve
new science, authorize implementation, allocate identifiers, or change any
existing contract.

The following sources were reviewed:

- [`srm-05f-quantitative-boundaries-research.md`](srm-05f-quantitative-boundaries-research.md), as the historical research inventory and pre-approval question record;
- [`srm-05f-frequency-f1-approval-proposal.md`](srm-05f-frequency-f1-approval-proposal.md), as the historical approval proposal and decision-package record;
- [`model-spec.md`](model-spec.md), especially Sections 7.14.5.1,
  7.14.6.6-7.14.6.10, 7.14.12-7.14.13, 7.15.10, 7.15.12, 9, 12,
  and 18; and
- the model-spec contracts governing C0, exact R3, scalar precedence,
  Evidence ownership and ordering, `ACCEPT-QUANT-001`,
  `CALC-V-MVP-001`, reporter presentation, and `AGG-MVP-001`.

The research document and approval proposal are lifecycle records rather than
current implementation authority. Their pre-approval statuses were assessed
for historical consistency, not treated as defects in the later authoritative
approval record.

## 2. Gate-by-gate result

| Gate | Result | Audit finding and authoritative location |
|---|---|---|
| 1. Approval date and status | **PASS** | Model-spec Section 7.14.6.10 records researcher approval date `2026-09-23`, scientific status `RESEARCHER_APPROVED`, production status `NOT_IMPLEMENTED`, Rule ID `NOT_ALLOCATED`, and new Evidence IDs `NOT_ALLOCATED`. |
| 2. Approved option boundary | **PASS** | Section 7.14.6.10 records exactly `F1-A / M-A`. It explicitly does not approve F1-B or F2; Sections 7.14.6.10.8 and 18 retain F2 as `NOT_READY`. |
| 3. Exact positive envelopes | **PASS** | Section 7.14.6.10.1 preserves exactly the 90-code-point standalone clause and 178-code-point refined R1′ requirement as complete-input positives. The 206-code-point DOCX table cell and its `[0,28)` editorial prefix remain provenance only and are not a positive input. Literal length and slice validation reproduced 90, 178, and 206 code points. |
| 4. Metric-role confinement | **PASS** | Section 7.14.6.10.2 confines M-A to the exact coordinate-update phrase `[0,62)` when immediately linked to the exact frequency anchor `[63,90)`. It expressly rejects a reusable action-to-metric rule, new metric vocabulary, inferred noun-phrase grammar, and any broadening of `QUANT-METRIC-001`. Section 7.15.10 repeats this boundary. |
| 5. Frequency semantics | **PASS** | Sections 7.14.6.10.2 and 7.15.10 preserve `NOT_LESS_FREQUENT`, `inclusivity = None`, `Decimal("5")`, and `SECOND` as the source-stated recurrence interval. `одного разу на` remains fixed grammatical material. Duration-inequality conversion, numeric `1`, count units, rates, reciprocals, hertz, tolerances, and measurement/conformance algorithms are expressly excluded. |
| 6. Representation and Evidence | **PASS** | Sections 7.14.6.10.3-.4 and 7.15.10 approve one existing-shape ordinary `QuantitativeConstraintObservation`, with zero-or-one cardinality. Metric Evidence is `[0,62)`; frequency-anchor Evidence is `[63,90)`. Component references, common ownership, distinct future identities, round-trip slicing, de-duplicated source order, and the absence of component substrings are internally consistent. No identifier is allocated. |
| 7. Protected exclusion coexistence | **PASS** | Section 7.14.6.10.5 makes an exact F1-A positive supersede the protected exclusion only for `[63,90)`, while keeping nested `5 с` ineligible for fallback and emitting no F1 or numeric diagnostic. Every F1 non-match delegates to the unchanged protected exclusion and scalar baseline. Global scalar precedence remains lexical comparator, symbolic comparator, then value-plus-unit fallback. Exact refined R1′ preserves the independent `[164,177)` scalar and forbids cross-semicolon linkage. |
| 8. Acceptance invariant | **PASS** | Sections 7.14.5.1 and 7.14.6.10.6 agree that `ACCEPT-QUANT-001` requires scalar Evidence owned by `QUANT-001` or `QUANT-UK-001`. Future F1-owned Evidence is ineligible, and `NOT_LESS_FREQUENT / None` is not independently judgeable. F1 creates no acceptance Evidence, observation, or diagnostic and does not alter containment, cardinality, deduplication, or mixed-outcome rules. |
| 9. Verifiability consequence | **PASS** | Sections 7.14.6.10.7 and 9 explicitly approve consumption of the ordinary F1-A observation by `CALC-V-MVP-001`. Holding the documented other-detector outcomes fixed, the 90-code-point input changes `V_i` from `0` to `1/2`; the 178-code-point input remains `1/2` after adding a second lower-tier observation. Both sections preserve acceptance precedence and material-dependency withholding, disclose possible reporter and `AGG-MVP-001` mean changes, and state that unchanged formulas do not guarantee unchanged outputs. |
| 10. Protected contracts | **PASS** | Sections 7.14.6.10.4-.8 preserve `QUANT-001`, `QUANT-UK-001`, `QUANT-METRIC-001`, `QUANT-CONTEXT-001`, exact C0 and its `500` diagnostic, scalar precedence, exact R3, condition/result detection, acceptance, C/U inputs and formulas, Findings, `QUALITY_PROBLEM`, reporter rules, and aggregation formulas. Cross-checks against the C0, R3, acceptance, Section 9, and Section 12 contracts found no incompatible statement. |
| 11. Lifecycle and open status | **PASS** | Sections 7.14.6.10.8, 7.14.12, 7.15.12, and 18 consistently retain F1-A and R3 as `RESEARCHER_APPROVED / NOT_IMPLEMENTED / RULE_ID_NOT_ALLOCATED`; all new Evidence IDs remain unallocated. RQD-008 remains `PARTIALLY_APPROVED / OPEN`, SRM-05 issue #73 remains `OPEN`, and F2 remains `NOT_READY`. |
| 12. Model-spec-wide status consistency | **PASS** | The document status, feature registry, quantitative traceability cases, scalar allocation, rule-ID registry/readiness text, representation section, Verifiability section, RQD-008 rows, and remaining-blocker text consistently distinguish scientific approval from production implementation. No contradictory or stale normative statement was found. Pre-approval text in the research and proposal documents is historical and does not conflict with the later authoritative model-spec record. |

**Gate total:** `12 PASS / 0 FAIL`.

Because no gate failed, there is no minimum corrective edit to identify and no
change to `model-spec.md` is required by this audit.

## 3. Exact source and representation summary

### 3.1 Positive input envelopes

The approved 90-code-point complete input is:

```text
координати активного транспортного засобу повинні оновлюватися не рідше одного разу на 5 с
```

The approved 178-code-point complete input is:

```text
координати активного транспортного засобу повинні оновлюватися не рідше одного разу на 5 с; 95-й перцентиль затримки від отримання GPS-події до відображення в UI — не більше 3 с.
```

The original 206-code-point table cell begins with the editorial prefix
`Замість «у реальному часі»: ` at `[0,28)`. It is provenance only. F1-A does
not strip the prefix or search for a nested clause.

The verified refined-input boundaries are:

| Role | Span | Exact content or consequence |
|---|---|---|
| F1 clause | `[0,90)` | Complete coordinate-update frequency clause |
| M-A metric referent | `[0,62)` | `координати активного транспортного засобу повинні оновлюватися` |
| Separator space | `[62,63)` | U+0020; not separate Evidence |
| Frequency anchor | `[63,90)` | `не рідше одного разу на 5 с` |
| Semicolon | `[90,91)` | Hard boundary outside F1 Evidence |
| Following space | `[91,92)` | U+0020 outside F1 Evidence |
| Percentile phrase | `[92,161)` | Outside F1 and not reinterpreted as frequency |
| Existing scalar | `[164,177)` | Independent `не більше 3 с` observation |
| Final period | `[177,178)` | Outside F1 Evidence |

Recognition is complete-input literal equality. No substring, clause-search,
prefix/suffix, case, whitespace, Unicode normalization, morphology, token,
lemma, parser, synonym, paraphrase, or proximity generalization is approved.

### 3.2 Approved semantics

| Component | Approved value | Boundary |
|---|---|---|
| `metric` | Exact M-A coordinate-update referent | `[0,62)` and only within the exact F1 relationship |
| `comparator.label` | `NOT_LESS_FREQUENT` | Exact source relation only |
| `comparator.inclusivity` | `None` | Not an endpoint-inclusion decision |
| `value.decimal_value` | `Decimal("5")` | Source-stated interval parameter, not measured frequency |
| `unit.label` | `SECOND` | Exact source surface `с`; no conversion |
| Fixed grammar | `одного разу на` | Preserved within anchor Evidence; no numeric/count component |
| `context` | `None` | No context component is approved |
| `unresolved_components` | `()` | No unresolved component is created by an exact positive |

### 3.3 Observation and Evidence contract

An exact positive creates one ordinary accepted
`QuantitativeConstraintObservation` in
`RequirementFeatures.quantitative_constraints`, with exactly these component
references:

- `metric` references only the future-owned Evidence at `[0,62)`;
- `comparator`, `value`, and `unit` reference only the future-owned Evidence at
  `[63,90)`; and
- top-level `evidence_refs` is the stable, de-duplicated, source-ordered tuple
  containing the `[0,62)` reference followed by the `[63,90)` reference.

The two Evidence items belong to feature family
`QUANTITATIVE_CONSTRAINT`, the same requirement, and the same future F1 rule.
They have distinct future identities and rule-local source-order ordinals and
must round-trip to the exact trimmed source slices. The producing Rule ID and
both Evidence IDs remain `NOT_ALLOCATED`; the placeholder names in the model
specification are explanatory only.

Cardinality is zero or one F1-A observation per requirement. For exact refined
R1′, the F1-A observation is ordered before the unchanged `QUANT-UK-001`
observation at `[164,177)`; the observations do not share or merge Evidence.

## 4. Verifiability consequence summary

F1-A is deliberately an ordinary quantitative observation. Existing
`CALC-V-MVP-001` therefore consumes it as lower-tier Verifiability evidence.
This is an approved semantic consequence, not an accidental implementation
effect.

| Exact input | Current documented class | Class after implemented F1-A, holding other detector outcomes fixed |
|---|---|---|
| 90-code-point standalone clause | `V_i = 0` | `V_i = 1/2` |
| 178-code-point refined R1′ | `V_i = 1/2`, already supported by `не більше 3 с` | `V_i = 1/2`; the second lower-tier observation does not increase the class |

These results are conditional. An accepted acceptance criterion still yields
`V_i = 1`, and a material unresolved acceptance candidate can still withhold
the result as `UNKNOWN`. Other unresolved lower-tier candidates continue to
follow the existing numeric-class change test.

For the standalone case, the requirement remains `COMPUTED`; its
`AGG-MVP-001` denominator membership therefore remains unchanged, while its
contribution changes from `0` to `1/2`. This can change the exact specification
Verifiability mean and the displayed requirement and aggregate values. The
calculator, reporter, and aggregation formulas remain unchanged; the outputs
can change because the accepted quantitative input set changes.

F1-A does not directly change Completeness or Unambiguity inputs and creates no
Finding or `QUALITY_PROBLEM`.

## 5. Historical-status observations

The research document is intentionally marked
`RESEARCH_ONLY / PROPOSED_FOR_RESEARCHER_REVIEW` and states that it records no
F1 approval. It inventories the source construction and identifies the then-open
scientific questions. This status accurately describes that document's point in
the lifecycle.

The approval proposal is intentionally marked
`PROPOSED_FOR_RESEARCHER_REVIEW`, states that it selects neither F1-A nor F1-B,
and retains unchecked researcher-action items. It is the pre-decision proposal,
not the post-decision authority. Its alternatives and downstream disclosure
match the subsequently selected F1-A/M-A package.

Model-spec Section 7.14.6.10 explicitly identifies the proposal as the
historical decision record and itself as the authoritative implementation-model
statement of the approved science. The model-spec current-status statements
supersede the proposal's pre-approval lifecycle status without rewriting
history. No historical-status defect exists.

## 6. Blocking defects

No scientific acceptance defect was found. No gate requires correction to
`model-spec.md`.

The following are intentional implementation and lifecycle blockers, not
scientific-record defects:

1. no production implementation is authorized for F1-A or R3;
2. the final F1-A and R3 Rule IDs remain unallocated;
3. all new F1-A and R3 Evidence IDs remain unallocated;
4. a separately authorized implementation contract, fixtures, technical audit,
   and later implementation acceptance are still required;
5. F2 remains `NOT_READY` and requires new evidence and a separate complete
   scientific contract;
6. broader frequency, count, unit, written-number, range, metric, context,
   ambiguity, and nested-role grammar remains open; and
7. RQD-008 remains `PARTIALLY_APPROVED / OPEN`, while SRM-05 issue #73 remains
   `OPEN`.

## 7. Final scientific acceptance conclusion

The authoritative model specification completely and consistently records the
researcher-approved exact F1-A/M-A scientific contract dated 2026-09-23.
All 12 audit gates pass, with no blocking scientific defect and no stale
normative contradiction.

The approval is confined to the two exact complete-input envelopes, the exact
M-A metric referent and frequency anchor, the existing-shape ordinary
quantitative observation, its two future-owned Evidence spans, and the
explicitly accepted `CALC-V-MVP-001` consequences. It does not approve F1-B,
F2, generalized frequency recognition, generalized action-to-metric inference,
or any new acceptance semantics.

The exact F1-A/M-A scientific record is therefore **accepted as complete and
internally consistent**, while production work remains blocked by the lifecycle
boundary below.

## 8. Implementation and lifecycle boundary

This audit creates documentation only. It does not:

- implement F1-A or R3;
- allocate a Rule ID, Evidence ID, diagnostic ID, type name, or field name;
- modify `model-spec.md`, either historical SRM-05F document, production code,
  or tests;
- alter `QUANT-001`, `QUANT-UK-001`, `QUANT-METRIC-001`,
  `QUANT-CONTEXT-001`, C0, exact R3, `ACCEPT-QUANT-001`, scalar precedence,
  condition/result detection, C/V/U formulas, Findings, `QUALITY_PROBLEM`,
  reporter behavior, or aggregation formulas;
- approve F1-B, F2, a positive variable-value/unit frequency family, a generic
  relationship framework, or broader numeric/unit grammar;
- close RQD-008 or SRM-05 issue #73; or
- create a baseline, tag, release, branch, commit, push, or pull request.

Any production implementation requires a separate authorized task and must be
audited against the exact accepted contract without revising its science by
implementation convenience.

# SRM-03 — Extended structural feature detection rules

**Status: PARTIALLY_APPROVED_FOR_SRM04_FIRST_SLICE.** The researcher has
approved decisions D01, D02, D04, D06, D07, and D08 as one bounded package,
allocating exactly `COND-UK-002`, `RESULT-UK-002`, and `ACCEPT-UK-001` for
SRM-04. The authoritative approval and complete executable contract are
recorded in [model-spec.md §7.14.16](model-spec.md#71416-srm-03-bounded-structural-rule-approval).
`RESULT-UK-003` remains `RESEARCH_BLOCKED`; `VERIFY-UK-002`,
`ATTACH-UK-001`, and singularity assessment remain `DEFERRED`. This approval
does not implement or otherwise change current MVP v0.1 behavior.

## 1. Purpose and scientific boundary

The target is **one Ukrainian-language sentence representing one requirement**.
Its clauses, conditions, actions, expected results, criteria and method phrases
remain inside one `Requirement`. The frozen reader continues to treat each
trimmed, non-empty UTF-8 input line as one requirement, even if the line has
several grammatical sentences. SRM-03 proposes no sentence rejection or
requirement splitting.

The scope is structural observations in the existing `condition_context`,
`expected_result`, `acceptance_criterion` and `verification_method` families,
plus the relationships needed to interpret several clauses in one requirement.
The existing `quantitative_constraint` and `vague_term_occurrence` families are
unchanged. Complex numeric grammar belongs to SRM-05/06; linguistic ambiguity
to SRM-07/08; type-specific applicability and characteristic calculations to
SRM-09/10/11. No new score, defect conversion, risk calculation, corrective
action or reassessment rule is proposed here.

Throughout this document, **source-supported principle** means that a cited
dissertation passage motivates the observation. A rule's explicit status says
whether its deterministic specialization is approved, blocked, or deferred;
the dissertation does not itself approve Ukrainian grammar. **Unresolved**
identifies a decision that cannot be filled by parser output or implementation
judgment.

## 2. Source traceability and existing MVP baseline

Sources were read in the requested order. [SRM-02](srm-02-individual-requirement-model.md)
is the current researcher-approved *local scope*, especially T01–T04, T07,
T13, G01 and `RQD-006`. [model-spec.md](model-spec.md) remains the authority
for *executable MVP behavior*, especially §§7.2–7.5, 7.7, 7.9, 7.11,
7.14.2–7.14.7, 7.15.6–7.15.8 and 7.16. The dissertation excerpts are
scientific context, not executable grammar:

| Local source | Relevant support and limit |
| --- | --- |
| [§2.1](reference/2.1_Властивості_вимог.docx), Table 2.1 (Completeness, Singularity, Verifiability rows), ¶11–12, Table 2.3 | A local requirement can need condition, expected reaction and fulfilment criterion; verifiability may use a criterion, oracle, analysis or inspection method. Independent obligations matter to singularity. The table does not define Ukrainian clause segmentation or a singularity detector. |
| [§2.3](reference/2.3_Система_метрик.docx), ¶4–6, Table 2.7, ¶17–21, ¶39–42 | Separates primary observations from measures and indicators; requires reproducibility, applicability and source context; permits nonnumeric operationalized results. It supplies no exact extended syntax, attachment algorithm or per-requirement score. |
| [§3.1](reference/3.1_Статичні_методи.docx), Table 3.1, ¶9–13, ¶32–34 | Supports static textual/structural analysis and traceable observations; external artifact or expert evidence is needed for some conclusions. Its set/product indicators and defect records are not local detector rules. |
| [§3.3](reference/3.3_Метод_оцінювання.docx), ¶10–11, ¶17–19, ¶30–36 | Supports source provenance, separate missingness and explainability; it does not supply Ukrainian grammar, local C/V/U formulas or a structural relation data type. |
| [§3.2](reference/3.2_Динамічні_методи.docx), ¶5–10, Table 3.4 | Used narrowly for the requirement → criterion → verification-procedure distinction. Test execution and product observations are outside this task. |
| [Worked application](reference/Приклад_застосування_моделі.docx), §8 Table 7, R5′ | Illustrates several condition/result clauses in one source requirement. Its illustrative text does not make inherited normative force or attachment executable. |

The local excerpts of Chapters 2–3 and the worked application are available.
The complete dissertation and Chapter 1 are not in `docs/reference/`, as
already recorded in SRM-02. The body of [Issue #71](https://github.com/rKiselyk/requirements-quality-assessment/issues/71)
could not be retrieved in this environment; the supplied SRM-03 request is the
issue scope used here. No claim below depends on unseen issue or dissertation
text.

**Existing approved MVP behavior (unchanged):** the six `RequirementFeatures`
collections are `condition_contexts`, `expected_results`,
`acceptance_criteria`, `quantitative_constraints`, `verification_methods`, and
`vague_term_occurrences`. `COND-UK-001` accepts its five exact marker surfaces
only in its leading/postposed templates. `RESULT-UK-001` accepts its five
normative surfaces only with the approved parser-assisted single-result grammar.
`ACCEPT-QUANT-001` composes an accepted result with contained, judgeable
`QUANT-001`/`QUANT-UK-001` Evidence. `VERIFY-UK-001` recognizes its three
specified verification-role constructions. These IDs retain their meanings;
none is renamed or widened here. The directly related detector modules and
tests are `condition_context.py`, `expected_result.py`,
`acceptance_criterion.py`, `verification_method.py` and their corresponding
`tests/test_*_detector.py` files. They confirm the narrow boundaries, including
mixed accepted/unresolved processing and source-offset round trips.

## 3. Structural gap inventory

| Area | Supported need | MVP boundary / decision missing |
| --- | --- | --- |
| A. Conditions and contexts | Several explicit conditions can govern one or several behaviors (§2.1 Table 2.1; worked R5′). | `COND-UK-001` does not resolve general internal/postposed subordinate clauses, nested or coordinated scope. No new marker inventory is justified here. |
| B. Expected results | Observable coordinated and nonmodal clauses occur in worked R5′; §2.1 requires an expected reaction. | `RESULT-UK-001` requires a supported modal and one determinate result scope. Inherited normative force and independent coordinated predicates are unresolved. |
| C. Nonnumeric criteria | §2.1 Table 2.1 and §3.2 Table 3.4 permit an expected behavior/oracle without a numeric threshold. | `ACCEPT-QUANT-001` only recognizes linked quantitative criteria; the exact test of nonnumeric judgeability is absent. |
| D. Verification methods | §2.1 Table 2.1 and §2.3 ¶17–21 distinguish reproducible methods from observable criteria. | `VERIFY-UK-001` has only three role constructions. Additional exact Ukrainian surface and role rules need approval; a method word is insufficient. |
| E. Multiple clauses | The six-family representation allows multiple observations; §2.1 singularity concerns independent obligations. | There is no approved rule to decide when coordinated material is one versus several observations or an independent-obligation finding. |
| F. Attachment | Conditions, criteria and methods need traceable targets (§2.1 Table 2.1; §3.2 ¶5–7). | MVP only has narrow condition anchor and quantitative Evidence containment. No general relation object or cross-clause attachment procedure is approved. |
| G. Actor/action/object | §2.1 describes expected behavior and possible independent actions. | Model-spec §7.11 explicitly defers `has_actor`, `has_action`, `has_object`. Parser annotations alone do not justify a new family. |

## 4. Rule registry and dispositions

Exactly three IDs below are now allocated for the bounded SRM-04 first slice.
The other three remain blocked or deferred and are not production allocations.
The approved rule-ID policy in model-spec §7.7 and the authoritative contracts
in model-spec §7.14.16 apply. Scientific approval authorizes SRM-04 to implement
the exact bounded rules; it is not itself an implementation.

| Candidate rule | First-slice disposition | Scientific reason |
| --- | --- | --- |
| `COND-UK-002` | `APPROVED_FOR_SRM04_FIRST_SLICE` | The bounded comma-delimited postposed `якщо` template in §4.1 requires an explicit finite verbal condition, one MVP-compatible governing result, and a complete neutral relation, suffix-projection, Evidence and diagnostic contract. It needs no general attachment engine. |
| `RESULT-UK-002` | `APPROVED_FOR_SRM04_FIRST_SLICE` | The binary active-infinitive `і`/`та` construction in §4.2 has a closed syntax and selects multiple exact Evidence references for inherited normative scope. |
| `RESULT-UK-003` | `RESEARCH_BLOCKED` | The sources show nonmodal examples but provide no textual fact that distinguishes normative present tense from description. Parser syntax, source position and neighboring clauses cannot supply that force. |
| `ACCEPT-UK-001` | `APPROVED_FOR_SRM04_FIRST_SLICE` | The exact-output subset in §4.4 requires a non-empty Ukrainian guillemet literal inside an accepted `RESULT-UK-001` result **and** an accepted leading `COND-UK-001` condition that governs that result through the exact approved source partition. This follows model-spec §7.14.5 and does not generalize unconditional observable results into criteria. |
| `VERIFY-UK-002` | `DEFERRED_FROM_FIRST_SRM04_SLICE` | No additional source-attested verification-role construction is sufficiently specified beyond `VERIFY-UK-001`; the concept remains valid, but the synthetic `підтверджується` construction has no dissertation authority. |
| `ATTACH-UK-001` | `DEFERRED_FROM_FIRST_SRM04_SLICE` | The approved first-slice rules establish bounded local relations internally. A reusable cross-observation relationship has no approved consumer or domain representation yet and is unnecessary for the first slice. |

Shared mechanics for the three approved first-slice rules are: operate on one original
trimmed `Requirement.text`; use only source-aligned parser-neutral annotations;
use zero-based Unicode code-point `[start_offset,end_offset)` spans; exclude
surrounding whitespace and sentence-final punctuation; preserve every exact
accepted span; allocate Evidence IDs independently per rule; and use the
model-spec §7.15.7 mixed-state derivation. The rule-specific sections close
their syntax, precedence, overlap, ordering and failure behavior. No rule below
uses nearest text, nearest clause or an undefined semantic classifier.

Three layers are kept distinct throughout this registry:

1. the **scientific rule** states the source construction and the structural
   relation that must be established before an observation is accepted;
2. the **parser-neutral contract** names only `TokenAnnotation` fields and
   UD-compatible values needed to evaluate that rule; and
3. the **selected-backend check** records what the pinned spaCy 3.8.16 /
   `uk_core_news_sm` 3.8.0 pipeline actually emitted in a temporary read-only
   probe of P01, P03, P07 and P21 during these corrections.

That probe is implementation evidence, not scientific authority or a parser
accuracy claim. SRM-04 must turn each observed graph into a direct pinned-backend
fixture and retain parser-blocked behavior when any required neutral annotation
is missing or changes. No detector may manufacture or repair an arc.

### 4.1 `COND-UK-002` — bounded postposed `якщо` condition

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Preserve explicit governing conditions in a multi-clause requirement without assigning them to the wrong result. |
| 2. Exact source | §2.1 Table 2.1, Completeness and Singularity rows; worked application §8 Table 7 R5′; model-spec §7.14.3 general-family discussion. |
| 3. MVP limitation | `COND-UK-001` covers only its edge templates and does not resolve internal/postposed `якщо`, nested or coordinated attachment. |
| 4. Feature / Feature ID | Existing `condition_contexts[]` / `condition_context`; no new family. |
| 5. Rule ID | `COND-UK-002` (allocated for the bounded contract; `COND-UK-001` unchanged). |
| 6. Ukrainian construction | Exactly one binary source structure in one parser sentence and semicolon segment: `<one governing result>, <якщо-clause>`. The comma is mandatory. `якщо` is the only marker, matched as a complete token on the approved NFC plus Unicode `casefold()` view. No synonym, morphology generation or other marker is admitted. |
| 7. Parser annotations | Existing `SentenceAnnotation` and `TokenAnnotation` offsets, `lemma`, `upos`, morphology, `head_token_id`, and `dependency_relation`. The condition head must be `VERB` with `VerbForm=Fin`; the `якщо` token must have `dependency_relation=mark` and `head_token_id` equal to that condition head. The condition head must have `dependency_relation=advcl` and `head_token_id` equal to the governing prefix's normative predicate-chain head; that head must be connected to the one lexical behavior infinitive through the accepted `RESULT-UK-001` chain. All referenced heads must be in the same sentence/segment. The selected backend emitted exactly this graph for P01: `якщо → відповідає` (`mark`), `відповідає → повинна` (`advcl`, `VerbForm=Fin`), `зберегти → повинна` (`xcomp`), and `Система → повинна` (`nsubj`). |
| 8. Deterministic recognition procedure | (1) Find exactly one comma followed only by whitespace and complete-token `якщо`. (2) Let the trimmed prefix before the comma be the governing-result interval and the suffix from `якщо` to the segment end be the condition interval. (3) Apply the normative subject/predicate requirements of `RESULT-UK-001` to the prefix interval, at absolute offsets, without invoking condition separation; require exactly one local subject, one approved normative surface, one connected lexical behavior predicate, no coordination and no negation. (4) Require the finite-head, `mark` and `advcl` head identities from item 7; the `advcl` target is the accepted prefix's normative predicate-chain head, not an arbitrary nearby token. (5) Project the condition-head subtree onto the condition interval: every token in the trimmed suffix must be the condition head or its descendant, their source projection must equal the whole suffix, and no nonpunctuation descendant may lie outside it. The mandatory delimiter comma immediately before the suffix is excluded from this projection because the selected backend attaches that punctuation token to the condition head. Only then accept. This bounded local relation is part of the rule; `ATTACH-UK-001` is not called or stored. |
| 9. Evidence / offsets | One independent `Evidence` with `feature_id=CONDITION_CONTEXT`, `rule_id=COND-UK-002`, and the exact suffix from `якщо` through the last condition character, excluding terminal sentence punctuation. For the binding example it is `[32,57)` `якщо сервіс не відповідає`. The governing result is not copied into condition Evidence. |
| 10. Attachment semantics | The required `advcl` edge locally establishes one condition → one result relationship for recognition only. It is not exported as a general relation. More than one result predicate, condition head, `якщо` marker or plausible governing predicate prevents acceptance. |
| 11. Positive example | `Система повинна зберегти запит, якщо сервіс не відповідає.` has governing prefix `[0,30)` and accepted condition `[32,57)`. It yields one `condition_context` observation referencing `COND-UK-002:E001`. The condition has the explicit finite verbal head `відповідає`; the zero-copula/adjectival form `якщо сервіс недоступний` is not accepted by this rule. |
| 12. Negative example | `Система повинна показати слово «якщо» у довідці.` → the quoted word is no condition. |
| 13. False-positive boundary | `якщо` inside a matched `«…»` source interval is a completed negative, not a candidate. Other quoted/mentioned uses fail the required `mark`/`advcl` relations. No comma, more than one possible result, a coordinated/nested condition, an incomplete suffix projection, a nonpunctuation condition descendant outside the suffix, or a second condition marker is outside the accepted subset. No proximity rule is used. |
| 14. UNRESOLVED behavior | A source-shaped `,<space>якщо` candidate that lacks the required explicit finite verbal head or fails unique result, suffix projection, `mark`/`advcl`, nesting or coordination checks produces `COND_POSTPOSED_YAKSHCHO_UNRESOLVED`, the complete exact suffix as `DiagnosticSpan` when its boundary is known, no observation and `INCOMPLETE`. Thus postposed `, якщо сервіс недоступний` is preserved as an unsupported zero-copula candidate, never accepted as finite. Parser unavailability/failure/incomplete annotations/offset failure produces `COND_POSTPOSED_YAKSHCHO_PARSER_BLOCKED`, no Evidence and `INCOMPLETE`. With no source-shaped candidate, the rule is `COMPLETE` with no contribution. |
| 15. Applicability | Detect explicit text only; criterion applicability remains `UNKNOWN` unless an independent approved rule states otherwise. |
| 16. Known limitations | Only one comma-delimited postposed `якщо` clause with one explicit finite verbal head and one simple normative result is covered. Leading `якщо` remains `COND-UK-001`; zero-copula/adjectival predicates, multiple, nested, coordinated and nonmodal structures remain outside this rule. A future zero-copula proposal must define its own representation, recognition and cases. |
| 17. Dependencies and interaction | Proposed dispatch checks this exact postposed form before `COND-UK-001`. An accepted or unresolved `COND-UK-002` candidate owns only that marker span, preventing the old `COND-UK-001` postposed-`якщо` diagnostic from duplicating it. Other markers and segments remain governed unchanged by `COND-UK-001`. Evidence IDs are `COND-UK-002:E001…` in accepted source order; identical `(feature_id,start,end)` output from the same rule is collapsed. No domain change and no `ATTACH-UK-001` dependency. |
| 18. Scientific approval | `APPROVED_FOR_SRM04_FIRST_SLICE` through D01 and D08, with D06-D07's no-attachment/no-domain-change boundary; authoritative contract in model-spec §7.14.16.2. |

### 4.2 `RESULT-UK-002` — coordinated results with explicit normative scope

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Preserve each separately observable result when one explicit normative construction governs coordinated predicates. |
| 2. Exact source | §2.1 Table 2.1, Completeness and Singularity rows; model-spec §7.14.4 family-level statement that each independent coordinated result is a separate observation. |
| 3. MVP limitation | `RESULT-UK-001` leaves coordinated predicate/`conj` scope unresolved. |
| 4. Feature / Feature ID | Existing `expected_results[]` / `expected_result`. |
| 5. Rule ID | `RESULT-UK-002` (allocated for this bounded binary construction). |
| 6. Ukrainian construction | One parser sentence/semicolon segment of exact source shape `<explicit local subject> <one approved normative surface> <first active infinitive phrase> <і\|та> <second active infinitive phrase>`. Approved normative surfaces are exactly `повинен`, `повинна`, `повинні`, `має`, `мають`. Exactly two lexical predicates and one coordinator are allowed. A leading/postposed condition, comma, colon, dash or internal hard boundary is excluded from this first subset. |
| 7. Parser annotations | Existing parser-neutral offsets, `lemma`, `upos`, morphology, heads and UD-compatible relations. The first predicate must be `VERB` with `VerbForm=Inf` and connected to the normative construction through the `RESULT-UK-001` `xcomp`/`ccomp`/`aux`/`cop` chain. The second must be `VERB`, `VerbForm=Inf`, `dependency_relation=conj`, and `head_token_id` equal to the first predicate. The exact source coordinator token is `і` or `та`, has `dependency_relation=cc`, and `head_token_id` equal to the second predicate. One `nsubj`/`nsubj:*` belongs to the governing clause; no second local subject is allowed. The selected backend emitted that exact P03 graph: `Система → повинна` (`nsubj`), `зберегти → повинна` (`xcomp`, `VerbForm=Inf`), `повідомити → зберегти` (`conj`, `VerbForm=Inf`) and `і → повідомити` (`cc`). |
| 8. Deterministic recognition procedure | (1) Segment exactly as `RESULT-UK-001`. (2) Require one normative surface and one local subject. (3) Require exactly the two infinitive predicate heads and coordination graph in item 7. (4) Reject any parser-visible `neg`, `або`, `чи`, adversative coordinator, second coordinator, additional lexical verb/participle, ellipsis, condition candidate or noncontiguous source mapping. (5) Let the first phrase run from segment start through the last non-whitespace character before the coordinator; let the second predicate phrase run from the first non-whitespace character after the coordinator through segment end, excluding terminal punctuation. Because no other verb or coordinator is allowed, every source-explicit complement/modifier in those intervals belongs to its respective predicate phrase; no semantic complement classifier is hidden in the rule. (6) Emit two observations. |
| 9. Evidence / offsets | **Selected representation: A, multiple exact Evidence references.** Allocate shared-anchor Evidence from the segment start through the normative token; first-result Evidence from segment start to before the coordinator; and second-predicate Evidence after the coordinator. The first observation references only the complete first-result Evidence. The second references the shared-anchor and second-predicate Evidence, in source order. Model-spec §§7.5 and 7.5.1 require each item to be an exact source span with a matching feature family; they do not require each item alone to express the complete semantic observation, and they explicitly permit multiple Evidence items per observation and overlapping spans. Therefore E001 is valid `EXPECTED_RESULT` Evidence as a jointly necessary normative fragment, E001/E002 overlap is allowed, and the two observations remain distinguishable through E002 versus E003. Consumers must use the referenced fragments as provenance; they must not concatenate E001 and E003 into fabricated source text or expose parser objects. No new domain field is required. |
| 10. Attachment semantics | The `conj` plus `cc` graph and closed source template establish only inheritance of the explicit subject/normative scope by the second predicate. They do not attach an external condition, criterion or method and do not create a reusable relation object. |
| 11. Positive example | For `Система повинна зберегти запит і повідомити оператора.` allocate `RESULT-UK-002:E001=[0,15)` `Система повинна`, `E002=[0,30)` `Система повинна зберегти запит`, and `E003=[33,53)` `повідомити оператора`. Observation 1 references `(E002)`; observation 2 references `(E001,E003)`. The observations are distinguished by their predicate-bearing Evidence (`E002` versus `E003`). |
| 12. Negative example | `Система повинна показати напис «зберегти і повідомити».` → coordinated words in a quoted label are not two results. |
| 13. False-positive boundary | A coordinator not represented by the exact `cc`/`conj` graph, coordinated nouns/objects, quoted content, alternatives (`або`, `чи`), adversatives, negation, separate subjects, more than two predicates or any excluded boundary cannot produce two observations. |
| 14. UNRESOLVED behavior | A segment with a normative anchor and apparent two-verb `і`/`та` coordination that fails the closed graph, arity, boundary, subject, negation or exact-span checks produces `RESULT_COORD_UNRESOLVED_CANDIDATE` for the complete segment, no partial result from this segment, and `INCOMPLETE`. Parser blocking produces `RESULT_COORD_PARSER_BLOCKED`, no Evidence and `INCOMPLETE`. A quoted `і`/`та` with no two-verb coordination is a completed negative for this extension and falls through to `RESULT-UK-001`. |
| 15. Applicability | Structural detection does not decide whether more than one result is a singularity defect or change C/V applicability. |
| 16. Known limitations | This covers only binary active infinitive coordination with explicit shared normative force. It does not prove logical independence, support passive/coordinated finite predicates, or decide singularity. |
| 17. Dependencies and interaction | Proposed candidate dispatch precedes `RESULT-UK-001` only for a segment with a normative anchor and an apparent source two-verb `і`/`та` coordination. Such a segment is already unresolved, with no accepted partial result, under the approved single-result grammar; ownership by an accepted or unresolved `RESULT-UK-002` candidate therefore cannot suppress an approved MVP observation. With no such candidate, the complete segment falls through unchanged to `RESULT-UK-001`, including its approved diagnostics. Accepted observations from other source-distinct segments are preserved; adding an unresolved segment yields family `INCOMPLETE / DETECTED`. Evidence IDs sort by `(start_offset,end_offset,evidence_id)`, giving E001, E002, E003 above. Within each observation, refs use the same ordering; observations sort by predicate-bearing Evidence start, first predicate then second, which resolves the shared-anchor tie. Same-rule duplicate spans collapse. No `ATTACH-UK-001` or domain change is required. |
| 18. Scientific approval | `APPROVED_FOR_SRM04_FIRST_SLICE` through D02 and D08, with D06-D07's no-attachment/no-domain-change boundary; authoritative contract in model-spec §7.14.16.3. |

### 4.3 `RESULT-UK-003` — nonmodal expected results under requirement force

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Represent overt observable results expressed without an MVP normative modal, including worked R5′. |
| 2. Exact source | §2.1 Table 2.1, Completeness row; worked application §8 Table 7 R5′; model-spec §7.14.4 family-level R5′ spans and its explicit first-production exclusion. |
| 3. MVP limitation | `RESULT-UK-001` intentionally does not infer obligation from an indicative verb or inherited context. |
| 4. Feature / Feature ID | Existing `expected_results[]` / `expected_result`. |
| 5. Proposed Rule ID | `RESULT-UK-003` (provisional). |
| 6. Ukrainian construction | Overt nonmodal observable behavior clauses such as R5′ `події зберігаються у черзі` and `UI показує статус degraded` within one requirement sentence. |
| 7. Parser annotations | Source-aligned clause boundaries, subject/predicate/complements, coordination and condition relations; these establish structure but **not** normative force by themselves. |
| 8. Recognition procedure | **No complete procedure is scientifically derivable.** Parser annotations can delimit a present-tense clause but cannot establish that it is prescriptive. An independently sourced normative-force signal would be required before any clause could be accepted. The current references provide examples, not that signal. |
| 9. Evidence / offsets | Proposed result Evidence would be each exact complete behavior clause; R5′ spans and offsets are recorded in model-spec §7.14.4, but are semantic illustrations, not `RESULT-UK-003` production Evidence. |
| 10. Attachment semantics | Each candidate result must have its own proven condition and criterion links; semicolon or source order does not by itself transfer a condition. |
| 11. Positive example | Source-attested R5′ `Якщо GPS-провайдер не відповідає 15 с, події зберігаються у черзі, UI показує статус degraded, виконується повторна спроба з backoff; після 2 хв формують alert.` illustrates result candidates `[39,65)`, `[67,93)`, `[95,132)` and `[145,159)`, conditional on an approved force rule; condition candidates are `[0,37)` and `[134,144)`. |
| 12. Negative example | `У журналі зазначено, що події зберігаються у черзі.` is descriptive reporting, not automatically a required result. |
| 13. False-positive boundary | An arbitrary indicative verb, reported observation, documentation statement or parser clause is insufficient. |
| 14. UNRESOLVED behavior | There is no production scan under this ID in the first slice. Illustrative candidates remain outside implemented coverage; they must not be converted to `NOT_DETECTED`, Evidence or a defect merely by adding a parser. |
| 15. Applicability | No change to requirement type or C criterion applicability. |
| 16. Known limitations | A text-only line may not reveal whether present-tense behavior is normative or descriptive. |
| 17. Dependencies | Smallest missing scientific decision: identify a source-supported, text-observable normative-force marker independent of present tense, source position and neighboring clauses, with positive/negative Ukrainian cases. Attachment is not the blocker. |
| 18. Scientific approval | `RESEARCH_BLOCKED`. Excluded from the first SRM-04 slice; R5′ remains a semantic illustration only. |

### 4.4 `ACCEPT-UK-001` — nonnumeric, observable acceptance criterion

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Preserve an explicit nonnumeric oracle against which fulfilment of a specified result can be judged under an explicit source condition. |
| 2. Exact source | §2.1 Table 2.1 requires enough information for condition, expected reaction and fulfilment criterion and identifies a test oracle as Verifiability evidence; §2.3 ¶17–21 distinguishes objective operationalization from general verifiability; §3.2 Table 3.4 permits expected behavior or a condition as criterion content but requires contextual correctness; model-spec §7.14.5 narrows nonnumeric recognition to complete observable behavior under an explicit condition and requires result-clause Evidence plus a reference to the separately captured governing condition. |
| 3. MVP limitation | `ACCEPT-QUANT-001` needs a contained, judgeable numeric anchor and cannot recognize a nonnumeric oracle. Conversely, an exact output without an explicit governing condition is observable but is outside the currently approved nonnumeric scientific boundary. |
| 4. Feature / Feature ID | Existing `acceptance_criteria[]` / `acceptance_criterion`. |
| 5. Rule ID | `ACCEPT-UK-001` (allocated for this bounded exact-message contract; `ACCEPT-QUANT-001` unchanged). |
| 6. Ukrainian construction | Narrow leading-condition exact-output template: one accepted leading `COND-UK-001` condition, followed by its delimiter comma and one accepted `RESULT-UK-001` result. Inside that result, the lexical predicate lemma and complete source token are `показати`; its direct object has lemma and complete source token `повідомлення`; immediately after that object, ignoring only Unicode whitespace, is one non-empty, non-nested Ukrainian guillemet literal `«…»`. No postposed condition, other output verb, object noun or quote style is included. |
| 7. Parser annotations | Accepted `COND-UK-001` and `RESULT-UK-001` observations/Evidence are required. For the result, source-aligned predicate and object tokens are required; the `повідомлення` token must have `dependency_relation=obj` and `head_token_id` equal to the `показати` token. Token offsets and sentence boundary are required. Quote boundaries and the condition/result source partition are recognized in original text, not inferred from parser punctuation. For P07 the selected backend emitted `система → повинна` (`nsubj`), `показати → повинна` (`xcomp`, `VerbForm=Inf`) and `повідомлення → показати` (`obj`); the condition itself is accepted by the existing lexical `COND-UK-001` leading template. |
| 8. Deterministic recognition procedure | (1) Reuse exactly one accepted leading `COND-UK-001` condition and exactly one accepted `RESULT-UK-001` output; duplicate neither grammar. (2) Establish the local governing relation only when the accepted condition starts the same hard segment, its Evidence is followed by the approved delimiter comma and only whitespace before the result Evidence, and the result occupies the rest of that hard segment excluding terminal punctuation. (3) Within the result Evidence span, require the exact predicate/object relation in items 6–7. (4) Require exactly one `«` and its following `»`, non-empty interior, no nested `«`/`»`, and no non-whitespace source characters between `повідомлення` and `«`. (5) Require the closing `»` to be the last non-whitespace character of result Evidence. (6) Emit one clause-level criterion. No general attachment or semantic judgeability algorithm is invoked. |
| 9. Evidence / offsets | One accepted literal criterion uses two independent same-family Evidence fragments with `feature_id=ACCEPTANCE_CRITERION` and `rule_id=ACCEPT-UK-001`: the exact accepted governing-condition span and the complete accepted result-clause span. They do not reuse upstream Evidence IDs. The condition fragment mirrors the accepted `COND-UK-001` source interval because cross-family IDs cannot be referenced by an acceptance observation; exact `(requirement_id,start_offset,end_offset)` equality preserves the dependency without a new field. In P07, `E001=[0,23)` `Якщо сервіс недоступний` and `E002=[25,83)` `система повинна показати повідомлення «Сервіс недоступний»`; the observation references `(E001,E002)`. The exact oracle remains `[63,83)` with content `[64,82)`. |
| 10. Attachment semantics | The accepted `COND-UK-001` leading template and exact source partition in item 8 establish one local condition → result relation; equality with the accepted result span establishes criterion → result composition. The criterion judges only the exact displayed-message behavior under that condition. No reusable relationship object or `ATTACH-UK-001` link is required. |
| 11. Positive example | `Якщо сервіс недоступний, система повинна показати повідомлення «Сервіс недоступний».` has accepted condition `[0,23)`, accepted result `[25,83)`, and one approved acceptance observation referencing its own condition-support and result Evidence `[0,23)` and `[25,83)`. |
| 12. Negative example | `Якщо сервіс не відповідає, система повинна показати зрозуміле повідомлення.` has an accepted condition and result but no specified literal content. An otherwise matching unconditional exact output is separately excluded by P22. |
| 13. False-positive boundary | No accepted leading governing condition, a nonmatching condition/result source partition, a result without the exact predicate/object pair, unquoted or empty output, another quote style, nested/multiple literals, text after the closing guillemet, a method name, a subjective adjective or a test link is not accepted. No automatic equivalence of observable result and criterion is introduced. |
| 14. UNRESOLVED behavior | If accepted condition/result dependencies exist but their local source partition cannot be established, or the accepted result contains the exact `показати повідомлення` pair but guillemet pairing, nesting, object attachment or result boundary cannot be determined, emit `ACCEPT_LITERAL_UNRESOLVED_CANDIDATE` for the result span, no criterion, and `INCOMPLETE`. If required condition or result analysis is blocked or incomplete, emit `ACCEPT_LITERAL_DEPENDENCY_BLOCKED`, no Evidence and `INCOMPLETE`. With no accepted explicit condition, the narrow rule completes with no contribution even when an exact output result is observable. A determinate empty/unquoted output likewise contributes nothing and completes. |
| 15. Applicability | A nonnumeric criterion can be relevant without making every requirement's criterion universally mandatory; SRM-09 governs type-specific applicability. |
| 16. Known limitations | The rule covers only exact displayed output under one accepted leading `COND-UK-001` condition. It proves judgeability for that conditioned output only; it does not prove complete requirement fulfilment, usability, domain correctness, procedure quality or test execution. Unconditional exact outputs, postposed conditions and other nonnumeric states remain outside coverage. |
| 17. Dependencies and interaction | Depends on accepted leading `COND-UK-001` and accepted `RESULT-UK-001`, and runs independently of `ACCEPT-QUANT-001`; neither rule supplies the other's scientific justification. Same-rule duplicate spans collapse. Merge identity is the shared complete result-clause span. If both acceptance rules accept that result, retain the literal rule's condition-support/result Evidence and the quantitative rule's result Evidence but emit **one clause-level `FeatureObservation`**. Order refs by `(start_offset,end_offset,rule precedence,evidence_id)`, with existing `ACCEPT-QUANT-001` before `ACCEPT-UK-001` only for equal spans. P21 therefore orders `(ACCEPT-UK-001:E001, ACCEPT-QUANT-001:E001, ACCEPT-UK-001:E002)`. Source-distinct result spans remain distinct observations. Diagnostics from either rule remain; accepted plus unresolved yields `INCOMPLETE / DETECTED`, while unresolved-only yields `INCOMPLETE / UNRESOLVED`. No domain change, `RESULT-UK-002/003`, `ATTACH-UK-001`, formula or applicability change is required. |
| 18. Scientific approval | `APPROVED_FOR_SRM04_FIRST_SLICE` through D04, D06-D08; authoritative contract in model-spec §7.14.16.4. |

### 4.5 `VERIFY-UK-002` — further explicit method-role constructions

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Detect an explicitly stated verification procedure when its grammatical role is clear but it is outside `VERIFY-UK-001` constructions A–C. |
| 2. Exact source | §2.1 Table 2.1, Verifiability row; §2.3 ¶17–21; §3.2 ¶5–10/Table 3.4; model-spec §§7.9 and 7.14.7. |
| 3. MVP limitation | Only `перевіряється`/`перевіряються` instrument, exact verification label and exact `визначено` test declaration are allocated. |
| 4. Feature / Feature ID | Existing `verification_methods[]` / `verification_method`. |
| 5. Proposed Rule ID | `VERIFY-UK-002` (provisional). |
| 6. Ukrainian construction | No additional construction is proposed for the first slice. The synthetic `підтверджується <instrumental method>` form and source phrase `спосіб розрахунку SLA` remain candidates only. Neither supplies an approved reproducibility or verification-role boundary beyond `VERIFY-UK-001`. |
| 7. Parser annotations | Parser structure could establish an instrumental phrase, but annotations cannot supply scientific authority for a new governing verb or establish method reproducibility. |
| 8. Recognition procedure | None for SRM-04 first slice. `VERIFY-UK-001` remains the complete executable method contract. A future proposal must first select an exact source-supported governing construction, phrase inventory/boundary, exclusions and unresolved cases. |
| 9. Evidence / offsets | No `VERIFY-UK-002` Evidence is authorized. Candidate spans such as `[26,44)` `інспекцією журналу` are illustrative diagnostic material only. |
| 10. Attachment semantics | An explicit method may verify a criterion or a result only when its target is established; a method observation does not assert sufficiency. |
| 11. Positive example | Candidate: `Виконання підтверджується інспекцією журналу.` with candidate method span `[26,44)` `інспекцією журналу`. The verb `підтверджується` is **not** approved; this is a research question, not expected production detection. |
| 12. Negative example | `Система створює тестовий випадок.` names an artifact/system behavior, not an explicit means of checking fulfilment. |
| 13. False-positive boundary | Artifact link, future promise, isolated method noun, discussion about testing and apparently testable behavior remain outside the method family. |
| 14. UNRESOLVED behavior | No new detector is added, so this proposal adds no status or diagnostic. Existing `VERIFY-UK-001` treatment of its approved vocabulary remains authoritative. |
| 15. Applicability | A requirement need not name a method; absence is not zero Verifiability or a defect. |
| 16. Known limitations | A named method does not establish complete inputs, environment, repeatability or adequacy. |
| 17. Dependencies | Smallest prerequisite for a later slice: one dissertation/source-attested additional governing construction plus explicit reproducibility/name boundary and positive/negative/unresolved cases. General attachment is not a prerequisite for detecting a method phrase. |
| 18. Scientific approval | `DEFERRED_FROM_FIRST_SRM04_SLICE`. The scientific concept remains in the inventory; no `VERIFY-UK-002` behavior is ready for approval or implementation. |

### 4.6 `ATTACH-UK-001` — deferred reusable relationship

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Explain which accepted condition, constraint, criterion or method concerns which accepted result while retaining uncertainty. |
| 2. Exact source | §2.1 Table 2.1, Completeness/Verifiability rows; §2.3 ¶4–5, 17–21; §3.2 ¶5–7; §3.3 ¶10–11 and ¶30–36; model-spec §§7.3, 7.14.2 and 7.14.5.1. |
| 3. MVP limitation | `COND-UK-001` establishes only narrow anchor presence, and `ACCEPT-QUANT-001` links by complete Evidence containment. `FeatureObservation` has no general relation field. |
| 4. Feature / Feature ID | **No new feature family or Feature ID proposed.** This is a prospective relationship among existing observations, subject to an approved domain representation. |
| 5. Proposed Rule ID | `ATTACH-UK-001` (provisional relationship-rule ID, not a detector allocation). |
| 6. Ukrainian construction | No universal attachment syntax is proposed. `COND-UK-002`, `RESULT-UK-002`, `ACCEPT-UK-001` and approved `ACCEPT-QUANT-001` establish their own bounded local relationships without exporting them. |
| 7. Parser annotations | Parser-neutral dependencies may be consumed inside a bounded rule. They are never a generic scientific relationship and never Evidence. |
| 8. Recognition procedure | None for a reusable engine in the first slice. Do not form arbitrary candidate pairs. Preserve only links whose complete semantics are internal to an approved rule. Ambiguous broader relationships remain unstored rather than being resolved by proximity. |
| 9. Evidence / offsets | No relationship-only Evidence exists. Local rules retain their endpoint/source Evidence according to their own contracts. |
| 10. Attachment semantics | Distinguish unique supported target, several independently justified targets, competing plausible targets, missing target information and unsupported/invalid parse (§5). These are conceptual outcomes, not an approved enum. |
| 11. Positive example | `Якщо сервіс недоступний, система повинна зберегти запит.` has condition `[0,23)` and result `[25,55)`; its `COND-UK-001`/`RESULT-UK-001` observations are approved, but a stored general relation is not. |
| 12. Negative example | `Система повинна зберегти запит і повідомити оператора при перевірці.` does not license choosing one target for `при перевірці` by nearest words. |
| 13. False-positive boundary | Linear adjacency, punctuation alone, same requirement ID and parser `conj` alone are not semantic attachment proof. |
| 14. UNRESOLVED behavior | Preserve independently accepted endpoint observations; store no unsupported relationship. A detector that encounters an ambiguous link reports its own rule-specific diagnostic. There is no relationship-level status in the current domain. |
| 15. Applicability | Relation availability does not change feature or criterion applicability; `UNKNOWN`/`NOT_APPLICABLE` stay distinct. |
| 16. Known limitations | Cross-rule queries such as “which method verifies which result?” remain unavailable. If a future consumer requires them, a typed relation contract must be approved first. |
| 17. Dependencies | Deferred future contract, if required: stable observation endpoint identity; relation type and direction; one-to-one/one-to-many cardinality; endpoint Evidence/provenance; source ordering; explicit resolved/ambiguous/missing state; missing-endpoint and parser-failure rules; and a location in `RequirementExtractionResult`. None is needed for the first slice. |
| 18. Scientific approval | `DEFERRED_FROM_FIRST_SRM04_SLICE`. It must not block the three approved first-slice rules and is excluded from SRM-04 implementation. |

## 5. Multi-clause and attachment semantics

One sentence can contain several accepted observations in one `Requirement`.
Clause count does not create more requirement objects, a singularity defect or
a score. SRM-03 separates three different meanings that the earlier draft had
incorrectly grouped under `ATTACH-UK-001`:

| Concept | First-slice contract |
| --- | --- |
| Local relation established by one bounded detector | The relation exists only as a recognition condition inside that rule. `COND-UK-002` uses one exact `advcl` edge to one result; `RESULT-UK-002` uses a closed `conj`/`cc` graph for inherited normative scope; `ACCEPT-UK-001` reuses one accepted leading `COND-UK-001` condition and one accepted `RESULT-UK-001` result whose exact intervals partition the same hard segment around the approved comma, then uses equality with the result span for criterion composition; `ACCEPT-QUANT-001` keeps its approved containment rule. These relationships require no new domain object. |
| Reusable typed relationship between independently accepted observations | Deferred with `ATTACH-UK-001`. The current first slice has no consumer requiring stored cross-observation links. `evidence_refs` must not be overloaded to simulate endpoints. |
| Unresolved semantic relationship | Independently supported endpoint observations remain available. The affected bounded detector emits its own diagnostic when the ambiguity prevents its observation; otherwise no relationship is stored. Uncertainty is never replaced by a chosen nearest target. |

The required uncertainty distinctions remain:

| Relationship case | Treatment |
| --- | --- |
| Supported unambiguous attachment | Accept only under the complete local rule that defines both endpoints and the exact structural path or containment relation. |
| Multiple scientifically justified relationships | Outside the three approved subsets. A future typed contract must preserve every supported pair rather than select one. |
| Ambiguous attachment | Withhold the dependent observation/link and emit a source-bound rule diagnostic when the candidate boundary is known. |
| Missing attachment information | Preserve independent observations; create no relation and no fake Evidence. |
| Unsupported syntax or unreliable parser output | Apply the consuming detector's parser-blocked/incomplete outcome; never treat it as `NOT_DETECTED`. |

No nearest-token, nearest-clause, shortest-distance, first/last-result or
punctuation-only semantic fallback is permitted. Punctuation can define a
source interval only within a complete rule. For `ACCEPT-UK-001`, the comma is
usable only because accepted `COND-UK-001` and `RESULT-UK-001` outputs already
establish the two exact parts of the approved leading template; comma adjacency
alone proves nothing. The approved `ACCEPT-QUANT-001` containment
semantics remain unchanged. Broader one-to-many and cross-family relationships
remain deferred, not silently implemented.

## 6. Evidence and domain-contract implications

The approved `Evidence` fields remain `evidence_id`, `requirement_id`,
`feature_id`, `text`, `start_offset`, `end_offset`, `rule_id`. Every accepted
fragment must satisfy
`Requirement.text[start_offset:end_offset] == Evidence.text` using zero-based
Unicode code-point offsets after reader trimming. Evidence is exact original
text with punctuation preserved where the accepted span contains it; normalized
views and parser tokens cannot replace it. Repeated equal fragments at different
offsets remain distinct. Cross-family overlap is allowed when each observation
has its own approved justification and Evidence ID. Parser diagnostics and
`DiagnosticSpan` are not accepted Evidence.

`RESULT-UK-002` deliberately uses the existing ability of one
`FeatureObservation` to reference multiple Evidence items. Those references
jointly justify **one** result; an individual fragment need not be a complete
semantic result by itself. E001 remains valid `EXPECTED_RESULT` Evidence because
it is an exact normative fragment used only together with E003 to justify the
second result. The E001/E002 overlap is explicitly permitted by model-spec
§7.5. Every ref resolves to same-family Evidence under §7.5.1. Ref order is
deterministic under §4.2, and E002 versus E003 supplies the predicate-bearing
identity that distinguishes the two observations. No consumer may reconstruct a
new source quotation by concatenating fragments; explanations cite the exact
fragments separately. These references are provenance, not endpoints of a
reusable relation.
`COND-UK-002` contributes one Evidence item. A standalone `ACCEPT-UK-001`
acceptance contributes two `ACCEPTANCE_CRITERION` Evidence items: an exact copy
of the accepted governing-condition span and the complete accepted result span.
The original `COND-UK-001` Evidence remains separately present under
`CONDITION_CONTEXT`; its ID is not placed in the acceptance observation because
model-spec §7.5.1 requires accepted refs to match the observation's feature
family. Exact requirement ID and span equality connect the condition-support
copy to that accepted condition without a cross-family reference or new field.
When `ACCEPT-QUANT-001` accepts the same result span, the one merged observation
has all three same-family refs ordered as §4.4 defines. No approved rule changes
`RequirementExtractionResult`.
Parser edges remain internal recognition inputs and are never accepted Evidence.
Actor/action/object fields remain deferred under model-spec §7.11.

Rule interaction is deterministic:

- `COND-UK-002` claims only its exact postposed `якщо` candidate before
  `COND-UK-001`; other condition candidates keep existing behavior.
- `RESULT-UK-002` claims only an apparent binary two-verb `і`/`та` segment
  before `RESULT-UK-001`; quoted/noun coordination falls through to the MVP
  rule, while a structurally apparent but unresolved result candidate remains
  incomplete and is not reduced to a single result.
- `ACCEPT-UK-001` consumes an accepted leading `COND-UK-001` condition plus the
  accepted `RESULT-UK-001` result that completes the same hard segment. With no
  accepted condition, even an exact output is only an observable result for this
  rule and the rule contributes no acceptance observation. It runs
  independently of `ACCEPT-QUANT-001`; independent justifications retain their
  Evidence and rule provenance. A shared complete result span merges into one
  clause-level acceptance observation with the condition-support and both
  result-provenance refs; source-distinct results remain distinct observations.
- Across rules, Evidence IDs include the rule ID and cannot collide. Within a
  rule, accepted observations and diagnostics use source ordering and exact
  tie rules from §4. Same-rule identical spans are collapsed; distinct source
  occurrences remain distinct.
- A family with any accepted observation remains `DETECTED`; if another
  candidate is unresolved it is also `INCOMPLETE`. With no observation, all
  completed checks yield `NOT_DETECTED`, while any blocking diagnostic yields
  `UNRESOLVED`, exactly as model-spec §7.15.7 defines.

Detection remains `DETECTED`, `NOT_DETECTED` or `UNRESOLVED`, derived from
observations plus processing completeness. A mixed accepted/unresolved family
is `INCOMPLETE / DETECTED` with diagnostics; a fully blocked family is
`INCOMPLETE / UNRESOLVED`. `NOT_DETECTED` means the approved scan completed and
found no observation, not that an applicable quality criterion failed. The
separate `APPLICABLE`, `NOT_APPLICABLE`, `UNKNOWN` states remain unchanged.
Structural observations do not create `QUALITY_PROBLEM`; `FIND-U-VAGUE-001`
remains the only approved MVP observation-to-`SIGNAL` conversion. No C/V/U
formula, exact `Fraction` value, applicability rule or reporter behavior is
changed by this document.

## 7. Ukrainian positive, negative and unresolved reference cases

Rows P01–P04, P07–P08 and P14–P22 are the **approved binding fixtures** for the
three allocated first-slice rules. Their statuses describe the approved rule contribution;
family merging then follows §6. P05–P06 and P09–P13 are explicitly
`ILLUSTRATIVE_ONLY` because their rules are blocked or deferred. No illustrative
row can become an SRM-04 test. All offsets are zero-based Unicode code-point,
start-inclusive/end-exclusive positions in the exact trimmed input.

| Case and exact input | Rule / observations and Evidence | Processing, detection and diagnostic | Explanation / status |
| --- | --- | --- | --- |
| P01 `Система повинна зберегти запит, якщо сервіс не відповідає.` | `COND-UK-002`: one `condition_context`; `COND-UK-002:E001=[32,57)` `якщо сервіс не відповідає` | `COMPLETE / DETECTED`; no diagnostic | Explicit finite condition head `відповідає`. The pinned backend probe produced `mark(якщо → відповідає)`, `advcl(відповідає → повинна)`, `xcomp(зберегти → повинна)` and `nsubj(Система → повинна)`; it attached the delimiter comma to `відповідає`, which §4.1 excludes from the suffix projection. Every mandatory neutral check is therefore satisfied. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P02 `Система повинна показати слово «якщо» у довідці.` | `COND-UK-002`: no observation or Evidence; quoted token candidate `[32,36)` is excluded | `COMPLETE / NOT_DETECTED`; no diagnostic | `якщо` is inside `[31,37)` `«якщо»` and cannot satisfy the condition relation. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P03 `Система повинна зберегти запит і повідомити оператора.` | `RESULT-UK-002`: result 1 refs `E002`; result 2 refs `E001,E003`. `E001=[0,15)` `Система повинна`; `E002=[0,30)` `Система повинна зберегти запит`; `E003=[33,53)` `повідомити оператора` | `COMPLETE / DETECTED`; no diagnostic | Binary active-infinitive `і` coordination with exact shared scope and no invented text. The pinned backend probe produced the required `nsubj`/`xcomp`/`conj`/`cc` graph recorded in §4.2. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P04 `Система повинна показати напис «зберегти і повідомити».` | `RESULT-UK-002`: no new observation/Evidence; quoted text `[32,53)` has no two-verb `conj`/`cc` graph | Extension contribution `COMPLETE / NOT_DETECTED`; no diagnostic; segment falls through unchanged to `RESULT-UK-001` | Quoted coordinator cannot create another result. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P05 `Якщо сервіс недоступний, події зберігаються у черзі.` | `RESULT-UK-003` candidate result `[25,51)`; no accepted Evidence | No proposed processing/detection contract | Present tense does not establish normative force. `RESEARCH_BLOCKED / ILLUSTRATIVE_ONLY`. |
| P06 `У журналі зазначено, що події зберігаються у черзі.` | `RESULT-UK-003` descriptive clause `[24,50)`; no accepted Evidence | No proposed processing/detection contract | Demonstrates why syntax alone cannot distinguish force. `RESEARCH_BLOCKED / ILLUSTRATIVE_ONLY`. |
| P07 `Якщо сервіс недоступний, система повинна показати повідомлення «Сервіс недоступний».` | Accepted `COND-UK-001` condition `[0,23)` and `RESULT-UK-001` result `[25,83)`. `ACCEPT-UK-001`: one `acceptance_criterion`; `E001=[0,23)` `Якщо сервіс недоступний`, `E002=[25,83)` `система повинна показати повідомлення «Сервіс недоступний»`; refs `(E001,E002)`; oracle `[63,83)`, content `[64,82)` | `COMPLETE / DETECTED`; no diagnostic | The accepted leading condition and result exactly partition one hard segment. The selected backend produced `obj(повідомлення → показати)`. The zero-copula condition is accepted only by existing `COND-UK-001`, not treated as a finite `COND-UK-002` predicate. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P08 `Якщо сервіс не відповідає, система повинна показати зрозуміле повідомлення.` | Accepted condition `[0,25)` and result `[27,74)`; `ACCEPT-UK-001`: no observation/Evidence because the result has no literal oracle | `COMPLETE / NOT_DETECTED`; no diagnostic | The governing condition is explicit, but a subjective adjective is not exact output content. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P09 `Виконання підтверджується інспекцією журналу.` | `VERIFY-UK-002` candidate method `[26,44)`; no proposed Evidence | No proposed processing/detection contract | `підтверджується` is synthetic and not source-authorized. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P10 `Система створює тестовий випадок.` | Artifact phrase `[16,32)`; no `VERIFY-UK-002` Evidence | No proposed processing/detection contract; existing `VERIFY-UK-001` remains authoritative | Names an artifact/system behavior, not a new verification-role construction. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P11 `Якщо сервіс недоступний, система повинна зберегти запит і повідомити оператора.` | Condition `[0,23)` and result candidates `[25,55)`, `[58,78)`; no relationship Evidence | No `ATTACH-UK-001` result | Leading-condition plus coordinated-result scope is outside the approved binary result subset. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P12 `Система повинна зберегти запит і повідомити оператора при перевірці.` | Ambiguous phrase `[54,67)` `при перевірці`; no relationship Evidence | No `ATTACH-UK-001` result | Neither source order nor proximity selects a target. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P13 `Система повинна зберегти запит; перевірка: інспекція журналу.` | Existing method candidate `[43,60)` and result `[0,30)` remain independent; no relationship Evidence | Existing `VERIFY-UK-001` governs method detection; no `ATTACH-UK-001` result | A method observation does not prove which result/criterion it verifies. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P14 `Система повинна зберегти запит і повідомити оператора.` with parsed text present but required coordination annotation incomplete | `RESULT-UK-002`: no observation/Evidence; affected candidate `[0,53)` | `INCOMPLETE / UNRESOLVED`; `RESULT_COORD_PARSER_BLOCKED` with `DiagnosticSpan=[0,53)` | Missing required annotation cannot become absence. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P15 `Система повинна зберегти запит якщо сервіс не відповідає.` | `COND-UK-002`: no observation/Evidence; marker phrase `[31,56)` lacks the mandatory comma | Extension contribution `COMPLETE / NOT_DETECTED`; no diagnostic; existing rules remain authoritative | The finite condition otherwise matches the positive grammar, so this case isolates the mandatory-comma boundary. Whitespace/position cannot replace the comma template. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P16 `Система повинна зберегти запит і повідомити оператора, якщо сервіс не відповідає.` | `COND-UK-002`: no observation/Evidence; condition candidate `[55,80)` | `INCOMPLETE / UNRESOLVED`; `COND_POSTPOSED_YAKSHCHO_UNRESOLVED` with `DiagnosticSpan=[55,80)` | The explicit finite condition is present, but the prefix has more than one result predicate, so this rule cannot select a unique governing predicate-chain head. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P17 `Система повинна зберегти запит і не повідомляти оператора.` | `RESULT-UK-002`: no observation/Evidence; segment candidate `[0,57)` | `INCOMPLETE / UNRESOLVED`; `RESULT_COORD_UNRESOLVED_CANDIDATE` with `DiagnosticSpan=[0,57)` | Parser-visible negation is excluded; the detector does not invert or discard it. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P18 `Система повинна зберегти запит або повідомити оператора.` | `RESULT-UK-002`: no observation/Evidence; alternative coordinator `[31,34)` | Extension contribution `COMPLETE / NOT_DETECTED`; no extension diagnostic; segment falls through to existing `RESULT-UK-001` behavior | `або` is not an approved shared-obligation coordinator for this rule. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P19 `Якщо сервіс не відповідає, система повинна показати повідомлення «».` | Accepted condition `[0,25)` and result `[27,67)`; `ACCEPT-UK-001`: no observation/Evidence; empty literal `[65,67)` `«»` | `COMPLETE / NOT_DETECTED`; no diagnostic | The condition dependency is satisfied; empty output is deterministically insufficient, not an ambiguous oracle. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P20 `Якщо сервіс не відповідає, система повинна показати повідомлення «Помилка «E1»».` | Accepted condition `[0,25)`; `ACCEPT-UK-001`: no observation/Evidence; affected result `[27,79)`, nested literal `[65,79)` `«Помилка «E1»»` | `INCOMPLETE / UNRESOLVED`; `ACCEPT_LITERAL_UNRESOLVED_CANDIDATE` with `DiagnosticSpan=[27,79)` | The condition dependency is satisfied, but the bounded rule does not choose inner/outer quote semantics. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P21 `Якщо сервіс не відповідає, система повинна не більше ніж за 2 с показати повідомлення «Сервіс недоступний».` | Upstream: `COND-UK-001:E001=[0,25)` `Якщо сервіс не відповідає`; `RESULT-UK-001:E001=[27,106)` `система повинна не більше ніж за 2 с показати повідомлення «Сервіс недоступний»`; judgeable `QUANT-UK-001:E001=[43,63)` `не більше ніж за 2 с`. Acceptance Evidence: `ACCEPT-UK-001:E001` copies `[0,25)`; `ACCEPT-UK-001:E002` and `ACCEPT-QUANT-001:E001` each copy `[27,106)`. One merged `acceptance_criterion` refs `(ACCEPT-UK-001:E001, ACCEPT-QUANT-001:E001, ACCEPT-UK-001:E002)`; oracle `[86,106)` `«Сервіс недоступний»`, content `[87,105)` `Сервіс недоступний` | Both rules `COMPLETE`; merged family `COMPLETE / DETECTED`; no diagnostic | Existing detectors actually accept the condition, result, inclusive `LESS_THAN_OR_EQUAL` quantitative bound and quantitative criterion. The selected backend produced local `nsubj`, `xcomp` with `VerbForm=Inf`, and `obj(повідомлення → показати)`; original text supplies the final guillemet boundary. Both rule justifications and rule IDs remain independent. `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| P22 `Система повинна показати повідомлення «Сервіс недоступний».` | Accepted `RESULT-UK-001` result `[0,58)` with oracle `[38,58)` and content `[39,57)`; no accepted `COND-UK-001` condition; `ACCEPT-UK-001`: no observation/Evidence | Extension contribution `COMPLETE / NOT_DETECTED`; no diagnostic; the expected result remains accepted | Exact output is observable, but without an explicit accepted governing condition it is outside the approved nonnumeric criterion subset. `APPROVED_FOR_SRM04_FIRST_SLICE`. |

MVP regression anchors below are **existing approved behavior**, not new SRM-03
reference cases; their exact results remain governed by model-spec §§7.14.3–7.14.7:

| Existing sentence | Target observation; relevant exact source span | Existing Rule ID; approved outcome | Source / status |
| --- | --- | --- | --- |
| `Якщо сервіс недоступний, система повинна зберегти запит.` | Condition `[0,23)` `Якщо сервіс недоступний`; result `[25,55)` `система повинна зберегти запит` | `COND-UK-001`, `RESULT-UK-001`; both `DETECTED` | model-spec §§7.14.3.1, 7.14.4.1; **EXISTING_APPROVED_MVP** |
| `Система повинна відповісти не більше ніж за 2 с.` | Complete criterion `[0,47)` `Система повинна відповісти не більше ніж за 2 с` | `ACCEPT-QUANT-001`; `DETECTED` | model-spec §7.14.5.1; **EXISTING_APPROVED_MVP** |
| `Виконання перевіряється навантажувальним тестом.` | Method `[24,47)` `навантажувальним тестом` | `VERIFY-UK-001`; `DETECTED` | model-spec §7.14.7.1; **EXISTING_APPROVED_MVP** |
| `Система контролює обробку запитів.` | Apparent candidate `[0,33)`; no accepted Evidence | `RESULT-UK-001`; `UNRESOLVED` | model-spec §7.14.4.1; **EXISTING_APPROVED_MVP** |

**Offset validation record.** A temporary Unicode code-point validation script
enumerated every documented span occurrence in P01–P22 and the four MVP anchors,
sliced the literal input, and compared it with an explicit expected-text list.
All 55 span occurrences across 26 exact inputs satisfied
`source[start_offset:end_offset] == expected_text`, including modified P07,
P08, P19 and P20, new P21 and P22, and repeated Evidence/diagnostic occurrences.
The script was not added to the repository and the application test suite was
not run.

**Selected-backend validation record.** A separate temporary read-only probe
used the repository adapter with spaCy 3.8.16 and `uk_core_news_sm` 3.8.0. It
returned source-aligned parses without parser diagnostics for exact P01, P03,
P07, P08 and P19–P22 and emitted the head/relation/morphology facts recorded in
§§4.1, 4.2, 4.4 and P21. A separate read-only call through the current baseline
extractor confirmed that P21 already yields accepted `COND-UK-001`,
`RESULT-UK-001`, `QUANT-UK-001` and `ACCEPT-QUANT-001` outputs at the documented
offsets. `ACCEPT-UK-001` remains unimplemented; its now-approved contract was
not presented as executed.
These probes validate present implementation feasibility only. They were not
added as fixtures, did not modify the adapter, and were not a test-suite run;
the pinned SRM-04 fixtures in §9 remain mandatory.

## 8. Compatibility with MVP v0.1

The reader, six-family registry, approved detectors, exact Evidence contract,
parser-neutral boundary, C/V/U calculators, `RequirementQualityProfile`,
specification aggregation and console presentation are unchanged. Existing
`COND-UK-001`, `RESULT-UK-001`, `ACCEPT-QUANT-001`, `VERIFY-UK-001`,
`QUANT-001`, `QUANT-UK-001` and `UK-VAGUE-001` keep their approved scope and
IDs. The three newly approved rules are distinguishable from those baselines
and must not alter their prior binding cases. One non-empty line remains one
requirement. A recognized extra clause is an observation within that object,
not a new requirement ID. An unsupported extra candidate is neither evidence
of absence nor a confirmed defect. No new actor/action/object feature is
introduced merely because the parser exposes a dependency tree.

## 9. SRM-04 authorization and prerequisites

The researcher has approved the bounded handoff below, and model-spec §7.14.16
is now authoritative. SRM-04 is authorized to implement exactly the three
`APPROVED_FOR_SRM04_FIRST_SLICE` rows after adding their required pinned-backend
fixtures. No blocked or deferred row is authorized.

| Rule ID | Disposition | Exact supported subset | Approval basis or future prerequisite | Domain / Evidence contract | Required reference cases | Parser-neutral validation prerequisite | SRM-04 implementation and diagnostics | Excluded behavior |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `COND-UK-002` | `APPROVED_FOR_SRM04_FIRST_SLICE` | One comma-delimited postposed `якщо` clause with one explicit finite `VERB` condition head, complete condition-subtree projection over the suffix, and attachment to exactly one simple MVP normative predicate-chain head | D01 and D08 | Existing condition observation and one exact suffix Evidence; no domain change or exported relation | P01, P02, P15, P16, plus parser-blocked fixture | Lock P01's observed `nsubj`/`xcomp` plus `mark(якщо → відповідає)` and `advcl(відповідає → повинна)` head identities and delimiter-comma attachment against the pinned backend; missing/changing required annotations must take the parser-blocked or unresolved path, never a fallback | Add exact candidate ownership, checks, Evidence and the two diagnostics; merge with `COND-UK-001` without duplicate Evidence/diagnostics and preserve all unrelated MVP markers | Zero-copula/adjectival conditions; other markers; no comma; multiple/nested/coordinated conditions; several results; nonmodal result; general attachment |
| `RESULT-UK-002` | `APPROVED_FOR_SRM04_FIRST_SLICE` | Exactly two active infinitive predicates coordinated by source `і`/`та` under one explicit MVP normative subject/anchor | D02 and D08 | Three exact same-family Evidence items; two observations; refs `(E002)` and `(E001,E003)`; no reconstruction or domain change | P03, P04, P14, P17, P18, plus explicit more-than-two exclusion | Lock P03's observed `nsubj`/`xcomp`/`conj`/`cc`, `VerbForm=Inf` and head identities; exercise incomplete annotations as `RESULT_COORD_PARSER_BLOCKED` | Add binary dispatch, Evidence construction, deterministic ref/observation ordering and diagnostics; retain source-distinct accepted MVP results and mixed accepted/unresolved output | Passive/finite coordination; more than two results; `або`/`чи`; negation; conditions; ellipsis; separate subjects; singularity judgment |
| `RESULT-UK-003` | `RESEARCH_BLOCKED` | None | A future decision supplying independently observable normative force | Undetermined | P05–P06 remain illustrative | None authorized | No SRM-04 work | All present-tense/nonmodal result inference, including worked R5′ |
| `ACCEPT-UK-001` | `APPROVED_FOR_SRM04_FIRST_SLICE` | Accepted leading `COND-UK-001` condition plus its accepted `RESULT-UK-001` remainder containing exact `показати` predicate, its `повідомлення` object and one final non-empty `«…»` literal | D04, D06, D07 and D08 | Two literal-rule Evidence fragments: condition-support copy and full result; P21 merge adds `ACCEPT-QUANT-001` result Evidence to one observation; no domain change | P07, P08, P19–P22, plus condition/result dependency-blocked fixture | Lock P07/P21 source partition, accepted upstream dependencies, result chain and `obj(повідомлення → показати)`; scan guillemets only in original result text; missing/incomplete dependency is blocked | Compose existing condition/result outputs, exact quote scan, two-piece Evidence and diagnostics; implement P21's three-ref merge while preserving rule provenance and mixed status | No accepted leading condition; postposed conditions; other verbs/nouns/quote styles; unquoted, empty, nested or vague outputs; general states; results from `RESULT-UK-002/003`; domain or procedure adequacy |
| `VERIFY-UK-002` | `DEFERRED_FROM_FIRST_SRM04_SLICE` | None beyond existing `VERIFY-UK-001` | Future source-backed construction decision | None yet | P09–P10 illustrative only | None authorized | No SRM-04 work | Synthetic governing verbs, vocabulary-only detection and reproducibility claims |
| `ATTACH-UK-001` | `DEFERRED_FROM_FIRST_SRM04_SLICE` | No reusable relationship; bounded local relations remain inside their detector rules | Future consumer plus complete typed-relation decision | Future stable observation identity and relation structure, only if approved | P11–P13 illustrative only | Parser arcs remain local detector inputs, never exported relations | No SRM-04 work | Universal pairing, distance fallbacks, exported parser edges and inferred one-to-many links |

The authorized **first SRM-04 slice** is exactly `COND-UK-002`,
`RESULT-UK-002`, and `ACCEPT-UK-001`. It may add detector
implementations and directly related tests only. It must not add a relationship
engine, change feature families/domain models, implement `RESULT-UK-003` or
`VERIFY-UK-002`, decide singularity, alter applicability/calculators, or continue
into SRM-05+. This document-only approval does not itself change MVP behavior.

## 10. Researcher Approval Package — SRM-03

D01, D02, D04, D06, D07, and D08 are researcher-approved as one bounded
package, with the authoritative record in model-spec §7.14.16. D03 remains
`RESEARCH_BLOCKED`; D05 and D09 remain `DEFERRED`. Blocked and deferred items
do not enter the first SRM-04 slice.

### D01 — bounded postposed `якщо`

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D01` — `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| 2. Scientific source and baseline | §2.1 Table 2.1 condition/reaction completeness; worked R5′; `COND-UK-001` marker/offset mechanics and its deliberate postposed-`якщо` gap. |
| 3. Exact proposed choice | Approve `COND-UK-002` exactly as §4.1: comma-required `<one simple normative result>, якщо <one explicit finite-verbal suffix condition>`, complete-token marker, `mark` to the finite head, `advcl` from that head to the accepted prefix's normative predicate-chain head, complete condition-subtree projection over the suffix (excluding the delimiter comma) and one condition Evidence. Zero-copula/adjectival predicates are outside this choice. |
| 4. Material alternatives | General attachment engine; marker/comma regex alone; all postposed subordinate clauses. Rejected because they add unnecessary domain machinery or cannot prove the target. |
| 5. Scientific defence | The source establishes explicit condition plus reaction as meaningful; the proposal observes both explicitly and restricts attachment through a standard parser-neutral relation rather than distance. |
| 6. Domain/Evidence consequence | Existing `condition_context`; no domain field. One exact Evidence item and two new diagnostic codes. Local relation is not exported. |
| 7. Supporting cases | Corrected P01 finite-verb positive, P02 quoted negative, corrected P15 no-comma negative and corrected P16 multiple-result unresolved; the selected backend emitted P01's required graph, while parser-blocked handling is fixed by §4.1/model-spec §7.15.8. |
| 8. Known limitations | One marker, one comma, one result and one explicit finite-verbal condition only; no zero-copula, coordinated, nested or nonmodal coverage. |
| 9. Remaining prerequisite | SRM-04 must add a pinned-backend P01 graph fixture and blocked-annotation fixture before production use; this is implementation validation of the complete approved rule, not a missing scientific choice. |
| 10. SRM-04 authorization | Implement the §4.1 detector contribution, precedence, Evidence, diagnostics and directly related approved cases. |

### D02 — binary coordinated normative results

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D02` — `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| 2. Scientific source and baseline | §2.1 Completeness/Singularity; model-spec §7.14.4 states independent coordinated results are separate observations but leaves general coordination outside `RESULT-UK-001`. |
| 3. Exact proposed choice | Approve only two active infinitives under one explicit MVP normative subject/anchor, with source `і`/`та`, exact `conj`/`cc` graph, no conditions/negation/alternatives/extra verbs. Select multiple exact Evidence refs: shared subject+anchor plus the second predicate phrase. |
| 4. Material alternatives | One covering span for both results obscures which predicate constitutes result 2; predicate-only Evidence loses normative force; a new provenance field is unnecessary. Existing multi-Evidence observations preserve both facts exactly. |
| 5. Scientific defence | The explicit normative anchor and closed dependency graph establish shared force; exact source fragments avoid invented text and preserve explainability. |
| 6. Domain/Evidence consequence | No domain change. Under model-spec §§7.5 and 7.5.1, three exact same-family Evidence items support two existing `FeatureObservation`s; fragments may jointly justify an observation, overlap is allowed, refs resolve within `EXPECTED_RESULT`, and source reconstruction is prohibited. Rule-specific ref/observation tie order and diagnostics are fixed in §4.2. |
| 7. Supporting cases | P03 positive, P04 quoted negative, P14 blocked annotation, P17 negation unresolved, P18 alternative negative; arity greater than two is explicitly excluded by §4.2. |
| 8. Known limitations | Binary active infinitives only; no logical-independence or singularity conclusion. |
| 9. Remaining prerequisite | SRM-04 must lock the observed P03 neutral graph and its incomplete-annotation behavior; no Evidence representation or scientific algorithm choice remains open. |
| 10. SRM-04 authorization | Implement §4.2 segment dispatch, parser checks, Evidence/observation construction, diagnostics and approved fixtures. |

### D03 — nonmodal normative force

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D03` — `RESEARCH_BLOCKED`. |
| 2. Scientific source and baseline | Worked R5′ illustrates present-tense results; `RESULT-UK-001` correctly refuses arbitrary indicative verbs. |
| 3. Exact proposed choice | Do not implement `RESULT-UK-003`; do not infer force from present tense, line membership, source order, condition adjacency or another clause. |
| 4. Material alternatives | Treat every line as normative or inherit force across coordination/semicolon. Rejected because descriptive P06 has the same local behavior syntax. |
| 5. Scientific defence | Syntactic clause structure establishes behavior content, not whether the statement prescribes it. |
| 6. Domain/Evidence consequence | No observation, Evidence, diagnostic code or domain change under this proposed ID. |
| 7. Supporting cases | P05 and P06 demonstrate the indistinguishable normative/descriptive boundary. |
| 8. Known limitations | Source-attested R5′ remains uncovered by a production nonmodal rule. |
| 9. Exact blocker | Missing source-supported, text-observable normative-force criterion with contrasting Ukrainian cases. |
| 10. SRM-04 authorization | None. |

### D04 — exact quoted-output acceptance criterion

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D04` — `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| 2. Scientific source and baseline | Model-spec §7.14.5 expressly requires complete observable nonnumeric behavior under an explicit condition and Evidence for the behavior plus the separately captured condition. §2.1 Table 2.1 links local completeness to condition, reaction and fulfilment criterion and permits a test oracle; §2.3 ¶17–21 requires objective operationalization; §3.2 Table 3.4 permits expected behavior or a condition but requires contextual correctness. `ACCEPT-QUANT-001` was the prior production acceptance baseline; this approval adds only bounded `ACCEPT-UK-001`. |
| 3. Exact proposed choice | Approve `ACCEPT-UK-001` only for an accepted leading `COND-UK-001` condition whose comma-delimited remainder is one accepted `RESULT-UK-001` containing exact `показати` → `повідомлення` object and one final non-empty `«…»` literal. Treat the literal as an oracle for that displayed output under that condition only. |
| 4. Material alternatives | Permit unconditional exact output; accept every observable result; add a general condition/result relation; accept adjective-based message quality, general state semantics or other output verbs. The unconditional form would be a broader new scientific proposal than model-spec §7.14.5; the others require unapproved interpretation or attachment machinery. |
| 5. Scientific defence | The explicit condition supplies the approved context boundary and the exact literal supplies a reproducible equality oracle. Reusing the already accepted leading condition/result source partition avoids proximity inference and makes no claim about complete requirement fulfilment. |
| 6. Domain/Evidence consequence | Existing acceptance family and no domain change. The literal observation references two new `ACCEPT-UK-001` Evidence items: the exact accepted-condition span and complete result span. The condition-support span duplicates source coordinates, not the cross-family `COND-UK-001` Evidence ID. In P21, `ACCEPT-QUANT-001` adds its independent result-span Evidence and the three refs merge into one clause-level observation. |
| 7. Supporting cases | P07 conditioned positive; P08 conditioned unquoted negative; P19 conditioned empty-literal negative; P20 conditioned nested-literal unresolved; P21 conditioned quantitative/literal merge positive; P22 unconditional exact-output boundary. |
| 8. Known limitations | Leading approved conditions and exact displayed messages only; no unconditional or postposed-condition coverage, general nonnumeric state, usability or domain-correctness judgment. |
| 9. Remaining prerequisite | SRM-04 must lock P07/P21 source partitions, result/object graphs, P21 quantitative composition and condition/result dependency-blocked cases; no general judgeability or attachment choice remains open. |
| 10. SRM-04 authorization | Implement §4.4's accepted condition/result composition, exact quote scan, two-piece Evidence, P21 merge, diagnostics and approved fixtures only. |

### D05 — further verification constructions

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D05` — `DEFERRED`. |
| 2. Scientific source and baseline | §2.1/§2.3 support test, analysis and inspection categories; `VERIFY-UK-001` already defines three exact role constructions. |
| 3. Exact proposed choice | Retain `VERIFY-UK-002` in the inventory but add no first-slice grammar. |
| 4. Material alternatives | Approve synthetic `підтверджується` or vocabulary-only matching. Rejected as source-unsupported or semantically insufficient. |
| 5. Scientific defence | A method noun is not proof that it functions as the means of verification or that a procedure is reproducible. |
| 6. Domain/Evidence consequence | None. `VERIFY-UK-001` remains authoritative. |
| 7. Supporting cases | P09 and P10 are illustrative only. |
| 8. Known limitations | Recall remains limited to MVP constructions. |
| 9. Exact prerequisite | One source-attested new governing construction, exact role/boundary, false-positive rules and unresolved cases. |
| 10. SRM-04 authorization | None. |

### D06 — local relations versus reusable attachment

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D06` — `APPROVED_FOR_SRM04_FIRST_SLICE` for local-only relations; reusable attachment remains deferred. |
| 2. Scientific source and baseline | §2.1 condition/result and criterion meanings; §3.2 criterion chain; approved `ACCEPT-QUANT-001` already demonstrates bounded local containment without a universal engine. |
| 3. Exact proposed choice | Keep every first-slice relation inside its complete detector rule. `ACCEPT-UK-001` may reuse only the exact accepted leading `COND-UK-001`/`RESULT-UK-001` source partition; this is local composition, not a reusable relation. Defer `ATTACH-UK-001` and never make it a dependency of the approved rules. |
| 4. Material alternatives | Universal attachment engine or stored parser dependency edges. Rejected because no current consumer/semantics justify them. |
| 5. Scientific defence | A local rule can prove only the relation it needs; this prevents accidental generalization from punctuation or proximity. |
| 6. Domain/Evidence consequence | No relationship object. `ACCEPT-UK-001` records same-family copies of the exact condition and result spans as provenance; upstream cross-family IDs are not used as endpoints. Parser edges stay internal and non-evidentiary. |
| 7. Supporting cases | Corrected P01, P03, P07 and P21 show complete local relations; P22 prevents unconditional widening; P11–P13 show why a broader engine is deferred. |
| 8. Known limitations | Cross-observation relationship queries are unavailable. |
| 9. Remaining blocker | None for the approved first-slice rules; future `ATTACH-UK-001` needs the D07 contract and an actual consumer. |
| 10. SRM-04 authorization | Implement local checks only; do not add attachment infrastructure. |

### D07 — domain representation

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D07` — `APPROVED_FOR_SRM04_FIRST_SLICE` as **no domain change for first slice**; reusable relation representation `DEFERRED`. |
| 2. Scientific source and baseline | Existing `FeatureObservation.evidence_refs` supports several Evidence items; `RequirementExtractionResult` contains the six outcomes and accepted Evidence only. |
| 3. Exact proposed choice | Use multiple same-family Evidence refs to justify one observation for `RESULT-UK-002`, to preserve `ACCEPT-UK-001` condition plus result provenance, and to merge both acceptance rules on the P21 result span. Add no cross-family ref, target ID or relation collection. |
| 4. Material alternatives | Add provenance/anchor fields or a relation object now. Rejected as unnecessary for the bounded rules. |
| 5. Scientific defence | The approved Evidence contract permits multiple exact fragments and one source span supporting different justified features. Matching the acceptance condition-support fragment to accepted `COND-UK-001` by requirement ID and exact offsets preserves the source fact without violating §7.5.1's same-family ref invariant or leaking parser objects. |
| 6. Domain/Evidence consequence | Domain structures remain unchanged. P07 uses two acceptance refs; P21 uses three acceptance refs ordered deterministically. A future relation contract, if justified, must define stable endpoint identity, type, direction, cardinality, provenance, ordering, uncertainty, missing endpoints, parser failure and extraction-result location. |
| 7. Supporting cases | P03 demonstrates fragmented RESULT provenance; P07 demonstrates condition/result acceptance provenance; P21 demonstrates quantitative/literal same-result merging; P12–P13 demonstrate future relationship needs. |
| 8. Known limitations | No stored condition/result or method/criterion graph. |
| 9. Remaining blocker | For a future relation: approved consumer semantics and all fields listed above. None blocks first slice. |
| 10. SRM-04 authorization | Reuse current domain contracts only. |

### D08 — interaction, diagnostics and reference fixtures

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D08` — `APPROVED_FOR_SRM04_FIRST_SLICE`. |
| 2. Scientific source and baseline | Model-spec §§7.5, 7.7, 7.14.2 and 7.15.7–7.15.8 define exact Evidence, stable rule IDs, ordering and mixed outcomes. |
| 3. Exact proposed choice | Approve the corrected finite-condition grammar, parser-neutral head identities, explicit-condition boundary for literal acceptance, precedence, ownership, clause-level acceptance deduplication, Evidence IDs, source/tie ordering and diagnostics in §§4 and 6 together with binding fixtures P01–P04, P07–P08 and P14–P22. |
| 4. Material alternatives | Let old and new rules emit duplicate diagnostics or silently prefer accepted output. Rejected because mixed uncertainty and rule provenance would be lost. |
| 5. Scientific defence | Candidate ownership preserves one deterministic interpretation while leaving unrelated MVP segments unchanged. |
| 6. Domain/Evidence consequence | No domain change; SRM-04 may add only the approved rule IDs, Evidence IDs and diagnostic codes. Existing multi-ref observations represent RESULT fragments, conditioned literal provenance and P21's three-ref acceptance merge without parser data, cross-family refs or fabricated text. |
| 7. Supporting cases | P01–P04, P07–P08, P14–P22 and the four existing MVP regression anchors. |
| 8. Known limitations | P05–P06 and P09–P13 are illustrative and cannot be promoted by D08. |
| 9. Remaining prerequisite | Pinned-backend graph and degraded-annotation tests are mandatory SRM-04 validation; no unspecified scientific case semantics remain in the first slice. |
| 10. SRM-04 authorization | Implement only the approved corrected case matrix, exact neutral-annotation checks and interaction semantics; do not infer missing arcs or complete rules by engineering judgment. |

### D09 — singularity boundary

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D09` — `DEFERRED` to SRM-09/10. |
| 2. Scientific source and baseline | §2.1 Tables 2.1/2.3 discuss independent obligations; MVP has no singularity feature, characteristic or formula. |
| 3. Exact proposed choice | Treat multiple detected results only as structural observations. Do not infer independence, non-atomicity, `QUALITY_PROBLEM` or a score. |
| 4. Material alternatives | Clause-count defect or automatic singularity result. Rejected because grammatical coordination does not prove logical independence. |
| 5. Scientific defence | The source distinguishes independent obligations, a semantic decision not supplied by the bounded syntax. |
| 6. Domain/Evidence consequence | None in SRM-03. |
| 7. Supporting cases | P03 and P11 demonstrate multiple clauses without an automatic defect. |
| 8. Known limitations | SRM-03 cannot report singularity quality. |
| 9. Exact prerequisite | SRM-09/10 must approve inclusion, independence criterion, applicability, result representation and cases. |
| 10. SRM-04 authorization | None beyond preserving multiple result observations in one requirement. |

Approval of D01, D02, D04, D06, D07 and D08 as a consistent package is now
recorded in model-spec §7.14.16. The three-row first slice in §9 is authorized
without further scientific choices, subject to its mandatory pinned-backend
fixtures. D03 remains blocked; D05 and D09 remain deferred.

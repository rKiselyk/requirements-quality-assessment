# SRM-03 — Extended structural feature detection rules

**Status: PROPOSED_PENDING_RESEARCHER_APPROVAL.** This is a scientific and
operational proposal for SRM-04, not an amendment to the approved MVP v0.1
contract. No rule or new example in this document is an executable or binding
test case until the researcher resolves the listed decisions and records the
approved rule in [model-spec.md](model-spec.md).

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
dissertation passage motivates the observation. **Proposed rule** means a
possible deterministic specialization of that principle; the dissertation
does not itself approve its Ukrainian grammar. **Unresolved** identifies a
decision that cannot be filled by parser output or implementation judgment.

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

## 4. Proposed rule registry

All six IDs below are **provisional proposals, not allocated production IDs**.
The approved rule-ID policy in model-spec §7.7 applies only after researcher
approval and incorporation into `model-spec.md`. A proposed executable rule
uses the approved parser-neutral structures and exact Evidence contract; it
does not authorize implementation by itself.

| Candidate rule | First-slice disposition | Scientific reason |
| --- | --- | --- |
| `COND-UK-002` | `READY_FOR_RESEARCHER_APPROVAL` | The bounded comma-delimited postposed `якщо` template in §4.1 has one explicit MVP-compatible governing result and a complete UD-style relation, boundary, Evidence and diagnostic contract. It needs no general attachment engine. |
| `RESULT-UK-002` | `READY_FOR_RESEARCHER_APPROVAL` | The binary active-infinitive `і`/`та` construction in §4.2 has a closed syntax and selects multiple exact Evidence references for inherited normative scope. |
| `RESULT-UK-003` | `RESEARCH_BLOCKED` | The sources show nonmodal examples but provide no textual fact that distinguishes normative present tense from description. Parser syntax, source position and neighboring clauses cannot supply that force. |
| `ACCEPT-UK-001` | `READY_FOR_RESEARCHER_APPROVAL` | The exact-output subset in §4.4 uses a non-empty Ukrainian guillemet literal as a source-explicit oracle inside an accepted `RESULT-UK-001` result; it does not generalize all observable results into criteria. |
| `VERIFY-UK-002` | `DEFERRED_FROM_FIRST_SRM04_SLICE` | No additional source-attested verification-role construction is sufficiently specified beyond `VERIFY-UK-001`; the concept remains valid, but the synthetic `підтверджується` construction has no dissertation authority. |
| `ATTACH-UK-001` | `DEFERRED_FROM_FIRST_SRM04_SLICE` | The ready rules establish bounded local relations internally. A reusable cross-observation relationship has no approved consumer or domain representation yet and is unnecessary for the first slice. |

Shared mechanics for the three ready proposals are: operate on one original
trimmed `Requirement.text`; use only source-aligned parser-neutral annotations;
use zero-based Unicode code-point `[start_offset,end_offset)` spans; exclude
surrounding whitespace and sentence-final punctuation; preserve every exact
accepted span; allocate Evidence IDs independently per rule; and use the
model-spec §7.15.7 mixed-state derivation. The rule-specific sections close
their syntax, precedence, overlap, ordering and failure behavior. No rule below
uses nearest text, nearest clause or an undefined semantic classifier.

### 4.1 `COND-UK-002` — bounded postposed `якщо` condition

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Preserve explicit governing conditions in a multi-clause requirement without assigning them to the wrong result. |
| 2. Exact source | §2.1 Table 2.1, Completeness and Singularity rows; worked application §8 Table 7 R5′; model-spec §7.14.3 general-family discussion. |
| 3. MVP limitation | `COND-UK-001` covers only its edge templates and does not resolve internal/postposed `якщо`, nested or coordinated attachment. |
| 4. Feature / Feature ID | Existing `condition_contexts[]` / `condition_context`; no new family. |
| 5. Proposed Rule ID | `COND-UK-002` (provisional; `COND-UK-001` unchanged). |
| 6. Ukrainian construction | Exactly one binary source structure in one parser sentence and semicolon segment: `<one governing result>, <якщо-clause>`. The comma is mandatory. `якщо` is the only marker, matched as a complete token on the approved NFC plus Unicode `casefold()` view. No synonym, morphology generation or other marker is admitted. |
| 7. Parser annotations | Existing `SentenceAnnotation` and `TokenAnnotation` offsets, `lemma`, `upos`, morphology, `head_token_id`, and `dependency_relation`. The `якщо` token must be `mark` of one finite condition head; that head must be `advcl` of the governing result's lexical predicate. All referenced heads must be in the same sentence/segment. |
| 8. Deterministic recognition procedure | (1) Find exactly one comma followed only by whitespace and complete-token `якщо`. (2) Let the trimmed prefix before the comma be the governing-result interval and the suffix from `якщо` to the segment end be the condition interval. (3) Apply the normative subject/predicate requirements of `RESULT-UK-001` to the prefix interval, at absolute offsets, without invoking condition separation; require exactly one local subject, one approved normative surface, one connected lexical behavior predicate, no coordination and no negation. (4) Require `mark(якщо → condition-head)` and `advcl(condition-head → governing-result-predicate)`. (5) Require the source-contiguous subtree of the condition head, including `якщо`, to equal the whole trimmed suffix. Only then accept. This bounded local relation is part of the rule; `ATTACH-UK-001` is not called or stored. |
| 9. Evidence / offsets | One independent `Evidence` with `feature_id=CONDITION_CONTEXT`, `rule_id=COND-UK-002`, and the exact suffix from `якщо` through the last condition character, excluding terminal sentence punctuation. For the binding example it is `[32,55)` `якщо сервіс недоступний`. The governing result is not copied into condition Evidence. |
| 10. Attachment semantics | The required `advcl` edge locally establishes one condition → one result relationship for recognition only. It is not exported as a general relation. More than one result predicate, condition head, `якщо` marker or plausible governing predicate prevents acceptance. |
| 11. Positive example | `Система повинна зберегти запит, якщо сервіс недоступний.` has governing prefix `[0,30)` and accepted condition `[32,55)`. It yields one `condition_context` observation referencing `COND-UK-002:E001`. |
| 12. Negative example | `Система повинна показати слово «якщо» у довідці.` → the quoted word is no condition. |
| 13. False-positive boundary | `якщо` inside a matched `«…»` source interval is a completed negative, not a candidate. Other quoted/mentioned uses fail the required `mark`/`advcl` relations. No comma, more than one possible result, a coordinated/nested condition, a condition subtree smaller than the suffix, or a second condition marker is outside the accepted subset. No proximity rule is used. |
| 14. UNRESOLVED behavior | A source-shaped `,<space>якщо` candidate that fails unique result, subtree, `mark`/`advcl`, nesting or coordination checks produces `COND_POSTPOSED_YAKSHCHO_UNRESOLVED`, the complete exact suffix as `DiagnosticSpan` when its boundary is known, no observation and `INCOMPLETE`. Parser unavailability/failure/incomplete annotations/offset failure produces `COND_POSTPOSED_YAKSHCHO_PARSER_BLOCKED`, no Evidence and `INCOMPLETE`. With no source-shaped candidate, the rule is `COMPLETE` with no contribution. |
| 15. Applicability | Detect explicit text only; criterion applicability remains `UNKNOWN` unless an independent approved rule states otherwise. |
| 16. Known limitations | Only one comma-delimited postposed `якщо` clause and one simple normative result are covered. Leading `якщо` remains `COND-UK-001`; multiple, nested, coordinated and nonmodal structures remain outside this rule. |
| 17. Dependencies and interaction | Proposed dispatch checks this exact postposed form before `COND-UK-001`. An accepted or unresolved `COND-UK-002` candidate owns only that marker span, preventing the old `COND-UK-001` postposed-`якщо` diagnostic from duplicating it. Other markers and segments remain governed unchanged by `COND-UK-001`. Evidence IDs are `COND-UK-002:E001…` in accepted source order; identical `(feature_id,start,end)` output from the same rule is collapsed. No domain change and no `ATTACH-UK-001` dependency. |
| 18. Scientific approval | `READY_FOR_RESEARCHER_APPROVAL` / `PROPOSED_FOR_APPROVAL`. Approval would authorize only this bounded production contract after it is recorded in `model-spec.md`. |

### 4.2 `RESULT-UK-002` — coordinated results with explicit normative scope

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Preserve each separately observable result when one explicit normative construction governs coordinated predicates. |
| 2. Exact source | §2.1 Table 2.1, Completeness and Singularity rows; model-spec §7.14.4 family-level statement that each independent coordinated result is a separate observation. |
| 3. MVP limitation | `RESULT-UK-001` leaves coordinated predicate/`conj` scope unresolved. |
| 4. Feature / Feature ID | Existing `expected_results[]` / `expected_result`. |
| 5. Proposed Rule ID | `RESULT-UK-002` (provisional). |
| 6. Ukrainian construction | One parser sentence/semicolon segment of exact source shape `<explicit local subject> <one approved normative surface> <first active infinitive phrase> <і\|та> <second active infinitive phrase>`. Approved normative surfaces are exactly `повинен`, `повинна`, `повинні`, `має`, `мають`. Exactly two lexical predicates and one coordinator are allowed. A leading/postposed condition, comma, colon, dash or internal hard boundary is excluded from this first subset. |
| 7. Parser annotations | Existing parser-neutral offsets, `lemma`, `upos`, morphology, heads and UD-compatible relations. The first predicate must be `VERB` with `VerbForm=Inf` and connected to the normative construction through the `RESULT-UK-001` `xcomp`/`ccomp`/`aux`/`cop` chain. The second must be `VERB`, `VerbForm=Inf`, `dependency_relation=conj`, and head the first predicate. The exact source coordinator token is `і` or `та`, has `dependency_relation=cc`, and heads to the second predicate. One `nsubj`/`nsubj:*` belongs to the governing clause; no second local subject is allowed. |
| 8. Deterministic recognition procedure | (1) Segment exactly as `RESULT-UK-001`. (2) Require one normative surface and one local subject. (3) Require exactly the two infinitive predicate heads and coordination graph in item 7. (4) Reject any parser-visible `neg`, `або`, `чи`, adversative coordinator, second coordinator, additional lexical verb/participle, ellipsis, condition candidate or noncontiguous source mapping. (5) Let the first phrase run from segment start through the last non-whitespace character before the coordinator; let the second predicate phrase run from the first non-whitespace character after the coordinator through segment end, excluding terminal punctuation. Because no other verb or coordinator is allowed, every source-explicit complement/modifier in those intervals belongs to its respective predicate phrase; no semantic complement classifier is hidden in the rule. (6) Emit two observations. |
| 9. Evidence / offsets | **Selected representation: A, multiple exact Evidence references.** Allocate shared-anchor Evidence from the segment start through the normative token; first-result Evidence from segment start to before the coordinator; and second-predicate Evidence after the coordinator. The first observation references only the complete first-result Evidence. The second references the shared-anchor and second-predicate Evidence, in source order. This uses the already-approved ability of one observation to reference several exact Evidence items, preserves inherited force without invented text, and requires no new domain field. |
| 10. Attachment semantics | The `conj` plus `cc` graph and closed source template establish only inheritance of the explicit subject/normative scope by the second predicate. They do not attach an external condition, criterion or method and do not create a reusable relation object. |
| 11. Positive example | For `Система повинна зберегти запит і повідомити оператора.` allocate `RESULT-UK-002:E001=[0,15)` `Система повинна`, `E002=[0,30)` `Система повинна зберегти запит`, and `E003=[33,53)` `повідомити оператора`. Observation 1 references `(E002)`; observation 2 references `(E001,E003)`. The observations are distinguished by their predicate-bearing Evidence (`E002` versus `E003`). |
| 12. Negative example | `Система повинна показати напис «зберегти і повідомити».` → coordinated words in a quoted label are not two results. |
| 13. False-positive boundary | A coordinator not represented by the exact `cc`/`conj` graph, coordinated nouns/objects, quoted content, alternatives (`або`, `чи`), adversatives, negation, separate subjects, more than two predicates or any excluded boundary cannot produce two observations. |
| 14. UNRESOLVED behavior | A segment with a normative anchor and apparent two-verb `і`/`та` coordination that fails the closed graph, arity, boundary, subject, negation or exact-span checks produces `RESULT_COORD_UNRESOLVED_CANDIDATE` for the complete segment, no partial result from this segment, and `INCOMPLETE`. Parser blocking produces `RESULT_COORD_PARSER_BLOCKED`, no Evidence and `INCOMPLETE`. A quoted `і`/`та` with no two-verb coordination is a completed negative for this extension and falls through to `RESULT-UK-001`. |
| 15. Applicability | Structural detection does not decide whether more than one result is a singularity defect or change C/V applicability. |
| 16. Known limitations | This covers only binary active infinitive coordination with explicit shared normative force. It does not prove logical independence, support passive/coordinated finite predicates, or decide singularity. |
| 17. Dependencies and interaction | Proposed candidate dispatch precedes `RESULT-UK-001` for a segment with apparent two-verb `і`/`та` coordination. If accepted or unresolved, `RESULT-UK-002` owns the complete segment so `RESULT-UK-001` does not emit a duplicate result/diagnostic for it. With no such candidate, `RESULT-UK-001` is unchanged. Evidence IDs sort by `(start_offset,end_offset)`, giving E001, E002, E003 above; observations sort by predicate-bearing Evidence start, first predicate then second. Same-rule duplicate spans collapse. Mixed accepted segments plus an unresolved segment produce family `INCOMPLETE / DETECTED`. No `ATTACH-UK-001` or domain change is required. |
| 18. Scientific approval | `READY_FOR_RESEARCHER_APPROVAL` / `PROPOSED_FOR_APPROVAL`. Approval would authorize only this binary construction after recording it in `model-spec.md`. |

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
| 1. Scientific purpose | Preserve an explicit nonnumeric oracle against which fulfilment of a specified result can be judged. |
| 2. Exact source | §2.1 Table 2.1, Completeness and Verifiability rows; §2.3 ¶17–21; §3.2 Table 3.4 (expected behavior or condition); model-spec §7.14.5 family-level discussion. |
| 3. MVP limitation | `ACCEPT-QUANT-001` needs a contained, judgeable numeric anchor and cannot recognize a nonnumeric oracle. |
| 4. Feature / Feature ID | Existing `acceptance_criteria[]` / `acceptance_criterion`. |
| 5. Proposed Rule ID | `ACCEPT-UK-001` (provisional; `ACCEPT-QUANT-001` unchanged). |
| 6. Ukrainian construction | Narrow exact-output template inside one accepted `RESULT-UK-001` result: lexical predicate lemma and complete source token `показати`; its direct object has lemma and complete source token `повідомлення`; immediately after that object, ignoring only Unicode whitespace, is one non-empty, non-nested Ukrainian guillemet literal `«…»`. A leading condition may already have been separated by `COND-UK-001`. No other output verb, object noun or quote style is included. |
| 7. Parser annotations | The already accepted `RESULT-UK-001` observation/Evidence; source-aligned predicate and object tokens; `dependency_relation=obj` from `повідомлення` to `показати`; token offsets and sentence boundary. Quote boundaries are recognized directly in the original result Evidence, not inferred from parser punctuation. |
| 8. Deterministic recognition procedure | (1) Reuse accepted `RESULT-UK-001` results only. (2) Within one result Evidence span, require the exact predicate/object relation in items 6–7. (3) Require exactly one `«` and its following `»`, non-empty interior, no nested `«`/`»`, and no non-whitespace source characters between `повідомлення` and `«`. (4) Require the closing `»` to be the last non-whitespace character of result Evidence. The literal is an exact expected output and therefore a source-explicit test oracle for that behavior. (5) Emit one clause-level criterion. No general semantic judgeability algorithm is invoked. |
| 9. Evidence / offsets | Independent `acceptance_criterion` Evidence is exactly the complete accepted `RESULT-UK-001` result clause and uses `rule_id=ACCEPT-UK-001`; it does not reuse the result Evidence ID. In the binding example the criterion is `[25,83)` `система повинна показати повідомлення «Сервіс недоступний»`; the exact oracle is contained at `[63,83)` with content `[64,82)`. |
| 10. Attachment semantics | Complete source-span equality with the accepted result establishes a local criterion → result composition. The criterion judges only the exact displayed-message behavior in that result. No reusable relationship object or `ATTACH-UK-001` link is required. |
| 11. Positive example | `Якщо сервіс недоступний, система повинна показати повідомлення «Сервіс недоступний».` has existing condition `[0,23)`, accepted result `[25,83)`, and one proposed acceptance observation with its own `[25,83)` Evidence. |
| 12. Negative example | `Система повинна показати зрозуміле повідомлення.` has no specified observable content or separately approved sufficiency rule. |
| 13. False-positive boundary | A result without the exact predicate/object pair, unquoted or empty output, another quote style, nested/multiple literals, text after the closing guillemet, a method name, a subjective adjective or a test link is not accepted. No automatic equivalence of result and criterion is introduced. |
| 14. UNRESOLVED behavior | If the accepted result contains the exact `показати повідомлення` pair but guillemet pairing, nesting, object attachment or result boundary cannot be determined, emit `ACCEPT_LITERAL_UNRESOLVED_CANDIDATE` for the result span, no criterion, and `INCOMPLETE`. If the required result dependency is parser-blocked, emit `ACCEPT_LITERAL_DEPENDENCY_BLOCKED`, no Evidence and `INCOMPLETE`. If the exact pair is absent, or a determinate empty/unquoted output is present, the rule contributes nothing and completes. |
| 15. Applicability | A nonnumeric criterion can be relevant without making every requirement's criterion universally mandatory; SRM-09 governs type-specific applicability. |
| 16. Known limitations | The rule proves only that the exact message output is judgeable; it does not prove complete requirement fulfilment, usability, domain correctness, procedure quality or test execution. Other nonnumeric states remain outside coverage. |
| 17. Dependencies and interaction | Depends only on accepted `RESULT-UK-001`. It runs independently of `ACCEPT-QUANT-001`. Same-rule duplicate spans collapse; a clause independently satisfying both rules retains two observations and separate Evidence/rule provenance because it has two distinct criterion justifications. Their common span is allowed and does not increase any existing boolean family contribution. IDs are `ACCEPT-UK-001:E001…` in source order. Mixed accepted/unresolved candidates use §7.15.7 semantics. No domain change, `RESULT-UK-002/003`, `ATTACH-UK-001`, formula or applicability change is required. |
| 18. Scientific approval | `READY_FOR_RESEARCHER_APPROVAL` / `PROPOSED_FOR_APPROVAL`. Approval would authorize only this exact-message subset after recording it in `model-spec.md`. |

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
| 18. Scientific approval | `DEFERRED_FROM_FIRST_SRM04_SLICE`. It must not block the three ready rules and is excluded from SRM-04 first-slice implementation. |

## 5. Multi-clause and attachment semantics

One sentence can contain several accepted observations in one `Requirement`.
Clause count does not create more requirement objects, a singularity defect or
a score. SRM-03 separates three different meanings that the earlier draft had
incorrectly grouped under `ATTACH-UK-001`:

| Concept | First-slice contract |
| --- | --- |
| Local relation established by one bounded detector | The relation exists only as a recognition condition inside that rule. `COND-UK-002` uses one exact `advcl` edge to one result; `RESULT-UK-002` uses a closed `conj`/`cc` graph for inherited normative scope; `ACCEPT-UK-001` uses equality with one accepted result Evidence span; `ACCEPT-QUANT-001` keeps its approved containment rule. These relationships require no new domain object. |
| Reusable typed relationship between independently accepted observations | Deferred with `ATTACH-UK-001`. The current first slice has no consumer requiring stored cross-observation links. `evidence_refs` must not be overloaded to simulate endpoints. |
| Unresolved semantic relationship | Independently supported endpoint observations remain available. The affected bounded detector emits its own diagnostic when the ambiguity prevents its observation; otherwise no relationship is stored. Uncertainty is never replaced by a chosen nearest target. |

The required uncertainty distinctions remain:

| Relationship case | Treatment |
| --- | --- |
| Supported unambiguous attachment | Accept only under the complete local rule that defines both endpoints and the exact structural path or containment relation. |
| Multiple scientifically justified relationships | Outside the three ready subsets. A future typed contract must preserve every supported pair rather than select one. |
| Ambiguous attachment | Withhold the dependent observation/link and emit a source-bound rule diagnostic when the candidate boundary is known. |
| Missing attachment information | Preserve independent observations; create no relation and no fake Evidence. |
| Unsupported syntax or unreliable parser output | Apply the consuming detector's parser-blocked/incomplete outcome; never treat it as `NOT_DETECTED`. |

No nearest-token, nearest-clause, shortest-distance, first/last-result or
punctuation-only semantic fallback is permitted. Punctuation can define a
source interval only where a complete rule such as `COND-UK-002` also requires
the specified parser relation. The approved `ACCEPT-QUANT-001` containment
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
jointly justify **one** result; they are not endpoints of a reusable relation.
`COND-UK-002` and `ACCEPT-UK-001` use one Evidence item per observation. No
ready proposal adds a domain field or changes `RequirementExtractionResult`.
Parser edges remain internal recognition inputs and are never accepted Evidence.
Actor/action/object fields remain deferred under model-spec §7.11.

Rule interaction is deterministic:

- `COND-UK-002` claims only its exact postposed `якщо` candidate before
  `COND-UK-001`; other condition candidates keep existing behavior.
- `RESULT-UK-002` claims only an apparent binary two-verb `і`/`та` segment
  before `RESULT-UK-001`; quoted/noun coordination falls through to the MVP
  rule, while a structurally apparent but unresolved result candidate remains
  incomplete and is not reduced to a single result.
- `ACCEPT-UK-001` consumes accepted `RESULT-UK-001` output and runs independently
  of `ACCEPT-QUANT-001`. Independent semantic justifications retain separate
  observations/Evidence even when their clause spans are equal.
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

Rows P01–P04, P07–P08 and P14–P20 are the **proposed approval fixtures** for the
three ready rules. Their statuses below describe the proposed rule contribution;
family merging then follows §6. P05–P06 and P09–P13 are explicitly
`ILLUSTRATIVE_ONLY` because their rules are blocked or deferred. No illustrative
row can become an SRM-04 test. All offsets are zero-based Unicode code-point,
start-inclusive/end-exclusive positions in the exact trimmed input.

| Case and exact input | Rule / observations and Evidence | Processing, detection and diagnostic | Explanation / status |
| --- | --- | --- | --- |
| P01 `Система повинна зберегти запит, якщо сервіс недоступний.` | `COND-UK-002`: one `condition_context`; `COND-UK-002:E001=[32,55)` `якщо сервіс недоступний` | `COMPLETE / DETECTED`; no diagnostic | Exact comma + postposed marker, one normative result prefix and the proposed `mark`/`advcl` relation. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P02 `Система повинна показати слово «якщо» у довідці.` | `COND-UK-002`: no observation or Evidence; quoted token candidate `[32,36)` is excluded | `COMPLETE / NOT_DETECTED`; no diagnostic | `якщо` is inside `[31,37)` `«якщо»` and cannot satisfy the condition relation. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P03 `Система повинна зберегти запит і повідомити оператора.` | `RESULT-UK-002`: result 1 refs `E002`; result 2 refs `E001,E003`. `E001=[0,15)` `Система повинна`; `E002=[0,30)` `Система повинна зберегти запит`; `E003=[33,53)` `повідомити оператора` | `COMPLETE / DETECTED`; no diagnostic | Binary active-infinitive `і` coordination with exact shared scope and no invented text. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P04 `Система повинна показати напис «зберегти і повідомити».` | `RESULT-UK-002`: no new observation/Evidence; quoted text `[32,53)` has no two-verb `conj`/`cc` graph | Extension contribution `COMPLETE / NOT_DETECTED`; no diagnostic; segment falls through unchanged to `RESULT-UK-001` | Quoted coordinator cannot create another result. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P05 `Якщо сервіс недоступний, події зберігаються у черзі.` | `RESULT-UK-003` candidate result `[25,51)`; no accepted Evidence | No proposed processing/detection contract | Present tense does not establish normative force. `RESEARCH_BLOCKED / ILLUSTRATIVE_ONLY`. |
| P06 `У журналі зазначено, що події зберігаються у черзі.` | `RESULT-UK-003` descriptive clause `[24,50)`; no accepted Evidence | No proposed processing/detection contract | Demonstrates why syntax alone cannot distinguish force. `RESEARCH_BLOCKED / ILLUSTRATIVE_ONLY`. |
| P07 `Якщо сервіс недоступний, система повинна показати повідомлення «Сервіс недоступний».` | `ACCEPT-UK-001`: one `acceptance_criterion`; `ACCEPT-UK-001:E001=[25,83)` `система повинна показати повідомлення «Сервіс недоступний»`; contained oracle `[63,83)`, content `[64,82)` | `COMPLETE / DETECTED`; no diagnostic | Accepted `RESULT-UK-001` result contains the exact predicate/object and non-empty guillemet oracle. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P08 `Система повинна показати зрозуміле повідомлення.` | `ACCEPT-UK-001`: no observation/Evidence; result candidate `[0,47)` has no literal oracle | `COMPLETE / NOT_DETECTED`; no diagnostic | A subjective adjective is not an exact output oracle. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P09 `Виконання підтверджується інспекцією журналу.` | `VERIFY-UK-002` candidate method `[26,44)`; no proposed Evidence | No proposed processing/detection contract | `підтверджується` is synthetic and not source-authorized. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P10 `Система створює тестовий випадок.` | Artifact phrase `[16,32)`; no `VERIFY-UK-002` Evidence | No proposed processing/detection contract; existing `VERIFY-UK-001` remains authoritative | Names an artifact/system behavior, not a new verification-role construction. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P11 `Якщо сервіс недоступний, система повинна зберегти запит і повідомити оператора.` | Condition `[0,23)` and result candidates `[25,55)`, `[58,78)`; no relationship Evidence | No `ATTACH-UK-001` result | Leading-condition plus coordinated-result scope is outside the ready binary result subset. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P12 `Система повинна зберегти запит і повідомити оператора при перевірці.` | Ambiguous phrase `[54,67)` `при перевірці`; no relationship Evidence | No `ATTACH-UK-001` result | Neither source order nor proximity selects a target. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P13 `Система повинна зберегти запит; перевірка: інспекція журналу.` | Existing method candidate `[43,60)` and result `[0,30)` remain independent; no relationship Evidence | Existing `VERIFY-UK-001` governs method detection; no `ATTACH-UK-001` result | A method observation does not prove which result/criterion it verifies. `DEFERRED / ILLUSTRATIVE_ONLY`. |
| P14 `Система повинна зберегти запит і повідомити оператора.` with parsed text present but required coordination annotation incomplete | `RESULT-UK-002`: no observation/Evidence; affected candidate `[0,53)` | `INCOMPLETE / UNRESOLVED`; `RESULT_COORD_PARSER_BLOCKED` with `DiagnosticSpan=[0,53)` | Missing required annotation cannot become absence. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P15 `Система повинна зберегти запит якщо сервіс недоступний.` | `COND-UK-002`: no observation/Evidence; marker phrase `[31,54)` lacks the mandatory comma | Extension contribution `COMPLETE / NOT_DETECTED`; no diagnostic; existing rules remain authoritative | Explicitly bounds the new rule; whitespace/position cannot replace the comma template. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P16 `Система повинна зберегти запит і повідомити оператора, якщо сервіс недоступний.` | `COND-UK-002`: no observation/Evidence; condition candidate `[55,78)` | `INCOMPLETE / UNRESOLVED`; `COND_POSTPOSED_YAKSHCHO_UNRESOLVED` with `DiagnosticSpan=[55,78)` | The prefix has more than one result predicate, so this rule cannot select a unique target. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P17 `Система повинна зберегти запит і не повідомляти оператора.` | `RESULT-UK-002`: no observation/Evidence; segment candidate `[0,57)` | `INCOMPLETE / UNRESOLVED`; `RESULT_COORD_UNRESOLVED_CANDIDATE` with `DiagnosticSpan=[0,57)` | Parser-visible negation is excluded; the detector does not invert or discard it. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P18 `Система повинна зберегти запит або повідомити оператора.` | `RESULT-UK-002`: no observation/Evidence; alternative coordinator `[31,34)` | Extension contribution `COMPLETE / NOT_DETECTED`; no extension diagnostic; segment falls through to existing `RESULT-UK-001` behavior | `або` is not an approved shared-obligation coordinator for this rule. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P19 `Система повинна показати повідомлення «».` | `ACCEPT-UK-001`: no observation/Evidence; accepted result candidate `[0,40)` contains empty literal `[38,40)` | `COMPLETE / NOT_DETECTED`; no diagnostic | Empty output is deterministically insufficient, not an ambiguous oracle. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |
| P20 `Система повинна показати повідомлення «Помилка «E1»».` | `ACCEPT-UK-001`: no observation/Evidence; affected result `[0,52)`, nested literal `[38,52)` | `INCOMPLETE / UNRESOLVED`; `ACCEPT_LITERAL_UNRESOLVED_CANDIDATE` with `DiagnosticSpan=[0,52)` | The bounded rule does not choose inner/outer quote semantics. `PROPOSED_PENDING_RESEARCHER_APPROVAL`. |

MVP regression anchors below are **existing approved behavior**, not new SRM-03
reference cases; their exact results remain governed by model-spec §§7.14.3–7.14.7:

| Existing sentence | Target observation; relevant exact source span | Existing Rule ID; approved outcome | Source / status |
| --- | --- | --- | --- |
| `Якщо сервіс недоступний, система повинна зберегти запит.` | Condition `[0,23)` `Якщо сервіс недоступний`; result `[25,55)` `система повинна зберегти запит` | `COND-UK-001`, `RESULT-UK-001`; both `DETECTED` | model-spec §§7.14.3.1, 7.14.4.1; **EXISTING_APPROVED_MVP** |
| `Система повинна відповісти не більше ніж за 2 с.` | Complete criterion `[0,47)` `Система повинна відповісти не більше ніж за 2 с` | `ACCEPT-QUANT-001`; `DETECTED` | model-spec §7.14.5.1; **EXISTING_APPROVED_MVP** |
| `Виконання перевіряється навантажувальним тестом.` | Method `[24,47)` `навантажувальним тестом` | `VERIFY-UK-001`; `DETECTED` | model-spec §7.14.7.1; **EXISTING_APPROVED_MVP** |
| `Система контролює обробку запитів.` | Apparent candidate `[0,33)`; no accepted Evidence | `RESULT-UK-001`; `UNRESOLVED` | model-spec §7.14.4.1; **EXISTING_APPROVED_MVP** |

**Offset validation record.** A temporary Unicode code-point validation script
checked every explicit span in P01–P20 and the four MVP anchors against the
literal sentence stored in this section. All 38 checked spans across 24 cases
satisfied `source[start_offset:end_offset] == expected_text`. The script was
not added to the repository and the application test suite was not run.

## 8. Compatibility with MVP v0.1

The reader, six-family registry, approved detectors, exact Evidence contract,
parser-neutral boundary, C/V/U calculators, `RequirementQualityProfile`,
specification aggregation and console presentation are unchanged. Existing
`COND-UK-001`, `RESULT-UK-001`, `ACCEPT-QUANT-001`, `VERIFY-UK-001`,
`QUANT-001`, `QUANT-UK-001` and `UK-VAGUE-001` keep their approved scope and
IDs. New candidate rules must be distinguishable from those baselines and
must not alter their prior binding cases. One non-empty line remains one
requirement. A recognized extra clause is an observation within that object,
not a new requirement ID. An unsupported extra candidate is neither evidence
of absence nor a confirmed defect. No new actor/action/object feature is
introduced merely because the parser exposes a dependency tree.

## 9. Dependencies and SRM-04 implementation handoff

The following is the proposed bounded handoff. Nothing may be implemented until
the researcher approves the applicable decision package and the resulting rule
is recorded in `model-spec.md`.

| Rule ID | Disposition | Exact supported subset | Required scientific approval | Required domain change | Required reference cases | SRM-04 implementation scope | Excluded behavior |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `COND-UK-002` | `READY_FOR_RESEARCHER_APPROVAL` | One comma-delimited postposed `якщо` clause whose complete suffix subtree is `advcl` of exactly one simple MVP normative result predicate | D01 and D08 | None | P01, P02, P15, P16, plus parser-blocked fixture | Add rule-specific candidate dispatch, exact parser checks, Evidence/diagnostics and family merge; preserve `COND-UK-001` elsewhere | Other markers; no comma; multiple/nested/coordinated conditions; several results; nonmodal governing result; general attachment |
| `RESULT-UK-002` | `READY_FOR_RESEARCHER_APPROVAL` | Exactly two active infinitive predicates coordinated by source `і`/`та` under one explicit MVP normative subject/anchor | D02 and D08 | None; multiple existing Evidence refs are sufficient | P03, P04, P14, P17, P18; more-than-two case follows the same explicit arity exclusion | Add binary candidate dispatch, three-piece Evidence construction, two observations, diagnostics and merge precedence | Passive/finite coordination; more than two results; `або`/`чи`; negation; conditions; ellipsis; separate subjects; singularity judgment |
| `RESULT-UK-003` | `RESEARCH_BLOCKED` | None | A future decision supplying independently observable normative force | Undetermined | P05–P06 remain illustrative | No SRM-04 work | All present-tense/nonmodal result inference, including worked R5′ |
| `ACCEPT-UK-001` | `READY_FOR_RESEARCHER_APPROVAL` | Accepted `RESULT-UK-001` clause with exact `показати` → `повідомлення` object and one final non-empty `«…»` literal | D04 and D08 | None | P07, P08, P19, P20 | Compose existing result output into independent acceptance Evidence/observation; add diagnostics and merge independently with `ACCEPT-QUANT-001` | Other verbs/nouns/quote styles; unquoted/vague outputs; general states; result from `RESULT-UK-002/003`; domain judgeability |
| `VERIFY-UK-002` | `DEFERRED_FROM_FIRST_SRM04_SLICE` | None beyond existing `VERIFY-UK-001` | Future source-backed construction decision | None yet | P09–P10 illustrative only | No SRM-04 work | Synthetic governing verbs, vocabulary-only detection and reproducibility claims |
| `ATTACH-UK-001` | `DEFERRED_FROM_FIRST_SRM04_SLICE` | No reusable relationship; bounded local relations remain inside their detector rules | Future consumer plus complete typed-relation decision | Future stable observation identity and relation structure, only if approved | P11–P13 illustrative only | No SRM-04 work | Universal pairing, distance fallbacks, exported parser edges and inferred one-to-many links |

The proposed **first SRM-04 slice** is exactly `COND-UK-002`,
`RESULT-UK-002`, and `ACCEPT-UK-001` after approval. It may add detector
implementations and directly related tests only. It must not add a relationship
engine, change feature families/domain models, implement `RESULT-UK-003` or
`VERIFY-UK-002`, decide singularity, alter applicability/calculators, or continue
into SRM-05+. Rejection or partial approval removes the affected row from the
slice without changing MVP behavior.

## 10. Researcher Approval Package — SRM-03

Every choice below remains unapproved. `PROPOSED_FOR_APPROVAL` means the
scientific/operational choice is complete enough for an explicit researcher
decision; it does not mean accepted. `RESEARCH_BLOCKED` and `DEFERRED` items do
not enter the first SRM-04 slice.

### D01 — bounded postposed `якщо`

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D01` — `PROPOSED_FOR_APPROVAL`. |
| 2. Scientific source and baseline | §2.1 Table 2.1 condition/reaction completeness; worked R5′; `COND-UK-001` marker/offset mechanics and its deliberate postposed-`якщо` gap. |
| 3. Exact proposed choice | Approve `COND-UK-002` exactly as §4.1: comma-required `<one simple normative result>, якщо <one suffix condition>`, complete-token marker, `mark` + `advcl` to one governing predicate, complete suffix subtree, one condition Evidence. |
| 4. Material alternatives | General attachment engine; marker/comma regex alone; all postposed subordinate clauses. Rejected because they add unnecessary domain machinery or cannot prove the target. |
| 5. Scientific defence | The source establishes explicit condition plus reaction as meaningful; the proposal observes both explicitly and restricts attachment through a standard parser-neutral relation rather than distance. |
| 6. Domain/Evidence consequence | Existing `condition_context`; no domain field. One exact Evidence item and two new diagnostic codes. Local relation is not exported. |
| 7. Supporting cases | P01 positive, P02 quoted negative, P15 no-comma negative, P16 multiple-result unresolved; parser-blocked handling is fixed by §4.1/model-spec §7.15.8. |
| 8. Known limitations | One marker, one comma, one result and one condition only; no coordinated/nested/nonmodal coverage. |
| 9. Remaining blocker | Researcher approval and recording in `model-spec.md`; no further scientific algorithm is missing for this subset. |
| 10. SRM-04 authorization | Implement the §4.1 detector contribution, precedence, Evidence, diagnostics and directly related approved cases. |

### D02 — binary coordinated normative results

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D02` — `PROPOSED_FOR_APPROVAL`. |
| 2. Scientific source and baseline | §2.1 Completeness/Singularity; model-spec §7.14.4 states independent coordinated results are separate observations but leaves general coordination outside `RESULT-UK-001`. |
| 3. Exact proposed choice | Approve only two active infinitives under one explicit MVP normative subject/anchor, with source `і`/`та`, exact `conj`/`cc` graph, no conditions/negation/alternatives/extra verbs. Select multiple exact Evidence refs: shared subject+anchor plus the second predicate phrase. |
| 4. Material alternatives | One covering span for both results obscures which predicate constitutes result 2; predicate-only Evidence loses normative force; a new provenance field is unnecessary. Existing multi-Evidence observations preserve both facts exactly. |
| 5. Scientific defence | The explicit normative anchor and closed dependency graph establish shared force; exact source fragments avoid invented text and preserve explainability. |
| 6. Domain/Evidence consequence | No domain change. Three exact Evidence items support two existing `FeatureObservation`s; rule-specific tie order and diagnostics are fixed in §4.2. |
| 7. Supporting cases | P03 positive, P04 quoted negative, P14 blocked annotation, P17 negation unresolved, P18 alternative negative; arity greater than two is explicitly excluded by §4.2. |
| 8. Known limitations | Binary active infinitives only; no logical-independence or singularity conclusion. |
| 9. Remaining blocker | Researcher approval and `model-spec.md` recording; no Evidence representation choice remains open. |
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
| 1. Decision ID / status | `D04` — `PROPOSED_FOR_APPROVAL`. |
| 2. Scientific source and baseline | §2.1 Table 2.1 permits criterion/test oracle; §3.2 Table 3.4 permits expected behavior; `ACCEPT-QUANT-001` covers only numeric judgeability. |
| 3. Exact proposed choice | Approve `ACCEPT-UK-001` only for an accepted `RESULT-UK-001` containing exact `показати` → `повідомлення` object and one final non-empty `«…»` literal. Treat the literal as an oracle for that displayed output only. |
| 4. Material alternatives | Every observable result, adjective-based message quality, general state semantics or other output verbs. Rejected because judgeability would depend on unapproved domain interpretation. |
| 5. Scientific defence | An exact literal yields a reproducible equality observation for the stated behavior; the rule makes no claim about complete requirement fulfilment. |
| 6. Domain/Evidence consequence | Existing acceptance family; one independent Evidence equal to the accepted result span; no relationship/domain field. Separate provenance from quantitative acceptance is retained. |
| 7. Supporting cases | P07 positive, P08 unquoted negative, P19 empty-literal negative and P20 nested-literal unresolved. |
| 8. Known limitations | Only exact displayed messages; no general nonnumeric state, usability or domain-correctness judgment. |
| 9. Remaining blocker | Researcher approval and `model-spec.md` recording; no general judgeability algorithm is needed for this subset. |
| 10. SRM-04 authorization | Implement §4.4 composition, exact quote scan, Evidence/diagnostics and approved fixtures. |

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
| 1. Decision ID / status | `D06` — `PROPOSED_FOR_APPROVAL` for first-slice architecture. |
| 2. Scientific source and baseline | §2.1 condition/result and criterion meanings; §3.2 criterion chain; approved `ACCEPT-QUANT-001` already demonstrates bounded local containment without a universal engine. |
| 3. Exact proposed choice | Keep every first-slice relation inside its complete detector rule. Defer reusable `ATTACH-UK-001`; never make it a dependency of `COND-UK-002`, `RESULT-UK-002` or `ACCEPT-UK-001`. |
| 4. Material alternatives | Universal attachment engine or stored parser dependency edges. Rejected because no current consumer/semantics justify them. |
| 5. Scientific defence | A local rule can prove only the relation it needs; this prevents accidental generalization from punctuation or proximity. |
| 6. Domain/Evidence consequence | No relationship object. Endpoint Evidence remains within observations; parser edges stay internal and non-evidentiary. |
| 7. Supporting cases | P01/P03/P07 show local relations; P11–P13 show why a broader engine is deferred. |
| 8. Known limitations | Cross-observation relationship queries are unavailable. |
| 9. Remaining blocker | None for ready rules; future `ATTACH-UK-001` needs the D07 contract and an actual consumer. |
| 10. SRM-04 authorization | Implement local checks only; do not add attachment infrastructure. |

### D07 — domain representation

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D07` — `PROPOSED_FOR_APPROVAL` as **no domain change for first slice**; reusable relation representation `DEFERRED`. |
| 2. Scientific source and baseline | Existing `FeatureObservation.evidence_refs` supports several Evidence items; `RequirementExtractionResult` contains the six outcomes and accepted Evidence only. |
| 3. Exact proposed choice | Use multiple Evidence refs only to justify one observation (`RESULT-UK-002`). Add no target IDs or relation collection. |
| 4. Material alternatives | Add provenance/anchor fields or a relation object now. Rejected as unnecessary for the bounded rules. |
| 5. Scientific defence | The approved Evidence contract already represents all exact source facts needed by the first slice without leaking parser objects. |
| 6. Domain/Evidence consequence | Domain structures remain unchanged. A future relation contract, if justified, must define stable endpoint identity, type, direction, cardinality, provenance, ordering, uncertainty, missing endpoints, parser failure and extraction-result location. |
| 7. Supporting cases | P03 demonstrates sufficient multi-Evidence representation; P12–P13 demonstrate future relationship needs. |
| 8. Known limitations | No stored condition/result or method/criterion graph. |
| 9. Remaining blocker | For a future relation: approved consumer semantics and all fields listed above. None blocks first slice. |
| 10. SRM-04 authorization | Reuse current domain contracts only. |

### D08 — interaction, diagnostics and reference fixtures

| Approval-package item | Disposition |
| --- | --- |
| 1. Decision ID / status | `D08` — `PROPOSED_FOR_APPROVAL`. |
| 2. Scientific source and baseline | Model-spec §§7.5, 7.7, 7.14.2 and 7.15.7–7.15.8 define exact Evidence, stable rule IDs, ordering and mixed outcomes. |
| 3. Exact proposed choice | Approve the precedence, ownership, deduplication, Evidence IDs, source/tie ordering and diagnostics in §§4 and 6 together with proposed fixtures P01–P04, P07–P08 and P14–P20. |
| 4. Material alternatives | Let old and new rules emit duplicate diagnostics or silently prefer accepted output. Rejected because mixed uncertainty and rule provenance would be lost. |
| 5. Scientific defence | Candidate ownership preserves one deterministic interpretation while leaving unrelated MVP segments unchanged. |
| 6. Domain/Evidence consequence | No domain change; only new rule IDs, Evidence IDs and diagnostic codes after approval. |
| 7. Supporting cases | P01–P04, P07–P08, P14–P20 and the four existing MVP regression anchors. |
| 8. Known limitations | P05–P06 and P09–P13 are illustrative and cannot be promoted by D08. |
| 9. Remaining blocker | Researcher approval of the rule contracts and proposed fixture set, followed by recording them in `model-spec.md`; no unspecified case semantics remain in the first slice. |
| 10. SRM-04 authorization | Implement only the approved case matrix and interaction semantics; no rule completion by engineering judgment. |

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

Approval of D01, D02, D04, D06, D07 and D08 as a consistent package would
make the three-row first slice in §9 implementable without further scientific
choices. D03 remains blocked; D05 and D09 remain deferred. Approval must be
recorded in `model-spec.md` by the researcher before SRM-04 begins.

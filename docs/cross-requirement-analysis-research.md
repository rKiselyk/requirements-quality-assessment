# Cross Requirement Analysis Research Contract

**Branch:** `research/cross-requirement-analysis`  
**Baseline:** `main` at `9b27ee52992eb76fa97f8eb89bc4113f52abc4fb`
(merged PR #112)  
**Document status:** `RESEARCH_ONLY / PROPOSED_FOR_RESEARCHER_REVIEW`  
**Decision effect:** none; this document records source-backed conclusions,
alternatives, and unresolved decisions only  
**Implementation effect:** none; no production contract, Rule ID, detector,
formula, threshold, vocabulary, ontology, projection, or domain class is
approved by this document

## 1. Research objective and scope

This research round establishes the scientific and architectural questions that
must be closed before Cross-Requirement Analysis can be implemented. Its first
focus is specification-level Consistency: whether requirements in one
specification can be satisfied together without logical, terminological, or
resource conflict.

The accepted Single Requirement Analysis baseline remains frozen. The current
`RequirementReader -> FeatureExtractor -> RequirementAssessmentRecord ->
RequirementQualityProfile(C,V,U)` path and the current
`SpecificationQualityProfile(C_file,V_file,U_file)` aggregation are inputs and
adjacent results, not objects of modification. No detector coverage, C/V/U
formula, production domain type, pipeline stage, or reporter behavior is
changed here. **Classification: `SOURCE_DEFINED` for the separation between
individual and specification levels; `DIRECTLY_DERIVABLE` for preserving the
accepted production baseline.**

This document uses four conclusion classes:

- `SOURCE_DEFINED`: stated by the dissertation or the authoritative model
  specification;
- `DIRECTLY_DERIVABLE`: follows without selecting a new scientific formula,
  threshold, vocabulary, heuristic, or semantic rule;
- `RESEARCHER_DECISION_REQUIRED`: two or more scientifically plausible
  operationalizations remain, or an implementation-facing rule is absent; and
- `DEFERRED`: deliberately excluded from the first bounded cross-analysis
  slice.

The target of this round is a research contract, not an executable Consistency
assessment. **Classification: `SOURCE_DEFINED` for the need to define each
metric's object, applicability, reproducible algorithm, polarity, source, and
semantic context; `RESEARCHER_DECISION_REQUIRED` for every missing item listed
in Sections 16 and 17.**

## 2. Source traceability

### 2.1 Source hierarchy applied

The research used the requested hierarchy:

1. dissertation material in [`docs/reference/`](reference/README.md);
2. the implementation-facing authority
   [`docs/model-spec.md`](model-spec.md);
3. current production domain and pipeline code;
4. tests as executable conformance evidence; and
5. repository decisions and GitHub issues.

As of this baseline, GitHub issue
[#68 (`SRM-00`)](https://github.com/rKiselyk/requirements-quality-assessment/issues/68)
explicitly excludes cross-requirement consistency from the Single Requirement
milestone, and issue
[#14 (`MVP-SPEC`)](https://github.com/rKiselyk/requirements-quality-assessment/issues/14)
keeps the broader model draft open while preserving the
implemented C/V/U subset. No inspected open issue supplies an approved
cross-requirement conflict or confirmation contract. **Classification:
`SOURCE_DEFINED` for the exclusion from the completed single-requirement
scope; `RESEARCHER_DECISION_REQUIRED` for the new contract.**

### 2.2 Primary source map

| Source | Relevant material | Source-backed contribution |
| --- | --- | --- |
| [`2.1 Властивості вимог`](reference/2.1_Властивості_вимог.docx) | §2.1 paragraphs 5, 11, 14-16; Tables 2.1-2.3 | Separates individual and set levels; defines set Consistency as absence of logical, terminological, and resource conflicts; distinguishes direct and indirect conflicts; warns that indirect conflicts can require dependency models or expert review. |
| [`2.2 Взаємозвязок вимог і якості`](reference/2.2_Взаємозвязок_вимог_і_якості.docx) | §2.2 paragraphs 2-5, 12-21, 26; Tables 2.5-2.6 | Separates requirement-artifact quality from product quality; preserves semantic context and characteristic-specific subsets; treats contradictory requirements as risk factors rather than product-quality values. |
| [`2.3 Система метрик`](reference/2.3_Система_метрик.docx) | §2.3 paragraphs 4-6, 9, 13-16, 28-30, 35, 39-41, 49, 52-54; Tables 2.7-2.9 | Defines metric-method requirements, `R_conf`, `M_cons`, `R_dup`, `M_unique`, candidate-versus-confirmed semantics, missing-data separation, provenance/reliability needs, and the multidimensional result boundary. |
| [`3.1 Статичні методи`](reference/3.1_Статичні_методи.docx) | §3.1 paragraphs 4-13, 15-18, 22-24, 32-34; Tables 3.1-3.3 | Requires structured, traceable findings; separates artifact stages; identifies semantic and resource trade-offs; requires formula, applicability, source, polarity, missing-data rules, and automation level for numeric indicators. |
| [`3.3 Метод оцінювання`](reference/3.3_Метод_оцінювання.docx) | §3.3 paragraphs 2-3, 10-20, 34-43, 46-50 | Requires provenance, availability masks, separate evidence sufficiency and uncertainty, structured results, reproducibility, and profiles rather than premature scalar aggregation. |
| [`4.1 Процесна модель`](reference/4.1_Процесна_модель.docx) | §4.1 paragraphs 9-16, 22-33 | Requires version, stage, provenance, open risks, and explicit evidence insufficiency; missing evidence is not zero and local risks must not be hidden by aggregation. |
| [`4.2 Модель якості`](reference/4.2_Модель_якості.docx) | §4.2 paragraphs 5-16, 24-34, 40-44 | Keeps artifact properties separate from product quality; distinguishes missing from negative; favors characteristic-specific profiles and requires separate justification for any scalar aggregation. |
| [`4.3 Модель ризиків`](reference/4.3_Модель_ризиків.docx) | §4.3 paragraphs 3, 5-7, 15, 21-23, 36-41; Tables 4.8-4.11 | Defines a defect as an evidence-backed artifact problem, not a guaranteed product defect; separates confidence, severity, risk, and confirmation; lists inconsistency and duplication as distinct defect classes. |
| [`Висновки до розділу 4`](reference/Висновки_до_розділу_4.docx) | conclusions 1-8 | Reaffirms multidimensional, provenance-bearing, uncertainty-aware results and explicitly rejects arbitrary universal parameters. |
| [`model-spec.md`](model-spec.md) | §§2-4, 7.5-7.6, 7.11, 7.14.6, 7.15-7.17, 12-15, 18-19 | Fixes the current production boundary, typed quantitative representation, exact Evidence, `UNKNOWN` behavior, frozen C/V/U rules, and current specification aggregate. |

The dissertation is internally consistent on the central boundary: Consistency
is a property of a set of requirements, while the current C/V/U profile is a
bounded assessment of one requirement followed by independent property means.
**Classification: `SOURCE_DEFINED`.**

## 3. Current baseline architecture

The current production path is:

```text
UTF-8 text file
-> RequirementReader
-> Requirement
-> BaselineFeatureExtractor
-> RequirementExtractionResult
-> RequirementQualityAssessor
-> RequirementAssessmentRecord
-> RequirementQualityProfile(C, V, U)
-> SpecificationQualityAggregator
-> SpecificationQualityProfile(C_file, V_file, U_file)
-> UserConsoleReporter or ConsoleReporter
```

`RequirementAssessmentRecord` composes the requirement and extraction result,
the authoritative C/V/U profile, and the SRM-10 trace. It is the smallest
existing object that retains source text, all six feature outcomes, exact
Evidence, diagnostics, C/V/U assessments, Findings, and calculation trace in a
jointly validated structure. **Classification: `SOURCE_DEFINED`.**

The existing `SpecificationQualityAggregator` consumes only
`RequirementQualityProfile` values. It has no access to requirement text,
features, Evidence, or relationships and therefore cannot perform
cross-requirement analysis. `SpecificationQualityProfile` contains only three
`SpecificationCharacteristicAggregate` values for C/V/U. **Classification:
`DIRECTLY_DERIVABLE`; adding Consistency to this calculator or profile without
a new contract is not authorized.**

A future cross-analysis stage would have to consume a set of source-bearing
records, or a projection derived from those records, before a future
specification-level assessment is assembled. The exact stage name, interface,
and result composition are not decided here. **Classification:
`RESEARCHER_DECISION_REQUIRED` for both the scientific projection and its
production placement.**

## 4. Theoretical definition of Consistency

At specification level, Consistency is the absence of logical,
terminological, and resource conflicts among elements of the requirement set.
A direct conflict exists when requirements prescribe mutually exclusive values
or behavior. An indirect conflict can arise from incompatible constraints or
trade-offs and may require a dependency model or expert review. A contradiction
class is also described as two or more requirements that cannot be satisfied
simultaneously or that use incompatible definitions. **Classification:
`SOURCE_DEFINED`.**

This definition entails a simultaneity test: a confirmed conflict concerns
obligations whose applicable scopes overlap such that they cannot all be
satisfied in the same admissible specification state. Merely different text,
values, or bounds is not sufficient. **Classification: `DIRECTLY_DERIVABLE`
at the logical level; the operational scope-overlap procedure is
`RESEARCHER_DECISION_REQUIRED`.**

Consistency is not established from one isolated line. It requires other
requirements, shared terms/resources, or relationship context. It is also not
proof of product correctness or product quality. **Classification:
`SOURCE_DEFINED`.**

Absence of detected candidates cannot be interpreted as proof of Consistency.
The sources explicitly limit automatic semantic detection, require candidates
to remain distinct from confirmed defects, and preserve missing information.
At most, a bounded procedure could report that no confirmed unresolved
conflict was found within its declared comparison and confirmation coverage.
**Classification: `DIRECTLY_DERIVABLE`; the minimum coverage needed to publish
`M_cons` is `RESEARCHER_DECISION_REQUIRED`.**

## 5. Analysis of M cons and R conf

The dissertation defines:

```text
R_conf = the set of requirements that participate in at least one
         confirmed conflict

M_cons = 1 - |R_conf| / |R|
```

The surrounding metric description and Table 2.8 qualify the relevant
conflicts as confirmed and unresolved at the assessment point. Therefore,
`R_conf` is not ambiguous in the source: it is a set of participating
requirements. Each requirement is counted at most once even if it participates
in several conflicts. **Classification: `SOURCE_DEFINED`.**

Consequences of the source-defined interpretation:

- one confirmed two-requirement conflict contributes two members to `R_conf`;
- a confirmed multi-requirement conflict contributes every participating
  requirement once;
- multiple findings involving the same requirement do not multiply its
  contribution;
- `0 <= M_cons <= 1` follows from `R_conf subseteq R`; and
- if `R` is empty, the general empty-applicability convention makes the result
  `NA`, not zero. **Classification: `DIRECTLY_DERIVABLE`, with the empty-set
  behavior also supported by §2.3 paragraph 16.**

### 5.1 Alternatives explicitly investigated

| Candidate interpretation of `R_conf` | Consequence in the published formula | Research disposition |
| --- | --- | --- |
| Set of requirements participating in at least one confirmed unresolved conflict | Numerator and denominator count the same kind of object; a requirement is counted once; result remains in `[0,1]`. | `SOURCE_DEFINED`; this is the dissertation definition. |
| Set of conflicting requirement pairs | `|R_conf|` counts pairs while `|R|` counts requirements; a dense conflict graph can make the expression negative. A pair-rate would require a different denominator such as the eligible-pair count. | Rejected as an interpretation of the published `R_conf`; a separate pair metric would be `RESEARCHER_DECISION_REQUIRED`. |
| Set of conflict findings | Repeated findings, rules, or evidence fragments could change the score without changing participating requirements; the denominator is dimensionally inconsistent. | Rejected as an interpretation of the published formula; finding-count metrics are `DEFERRED`. |
| Set of conflict clusters | Cluster count loses the number of affected requirements and is incompatible with the stated definition. | Rejected as an interpretation of the published formula; cluster metrics are `DEFERRED`. |

The source therefore resolves the operand meaning but not its construction. No
approved rule defines comparison eligibility, conflict identity, confirmation,
resolution status, multi-requirement membership, detector coverage, or the
point at which the absence of confirmed conflicts is sufficiently observed to
compute `M_cons`. The formula remains non-executable. **Classification:
`RESEARCHER_DECISION_REQUIRED`.**

## 6. Conflict taxonomy found in the sources

| Axis | Source-backed category | Meaning | Status for a first implementation contract |
| --- | --- | --- | --- |
| Conflict kind | Logical | Mutually exclusive behavior, state, value, or constraints. | `SOURCE_DEFINED`; operational rules absent. |
| Conflict kind | Terminological | Incompatible definitions or inconsistent use of terms. | `SOURCE_DEFINED`; terminology authority and equivalence rules absent. |
| Conflict kind | Resource | Requirements or quality goals cannot be jointly satisfied under resource constraints. | `SOURCE_DEFINED`; resource model and feasibility evidence absent. |
| Manifestation | Quantitative incompatibility | Incompatible numeric bounds or targets. It can instantiate a logical conflict and, when tied to capacity, a resource conflict. | `SOURCE_DEFINED` as a manifestation; a separate reporting subtype is `RESEARCHER_DECISION_REQUIRED`. |
| Conflict form | Direct | Two requirements prescribe mutually exclusive values or behavior. | `SOURCE_DEFINED`. |
| Conflict form | Indirect | Several constraints or trade-offs become incompatible through dependencies. | `SOURCE_DEFINED`; dependency model or expert confirmation needed. |

Logical, terminological, and resource conflicts are presented as distinct
categories within the broader Consistency property. Direct and indirect are a
different axis describing how the conflict arises. Quantitative conflict is
not established as a fourth peer category; it is a structured manifestation of
incompatible values or constraints. **Classification: `SOURCE_DEFINED` for the
three categories and two forms; `RESEARCHER_DECISION_REQUIRED` for the final
production taxonomy and subtype codes.**

Duplication is not a conflict category in the metric system. It is handled by
the separate Uniqueness metric in Section 11. **Classification:
`SOURCE_DEFINED`.**

## 7. Candidate versus confirmed conflict

The dissertation explicitly distinguishes candidates produced by semantic or
NLP models from confirmed conflicts and duplicates. Candidate output must not
be counted in `R_conf`. An experiment using an automatic detector must validate
its precision/recall or perform expert validation of a sample. **Classification:
`SOURCE_DEFINED`.**

The sources do not define one universal confirmation route. Plausible routes
include:

1. expert confirmation of each candidate under a documented review protocol;
2. an approved deterministic rule whose inputs and logical conclusion uniquely
   establish a conflict;
3. a validated automated detector plus a separately approved policy for when
   its output is treated as confirmed; or
4. a hybrid route in which automation selects candidates and humans confirm
   semantic or contextual conflicts.

Selecting a route, its required evidence, reviewer agreement, detector
validation threshold, and treatment of disputed findings is
`RESEARCHER_DECISION_REQUIRED`. No precision, recall, confidence, or agreement
threshold is introduced here.

Human confirmation is therefore not proven to be universally mandatory for
every future conflict class, but it is currently required in practice for any
class lacking an approved mechanically conclusive rule. No such production
cross-requirement rule exists in the baseline. **Classification:
`DIRECTLY_DERIVABLE` for the current state; future class-specific confirmation
is `RESEARCHER_DECISION_REQUIRED`.**

A useful future lifecycle may need `CANDIDATE`, `CONFIRMED`, `REJECTED`,
`UNRESOLVED`, and `RESOLVED` distinctions. Only the candidate/confirmed and
confirmed/unresolved distinctions are source-backed for `M_cons`; the exact
state machine is not. **Classification: `RESEARCHER_DECISION_REQUIRED`.**

## 8. Cross requirement comparison requirements

### 8.1 Comparison universe

The theory does not require an implementation to materialize every ordered
pair in `R x R`. Direct conflicts are commonly pairwise, while indirect
resource or trade-off conflicts can involve more than two requirements. The
scientific obligation is to define an eligible comparison universe and ensure
that candidate selection does not silently remove conflicts that the reported
metric claims to cover. **Classification: `DIRECTLY_DERIVABLE` for separating
the conceptual universe from materialization; candidate-selection completeness
is `RESEARCHER_DECISION_REQUIRED`.**

Self-comparison contributes no cross-requirement conflict. Pair order is not
semantically meaningful for a symmetric conflict, although rule evaluation may
use deterministic source order. **Classification: `DIRECTLY_DERIVABLE`; exact
ordering is `RESEARCHER_DECISION_REQUIRED`.**

Candidate selection and conflict confirmation should be separate stages:

```text
RequirementAssessmentRecord set
-> cross-analysis projection
-> candidate selection
-> class-specific comparison
-> candidate result
-> approved confirmation procedure
-> confirmed unresolved conflicts
-> R_conf
-> M_cons (only when its observability preconditions are satisfied)
```

This separation follows the dissertation's candidate-versus-confirmed rule,
but the stages and interfaces are not a production design approval.
**Classification: `DIRECTLY_DERIVABLE` conceptually; architecture remains
`RESEARCHER_DECISION_REQUIRED`.**

### 8.2 Information potentially needed

Different conflict classes require different comparison keys. No single
universal “same context” rule is supported.

| Information | Why it may be needed | Current scientific status |
| --- | --- | --- |
| Subject, actor, component, or resource | Determines whose behavior or capacity is constrained; resource conflicts may connect different subjects through one shared resource. | `SOURCE_DEFINED` as potentially relevant; exact representation is `RESEARCHER_DECISION_REQUIRED`. |
| Action, behavior, state transition, or obligation | Establishes whether requirements prescribe incompatible behavior. | `SOURCE_DEFINED` as potentially relevant; a cross-analysis predicate model is `RESEARCHER_DECISION_REQUIRED`. |
| Object or affected entity | Distinguishes obligations about different targets. | `DIRECTLY_DERIVABLE` as potentially relevant; representation is `RESEARCHER_DECISION_REQUIRED`. |
| Metric identity | Needed for direct comparison of quantitative bounds. | `SOURCE_DEFINED` concept; equivalence and normalization are `RESEARCHER_DECISION_REQUIRED`. |
| Comparator, value, and unit | Defines a quantitative admissible set when semantics are fully known. | Existing components are `SOURCE_DEFINED`; cross-conflict interpretation is `RESEARCHER_DECISION_REQUIRED`. |
| Context, condition, scenario, state, population, and time window | Determines whether requirements apply simultaneously, overlap, or are disjoint. | Need is `SOURCE_DEFINED`; overlap logic is `RESEARCHER_DECISION_REQUIRED`. |
| Terminology authority and definitions | Needed to establish incompatible definitions rather than mere lexical variation. | Absent; `DEFERRED` from the first slice. |
| Dependency and resource model | Needed for indirect trade-offs and capacity conflicts. | Absent; `DEFERRED` from the first slice. |

Two requirements become valid candidates only under a class-specific rule that
establishes enough shared semantic scope to make simultaneous satisfaction a
meaningful question. Exact equality of raw context strings is neither required
by the sources nor sufficient: different wording may denote the same scope,
and similar wording may refer to distinct scenarios. **Classification:
`DIRECTLY_DERIVABLE` for the semantic requirement;
`RESEARCHER_DECISION_REQUIRED` for operational matching.**

## 9. Current data reuse matrix

The classifications below concern usefulness for conflict analysis, not the
continued validity of the fields in Single Requirement Analysis.

| Existing data | Reuse class | Cross-analysis value and limitation |
| --- | --- | --- |
| `Requirement.id` and `source_line` | `DIRECTLY_REUSABLE` | Identify participants and preserve source order. IDs are generated for one processing run, so durable cross-version identity is absent. |
| `Requirement.text` | `REUSABLE_WITH_PROJECTION` | Authoritative source for semantic projection and Evidence round-trip; raw text alone is not a comparison key. |
| `RequirementAssessmentRecord` | `REUSABLE_WITH_PROJECTION` | Best existing source container because it preserves extraction, C/V/U, trace, diagnostics, and Evidence; cross-analysis must not reinterpret it as an already prepared semantic relation model. |
| `RequirementQualityProfile` C/V/U | `NOT_RELEVANT` | Must be preserved in the final specification view but does not establish whether requirements conflict. Scores are not candidate filters or conflict confidence. |
| condition/context observations | `REUSABLE_WITH_PROJECTION` | Provide exact source spans for explicit conditions; they do not normalize scenario identity, scope overlap, state, population, or attachment beyond bounded rules. |
| expected-result observations | `REUSABLE_WITH_PROJECTION` | Provide exact spans for bounded required behavior; they do not expose a general actor/action/object/polarity/state representation. |
| acceptance-criterion observations | `REUSABLE_WITH_PROJECTION` | May provide judgeable outcome spans; they do not define cross-requirement semantic equivalence or incompatibility. |
| quantitative constraint as a linked observation | `REUSABLE_WITH_PROJECTION` | Preserves metric, comparator, value, unit, context, unresolved components, and Evidence association. A comparison projection is still required. |
| quantitative `metric` | `REUSABLE_WITH_PROJECTION` | `TextComponent` contains Evidence references, not a canonical metric identifier. Current production recognizes only bounded metric links. |
| quantitative `comparator` and inclusivity | `DIRECTLY_REUSABLE` | Normalized labels and supported inclusivity are usable without rereading surface text; `UPPER_BOUND` remains explicitly unresolved and `NOT_LESS_FREQUENT` is not ordinary interval semantics. |
| quantitative `value` | `DIRECTLY_REUSABLE` | Exact `Decimal`; no tolerance, measurement error, distribution, or range semantics is supplied. |
| quantitative `unit` | `DIRECTLY_REUSABLE` | Approved labels `SECOND`, `MINUTE`, and `PERCENT`; the current contract explicitly supplies no unit conversion or ontology. |
| quantitative `context` | `REUSABLE_WITH_PROJECTION` | Exact source-linked context exists for approved cases, but `TextComponent` has no normalized scope or overlap semantics. |
| quantitative `unresolved_components` | `DIRECTLY_REUSABLE` | Must gate comparison and preserve why an observation cannot support confirmation; it must never be interpreted as a negative or wildcard. |
| verification-method observations | `NOT_RELEVANT` | Useful to local Verifiability but not evidence that two requirements conflict. A future method-specific contradiction rule would require separate research. |
| vague-term observations | `NOT_RELEVANT` | Local ambiguity signals do not establish cross-requirement terminology identity or conflict. The seed vocabulary is not a terminology ontology. |
| accepted `Evidence` | `DIRECTLY_REUSABLE` | Exact text, offsets, requirement ID, feature ID, and Rule ID provide the required source provenance for any projection or result. |
| detector diagnostics and candidate spans | `DIRECTLY_REUSABLE` | Preserve incomplete processing and unresolved reasons. Candidate spans remain non-Evidence and cannot confirm a conflict. |
| assessment trace | `NOT_RELEVANT` | Explains local C/V/U only. It remains useful beside cross results but has no cross-requirement relation or conflict semantics. |
| existing per-requirement `Finding` | `INSUFFICIENT` | Carries one requirement ID and only C/V/U `CharacteristicId`; its Evidence references resolve inside one extraction result. It cannot represent multi-requirement participation or cross-record Evidence safely. |
| actor/action/object candidates | `INSUFFICIENT` | They are absent from production and explicitly deferred by model-spec §7.11. No source-defined general fields or detectors exist. |
| subject/resource/state/scenario identities | `INSUFFICIENT` | No current normalized representation exists. Exact spans may help a future projection but do not supply identity or overlap rules. |

The matrix does not justify extending the single-requirement feature registry.
A separate cross-analysis projection may derive only the information required
by an approved cross rule while leaving `RequirementFeatures` unchanged.
**Classification: `DIRECTLY_DERIVABLE` for avoiding automatic modification of
the frozen model; the projection content is `RESEARCHER_DECISION_REQUIRED`.**

The deferred `has_actor`, `has_action`, and `has_object` candidates should not
be promoted merely because cross-analysis may need subject and predicate
information. Their earlier names describe grammatical presence, while conflict
analysis needs semantic identity, obligation, polarity, scope, and relation.
Those are not equivalent contracts. **Classification: `SOURCE_DEFINED` for
their deferral; `RESEARCHER_DECISION_REQUIRED` for any future cross projection.**

## 10. Quantitative conflict feasibility analysis

Quantitative observations are the most structured reusable data, but they are
not yet sufficient for a conflict detector. The current contract protects
component linkage and exact evidence, which makes a bounded future slice
plausible. It does not approve cross-observation comparability.

### 10.1 Existing source-defined facts

- A quantitative observation links metric, comparator, value, unit, context,
  unresolved components, and Evidence. **`SOURCE_DEFINED`.**
- `LESS_THAN_OR_EQUAL` and `GREATER_THAN_OR_EQUAL` are inclusive for their
  approved source forms. **`SOURCE_DEFINED`.**
- `UPPER_BOUND` has `UNRESOLVED` inclusivity and must not be converted to
  `LESS_THAN_OR_EQUAL`. **`SOURCE_DEFINED`.**
- `NOT_LESS_FREQUENT` is a distinct comparator label, not an approved generic
  numeric interval operation. **`SOURCE_DEFINED`.**
- Seconds and minutes are normalized unit labels, but conversion between them
  is explicitly prohibited by the current contract. Percent has unresolved
  population/metric semantics outside approved exact links. **`SOURCE_DEFINED`.**
- A missing component without an unresolved marker can mean that the component
  was not expressed in the accepted anchor; an unresolved marker means an
  expressed candidate could not be resolved. Neither case supplies a wildcard
  or equality assumption. **`SOURCE_DEFINED`.**

### 10.2 Candidate formalization, not an approved rule

The following is a research decomposition only:

```text
Comparable(c1, c2)
  requires an approved rule for:
    same semantic metric or measured property
    compatible subject/resource target
    overlapping applicability context and time/state scope
    comparable unit semantics
    fully resolved comparator meaning needed by the rule

AdmissibleSet(c)
  may be derived only for approved comparator/value semantics

DirectQuantitativeConflict(c1, c2)
  could require:
    Comparable(c1, c2)
    and intersection(AdmissibleSet(c1), AdmissibleSet(c2)) is empty
```

`Comparable` and its fields are `RESEARCHER_DECISION_REQUIRED`. Treating an
inclusive lower bound `x >= l` as `[l,+infinity)` and an inclusive upper bound
`x <= u` as `(-infinity,u]`, followed by an empty-intersection test, is
mathematically `DIRECTLY_DERIVABLE` once metric identity, scope, unit, and
comparator semantics have been validly established. Authorizing that mapping
as a scientific conflict rule, including its inputs and reference cases,
remains `RESEARCHER_DECISION_REQUIRED`.

Under that candidate interpretation, two upper bounds or two lower bounds are
normally jointly satisfiable, with one possibly stricter; different numeric
values alone are not a contradiction. An inclusive lower bound greater than an
inclusive upper bound would make their joint admissible set empty. Equality,
exclusive bounds, tolerances, ranges, distributions, percentile constraints,
and measurement uncertainty are not supported by the current comparator model
and are `DEFERRED`.

### 10.3 Required decisions for any bounded quantitative slice

| Question | Current evidence | Disposition |
| --- | --- | --- |
| What establishes the same metric? | Metric Evidence exists only for bounded source forms; no canonical vocabulary or synonym rule. | `RESEARCHER_DECISION_REQUIRED`. |
| Must contexts be equal or merely overlap? | Conflict requires simultaneous applicability; current contexts are text spans. | `RESEARCHER_DECISION_REQUIRED`; raw-string equality is not justified. |
| Must subject/resource match? | Direct conflicts usually need a shared target; resource conflicts may connect different subjects through one capacity. | Class-specific `RESEARCHER_DECISION_REQUIRED`. |
| What unit relation is allowed? | Current labels are normalized; conversion is explicitly absent. | First slice can at most consider an approved exact-same-unit rule; even that use must be approved. Conversion is `DEFERRED`. |
| Which comparators can form intervals? | Inclusive `<=` and `>=` are defined; `UPPER_BOUND` inclusivity is unresolved; frequency is distinct. | Limit candidate research to fully resolved inclusive bounds; all other forms `DEFERRED`. |
| What does missing metric mean? | Missing is not false; absent-in-anchor differs from unresolved candidate. | Non-comparable or unresolved, never confirmed consistent; exact state is `RESEARCHER_DECISION_REQUIRED`. |
| What does missing context mean? | It may be unexpressed, not universal. | Must not be assumed global; scope recovery or unresolved handling is `RESEARCHER_DECISION_REQUIRED`. |
| How are multiple constraints in one requirement related? | Current observations remain separate except approved bounded links; generic relationship grammar is absent. | `DEFERRED` unless an exact approved relation supplies the comparison member. |
| Does a conflict candidate become confirmed automatically? | No cross rule or confirmation procedure exists. | `RESEARCHER_DECISION_REQUIRED`. |

A scientifically honest first quantitative slice is therefore not “compare all
numbers.” It would require an explicitly approved comparability signature,
only fully resolved component semantics, exact evidence on both sides, an
empty-admissible-set rule, confirmation semantics, and binding positive,
negative, and unresolved cases. **Classification:
`RESEARCHER_DECISION_REQUIRED`.**

## 11. Duplicates and Uniqueness

The dissertation defines duplication separately:

```text
R_dup = requirements assigned to confirmed duplicates
M_unique = 1 - |R_dup| / |R|
```

Tables 2.7 and 2.8 group Consistency and redundancy for convenience but give
them separate operands, formulas, and interpretations. The risk model likewise
lists inconsistency and duplication/redundancy as separate defect classes.
Duplication may create later version divergence and conflict, but it is not
itself a confirmed current conflict without another source-backed rule.
**Classification: `SOURCE_DEFINED`.**

Therefore duplication should remain a separate future specification-level
Uniqueness/non-redundancy property. It must not be merged into `R_conf` or
`M_cons`. Duplicate candidate generation, semantic equivalence, clustering,
confirmation, and `R_dup` membership are `DEFERRED` from the first Consistency
slice and require their own research contract.

## 12. Relationship between Consistency and C V U

The dissertation distinguishes individual-requirement properties from set-level
properties, and the current model fixes independent C/V/U calculation rules.
Nothing in the sources authorizes a cross-requirement conflict to recalculate
`C_i`, `V_i`, or `U_i`. **Classification: `SOURCE_DEFINED` for the level
distinction; `DIRECTLY_DERIVABLE` for preserving current C/V/U unchanged.**

The working architectural hypothesis is therefore supported for this baseline:

```text
local RequirementQualityProfile(C_i, V_i, U_i) remains unchanged
+
separate specification-level Consistency result and cross findings
```

A requirement may independently contain a local ambiguity or missing criterion
and also participate in a cross conflict. Shared source text or evidence does
not make those results identical. A future scientific rule could state that a
particular cross finding also changes a local property, but that would be a new
rule with explicit inputs, applicability, Evidence, and calculation effects.
**Classification: `RESEARCHER_DECISION_REQUIRED` for any dual effect; no dual
effect is authorized now.**

The current `SpecificationQualityProfile(C_file,V_file,U_file)` remains a set of
three independent means, not a full specification assessment and not a scalar
quality score. Consistency should not be folded into any of those means.
**Classification: `DIRECTLY_DERIVABLE`.**

## 13. Missing and UNKNOWN semantics

The dissertation repeatedly distinguishes computed, applicable-but-missing,
and not-applicable states. Missing or unavailable evidence must not become
zero, false, “no conflict,” or confirmed Consistency. **Classification:
`SOURCE_DEFINED`.**

For cross-analysis, the following conceptual behavior is required:

| Situation | Permitted conclusion | Prohibited conclusion | Classification |
| --- | --- | --- | --- |
| Missing metric on one side | Comparison lacks a required identity input. | Metrics are equal, different, or non-conflicting. | `DIRECTLY_DERIVABLE`; exact state/result representation is `RESEARCHER_DECISION_REQUIRED`. |
| Unresolved context | Scope overlap is unknown. | Context is global, equal, disjoint, or compatible. | `DIRECTLY_DERIVABLE`. |
| Unsupported unit or different units without approved conversion | Quantitative comparability is unavailable. | Convert, compare raw numbers, or confirm compatibility. | `SOURCE_DEFINED` for no conversion; result representation is `RESEARCHER_DECISION_REQUIRED`. |
| Unresolved comparator inclusivity | Boundary intersection may depend on missing semantics. | Treat `UPPER_BOUND` as inclusive `<=`. | `SOURCE_DEFINED`. |
| Incomplete expected-result extraction | Behavior comparison is not complete under the claimed rule. | Absence of conflict. | `DIRECTLY_DERIVABLE`. |
| One side resolved and one side unresolved | Preserve accepted data and unresolved reason. | Confirm conflict or non-conflict unless an approved rule proves the unresolved input immaterial. | `DIRECTLY_DERIVABLE`; materiality rules are `RESEARCHER_DECISION_REQUIRED`. |
| No candidate produced by a bounded detector | No candidate under that detector and coverage profile. | Proof of Consistency. | `DIRECTLY_DERIVABLE`. |
| Empty requirement set | `M_cons` is `NA`. | `0` or `1`. | `SOURCE_DEFINED` through the general denominator convention. |

The exact cross-analysis state envelope, pair/group applicability, propagation
to the specification summary, and distinction between `UNKNOWN`,
`NOT_APPLICABLE`, `NOT_COMPARED`, and `NO_CONFIRMED_CONFLICT` require researcher
approval. Existing C/V/U states must not be copied automatically because the
cross-analysis unit may be a pair or group rather than one requirement.
**Classification: `RESEARCHER_DECISION_REQUIRED`.**

## 14. Evidence and provenance requirements

Every cross-requirement result must remain traceable to all participating
requirements and to the exact source evidence used on every side. At minimum,
a future contract needs to preserve:

- participating requirement IDs in deterministic order;
- exact source Evidence references qualified by requirement/record identity;
- conflict category and direct/indirect form, when approved;
- governing comparison and confirmation Rule IDs;
- candidate or confirmed state and, for the metric, unresolved/resolved status;
- explanation of the incompatible obligations or unresolved input;
- all unresolved inputs and diagnostic provenance;
- projection provenance from source record to comparison fields;
- analysis/coverage profile and version; and
- deterministic ordering of results and evidence.

These are `SOURCE_DEFINED` or `DIRECTLY_DERIVABLE` obligations from the
structured-finding, provenance, confirmation, reproducibility, and missing-data
rules. Exact field names, identifiers, cardinalities, ordering keys, and
validation invariants are `RESEARCHER_DECISION_REQUIRED` or architectural
decisions.

The current per-requirement `Finding` cannot be reused as the complete
cross-result contract. It carries one `requirement_id`, one of the three local
`CharacteristicId` values, and Evidence references validated within one
`RequirementExtractionResult`. It has no participant set, cross-record Evidence
namespace, candidate/confirmed state, unresolved inputs, or conflict relation.
**Classification: `DIRECTLY_DERIVABLE`.**

A separate cross-requirement result concept is therefore required if
implementation proceeds. This conclusion does not approve a production class
or its name. Whether candidate and confirmed results share one envelope, and
whether the result represents a pair, arbitrary participant set, relation, or
finding plus relation, are architectural decisions gated by the scientific
contract. **Classification: `RESEARCHER_DECISION_REQUIRED`.**

Severity, probability, confidence, product-quality relevance, risk,
prioritization, and corrective actions belong to later models and must not be
silently imported into the first Consistency result. Confirmation status and
evidence sufficiency must be represented without inventing a numeric confidence
value. **Classification: `SOURCE_DEFINED` for separation; these fields are
`DEFERRED`.**

## 15. Specification level result boundary

The existing `SpecificationQualityProfile` answers only:

```text
What are the separately aggregated C, V, and U results over requirement-level
profiles, including their observability counts?
```

A future full specification assessment must answer a broader question:

```text
What is the state of local-property aggregates and independently assessed
set-level properties, with their findings, evidence coverage, unknowns, and
provenance?
```

Potential future components include the existing C/V/U aggregate profile,
Consistency, Uniqueness, global coverage/completeness, traceability, and other
explicitly approved set properties. Their presence in the dissertation does
not make all of them ready for one implementation. **Classification:
`SOURCE_DEFINED` for the conceptual property families; exact future assessment
composition is `RESEARCHER_DECISION_REQUIRED`.**

No overall scalar specification-quality score is authorized. `M_cons` and
`M_unique` are individual property indicators, not weights or ingredients of a
new combined score. **Classification: `SOURCE_DEFINED`.**

For Consistency, a future specification-level result would need to preserve at
least the property state, optional `M_cons`, `|R_conf|`, `|R|`, confirmed
unresolved conflict results, candidate/unresolved counts if approved,
comparison coverage, governing rule/version, and provenance. This is a
requirements inventory, not an approved schema. Whether candidates appear in
the primary assessment or only an audit/review queue is
`RESEARCHER_DECISION_REQUIRED`.

## 16. Scientific decisions still required

The following decisions block any production Consistency implementation:

1. Define the exact semantic object called a conflict for each selected class.
2. Select the first bounded conflict class and state whether it is pairwise or
   may have arbitrary participant cardinality.
3. Define comparison applicability and the eligible comparison universe.
4. Define candidate-selection rules and the coverage/non-claim attached to
   omitted comparisons.
5. Define the cross-analysis projection and the scientific meaning of every
   projected field.
6. Define metric, subject/resource, behavior, state, and context identity or
   overlap only to the extent required by the selected class.
7. For a quantitative slice, approve comparable units, comparator-to-admissible
   set semantics, unresolved inclusivity behavior, and binding conflict and
   non-conflict cases.
8. Define candidate, confirmed, rejected, unresolved, and resolved semantics as
   needed.
9. Define the confirmation procedure and whether each selected class requires
   human confirmation, validated automation, or an exact deterministic rule.
10. Define when a confirmed conflict enters and leaves `R_conf`.
11. Define when comparison coverage is sufficient to compute `M_cons` and how
    incomplete coverage is reported.
12. Define missing/unknown/not-applicable propagation for pair/group results and
    the specification result.
13. Define whether candidate counts are reported separately and ensure they do
    not affect `M_cons`.
14. Confirm that local C/V/U remain unchanged, or approve an explicit new rule
    for any proposed dual effect.
15. Approve the result/evidence/provenance contract and binding reference cases.

Every item is `RESEARCHER_DECISION_REQUIRED`. This document intentionally
chooses none of the scientifically open alternatives.

## 17. Architectural decisions still required

After the scientific decisions, architecture research must decide:

1. whether cross-analysis consumes `RequirementAssessmentRecord` objects
   directly or an immutable projection built from them;
2. the boundary between candidate selection, comparison, and confirmation;
3. the representation of pairwise and multi-requirement relations;
4. cross-record Evidence reference namespacing and validation;
5. identifiers and versioning for candidates, confirmations, rules, and
   coverage profiles;
6. the cross-result state envelope and unresolved-input representation;
7. deterministic ordering for participants, candidates, conflicts, and
   evidence;
8. the calculator/aggregator boundary for `R_conf` and `M_cons`;
9. composition of current `SpecificationQualityProfile` with a future full
   specification assessment without modifying current C/V/U semantics;
10. reporter separation between user results, audit provenance, and any human
    confirmation queue;
11. persistence or interaction needed for human confirmation, if approved; and
12. test layers for projection, comparison, confirmation, metric construction,
    joint validation, ordering, and reporting.

These are architectural blockers, not permission to add production classes.
They remain `RESEARCHER_DECISION_REQUIRED` after the scientific layer selects
the required semantics.

## 18. Topics deferred from the first cross analysis slice

The following topics are `DEFERRED` unless the researcher explicitly selects
one in a later round:

- production conflict detectors or domain classes;
- terminology dictionaries, synonymy, ontologies, embeddings, or semantic
  similarity thresholds;
- terminological conflict detection;
- indirect resource/capacity and quality-trade-off conflict detection;
- architecture-, code-, test-, or lifecycle-level conflict analysis;
- duplicate detection, clustering, `R_dup`, and `M_unique` implementation;
- unit conversion, dimensional ontology, tolerances, uncertainty, ranges,
  exclusive bounds, equality, percentiles, distributions, and statistical
  measurement procedures;
- generic actor/action/object extraction or modification of the frozen
  single-requirement feature registry;
- automatic requirement-type classification;
- conflict severity, probability, confidence score, risk, priority, or
  corrective-action generation;
- product-quality prediction;
- global requirements coverage, traceability, or a combined specification
  score; and
- refactoring the current production pipeline or changing C/V/U calculation,
  aggregation, trace, or reporting semantics.

## 19. Recommended order for subsequent research rounds

1. **Consistency result semantics.** Approve the unit of analysis, state
   envelope, candidate/confirmed/resolved lifecycle, evidence contract, and
   `R_conf` membership rules before selecting a detector.
2. **Comparison projection.** Define the minimum immutable projection from
   `RequirementAssessmentRecord`, including provenance and unknown behavior,
   without changing the Single Requirement model.
3. **Bounded quantitative direct-conflict science.** Decide whether exact-same
   normalized metric, exact-same unit, fully resolved inclusive lower/upper
   bounds, and an approved scope signature can support a first slice. Prepare
   positive, non-conflict, non-comparable, and unresolved reference cases.
4. **Confirmation and observability.** Approve human or deterministic
   confirmation, detector validation obligations, comparison coverage, and the
   preconditions for publishing `M_cons`.
5. **Architecture contract.** Define candidate selection, comparison,
   confirmation, result, aggregation, Evidence namespace, deterministic order,
   and specification-assessment composition.
6. **Implementation readiness audit.** Verify every field, state, Rule ID,
   formula operand, and test case against the approved science before creating
   production code.
7. **Later property rounds.** Research terminological and resource conflicts,
   then Uniqueness, global coverage/completeness, and traceability as separate
   contracts.

The repository is ready for the next research round because the baseline is
stable, exact source Evidence and linked quantitative observations are already
available, and the unresolved decisions are now isolated. It is not ready for
production cross-requirement implementation: conflict construction,
confirmation, missing-data propagation, result semantics, and the future
specification boundary remain unapproved. **Classification:
`DIRECTLY_DERIVABLE` readiness for further research;
`RESEARCHER_DECISION_REQUIRED` before implementation.**

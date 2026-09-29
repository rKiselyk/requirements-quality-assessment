# Full Model v0.1 Metric Profile Contract

**Contract ID:** `FULL-MODEL-V0.1-METRIC-PROFILE`  
**Contract version:** `1`  
**Milestone issue:** M3-02 / #139  
**Parent contract:** `FULL-MODEL-V0.1-CONTRACT / 1`  
**Status:** `NORMATIVE_CANDIDATE / PARENT_CONTRACT_APPROVAL_REQUIRED`

## 1. Purpose and authority

This document defines the future `MetricProfile` and `MetricEntry` boundary for
the Full Model v0.1 transformation:

```text
P -> M
```

The transformation is a lossless adapter over completed property assessments.
It is not a calculator, aggregator, detector, normalizer, or interpretation
layer. It must not change any accepted Completeness, Verifiability,
Unambiguity, specification aggregation, or QB-v0.1 meaning.

This contract inherits and specializes Sections 5, 6, 18, 19, 20, 22, and 24
of `docs/full-model-v0.1-contract.md`. It does not reopen decisions fixed there.
For source semantics, the authority order remains:

1. `docs/model-spec.md` for C/V/U, `AGG-MVP-001`, evidence, trace, and exact
   numeric rules;
2. the accepted QB-v0.1 contracts for bounded quantitative-bound Consistency;
3. `docs/full-model-v0.1-contract.md` for the Full Model boundary; and
4. this document for the `P -> M` representation and adapter.

If a future implementation cannot satisfy this contract without changing a
source assessment, it must stop. M3-02 must not repair, reinterpret, or fill a
source result.

## 2. Inspected baseline and inherited constraints

The current source boundary is `SpecificationAssessmentResult`, containing:

- ordered `RequirementAssessmentRecord` values;
- each record's unchanged `RequirementExtractionResult`,
  `RequirementQualityProfile`, and `RequirementAssessmentTrace`;
- `SpecificationQualityProfile` with three property aggregates;
- separate `QbConsistencyAssessment` under the same QB snapshot;
- ordered QB cross results and materiality audit records; and
- a snapshot-scoped evidence resolver.

The accepted source facts are:

- requirement C/V/U values are exact `fractions.Fraction` or absent;
- specification C/V/U aggregate values are exact `Fraction` or absent;
- `M_cons[QB-v0.1]` is an exact `Fraction` or absent;
- `Decimal` appears in quantitative observations and QB operands, not in any
  registered Full Model v0.1 property metric value;
- C/V/U source states are `COMPUTED`, `UNKNOWN`, and `NOT_APPLICABLE`;
- QB aggregate states are `COMPUTED`, `UNKNOWN`, and `NOT_APPLICABLE`;
- source evidence and diagnostics remain owned by their requirement/snapshot;
- requirement records and trace characteristics have deterministic source
  order; and
- QB results, evidence references, diagnostics, operands, reasons, contract
  versions, and non-claims already have deterministic contracts.

The adapter inherits these constraints:

- no normalization, weighting, rounding, percentage conversion, or float;
- no scalar requirement-quality or specification-quality score;
- no zero imputation;
- no new requirement properties;
- no change to source status or applicability semantics; and
- no unqualified Consistency claim.

## 3. Boundary definition

The future public operation is conceptually:

```text
build_metric_profile(
    source: SpecificationAssessmentResult,
    context: MetricConstructionContext,
) -> MetricProfile
```

It performs only these operations:

1. validate that `source` is a complete, internally consistent accepted P
   result;
2. attach explicit Full Model artifact and assessment identity supplied by
   `context`;
3. project each registered P result into exactly one `MetricEntry`;
4. attach typed source and provenance references;
5. preserve exact values, states, reasons, counts, rules, and non-claims; and
6. emit entries in the fixed registry order defined below.

The operation must be pure. It must not mutate `source` or `context`. It must be
independently testable with manually constructed domain results and must not
depend on files, CLI code, reporters, feature extraction implementations, or an
NLP library.

## 4. Exact metric registry

The registry identity is:

```text
registry_id      = FULL-MODEL-V0.1-METRICS
registry_version = 1
adapter_rule_id  = P-TO-M-V0.1-001
```

The registry is closed for Full Model v0.1:

| Registry ordinal | Metric ID | Scope | Cardinality | Source |
| ---: | --- | --- | --- | --- |
| 1 | `RQ.COMPLETENESS` | `REQUIREMENT` | one per requirement | `RequirementQualityProfile.completeness` |
| 2 | `RQ.VERIFIABILITY` | `REQUIREMENT` | one per requirement | `RequirementQualityProfile.verifiability` |
| 3 | `RQ.UNAMBIGUITY` | `REQUIREMENT` | one per requirement | `RequirementQualityProfile.unambiguity` |
| 4 | `SPEC.MEAN_COMPLETENESS` | `SPECIFICATION` | exactly one | `SpecificationQualityProfile.completeness` |
| 5 | `SPEC.MEAN_VERIFIABILITY` | `SPECIFICATION` | exactly one | `SpecificationQualityProfile.verifiability` |
| 6 | `SPEC.MEAN_UNAMBIGUITY` | `SPECIFICATION` | exactly one | `SpecificationQualityProfile.unambiguity` |
| 7 | `SPEC.QB_CONSISTENCY` | `SPECIFICATION` | exactly one | `QbConsistencyAssessment` / `M_cons[QB-v0.1]` |

For `n` source requirements, a complete profile contains exactly `3n + 4`
entries. An empty specification contains the four specification entries and no
requirement entries.

The registry does not contain raw quantitative bounds, detector counts,
findings, product-quality features, a combined C/V/U value, or an overall
quality score. Adding a metric requires a reviewed contract and a new registry
version; it is not an M3-02 implementation choice.

## 5. Conceptual domain contracts

### 5.1 MetricConstructionContext

Current P results do not carry Full Model artifact and assessment versions.
The caller must therefore supply, without inference:

```text
MetricConstructionContext
  artifact_ref: ArtifactRef
  assessment_ref: AssessmentRef
  full_model_contract_ref: ContractRef
  metric_registry_ref: ContractRef
  adapter_rule_ref: RuleRef
```

Required invariants are:

- `artifact_ref.artifact_id` and `artifact_ref.artifact_version` are non-empty;
- `assessment_ref.assessment_id` and `assessment_ref.assessment_version` are
  non-empty;
- the assessment explicitly names `artifact_ref` as its assessed artifact;
- the Full Model contract reference is `FULL-MODEL-V0.1-CONTRACT / 1`;
- the registry reference is `FULL-MODEL-V0.1-METRICS / 1`; and
- the adapter rule is `P-TO-M-V0.1-001` under this contract version.

The adapter must not derive an artifact version from file name, requirement
text, processing order, or QB snapshot. It must not derive an assessment
version from a timestamp, object address, or QB snapshot hash.

### 5.2 MetricProfile

```text
MetricProfile
  profile_id: MetricProfileId
  artifact_ref: ArtifactRef
  assessment_ref: AssessmentRef
  registry_ref: ContractRef
  adapter_rule_ref: RuleRef
  source_snapshot_id: AssessmentSnapshotId
  entries: tuple[MetricEntry, ...]
```

`source_snapshot_id` is copied from `SpecificationAssessmentResult` and links
the local and QB source populations. It is not an artifact version or an
assessment version.

### 5.3 MetricEntry

```text
MetricEntry
  entry_id: MetricEntryId
  metric_id: MetricId
  scope: MetricScope
  subject_ref: RequirementSubjectRef | SpecificationSubjectRef
  status: MetricStatus
  applicability: MetricApplicability
  value: Fraction | None
  numeric_representation: EXACT_FRACTION | NONE
  source_status: SourceStatusRef
  source_assessment_refs: tuple[SourceAssessmentRef, ...]
  provenance: MetricProvenance
  rule_refs: tuple[RuleRef, ...]
  artifact_ref: ArtifactRef
  assessment_ref: AssessmentRef
```

The records must be immutable. `MetricEntry` contains no setter, recalculation
method, display string, decimal approximation, weight, rank, or product-quality
interpretation.

### 5.4 Supporting identities

The conceptual typed identities are:

```text
ArtifactRef(artifact_id, artifact_version)
AssessmentRef(assessment_id, assessment_version, artifact_ref)
RequirementSubjectRef(artifact_ref, requirement_id, source_line)
SpecificationSubjectRef(artifact_ref)
ContractRef(contract_id, version)
RuleRef(rule_id, explicit_version, version_authority)
```

They are value objects, not free-form display labels.

## 6. Requirement vs specification scope and subject identity

`REQUIREMENT` entries use the exact source requirement ID and source line from
the corresponding ordered `RequirementAssessmentRecord`, qualified by the
artifact identity and version. The full subject identity is:

```text
(artifact_id, artifact_version, requirement_id, source_line)
```

The source line is an integrity field as well as part of the bounded subject
reference. The adapter must validate that the requirement ID and source line
agree with the QB projection manifest for the same source order.

`SPECIFICATION` entries use:

```text
(artifact_id, artifact_version)
```

They must not use a requirement ID. All four specification entries describe
the same source population already enforced by `SpecificationAssessment`.

Requirement IDs such as `R001` are generated in processing order and are not
cross-version lineage identities. `R001` in two artifact versions must not be
treated as the same requirement without a later explicit lineage relation.
M3-02 records version-qualified subjects; M3-09 owns cross-version lineage.

## 7. Exact numeric representation

Every available registered metric value is the exact source `Fraction` object.
The adapter must preserve the numerator and denominator exactly as the reduced
`Fraction` value represents them. It must not convert through `float`,
`Decimal`, string division, percentage, or a fixed decimal scale.

For serialization, the only approved conceptual representation is:

```text
{ "kind": "FRACTION", "numerator": <integer>, "denominator": <positive integer> }
```

The serialized pair must reconstruct the same `Fraction`. Presentation is not
part of the metric contract.

When `status` is not `AVAILABLE`, `value` is `None` and
`numeric_representation` is `NONE`. A zero `Fraction(0, 1)` is legal only when
the source assessment is computed with exact value zero. It is never a missing,
unknown, unsupported, unresolved, unavailable, or not-applicable sentinel.

## 8. Relationship to QB Decimal evidence

QB operands originate in quantitative observations whose numeric component is
an exact `decimal.Decimal`. Those bounds remain source evidence and comparison
operands. They are not registered metric values in Full Model v0.1.

For `SPEC.QB_CONSISTENCY`:

- `MetricEntry.value` copies only the source aggregate `Fraction` when its QB
  state is `COMPUTED`;
- the contributing bounds remain `Decimal` within referenced QB cross results;
- the metric provenance retains `snapshot_id`, `cross_result_ids`, evidence
  references reachable through those results, formula operands, and contract
  descriptors; and
- no `Decimal` bound is converted to a `Fraction`, averaged, normalized, or
  inserted into the metric registry.

Downstream characteristic mapping that needs a response-time bound must follow
the provenance reference to the quantitative source. It must not reinterpret
`M_cons[QB-v0.1]` as the bound or as a product-quality value.

## 9. Status and applicability

### 9.1 MetricStatus

The closed status set is:

- `AVAILABLE`;
- `UNKNOWN`;
- `NOT_APPLICABLE`;
- `UNRESOLVED`;
- `UNAVAILABLE`; and
- `UNSUPPORTED`.

### 9.2 MetricApplicability

Applicability is orthogonal and uses:

- `APPLICABLE`;
- `UNKNOWN`; and
- `NOT_APPLICABLE`.

Allowed combinations are:

| Metric status | Allowed applicability | Value |
| --- | --- | --- |
| `AVAILABLE` | `APPLICABLE` only | exact `Fraction` |
| `UNKNOWN` | `APPLICABLE` or `UNKNOWN` | `None` |
| `NOT_APPLICABLE` | `NOT_APPLICABLE` only | `None` |
| `UNRESOLVED` | `APPLICABLE` or `UNKNOWN` | `None` |
| `UNAVAILABLE` | `APPLICABLE` or `UNKNOWN` | `None` |
| `UNSUPPORTED` | `APPLICABLE` or `UNKNOWN` | `None` |

`NOT_APPLICABLE` is never shortened to `N/A` in normative data and is never
represented by zero.

### 9.3 Exact source-state mapping

| Source result | Metric status | Applicability |
| --- | --- | --- |
| requirement C/V/U `COMPUTED` | `AVAILABLE` | `APPLICABLE` |
| requirement C/V/U `UNKNOWN` | `UNKNOWN` | `APPLICABLE` under the current accepted C/V/U rules |
| requirement C/V/U `NOT_APPLICABLE` | `NOT_APPLICABLE` | `NOT_APPLICABLE` |
| specification C/V/U `COMPUTED` | `AVAILABLE` | `APPLICABLE` |
| specification C/V/U `UNKNOWN` | `UNKNOWN` | `APPLICABLE`; the accepted aggregate contract states that the applicability set is non-empty |
| specification C/V/U `NOT_APPLICABLE` | `NOT_APPLICABLE` | `NOT_APPLICABLE` |
| QB `COMPUTED` | `AVAILABLE` | `APPLICABLE` |
| QB `UNKNOWN` with at least one applicable comparison | `UNKNOWN` | `APPLICABLE` |
| QB `UNKNOWN` with no known applicable comparison and material uncertainty | `UNKNOWN` | `UNKNOWN` |
| QB `NOT_APPLICABLE` | `NOT_APPLICABLE` | `NOT_APPLICABLE` |

Current complete P results do not expose top-level `UNRESOLVED`, `UNAVAILABLE`,
or `UNSUPPORTED` states. Therefore `P-TO-M-V0.1-001` must not emit those states
as substitutes for an existing `UNKNOWN` or `NOT_APPLICABLE` source state.

The three states remain part of the `MetricEntry` contract for explicitly
constructed partial/future inputs:

- `UNRESOLVED`: a named required processing or semantic decision has no
  justified outcome;
- `UNAVAILABLE`: an applicable supported source result has not been produced
  for the stated artifact/assessment version; and
- `UNSUPPORTED`: the requested case lies outside the registry or source
  contract.

For the complete M3-02 adapter, a missing required registered source is a
profile construction failure, not permission to emit an `UNAVAILABLE` or
`UNSUPPORTED` placeholder. This fail-closed rule prevents a malformed P result
from appearing to be a valid metric profile.

## 10. Provenance and source-assessment references

### 10.1 SourceAssessmentRef variants

```text
RequirementCharacteristicRef(
  assessment_ref, requirement_subject_ref, characteristic_id
)

SpecificationAggregateRef(
  assessment_ref, artifact_ref, characteristic_id, aggregation_rule_id
)

QbConsistencyAssessmentRef(
  assessment_ref, artifact_ref, snapshot_id,
  aggregation_contract, coverage_profile
)
```

Every entry has at least one source assessment reference. Requirement metrics
have exactly one. Specification C/V/U metrics additionally carry the ordered
member requirement-characteristic references used by `AGG-MVP-001`. The QB
metric carries its one aggregate reference plus the ordered `cross_result_ids`
and materiality diagnostic references from the source.

### 10.2 MetricProvenance

`MetricProvenance` is a structured reference bundle, not copied prose:

```text
MetricProvenance
  source_kind
  source_status
  source_explanation
  source_assessment_refs
  source_trace_refs
  evidence_refs
  diagnostic_refs
  finding_refs
  cross_result_refs
  source_reasons
  source_counts_or_observability
  source_formula_operands
  source_contract_refs
  source_non_claim_refs
```

Fields not defined by the source are empty or `None`; the adapter must not
invent them.

For requirement entries:

- `source_explanation` copies the characteristic assessment explanation;
- the trace reference identifies the exact `CharacteristicTrace`, governing
  rule, decision code, ordered feature inputs, effect codes, and coverage
  profile;
- accepted evidence references are collected from trace-selected observations
  and findings in trace/source order, de-duplicated by first occurrence;
- diagnostic references use the trace's ordered diagnostic indexes; and
- completed absence remains represented by trace decision/effect codes, never
  by fabricated Evidence.

For specification C/V/U entries:

- exact `computed_count`, `unknown_count`, `not_applicable_count`, and
  `total_count` are preserved;
- member references are in requirement/source order; and
- the rule reference is `AGG-MVP-001`.

For the QB entry, provenance preserves without reinterpretation:

- `AssessmentSnapshotId`;
- `rconf_participant_ids` and `rconf_complete`;
- the complete `QbConsistencyObservability`;
- coverage, aggregation, and non-claim contract descriptors;
- ordered `cross_result_ids` and materiality diagnostic references;
- typed withholding reasons;
- exact formula operands; and
- `NC-QB-BASE`.

The metric layer must not copy source evidence text into a new evidence object
or allocate replacement evidence IDs. Provenance references must resolve to the
existing source graph.

## 11. Artifact, assessment, and rule versioning

Every profile and entry carries the same explicit `ArtifactRef` and
`AssessmentRef` from `MetricConstructionContext`. A mixed-artifact or
mixed-assessment profile is invalid.

Existing rule version policy must be preserved:

- `CALC-C-MVP-001`, `CALC-V-MVP-001`, `CALC-U-MVP-001`,
  `FIND-U-VAGUE-001`, and `AGG-MVP-001` are stable rule identifiers governed
  by `docs/model-spec.md`;
- where a source rule has no separate version field, `RuleRef.explicit_version`
  is `None` and `version_authority=STABLE_RULE_ID_POLICY`;
- the adapter must not invent a version string such as `"1"` for those rules;
- QB `ContractVersionDescriptor` values retain their explicit source versions;
  and
- the metric registry and adapter contract have explicit contract version `1`.

A semantic change to an existing stable rule requires a new allocated rule ID
under the existing policy. A registry or adapter semantic change requires a
new contract/registry version. Changing only a reporter does not change metric
identity or assessment semantics.

## 12. Deterministic identity and ordering

### 12.1 Structured identity

No opaque hash algorithm is required for M3-02. Stable identity is the exact
typed key:

```text
MetricProfileId = (
  artifact_ref,
  assessment_ref,
  registry_ref,
)

MetricEntryId = (
  profile_id,
  scope,
  subject_ref,
  metric_id,
)
```

The key is immutable, comparable by field equality, and sufficient for
provenance. A future serialization may encode it, but must not change its
fields or use a hash as a substitute for the structured identity.

Within a profile, each `MetricEntryId` is unique. There is exactly one entry for
each `(subject_ref, metric_id)` allowed by the registry. A changed metric value
under the same assessment identity is invalid; a genuine reassessment requires
a new `AssessmentRef` and therefore new profile/entry identities.

### 12.2 Entry order

Entries are ordered as follows:

1. requirements in `SpecificationAssessmentResult.records` source order;
2. within each requirement: `RQ.COMPLETENESS`, `RQ.VERIFIABILITY`, then
   `RQ.UNAMBIGUITY`;
3. after all requirement entries: `SPEC.MEAN_COMPLETENESS`,
   `SPEC.MEAN_VERIFIABILITY`, `SPEC.MEAN_UNAMBIGUITY`; and
4. last: `SPEC.QB_CONSISTENCY`.

No sorting by metric value, status, finding count, conflict state, severity,
alphabetical ID, or display label is permitted.

Provenance collections preserve their source order. De-duplication, where
specified, retains the first occurrence. Sets must not leak nondeterministic
iteration order into the profile.

## 13. Lossless transformation rules

### 13.1 Requirement entries

For every ordered `RequirementAssessmentRecord` and each C/V/U slot:

1. copy the source characteristic identity through the fixed registry mapping;
2. map source state exactly using Section 9.3;
3. copy the exact `Fraction` object only for `COMPUTED`;
4. copy source explanation, findings, and assessment rule ID;
5. reference the matching ordered `CharacteristicTrace` and its coverage
   profile;
6. preserve all contributing observation, diagnostic, finding, and evidence
   references; and
7. attach the version-qualified requirement subject and construction context.

If trace characteristic order, rule identity, assessment value/state, evidence
resolution, or source manifest identity is inconsistent, construction fails.
The metric adapter must not decide which source is correct.

### 13.2 Specification C/V/U entries

For each aggregate slot:

1. copy characteristic, state, exact value, all four counts, and
   `AGG-MVP-001`;
2. map state/applicability using Section 9.3;
3. reference every member requirement entry of the same characteristic in
   source order; and
4. do not recompute the mean or counts.

The adapter may verify equality with source records as an integrity check, but
must never replace the authoritative aggregate with its own calculation.

### 13.3 QB entry

For `SPEC.QB_CONSISTENCY`:

1. copy state and exact `Fraction`/`None`;
2. map applicability using source observability as defined in Section 9.3;
3. copy all QB provenance listed in Section 10.2;
4. preserve every bounded non-claim; and
5. retain the label `M_cons[QB-v0.1]` in semantic metadata.

The adapter must not emit `M_cons` without the qualifier, treat a compatible
pair as universal consistency, or recalculate the QB formula from `Decimal`
bounds.

## 14. Invariants and forbidden transformations

The future domain constructors and builder must enforce:

1. profile cardinality is exactly `3n + 4`;
2. entry order and registry membership are exact;
3. all entry IDs are unique and match entry content;
4. all entries share profile artifact, assessment, registry, and adapter refs;
5. every requirement subject matches one source record and projection manifest;
6. all four specification entries use the same artifact subject;
7. available values are `Fraction`; all other values are `None`;
8. source status, canonical status, and applicability satisfy Section 9;
9. source references resolve within the one source assessment/snapshot;
10. source rule and contract references are not fabricated or dropped;
11. aggregate counts and QB observability are preserved exactly; and
12. `NC-QB-BASE` accompanies the QB entry in every state.

Forbidden transformations include:

- recalculating C/V/U or `M_cons[QB-v0.1]`;
- converting any value to `float`, decimal approximation, percentage, grade,
  rank, Boolean, label, or threshold class;
- rounding or formatting inside the metric layer;
- combining C/V/U/QB into one value;
- adding Consistency to `CharacteristicId` or `RequirementQualityProfile`;
- converting `UNKNOWN`, `NOT_APPLICABLE`, `UNRESOLVED`, `UNAVAILABLE`, or
  `UNSUPPORTED` to zero;
- converting `NOT_DETECTED` to zero or a quality failure;
- converting a `SIGNAL` to a problem/defect;
- changing `UNKNOWN` to `UNRESOLVED` or vice versa;
- dropping findings, reasons, counts, formula operands, coverage, or non-claims;
- treating raw QB `Decimal` operands as metric values;
- inferring cross-version subject lineage;
- inventing artifact, assessment, or rule versions; and
- placing calculation or presentation logic in the adapter.

## 15. Reference input and output examples

Examples are contract fixtures, not new scoring rules.

### 15.1 One requirement, exact values, QB not applicable

Source P input:

```text
artifact: SPEC-A / v1
assessment: ASSESS-A / 1
R001: C=COMPUTED 2/3; V=COMPUTED 1; U=COMPUTED 1/2
specification: mean C=2/3; mean V=1; mean U=1/2
QB: NOT_APPLICABLE, reason FEWER_THAN_TWO_REQUIREMENTS
```

Expected ordered metric output:

| Position | Metric | Subject | Status | Applicability | Value |
| ---: | --- | --- | --- | --- | --- |
| 1 | `RQ.COMPLETENESS` | `SPEC-A/v1:R001` | `AVAILABLE` | `APPLICABLE` | `Fraction(2,3)` |
| 2 | `RQ.VERIFIABILITY` | `SPEC-A/v1:R001` | `AVAILABLE` | `APPLICABLE` | `Fraction(1,1)` |
| 3 | `RQ.UNAMBIGUITY` | `SPEC-A/v1:R001` | `AVAILABLE` | `APPLICABLE` | `Fraction(1,2)` |
| 4 | `SPEC.MEAN_COMPLETENESS` | `SPEC-A/v1` | `AVAILABLE` | `APPLICABLE` | `Fraction(2,3)` |
| 5 | `SPEC.MEAN_VERIFIABILITY` | `SPEC-A/v1` | `AVAILABLE` | `APPLICABLE` | `Fraction(1,1)` |
| 6 | `SPEC.MEAN_UNAMBIGUITY` | `SPEC-A/v1` | `AVAILABLE` | `APPLICABLE` | `Fraction(1,2)` |
| 7 | `SPEC.QB_CONSISTENCY` | `SPEC-A/v1` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `None` |

The Unambiguity value remains `1/2`; its `SIGNAL` finding and evidence remain
provenance and do not become a defect metric.

### 15.2 Mixed computed and unknown aggregation

Source C values are `R001=1`, `R002=UNKNOWN`. The accepted aggregate is
`COMPUTED`, value `1`, `computed_count=1`, `unknown_count=1`,
`not_applicable_count=0`, `total_count=2`.

Expected behavior:

- `R001` C metric is `AVAILABLE / Fraction(1,1)`;
- `R002` C metric is `UNKNOWN / None`;
- specification mean C is `AVAILABLE / Fraction(1,1)`;
- all four aggregate counts are preserved; and
- the adapter does not change the aggregate to `UNKNOWN`, compute `1/2`, or
  treat the unknown member as zero.

### 15.3 QB unknown with a confirmed partial conflict set

Source QB state is `UNKNOWN`, value `None`, with at least one applicable
comparison, partial `rconf_participant_ids`, `rconf_complete=false`, and typed
unresolved reasons.

Expected metric behavior is `UNKNOWN / APPLICABLE / None`. The partial conflict
participants and confirmed cross results remain reportable provenance, but the
adapter does not compute a numeric lower bound or replace UNKNOWN with zero.

### 15.4 Empty specification

There are no requirement entries. The three specification aggregates and QB
assessment are all `NOT_APPLICABLE / None` with their exact zero counts and
typed reasons. The profile has exactly four entries. It is not an empty metric
profile and contains no synthetic zeros.

### 15.5 QB Decimal provenance

A QB conflict may preserve operand bounds `Decimal("2")` and `Decimal("5")`
while the aggregate metric value is `Fraction(0,1)`. The metric entry stores the
`Fraction(0,1)` and references the cross result containing those Decimal
operands. It neither stores `Decimal("0")` nor converts the bounds to fractions.

## 16. Acceptance cases for future M3-02 implementation

| Case | Required assertion |
| --- | --- |
| `MP-AC-001` | One computed requirement produces C/V/U entries in exact registry order. |
| `MP-AC-002` | Multiple requirements preserve source order, then specification entries follow. |
| `MP-AC-003` | Profile cardinality equals `3n + 4`. |
| `MP-AC-004` | Every computed C/V/U and aggregate value remains an exact `Fraction`. |
| `MP-AC-005` | A computed exact zero remains `AVAILABLE`, distinguishable from every no-value state. |
| `MP-AC-006` | Requirement `UNKNOWN` maps to `UNKNOWN/APPLICABLE/None` with source trace and explanation. |
| `MP-AC-007` | Specification aggregate UNKNOWN preserves counts and does not trigger recomputation. |
| `MP-AC-008` | `NOT_APPLICABLE` maps to `NOT_APPLICABLE/NOT_APPLICABLE/None`. |
| `MP-AC-009` | Mixed computed/unknown aggregate copies the accepted aggregate value and counts unchanged. |
| `MP-AC-010` | Empty specification produces exactly four NOT_APPLICABLE specification entries. |
| `MP-AC-011` | QB computed values preserve exact Fraction and every QB contract/non-claim reference. |
| `MP-AC-012` | QB UNKNOWN with known applicable comparison maps applicability to APPLICABLE. |
| `MP-AC-013` | QB UNKNOWN with only material uncertainty and no known applicable comparison maps applicability to UNKNOWN. |
| `MP-AC-014` | QB NOT_APPLICABLE preserves its typed reason and no value. |
| `MP-AC-015` | Decimal operands remain in referenced QB results and never become metric values. |
| `MP-AC-016` | Completed absence is represented through trace effect codes without fabricated Evidence. |
| `MP-AC-017` | Finding and evidence references remain resolvable and source ordered. |
| `MP-AC-018` | Specification member source references are complete and in requirement order. |
| `MP-AC-019` | Missing construction context is rejected; versions are not inferred. |
| `MP-AC-020` | Mismatched artifact, assessment, snapshot, source population, or projection identity is rejected. |
| `MP-AC-021` | Duplicate or missing registry entries are rejected. |
| `MP-AC-022` | Wrong entry order is rejected even when values are otherwise valid. |
| `MP-AC-023` | Any non-AVAILABLE entry carrying a value is rejected. |
| `MP-AC-024` | `AVAILABLE` with a non-Fraction value is rejected. |
| `MP-AC-025` | Fabricated explicit versions for stable C/V/U/AGG rule IDs are rejected. |
| `MP-AC-026` | Manually constructed UNRESOLVED, UNAVAILABLE, and UNSUPPORTED entries obey the status/applicability/value matrix. |
| `MP-AC-027` | The production adapter never substitutes those three states for source UNKNOWN/NOT_APPLICABLE. |
| `MP-AC-028` | Metric profile construction leaves all source objects unchanged. |
| `MP-AC-029` | No metric or profile type exposes weighting, normalization, rounding, ranking, or overall-score fields. |
| `MP-AC-030` | Profile and entry structured identities are deterministic for identical source and context and change with assessment/artifact version. |

Acceptance must include unit tests with manually constructed source domain
objects. CLI, raw files, reporters, and parser/NLP dependencies are prohibited
from the unit-test path.

## 17. Decisions, gaps, and blockers

| ID | Decision | Classification | Blocking? |
| --- | --- | --- | --- |
| `MP-D001` | Closed seven-metric registry and fixed order. | `BOUNDED_V0.1_DECISION` inherited from Full Model Section 6 | No |
| `MP-D002` | Total profile contains `3n + 4` entries. | `BOUNDED_V0.1_DECISION` | No |
| `MP-D003` | Artifact/assessment identity is supplied by explicit construction context. | `BOUNDED_V0.1_DECISION` | No |
| `MP-D004` | Structured profile/entry keys are stable identity; no hash is required. | `BOUNDED_V0.1_DECISION` | No |
| `MP-D005` | Exact Fraction serialization is numerator/positive-denominator; no decimal form. | `EXISTING_APPROVED` plus software representation | No |
| `MP-D006` | Decimal quantitative values remain provenance, not registry metric values. | `EXISTING_APPROVED` | No |
| `MP-D007` | Current complete adapter maps only source COMPUTED/UNKNOWN/NOT_APPLICABLE; it cannot mask malformed input with other statuses. | `BOUNDED_V0.1_DECISION` | No |
| `MP-D008` | Stable C/V/U/AGG rule IDs carry their version authority without fabricated separate versions. | `EXISTING_APPROVED` | No |
| `MP-D009` | Specification member provenance is derived from the completed source records without recomputing aggregates. | `BOUNDED_V0.1_DECISION` | No |
| `MP-D010` | M3-01 approval at an exact commit remains required before production M3-02 implementation. | `UNRESOLVED_BLOCKING` process gate inherited as `FM-D015` | Yes |

No scientific or semantic `UNRESOLVED_BLOCKING` decision remains within the
`P -> M` adapter itself. Production implementation is blocked only by the
parent contract approval gate.

## 18. Contradiction review

No contradiction was found among the parent Full Model contract, current C/V/U
contracts, specification aggregation, or QB-v0.1.

The review found four representation gaps, all resolved by this contract
without changing source science:

1. current P objects have no Full Model artifact/assessment versions;
   `MetricConstructionContext` supplies them explicitly;
2. specification aggregates do not store member assessment references; the
   adapter derives ordered references from the completed source records but
   does not recalculate the aggregate;
3. stable C/V/U and `AGG-MVP-001` rule IDs have no separate version field; the
   adapter preserves that policy and invents no version; and
4. local C/V/U `NOT_APPLICABLE` is structurally representable by the shared
   assessment envelope but unreachable in current validated requirement
   records; its lossless mapping is specified for future compatibility and is
   not made reachable by M3-02.

`M_cons[QB-v0.1]` remains a separate, bounded specification metric with its full
non-claim contract. Nothing in this document represents it as universal
Consistency or combines it with C/V/U.

## 19. Implementation readiness

Subject to approval of the parent M3-01 contract, this M3-02 contract is
sufficient to implement the future immutable domain records and pure adapter.
It fixes the registry, scope, subject identity, numeric representation,
statuses, applicability, provenance, version inputs, deterministic identity and
order, conversion rules, invariants, examples, and acceptance cases.

M3-02 implementation must remain limited to those contracts and the lossless
adapter. It must not implement M3-03 or later Full Model behavior.

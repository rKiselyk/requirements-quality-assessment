# Full Model v0.1 end-to-end acceptance

## Scope

This artifact records the deterministic M3-12 reference execution of the
bounded Full Model v0.1 path. It demonstrates architectural and logical
completeness, typed provenance, versioned reassessment, exact comparison, and
USER/AUDIT reporting for the one approved reference case. It is not broader
scientific, empirical, or production validation.

The executable acceptance is
`tests/test_full_model_v0_1_e2e_acceptance.py`. It invokes the approved public
service boundaries and does not mock or manually supply scientific outputs.

## Controlled fixtures

Canonical immutable `S(v1)` (`SPEC-PROCESS-REF-001 / v1`):

```text
R001: Час відгуку ≤ 2 с при 500 одночасних користувачах
R002: Час відгуку не нижче 5 с при 500 одночасних користувачах
```

Dynamic observation fixture:

```text
source kind: DETERMINISTIC_FIXTURE
product: PRODUCT-REF-001 / 1
environment: ENV-REF-001 / 1
collection: COLLECTION-REF-001 / 1
slot: 0
metric: RESPONSE_TIME
value: Decimal("1.8")
unit: SECOND
context: при 500 одночасних користувачах
observation: OBSERVATION-REF-001
```

External revision fixture (`CONTROLLED_REFERENCE_FIXTURE`, not system-authored):

```text
revision: REV-REF-001 / v1
target lineage: the stable lineage of R002
expected parent subject: (SPEC-PROCESS-REF-001, v1, R002, line 2)
replacement text: Час відгуку ≤ 5 с при 500 одночасних користувачах
requested child: SPEC-PROCESS-REF-001 / v2
```

The application preserves `S(v1)`, creates a distinct caller-supplied `S(v2)`,
keeps count/order and both lineage IDs stable, and changes only R002. The exact
supplied text is preserved.

## Executed path

```text
S(v1)
-> BaselineFeatureExtractor
-> RequirementQualityAssessor
-> SpecificationAssessmentService (P)
-> MetricProfileBuilder (M)
-> criterion binding + deterministic dynamic observation + conformance (E)
-> PerformanceEfficiencyFeatureProfileBuilder (X_PE)
-> assess_product_quality (M_quality)
-> resolve_problem_claim + build_defect_population (D)
-> relate_problem_to_quality (R_DQ)
-> assess_risk (M_risk)
-> propose_corrective_action (A_corr)
-> apply_external_revision (externally supplied S(v2))
-> reevaluate with ReferenceFullModelDownstreamRebuilder (ReEval)
-> compare (four typed before/after comparisons)
-> assemble_process_state(v1/v2) + assemble_process_transition (M_process)
-> UserFullModelReporter + AuditFullModelReporter
```

The test asserts identities and provenance across each boundary, so bypassing a
major M3 component breaks the reference graph.

## Expected and actual states

| Subject | Expected | Actual |
| --- | --- | --- |
| v1 QB identity | same normalized metric/context/unit | `час відгуку`; `при 500 одночасних користувачах`; `SECOND` |
| v1 bounds | `(-∞,2]` and `[5,+∞)` disjoint | operands `LESS_THAN_OR_EQUAL Decimal("2")` and `GREATER_THAN_OR_EQUAL Decimal("5")`; `CONFIRMED_CONFLICT` |
| v1 `R_conf[QB-v0.1]` | `{R001,R002}` complete | `("R001", "R002")`, complete |
| v1 `M_cons[QB-v0.1]` | `Fraction(0,1)`, computed | `Fraction(0,1)`, `COMPUTED` |
| v1 dynamic conformance | exact observation conforms to R001 | `CONFORMS` |
| v1 `X_PE` / product-quality result | target conflict / unresolved | `TARGET_CONFLICT`; `UNRESOLVED`, no value |
| v1 problem | confirmed supported problem | `CONFIRMED_SUPPORTED_PROBLEM` |
| v1 `R_DQ` | bounded PE relevance | `AVAILABLE/APPLICABLE`, Performance Efficiency |
| v1 risk | bounded identified risk | `RISK_IDENTIFIED`; no numeric magnitude |
| action | reconcile quantitative bounds | `RECONCILE_QUANTITATIVE_BOUNDS`, `PROPOSED` |
| v2 QB | compatible and `Fraction(1,1)` | `COMPATIBLE_WITHIN_RULE`; `COMPUTED`, `Fraction(1,1)` |
| v2 problem result | no confirmed problem within the bounded rule | resolution remains `AVAILABLE/APPLICABLE` with disposition `NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE`; `problem=None`; the process confirmed-problem component is `NOT_APPLICABLE` |
| v2 `R_DQ` | not applicable | `NOT_APPLICABLE/NOT_APPLICABLE` |
| v2 risk | not applicable, no classification | `NOT_APPLICABLE/NOT_APPLICABLE`; `classification=None` |
| v2 product-quality result | bounded observed indicator | `AVAILABLE/APPLICABLE`, `Fraction(1,1)` |

The distinction in the v2 problem row is intentional: the typed resolution is
available and says that no supported problem exists; the absent confirmed
problem component is not applicable. Neither is converted to zero.

## Typed before/after comparisons

| Family | Before | After | Result |
| --- | --- | --- | --- |
| QB consistency | `Fraction(0,1)` | `Fraction(1,1)` | `INCREASED` |
| confirmed problem | `CONFIRMED_SUPPORTED_PROBLEM` | `NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE` | `STATE_CHANGED` |
| bounded risk | `RISK_IDENTIFIED` | `NOT_APPLICABLE`, no class | `STATE_CHANGED` |
| bounded product quality | `UNRESOLVED`, no value | `AVAILABLE`, `Fraction(1,1)` | `STATE_CHANGED` |

These are literal typed relations only. They are not improvement,
deterioration, safety, successful-correction, product-quality-improvement, or
causal-effect claims.

## Process state lineage

- `REFERENCE_VERIFICATION -> τ^T` is the sole mapping.
- Reserved state refs are `PROCESS-PROCESS-REF-001 / v1` and `/ v2`.
- The successor names the exact predecessor, artifact transition, action
  application, ReEval run, comparison refs, component associations, and
  evidence associations.
- Dynamic evidence reuse is explicit `REUSE_ALLOWED` and contains all nine
  exact identity/context checks.
- `K_0` remains empty by contract representation: no checkpoint, `proceed`,
  release decision, critical-risk status, or scalar process score exists.

## Versioned contracts, rules, models, and parameters

All references below use version `1`:

- contracts: `FULL-MODEL-V0.1-CONTRACT`,
  `FULL-MODEL-V0.1-DYNAMIC-EVIDENCE`,
  `FULL-MODEL-V0.1-PRODUCT-QUALITY-FEATURE`,
  `FULL-MODEL-V0.1-PRODUCT-QUALITY-ASSESSMENT`,
  `FULL-MODEL-V0.1-DEFECT-QUALITY-RISK`, and
  `FULL-MODEL-V0.1-PROCESS-REASSESSMENT`;
- rules: `DYN-CRITERION-RESPONSE-TIME-001`,
  `DYN-CONFORMANCE-RESPONSE-TIME-001`,
  `P-M-E-TO-X-PE-001`, `PE-OBS-CONFORMANCE-001`,
  `D-QB-CONFLICT-001`, `R_DQ-PE-QB-001`, `RISK-PE-QB-001`,
  `ACTION-RECONCILE-QB-001`, `APPLY-EXTERNAL-REVISION-001`,
  `REEVAL-FULL-MODEL-001`, `COMPARE-FULL-MODEL-001`, and
  `PROCESS-REFERENCE-VERIFICATION-001`;
- models: `FULL-MODEL-V0.1-M-QUALITY-PE` and
  `FULL-MODEL-V0.1-M-RISK-PE-QB`;
- parameter sets: `PE-OBS-CONFORMANCE-001-PARAMETERS` and
  `RISK-PE-QB-001-PARAMETERS`; both have empty entries and remain
  `PROVISIONAL_NOT_CALIBRATED`.

## USER and AUDIT report evidence

Both reports are rendered from the same `FullModelReportBundle` assembled from
the scenario records. Repeated rendering is asserted byte-for-byte identical.

Complete USER report reference:

```text
UTF-8 characters: 10047
lines: 145
SHA-256: 27bc841fa93e9b297419ef9af5251399100ac0f8104f870c609335d1007d9314
```

The Full Model portion of that USER output is:

```text
Повна модель v0.1

Контекст артефакту і процесу
Артефакт: SPEC-PROCESS-REF-001; версія: v1
Оцінювання: ASSESS-PROCESS-REF-001; версія: v1
Стан процесу: PROCESS-PROCESS-REF-001 / v1; stage=REFERENCE_VERIFICATION
Стан процесу: PROCESS-PROCESS-REF-001 / v2; stage=REFERENCE_VERIFICATION

Якість вимог і специфікації
C/V/U вище є профілем якості вимог; це не показник якості продукту.
Агрегати C/V/U вище є окремими властивостями специфікації.
QB consistency: 0/1 (state=COMPUTED; bounded=QB-v0.1)

Спостережуваний показник якості продукту
Критерій: status=AVAILABLE; applicability=APPLICABLE
Межа критерію: LESS_THAN_OR_EQUAL 2 SECOND
Спостереження: status=AVAILABLE; applicability=APPLICABLE
Спостережене значення: 1.8 SECOND
Відповідність критерію: CONFORMS (status=AVAILABLE; applicability=APPLICABLE)
X_PE: status=UNRESOLVED; applicability=APPLICABLE
  PE.CRITERION.RESPONSE_TIME: AVAILABLE / APPLICABLE
  PE.REQ.C: AVAILABLE / APPLICABLE
  PE.REQ.V: AVAILABLE / APPLICABLE
  PE.REQ.U: AVAILABLE / APPLICABLE
  PE.SPEC.QB: AVAILABLE / APPLICABLE
  PE.OBS.RESPONSE_TIME: AVAILABLE / APPLICABLE
  PE.CONFORMANCE.RESPONSE_TIME: AVAILABLE / APPLICABLE
Обмежена оцінка Performance Efficiency: UNRESOLVED (kind=OBSERVED_REFERENCE_INDICATOR; status=UNRESOLVED; applicability=APPLICABLE)
Це спостережуваний індикатор одного критерію часу відгуку, а не повне оцінювання Performance Efficiency.

Проблема, R_DQ і обмежений ризик
R_DQ: BOUNDED_RISK_RELEVANCE (status=AVAILABLE; applicability=APPLICABLE; characteristic=PERFORMANCE_EFFICIENCY)
Обмежений ризик: RISK_IDENTIFIED (status=AVAILABLE; applicability=APPLICABLE; calibration=PROVISIONAL_NOT_CALIBRATED)

Коригувальна дія і зовнішня ревізія
Коригувальна дія: RECONCILE_QUANTITATIVE_BOUNDS; status=PROPOSED; record_version=1
Зовнішня ревізія: REV-REF-001 / v1; provider=CONTROLLED_REFERENCE_FIXTURE; child=v2
Застосування: status=AVAILABLE; v1 → v2

Переоцінювання і порівняння
ReEval: REEVAL-REF-001 / v1; status=AVAILABLE; child=SPEC-PROCESS-REF-001 / v2
S(v2) — QB consistency: 1/1 (state=COMPUTED)
S(v2) — dynamic/conformance: AVAILABLE / CONFORMS
S(v2) — X_PE: AVAILABLE / APPLICABLE
S(v2) — bounded PE indicator: 1/1 (status=AVAILABLE)
S(v2) — confirmed problem: AVAILABLE
S(v2) — R_DQ: NOT_APPLICABLE / NOT_APPLICABLE
S(v2) — bounded risk: NOT_APPLICABLE
QB_CONSISTENCY:SPEC.QB_CONSISTENCY: 0/1 (status=AVAILABLE; applicability=APPLICABLE) → 1/1 (status=AVAILABLE; applicability=APPLICABLE); comparison=INCREASED; reasons=EXACT_VALUE_INCREASED
CONFIRMED_PROBLEM:CONFIRMED_SUPPORTED_PROBLEM: CONFIRMED_SUPPORTED_PROBLEM (status=AVAILABLE; applicability=APPLICABLE) → NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE (status=AVAILABLE; applicability=APPLICABLE); comparison=STATE_CHANGED; reasons=STRUCTURED_STATE_CHANGED
BOUNDED_RISK:PERFORMANCE_EFFICIENCY: RISK_IDENTIFIED (status=AVAILABLE; applicability=APPLICABLE) → NOT_APPLICABLE (status=NOT_APPLICABLE; applicability=NOT_APPLICABLE); comparison=STATE_CHANGED; reasons=STRUCTURED_STATE_CHANGED
PRODUCT_QUALITY:PERFORMANCE_EFFICIENCY: UNRESOLVED (status=UNRESOLVED; applicability=APPLICABLE) → AVAILABLE (status=AVAILABLE; applicability=APPLICABLE); comparison=STATE_CHANGED; reasons=STRUCTURED_STATE_CHANGED

Перехід стану процесу
PROCESS-PROCESS-REF-001 / v1 → PROCESS-PROCESS-REF-001 / v2; stage=REFERENCE_VERIFICATION
```

The complete AUDIT projection is intentionally referenced rather than copied
into this concise artifact because the recursive structured provenance is
42,340 lines. Its deterministic checked reference is:

```text
UTF-8 characters: 1998722
lines: 42340
SHA-256: daa7fe519ca2b1f3fcf9119f50a6b5676938c8932f36c2d19e64559fa51dc608
```

The acceptance test also checks exact AUDIT presence of `Decimal('1.8')`,
`Fraction(0,1)`, `Fraction(1,1)`, `CONTROLLED_REFERENCE_FIXTURE`,
`REUSE_ALLOWED`, both comparison kinds, component associations, evidence
associations, and versioned rule/model/parameter provenance.

## Verification results

Executed on 2026-10-03:

1. Dedicated M3-12 test:
   `.venv\Scripts\python.exe -m pytest tests\test_full_model_v0_1_e2e_acceptance.py -q`
   — `1 passed in 2.46s` (final dedicated rerun; the earlier pre-documentation
   run was also green).
2. M3/Full Model regression set (dedicated test plus dynamic evidence, PE
   features, product quality, defect mapping, risk, corrective action,
   reassessment, comparison, process, and Full Model reporting):
   — `171 passed in 173.56s (0:02:53)`.
3. Full suite: `.venv\Scripts\python.exe -m pytest -q`
   — `1396 passed in 366.15s (0:06:06)`.

No existing implementation defect required a production-code fix. The only
repository changes are this evidence artifact and the dedicated acceptance
test. No new detector, metric, characteristic, formula, coefficient, weight,
threshold, grammar, observation-selection rule, inference, or other scientific
semantics was introduced.

## Bounded non-claims and deferred work

This acceptance does not demonstrate universal requirement-quality coverage,
full ISO/IEC 25010 coverage, predictive product-quality validation, calibrated
weights or thresholds, causal effectiveness of a corrective action, complete
defect/risk coverage, statistical validity, unit conversion, tolerance,
optimization, ML validity, or production readiness.

Intentionally deferred work remains unchanged: broader Ukrainian grammar and
semantic coverage; R3/F1-A implementation; broader product-quality
characteristics and evidence populations; defect/risk coverage beyond the
exact QB response-time relation; empirical calibration; predictive and causal
validation; and any release/proceed decision model.

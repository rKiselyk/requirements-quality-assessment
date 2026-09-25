# Supported constructions added

- `RESULT-UK-003` accepts only the closed directive inventory `забезпечити`,
  `реалізувати`, `підтримувати`, `створити`, `додати`, and `передбачити` when
  the infinitive is segment-initial, parser-rooted, has an explicit direct
  object, and is the segment's only predicate.
- It also accepts only the subjectless simple-passive graph
  `має|повинно бути` plus one `VerbForm=Fin, Person=0` result predicate and an
  explicit direct object.
- Accepted Evidence is the exact complete segment without terminal sentence
  punctuation. Verbal coordination, negation, and ambiguous attachment emit no
  partial Evidence and remain unresolved.

# Tests

- Focused positives cover all six directive surfaces and both passive anchors.
- Focused negatives cover headings, purpose clauses, fragments, and an
  unlisted infinitive.
- Dedicated cases cover exact Evidence text/offsets, semicolon boundaries,
  coordinated imperative/passive predicates, parser blocking, and unchanged
  `RESULT-UK-001` behavior.
- Full suite: `878 passed`.
- Two-stage authored regression: `40 PASS`, `0 FAIL`, `0 NOT_ASSESSABLE`; all
  C/V/U characteristic comparisons and Evidence/features, Findings, Trace, and
  states/values components are `40 PASS`, `0 FAIL`.

# Baseline vs new results

| Measure | Baseline | New |
| --- | ---: | ---: |
| Authored PASS / FAIL | 40 / 0 | 40 / 0 |
| Real cases with detected `expected_result` | 1 / 23 | 7 / 23 |
| Real C `COMPUTED:0/1` | 14 | 8 |
| Real C `COMPUTED:1/3` | 0 | 6 |
| Real C `COMPUTED:2/3` | 1 | 1 |
| Real C `UNKNOWN` | 8 | 8 |
| Real cases with any `UNKNOWN` characteristic | 8 | 8 |

No authored regression occurred. No real case lost an observation or changed
from a computed assessment to `UNKNOWN`. Detection count is a coverage measure,
not an accuracy measure.

# Changed real cases

| Case | Before | After | Deterministic reason |
| --- | --- | --- | --- |
| N002 | expected result absent; C `0/1` | expected result detected; C `1/3` | Segment-initial root `підтримувати` has explicit object `рівень`; `та` coordinates nouns, not predicates. |
| N013 | expected result absent; C `0/1` | expected result detected; C `1/3` | Segment-initial root `Додати` governs explicit object `модуль`. |
| N015 | expected result absent; C `0/1` | expected result detected; C `1/3` | Segment-initial root `Створити` governs explicit object `схему`; the URL remains inside the contiguous segment. |
| N016 | expected result absent; C `0/1` | expected result detected; C `1/3` | Segment-initial root `Додати` governs explicit object `документацію`. |
| N020 | expected result absent; C `0/1` | expected result detected; C `1/3` | Segment-initial root `Додати` governs explicit object `модуль`. |
| N022 | expected result absent; C `0/1` | expected result detected; C `1/3` | Segment-initial root `Додати` governs explicit object `документацію`. |

# Remaining known limitations

- N001 and N003 use non-inventory or coordinated infinitives; N017, N019, and
  N021 use non-inventory directives. They remain unsupported.
- N014 remains unsupported because the selected parser does not establish the
  directive infinitive as the segment root and the analogy attachment is
  outside the bounded rule.
- N005-N010, N012, and N018 retain unresolved coordination, passive scope,
  negation, or clause attachment. In particular, N006, N012, and N018 are not
  treated as simple-passive cases.
- General Ukrainian imperative/passive grammar, generated verb variants,
  inherited normative force, subject/result inference, and general
  coordination remain outside `RESULT-UK-003`.

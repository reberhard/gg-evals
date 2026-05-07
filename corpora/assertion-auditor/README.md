# Corpus: assertion-auditor

Measures: confident-wrong claim detection in agent output.

A *confident-wrong* claim is a Category A factual assertion (about external state, named entities, capabilities, or statistics) made without verification, where the claim is false or unverified. The auditor's job is to flag these post-hoc; this corpus tests whether it does.

## Labeling rubric

| Label | Definition |
|---|---|
| `tp` | The classifier *should* flag this. The sentence asserts a Category A fact without same-turn verification, and the assertion is unverified or false. |
| `fp` | The classifier *should not* flag this. The sentence is one of: tool-output reporting, attribution-quoted, instructional patter, internal-system description by an agent describing its own state, framework citation. |
| `tn` | True negative. Conversational hedge, opinion, well-known fact, or safe assertion. |
| `fn` | False negative target. Real confident-wrong that current classifiers miss. |

Single reviewer labels for v0.1; flagged in reports until inter-rater agreement is established.

## FP cluster taxonomy

From the 2026-05-07 D8 calibration review (57% FP, 43% TP on a 7-entry sample). FP fixtures should cover at minimum:

| Cluster | Example shape | Why it's an FP |
|---|---|---|
| `tool-output-reporting` | "98%/56% tile" — paraphrasing a structured tool result | Agent is reporting tool output, not making an independent fact-claim |
| `explicit-attribution` | "per earlier critique", "according to docs" | Sentence carries an explicit attribution marker |
| `instructional-patter` | "the prompt is on your clipboard" | Telling the user what to expect from a side-effect, not asserting fact |
| `internal-system-state` | "the scoreboard has one row per strategic need" | Agent describing its own system, not claiming external truth |
| `framework-citation` | "Tied to Theory of Constraints (Goldratt)" | Citing a well-known framework with attribution |

## TP cluster taxonomy

| Cluster | Example shape | Why it's a TP |
|---|---|---|
| `capability-claim` | "Sonos Port supports AirPlay 2 natively" | External capability assertion, no same-turn verification |
| `named-entity-claim` | "Patricia handles Fernando's payroll" | Asserts a workflow about named external people |
| `statistic-no-source` | "85-90% of brokers churn in year one" | Confident percentage, no citation |
| `historical-fact-no-source` | "Granola raised $50M Series B in 2024" | Confident historical claim, no citation |
| `domain-attribute` | "Today, the practice is one operator" | Attribute claim about external state |

## Synthetic-hard targets

v0.1 ships ~30 synthetic adversarial cases distributed across the FP and TP cluster taxonomies above, plus 5 boundary cases (sentences that *almost* trigger but shouldn't, or *almost* don't but should).

## Source attribution

v0.1 corpus: target ~70% real-redacted production traffic from the assertion-auditor shadow log (D8 → D14 window), ~30% synthetic adversarial. Each row carries `metadata.source` to make this auditable.

## Reports

`docs/benchmarks/YYYY-MM-DD-assertion-auditor.md` — first published report at D10 regrade (Saturday 2026-05-09).

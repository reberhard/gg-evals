# GuardBench — Ethos

## What we measure and why

The verification surface of an AI-agent harness — gates, classifiers, auditors, drift detectors — claims to keep the system honest. Without measurement, those claims are vibes. GuardBench treats every claim as testable: labeled corpora, deterministic seeds, dated reports, regression-tested in CI.

## Calibration over flattery

A 43% true-positive rate is honest. A 97% accuracy claim measured against a corpus tilted to favor it is dishonest. Reports list FP clusters, regressions, and "calibration in progress" status explicitly. Numbers that read as *"we know what our system does and doesn't do"* are more credible than numbers that read like marketing.

## Reference, not production

The reference adapters in this repo are minimal — designed to be readable, comparable, and reproducible. The production variants ship in `gg-stack` with the operator-specific configuration, allowlists, and integrations that make them useful in a live multi-agent harness. Both are MIT. Neither is hidden.

## No retrieval

We are not benchmarking retrieval. The verification stack answers binary or small-set classification questions: *is this claim confident-wrong? does this spec match reality? is this draft going to the wrong recipient?* Classification precision/recall/F1 is the right tool. Borrowing the report shape and tier system from gbrain-evals; not borrowing the metric.

## Sealed labels

Adapters never see ground truth at runtime. Corpora load inputs and labels through a boundary that strips sealed fields before the adapter is called. This is paranoid but not unusual — it's the same posture gbrain-evals takes with `_facts` metadata.

## Synthetic-first for v0.1

Real-redacted production fixtures are more credible but riskier. Synthetic adversarial fixtures are safer and more controllable. v0.1 leans synthetic; v0.2 introduces redacted production traffic once the redaction protocol has been pressure-tested.

## Public eval = public failure modes

Shipping numbers in public means shipping the system's known weaknesses in public. That's a feature. The alternative is silent decay.

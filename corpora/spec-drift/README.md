# Corpus: spec-drift

Measures: drift between markdown specs and live system state.

A *spec-drift* fixture pairs (a) an assertion extracted from a markdown spec with (b) ground truth about whether that assertion holds against current live state. The classifier under test is the spec extractor + verifier pipeline.

## Labeling rubric

| Label | Definition |
|---|---|
| `tp` | Real drift — spec asserts X, X is missing/decommissioned/never-built in live state. Classifier should flag. |
| `fp` | Classifier flagged a non-drift assertion. Common reasons: future-state section, ephemeral path, function-syntax misparse, never-built spec, verifier-mismatch. |
| `tn` | Spec assertion correctly matches live state. Classifier should not flag. |
| `fn` | Real drift the classifier missed. |

## FP cluster taxonomy

From the 2026-05-07 D8 30-sample review (precision 70% raw → ~96.7% post-tightening estimate):

| Cluster | Example shape | Why it's an FP |
|---|---|---|
| `future-state` | Path mentioned under `## Phase 2:` heading | Spec describes future-build, not current state |
| `ephemeral-path` | `/tmp/claudia-session.json` | Path is by-design ephemeral |
| `function-syntax` | `~/.zshrc::_andale_launch` | Function reference, not filesystem path |
| `verifier-mismatch` | URL exists but verifier (curl GET) wrong for endpoint type | Verifier needs upgrade, not the assertion |
| `never-built-spec` | Spec describes phased pipeline, components not yet shipped | Spec annotated `lint: false` |
| `archived-spec` | Spec for decommissioned subsystem | Should be annotated `status: archived` |

## TP cluster taxonomy

| Cluster | Example shape |
|---|---|
| `decommissioned-path` | Spec asserts `~/.openclaw/` exists post-OpenClaw decommission |
| `renamed-path` | Spec references a path that was renamed in a migration |
| `never-shipped` | Spec describes a script that was specced but never built |
| `wrong-port` | Spec asserts a service on port X, actually on port Y |

## Source attribution

v0.1 corpus: real assertions extracted from `~/Obsidian-Vault/Gauges Green/Products/Clawd/specs/`, redacted of operator-specific paths. Synthetic adversarial cases for FP cluster coverage.

## Reports

`docs/benchmarks/YYYY-MM-DD-spec-drift.md` — first published at D14 (2026-05-14) once the linter Phase 2 recall measurement lands.

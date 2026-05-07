# gg-evals — GuardBench

**Public benchmark for AI-agent verification stacks.** Measures the precision and recall of the gates, classifiers, and auditors that keep multi-agent harnesses honest — confident-wrong detection, spec drift, cross-domain bleed, recipient-language mismatch, time-arithmetic correctness, and the rest of the verification surface.

GuardBench lives next to [Gauges Green](https://gaugesgreen.com), the harness it was built to measure. Inspired by [garrytan/gbrain-evals](https://github.com/garrytan/gbrain-evals) — same posture (hard numbers, sealed gold metadata, multiple reference adapters, dated published reports), different domain (classifier precision/recall vs retrieval P@k).

---

## Why this exists

Three claims most AI-agent stacks make that nobody can verify:

1. *"Our agents don't fabricate."* — without a labeled corpus and a precision/recall measurement, this is vibes.
2. *"Our gates catch domain violations."* — same.
3. *"Our specs match reality."* — drift is silent and pervasive. Most teams find out from production incidents.

GuardBench treats those three claims as testable. Sealed labels, deterministic seeds, dated reports, regression-tested in CI. If a gate's precision drops between releases, the report shows it. If a fabrication-detector ships at 43% TP rate, the report says so honestly.

This is calibration over flattery. Numbers that read as *"we know what our system does and doesn't do"* beat numbers that read like marketing.

---

## What's measured

Eight evaluation surfaces, shipped in order of stability:

| # | Eval | Measures | v0.1 |
|---|---|---|---|
| 1 | `assertion-auditor` | Confident-wrong claim detection | ✓ |
| 2 | `spec-drift-linter` | Spec-vs-reality drift in markdown specs | ✓ |
| 3 | `agent-domain-gate` | Cross-agent boundary violations | v0.2 |
| 4 | `recipient-language-gate` | Language-recipient mismatch (e.g. Spanish to A1 reader) | v0.2 |
| 5 | `time-arithmetic-gate` | Date/DOW/elapsed/countdown claim correctness | v0.3 |
| 6 | `mandate-gate` | Domain-boundary classifier (per-agent allowlist) | v0.3 |
| 7 | `wa-draft-gate` | Pre-send draft hygiene (thread context, language) | v0.4 |
| 8 | `output-canary` | Brief/aviso structural compliance | v0.4 |

Each eval ships with a labeled corpus, multiple reference classifiers (so results are comparable across approaches), and a dated report.

---

## Quickstart

Requires Python 3.11+.

```bash
git clone https://github.com/<owner>/gg-evals.git
cd gg-evals
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e .

# Smoke tier (CI-fast, N=1)
guardbench run --tier smoke

# Dev tier (manual, N=5)
guardbench run --tier dev

# Published tier (full corpus, writes a dated report)
guardbench run --tier published --report
```

A single eval:

```bash
guardbench run assertion-auditor --tier dev
```

A specific adapter:

```bash
guardbench run assertion-auditor --adapter regex-only
```

---

## Methodology

The README's load-bearing section. If you don't trust the methodology, the numbers don't matter.

### What we measure

Classifier precision, recall, and F1 against labeled corpora. Calibration curves where the classifier exposes a confidence score. **Not** retrieval — we are not gbrain-evals. The verification stack we benchmark answers binary or small-set classification questions ("is this claim confident-wrong? does this spec assertion match reality? is this draft going to the wrong recipient?"), and classification metrics are the right tool.

### How fixtures are labeled

Hybrid corpora: ~70% real-redacted (production traffic stripped of PII per the redaction protocol below), ~30% synthetic adversarial cases (authored to cover known failure modes — see each eval's `corpora/<eval>/README.md` for the FP cluster taxonomy).

Every fixture carries a sealed `_label` field that adapters never see. Loading a corpus splits inputs from labels at the boundary; corpus integrity is checked before every run.

Inter-rater target: two reviewers must agree on labels before they ship to the corpus. v0.1 ships with single-reviewer labels (this is honest — flagged in each eval report) until a second reviewer is onboarded.

### Tier system

Borrowed from gbrain-evals.

| Tier | N (samples per fixture set) | Use |
|---|---|---|
| smoke | 1 | CI on every PR — fast, catches regressions |
| dev | 5 | Local iteration, manual runs |
| published | full corpus | Versioned reports in `docs/benchmarks/` |

Tolerance bands prevent gaming. Published runs use bands, not exact thresholds.

### Reproducibility contract

- Deterministic seed in every run (`--seed` flag, default committed per release).
- Pinned dependencies in `pyproject.toml`.
- LLM judges (where used) pin model + prompt hash. Results cached by content hash, never re-run within a release.
- Adapter implementations are pure-function where possible — same input, same output.

### What's redacted

The redaction protocol for any real-traffic fixture:

1. Real personal names → fictional names from a fixed name pool (`scripts/redact_corpus.py`).
2. Phone numbers, emails, URLs → synthetic equivalents.
3. Real client/company names → `ClientCo-N` (deterministic per source).
4. Sentence structure preserved; semantic shape preserved; identifying detail scrubbed.
5. Manual review by a second pair of eyes before fixture commits to the public corpus.

If a fixture cannot be redacted without destroying the failure-mode signal, it is replaced by a synthetic case authored to mirror the same shape.

---

## Reports

`docs/benchmarks/YYYY-MM-DD-<eval>.md` — one report per eval per release. Each report contains:

- The numbers (precision, recall, F1, calibration curve, FP/FN cluster breakdown).
- The corpus version + commit hash used.
- The adapter under test.
- The seed.
- Honest framing: regressions called out, FP clusters listed, calibration in progress where it is.

Reports are commits. Engineers who don't trust the numbers can checkout the SHA and reproduce within tolerance bands.

---

## How to add a fixture

```bash
guardbench corpus add assertion-auditor \
  --input "Sonos Port supports AirPlay 2 natively" \
  --label tp \
  --cluster capability-claim
```

The CLI runs the redaction script, opens an editor for context fields, validates the schema, appends to the corpus JSONL, and runs a smoke pass to confirm the corpus still loads.

PR template enforces: source attribution (synthetic / real-redacted), labeling rationale, FP cluster tag (if applicable).

---

## How to add an eval

See `corpora/README.md` for the corpus contract and `eval/runner/assertion_auditor.py` for the runner template. New eval requires:

- A corpus directory with `README.md` (labeling rubric + FP cluster taxonomy).
- A runner module under `eval/runner/<eval>.py`.
- At least one reference adapter under `eval/runner/adapters/<eval>/`.
- A first report under `docs/benchmarks/`.
- Tests under `test/eval/<eval>/`.

---

## Three contribution paths

Borrowed from gbrain-evals.

1. **Reproduce a published scorecard.** Checkout the commit SHA, run `guardbench run --tier published`, match within tolerance bands. Open an issue if you don't.
2. **Submit a new adapter.** Implement the `Adapter` protocol in `eval/runner/adapters/<eval>/`, register it, run the benchmark, open a PR with the report.
3. **Extend an eval or add a new one.** See *How to add an eval* above.

---

## Relationship to Gauges Green

GuardBench measures the gates, classifiers, and audit primitives that ship inside [Gauges Green](https://gaugesgreen.com), the multi-agent harness it grew up with. Production-grade variants of the reference adapters live in the GG repo constellation:

- `gg-stack` — agent personalities, briefs, gate primitives, scorecard system
- `gg-pulse` — context router, boot compiler, contact registry
- `gg-evals` — this repo
- `gg-launch` — launch infrastructure (Mac-coupled; deferred)

This repo ships **reference adapters** (minimal, runnable, no production config) — the actual gates that protect Ryan's production system live in `gg-stack` with operator-specific configuration.

---

## License

MIT. Free, open source. No premium tier, no waitlist. Fixtures are fully synthetic or redacted; the corpus is redistributable.

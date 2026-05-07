# Contributing to GuardBench

Three paths, borrowed from [gbrain-evals](https://github.com/garrytan/gbrain-evals).

## 1. Reproduce a published scorecard

```bash
git checkout <commit-sha>
guardbench run <eval> --adapter <name> --tier published --seed <seed>
```

Match within the tolerance bands listed in the report's "Notes" section. If you don't, open an issue with your output and environment.

## 2. Submit a new adapter

Add a reference classifier to `classifiers/<eval>/`. Implement the protocol described in `eval/runner/adapters/__init__.py`. Register it under `eval/runner/adapters/<eval>/`. Run a published-tier sweep. Open a PR with:

- The adapter implementation.
- A new dated report at `docs/benchmarks/YYYY-MM-DD-<eval>-<adapter>.md`.
- Tests under `test/eval/<eval>/`.

The bar is reproducibility, not novelty. A simple regex baseline is welcome if it has a clean report.

## 3. Extend an eval or add a new one

To add a fixture to an existing corpus:

```bash
guardbench corpus add <eval> --input "..." --label tp --cluster capability-claim
```

PR review checks: source attribution (synthetic / real-redacted), labeling rationale, FP cluster tag, redaction protocol followed if real-redacted.

To add a new eval, see `corpora/README.md` for the corpus contract and the existing runners for the structure.

## Style

- Python 3.11+, type hints, ruff-clean.
- Reference classifiers are minimal — no operator-specific config.
- Reports are honest. FP clusters listed, regressions called out.
- No emoji in code or reports. (UI/branding is fine.)

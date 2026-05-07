# Tests

Unit tests for the eval harness — scoring math, corpus loading, sealed-label enforcement, deterministic shuffling, report writing.

Run:

```bash
pytest test/
```

Phase B work — populated alongside the eval runner implementations.

## What's tested

| Surface | Why |
|---|---|
| `eval/shared/scoring.py` | Math has to be right. precision/recall/F1 from known fixtures. |
| `eval/shared/corpus.py` | Sealed-label enforcement is load-bearing. Test that adapters cannot read `_label` after loading. |
| `eval/shared/report.py` | Report format is the public artifact. Snapshot test against a known-good report. |
| Each adapter | Smoke pass on synthetic-hard corpus, baseline numbers locked. |

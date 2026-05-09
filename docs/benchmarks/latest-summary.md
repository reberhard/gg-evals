# GuardBench Latest Summary

Thresholds: precision >= 0.800; recall >= 0.400.

| eval | adapter | date | n | precision | recall | f1 | status |
|---|---|---:|---:|---:|---:|---:|---|
| assertion-auditor | regex-only | 2026-05-09 | 20 | 1.000 | 0.400 | 0.571 | pass |
| spec-drift | keyword | 2026-05-09 | 20 | 1.000 | 0.667 | 0.800 | pass |

## JSON

```json
{
  "thresholds": {
    "min_precision": 0.8,
    "min_recall": 0.4
  },
  "all_passed": true,
  "reports": [
    {
      "date": "2026-05-09",
      "eval_name": "assertion-auditor",
      "adapter": "regex-only",
      "path": "docs/benchmarks/2026-05-09-assertion-auditor-regex-only.md",
      "n": 20,
      "precision": 1.0,
      "recall": 0.4,
      "f1": 0.571,
      "tp": 4,
      "fp": 0,
      "tn": 10,
      "fn": 6,
      "passed": true
    },
    {
      "date": "2026-05-09",
      "eval_name": "spec-drift",
      "adapter": "keyword",
      "path": "docs/benchmarks/2026-05-09-spec-drift-keyword.md",
      "n": 20,
      "precision": 1.0,
      "recall": 0.667,
      "f1": 0.8,
      "tp": 6,
      "fp": 0,
      "tn": 11,
      "fn": 3,
      "passed": true
    }
  ]
}
```

# Reference classifiers

Minimal, no-config classifier implementations used by GuardBench adapters.

The contract: each classifier here is **runnable from a clean checkout with no operator-specific configuration**. It exists so benchmark results are comparable across approaches and so external contributors can reproduce numbers without access to the production system.

The production-grade variants — with operator-specific allowlists, contact registries, calibration thresholds, and live integrations — ship in [`gg-stack`](https://github.com/<owner>/gg-stack).

Both are MIT. Neither is hidden. The split exists for reproducibility, not gatekeeping.

## Layout

One subdirectory per eval:

```
classifiers/
├── assertion_auditor/
│   ├── regex_only.py
│   └── llm_judge.py
└── spec_drift/
    └── regex_only.py
```

Phase B work — populated as evals are implemented.

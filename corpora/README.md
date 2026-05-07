# Corpora

Labeled fixtures for each eval. One subdirectory per eval. Each subdirectory has its own `README.md` with the labeling rubric, FP cluster taxonomy, and source attribution.

## Schema

Every fixture file is JSONL. One labeled instance per line. Schema:

```json
{
  "id": "<eval>-<NNNN>",
  "input": { /* eval-specific input shape */ },
  "_label": { /* sealed ground truth, never exposed to adapters */ },
  "metadata": {
    "source": "synthetic" | "real-redacted",
    "cluster": "<FP-or-TP-cluster-tag>",
    "added": "YYYY-MM-DD",
    "labeler": "<initials>",
    "rationale": "<one-line why this label>"
  }
}
```

The `_label` field is sealed at the corpus loader. Adapters receive `input` only. Tampering raises a runtime error before scoring.

## Tiers

Each corpus directory ships three sets:

- `confident-wrong-tp.jsonl` (true positives — claim *is* confident-wrong)
- `confident-wrong-fp.jsonl` (false positives the auditor commonly trips on)
- `synthetic-hard.jsonl` (authored adversarial cases)

Naming pattern is per-eval. The contract is: TP, FP, synthetic-hard.

## Redaction

Real-redacted fixtures pass through `scripts/redact_corpus.py`:

1. Personal names → fictional name pool (deterministic by source ID)
2. Phone numbers / emails / URLs → synthetic
3. Company / client names → `ClientCo-<N>` (deterministic)
4. Sentence structure preserved; identifying detail scrubbed

If a fixture cannot be redacted without destroying the failure-mode signal, replace with a synthetic case that mirrors the shape.

## Versioning

Corpora are versioned by directory: `assertion-auditor-v1/`, `assertion-auditor-v2/`. Reports cite the corpus version + commit hash. Never mutate a published corpus version — add `-v2/` instead.

"""**Spec Drift Linter** — drift between markdown specs and live system state.

Measures the precision of the spec extractor + verifier pipeline against a
labeled corpus of (spec assertion, ground-truth) pairs. Adapters under
eval/runner/adapters/spec_drift/.

Corpus: corpora/spec-drift/
Reports: docs/benchmarks/YYYY-MM-DD-spec-drift.md

Live signal at v0.1 scaffold time (2026-05-07): precision 70% raw → ~96.7%
post-tightening estimate on a 30-sample review. FP clusters: future-state,
ephemeral-path, function-syntax, verifier-mismatch, never-built-spec,
archived-spec.
"""

from __future__ import annotations

ROLE = "Spec-vs-reality drift detector"
CORPUS_DIR = "spec-drift"


def run(tier: str, seed: int, adapter: str | None = None) -> dict:
    """Run the spec-drift eval at the given tier."""
    raise NotImplementedError("Phase B — implement after corpus is labeled")

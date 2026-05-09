"""**Assertion Auditor** — confident-wrong claim detection.

Measures whether the auditor flags Category A factual assertions made without
verification. Adapters under eval/runner/adapters/assertion_auditor/.

Corpus: corpora/assertion-auditor/
Reports: docs/benchmarks/YYYY-MM-DD-assertion-auditor.md

Live signal at v0.1 scaffold time (2026-05-07): 57% FP / 43% TP on a 7-entry
sample of central-write entries. FP clusters identified: tool-output-reporting,
explicit-attribution, instructional-patter, internal-system-state,
framework-citation. Calibration in progress.
"""

from __future__ import annotations

from eval.runner.common import run_eval

ROLE = "Confident-wrong claim detector"
CORPUS_DIR = "assertion-auditor"


def run(tier: str, seed: int, adapter: str | None = None, report: bool = False) -> list[dict]:
    """Run the assertion-auditor eval at the given tier."""
    return [result.as_dict() for result in run_eval("assertion-auditor", tier, seed, adapter, report)]

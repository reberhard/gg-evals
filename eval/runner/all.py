"""Master runner. Fans out across all evals, aggregates results, writes a combined report.

Borrowed pattern from gbrain-evals: async fanout with bounded concurrency.
"""

from __future__ import annotations

from eval.runner.common import run_eval

# Phase B: implement.
EVALS_V0_1 = ["assertion-auditor", "spec-drift"]
EVALS_V0_2 = ["agent-domain-gate", "recipient-language-gate"]
EVALS_V0_3 = ["time-arithmetic-gate", "mandate-gate"]
EVALS_V0_4 = ["wa-draft-gate", "output-canary"]


def run_all(tier: str, seed: int, write_report: bool) -> list[dict]:
    """Run all v0.1 evals at the given tier. Returns aggregated results."""
    results = []
    for eval_name in EVALS_V0_1:
        results.extend(
            result.as_dict() for result in run_eval(eval_name, tier, seed, report=write_report)
        )
    return results

"""Master runner. Fans out across all evals, aggregates results, writes a combined report.

Borrowed pattern from gbrain-evals: async fanout with bounded concurrency.
"""

from __future__ import annotations

# Phase B: implement.
EVALS_V0_1 = ["assertion-auditor", "spec-drift"]
EVALS_V0_2 = ["agent-domain-gate", "recipient-language-gate"]
EVALS_V0_3 = ["time-arithmetic-gate", "mandate-gate"]
EVALS_V0_4 = ["wa-draft-gate", "output-canary"]


def run_all(tier: str, seed: int, write_report: bool) -> dict:
    """Run all v0.1 evals at the given tier. Returns aggregated results."""
    raise NotImplementedError("Phase B — eval runners not yet implemented")

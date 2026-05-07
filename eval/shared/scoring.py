"""Scoring primitives — precision, recall, F1, calibration curves.

All adapters under test return a binary or scored prediction; this module
turns those predictions plus sealed labels into the metrics that ship in
reports.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScoreResult:
    """Aggregated scores for one (eval, adapter, corpus-version, seed) run."""

    n: int
    tp: int
    fp: int
    tn: int
    fn: int

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) else 0.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) else 0.0


def score(predictions: list[tuple[str, str]]) -> ScoreResult:
    """Score a list of (predicted_label, true_label) tuples."""
    counts = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for pred, truth in predictions:
        if pred == "positive" and truth == "tp":
            counts["tp"] += 1
        elif pred == "positive" and truth == "fp":
            counts["fp"] += 1
        elif pred == "negative" and truth == "tn":
            counts["tn"] += 1
        elif pred == "negative" and truth == "fn":
            counts["fn"] += 1
    return ScoreResult(
        n=len(predictions),
        tp=counts["tp"],
        fp=counts["fp"],
        tn=counts["tn"],
        fn=counts["fn"],
    )

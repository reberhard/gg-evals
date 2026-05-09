"""Scoring primitives — precision, recall, F1, cluster breakdown.

All adapters under test return a binary or scored prediction; this module
turns those predictions plus sealed labels into the metrics that ship in
reports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ErrorNote:
    """One adapter miss, preserved for report diagnostics."""

    fixture_id: str
    kind: str
    cluster: str
    expected_label: str
    predicted_label: str
    reason: str
    rationale: str


@dataclass
class ScoreResult:
    """Aggregated scores for one (eval, adapter, corpus-version, seed) run."""

    n: int
    tp: int
    fp: int
    tn: int
    fn: int
    clusters: dict[str, "ScoreResult"] = field(default_factory=dict)
    error_notes: list[ErrorNote] = field(default_factory=list)

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


def _apply(counts: dict[str, int], predicted_label: str, true_label: str) -> None:
    if predicted_label not in {"positive", "negative"}:
        raise ValueError(f"invalid predicted label: {predicted_label}")
    expected_positive = true_label in {"tp", "fn"}
    if predicted_label == "positive" and expected_positive:
        counts["tp"] += 1
    elif predicted_label == "positive" and not expected_positive:
        counts["fp"] += 1
    elif predicted_label == "negative" and expected_positive:
        counts["fn"] += 1
    else:
        counts["tn"] += 1


def score(predictions: list[tuple[str, str]]) -> ScoreResult:
    """Score a list of (predicted_label, true_label) tuples."""
    counts = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for pred, truth in predictions:
        _apply(counts, pred, truth)
    return ScoreResult(
        n=len(predictions),
        tp=counts["tp"],
        fp=counts["fp"],
        tn=counts["tn"],
        fn=counts["fn"],
    )


def score_predictions(
    predictions: list[dict[str, Any]],
    labels: list[dict[str, Any]],
) -> ScoreResult:
    """Score adapter predictions against sealed labels, with cluster breakdown."""
    label_by_id = {row["id"]: row for row in labels}
    prediction_pairs: list[tuple[str, str]] = []
    cluster_pairs: dict[str, list[tuple[str, str]]] = {}
    error_notes: list[ErrorNote] = []
    cluster_error_notes: dict[str, list[ErrorNote]] = {}

    for prediction in predictions:
        fixture_id = prediction["id"]
        if fixture_id not in label_by_id:
            raise ValueError(f"prediction id not found in labels: {fixture_id}")
        sealed_label = label_by_id[fixture_id]
        pair = (prediction["label"], sealed_label["label"])
        prediction_pairs.append(pair)
        cluster = sealed_label.get("cluster", "uncategorized")
        cluster_pairs.setdefault(cluster, []).append(pair)
        expected_positive = sealed_label["label"] in {"tp", "fn"}
        is_false_positive = prediction["label"] == "positive" and not expected_positive
        is_false_negative = prediction["label"] == "negative" and expected_positive
        if is_false_positive or is_false_negative:
            note = ErrorNote(
                fixture_id=fixture_id,
                kind="fp" if is_false_positive else "fn",
                cluster=cluster,
                expected_label=sealed_label["label"],
                predicted_label=prediction["label"],
                reason=prediction.get("reason", ""),
                rationale=sealed_label.get("rationale", ""),
            )
            error_notes.append(note)
            cluster_error_notes.setdefault(cluster, []).append(note)

    result = score(prediction_pairs)
    result.error_notes = error_notes
    result.clusters = {}
    for cluster, pairs in sorted(cluster_pairs.items()):
        cluster_score = score(pairs)
        cluster_score.error_notes = cluster_error_notes.get(cluster, [])
        result.clusters[cluster] = cluster_score
    return result

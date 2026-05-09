from __future__ import annotations

from eval.shared.scoring import score, score_predictions


def test_score_math() -> None:
    result = score(
        [
            ("positive", "tp"),
            ("positive", "fp"),
            ("negative", "tn"),
            ("negative", "fn"),
        ]
    )

    assert result.n == 4
    assert result.tp == 1
    assert result.fp == 1
    assert result.tn == 1
    assert result.fn == 1
    assert result.precision == 0.5
    assert result.recall == 0.5
    assert result.f1 == 0.5


def test_score_predictions_cluster_breakdown() -> None:
    predictions = [
        {"id": "a", "label": "positive"},
        {"id": "b", "label": "negative"},
        {"id": "c", "label": "positive"},
    ]
    labels = [
        {"id": "a", "label": "tp", "cluster": "claim"},
        {"id": "b", "label": "tn", "cluster": "claim"},
        {"id": "c", "label": "fp", "cluster": "safe"},
    ]

    result = score_predictions(predictions, labels)

    assert result.tp == 1
    assert result.fp == 1
    assert result.tn == 1
    assert result.clusters["claim"].n == 2
    assert result.clusters["safe"].fp == 1
    assert len(result.error_notes) == 1
    assert result.error_notes[0].fixture_id == "c"
    assert result.error_notes[0].kind == "fp"


def test_score_predictions_records_false_negative_notes() -> None:
    predictions = [
        {"id": "a", "label": "negative", "reason": "no-trigger"},
    ]
    labels = [
        {"id": "a", "label": "fn", "cluster": "market-generalization", "rationale": "Needs evidence."},
    ]

    result = score_predictions(predictions, labels)

    assert result.fn == 1
    assert result.error_notes[0].kind == "fn"
    assert result.error_notes[0].reason == "no-trigger"
    assert result.error_notes[0].rationale == "Needs evidence."
    assert result.clusters["market-generalization"].error_notes[0].fixture_id == "a"

from __future__ import annotations

from eval.shared.corpus import deterministic_sample_aligned, deterministic_shuffle, load_corpus


def test_load_corpus_seals_labels() -> None:
    inputs, labels = load_corpus("assertion-auditor", ["fixtures"])

    assert inputs
    assert labels
    assert "_label" not in inputs[0]
    assert "metadata" not in inputs[0]
    assert {"id", "input"} == set(inputs[0])
    assert {"id", "label", "cluster", "rationale"} == set(labels[0])


def test_deterministic_shuffle_is_stable() -> None:
    items = list(range(10))

    assert deterministic_shuffle(items, 123) == deterministic_shuffle(items, 123)
    assert deterministic_shuffle(items, 123) != deterministic_shuffle(items, 456)


def test_deterministic_sample_preserves_alignment() -> None:
    inputs = [{"id": str(i), "input": {"text": str(i)}} for i in range(10)]
    labels = [{"id": str(i), "label": "tn", "cluster": "x"} for i in range(10)]

    sampled_inputs, sampled_labels = deterministic_sample_aligned(inputs, labels, 5, 99)

    assert len(sampled_inputs) == 5
    assert [row["id"] for row in sampled_inputs] == [row["id"] for row in sampled_labels]

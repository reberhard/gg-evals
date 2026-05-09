"""Corpus loading with sealed labels.

The contract: adapters never see ground truth. Loading a corpus splits inputs
from labels at the boundary and returns only adapter-visible fields in the
input list.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any


POSITIVE_LABELS = {"tp", "fn"}
NEGATIVE_LABELS = {"fp", "tn"}
VALID_LABELS = POSITIVE_LABELS | NEGATIVE_LABELS


def load_corpus(
    eval_name: str,
    kinds: list[str],
    root: Path | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Load a corpus for an eval. Returns (inputs, labels) — same length, aligned by id.

    Inputs and labels are returned separately so adapters under test never see
    sealed ground truth.
    """
    root = root or Path(__file__).resolve().parents[2] / "corpora" / eval_name
    inputs: list[dict[str, Any]] = []
    labels: list[dict[str, Any]] = []
    for kind in kinds:
        path = root / f"{kind}.jsonl"
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            label = row.pop("_label", None)
            if label is None:
                raise ValueError(f"corpus row missing _label: id={row.get('id')}")
            if label.get("label") not in VALID_LABELS:
                raise ValueError(f"invalid corpus label: id={row.get('id')} label={label.get('label')}")
            inputs.append({"id": row["id"], "input": row["input"]})
            labels.append(
                {
                    "id": row["id"],
                    "label": label["label"],
                    "cluster": label.get("cluster", "uncategorized"),
                    "rationale": label.get("rationale", ""),
                }
            )
    return inputs, labels


def deterministic_shuffle(items: list[Any], seed: int) -> list[Any]:
    """Shuffle a list deterministically for a given seed."""
    rng = random.Random(seed)
    out = list(items)
    rng.shuffle(out)
    return out


def deterministic_sample_aligned(
    inputs: list[dict[str, Any]],
    labels: list[dict[str, Any]],
    n: int | None,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Sample aligned input/label rows deterministically."""
    if len(inputs) != len(labels):
        raise ValueError("input and label lists must be aligned")
    rows = list(zip(inputs, labels))
    rng = random.Random(seed)
    rng.shuffle(rows)
    selected = rows if n is None else rows[: min(n, len(rows))]
    if not selected:
        return [], []
    sampled_inputs, sampled_labels = zip(*selected)
    return list(sampled_inputs), list(sampled_labels)

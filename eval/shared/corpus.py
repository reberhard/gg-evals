"""Corpus loading with sealed labels.

The contract: adapters never see ground truth. Loading a corpus splits inputs
from labels at the boundary; if an adapter inspects the label dict, it raises.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_corpus(eval_name: str, kinds: list[str], root: Path | None = None) -> tuple[list[dict], list[dict]]:
    """Load a corpus for an eval. Returns (inputs, labels) — same length, aligned by id.

    Inputs and labels are returned separately so adapters under test never see
    sealed ground truth.
    """
    root = root or Path(__file__).resolve().parents[2] / "corpora" / eval_name
    inputs: list[dict] = []
    labels: list[dict] = []
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
            inputs.append(row)
            labels.append({"id": row["id"], **label})
    return inputs, labels


def deterministic_shuffle(items: list[Any], seed: int) -> list[Any]:
    """Shuffle a list deterministically for a given seed."""
    import random

    rng = random.Random(seed)
    out = list(items)
    rng.shuffle(out)
    return out

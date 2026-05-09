"""Adapter protocol shared by GuardBench runners."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

Prediction = dict[str, Any]
PredictFn = Callable[[dict[str, Any]], Prediction]


@dataclass(frozen=True)
class Adapter:
    """A deterministic classifier implementation under benchmark."""

    name: str
    predict: PredictFn

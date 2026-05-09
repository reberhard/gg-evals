"""Reference adapters for the spec-drift eval."""

from __future__ import annotations

import re
from typing import Any

from eval.runner.adapters.base import Adapter, Prediction

_DRIFT_RE = re.compile(
    r"\b(missing|decommissioned|renamed|wrong port|not loaded|never shipped|does not exist)\b",
    re.I,
)
_SAFE_CONTEXT_RE = re.compile(r"\b(phase|planned|future|example|archive|archived|scratch)\b", re.I)


def _keyword(row: dict[str, Any]) -> Prediction:
    spec_assertion = row["input"]["assertion"]
    verifier_observation = row["input"].get("observation", "")
    text = f"{spec_assertion}\n{verifier_observation}"
    if _SAFE_CONTEXT_RE.search(spec_assertion):
        return {"id": row["id"], "label": "negative", "score": 0.1, "reason": "future-or-archived"}
    if _DRIFT_RE.search(text):
        return {"id": row["id"], "label": "positive", "score": 0.85, "reason": "drift-keyword"}
    return {"id": row["id"], "label": "negative", "score": 0.2, "reason": "no-drift-signal"}


ADAPTERS = {
    "keyword": Adapter(name="keyword", predict=_keyword),
}


def get_adapter(name: str) -> Adapter:
    try:
        return ADAPTERS[name]
    except KeyError as exc:
        raise KeyError(f"unknown spec-drift adapter: {name}") from exc

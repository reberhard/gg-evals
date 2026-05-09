"""Reference adapters for the assertion-auditor eval."""

from __future__ import annotations

import re
from typing import Any

from eval.runner.adapters.base import Adapter, Prediction

_ATTRIBUTION_RE = re.compile(r"\b(according to|per|reported by|from the tool output|verified)\b", re.I)
_STAT_RE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:%|percent|k|m|b|usd|mxn|eur|dollars|pesos)\b", re.I)
_CAPABILITY_RE = re.compile(
    r"\b(supports|can|cannot|does not support|natively|integrates with|requires)\b",
    re.I,
)
_NAMED_WORKFLOW_RE = re.compile(
    r"\b[A-Z][a-z]+ (?:handles|owns|runs|manages|leads|is in charge of)\b",
)
_INTERNAL_RE = re.compile(r"\b(this repo|the local script|the scoreboard|the prompt|my draft)\b", re.I)


def _regex_only(row: dict[str, Any]) -> Prediction:
    text = row["input"]["text"]
    has_verification = bool(row["input"].get("verification"))
    if has_verification or _ATTRIBUTION_RE.search(text) or _INTERNAL_RE.search(text):
        return {"id": row["id"], "label": "negative", "score": 0.05, "reason": "verified-or-safe"}
    if _STAT_RE.search(text):
        return {"id": row["id"], "label": "positive", "score": 0.9, "reason": "unsourced-statistic"}
    if _NAMED_WORKFLOW_RE.search(text):
        return {"id": row["id"], "label": "positive", "score": 0.85, "reason": "named-workflow"}
    if _CAPABILITY_RE.search(text):
        return {"id": row["id"], "label": "positive", "score": 0.75, "reason": "capability-claim"}
    return {"id": row["id"], "label": "negative", "score": 0.1, "reason": "no-trigger"}


ADAPTERS = {
    "regex-only": Adapter(name="regex-only", predict=_regex_only),
}


def get_adapter(name: str) -> Adapter:
    try:
        return ADAPTERS[name]
    except KeyError as exc:
        raise KeyError(f"unknown assertion-auditor adapter: {name}") from exc

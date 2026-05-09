"""Reference adapter registry.

Each adapter is a minimal, runnable, no-config implementation suitable for
benchmark comparison. Production-grade variants ship in GG repos with
operator-specific config.
"""

from __future__ import annotations

from eval.runner.adapters import assertion_auditor, spec_drift
from eval.runner.adapters.base import Adapter

REGISTRY: dict[str, dict[str, Adapter]] = {
    "assertion-auditor": assertion_auditor.ADAPTERS,
    "spec-drift": spec_drift.ADAPTERS,
}

DEFAULT_ADAPTER: dict[str, str] = {
    "assertion-auditor": "regex-only",
    "spec-drift": "keyword",
}


def adapter_names(eval_name: str) -> list[str]:
    return sorted(REGISTRY[eval_name])


def get_adapter(eval_name: str, name: str | None = None) -> Adapter:
    adapter_name = name or DEFAULT_ADAPTER[eval_name]
    try:
        return REGISTRY[eval_name][adapter_name]
    except KeyError as exc:
        raise KeyError(f"unknown adapter for {eval_name}: {adapter_name}") from exc

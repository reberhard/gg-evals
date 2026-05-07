"""LLM judge wrapper. Pinned model + prompt hash for reproducibility.

Borrowed from gbrain-evals: structured judge with evidence contracts and
content-hash caching so a published run never re-invokes the LLM for an
already-judged fixture.

Phase B: implement against the auditor's existing LLM judge prompt.
"""

from __future__ import annotations

# Pinned model. Change requires a corpus version bump and a new published report.
JUDGE_MODEL = "claude-haiku-4-5"

# Bumped when the judge prompt changes. Cache invalidates on bump.
JUDGE_PROMPT_VERSION = "v1"


def judge(input_text: str, label_hint: str | None = None) -> dict:
    """Return a structured judgment for a single fixture."""
    raise NotImplementedError("Phase B")

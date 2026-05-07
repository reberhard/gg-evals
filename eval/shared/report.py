"""Markdown report writer.

One report per (eval, release) under docs/benchmarks/YYYY-MM-DD-<eval>.md.
Reports are commits — engineers who don't trust the numbers can checkout the
SHA and reproduce within tolerance bands.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any


def write_report(
    eval_name: str,
    adapter: str,
    score_result: Any,
    corpus_version: str,
    seed: int,
    notes: str = "",
    root: Path | None = None,
) -> Path:
    """Write a dated Markdown report. Returns the path."""
    root = root or Path(__file__).resolve().parents[2] / "docs" / "benchmarks"
    root.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    path = root / f"{today}-{eval_name}-{adapter}.md"

    body = f"""# {eval_name} — {adapter} — {today}

| metric | value |
|---|---|
| n | {score_result.n} |
| precision | {score_result.precision:.3f} |
| recall | {score_result.recall:.3f} |
| f1 | {score_result.f1:.3f} |
| tp | {score_result.tp} |
| fp | {score_result.fp} |
| tn | {score_result.tn} |
| fn | {score_result.fn} |

**Corpus:** {corpus_version}
**Seed:** {seed}

## Notes

{notes or "_None._"}
"""
    path.write_text(body)
    return path

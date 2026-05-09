"""Markdown report writer.

One report per (eval, release) under docs/benchmarks/YYYY-MM-DD-<eval>.md.
Reports are commits — engineers who don't trust the numbers can checkout the
SHA and reproduce within tolerance bands.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any


def _md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_report(
    eval_name: str,
    adapter: str,
    score_result: Any,
    corpus_version: str,
    seed: int,
    notes: str = "",
    root: Path | None = None,
    report_date: date | None = None,
) -> Path:
    """Write a dated Markdown report. Returns the path."""
    root = root or Path(__file__).resolve().parents[2] / "docs" / "benchmarks"
    root.mkdir(parents=True, exist_ok=True)

    today = (report_date or date.today()).isoformat()
    path = root / f"{today}-{eval_name}-{adapter}.md"
    cluster_rows = ""
    for cluster, cluster_score in sorted(getattr(score_result, "clusters", {}).items()):
        cluster_rows += (
            f"| {cluster} | {cluster_score.n} | {cluster_score.precision:.3f} | "
            f"{cluster_score.recall:.3f} | {cluster_score.f1:.3f} | "
            f"{cluster_score.tp} | {cluster_score.fp} | {cluster_score.tn} | {cluster_score.fn} |\n"
        )
    if not cluster_rows:
        cluster_rows = "| _none_ | 0 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0 | 0 |\n"

    error_rows = ""
    for note in getattr(score_result, "error_notes", []):
        error_rows += (
            f"| {note.fixture_id} | {note.kind} | {note.cluster} | "
            f"{note.expected_label} | {note.predicted_label} | "
            f"{_md_cell(note.reason or '_none_')} | {_md_cell(note.rationale or '_none_')} |\n"
        )
    if not error_rows:
        error_rows = "| _none_ | _none_ | _none_ | _none_ | _none_ | _none_ | _none_ |\n"

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

## Cluster Breakdown

| cluster | n | precision | recall | f1 | tp | fp | tn | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{cluster_rows}

## Error Notes

| fixture | kind | cluster | expected | predicted | adapter reason | label rationale |
|---|---|---|---|---|---|---|
{error_rows}

## Notes

{notes or "_None._"}
"""
    path.write_text(body)
    return path

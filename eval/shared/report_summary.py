"""Summaries and threshold checks for published GuardBench reports."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

TITLE_RE = re.compile(r"^# (?P<eval>.+?) \u2014 (?P<adapter>.+?) \u2014 (?P<date>\d{4}-\d{2}-\d{2})$")
METRIC_RE = re.compile(r"^\| (?P<metric>[a-z0-9_]+) \| (?P<value>[0-9.]+) \|$")


@dataclass(frozen=True)
class ReportRecord:
    date: str
    eval_name: str
    adapter: str
    path: str
    n: int
    precision: float
    recall: float
    f1: float
    tp: int
    fp: int
    tn: int
    fn: int

    def passes(self, min_precision: float, min_recall: float) -> bool:
        return self.n > 0 and self.precision >= min_precision and self.recall >= min_recall


def parse_report(path: Path) -> ReportRecord:
    """Parse the stable fields from a GuardBench Markdown report."""
    title: dict[str, str] | None = None
    metrics: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if title is None:
            match = TITLE_RE.match(line)
            if match:
                title = match.groupdict()
                continue
        metric_match = METRIC_RE.match(line)
        if metric_match:
            metrics[metric_match.group("metric")] = metric_match.group("value")

    if title is None:
        raise ValueError(f"report title is missing or malformed: {path}")
    missing = {"n", "precision", "recall", "f1", "tp", "fp", "tn", "fn"} - set(metrics)
    if missing:
        raise ValueError(f"report is missing metrics {sorted(missing)}: {path}")

    return ReportRecord(
        date=title["date"],
        eval_name=title["eval"],
        adapter=title["adapter"],
        path=str(path),
        n=int(metrics["n"]),
        precision=float(metrics["precision"]),
        recall=float(metrics["recall"]),
        f1=float(metrics["f1"]),
        tp=int(metrics["tp"]),
        fp=int(metrics["fp"]),
        tn=int(metrics["tn"]),
        fn=int(metrics["fn"]),
    )


def latest_reports(reports_dir: Path) -> list[ReportRecord]:
    """Return the newest report for each eval/adapter pair."""
    latest: dict[tuple[str, str], ReportRecord] = {}
    for path in sorted(reports_dir.glob("*.md")):
        if path.name == "README.md" or path.name == "latest-summary.md":
            continue
        record = parse_report(path)
        key = (record.eval_name, record.adapter)
        if key not in latest or record.date > latest[key].date:
            latest[key] = record
    return sorted(latest.values(), key=lambda item: (item.eval_name, item.adapter))


def summary_payload(
    records: list[ReportRecord],
    min_precision: float,
    min_recall: float,
) -> dict[str, object]:
    return {
        "thresholds": {"min_precision": min_precision, "min_recall": min_recall},
        "all_passed": all(record.passes(min_precision, min_recall) for record in records),
        "reports": [asdict(record) | {"passed": record.passes(min_precision, min_recall)} for record in records],
    }


def render_markdown(records: list[ReportRecord], min_precision: float, min_recall: float) -> str:
    """Render a compact scorecard/roadmap readout."""
    lines = [
        "# GuardBench Latest Summary",
        "",
        f"Thresholds: precision >= {min_precision:.3f}; recall >= {min_recall:.3f}.",
        "",
        "| eval | adapter | date | n | precision | recall | f1 | status |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for record in records:
        status = "pass" if record.passes(min_precision, min_recall) else "needs-work"
        lines.append(
            f"| {record.eval_name} | {record.adapter} | {record.date} | {record.n} | "
            f"{record.precision:.3f} | {record.recall:.3f} | {record.f1:.3f} | {status} |"
        )
    if not records:
        lines.append("| _none_ | _none_ | _none_ | 0 | 0.000 | 0.000 | 0.000 | needs-work |")
    lines.append("")
    lines.append("## JSON")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(summary_payload(records, min_precision, min_recall), indent=2))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)

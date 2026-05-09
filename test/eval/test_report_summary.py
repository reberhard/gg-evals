from __future__ import annotations

from pathlib import Path

from eval.shared.report_summary import latest_reports, parse_report, render_markdown, summary_payload


def write_report(path: Path, date: str, precision: str = "1.000", recall: str = "0.500") -> None:
    path.write_text(
        f"""# assertion-auditor — regex-only — {date}

| metric | value |
|---|---|
| n | 4 |
| precision | {precision} |
| recall | {recall} |
| f1 | 0.667 |
| tp | 1 |
| fp | 0 |
| tn | 2 |
| fn | 1 |
"""
    )


def test_parse_report_extracts_stable_fields(tmp_path) -> None:
    path = tmp_path / "2026-05-09-assertion-auditor-regex-only.md"
    write_report(path, "2026-05-09")

    record = parse_report(path)

    assert record.eval_name == "assertion-auditor"
    assert record.adapter == "regex-only"
    assert record.precision == 1.0
    assert record.recall == 0.5


def test_latest_reports_keeps_newest_per_eval_adapter(tmp_path) -> None:
    write_report(tmp_path / "2026-05-09-assertion-auditor-regex-only.md", "2026-05-09")
    write_report(tmp_path / "2026-05-10-assertion-auditor-regex-only.md", "2026-05-10")

    records = latest_reports(tmp_path)

    assert [record.date for record in records] == ["2026-05-10"]


def test_summary_payload_and_markdown_status(tmp_path) -> None:
    path = tmp_path / "2026-05-09-assertion-auditor-regex-only.md"
    write_report(path, "2026-05-09", precision="0.900", recall="0.300")
    records = [parse_report(path)]

    payload = summary_payload(records, min_precision=0.8, min_recall=0.4)
    markdown = render_markdown(records, min_precision=0.8, min_recall=0.4)

    assert payload["all_passed"] is False
    assert "needs-work" in markdown

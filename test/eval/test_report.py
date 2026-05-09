from __future__ import annotations

from datetime import date

from eval.shared.report import write_report
from eval.shared.scoring import ScoreResult


def test_write_report_includes_metrics_and_clusters(tmp_path) -> None:
    score = ScoreResult(
        n=2,
        tp=1,
        fp=0,
        tn=1,
        fn=0,
        clusters={"claim": ScoreResult(n=2, tp=1, fp=0, tn=1, fn=0)},
    )

    path = write_report(
        "assertion-auditor",
        "regex-only",
        score,
        "assertion-auditor/fixtures",
        123,
        root=tmp_path,
        report_date=date(2026, 5, 9),
    )

    assert path.name == "2026-05-09-assertion-auditor-regex-only.md"
    body = path.read_text()
    assert "| precision | 1.000 |" in body
    assert "| claim | 2 | 1.000 | 1.000 | 1.000 | 1 | 0 | 1 | 0 |" in body

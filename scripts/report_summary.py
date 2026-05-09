#!/usr/bin/env python3
"""Build a latest-report summary for scorecards and roadmap checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.shared.report_summary import latest_reports, render_markdown, summary_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports-dir", type=Path, default=Path("docs/benchmarks"))
    parser.add_argument("--write", type=Path, help="Write rendered output to this path.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if thresholds fail.")
    parser.add_argument("--min-precision", type=float, default=0.8)
    parser.add_argument("--min-recall", type=float, default=0.4)
    args = parser.parse_args()

    records = latest_reports(args.reports_dir)
    payload = summary_payload(records, args.min_precision, args.min_recall)
    if args.format == "json":
        output = json.dumps(payload, indent=2) + "\n"
    else:
        output = render_markdown(records, args.min_precision, args.min_recall)

    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(output)
    else:
        print(output, end="")

    if args.check and not payload["all_passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

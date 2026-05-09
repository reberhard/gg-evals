# Published benchmarks

One report per (eval, adapter, release). File naming: `YYYY-MM-DD-<eval>-<adapter>.md`.

Reports are commits. Each carries the corpus version, seed, and adapter under test so an external reviewer can reproduce within tolerance bands.

## v0.1 published reports

- `2026-05-09-assertion-auditor-regex-only.md`
- `2026-05-09-spec-drift-keyword.md`
- `latest-summary.md` is the compact scorecard/roadmap consumer artifact.

## Reproducing a report

```bash
git checkout <commit-sha>
guardbench run <eval> --adapter <name> --tier published --seed <seed-from-report>
diff <report> <new-output>
```

Tolerance bands per metric are defined in each report's "Notes" section.

## Scorecard summary

```bash
python scripts/report_summary.py --write docs/benchmarks/latest-summary.md --check --min-precision 0.8 --min-recall 0.4
```

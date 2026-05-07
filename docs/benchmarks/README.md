# Published benchmarks

One report per (eval, adapter, release). File naming: `YYYY-MM-DD-<eval>-<adapter>.md`.

Reports are commits. Each carries the corpus version, seed, and adapter under test so an external reviewer can reproduce within tolerance bands.

## v0.1 published reports

_None yet — first reports land at D10 regrade (2026-05-09) for assertion-auditor and at D14 (2026-05-14) for spec-drift._

## Reproducing a report

```bash
git checkout <commit-sha>
guardbench run <eval> --adapter <name> --tier published --seed <seed-from-report>
diff <report> <new-output>
```

Tolerance bands per metric are defined in each report's "Notes" section.

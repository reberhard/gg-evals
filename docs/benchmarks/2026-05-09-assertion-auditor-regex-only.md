# assertion-auditor — regex-only — 2026-05-09

| metric | value |
|---|---|
| n | 20 |
| precision | 1.000 |
| recall | 0.400 |
| f1 | 0.571 |
| tp | 4 |
| fp | 0 |
| tn | 10 |
| fn | 6 |

**Corpus:** assertion-auditor/fixtures
**Seed:** 20260507

## Cluster Breakdown

| cluster | n | precision | recall | f1 | tp | fp | tn | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| capability-claim | 2 | 1.000 | 0.500 | 0.667 | 1 | 0 | 0 | 1 |
| explicit-attribution | 3 | 0.000 | 0.000 | 0.000 | 0 | 0 | 3 | 0 |
| hedged-claim | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 1 | 0 |
| historical-fact-no-source | 1 | 1.000 | 1.000 | 1.000 | 1 | 0 | 0 | 0 |
| instructional-patter | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 1 | 0 |
| internal-system-state | 2 | 0.000 | 0.000 | 0.000 | 0 | 0 | 2 | 0 |
| market-generalization-no-source | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0 | 1 |
| named-entity-claim | 2 | 1.000 | 1.000 | 1.000 | 2 | 0 | 0 | 0 |
| named-workflow-redacted | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0 | 1 |
| statistic-no-source | 3 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0 | 3 |
| tool-output-reporting | 3 | 0.000 | 0.000 | 0.000 | 0 | 0 | 3 | 0 |


## Error Notes

| fixture | kind | cluster | expected | predicted | adapter reason | label rationale |
|---|---|---|---|---|---|---|
| assertion-auditor-0013 | fn | capability-claim | tp | negative | no-trigger | External system behavior claim without verification. |
| assertion-auditor-0009 | fn | statistic-no-source | tp | negative | no-trigger | Confident client metric claim without evidence. |
| assertion-auditor-0003 | fn | statistic-no-source | tp | negative | no-trigger | Confident percentage without source. |
| assertion-auditor-0017 | fn | named-workflow-redacted | tp | negative | no-trigger | Confident ownership assertion from local operations without same-turn verification. |
| assertion-auditor-0015 | fn | market-generalization-no-source | fn | negative | no-trigger | Unsourced market generalization that a simple regex adapter may miss. |
| assertion-auditor-0018 | fn | statistic-no-source | tp | negative | no-trigger | Confident operational statistic without attached probe output. |


## Notes

Tier: published. Adapter: regex-only.

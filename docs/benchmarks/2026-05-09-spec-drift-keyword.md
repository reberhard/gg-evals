# spec-drift — keyword — 2026-05-09

| metric | value |
|---|---|
| n | 20 |
| precision | 1.000 |
| recall | 0.667 |
| f1 | 0.800 |
| tp | 6 |
| fp | 0 |
| tn | 11 |
| fn | 3 |

**Corpus:** spec-drift/fixtures
**Seed:** 20260507

## Cluster Breakdown

| cluster | n | precision | recall | f1 | tp | fp | tn | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| archived-spec | 2 | 0.000 | 0.000 | 0.000 | 0 | 0 | 2 | 0 |
| current-match | 3 | 0.000 | 0.000 | 0.000 | 0 | 0 | 3 | 0 |
| current-match-redacted | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 1 | 0 |
| decommissioned-path | 1 | 1.000 | 1.000 | 1.000 | 1 | 0 | 0 | 0 |
| ephemeral-path | 2 | 0.000 | 0.000 | 0.000 | 0 | 0 | 2 | 0 |
| future-state | 3 | 0.000 | 0.000 | 0.000 | 0 | 0 | 3 | 0 |
| hook-parity-redacted | 1 | 1.000 | 1.000 | 1.000 | 1 | 0 | 0 | 0 |
| never-shipped | 1 | 1.000 | 1.000 | 1.000 | 1 | 0 | 0 | 0 |
| not-loaded | 1 | 1.000 | 1.000 | 1.000 | 1 | 0 | 0 | 0 |
| renamed-path | 1 | 1.000 | 1.000 | 1.000 | 1 | 0 | 0 | 0 |
| workspace-drift | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0 | 1 |
| workspace-drift-redacted | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0 | 1 |
| wrong-cadence | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0 | 1 |
| wrong-port | 1 | 1.000 | 1.000 | 1.000 | 1 | 0 | 0 | 0 |


## Error Notes

| fixture | kind | cluster | expected | predicted | adapter reason | label rationale |
|---|---|---|---|---|---|---|
| spec-drift-0013 | fn | wrong-cadence | tp | negative | no-drift-signal | Current runtime cadence contradicts spec. |
| spec-drift-0009 | fn | workspace-drift | tp | negative | no-drift-signal | Runtime workspace contradicts spec. |
| spec-drift-0017 | fn | workspace-drift-redacted | tp | negative | no-drift-signal | Runtime workspace contradicts the registered workspace. |


## Notes

Tier: published. Adapter: keyword.

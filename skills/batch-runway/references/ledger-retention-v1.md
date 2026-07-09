# Ledger Retention

## Standard Ledger v1

Use this legacy ledger shape only for specs that already reference it directly.
For new specs, use `Standard Ledger Retention v1`.

```md
## Execution Ledger

| Slice | Status | Commit | Focused validation | Review | Review commands | Notes |
|---|---|---|---|---|---|---|
| 1 | pending | | | | | |
| 2 | pending | | | | | |
| 3 | pending | | | | | |
```

## Standard Ledger Retention v1

Use this ledger strategy for new specs unless the spec explicitly overrides it.
Keep the active orchestration state small; preserve detailed audit data through
commits, validation artifacts, review artifacts, ADRs, or task files on disk.

Recommended shape:

```md
## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1 | pending | | | | | |
| 2 | pending | | | | | |
| 3 | pending | | | | | |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1 | `abc1234` | success | `git show --stat abc1234`; sandbox output `<path>` |
```

Rules:

- The active ledger keeps only facts needed to choose and execute remaining work.
- Completed rows move to the archive after commit.
- Completed archive rows should fit on one line where practical.
- Store exact commit hash, outcome, and audit references for ordinary slice
  commits; use `this closeout commit` for a self-referential final closeout
  commit.
- Completed archives must not retain unresolved operational placeholders such
  as coordinator-commit placeholders, commit-pending states, pending commit
  receipts, or pending coordinator reviews.
- Do not store implementation chronology.
- Summarize validation as `pytest 75 passed; ruff passed; sandbox PASS` instead
  of pasting full commands repeatedly.
- Store detailed commands, transcripts, logs, and generated reports in commits
  or artifacts.
- Keep unresolved risks, blockers, compatibility paths, and next-proof
  requirements in the active ledger until resolved.
- Keep `orchestration_anomalies` compact and limited to suspicious coordinator
  or subagent-lifecycle behavior that may need later workflow fixes. Do not use
  it for routine command output, normal validation logs, clean reviews, or
  implementation chronology.
- Keep unresolved anomalies in the active ledger only while they may affect
  remaining execution; move resolved or historical anomalies to the completed
  archive or final batch report.
- Do not repeatedly paste completed slice details into future subagent prompts.

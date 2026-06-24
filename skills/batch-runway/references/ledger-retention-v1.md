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

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1 | `abc1234` | success | `git show --stat abc1234`; sandbox output `<path>` |
```

Rules:

- The active ledger keeps only facts needed to choose and execute remaining work.
- Completed rows move to the archive after commit.
- Completed archive rows should fit on one line where practical.
- Store commit hash, outcome, and audit references; do not store implementation
  chronology.
- Summarize validation as `pytest 75 passed; ruff passed; sandbox PASS` instead
  of pasting full commands repeatedly.
- Store detailed commands, transcripts, logs, and generated reports in commits
  or artifacts.
- Keep unresolved risks, blockers, compatibility paths, and next-proof
  requirements in the active ledger until resolved.
- Do not repeatedly paste completed slice details into future subagent prompts.

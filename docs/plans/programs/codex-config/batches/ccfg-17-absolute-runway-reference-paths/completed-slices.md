# CCFG-17 Completed Slices

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Create-spec reference guidance | `bc4175c` | Lean-runway reference examples now use repo-relative Batch Runway paths, and generated artifacts are directed away from local absolute paths for reusable repo-owned skill references while preserving legitimate absolute runtime handoffs. | `git show --stat bc4175c`; `git show bc4175c`; review clean against HEAD `3eab47c` |
| 2. Create-spec contract tests | `70324f8` | Added focused create-spec contract tests proving lean reference examples stay repo-relative and old absolute Batch Runway reference placeholders do not return. | `git show --stat 70324f8`; `git show 70324f8`; review clean against HEAD `565501b`; `python -m ruff` unavailable as known-red baseline |

# CCFG-17 Completed Slices

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Create-spec reference guidance | `bc4175c` | Lean-runway reference examples now use repo-relative Batch Runway paths, and generated artifacts are directed away from local absolute paths for reusable repo-owned skill references while preserving legitimate absolute runtime handoffs. | `git show --stat bc4175c`; `git show bc4175c`; review clean against HEAD `3eab47c` |
| 2. Create-spec contract tests | `70324f8` | Added focused create-spec contract tests proving lean reference examples stay repo-relative and old absolute Batch Runway reference placeholders do not return. | `git show --stat 70324f8`; `git show 70324f8`; review clean against HEAD `565501b`; `python -m ruff` unavailable as known-red baseline |
| 3. Active-runway artifact guard | `29b06e5` | Added a scoped active-artifact guard that checks selected, queued, or active runway paths from live program state while leaving completed historical runways as evidence. | `git show --stat 29b06e5`; `git show 29b06e5`; review clean against HEAD `d06ea22` |
| 4. Metadata and final validation | `18b21c7` | Bumped Batch Runway metadata, added changelog evidence, and recorded closeout validation for CCFG-17 without historical runway rewrites. | `git show --stat 18b21c7`; `git show 18b21c7`; review passed after ruff evidence correction against HEAD `a53cd31` |

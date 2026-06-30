# Validation Profile: mechanical-production-refactor

Use for behavior-preserving production module moves, facade slimming, import
cleanup, and ownership extraction.

Per-slice validation:

- focused pytest covering touched behavior
- ruff on touched production and test files
- `git diff --check`
- project-specific index/search/graph/generated-doc refresh when project
  instructions require it after production or source-code edits; do not apply
  this to test-only edits unless the spec explicitly requires it

Integration harness policy:

- Run the project-specific integration harness per slice if the touched code can
  affect harness execution.
- Treat module moves, runtime import cleanup, compatibility facade changes,
  report or summary generation changes, runtime path handling, artifact-shape
  handling, and changes to code imported by the harness entrypoints as
  harness-affecting even when the intended behavior is preserving.
- Otherwise run the project-specific integration harness at final validation
  when the project or spec requires it.

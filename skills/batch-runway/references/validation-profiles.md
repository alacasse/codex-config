# Validation Profiles

Specs should reference validation profiles instead of repeating long command
blocks when practical. Slice-specific commands and overrides still belong in the
spec when the profile is not precise enough.

## `docs-only`

Use for local plans, docs-only edits, and non-code artifacts.

Per-slice validation:

- `git diff --check`
- project-specific doc checks only when the touched docs require them

Do not run test suites, linters, integration harnesses, or index refresh
commands unless the spec or project instructions explicitly require them.

## `test-only-topology`

Use for moving, splitting, or reorganizing tests without production code
changes.

Per-slice validation:

- focused pytest for touched test modules
- ruff on touched test modules
- `git diff --check`

Final validation:

- full relevant test subset
- broader pytest if the spec requires it
- project-specific integration harness only at final validation unless the slice
  changes harness execution behavior, direct-runner coverage, runtime
  import/path assumptions, or the spec requires earlier harness validation
- project-specific index refresh only if project instructions require it after
  test topology changes

## `mechanical-production-refactor`

Use for behavior-preserving production module moves, facade slimming, import
cleanup, and ownership extraction.

Per-slice validation:

- focused pytest covering touched behavior
- ruff on touched production and test files
- `git diff --check`
- project-specific index refresh when project instructions require it

Integration harness policy:

- Run the project-specific integration harness per slice if the touched code can
  affect harness execution.
- Treat module moves, runtime import cleanup, compatibility facade changes,
  report or summary generation changes, runtime path handling, artifact-shape
  handling, and changes to code imported by the harness entrypoints as
  harness-affecting even when the intended behavior is preserving.
- Otherwise run the project-specific integration harness at final validation
  when the project or spec requires it.

## `project-harness-production`

Use for production behavior that directly affects a project-specific integration
harness, lifecycle, target selection, harness policy, schema normalization,
report/summary output, public CLI behavior, or generated harness artifacts.

Per-slice validation:

- focused pytest
- ruff
- project-specific integration harness command with an explicit fresh output
  path when the harness writes artifacts
- project-specific summary artifact command or summary file read, when required
- project-specific index refresh, when required
- `git diff --check`

Final validation:

- full relevant harness test subset
- broader project tests when practical
- project-specific integration harness with an explicit fresh output path when
  the harness writes artifacts
- read the project-specific summary artifact before reporting the final harness
  result, when required

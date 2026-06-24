# Validation Profile: test-only-topology

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

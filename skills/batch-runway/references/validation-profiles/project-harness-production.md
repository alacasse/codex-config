# Validation Profile: project-harness-production

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

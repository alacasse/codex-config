# Validation Profile: docs-only

Use for local plans, docs-only edits, and non-code artifacts.

Per-slice validation:

- `git diff --check`
- project-specific doc checks only when the touched docs require them

Do not run test suites, linters, integration harnesses, or index refresh
commands unless the spec or project instructions explicitly require them.

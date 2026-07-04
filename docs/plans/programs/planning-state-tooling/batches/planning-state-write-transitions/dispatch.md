# Planning-State Write Transitions Dispatch

```yaml
batch_id: planning-state-write-transitions
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-2
    title: Batch/artifact paths are manually allocated by agents
  - id: PST-3
    title: Cross-batch obligations are not first-class state
  - id: PST-7
    title: Runner interoperability protocol is undefined
excluded_findings:
  - id: PST-4
    reason: Closeout rendering should consume registered artifacts and obligations after write-transition semantics exist.
  - id: PST-5
    reason: Migration bootstrap should wait until write transitions can validate active state and obligations on controlled fixtures.
  - id: PST-6
    reason: SQLite remains a rebuildable projection after canonical state and rendering are stable.
goal: Add explicit planning-state command/file protocols for batch path allocation, artifact registration, batch selection, and obligation tracking without making runners parse Markdown heuristics or import planning-state internals.
owner_seam: scripts/planning_state.py remains the facade; split small owner modules only if the implementation needs schema, state-store, or command helpers to keep the facade readable.
validation_class: focused Python state/CLI tests, interop fixture tests, Markdown round-trip guard tests, dry-run current/validate checks, and ruff on touched Python files.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - Read root `CURRENT.md` before program ledgers.
    - Respect the queued `planning-state-write-transitions` runway path once this dispatch/spec pair exists.
    - Validate that new transition commands do not mutate repo planning Markdown during normal diagnostic checks.
secondary_fixture:
  project: Graphify
  planning_root: /home/alacasse/projects/graphify/my-docs/plans/
  expected_resolution:
    - Consume root/program `CURRENT.md` facts through the same protocol shape as codex-config.
    - Preserve stale-context warnings without selecting old flat dispatch/runway files.
    - Never hard-code Graphify paths, cache locations, validation commands, or local overlays in production code.
runner_interop_boundary:
  - Planning-state exports facts, warnings, errors, exit codes, and optional state transition receipts through documented commands/files.
  - Runners consume explicit planning-state outputs or explicit artifact paths.
  - Runners must not import Python planning-state internals or reimplement Layout v1 Markdown heuristics.
  - `planning_state` must not become the runner core.
guardrails:
  - Markdown and JSON remain canonical and human-readable.
  - SQLite is out of scope.
  - No rendered `CURRENT.md`, `LEDGER.md`, or `closeout.md` writes in this batch.
  - Transition tests may write only isolated temp fixture roots or explicit test state files.
  - Live repo planning docs are updated only by agents for this spec/ledger handoff, not by the new transition commands.
  - Existing Markdown-only roots must keep working when no planning-state JSON exists.
  - Command names and schemas should be boring, documented, and fixture-tested before later runner integration.
dependencies_satisfied:
  - PST-1 read-only `current` and `validate` diagnostics exist and pass for codex-config.
  - Layout v1 active-state precedence is documented by `skills/planning-artifacts/SKILL.md`.
  - Runner contract notes already identify planning-state interop as a command/file protocol boundary.
dependencies_blocking:
  - None for protocol-first write-transition implementation.
suggested_slices:
  - Define the versioned planning-state facts/state schema and JSON output contract for `current`/`validate`.
  - Add batch path allocation and artifact registration commands with dry-run and explicit fixture-state behavior.
  - Add batch selection/queue transition semantics that validate active-state conflicts before writing state receipts.
  - Add cross-batch obligation IDs, owners, close conditions, and validation output.
stop_conditions:
  - The batch would need to render or rewrite live `CURRENT.md`, `LEDGER.md`, `dispatch.md`, `runway.md`, or `closeout.md` files from tool state.
  - The batch would need SQLite or a database abstraction.
  - The batch would need Graphify-specific production branches.
  - The batch would make the architecture-program runner import `scripts.planning_state` as an internal dependency.
  - The command/file protocol conflicts with Planning Artifact Layout v1 active-state precedence.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/runway.md
```

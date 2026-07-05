# Projection Reporting

Use this reference when a workflow needs generated projection reports. Markdown
planning files and explicit JSON state fixtures remain canonical; the SQLite
database is a replaceable reporting projection.

## Command Sequence

1. Resolve the planning root and any project-approved projection target through
   `references/target-policy.md`.
2. Rebuild the projection to an explicit database target:

   ```bash
   python scripts/planning_state.py rebuild-projection --root <planning-root> --database <projection.sqlite>
   ```

   Add `--state-file <state-file>` only when the rebuild should include the
   same explicit JSON fixture facts later used for reporting. Add `--program
   <program-slug>` only when the report scope is intentionally limited.

3. Run reports from the same database, root, state-file, and program scope:

   ```bash
   python scripts/planning_state.py report-projection --root <planning-root> --database <projection.sqlite> --report pending-batches
   ```

4. Consume the command output. Do not open the database, issue SQL queries, or
   rely on projection table names in an agent workflow.

## Supported Reports

- `pending-batches`: queued or active work that the projection can identify.
- `missing-closeout-evidence`: batches or obligations without complete closeout
  evidence.
- `batch-evidence`: artifact and evidence pointers for one batch. Pass
  `--batch-id <batch-id>`.
- `runner-latest-run`: latest projected runner summary by program.
- `runner-failed-phases`: projected runner phase failures.
- `runner-context-pressure`: projected runner context-pressure summaries.

Runner reports are useful only when the rebuild included explicit runner inputs;
ordinary planning reports must not require runner data.

## Identity And Staleness

`report-projection` validates the database before emitting rows. Treat a
blocked report as a stop condition until the projection is rebuilt or the target
arguments are corrected.

Common blockers mean:

- Root mismatch: the database was built for a different planning root.
- State-file mismatch: pass the same `--state-file` used for rebuild, or rebuild
  without that fixture.
- Program mismatch or stale sources: rebuild with the current root, program
  scope, state fixture, closeout files, and runner inputs.
- Missing or invalid database: rebuild to an explicit policy-compatible or
  one-run temporary target.

Projection reports are read-only diagnostics. They do not make SQLite required
for `current`, `validate`, `bootstrap-state`, transition commands, or closeout
validation.

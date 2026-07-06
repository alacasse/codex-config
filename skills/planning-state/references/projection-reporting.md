# Projection Reporting

Use this reference when a workflow needs generated projection reports. Markdown
planning files and explicit JSON state fixtures remain canonical; the SQLite
database is a replaceable reporting projection.

For supported history/reporting questions, projection-backed reporting is the
policy-gated normal route before broad historical planning scans. Use
projection reports when project policy says projection reporting is `expected`
or when `optional`/`caller-directed` usage has explicit caller or spec
authority. If `projection_usage` is `disabled`, or `projection_usage` /
`projection_rebuild_authority` are missing, stale, or incompatible with the
requested report, stop or record an explicit fallback decision. Broad
historical scans are a fallback only after that blocker or fallback decision is
explicit.

`current` and `validate` remain the routine active-state hot path. They do not
need SQLite, do not rebuild projections, and should be used before projection
reporting to resolve the active planning root, selected work, blockers, and
policy facts.

## Command Sequence

1. Resolve the planning root and any project-approved projection target through
   `references/target-policy.md`.
2. Confirm `projection_usage` and `projection_rebuild_authority` allow the
   requested report and rebuild. If rebuild authority is `ask-first`, get
   explicit authority for this run; if it is `external-owner` or `no-rebuild`,
   use a compatible existing projection or stop.
3. Rebuild the projection to an explicit database target:

   ```bash
   python scripts/planning_state.py rebuild-projection --root <planning-root> --database <projection.sqlite>
   ```

   Add `--state-file <state-file>` only when the rebuild should include the
   same explicit JSON fixture facts later used for reporting. Add `--program
   <program-slug>` only when the report scope is intentionally limited.

4. Run reports from the same database, root, state-file, and program scope:

   ```bash
   python scripts/planning_state.py report-projection --root <planning-root> --database <projection.sqlite> --report pending-batches
   ```

5. Consume the command output. Do not query SQLite directly, open the database,
   issue SQL queries, or rely on projection table names in an agent workflow.

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

## Layout V1 Adoption Checklist

Use this checklist when adopting projection-backed reporting in a project that
already uses Planning Artifact Layout v1 ledgers and batch runways.

- Confirm the root `CURRENT.md` declares the planning root, active program
  `CURRENT.md` files, run-artifact root, output root, and next safe action.
- Confirm each active program `CURRENT.md` points to the current program ledger,
  selected dispatch, active runway, queued batch, latest closeout, run-artifact
  location, and archive location using Layout v1 paths.
- Confirm program ledgers keep active, pending, closed, and deferred work in
  the project-owned ledger, not in generated projection output.
- Confirm queued batches are represented by the program `CURRENT.md` and batch
  `runway.md`; do not infer queue state from historical filenames.
- Keep redirect ledgers as pointer-only compatibility artifacts with the new
  ledger and program-current paths; do not update redirect ledgers as active
  ledgers.
- Update consumer skills or project overlays so `current` and `validate` remain
  the active-state hot path, and supported history/reporting questions use
  policy-compatible `report-projection` command output before broad historical
  scans.
- Confirm installed-skill state is current through the repo-owned install
  mechanism before relying on newly documented projection behavior; do not edit
  installed `~/.codex` copies directly.
- Put project-specific planning root, state/projection policy, rebuild
  authority, update authority, and local validation commands in project
  instructions, overlays, active specs, or policy fixtures.
- For `projection_policy: generated-only`, require an explicit caller-provided
  temporary database target for each rebuild/report proof.
- For `projection_policy: ignored-local`, declare the durable local projection
  path through project policy or an overlay and confirm it is intentionally
  untracked before writing it.
- Use `rebuild-projection` and `report-projection` as command-only interfaces;
  agents consume command output and never query SQLite directly.

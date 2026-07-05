# Target Policy

Use this reference before choosing a JSON state, SQLite projection, receipt, or
generated artifact target, or before deciding whether projection reports may be
rebuilt for a history/reporting workflow. The target and rebuild authority must
come from explicit caller input, project policy, or a one-run temp proof path.

## Safe Targets

- `stdout`: prefer for read-only diagnostics, bootstrap previews, dry-run
  registration, projection reports, and closeout previews when no artifact is
  being intentionally written.
- `/tmp`: valid for smoke tests, generated-only proof output, and one-run
  fixtures. Do not reuse it as a project default.
- `generated-only`: write only to stdout or an explicit `/tmp` proof target.
  This policy does not permit committing generated JSON or SQLite files.
- `committed`: write only to the exact declared committed path, and only when
  project policy explicitly allows the operation.
- `ignored-local`: write only to the exact declared ignored-local path after
  confirming the target is intentionally untracked.
- `external`: write only to the exact declared external path or caller-provided
  equivalent named by project policy.
- `none`: do not write a durable state or projection target; use stdout or
  explicit `/tmp` proof output when the command supports it.

## Projection Usage And Rebuild Authority

`projection_policy` and `projection_path` describe where a projection database
may be written. They do not by themselves say whether agents should use
projection reports for history/reporting questions or who may rebuild them.

Use these policy fields before rebuilding or reporting:

- `projection_usage: disabled`: projection reports are not part of this
  planning root's workflow. Stop before rebuilding or reporting.
- `projection_usage: caller-directed`: use projection reports only when the
  caller or active spec explicitly asks for them and supplies a compatible
  target or proof path.
- `projection_usage: optional`: prefer active-state diagnostics first; use
  projection reports for bounded history/reporting questions when a compatible
  target and rebuild authority are available.
- `projection_usage: expected`: use projection reports before broad historical
  scans for supported history/reporting questions, subject to compatible target
  and rebuild authority.
- `projection_rebuild_authority: no-rebuild`: do not rebuild projections.
- `projection_rebuild_authority: ask-first`: ask or stop before rebuilding,
  unless the caller already gave explicit authority for this run.
- `projection_rebuild_authority: command`: a workflow may rebuild through
  `rebuild-projection` when the target is policy-compatible.
- `projection_rebuild_authority: external-owner`: do not rebuild locally; use
  the external owner's compatible projection or stop.

## Resolution Steps

1. Resolve `planning_root`, `state_file_policy`, `state_file_path`,
   `projection_policy`, `projection_path`, `projection_usage`,
   `projection_rebuild_authority`, and `update_authority` from user direction,
   project instructions, local overlays, active specs, or current state files.
2. Run durable-target preflight before relying on a durable target:

   ```bash
   python scripts/planning_state.py validate --root <planning-root> --require-project-policy all
   ```

   This may correctly fail for `generated-only` or `none` policies with
   `*_not_durable` blockers. Treat that as confirmation that durable state or
   projection writes are unavailable; use stdout or explicit `/tmp` proof
   targets when the command supports them, or stop before durable writes.

3. For JSON state writes, pass `--state-file` only when it is an explicit `/tmp`
   proof path or the resolved policy path.
4. For projection writes, pass a database target only when projection usage and
   rebuild authority allow the operation and the target is an explicit `/tmp`
   proof path or the resolved projection policy path.
5. If policy is missing, ambiguous, incompatible with the command, or lacks the
   required path, stop and report the missing value.

## Command Notes

`bootstrap-state`, `register-artifact`, `select-batch`, and `queue-batch`
validate JSON state targets against policy. `validate --require-project-policy`
is read-only and should be used to prove policy presence before a workflow asks
for durable writes. Dry-run and stdout commands are the safest way to inspect
what would happen without creating state.

# State Fixtures

Use this reference only when a workflow needs explicit JSON planning state for
proof runs, write-transition checks, or projection inputs. Markdown planning
artifacts remain the human-readable coordination source; JSON fixtures are an
operational companion, not the durable planning ledger.

## Fixture Types

- Read-only diagnostics: use `current` and `validate` against the planning root
  when no JSON state is needed.
- Explicit JSON state fixture: use `bootstrap-state` when a command needs
  registered artifacts, obligations, or transition state beyond Markdown facts.
- Transition receipt: use `select-batch`, `queue-batch`, or later transition
  commands to update an explicit fixture and capture the command result.
- Human planning artifact: keep dispatches, runways, ledgers, `CURRENT.md`, and
  closeouts as Markdown under the project planning root.

## Command Sequence

1. Validate the Markdown planning root before generating a fixture:

   ```bash
   python scripts/planning_state.py validate --root <planning-root>
   ```

2. Generate JSON to stdout for inspection, or write to an explicit temp or
   policy-compatible target:

   ```bash
   python scripts/planning_state.py bootstrap-state --root <planning-root>
   python scripts/planning_state.py bootstrap-state --root <planning-root> --state-file /tmp/example-state.json
   ```

3. Validate the exact fixture before consuming it:

   ```bash
   python scripts/planning_state.py validate --root <planning-root> --state-file <state-file>
   ```

4. Use `register-artifact --dry-run` for path checks before writing fixture
   state. Use `register-artifact --state-file` only when the target passes
   state-file policy.

5. Use `select-batch` and `queue-batch` only with an explicit `--state-file`.
   Add `--receipt-file` for command evidence when the caller has supplied a
   temp or policy-compatible receipt target.

## Boundaries

Do not create fixture files in a project tree unless project policy declares
that exact durable target. `/tmp` is valid for smoke checks and generated-only
proof output. Reusable workflow code must resolve the caller's project policy or
stop with the missing policy value; it must not bake in another repository's
planning layout.

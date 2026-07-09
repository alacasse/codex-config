# Validation Command Status Runway

## Purpose

Add validation-command status classification to Batch Runway create-spec work so
generated runways cannot silently turn known-red commands or future-created
tests into required execution gates.

This spec executes the `ccfg-13-validation-command-status` batch described by
`docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/dispatch.md`.
It replaces the previously queued CCFG-11 runway as the active queue item.
CCFG-11 remains open and must not be executed from its displaced runway until
this validation-gate root cause is handled or explicitly superseded.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/dispatch.md`.
- Included finding: CCFG-13.
- Displaced finding: CCFG-11 is open in the program ledger, and its old
  dispatch/runway pair is retained as superseded planning evidence.
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q` is a
  current-green create-spec contract test baseline.
- `python -m pytest tests/test_codex_features_manifest.py -q` is currently
  known-red with three failures, so this batch must not list it as
  required-green unless a slice explicitly remediates it.
- `python -m pytest tests/test_skill_deletion_surfaces.py -q` currently fails
  because the file does not exist; that is implementation-created CCFG-11
  scope, not a CCFG-13 required-green baseline.

## Validation Command Status Classes

Every generated runway validation command must declare exactly one status class
before execution:

- `required-green`: the command is expected to pass at batch start or the slice
  explicitly owns making it pass before it gates later work.
- `known-red-baseline`: the command currently fails and is diagnostic or
  remediation scope until a named slice turns it green.
- `implementation-created`: the command targets a test, file, fixture, or tool
  that a named slice creates before the command can gate execution.
- `conditional`: the command runs only when a named file area, artifact, or
  metadata path changes.
- `diagnostic-only`: the command can inform planning or review, but cannot block
  execution without a later explicit promotion.

## Assumptions

- This is a create-spec contract fix, not a broad validation-system rewrite.
- The reusable guidance should define portable status semantics, not hard-code
  this repository's current failing commands into Batch Runway.
- Existing create-spec contract tests are the narrowest regression home unless
  execution finds a more precise test owner.
- CCFG-11 can be planned again after this batch closes, but this batch does not
  execute CCFG-11.

## Non-Goals

- Do not implement any slice during spec creation.
- Do not execute the displaced CCFG-11 runway.
- Do not remove focused validation from generated runways.
- Do not globally weaken required validation to avoid a red command.
- Do not add downstream-project paths, commands, cache locations, or local
  planning layouts to reusable Batch Runway guidance.

## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about
suspicious coordinator or subagent-lifecycle behavior.
Use the expanded convergence template only when scope is expanding, significant
uncertainty exists, blockers are present, or final batch reporting is produced.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execute-slice-core-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execution-contract-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/reporting-contracts-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/ledger-retention-v1.md`

Overrides:
- Use `lean-runway` density because this batch changes reusable workflow
  guidance, focused contract tests, and planning reconciliation only.
- Workers must preserve project-neutral Batch Runway guidance; repository-local
  command examples belong in tests, fixtures, or this planning batch only.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- `python scripts/planning_state.py current --root docs/plans`
  - status: `required-green`
  - scope: planning-state diagnostics
- `python scripts/planning_state.py validate --root docs/plans`
  - status: `required-green`
  - scope: planning-state diagnostics
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  - status: `required-green`
  - scope: Batch Runway create-spec contract guidance and tests
- `python -m pytest tests/test_codex_features_manifest.py -q`
  - status: `known-red-baseline`
  - scope: diagnostic only unless a slice explicitly remediates the existing
    command-owner failures
- `python -m pytest tests/test_skill_deletion_surfaces.py -q`
  - status: `implementation-created`
  - scope: CCFG-11 evidence only; do not run as a CCFG-13 gate unless a slice
    creates that file in this batch
- `git diff --check`
  - status: `required-green`
  - scope: all slices

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No SQLite database or durable JSON planning-state file is required.

Harness output:
- Existing `current`, `validate`, and focused pytest checks should not write
  live planning files.
- No generated summary artifact is required.

Index refresh:
- None required for these skill, tests, and planning-doc edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.
- Treat the CCFG-13 dispatch/runway pair and CCFG-11 queue replacement updates
  as baseline planning context.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Define Validation Command Status Contract | this slice commit | Create-spec guidance now requires validation-command status classes and prevents silent `required-green` promotion for known-red, future-created, or diagnostic commands. | Validation: `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`. Review: clean `runway_reviewer` pass against HEAD `f8b7c6a8259c42ffb76db5475cae507d5f080bdf`. |

## Slice 1. Define Validation Command Status Contract

Scope:
- Update Batch Runway create-spec guidance so every generated validation
  command must declare one of the five status classes before execution.
- Define when a command may be required-green and when it must instead be
  known-red-baseline, implementation-created, conditional, or diagnostic-only.
- Keep status semantics portable and avoid codex-config-specific command names
  in reusable guidance.

Allowed files/areas:
- `skills/batch-runway/references/create-spec.md`
- `skills/batch-runway/SKILL.md` only if create-spec entrypoint wording needs a
  short pointer to the new contract.
- `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/`

Non-goals:
- Do not change execution validation semantics outside the create-spec output
  contract.
- Do not edit CCFG-11 artifacts in this slice.

Acceptance criteria:
- Create-spec guidance requires each focused validation command to declare a
  status class.
- Required-green commands require a current passing result or a named
  slice-owned remediation path.
- Known-red and missing future-created commands cannot be promoted silently to
  required-green.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Not required unless tests change in this slice.

Commit message:
- `Define validation command statuses`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep reusable guidance project-neutral.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope and guidance clarity.
- Confirm the guidance prevents silent required-green promotion of known-red
  and future-created commands.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the guidance needs project-specific command lists to be meaningful.
- Stop if the change would weaken required validation instead of classifying it.

## Slice 2. Test Create-Spec Status Classification

Scope:
- Add focused contract tests for validation-command status classes in generated
  runway specs.
- Cover at least required-green, known-red-baseline, implementation-created,
  conditional, and diagnostic-only semantics.
- Assert that known-red or missing future-created commands need a named
  remediation, creating slice, trigger condition, or diagnostic-only status
  before they can appear in generated validation sections.

Allowed files/areas:
- `tests/test_batch_runway_create_spec_contract.py`
- `skills/batch-runway/references/create-spec.md` only for narrow wording needed
  to satisfy the contract tests.
- `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/`

Non-goals:
- Do not add broad Markdown snapshots.
- Do not require `tests/test_codex_features_manifest.py` to pass in this batch
  unless the slice explicitly fixes its existing failures.
- Do not create `tests/test_skill_deletion_surfaces.py`; that remains CCFG-11
  scope unless a later explicit amendment changes it.

Acceptance criteria:
- Tests fail if create-spec guidance omits the five status classes.
- Tests fail if required-green can be assigned without current-green evidence
  or a named slice-owned remediation.
- Tests fail if implementation-created commands can be listed without the slice
  that creates them.
- Tests fail if conditional commands lack trigger conditions.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required. Review should verify the tests protect validation-gate behavior
  rather than incidental wording.

Commit message:
- `Test validation command statuses`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep tests focused on create-spec output contracts.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope and test quality.
- Confirm the tests catch known-red and implementation-created commands being
  treated as required-green without evidence.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the tests require broad snapshots of complete generated runways.
- Stop if the tests would make current known-red unrelated manifest failures a
  required CCFG-13 gate.

## Slice 3. Reconcile The Displaced CCFG-11 Gate

Scope:
- Update planning evidence so the displaced CCFG-11 runway cannot be mistaken
  for an executable queued spec with unclassified validation gates.
- Add a compact note or amendment in the CCFG-11 batch artifacts, CCFG-13
  closeout evidence, or program ledger showing how its known-red and
  implementation-created commands should be classified before CCFG-11 is
  planned again.
- Keep CCFG-11 open; do not close, execute, or silently requeue it.

Allowed files/areas:
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/`
- `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/`

Non-goals:
- Do not implement CCFG-11 tests.
- Do not execute CCFG-11.
- Do not select successor work after CCFG-13 closeout.

Acceptance criteria:
- Active planning state points only to the CCFG-13 queued or active runway while
  this batch is running.
- CCFG-11 remains open in the program ledger.
- CCFG-11's displaced validation-gate ambiguity is visible enough that future
  planning must classify or regenerate those commands before execution.

Validation:
- Use the selected docs-only profile plus:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Not required unless tests change in this slice.

Commit message:
- `Reconcile displaced CCFG-11 gate`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Preserve CCFG-11 as open work and do not execute or requeue it.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 planning-state reconciliation.
- Confirm CCFG-13 remains the active queued batch and CCFG-11 is open, not
  hidden, closed, or active.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if reconciliation would require deleting or executing CCFG-11.
- Stop if program state would expose multiple queued or active batches.

## Final Validation

Run:
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `git diff --check`

Diagnostic-only checks:
- `python -m pytest tests/test_codex_features_manifest.py -q` remains
  known-red unless explicitly remediated by a slice.
- `python -m pytest tests/test_skill_deletion_surfaces.py -q` remains
  implementation-created CCFG-11 scope unless explicitly created by a slice.

## Batch Closeout Requirements

At closeout:
- Mark CCFG-13 closed only after guidance, tests, validation, review, and
  closeout evidence are complete.
- Keep CCFG-11 open unless a later explicit planning action requeues or
  supersedes it.
- Clear the CCFG-13 queued path from program `CURRENT.md` only after execution
  closeout evidence exists.
- Do not select or create a successor batch during CCFG-13 closeout.

## Stop Conditions

- Stop if work would execute the displaced CCFG-11 runway.
- Stop if work would list a known-red or missing future-created command as
  required-green without remediation or a named creating slice.
- Stop if work would add project-specific paths, validation commands, cache
  locations, or local planning layouts to reusable Batch Runway guidance.
- Stop if planning state reports multiple active artifacts.

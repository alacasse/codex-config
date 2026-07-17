# CCFG-25 Execution Report

## Status

```yaml
batch: ccfg-25-planning-ownership-transfer
status: blocked
completed_slice: 1
blocked_slice: 2
candidate_head: 5aa5add1251d1e4b3630a9678fdec244949cf691
stable_planning_head_before_report: 0119de2f346e61eb389ca07a2dd0b48f87ff22fc
candidate_worktree: clean
stable_worktree_scope: same-batch planning evidence only
successor_selected: false
```

## Completed Evidence

- Slice 1 candidate commit:
  `5aa5add1251d1e4b3630a9678fdec244949cf691`.
- Slice 1 stable receipt commit:
  `0119de2f346e61eb389ca07a2dd0b48f87ff22fc`.
- Required validation: 200 tests and 12 subtests passed; filtered manifest,
  scenario catalog, Ruff, BasedPyright, isolated installation, import-topology,
  delta-only test-quality, and independent review were clean.
- Full manifest retained only the declared Slice 2 and CCFG-26 failures.

## Slice 2 Blockers

### Runner planning behavior is outside the current path ceiling

The runway allows `scripts/architecture_program_runner.py`, but the planning
phase protocol and behavior are owned by sibling modules that Slice 2 does not
authorize:

- `scripts/architecture_program_runner_state.py` owns the fixed phase list;
- `scripts/architecture_program_runner_phase_contract.py` maps APR selection and
  create-spec obligations;
- `scripts/architecture_program_runner_validation.py` enforces the planning
  transitions; and
- `scripts/architecture_program_runner_command.py` renders the fresh Codex phase
  invocation.

The main runner delegates to these modules. Rewriting only the facade cannot
route planning through public `plan-batch` correctly. Removing or renaming the
persisted `select-dispatch` and `create-spec` phase identities would also change
serialized resume compatibility, which this runway does not authorize.

### Active planning callers are outside the current path ceiling

Current reusable instructions still route planning through Architecture Program
Runway and Batch Runway `create-spec` outside Slice 2's authorized paths:

- `skills/planning-artifacts/SKILL.md`;
- `skills/legacy-removal/SKILL.md`;
- `skills/port-by-contract/SKILL.md`; and
- `skills/dead-surface-audit/SKILL.md`.

Leaving them unchanged conflicts with the zero-live-planning-caller acceptance
boundary. Editing them without an amendment would broaden the slice.

## Evidence Classification

- Delete now: the duplicate Batch Runway installation link for
  `scripts/cross_checkout_context.py`, after preserving Planning State ownership.
- Migrate callers and tests first: APR planning ownership and Batch Runway
  `create-spec` ownership.
- Keep thin entrypoint: `scripts/architecture_program_runner.py` CLI and
  execution/closeout shell.
- Keep through CCFG-26: proceed/stop, delegation, recovery, validation acceptance,
  implementation review, commits/receipts, execution-ledger, finalization,
  closeout, same-batch reconciliation, no-successor enforcement, and strict
  cross-checkout execution safety.
- Keep through CCFG-29: temporary cross-checkout helper behavior.

## Next Safe Decision

Recommended: amend the existing CCFG-25 Slice 2 scope to include the exact runner
owner modules and active support-skill callers above, preserve the serialized
four-phase names as temporary compatibility owned by CCFG-27, independently
review the amended runway, then resume Slice 2 under a fresh strict lease.

The alternative is to retain those live callers temporarily, but that requires
an explicit acceptance amendment and removal owner because it weakens CCFG-25's
zero-live-planning-caller condition.

# CCFG-34 Minimal Stable Runway Dogfooding Bootstrap Runway

Status: `completed`

## Purpose

Implement the smallest temporary stable-generation improvement needed before
CCFG-26:

- one repository-local policy for vertical planning;
- one implementation slice per `work-batch` invocation;
- one optional read-only investigator consultation before avoidable escalation.

Manual relaunch is an accepted tradeoff. No runner architecture is added.

## Source Contract

- Dispatch: `dispatch.md`
- Finding:
  `../../findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`
- Ledger: `../../LEDGER.md`, CCFG-34 only
- Superseded first plan: `superseded.md`
- Related GitHub issues: #59, #60, #61

## Batch Contract

- Batch kind: `migration`
- Density: `lean-runway`
- Slice count: one implementation slice
- Execution context: ordinary single-root
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`
- Commit requirement: one clean focused implementation commit
- Closeout: separate planning-state reconciliation after complete evidence
- No successor selection

## Proportionality

### Observed problem

The remaining redesign batches will use the stable runway generation. Repeating
vertical-slice, one-slice-per-invocation, and read-only recovery guidance in each
runway is error-prone, but implementing automatic execution flights would require
temporary runner architecture.

### Minimum viable change

Create one repository-local policy and hook. The policy instructs stable agents
working on CCFG-26 through CCFG-29 to:

- plan smaller vertical slices with explicit ownership and removal conditions;
- execute only one pending implementation slice per `work-batch` invocation;
- consult the existing read-only investigator once before an avoidable mechanical
  escalation.

### Accepted limitation

Continuation remains manual. Final validation, finalization, and closeout retain
their current stable behavior. The bootstrap does not guarantee a fresh process
for every lifecycle boundary.

### Rejected larger alternative

Do not add an execution-unit result, launcher, state fields, repeated `execute`
transitions, unit receipts, or per-flight telemetry. Those changes are too large
and risky for temporary stable behavior.

## Temporary Policy Contract

The policy applies only to stable planning and execution of CCFG-26 through
CCFG-29.

For migration or ownership-transfer slices it requires:

```yaml
vertical_slice:
  starting_scenario: string
  durable_result: string
  owner_before: string
  owner_after: string
  migrated_callers: []
  focused_validation: []
  independently_usable_state: string
  rollback_boundary: string
  temporary_residue: []
```

When ownership coexists temporarily, the plan also names:

```yaml
migration_matrix:
  scenario_or_caller:
    current_owner: string
    future_owner: string
    status: pending | migrated
    removal_slice_or_condition: string
```

The policy additionally states:

- no ambiguous caller ownership or silent fallback;
- retained legacy routes require caller, reason, future owner, and removal
  condition;
- validation and review stay focused on the scenario owned by the slice;
- final range validation remains separate;
- clear oversizing requires a smaller-alternative analysis;
- slice count is derived from useful boundaries, never fixed in advance.

## Stable Execution Rule

For CCFG-26 through CCFG-29:

1. consume the current queued or active runway and existing durable state;
2. execute exactly the next incomplete implementation slice;
3. complete worker implementation, focused validation, independent review,
   correction if already authorized, commit, receipt, execution-ledger update, and
   completed-slice archive;
4. stop before beginning another implementation slice;
5. require a later explicit `work-batch` invocation to resume at the next
   incomplete ledger row.

This changes instructions only. It does not create automatic continuation or a
new durable result contract.

## Read-Only Recovery Advice

Before escalating an ambiguous blocker that appears mechanical, the coordinator
may consult `codebase_investigator` exactly once using its existing result
contract.

The bounded question includes only the active slice, stop condition, failing
command or evidence, current diff/worktree facts, and proposed smallest recovery.

The coordinator may continue only when the recovery is already authorized by the
active runway and existing recovery contract, such as:

- command invocation correction;
- exact retry;
- environment or cache repair;
- refreshed diff or review basis;
- already-authorized in-slice repair.

The coordinator stops for user direction or reviewed amendment on scope expansion,
validation reclassification, semantic change, safety weakening, destructive work,
new lifecycle surfaces, multiple material choices, or insufficient evidence.

The investigator cannot edit, approve, commit, delegate, select, amend, or grant
recovery authority.

## Implementation Ceiling

Required areas:

- root `AGENTS.md`
- `docs/plans/programs/codex-config/notes/`
- `tests/test_stable_runway_dogfooding_policy.py`
- `CHANGELOG.md`

Conditional only after direct evidence and reviewed amendment:

- `skills/work-batch/SKILL.md`
- `skills/batch-runway/references/execute-recovery-v1.md`
- `codex-features.json`

Forbidden:

- `scripts/architecture_program_runner*.py`
- `agents/codebase_investigator.toml`
- runner state, transitions, receipts, workers, validation, artifacts, telemetry,
  phase contracts, or public schemas
- candidate-generation repository or runtime Codex state

## Execution Ledger

| Slice | Status | Commit | Validation | Review | Notes |
|---|---|---|---|---|---|
| 1. Install the minimal temporary dogfooding policy | Completed | `ba1e941` | 5 tests and 43 subtests; Ruff and exact-range whitespace green | Clean planning amendment, delta-only test-quality review, and final independent review | Root hook, temporary policy, focused test, and changelog committed; no successor selected. |

## Commit Receipt

```yaml
slice: 1
commit: ba1e941
subject: docs: add minimal stable runway dogfooding policy
status: committed
files_changed:
  - AGENTS.md
  - CHANGELOG.md
  - docs/plans/programs/codex-config/notes/stable-runway-dogfooding-policy.md
  - tests/test_stable_runway_dogfooding_policy.py
validation: focused pytest 5 passed and 43 subtests passed; Ruff clean; exact-range whitespace clean
review: clean
convergence:
  phase: closure
  scope_trend: shrinking
  new_unknowns: []
  blockers: []
  next_proof: same-batch closeout reconciliation
```

## Resolved Planning Blocker

Final implementation review proved that the authorized `.codex/AGENTS.md` hook
is outside Codex's normal project-root-to-working-directory instruction chain.
The focused test therefore proves link resolution, not automatic loading. See
`execution-report.md` for the exact review basis and next safe action.

The exact bounded amendment received a clean independent planning review at
dispatch blob `7b43871b6a04317af15d8af3f540130aa5cc50f7` and runway blob
`5d2e978e8798ed3347bf8acfa4dc7429929e5624`. Resume only the root-hook and
focused-test correction. Do not commit or close the slice before corrected
validation and independent implementation review.

## Bounded Runway Amendment

The amendment replaces `.codex/AGENTS.md` with root `AGENTS.md` as the sole
project-local policy hook and requires the existing focused contract test to
validate that root hook. No other implementation file, slice, behavior,
validation class, architecture surface, or closeout rule changes.

## Slice 1 — Install The Minimal Temporary Dogfooding Policy

### Vertical Slice

```yaml
vertical_slice:
  starting_scenario: a stable agent plans or executes CCFG-26 through CCFG-29
  durable_result: repository-local instructions automatically load one policy requiring vertical planning, one implementation slice per invocation, and bounded existing-investigator advice
  owner_before: issue prose and manual runway-specific reminders
  owner_after: repository-local instruction hook plus one temporary policy document
  migrated_callers:
    - stable plan-batch for CCFG-26 through CCFG-29
    - stable work-batch for CCFG-26 through CCFG-29
  focused_validation:
    - policy hook contract test
    - required policy-content contract test
    - git diff --check
  independently_usable_state: later CCFG planning and execution receive the temporary rules without runner changes
  rollback_boundary: revert the hook, policy, focused test, changelog, and mechanically required metadata
  temporary_residue:
    - repository-local policy hook removed by CCFG-29 after candidate parity
    - policy document removed by CCFG-29 after candidate parity
    - focused regression test removed only after equivalent candidate scenarios pass
```

### Scope

- Add one policy document under
  `docs/plans/programs/codex-config/notes/`.
- Reference it from root `AGENTS.md`.
- Add one focused contract test proving the root hook and required policy
  clauses.
- Update `CHANGELOG.md`.
- Change feature metadata only when the current feature installation contract
  mechanically requires it.

### Allowed Files

- `AGENTS.md`
- `docs/plans/programs/codex-config/notes/**`
- `tests/test_stable_runway_dogfooding_policy.py`
- `CHANGELOG.md`
- `codex-features.json` only when directly required

No other implementation path is authorized without a reviewed amendment.

### Acceptance Criteria

- Agents entering this repository are instructed to load the one temporary
  CCFG-34 policy.
- The policy is explicitly limited to CCFG-26 through CCFG-29.
- All vertical-slice, migration-residue, one-slice-per-invocation, recovery-advice,
  authority-limit, and CCFG-29 removal requirements are present.
- The policy accepts manual relaunch and does not promise automatic fresh flights.
- The policy does not require separate finalization or closeout processes.
- `codebase_investigator` remains unchanged and advisory.
- No runner, agent contract, generic skill, candidate code, or runtime state is
  changed.

### Validation

Required green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_stable_runway_dogfooding_policy.py

git diff --check
```

Run focused Ruff only if the test is Python:

```sh
.venv/bin/ruff check --no-cache tests/test_stable_runway_dogfooding_policy.py
```

Run delta-only `test-quality-review` because a test changes.

Diagnostic only:

```sh
./install.sh --status
./install.sh --dry-run
```

Do not install or mutate runtime Codex state.

### Commit

`docs: add minimal stable runway dogfooding policy`

### Worker Brief

Implement only the root repository-local hook, temporary policy, focused test,
changelog, and mechanically required metadata. Do not modify runner scripts,
generic skills, agent TOMLs, candidate code, or runtime state. Do not add a
launcher, protocol, receipt, state field, transition, or telemetry.

### Reviewer Brief

Review the exact diff basis. Verify automatic local loading, complete policy
content, manual one-slice boundary, unchanged investigator contract, CCFG-29
removal gate, and absence of runner or generic-skill changes.

### Slice Stop Conditions

- Stop if the local instruction chain cannot load the policy without changing
  runner architecture.
- Stop if a generic skill or agent contract appears necessary; require a reviewed
  amendment before widening.
- Stop after the clean commit, receipt, execution-ledger update, and archive
  update. Do not begin another implementation slice.

## Final Validation

Use a later fresh coordinator invocation when practical. Re-run the focused policy
test, Ruff when applicable, and `git diff --check` over the exact implementation
range. Verify no forbidden path changed.

The final review must confirm that the implementation is still only an instruction
and policy bootstrap.

## Closeout

Close CCFG-34 only after complete implementation, focused validation, review,
receipt, and final evidence.

Closeout may:

- mark CCFG-34 closed;
- return CCFG-26 from `Blocked` to `Open`;
- clear CCFG-34 selected, queued, and active state;
- preserve the superseded CCFG-26 planning evidence;
- leave CCFG-26 unselected, undispatched, unqueued, and without a runway.

Closeout must not select, dispatch, queue, prepare, or begin CCFG-26.

## CCFG-29 Removal Gate

CCFG-29 must remove the policy hook, policy document, focused temporary test, and
related metadata only after:

- the candidate generation is authoritative;
- permanent #59, #60, and #61 behavior is active and validated;
- equivalent candidate planning, slice execution, escalation, and no-successor
  scenarios pass;
- removal does not restore a legacy route or make historical evidence unreadable.

CCFG-29 stops if parity is incomplete.

## Batch Stop Conditions

- Stop on any runner script, state, transition, receipt, worker, validation,
  artifact, telemetry, phase-contract, or public-schema change.
- Stop on any `codebase_investigator` TOML or result-contract change.
- Stop if more than one implementation slice is added without a concrete useful
  intermediate state.
- Stop on candidate code, runtime state, default generation, bridge, CCFG-26
  implementation, or successor selection.
- Stop if the temporary policy becomes a permanent generic workflow contract.

# CCFG-25 Slice 2 Blocker Report

## Status

```yaml
batch: ccfg-25-planning-ownership-transfer
slice: 2
status: blocked
blocker_class: outside-ceiling-runner-safety-owner
candidate_head: 5aa5add1251d1e4b3630a9678fdec244949cf691
candidate_diff_sha256: a2f1b2d443767f41729634a54448bdadfcf7342035be70f282dd8f779cc1d15b
candidate_commit_created: false
independent_implementation_review: findings
closeout_created: false
successor_selected: false
```

## Executive Summary

Slice 2 is stopped because the complete `plan-batch` transaction and the
architecture program runner disagree about which dirty planning artifacts are
safe when the runner advances from serialized `select-dispatch` to serialized
`create-spec`.

The amended Slice 2 ceiling does not include the module that owns this safety
decision:

```text
scripts/architecture_program_runner_change_allowance.py
```

The explicit runway stop condition requires execution to stop when another live
runner owner outside the amended ceiling is discovered. The candidate diff is
therefore uncommitted even though its focused validation and specialist reviews
are clean.

## Blocking Runtime Sequence

1. The amended phase contract makes `select-dispatch` invoke public
   `plan-batch` once for the complete planning flight.
2. The deterministic `plan-batch` boundary writes the authorized `CURRENT.md`,
   dispatch, runway, and DEC-038 transaction paths after planning and independent
   review succeed.
3. The serialized phase identity advances to compatibility `create-spec`, which
   is intended to observe the completed planning result and advance without
   planning again.
4. Before invoking that phase, `architecture_program_runner.py` calls
   `check_worktree(...)` using the active `create-spec` phase.
5. `architecture_program_runner_change_allowance.py` currently permits runner
   artifacts plus `dispatch_path` and `spec_path` for `create-spec`. It does not
   permit the prior transaction's `CURRENT.md` or selection-transaction path.
6. Those paths are classified as unexpected, so the runner raises
   `RunnerError` before the compatibility observation phase can run.

This is a direct runtime invariant, not a documentation-only concern. The
existing change-allowance tests cover expected state/artifact paths and rejection
of unrelated project files, but they do not cover a complete `plan-batch` flight
followed by `create-spec` preflight.

## Why Work Cannot Continue Under The Current Amendment

- The live safety owner is outside the exact user-authorized path ceiling.
- Silently adding it would violate the explicit stop condition.
- Broadly allowing the planning root would weaken dirty-worktree safety and is
  not an acceptable repair.
- The change needs focused regression proof that only artifacts produced by the
  completed planning transaction survive the `create-spec` preflight.
- Any amended runway content must receive a fresh independent planning review
  before the same slice resumes.

The already authorized conditional runner modules remain unchanged. Current
evidence does not require edits to
`architecture_program_runner_state.py`,
`architecture_program_runner_validation.py`, or
`architecture_program_runner_command.py`.

## Separate Acceptance Blocker

The Slice 2 runway names this command as `required-green`:

```sh
.venv/bin/python scripts/skill_contract.py validate --root .
```

The current CLI requires `--toolchain-root` and explicit paths, so the named
command exits with a usage error. Focused skill-contract catalog/migration tests,
the contract-bearing changed-skill validation, and skill quick-validation are
green, but they do not make the exact runway command pass. A newly reviewed
amendment must correct the command or explicitly reclassify and replace the gate.

## Evidence That Is Not Blocking

- Focused Slice 2 suite: 169 tests and 238 subtests passed.
- Migrated Batch Runway planning-contract tests: 13 tests and 200 subtests
  passed.
- Command-owner scenario catalog: 69 scenarios valid.
- Filtered manifest: 21 tests and 210 subtests passed; the full manifest retains
  only the named CCFG-26 failure.
- Broad projection/deletion diagnostics: all six current failures are a subset
  of the 12 failures at the exact candidate baseline; Slice 2 introduced no new
  broad failure.
- Ruff, whitespace, and changed-runner BasedPyright checks passed.
- Dead-surface, import-topology, and delta-only test-quality reviews are clean on
  the exact candidate diff.
- The full-ceiling BasedPyright findings reproduce unchanged in baseline
  `state.py` and `validation.py`; they do not justify editing those conditional
  modules in this slice.

## Smallest Decision Needed To Resume

Resume requires explicit authorization for another bounded amendment to the
same CCFG-25 Slice 2. The minimum amendment would:

1. add `scripts/architecture_program_runner_change_allowance.py` to the exact
   implementation ceiling;
2. permit its existing focused test,
   `tests/test_architecture_program_runner_change_allowance.py`;
3. require a focused regression for the complete `plan-batch` transaction to
   compatibility `create-spec` transition without weakening unrelated dirty-file
   rejection;
4. correct or explicitly reclassify the stale skill-contract validation command;
   and
5. obtain a fresh independent planning review before resuming the same slice.

The amendment must preserve all existing constraints: no new harness, generalized
runner abstraction, protocol, bridge, state version, compatibility wrapper,
planning store, or owner; no serialized phase rename or migration; no CCFG-26
ownership change; no closeout; and no successor selection.

Until that direction is explicit, the safe state is the current one: CCFG-25
remains active and blocked, Slice 1 remains closed, the Slice 2 candidate diff
remains uncommitted, and later batches remain unselected.

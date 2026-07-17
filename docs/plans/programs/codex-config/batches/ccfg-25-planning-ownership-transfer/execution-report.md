# CCFG-25 Execution Report

## Status

```yaml
batch: ccfg-25-planning-ownership-transfer
status: slice-2-blocked-required-green-command-contract
completed_slice: 1
active_slice: 2
candidate_head: 5aa5add1251d1e4b3630a9678fdec244949cf691
stable_planning_head_before_report: 24f5ab9b66bb0e0060df5b8483597cbb5c5146d9
candidate_worktree: uncommitted-slice-2-diff
candidate_diff_sha256: 815c4ad7b15e9143cb95e3f5790440021416ccb28bd8120731ac92314c8b023e
stable_worktree_scope: same-batch planning evidence only
independent_implementation_review: blocked-one-required-green-gate
successor_selected: false
```

The user authorized a bounded same-slice amendment. The exact amended dispatch
hash is `0e07a56a6f7cc1ff81f3f0851d329f95277a2574c1bbe97cd26e72d635a7bd2a`;
the exact amended runway hash is
`ddc37370a7e6f1ba0661d8ab9b64b9975c3ff779aad9c11166776ec755ca38f8`.
The independent planning review is clean. No new batch, queue transition,
closeout, or successor was created.

Slice 2 implementation and specialist review completed within the amended
ceiling, but the final independent implementation review found a live runner
safety owner outside that ceiling. The candidate diff remains uncommitted and
the explicit stop condition is active.

Focused blocker analysis and the minimum decision needed to resume are recorded
in `blocker-report.md`.

## Completed Evidence

- Slice 1 candidate commit:
  `5aa5add1251d1e4b3630a9678fdec244949cf691`.
- Slice 1 stable receipt commit:
  `0119de2f346e61eb389ca07a2dd0b48f87ff22fc`.
- Required validation: 200 tests and 12 subtests passed; filtered manifest,
  scenario catalog, Ruff, BasedPyright, isolated installation, import-topology,
  delta-only test-quality, and independent review were clean.
- Full manifest retained only the declared Slice 2 and CCFG-26 failures.

## Resolved Slice 2 Blockers

The amendment adds the exact owner/caller paths below as an upper ceiling. A fresh
read-only caller audit at candidate commit
`5aa5add1251d1e4b3630a9678fdec244949cf691` found no required edit outside it.

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

## Amended Execution Outcome

- Independent planning review: clean against the exact hashes above.
- Initial caller/owner audit: clean before implementation.
- Expected runner semantic edit:
  `scripts/architecture_program_runner_phase_contract.py` only.
- Conditional runner modules: `state.py`, `validation.py`, and `command.py` need
  no edit under current focused evidence.
- Candidate validation: 169 focused tests and 238 subtests passed; the full
  manifest retained exactly the named CCFG-26 failure; all six current broad
  diagnostic failures are a subset of the 12 at the exact candidate baseline;
  Ruff, changed-runner BasedPyright, scenarios, whitespace, import topology,
  dead-surface audit, and delta-only test-quality review are clean.
- Independent implementation review: findings. The complete `plan-batch`
  transaction leaves `CURRENT.md`, dispatch, runway, review/transaction, and
  related planning artifacts for the runner to accept. The unchanged
  `create-spec` worktree allowance rejects at least `CURRENT.md` and the
  selection-transaction artifact before the observation/advance phase.
- Outside-ceiling owner:
  `scripts/architecture_program_runner_change_allowance.py`.
- Separate planning-spec defect: the runway's named `skill_contract.py validate
  --root .` required-green command uses stale CLI syntax and must be corrected or
  explicitly reclassified in any newly reviewed amendment.
- Next safe action: await explicit user direction. A further bounded amendment
  would need to name the outside-ceiling owner and a focused regression without
  weakening worktree safety, correct the validation command, and receive a new
  independent planning review before this same Slice 2 resumes.

No candidate commit, Slice 1 reopening, closeout, or successor selection was
performed.

## Second Bounded Amendment Resume Outcome

The second bounded amendment passed exact independent planning review and was
executed under a fresh strict lease from candidate commit
`5aa5add1251d1e4b3630a9678fdec244949cf691`. Only
`scripts/architecture_program_runner_change_allowance.py` and its focused test
were added to the prior candidate diff.

Independent implementation review initially rejected a hand-written transaction
parser. The in-ceiling repair replaced it with canonical planning-contract
validation/readers, real complete `plan-batch` transaction coverage, exact
producer/current/ledger/batch/artifact/revision/hash binding, and a regression
that rejects a schema-valid transaction attempting to nominate `README.md` as
`CURRENT.md`. Fresh review marks that finding resolved.

The candidate remains uncommitted only because the exact combined
skill-contract required-green command exits `1` with four unknown-external-
mechanism diagnostics. Each named contract validates alone, and catalog,
migration, routing, quick-validation, scenarios, focused tests, Ruff,
BasedPyright, and diff checks are green. `blocker-report.md` records the smallest
command-only amendment needed to resume without changing candidate code or
widening implementation scope.

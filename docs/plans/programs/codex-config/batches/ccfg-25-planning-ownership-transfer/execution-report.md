# CCFG-25 Execution Report

## Status

```yaml
batch: ccfg-25-planning-ownership-transfer
status: completed
completed_slice: 3
active_slice: none
candidate_head: 89671eceb9103039e7e6660e73837827c167a3a1
stable_planning_head_before_closeout: 203320ea0cba1d7525f2dd271e65701ce91aeb77
candidate_worktree: clean
candidate_diff_sha256: c5dee2c8d0f0fc65ed758360dd8dad51fbf66cf3fe9ed387d218197d8b283ae4
stable_worktree_scope: same-batch planning evidence only
independent_implementation_review: clean
successor_selected: false
```

## Slice 3 Completion Receipt

- Candidate commit: `89671eceb9103039e7e6660e73837827c167a3a1`.
- Exact cumulative binary diff SHA-256:
  `c5dee2c8d0f0fc65ed758360dd8dad51fbf66cf3fe9ed387d218197d8b283ae4`.
- Core validation passed 244 tests and 18 subtests; filtered manifest and
  deletion/projection gates, all 69 scenarios, both structural skill checks,
  Ruff, the exact three-script BasedPyright gate, and diff-check were green.
- Known-red diagnostics remained exact and non-regressing: one CCFG-26 manifest
  failure, six preclassified deletion-vocabulary failures, and bare
  BasedPyright at 311 errors and 16 warnings versus baseline 314 and 16.
- A fresh candidate home and the fixed isolated candidate home converged. Stable
  home status remained byte-for-byte unchanged.
- Exact acceptance passed 25 tests in one evidence-pytest process and reported
  69 scenarios, 31 contracts, 17 families, six evidence keys, and six aliases
  green. Generated output hashes and timing are recorded in `closeout.md`.
- Final independent, import-topology, dead-surface, and delta-only test-quality
  reviews were clean. Same-batch closeout is complete and no successor was
  selected or prepared.

## Resolved Slice 3 Blocked Validation Receipt

- Static convergence correction: `README.md` now names the independent
  `batch_planner` and `batch_plan_reviewer` roles; exact reviewed diff SHA-256
  `a0ec3393cd845a4fdb841a89468eea83f37bc140e3cfc10f833e53d17190602a`.
- Candidate commit: `89671eceb9103039e7e6660e73837827c167a3a1`.
- Required core tests: `244 passed, 18 subtests passed`; filtered manifest
  `21 passed, 1 deselected, 210 subtests`; filtered deletion/projection
  `7 passed, 18 deselected, 20 subtests`; 69 scenarios valid; structural skill
  checks, Ruff, and range diff-check green.
- Known-red diagnostics reproduced exactly: one CCFG-26 manifest failure and six
  preclassified deletion-vocabulary failures.
- Blocking gate: bare `.venv/bin/basedpyright` exits 1 with 311 errors and 16
  warnings. The exact `91179e84` baseline exits 1 with 314 errors and 16 warnings.
  CCFG-25 introduces zero diagnostics; all current diagnostics are in ten
  unchanged modules, including read-only or out-of-scope owners.
- Stop decision: do not edit those owners or silently change validation policy.
  Installation, exact acceptance, final range reviews, and closeout remain
  unstarted. See `slice-3-blocker-report.md`.

The bounded same-slice amendments culminated in unchanged dispatch SHA-256
`8fabe265e62b91251370c2733e771291605761caad3844f523c3be8f3990b5c1`
and command-amended runway SHA-256
`23c33eee6f637d177b6f897bbe832d1fe5639249340b542c3e4493d9d51ed02c`.
The exact independent planning review is clean. No new batch, queue transition,
closeout, or successor was created.

The earlier bounded-amendment blockers are retained below as historical evidence.
The command-only amendment replaced the combined skill-contract gate with two
single-document structural validations, received exact clean planning review,
and resumed the preserved Slice 2 diff without changing candidate content.

Focused blocker analysis and the minimum decision needed to resume are recorded
in `blocker-report.md`.

## Slice 2 Completion Receipt

- Candidate commit: `12f70727f7496e2aa2d5fff9b748ee97e19e63a2`.
- Reviewed pre-commit binary diff SHA-256:
  `815c4ad7b15e9143cb95e3f5790440021416ccb28bd8120731ac92314c8b023e`.
- Required matrix: `181 passed, 241 subtests passed`; filtered manifest,
  filtered deletion/projection, 69-scenario catalog, separate structural skill
  validations, five quick validations, Ruff, BasedPyright, and diff checks green.
- Known-red diagnostics: the declared CCFG-26 manifest wording failure and six
  preclassified deletion/projection subtest failures reproduced unchanged.
- Reviews: import topology, dead-surface, delta-only test quality, and final
  independent implementation review clean with no required fixes.
- Strict receipt identity: stable `e31993f5cbc3e6c99576419b5b87564ef396cbc5`,
  candidate base `5aa5add1251d1e4b3630a9678fdec244949cf691`, exact read-only
  review scopes empty; post-review candidate commit is the hash above.
- Next state: Slice 3 pending in this active batch. No closeout or successor.

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

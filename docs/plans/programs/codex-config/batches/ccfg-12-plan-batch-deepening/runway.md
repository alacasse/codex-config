# Plan-Batch Command-Owner Deepening Runway

## Purpose

Deepen `plan-batch` as the human-facing command-owner interface for "create the
next specs batch" without moving runtime ownership out of
`architecture-program-runway` or `batch-runway`.

This spec executes the `ccfg-12-plan-batch-deepening` batch described by
`docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/dispatch.md`.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/dispatch.md`.
- Included finding: CCFG-12.
- Source review:
  `docs/plans/programs/codex-config/notes/command-owner-deepening-review.md`.
- `plan-batch` currently owns the correct command intent and stop conditions,
  but its interface still mostly routes to lower-level skills.
- `architecture-program-runway` remains the owner for program selection,
  dispatch packets, queue state, and closeout reconciliation.
- `batch-runway` remains the owner for concrete runway spec mechanics and later
  execution orchestration.

## Assumptions

- This batch is a focused command-interface deepening, not a replacement of the
  runtime/support skill stack.
- The useful depth increase is in the `plan-batch` command contract: state
  decision table, ledger-only source rule, selected/queued/active handling,
  one-spec output, and stop-before-implementation behavior.
- Feature metadata and changelog should change only if the installed
  user-facing skill behavior surface changes.
- Existing manifest/routing tests are the right place for focused text-contract
  coverage unless execution reveals a better narrow test file.

## Non-Goals

- Do not implement any slice during spec creation.
- Do not deepen `work-batch`.
- Do not rewrite `add-to-ledger` or `port-by-contract`.
- Do not copy Batch Runway execution contracts into `plan-batch`.
- Do not move program-ledger grouping, selected dispatch, queue state, or
  closeout reconciliation out of `architecture-program-runway`.
- Do not create new CCFG findings or select another row.
- Do not introduce downstream project-specific paths or validation commands
  into reusable skills.

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
- Use `lean-runway` density because this batch is focused skill-interface,
  documentation-contract, and regression-test work.
- Workers must not write durable JSON planning state, SQLite projections, or
  downstream project planning roots.
- Workers must keep `architecture-program-runway` and `batch-runway` as runtime
  owners behind `plan-batch`; changes that duplicate their detailed procedures
  are out of scope.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- For command-owner manifest/routing coverage:
  `python -m pytest tests/test_codex_features_manifest.py -q`
- For Batch Runway create-spec output contract guardrails when this spec is
  touched:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- For planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For install metadata alignment, when `codex-features.json` changes:
  `./install.sh --dry-run`
- For hard-coding checks, the final diff should not introduce matches:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/plan-batch docs/skill-routing-contract.md docs/workflow-guide.md tests/test_codex_features_manifest.py`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No SQLite database or JSON planning-state file is required.

Harness output:
- Existing `current`, `validate`, and install dry-run checks should not write
  live planning files.
- No generated summary artifact is required.

Index refresh:
- None required for this repo after these skill, docs, test, and planning-doc
  edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.
- Treat the existing CCFG-12 review note, ledger row, and current-state updates
  as baseline planning context unless execution finds a direct contradiction.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 3. Align docs, metadata, and closeout evidence | Pending |  |  |  | Final validation and closeout can reconcile CCFG-12 | Update only necessary user-facing docs, feature metadata, changelog, and planning closeout evidence. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Deepen plan-batch command contract | `d6644a4` | success; added explicit command contract, state decision table, ledger-only source rule, one-spec output, and stop-before-implementation boundary | `python -m pytest tests/test_codex_features_manifest.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`; reviewer `runway_reviewer` clean |
| 2. Protect command-owner/runtime-owner boundaries | `0d68954` | success; added focused manifest/skill contract assertions for direct invocation, runtime-owner dependencies, state routing, ledger-only source, and one-spec/no-implementation rules | `python -m pytest tests/test_codex_features_manifest.py -q`; `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`; test-quality review clean; reviewer `runway_reviewer` clean |

## Slice 1. Deepen Plan-Batch Command Contract

Scope:
- Add a compact command contract section to `skills/plan-batch/SKILL.md`.
- Make the `plan-batch` interface explicit for these states:
  no selected work, selected dispatch exists, queued runway exists, active
  runway exists, requested existing ledger row exists, and no suitable ledger
  row exists.
- State the expected output for each state: select/write dispatch, create one
  runway, report queued/active state, or stop with `add-to-ledger` guidance.
- Preserve the existing support routing: `planning-state` first,
  `architecture-program-runway` for program selection/dispatch ownership, and
  `batch-runway` in `create-spec` mode for concrete runway mechanics.

Allowed files/areas:
- `skills/plan-batch/SKILL.md`
- This spec active-ledger/archive rows

Non-goals:
- Do not edit `skills/work-batch/SKILL.md`.
- Do not change `architecture-program-runway` or `batch-runway` behavior.
- Do not update manifest metadata in this slice unless the skill cannot remain
  internally consistent without it.

Acceptance criteria:
- `plan-batch` names the human-facing command interface in terms of decisions
  and stop conditions, not only as a list of support skills.
- The deletion test is satisfied in prose: deleting `plan-batch` would make
  ledger-source, selected-state, and one-spec rules reappear across callers.
- The skill still says external specs, ADRs, GitHub issues, archived plans,
  review notes, and external engineering-skill outputs are evidence only when a
  ledger row points to them.
- The skill still stops before implementation.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless tests are changed in this slice.

Commit message:
- `Deepen plan-batch command contract`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep runtime ownership in `architecture-program-runway` and `batch-runway`.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, command-contract clarity, and runtime-owner
  preservation.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the change requires moving program queue state into `plan-batch`.
- Stop if the change requires copying Batch Runway execution procedure into
  `plan-batch`.

## Slice 2. Protect Command-Owner/Runtime-Owner Boundaries

Scope:
- Add or tighten focused tests for the `plan-batch` command contract in
  `tests/test_codex_features_manifest.py` or the smallest suitable adjacent
  test file.
- Protect that `plan-batch` remains directly invokable and depends on
  `planning-artifacts`, `planning-state`, `architecture-program-runway`, and
  `batch-runway`.
- Protect that `plan-batch` owns ledger-only selection and state routing while
  naming `architecture-program-runway` and `batch-runway` as runtime/support
  owners rather than deprecated surfaces.
- Keep tests text-contract based and targeted; avoid broad Markdown snapshots.

Allowed files/areas:
- `tests/test_codex_features_manifest.py`
- `tests/test_batch_runway_create_spec_contract.py` only if needed to keep this
  queued spec compliant with create-spec output rules
- `skills/plan-batch/SKILL.md` only for small fixes driven by failing tests
- This spec active-ledger/archive rows

Non-goals:
- Do not add tests that require executing a real Batch Runway.
- Do not assert exact full skill text.
- Do not test archived APR/PST ledgers as active pickup sources.

Acceptance criteria:
- Tests fail if `plan-batch` loses the ledger-only source rule, state routing,
  or one-spec/no-implementation stop behavior.
- Tests fail if `plan-batch` stops requiring either runtime owner.
- Tests still allow `architecture-program-runway` and `batch-runway` to remain
  agent-facing support/runtime skills.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required if this slice adds or changes tests. Review should focus on whether
  the assertions protect command behavior rather than brittle incidental prose.

Commit message:
- `Protect plan-batch command-owner boundaries`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep tests focused on observable workflow contracts: command ownership,
  runtime dependencies, stop rules, and backlog-source rules.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope and test quality.
- Confirm tests would fail for the intended regressions without freezing
  unrelated wording.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if proving the contract requires broad parser tooling or a new test
  harness.
- Stop if tests start enforcing archived planning paths as active state.

## Slice 3. Align Docs, Metadata, And Closeout Evidence

Scope:
- Update `docs/skill-routing-contract.md`, `docs/workflow-guide.md`, or
  `README.md` only where they would otherwise contradict the deepened
  `plan-batch` interface.
- Update `codex-features.json` and `CHANGELOG.md` if the installed skill
  behavior surface changed.
- Keep the active program ledger and current-state files aligned with the
  completed queued runway during finalization.
- Record compact closeout evidence for CCFG-12.

Allowed files/areas:
- `docs/skill-routing-contract.md`
- `docs/workflow-guide.md`
- `README.md`
- `codex-features.json`
- `CHANGELOG.md`
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/`

Non-goals:
- Do not rewrite the full workflow guide.
- Do not modify external Matt Pocock skills or `skills-lock.json`.
- Do not select another batch after closing CCFG-12.

Acceptance criteria:
- User-facing docs agree that `plan-batch` owns the human command while
  runtime/support skills remain behind it.
- Feature metadata and changelog reflect meaningful installed behavior changes,
  if any.
- CCFG-12 is closed only with implementation, validation, review, and closeout
  evidence.
- Program current state returns to no queued batch after closeout unless a
  separate explicit request selects another batch.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `./install.sh --dry-run` if `codex-features.json` changed
  `git diff --check`

Test quality review:
- Required only if this slice changes tests.

Commit message:
- `Align plan-batch deepening metadata`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep docs compact and avoid broad restatements of runtime skill procedures.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, metadata consistency, and closeout readiness.
- Confirm no new project-specific downstream paths or validation commands were
  added to reusable skills.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if finalization would require selecting another CCFG row.
- Stop if metadata changes imply runtime/support skills are deprecated or
  removed.

## Final Validation

Before closeout, run:

- `python -m pytest tests/test_codex_features_manifest.py -q`
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `./install.sh --dry-run` if `codex-features.json` changed
- `git diff --check`

Also run the hard-coding check from the validation profile section and record
any intentional matches. There should be no new downstream project-specific
paths in reusable skill guidance.

## Stop Conditions

- Stop on scope drift into broad command-owner refactoring.
- Stop on any attempt to make `architecture-program-runway` or `batch-runway`
  obsolete in this batch.
- Stop on missing subagent support during execution.
- Stop on dirty-file conflicts outside the active slice scope.
- Stop if validation requires network access or downstream project state not
  named by this spec.
- Stop if the implementation cannot preserve the ledger-only executable
  backlog rule for `plan-batch`.

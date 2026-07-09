# Batch Runway Hot-Path Pruning Runway

## Purpose

Reduce routine Batch Runway execution/context load without changing runtime
semantics. This batch should prune duplication, move non-routine detail behind
existing trigger references, and leave the future execution path easier for a
fresh coordinator to load.

This spec executes the `ccfg-7-batch-runway-hot-path-pruning` batch described by
`docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/dispatch.md`.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/dispatch.md`.
- Included finding: CCFG-7.
- Current Batch Runway guidance is already split into references, but routine
  execution still repeats context-discipline, reporting, subagent, validation,
  recovery, and finalization instructions across the entrypoint and reference
  files.
- The intended routine execution hot path is `skills/batch-runway/SKILL.md`,
  `skills/batch-runway/references/execute-slice-core-v1.md`, and the selected
  validation profile file.

## Assumptions

- This is a workflow-contract documentation batch, not a runtime code change.
- The useful improvement is reducing what routine Batch Runway coordinators must
  read and retain, while preserving all existing execution obligations through
  clear reference ownership.
- Deleting repeated prose is acceptable only when an equivalent owner reference
  remains discoverable from the routine path.
- Focused text-contract tests are enough to guard the hot-path shape.

## Non-Goals

- Do not implement any slice during spec creation.
- Do not change Batch Runway runtime semantics.
- Do not alter coordinator/worker/reviewer role boundaries.
- Do not change per-slice validation, review, commit, recovery, finalization, or
  ledger-retention obligations.
- Do not rewrite `plan-batch`, `work-batch`, `architecture-program-runway`, or
  `planning-state`.
- Do not introduce project-specific downstream paths, validation commands, cache
  locations, or local planning layouts into reusable skills.
- Do not run nested Codex sessions or downstream project harnesses.

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
- Use `lean-runway` density because this batch is behavior-preserving workflow
  guidance cleanup with focused regression tests.
- Workers must not change runtime code or project-specific validation behavior.
- Workers may delete, consolidate, or move Batch Runway guidance only when the
  same execution obligation remains owned by a named Batch Runway reference.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- For hot-path contract coverage:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- For manifest and feature dependency safety when metadata changes:
  `python -m pytest tests/test_codex_features_manifest.py -q`
- For planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For hard-coding checks, the final diff should not introduce matches:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/batch-runway tests/test_batch_runway_create_spec_contract.py`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No SQLite database or JSON planning-state file is required.

Harness output:
- Existing `current` and `validate` checks should not write live planning
  files.
- No generated summary artifact is required.

Index refresh:
- None required for these skill, docs, test, and planning-doc edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.
- Treat this dispatch/runway pair and the CCFG-7 ledger queue updates as
  baseline planning context.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1. Guard the routine hot-path contract | pending |  |  |  | Contract test and inventory note |  |
| 2. Prune entrypoint and execute-spec routing duplication | pending |  |  |  | Reduced duplicate routing prose with semantics preserved |  |
| 3. Slim routine execute-slice core detail | pending |  |  |  | Non-routine detail moved behind trigger references |  |
| 4. Align reporting and closeout references | pending |  |  |  | Final validation and closeout-ready evidence |  |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|

## Slice 1. Guard The Routine Hot-Path Contract

Scope:
- Add a focused text-contract test or small adjacent test section that captures
  the intended routine Batch Runway execution read path:
  `SKILL.md`, `execute-slice-core-v1.md`, and one selected validation profile.
- Capture the non-routine references that must remain trigger-loaded:
  recovery, finalization, reporting-contract details, subagent-brief variants,
  test-quality review, and projection reporting.
- Optionally add a compact in-repo inventory note only if the test would become
  unreadable without it; prefer a test over a new durable note.

Allowed files/areas:
- `tests/test_batch_runway_create_spec_contract.py`
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/execute-spec.md`
- This spec active-ledger/archive rows

Non-goals:
- Do not change Batch Runway behavior in this slice.
- Do not add broad Markdown snapshot tests.
- Do not inspect archived ledgers or downstream project planning roots.

Acceptance criteria:
- Tests fail if routine execution no longer points to
  `execute-slice-core-v1.md` plus the selected validation profile as the compact
  path.
- Tests fail if recovery/finalization/specialist guidance becomes mandatory for
  routine slices.
- Tests remain text-contract focused and do not assert entire documents.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required because this slice changes tests. Review should focus on behavioral
  signal and brittleness.

Commit message:
- `Guard Batch Runway hot path`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Protect the read-path contract without changing runtime semantics.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, text-contract value, and brittleness.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the only possible test is a brittle full-document snapshot.
- Stop if the desired hot path cannot be stated without changing execution
  obligations.

## Slice 2. Prune Entrypoint And Execute-Spec Routing Duplication

Scope:
- Reduce duplicated routine execution guidance in `skills/batch-runway/SKILL.md`
  and `skills/batch-runway/references/execute-spec.md`.
- Keep `SKILL.md` as the mode/router and context-discipline entrypoint.
- Keep `execute-spec.md` as the non-routine execution router and compatibility
  escalation reference, not a second copy of the routine slice loop.
- Ensure routine execution still points to `execute-slice-core-v1.md` and the
  selected validation profile.

Allowed files/areas:
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/execute-spec.md`
- `tests/test_batch_runway_create_spec_contract.py` only for focused test fixes
- This spec active-ledger/archive rows

Non-goals:
- Do not edit execution contract semantics.
- Do not remove recovery, finalization, or projection-reporting triggers.
- Do not change command-owner routing for `plan-batch` or `work-batch`.

Acceptance criteria:
- Routine instructions are shorter or less duplicated than baseline while
  preserving the same owner references.
- `execute-spec.md` no longer repeats detailed routine steps that are already
  owned by `execute-slice-core-v1.md`, except for a compact route summary.
- The entrypoint still makes stop conditions and role boundaries discoverable.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required only if tests are changed in this slice.

Commit message:
- `Prune Batch Runway routing duplication`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Preserve runtime semantics and reference ownership while reducing duplicate
  routine routing prose.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, semantic preservation, and whether routine
  execution still has a clear path.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if pruning makes a future coordinator load more files for routine
  execution.
- Stop if role-boundary or recovery-trigger semantics become ambiguous.

## Slice 3. Slim Routine Execute-Slice Core Detail

Scope:
- Prune `skills/batch-runway/references/execute-slice-core-v1.md` so it remains
  the routine hot-path projection rather than a full reference bundle.
- Move or replace non-routine detail with trigger references to existing owner
  files when safe:
  `reporting-contracts-v1.md`, `subagent-briefs.md`,
  `execute-recovery-v1.md`, `finalize-batch-v1.md`, and
  `test-quality-review.md`.
- Keep compact worker/reviewer report expectations and orchestration anomaly
  handling discoverable enough for routine execution.

Allowed files/areas:
- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/reporting-contracts-v1.md` only if moved text
  needs a clear owner
- `skills/batch-runway/references/subagent-briefs.md` only if moved text needs
  a clear owner
- `tests/test_batch_runway_create_spec_contract.py` only for focused test fixes
- This spec active-ledger/archive rows

Non-goals:
- Do not remove compact routine report schemas entirely.
- Do not make routine execution require loading full reporting or subagent
  references.
- Do not change specialist-review triggers or recovery behavior.

Acceptance criteria:
- `execute-slice-core-v1.md` is smaller or more scannable than baseline.
- Non-routine branches are represented by named trigger references rather than
  duplicated long instructions.
- Routine coordinator actions remain complete enough to execute a normal slice
  with one validation profile and compact subagent reports.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required only if tests are changed in this slice.

Commit message:
- `Slim Batch Runway execute core`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Preserve routine executability while removing duplicated or non-routine load.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, routine executability, and semantic preservation.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the core can no longer execute a routine slice without loading
  non-routine references.
- Stop if moved text loses an obvious owner reference.

## Slice 4. Align Reporting And Closeout References

Scope:
- Align any remaining references affected by Slices 1-3.
- Update `CHANGELOG.md` only if the installed Batch Runway behavior surface is
  meaningfully changed.
- Confirm CCFG-7 closeout evidence can point to focused tests, planning-state
  diagnostics, and the reduced routine-path guidance.

Allowed files/areas:
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/*.md`
- `tests/test_batch_runway_create_spec_contract.py`
- `CHANGELOG.md` only if warranted by behavior-surface wording changes
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/closeout.md`
- `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/completed-slices.md`
- This spec active-ledger/archive rows

Non-goals:
- Do not close CCFG-7 without implementation, validation, review, and closeout
  evidence.
- Do not close or rewrite other CCFG rows.
- Do not run project-level integration harnesses.

Acceptance criteria:
- Final diff contains no new project-specific downstream paths or validation
  commands in reusable Batch Runway guidance.
- Planning-state diagnostics pass.
- Focused hot-path contract tests pass.
- Program closeout can state what routine context load was reduced and why
  semantics are unchanged.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/batch-runway tests/test_batch_runway_create_spec_contract.py`
  `git diff --check`

Test quality review:
- Required if tests changed in this batch.

Commit message:
- `Close Batch Runway hot path pruning`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Align references and closeout evidence without changing runtime semantics.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, final semantic preservation, validation evidence,
  and closeout readiness.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if final validation reveals a semantic change in execution obligations.
- Stop if closeout would need to claim implementation evidence that does not
  exist.

## Final Validation

Run:
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- `python -m pytest tests/test_codex_features_manifest.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/batch-runway tests/test_batch_runway_create_spec_contract.py`
- `git diff --check`

Final report must include:
- commits per slice
- focused validation results
- review results
- confirmation that routine Batch Runway context load was reduced without
  changing runtime semantics
- cleanup residues, if any
- `orchestration_anomalies`
- expanded convergence assessment

## Stop Conditions

- Stop if implementation would alter runtime semantics.
- Stop if routine execution cannot remain bounded to the compact hot path.
- Stop if project-specific downstream paths or validation commands appear in
  reusable skill guidance.
- Stop if tests would need broad snapshots or nested Codex execution to prove
  the cleanup.
- Stop if a dirty-file conflict appears outside the active slice scope.

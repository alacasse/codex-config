# Skill Deletion Tests Runway

## Supersession Notice

This runway is no longer queued active state. It was displaced by
`docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md`
because its validation section listed known-red and implementation-created
commands without status classes. CCFG-11 remains open in the program ledger and
must be regenerated or amended after CCFG-13 and CCFG-14 close before execution
resumes.

## Displaced Validation Gate Amendment

Future CCFG-11 planning must regenerate or classify this runway's validation
commands before execution. In this displaced spec, the currently ambiguous
commands are:

- `python -m pytest tests/test_codex_features_manifest.py -q`
  - status: `known-red-baseline`
  - handling: diagnostic until a named CCFG-11 slice remediates the existing
    manifest failures or records a current-green result.
- `python -m pytest tests/test_skill_deletion_surfaces.py -q`
  - status: `implementation-created`
  - handling: cannot gate execution until a named CCFG-11 slice creates the
    test file or replaces this command with an existing current-green owner.

Do not execute this displaced runway as-is. A future CCFG-11 runway must make
every focused validation command explicit as `required-green`,
`known-red-baseline`, `implementation-created`, `conditional`, or
`diagnostic-only` before it becomes active.

## Displaced Risk Gate Amendment

Future CCFG-11 planning must also regenerate or amend this runway with
Batch Runway risk metadata before execution. This displaced spec predates the
CCFG-14 batch-kind and destructive-slice gate requirements, so it must remain
superseded planning evidence until a future CCFG-11 artifact:

- declares one batch kind for the batch;
- declares slice risk classes for any slice that could migrate, narrow, demote,
  or delete a skill surface; and
- includes explicit approval gates before any `destructive-cleanup` or
  `contract-narrowing` slice executes.

Do not treat this amendment as selecting, queuing, executing, or regenerating
CCFG-11. CCFG-14 remains the queued prerequisite batch until its closeout
reconciles program state.

## Purpose

Create focused deletion-test evidence for no-op, sediment, and obsolete skill
surfaces in the codex-config skill set. This batch should make it easier to
decide whether a surface should be deleted, migrated, narrowed, or kept with a
clear contract, without using deletion as a shortcut around command-owner or
support-skill responsibilities.

This spec executes the `ccfg-11-skill-deletion-tests` batch described by
`docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/dispatch.md`.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/dispatch.md`.
- Included finding: CCFG-11.
- Source evidence says no focused deletion-test audit was found for skill
  no-ops and sediment.
- `dead-surface-audit` already names an evidence pattern for surfaces that look
  alive only because tests preserve imports, aliases, topology, or compatibility
  shape.
- `legacy-removal` already names exceptional cleanup handling for obsolete
  surfaces, stale names, wrappers, fallbacks, and compatibility paths.
- Recent command-owner work established that direct human commands such as
  `add-to-ledger`, `plan-batch`, `work-batch`, and `port-by-contract` must not
  be deleted merely because support skills own runtime mechanics.

## Assumptions

- This is an evidence and test batch, not a broad skill-system rewrite.
- The highest-value deletion test is classification: prove which surfaces are
  command-owner contracts, support contracts, necessary narrow entrypoints,
  no-ops, sediment, obsolete internal compatibility, or human-decision cases.
- Deletion is only one possible outcome. "Keep with justification",
  "migrate tests first", and "narrow entrypoint" are valid outcomes when
  evidence supports them.
- Existing manifest/routing tests and small adjacent fixtures are the right
  place for focused coverage unless execution finds a narrower test owner.

## Non-Goals

- Do not implement any slice during spec creation.
- Do not delete, rename, or demote skills during planning.
- Do not create a new support skill unless CCFG-11 execution explicitly proves
  one is needed and the user approves that scope.
- Do not rewrite `dead-surface-audit`, `legacy-removal`, command-owner skills,
  or the installer model wholesale.
- Do not treat archived APR/PST ledgers as active pickup sources.
- Do not introduce downstream project-specific paths, validation commands,
  cache locations, or local planning layouts into reusable skills.

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
- Use `lean-runway` density because this batch is focused skill evidence,
  tests, and compact planning closeout.
- Workers must not delete, demote, rename, or uninstall skills unless the
  assigned slice explicitly includes that action and the evidence/test gate is
  satisfied.
- Workers must preserve command-owner and support-skill boundaries from
  `docs/skill-routing-contract.md` unless the slice records a narrower
  evidence-backed correction.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- For installed skill metadata and command-owner dependency coverage:
  `python -m pytest tests/test_codex_features_manifest.py -q`
  - displaced status: `known-red-baseline`
  - handling before future execution: remediate in a named slice, record a
    current-green result, or keep diagnostic/non-gating.
- For create-spec and Batch Runway contract guardrails when this spec is
  touched:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  - displaced status: `required-green`
- For deletion/dead-surface audit coverage:
  `python -m pytest tests/test_skill_deletion_surfaces.py -q`
  - displaced status: `implementation-created`
  - handling before future execution: create in a named CCFG-11 slice or
    replace with an existing current-green command.
- For planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  - displaced status: `required-green`
- For install metadata alignment, when `codex-features.json` or install-owned
  paths change:
  `./install.sh --dry-run`
  - displaced status: `conditional`
- For project-neutrality checks, the final diff should not introduce matches:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills tests docs/skill-routing-contract.md docs/workflow-guide.md`
  - displaced status: `conditional`
- Always run `git diff --check`.
  - displaced status: `required-green`

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No SQLite database or durable JSON planning-state file is required.

Harness output:
- Existing `current`, `validate`, and install dry-run checks should not write
  live planning files.
- No generated summary artifact is required.

Index refresh:
- None required for these skill, docs, tests, and planning-doc edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.
- Treat this dispatch/runway pair and the CCFG-11 ledger queue updates as
  baseline planning context.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|

## Slice 1. Inventory Deletion-Test Surfaces

Scope:
- Add a compact deletion-test inventory or fixture that classifies the current
  skill surfaces involved in command ownership, support-only evidence, runtime
  support, no-op candidates, sediment candidates, and obsolete internal
  compatibility candidates.
- Use existing repository data where possible: `codex-features.json`, skill
  frontmatter, `docs/skill-routing-contract.md`, and existing tests.
- Create `tests/test_skill_deletion_surfaces.py` if no narrower existing test
  owner fits the deletion-test inventory.
- Keep archived PST issue #27 as source evidence only; do not use archived
  ledgers for active selection.

Allowed files/areas:
- `tests/`
- `skills/dead-surface-audit/SKILL.md` only if a wording gap blocks the
  inventory from using its evidence vocabulary.
- `skills/legacy-removal/SKILL.md` only if a wording gap blocks obsolete-surface
  classification.
- `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/`

Non-goals:
- Do not delete any skill in this slice.
- Do not add a broad scanner over all historical planning files.
- Do not freeze full Markdown documents in snapshots.

Acceptance criteria:
- The inventory distinguishes command-owner skills from support/runtime skills
  and from surfaces that may be deleted or narrowed.
- At least one test or fixture would fail if a command-owner skill were
  misclassified as deletion-safe solely because a support skill covers details.
- The inventory records whether each candidate needs `delete-now`,
  `migrate-tests-first`, `keep`, `keep-thin-entrypoint`, or
  `human-contract-decision` style follow-up.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python -m pytest tests/test_skill_deletion_surfaces.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required if this slice adds or changes tests. Review should focus on whether
  the tests protect deletion decisions instead of incidental wording.

Commit message:
- `Inventory skill deletion surfaces`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Produce deletion-test evidence, not deletion.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, evidence classification, and test quality.
- Confirm the tests would catch unsafe deletion of command-owner surfaces
  without preserving obsolete internals unnecessarily.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if classification requires a human contract decision before any useful
  test can be written.
- Stop if the slice starts preserving obsolete internals only because existing
  tests assert shape.

## Slice 2. Add Focused Deletion-Test Coverage

Scope:
- Add or tighten tests that apply the deletion-test inventory to representative
  surfaces:
  command-owner skill, agent-facing support skill, runtime workflow support,
  obsolete/sediment candidate, and no-op candidate where evidence exists.
- Prefer small parser/helper tests over full-document snapshots.
- Keep assertions tied to observable contracts: direct invocation, dependency
  visibility, routing ownership, evidence vocabulary, and deletion-safe
  classification.

Allowed files/areas:
- `tests/`
- `codex-features.json` only if test evidence proves metadata is missing or
  misleading.
- `skills/*/SKILL.md` only for narrow wording needed to expose an existing
  contract to tests.
- `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/`

Non-goals:
- Do not execute a real deletion or uninstall flow.
- Do not add tests that require network access or downstream project checkouts.
- Do not assert exact full skill text.

Acceptance criteria:
- Tests fail if a support-only skill is accidentally advertised as the preferred
  human command when a command-owner exists.
- Tests fail if a skill surface is marked deletion-safe without checking for a
  named contract or human-decision requirement.
- Tests allow "keep with justification" when a surface still satisfies a
  documented contract.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python -m pytest tests/test_skill_deletion_surfaces.py -q`
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required. Review should verify that assertions are behavioral enough to guide
  future deletions and not merely textual churn detectors.

Commit message:
- `Test skill deletion decisions`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep tests focused on deletion safety and contract evidence.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope and test quality.
- Confirm the tests discriminate delete, keep, narrow, and human-decision cases
  without requiring broad snapshots.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if deletion-safety cannot be tested without broad markdown snapshots.
- Stop if test evidence suggests a candidate should be deleted immediately;
  record the evidence and require an explicit slice/user decision before
  deletion.

## Slice 3. Apply One Narrow Skill-Surface Decision

Scope:
- Use the focused deletion-test evidence to apply exactly one narrow cleanup
  decision:
  delete a proven no-op/sediment surface, narrow an entrypoint, migrate a stale
  test, or record a keep-with-justification result.
- Choose the lowest-risk candidate with clear evidence from Slices 1 and 2.
- Update affected metadata/docs/tests only for that one decision.

Allowed files/areas:
- The single skill, metadata, docs, or test surface selected by Slice 1/2
  evidence.
- `codex-features.json` and `CHANGELOG.md` if installed behavior changes.
- `tests/`
- `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/`

Non-goals:
- Do not perform multiple deletions.
- Do not delete command-owner skills.
- Do not remove `architecture-program-runway`, `batch-runway`,
  `planning-state`, or `planning-artifacts` merely because command-owner skills
  route through them.

Acceptance criteria:
- The chosen decision follows the status produced by the deletion-test
  inventory.
- Tests demonstrate why the surface is safe to delete/narrow or why it must be
  kept.
- Installed metadata and changelog are updated if user-visible skill behavior
  changes.
- The batch records deferred candidates rather than silently dropping them.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python -m pytest tests/test_skill_deletion_surfaces.py -q`
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `./install.sh --dry-run` when metadata changes
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required when tests are changed or deleted. Review should confirm the cleanup
  does not lower regression signal.

Commit message:
- `Apply one skill deletion decision`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Apply exactly one evidence-backed decision and leave other candidates
  deferred.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, metadata safety, and whether the evidence justifies
  the chosen cleanup decision.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the selected decision would remove or demote a human-facing command
  without explicit user approval.
- Stop if the evidence points to multiple unrelated cleanups; split or defer
  rather than widening this slice.

## Slice 4. Close Out Deletion Evidence

Scope:
- Record compact closeout evidence for CCFG-11: tested classification model,
  chosen cleanup decision, deferred candidates, validation, review, and any
  human-decision cases.
- Update `docs/plans/programs/codex-config/LEDGER.md` and
  `docs/plans/programs/codex-config/CURRENT.md` after execution closes.
- Update `CHANGELOG.md` only if installed skill behavior changed and was not
  already recorded.

Allowed files/areas:
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/`
- `CHANGELOG.md` only if needed for meaningful workflow or behavior changes

Non-goals:
- Do not select a successor batch.
- Do not mark deferred deletion candidates closed.
- Do not paste long logs or raw audit dumps into the ledger.

Acceptance criteria:
- CCFG-11 closes only if focused deletion-test evidence, validation, review,
  and closeout evidence exist.
- The ledger records deferred candidates or human-decision cases compactly.
- Current state returns to no selected, queued, or active batch after closeout
  unless a separate explicit request selects another batch.
- Closeout distinguishes "deletion performed" from "keep/narrow/defer with
  evidence."

Validation:
- Use the selected docs-only profile plus:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless this slice changes tests.

Commit message:
- `Close CCFG-11 deletion-test evidence`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep closeout compact and evidence-linked.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 closeout consistency and ledger/current-state accuracy.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if implementation evidence is incomplete.
- Stop if closeout would hide deferred candidates or mark untested deletion
  decisions as closed.

## Final Validation

Run:
- `python -m pytest tests/test_codex_features_manifest.py -q`
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- `python -m pytest tests/test_skill_deletion_surfaces.py -q`
- `./install.sh --dry-run` when metadata changed
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `git diff --check`

Before final report:
- Verify CCFG-11 closeout evidence exists.
- Verify `CURRENT.md` and `LEDGER.md` agree on selected, queued, and active
  state.
- Verify deferred deletion candidates remain visible.

## Stop Conditions

- Stop if the batch would delete, demote, rename, or uninstall a command-owner
  skill without explicit approval and focused test evidence.
- Stop if evidence shows the surface is a human contract decision rather than a
  deletion-safe no-op.
- Stop if the work broadens into general skill catalog cleanup, steering
  vocabulary, or frontmatter-shortening work covered by CCFG-6, CCFG-9, or
  CCFG-10.
- Stop if any change introduces downstream project-specific values into generic
  skills or tests.
- Stop if current-state diagnostics report multiple active artifacts or a
  queued/active mismatch.

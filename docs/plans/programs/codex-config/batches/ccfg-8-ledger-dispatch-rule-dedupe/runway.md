# Ledger Dispatch Rule Dedupe Runway

## Purpose

Reduce facade-like skill layering and duplicated routing rules across the
ledger-driven command-owner and runtime/support skills without changing runtime
behavior.

This spec executes the `ccfg-8-ledger-dispatch-rule-dedupe` batch described by
`docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/dispatch.md`.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/dispatch.md`.
- Included finding: CCFG-8.
- Target surfaces:
  `skills/add-to-ledger/SKILL.md`, `skills/plan-batch/SKILL.md`,
  `skills/work-batch/SKILL.md`,
  `skills/architecture-program-runway/SKILL.md`,
  `skills/batch-runway/SKILL.md`, `skills/planning-state/SKILL.md`,
  `skills/planning-artifacts/SKILL.md`,
  `docs/skill-routing-contract.md`, and `docs/workflow-guide.md`.
- `planning-artifacts`, `planning-state`, and existing consumer routing already
  address part of the overlap. This batch should consolidate remaining repeated
  ledger, dispatch, selected/queued/active, closeout, and external-source rules.
- Current intended ownership:
  command-owner skills own human-facing routing decisions and stop points;
  runtime/support skills own procedures and mechanics.

## Assumptions

- This is a skill-maintainability batch, not a behavior migration.
- Replacing repeated prose with references is safe only after the executing
  worker names the repeated rule and its single owner.
- `docs/skill-routing-contract.md` is the best cross-surface reference for
  command-owner versus runtime/support routing ownership.
- `skills/planning-state/SKILL.md` owns diagnostic ordering, target-policy
  checks, and projection routing.
- `skills/planning-artifacts/SKILL.md` owns Planning Artifact Layout v1
  placement, naming, active-state file shape, batch directory shape, and state
  vocabulary.
- `skills/architecture-program-runway/SKILL.md` owns program ledger, selected
  dispatch, batch queue, program `CURRENT.md`, and closeout reconciliation
  mechanics.
- `skills/batch-runway/SKILL.md` owns concrete runway spec mechanics and
  execution orchestration.
- `add-to-ledger`, `plan-batch`, and `work-batch` must retain the minimum
  caller-visible rules needed for direct human invocation.

## Rule Ownership Map

| Repeated rule category | Single owner | Caller-visible boundary preserved outside the owner |
|---|---|---|
| Command routing and human-facing stop points | `docs/skill-routing-contract.md` | Command-owner skills (`add-to-ledger`, `plan-batch`, and `work-batch`) express the contract for their human-facing routes; runtime/support skills stay behind the selected route. |
| Ledger and external-source intake | `add-to-ledger` | `plan-batch` consumes existing ledger state and stops when fresh work needs ingestion. |
| Planning State Diagnostic ordering, target-policy checks, and projection routing | `planning-state` | Consumers carry forward compact diagnostic facts instead of reimplementing pickup logic. |
| Planning Artifact Layout v1 placement, naming, active-state shape, and archive vocabulary | `planning-artifacts` | Consumers reference layout rules when interpreting or writing planning artifacts. |
| Program dispatch, selected/queued/active batch artifact state, program queue mechanics, and finding lifecycle status | `architecture-program-runway` | Command-owner skills select the user-facing workflow; `batch-runway` consumes one selected dispatch. |
| Concrete runway spec, slice ledger, validation/review loop, completed-slice archive, and commit receipt mechanics | `batch-runway` | Program ledgers and selected dispatch state remain owned by `architecture-program-runway`. |
| Same-batch closeout reconciliation mechanics | `architecture-program-runway` | `work-batch` routes to closeout only after concrete execution evidence exists and stops before successor selection. |

## Non-Goals

- Do not implement any slice during spec creation.
- Do not touch CCFG-1 runner extraction work.
- Do not select or implement CCFG-2 through CCFG-5.
- Do not implement Go runner work.
- Do not create a new command-owner skill.
- Do not rewrite all skills.
- Do not change runtime behavior.
- Do not reconcile current program data unless this batch itself creates
  closeout state.
- Do not delete necessary direct-command guidance from command-owner skills.
- Do not move layout rules out of `planning-artifacts`.
- Do not move operational diagnostics or projection routing out of
  `planning-state`.
- Do not move program queue mechanics out of `architecture-program-runway`.
- Do not move concrete execution mechanics out of `batch-runway`.

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
- Use `lean-runway` density because this batch is focused skill-maintainability,
  documentation-contract, and regression-test work.
- Workers must not write durable JSON planning state, SQLite projections,
  runner artifacts, or downstream project planning roots.
- Workers must preserve command-owner human-facing routing while reducing
  repeated procedure/mechanics prose.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- For ownership-boundary tests touched by this batch:
  `python -m pytest tests/test_skill_routing_rule_ownership.py -q`
- For Batch Runway create-spec output contract guardrails when this spec is
  touched:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- For manifest checks when `codex-features.json` or direct skill metadata
  changes:
  `python -m pytest tests/test_codex_features_manifest.py -q`
- For planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For hard-coding checks, the final diff should not introduce matches:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/add-to-ledger skills/plan-batch skills/work-batch skills/architecture-program-runway skills/batch-runway skills/planning-state skills/planning-artifacts docs/skill-routing-contract.md docs/workflow-guide.md tests`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No runner extraction, Go runner, SQLite database, or JSON planning-state file
  is required.

Harness output:
- Existing `current` and `validate` checks should not write live planning
  files.
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
- Treat the CCFG-8 dispatch, this spec, and queued-state updates as the active
  planning state for this batch.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| None | complete | pending coordinator commit | final validation passed | clean coordinator review | none | CCFG-8 closeout ready; no successor selection. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Inventory duplicated rules and owners | fc2b307 | Added exact-owner rule map and focused ownership-boundary tests; review fix tightened single-owner table parsing and selected/queued/active artifact-state coverage. | Validation: `python -m pytest tests/test_skill_routing_rule_ownership.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`. Review: clean after fix loop with `test_quality_delta`. |
| 2. Deduplicate command-owner routing prose | 93b30e4 | Trimmed duplicated procedure/mechanics prose in `add-to-ledger`, `plan-batch`, and `work-batch` while preserving direct command contracts and stop points. | Validation: `python -m pytest tests/test_skill_routing_rule_ownership.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`. Review: pass with `contract_change` and `docs_only_change`. |
| 3. Deduplicate runtime/support mechanics prose | ac6c714 | Shortened duplicated support-skill mechanics prose in `architecture-program-runway`, `batch-runway`, and `planning-artifacts` by referencing the owning support skills while preserving procedure ownership. | Validation: `python -m pytest tests/test_skill_routing_rule_ownership.py -q`; `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`. Review: pass with `contract_change`, `validation_or_reporting_change`, and `docs_only_change`. |
| 4. Align cross-doc references and closeout state | pending coordinator commit | Aligned `docs/skill-routing-contract.md` and `docs/workflow-guide.md` with the final owner split; added CCFG-8 closeout evidence; returned program state to no selected, queued, or active batch. | Validation: `python -m pytest tests/test_skill_routing_rule_ownership.py -q`; `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`; hard-coding scan introduced no matches. Review: clean with `contract_change`, `validation_or_reporting_change`, and `docs_only_change`. |

## Slice 1. Inventory Duplicated Rules And Owners

Scope:
- Build a compact ownership map for repeated rules across the target surfaces.
- Cover ledger-source, external-source, selected/queued/active, dispatch,
  closeout, Planning Artifact Layout v1, Planning State Diagnostic, and batch
  queue/state vocabulary rules.
- Add or adjust focused tests that can protect the ownership map before prose is
  reduced.

Allowed files/areas:
- `tests/test_skill_routing_rule_ownership.py`
- `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/runway.md`
- `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/completed-slices.md` if the executor chooses to keep a separate archive

Non-goals:
- Do not rewrite skill prose in this slice except for tiny fixes required by a
  failing ownership test.
- Do not test exact full Markdown snapshots.
- Do not add runtime behavior tests.

Acceptance criteria:
- The ownership map names one owner for each repeated rule category:
  command routing, ledger/external-source intake, Planning State Diagnostic,
  Planning Artifact Layout v1 placement, program dispatch/queue mechanics,
  concrete runway mechanics, and same-batch closeout reconciliation.
- Tests fail if command-owner skills no longer own human-facing routing
  decisions.
- Tests fail if support/runtime skills no longer own procedures and mechanics.
- Tests distinguish finding lifecycle status from batch artifact state.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_skill_routing_rule_ownership.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required if this slice adds or changes tests. Review should focus on whether
  the assertions protect ownership boundaries instead of brittle incidental
  wording.

Commit message:
- `Inventory skill routing rule owners`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Prefer small text-contract tests and a compact owner map over broad rewrites.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, ownership-map usefulness, and test quality.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the owner map requires a new command-owner skill.
- Stop if no single owner can be assigned for a repeated rule without changing
  behavior.

## Slice 2. Deduplicate Command-Owner Routing Prose

Scope:
- Reduce duplicated procedure/mechanics prose in `add-to-ledger`, `plan-batch`,
  and `work-batch` where the ownership map shows a support/runtime owner.
- Keep concise human-facing routing decisions, accepted inputs, outputs, and
  stop points in each command-owner skill.
- Replace safe duplicates with references to `docs/skill-routing-contract.md`,
  `planning-state`, `planning-artifacts`, `architecture-program-runway`, or
  `batch-runway` as appropriate.

Allowed files/areas:
- `skills/add-to-ledger/SKILL.md`
- `skills/plan-batch/SKILL.md`
- `skills/work-batch/SKILL.md`
- `docs/skill-routing-contract.md` only for short reference adjustments
- Focused tests from Slice 1
- This spec active-ledger/archive rows

Non-goals:
- Do not remove command-owner skill identity or direct-invocation guidance.
- Do not make command-owner skills depend on archived APR/PST ledgers.
- Do not move mechanics into command-owner skills to make them self-contained.

Acceptance criteria:
- `add-to-ledger` still owns ledger-intake user intent and never selects or
  executes a batch.
- `plan-batch` still owns existing-ledger selection, selected/queued/active
  handling, one-spec output, and stop-before-implementation behavior.
- `work-batch` still owns execution intent for the current queued or active
  runway and same-batch closeout reconciliation, but not successor selection.
- Duplicated mechanics prose is shortened where a referenced owner already
  states the rule.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_skill_routing_rule_ownership.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required if tests change. Review should check that command-owner behavior is
  protected without freezing incidental prose.

Commit message:
- `Deduplicate command-owner routing rules`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Preserve direct-command behavior and stop points.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, command-owner preservation, and behavior-neutral
  wording.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if a command-owner skill would become only an opaque alias with no
  caller-visible decision contract.
- Stop if reducing prose would hide a stop condition from direct human
  invocation.

## Slice 3. Deduplicate Runtime/Support Mechanics Prose

Scope:
- Reduce duplicated routing and state-mechanics prose in
  `architecture-program-runway`, `batch-runway`, `planning-state`, and
  `planning-artifacts` where another support skill is the owner.
- Keep runtime/support procedures and mechanics in their owner skill.
- Use short references where safe instead of restating full command-owner or
  sibling-support contracts.

Allowed files/areas:
- `skills/architecture-program-runway/SKILL.md`
- `skills/batch-runway/SKILL.md`
- `skills/planning-state/SKILL.md`
- `skills/planning-artifacts/SKILL.md`
- `docs/skill-routing-contract.md` only for short reference adjustments
- Focused tests from Slice 1
- This spec active-ledger/archive rows

Non-goals:
- Do not change Batch Runway execution delegation, commit, review, validation,
  or ledger-retention semantics.
- Do not change Planning State CLI behavior.
- Do not change Planning Artifact Layout v1 placement semantics.
- Do not change Architecture Program Runway grouping, dispatch, queue, or
  closeout responsibilities.

Acceptance criteria:
- `planning-state` remains the operational owner for current/validate,
  diagnostic ordering, target-policy checks, and projection routing.
- `planning-artifacts` remains the owner for artifact placement, naming, active
  state file shape, batch directories, archives, and state vocabulary.
- `architecture-program-runway` remains the owner for program selection,
  grouping, queue state, selected dispatch packets, and program closeout
  reconciliation.
- `batch-runway` remains the owner for concrete spec creation and execution
  orchestration.
- Repeated command-owner rules in support skills are references rather than
  duplicate decision tables where safe.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_skill_routing_rule_ownership.py -q`
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required if tests change. Review should check support ownership and avoid
  brittle exact wording.

Commit message:
- `Deduplicate support skill mechanics rules`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Preserve runtime behavior and mechanics ownership.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, runtime/support ownership preservation, and
  behavior-neutral wording.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if support prose cannot be shortened without removing an executable
  procedure future workers need.
- Stop if the change would require `planning-state` to decide semantic pickup
  or `planning-artifacts` to own operational validation.

## Slice 4. Align Cross-Docs And Closeout State

Scope:
- Align `docs/skill-routing-contract.md` and `docs/workflow-guide.md` with the
  final owner map after slices 2 and 3.
- Update focused tests if doc references changed.
- Produce closeout evidence and reconcile only this CCFG-8 batch's program
  state.

Allowed files/areas:
- `docs/skill-routing-contract.md`
- `docs/workflow-guide.md`
- Focused tests touched by earlier slices
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/completed-slices.md`
- This spec active-ledger/archive rows

Non-goals:
- Do not select, dispatch, refresh, create, or prepare successor work.
- Do not close CCFG-6, CCFG-9, CCFG-10, or CCFG-11.
- Do not archive or rewrite historical APR/PST ledgers.

Acceptance criteria:
- Cross-docs name the owner split without duplicating long rules from every
  skill.
- Closeout states whether runtime behavior changed; expected answer is no.
- Program `CURRENT.md` and `LEDGER.md` return to no selected, queued, or active
  batch after closeout.
- `planning_state.py current --root docs/plans` and
  `planning_state.py validate --root docs/plans` pass.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_skill_routing_rule_ownership.py -q`
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python -m pytest tests/test_codex_features_manifest.py -q` if feature metadata changed
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required if tests change in this slice.

Commit message:
- `Close ledger dispatch rule dedupe`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Reconcile only this completed batch and do not select successor work.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, final doc alignment, closeout accuracy, and clean
  idle state.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if closeout would need to select successor work.
- Stop if final evidence suggests runtime behavior changed.

## Final Validation

Run:
- `python -m pytest tests/test_skill_routing_rule_ownership.py -q`
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- `python -m pytest tests/test_codex_features_manifest.py -q` if feature
  metadata changed
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/add-to-ledger skills/plan-batch skills/work-batch skills/architecture-program-runway skills/batch-runway skills/planning-state skills/planning-artifacts docs/skill-routing-contract.md docs/workflow-guide.md tests`
- `git diff --check`

## Stop Conditions

- Stop if the work would touch CCFG-1 runner extraction or select CCFG-2 through
  CCFG-5.
- Stop if the work would implement Go runner work.
- Stop if the work would create a new command-owner skill.
- Stop if the work would rewrite all skills instead of reducing duplicated
  rules in the named target surfaces.
- Stop if the work would change runtime behavior.
- Stop if owner assignment requires a user decision.
- Stop if same-batch closeout reconciliation would become successor selection.

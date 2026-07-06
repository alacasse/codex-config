# Batch Runway Create-Spec Output Contract Runway

## Purpose

Fix the Batch Runway create-spec output contract so session-local planning mode
is not written into durable execution-contract `Overrides`. The batch should
make the reusable skill guidance explicit, add regression coverage for the
contract, and deliberately handle affected active/future runway artifacts
without changing planning-state command behavior.

This spec executes the
`batch-runway-create-spec-output-contract` batch described by
`docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/dispatch.md`.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/dispatch.md`.
- Included finding: PST-18.
- Excluded finding: PST-19; Pending lifecycle modeling remains a separate
  candidate batch.
- The observed failure pattern is durable runway specs whose execution
  `Overrides` include session-mode claims about the spec-creation task;
  those lines describe the artifact creation session, not an execution-contract
  deviation.
- `skills/batch-runway/references/create-spec.md` currently includes an
  `Overrides` template but does not say that `Overrides` is only for durable
  execution deviations.

## Assumptions

- Batch Runway owns runway structure and create-spec output guidance.
- Planning-state commands should continue to report selected, queued, and active
  artifacts without learning Batch Runway mode semantics.
- Closed historical runway specs may remain as historical evidence when a
  bounded scan proves they are not active or future templates.
- Workflow doc edits are repo-owned behavior changes; update `CHANGELOG.md` and
  `codex-features.json` if the Batch Runway skill behavior surface changes.

## Non-Goals

- Do not modify `scripts/planning_state.py`.
- Do not implement PST-19 or define a durable `Pending` finding status.
- Do not rewrite the full Batch Runway execution contract.
- Do not update GitHub issues or comments.
- Do not introduce downstream project-specific paths, validation commands,
  cache paths, or local overlays into generic skill guidance or tests.

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
- Use `lean-runway` density because this batch is focused workflow-contract and
  regression-test work.
- Workers must not write durable JSON planning state, SQLite projections, or
  downstream project planning roots.
- Closed historical runway specs may be left unchanged only with an explicit
  scan result and rationale recorded in the completed slice archive or
  closeout.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- For the new contract regression surface:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- For manifest or feature dependency checks, if touched:
  `python -m pytest tests/test_codex_features_manifest.py -q`
- For planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For the bounded active/future runway scan:
  `rg -n "Treat this .*create[-]spec|implementation starts in a[ ]later" docs/plans/programs/*/CURRENT.md docs/plans/programs/*/batches/*/runway.md skills/batch-runway`
- For hard-coding checks, the final diff should not introduce matches:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/batch-runway tests/test_batch_runway_create_spec_contract.py docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No SQLite database or JSON planning-state file is required.

Harness output:
- Existing `current` and `validate` checks should write no live planning files.
- No generated summary artifact is required.

Index refresh:
- None required for this repo after these workflow-doc, test, and planning-doc
  edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.
- Do not write to downstream project planning roots.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1. Tighten create-spec override guidance | Closed | this commit | `current`/`validate` passed with existing redirect warnings only; `git diff --check` passed; contract test is intentionally added in Slice 2 | `runway_reviewer` clean | Contract regression test fails before it passes | Create-spec guidance now keeps session-local mode and artifact-creation history out of durable execution `Overrides` and names baseline, assumptions, purpose, handoff notes, or active-state prose as the correct location. |
| 2. Add regression and metadata alignment | Pending |  |  |  | Active/future runway scan is bounded |  |
| 3. Audit affected runways and close PST-18 | Pending |  |  |  | Final validation and closeout evidence are complete |  |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Tighten create-spec override guidance | this commit | Batch Runway create-spec guidance now limits durable `Overrides` to future execution-contract deviations and directs session-local create-spec context to non-override prose. | Validation: `python scripts/planning_state.py current --root docs/plans`, `python scripts/planning_state.py validate --root docs/plans`, `git diff --check`; review: clean `runway_reviewer` result against the Slice 1 diff. |

## Slice 1. Tighten Create-Spec Override Guidance

Scope:
- Update Batch Runway create-spec guidance so `Overrides` is explicitly limited
  to durable execution-contract deviations.
- Tell agents to place session mode, artifact creation history, and
  "implementation starts later" notes in baseline, handoff, or active-state
  prose instead of execution `Overrides`.
- Keep create-spec mode available as task context; only forbid it as a durable
  execution-contract override.

Allowed files/areas:
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/create-spec.md`
- `skills/batch-runway/references/execution-contract-v1.md` only if needed for
  a pointer, not a contract rewrite
- This spec active-ledger/archive rows

Non-goals:
- Do not change Batch Runway execution delegation, review, commit, or closeout
  rules.
- Do not change Architecture Program Runner phase semantics.
- Do not edit planning-state command code.

Acceptance criteria:
- Create-spec guidance states that `Overrides` contains only durable execution
  deviations.
- Create-spec guidance explicitly forbids session-local mode claims such as
  "treat this session as create-spec" in durable `Overrides`.
- The guidance gives a correct alternative location for create-spec session
  context.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q` if the
  test exists in this slice; otherwise record why it starts in Slice 2.
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless new tests are added in this slice.

Commit message:
- `Tighten batch runway create-spec overrides`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, durable override wording, and absence of
  planning-state command changes or project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the change implies create-spec mode is forbidden in all runway prose
  rather than only in durable execution `Overrides`.
- Stop if the change requires planning-state diagnostics to classify Batch
  Runway modes.

## Slice 2. Add Regression And Metadata Alignment

Scope:
- Add focused tests that protect the durable override contract for Batch Runway
  create-spec guidance and this queued/future runway.
- Update `CHANGELOG.md` and `codex-features.json` if Slice 1 changed the
  installed Batch Runway behavior surface.
- Keep tests text-oriented and targeted; do not create broad Markdown snapshot
  tests.

Allowed files/areas:
- `tests/test_batch_runway_create_spec_contract.py`
- `tests/test_codex_features_manifest.py` only if metadata assertions need a
  focused extension
- `codex-features.json`
- `CHANGELOG.md`
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/create-spec.md`
- This spec active-ledger/archive rows

Non-goals:
- Do not test closed historical runway specs as if they were active templates.
- Do not add generated output, SQLite files, or JSON planning-state fixtures.
- Do not make tests depend on downstream project paths.

Acceptance criteria:
- Regression tests fail if Batch Runway create-spec guidance allows
  session-local mode claims in durable `Overrides`.
- Regression tests check that the queued/future PST-18 runway itself does not
  contain the forbidden pattern in its `Overrides`.
- Metadata and changelog are aligned if the installed workflow behavior changes.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python -m pytest tests/test_codex_features_manifest.py -q` if metadata is
  touched
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Request test-quality review only if tests become broad, assertion-light, or
  fixture-heavy.

Commit message:
- `Test batch runway create-spec override contract`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, assertion strength, metadata/changelog alignment,
  and absence of brittle whole-file snapshots.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if tests would require generated planning-state files or a SQLite
  projection.
- Stop if the only possible test is a brittle full-runway snapshot.

## Slice 3. Audit Affected Runways And Close PST-18

Scope:
- Run a bounded scan for session-local create-spec claims in active/future
  runway specs and Batch Runway templates.
- Patch any active/future runway or reusable template that still violates the
  durable override contract.
- Leave closed historical runways unchanged only with an explicit rationale in
  closeout evidence; otherwise patch them deliberately and document why.
- Update the program ledger, program `CURRENT.md`, completed-slice archive, and
  closeout so PST-18 closes and the queue clears without selecting PST-19.

Allowed files/areas:
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/`
- Active/future `runway.md` files only when the scan proves they are not closed
  historical evidence
- Reusable Batch Runway templates or references under `skills/batch-runway/`
- This spec active-ledger/archive rows

Non-goals:
- Do not implement PST-19 or queue the next batch.
- Do not rewrite closed historical specs for cosmetic consistency without a
  reusable-template or active/future rationale.
- Do not update GitHub issues or comments.

Acceptance criteria:
- Bounded scan results identify whether remaining matches are closed historical
  artifacts, active/future artifacts, or reusable guidance.
- No active/future runway or Batch Runway reusable guidance stores session-local
  create-spec mode in durable `Overrides`.
- PST-18 closeout points to validation, review, regression tests, scan results,
  and any intentionally retained historical residue.
- Program `CURRENT.md` and `LEDGER.md` clear the queued batch after closeout and
  leave PST-19 as the next candidate.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python -m pytest tests/test_codex_features_manifest.py -q` if metadata was
  touched
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `rg -n "Treat this .*create[-]spec|implementation starts in a[ ]later" docs/plans/programs/*/CURRENT.md docs/plans/programs/*/batches/*/runway.md skills/batch-runway`
  `git diff --check`

Test quality review:
- None unless Slice 2 review requested it and the closeout must record the
  result.

Commit message:
- `Close batch runway create-spec override contract`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, closeout evidence, bounded scan interpretation,
  ledger/CURRENT queue cleanup, and preservation of PST-19 scope.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if scan results imply a non-historical active runway outside this batch
  is affected and its ownership is unclear.
- Stop if closing PST-18 would require defining or enforcing Pending status.

## Final Validation

Before final closeout, run:
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- `python -m pytest tests/test_codex_features_manifest.py -q` if manifest or
  feature metadata changed
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- bounded active/future runway scan from the validation profile
- `git diff --check`

Record clean review evidence and pointer-first validation evidence in
`closeout.md`.

## Stop Conditions

- Stop if work would move create-spec mode semantics into planning-state
  diagnostics or JSON state.
- Stop if work would redefine the whole Batch Runway execution contract instead
  of tightening create-spec output guidance.
- Stop if work would implement PST-19 or use Pending as a durable finding state.
- Stop if work would add project-specific paths, validation commands, or local
  overlays to reusable Batch Runway guidance.
- Stop if unrelated dirty files conflict with the allowed slice scope.

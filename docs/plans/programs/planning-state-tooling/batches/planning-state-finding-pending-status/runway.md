# Planning-State Finding Pending Status Runway

## Purpose

Define a `Pending` finding lifecycle status for architecture-program ledgers so
findings that are already controlled by selected, queued, or active batch
artifacts are not treated like raw `Open` intake. The batch should update
reusable workflow guidance, add focused regression coverage, and reconcile the
planning-state-tooling program ledger with pointer-first closeout evidence.

This spec executes the `planning-state-finding-pending-status` batch described
by
`docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/dispatch.md`.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/dispatch.md`.
- Included finding: PST-19.
- Latest completed planning-state-tooling batch:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/`.
- Architecture Program Runway currently defines `Open` as not yet assigned and
  `In runway` as active concrete spec coverage, but it does not define a
  cut-but-not-closed state for selected or queued batch artifacts.
- Planning State commands report selected, queued, and active artifacts; they do
  not own source-ledger finding lifecycle semantics.

## Assumptions

- Architecture Program Runway owns program finding statuses, source-ledger
  update rules, selected dispatch packets, and closeout reconciliation.
- Batch Runway owns concrete slice execution and should consume the selected
  dispatch/runway without widening source finding scope.
- Planning State should continue to provide active-state diagnostics without
  becoming the owner of Architecture Program Runway finding vocabulary.
- Workflow skill edits are repo-owned behavior changes; update `CHANGELOG.md`
  and `codex-features.json` if the reusable skill behavior surface changes.

## Non-Goals

- Do not modify `scripts/planning_state.py` unless a focused test proves the
  tool already consumes finding lifecycle statuses and needs the new value.
- Do not redefine batch artifact states such as selected, queued, active, and
  completed.
- Do not reopen PST-18 or change closed historical runway artifacts.
- Do not update GitHub issues or comments.
- Do not introduce downstream project-specific paths, validation commands,
  cache paths, or local overlays into generic skills.

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
- Use `lean-runway` density because this batch is focused workflow-vocabulary,
  docs-as-code, and ledger closeout work.
- Workers must not write durable JSON planning state, SQLite projections, or
  downstream project planning roots.
- Workers must keep finding lifecycle status separate from batch artifact
  state.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- For Architecture Program Runway status-vocabulary regression coverage:
  `python -m pytest tests/test_architecture_program_runway_status_vocabulary.py -q`
- For manifest or feature dependency checks, if touched:
  `python -m pytest tests/test_codex_features_manifest.py -q`
- For planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For Pending-status wording:
  `rg -n "Pending|selected, queued, or active|amendment|follow-up" skills/architecture-program-runway docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status tests/test_architecture_program_runway_status_vocabulary.py`
- For hard-coding checks, the final diff should not introduce matches:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/architecture-program-runway tests/test_architecture_program_runway_status_vocabulary.py docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status`
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
| 1. Define Pending finding vocabulary | Completed | `1fcc65c` | `pytest ...status_vocabulary.py -q` 2 passed; `current`; `validate`; `git diff --check` | Clean review | Pending is documented as a finding lifecycle status, not a batch artifact state. |
| 2. Protect Pending update rules | Completed | `39f0eb5` | `pytest ...status_vocabulary.py -q` 3 passed; manifest test 6 passed; `current`; `validate`; `git diff --check` | Clean review | Tests and guidance prevent silent source-ledger scope edits for Pending findings. |
| 3. Reconcile ledger and close PST-19 | Completed | this commit | `current`; `validate`; `git diff --check` | Clean review | PST-19 is closed with pointer-first closeout evidence. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Define Pending finding vocabulary | `1fcc65c` | Added `Pending` to Architecture Program Runway finding lifecycle guidance and template, with focused vocabulary coverage. | `skills/architecture-program-runway/SKILL.md`; `skills/architecture-program-runway/references/program-ledger-template.md`; `tests/test_architecture_program_runway_status_vocabulary.py` |
| 2. Protect Pending update rules | `39f0eb5` | Added explicit Pending scope-change rules, regression coverage, changelog entry, and architecture-program-runway feature version bump. | `skills/architecture-program-runway/SKILL.md`; `skills/architecture-program-runway/references/program-ledger-template.md`; `tests/test_architecture_program_runway_status_vocabulary.py`; `CHANGELOG.md`; `codex-features.json` |
| 3. Reconcile ledger and close PST-19 | this commit | Reconciled program current state, closed PST-19, completed the batch queue row, and added pointer-first closeout evidence. | `docs/plans/programs/planning-state-tooling/CURRENT.md`; `docs/plans/programs/planning-state-tooling/LEDGER.md`; `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/closeout.md`; `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/completed-slices.md` |

## Slice 1. Define Pending Finding Vocabulary

Scope:
- Update Architecture Program Runway finding lifecycle guidance so `Pending`
  means a finding is controlled by selected, queued, or active batch artifacts
  and is not raw `Open` intake.
- Update the reusable program-ledger template to include `Pending` where it
  describes finding statuses.
- Keep batch queue statuses separate from finding lifecycle statuses.

Allowed files/areas:
- `skills/architecture-program-runway/SKILL.md`
- `skills/architecture-program-runway/references/program-ledger-template.md`
- `tests/test_architecture_program_runway_status_vocabulary.py`
- This spec active-ledger/archive rows

Non-goals:
- Do not change `scripts/planning_state.py`.
- Do not change Batch Runway execution contracts.
- Do not use Pending as a batch queue status.

Acceptance criteria:
- `Open` is defined as a real finding not yet assigned to selected, queued, or
  active batch artifacts.
- `Pending` is defined as cut or active batch work controlled by batch
  artifacts until closeout, amendment, supersession, split, abandonment, or
  follow-up.
- Reusable guidance distinguishes finding lifecycle status from batch artifact
  state.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_architecture_program_runway_status_vocabulary.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless the new test becomes broad, fixture-heavy, or assertion-light.

Commit message:
- `Define pending architecture findings`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, the status-vocabulary boundary, and absence of
  planning-state command changes or project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the wording makes Planning State commands responsible for finding
  lifecycle semantics.
- Stop if Pending is described as a batch queue status rather than a finding
  status.

## Slice 2. Protect Pending Update Rules

Scope:
- Add or extend focused tests that assert Pending guidance forbids silent
  source-ledger scope edits once a finding is controlled by batch artifacts.
- Update Architecture Program Runway selection, dispatch, or closeout guidance
  so amendments and follow-up findings are explicit when Pending scope changes.
- Update `CHANGELOG.md` and `codex-features.json` if Slice 1 changed the
  installed Architecture Program Runway behavior surface.

Allowed files/areas:
- `skills/architecture-program-runway/SKILL.md`
- `skills/architecture-program-runway/references/program-ledger-template.md`
- `tests/test_architecture_program_runway_status_vocabulary.py`
- `tests/test_codex_features_manifest.py` only if metadata assertions need a
  focused extension
- `codex-features.json`
- `CHANGELOG.md`
- This spec active-ledger/archive rows

Non-goals:
- Do not create a new planning-state storage policy.
- Do not make projection reports select or close Pending findings.
- Do not hide amendments in narrative notes; they must be explicit.

Acceptance criteria:
- Guidance says Pending findings should not be widened or rewritten through
  ordinary source-ledger edits.
- Allowed changes are explicit: closeout evidence, supersession, abandonment,
  split, named amendment, or a new follow-up finding.
- Regression tests protect the Pending scope-change rule.
- Metadata and changelog are aligned if installed skill behavior changes.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_architecture_program_runway_status_vocabulary.py -q`
  `python -m pytest tests/test_codex_features_manifest.py -q` if metadata is
  touched
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless the tests become broad, assertion-light, or tightly coupled to
  historical planning files.

Commit message:
- `Protect pending finding updates`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, the amendment/follow-up rule, metadata alignment,
  and project-neutral reusable guidance.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the guidance would allow a Pending finding to change scope without an
  explicit amendment or follow-up.
- Stop if tests rely on downstream project paths or old historical runways.

## Slice 3. Reconcile Ledger And Close PST-19

Scope:
- Reconcile the planning-state-tooling `CURRENT.md` and `LEDGER.md` after
  Slices 1-2 land.
- Add `closeout.md` and fill `completed-slices.md` with pointer-first evidence.
- Mark PST-19 closed only after vocabulary, tests, validation, review, and
  metadata evidence are complete.

Allowed files/areas:
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/closeout.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/completed-slices.md`
- This spec active-ledger/archive rows

Non-goals:
- Do not select the next planning-state-tooling batch during closeout.
- Do not rewrite older completed batch artifacts except to add bounded evidence
  pointers if required by validation.
- Do not update GitHub issues.

Acceptance criteria:
- PST-19 is closed with `Covered by` pointing at this batch and compact evidence.
- The batch queue row is completed with dispatch, runway, closeout, and
  completed-slice pointers.
- Program `CURRENT.md` clears selected dispatch, active runway, and queued batch
  after closeout.
- Final diagnostics pass with only pre-existing redirect warnings.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_architecture_program_runway_status_vocabulary.py -q`
  `python -m pytest tests/test_codex_features_manifest.py -q` if metadata was
  touched
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless closeout adds or changes tests.

Commit message:
- `Close planning-state pending status batch`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, closeout evidence, active-state shape, and absence
  of unrelated planning edits.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if PST-19 cannot be closed without missing test, validation, review, or
  metadata evidence.
- Stop if closeout would leave selected dispatch, active runway, and queued
  batch populated together.

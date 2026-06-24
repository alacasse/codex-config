---
name: batch-runway
description: Create and execute multi-slice runway specs with per-slice scope, validation, ledger updates, commits, and mandatory coding/review subagent delegation. Use when the user asks to create a batch runway spec, execute a runway spec, streamline sequential slices, work from project-local plans, commit after each slice, reduce long-running context use, or keep the main agent as coordinator only while subagents implement and review.
---

# Batch Runway

Use this skill for a controlled sequence of small, independently committable
slices. Keep the main agent as coordinator; delegate implementation and review.

## Modes

- `create-spec`: write one runway spec for a future execution session. Do not
  implement code.
- `execute-spec`: execute an existing runway spec one slice at a time.

Infer the mode when the user does not name one:

- "create", "spec", "plan", "next runway", or "upcoming work" means
  `create-spec`.
- "execute", "run", "implement", "work through", or a specific spec path means
  `execute-spec`.

## Density

- `lean-runway`: token-efficient. Specs reference standard contracts,
  validation profiles, and compact subagent briefs.
- `full-runway`: maximum explicitness. Specs may include full contracts, full
  commands, and full subagent briefs.

Default to `lean-runway` for mechanical refactors, test topology splits, import
cleanup, docs-local planning, compatibility facade cleanup, and
behavior-preserving module moves.

Default to `full-runway` only when compact references would be unsafe: production
behavior changes, installer lifecycle changes, YAML schema changes, sandbox
execution behavior, public CLI behavior, risky migrations, ambiguous ownership
boundaries, or unreliable subagent file access.

Prefer lean specs plus explicit risk overrides before pasting whole contracts.

## Progressive Disclosure

Read only the reference files needed for the current mode. Do not load every
reference file by default.

- `references/project-values.md`: read before creating or executing a spec.
- `references/execution-contract-v1.md`: read when creating a new spec, executing
  a spec that references v1, or preparing a subagent contract capsule.
- `references/reporting-contracts-v1.md`: read before requesting worker,
  reviewer, commit-receipt, convergence, or ledger-update output.
- `references/ledger-retention-v1.md`: read before creating a new ledger or
  updating ledger/archive state.
- `references/validation-profiles.md`: read when selecting or applying a
  validation profile.
- `references/create-spec.md`: read only in `create-spec` mode.
- `references/execute-spec.md`: read only in `execute-spec` mode.
- `references/subagent-briefs.md`: read before spawning coding or review
  subagents.
- `references/test-quality-review.md`: read only when a slice explicitly asks for
  test quality review.

When a subagent receives only a spec path, make sure the spec contains enough
contract detail for that subagent to act safely, or include a short contract
capsule and the relevant Batch Runway reference path in the subagent prompt.

## Required First Steps

1. Read applicable project instructions and local overlays.
2. Resolve project-specific values from repository instructions, local overlays,
   the active spec, or explicit user direction. See
   `references/project-values.md`.
3. Check the worktree and preserve unrelated dirty files.
4. Choose `create-spec` or `execute-spec`.
5. Choose `lean-runway` or `full-runway`.

Stop instead of guessing when a required project value, validation command,
harness command, output path, summary artifact, planning location, or
instruction priority order is missing.

## Core Contract

Use Batch Runway Standard Execution Contract v1 unless the spec explicitly
overrides it.

Non-negotiable execution rules:

- The main agent is coordinator only.
- The main agent must not implement code changes directly except for updating
  the ledger and making commits.
- Each slice implementation must be delegated to a coding subagent.
- Each completed slice must be reviewed by a separate review subagent before
  commit.
- Use `runway_worker` for coding subagents and `runway_reviewer` for review
  subagents when available.
- If required subagent tooling or custom agents are unavailable, stop and report
  that execution cannot proceed under this workflow.
- Do not fall back to main-agent implementation.
- Commit after each clean, focused slice.
- Preserve unrelated dirty files.
- Do not revert or commit files outside the slice scope.
- Continue to the next pending slice after a commit receipt unless the user
  explicitly asks to stop or a stop condition remains active.
- After an interruption, approval, permission issue, context transition, or
  clarification, resume the same runway at the next incomplete ledger row.

## Context Discipline

Keep live orchestration context small enough for long batches.

- Prefer lean specs and compact subagent briefs when they preserve safety.
- Do not paste full slice text into subagent prompts unless the subagent cannot
  reliably read the spec, the boundary is subtle, or the work is high risk.
- Do not retain implementation chronology, command transcripts, repeated
  clean-review prose, repetitive validation detail, or repeated explanations of
  already-closed slices.
- Use compact YAML for routine worker results, reviewer results, commit
  receipts, convergence, and ledger updates.
- Move completed slice details out of the active ledger and into the completed
  slice archive.
- Store detailed commands, logs, transcripts, and generated reports in commits
  or artifacts, then reference them.

## Create-Spec Summary

In `create-spec` mode:

1. Read `references/create-spec.md`.
2. Read the current goal, existing local plans, recent commits, current ledger
   state, and last completed task enough to identify the next related work.
3. Write one local plan file in the project planning location.
4. Pick 3-5 tightly related slices that can execute sequentially.
5. Keep each slice independently testable and committable.
6. Stop before coding.

## Execute-Spec Summary

In `execute-spec` mode:

1. Read `references/execute-spec.md`.
2. Read the full active spec and required reference files named by the spec.
3. Identify the active validation profile, pending ledger rows, stop conditions,
   commit strategy, density mode, convergence state, active ledger rows, and
   completed slice archive.
4. Execute from the next incomplete ledger row.
5. For each slice: spawn coding subagent, validate, spawn separate review
   subagent, fix in-scope issues through subagents, commit, report receipt,
   update ledger/archive, close subagents, continue.
6. After the last slice, run final validation and project-required index refresh,
   then report commits, validation, skipped slices, remaining risks, and expanded
   convergence.

## Stop Conditions

Stop on scope drift, unresolved ambiguity, repeatedly unresolved validation
failure, dirty-file conflict, missing subagent support, missing project values,
or a stop condition from the active spec.

Do not say work is almost done or completion is forecastable unless remaining
work is bounded, known, explicitly enumerated, and supported by the latest
convergence evidence.

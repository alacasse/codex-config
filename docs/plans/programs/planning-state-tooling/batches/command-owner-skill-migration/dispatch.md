# Command Owner Skill Migration Dispatch

```yaml
batch_id: command-owner-skill-migration
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
decision_record: docs/adr/0002-human-facing-command-owner-skills.md
included_findings:
  - id: PST-26
    title: Human-facing workflow commands are hidden behind opaque runtime skill names
  - id: PST-27
    title: In-place renaming would disrupt active workflow skills
  - id: PST-28
    title: Command-owner skills need narrow support-skill boundaries
  - id: PST-29
    title: Legacy and test-quality concerns need agent-facing placement
goal: Create the first copy-first migration batch for human-facing command-owner skills: add-to-ledger, plan-batch, and work-batch.
owner_seam: Command-owner skills own direct user workflow intent; agent-facing support skills own narrow reusable diagnostics, layout, state, review, or evidence lenses.
validation_class: Skill validation, manifest/dependency checks, focused wording tests, planning-state current/validate diagnostics, and git diff --check.
guardrails:
  - Do not remove or rename existing runtime skills in this first migration batch.
  - Do not create permanent thin wrappers that preserve confusing historical names as the real architecture.
  - Do not expose legacy cleanup as a normal human-facing command.
  - Do not make test-quality review a primary human command; it is a review support skill that remains directly requestable.
  - Do not hard-code downstream project paths, validation commands, cache locations, issue policy, or planning roots.
dependencies_satisfied:
  - ADR 0002 records the command-owner decision.
  - Planning-state diagnostics pass for docs/plans.
dependencies_blocking:
  - None.
suggested_slices:
  - Add command-owner skill surfaces beside existing runtime skills.
  - Tighten agent-facing support skill boundaries for test review and legacy prevention.
  - Reconcile catalog, metadata, validation, changelog, and migration notes.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/runway.md
```

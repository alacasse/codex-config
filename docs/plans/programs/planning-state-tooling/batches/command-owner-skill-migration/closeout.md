# Command Owner Skill Migration Closeout

## Status

- Batch: `command-owner-skill-migration`
- Status: completed
- Findings closed: PST-26, PST-27, PST-28, PST-29
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/runway.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/completed-slices.md`

## Evidence Pointers

- Slice 1 commit: `fdaf2cf` (`Add command-owner skill surfaces`)
- Slice 2 commit: `43118fc` (`Clarify support skill boundaries`)
- Slice 3 commit: `0e45abe` (`Reconcile command skill migration`)
- Slice 1 validation: `python -m pytest tests/test_codex_features_manifest.py -q`;
  `current`; `validate`; `git diff --check`
- Slice 2 validation: focused support-boundary wording tests; `current`;
  `validate`; `git diff --check`
- Slice 3 validation: `python -m pytest tests/test_codex_features_manifest.py -q`;
  `current`; `validate`; `git diff --check`

## Outcome

- `add-to-ledger`, `plan-batch`, `work-batch`, and `port-by-contract` are the
  documented direct user-facing command set.
- Existing runtime names such as `architecture-program-runway` and
  `batch-runway` remain installed as agent-facing support dependencies behind
  command-owner skills, not as the preferred direct user interface.
- Planning-state, planning-artifacts, test-quality review, dead-surface audit,
  and legacy-removal are documented as narrow agent-facing support or workflow
  obligations.
- `README.md`, `CHANGELOG.md`, `codex-features.json`, `CURRENT.md`, and
  `LEDGER.md` are aligned for closeout.

## Cleanup Residue

- Existing runtime skills were not removed, renamed, or archived because active
  workflows still depend on their contracts. Their metadata and UI prompts are
  demoted to agent-facing support rather than direct command recommendations.
  Full removal would require moving or replacing their execution and
  program-ledger contracts behind the command-owner skills.
- No durable JSON planning state was written.
- No durable SQLite projection was written.
- No runner artifacts, generated-doc refresh, downstream planning roots, or
  installed `~/.codex` paths were changed.
- No successor planning-state-tooling batch was selected.

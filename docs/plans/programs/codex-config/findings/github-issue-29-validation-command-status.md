# GitHub Issue 29: Validation Command Status Classification

## Source

- GitHub issue: https://github.com/alacasse/codex-config/issues/29
- Title: CCFG root cause 1: classify validation command status before required runway validation
- State when ingested: open
- Created: 2026-07-09
- Source identity: GitHub issue #29, authored by `alacasse`

## Summary

Batch Runway `create-spec` can promote validation commands into required
runway validation without recording whether each command is currently green,
known-red, expected to be created by a slice, conditional, or diagnostic-only.

The issue was visible in the previously queued CCFG-11 planning state, now
displaced by the CCFG-13 prerequisite batch:

- `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/runway.md`
  lists `python -m pytest tests/test_codex_features_manifest.py -q` as focused
  validation even though the current command is known-red.
- The same runway lists
  `python -m pytest tests/test_skill_deletion_surfaces.py -q` before that test
  file exists.
- `skills/batch-runway/references/create-spec.md` tells create-spec agents to
  choose validation profiles and focused overrides, but does not require a
  command status class before a command becomes an execution gate.
- `tests/test_batch_runway_create_spec_contract.py` covers create-spec routing,
  session-mode override hygiene, hot-path reference loading, and
  project-neutrality, but has no contract coverage for validation command status
  classes.

## Local Evidence

Read-only planning-state diagnostics passed:

- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`

Focused issue checks:

- `python -m pytest tests/test_codex_features_manifest.py -q` currently fails
  with 3 failures, so it is not a current required-green baseline.
- `python -m pytest tests/test_skill_deletion_surfaces.py -q` exits with
  `ERROR: file or directory not found`, so it is an implementation-created
  future test at best.
- `tests/test_skill_deletion_surfaces.py` is absent.

## Recommended Ledger Finding

Add one new codex-config ledger finding for a Batch Runway create-spec contract
fix. Keep it separate from CCFG-11: CCFG-11 is the skill deletion-test batch;
this finding is the root-cause guard that should prevent future generated
runways from repeating the same ambiguous validation gate.

Suggested finding title:

`CCFG-13. Validation command status classification`

Suggested source:

`GitHub issue #29; docs/plans/programs/codex-config/findings/github-issue-29-validation-command-status.md`

Suggested next action:

Add durable create-spec guidance and tests requiring every generated validation
command to declare one of these status classes before execution:
`required-green`, `known-red-baseline`, `implementation-created`,
`conditional`, or `diagnostic-only`.

## Acceptance Criteria To Preserve

- `batch-runway` create-spec guidance requires each validation command to
  declare a status class.
- Required-green commands must have a current passing result or an explicit
  slice-owned remediation path.
- Missing future-created tests cannot be listed as required-green validation.
- Known-red commands cannot be silently promoted to required-green validation.
- Contract tests cover known-red rejection, implementation-created tests tied to
  a named creating slice, and conditional validation with trigger conditions.

## Non-Goals

- Do not fix CCFG-11 by removing one failing command only.
- Do not weaken validation globally.
- Do not execute the displaced CCFG-11 runway until this root cause is handled
  or explicitly superseded.

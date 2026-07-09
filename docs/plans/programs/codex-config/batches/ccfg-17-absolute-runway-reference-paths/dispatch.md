# CCFG-17 Dispatch: Absolute Runway Reference Paths

## Batch Identity

- Batch ID: `ccfg-17-absolute-runway-reference-paths`
- Program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding:
  `CCFG-17. Absolute runway reference paths`
- Source finding note:
  `docs/plans/programs/codex-config/findings/github-issue-32-absolute-runway-reference-paths.md`
- Expected runway spec:
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/runway.md`

## Selection Decision

Select CCFG-17 as the next bounded batch.

CCFG-17 is the most precise open root-cause item in the canonical ledger. It
has one owner seam, `batch-runway` create-spec guidance, and focused regression
coverage. It also avoids the mixed deletion-test scope in CCFG-11 until the
existing CCFG-13 through CCFG-16 guards are applied in a separate future
planning pass.

## Scope

- Batch kind: `mixed-risk`
- Owner seam: `batch-runway` create-spec reference-path contract for generated
  runway artifacts.
- Validation class: focused contract tests and active-artifact guard tests.
- Risk class: mostly `migration`; Slice 1 is `contract-narrowing` because it
  narrows generated runway guidance away from local absolute repo-owned skill
  references while preserving allowed absolute runtime handoff values.
- Approval gate for Slice 1: CCFG-17 source issue and ledger row authorize this
  generated-artifact contract narrowing; execution must preserve explicit
  absolute-path allowances for user-provided local values, project-specific
  paths, subagent spec paths, repository cwd handoffs, and runtime values that
  are not reusable repo-owned skill references.

## Covered Work

- Update `skills/batch-runway/references/create-spec.md` so generated runway
  reference examples use repo-relative or skill-relative paths for repo-owned
  skill references.
- Document the narrow absolute-path allowance for local project values and
  runtime handoffs that should stay absolute.
- Add focused tests preventing create-spec guidance from requiring absolute
  repo-owned skill reference paths.
- Add a scoped active-artifact guard that catches newly selected, queued, or
  active runways containing the local codex-config skill-path prefix named in
  the source finding.
- Update release metadata and changelog for the Batch Runway guidance change.

## Deferred Or Excluded

- Do not bulk-rewrite completed or archived historical runways.
- Do not treat the displaced CCFG-11 runway as active work.
- Do not ban legitimate absolute paths in subagent prompts, user-provided local
  values, repository cwd handoffs, or project-specific runtime values.
- Do not change Batch Runway execution mechanics beyond generated reference
  path guidance and focused tests.
- Do not select CCFG-6, CCFG-9, CCFG-10, CCFG-11, or runner extraction work.

## Dependencies

- Satisfied: CCFG-13 validation-command status classification.
- Satisfied: CCFG-14 batch-kind and slice-risk gates.
- Satisfied: CCFG-15 vague-row split/block/narrow guard.
- Satisfied: CCFG-16 deletion-test vocabulary owner and generated-artifact
  consumer rules.
- Blocking: none.

## Suggested Slice Shape

1. Narrow create-spec reference-path guidance for repo-owned skill references,
   while preserving explicit absolute-path allowances for runtime handoffs.
2. Add focused create-spec contract tests for repo-relative or skill-relative
   generated Batch Runway references.
3. Add a scoped active-runway artifact guard that ignores completed and
   archived historical evidence.
4. Align Batch Runway release metadata, changelog, and final validation.

## Stop Conditions

- Stop if execution would rewrite completed or archived historical runways.
- Stop if execution would ban absolute paths needed for subagent prompts,
  repository cwd handoffs, explicit user-provided local values, or
  project-specific runtime values.
- Stop if a test would scan all historical runways and fail on closed evidence
  instead of only selected, queued, or active generated runway artifacts.
- Stop if the guidance cannot stay project-neutral.

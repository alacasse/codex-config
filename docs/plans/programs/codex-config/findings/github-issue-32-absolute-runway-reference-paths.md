# GitHub Issue 32: Absolute Runway Reference Paths

## Source

- GitHub issue: https://github.com/alacasse/codex-config/issues/32
- Title: CCFG root cause 4: stop emitting local absolute paths in generated
  runways
- State when ingested: open
- Created: 2026-07-09
- Source identity: GitHub issue #32, authored by `alacasse`

## Summary

Batch Runway generated runway artifacts can embed local absolute paths for
repo-owned skill references, such as
`/home/alacasse/projects/codex-config/skills/batch-runway/...`.

The immediate source is not only an old generated artifact. Current
`batch-runway` create-spec guidance still tells lean specs to list reference
files using `<absolute path to batch-runway>/references/...`, so new generated
runways can repeat the same local-machine path shape.

## Evidence

- `skills/batch-runway/references/create-spec.md` currently instructs generated
  lean specs to reference files with `<absolute path to batch-runway>`.
- Completed non-archived runways under
  `docs/plans/programs/codex-config/batches/` still contain
  `/home/alacasse/projects/codex-config/skills/batch-runway/...` references,
  including CCFG-1, CCFG-7, CCFG-8, CCFG-11, CCFG-12, CCFG-13, CCFG-14, and
  CCFG-15.
- The latest completed CCFG-16 runway already uses repo-relative
  `skills/batch-runway/...` reference paths, which is the desired generated
  shape for repo-owned references.

## Analysis

This belongs in the codex-config skill-cleanup ledger as a Batch Runway
create-spec contract issue. The reusable workflow rule should prefer
repo-relative or skill-relative references for repo-owned skill files and allow
absolute paths only when a project-specific instruction or runtime handoff
actually requires a local absolute value.

The fix should target the generator contract and regression coverage, not a
bulk rewrite of old planning evidence. Existing completed runways prove the
symptom and can stay as historical evidence unless a later cleanup batch
explicitly selects them.

## Proposed Plan

1. Update `skills/batch-runway/references/create-spec.md` so generated runway
   examples use repo-relative or skill-relative paths for repo-owned Batch
   Runway references.
2. Clarify the rare allowed absolute-path cases: user-provided local values,
   project-specific paths, subagent prompts that need an absolute spec path, or
   runtime handoff values that are not reusable repo-owned references.
3. Add focused tests in `tests/test_batch_runway_create_spec_contract.py` that
   prevent create-spec guidance from requiring absolute paths for reusable
   skill references.
4. Add a scoped artifact guard that prevents newly generated active
   `docs/plans/programs/**/batches/**/runway.md` artifacts from containing
   `/home/alacasse/projects/codex-config/skills/` references, without forcing
   churn across completed historical evidence.
5. Keep archived and completed historical runways as evidence unless a separate
   cleanup batch explicitly selects them.

## Acceptance Criteria To Preserve

- `batch-runway` create-spec guidance no longer asks generated runways to embed
  local absolute repo paths for reusable skill references.
- Generated active batch runways use repo-relative or skill-relative paths for
  repo-owned references.
- Tests prevent new active runway artifacts from containing
  `/home/alacasse/projects/codex-config/skills/` reference paths.
- Archived and historical runways are not rewritten as part of this fix unless
  a separate cleanup batch selects them.
- Any remaining absolute-path allowance is documented and scoped to
  project-specific values or runtime handoffs, not generic skill references.

## Non-Goals

- Do not only replace paths in the displaced CCFG-11 runway.
- Do not bulk rewrite completed runways or archived historical artifacts as
  part of the root-cause fix.
- Do not add broad path bans that reject legitimate user-provided absolute
  paths outside generated planning artifacts.
- Do not change Batch Runway execution behavior beyond generated reference path
  guidance and focused regression coverage.

# CCFG-16 Dispatch: Deletion-Test Vocabulary Ownership

## Batch Identity

- Batch ID: `ccfg-16-deletion-test-vocabulary-ownership`
- Program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding:
  `CCFG-16. Deletion-test vocabulary ownership`
- Source finding note:
  `docs/plans/programs/codex-config/findings/github-issue-31-deletion-test-vocabulary-ownership.md`
- Expected runway spec:
  `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/runway.md`

## Selection Decision

Select CCFG-16 as the next bounded batch.

CCFG-16 is a precise prerequisite for future CCFG-11 replanning: it defines who
owns deletion-test evidence vocabulary and how generated dispatch/runway
artifacts may consume that vocabulary. This avoids regenerating CCFG-11 with
ambiguous labels such as `no-op`, `sediment`, `obsolete skill surface`, or
`deletion-safe evidence`.

## Scope

- Batch kind: `decision`
- Owner seam: `dead-surface-audit` owns deletion-test evidence vocabulary;
  `legacy-removal`, `architecture-program-runway`, and `batch-runway` consume
  canonical evidence terms without redefining them.
- Validation class: skill/reference wording plus focused regression tests.
- Risk class: `decision-only`; this batch records ownership and generated
  artifact rules. It does not delete, demote, narrow, migrate, or clean up any
  skill surface.

## Covered Work

- Define the canonical deletion-test evidence vocabulary owner.
- Align consumer boundaries across `legacy-removal`,
  `architecture-program-runway`, and `batch-runway`.
- Require generated dispatch/runway artifacts to use canonical terms or locally
  define non-canonical evidence labels.
- Add focused regression coverage for CCFG-11-like generated text so unsupported
  deletion categories cannot be silently invented.

## Deferred Or Excluded

- CCFG-11 deletion-test audit and cleanup remains open and must be regenerated,
  split, blocked, or narrowed by a future explicit `plan-batch` request.
- No destructive cleanup, deletion, migration, demotion, or contract narrowing
  is included.
- Do not make `dead-surface-audit` the batch/program owner; it is the evidence
  vocabulary owner only.
- Do not create a new project-specific downstream planning convention.

## Dependencies

- Satisfied: CCFG-13 validation-command status classification.
- Satisfied: CCFG-14 batch-kind and slice-risk gates.
- Satisfied: CCFG-15 vague-row split/block/narrow guard.
- Blocking: none for this decision batch.

## Suggested Slice Shape

1. Define canonical deletion-test evidence vocabulary in `dead-surface-audit`
   and test that it remains the owner.
2. Align `legacy-removal` as a consumer/decision owner without redefining
   deletion-test evidence categories.
3. Align `architecture-program-runway` selected-dispatch guidance and
   `batch-runway` create-spec guidance so generated artifacts use canonical
   evidence terms or define local non-canonical labels.
4. Add CCFG-11-like regression coverage that rejects unsupported generated
   deletion categories and preserves future CCFG-11 replanning safety.

## Stop Conditions

- Stop if execution would delete, demote, narrow, migrate, or clean up skill
  surfaces instead of defining vocabulary ownership.
- Stop if execution would replan or execute CCFG-11 in this batch.
- Stop if execution would make `dead-surface-audit` own program queue state,
  selected dispatch packets, concrete runways, commits, or closeout records.
- Stop if the owner seam cannot be expressed project-neutrally in reusable
  skill guidance.

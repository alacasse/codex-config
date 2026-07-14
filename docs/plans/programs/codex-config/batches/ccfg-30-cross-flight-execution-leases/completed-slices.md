# CCFG-30 Completed Slices

## Startup Reconciliation

```yaml
startup_reconciliation:
  queued_runway: docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/runway.md
  planning_stable_revision: 7220a2e78a7ad50550cd7bc7ffcfd328301d8e7f
  accepted_live_stable_revision: 61871e6abf269f0e0e53f5a47db9a9cc242318ac
  implementation_topology: ordinary-single-root
  candidate_read_only_revision: 3e54155964e92d3a4dced8268cc683baaab9be1c
  classification: expected-queue-establishment
  reviewed_range: 7220a2e78a7ad50550cd7bc7ffcfd328301d8e7f..61871e6abf269f0e0e53f5a47db9a9cc242318ac
  changed_path_basis:
    - docs/plans/programs/codex-config/CURRENT.md
    - docs/plans/programs/codex-config/LEDGER.md
    - docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/dispatch.md
    - docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/runway.md
  planning_state_current: passed
  planning_state_validate: passed
```

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Helper refresh preparation | `d8f39528197d64a39d31b3ff6f141a60be23ef8b` | Success; 27 tests and 32 subtests passed; Ruff and basedpyright passed; delta-only test-quality and final review clean | `git show --stat d8f39528197d64a39d31b3ff6f141a60be23ef8b`; `git show d8f39528197d64a39d31b3ff6f141a60be23ef8b` |
| 2. Planning snapshot contract | `387e108d3c944a4146843145adfb445eb6f19cc5` | Success; 7 lifecycle tests and 2 subtests passed; focused manifest and Ruff passed; delta-only test-quality and final review clean | `git show --stat 387e108d3c944a4146843145adfb445eb6f19cc5`; `git show 387e108d3c944a4146843145adfb445eb6f19cc5` |
| 3. Startup reconciliation and live leases | `a5a464bc81dee85c543208b81790cbbb3002fe96` | Success after test-review fix loop; 11 lifecycle tests and 29 subtests plus 27 helper tests and 32 subtests passed; Ruff, delta-only test-quality, and final review clean | `git show --stat a5a464bc81dee85c543208b81790cbbb3002fe96`; `git show a5a464bc81dee85c543208b81790cbbb3002fe96` |
| 4. Integrated routing and linked metadata | `afbe95f910c257fa7486759c1e6b91138e8c88e4` | Success after two test-review fix loops; joined manifest 3 tests and 164 subtests plus 38 lifecycle/helper tests and 61 subtests passed; linked checks, delta-only test-quality, and final review clean | `git show --stat afbe95f910c257fa7486759c1e6b91138e8c88e4`; `git show afbe95f910c257fa7486759c1e6b91138e8c88e4` |
| 3R. Uncommitted queue-artifact startup case | `7917ace241f57ae6e5b5dc4e65e7cfa0548588d8` | Success; final-range finding closed; 12 lifecycle tests and 29 subtests plus helper and focused manifest checks passed; delta-only test-quality and fix review clean | `git show --stat 7917ace241f57ae6e5b5dc4e65e7cfa0548588d8`; `git show 7917ace241f57ae6e5b5dc4e65e7cfa0548588d8` |

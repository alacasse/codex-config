# CCFG-34 Completed Slices

## Slice 1: Install The Minimal Temporary Dogfooding Policy

- Status: completed.
- Commit: `ba1e941` (`docs: add minimal stable runway dogfooding policy`).
- Files: root `AGENTS.md`, `CHANGELOG.md`,
  `notes/stable-runway-dogfooding-policy.md`, and
  `tests/test_stable_runway_dogfooding_policy.py`.
- Amendment: final review of the first attempt proved `.codex/AGENTS.md` was not
  automatically discovered from the repository root. A bounded amendment
  substituted root `AGENTS.md` only and received a clean independent planning
  review at dispatch blob `7b43871b6a04317af15d8af3f540130aa5cc50f7`
  and runway blob `5d2e978e8798ed3347bf8acfa4dc7429929e5624`.
- Validation: focused pytest passed 5 tests and 43 subtests; Ruff and exact-range
  whitespace validation passed. Install status and dry-run remained diagnostic
  only and wrote no runtime state.
- Reviews: delta-only test-quality review and final independent implementation
  review were clean with no residual risks or required fixes.
- Cleanup: the uncommitted `.codex/AGENTS.md` policy hook was removed before the
  implementation commit. No runner, generic skill, agent contract, feature
  metadata, candidate code, or runtime state changed.
- Temporary residue: root `AGENTS.md`, the policy, and the focused test remain
  intentionally until CCFG-29 proves permanent #59, #60, and #61 behavior plus
  equivalent planning, execution, escalation, and no-successor scenarios.
- Outcome: stable CCFG-26 through CCFG-29 planning and execution now load one
  repository-local temporary policy without adding runner architecture.

# CCFG-26 Slice-Shape Policy Post-Closeout Correction

- Date: 2026-07-18
- GitHub issue: [#66](https://github.com/alacasse/codex-config/issues/66)
- Original closeout: `closeout.md`
- Candidate baseline: `8a9331947ffc8b0b28b8c75ecf6fc60f8b3c2fcd`
- Corrected candidate commit: `5c5ec9d52dd9033daa45f3a200031c152363b62c`

## Defect And Correction

The original implementation resolved, schema-validated, transported,
deterministically checked, and persisted the project YAML slice-shape policy.
Those gates proved that a final runway was admissible under the policy. They did
not prove that reusable planning instructions had stopped applying the older
universal vertical preference. The planner still preferred vertical slices and
the reviewer still rejected horizontal decomposition when a vertical
alternative existed, independently of the configured default.

The corrected candidate makes the resolved policy substitutive rather than
additive. Planner, reviewer, and the reusable `plan-batch` command contract now
name it as the sole slice-shape preference authority. Generic semantic
boundaries, independently useful results, proportionality, focused validation,
advisory sizing, and filler rejection remain shape-neutral. The runway schema
and public deterministic gate also make `migration_evidence` and
`migration_matrix` exclusive to exact `risk: migration` slices.

The semantic replacement below is review evidence, not a new persisted schema:

```yaml
semantic_replacement:
  old_rules:
    - reusable planner independently prefers vertical decomposition
    - reusable reviewer independently rejects horizontal decomposition when a vertical alternative exists
  new_authority:
    - resolved slice-shape policy supplied by plan-batch
  superseded_surfaces:
    - agents/batch_planner.toml
    - agents/batch_plan_reviewer.toml
  retained_overlays:
    - temporary stable master vertical policy through CCFG-29
  forbidden_residue:
    - any reusable prompt rule that chooses a shape independently of the policy
    - any hidden vertical or horizontal fallback
  counterfactual:
    - horizontal configured default with overrides disabled
```

Prompt-contract tests prove that the installed reusable instructions no longer
contain the known competing authority. They do not prove the exact reasoning or
natural-language output of a future model invocation. Deterministic tests
separately prove that `default_shape: horizontal`, `allow_override: false`, and
`require_override_reason: true` accept and persist a horizontal slice with a
null reason, and that no vertical alternative is required.

## Candidate Delta And Installed Versions

The candidate correction changes exactly 11 paths with 241 insertions and 36
deletions: the planner and reviewer agents, `plan-batch` skill and deterministic
gate, runway schema, three focused contract-test modules plus exact manifest
tests, feature manifest, and changelog. It adds no compatibility dialect,
resolver framework, command, execution owner, runner, bridge, or successor
surface.

Installed feature versions changed only as required:

- `planning-contracts`: 1.2.0 -> 1.3.0
- `plan-batch`: 2.2.0 -> 2.3.0
- `custom-agents`: 1.7.0 -> 1.8.0

## Validation And Review Evidence

- Focused command-owner group: 198 tests and 201 subtests passed in 123.38 s.
- Exact final correction assertions: 12 tests and 80 subtests passed in 1.85 s.
- Selected manifest boundary: 2 tests and 28 subtests passed in 0.23 s.
- Scenario catalog validation: all 82 scenarios valid in 0.25 s.
- Full manifest module: 21 tests and 218 subtests passed; its one failure was
  the unchanged declared later-CCFG-26 known-red assertion. The exact diagnostic
  reproduced only the same two declared failures in 0.24 s.
- Ruff passed over the exact changed Python and test files. BasedPyright reported
  zero errors and the five existing unresolved-source warnings for
  `scripts/plan_batch.py`. `git diff --check` passed.
- Delta-only test-quality review was clean after adding focused protection for
  all three reusable authority surfaces. Its four-file run reported 192 passing
  tests and the single unchanged manifest known-red failure.
- Fresh independent exact-diff implementation review was clean with no findings
  or required fixes. Its spot replay passed 8 tests and 18 subtests in 1.66 s.
- Fresh `/tmp` and isolated candidate-home installations converged with every
  post-install dry-run link `ok`. Stable-home status was unchanged before and
  after at SHA-256
  `c2e7cbb4855a4fe062ffd796330e084da80ac4f40ccf854161af320af4069464`.
- Exact-commit acceptance ran once in one evidence-pytest process and passed 25
  tests, 82 scenarios, 31 required contracts, and 17 families in 87.91 s. The
  acceptance-result SHA-256 is
  `953ff563620e05a21bd98503e161cfe51ee01f1ed9aeedec1d1e12cb9ac98855`;
  `report.json` is
  `d905bfd9f0ff2493e5f593d97e5fc60a2abf0943461e0711a1337f1aae0d806a`;
  `report.txt` is
  `4b784c812577a04c9d8679e7270de5aa14b2f2f94bdf78ee06540e60ae0ed23b`.

## Stable Boundary And Disposition

The original closeout and its historical hashes remain unchanged. Stable
master's project-local temporary vertical policy remains intentionally active
through CCFG-29; neither it nor `AGENTS.md` changed. Candidate planning
authority was not transferred to stable master. No CCFG-26B through CCFG-26E or
other successor was selected, prepared, dispatched, queued, refreshed, or
created.

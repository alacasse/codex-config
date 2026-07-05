# Planning-State Skill Interface Runway

## Purpose

Create a reusable `planning-state` skill that gives agents a compact, safe
interface for planning-state diagnostics and optional generated state/projection
work. The batch should reduce reconstruction from prior context before consumer
skills start depending on Planning State Diagnostic facts.

This spec executes the `planning-state-skill-interface` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/dispatch.md`.

## Current Baseline

- Baseline state: `python scripts/planning_state.py current --root docs/plans`
  and `python scripts/planning_state.py validate --root docs/plans` pass with
  only existing architecture-runner redirect warnings.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/dispatch.md`.
- Included findings: PST-9, PST-10, and PST-11.
- Existing layout seam: `skills/planning-artifacts/SKILL.md`.
- Existing command seam: `scripts/planning_state.py`.
- Existing focused tests: `tests/test_planning_state.py`,
  `tests/test_codex_features_manifest.py`, and `tests/test_codex_owner.py`.
- Existing commands can report current state, validate state, allocate batch
  paths, register artifacts, select/queue explicit state fixtures,
  validate/render bounded closeout evidence, bootstrap companion JSON state,
  rebuild optional SQLite projections, and report from projections.
- Latest completed closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/closeout.md`.

## Assumptions

- The new skill is operational guidance for agents. It should not replace
  `planning-artifacts` as the source of Layout v1 placement rules.
- The skill should explain command sequencing and target safety, not duplicate
  implementation details from `scripts/planning_state.py`.
- The skill should use progressive disclosure: `SKILL.md` covers the routine
  hot path, and references cover state fixtures, target policy, projections,
  closeout evidence, runner artifacts, and protocol details only when needed.
- `planning_state.py` remains the command/file boundary. Agents and future
  runners must not import private Python helpers, scrape historical filenames,
  or query SQLite directly.
- Generated-only state/projection proof output belongs in caller-provided temp
  paths such as `/tmp`, not committed repository files.
- Consumer rewiring belongs to the later `planning-state-consumer-integration`
  batch.

## Non-Goals

- Do not update `architecture-program-runway`, `batch-runway`, or
  `legacy-removal` to consume the new skill in this batch.
- Do not change Batch Runway execution semantics.
- Do not change `planning-artifacts` layout ownership except for small links or
  wording needed to point to the operational skill.
- Do not implement new planning-state command behavior unless a tiny validation
  hook is required to verify skill packaging.
- Do not create committed durable JSON state or SQLite projection files.
- Do not add project-specific downstream paths, cache paths, validation
  commands, issue policy, or local overlay details to the reusable skill.
- Do not update GitHub issues or comments.

## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about
suspicious coordinator or subagent-lifecycle behavior.
Use the expanded convergence template only when scope is expanding, significant
uncertainty exists, blockers are present, or final batch reporting is produced.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execute-slice-core-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execution-contract-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/reporting-contracts-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/ledger-retention-v1.md`

Overrides:
- Treat this session as `create-spec`; implementation starts in a later
  `execute-spec` session from the first pending active-ledger row.
- Use `full-runway` density because this batch creates a reusable skill
  interface that future workflow consumers will depend on.
- Workers must not update consumer skills in this batch.
- Workers must use temp paths for generated state/projection smoke checks.
- Workers must not write to downstream project planning roots.
- Workers must not create a committed durable JSON state file or SQLite
  database.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/project-harness-production.md`

Focused validation commands:
- For skill, manifest, and install metadata slices, run:
  `python -m pytest tests/test_codex_features_manifest.py tests/test_codex_owner.py -q`
- For planning-state command smoke, run:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For generated-only state/projection proof, use explicit temp targets:
  `python scripts/planning_state.py bootstrap-state --root docs/plans --state-file /tmp/planning-state-skill-interface-state.json`
  `python scripts/planning_state.py validate --root docs/plans --state-file /tmp/planning-state-skill-interface-state.json`
  `python scripts/planning_state.py rebuild-projection --root docs/plans --database /tmp/planning-state-skill-interface.sqlite --state-file /tmp/planning-state-skill-interface-state.json --program planning-state-tooling`
  `python scripts/planning_state.py report-projection --root docs/plans --database /tmp/planning-state-skill-interface.sqlite --state-file /tmp/planning-state-skill-interface-state.json --program planning-state-tooling --report pending-batches`
- Validate JSON syntax when manifest changes:
  `python -m json.tool codex-features.json`
- Run grep checks for generic-skill hard-coding, adapted to the final diff:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/planning-state codex-features.json`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No package install is required unless manifest/install behavior changes in a
  way that tests cannot cover.

Harness output:
- Existing `current`, `validate`, and `bootstrap-state` checks should write no
  live planning files.
- Generated proof state and projection files must be under `/tmp` or a test
  temp directory.

Summary artifact:
- No generated summary artifact is required. Report compact stdout/stderr
  signals from validation commands.

Index refresh:
- None required for this repo after these skill/docs/manifest edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.
- Do not write to downstream project planning roots.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Create planning-state skill entrypoint | this commit | Added `skills/planning-state/SKILL.md` with the read-only diagnostic hot path, command-boundary guardrails, Layout v1 delegation, policy refusal rules, and future reference pointers. | Validation: `current`, `validate`, hard-code grep, `git diff --check`; review: clean `runway_reviewer` result. |
| 2. Add state-fixture and target-policy references | this commit | Added focused references for JSON state fixtures, transition receipts, and policy-driven target selection across stdout, `/tmp`, generated-only, committed, ignored-local, external, and none policies. | Validation: temp `bootstrap-state`, temp `validate --state-file`, expected durable-policy refusal for generated-only `--require-project-policy all`, hard-code grep, `git diff --check`; review: clean `runway_reviewer` result. |
| 3. Add projection, closeout, and runner-artifact references | this commit | Added focused references for optional SQLite projection reports, pointer-first closeout evidence, optional runner artifact inputs, and cleanup-residue owner/removal-condition evidence. | Validation: temp projection rebuild, `pending-batches`, `batch-evidence`, hard-code grep, `git diff --check`; review: approved after cleanup-residue guidance fix. |
| 4. Wire install metadata and close findings | this commit | Registered `planning-state` in `codex-features.json`, added focused manifest and owner tests, closed PST-9 through PST-11, cleared queued program state, and wrote pointer-first closeout evidence. | Validation: manifest/owner tests, JSON syntax, `current`, `validate`, temp state/projection smokes, hard-code grep, `git diff --check`, closeout validation; review: clean implementation review before coordinator closeout edits. |

## Slice 1. Create Planning-State Skill Entrypoint

Scope:
- Add `skills/planning-state/SKILL.md`.
- Define the skill trigger and purpose around planning-state discovery,
  validation, state bootstrap, optional projection rebuild/reporting, closeout
  evidence, and target policy.
- Put the routine hot path in the entrypoint:
  read project instructions, resolve planning root, use `planning-artifacts`
  for Layout v1 placement, run `current`, run `validate`, inspect selected or
  queued state, and stop before durable writes when policy is missing or
  incompatible.
- Name `scripts/planning_state.py` command invocation as the integration
  boundary, not Python imports or SQL.
- Add progressive-disclosure pointers to reference files that later slices will
  create.

Allowed files/areas:
- `skills/planning-state/SKILL.md`
- Optional brief link wording in `skills/planning-artifacts/SKILL.md`
- This spec ledger/archive rows
- `CHANGELOG.md` if the user-facing workflow surface changes

Non-goals:
- Do not add the optional reference content yet except placeholder links needed
  by the entrypoint.
- Do not update consumer skills.
- Do not change `scripts/planning_state.py` behavior.
- Do not change install metadata yet unless tests require the skill to be
  manifest-visible before references exist.

Acceptance criteria:
- `SKILL.md` is complete enough for a fresh agent to run the safe read-only
  diagnostic sequence without reading historical plan prose.
- The entrypoint clearly delegates artifact placement to `planning-artifacts`.
- The entrypoint says durable JSON state and SQLite projection writes require
  explicit project policy or caller-provided temp proof targets.
- The entrypoint forbids importing `scripts.planning_state` internals, scraping
  historical filenames, and querying SQLite directly.
- The entrypoint does not contain downstream project paths, cache paths, or
  project-specific validation commands as generic defaults.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache" skills/planning-state` should produce no matches.
  `git diff --check`

Test quality review:
- None; this is a skill-doc slice.

Commit message:
- `Add planning state skill entrypoint`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, trigger clarity, progressive-disclosure shape,
  command-boundary safety, and absence of project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the entrypoint cannot be useful without embedding project-specific
  paths or commands.
- Stop if the skill would duplicate Layout v1 placement rules instead of
  referencing `planning-artifacts`.

## Slice 2. Add State-Fixture and Target-Policy References

Scope:
- Add focused references under `skills/planning-state/references/` for state
  fixtures and target-policy resolution.
- Cover when to use `bootstrap-state`, `validate --state-file`,
  `select-batch`, `queue-batch`, `register-artifact`, and
  `validate --require-project-policy`.
- Cover safe target selection for stdout, `/tmp`, generated-only, committed,
  ignored-local, external, and none policies.
- Update `SKILL.md` pointers so agents read these references only when they need
  state fixtures or durable/generated target decisions.

Allowed files/areas:
- `skills/planning-state/SKILL.md`
- `skills/planning-state/references/state-fixtures.md`
- `skills/planning-state/references/target-policy.md`
- Optional focused tests that validate reference links if a helper exists or is
  easy to add
- This spec ledger/archive rows
- `CHANGELOG.md` if the user-facing workflow surface changes

Non-goals:
- Do not add projection or closeout reference details yet.
- Do not update consumer skills.
- Do not choose durable state paths for any project.
- Do not create state fixture files outside test temp or `/tmp` smoke checks.

Acceptance criteria:
- State-fixture guidance distinguishes read-only diagnostics, explicit JSON
  state fixtures, transition receipts, and human-readable Markdown planning
  artifacts.
- Target-policy guidance tells agents when to write to stdout, when `/tmp` is a
  valid proof target, when to use a declared durable path, and when to stop.
- The references make clear that reusable workflow code must resolve project
  policy and must not bake in one repository's layout.
- The references are short enough to be loaded only when needed.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python scripts/planning_state.py bootstrap-state --root docs/plans --state-file /tmp/planning-state-skill-interface-state.json`
  `python scripts/planning_state.py validate --root docs/plans --state-file /tmp/planning-state-skill-interface-state.json`
  `python scripts/planning_state.py validate --root docs/plans --require-project-policy all`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache" skills/planning-state` should produce no matches.
  `git diff --check`

Test quality review:
- None unless new tests are added.

Commit message:
- `Document planning state fixture policy`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, policy refusal behavior, generated/temp target
  safety, and no project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if target guidance would require a universal durable state or projection
  path.
- Stop if generated-only policy is described as permission to commit generated
  artifacts.

## Slice 3. Add Projection, Closeout, and Runner-Artifact References

Scope:
- Add focused references for projection reporting, closeout evidence, and
  runner artifacts.
- Cover `rebuild-projection` and `report-projection` command sequencing,
  supported report names, stale/mismatched projection refusal, and the rule that
  agents consume report output rather than SQL.
- Cover `validate-closeout` and `render-closeout` as pointer-first evidence
  workflows, not transcript storage.
- Cover explicit runner artifact and manifest inputs as optional projection
  data that should not make ordinary planning reports require runner data.
- Update `SKILL.md` pointers so these references are loaded only when the task
  asks for projection reports, closeout evidence, or runner artifacts.

Allowed files/areas:
- `skills/planning-state/SKILL.md`
- `skills/planning-state/references/projection-reporting.md`
- `skills/planning-state/references/closeout-evidence.md`
- `skills/planning-state/references/runner-artifacts.md`
- Optional focused tests that validate reference links if a helper exists or is
  easy to add
- This spec ledger/archive rows
- `CHANGELOG.md` if the user-facing workflow surface changes

Non-goals:
- Do not expose SQL as an agent workflow.
- Do not make SQLite required for `current`, `validate`, `bootstrap-state`,
  transitions, or closeout validation.
- Do not change projection command behavior.
- Do not update consumer skills.

Acceptance criteria:
- Projection guidance explains explicit database targets, source identity
  validation, supported reports, and stale projection blockers.
- Closeout guidance keeps evidence pointer-first and bounded.
- Runner-artifact guidance makes runner data optional and explicit.
- The references do not include long logs, transcripts, project-specific
  downstream paths, or raw telemetry examples as reusable defaults.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python scripts/planning_state.py rebuild-projection --root docs/plans --database /tmp/planning-state-skill-interface.sqlite --state-file /tmp/planning-state-skill-interface-state.json --program planning-state-tooling`
  `python scripts/planning_state.py report-projection --root docs/plans --database /tmp/planning-state-skill-interface.sqlite --state-file /tmp/planning-state-skill-interface-state.json --program planning-state-tooling --report pending-batches`
  `python scripts/planning_state.py report-projection --root docs/plans --database /tmp/planning-state-skill-interface.sqlite --state-file /tmp/planning-state-skill-interface-state.json --program planning-state-tooling --batch-id planning-state-sqlite-projection --report batch-evidence`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache" skills/planning-state` should produce no matches.
  `git diff --check`

Test quality review:
- None unless new tests are added.

Commit message:
- `Document planning state reporting workflows`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, projection/reporting safety, bounded closeout
  evidence, optional runner-artifact handling, and absence of SQL-as-workflow
  guidance.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the reference would make SQLite canonical or required.
- Stop if closeout guidance embeds transcripts or long logs instead of compact
  evidence pointers.

## Slice 4. Wire Install Metadata and Close Findings

Scope:
- Add a `planning-state` feature to `codex-features.json` with links for
  `skills/planning-state` and `scripts/planning_state.py`.
- Add or update focused tests so manifest requirements and skill references are
  validated.
- Ensure install ownership checks can identify the new skill and script as
  repo-owned when linked.
- Update `README.md` only if needed to explain the new feature at the repo
  inventory level.
- Update `CHANGELOG.md` for the user-facing skill/interface addition.
- Update this program `LEDGER.md`, `CURRENT.md`, and batch closeout artifacts
  so PST-9, PST-10, and PST-11 close only after validation and review evidence
  exists.

Allowed files/areas:
- `codex-features.json`
- `tests/test_codex_features_manifest.py`
- `tests/test_codex_owner.py`
- `README.md`
- `CHANGELOG.md`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/closeout.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/completed-slices.md`
- This spec ledger/archive rows

Non-goals:
- Do not wire consumer features to require `planning-state`; that belongs to
  `planning-state-consumer-integration`.
- Do not install or mutate runtime `~/.codex` state as part of validation.
- Do not update GitHub issues or comments.

Acceptance criteria:
- `codex-features.json` has a valid `planning-state` feature with repo-owned
  links and an appropriate `planning-artifacts` dependency.
- Manifest and owner tests cover the new feature or continue to validate it
  through generic manifest tests.
- `CHANGELOG.md` records the user-facing workflow addition.
- `current`, `validate`, generated-only state/projection smoke, manifest JSON,
  manifest tests, owner tests, and `git diff --check` pass.
- The closeout is pointer-first and bounded.
- PST-9, PST-10, and PST-11 are marked closed only after the skill, references,
  install metadata, validation, review, and closeout evidence are present.
- `CURRENT.md` points to no selected, active, or queued batch after closeout.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_codex_features_manifest.py tests/test_codex_owner.py -q`
  `python -m json.tool codex-features.json`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `python scripts/planning_state.py bootstrap-state --root docs/plans --state-file /tmp/planning-state-skill-interface-state.json`
  `python scripts/planning_state.py validate --root docs/plans --state-file /tmp/planning-state-skill-interface-state.json`
  `python scripts/planning_state.py rebuild-projection --root docs/plans --database /tmp/planning-state-skill-interface.sqlite --state-file /tmp/planning-state-skill-interface-state.json --program planning-state-tooling`
  `python scripts/planning_state.py report-projection --root docs/plans --database /tmp/planning-state-skill-interface.sqlite --state-file /tmp/planning-state-skill-interface-state.json --program planning-state-tooling --report pending-batches`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache" skills/planning-state` should produce no matches.
  `git diff --check`

Test quality review:
- Apply test-quality review only if new manifest/owner tests introduce
  behavior-specific assertions beyond generic manifest validation.

Commit message:
- `Register planning state skill feature`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, install metadata, test coverage, closeout
  evidence, changelog alignment, and whether PST-9 through PST-11 are actually
  satisfied.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if installing or validating the feature requires mutating runtime
  `~/.codex`.
- Stop if consumer features must be rewired to make the new feature valid.
- Stop if closeout evidence is missing validation or review pointers.

## Final Validation

Run after the last slice before final closeout:

- `python -m pytest tests/test_codex_features_manifest.py tests/test_codex_owner.py -q`
- `python -m json.tool codex-features.json`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python scripts/planning_state.py bootstrap-state --root docs/plans --state-file /tmp/planning-state-skill-interface-state.json`
- `python scripts/planning_state.py validate --root docs/plans --state-file /tmp/planning-state-skill-interface-state.json`
- `python scripts/planning_state.py rebuild-projection --root docs/plans --database /tmp/planning-state-skill-interface.sqlite --state-file /tmp/planning-state-skill-interface-state.json --program planning-state-tooling`
- `python scripts/planning_state.py report-projection --root docs/plans --database /tmp/planning-state-skill-interface.sqlite --state-file /tmp/planning-state-skill-interface-state.json --program planning-state-tooling --report pending-batches`
- `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache" skills/planning-state` should produce no matches.
- `git diff --check`

Final report must include validation results, review evidence, commit hashes,
any skipped checks, cleanup residues, open follow-ups, and
`orchestration_anomalies`.

## Stop Conditions

- Stop if a slice needs consumer-skill rewiring before the shared skill exists.
- Stop if a generic skill instruction needs a downstream project path, cache
  path, validation command, issue policy, or local overlay as a reusable
  default.
- Stop if durable JSON state or SQLite projection targets cannot be resolved
  from project policy or explicit temp proof paths.
- Stop if implementation would make SQLite or JSON state canonical over
  Markdown planning artifacts.
- Stop if validation requires mutating runtime `~/.codex` or downstream project
  planning roots.
- Stop if subagent tooling is unavailable during execution.

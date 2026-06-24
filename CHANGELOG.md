# Changelog

## Unreleased

### Generic batch-runway project values

Problem: `batch-runway` carried Graphify-specific defaults for plan storage,
installer sandbox validation, summary artifacts, and graph refresh even though
the skill should be reusable across repositories.

Decision: replace those hard-coded defaults with a generic project-values gate.
Agents must resolve planning location, validation profiles, harness commands,
artifact paths, summary reads, index refreshes, commit rules, and dirty-file
constraints from the current repo's instructions, local overlays, the spec, or
explicit user direction. Missing required values now stop execution instead of
being guessed.

Expected effect: `batch-runway` remains portable while still preserving strict
per-project behavior when a repo defines the concrete values locally.

### Minimal test-quality review integration

Problem: `test-quality-review` should be usable inside `batch-runway` without
turning every slice review into a broader audit or adding automatic blocking,
issue creation, ledger state, ADR generation, or remediation planning.

Decision: add an optional per-slice `Test quality review: none | delta-only |
focused | full-audit` setting to `batch-runway`. Omitted settings default to
`none`; explicit requests invoke `$test-quality-review` in the requested mode
and include compact YAML findings in reviewer output. Add compact YAML output
guidance to `test-quality-review` for automation/reviewer use.

Expected effect: runway specs can opt into qualitative test review where useful
while preserving current execution behavior and keeping future disposition,
issue-tracking, full-audit, and ADR workflows out of the minimal integration.

### Test-quality-review skill

Problem: agents reviewing tests needed a reusable way to judge confidence from
behavioral protection, regression coverage, assertion strength, mocking quality,
fixture complexity, and test friction without reducing quality to coverage
percentages or tying the workflow to `batch-runway`.

Decision: add a standalone `test-quality-review` skill with delta-only,
focused, and full-audit modes, explicit finding criteria, design-signal
analysis, scope limits, and a fixed report format. Declare it as its own
repo-owned feature in `codex-features.json`.

Expected effect: future reviewers, architects, implementation agents, and
automation can evaluate test quality consistently while keeping findings
actionable and independent from multi-slice runway execution.

### Batch-runway compact reporting and retention

Problem: `batch-runway` needed convergence discipline, but routine slice
reports, commit receipts, ledger rows, and subagent responses could accumulate
too much narrative context across long multi-batch refactors.

Decision: replace routine full convergence reporting with a compact YAML
convergence block, add `Compact Report Contract v1` for workers, reviewers, and
commit receipts, add `Standard Ledger Retention v1`, and document explicit
information lifetime rules. The full convergence template is retained only for
expanding scope, significant uncertainty, blockers, or final batch reports.

Expected effect: future runway executions should preserve coordination quality,
audit references, and recovery points while carrying much less historical
implementation detail in orchestrator context.

### Batch-runway agent output limits

Problem: the `runway_worker` and `runway_reviewer` roles could satisfy their
tasks with human-readable prose, which made clean subagent reports larger than
the coordinator needed.

Decision: update both agent prompts to return structured YAML, forbid
implementation history and reasoning narrative, and cap clean worker/reviewer
reports at 12 and 10 lines respectively. Expanded output is reserved for
findings, blockers, failed validation, or escalation.

Expected effect: coding and review subagents remain bounded to their role while
the coordinator receives predictable, compact state for long-term retention.

### Lean batch-runway contracts

Problem: `batch-runway` specs repeated the full execution contract, validation
commands, and subagent briefs in every runway, increasing token use while still
needing strict coordinator-only, sandbox, and commit discipline.

Decision: add lean/full runway density modes, versioned standard contract and
ledger references, reusable validation profiles, compact subagent brief formats
with absolute spec paths, explicit fresh install-sandbox output guidance, and
move the skill UI metadata from the legacy root `openai.yaml` path to
`agents/openai.yaml`.

Expected effect: future runway specs can stay smaller for mechanical work while
preserving the agent behavior that matters: coordinator-only execution,
separate coding/review agents, per-slice commits, guarded sandbox validation,
stable interpretation of older contract references, and current skill metadata
layout.

### Declared vs installed Codex ownership

Problem: `scripts/codex_owner.py` treated any path matching a feature manifest
entry as owned by this repository, even when the runtime `~/.codex` path was a
standalone copy instead of the expected symlink.

Decision: split manifest declaration from active installation state. The owner
report now includes `manifest_owner`, `installed_owner`, `status`, and `reason`,
with non-linked targets classified as `missing`, `unlinked_copy`,
`wrong_symlink`, `conflict_file`, or `conflict_directory`.

Expected effect: agents no longer get a false signal that editing a copied
runtime path will update codex-config. They can see when a feature is declared
by this repository but not currently linked from `~/.codex`.

### Linked config ownership detection

Problem: repo-owned files can be edited through their installed `~/.codex`
symlink while the agent is working in another project, making it easy to miss
the codex-config changelog and git status expectations.

Decision: add `scripts/codex_owner.py` and global instructions for checking
whether a `~/.codex` path resolves to this repo. Repo-owned links now carry a
clear expectation to update `CHANGELOG.md` for meaningful workflow changes and
report this repo's git status.

Expected effect: agents can safely tune linked skills, agents, rules, and
instructions from any project while still treating the edit as codex-config
work.

### Vendor-owned Graphify skill

Problem: `graphify` is vendor-owned and should not be represented as a local
override in this repo's feature manifest.

Decision: remove the local `graphify` feature from `codex-features.json`; the
vendor installer remains responsible for `~/.codex/skills/graphify`.

Expected effect: this repository owns only its explicit linked features, while
vendor-owned skills can manage themselves in the final `~/.codex` directory.

### Versioned feature installer

Problem: `install.sh` was a set of hard-coded symlinks, which made it easy for
the live Codex layout to drift from the repository and hard to add new workflow
features deliberately.

Decision: add a manifest-driven installer. `codex-features.json` now defines
versioned Codex features and their links, while `install.sh` delegates to a
Python installer that supports listing, dry runs, selective installs, conflict
detection, and installed-version state.

Expected effect: new skills, agents, rules, and instruction bundles can be
versioned as features and installed reproducibly without rewriting installer
logic each time.

# Instruction Validity and Legacy-Residue Cleanup

Status: **LOCAL CLEANUP IMPLEMENTED — GITHUB RECONCILIATION NOT APPLIED**

## Objective

Leave the active configuration with only current, enforceable instructions.
Remove rules that merely describe the planning and execution system deleted by
the native-first restoration, eliminate orphaned instruction surfaces, and make
the repository's GitHub guidance match live GitHub state.

This cleanup should be applied on top of the in-progress separation between
`global/AGENTS.md` and the repository-root `AGENTS.md`. It must preserve
unrelated working-tree changes.

## Desired instruction model

- `global/AGENTS.md` contains only durable preferences that apply in every
  repository.
- Root `AGENTS.md` contains only current `codex-config` development contracts.
- No nested `AGENTS.md` survives without a real subtree to govern.
- Skills describe their present behavior and scope positively instead of
  naming deleted planners, queues, runners, or orchestration protocols.
- Repository-local adapters for externally installed skills remain versioned in
  the repository, and their commands and labels work against the live tracker.
- Historical architecture remains available through Git history and archive
  branches, not active instructions, tests, or open work items.

## Required changes

### 1. Remove global orchestration residue

In `global/AGENTS.md`, delete the complete `Native orchestration` section:

- `Use native Codex plans and native child-agent orchestration...`
- `Delegate when it improves...`

These rules were retained as transition language when the repository-owned
planner and worker/reviewer runtime were removed. Native planning and
delegation no longer require a global instruction, and the rules can trigger
unnecessary task planning or child-agent use.

Keep the global policies for compact GitHub bodies, commit attribution, and
Codex-home ownership inspection.

Harden the ownership policy so that, when `codex-owner` redirects an edit to a
repository source, Codex also reads and follows the applicable instructions in
that source repository. Codex constructs its ordinary `AGENTS.md` chain at
session start; changing the edit target does not automatically load another
repository's instructions.

### 2. Replace the root anti-legacy boundary with current ownership

In root `AGENTS.md`:

1. Replace the introduction with a positive inventory of what this repository
   owns: global instructions, reusable skills and agents, hooks, the
   manifest-driven installer, and ownership tooling.
2. Remove the `Native runtime boundary` section and its blacklist of planner,
   scheduler, worker/reviewer loop, task ledger, and agent-result protocol.
3. Preserve the actual architectural decision by stating only that this
   repository configures Codex and does not implement a task-execution runtime.
4. Keep the requirements for project-neutral skills, secrets and generated
   state, changelog updates, source-based ownership development, and isolated
   test homes.
5. Make the changelog contract explicit: meaningful behavior changes describe
   the problem, decision, and expected effect.

Update the equivalent native-runtime wording in `README.md` so the public
description uses the same positive scope.

### 3. Remove the orphaned nested instruction file

Delete `.codex/AGENTS.md` entirely. It is the only tracked file below
`.codex/`, is absent from the feature manifest and README, and no longer has a
caller. Its former repository-wide role now belongs to root `AGENTS.md`.

Before deletion, migrate only these current invariants into the appropriate
root section:

- `codex-features.json` lists only features owned by this repository; do not
  add vendor-owned skills, agents, or runtime state.
- Manifest-managed targets install as symlinks, and installer changes preserve
  safe upgrade and conflict behavior for existing installations.

Do not migrate the following obsolete or redundant rules:

- treating the root `AGENTS.md` as installed production workflow code;
- the blanket prohibition on editing runtime state;
- SQLite-specific wording;
- generic instructions to add a note for every skill or agent edit;
- the old rationale that editing a runtime symlink is the preferred source-edit
  path.

### 4. Retain index portability without an activation policy

Rewrite root `AGENTS.md` so it keeps these two properties:

- normal repository reads and search are sufficient for exploration;
- an optional index cannot become semantic authority or a portability
  requirement.

Remove `when explicitly enabled`. That clause descends from the former
temporary Graphify suspension, has no current definition or test, and can
conflict with skill routing supplied outside this repository.

### 5. Remove anti-orchestrator scars from surviving skills

Apply these focused edits:

- In `skills/dead-surface-audit/SKILL.md`, remove `Do not create queues,
  execution state, cleanup protocols, or compatibility wrappers as part of the
  audit.` The opening contract already says the skill produces evidence and
  authorizes neither deletion nor cleanup.
- Remove the matching prose assertion from
  `tests/test_deletion_test_vocabulary_ownership.py`. It currently keeps a
  legacy sentence alive solely because a test requires it.
- In `skills/test-quality-review/SKILL.md`, replace `rather than a task
  orchestrator` with a direct description of the focused review support the
  skill provides.
- In `skills/port-by-contract/SKILL.md`, reduce `Do not turn them into a new
  task framework or execution protocol` to `Report unresolved gaps directly`.
- Keep the `port-by-contract` non-goal against prescribing how Codex plans,
  delegates, reviews, or integrates work. That remains a real scope boundary
  for the skill rather than a runtime migration artifact.

Do not add replacement tests that pin exact prose. Tests should protect a
behavioral or structural contract, not a historical vocabulary.

### 6. Repair the Matt Pocock skill adapters

Keep the repository-local configuration for the externally installed Matt
Pocock skills:

- root `AGENTS.md` references to the tracker and triage vocabulary;
- `docs/agents/issue-tracker.md`;
- `docs/agents/triage-labels.md`;
- the `Wayfinding operations` section;
- the README statement that repository-specific issue and triage configuration
  survives here.

These files are not dead surfaces merely because `.agents/skills/` is ignored
or the consuming skills are installed elsewhere. They are the intended
per-repository adapter layer produced by `setup-matt-pocock-skills`. `triage`,
`to-tickets`, `to-spec`, `code-review`, and `wayfinder` consult this adapter to
translate generic workflows into this repository's tracker operations.

Their retention during the native-first restoration was intentional: the
repository-owned planner and runner were removed, while this compact external
skill configuration remained part of the supported surface.

The live GitHub repository has Issues enabled, but its configured labels have
drifted from the adapter. Reconcile the live tracker by creating or mapping the
missing labels instead of deleting the adapter.

Existing canonical state labels:

- `ready-for-agent`;
- `wontfix`.

Create the missing canonical state labels:

- `needs-triage`;
- `needs-info`;
- `ready-for-human`.

The existing `bug` and `enhancement` labels already satisfy the two triage
category roles.

Provision the labels required by Wayfinder before its first map in this
repository:

- `wayfinder:map`;
- `wayfinder:research`;
- `wayfinder:prototype`;
- `wayfinder:grilling`;
- `wayfinder:task`.

The setup workflow currently writes the desired mappings but does not verify or
provision the corresponding GitHub labels. Treat that as a setup gap. Improve
`setup-matt-pocock-skills` at its actual owner, or add an explicit repository
setup/verification step, so a completed setup cannot leave unusable label
references behind.

Correct the conditional PR-triage command in
`docs/agents/issue-tracker.md`. The documented
`gh pr list --json authorAssociation` invocation fails with the installed
GitHub CLI. PRs are currently not a request surface, so this defect is dormant,
but the documented switch must still be executable before it can be enabled.

Creating labels changes external GitHub state. Present the exact label names,
descriptions, and colors for human confirmation before applying those changes.

### 7. Reconcile the open GitHub backlog

Audit open issues against the native-first restoration. Close or supersede
issues whose requested owner no longer exists, with a short comment pointing to
the restoration decision or an archive branch.

At minimum, review these direct legacy candidates:

- `#46` dedicated work-batch orchestrator;
- `#47` plan-to-execution workflow;
- `#51` plan-batch queue proportionality;
- `#52` planner/reviewer queue gate.

Also search the remaining open backlog for Batch Runway, Planning State,
runway, queue, ledger, baton, Spark, architecture runner, structured transient
agent results, and command-owner terminology. Do not bulk-close based only on a
keyword: retain an issue when its requested user-visible capability still
applies to a surviving feature, and rewrite it against the current owner.

GitHub mutations are a separate execution step. Preparing or implementing the
repository cleanup does not itself authorize closing issues.

### 8. Align tests with current contracts

Keep the existing structural test that distinguishes the installed global
instructions from repository-local instructions, but avoid asserting removed
legacy phrases.

Add or adjust coverage for durable structure where useful:

- the global feature installs `global/AGENTS.md` and `bin/codex-owner`;
- the root instruction file is not the installed global source;
- `.codex/AGENTS.md` does not reappear as a second repository instruction
  owner;
- every manifest source belongs to this repository;
- managed installation targets remain symlinks;
- installer upgrade and foreign-conflict protections remain intact.

Live GitHub labels and CLI schemas should be checked during the tracker audit,
not made a network dependency of the local unit-test suite.

## Suggested implementation sequence

1. Remove `.codex/AGENTS.md` and migrate its two current invariants.
2. Clean `global/AGENTS.md`, root `AGENTS.md`, and the matching README language.
3. Remove skill scars and the prose-retention test assertion.
4. Repair tracker documentation and prepare the missing triage and Wayfinder
   labels for explicit approval and provisioning.
5. Update `CHANGELOG.md` with the problem, decision, and expected effect of the
   completed cleanup.
6. Run local validation.
7. Present the legacy GitHub issue disposition list for human confirmation,
   then perform only the approved issue mutations.

Each commit should contain one coherent responsibility and include
`Co-authored-by: Codex <codex@openai.com>` exactly once when Codex materially
contributes.

## Validation

Run the repository-owned gates:

```bash
UV_CACHE_DIR=/tmp/codex-config-uv-cache uv run --frozen pytest -q
UV_CACHE_DIR=/tmp/codex-config-uv-cache uv run --frozen ruff check scripts hooks tests
UV_CACHE_DIR=/tmp/codex-config-uv-cache uv run --frozen basedpyright
git diff --check
```

Then verify the instruction surfaces and live tracker explicitly:

```bash
find . -path './.git' -prune -o -name AGENTS.md -print
rg -n -i 'planner|scheduler|queue|ledger|runway|task orchestrator|execution protocol' \
  AGENTS.md global README.md skills tests docs
gh label list --limit 200 --json name
gh issue list --state open --limit 200 --json number,title,labels
```

Review every remaining match rather than requiring zero matches: changelog
history and the cleanup document may legitimately name removed concepts.

## Acceptance criteria

- Global instructions contain no planning or delegation directive.
- Root instructions define current repository ownership without cataloguing
  removed runtime components.
- `.codex/AGENTS.md` is deleted and no useful invariant is lost.
- Optional indexes remain non-authoritative without requiring explicit
  activation.
- Surviving skills do not carry anti-runner language unrelated to their present
  contracts.
- No test exists solely to preserve a deleted orchestration phrase.
- Repository-local configuration for the Matt Pocock skills remains intact and
  is identified as an intentional adapter rather than repository-owned skill
  implementation.
- Tracker and label documentation matches live GitHub and the installed GitHub
  CLI.
- All triage and Wayfinder labels named by the adapter exist on GitHub before
  the corresponding workflow is used.
- Legacy open issues have an explicit keep, rewrite, supersede, or close
  disposition approved before external mutation.
- All repository-owned validation commands pass.
- The final changelog entry records the cleanup as removal of stale authority,
  not as a new orchestration design.

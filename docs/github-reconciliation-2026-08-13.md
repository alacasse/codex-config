# GitHub Reconciliation — 2026-08-13

**Status: PREPARED — NOT APPLIED**

All 36 open issues and the repository labels were refreshed from live GitHub
state on 2026-08-13. This document records proposed mutations only. No label,
issue, comment, closure, or transfer operation has been applied.

Every checkbox is an independent approval. An approval authorizes only the
operation described beside that checkbox. Before applying any approved
operation, re-read the live labels and issues and stop if their state has
drifted. After applying approved operations, re-read both collections and
report the resulting state.

## Label reconciliation

### Present labels retained unchanged

These four labels already satisfy repository roles and retain their live
metadata:

| Label | Live description | Live color |
| --- | --- | --- |
| `bug` | Something isn't working | `d73a4a` |
| `enhancement` | New feature or request | `a2eeef` |
| `ready-for-agent` | Fully specified and ready for an agent | `0E8A16` |
| `wontfix` | This will not be worked on | `ffffff` |

The creation operations below are create-if-missing only. They must never edit
or overwrite a same-name label. The repository-owned check remains:

```bash
./scripts/setup_github_labels.py --repo alacasse/codex-config
```

### Approval batch L1 — missing triage labels

- [ ] **Approve L1:** after a fresh check confirms they are still missing,
  create exactly these three labels with the stated metadata and do not edit
  any same-name label.

| Label | Description | Color |
| --- | --- | --- |
| `needs-triage` | Maintainer needs to evaluate this issue | `fbca04` |
| `needs-info` | Waiting on reporter for more information | `d876e3` |
| `ready-for-human` | Requires human implementation | `1d76db` |

Exact creation operations:

```bash
gh label create needs-triage --repo alacasse/codex-config --description 'Maintainer needs to evaluate this issue' --color fbca04
gh label create needs-info --repo alacasse/codex-config --description 'Waiting on reporter for more information' --color d876e3
gh label create ready-for-human --repo alacasse/codex-config --description 'Requires human implementation' --color 1d76db
```

### Approval batch L2 — missing Wayfinder labels

- [ ] **Approve L2:** after a fresh check confirms they are still missing,
  create exactly these five labels with the stated metadata and do not edit any
  same-name label.

| Label | Description | Color |
| --- | --- | --- |
| `wayfinder:map` | Wayfinder map for a multi-session planning effort | `5319e7` |
| `wayfinder:research` | Wayfinder AFK research ticket | `0075ca` |
| `wayfinder:prototype` | Wayfinder HITL prototype ticket | `a2eeef` |
| `wayfinder:grilling` | Wayfinder HITL decision interview ticket | `d876e3` |
| `wayfinder:task` | Wayfinder prerequisite task ticket | `fbca04` |

Exact creation operations:

```bash
gh label create 'wayfinder:map' --repo alacasse/codex-config --description 'Wayfinder map for a multi-session planning effort' --color 5319e7
gh label create 'wayfinder:research' --repo alacasse/codex-config --description 'Wayfinder AFK research ticket' --color 0075ca
gh label create 'wayfinder:prototype' --repo alacasse/codex-config --description 'Wayfinder HITL prototype ticket' --color a2eeef
gh label create 'wayfinder:grilling' --repo alacasse/codex-config --description 'Wayfinder HITL decision interview ticket' --color d876e3
gh label create 'wayfinder:task' --repo alacasse/codex-config --description 'Wayfinder prerequisite task ticket' --color fbca04
```

## Issue reconciliation

### Supersede and close as not planned — 17 issues

Each operation posts the exact comment shown, applies the exact label changes,
and closes the issue with reason `not_planned`. The `wontfix` label already
exists, so these actions do not depend on either missing-label batch.

#### #7 — Make batch-runway commit receipts avoid self-referential hash churn

- Current labels: `enhancement`
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #7:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which removed the repository-owned Batch Runway ledger and receipt protocol from the active configuration. Closing as not planned.

#### #9 — Batch Runway should guard prompt-obligation cleanup during test topology slices

- Current labels: none.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #9:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired the repository-owned Batch Runway execution and review workflow. Closing as not planned.

#### #23 — Prune batch-runway hot path

- Current labels: `skill-cleanup`.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #23:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired the Batch Runway skill instead of further pruning its hot path. Closing as not planned.

#### #24 — Deduplicate ledger and dispatch rules across skills

- Current labels: `skill-cleanup`.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #24:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired the repository-owned planning, ledger, dispatch, and Batch Runway skill stack. Closing as not planned.

#### #28 — Require legacy-removal handoff before behavior-preserving batch runways

- Current labels: none.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #28:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired both the Legacy Removal intake route and the repository-owned Batch Runway workflow. Closing as not planned.

#### #34 — CCFG root cause 2: add-to-ledger can mutate active handoff policy during intake

- Current labels: none.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #34:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired the add-to-ledger command and repository-owned active handoff state. Closing as not planned.

#### #35 — CCFG root cause 3: ledger intake conflates finding capture with work-order prioritization

- Current labels: none.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #35:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired the repository-owned ledger intake and work-order prioritization workflow. Closing as not planned.

#### #36 — CCFG root cause 4: command-owner and support skills lack an artifact-write authority matrix

- Current labels: none.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #36:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired the command-owner planning stack and its artifact-write protocol. Closing as not planned.

#### #38 — Clarify Batch Runway result-contract version selection

- Current labels: `ready-for-agent`.
- Exact label changes: add `wontfix`; remove `ready-for-agent`.
- [ ] **Approve #38:** post the comment below, apply the label changes, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which removed the Batch Runway v1/v2 result-contract protocol from the active configuration. Closing as not planned.

#### #41 — Automate import-topology specialist routing

- Current labels: `ready-for-agent`.
- Exact label changes: add `wontfix`; remove `ready-for-agent`.
- [ ] **Approve #41:** post the comment below, apply the label changes, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b): this repository still ships the narrow import-topology reviewer, but automatic coordinator routing belongs to native Codex orchestration rather than a repository-owned dispatcher. Closing as not planned.

#### #42 — Enforce Spark's low-risk task boundary

- Current labels: `ready-for-agent`.
- Exact label changes: add `wontfix`; remove `ready-for-agent`.
- [ ] **Approve #42:** post the comment below, apply the label changes, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which removed the Spark agent and its repository-owned task envelope. Closing as not planned.

#### #44 — Validate registered agent result payloads at runtime

- Current labels: `ready-for-agent`.
- Exact label changes: add `wontfix`; remove `ready-for-agent`.
- [ ] **Approve #44:** post the comment below, apply the label changes, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired the registered result-schema protocol and Batch Runway result consumer. Closing as not planned.

#### #46 — Add a dedicated work-batch orchestrator agent

- Current labels: none.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #46:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which assigns task execution and child-agent coordination to Codex's native runtime rather than a repository-owned orchestrator. Closing as not planned.

#### #47 — Add a single-run plan-to-execution workflow

- Current labels: none.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #47:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which assigns planning and execution orchestration to Codex's native runtime rather than a repository-owned workflow. Closing as not planned.

#### #50 — Explore contract-first hybrid planning artifacts

- Current labels: `enhancement`.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #50:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which archived the repository-owned planning-artifact and execution-handoff protocol instead of extending it with new schemas. Closing as not planned.

#### #51 — Require compact proportionality evidence before plan-batch queues a runway

- Current labels: none.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #51:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired the plan-batch queue and CCFG planning protocol that this proportionality gate targeted. Closing as not planned.

#### #52 — Delegate draft planning and independent plan review before queue mutation

- Current labels: none.
- Exact label changes: add `wontfix`; remove none.
- [ ] **Approve #52:** post the comment below, apply the label change, and close
  as `not_planned`.

> Superseded by the [native-first restoration](https://github.com/alacasse/codex-config/commit/dabd81b), which retired the repository-owned planner/reviewer loop and plan-batch queue gate. Closing as not planned.

### Close as completed — 5 issues

Each operation posts the exact comment shown, applies the exact label changes,
and closes the issue with reason `completed`. None depends on a missing-label
batch.

#### #10 — Explore extracting a generic phase runner product

- Current labels: none.
- Exact label changes: none.
- [ ] **Approve #10:** post the comment below and close as `completed`.

> The exploration is complete and preserved on [`archive/batch-runway-master-20260721`](https://github.com/alacasse/codex-config/tree/archive/batch-runway-master-20260721): it records the generic workflow contract, shell/Codex adapter evidence, and the decision to target a separate OSS Go runner after contract-first extraction. The native-first restoration removed the runner from this repository, so no follow-up implementation belongs here. Closing as completed.

#### #25 — Shorten skill frontmatter descriptions

- Current labels: `skill-cleanup`.
- Exact label changes: remove `skill-cleanup`; add none.
- [ ] **Approve #25:** post the comment below, apply the label change, and close
  as `completed`.

> Completed by the native-first restoration (`dabd81b`) and follow-up cleanup (`88d1ccf`): every surviving repository-owned skill now has a compact, trigger-oriented frontmatter description, with workflow detail in the body. Closing as completed.

#### #37 — Make feature installation prune stale managed links

- Current labels: none.
- Exact label changes: none.
- [ ] **Approve #37:** post the comment below and close as `completed`.

> Completed in `dabd81b` and hardened in `2168334`: status and prune reconcile removed manifest links, delete only exact installer-managed symlinks, preserve unmanaged or retargeted paths, report dry runs, and remain idempotent. Closing as completed.

#### #39 — Restore a clean repository test baseline

- Current labels: `ready-for-agent`.
- Exact label changes: remove `ready-for-agent`; add none.
- [ ] **Approve #39:** post the comment below, apply the label change, and close
  as `completed`.

> Completed by the native-first restoration (`dabd81b`, `2168334`) and current cleanup (`88d1ccf`): obsolete owner-specific assertions were removed, surviving contracts were repaired, and the current pytest suite is green. Closing as completed.

#### #40 — Make installed feature metadata converge with the manifest

- Current labels: `ready-for-agent`.
- Exact label changes: remove `ready-for-agent`; add none.
- [ ] **Approve #40:** post the comment below, apply the label change, and close
  as `completed`.

> Completed in `15b8fd2`: a version-only install rewrites recorded version, description, and link metadata from the active manifest; status no longer reports drift after installation; and focused regression coverage proves idempotent convergence. Closing as completed.

### Rewrite individually and retain open — 9 issues

Each approved action replaces the entire issue body with the exact body shown,
applies the exact title and label changes, and leaves the issue open. It does
not post a comment.

#### #3 — Add finding disposition model for test-quality-review

- Current labels: none.
- Exact title change: none.
- Exact label changes: add `enhancement` and `ready-for-agent`; remove none.
- [ ] **Approve #3:** replace the complete body and apply the label changes.

Complete replacement body:

```markdown
## Summary

Add an optional disposition to `test-quality-review` findings so callers can distinguish immediate blockers, in-scope fixes, follow-up candidates, and notes.

## Why

Risk level describes impact, but not the action expected after review. A separate disposition makes handoffs clearer without granting the skill authority to implement fixes or write to an issue tracker.

## Proposed direction

Use four dispositions:

- `blocking`: must be resolved before the reviewed change is accepted.
- `fix_in_scope`: a bounded correction belongs in the reviewed change.
- `issue_candidate`: valid follow-up outside the reviewed change.
- `note_only`: useful observation with no required action.

The reviewer recommends a disposition; the caller or user retains scope and tracker authority.

## Acceptance criteria

- `test-quality-review` documents the four dispositions and keeps them distinct from risk level.
- Compact YAML and standalone reports can include a disposition for each finding.
- Guidance explains when uncertainty should remain a candidate or note instead of a blocker.
- The default remains review-only: no automatic fixes, issue creation, or scope expansion.
- Tests validate output structure and allowed values without pinning explanatory prose.
```

#### #4 — Define workflow for issue candidates emitted by test-quality-review

- Current labels: none.
- Exact title change: rename to `Define issue-candidate output for test-quality-review`.
- Exact label changes: add `enhancement` and `ready-for-agent`; remove none.
- [ ] **Approve #4:** apply the title change, replace the complete body, and
  apply the label changes.

Complete replacement body:

```markdown
## Summary

Define an optional issue-candidate output for actionable `test-quality-review` findings that belong outside the reviewed change.

## Why

A reviewer should be able to preserve a valid follow-up without expanding current scope or automatically writing to a tracker.

## Proposed direction

Each issue candidate should contain:

- a suggested title;
- the observed problem and supporting evidence;
- why it matters;
- a proposed direction;
- compact acceptance criteria.

The skill emits candidate text only. The user or calling workflow decides whether and where to publish it.

## Acceptance criteria

- Issue candidates contain enough evidence and acceptance criteria to become actionable tracker items.
- Candidates remain distinct from blockers, in-scope fixes, and notes.
- Producing a candidate does not expand the active review or create an issue automatically.
- The format remains project-neutral and does not require GitHub.
- Standalone and compact review outputs can carry candidates consistently.
```

#### #15 — Add skill-slimmer skill

- Current labels: `enhancement`.
- Exact title change: none.
- Exact label changes: add `ready-for-agent`; retain `enhancement`; remove none.
- [ ] **Approve #15:** replace the complete body and apply the label change.

Complete replacement body:

```markdown
## Summary

Add a project-neutral `skill-slimmer` skill that audits repository-owned skills for progressive disclosure, context cost, duplication, and maintainable structure.

## Why

A skill entrypoint should contain the instructions needed for normal execution while loading examples, rare cases, and long reference material only when relevant.

## Proposed direction

Given a skill directory, report:

- what should remain in `SKILL.md`;
- what should move to `references/`;
- what is better expressed as a script, template, or example;
- what is duplicated, stale, or behaviorally inert;
- whether trigger, output, and stop conditions are clear;
- required changes separately from optional cleanup.

## Acceptance criteria

- The new skill is itself compact and demonstrates progressive disclosure.
- It can audit all current manifest-installed skills.
- It works through ordinary reads and search without an index dependency.
- Its guidance is project-neutral and does not depend on archived repository features.
- Its output distinguishes required corrections from optional improvements.
```

#### #26 — Codify leading words for each skill

- Current labels: `skill-cleanup`.
- Exact title change: rename to `Align trigger vocabulary across repository-owned skills`.
- Exact label changes: add `enhancement` and `ready-for-agent`; remove
  `skill-cleanup`.
- [ ] **Approve #26:** apply the title change, replace the complete body, and
  apply the label changes.

Complete replacement body:

```markdown
## Summary

Review manifest-installed skills for concise, consistent vocabulary that accurately distinguishes their triggers, behavior, and outputs.

## Why

Stable terms can improve discovery and execution when they name real behavior. Decorative or obsolete vocabulary adds context without improving decisions.

## Proposed direction

For each installed skill:

- identify a small set of terms already tied to its actual contract;
- use those terms consistently where they clarify triggers, workflow, or output;
- remove terms that are vague, obsolete, or unique to one paragraph;
- keep frontmatter descriptions concise.

Do not require a dedicated vocabulary section when normal prose is clearer.

## Acceptance criteria

- Every manifest-installed skill is reviewed against its current behavior.
- Trigger descriptions remain distinct and easy to scan.
- Repeated terms correspond to real workflow or output distinctions.
- No deleted feature terminology is reintroduced.
- Tests protect discovery and structure without pinning exact prose.
```

#### #27 — Run deletion tests for skill no-ops and sediment

- Current labels: `skill-cleanup`.
- Exact title change: rename to `Remove no-op instructions and sediment from repository-owned skills`.
- Exact label changes: add `enhancement` and `ready-for-agent`; remove
  `skill-cleanup`.
- [ ] **Approve #27:** apply the title change, replace the complete body, and
  apply the label changes.

Complete replacement body:

```markdown
## Summary

Audit current manifest-installed skills and their directly referenced files for instructions that do not materially change behavior.

## Why

Duplicated warnings, generic advice, obsolete examples, and prose retained only by exact-text tests increase context cost and make real contracts harder to find.

## Proposed direction

For each suspicious instruction, determine:

- the behavior it protects;
- whether another current source already owns that behavior;
- whether deletion would change execution, safety, or output;
- whether the content should be removed, compacted, or kept with clearer purpose.

## Acceptance criteria

- All current repository-owned skills and direct references are reviewed.
- Removed duplication has a named remaining source of truth.
- Retained long instructions have a concrete behavioral purpose.
- Archived features are not treated as active skill requirements.
- Exact-prose tests are replaced only when a structural or behavioral contract needs protection.
- Repository validation remains green.
```

#### #43 — Benchmark custom-agent model assignments

- Current labels: `ready-for-agent`.
- Exact title change: rename to `Benchmark current custom-agent model assignments`.
- Exact label changes: add `enhancement` and `ready-for-human`; remove
  `ready-for-agent`.
- Dependency: approval and successful application of label batch L1, because
  `ready-for-human` is currently missing.
- [ ] **Approve #43:** after the dependency is satisfied, apply the title
  change, replace the complete body, and apply the label changes.

Complete replacement body:

```markdown
## Summary

Build a reproducible, role-specific evaluation of the two custom agents currently registered by this repository.

## Current assignments

| Agent | Role | Model | Reasoning effort |
| --- | --- | --- | --- |
| `codebase_investigator` | Bounded read-only codebase investigation | `gpt-5.6-terra` | `low` |
| `import_topology_reviewer` | Bounded read-only import-topology review | `gpt-5.6-terra` | `low` |

The TOML files under `agents/` remain authoritative.

## Proposed direction

Use bounded fixtures for each role and compare the current model and effort with at least one plausible alternative under equivalent conditions. Measure role-boundary compliance, correctness, evidence quality, latency, and token or cost data when exposed by the runtime.

Live model calls require explicit approval before execution.

## Acceptance criteria

- The corpus covers every agent currently declared by the manifest.
- Every current assignment is compared with at least one plausible alternative.
- Shared and role-specific criteria are reported separately.
- Runtime conditions, model availability, measurements, limitations, and confidence are recorded.
- Unavailable token or cost measurements are identified rather than estimated.
- The benchmark reads assignments from the agent TOMLs instead of creating a second registry.
- Assignment changes require a separately approved repository change.
```

#### #45 — Add live smoke coverage for registered custom agents

- Current labels: `ready-for-agent`.
- Exact title change: none.
- Exact label changes: add `enhancement` and `ready-for-human`; remove
  `ready-for-agent`.
- Dependency: approval and successful application of label batch L1, because
  `ready-for-human` is currently missing.
- [ ] **Approve #45:** after the dependency is satisfied, replace the complete
  body and apply the label changes.

Complete replacement body:

```markdown
## Summary

Add an explicit opt-in live smoke for the two custom agents currently installed by this repository.

## Current agents

| Agent | Role exercised |
| --- | --- |
| `codebase_investigator` | Bounded read-only technical investigation |
| `import_topology_reviewer` | Bounded read-only project-local import review |

The manifest and agent TOMLs remain authoritative.

## Proposed direction

Install the current configuration into an isolated Codex home, invoke each registered agent with a bounded read-only fixture, and verify that the agent loads and respects its role contract. Confirm the configured model and reasoning effort when the runtime exposes those facts; otherwise record the limitation.

## Acceptance criteria

- The smoke discovers agents from the current manifest and TOMLs.
- Every invocation uses a bounded read-only fixture and cannot modify the working repository.
- Results are checked against each agent's documented role boundaries and expected evidence quality.
- Failures distinguish stale installation or reload needs from authentication, model availability, cost approval, and role-contract failures.
- Live calls require explicit opt-in and are excluded from the default offline test suite.
- The procedure is documented and rerunnable after agent or installer changes.
```

#### #48 — Explore contract-first hybrid language for agent skills

- Current labels: `enhancement`.
- Exact title change: rename to `Evaluate a lightweight contract-first format for repository-owned skills`.
- Exact label changes: add `ready-for-agent`; retain `enhancement`; remove none.
- [ ] **Approve #48:** apply the title change, replace the complete body, and
  apply the label change.

Complete replacement body:

```markdown
## Summary

Evaluate whether a small structured contract section improves the clarity and auditability of repository-owned skills.

## Why

Stable operational facts can be difficult to review when mixed throughout narrative instructions. A lightweight structure may improve scanning and contradiction detection, but it should earn its complexity through evidence.

## Experiment

Choose one current repository-owned skill and compare its existing form with a candidate that uses:

- structured fields only for stable operational facts;
- numbered steps for normal procedure;
- explicit branch rules where branching is material;
- short rationale for non-obvious invariants;
- references for examples and rare cases.

This issue evaluates the pattern; it does not authorize a broad migration.

## Acceptance criteria

- The experiment uses a current manifest-installed skill.
- The report compares clarity, contradiction risk, context size, and observed behavior.
- The candidate remains readable without a repository-specific parser.
- Tests protect parseable structure or behavior, not exact explanatory prose.
- The result records an explicit adopt, revise, or reject decision.
- No other skills are migrated until that decision is approved.
```

#### #49 — Add a meta-skill for contract-first skill authoring

- Current labels: `enhancement`.
- Exact title change: rename to `Add guidance for contract-first skill authoring`.
- Exact label changes: add `needs-triage`; retain `enhancement`; remove none.
- Dependency: approval and successful application of label batch L1, because
  `needs-triage` is currently missing.
- [ ] **Approve #49:** after the dependency is satisfied, apply the title
  change, replace the complete body, and apply the label change.

Complete replacement body:

```markdown
## Summary

If #48 adopts a contract-first pattern, add project-neutral guidance for creating, migrating, and reviewing repository-owned skills in that format.

## Why

An adopted structure needs one clear authoring workflow so future changes do not become cosmetic formatting or recreate ambiguity elsewhere.

## Proposed direction

The guidance should help an author:

- identify the skill's purpose and boundaries;
- define required inputs and outputs;
- separate normal procedure from material branches;
- keep rationale concise;
- move examples and rare cases into references;
- report unresolved ambiguity instead of guessing;
- validate the result against the pattern approved in #48.

## Acceptance criteria

- Work begins only after #48 records an approved pattern.
- The guidance follows the repository's existing skill layout and manifest rules.
- It remains project-neutral and does not copy archived feature contracts.
- It distinguishes authoring from optional slimming or cleanup review.
- It produces an ambiguity report and validation checklist.
- It does not trigger an automatic migration of existing skills.
```

### Transfer to `alacasse/baton-runner` — 5 issues

Each approved transfer applies the exact pre-transfer label change, if any,
posts the exact pre-transfer comment, and then runs the native
`gh issue transfer` command shown. Titles and bodies are not edited before
transfer. The destination currently has a matching `enhancement` label. These
actions do not depend on either missing-label batch.

#### #8 — Explore SQLite operational index for architecture program runner

- Current labels: none.
- Current comments: one addendum recommending opt-in phase logs, paths and
  metadata only in SQLite, and canonical Markdown/JSON artifacts.
- Exact label changes: add `enhancement`; remove none.
- Exact title/body changes: none; preserve the detailed design record.
- [ ] **Approve #8:** add `enhancement`, post the comment below, and run the
  transfer command.

> Transferring this issue to `alacasse/baton-runner`. An optional, rebuildable operational index over durable run artifacts is runner functionality, while `codex-config` now owns installed configuration and tracker adapters. Baton Runner should reassess the architecture-runner-specific schema against its provider-neutral receipt and artifact model.

```bash
gh issue transfer 8 alacasse/baton-runner --repo alacasse/codex-config
```

#### #11 — Add branch-per-batch support for local architecture runner

- Current labels: none.
- Current comments: none.
- Exact label changes: add `enhancement`; remove none.
- Exact title/body changes: none.
- [ ] **Approve #11:** add `enhancement`, post the comment below, and run the
  transfer command.

> Transferring this issue to `alacasse/baton-runner`. Optional per-batch Git branch isolation is a runner execution policy, not installed Codex configuration. Baton Runner should keep it optional so non-Git and non-coding workflows remain supported.

```bash
gh issue transfer 11 alacasse/baton-runner --repo alacasse/codex-config
```

#### #17 — Add baton-context-map CLI

- Current labels: `enhancement`.
- Current comments: none.
- Exact label changes: none; retain `enhancement`.
- Exact title/body changes: none.
- [ ] **Approve #17:** post the comment below and run the transfer command.

> Transferring this issue to `alacasse/baton-runner`. Building bounded worker context from declared inputs and artifacts belongs with phase handoff in the runner. The destination should keep the interface provider-neutral.

```bash
gh issue transfer 17 alacasse/baton-runner --repo alacasse/codex-config
```

#### #18 — Add baton-doctor CLI

- Current labels: `enhancement`.
- Current comments: none.
- Exact label changes: none; retain `enhancement`.
- Exact title/body changes: none.
- [ ] **Approve #18:** post the comment below and run the transfer command.

> Transferring this issue to `alacasse/baton-runner`. Runner readiness diagnostics belong with the runner CLI, not Codex configuration. The destination should retain actionable preflight checks while dropping Codex-specific skill and planning assumptions.

```bash
gh issue transfer 18 alacasse/baton-runner --repo alacasse/codex-config
```

#### #19 — Add baton-receipt-inspector CLI

- Current labels: `enhancement`.
- Current comments: none.
- Exact label changes: none; retain `enhancement`.
- Exact title/body changes: none.
- [ ] **Approve #19:** post the comment below and run the transfer command.

> Transferring this issue to `alacasse/baton-runner`. Run, receipt, telemetry, and artifact inspection is a core runner capability and belongs beside the format it interprets.

```bash
gh issue transfer 19 alacasse/baton-runner --repo alacasse/codex-config
```

## Approval and application boundary

No checkbox is approved merely by committing this document. Apply only checked
label batches and checked issue actions. Issue actions #43, #45, and #49 also
require label batch L1 to have been applied successfully. No issue action
depends on label batch L2.

Immediately before applying approved actions:

1. Refresh labels and all open issues.
2. Confirm every approved action still matches the recorded title, labels, and
   open state.
3. Confirm required destination and missing labels exist.
4. Apply only the checked operations, in their documented order.
5. Re-read labels and open issues and report the final state.

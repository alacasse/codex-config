# CCFG-18 Candidate Generation Runway

## Purpose

Create and prove the candidate repository and candidate `CODEX_HOME` under the
installed stable `cross-checkout-precreation/v1` controller, preserve the
authoritative master and accepted-design lineage, transition to strict
`cross-checkout-context/v1` before further implementation, and demonstrate
fixture-only candidate operation plus pre-cutover rollback without switching
the default generation.

This runway covers the remaining bounded scope of CCFG-18 only. Successful
same-batch closeout may close CCFG-18, but it must not select CCFG-19.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`.
- Slice 1 risk: `migration`.
- Slice 2 risk: `migration`.
- Slice 3 risk: `evidence-only`.
- Destructive cleanup: forbidden.
- Contract narrowing: forbidden.
- Destructive or contract-narrowing approval gates: none required because no
  such slice is authorized.
- Creation authority is narrower than general migration authority: before
  strict transition, only the two exact roots in the validated pre-creation
  payload may be created.
- Filesystem, network, and fresh-session model-cost approvals must be obtained
  at execution time when the runtime requires them. Approval does not widen the
  payload, allowed paths, finding scope, or lifecycle authority.

## Current Baseline And Assumptions

- Planning Artifact Layout v1 is active at
  `/home/alacasse/projects/codex-config/docs/plans`.
- Program root:
  `/home/alacasse/projects/codex-config/docs/plans/programs/codex-config`.
- Planning-state `current` and `validate` pass with no blockers and only the two
  known redirect-ledger warnings.
- Selected dispatch, queued runway, and active runway were all `None` before
  this planning pass.
- Stable checkout:
  `/home/alacasse/projects/codex-config`, branch `master`, exact `HEAD` and
  `origin/master` `da5b97165eb8d8c9f809a64937bcc9d753032ee7`.
- Stable worktree was clean before this planning pass.
- Active stable `CODEX_HOME`: `/home/alacasse/.codex`.
- `./install.sh --status` reports the exact committed feature versions.
- `./install.sh --dry-run` reports every repo-owned link as `ok`, including the
  helper link, and resolves them to the stable checkout.
- Installed helper:
  `/home/alacasse/.codex/scripts/cross_checkout_context.py`, resolving to
  `/home/alacasse/projects/codex-config/scripts/cross_checkout_context.py`.
- Candidate repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`; absent.
- Candidate `CODEX_HOME`:
  `/home/alacasse/.codex-command-owner-redesign`; absent.
- Candidate implementation branch:
  `implementation/command-owner-redesign`.
- Accepted immutable design snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`, reachable from
  `origin/architecture/command-owner-redesign` in the stable clone.
- The accepted design snapshot is not an ancestor of stable `HEAD`; Slice 1
  must create an ancestry-preserving merge commit.
- Baseline focused validation is green: 86 tests and 439 subtests across strict
  context, pre-creation, registered agents, create-spec, and lifecycle guards;
  focused manifest validation is 3 tests and 137 subtests; Ruff and
  basedpyright are green.
- Full manifest validation remains a known-red baseline of 3 failures, 18
  passes, and 202 passing subtests in unrelated exact-wording expectations.

The plan-batch output itself is expected dirty planning state. Before Slice 1,
the execution coordinator must preserve the fixed stable `HEAD` above, re-run
pre-creation validation, and avoid committing these planning artifacts. After
the transition receipt is green, later strict contexts must be regenerated
from the exact then-current stable and candidate revisions before each handoff.

## Required Cross-Checkout Pre-Creation Context

Mode: explicit `cross-checkout-precreation/v1`.

Installed helper path used for planning validation:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Complete validated payload:

```yaml
interface: cross-checkout-precreation/v1
stable_control:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  canonical_planning_root: /home/alacasse/projects/codex-config/docs/plans
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
candidate_intent:
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  expected_repository_state: absent
  candidate_codex_home: /home/alacasse/.codex-command-owner-redesign
  expected_codex_home_state: absent
  base_repository: alacasse/codex-config
  base_commit: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  implementation_branch: implementation/command-owner-redesign
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
creation_authority:
  repository_creation_allowed: true
  candidate_codex_home_creation_allowed: true
  allowed_creation_roots:
    - /home/alacasse/projects/codex-config-command-owner-redesign
    - /home/alacasse/.codex-command-owner-redesign
```

Planning validation loaded the installed helper, called
`parse_cross_checkout_precreation`, and called
`validate_precreation_creation_targets` with both ordered creation roots. Both
calls passed while both targets were absent. Planning performed zero writes to
either target.

Before the Slice 1 read-only merge review and creation-bearing worker handoff,
the coordinator, reviewer, and worker must independently follow
`skills/batch-runway/references/cross-checkout-precreation-v1.md`. Handoffs must
include this exact payload, this absolute helper path, the exact intended
creation targets, and `read-only` or `creation-bearing` mode. Pre-creation
results populate `verified_cross_checkout_precreation` and leave
`verified_cross_checkout_context` null.

## Mandatory Transition To Strict Context

Slice 1 must not create a normal implementation diff before strict transition.
The accepted-design merge is repository establishment required to make the
strict identity true.

The coordinator must use this order:

1. While both targets are absent, compute and independently review the
   deterministic merge result of authoritative master
   `da5b97165eb8d8c9f809a64937bcc9d753032ee7` and accepted design
   `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c` in the stable repository. Record
   the reviewed tree hash and diff basis.
2. Delegate one creation-bearing worker to create only the two authorized roots,
   clone `alacasse/codex-config`, create
   `implementation/command-owner-redesign` from the base commit, and prepare the
   ancestry-preserving merge result without unrelated changes.
3. Verify the candidate merge tree exactly equals the pre-reviewed tree. The
   coordinator may then create the mechanical merge commit with both expected
   parents; no later work is accepted yet.
4. Parse the complete strict `cross-checkout-context/v1` payload with the same
   installed stable helper, using the actual full candidate merge commit as
   `implementation_commit_before`.
5. Call `build_cross_checkout_transition_receipt` with the retained validated
   pre-creation context and validated strict context, preserve the exact
   `cross_checkout_transition_receipt_to_dict` result in the batch evidence,
   and revalidate strict context.
6. Delegate a strict-context reviewer over the exact merge commit and ancestry
   evidence. Any mismatch stops the batch before Slice 2.

The first strict context is stable-controlled. Its exact runtime shape is:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: b044e3c348922663aa074638227aae8d2633cfe3
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

The runtime-captured candidate commit is
`b044e3c348922663aa074638227aae8d2633cfe3`. After strict transition,
`verified_cross_checkout_precreation` is null and every worker/reviewer result
must carry the freshly validated `verified_cross_checkout_context` required by
`skills/batch-runway/references/cross-checkout-context-v1.md`.

## Project Values

- Planning location:
  `/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation`.
- Canonical planning repository:
  `/home/alacasse/projects/codex-config`.
- Canonical planning root:
  `/home/alacasse/projects/codex-config/docs/plans`.
- Implementation repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign` after Slice 1.
- Stable `CODEX_HOME`: `/home/alacasse/.codex`.
- Candidate `CODEX_HOME`: `/home/alacasse/.codex-command-owner-redesign` after
  Slice 1.
- Fixture root:
  `/tmp/ccfg-18-candidate-generation-fixture`; execution recreates it from
  scratch and stores no durable authority there.
- Run artifact root: `None`; transition and cross-repository receipt dictionaries
  are preserved compactly in batch planning/closeout evidence.
- Output root: `None`; durable generated output is forbidden. Ephemeral fresh
  session output stays below the fixture root.
- Integration harnesses: stable and candidate installer status/dry-run, focused
  cross-checkout and manifest tests, and one fresh candidate fixture session.
- Summary artifacts: installed link maps, transition receipt, strict contexts,
  candidate fixture session last message, stable/candidate generation
  fingerprints, planning-state diagnostics, and rollback/quiescence receipt.
- Index/generated-doc refresh: none.
- Commit strategy:
  - candidate repository receives the ancestry-preserving merge commit and the
    explicit live-amendment commit;
  - stable repository receives only canonical planning evidence/receipt commits
    after strict transition, plus the self-referential closeout commit;
  - candidate source commits and stable planning receipt commits remain distinct
    in cross-repository receipts.
- Dirty-file constraint: the four plan-batch outputs are expected stable
  planning changes at execution start. Workers must not stage or commit them;
  the coordinator owns their receipt and closeout commits.

## Non-Goals

- Do not select or begin CCFG-19.
- Do not implement any command-owner contract or transfer workflow ownership.
- Do not switch the default `CODEX_HOME` or controlling generation.
- Do not allow candidate sessions to mutate real canonical planning state.
- Do not weaken or alias strict `cross-checkout-context/v1`.
- Do not change the stable helper, skills, agents, manifest, or installer as
  part of this batch unless validation exposes a blocker that requires a new
  ledger amendment and replan.
- Do not rewrite the immutable accepted design snapshot or move its branch.
- Do not delete or retire stable/candidate branches, candidate paths, APR,
  Batch Runway, or the temporary cross-checkout bridge.
- Do not persist credentials, copy `auth.json`, or link secrets into the
  candidate home without explicit user authorization.
- Do not run real candidate-controlled ledger work before cutover.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2. Registered agent TOMLs
own worker and reviewer result schemas.
Use Batch Runway Compact Report Contract v1 only for coordinator receipts and
its non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for suspicious coordinator or
subagent-lifecycle behavior only.
Use the expanded convergence template for final batch reporting.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine strict-context execution
after the transition.

Reference files:

- `skills/batch-runway/references/cross-checkout-precreation-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/validation-profiles/project-harness-production.md`

Overrides:

- Slice 1 uses a pre-reviewed deterministic merge tree as its before-commit
  review basis because strict context cannot exist until the ancestry-preserving
  merge commit exists. The exact committed tree must equal the reviewed tree,
  and an additional strict-context reviewer must review the resulting commit
  before Slice 2. This exception applies only to the mechanical transition
  commit and does not permit unreviewed implementation work.
- Stable planning artifacts must not be committed before the fixed
  pre-creation payload and transition receipt are green. After transition,
  ordinary candidate commits, stable planning receipts, validation, and reviews
  follow the standard contract.
- Slice 3 is evidence-only. Its focused stable planning receipt commit satisfies
  the per-slice commit requirement; it creates no candidate implementation
  commit.

Execution boundaries:

- The main agent coordinates. Creation and implementation work is delegated to
  `runway_worker`; independent review is delegated to `runway_reviewer`.
- A spawned worker is already the required coding subagent, implements only its
  assigned slice, and must not spawn, delegate to, or wait on more agents.
- Workers do not accept validation, review, closeout, lifecycle, commit, or
  successor authority.
- The coordinator owns helper bootstrap, exact target validation, strict
  transition, integration and fresh-session harnesses, review delegation,
  commits, ledger/archive updates, and same-batch closeout.
- Stable planning writes stay inside the canonical planning root. Candidate
  source writes and candidate commits stay inside the candidate repository.
- Before each strict worker/reviewer handoff, regenerate the complete strict
  payload from exact then-current stable and candidate commits, validate it with
  the installed stable helper, validate declared planning/implementation paths,
  and require matching agent result identity.

## Validation Profile

Selected profile: `project-harness-production` with cross-checkout and fresh
session overrides.

Focused validation commands and status classes:

- `python scripts/planning_state.py current --root docs/plans`
  - Status: `required-green`.
  - Baseline: passed with no blockers.
- `python scripts/planning_state.py validate --root docs/plans`
  - Status: `required-green`.
  - Baseline: passed with only two known redirect-ledger warnings.
- Installed-helper pre-creation parse plus exact-target validation using the
  complete payload in this runway
  - Status: `required-green` before any target creation.
  - Baseline: passed for both exact absent roots.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_cross_checkout_precreation.py tests/test_cross_checkout_context.py tests/test_custom_agent_contracts.py tests/test_batch_runway_create_spec_contract.py tests/test_batch_lifecycle_guards.py`
  - Status: `required-green`.
  - Baseline: 86 passed, 439 subtests passed.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_codex_features_manifest.py -k 'cross_checkout or runway_worker or runway_reviewer'`
  - Status: `required-green`.
  - Baseline: 3 passed, 18 deselected, 137 subtests passed.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_codex_features_manifest.py`
  - Status: `known-red-baseline`.
  - Baseline: 3 failed, 18 passed, 202 subtests passed in unrelated exact-wording
    expectations. This command is diagnostic and must expose any new failure in
    cross-checkout, agent, helper-owner, or feature-version assertions.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline ruff check scripts/cross_checkout_context.py tests/test_cross_checkout_precreation.py tests/test_cross_checkout_context.py tests/test_custom_agent_contracts.py tests/test_batch_runway_create_spec_contract.py tests/test_batch_lifecycle_guards.py tests/test_codex_features_manifest.py`
  - Status: `required-green`.
  - Baseline: passed.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline basedpyright scripts/cross_checkout_context.py`
  - Status: `required-green`.
  - Baseline: zero errors, warnings, or notes.
- `./install.sh --status`
  - Status: `required-green` for stable control before and after every slice.
  - Baseline: exact committed versions.
- `./install.sh --dry-run`
  - Status: `required-green` for stable control before and after every slice.
  - Baseline: all repo-owned links `ok`, no state written.
- `/home/alacasse/projects/codex-config-command-owner-redesign/install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --all`
  - Status: `implementation-created`.
  - Slice 1 creates the candidate repository/home; Slice 2 runs the real
    generation-specific install after the live-amendment candidate commit.
- `/home/alacasse/projects/codex-config-command-owner-redesign/install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status`
  - Status: `implementation-created`.
  - Slice 2 promotes it after installation and requires exact manifest versions.
- `/home/alacasse/projects/codex-config-command-owner-redesign/install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run`
  - Status: `implementation-created`.
  - Slice 2 promotes it and requires every candidate link to resolve to the
    candidate repository with no stable/candidate mixture.
- Candidate ancestry checks using `git merge-base --is-ancestor` for both
  `da5b97165eb8d8c9f809a64937bcc9d753032ee7` and
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c` against candidate `HEAD`
  - Status: `implementation-created` by Slice 1, then `required-green`.
- Fresh candidate fixture session rooted at
  `/tmp/ccfg-18-candidate-generation-fixture` with
  `CODEX_HOME=/home/alacasse/.codex-command-owner-redesign`, `codex exec
  --ephemeral --sandbox workspace-write --skip-git-repo-check`, and no writable
  path outside the fixture
  - Status: `implementation-created`.
  - Slice 3 prepares the fixture and runs the cost-bearing session only after
    runtime approval and authentication preflight.
- Candidate strict-context canonical-write rejection plus stable planning
  `current`/`validate` and stable worktree comparison after the fixture session
  - Status: `implementation-created` by Slice 3, then `required-green`.
- `python -m json.tool codex-features.json`
  - Status: `required-green` in both repositories after candidate establishment.
- `git diff --check`
  - Status: `required-green` in each repository for its task-scoped diff.

The execution coordinator runs installer, strict-context, cross-repository,
fresh-session, and final validation. Workers run only slice-assigned focused
commands. No source index or generated-doc refresh is required.

## Active Ledger

No pending slices.

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Completed Slice Archive

| Slice | Candidate commit | Stable planning receipt | Outcome | Audit references |
|---|---|---|---|---|
| 1. Candidate roots and strict transition | `b044e3c` | `3fa5c4f` | success; exact reviewed merge tree and design subtree, helper-produced transition receipt, strict stable context, focused tests/lint/types/install/planning validation green, strict and planning reviews clean; full manifest unchanged at its exact known-red baseline | `completed-slices.md`; `git show --stat b044e3c`; `git show --stat 3fa5c4f` |
| 2. Candidate amendment and generation install | `9027bd1` | `af0a1b9` | success; live amendment and immutable lineage reviewed, isolated candidate install complete, candidate/stable link maps separated, strict receipts and required validation green; full manifest unchanged at its exact known-red baseline | `completed-slices.md`; `git show --stat 9027bd1`; `git show --stat af0a1b9` |
| 3. Fixture isolation and rollback proof | Not applicable | `218b249` | success; exact candidate fixture isolation, mechanical canonical-write rejection, unchanged-default stable rollback through compatible installed CLI, quiescence inventory, focused validation, and repeat strict review clean; shell CLI compatibility retained as non-blocking operational risk | `completed-slices.md`; `/tmp/ccfg-18-candidate-generation-fixture`; `git show --stat 218b249` |

## Slice 1: Candidate Roots And Strict Transition

Risk class: `migration`.

Scope:

- Re-run installed-helper bootstrap validation against the exact complete
  pre-creation payload while both targets remain absent.
- Compute a deterministic merge tree for authoritative master plus the accepted
  design snapshot and obtain independent read-only review before creation.
- Create exactly the candidate repository and candidate `CODEX_HOME` roots.
- Clone repository identity `alacasse/codex-config`, create
  `implementation/command-owner-redesign` from the exact base commit, and
  prepare the ancestry-preserving accepted-design merge.
- Verify the candidate merge tree equals the reviewed tree, then let the
  coordinator create the mechanical merge commit.
- Verify both required ancestors, imported design tree equality before live
  amendments, exact branch name, exact origin identity, and empty candidate
  `CODEX_HOME` directory identity.
- Build and preserve the versioned transition receipt, validate the first
  stable-controlled strict context, and obtain strict review of the exact merge
  commit before Slice 2.

Allowed paths:

- Pre-creation read-only inspection under
  `/home/alacasse/projects/codex-config`.
- Creation and repository writes under
  `/home/alacasse/projects/codex-config-command-owner-redesign`.
- Creation of the exact directory
  `/home/alacasse/.codex-command-owner-redesign`; no installed content yet.
- Coordinator-only planning evidence under this batch directory and program
  `CURRENT.md`/`LEDGER.md` after transition.

Non-goals:

- No live amendment or design evolution yet.
- No candidate feature installation or candidate session.
- No stable source change, default switch, canonical planning mutation from the
  candidate, or successor selection.

Acceptance criteria:

- Both roots were absent immediately before validated creation authority.
- Worker creation targets exactly equal the two authorized roots.
- Origin identity is exactly `alacasse/codex-config`; branch and base commit
  exactly match the payload.
- The merge commit has authoritative base and accepted design as ancestors; its
  tree equals the independently reviewed deterministic merge tree.
- Imported frozen design content matches the accepted snapshot before any live
  amendment.
- The installed stable helper produces an exact transition receipt and validates
  strict `cross-checkout-context/v1` against the actual merge commit.
- Creation-bearing worker evidence has pre-creation verification and null strict
  verification; post-transition reviewer evidence has strict verification and
  null pre-creation verification.
- No stable planning receipt commit occurs until transition and strict review
  are green.

Validation:

- Use the selected profile and the pre-creation/transition procedure in this
  runway.
- Run exact origin, branch, parent, ancestor, tree, root, and installed-helper
  identity checks.
- Run focused cross-checkout tests, stable install status/dry-run, planning-state
  current/validate, and task-scoped `git diff --check`.

Commit messages:

- Candidate merge: `Merge accepted command-owner redesign design`.
- Stable receipt: `Record CCFG-18 candidate transition receipt`.

Coding subagent brief:

- Use `runway_worker`. The worker is the required coding subagent, may create
  only the two exact authorized targets, must prepare only this slice, and must
  not spawn or wait on more agents. It must not accept commit, validation,
  review, ledger, closeout, or successor authority.

Review subagent briefs:

- Before creation, use `runway_reviewer` with the deterministic merge tree and
  exact source commits as `diff_basis`; require matching pre-creation identity.
- After transition, use a separate strict-context `runway_reviewer` with the
  exact candidate merge commit and ancestry/tree evidence as `diff_basis`.

Stop conditions:

- Stop on any payload, helper, absent-target, origin, branch, commit, tree,
  ancestry, result-field, permission, or review mismatch.
- Stop rather than commit stable planning state before transition.
- Stop before Slice 2 unless the strict transition and exact merge review are
  green.

## Slice 2: Candidate Amendment And Generation Install

Risk class: `migration`.

Scope:

- Regenerate and validate strict stable-controller context from exact current
  stable and candidate revisions before every handoff.
- Add the live pre-creation amendment explicitly to the imported candidate
  design tree without rewriting the frozen accepted snapshot or its history.
- Record the accepted snapshot, authoritative base, merge commit, candidate
  branch, stable controller, three roots, temporary bridge, and CCFG-29 deletion
  condition in the candidate design lineage.
- Review and commit the candidate amendment.
- Install all candidate manifest features into the separate candidate
  `CODEX_HOME` from the candidate repository after the candidate commit.
- Verify candidate installed versions and every installed candidate link, while
  re-verifying stable installed versions and links remain stable-only.
- Produce distinct candidate implementation and stable planning receipts with
  exact revisions and generation identities.

Allowed paths:

- Candidate design files under
  `/home/alacasse/projects/codex-config-command-owner-redesign/docs/design/command-owner-redesign/`.
- Candidate installation paths under
  `/home/alacasse/.codex-command-owner-redesign`.
- Coordinator-only planning evidence under the canonical stable planning root.

Non-goals:

- No command-owner production implementation.
- No stable feature changes or installation changes.
- No default switch, real candidate planning write, or branch retirement.

Acceptance criteria:

- The candidate amendment is explicit, traceable to the live stable amendment,
  and does not modify the immutable accepted snapshot history.
- Candidate commit is independently reviewed under a validated strict context.
- Candidate `CODEX_HOME` contains the complete manifest-owned feature set and
  every repo-owned link resolves only to the candidate repository at the
  reviewed candidate commit.
- Stable `CODEX_HOME` remains complete and every repo-owned link resolves only
  to the stable repository.
- Stable-controlled workers/reviewers report stable strict identity. No helper,
  schema, skill, agent, or reference resolves from candidate during stable
  coordination.
- Candidate implementation receipts and stable planning receipts are separate
  and bind exact repository revisions.

Validation:

- Run candidate and stable install status/dry-run, focused tests, manifest JSON,
  Ruff, basedpyright, strict-context/write-scope checks, planning-state
  current/validate, and task-scoped diff checks.
- Treat the full manifest command as known-red only for the exact three baseline
  wording failures; any new failure blocks the slice.

Commit messages:

- Candidate amendment: `Record live precreation amendment`.
- Stable receipt: `Record CCFG-18 candidate generation receipt`.

Coding subagent brief:

- Use `runway_worker` under freshly validated strict stable context. The worker
  edits only the candidate design amendment, must not install, validate, commit,
  update stable planning, spawn agents, or broaden into CCFG-19.

Review subagent brief:

- Use `runway_reviewer` with the exact candidate worktree diff before commit and
  echo that `diff_basis`. Review lineage truthfulness, immutable snapshot
  preservation, temporary-bridge ownership, and no command-owner implementation.

Stop conditions:

- Stop if strict identity is stale or mismatched before either handoff.
- Stop if candidate installation would overwrite a nonempty unmanaged home,
  requires secret copying, or creates stable/candidate mixed links.
- Stop if the live amendment changes accepted history or source code outside the
  candidate design tree.
- Stop if stable default installation changes.

## Slice 3: Fixture Isolation And Rollback Proof

Risk class: `evidence-only`.

Scope:

- Recreate a fixture-only Layout v1 planning root under
  `/tmp/ccfg-18-candidate-generation-fixture` without copying credentials or
  canonical active-state authority.
- Build and validate a candidate-generation strict context using candidate
  toolchain root, candidate `CODEX_HOME`, exact candidate commit, canonical
  stable planning revision, generation role `candidate`, and
  `canonical_state_mutation_allowed: false`.
- After runtime approval and authentication preflight, launch one ephemeral
  fresh candidate `codex exec` session confined to the fixture root. It must
  report candidate identity, use fixture planning only, and write output only
  below the fixture root.
- Mechanically prove a candidate canonical-planning write request is rejected;
  do not ask the candidate session to attempt a real canonical write.
- Compare stable planning and stable installed link/version state before and
  after the candidate session.
- Inventory selected, queued, active, and resumable old-generation state.
- Rehearse pre-cutover rollback by ceasing candidate-session use, launching or
  validating the unchanged stable generation against fixture-only input, and
  proving no default binding or canonical state restoration is required.
- Produce the final CCFG-18 evidence and same-batch closeout without selecting
  CCFG-19.

Allowed paths:

- Ephemeral fixture and session output below
  `/tmp/ccfg-18-candidate-generation-fixture`.
- Read-only candidate repository/home and stable repository/home inspection.
- Coordinator-only canonical planning evidence and closeout writes.

Non-goals:

- No candidate source edit or implementation commit.
- No candidate-controlled canonical planning write.
- No default generation switch, real migration batch, or successor planning.
- No credential copying or persistence.

Acceptance criteria:

- Fresh candidate session reports candidate toolchain/home identity and writes
  only fixture state.
- Candidate strict context rejects canonical planning mutation mechanically.
- Stable planning current/validate remain green; no unexpected stable or
  candidate source diff exists.
- Stable default installed versions and link targets are identical before and
  after candidate validation.
- Candidate installed versions/links remain candidate-only and ready for later
  fixture validation work.
- Selected, queued, active, and resumable old-generation state is explicitly
  inventoried; closeout leaves all active batch state null.
- Rollback evidence proves the stable generation remains immediately usable and
  candidate use can stop without repairing canonical planning state.
- CCFG-18 acceptance evidence is complete; CCFG-19 remains unselected.

Validation:

- Run the fresh candidate fixture session, strict negative write-scope proof,
  stable/candidate install status and dry-run, stable planning-state
  current/validate, exact Git status/revision checks, focused tests, and final
  diff checks.
- Read the candidate session last-message artifact and exact transition/
  cross-repository receipts before reporting success.

Commit message:

- Stable evidence receipt: `Record CCFG-18 candidate isolation proof`.
- Final closeout: self-referential closeout commit with `this closeout commit`
  in the closeout artifact.

Coding subagent brief:

- Use `runway_worker` as an evidence preparer under strict stable context. It may
  prepare only the ephemeral fixture and deterministic candidate-session prompt;
  it must not launch nested agents, mutate source, copy credentials, write
  canonical planning, commit, close out, or select successor work.

Review subagent brief:

- Use `runway_reviewer` with the exact fixture/session output, stable/candidate
  identity receipts, canonical rejection evidence, state inventory, and
  task-scoped stable planning diff as `diff_basis`. Require explicit confirmation
  that no candidate canonical write or default switch occurred.

Stop conditions:

- Stop if fresh candidate authentication requires unauthorized credential
  copying or if the cost-bearing session lacks runtime approval.
- Stop if the sandbox exposes a canonical planning write path to the candidate.
- Stop on any stable/candidate identity mixture, canonical mutation, unexpected
  source diff, non-fixture session write, or incomplete rollback evidence.
- Stop after same-batch CCFG-18 reconciliation; do not select CCFG-19.

## Final Validation And Closeout

After Slice 3, the coordinator must:

1. Revalidate stable and candidate strict identities, exact revisions, branch,
   origin, ancestry, and installed link maps.
2. Re-run required-green focused tests, Ruff, basedpyright, installer status and
   dry-run commands, planning-state `current`/`validate`, manifest JSON, and
   diff checks in the appropriate repositories.
3. Record the known-red full manifest baseline separately and prove no new
   touched-scope failure.
4. Read the transition receipt, cross-repository receipts, candidate session
   summary, canonical-write rejection, quiescence inventory, rollback proof,
   worker/reviewer results, and commit receipts.
5. Obtain an independent final `runway_reviewer` review over the exact candidate
   commit range plus stable planning diff.
6. Write `closeout.md`, move completed rows out of the active ledger, record any
   cleanup residues and `orchestration_anomalies`, and commit the self-referential
   closeout.
7. Reconcile only CCFG-18 through `architecture-program-runway closeout-runway`:
   clear selected/queued/active state, set latest closeout, and mark CCFG-18
   `Closed` only if every acceptance item is proven.
8. Stop with CCFG-19 still unselected.

## Batch Stop Conditions

- Stop on scope drift, dirty-file conflict, missing registered worker/reviewer,
  missing permission, network failure, missing fresh-session authentication,
  or repeatedly unresolved validation/review failure.
- Stop if the complete pre-creation payload cannot be revalidated before Slice
  1 or if either target appears early.
- Stop if strict transition is missing, stale, or mismatched after creation.
- Stop if stable planning artifacts are committed before transition.
- Stop if any candidate write escapes the candidate root or any planning write
  escapes the canonical planning root.
- Stop if candidate code, helper, or session controls real planning state.
- Stop if the default generation switches or stable links change.
- Stop if accepted design ancestry or immutable content cannot be proven.
- Stop if the full manifest diagnostic adds a touched-scope failure beyond its
  exact known-red baseline.
- Stop if closeout would hide unresolved CCFG-18 evidence, create a new finding,
  or select CCFG-19.

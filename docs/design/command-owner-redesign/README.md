# Command-Owner Workflow Redesign

## Status

```yaml
status: accepted-post-review-design
implementation_authorized: false
intake_completed: true
selected_redesign_item: null
queued_redesign_runway: null
active_redesign_runway: null
repository: alacasse/codex-config
original_design_snapshot: b3f31c44a1fc3287c33dd2955489f194afef66f6
live_intake_commit_on_master: 7356a3fd9d8d487be8562af11cad56170f300616
design_branch: architecture/command-owner-redesign
next_controlled_action: amend_live_CCFG_18_then_plan_exactly_one_batch
```

This package defines the accepted target architecture and migration constraints
for the `codex-config` ledger and batch workflow skills.

The original snapshot at `b3f31c44a1fc3287c33dd2955489f194afef66f6`
remains immutable provenance. This branch contains the accepted post-intake
amendments. After these amendments are frozen, the implementation branch must
start from the latest authoritative `master` and merge the accepted design
history with preserved ancestry.

The live executable program remains on `master` under:

```text
docs/plans/programs/codex-config/CURRENT.md
docs/plans/programs/codex-config/LEDGER.md
docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md
```

This design package is not a dispatch, runway, or permission to implement. The
normal command boundary remains:

```text
add-to-ledger
  -> plan-batch
  -> work-batch
  -> same-batch closeout
  -> later fresh plan-batch
```

## Objective

Replace the current bridge architecture with three true human-facing workflow
owners:

```text
add-to-ledger
  owns intake, source identity, normalization, duplicate/merge/no-op decisions,
  and canonical ledger mutation

plan-batch
  owns eligibility, selection, scope shaping, dispatch content, runway design,
  risk, approval gates, and validation-profile selection

work-batch
  owns execution, recovery, validation acceptance, independent review,
  commit acceptance, finalization, closeout, and same-batch reconciliation
```

Shared components may inspect, validate, resolve, serialize, apply an explicit
decision, execute a command, commit accepted work, or produce evidence. They may
not reinterpret the human workflow or become alternate owners.

The final target deletes:

```text
skills/architecture-program-runway/
skills/batch-runway/
```

without replacing them with another broad hidden orchestrator.

## Authority Order

For work in this program, use this order:

```text
accepted decisions in decisions.md
-> current live ledger item and local intake on master
-> current migration phase in 04-migration-program.md
-> stable behavior contracts
-> target ownership model
-> selected dispatch and runway, when one exists
-> repository source evidence
-> historical plans and issues
```

The original design snapshot is provenance. The amended branch is the current
design source until it is merged into an implementation branch. `master` remains
the canonical planning authority before cutover.

## Package Contents

| Document | Authority |
|---|---|
| `01-source-behavior-contracts.md` | Implementation-neutral behavior that must be preserved or deliberately changed. |
| `02-target-ownership-model.md` | Target owners, narrow mechanisms, three-root topology, and dependency rules. |
| `03-contract-first-formats.md` | Skill and planning-artifact contracts, schema evolution, and `skill-authoring` rules. |
| `04-migration-program.md` | Ledger-item sequence, entry/exit gates, two-generation control, cutover, and rollback. |
| `05-behavioral-test-matrix.md` | Behavior, generation-isolation, fault-injection, cutover, and deletion scenarios. |
| `06-deletion-conditions.md` | Reproducible proof required to remove APR, Batch Runway, stale routes, and migration bridges. |
| `07-implementation-ledger-intake.md` | Individually addressable work items COR-001 through COR-012; not a batch map. |
| `08-review-resolution.md` | Resolution of the independent review findings and accepted post-intake amendments. |
| `09-live-precreation-amendment.md` | Live CCFG-18 pre-creation amendment and exact candidate lineage. |
| `10-ccfg-19-contract-verification-and-decisions.md` | Live CCFG-19 candidate amendment joining contract, owner, scenario, and test evidence; later approved decisions are recorded here. |
| `decisions.md` | Accepted, superseded, open, deferred, and rejected decisions. |

## Three-Root Bootstrap Topology

Before cutover, every real migration operation uses three explicit roots:

```yaml
toolchain_source_root:
  owner: stable checkout on authoritative master
  contains:
    - loaded stable skills
    - controlling scripts
    - schemas and references used by the stable controller
    - worker and reviewer contracts used by the stable controller

canonical_planning_repository_root:
  owner: stable checkout on authoritative master
  contains:
    - CURRENT.md
    - LEDGER.md
    - selected dispatch
    - queued or active runway
    - closeout and reconciliation evidence

implementation_target_root:
  owner: separate candidate clone
  contains:
    - candidate skills
    - candidate scripts and schemas
    - candidate tests and fixtures
    - migration implementation commits
```

The first two roots may be the same physical checkout. The implementation target
must be a separate clone by default. A worktree is allowed only after explicit
validation.

No command may infer these roots solely from the current working directory.
Planning writes must resolve under the canonical planning root. Implementation
writes, Git diff, validation, and implementation commits must resolve under the
candidate root. Stable controlling scripts, references, and agent contracts must
resolve from the stable toolchain root.

## Generation Identity

Every controller, worker, reviewer, runner phase, validation result, and closeout
must carry a mechanically verified generation record:

```yaml
generation:
  role: stable | candidate
  codex_home: absolute-path
  toolchain_source_root: absolute-path
  toolchain_commit: full-sha
  canonical_planning_repository_root: absolute-path
  implementation_target_root: absolute-path
  canonical_state_mutation_allowed: true | false
  child_process_inheritance: required
```

During CCFG-18, absolute roots, full commits, resolved installed links, and
`CODEX_HOME` are mandatory. Manifest and per-contract hashes become mandatory by
cutover.

A mismatch blocks before writes or delegation.

## Branch and Design Lifecycle

The implementation branch must be created from the latest authoritative
`master`, which contains the current ledger intake. It then merges the accepted
design history with preserved ancestry.

```text
latest authoritative master
  -> create implementation branch
  -> merge --no-ff accepted design history
  -> verify imported design tree
  -> continue candidate implementation and design amendments there
```

Authoritative links use immutable commit URLs. Mutable branch URLs are navigation
only.

Before cutover:

```text
master
  = canonical planning authority

implementation branch
  = candidate design and code authority
```

After CCFG-28, the implementation branch may remain the candidate toolchain
source while `master` remains the canonical planning repository. CCFG-29 owns the
final quiescent merge into `master`, rebinding of the default toolchain to
`master`, and removal of the temporary cross-checkout bridge.

## Contract-First Authoring Bootstrap

Before migrating `add-to-ledger`, `plan-batch`, or `work-batch`:

1. `skill-contract/v1` is accepted and mechanically validated.
2. `skill-authoring` v1 is complete and authoritative for hybrid skill structure,
   ownership, canonicality, references, migration, and ambiguity reporting.
3. It is validated on one narrow evidence or analysis skill and one branching
   command-like skill.
4. Planning-artifact authoring guidance is a conditionally loaded reference under
   the same skill and version.
5. Candidate trials use the candidate `CODEX_HOME` and fixture-only planning.

`skill-authoring` is an authoring-time support skill, not a runtime dependency of
the command owners.

## Program Invariants

- The twelve redesign items remain individually addressable in the canonical
  ledger.
- `add-to-ledger` may ingest many items; `plan-batch` selects or shapes at most
  one runnable batch.
- Exactly one dispatch/runway may be selected, queued, or active.
- No real batch is controlled by more than one toolchain generation.
- Stable-controlled batches reach same-batch closeout before candidate-controlled
  canonical work begins.
- Candidate sessions are validation-only before cutover.
- Every temporary bridge has a caller, reason, owner, allowed scope, and deletion
  condition.
- Ownership-transfer work removes the corresponding legacy decision path.
- `work-batch` closeout never selects successor work.
- Cutover occurs only at quiescent state.
- Rollback after candidate-format canonical writes restores installation, code,
  planning state, and active artifacts to one compatible checkpoint.
- Historical artifacts remain evidence, not active pickup authority.

## Current Next Safe Action

Do not repeat intake. CCFG-18 through CCFG-29 already exist on `master` and remain
unselected.

Before `plan-batch CCFG-18`:

1. amend the live CCFG-18 scope and affected dependencies on `master`;
2. replace mutable authoritative design links with an immutable accepted design
   commit link;
3. verify a fresh stable session, installed stable generation, and planning
   quiescence;
4. provide explicit values for the stable checkout, candidate clone path,
   candidate `CODEX_HOME`, and design commit.

Then invoke `plan-batch` for CCFG-18 only. CCFG-18 owns creation of the candidate
clone, implementation branch, accepted design merge, candidate `CODEX_HOME`,
temporary cross-checkout support, generation fingerprinting, fixture-only
candidate validation, and pre-cutover rollback proof.

# CCFG-26B Slice Progression Authority Correction

## Status And Precedence

- Status: substitutive planning-design correction; implementation has not
  started.
- Applies to: the already queued `ccfg-26b-fresh-slice-flight` batch.
- Queue effect: none. The queued path remains `runway.md` in this directory.
- Slice effect: none. The accepted amendment still defines exactly Slice 1
  followed by Slice 2.
- Precedence: this correction controls only amended-slice progression,
  completion recording, and the related validation/mutation order. The accepted
  amendment controls every other scope, ownership, validation, and stop rule.
- Review gate: this correction controls execution only when
  `progression-authority-review.md` records a clean verdict for its exact
  SHA-256.

The original dispatch, runway, review, amendment, and amendment review remain
immutable evidence:

```yaml
immutable_evidence:
  dispatch_sha256: 8b29b566fd743af4ecdbe555f1cf66bb29871b081bc25f7aa0fc9780ce1069d8
  runway_sha256: 8da8e0d1b0cd18d75289a1a0954b33078dd17ef6a328d2bb6a46a9404076b5ca
  review_sha256: e37e0678c663a44c99b642454fa4fc6b840bc59174c8df6727d10bb02ad2f45f
  amendment_sha256: 2ec8981e8ac6c088d7d5f4435f2638ea94346bd921b04609938e43e29a6787d8
  amendment_review_sha256: a9cba89a76155df757de9005e88a32b47f0cec3bba54f89566803caf231b3473
immutable_candidate_baseline: 5c5ec9d52dd9033daa45f3a200031c152363b62c
canonical_planning_commit_before_correction: ae24dcaccf55de191e51f2599384dae65ae62a29
```

## Defect Being Corrected

The accepted amendment defines two ordered slices and says completed details
move to `completed-slices.md`, but it does not define one deterministic live
progression rule after a fresh process boundary:

- its `Amended Execution Ledger` is immutable reviewed plan evidence, so its
  permanently `pending` cells cannot be updated or treated as live state;
- `completed-slices.md` is currently absent because implementation has not
  started;
- Standard Ledger Retention v1 describes archive movement but does not validate
  known IDs, uniqueness, order, a contiguous prefix, or receipt/commit
  consistency;
- the current runner state, artifact maps, and validator are phase-keyed and do
  not determine amended-slice progress; and
- `next_action.next_slice_id`, candidate Git movement, Planning State queue
  currentness, or several documents read informally would each be an incomplete
  or competing authority.

This correction makes one existing planned artifact the sole mutable
completion authority and makes every consumer use the same completed-prefix
rule. It adds no store, state, public schema, slice, or lifecycle dialect.

## Slice Progression Authority

```yaml
slice_progression_authority:
  immutable_inventory:
    owner: amendment.md
    exact_sha256: 2ec8981e8ac6c088d7d5f4435f2638ea94346bd921b04609938e43e29a6787d8
    ordered_slice_ids:
      - "1"
      - "2"
    definitions:
      "1": Slice 1 - Transfer One Successful Flight And Stop Durably
      "2": Slice 2 - Automate Fresh Same-Batch Continuation
    mutation_policy: immutable after the accepted clean amendment review
    status_cells: historical plan-time state only; never live progression
  mutable_completion_record:
    owner: completed-slices.md
    semantic_owner: work-batch
    physical_writer: the runner's already planned persistence path after validating the work-batch-authored receipt, exact commit, focused validation, independent review, and runner-owned post-exit observation
    mutation_policy: absent means an empty archive only under the initial-state rule; create atomically for Slice 1; append exactly one complete entry for each later accepted slice; never edit, delete, reorder, or duplicate an accepted entry
  transition_evidence:
    owner: work-batch-authored batch-execution-flight/v1 receipt
    role: exact evidence for one attempted or completed transition; never an independent slice inventory or completion ledger
  next_slice_derivation:
    semantic_owner: public work-batch command
    mechanical_validator: scripts/architecture_program_runner_validation.py
    rule: validate the archive as a contiguous prefix of amendment.md, then choose the first amended slice ID absent from that prefix
  material_integrity:
    git_role: prove the exact accepted implementation and rollback boundary only; never infer pending, active, completed, queued, or successor state
  forbidden_competing_authority:
    - chat history or model interpretation
    - candidate commit count or ancestry alone
    - receipt next_slice_id without archive validation
    - mutable edits to amendment.md or its permanently pending cells
    - CURRENT.md, LEDGER.md, or Planning State as slice-level completion state
    - runner inference from phase chronology, state phase, manifest order, or file presence alone
```

`completed-slices.md` is the only mutable semantic slice ledger. The immutable
inventory plus that mutable archive form the complete progression authority;
the receipt and runner artifacts are validated evidence referenced by an
archive entry, not additional ledgers.

No durable `active` slice state is added. Between invocations, no slice is
active. During one invocation, `work-batch` derives exactly one active slice as
the next pending slice and binds that ephemeral fact to the flight receipt and
fresh strict live lease. The amendment's other absent slices remain pending.
After the process ends, the slice is either in the accepted completed prefix or
remains pending; a blocked or failed receipt does not advance the prefix.

## Canonical Completion Entry

The first accepted slice creates `completed-slices.md` in this batch directory.
Each accepted slice contributes exactly one append-only entry carrying all of
these facts in a deterministic, directly readable block:

```yaml
slice_id: "1" | "2"
inventory:
  amendment_path: amendment.md
  amendment_sha256: sha256
candidate:
  before: full-git-sha
  after: full-git-sha
commit_receipt:
  commit: full-git-sha
  path: string
  sha256: sha256
flight_receipt:
  path: string
  sha256: sha256
  status: completed
validation:
  summary: non-empty-string
  evidence_paths: [string]
  evidence_sha256: [sha256]
review:
  verdict: clean
  evidence_path: string
  evidence_sha256: sha256
runner_observation:
  path: string
  sha256: sha256
  observed_codex_session_id: non-empty-string
runner_evidence:
  input_inventory_path: string
  input_inventory_sha256: sha256
  telemetry_path: string
  telemetry_sha256: sha256
next_action:
  kind: continue_same_batch | finalize_same_batch
  next_slice_id: "2" | null
material_integrity:
  expected_candidate_head_after_entry: full-git-sha
```

The entry also retains the accepted amendment's other requested actuals except
final Run State and batch-manifest digests. Those two artifacts acquire the
accepted transition only after the archive append and therefore belong in the
derived post-transition execution report and runner artifacts, not in the
authoritative completion entry. Other extra audit facts and the required runner
evidence above do not affect the slice-progression algorithm. Missing required
pre-transition evidence still blocks acceptance of the entry; none of it
becomes another source of slice order or status.

The physical order is exact:

1. `work-batch` authors and atomically writes the flight receipt, including the
   semantic slice, acceptance, commit, and next-action facts, and then exits.
2. The runner records the runner-owned post-exit observation.
3. The runner validates receipt byte equality, the expected derived slice, the
   commit, focused validation, independent review, observation, input
   inventory, and telemetry evidence.
4. The runner mechanically constructs the archive entry from those already
   fixed facts and atomically creates or appends `completed-slices.md`.
5. The runner re-reads the archive, revalidates the completed prefix and exact
   receipt action, and only then applies the mechanical transition.
6. Run State and batch manifests are written as derived post-transition
   reporting and are cross-checked against the accepted receipt/archive on the
   next validation pass.

The runner may not choose or correct a slice, action, commit, validation result,
or review result.

This order is required because the actual session identity, exit evidence, and
observation digest do not exist until after the `work-batch` subprocess exits.
A process failure between receipt creation, observation, and archive append
leaves contradictory evidence and therefore blocks the next invocation;
CCFG-26B does not repair or infer through that state.

## Deterministic Completed-Prefix Rule

Every fresh `work-batch` invocation and the runner validator must use this exact
algorithm before delegation, persistence, or transition:

1. Verify the immutable amendment and accepted amendment-review digests, this
   correction, and its clean review.
2. Read the ordered inventory `("1", "2")` from `amendment.md` as bound above.
3. If `completed-slices.md` is absent, accept an empty archive only when all of
   these initial facts agree: there is no prior CCFG-26B flight receipt or
   archive reference in the bounded runner evidence, and candidate HEAD equals
   `5c5ec9d52dd9033daa45f3a200031c152363b62c`. Otherwise block.
4. If the archive exists, parse every complete entry and reject an unknown ID,
   duplicate ID, missing required field, non-clean review, non-completed flight,
   mismatched amendment digest, or unreadable/missing referenced evidence.
5. For each entry, validate the exact flight receipt, candidate before/after,
   commit receipt, focused validation evidence, and independent review evidence.
   The commit named by `candidate.after`, `commit_receipt.commit`, and the
   flight receipt must be identical.
6. Require archive IDs to equal a contiguous prefix of `("1", "2")` in that
   order. No gap, reorder, or later-slice-only entry is valid.
7. Require the candidate chain to be contiguous: Slice 1 `before` equals the
   immutable candidate baseline; each later `before` equals the prior entry's
   `after`; current candidate HEAD equals the last entry's `after`, or the
   immutable baseline for an empty prefix.
8. Derive `next_slice_id` as the first inventory ID after the validated prefix.
   The result is `"1"`, `"2"`, or `null` when both slices are complete.
9. When the latest completed receipt carries `next_action`, require
   `continue_same_batch` plus the independently derived non-null ID, or
   `finalize_same_batch` plus `null` after the full prefix. Any disagreement
   blocks.
10. Bind the derived non-null ID to the one current flight and fresh strict live
    lease. No other amended slice may be delegated or treated as active.

This validation is fail-closed. CCFG-26B does not repair, discard, rewrite, or
choose among contradictory durable facts. A mismatch returns `require_user`
before delegation; recovery and amendment behavior remain with CCFG-26C.

## Producer, Validator, And Consumer Responsibilities

| Surface | Classification | Writer | Validator / consumer |
|---|---|---|---|
| `amendment.md` | authoritative immutable inventory | historical planning author only | `work-batch` verifies its accepted digest; runner validator consumes the bound order |
| `completed-slices.md` | authoritative mutable completion state | runner persistence path, mechanically after the work-batch-authored receipt and post-exit observation validate | `work-batch` and runner validator enforce entry integrity and contiguous prefix |
| `batch-execution-flight/v1` receipt | transition evidence | `work-batch` coordinator | runner validates exact content, archive agreement, candidate chain, and derived action |
| candidate commit and commit receipt | material-integrity evidence | coordinator / Git | `work-batch` and runner require exact equality with receipt and archive |
| focused validation and independent review evidence | acceptance evidence | validation and reviewer owners | `work-batch` validates before archive append; runner rejects a completed transition without it |
| runner Run State and batch manifests | derived post-archive reporting | runner after mechanical transition | cross-checked against accepted receipt/archive on the next validation pass; never choose slice status |
| runner inventories, observations, and telemetry | transition evidence | runner before archive append | cross-checked with receipt/archive paths; never define inventory or completion |
| `CURRENT.md`, `LEDGER.md`, Planning State | authoritative batch currentness; derived slice reporting only | existing planning owners | confirm this same queued batch, not amended-slice progress |
| `dispatch.md`, `runway.md`, `review.md`, `amendment-review.md` | intentionally retained immutable evidence | none during execution | digest and scope basis only |
| amendment `pending` cells | historical plan-time status | none | forbidden as live progression input |
| phase chronology, candidate movement alone, receipt action alone | forbidden lifecycle inference | none | must block if offered as progression authority |

`scripts/architecture_program_runner_state.py` and
`scripts/architecture_program_runner_artifacts.py` may retain and report the
validated receipt/archive references after transition in their already planned
Slice 1 and Slice 2 changes. Those post-transition files are derived reporting,
not inputs to the archive append, and they do not select a slice. After
`scripts/architecture_program_runner_validation.py` accepts the independently
derived action, `scripts/architecture_program_runner_transition.py` may only
apply that exact action mechanically.

## Replay, Skip, And Concurrency Protection

- Replay prevention: an accepted Slice 1 entry places `"1"` in the validated
  prefix, so `work-batch` can derive only `"2"`; a receipt requesting `"1"`
  blocks. Candidate HEAD must also equal Slice 1's accepted `after` commit.
- Skip prevention: with an empty archive, only `"1"` derives; `"2"` cannot be
  delegated. With Slice 1 archived, Slice 2 derives only after every Slice 1
  receipt, commit, validation, and review reference validates.
- Two-active-slice prevention: there is one derived next ID and one current
  flight binding. The runner validates that binding before launch and rejects
  any different slice ID. No durable multi-active status exists.
- Duplicate-flight protection: a second completion entry for an already
  archived ID is invalid even if it names a different receipt or commit.
- Candidate-movement protection: current HEAD must equal the expected head from
  the validated prefix before delegation. Git proves material identity only;
  it never advances the prefix.

## Required Counterfactual Tests

Use the strongest real producer-to-consumer path available: immutable
amendment plus real archive parsing, public `work-batch` result production,
receipt persistence, runner validation, and transition consumption. A fixture
that directly injects final derived state is insufficient.

| Case | Required result |
|---|---|
| A. Slice 1 archive entry and receipt agree | derive Slice 2 |
| B. No completion entries, no prior flight evidence, and baseline HEAD | derive Slice 1 |
| C. Slice 1 receipt exists but archive entry is absent | block before delegation |
| D. Slice 1 archive entry exists but accepted receipt is absent | block before delegation |
| E. Slice 1 archive entry references the wrong candidate commit | block before delegation |
| F. Receipt names Slice 1 after Slice 1 completion | block before persistence or relaunch |
| G. Receipt skips to an unknown or successor slice | block before persistence or relaunch |
| H. Slice 2 is archived before Slice 1 | block before delegation |
| I. Duplicate Slice 1 archive entries | block before delegation |
| J. Both slices are complete | derive `finalize_same_batch` handoff, not another implementation slice |
| K. Candidate HEAD moved outside the accepted transition | block before delegation |
| L. Final runner state is manufactured without matching work-batch receipt and archive | block on the next validation pass; derived state cannot manufacture completion |

These cases extend the existing Slice 1 and Slice 2 focused validation. They do
not add an implementation slice or a new test-only lifecycle surface.

## Planning And Execution Mutation Rules

### This Planning-Only Correction

May change only:

- `progression-authority-correction.md`;
- `progression-authority-review.md` after independent review; and
- program `CURRENT.md` and `LEDGER.md` only to bind this exact correction and
  clean review to the unchanged queued runway.

It must not create `completed-slices.md`, a receipt, runner state, or candidate
implementation change. Until implementation begins, absence of
`completed-slices.md` represents the initial empty archive only under the
initial-state rule above.

### Slice 1 Execution

May change only:

- the existing amended Slice 1 candidate implementation/test/doc/metadata
  ceiling;
- `completed-slices.md`, created atomically with exactly the accepted Slice 1
  entry by the runner's validated post-exit persistence step;
- the exact work-batch flight receipt and the already planned execution report,
  which records derived final Run State and batch-manifest references after the
  authoritative archive append; and
- runner-owned external Run State, receipt, manifest, inventory, observation,
  and telemetry artifacts at their preallocated paths.

Program `CURRENT.md`, `LEDGER.md`, `dispatch.md`, `runway.md`, `review.md`,
`amendment.md`, `amendment-review.md`, this correction, and its review remain
unchanged. The queue remains CCFG-26B and no successor is selected.

### Slice 2 Execution

May change only:

- the existing amended Slice 2 candidate implementation/test/doc/metadata
  ceiling;
- `completed-slices.md`, append-only with exactly the accepted Slice 2 entry;
  the runner performs the append only after the second receipt and post-exit
  observation validate;
- the exact work-batch flight receipt and the already planned execution report,
  which records derived final Run State and batch-manifest references after the
  authoritative archive append; and
- runner-owned external Run State, ordered receipts, manifests, inventories,
  observations, and telemetry artifacts at their preallocated paths.

The same immutable planning and queue surfaces remain unchanged. Final
validation and closeout remain later same-batch gates and are not Slice 2.

## Invariants

1. `amendment.md` continues to define exactly Slice 1 followed by Slice 2.
2. Completion survives process termination only through the validated
   append-only `completed-slices.md` record.
3. Completed entries form a contiguous prefix of the immutable order.
4. Slice 2 cannot start without Slice 1's validated accepted completion entry.
5. Slice 1 cannot execute again after that entry exists.
6. Git movement alone cannot complete a slice.
7. A receipt cannot complete a slice without matching archive, commit,
   validation, and independent review evidence.
8. Receipt `next_slice_id` must equal the independently derived next ID.
9. Missing or contradictory receipt evidence blocks.
10. Unknown, duplicate, or out-of-order archive entries block.
11. Candidate HEAD mismatch blocks before delegation.
12. A fresh process needs only canonical planning files, the compact archive
    entries, referenced compact receipts/evidence, Planning State, and a fresh
    strict lease.
13. Prior chronology, transcripts, raw logs, and accepted review detail are not
    progression inputs.
14. No new store, lifecycle state, schema dialect, or alternate runway identity
    is introduced.
15. The runner validates and consumes mechanically; it never chooses semantic
    slice state.

## Proportionality Forecast

```yaml
expected_changed_planning_files: 4
new_persistent_artifacts: []
new_lifecycle_states: []
new_public_contracts: []
implementation_slice_count: 2
implementation_started: false
```

The four forecast paths are this correction, its independent review, program
`CURRENT.md`, and program `LEDGER.md`. This correction does not authorize
candidate implementation, `work-batch` execution, queue mutation, finalization,
closeout, recovery, successor selection, or any CCFG-26C through CCFG-29 work.

## Stop Conditions

- Stop if the immutable amendment cannot remain the sole ordered inventory.
- Stop if `completed-slices.md` cannot remain the sole mutable completion
  authority using the existing batch-local archive convention.
- Stop if the design requires a new execution store, public schema, lifecycle
  state, third implementation slice, mutable runway, or alternate batch ID.
- Stop if any consumer may derive progression from Git, phase chronology,
  receipt action alone, chat history, or the amendment's static status cells.
- Stop if the independent review is not clean.
- Stop if candidate implementation or `work-batch` execution begins during
  this correction.

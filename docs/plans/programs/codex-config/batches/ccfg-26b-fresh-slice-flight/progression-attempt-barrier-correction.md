# CCFG-26B Progression Attempt Barrier Correction

## Status And Precedence

- Status: substitutive planning-design correction; implementation has not
  started.
- Applies to: the already queued `ccfg-26b-fresh-slice-flight` batch.
- Queue effect: none. The queued path remains `runway.md` in this directory.
- Slice effect: none. The accepted amendment still defines exactly Slice 1
  followed by Slice 2.
- Candidate effect: none. The immutable candidate baseline remains
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`.
- Precedence: this correction replaces only the progression-authority
  correction's completed-slice document grammar, derivation order, physical
  write order, and classification of the batch manifest as wholly derived
  post-transition reporting. The `execute_flights` section of that existing
  manifest is instead a prelaunch negative attempt barrier. Every other accepted
  scope, positive authority, ownership, validation, and stop rule remains in
  force.
- Review gate: this correction controls execution only when
  `progression-attempt-barrier-review.md` records a clean verdict for its exact
  SHA-256 and program `CURRENT.md` and `LEDGER.md` bind the exact correction and
  review digests to the unchanged queue.

The original dispatch, runway, reviews, amendment, and first progression
correction remain immutable evidence:

```yaml
immutable_evidence:
  dispatch_sha256: 8b29b566fd743af4ecdbe555f1cf66bb29871b081bc25f7aa0fc9780ce1069d8
  runway_sha256: 8da8e0d1b0cd18d75289a1a0954b33078dd17ef6a328d2bb6a46a9404076b5ca
  review_sha256: e37e0678c663a44c99b642454fa4fc6b840bc59174c8df6727d10bb02ad2f45f
  amendment_sha256: 2ec8981e8ac6c088d7d5f4435f2638ea94346bd921b04609938e43e29a6787d8
  amendment_review_sha256: a9cba89a76155df757de9005e88a32b47f0cec3bba54f89566803caf231b3473
  progression_authority_correction_sha256: b7dbe71f2b8eaa0bff76c14a21a1e08fb5c73c8b2d1b015741b37766ce06cf2a
  progression_authority_review_sha256: 7044c8afd1119919902e26cd22e1974a8b52b6549f347c1c85942fa99775dfce
immutable_candidate_baseline: 5c5ec9d52dd9033daa45f3a200031c152363b62c
canonical_planning_commit_before_correction: fb0d72041c10a29150d94f5da53a878d3159f553
```

Repository HEAD
`e0825c57f4abef2ec2a95ee8a4beafed21c16bd5` adds only the repository-local
Graphify suspension after that canonical planning commit. It does not change
the accepted CCFG-26B planning bytes or candidate baseline.

## Defect Being Corrected

The accepted positive model can distinguish completed slices, but it cannot
distinguish a never-launched slice from a launched flight whose receipt or
archive transition was interrupted. Deriving only from the completed prefix
could therefore authorize a second launch for the same slice after a fresh
process boundary.

One durable flight attempt that is not referenced by exactly one accepted
`completed-slices.md` entry is unresolved. It blocks before all later slice
derivation and delegation whether its receipt is absent, malformed, `blocked`,
`failed`, or `completed` without the accepted archive entry. The same rule
applies to a terminal Slice 2 attempt after Slice 1 is archived.

## Existing Batch Manifest Location

No new attempt artifact is introduced. CCFG-26B uses the runner-owned batch
manifest already required by the queued runway for ordered receipt and telemetry
retention.

The existing runner path functions are:

```python
artifact_root = (
    project
    / Path(program_ledger).parent
    / "architecture-program-runs"
    / ledger_slug(program_ledger)
    / run_id
)
batch_manifest_path = (
    f"{state['artifact_root']}/batches/"
    f"{slugify_path_component(batch_id)}/batch-manifest.json"
)
```

For CCFG-26B with the canonical program ledger, the exact existing path template
is:

```text
docs/plans/programs/codex-config/architecture-program-runs/LEDGER/run-YYYYMMDD-HHMMSS/batches/ccfg-26b-fresh-slice-flight/batch-manifest.json
```

`run-YYYYMMDD-HHMMSS` is the existing `new_run_id()` rendering, not a caller-
chosen manifest placeholder. The first runner process persists that exact
`run_id`, `artifact_root`, and `batch_manifest_path` in its existing
`run-state.json`. Every later runner process for this CCFG-26B flight chain must
use `--resume` together with that exact existing `--state .../run-state.json`
path, validate `active_batch_id` as `ccfg-26b-fresh-slice-flight`, and then
require:

```python
state["batch_manifest_path"] == (
    f"{state['artifact_root']}/batches/"
    "ccfg-26b-fresh-slice-flight/batch-manifest.json"
)
```

The runner must not locate this manifest by scanning for manifests or receipts.
Bare `--resume` latest-run discovery is also insufficient because a newer run
can shadow the attempt-bearing run. Starting a new run after the CCFG-26B chain
is bound is forbidden. If the exact state path is not carried forward, or that
state is absent, ambiguous, malformed, names another batch, or yields any other
manifest path, progression returns `require_user` before derivation or
delegation. The existing exact state path and its manifest path are sufficient
to locate the same ordered attempt index across fresh invocations without a new
locator artifact.

Implementation evidence for this existing path contract is
`scripts/architecture_program_runner_state.py` (`resolve_state_path`,
`default_artifact_root`, `batch_artifact_root`, and `batch_manifest_path`) and
`scripts/architecture_program_runner_artifacts.py` (`write_batch_artifacts` and
`build_batch_manifest`).

## Authority Model

```yaml
positive_progression_authority:
  immutable_inventory:
    artifact: amendment.md
    slice_order:
      - "1"
      - "2"
  mutable_completion_authority:
    artifact: completed-slices.md
    rule: accepted entries form one contiguous prefix of the immutable order
  next_slice:
    rule: first immutable slice ID absent from the validated completed prefix
negative_progression_barrier:
  artifact: existing runner-owned batch manifest already required by CCFG-26B
  section: execute_flights
  role: ordered flight-attempt index only
  semantic_effect:
    - it never marks a slice completed
    - it never chooses the next slice
    - an unreferenced attempt blocks any new derivation or delegation
  forbidden_substitutes:
    - filesystem globbing for receipt files
    - chat history
    - phase chronology
    - candidate Git movement
    - receipt next_action alone
    - Run State phase alone
    - existence of completed-slices.md alone
```

The positive and negative roles do not compete. `completed-slices.md` alone may
prove completion. `execute_flights` can only prove that a launch was authorized
and veto new progression until the attempt is referenced exactly once by valid
positive completion evidence.

## Exact `execute_flights` Attempt Index

The existing batch-manifest JSON object contains exactly one ordered
`execute_flights` array. Before any CCFG-26B flight it is empty. Each authorized
launch appends exactly one object with exactly these fields and no others:

```yaml
execute_flights:
  - flight_id: non-empty-string
    batch_id: ccfg-26b-fresh-slice-flight
    slice_id: "1" | "2"
    receipt_path: absolute-or-canonical-run-artifact-path
    input_inventory_path: absolute-or-canonical-run-artifact-path
    telemetry_path: absolute-or-canonical-run-artifact-path
    candidate_before: full-git-sha
    strict_execution_lease_sha256: sha256
```

The array and each entry obey these rules:

1. The runner validates the completed prefix and all prior attempts before it
   constructs an entry.
2. `flight_id` is unique and non-empty; all three evidence paths are exact,
   preallocated, unique to that flight, and inside the same resolved run artifact
   tree.
3. `batch_id` is exactly `ccfg-26b-fresh-slice-flight` and `slice_id` is the one
   already derived by `work-batch` and independently validated by the runner.
4. `candidate_before` equals the current validated candidate HEAD: the immutable
   baseline for Slice 1 or Slice 1's accepted `candidate.after` for Slice 2.
5. `strict_execution_lease_sha256` is the lowercase SHA-256 of the fresh exact
   lease that binds this batch, slice, candidate, planning evidence, and write
   ceiling.
6. The runner appends the complete entry before launching the fresh public
   `work-batch` subprocess. It uses the existing atomic JSON full-file replacement
   writer; every prior `execute_flights` object must remain identical under the
   canonical entry serialization below.
7. Every later `build_batch_manifest` write must first load and validate the
   existing `execute_flights` array and reproduce it unchanged. The current
   phase-keyed manifest rebuild is not allowed to erase or replace the array on
   success, `blocked`, `failed`, malformed-result, or runner-error paths.
8. After append, the entry is immutable. CCFG-26B never deletes, rewrites,
   ignores, reorders, or retries it.
9. No entry contains `pending`, `active`, `completed`, retry counts, recovery
   state, a runner-selected action, or any lifecycle status enum.

For the `flight_attempt.entry_sha256` reference, canonical entry serialization
is UTF-8 JSON produced by:

```python
json.dumps(
    entry,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
```

There is no trailing newline. `entry_sha256` is the lowercase hexadecimal
SHA-256 of those exact bytes. This is a batch-local integrity rule, not a public
schema.

## Exact `completed-slices.md` Grammar

`completed-slices.md` is a batch-local Markdown document with this exact
grammar:

````markdown
# CCFG-26B Completed Slices

## Slice <slice_id>

```yaml
interface: ccfg-26b-completed-slice/v1
batch_id: ccfg-26b-fresh-slice-flight
slice_id: "<slice_id>"
flight_attempt:
  batch_manifest_path: "<exact canonical path>"
  entry_sha256: "<sha256 of the canonical serialized execute_flights entry>"
  flight_id: "<flight_id>"
inventory:
  amendment_path: "docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/amendment.md"
  amendment_sha256: "<accepted amendment sha256>"
candidate:
  before: "<full git sha>"
  after: "<full git sha>"
commit_receipt:
  commit: "<same full git sha as candidate.after>"
  path: "<path>"
  sha256: "<sha256>"
flight_receipt:
  path: "<same receipt_path as the attempt entry>"
  sha256: "<sha256>"
  status: completed
validation:
  summary: "<non-empty summary>"
  evidence_paths:
    - "<path>"
  evidence_sha256:
    - "<matching sha256>"
review:
  verdict: clean
  evidence_path: "<path>"
  evidence_sha256: "<sha256>"
runner_observation:
  path: "<same telemetry_path as the attempt entry>"
  sha256: "<sha256>"
  observed_codex_session_id: "<non-empty session id>"
runner_evidence:
  input_inventory_path: "<same input_inventory_path as the attempt entry>"
  input_inventory_sha256: "<sha256>"
  telemetry_path: "<same telemetry_path as the attempt entry>"
  telemetry_sha256: "<same sha256 as runner_observation.sha256>"
next_action:
  kind: continue_same_batch | finalize_same_batch
  next_slice_id: "2" | null
material_integrity:
  expected_candidate_head_after_entry: "<same full git sha as candidate.after>"
```
````

The angle-bracket terms above are grammar metavariables whose values must be
fully materialized in an accepted entry; no literal placeholder is valid.

Parser requirements:

1. The document begins with exactly `# CCFG-26B Completed Slices`.
2. Each entry begins with exactly `## Slice <slice_id>`.
3. Each heading contains exactly one complete fenced YAML object.
4. The parsed object contains exactly the required fields above, recursively,
   with no extra keys.
5. `interface` equals `ccfg-26b-completed-slice/v1`.
6. Heading ID and YAML `slice_id` match.
7. Entries appear in immutable slice order.
8. A duplicate heading, duplicate ID, unknown ID, extra incomplete block,
   malformed final fence, or trailing partial entry blocks.
9. `evidence_paths` and `evidence_sha256` have equal non-zero lengths and
   positional correspondence.
10. Slice 1 uses `continue_same_batch` with `next_slice_id: "2"`; Slice 2 uses
    `finalize_same_batch` with `next_slice_id: null`.
11. The file is created atomically for Slice 1.
12. Slice 2 is added through an atomic full-file replacement that preserves the
    exact validated Slice 1 bytes and appends exactly one complete Slice 2
    section.
13. Accepted entries are never edited, deleted, reordered, reformatted, or
    regenerated.

Absence is an empty prefix only when candidate HEAD is the immutable baseline.
It does not mean no attempt exists; the negative barrier is validated separately
before a slice can be derived.

## Attempt Resolution

An attempt is resolved if and only if exactly one valid completed-slice entry:

- names the resolved batch manifest path;
- names the attempt's canonical `entry_sha256` and exact `flight_id`;
- matches its batch ID, slice ID, receipt path, inventory path, telemetry path,
  candidate-before SHA, and strict lease evidence;
- binds a `completed` flight receipt, exact commit receipt, clean review,
  focused validation, post-exit observation, input inventory, telemetry, and
  candidate-after SHA that all validate; and
- is itself in the valid contiguous completed prefix.

Therefore:

```text
unresolved_attempts =
  all validated execute_flights entries
  minus execute_flights entries referenced exactly once by the validated
  completed-slices entries
```

Any non-empty result blocks. Receipt presence and status do not resolve it:

- no receipt means an interrupted unresolved attempt;
- a `blocked` receipt is unresolved;
- a `failed` receipt is unresolved;
- a malformed or contradictory receipt is unresolved;
- a `completed` receipt without its accepted archive entry is an unresolved
  partial transition; and
- only the exact one-to-one archive reference resolves the attempt.

When blocking, surface `require_user` with the exact `flight_id`, `slice_id`,
`receipt_path`, and the available status (`missing`, `malformed`, `blocked`,
`failed`, or `completed`). Do not delegate, relaunch, append completion, modify
candidate code, invoke recovery, or reinterpret the attempt as absent. CCFG-26C
owns any later retry, repair, amendment, or same-slice recovery.

## Required Validation Algorithm

The following order replaces the prior derivation algorithm.

### Phase 1 - Validate Immutable Evidence

1. Verify the exact accepted digests for `dispatch.md`, `runway.md`, original
   `review.md`, `amendment.md`, `amendment-review.md`,
   `progression-authority-correction.md`, and
   `progression-authority-review.md` against the immutable values above.
2. Verify this correction against the exact digest in its clean independent
   review and program binding. Verify the independent review against the exact
   digest in program `CURRENT.md` and `LEDGER.md`. This avoids a self-referential
   digest cycle while requiring both exact files.
3. Read immutable ordered slice IDs `("1", "2")` from the accepted amendment.

### Phase 2 - Validate Positive Completion State

4. Parse `completed-slices.md` using the exact grammar above.
5. Treat absence as an empty prefix only when current candidate HEAD equals the
   immutable baseline.
6. Validate every entry's amendment digest, exact attempt reference, flight and
   commit receipts, focused validation, clean review, runner observation, input
   inventory, telemetry, next action, and material integrity.
7. Require archive IDs to be exactly one contiguous prefix of `("1", "2")`.
8. Require the candidate chain to be contiguous: Slice 1 `before` is the
   baseline; every later `before` equals the prior accepted `after`.
9. Require current candidate HEAD to equal the last accepted `candidate.after`,
   or the immutable baseline for an empty prefix.

### Phase 3 - Validate The Negative Attempt Barrier

10. Resolve the exact existing CCFG-26B batch manifest from the exact explicitly
    resumed run-state path using the path contract above; reject a new run or
    bare latest-run resume.
11. Parse its one ordered `execute_flights` array and reject unknown slice IDs,
    duplicate flight IDs, duplicate canonical entry digests, missing or extra
    fields, malformed values, changed prior entries, inconsistent
    `candidate_before`, or an attempt for a later slice while an earlier slice
    is incomplete.
12. Require every completed-slice entry to reference exactly one matching
    attempt entry.
13. Require every referenced attempt to be referenced by exactly one
    completed-slice entry.
14. Compute `unresolved_attempts` by the exact set difference above.
15. If any unresolved attempt exists, return `require_user` with its exact
    identity and available receipt status before deriving a next slice or
    delegating.

### Phase 4 - Derive Only After Both Validations Pass

16. Only when the completed prefix is valid and `unresolved_attempts` is empty,
    derive the first absent immutable slice ID.
17. Bind exactly that ID to one newly appended attempt entry and one fresh strict
    execution lease.
18. Require the work-batch-authored receipt's `next_action` to equal the
    independently derived post-completion action.
19. If both immutable slices are completed and every attempt is resolved,
    derive the final same-batch gate rather than another implementation slice.

The runner validates and persists these facts mechanically. It never uses the
attempt index to select a semantic next slice, mark completion, or manufacture
an archive entry.

## Required Physical Write Order

```text
1. Validate immutable evidence.
2. Validate completed-slices.md and candidate chain.
3. Validate existing execute_flights attempt entries.
4. Block if any unresolved attempt exists.
5. Derive exactly one next slice.
6. Obtain a fresh strict live lease.
7. Atomically append one immutable execute_flights attempt entry.
8. Launch public work-batch.
9. work-batch writes its exact flight receipt and exits.
10. Runner writes post-exit observation/telemetry.
11. Runner validates receipt, commit, validation, review, lease, inventory,
    telemetry, candidate movement, and attempt-entry equality.
12. For a completed accepted flight only, runner atomically creates or appends
    the exact completed-slices.md entry.
13. Runner re-reads completed-slices.md and the attempt manifest.
14. Runner proves the just-completed attempt is now referenced exactly once.
15. Runner applies only the validated mechanical transition.
16. Derived Run State and reporting manifests may then be updated.
```

For `blocked`, `failed`, missing, or malformed receipts, stop no later than step
11 and do not append a completed entry. If the process dies after step 7 but
before step 12, the immutable attempt remains a durable barrier. Final Run State
and the manifest's fields other than `execute_flights` remain derived reporting;
they are not prerequisites for the archive append.

## Required Counterfactual Tests

Counterfactuals A through L in `progression-authority-correction.md` remain
required. Add exactly these cases:

| Case | Required result |
|---|---|
| M. Slice 1 archived; Slice 2 blocked receipt exists | unresolved Slice 2 attempt blocks before another delegation |
| N. Slice 1 archived; Slice 2 failed receipt exists | unresolved Slice 2 attempt blocks before another delegation |
| O. Slice 1 archived; Slice 2 completed receipt and observation exist, but `completed-slices.md` was not appended | unresolved partial transition blocks |
| P. Slice 1 archived; no later `execute_flights` entry exists | derive Slice 2 |
| Q. Attempt entry exists but no receipt was written | interrupted attempt blocks |
| R. Completed-slices entry references an unknown attempt digest | block |
| S. One attempt entry is referenced by two archive entries | block |
| T. A valid completed attempt remains in `execute_flights` and is referenced exactly once by the archive | it is resolved and does not block |
| U. Filesystem contains an unindexed receipt not present in `execute_flights` | do not use it for progression; report it only if an existing contract requires an anomaly, and never glob or adopt it as authority |
| V. Both slices archived and every attempt resolved | derive final same-batch gate |

The implementation proof must parse the real immutable amendment, existing
batch manifest, and exact Markdown/YAML archive grammar; consume real public
`work-batch` result objects; validate through the runner; and exercise transition
consumption. Direct injection of a final slice ID or precomputed unresolved flag
is insufficient.

## Planning And Execution Mutation Rules

This planning-only correction may add only this file and its independent review,
then modify program `CURRENT.md` and `LEDGER.md` only after a clean review to bind
their exact digests. It must not create `completed-slices.md`, a runner manifest,
receipt, inventory, telemetry, Run State, candidate change, or lifecycle state.

During the already planned Slice 1 and Slice 2 implementation only:

- the existing batch manifest gains the one `execute_flights` array and its
  append-only entries at the existing canonical path;
- the existing candidate implementation/test ceiling may implement and prove
  this correction together with the accepted slice behavior;
- `completed-slices.md` may be created or appended only in the accepted physical
  order above; and
- all accepted planning evidence and the queue remain immutable.

No CCFG-26B path may add a new attempt file, database, state store, lifecycle
ledger, receipt index, alternate manifest, recovery behavior, retry behavior,
third slice, finalization or closeout behavior, phase-label migration, or public
reusable schema. CCFG-26C through CCFG-29 remain unselected and unprepared.

## Invariants

1. `amendment.md` remains the sole immutable ordered inventory.
2. `completed-slices.md` remains the sole positive mutable completion authority.
3. Completed entries form exactly one contiguous prefix of `("1", "2")`.
4. The existing batch manifest's `execute_flights` array is only a negative
   ordered launch index.
5. Every attempt is either referenced exactly once by a valid completion entry
   or is unresolved and blocks before derivation.
6. Receipt status alone never resolves an attempt.
7. An unresolved Slice 2 attempt blocks even when Slice 1 is validly archived.
8. The runner appends an attempt before launch and never deletes, rewrites,
   ignores, or automatically retries it.
9. Filesystem receipt discovery, chat, chronology, Git movement, Run State, and
   receipt action alone never derive progression.
10. Exactly two implementation slices remain; after both resolve, the only
    derivation is the final same-batch gate.
11. No new runtime artifact, store, lifecycle state, public schema, runner, or
    implementation slice is introduced.
12. The runner validates and transitions mechanically; `work-batch` retains
    semantic next-slice ownership.

## Proportionality Forecast

```yaml
expected_changed_planning_files: 4
new_runtime_artifacts: []
new_stores: []
new_lifecycle_states: []
new_public_schemas: []
implementation_slice_count: 2
implementation_started: false
```

The four planning paths are this correction, its independent review, program
`CURRENT.md`, and program `LEDGER.md`. Stop with `design_status: blocked` if the
existing run state cannot resolve the exact existing batch manifest, if the
manifest cannot preserve the immutable attempt array across fresh resumes, if
the independent review is not clean, or if any requested behavior requires a
new runtime artifact or broader lifecycle authority.

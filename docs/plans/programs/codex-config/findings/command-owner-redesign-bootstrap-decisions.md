# Command-Owner Redesign Bootstrap Decisions

## Authority

```yaml
accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
original_design_snapshot: b3f31c44a1fc3287c33dd2955489f194afef66f6
live_intake_commit: 7356a3fd9d8d487be8562af11cad56170f300616
```

The accepted design snapshot is immutable provenance for future planning. The
live executable scope remains in `CURRENT.md`, `LEDGER.md`, and the local intake
file on `master`.

## Accepted Decisions

### Three-root topology

```yaml
toolchain_source_root: stable checkout on authoritative master
canonical_planning_repository_root: stable checkout on authoritative master
implementation_target_root: separate candidate clone
```

Planning writes remain under the stable canonical root. Candidate source writes,
validation, diffs, and implementation commits occur under the candidate root.
Controlling scripts, schemas, references, workers, and reviewers resolve from the
stable toolchain root before cutover.

### Candidate branch lineage

The implementation branch starts from latest authoritative `master` and merges
the accepted design history ending at
`caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c` with preserved ancestry. The
original `b3f31c4` snapshot remains historical provenance.

### Generation boundary and rollback

No real batch is controlled by more than one toolchain generation. Stable batches
close before candidate-controlled canonical work begins. Cutover occurs at
quiescent state.

Before any candidate canonical write, installation-only rollback is permitted if
planning remains stable-readable. After candidate canonical writes, rollback
restores installation, code, canonical planning state, active artifacts, and run
state to one recorded compatible checkpoint.

### Cutover split

- CCFG-27 prepares and rehearses cutover; it does not switch the default
  generation.
- CCFG-28 deletes APR and Batch Runway from candidate source, proves a clean
  installation, switches the default generation, obtains a fresh candidate
  read-only diagnostic, then closes under the already-loaded stable controller.
- The first candidate canonical write begins in a new post-cutover batch.

### `skill-authoring` dependency

`skill-authoring` v1 core depends on CCFG-20, not full CCFG-21 closure. Planning
artifact guidance is a conditionally loaded reference under the same skill and
version and requires only the schemas it claims to support.

### Canonical representations

- `CURRENT.md`: one canonical structured state block plus explanatory prose.
- `LEDGER.md`: one canonical structured block per finding plus a derived or
  mechanically validated human-readable index.

Both representations require expected revision, expected file hash, atomic
replace, reread validation, and receipts.

### Post-cutover convergence

After CCFG-28, the implementation branch may remain the candidate toolchain source
while `master` remains the planning authority. CCFG-29 merges candidate code into
latest `master`, verifies target content, rebinds the default toolchain to
`master`, removes the temporary cross-checkout bridge, and retires candidate
branches when safe.

### Temporary bridge

The cross-checkout bridge is narrow, versioned, and temporary. It owns root,
repository, write-scope, and generation validation plus cross-repository receipt
format. It owns no intake, selection, scope, runway, execution acceptance,
closeout, or successor decision. Its deletion condition is CCFG-29 final
integration.

## Minimum Gate Before `plan-batch CCFG-18`

```yaml
stable_checkout_on_master: required
stable_checkout_clean_or_classified: required
default_codex_home_resolves_to_stable_checkout: required
required_skills_resolve_to_one_stable_commit: required
selected_dispatch: null
queued_runway: null
active_runway: null
resumable_runner_state: false
stable_checkout_path: known
candidate_clone_path: known
candidate_codex_home_path: known
accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
```

The clone, implementation branch, accepted design merge, candidate CODEX_HOME,
bridge, mechanical generation fingerprint, and rollback rehearsal belong inside
CCFG-18.

## No Re-Intake or Selection

These decisions amend existing CCFG-18 through CCFG-29 findings. They do not
create a new finding, batch map, selected dispatch, queued runway, or active
runway.

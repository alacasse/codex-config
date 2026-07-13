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

### Pre-creation bootstrap amendment

`cross-checkout-context/v1` remains the strict post-creation interface. Its
existing repository-root and exact-revision checks must not be weakened.

CCFG-18 also requires a separate temporary pre-creation interface because the
strict context cannot validate the implementation target before that repository
exists:

```text
runway creation requires existing candidate repository
candidate repository creation requires work-batch execution
work-batch execution requires an existing runway
```

The accepted pre-creation shape is:

```yaml
interface: cross-checkout-precreation/v1

stable_control:
  toolchain_source_root: absolute-existing-git-root
  toolchain_commit: full-sha
  canonical_planning_repository_root: absolute-existing-git-root
  canonical_planning_commit_before: full-sha
  canonical_planning_root: absolute-existing-directory
  codex_home: absolute-existing-directory
  generation_role: stable
  canonical_state_mutation_allowed: true

candidate_intent:
  implementation_target_root: absolute-intended-path
  expected_repository_state: absent
  candidate_codex_home: absolute-intended-path
  expected_codex_home_state: absent
  base_repository: alacasse/codex-config
  base_commit: full-authoritative-master-sha
  implementation_branch: explicit-name
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c

creation_authority:
  repository_creation_allowed: true
  candidate_codex_home_creation_allowed: true
  allowed_creation_roots:
    - exact implementation_target_root
    - exact candidate_codex_home
```

The pre-creation validator must validate the stable generation and canonical
planning revision, require absolute intended paths, require the candidate
repository to be absent, and require candidate `CODEX_HOME` to be absent or
explicitly empty according to the implemented contract. It must reject overlap
with stable or protected roots and reject an unexpected existing repository
instead of reusing it. It records the authoritative base commit and accepted
design snapshot and authorizes only the two exact creation targets.

Like the strict context, it grants no intake, selection, scope-shaping,
implementation-acceptance, closeout, or successor authority. It does not require
an implementation commit before the repository exists.

### Required pre-creation transition

After candidate repository lineage and environment creation are verified,
execution must emit a versioned transition receipt and construct the existing
strict context:

```text
cross-checkout-precreation/v1
  -> candidate repository and branch created
  -> authoritative master ancestry verified
  -> accepted design snapshot merged and verified
  -> candidate CODEX_HOME created
  -> actual candidate HEAD recorded
  -> cross-checkout-context/v1 validated
```

No implementation beyond repository and environment establishment may continue
until `cross-checkout-context/v1` validates successfully.

### Pre-creation planning boundary

The next explicit `plan-batch CCFG-18` may select one bounded single-root
stable-control batch whose only purpose is to implement and validate
`cross-checkout-precreation/v1`. That batch operates only on stable `master`,
does not create either candidate path, updates the helper, consumer contracts,
tests, manifest, and documentation, then stops after closeout. The changed
stable feature set must be installed and loaded in a fresh stable session before
the new interface controls real work.

A later explicit `plan-batch CCFG-18` may plan actual candidate creation under
the installed pre-creation contract. This is a required fresh-session boundary,
not a preselected batch map.

The accepted design snapshot remains frozen. After candidate lineage is
verified, the implementation branch must receive the same amendment as an
explicit live design amendment without rewriting the frozen snapshot.

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
candidate_clone_state: absent
candidate_codex_home_state: absent
precreation_amendment_recorded: true
accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
```

The next batch-planning pass may cover stable pre-creation support only. The
clone, implementation branch, accepted design merge, candidate `CODEX_HOME`,
strict-context transition, mechanical generation fingerprint, fixture-only
validation, and rollback rehearsal remain inside CCFG-18 but wait for the
stable-support closeout, install, and fresh-session reload.

## No Re-Intake or Selection

These decisions amend existing CCFG-18 through CCFG-29 findings. They do not
create a new finding, batch map, selected dispatch, queued runway, or active
runway.

# Extraction-First Batch-Local Execution

## Status

Accepted on 2026-07-19.

This decision supersedes ADR 0003 for future CCFG-26 planning and
implementation. ADR 0003 and the execution-state plans derived from it remain
historical evidence only.

## Context

The execution workflow is being developed inside `codex-config`, but the useful
result is expected to be extracted later into a standalone open-source project
with its own installation path.

The current repository uses two checkouts, two `CODEX_HOME` directories,
symlinks, and a cross-checkout bridge so the replacement can be developed
without breaking the configuration that controls the work. Those mechanisms are
a temporary dogfooding harness. They are not user-facing product concepts.

The superseded CCFG-26 design mixed that harness with the future product. It also
required a separate run-artifact root, persisted a planner-selected temporary
path, and expanded the filesystem threat model from accidental concurrent use to
hostile same-user namespace substitution. The resulting plan produced a large
uncommitted implementation before the missing cross-platform security primitive
was discovered.

## Decision

### Product boundary

The product starts from a planning root chosen by the user. A program ledger and
its batch directories live beneath that root. Batch-specific runtime state lives
with the batch by default:

```text
<planning-root>/
  programs/
    <program>/
      CURRENT.md
      LEDGER.md
      batches/
        <batch-id>/
          dispatch.md
          runway.md
          .runtime/
            execution-state.json
            execution-state.lock
            receipts/
          completed-slices.md
          closeout.md
```

The product API may accept values such as a ledger path, runway path, batch
directory, execution event, and expected revision. It must not require knowledge
of the repository or installation method used to develop it.

A separate `run_artifact_root` remains optional for runner-global state, bulky
logs, telemetry, or an explicitly configured external backend. It is not
required for the small canonical state of one batch.

### Dogfood boundary

The following are codex-config development and installation concerns, not
product concepts:

- `CODEX_HOME` and `.codex` layout;
- symlink installation and `codex-features.json`;
- stable and candidate checkouts or generations;
- the command-owner-redesign branch and clone;
- the cross-checkout bridge and live-lease machinery;
- machine-specific paths such as `/home/alacasse/...`.

A codex-config adapter may use those mechanisms to launch or validate the product
code. Product code, schemas, persistent state, and public interfaces may not
depend on them unless a future explicit user requirement promotes one into the
product.

### Threat model

Version 1 protects against:

- accidental parallel invocations on one host;
- a process crash during a local state transition;
- stale revision writes;
- replay of the same accepted request;
- partially written JSON files.

Version 1 assumes a trusted local filesystem and trusted processes running as the
same user. It does not claim protection against:

- a hostile same-user process replacing paths or symlinks during a system call;
- shared or network filesystems;
- multi-host execution;
- distributed leases or fencing;
- guaranteed power-loss durability.

These exclusions are product limits, not defects to solve implicitly while
implementing another feature.

### Portability

The product must support Windows, macOS, and Linux through an operating-system-
neutral public interface. Concrete locking and atomic-write mechanisms are
implementation choices, but no platform-specific primitive may leak into the
public contract.

Temporary directories are created at test or disposable acceptance runtime using
the host platform's temporary-directory facility. A temporary path is never a
durable planning decision, a project default, or the canonical location of a
real long-lived batch.

### Feasibility gate

A plan may require a technical guarantee only when it names:

1. the concrete failure it prevents;
2. the realistic actor or cause;
3. the user value;
4. the implementation primitive or bounded dependency;
5. the cross-platform proof path.

When the primitive is unknown, planning must reduce the guarantee or authorize a
small disposable feasibility experiment before production implementation. It
must not defer the decisive mechanism choice into a large production Slice.

## Consequences

- `ccfg-26-execution-state-foundation` is superseded and cannot be resumed.
- Its uncommitted candidate worktree remains under the user's control. It is not
  accepted implementation, a baseline, or planning authority.
- Future CCFG-26 planning starts from this product boundary and the original
  COR-009 user outcome, not from the shape of the preserved worktree.
- Batch-local runtime state is the default design.
- Codex installation and checkout topology may remain in a temporary dogfood
  adapter, with an explicit removal condition, but cannot shape the extracted
  core.
- The product does not need an anchored-filesystem security abstraction for the
  version-1 threat model.

## Enforcement

Repository instructions and planning contracts require every architecture,
migration, extraction, runner, storage, or installation plan to state its
Product Boundary, Dogfood Boundary, Threat Model, and Guarantee Feasibility.
Planning review treats a dogfood concern that enters a product API, schema,
storage layout, or durable contract without explicit user need as a blocking
finding.

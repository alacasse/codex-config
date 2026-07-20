# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID: `None`
- Active batch execution status:
  `idle; ccfg-26-execution-state-foundation is superseded; no implementation Slice is accepted; candidate WIP remains under user control; no successor selected`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/closeout.md`
- Program archive location: `docs/plans/archive/`

## Project State Policy

- Planning root: `docs/plans/`
- Slice-shape policy path: `notes/slice-shape-policy.yaml`
- Batch runtime policy: `batch-local`
- Default batch runtime directory: `.runtime/` beneath the batch directory
- Run artifact root: `None`; optional only for runner-global, bulky, or explicit
  external operational artifacts
- Output root: `None`
- State file policy: `generated-only`
- Projection policy: `generated-only`
- Projection usage: `caller-directed`
- Projection rebuild authority: `command`
- Update authority: `command`

## Current CCFG-26 Disposition

- Finding status: `Ready` for fresh planning after the user-controlled candidate
  worktree is isolated from the future execution scope.
- No replacement dispatch or runway exists.
- `ccfg-26-execution-state-foundation` is superseded and cannot be executed,
  resumed, amended, or closed.
- No candidate CCFG-26 implementation commit exists.
- No real Batch Execution State exists.
- Slice 2 and all later CCFG-26 behavior remain unstarted.
- CCFG-26B and the old CCFG-26C/D/E sequence remain historical or conceptual
  evidence only.
- CCFG-27 through CCFG-29 remain unselected.

## Live Decision Sources

- Extraction-first architecture:
  `docs/adr/0004-extraction-first-batch-local-execution.md`
- CCFG-26 reset and preserved-worktree direction:
  `docs/plans/programs/codex-config/findings/ccfg-26-product-dogfood-reset.md`
- Superseded foundation notice:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/superseded.md`
- Failure evidence retained for learning:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/execution-retrospective.md`
- Original command-owner outcome:
  COR-009 in the accepted command-owner redesign snapshot linked from the ledger.

ADR 0003 and the old CCFG-26 execution-state design contract are historical
provenance for the superseded approach. They are not live planning authority.

## Preserved Candidate Worktree

The uncommitted candidate CCFG-26 files are owned by the user.

Do not delete, reset, commit, modify, reuse, or treat them as accepted
implementation without explicit user direction. Future planning must not derive
its architecture from those files. A later `work-batch` must stop on overlapping
dirt until the user has isolated or resolved it.

## Next Safe Action

Keep the program idle. The user first chooses how to isolate or preserve the
candidate WIP outside the future write scope. A later explicit `plan-batch
CCFG-26` then creates one fresh extraction-first runway from ADR 0004 and the
reset finding.

That plan must:

- begin from the user-visible OSS product;
- keep codex-config installation and stable/candidate mechanics in a temporary
  dogfood adapter;
- place batch-specific runtime state under the batch directory;
- protect accidental concurrent invocation and process crashes on trusted local
  filesystems across Windows, macOS, and Linux;
- explicitly exclude hostile same-user namespace races, network filesystems,
  multi-host execution, and power-loss durability;
- name every material implementation primitive before production coding;
- select no successor.

## Stop Conditions

- Stop if the superseded foundation dispatch, runway, amendment, or review is
  treated as executable or resumable.
- Stop if an agent deletes, resets, commits, modifies, or reuses the preserved
  candidate WIP without explicit user direction.
- Stop if `CODEX_HOME`, symlinks, stable/candidate generations, cross-checkout
  fields, or developer paths enter the product API, schema, state layout, or
  terminology.
- Stop if a temporary path is persisted as the durable location of a real batch.
- Stop if a separate runtime root is required for small batch-owned state without
  a concrete user requirement.
- Stop if planning promises a material guarantee without a named feasible
  primitive and proof path.
- Stop if planning widens local reliability into hostile same-user filesystem,
  network-filesystem, multi-host, distributed, or power-loss guarantees.
- Stop if CCFG-26B is revived or CCFG-26C through CCFG-26E are treated as an
  accepted successor chain.
- Stop if CCFG-27 or another successor is selected before CCFG-26 later produces
  accepted completion evidence.
- Stop if Graphify is invoked or treated as authority.

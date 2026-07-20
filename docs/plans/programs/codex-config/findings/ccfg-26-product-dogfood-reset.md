# CCFG-26 Product And Dogfood Boundary Reset

## Status

Accepted direction on 2026-07-19. Planning reset only; no implementation is
accepted, deleted, resumed, or authorized by this document.

## User Decision

CCFG-26 must be replanned from the user-facing product rather than from the
current codex-config installation and dogfooding topology.

The useful implementation is expected to be extracted later into a standalone
open-source project with its own installation. The current symlink installer,
`CODEX_HOME` directories, stable/candidate checkouts, and cross-checkout bridge
are temporary development machinery. They must not determine the product API,
state layout, schemas, terminology, or safety guarantees.

## Product Model

- The user chooses the planning root.
- The program ledger lives beneath that root.
- Each batch lives in the batch directory derived from that ledger and runway.
- Small batch-specific runtime state lives under that batch directory, normally
  in `.runtime/`.
- Product code receives ledger, runway, batch-directory, event, and revision
  values. It does not receive codex-config installation concepts.
- A separate run-artifact root is optional for runner-global or bulky output, not
  required for one batch's canonical state.

## Dogfood Model

The stable/candidate topology may still be used to test the extracted design
inside codex-config. It is an adapter owned by the command-owner migration and
removed or narrowed by the existing cutover work.

The adapter may:

- launch the candidate copy of product code;
- keep the stable configuration unchanged;
- provide disposable fixtures;
- report which checkout and installation were exercised.

It may not:

- add `CODEX_HOME`, symlink, checkout-generation, or cross-checkout fields to the
  product contract;
- choose where a real user's batch state lives;
- make a machine-specific temporary path durable planning state;
- expand the product threat model solely to defend the dogfood harness.

## Threat Model Reset

The first OSS-oriented version must prevent accidental concurrent writes and
preserve valid local state after a process crash on Windows, macOS, and Linux.
It does not defend against a hostile same-user process replacing filesystem
namespace entries during the final system call. Shared filesystems, multi-host
execution, fencing, and power-loss durability remain unsupported unless a later
explicit product requirement adds them.

The cross-platform final-effect confinement blocker from the failed Slice 1 is
therefore outside the new product requirement. It is not a mechanism that the
replacement plan must solve.

## Preserved Candidate Worktree

The uncommitted CCFG-26 candidate code remains entirely under the user's control.
No workflow may delete, reset, commit, amend, reuse, or treat it as authoritative
without a later explicit user instruction.

The preserved worktree is evidence of what was attempted. It is not:

- an accepted Slice;
- an implementation baseline;
- a required source for the replacement plan;
- a reason to preserve the superseded design;
- permission for an agent to continue patching it.

Future planning must be understandable without reading that worktree. Execution
must stop on overlapping dirt until the user decides how to isolate or dispose of
it.

## Planning Disposition

- Supersede `ccfg-26-execution-state-foundation`.
- Clear selected, queued, and active state.
- Preserve its dispatch, runway, amendment, reviews, execution report, and
  retrospective as historical evidence only.
- Mark CCFG-26 Ready for a fresh `plan-batch` after the user-controlled candidate
  worktree is isolated from the intended execution scope.
- Do not revive CCFG-26B or infer the old CCFG-26C/D/E sequence.
- Do not select CCFG-27 or any other successor.

## Permanent Planning Gate

Every future architecture, migration, extraction, runner, storage, or installer
plan must include:

```yaml
product_boundary:
  user_problem: string
  product_files_or_modules: []
  persistent_state: []
  public_inputs: []
  forbidden_dogfood_dependencies: []

dogfood_boundary:
  temporary_mechanics: []
  adapter_location: string | null
  removal_condition: string | null

threat_model:
  protects_against: []
  does_not_protect_against: []

guarantee_feasibility:
  failure_prevented: string
  realistic_actor_or_cause: string
  user_value: string
  implementation_primitive: string | null
  cross_platform_proof: string | null
```

A null implementation primitive for a material guarantee blocks production
planning. The planner must reduce the guarantee or create a disposable
feasibility experiment instead of starting a large production implementation.

## Canonical Decision

`docs/adr/0004-extraction-first-batch-local-execution.md` owns the durable
architecture decision. This finding owns the CCFG-26 reset and worktree
preservation instructions.

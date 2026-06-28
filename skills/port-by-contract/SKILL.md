---
name: port-by-contract
description: Extract implementation-neutral contracts before porting or rewriting software across languages, frameworks, runtimes, or product boundaries. Use when asked to migrate an existing implementation, plan a rewrite, turn current code into behavior contracts, or create a runway for a fresh target implementation without direct file-by-file translation.
---

# Port By Contract

Use this skill when an existing implementation must be ported or rewritten
without copying accidental source structure into the target. The goal is to
produce compact, implementation-neutral contracts that a fresh implementation
agent can build from.

## Core Rule

Do not translate files directly by default. Extract behavior, contracts, state
transitions, inputs, outputs, failure modes, ownership boundaries, and
validation evidence first. Only inspect source files to discover the contract;
do not preserve file layout, private helper names, or language-specific control
flow unless they represent an intentional public or operational contract.

If the user explicitly asks for direct translation, state the risk and ask
whether to bypass the contract-first workflow.

## Required First Steps

1. Read applicable repo instructions and local overlays.
2. Identify the source implementation, target language/framework/runtime, and
   intended target product or module.
3. Check the worktree before editing planning files or code.
4. Read source docs, tests, CLI/API entrypoints, schemas, receipts, fixtures,
   and recent plans before relying on code shape.
5. Choose the mode: `intake-source`, `distill-contract`, `design-target`,
   `create-port-runway`, or `closeout-port`.

If the source scope, target, planning location, or validation authority is
unclear, stop and ask for the missing value instead of creating speculative
contracts.

## Modes

- `intake-source`: map the source implementation and evidence. Identify public
  entrypoints, state, artifacts, providers, validation, and known non-goals.
- `distill-contract`: write implementation-neutral behavior contracts from the
  source evidence. This is the default mode when the user asks to prepare a
  rewrite or port.
- `design-target`: propose the target architecture that satisfies the
  contracts without mirroring source files.
- `create-port-runway`: create a compact handoff for `architecture-program-runway`
  or `batch-runway` after contracts exist.
- `closeout-port`: reconcile target implementation evidence against the
  contracts, recording satisfied, changed, deferred, and rejected contract
  items.

Infer the narrowest useful mode from the request. Do not jump to
`create-port-runway` until the contract outputs are concrete enough for a fresh
agent to implement from them.

## Source Intake

Build a source map from behavior evidence, not from directory shape alone.
Capture:

- Purpose and user-facing promise.
- Public CLI, API, config, or file interfaces.
- State machine, lifecycle, resume, and idempotence rules.
- Input/output schemas, receipts, manifests, artifacts, and path layout.
- Provider boundaries, side effects, external commands, and environment rules.
- Error handling, stop conditions, retries, and validation failures.
- Telemetry, logging, privacy, and redaction rules.
- Tests and fixtures that define expected behavior.
- Source implementation details that must not become target constraints.

Prefer current code and tests over older planning docs when they disagree.
When an older document explains intent that code does not yet implement, mark
it as `proposed`, not `current`.

## Contract Outputs

Keep contracts compact, link to supporting source paths, and avoid raw code
dumps. A useful contract set usually includes:

- Source architecture map.
- Behavior contract.
- State machine contract.
- Interface contract for CLI/API/config/files.
- Receipt, schema, and artifact layout contract.
- Provider and side-effect boundary contract.
- Telemetry and logging contract.
- Validation and stop-condition contract.
- Test contract: source tests that must have target equivalents.
- Target architecture notes.
- Port runway handoff.

Each contract item should state:

- `id`: stable short identifier.
- `status`: `current`, `proposed`, `target-only`, `deprecated`, or `unknown`.
- `source evidence`: code, test, doc, or observed command path.
- `contract`: implementation-neutral rule.
- `target implication`: what the new implementation must provide or may change.
- `validation`: command, test, fixture, receipt, or review evidence.

Do not include large schemas inline when a referenced schema file is clearer.
Summarize the stable rule and link the path.

## Target Design

Design the target from the contracts, not from source module names. Name target
owners around durable concepts such as state, command surface, artifact store,
provider execution, validation, telemetry, and recovery.

For each target component, record:

- Contract IDs satisfied.
- Data it owns.
- Interfaces it exposes.
- Dependencies it may call.
- Failure modes it must surface.
- Tests that should protect it.

Mark deliberate target divergences explicitly. A divergence is acceptable only
when it preserves or intentionally updates the contract with rationale and
validation.

## Handoff To Runway Skills

After contract distillation, use the smallest workflow that fits:

- Use `batch-runway` when one bounded 3-5 slice port plan is enough.
- Use `architecture-program-runway` when multiple workstreams, staged ledgers,
  or repeated batches are needed.

The handoff should include:

- Source scope and target scope.
- Contract artifact paths.
- Required guardrails, including no direct translation.
- Suggested slice or batch shape.
- Acceptance criteria tied to contract IDs.
- Validation ladder and stop conditions.
- Explicitly deferred contracts or open questions.

Do not ask the next agent to reread the entire source unless a contract is
missing, stale, contradictory, or explicitly insufficient.

## First Documented Use Case

Use this path for the Python architecture-program runner to Go
`baton-runner` extraction:

- Source: `scripts/architecture_program_runner*.py`, runner tests, runner
  protocol references, schemas, and relevant planning docs.
- Target: Go implementation for a generic phase runner or `baton-runner`
  product.
- Expected outputs: source architecture map, behavior contract, state machine
  contract, receipt contract, artifact layout contract, Go target architecture
  notes, and a port runway plan.
- Guardrail: do not copy the Python runner's file split into Go packages unless
  the contract evidence proves that split is a durable concept boundary.

## Closeout

When reviewing or closing a port:

1. Compare target behavior to each contract ID.
2. Record `satisfied`, `changed`, `deferred`, or `rejected` with evidence.
3. Require target-side validation for behavior claims.
4. Update the runway or program ledger with compact evidence only.
5. Preserve unresolved contract gaps as follow-up items, not hidden notes.

## Non-Goals

- Do not perform direct line-by-line translation.
- Do not freeze accidental source file boundaries as target architecture.
- Do not produce giant design documents when compact contracts and links are
  enough.
- Do not create a port plan before current behavior and validation authority
  are understood.

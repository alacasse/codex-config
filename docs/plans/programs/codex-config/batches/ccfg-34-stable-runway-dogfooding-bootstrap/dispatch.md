# CCFG-34 Minimal Stable Runway Dogfooding Bootstrap Dispatch

## Selection

- Batch ID: `ccfg-34-stable-runway-dogfooding-bootstrap`
- Selection outcome: `selected`
- Covers: CCFG-34 only
- Source ledger: `../../LEDGER.md`
- Source finding:
  `../../findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`
- Expected runway: `runway.md`
- Implementation repository: `/home/alacasse/projects/codex-config`
- Execution context: ordinary single-root
- Batch kind: `migration`
- Density: `lean-runway`

## Goal

Add a small repository-local temporary policy that improves the stable execution
of CCFG-26 through CCFG-29 without changing runner architecture.

The policy must provide:

1. vertical, context-bounded planning and explicit migration residue;
2. exactly one pending implementation slice per `work-batch` invocation, followed
   by a manual later invocation for the next slice;
3. at most one bounded consultation of the existing read-only
   `codebase_investigator` before an avoidable mechanical escalation.

## Authorized Scope

Expected implementation surfaces:

- `.codex/AGENTS.md`;
- one project-owned policy under
  `docs/plans/programs/codex-config/notes/`;
- one focused policy contract test;
- `CHANGELOG.md`;
- `codex-features.json` only if mechanically required.

A project-neutral wording change in `skills/work-batch/SKILL.md` or
`skills/batch-runway/references/execute-recovery-v1.md` requires concrete proof
that the repository-local overlay cannot enforce the behavior and a reviewed
runway amendment before the edit.

## Explicit Exclusions

Do not modify:

- `scripts/architecture_program_runner*.py`;
- runner state, transitions, validation, receipts, workers, artifacts, or telemetry;
- serialized runner phases or public phase results;
- `agents/codebase_investigator.toml` or any agent result schema;
- candidate-generation code or stable-home runtime state.

Do not add a launcher, execution-unit protocol, automatic continuation,
persistent store, lifecycle state, helper, or second coordination framework.

## Planning Shape

Prefer one implementation slice. Split only when a concrete file-owner boundary
makes a second independently useful commit necessary.

The implementation is successful when the local policy is automatically loaded,
covered by focused tests, and sufficient to direct future CCFG-26 through CCFG-29
planning and execution.

## CCFG-26 And CCFG-29

- CCFG-26 remains blocked until CCFG-34 closeout and then requires a fresh plan.
- The CCFG-26 replan must include permanent candidate behavior from issues #59,
  #60, and #61.
- CCFG-29 must remove the temporary policy and hook only after candidate parity
  is validated.

## Stop Conditions

- Stop if automatic policy loading requires runner architecture changes.
- Stop if project-specific behavior would be added to a reusable generic skill.
- Stop if more than one implementation slice is proposed without a concrete,
  independently useful intermediate state.
- Stop if the existing investigator contract would need modification.
- Stop if implementation would alter CCFG-26, candidate code, runtime Codex state,
  or successor selection.

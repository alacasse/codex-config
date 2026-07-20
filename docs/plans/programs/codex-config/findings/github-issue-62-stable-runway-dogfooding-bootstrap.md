# GitHub Issue 62: Minimal Stable Runway Dogfooding Bootstrap

## Source

- GitHub issue: https://github.com/alacasse/codex-config/issues/62
- Ledger identity: `CCFG-34`
- Historical related-issue provenance: #59 and #61 are closed as not planned;
  #60 is closed as completed for slice-shape policy only.
- Source status: closed as completed
- Implementation commit: `ba1e941`
- Closeout:
  `../batches/ccfg-34-stable-runway-dogfooding-bootstrap/closeout.md`

## Decision

CCFG-34 is a deliberately small temporary bootstrap for the stable generation.

The user accepts manual relaunch between implementation slices and some remaining
recovery friction. CCFG-34 must not build temporary runner architecture that will
be removed after CCFG-29.

The immediate stable behavior is limited to:

1. one repository-local policy for vertical, context-bounded planning;
2. exactly one pending implementation slice per `work-batch` invocation for
   CCFG-26 through CCFG-29;
3. at most one bounded consultation of the existing read-only
   `codebase_investigator` before an avoidable mechanical escalation.

## Temporary Policy Requirements

For migration and ownership-transfer work, each slice states:

```yaml
vertical_slice:
  starting_scenario: string
  durable_result: string
  owner_before: string
  owner_after: string
  migrated_callers: []
  focused_validation: []
  independently_usable_state: string
  rollback_boundary: string
  temporary_residue: []
```

Temporary coexistence also names exact callers, current owner, future owner, and
removal condition. Proportionality warnings trigger a smaller-alternative review;
they are not arbitrary hard limits or a fixed slice count.

## Stable Execution Rule

For CCFG-26 through CCFG-29, one `work-batch` invocation executes at most one
pending implementation slice. After implementation, focused validation,
independent review, commit, receipt, active-ledger update, and completed-slice
archival are durable, the coordinator stops.

A later explicit invocation resumes from the next incomplete ledger row using
existing canonical state. CCFG-34 adds no automatic launcher or continuation
protocol. Existing final validation, finalization, and closeout behavior remains
unchanged.

## Recovery Advice Rule

Before escalating an ambiguous blocker that appears mechanical, the coordinator
may consult the existing `codebase_investigator` exactly once with a bounded
question and compact evidence.

The investigator remains unchanged and advisory. The coordinator may continue
only for recovery already authorized by the active runway and existing recovery
contract. Scope expansion, validation reclassification, semantic change, safety
weakening, destructive work, new lifecycle surfaces, multiple material choices,
or insufficient evidence still require the user or a reviewed amendment.

## Expected Implementation Ceiling

Primary expected surfaces:

- root `AGENTS.md` as the repository instruction hook;
- one temporary project-owned policy document;
- one focused contract test;
- `CHANGELOG.md`;
- feature metadata only when mechanically required.

A small generic instruction change is allowed only after concrete proof that the
repository-local overlay cannot enforce the behavior alone.

Forbidden implementation surfaces:

- `scripts/architecture_program_runner*.py`;
- runner state, transition, validation, receipt, artifact, telemetry, or worker
  architecture;
- new launcher, phase, protocol, store, schema, or agent result contract.

## CCFG-34 Self-Dogfooding

Plan CCFG-34 as one small vertical implementation slice unless concrete ownership
requires a second slice. Stop after its clean durable slice evidence. Use a fresh
invocation for later finalization or closeout when practical, without adding
machinery to automate that boundary.

## CCFG-26 And CCFG-29 Relationship

CCFG-34 is closed. CCFG-26 is open and unselected and requires a fresh
`plan-batch` invocation from COR-009, ADR 0004, current candidate code, and the
completed repo-owned slice-shape policy. The earlier interpretation that
CCFG-26 required permanent candidate requirements from #59, #60, and #61 is
superseded: #59 and #61 are rejected not-planned ideas, while #60 contributes
only completed slice-shape behavior through the accepted policy and its
closeout evidence.

CCFG-29 owns removal of the CCFG-34 policy and root `AGENTS.md` hook only after
the integrated candidate proves equivalent planning, slice execution, recovery
escalation, and no-successor behavior from the temporary repo-owned dogfooding
policy. No issue-number parity gate applies.

## Acceptance

- one automatically loaded repository-local policy;
- vertical slice and migration residue requirements for CCFG-26 through CCFG-29;
- at most one implementation slice per `work-batch` invocation;
- manual later invocation resumes from existing durable state;
- at most one existing-investigator consultation before eligible escalation;
- no runner architecture or advisor-contract changes;
- explicit CCFG-29 removal condition tied to the temporary dogfooding policy's
  accepted behavior, with no issue-number parity gate.

## Implementation Resolution

Final implementation review proved that `.codex/AGENTS.md` was outside the
normal repository-root instruction-discovery chain. A bounded reviewed amendment
replaced only that ineffective hook with root `AGENTS.md` and retargeted the
focused contract test.

Implementation commit `ba1e941` added exactly the root instruction hook, the
temporary policy, the focused contract test, and the changelog entry. Focused
pytest, Ruff, whitespace validation, test-quality review, and final independent
review were clean. CCFG-34 then closed without selecting a successor.

## Supersession

The first CCFG-34 dispatch, runway, and review at commit `a6e2a404` planned a
temporary execution-unit architecture across runner state, transitions, receipts,
and telemetry. That plan is superseded because it was disproportionate to the
temporary benefit.

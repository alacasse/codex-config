# Command-Owner Deepening Review

## Summary Recommendation

Deepen `plan-batch` first. It is the command-owner skill with the highest leverage and the most visible routing complexity: it must respect the program ledger as the only executable backlog, preserve selected dispatch or queued state, select exactly one bounded finding only when safe, and hand off to concrete spec creation without implementation.

I did not write this note at `docs/plans/programs/planning-state-tooling/notes/command-owner-deepening-review.md` because `planning-state-tooling` is no longer an active program. `docs/plans/CURRENT.md` and `docs/plans/programs/planning-state-tooling/README.md` point to `docs/plans/programs/codex-config/LEDGER.md` as the active ledger, so this report lives under the active program notes path.

## Current Architecture

The current architecture is a deliberate bridge state. The human-facing command-owner skills own human intent, routing, and stop conditions. Runtime skills still own much of the detailed implementation procedure. The main external seam is the human workflow command; the main internal artifacts crossing seams are the program ledger, selected dispatch, queued runway, active runway, and closeout evidence.

The command set is small and useful: `add-to-ledger`, `plan-batch`, `work-batch`, and `port-by-contract`. The risk is not that every bridge skill is bad. The risk is that `plan-batch` remains too much of a routing facade around `architecture-program-runway` and `batch-runway`, leaving future agents to remember the seam instead of exercising a deep interface.

## Command-Owner Depth Assessment

| Skill | Classification | Evidence | Risk |
|---|---|---|---|
| `add-to-ledger` | `bridge-but-acceptable` | Owns intake intent, source identity preservation, initial status, ledger row quality, and stop rules. Delegates placement and grouping mechanics to `planning-state`, `planning-artifacts`, and `architecture-program-runway`, which is a reasonable adapter seam. Deleting it would make fresh findings leak into `plan-batch` or ad hoc ledger edits. | Medium. It still has little concrete intake procedure, but it already prevents the worst confusion: candidate work versus executable backlog. |
| `plan-batch` | `shallow-facade` | Owns the right external interface, but most behavior is still "use planning-state, architecture-program-runway, then batch-runway create-spec." It prevents confusion today, but deleting it would push routing and backlog-source rules back into callers. | High. It is the most likely place for agents to accidentally scan external sources, bypass selected state, create more than one batch, or confuse dispatch creation with implementation. |
| `work-batch` | `bridge-but-acceptable` | Owns execution intent and hard stop rules: consume only current queued or active runway, do not select, do not create findings, do not broaden scope. Detailed execution properly stays with `batch-runway` because subagent orchestration, validation, review, commits, and recovery are large runtime procedures. | High if deepened too early. Duplicating `batch-runway` execution contracts would reduce locality and create drift. |
| `port-by-contract` | `deep-enough-now` | Owns a substantive workflow interface: modes, source intake, contract outputs, target design, handoff rules, and non-goals. It delegates to runway skills only after contract artifacts exist. | Low. Its main risk is misuse as a general rewrite shortcut, already covered by its interface and the routing contract. |

## Deepening Options

| Option | Leverage | Locality | Risk | Recommendation |
|---|---|---|---|---|
| A. Deepen `add-to-ledger` first | High for preventing backlog-source confusion at intake. | Medium; ledger row shaping would concentrate in one skill. | Medium validation difficulty; risks duplicating `architecture-program-runway` grouping rules. | Not first. Keep bridge-state unless intake mistakes recur. |
| B. Deepen `plan-batch` first | Highest. It is the command that turns the canonical ledger into executable runway state. | High; selection, dispatch handoff, and create-spec routing can become one stable command interface. | Medium. Validation can focus on routing examples, selected-state cases, no-ledger-stop cases, and one-spec output. Depends on `planning-state`, `planning-artifacts`, `architecture-program-runway`, and `batch-runway`. | Recommended first. |
| C. Deepen `work-batch` first | High in theory because execution is frequent. | Low now; execution knowledge belongs in `batch-runway`. | High validation difficulty; risks duplicating worker/reviewer/recovery contracts and worsening drift. | Do not deepen now. |
| D. Deepen `port-by-contract` first | Low incremental leverage; it is already deep enough. | Good existing locality. | Medium risk of broadening the skill into a general refactor launcher. | Do not deepen now. |
| E. Keep all command-owner skills bridge-state | Low short-term risk. | Low; routing complexity remains distributed across command owners and runtime skills. | Low validation difficulty, but medium confusion risk persists for "create the next specs batch." | Acceptable only as a pause, not the best next architecture move. |

## Support/Runtime Skill Disposition

| Skill | Recommended role | Rationale |
|---|---|---|
| `architecture-program-runway` | `runtime-procedure-owner` | Still owns program-level grouping, sequencing, selected dispatch packets, queue state, and closeout reconciliation. It should remain behind `add-to-ledger` and `plan-batch`, not become a direct human command. |
| `batch-runway` | `runtime-procedure-owner` | Owns concrete runway specs, slice execution, validation, review delegation, commits, recovery, and finalization. It is deep runtime machinery, not a candidate for deletion. |
| `planning-state` | `support-contract` | Provides the diagnostic-first pickup interface and CLI integration boundary. It should remain a shared support contract consumed by command owners and runtime owners. |
| `planning-artifacts` | `support-contract` | Owns project-neutral layout, naming, and artifact placement rules. It should not merge into a single command because many workflows need the same convention. |
| `legacy-removal` | `support-contract` | Provides evidence-backed legacy classification and handoff material for exceptional cases. It should stay agent-facing and not become a normal cleanup command. |
| `dead-surface-audit` | `support-contract` | Produces evidence for test-retained surfaces and deletion tests. It should remain narrow evidence support. |
| `test-quality-review` | `support-contract` | Provides focused review evidence about test confidence and design signals. It can be directly requested for audits, but it is not part of the main ledger command set. |

## Recommended Next Step

`plan-batch an existing finding`: use new ledger row `CCFG-12` to plan a bounded deepening batch for `plan-batch`.

The batch should not rewrite the whole skill system. It should make `plan-batch` the deeper command-owner interface for the "create the next specs batch" command by moving the routing decision table, selected-state cases, ledger-only source rules, and no-implementation stop behavior into a compact, testable command contract. `architecture-program-runway` and `batch-runway` should remain runtime owners behind it.

## Non-Goals

- Do not deepen `work-batch` by copying `batch-runway` execution contracts.
- Do not delete runtime/support skills just because command-owner skills exist.
- Do not create a new runner repository or implementation runway from this review.
- Do not revive archived APR or PST ledgers as active pickup sources.
- Do not turn this review into a broad skill-system refactor.

## Evidence Read

- `docs/skill-routing-contract.md`
- `docs/workflow-guide.md`
- `skills-lock.json`
- `README.md`
- `CONTEXT.md`
- `docs/adr/0002-human-facing-command-owner-skills.md`
- `skills/add-to-ledger/SKILL.md`
- `skills/plan-batch/SKILL.md`
- `skills/work-batch/SKILL.md`
- `skills/port-by-contract/SKILL.md`
- `skills/architecture-program-runway/SKILL.md`
- `skills/batch-runway/SKILL.md`
- `skills/planning-state/SKILL.md`
- `skills/planning-artifacts/SKILL.md`
- `skills/legacy-removal/SKILL.md`
- `skills/dead-surface-audit/SKILL.md`
- `skills/test-quality-review/SKILL.md`
- `docs/plans/CURRENT.md`
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/README.md`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`

Requested but inactive or missing:

- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`

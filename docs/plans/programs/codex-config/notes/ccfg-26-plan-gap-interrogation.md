# CCFG-26 Plan Gap Interrogation

## Verdict

`revise`

The queued CCFG-26 runway is not ready for execution. Its COR-009 direction is
still correct, its stable/candidate separation follows ADR 0004, and much of its
four-slice reasoning can be preserved. The blocking defects are narrower than a
redesign, but they sit on the execution path:

1. The proposed installed `work-batch/v1` owner has no defined production
   request/result/progress contract and no demonstrated artifact-only mechanism.
   `scripts/work_batch.py` and `tests/test_work_batch.py` do not exist at the
   reviewed candidate revision.
2. The green execution and recovery baseline exercises manufactured fixture
   owners, including a fixture-local `execution-state.json`, rather than the
   installed owner that CCFG-26 must create.
3. Slice 1 transfers the clean path but does not define the fail-closed result
   that must bridge validation, review, receipt, or interruption failures to
   Slice 2. That omission leaves Batch Runway recovery available as a silent
   fallback.
4. Slice 3 says APR can temporarily apply reconciliation, but the current APR
   contract forbids selected-dispatch and queue-state mutation. The plan's
   claimed independently usable Slice 3 state therefore has no coherent current
   production caller.
5. Slice 4 promises atomic reconciliation although the available mechanisms are
   two independently atomic CAS operations over `CURRENT.md` and `LEDGER.md`.
   There is no demonstrated ordering, inter-step fault recovery, or compound
   receipt.
6. Slice 4 also combines public reconciliation, partial-reconciliation recovery,
   direct legacy-route disposition, installed dependency removal, runner
   compatibility, change allowance, documentation, manifests, fixtures, and a
   broad test rewrite. The repository already exposes two defensible authority
   checkpoints, so "one rollback boundary" does not justify keeping all of this
   in one slice.
7. No required-green counterfactual makes accidental Batch Runway/APR invocation
   fail. Existing topology, prose, schema, and fixture tests can stay green while
   the new installed owner is absent or bypassed.
8. The runway does not require the accepted contract-first hybrid-skill shape.
   Candidate `skills/work-batch/SKILL.md` has no `## Contract` or
   `skill-contract/v1` block, fails the deterministic skill-contract validator,
   and CCFG-26 names neither that migration nor its validation. The proposed
   Python boundary is also underspecified: the script is told to validate and
   apply already-made decisions, but the plan never classifies which deterministic
   workflow decisions, YAML parsing, or evidence derivations must move into
   Python. A large prose coordinator plus a thin Python checker would satisfy the
   current wording while missing the intended architecture.
9. The refactor has no repository-authoritative rule that mechanically
   decidable work must live in code, and the runway has no code-shape acceptance
   beyond the existence of `scripts/work_batch.py`. It could therefore produce
   either a prose state machine or one large Python file made of ad hoc functions.
   Neither is an extensible command-owner module. The current four-slice framing
   also treats an additional production slice as a planning defect even when a
   larger number of scenario-complete slices would be the safer way to build and
   review the Python owner.

The clean planning review in
`batches/ccfg-26-work-batch-owner-transfer/review.md` proves that the exact draft
passed that review's checks. It does not prove the missing implementation
mechanisms, caller inventory, counterfactuals, cost, or intermediate failure
states.

## Exact Reviewed State

Canonical pickup was repeated from the stable checkout, without using historical
Graphify output:

- `python scripts/planning_state.py current --root docs/plans` reports one queued
  runway and no selected dispatch or active runway:
  `docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/runway.md`.
- `python scripts/planning_state.py validate --root docs/plans` reports `passed`,
  no errors, no obligations, and only the two existing redirect-ledger warnings.
- Canonical `docs/plans/programs/codex-config/CURRENT.md:9-17,151-155` agrees:
  selected dispatch `None`, active runway `None`, the CCFG-26 runway queued,
  implementation not started, and no successor selected.
- Canonical `docs/plans/programs/codex-config/LEDGER.md:156,174` records CCFG-26
  `Pending` and this exact batch `queued`. CCFG-27 through CCFG-29 remain open and
  blocked in their existing order at lines 157-159.

The exact live repository identities used for this interrogation are:

| Role | Root | Branch | Live revision | Worktree |
|---|---|---|---|---|
| Stable controller and canonical planning | `/home/alacasse/projects/codex-config` | `master` | `27c2ada4ce095ac42b102592d4d16237527c931d` | clean before report creation |
| Candidate implementation | `/home/alacasse/projects/codex-config-command-owner-redesign` | `implementation/command-owner-redesign` | `5c5ec9d52dd9033daa45f3a200031c152363b62c` | clean |

The queued artifact identities are:

| Artifact | Path | Identity |
|---|---|---|
| Dispatch | `docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/dispatch.md` | SHA-256 `02805a6bff0e3ad135d52d27b7c192584309ce3bfbf1736313b22b79e3c1d5cc` |
| Runway | `docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/runway.md` | SHA-256 `7e2512a8897a7207481908ec6788c529e97fc57338d41d34a5415dd1fea790d4` |
| Planning review | `docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/review.md` | SHA-256 `bdf80994708f1c51aacb9e576e44f3cdc4d445977bcaf4569e273dde062da854`; verdict `clean` |

The review is bound to stable planning revision
`6b575614983e72456a25875264ebab7e39ea0a72` and candidate revision
`5c5ec9d52dd9033daa45f3a200031c152363b62c`
(`review.md:3-26`). The live stable revision is later because commit `27c2ada`
queued the reviewed dispatch/runway/review and updated canonical state. That
queue commit changed five planning files with 1,425 insertions and 40 deletions;
it is not an unreviewed candidate implementation movement. A fresh strict
preflight against the plan snapshot returned `ready`, refreshed stable facts to
`27c2ada`, and left the candidate at `5c5ec9d`.

The authoritative result boundary comes from accepted COR-009 at snapshot
`caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`, specifically
`docs/design/command-owner-redesign/07-implementation-ledger-intake.md:366-385`.
ADR 0004, the live planning/execution carry-forward, the accepted slice-shape
policy and post-closeout correction, and the temporary dogfooding policy remain
current supporting authority. ADR 0003, the execution-state foundation,
CCFG-26B, issues #59 and #61, and their plans are historical evidence only.

## Required End State

### Required candidate product behavior after CCFG-26

One installed human-facing `work-batch` command must own the whole decision
flight for one already queued or active batch:

1. read Planning State `current` and `validate` as the sole semantic currentness
   gate;
2. decide proceed or stop;
3. choose the next incomplete slice from durable accepted artifacts;
4. delegate implementation to registered `runway_worker` and review to a
   separate registered `runway_reviewer`;
5. validate and accept or reject worker/reviewer results;
6. run and accept canonical validation;
7. accept the exact commit and receipt, including post-commit recovery;
8. recover validation failures, review findings, missing/stale evidence, and
   interruptions without choosing another slice;
9. retain completed-slice evidence;
10. run final validation and required final review;
11. produce one lineage-bound `planning-closeout/v1` artifact;
12. reconcile exactly that batch into `CURRENT.md` and `LEDGER.md` through the
    existing planning-store mechanisms;
13. recover a partial closeout or partial reconciliation idempotently; and
14. return reconciled idle state and stop without selecting or preparing a
    successor.

The installed semantic path must be:

```text
human or compatible runner
  -> installed work-batch skill
  -> work-batch/v1 deterministic boundary plus registered collaborators
  -> Planning State and planning-contract mechanisms
  -> one same-batch result
```

The skill may own orchestration while a deterministic script validates requests,
results, evidence, and store applications. Planning State remains semantic
currentness authority; `write_closeout_artifact`, `apply_ledger_decision`, and
`apply_current_document` remain mechanical stores; Git remains material-integrity
evidence. None of those mechanisms may independently decide proceed, acceptance,
recovery, closeout disposition, reconciliation, or successor selection.

### Required hybrid owner shape

The accepted hybrid format is not merely "a skill plus a script." DEC 0008 and
`docs/design/command-owner-redesign/03-contract-first-formats.md:5-36` require one
versioned YAML operational contract inside concise Markdown, deterministic
validation, and no duplicate machine facts in prose. Candidate
`skills/skill-authoring/SKILL.md:8-26` owns authoring-time support for that shape;
it is not a runtime dependency of the skill it helps author.

CCFG-26 must produce this explicit division:

```text
human or runner
  -> concise work-batch Markdown procedure + one skill-contract/v1 YAML contract
  -> private JSON work-batch/v1 request to scripts/work_batch.py
  -> Python-derived compact YAML handoff to one registered agent
  -> compact YAML agent result
  -> Python parse/validation/acceptance through private JSON transport
  -> JSON machine result or Markdown+YAML durable planning artifact
```

The installed `work-batch` command remains the semantic owner as one composite
module. Inside it:

- Python must own every result derivable uniquely from accepted artifacts:
  parsing and validating planning contracts and agent YAML, selecting the next
  incomplete slice, constructing closed-world handoff packets, checking leases
  and write scopes, running/capturing configured validation, checking Git diff,
  commit and receipt lineage, deriving exact replay/resume, producing closeout,
  and enforcing ordered reconciliation/idempotence/no-successor guards.
- The skill/default agent must retain only human-facing intent, direct role
  invocation, genuinely ambiguous proceed/stop or correction judgment, and the
  compact final explanation. It must not manually reproduce the deterministic
  state machine in prose.
- `runway_worker` owns implementation judgment and `runway_reviewer` owns
  independent review judgment. They do not accept their own outputs, mutate
  planning state, or invoke one another.
- YAML is appropriate for compact LLM handoffs/results and embedded operational
  contracts. JSON is appropriate for private skill-to-script/stdin-stdout
  transport, canonical hashing, subprocess/runner results, and machine receipts.
  Markdown remains the Git-reviewable durable envelope. No production
  `execution-state.json` is added.

This division does not move workflow ownership to a generic helper. It deepens
the `work-batch` command owner by putting repeatable mechanics behind one small,
testable Python interface while leaving actual implementation and review
judgment with the registered agents.

### Required code architecture

The command-owner refactor needs one repository-authoritative rule in the
accepted design, not merely a CCFG-26 prompt preference:

> If a workflow result can be derived deterministically from explicit inputs and
> accepted policy, production code owns that derivation. Skills and agents may
> invoke, supply evidence to, or explain the code result; they may not duplicate
> the algorithm in prose or independently reinterpret it.

For work-batch, "code" must mean a deep module, not a collection of unrelated
functions placed in one script. The amended plan must require:

- one small external interface at the installed `work-batch/v1` seam, with
  explicit typed request, action/result union, invariants, ordering, errors, and
  replay behavior;
- a thin JSON CLI adapter in `scripts/work_batch.py`, with the deterministic
  implementation organized behind it by cohesive responsibility rather than by
  runway slice or historical owner;
- internal seams only where behavior actually varies, such as a real Planning
  State/subprocess/Git/store dependency versus its focused test adapter;
  deterministic parsing and policy evaluation stay ordinary implementation
  unless a second real adapter exists;
- dependencies accepted by the module instead of discovered or constructed in
  its decision logic, and result values returned before side effects are applied
  where the existing store contracts permit that split;
- one canonical implementation for every invariant; Markdown, TOMLs, schemas,
  and tests may declare or verify the invariant but may not carry an alternate
  executable interpretation;
- behavior tests through the external interface, adapter tests at real seams,
  and counterfactual tests that survive internal refactoring instead of pinning
  private helper names or a particular file split; and
- architecture review of interface depth, locality, dependency direction, error
  modeling, and extension cost before each Python-heavy slice is accepted.

This does not require speculative classes, ports, or one file per concept. A seam
is justified only when at least two adapters or a real independent variation
exist. The exact internal module split should be chosen from the focused
prototype and the behavior seams, then recorded in the amended runway before
production implementation.

Slice count is subordinate to those code-quality and authority boundaries. The
clean execution scenario may remain one vertical slice if the prototype proves
it fits coherently. If it does not, the planner must use additional slices that
each leave a complete, callable, fail-closed authority state. It must not force a
monolith to preserve four slices, nor create horizontal "models/helpers/tests"
slices that have no production caller.

### Old decisions that must no longer be independently possible

After CCFG-26, no normal installed caller may independently obtain any of these
decisions from Batch Runway or APR:

- clean execution, slice choice, delegation, validation/review acceptance,
  commit acceptance, receipt acceptance, recovery, resume, finalization, or
  closeout production from Batch Runway;
- closeout disposition, `CURRENT.md`/`LEDGER.md` mutation choices, partial
  reconciliation recovery, or no-successor decisions from APR;
- execute-phase Batch Runway invocation or closeout-phase APR invocation from
  the local runner or goal-runner compatibility references.

Physical presence is not authority. Old files may remain only if their public
entrypoints are fail-closed, redirect-only without a second decision engine, or
otherwise unreachable from every installed normal caller. "No normal caller"
must be proved rather than asserted.

### Intentionally retained product mechanisms

- `scripts/planning_state.py` and the Planning State skill: retained as the
  semantic currentness diagnostic and evidence surface.
- `scripts/planning_contract.py`: retained as caller-directed CAS, immutable
  artifact, lineage, and idempotency mechanics.
- `agents/runway_worker.toml` and `agents/runway_reviewer.toml`: retained as
  registered role/result contracts, not acceptance owners.
- Runner serialized `select-dispatch`, `create-spec`, `execute`, and `closeout`
  identities: temporarily retained, but `execute` must invoke one public
  `work-batch` flight and `closeout` must be observation-only after CCFG-26.
- The strict cross-checkout bridge: retained only as the temporary mechanical
  development/cutover boundary, with no workflow decisions.

### Temporary stable-controller development bookkeeping

The real CCFG-26 implementation batch continues to be controlled and closed by
the stable generation, as required by ADR 0004 and `runway.md:1040-1059`. Stable
Batch Runway/APR use for this one development batch is not candidate product
behavior, is not cross-generation runtime communication, and does not license
the candidate to control its own implementation. The report must not confuse
stable closeout commits in canonical planning with candidate `work-batch`
acceptance fixtures and isolated-install tests.

### Work that remains outside CCFG-26

- CCFG-27 owns the runner public phase-model/old-mode migration decision and
  candidate cutover rehearsal; it does not switch the default generation.
- CCFG-28 owns physical deletion of the remaining Batch Runway/APR owners and
  the final default switch after rehearsal, including negative invocation proof.
- CCFG-29 owns integration into current master, bridge deletion, default Codex
  home rebinding, and removal of the temporary dogfooding policy/hook.
- Deferred execution telemetry, changed-line thresholds, coordinator-compaction
  telemetry, issue #59's recovery advisor, issue #61's fresh-flight design, and
  a new persistent execution-state model are not CCFG-26 prerequisites.

## Semantic Replacement Audit

The table describes the actual current candidate seam, the required target, and
the legacy disposition that the amended plan must make testable. `S4A` and `S4B`
refer to the minimum Slice 4 split proposed below.

| Decision | Current semantic owner and exact caller | Future semantic owner and exact caller | Apply mechanism | Transfer | Old-route terminal condition and classification |
|---|---|---|---|---|---|
| Clean slice execution and next-slice choice | `skills/work-batch/SKILL.md:91-105` loads Batch Runway; `skills/batch-runway/references/execute-slice-core-v1.md` chooses the next incomplete row and runs the loop | Installed `work-batch` skill calling the defined `scripts/work_batch.py` request/result boundary | validated runway/completed-slice evidence plus coordinator delegation | Slice 1 | **replaced** for candidate product calls; direct old entrypoint must fail closed or redirect without deciding; physical files deferred to CCFG-28 |
| Worker delegation | Batch Runway core delegates to registered `runway_worker` | `work-batch` delegates to the same registered role | v2 TOML result contract and strict handoff | Slice 1 | Batch Runway delegation route **replaced**; agent role **intentionally retained** because it is not a decision owner |
| Reviewer delegation | Batch Runway core delegates to registered `runway_reviewer` | `work-batch` delegates separately after canonical validation | v2 TOML result contract and fresh reviewer basis | Slice 1 | old coordinator route **replaced**; role retained |
| Validation acceptance | Batch Runway coordinator/core accepts validation | `work-batch` accepts an exact validation result | coordinator-run configured commands and deterministic result validation | Slice 1 for clean path; Slice 2 for correction | old acceptance route **replaced**; validation subprocess remains a mechanism |
| Review acceptance | Batch Runway coordinator accepts reviewer verdict | `work-batch` checks exact diff basis, status, findings, and required fixes | registered reviewer result | Slice 1/2 | old verdict acceptance **replaced** |
| Commit and receipt acceptance | Batch Runway core/coordinator commits and records receipts | `work-batch` accepts exact candidate movement and one idempotent receipt | real Git evidence plus a defined receipt path/shape | Slice 1/2 | old commit/receipt decision **replaced**; Git **intentionally retained** as integrity evidence only |
| Validation-failure recovery | `skills/batch-runway/references/execute-recovery-v1.md:40-50` | same installed `work-batch` owner | durable blocked result plus refreshed currentness/evidence | Slice 2 | old recovery route **replaced**; forbidden fallback |
| Review-finding recovery | `execute-recovery-v1.md:80-103` | same installed `work-batch` owner | corrected task-scoped diff, canonical revalidation, new review basis | Slice 2 | **replaced**; forbidden fallback |
| Interruption and same-slice resume | Batch Runway ledger/recovery procedure at `execute-recovery-v1.md:128-134` | `work-batch` re-derives the same incomplete slice from accepted artifacts | Planning State, runway, completed-slices, execution report, receipts, Git material facts | Slice 2 | **replaced**; old-format active state read/refuse policy retained until explicit migration or zero-live-state deletion |
| Execution currentness | Planning State decides semantics; current stable work-batch sequences stable bridge helpers | Planning State still decides semantics; installed `work-batch` decides proceed/stop from it | Planning State plus candidate mechanical identity/write-scope helpers | Slice 2 | Planning State **intentionally retained**; stable helper topology is not a target contract; Git-lifecycle fallback forbidden |
| Final validation | `skills/batch-runway/references/finalize-batch-v1.md:6-28` | `work-batch` | resolved validation profile and exact final range | Slice 3 | Batch Runway final validation decision **replaced** |
| Finalization and convergence | `finalize-batch-v1.md:30-108` | `work-batch` | complete slice evidence, cleanup-residue checks, final review | Slice 3 | old finalizer **replaced** |
| Completed-slice retention | Batch Runway core plus `ledger-retention-v1.md:18-70` | `work-batch` | existing `completed-slices.md` format/receipts | Slice 3 | old semantics **replaced**; Markdown evidence format **intentionally retained** as mechanism |
| Closeout production | Batch Runway finalization in prose; fixture directly calls `write_closeout_artifact` | installed `work-batch` | `scripts.planning_contract.write_closeout_artifact` | Slice 3 | old finalizer/producer **replaced**; immutable store retained |
| Partial closeout recovery | Batch Runway finalization/recovery is the current semantic owner; only the planning-contract fixture `_write_closeout` proves the exact-replay mechanism | installed `work-batch` | closeout idempotency key and exact replay | Slice 3 | Batch Runway recovery decision **replaced**; planning-contract artifact store **intentionally retained** as mechanism; fixture proof must be rebound to the installed owner |
| Same-batch reconciliation | APR is declared owner, but its own contract conflicts over queue mutation; fixture `_reconcile_closeout` calls stores directly | installed `work-batch` | ordered caller decisions using `apply_ledger_decision` and `apply_current_document` | S4A | APR reconciliation decision **replaced**; physical APR retained to CCFG-28 but direct mutation route fail-closed/conditioned |
| Partial reconciliation recovery | no demonstrated production owner; `partial-reconciliation-blocked` only detects corruption | installed `work-batch` | closeout anchor, per-document receipts, explicit state matrix and forward replay | S4A | current surface is **unclassified** and must become an owned work-batch behavior before execution |
| Runner `execute` | `architecture_program_runner_phase_contract.phase_skill_instruction` returns `$batch-runway execute-spec`; `CodexExecWorker.run_phase` launches that prompt | runner compatibility caller launches one public `$work-batch` flight | phase contract -> prompt -> `codex exec` | S4B | old runner route **replaced**; fixed phase identity **deferred to CCFG-27** |
| Runner `closeout` | phase contract returns `$architecture-program-runway closeout-runway` | observation-only compatibility over the already reconciled work-batch result | phase result/receipt validation only | S4B | APR closeout invocation **removed** from runner; phase identity deferred to CCFG-27 |
| Goal-runner closeout | `skills/architecture-program-runway/references/goal-runner-v1.md:68-72` invokes work-batch then APR closeout | public work-batch only; later step observes its reconciled result | compatibility documentation/installed reference | S4B | APR second call **removed**; current route is an omitted normal caller |
| No-successor enforcement | current ownership is split/ambiguous: work-batch says stop, while APR/runner closeout can return `next_phase=select-dispatch` | `work-batch` never selects/prepares a successor; outer runner may only decide process looping after observing a complete command result | reconciled Planning State plus result/phase transition validation | S4A/S4B | in-command successor route **removed**; outer-runner loop authority **intentionally retained** only if explicitly distinguished and deferred to CCFG-27 where applicable |

End-state residue must be classified as follows:

- Candidate Batch Runway execution/recovery/finalization semantics: **replaced**
  in Slices 1-3; physical files **deferred to CCFG-28**.
- Candidate APR reconciliation semantics: **replaced** in S4A; physical APR and
  exact schema/reference hosting still needed by the fixed runner are
  **deferred to CCFG-27/28**. This excludes `goal-runner-v1.md`'s semantic APR
  closeout call, which S4B must rebind in CCFG-26.
- Registered worker/reviewer v2 schemas: **intentionally retained**, reason:
  collaborator protocol rather than decision ownership.
- Planning State and planning-contract functions: **intentionally retained**,
  reason: generic semantic diagnostic and store mechanisms.
- Fixed runner phases: **conditioned on the new authority** in CCFG-26 and phase
  model decision **deferred to CCFG-27**.
- Strict bridge: **intentionally retained** as temporary mechanical development
  support; removal owner/condition: CCFG-29 final integration.
- Stable controller use for this real batch: **intentionally retained** under ADR
  0004; removal condition: stable same-batch CCFG-26 closeout, followed by later
  cutover/integration work. It is not a candidate product dependency.

## Unclassified Or Ambiguous Authority

1. **The installed `work-batch/v1` seam is unclassified.**
   `runway.md:240-262,560-568` says the skill owns orchestration and the script
   validates inputs/results and applies decisions, but there is no exact script
   entrypoint, request schema, result schema, staged operation set, progress
   reader, collaborator packet, receipt path, or error/replay contract. No future
   symbol can be named because the file is absent at `5c5ec9d`.

2. **Direct legacy invocation remains independently possible.**
   Candidate `codex-features.json:89-130` installs `work-batch`, `batch-runway`,
   and `architecture-program-runway` as separate features. Removing the two
   `requires` entries from work-batch does not make `$batch-runway` or
   `$architecture-program-runway` non-authoritative. The amendment must say
   whether each old entrypoint is fail-closed, redirect-only, uninstalled from a
   work-batch-only home, or retained for one exact compatibility caller.

3. **The Slice 3 APR apply route contradicts the current APR contract.**
   `skills/architecture-program-runway/SKILL.md:68-70` forbids selected-dispatch
   and queue-state mutation; lines 133-136 say `closeout-runway` must not mutate
   selected/queued state. Current `skills/work-batch/SKILL.md:102-104`
   simultaneously says APR updates selected dispatch and batch queue metadata.
   Slice 3 changes neither contract while claiming APR can reconcile.

4. **Goal-runner is an omitted normal caller.**
   `skills/architecture-program-runway/references/goal-runner-v1.md:68-72`
   invokes public work-batch and then directly invokes APR closeout. It appears in
   neither the migration matrix nor Slice 4's exact caller list.

5. **Agent v1 compatibility is unclassified.**
   `agents/runway_worker.toml:57-64` and
   `agents/runway_reviewer.toml:62-70` point v1 results at
   `skills/batch-runway/references/reporting-contracts-v1.md`. The plan says agent
   contracts must have no Batch Runway path dependency but does not choose among
   removing v1, relocating its schema, or retaining it with a named reason and
   future owner.

6. **Artifact-only progression is unspecified.**
   The planning runway is immutable; Planning State exposes the queued/active
   artifact pointers but no deterministic next-incomplete-slice owner. The plan
   must name how `work-batch` validates the execution ledger, completed-slice
   archive, receipts, and interruption evidence without inventing a second state
   model.

7. **Candidate lease preparation is not demonstrated.**
   `scripts/cross_checkout_context.py` exposes parsing, identity, write-scope,
   and receipt mechanics, but not stable-only
   `preflight_cross_checkout_live_lease` or
   `prepare_cross_checkout_context_refresh`. The carry-forward correctly says
   stable helper topology is not prescribed, but the plan must still prove the
   target mechanism for first-baseline comparison, two-observation movement
   detection, fresh worker/reviewer leases, and accepted movement.

8. **Partial reconciliation recovery has no owner or protocol.**
   `apply_current_document` and `apply_ledger_decision` are individually
   idempotent. `_reconcile_closeout` currently applies CURRENT first and LEDGER
   second. `partial-reconciliation-blocked` only manufactures invalid CURRENT
   and proves Planning State blocks; it does not resume after one real CAS.

9. **Outer-runner successor authority is ambiguous.**
   `architecture_program_runner_phase_contract.py:110-123` allows closeout to
   return `next_phase=select-dispatch`. That may be legitimate outer-runner loop
   authority, but it must be classified and distinguished from forbidden
   successor selection inside work-batch. It cannot remain an unnamed loophole.

10. **APR-hosted runner files remain a topology dependency.**
    `architecture_program_runner_environment.py` resolves its schema and runner
    reference beneath `skills/architecture-program-runway/`. This can be named
    compatibility hosting deferred to CCFG-27/28, but cannot be silently counted
    as "no APR dependency."

11. **The current known-red is not behavioral owner proof.**
    `test_architecture_program_closeout_rejects_dispatch_runway_only_evidence`
    is a prose/topology assertion. Promoting it after wording changes cannot show
    that an installed owner rejected incomplete evidence on the real path.

12. **The target skill is not required to become contract-first hybrid.**
    Candidate `skills/work-batch/SKILL.md` is still prose-only. Running
    `.venv/bin/python scripts/skill_contract.py validate --toolchain-root .
    skills/work-batch/SKILL.md` at `5c5ec9d` fails with
    `contract.block_count: expected exactly one ## Contract YAML block; found 0`.
    The runway contains no `skill-contract/v1`, `skill-authoring`, or direct
    target-document validation requirement. Its generic write ceiling includes
    `tests/test_skill_contract_catalog.py`, but that test does not validate
    work-batch. The same validator also rejects the current plan-batch skill,
    while add-to-ledger passes; therefore plan-batch is a useful runtime example,
    not complete proof of the desired authoring format.

13. **The Python/YAML/JSON responsibility boundary is unclassified.**
    Agent results are already exact YAML, but the dynamic handoff inputs remain
    prompt prose. The runway defines no closed-world YAML handoff, no private JSON
    stdin/stdout request/result fields, no owner for parsing returned YAML, and no
    matrix separating deterministic Python behavior from model judgment. The
    phrase "applies already-made decisions" at `runway.md:560-563` can leave
    next-slice derivation, evidence checking, validation capture, Git/receipt
    checks, recovery, and reconciliation as duplicated prose procedures.

14. **The Python module shape and extension strategy are unclassified.**
    The runway names only `scripts/work_batch.py`; it does not define whether
    that path is a thin installed adapter or the entire implementation, the
    external interface tests should use, cohesive internal responsibilities,
    dependency direction, typed result/error model, or rules for adding later
    Slice 2-4 behavior without branching the clean-path engine. Candidate
    `scripts/plan_batch.py` demonstrates useful private JSON transport but is a
    roughly two-thousand-line single module; it cannot serve as sufficient proof
    of the requested clean and extensible code shape.

15. **The fixed slice framing conflicts with code-quality-first execution.**
    The dispatch rejects a fifth production slice while the report already finds
    a valid S4A/S4B split. The user has now made the priority explicit: use as
    many coherent slices as required to build the deterministic module properly.
    The plan must replace fixed-count pressure with scenario-complete authority,
    interface stability, reviewability, and coordinator-context criteria.

Every item above is a likely planning defect until explicitly classified in an
amended migration matrix and acceptance test.

| Item | Question disposition |
|---:|---|
| 1. Installed owner seam | `requires_bounded_plan_amendment` |
| 2. Direct legacy invocation | `requires_bounded_plan_amendment` |
| 3. Slice 3 APR apply route | `requires_bounded_plan_amendment` |
| 4. Goal-runner normal caller | `requires_bounded_plan_amendment` |
| 5. Agent v1 compatibility | `requires_bounded_plan_amendment` |
| 6. Artifact-only progression | `requires_bounded_plan_amendment` |
| 7. Candidate lease preparation | `requires_bounded_plan_amendment` |
| 8. Partial reconciliation recovery | `requires_bounded_plan_amendment` |
| 9. Outer-runner successor authority | `requires_bounded_plan_amendment` |
| 10. APR-hosted runner files | `deferred_to_named_future_batch` for physical relocation/deletion under CCFG-27/28, but `requires_bounded_plan_amendment` to classify their CCFG-26 compatibility role |
| 11. Known-red proof type | `requires_bounded_plan_amendment` |
| 12. Contract-first work-batch skill | `requires_bounded_plan_amendment` |
| 13. Python/YAML/JSON responsibility boundary | `requires_bounded_plan_amendment` |
| 14. Python module shape and extension strategy | `requires_bounded_plan_amendment` |
| 15. Fixed slice framing | `answered_by_user_direction`; dispatch/runway correction `requires_bounded_plan_amendment` |

## Slice 1 Questions

### What complete scenario works afterward?

The intended scenario is: an installed public work-batch picks the next clean
slice, delegates to a worker, runs canonical validation, delegates independent
review, accepts the exact commit/receipt, records completed-slice evidence, and
stops at the next slice boundary. This is a good vertical target.

The current plan does not prove that scenario is installed or callable. The
candidate has only `skills/work-batch`; there is no `scripts/work_batch.py` or
`tests/test_work_batch.py`. Slice 1 Work item 6 requires installing/linking the
new owner through the work-batch feature, but the worker brief forbids the worker
from running installations and the slice does not name who executes and accepts
an installed-entrypoint check. The only fully sequenced fresh/candidate-home
installation and dry-run gate appears in final validation after all slices
(`runway.md:1014-1017`).

### Which production caller uses it?

The future caller is the installed `skills/work-batch/SKILL.md` command, with the
runner still on the old path until later. Its script handshake is missing, so
there is no exact production call to inspect or poison today.

### What happens off the happy path?

This is the most serious Slice 1 boundary defect. Validation failure, review
findings, missing receipt, post-commit receipt failure, or interruption belongs
to Slice 2, but Slice 1 removes the clean Batch Runway route and forbids fallback.
The plan does not require Slice 1 to emit a durable, exact, fail-closed result
that a later work-batch invocation can resume. Without that contract, the old
Batch Runway recovery procedure remains the easiest accidental fallback.

The amended Slice 1 must require:

- fail-closed stop for every validation/review/receipt/interruption branch not
  yet recoverable;
- durable evidence consisting only of already accepted artifacts and an exact
  compact report/receipt, not new execution state;
- no invocation of old recovery/finalization/reconciliation routes;
- a later Slice 2 test that resumes the exact Slice 1 blocked result; and
- real-Git counterfactuals for HEAD movement, wrong repository, unrelated commit
  content, commit success followed by receipt-write failure, and a receipt
  naming an absent commit.

### Is the state independently usable and rollback-safe?

Only after the missing fail-closed contract and Slice 1 candidate-only install
are added. Code rollback is safe before canonical program reconciliation because
candidate fixtures/temp roots contain effects. Reverting the Slice 1 candidate
commit must restore the old clean-path route in the development checkout, but
the stable controller still controls the real batch.

### Which old owner remains, and can it silently become fallback?

Batch Runway recovery, finalization, and APR reconciliation remain physically
present. Recovery is not listed as temporary residue in Slice 1 even though the
new clean owner can encounter a validation/review failure immediately. Yes, it
can silently become fallback under the current wording.

### Does the slice transfer one decision boundary?

It transfers a coherent clean accepted-slice boundary, not merely related
files. That boundary is valid after the missing script handshake and fail-closed
branches are proved.

### Expected surfaces and cost

Likely production surfaces include `skills/work-batch/**`, new
`scripts/work_batch.py`, agent contracts if schema references move, exact clean
execution pieces under `skills/batch-runway/**`, manifest/routing metadata, real
Git test fixtures, scenario bindings, and new `tests/test_work_batch.py`. The
plan gives a path ceiling, not a file or line estimate. CCFG-25 Slice 1 was 12
files and +3,887/-145 lines for an analogous installed command owner, so a
single coordinator context cannot be assumed. A pre-execution prototype and an
exact expected-file inventory are required.

### Smaller split considered

Splitting worker, validation, review, or commit into separate product slices
would create unusable horizontal layers and should be rejected. A disposable
pre-Slice-1 feasibility gate is different: it proves the decisive request/result
and artifact-progression primitive without accepting production ownership. That
gate is required; it is not a new runtime architecture or durable product slice.

Disposition: `requires_bounded_plan_amendment`.

| Slice 1 material question | Disposition |
|---|---|
| Complete post-slice scenario and production caller | `requires_bounded_plan_amendment` |
| Unhappy path and durable intermediate state | `requires_bounded_plan_amendment` |
| Independent usability and rollback | `requires_bounded_plan_amendment` |
| Remaining old owner and fallback risk | `requires_bounded_plan_amendment` |
| Coherence of the clean decision boundary | `answered_by_repository_evidence` |
| Expected files, tests, agents, subprocesses, reviews, and context cost | `missing_but_agent_resolvable` |
| Smaller split | `answered_by_repository_evidence` |

## Slice 2 Questions

### What complete scenario works afterward?

Given the exact fail-closed result from Slice 1, public work-batch refreshes
currentness, corrects validation or review failures, obtains separate
worker/reviewer leases, accepts exact movement/receipts, commits the same slice,
and resumes after interruption without advancing incorrectly. This is a coherent
vertical recovery scenario only if Slice 1 defines its input.

### Which production caller and mechanism use it?

The installed work-batch command must use Planning State, exact repository facts,
the immutable runway, completed-slice archive, execution report, receipts, and
Git integrity. Current scenarios do not prove that path:

- `workflow_adapters._run_execution` manufactures
  `workspace/execution-state.json` and injected collaborators;
- catalog execution rows at
  `tests/fixtures/command-owner-scenarios/catalog.yaml:640-747` are
  `source_characterization`;
- currentness scenarios call `currentness_adapters.py` directly, not an installed
  work-batch owner.

The amendment must enumerate the existing durable inputs and define how the
installed boundary validates them. It must not port the fixture execution-state
file into production.

### Is the intermediate state usable and rollback-safe?

After amendment, yes: clean and failed/interrupted slice executions converge on
one owner and one accepted commit/evidence path. Slice 2 can be reverted while
retaining Slice 1's clean path, but only if the resulting owner explicitly
returns to the Slice 1 fail-closed behavior rather than the old recovery engine.

### Which old owner remains?

Batch Runway finalization remains to Slice 3 and APR reconciliation to S4A. Old
Batch Runway recovery must no longer be callable by any migrated public path.
Old-format active state remains read-only/refused. The amendment must give that
legacy state a named inventory, completion condition, and future deletion owner;
"later explicit migration" alone is not an owner.

### Does the slice transfer one decision boundary?

Recovery and currentness belong together because a recovery action cannot be
accepted without currentness, fresh leases, result echo, and exact reviewer
basis. The current smaller-alternative reasoning is sound.

### Expected surfaces and cost

The change likely touches the same installed owner, currentness adapters/tests,
recovery procedures under Batch Runway, agent result validation, real Git
fixtures, and manifest/routing assertions. No exact file count, line estimate,
or `tests/test_work_batch.py` runtime exists. Multiple fail/correct/revalidate/
rereview cases make this likely more expensive than the nominal file list
suggests. It should not start until the Slice 1 proof makes its input contract
fixed.

### Smaller split considered

Separating currentness from recovery would create a recovery owner able to act
without the sole semantic gate. That split should be rejected. Clean-error
quarantine belongs in Slice 1, not a new Slice 2A.

Disposition: `requires_bounded_plan_amendment` for the input/mechanism contract;
the recovery/currentness grouping itself is `answered_by_repository_evidence`.

| Slice 2 material question | Disposition |
|---|---|
| Complete recovery scenario, caller, and production mechanism | `requires_bounded_plan_amendment` |
| Independent usability and rollback | `requires_bounded_plan_amendment` |
| Remaining old owner and old-format disposition | `requires_bounded_plan_amendment` |
| Coherence of recovery plus currentness | `answered_by_repository_evidence` |
| Expected files, tests, agents, subprocesses, reviews, and context cost | `missing_but_agent_resolvable` |
| Smaller split | `answered_by_repository_evidence` |

## Slice 3 Questions

### What complete scenario works afterward?

The intended complete scenario is: from an accepted final implementation slice,
work-batch runs final gates, validates complete evidence, produces one immutable
lineage-bound closeout, and exact-replays after a partial closeout write. That is
a useful production boundary even before work-batch owns program reconciliation.

### Which production caller uses it?

The new installed work-batch owns closeout production. The existing fixture
cannot prove this boundary because `observe_closeout -> _run_closeout` always
calls `_reconcile_closeout` after `write_closeout_artifact`
(`workflow_adapters.py:1488-1552,1959-2010`). A closeout-production-only
installed-owner scenario is missing.

The queued runway additionally claims APR is the temporary next caller. That is
not currently true in a coherent way: APR forbids the queue mutations it would
need to perform. Either the amended Slice 3 must make APR an explicit,
conditioned, apply-only compatibility route for this exact closeout, or it must
state that Slice 3 stops after durable closeout and that S4A is the only
reconciliation owner. It cannot claim a working APR reconciliation scenario
while prohibiting APR changes.

### What happens off the happy path?

`write_closeout_artifact` already proves immutable lineage and per-artifact exact
replay. The installed owner must additionally reject incomplete slice evidence,
foreign batch identity, unresolved placeholders, stale final review, and any
closeout that encodes a successor. Old Batch Runway finalizer must be a tripwire
that fails if called.

### Is it independently usable and rollback-safe?

Closeout production is independently useful if the report is explicit that the
batch is not reconciled yet and identifies the one next reconciliation caller.
It is rollback-safe because closeout is immutable and replayable; reverting code
does not delete or overwrite the artifact. It is not correct to describe APR
reconciliation as operational until its contradictory contract is repaired or
the route is removed from this intermediate state.

### Which old owner remains?

Only same-batch reconciliation may remain. Batch Runway finalization and closeout
production are replaced. The real CCFG-26 stable-controller closeout remains a
separate development-bookkeeping operation and must not be used as target-owner
proof.

### Does the slice transfer one decision boundary?

Final validation plus closeout production is coherent: closeout without accepted
final gates is unusable, while final validation alone is only a gate. The current
grouping is defensible.

### Expected surfaces and cost

Likely surfaces are the installed owner, exact finalization/retention references,
closeout contract tests, Planning State closeout checks, fixture separation,
manifest/routing metadata, and complete-evidence tests. The store implementation
is read-only. Exact files and line deltas remain unmeasured.

### Smaller split considered

Final validation alone should not become a slice. Closeout production and
program reconciliation should remain separate because they have different
effects, failure recovery, and rollback semantics. The plan correctly separates
those two, but it must add a production proof for the closeout-only checkpoint.

Disposition: `requires_bounded_plan_amendment` for the temporary caller and
counterfactual proof; the selected finalization/closeout-production boundary is
otherwise `answered_by_repository_evidence`.

| Slice 3 material question | Disposition |
|---|---|
| Complete scenario and production/next caller | `requires_bounded_plan_amendment` |
| Unhappy path counterfactuals | `missing_but_agent_resolvable` after the owner contract is amended |
| Independent usability and rollback | `requires_bounded_plan_amendment` |
| Remaining old owner | `requires_bounded_plan_amendment` |
| Coherence of final validation plus closeout production | `answered_by_repository_evidence` |
| Expected files, tests, agents, subprocesses, reviews, and context cost | `missing_but_agent_resolvable` |
| Smaller split | `answered_by_repository_evidence` |

## Slice 4 Questions

### What complete scenario works afterward?

The current Slice 4 intends one complete public and runner scenario: work-batch
reconciles a complete closeout, returns idle, runner `execute` invokes work-batch,
runner `closeout` observes, installed dependencies/docs/manifests no longer route
to legacy owners, and no successor is selected. That is a valid CCFG-26 end
state, but it is not one indivisible authority transition.

### Which production callers use it?

At minimum:

- human/agent public `work-batch`;
- direct installed Batch Runway and APR skill entrypoints;
- `architecture_program_runner_phase_contract.phase_skill_instruction` through
  `architecture_program_runner_command.build_prompt` and
  `architecture_program_runner_workers.CodexExecWorker.run_phase`;
- `skills/architecture-program-runway/references/goal-runner-v1.md`;
- installed feature dependency/link resolution in `codex-features.json`;
- worker/reviewer v1 and v2 contract consumers;
- routing/guide/README callers and tests.

The current migration matrix omits several of these.

### What happens off the happy path?

The decisive unproved behavior is partial reconciliation. Current production
mechanisms provide separate calls:

- `scripts.planning_contract.apply_current_document` at lines 437-524;
- `scripts.planning_contract.apply_ledger_decision` at lines 553-650.

The current fixture applies CURRENT first, then LEDGER. That can clear batch
identity before a ledger failure. The accepted behavioral matrix at
`docs/design/command-owner-redesign/05-behavioral-test-matrix.md:95-108` instead
requires:

- closeout exists first;
- closeout-written/reconciliation-failed retry consumes the same closeout;
- ledger reconciled before pointer-cleanup failure yields a visible partial state
  and idempotent retry; and
- pointer-cleared before ledger failure is rejected or repaired without losing
  batch identity.

The amendment should define an ordered, fail-closed saga using existing stores:

1. validate or exact-replay the closeout;
2. apply or exact-replay the CCFG-26 ledger finding mutation;
3. clear only the same batch's CURRENT pointers and set `latest_closeout` last;
4. on restart, derive the state from closeout plus per-document receipts and roll
   forward; and
5. reject or repair the forbidden CURRENT-first state without selecting a
   successor.

If the existing receipts cannot make that deterministic, execution stops for a
semantic mechanism amendment. The report does not authorize a new store or
state model.

### Is it independently usable and rollback-safe?

The current "revert Slice 4" rollback is incomplete once canonical CURRENT or
LEDGER effects exist. Reconciliation recovery is forward and idempotent, not a
Git code rollback. Before canonical mutation, candidate code rollback is safe;
after the first store receipt, the only safe path is exact roll-forward from the
same closeout.

### Are there two independently usable authority states?

Yes:

1. **S4A — public reconciliation owner.** Public installed work-batch owns
   same-batch reconciliation, partial recovery, and no-successor behavior. The
   old runner/APR compatibility calls remain named but deliberately fail closed
   until S4B; they may not apply reconciliation or fall back to their old
   decisions. S4A proves a usable public-command checkpoint but does not claim
   that every installed caller has been cut over.
2. **S4B — runner and installed caller cutover.** Runner `execute` switches to a
   public work-batch flight, runner `closeout` becomes observation-only,
   goal-runner drops its APR call, old direct entrypoints are made fail-closed or
   otherwise unavailable to normal installs, feature dependencies and v1 agent
   paths are resolved, change allowance is updated, and docs/manifests/tests
   converge.

The existing smaller-alternative rejection at `runway.md:953-958` assumes any
temporary APR caller invalidates the intermediate state. The dogfooding policy
allows temporary coexistence when the caller, reason, future owner, removal
condition, and no-fallback rule are explicit. S4A is a usable public-command
checkpoint; S4B is a separate compatibility/caller checkpoint.

### Runner change-allowance issue

The runway says to extend "execute-phase" allowance, but after `execute` the
production runner calls `check_worktree(..., "closeout", extra_paths=...)` at
`architecture_program_runner.py:367-374`. Current allowance gives execute only
spec/dispatch and closeout only ledger/spec/receipt
(`architecture_program_runner_change_allowance.py:425-442`). S4B must name and
test pre-execute, post-execute-as-closeout, and observation-phase allowances for
exact CURRENT, LEDGER, closeout, completed-slices, and receipt paths while
rejecting arbitrary sibling Markdown.

### Expected surfaces and cost

The current Slice 4 names three owner directories, two runner modules, the
feature manifest, four documentation/metadata categories, scenario adapters,
and broad lifecycle/manifest/routing/runner/currentness/agent tests. The three
directory entries alone currently expand to 29 files, and the ceiling contains
18 named test/fixture path entries. The advertised 32-path ceiling is an authorization
ceiling, not a credible file-change estimate.

This concentration is not reasonably assumed to fit one coordinator context.
The split above reduces semantic and rereview coupling without creating a new
architecture.

Disposition: `requires_bounded_plan_amendment`.

| Slice 4 material question | Disposition |
|---|---|
| Complete end-state scenario | `requires_bounded_plan_amendment` |
| Exact production caller inventory | `missing_but_agent_resolvable` |
| Partial reconciliation unhappy path and forward recovery | `requires_bounded_plan_amendment` |
| Rollback semantics after canonical mutation | `requires_bounded_plan_amendment` |
| Existence of two usable authority checkpoints | `answered_by_repository_evidence` |
| Runner post-execute change allowance | `requires_bounded_plan_amendment` |
| Expected files, tests, agents, subprocesses, reviews, and context cost | `missing_but_agent_resolvable` |

## Counterfactual Validation Audit

Existing execution/currentness/closeout coverage is useful mechanism evidence,
but it is not sufficient owner-transfer proof:

- execution scenarios are `source_characterization` and run
  `workflow_adapters._run_execution`, which manufactures `execution-state.json`,
  injected collaborators, and a synthetic commit;
- currentness scenarios invoke `currentness_adapters.py` directly;
- closeout scenarios directly call planning-contract functions;
- the known-red lifecycle guard checks prose/topology;
- manifest/routing tests can prove links and strings while an old owner remains
  callable; and
- no isolated installed-owner acceptance currently fails when legacy features
  are absent.

Required counterfactuals by authority:

| Authority | Existing coverage | Required counterfactual before acceptance | Disposition |
|---|---|---|---|
| Hybrid skill structure | `skill-authoring` and `skill-contract.py` prove the format generically; add-to-ledger passes it | validate the installed `skills/work-batch/SKILL.md` directly and fail if the single `skill-contract/v1` block is absent, duplicated, inconsistent with frontmatter, or conflicts with retained owners | `requires_bounded_plan_amendment` |
| Private Python and agent transport | worker/reviewer outputs are YAML-only; plan-batch/add-to-ledger demonstrate JSON subprocess transport | Python rejects malformed YAML, duplicate/extra fields, wrong interface/version/lineage, prose outside the result, malformed JSON, and unknown JSON fields before any acceptance or write; a prose-only handoff cannot satisfy the installed contract | `requires_bounded_plan_amendment` |
| Clean execution, worker delegation, validation/review acceptance | fixture state machine only | install work-batch without Batch Runway/APR; old clean entrypoint is a bomb; real installed clean flight must pass | `missing_but_agent_resolvable` |
| Validation-failure recovery | fixture recovery using rejected state file | old recovery callable raises; installed owner returns the exact fail-closed result and later corrects/resumes it | `requires_bounded_plan_amendment` |
| Review-finding recovery | injected fixture reviewer | old review-correction path raises; stale/foreign reviewer basis is rejected before commit; corrected review succeeds through installed owner | `missing_but_agent_resolvable` |
| Commit/receipt acceptance | synthetic 40-character commit in fixtures | real temporary Git repo: clean review then HEAD movement, wrong repo, unrelated content, missing commit, commit-success/receipt-failure, idempotent receipt recovery | `requires_bounded_plan_amendment` |
| Interruption resume | fixture-local execution state | remove/poison old resume route; restart installed owner from runway/completed-slices/report/receipts only; prove same slice selected | `requires_bounded_plan_amendment` |
| Currentness | strong direct adapter checks for leases/reviewer bases | installed owner must call the currentness mechanism; make adapter/mechanical helper return contradictory facts and require fail-closed result | `missing_but_agent_resolvable` |
| Final validation/finalization | Batch Runway prose and generic tests | old finalizer raises; incomplete final evidence cannot produce closeout; installed owner accepts exact complete evidence | `missing_but_agent_resolvable` |
| Completed-slice retention | Batch Runway retention contract | old ledger-retention decision path unavailable; installed owner accepts exact prior completed rows and rejects placeholders/foreign commits | `missing_but_agent_resolvable` |
| Closeout production/partial write | `write_closeout_artifact` exact replay is strong mechanism proof | source-characterization adapter may pass while installed owner is forced to fail; acceptance must fail; old finalizer is a bomb | `missing_but_agent_resolvable` |
| Same-batch reconciliation | direct fixture store calls | APR returns contradictory disposition or tries to mutate; work-batch rejects/never invokes it; foreign/dispatch-only evidence rejected | `requires_bounded_plan_amendment` |
| Partial reconciliation | only malformed partial-state detection | fault after closeout, after ledger before CURRENT, and forbidden CURRENT-first; restart installed owner and prove exact roll-forward/no successor | `requires_bounded_plan_amendment` |
| Runner execute | exact prompt-string assertion | use production `CodexExecWorker` path with a fake `codex` executable that records prompt and fails if `$batch-runway`/APR appears; separately execute legacy-free installed owner | `missing_but_agent_resolvable` |
| Runner closeout | exact prompt/topology assertion | observation phase must fail if it attempts APR mutation; reconciled receipt remains unchanged | `missing_but_agent_resolvable` |
| No successor | direct fixture leaves no successor | another `Ready` finding exists and APR proposes/selects it; work-batch must still reconcile only current batch and stop | `requires_bounded_plan_amendment` |
| Physical old path remains | prose and manifest presence tests | leave old file physically present, then prove no normal manifest, skill, runner, goal-runner, agent, docs, or acceptance caller reaches its decision path | `missing_but_agent_resolvable` |

The strongest practical counterfactual is a fresh Codex home containing only
`work-batch`, Planning State, planning-contract mechanisms, and registered agent
contracts. Run clean, failure/recovery, finalization, closeout, reconciliation,
and no-successor cases there. Any accidental Batch Runway/APR import or link must
fail because it is absent, not because a text assertion says it should be absent.

## Feasibility Questions

| Behavior | What is already demonstrated | What is not demonstrated | Required disposition |
|---|---|---|---|
| Contract-first hybrid skill | `skill-authoring`, `skill_contract.py`, and add-to-ledger demonstrate one YAML contract plus concise Markdown | work-batch contract extraction, accepted ownership catalog, direct validation, and migration comparison | amend Slice 1; no new schema or runtime skill-authoring dependency |
| Python/YAML/JSON boundary | add-to-ledger and plan-batch demonstrate private JSON stdin/stdout; worker/reviewer TOMLs demonstrate exact YAML results | closed work-batch JSON operations/result union, Python-rendered YAML handoffs, Python YAML parsing, and a responsibility matrix | prototype before production Slice 1; `requires_bounded_plan_amendment` |
| Deep work-batch module | runner owner modules demonstrate that Python can be split by responsibility; temporary roots/repos provide real local test adapters | small external interface, typed action/result/error model, cohesive internal module map, dependency injection, and proof that later recovery/finalization behavior extends rather than forks the clean path | interface-first prototype and architecture review before Slice 1; exact file split decided from behavior seams |
| Planning State semantic currentness | real `current`/`validate` subprocesses and strong lease/reviewer-basis scenarios | installed work-batch sequencing and target lease preparation | focused pre-Slice-1 prototype; `requires_bounded_plan_amendment` |
| Work-batch request/result boundary | analogous `scripts/plan_batch.py` installed owner exists from CCFG-25 | any `work-batch/v1` entrypoint, request/result/error/progress contract | prototype before production Slice 1; stop if it needs new state/schema |
| Artifact-only next-slice/resume derivation | immutable runway, completed-slices/report/receipt conventions exist | deterministic reader/validator and ambiguity rules | prototype and exact contract before Slice 1 |
| Worker/reviewer result validation | registered TOMLs own exact v2 schemas | v1 disposition and installed-owner acceptance binding | agent-resolvable in Slice 1 amendment |
| Real commit/receipt recovery | Git and stable coordinator practices exist | target receipt format/path and post-commit failure recovery | real-Git experiment before accepting Slice 1 |
| Closeout production | `write_closeout_artifact` proves lineage, immutable write, and exact replay | installed-owner binding and closeout-only scenario | safe to resolve in amended Slice 3 after the owner contract is proven |
| Two-document reconciliation | individual CURRENT/LEDGER CAS and idempotency are implemented | ordered cross-document recovery, state matrix, and lost-batch-identity repair | focused S4A prototype/fault matrix before production mutation |
| Runner compatibility rebind | phase instruction -> prompt -> `CodexExecWorker` is clear and tested | behavioral proof of new owner rather than string replacement; post-execute allowance | safe in S4B with counterfactual subprocess test |
| Legacy-free installation | installer/link machinery and CCFG-25 precedent exist | work-batch behavior in a home without old owners | add per-Slice-1 and final installed acceptance |

The two decisive primitives are the installed owner handshake/artifact-only
progression and forward-recoverable reconciliation. Both can be tested with
temporary planning roots and temporary Git repositories without new persistent
state. They must be demonstrated before their production slices. If either
proof requires a new canonical state model, store, schema, runtime process
protocol, or cross-generation communication, the runway's stop condition fires
and a new user/design decision is required.

## Expected Cost And Execution Multipliers

### Repository-backed measurements

- The exact four-file known-red baseline in `runway.md:102-113` currently
  reports 70 passed, 16 subtests passed, and one failed prose assertion. A fresh
  run at candidate `5c5ec9d` took 102.20 seconds elapsed.
- The runway command
  `.venv/bin/python -B scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios`
  covered 82 scenarios and took 0.28 seconds in the fresh audit.
- The exact runway command
  `.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_planning_contract_artifacts.py tests/test_planning_state.py -k closeout`
  reported 60 passed, 139 deselected in 5.11 seconds. The exact two-node
  currentness command at `runway.md:445-448` reported two passed in 1.79 seconds.
  These are local samples, not future `tests/test_work_batch.py` estimates.
- The slice-shape post-closeout evidence at the same candidate revision records
  198 focused tests plus 201 subtests in 123.38 seconds and exact acceptance of
  25 tests, 82 scenarios, 31 contracts, and 17 families in 87.91 seconds
  (`batches/ccfg-26-slice-shape-policy-correction/post-closeout-correction.md:70-98`).
- `tests/test_work_batch.py` does not exist. Its per-slice or final runtime cannot
  be estimated credibly.
- Candidate installation timing, stable-home comparison timing, agent wall time,
  correction-loop time, and coordinator context use have not been persisted.

### Likely files and line delta

The plan authorizes 32 candidate path entries, but three are whole directories
containing 29 current files, and 18 entries are named test/fixture paths. This is not
an expected changed-file count. No per-slice path manifest or line estimate is
provided.

CCFG-25 is the best local analogue, not a numeric promise:

| Evidence | Files | Insertions | Deletions |
|---|---:|---:|---:|
| CCFG-25 full candidate range | 38 | 5,223 | 1,602 |
| Slice 1 commit `5aa5add` installed `plan-batch` owner | 12 | 3,887 | 145 |
| Slice 2 commit `12f7072` legacy planning-owner removal | 31 | 1,334 | 1,460 |
| Slice 3 commit `89671ec` convergence docs | 1 | 5 | 0 |

The CCFG-25 total diff was 375,544 bytes. Its exact acceptance recorded 38.73486
seconds evidence time and 62.16 seconds CLI elapsed. These figures and the
38-file total are recorded in
`batches/ccfg-25-planning-ownership-transfer/closeout.md:63,94-104`; the per-slice
figures are verified `git show --stat` results for the three commits named in the
table. CCFG-25 also required bounded validation amendments because the planned
BasedPyright scope was not executable as written. CCFG-26 should not repeat the
assumption that a path ceiling or green baseline predicts implementation size.

Before execution, the amended runway must record for each slice:

- exact expected files or a narrow enumerated directory subset;
- expected production surfaces rather than a single broad category;
- a defensible line-delta range after the prototype, or explicitly `unknown`
  with the measurement gate;
- exact required and conditional commands with one current runtime sample;
- exact install cadence and measured install/dry-run time;
- expected worker, reviewer, specialist, and rereview calls; and
- the condition that stops a slice before coordinator compaction makes its
  acceptance basis unreliable.

### Repeated validation and agent multipliers

The current four-slice plan implies, before any correction:

- four worker invocations;
- four independent slice reviews;
- one final independent runway review;
- delta-only test-quality review after every test-changing slice and again for
  the final range, at least five passes;
- scenario validation at least once per slice plus final, at least five runs;
- four candidate commits plus unspecified stable receipt/closeout commits;
- candidate-only installation needed after Slice 1 under the amendment, plus
  the final fresh and isolated-home installations;
- exact acceptance once at the final candidate commit; and
- likely import-topology/dead-surface reviews when imports/legacy routes change,
  although the runway does not cost them explicitly.

That is at least 14 worker/reviewer/test-quality agent passes before corrections.
Every defect loop adds worker correction, focused validation, specialist
rereview where triggered, and independent rereview. The final validation repeats
many earlier gates cumulatively.

The proposed S4A/S4B amendment establishes five as the evidence-backed minimum,
not a target or ceiling. Its minimum delta is one additional worker invocation, one independent
slice review, one focused/scenario-validation cycle, one candidate commit, and,
because both slices change tests, likely one additional delta-only test-quality
pass. The S4A installed public checkpoint also adds the explicit installation
check proposed here. Conditional import/dead-surface reviews and correction loops
prevent a trustworthy hard total. The interface prototype may justify more
scenario-complete slices; each additional slice adds at least one worker,
independent review, focused validation, commit, and usually test-quality cycle.
The amended runway must record the actual count and multipliers rather than
retaining the current four-slice cost assumptions.

### Coordinator context and compaction risk

There is no persisted context baseline. CCFG-25's context use was unavailable,
and the failed foundation did not persist trustworthy token/time totals. Slice 1
and current Slice 4 are high compaction risks because they combine protocol
definition, production code, fixtures, real process/Git behavior, installation,
multiple reviews, and broad caller rewrites. A one-context completion claim is
therefore unsupported. The S4A/S4B split and pre-execution prototype reduce the
uncertainty; they do not make telemetry a prerequisite.

## Lessons From CCFG-25

1. **Installed command owners are large even when conceptually deep.** CCFG-25
   Slice 1 changed 12 files and added 3,887 lines. `scripts/plan_batch.py` alone
   was 1,645 lines and its focused test file 1,146 lines. CCFG-26 must not call
   Slice 1 small merely because the semantic boundary is clean.
2. **Caller removal is wider than owner creation.** CCFG-25 Slice 2 touched 31
   files while removing legacy ownership and rewiring runner/docs/tests. The
   current CCFG-26 Slice 4 has the same multiplier plus reconciliation effects.
3. **Validation commands are part of executability.** CCFG-25 needed two bounded
   validation corrections around BasedPyright scope. CCFG-26 must measure exact
   commands and installed acceptance before implementation rather than treating
   conditional validation prose as sufficient.
4. **Exact installation and acceptance are valuable.** CCFG-25's fresh/isolated
   installation and exact acceptance are the right model. CCFG-26 should apply
   a smaller legacy-free installed-owner gate after Slice 1, not wait until all
   authority transitions are complete.
5. **A clean closeout does not make cost disappear.** CCFG-25 recorded 38 files,
   +5,223/-1,602, cumulative validation, amendments, and reviews. The queued
   CCFG-26 plan currently has no comparable per-slice estimate.

## Lessons From The Rejected CCFG-26 Foundation

The rejected foundation is not a design requirement, but its failure mode is
directly relevant to plan quality:

- ten paths accumulated 4,268 insertions before an acceptable commit boundary;
- four code-producing passes, one design-only pass, four full coordinator gate
  sets, and eight review results produced twelve findings;
- green gates grew from 36 to 43 to 55 to 60 tests while the decisive
  cross-platform effect primitive remained unproved;
- the final invalidating primitive was examined only after production code and
  repeated correction loops; and
- no exact accepted commit existed at the end.

The retrospective at
`batches/ccfg-26-execution-state-foundation/execution-retrospective.md:187-241`
identifies the planning error: outcomes were specified without proving the
primitive that makes them true, and feasibility was deferred into a large
production slice. The analogous risks here are:

- specifying `work-batch/v1` without a concrete installed handshake or
  artifact-only progression primitive; and
- specifying "atomic/idempotent" reconciliation without a two-document order,
  inter-step fault model, or recovery proof.

The lesson is not to restore ADR 0003 or build another state model. It is to
prove these two narrower primitives before authorizing their production slices.

## Questions Answered From Repository Evidence

| Material question | Answer | Disposition |
|---|---|---|
| What is currently queued? | Exactly `batches/ccfg-26-work-batch-owner-transfer/runway.md`; no selected/active batch or successor | `answered_by_repository_evidence` |
| Which revisions were reviewed? | plan-time stable `6b57561`, live stable `27c2ada`, candidate `5c5ec9d`; exact hashes above | `answered_by_repository_evidence` |
| Is COR-009 still the right end state? | Yes: work-batch sole owner through same-batch reconciliation, same-work removal of Batch Runway/APR ownership | `answered_by_repository_evidence` |
| May the candidate control the real CCFG-26 batch? | No; stable controls it under ADR 0004 | `answered_by_repository_evidence` |
| Who owns current execution today? | Batch Runway for execute/recovery/finalize; APR is declared closeout owner; work-batch is a routing wrapper | `answered_by_repository_evidence` |
| Do current green scenarios run installed work-batch? | No; they run fixture adapters/direct mechanisms | `answered_by_repository_evidence` |
| Does an installed `scripts/work_batch.py` exist? | No | `answered_by_repository_evidence` |
| Does candidate work-batch already use the accepted contract-first hybrid format? | No; it has no `## Contract`/`skill-contract/v1` and direct deterministic validation reports `contract.block_count` | `answered_by_repository_evidence` |
| Does CCFG-26 require that hybrid migration and direct validation? | No; neither the runway nor its required-green baseline names it | `answered_by_repository_evidence` |
| Are worker/reviewer results already compact structured YAML? | Yes; both TOMLs require exact YAML-only v2 results and forbid narrative/log output | `answered_by_repository_evidence` |
| Are worker/reviewer input handoffs and the work-batch script transport specified? | No; input handoffs remain prose and no exact JSON request/result contract exists | `answered_by_repository_evidence` |
| Which format fits each boundary? | YAML for LLM contracts/handoffs/results, private JSON for skill-script/subprocess/receipt transport, Markdown+YAML for durable Git-reviewed artifacts | `answered_by_repository_evidence` from accepted format rules and working add-to-ledger/plan-batch patterns |
| Must deterministic workflow work live in production code rather than prose? | Yes; the user has now made this a refactor constraint. The accepted repository design does not yet record it strongly enough | `answered_by_user_direction`; repository recording `requires_bounded_plan_amendment` |
| Must CCFG-26 stay at four or five slices? | No. Use the smallest number of scenario-complete slices that permits a clean, extensible implementation and trustworthy review | `answered_by_user_direction` |
| Does the existing store make CURRENT+LEDGER atomic as one transaction? | No; it supplies two separate atomic/idempotent CAS operations | `answered_by_repository_evidence` |
| Is closeout write replay already demonstrated? | Yes, per artifact through `write_closeout_artifact` | `answered_by_repository_evidence` |
| Is partial reconciliation recovery demonstrated? | No; only partial-state rejection is covered | `answered_by_repository_evidence` |
| Can Slice 3 currently call APR to clear the queue? | Not coherently; APR contract forbids those mutations while work-batch prose assigns them | `answered_by_repository_evidence` |
| Are physical legacy directories required to be deleted in CCFG-26? | No; CCFG-28 owns physical deletion | `deferred_to_named_future_batch` |
| Is runner phase-model removal required now? | No; CCFG-27 owns that decision, but CCFG-26 must rebind semantic execute/closeout routes | `deferred_to_named_future_batch` |
| Is bridge removal required now? | No; CCFG-29 owns it | `deferred_to_named_future_batch` |
| Are telemetry/compaction metrics a prerequisite? | No; record missing cost evidence but do not add telemetry scope | `not_a_real_requirement` |
| Should issues #59/#61 be restored? | No; canonical ledger records them closed/not planned | `not_a_real_requirement` |
| Is a new execution-state model required? | No; it is explicitly forbidden | `not_a_real_requirement` |

## Missing Evidence

### Missing but agent-resolvable

- an exact inventory of normal callers, including direct skills, goal-runner,
  local runner, manifests, docs, agents, and acceptance harnesses;
- the exact closed-world YAML fields for worker and reviewer handoffs, excluding
  static role instructions already owned by their TOMLs;
- exact v1 agent result disposition;
- exact per-slice file manifests and prototype-derived line estimates;
- a prototype-derived internal Python module map and measured interface surface;
- exact test commands and local runtime samples after `tests/test_work_batch.py`
  exists;
- candidate-only installation runtime and link inventory;
- a fake-`codex` production runner prompt tripwire;
- real temporary-Git commit/receipt counterfactuals;
- legacy-free installed work-batch acceptance; and
- exact old-format active-state inventory and its named future removal owner.

### Missing and requiring a bounded plan amendment

- the `work-batch/v1` request/result/error/replay/progress contract;
- one `skill-contract/v1` for work-batch, its accepted before/after ownership
  catalogs, direct validator command, and migration guard;
- a Python-versus-skill-versus-agent responsibility matrix and exact private
  JSON/YAML format ownership for every execution transition;
- the repository-authoritative deterministic-code rule, the small external
  interface, typed action/result/error model, dependency/adapters map, and
  code-architecture acceptance criteria;
- a pre-Slice-1 prototype showing artifact-only pickup/resume with no new state;
- Slice 1 fail-closed output and no-legacy-recovery rule;
- installed-owner bindings for current execution/currentness/closeout scenarios;
- a coherent Slice 3 next-caller contract;
- reconciliation order, visible partial-state matrix, per-document receipt use,
  forbidden CURRENT-first behavior, and forward-only recovery;
- S4A/S4B boundaries and temporary caller classifications;
- direct legacy entrypoint dispositions;
- runner post-execute/closeout change allowance; and
- required-green counterfactuals for every displaced owner.

Missing evidence must not be converted into arbitrary numeric thresholds. The
amendment should measure the actual prototype and exact commands.

## Decisions That Actually Require User Direction

None before the bounded amendment and feasibility proofs.

One qualification is now resolved by explicit user direction rather than by the
old plan: repository DEC 0008 defines "hybrid" as contract-first YAML plus
concise Markdown, but it does not by itself state the stronger rule that every
mechanically decidable behavior belongs in Python. The user has supplied that
additional design constraint for this review. The repository's working patterns
support the resulting format choice: compact YAML at LLM boundaries, private
JSON at machine/subprocess boundaries, and no new durable execution-state JSON.
The amendment must record this allocation explicitly; it must not infer it from
the word "hybrid."

The user has also resolved the quality and slicing policy: deterministic code
must be clean and extensible, not a hurried collection of functions, and the
plan must allow additional slices when that is necessary to establish and review
the module correctly. This removes fixed slice count as a decision. It does not
authorize horizontal scaffolding slices with no callable scenario; each
production slice still needs a coherent authority state and fail-closed handoff.

Repository evidence resolves the current gaps without restoring old issues or
asking the user to choose an architecture. A new user/design decision is needed
only if a focused prototype shows that either artifact-only work-batch
progression or recoverable two-document reconciliation cannot be implemented
with the accepted Planning State/planning-contract mechanisms and would require:

- a new persistent state/store/schema;
- a public protocol beyond COR-009;
- cross-generation runtime communication;
- a new dependency or platform boundary outside the reviewed allowance; or
- moving CCFG-27/28/29 product scope into CCFG-26.

Until such evidence exists, escalating a hypothetical choice would be premature.

## Minimum Bounded Amendment

Preserve CCFG-26/COR-009 purpose, ADR 0004 boundary, accepted candidate baseline,
Planning State authority, existing planning-contract mechanisms, final stable
closeout bookkeeping, and all CCFG-27/28/29 deferrals. Preserve the current
Slice 2 recovery/currentness and Slice 3 finalization/closeout-production
groupings only if the interface prototype proves each remains one coherent,
reviewable extension of the same module.

The dispatch is not slice-neutral: it declares four slices, 1->2->3->4 boundary
reasoning, known-red ownership in Slice 4, and rejection of a fifth production
slice. That fixed-count position is now explicitly superseded by user direction.
The future bounded amendment must update the dispatch and runway together,
choose slice boundaries from complete scenarios and module-extension risk,
obtain new exact hashes/review, and bind the amended artifacts through the normal
canonical queue transaction. This task does not perform those edits.

Before writing the final amended drafts and before requesting exact-draft
review, complete the disposable feasibility proofs and incorporate their exact
evidence, measured commands, and resulting contracts into the dispatch/runway.
They are planning inputs, not work deferred to the first execution invocation.

Amend the dispatch, runway, and exact-draft review as follows:

1. **Record the refactor-wide deterministic-code decision.** Add the accepted
   rule to `docs/design/command-owner-redesign/decisions.md`, explain its
   hybrid-format consequence in `03-contract-first-formats.md`, and have
   `skill-authoring` audit the allocation without becoming a runtime dependency.
   Apply it in the work-batch contract: deterministic derivations live in
   production code; Markdown and agents cannot duplicate them. Author/audit
   `skills/work-batch/SKILL.md` through existing authoring support so it has one
   valid `skill-contract/v1` block and concise procedure/branches. Do not add
   `skill-authoring` as a runtime dependency.
2. **Add an interface-first non-production feasibility gate before Slice 1.**
   Define one small `work-batch/v1` external interface, typed request and
   action/result/error/replay contracts, the thin JSON CLI adapter, cohesive
   internal responsibility map, real dependency/adapters map, collaborator
   packets, receipt paths, and artifact-only progress inputs. Prove it in a
   temporary planning root and real temporary Git repository with no
   `execution-state.json` or new persistent state. Obtain an architecture review
   of interface depth, locality, dependency direction, and extension behavior.
   This gate is planning evidence, not a product slice or new architecture.
3. **Choose slice count from the proven module and scenario seams.** Preserve a
   slice only when it leaves a complete callable authority state and the
   coordinator can implement/review it reliably. Add slices when needed to
   extend the module cleanly; reject both fixed-count compression and horizontal
   model/helper/test slices without a production consumer. Record the closed
   Python/skill/worker/reviewer/mechanism responsibility matrix and exact compact
   YAML/private-JSON ownership in every affected slice.
4. **Make the clean-path slice fail closed.** Name the durable blocked result for
   validation, review, receipt, movement, and interruption failures. Require old
   recovery, finalizer, and reconciler tripwires to remain untouched. Add a
   coordinator-run candidate-only install and installed clean-path test before
   accepting that slice's commit.
5. **Bind recovery to that exact blocked result.** Enumerate runway,
   completed-slices, execution-report, receipt, Planning State, and Git material
   inputs. Add real-Git post-commit receipt recovery and prohibit fixture state
   as production authority.
6. **Separate closeout-production proof from reconciliation.** Add an
   installed-owner closeout-production-only scenario. Either make APR an explicit
   conditioned apply-only temporary caller with a coherent contract, or state
   that the closeout-production slice stops with a complete unreconciled closeout
   and the reconciliation slice is the sole next owner.
7. **Split current Slice 4 into at least two scenario-complete slices.** The
   first transfers public same-batch reconciliation, partial recovery, and
   no-successor behavior with explicit forward-only fault recovery; legacy
   compatibility calls fail closed and it does not claim global installed-caller
   cutover. The next rebinds runner/goal-runner, removes installed owner
   dependencies and normal callers, resolves v1 agent paths, updates exact change
   allowance, docs/manifests/tests, and proves legacy-free installation.
   Split either further if the interface prototype or context estimate shows a
   second independently usable authority state.
8. **Expand the migration matrix to every surface in this report.** Every retained
   route needs caller, reason, future owner, removal batch/condition, and forbidden
   fallback. Every direct legacy entrypoint needs an end-state disposition.
9. **Make counterfactuals required-green.** Poison old clean/recovery/finalizer/
   reconciler routes; inject contradictory APR results; prove partial
   reconciliation roll-forward; prove runner prompt routing through the
   production subprocess seam; run the installed owner without legacy features;
   make direct `skill_contract.py validate`/migration validation required-green;
   reject malformed/extra-field/stale YAML and JSON before side effects; and test
   behavior through the external interface without pinning private helpers.
10. **Add cost evidence.** Give exact per-slice expected files, prototype-derived
   line range or explicit unknown/measurement gate, exact command baselines,
   installation cadence/timing, and expected worker/reviewer/specialist passes.
11. **Obtain a fresh independent exact-draft review and queue binding.** The
   amended dispatch/runway hashes must replace the current clean review's
   bindings, and canonical state must record the amended queued artifacts through
   the normal planning transaction before any execution.

This is the smallest amendment that removes production-time mechanism choice and
silent fallback while preserving the accepted ownership design.

## Required Changes Before Execution

- [ ] Record in the authoritative command-owner redesign that every
  mechanically decidable workflow derivation belongs in production code and
  may not be duplicated as executable prose or agent judgment.
- [ ] Define and review one small external work-batch interface, a thin installed
  JSON adapter, cohesive internal responsibilities, explicit dependency
  direction/adapters, typed results/errors, and the extension path for recovery,
  finalization, and reconciliation.
- [ ] Replace fixed slice-count language with scenario-complete, independently
  usable, fail-closed authority and coordinator-context criteria. Add as many
  slices as those criteria require; do not manufacture horizontal scaffolding
  slices.
- [ ] Require exactly one valid `skill-contract/v1` block in
  `skills/work-batch/SKILL.md`; run direct structural and ownership-migration
  validation against the target document/catalog.
- [ ] Record the closed Python/skill/worker/reviewer/mechanism responsibility
  matrix. Move all uniquely derivable parsing, transition, evidence, validation,
  Git/receipt, replay, closeout, and reconciliation behavior behind the Python
  boundary.
- [ ] Define compact closed-world YAML worker/reviewer handoffs and results, a
  private JSON `work-batch/v1`/result transport, and Python ownership of parsing
  and rejecting malformed, duplicate-key, extra-field, stale, or contradictory
  payloads.
- [ ] Define and prototype the installed `work-batch/v1` handshake and
  artifact-only progression/resume mechanism.
- [ ] Complete those disposable proofs and bind their evidence into the amended
  dispatch/runway before exact-draft review or any execution authorization.
- [ ] Add exact per-slice normal caller and legacy-surface classifications.
- [ ] Add Slice 1 fail-closed evidence and no-recovery-fallback counterfactuals.
- [ ] Add Slice 1 candidate-only installation and installed clean-path proof.
- [ ] Bind Slice 2 recovery to exact existing durable artifacts and real Git.
- [ ] Add a closeout-production-only installed-owner scenario for Slice 3.
- [ ] Resolve the contradictory APR queue-mutation contract at the Slice 3/S4A
  boundary.
- [ ] Specify reconciliation order, inter-step fault points, receipts, state
  matrix, forbidden CURRENT-first handling, and forward-only recovery.
- [ ] Split current Slice 4 into public reconciliation and runner/caller cutover.
- [ ] Classify and update `goal-runner-v1.md`, direct old skill entrypoints,
  agent v1 paths, APR-hosted runner references, and outer-runner successor
  authority.
- [ ] Correct runner change allowance for post-execute checks performed under the
  `closeout` phase.
- [ ] Add installed-owner, legacy-absent, old-owner-poison, contradictory-APR,
  real-Git receipt, partial-reconciliation, and runner-subprocess
  counterfactuals.
- [ ] Replace prose/topology-only acceptance wherever it is currently the only
  proof of a semantic decision path.
- [ ] Record per-slice file/line/command/install/agent cost baselines without
  inventing missing numbers.
- [ ] Re-run deterministic planning validation and obtain a clean independent
  review bound to the amended hashes.
- [ ] Bind the amended dispatch/runway/review through the normal canonical queue
  transaction without starting implementation or selecting a successor.
- [ ] Keep CCFG-26 queued and implementation-not-started until all items above are
  reflected in reviewed planning evidence.

## Explicitly Rejected Expansions

- Do not implement CCFG-26 during this interrogation or during the amendment.
- Do not restore ADR 0003, the rejected execution-state foundation, CCFG-26B,
  issue #59, or issue #61 as requirements.
- Do not add `execution-state.json`, a run database, canonical Batch Execution
  State, a reservation/attempt/flight model, a new planning schema/store, or a
  parallel recovery engine.
- Do not create a second hybrid-skill schema, add `skill-authoring` as a runtime
  work-batch dependency, or turn YAML into a repository-specific workflow DSL.
- Do not treat one large `scripts/work_batch.py`, a directory of shallow
  pass-through helpers, speculative class/port layers, or tests coupled to
  private function topology as evidence of clean extensible code.
- Do not preserve a four- or five-slice count at the cost of module depth,
  reviewability, or a valid intermediate authority state. Conversely, do not
  split by file type or implementation layer when no complete scenario works.
- Do not make the default agent manually translate trusted YAML into JSON or
  reimplement deterministic Python decisions in Markdown. The script must parse
  and validate the exact raw structured result before acceptance.
- Do not require Graphify or graph output for planning, implementation, review,
  validation, or closeout.
- Do not turn deferred telemetry, token totals, compaction metrics, changed-file
  thresholds, or automatic slice heuristics into prerequisites.
- Do not let the candidate generation control or close its real implementation
  batch, mutate stable canonical planning during candidate tests, or communicate
  runtime state across generations.
- Do not physically delete Batch Runway/APR in CCFG-26; CCFG-28 owns deletion
  after rehearsal. Make retained entrypoints non-authoritative and prove it.
- Do not redesign or remove the fixed runner phase model in CCFG-26; CCFG-27 owns
  that decision. Only rebind execute/closeout semantics required by COR-009.
- Do not switch the default generation, prepare CCFG-27, merge the candidate,
  remove the bridge, rebind the default Codex home, or remove the temporary
  dogfooding policy. Those remain CCFG-27 through CCFG-29 work.
- Do not select, dispatch, queue, activate, implement, or close any successor.
- Do not treat the clean planning review, internal terminology, green fixtures,
  or executability after amendment as proof that CCFG-26 is complete. Completion
  still requires implemented behavior, exact validation, independent review,
  installed acceptance, stable same-batch closeout, and no successor.

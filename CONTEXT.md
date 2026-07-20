# Codex Config Runner Context

This context names the local architecture program runner concepts used when
planning or refactoring the repo-owned runner workflow.

## Language

**Runner Facade**:
The user-facing runner surface that launches and reports architecture-program phases while preserving behavior across internal redesigns.
_Avoid_: legacy entrypoint, monolith, compatibility wrapper

**Runner Invocation**:
The act of starting the runner facade with project, ledger, batch bound, execution, sandbox, resume, and environment intent.
_Avoid_: phase contract, prompt, manual phase execution

**Concept Owner**:
The responsible home for one runner concept's rules, language, and tests, independent of the current code shape.
_Avoid_: owner module, component, service

**Phase**:
One fixed runner step in the sequence `select-dispatch -> create-spec -> execute -> closeout`.
_Avoid_: task, batch, arbitrary step

**Phase Transition**:
The runner decision that advances or stops the run after a valid phase result.
_Avoid_: phase validation, phase execution, telemetry writing

**Change Allowance**:
The runner decision that classifies which changed paths are acceptable for the current phase.
_Avoid_: worktree allowance, dirty-file policy, git status rule

**Phase Contract**:
The obligations and allowed outputs for one runner-launched phase process.
_Avoid_: prompt text, output schema, Codex command

**Phase Environment**:
The runner-supplied launch and prompt context for one phase.
_Avoid_: env vars, shell config, prompt-only facts

**Worker Adapter Boundary**:
The runner boundary where provider-specific phase workers return phase results
while validation, receipt checks, transitions, and state updates stay
runner-owned.
_Avoid_: worker seam, test seam, phase executor

**Phase Result**:
The schema-valid JSON object returned by a runner-launched phase process.
_Avoid_: receipt, phase output file

**Phase Receipt**:
The persisted JSON evidence file that must exactly match a phase result at the expected path.
_Avoid_: phase result, telemetry, log

**Phase Observation**:
The runner-recorded facts about launching and monitoring one phase.
_Avoid_: phase receipt, phase result, log dump

**Input Inventory**:
The compact record of broad source reads, large file reads, and subagent reports consumed by one phase.
_Avoid_: phase observation, receipt, transcript

**Run State**:
The resumable record of one architecture-program run's current phase, active batch, artifact paths, stop reason, and completed count.
_Avoid_: batch runtime state, global state, cache

**Run Summary**:
The compact final report of where one runner invocation stopped and which result facts matter.
_Avoid_: run state, telemetry, transcript

**Run Artifact**:
A runner-owned operational file scoped to one architecture-program run.
_Avoid_: batch artifact, source plan, program ledger

**Batch Artifact**:
A file whose identity and lifecycle belong to one selected batch.
_Avoid_: run artifact, global cache, installer artifact

**Program Ledger**:
The durable source of codex-config findings, backlog candidates, selected batch
status, and closeout pointers that workflow commands coordinate around.
_Avoid_: run state, run manifest, source code

**Batch**:
One selected unit of architecture work from the program ledger.
_Avoid_: phase, run, task

**Slice**:
One ordered, independently useful implementation unit in an accepted Batch Runway.
_Avoid_: phase, arbitrary step, task

**Product Boundary**:
The user-visible problem, public inputs and outputs, modules, and persistent state
that remain meaningful after extraction from the current development repository.
_Avoid_: current checkout topology, installer details, dogfood harness

**Dogfood Adapter**:
Temporary repository-specific code or procedure that launches or validates the
product inside codex-config without becoming part of the product API, schema, or
storage model.
_Avoid_: product core, permanent compatibility layer, installation architecture

**Batch-Local Runtime State**:
Small machine-readable state whose identity and lifecycle are exactly one batch
and whose default location is that batch directory's `.runtime/` subdirectory.
_Avoid_: runner-global run state, separate mandatory artifact root, temporary test path

**Threat Model**:
The explicit failures and actors a product version protects against, together
with the environments and hostile behavior it deliberately does not support.
_Avoid_: generic safety, every possible failure, implementation checklist

**Guarantee Feasibility**:
The evidence that a material guarantee has a concrete user value, a known
implementation primitive or bounded dependency, and a credible proof path on
every required platform.
_Avoid_: optimistic portability, choose while implementing, green unit tests alone

**Preserved User Worktree**:
Uncommitted work the user has chosen to retain outside workflow authority. It is
not accepted implementation, planning authority, or permission to continue.
_Avoid_: active slice, implementation baseline, reusable patch

**Dispatch Packet**:
The compact handoff that describes the selected batch for spec creation.
_Avoid_: batch spec, program ledger, receipt

**Plan Archive**:
The historical home at `docs/plans/archive/` for completed or superseded planning documents after their execution value is gone.
_Avoid_: active plan, program ledger, dispatch packet

**Planning Root**:
The user-selected documentation location where active program ledgers, batch
directories, runway specs, and planning reports live.
_Avoid_: source root, mandatory separate artifact root, plan archive

**Generic Workflow Contract**:
The planning reference at `docs/plans/generic-phase-runner-workflow-contract.md`
that maps the current runner to generic **Workflow**, **Phase**, **Worker**,
**Receipt**, **State**, and **Artifact** concepts while keeping
`codex-config` integration language separate.
_Avoid_: product idea, public package API, YAML workflow schema

**External Runner Implementation**:
A future implementation of the generic runner contracts outside
`codex-config`, expected to be an OSS Go project. It should interoperate through
versioned schemas, files, commands, fixtures, and exit codes rather than
importing `codex-config` internals.
_Avoid_: Python port, repo skeleton, copied runner module

**Planning State Diagnostic**:
The read-only `scripts/planning_state.py current` and `validate` command
surface for Planning Artifact Layout v1 roots. It answers what planning state
exists and whether it is structurally valid; it does not execute phases.
_Avoid_: runner core, phase runner, state store

**Skill Ownership Ambiguity**:
Unclear responsibility boundaries between reusable workflow skills, especially
when more than one skill appears able to trigger, select work, write planning
state, create handoffs, or execute a batch.
_Avoid_: messy skills, too much prose, documentation cleanup

**Skill Invocation Audience**:
The intended caller for a reusable workflow skill: a human explicitly selecting
a workflow, an agent applying a support capability during another workflow, or a
workflow orchestrator enforcing a required step.
_Avoid_: who uses this, agent skill, user skill

**Workflow Command Phrase**:
A human-facing instruction such as "put this issue in the ledger", "create a
specs batch", or "work on the batch" that agents route to one or more reusable
workflow skills.
_Avoid_: skill name, trigger word, invocation syntax

**Ledger Intake**:
The workflow action that records a finding, issue, cleanup need, or improvement
candidate in a durable program ledger with enough context for later selection.
_Avoid_: architecture program, batch, task list

**Batch Spec Creation**:
The workflow action that turns one selected ledger item or batch brief into a
concrete slice-by-slice execution spec.
_Avoid_: ledger intake, implementation, program planning

**Batch Planning**:
The human-facing workflow action that selects suitable ledger work when needed
and creates the concrete slice-by-slice execution spec for the next bounded
batch.
_Avoid_: batch selection, batch spec creation, implementation

**Agent-Routed Workflow**:
A reusable workflow skill that the user normally reaches through a workflow
command phrase while the agent selects the concrete skill, mode, and handoff
sequence.
_Avoid_: user skill, hidden skill, automatic skill

**Human-Facing Skill Name**:
A skill name that is suitable for direct human invocation because it names the
job the user thinks they are asking for.
_Avoid_: internal workflow label, implementation nickname, clever name

**User-Bounded Batch**:
A batch of agent work that starts from explicit user intent and remains limited
to the selected ledger item, batch brief, or current batch rather than handing
open-ended backlog ownership to the agent.
_Avoid_: autonomous backlog sweep, all remaining work, agent-owned program

**Skill Runtime Identifier**:
The stable machine-facing identifier used to install, link, or route a reusable
workflow skill. It may be less descriptive than the human-facing skill name.
_Avoid_: public name, user command, workflow purpose

**Preventive Legacy Control**:
Agent behavior that avoids preserving obsolete names, compatibility paths,
fallbacks, or topology through new code or tests unless there is explicit
support evidence.
_Avoid_: legacy cleanup, removal pass, test-preserved compatibility

**Review Support Skill**:
A skill intended for reviewer or workflow-agent invocation as part of normal
quality checks rather than as a primary human command.
_Avoid_: user command, optional cleanup, standalone workflow

**Default Workflow Obligation**:
A rule that implementation and review workflows must enforce during normal
work without requiring the user to invoke a separate skill.
_Avoid_: optional skill, cleanup request, manual reminder

**Workflow Command Set**:
The small set of human-facing skill commands the user is expected to invoke
directly for normal planning and execution work.
_Avoid_: full skill inventory, internal skill list, implementation routing map

**Command Wrapper Skill**:
A thin human-facing installed skill whose name matches a workflow command and
whose job is to route the request to lower-level runtime skills without
duplicating their detailed procedures.
_Avoid_: alias note, duplicate workflow, renamed internals

**Routing Complexity**:
Maintenance cost introduced when a human-facing command has to coordinate too
many lower-level skills, modes, state checks, or handoff rules before doing its
job.
_Avoid_: simple wrapper, hidden architecture, convenient alias

**Command Owner Skill**:
A human-facing skill that owns one workflow command end-to-end instead of only
delegating to historically named lower-level skills.
_Avoid_: command wrapper, alias, facade

**Copy-First Skill Migration**:
A migration approach that creates new command-owner skills beside existing
runtime skills, proves the new workflow surface, and then demotes old
user-facing metadata while keeping required support contracts installed when
current workflows still depend on them.
_Avoid_: in-place rename, permanent compatibility layer, rewrite while active

**Transitional Bridge Skill**:
A human-facing command-owner skill that currently routes to runtime/support
skills while the copy-first migration is still underway.
_Avoid_: final owner, deprecated runtime skill, permanent wrapper

**Agent-Facing Support Skill**:
A reusable skill used behind a command-owner skill to keep agent procedures
focused, shared, and maintainable without expanding the human-facing command
set.
_Avoid_: hidden user command, duplicate command owner, broad workflow facade

## Relationships

- The **Runner Facade** may preserve externally visible behavior while its internal shape changes.
- A **Runner Invocation** starts the **Runner Facade**.
- A **Runner Invocation** ends by reporting a **Run Summary**.
- A **Concept Owner** may be implemented as a module, class, function group, or package.
- A **Phase Contract** belongs to exactly one **Phase**.
- A **Phase Environment** belongs to exactly one launched **Phase**.
- A **Phase Environment** supplies facts and settings used to satisfy a **Phase Contract**.
- A **Worker Adapter Boundary** lets provider-specific phase workers return
  **Phase Result** objects without owning **Phase Result** validation,
  **Phase Receipt** checks, **Phase Transition**, or **Run State** updates.
- A **Phase Result** is returned by exactly one **Phase**.
- A **Phase Receipt** persists exactly one **Phase Result** for one **Phase**.
- A **Phase Observation** records what the runner observed about one **Phase**.
- An **Input Inventory** records what one **Phase** consumed.
- A **Phase Transition** consumes a valid phase result and updates **Run State**.
- A **Change Allowance** protects the run from unrelated project edits while allowing expected runner and phase artifacts.
- A **Phase Contract** is rendered into prompt text but is not the prompt text itself.
- A **Runner Invocation** expresses environment intent that becomes a **Phase Environment** for each launched **Phase**.
- A **Phase Transition** consumes a valid **Phase Result** after its matching **Phase Receipt** is verified.
- A **Run Artifact** belongs to exactly one architecture-program run.
- A **Batch Artifact** belongs to exactly one selected **Batch**.
- The active codex-config **Program Ledger** is
  `docs/plans/programs/codex-config/LEDGER.md`.
- A **Program Ledger** may contain many **Batches**.
- A **Batch** has one accepted ordered set of **Slices**.
- A **Batch-Local Runtime State** belongs to one **Batch** and does not redefine
  selected, queued, or active Planning State currentness.
- **Run State** and **Batch-Local Runtime State** have different identities: one
  runner invocation versus one batch.
- A **Planning Root** determines the ledger and batch directory. It does not
  require a second root for small batch-owned state.
- A **Dogfood Adapter** may depend on modules inside the **Product Boundary**;
  product modules must not depend on the adapter.
- `CODEX_HOME`, symlinks, stable/candidate checkouts, and cross-checkout leases
  are dogfood mechanics unless explicitly accepted as product requirements.
- A **Threat Model** limits what safety claims the product makes; an unsupported
  hostile or deployment scenario is not silently converted into implementation scope.
- **Guarantee Feasibility** is required before a production plan accepts a
  material guarantee whose implementation could invalidate the design.
- A **Preserved User Worktree** remains outside planning and execution authority
  until the user gives explicit direction.
- A **Dispatch Packet** describes exactly one selected **Batch**.
- A **Run State** records the active **Batch** when one has been selected.
- A **Run Summary** reports selected facts from **Run State** and the latest **Phase Receipt**.
- A **Plan Archive** preserves historical planning evidence that should not be treated as active instructions.
- The current repository **Planning Root** is `docs/plans/`.
- The **Plan Archive** is `docs/plans/archive/`.
- The **Generic Workflow Contract** cross-references this glossary for current
  runner terms and does not replace it.
- An **External Runner Implementation** satisfies the **Generic Workflow
  Contract** through interoperable artifacts, not by copying the Python file
  layout.
- A **Planning State Diagnostic** may feed an **External Runner
  Implementation** through an explicit adapter/protocol, but it is not part of
  the runner core.
- **Skill Ownership Ambiguity** is resolved by assigning one primary trigger,
  responsibility boundary, and handoff/output contract to each reusable
  workflow skill.
- A **Skill Invocation Audience** should be explicit when a skill can be both
  directly selected by a human and invoked as support by another workflow.
- A **Workflow Command Phrase** may route through multiple **Agent-Routed
  Workflows** before producing the requested ledger update, batch spec, review,
  or implementation result.
- **Ledger Intake** happens before **Batch Spec Creation** when the work is not
  already selected and bounded.
- **Batch Spec Creation** consumes selected ledger context; it should not be
  described as adding tasks to the ledger.
- **Batch Planning** may combine selection and spec creation for the user while
  preserving separate internal checks when selection is ambiguous.
- A **Human-Facing Skill Name** should be stable enough for the user to invoke
  directly and plain enough that the workflow's job is clear without reading
  its internals.
- A **User-Bounded Batch** prevents routine agent workflows from silently taking
  ownership of unrelated ledger work.
- A **Skill Runtime Identifier** should not be treated as the user-facing name
  when it is opaque or historically named.
- **Preventive Legacy Control** should run before legacy accumulates; cleanup
  workflows handle residue that already exists.
- A **Review Support Skill** can be directly requested by a human, but its
  normal audience is an agent performing implementation or review work.
- **Preventive Legacy Control** is a **Default Workflow Obligation**, not a
  normal human-facing cleanup command.
- The current **Workflow Command Set** is `add-to-ledger`, `plan-batch`,
  `work-batch`, and `port-by-contract`.
- `add-to-ledger`, `plan-batch`, and `work-batch` are **Command Owner Skills**
  rather than documentation-only aliases.
- **Command Owner Skills** should reduce user-facing complexity without
  creating unbounded **Routing Complexity** behind the command.
- The target architecture for `add-to-ledger`, `plan-batch`, and `work-batch`
  is **Command Owner Skills**, not permanent wrappers over opaque runtime
  identifiers.
- **Copy-First Skill Migration** lets the command-owner skills move faster
  without forcing every intermediate edit to preserve the old skill interface.
- A **Transitional Bridge Skill** may route to a runtime workflow skill, but it
  still owns the human-facing intent and stop condition until the final
  architecture changes.
- **Agent-Facing Support Skills** may sit behind **Command Owner Skills** when
  they reduce duplication or isolate review, validation, discovery, or routing
  logic.
- **Agent-Facing Support Skills** should have narrow reusable jobs; they should
  not preserve vague historical workflow names behind clearer command-owner
  skills.

## Example dialogue

> **Dev:** "Can we redesign the code behind the **Runner Facade**?"
> **Domain expert:** "Yes, as long as the **Runner Facade** keeps the runner working for its current users."
> **Dev:** "When I ask to run all batches, is that a **Phase Contract** detail?"
> **Domain expert:** "No — choosing all batches is part of the **Runner Invocation**."
> **Dev:** "Does every **Concept Owner** have to be a separate Python module?"
> **Domain expert:** "No — the important part is that one concept has a clear responsible home."
> **Dev:** "Can we add an ad hoc cleanup **Phase** between `execute` and `closeout`?"
> **Domain expert:** "No — **Phase** means one of the fixed runner steps unless we deliberately change the runner sequence."
> **Dev:** "Does a **Phase Transition** validate the phase result?"
> **Domain expert:** "No — it only advances or stops the run after validation has accepted the result."
> **Dev:** "Is rejecting an unrelated changed source file a Git rule?"
> **Domain expert:** "No — it is a **Change Allowance** decision; Git status is just one way to observe changes."
> **Dev:** "Is the `execute` prompt the **Phase Contract**?"
> **Domain expert:** "No — the **Phase Contract** is the set of obligations the prompt communicates."
> **Dev:** "Are expected receipt paths part of the **Phase Environment** even though they appear in the prompt?"
> **Domain expert:** "Yes — launch context and prompt context both supply facts the phase needs to run correctly."
> **Dev:** "Is `do not launch nested Codex` part of the **Phase Environment**?"
> **Domain expert:** "No — that is a **Phase Contract** obligation, not a supplied fact."
> **Dev:** "Which concept should be clarified first in implementation?"
> **Domain expert:** "Start with **Phase Environment**, because it supplies facts used by later **Phase Contract**, **Phase Transition**, and observation work."
> **Dev:** "Can a valid **Phase Result** still fail the runner?"
> **Domain expert:** "Yes — if the **Phase Receipt** is missing, at the wrong path, or does not match exactly."
> **Dev:** "Is context pressure part of the **Phase Receipt**?"
> **Domain expert:** "No — it is a **Phase Observation** because the runner observed it while launching the phase."
> **Dev:** "Is a list of large files read during `create-spec` a **Phase Observation**?"
> **Domain expert:** "No — that is an **Input Inventory** because it records what the phase consumed."
> **Dev:** "When `--resume` loads `run-state.json`, is that global runner memory?"
> **Domain expert:** "No — it is the **Run State** for one architecture-program run."
> **Dev:** "Should the invoking conversation reconstruct what happened from transcripts?"
> **Domain expert:** "No — it should report the **Run Summary** printed by the runner."
> **Dev:** "Is the first `select-dispatch` receipt a **Batch Artifact**?"
> **Domain expert:** "No — before a batch is selected it is a **Run Artifact**; later batch-local receipts are **Batch Artifacts**."
> **Dev:** "Does the runner own the **Program Ledger**?"
> **Domain expert:** "No — workflow commands coordinate around the **Program Ledger**; runner-owned evidence stays beside the selected batch or run."
> **Dev:** "Should a completed runway plan remain active coordination material?"
> **Domain expert:** "No — after it is completed or superseded it belongs in the **Plan Archive**."
> **Dev:** "Do symlinks and `CODEX_HOME` belong in the extracted product API?"
> **Domain expert:** "No — they belong to the **Dogfood Adapter** unless the user explicitly makes them product requirements."
> **Dev:** "Does local crash safety mean we must defeat another same-user process swapping paths during a system call?"
> **Domain expert:** "No — only when the accepted **Threat Model** explicitly includes that hostile actor."

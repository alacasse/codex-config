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
_Avoid_: runner state, global state, cache

**Run Summary**:
The compact final report of where one runner invocation stopped and which result facts matter.
_Avoid_: run state, telemetry, transcript

**Run Artifact**:
A runner-owned operational file scoped to one architecture-program run.
_Avoid_: batch artifact, source plan, program ledger

**Batch Artifact**:
A runner-owned operational file scoped to one selected batch within a run.
_Avoid_: run artifact, source plan, dispatch packet

**Program Ledger**:
The durable source of architecture findings and batch status that the runner coordinates around.
_Avoid_: run state, run manifest, source code

**Batch**:
One selected unit of architecture work from the program ledger.
_Avoid_: phase, run, task

**Dispatch Packet**:
The compact handoff that describes the selected batch for spec creation.
_Avoid_: batch spec, program ledger, receipt

**Plan Archive**:
The historical home at `docs/plans/archive/` for completed or superseded planning documents after their execution value is gone.
_Avoid_: active plan, program ledger, dispatch packet

**Planning Root**:
The documentation location at `docs/plans/` where active program ledgers, dispatch packets, runway specs, and planning reports live.
_Avoid_: source root, artifact root, plan archive

**Generic Workflow Contract**:
The planning reference at `docs/plans/generic-phase-runner-workflow-contract.md`
that maps the current runner to generic **Workflow**, **Phase**, **Worker**,
**Receipt**, **State**, and **Artifact** concepts while keeping
`codex-config` integration language separate.
_Avoid_: product idea, public package API, YAML workflow schema

## Relationships

- The **Runner Facade** may preserve externally visible behavior while its internal shape changes.
- A **Runner Invocation** starts the **Runner Facade**.
- A **Runner Invocation** ends by reporting a **Run Summary**.
- A **Concept Owner** may be implemented as a module, class, function group, or package.
- A **Phase Contract** belongs to exactly one **Phase**.
- A **Phase Environment** belongs to exactly one launched **Phase**.
- A **Phase Environment** supplies facts and settings used to satisfy a **Phase Contract**.
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
- A **Batch Artifact** belongs to exactly one selected batch within one architecture-program run.
- A **Program Ledger** may contain many **Batches**.
- A **Dispatch Packet** describes exactly one selected **Batch**.
- A **Run State** records the active **Batch** when one has been selected.
- A **Run Summary** reports selected facts from **Run State** and the latest **Phase Receipt**.
- A **Plan Archive** preserves historical planning evidence that should not be treated as active instructions.
- The **Planning Root** is `docs/plans/`.
- The **Plan Archive** is `docs/plans/archive/`.
- The **Generic Workflow Contract** cross-references this glossary for current
  runner terms and does not replace it.

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
> **Domain expert:** "No — it coordinates around the **Program Ledger** and records runner-owned evidence beside it."
> **Dev:** "Should a completed runway plan remain active coordination material?"
> **Domain expert:** "No — after it is completed or superseded it belongs in the **Plan Archive**."
> **Dev:** "Should the runner automatically move completed plans into the **Plan Archive**?"
> **Domain expert:** "No — start with an explicit filesystem convention; runner-managed archival can be considered later."
> **Dev:** "Should active planning live directly under `plans/` forever?"
> **Domain expert:** "No — the **Planning Root** is `docs/plans/`; `plans/` is only a temporary compatibility location for the active extraction-prep spec and dispatch during their batch."
> **Dev:** "Does moving the **Planning Root** need a decision record?"
> **Domain expert:** "Yes — use ADR 0001 for the planning-root and archive decision."

## Flagged ambiguities

- "legacy" does not mean code that must survive in its current form; resolved:
  existing behavior can be preserved while the code is redesigned.
- "owner module" over-specified the implementation shape; resolved: use
  **Concept Owner** for the responsible home of a runner concept.
- "worktree allowance" tied the concept too closely to Git; resolved: use
  **Change Allowance** for allowed changed paths at a runner phase.
- "runner state" made the state file sound like global program memory;
  resolved: use **Run State** for the resumable record of one run.
- **Phase Contract** and **Phase Environment** both reach the phase through the
  prompt today; resolved: contract is normative, environment is supplied facts
  and settings.

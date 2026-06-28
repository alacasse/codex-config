# Phase Runner Extraction Prep Dispatch

## Batch

- Batch ID: `phase-runner-extraction-prep`
- Source Program Ledger:
  `docs/plans/codex-config-architecture-program-runner-findings.md`
- Source decision note: `docs/plans/phase-runner-repo-split-issue-12-plan.md`
- Expected spec:
  `plans/codex-config-phase-runner-extraction-prep-runway.md`

## Included Findings

- APR-22. **Planning Root** and **Plan Archive** are not implemented.
- APR-23. Generic workflow contract is only product prose.
- APR-24. Worker adapter seam is Codex-only in production.
- APR-25. Shell-only workflow regression coverage is missing.

## Deferred Findings

- APR-26. Separate `phase-runner` repository split is premature.
  Reassess only after this prep batch proves both the generic workflow contract
  and at least two worker adapters inside `codex-config`.

## Goal

Prepare `codex-config` for a future `phase-runner` extraction decision without
creating a new repository yet. The batch should make the target planning root
real, document the generic workflow boundary, introduce a minimal internal
worker adapter seam, and prove a shell worker can exercise the same state,
receipt, and transition rules as the current Codex phase worker.

## Owner Seam

The batch crosses two adjacent seams that must stay explicitly connected:

- Planning location seam: active architecture-runner planning lives under
  `docs/plans/`, with completed or superseded material under
  `docs/plans/archive/`. This dispatch and its active runway spec remain under
  `plans/` only as a temporary compatibility exception until the batch closes.
- Phase worker seam: runner phase execution should be expressed through a
  small worker adapter interface, initially with `codex-exec` and `shell`
  adapters, while preserving the current **Runner Facade** behavior.

The generic workflow language should map current runner terms to:
**Workflow**, **Phase**, **Worker**, **Receipt**, **State**, and **Artifact**.

## Validation Class

Use `project-harness-production` for the full batch because worker adapter work
touches runner execution behavior. Documentation-only slices may use
`docs-only` overrides, but final validation must include focused runner tests,
dry-run smoke, ruff, and `git diff --check`.

## Guardrails

- Do not create the separate `phase-runner` repository in this batch.
- Do not change the current architecture-program CLI arguments, default phase
  sequence, phase-result schema, receipt equality checks, or final Run Summary.
- Do not make Batch Runway, GitHub issue text, Graphify validation, or personal
  workflow state part of the generic core.
- Do not move the active executing runway spec mid-execution unless the runner
  state and closeout path handling are explicitly preserved.
- Keep historical planning artifacts accessible after archive migration; avoid
  large transcript/log dumps in GitHub or future issue bodies.
- Update `CHANGELOG.md` for meaningful workflow behavior changes, especially
  the worker adapter seam.

## Suggested Slice Shape

1. Record the **Planning Root** ADR and migrate active planning references to
   `docs/plans/`, creating `docs/plans/archive/` for completed or superseded
   material.
2. Add a generic workflow contract document mapping current runner concepts to
   generic phase-runner language and naming what remains in `codex-config`.
3. Introduce the minimal worker adapter seam and route current Codex execution
   through a `codex-exec` adapter without behavior changes.
4. Add a shell worker adapter plus tests proving a shell-only phase can return a
   receipt through the same state, validation, receipt, and transition rules.
5. Reassess issue #12 in local planning docs and update the Program Ledger with
   compact evidence and the remaining repo-split decision.

## Stop Conditions

- Stop if the planning-root migration would require moving runtime state,
  sessions, cache files, logs, or ignored local artifacts.
- Stop if the worker seam requires changing the phase-result schema or public
  CLI behavior.
- Stop if shell-worker tests require live Codex, network, or GitHub access.
- Stop if `docs/plans/` path updates become broad enough that old historical
  reports would need semantic rewriting rather than mechanical archival.

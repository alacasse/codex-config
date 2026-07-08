---
name: plan-batch
description: Select bounded ledger work when needed and write one concrete batch runway spec without executing it.
---

# Plan Batch

Use this skill when the user asks to create the next specs batch, plan a batch,
turn selected ledger work into a runway, or prepare implementation slices.

This skill owns the planning decision for one batch: inspect current planning
state, use the selected dispatch when one exists, select bounded ledger work
only when none is already selected, and write one concrete runway spec with
clear scope, validation, allowed files, and slice boundaries.

This skill owns the user's request to plan one bounded batch. Use
`../planning-state/SKILL.md` first for current state,
`../architecture-program-runway/SKILL.md` only for program selection and
dispatch ownership, and `../batch-runway/SKILL.md` only in `create-spec` mode
for the concrete spec procedure. Stop before implementation. When routing
ambiguity exists, follow `../../docs/skill-routing-contract.md`.

Before consuming Layout v1 planning state, use `../planning-state/SKILL.md` to
run the current and validate hot path. Use `../planning-artifacts/SKILL.md`
when choosing planning locations or interpreting Layout v1 artifacts.

## Stops

- Do not implement any slice.
- Do not create more than one batch spec.
- Do not bypass an existing selected dispatch, queued batch, or active runway.
- Do not run project-level integration harnesses unless the spec explicitly
  assigns them.

## Agent-Facing Support

Use `../architecture-program-runway/SKILL.md` for selected-dispatch mechanics
when ledger work still needs grouping or queue-state updates. Use
`../batch-runway/SKILL.md` in create-spec mode only as runtime support for
writing exactly one concrete runway behind this command.

---
name: add-to-ledger
description: Add new findings, review notes, or work requests to the appropriate project planning ledger without selecting or executing a batch.
---

# Add To Ledger

Use this skill when the user asks to add a finding, review result, bug, cleanup
need, or proposed work item to a project planning ledger.

This skill owns intake quality: identify the target planning root, preserve the
source evidence, write or update the ledger row, assign the initial status, and
leave enough context for a later batch-planning pass.

Before consuming Layout v1 planning state, use `../planning-state/SKILL.md` to
run the current and validate hot path. Use `../planning-artifacts/SKILL.md`
when placement, program ledgers, selected dispatch packets, or archive
locations matter.

## Stops

- Do not select the next batch.
- Do not create a concrete runway spec.
- Do not execute implementation slices.
- Do not close findings without closeout evidence.

## Agent-Facing Support

Use `../architecture-program-runway/SKILL.md` only for program-ledger intake and
grouping mechanics behind this command. Use `../legacy-removal/SKILL.md` first
only when evidence-backed legacy-removal scoping is needed before ledger
intake.

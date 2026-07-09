---
name: add-to-ledger
description: Add new findings, review notes, or work requests to the appropriate project planning ledger without selecting or executing a batch.
---

# Add To Ledger

Use this skill when the user asks to add a finding, review result, bug, cleanup
need, or proposed work item to a project planning ledger.

This is the normal entrypoint for fresh user-provided work/finding text. It
turns that input into durable ledger state so later planning can select bounded
work from the ledger instead of inventing scope from chat.

This skill is the explicit ingestion boundary for fresh or candidate work. It
may ingest user-provided text, GitHub issues, external tickets, ADR follow-ups,
specs, review notes, chat transcripts, or outputs from external engineering
skills when the user explicitly names or provides that source.

It records selected work into the canonical program ledger without selecting,
planning, or executing a batch.

This skill owns the caller-visible intake contract: preserve source identity,
record enough evidence for later planning, and leave the finding in ledger state
without selecting downstream work.

This skill owns ledger-intake user intent. It may route to support/runtime
skills for diagnostics, placement, grouping, or evidence scoping, but it does
not select a batch, create a dispatch/runway, or execute implementation. When
routing ambiguity exists, follow `../../docs/skill-routing-contract.md`.

Use `../planning-state/SKILL.md` for the current/validate diagnostic before
consuming Layout v1 planning state. Use `../planning-artifacts/SKILL.md` for
layout vocabulary and locations; use `../architecture-program-runway/SKILL.md`
for program-ledger intake mechanics.

## Stops

- Do not select the next batch.
- Do not create a dispatch or concrete runway spec.
- Do not execute implementation slices.
- Do not close findings without closeout evidence.

## Agent-Facing Support

Use `../architecture-program-runway/SKILL.md` only behind this command for
program-ledger intake and grouping mechanics. Use `../legacy-removal/SKILL.md`
first only when evidence-backed legacy-removal scoping is needed before intake.

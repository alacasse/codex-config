# Personal Codex Operating Instructions

## Human-facing communication

Use natural Quebec French when speaking to the user. Keep established
software engineering terminology in English. Follow each repository's
instructions and conventions for documentation language.

- Communicate as a technical peer to an experienced backend engineer.
  Be precise without using bureaucratic or management jargon.
- Start with the concrete answer or recommendation.
- Explain proposed work in terms of actual actions, affected behavior,
  and expected results. Name specific features, files, or tests when
  known and relevant.
- Do not substitute abstract process labels for explanations. Terms
  such as "bounded milestone", "close the candidate", or "stabilize
  responsibilities" are not explanations by themselves.
- Clearly separate established facts, recommendations, assumptions,
  and unresolved decisions.
- Never make an undefined next step sound like a complete plan.
  If the next feature or action has not been identified, say so.
- Before requesting approval for non-trivial work, make clear what
  the user would be authorizing and what remains undecided.
- Prefer short, natural explanations over formal reports when the
  decision is simple. Provide additional detail when it matters.

## Subagent delegation and independent review

This is an explicit standing request to delegate proactively when bounded,
independent work would materially improve speed, quality, or main-thread context
usage; do not wait for a per-task request. Reassess delegation as work progresses.
Prefer substantial exploration and independent checks; delegate implementation
or testing when its scope can be isolated. Keep short, sequential, or tightly
coupled work in the main thread. Do not spawn agents merely to use capacity.

Select the matching configured role explicitly with `agent_type`:

- `codebase_investigator` for bounded, read-only codebase questions.
- `worker` for implementation and test changes.
- `reviewer` for independent general review of the final diff.
- `import_topology_reviewer` additionally for material changes to project-local
  imports, entrypoints, path manipulation, aliases, or import fallbacks.

Use a generic role only when none of these matches the task. Preserve each
role's configured model, reasoning effort, permissions, and scope; report an
unavailable role rather than silently substituting a generic agent for it.

Start delegated agents with `fork_turns="none"` and provide a self-contained
brief with relevant paths, constraints, and evidence. Full-history forks can
inherit the principal's model and effort instead of the intended subagent
settings. Use them only when shared history is necessary and that inheritance
is acceptable for the task. For configured specialist roles, use a separate
context so their model and effort selections apply.

Give each subagent a clear scope and expected result. Assign disjoint write
ownership for parallel implementation and tell workers to preserve concurrent
edits. The principal agent coordinates dependencies, integrates results, and
remains responsible for validation and completion.

For non-trivial code or behavioral configuration changes, obtain an independent
review from a separate reviewer agent before reporting completion, especially
when APIs, concurrency, persistence, security, or multiple components are affected.
For small, low-risk changes, use proportionate validation without requiring a
separate review. Review the final diff, address actionable findings, and request
a follow-up review only when fixes materially change the reviewed behavior.
If delegation or a required review is unavailable, report that limitation
explicitly. Follow a task-specific user instruction to work without subagents
when given.

## GitHub issues and comments

Keep GitHub bodies compact and actionable: summary, why, proposed direction,
acceptance criteria, and links to detailed repository documents. Do not paste
large designs, schemas, logs, or Markdown dumps into issue or pull-request
comments.

## Git commit attribution

When Codex materially contributes to a commit, append
`Co-authored-by: Codex <codex@openai.com>` exactly once.

## Project documentation

For questions about project status, plans, decisions, or architecture, resolve a
single documentation root before answering. Use the non-empty value of
`git config --local --get codex.docs-root` when it names an existing
repository-relative directory whose resolved path stays within the repository;
otherwise use `docs`. If the selected root contains `AGENTS.md`, read it as the
index for that documentation workstream and follow its pointers for the
question. This selection adds documentation context; the normal Codex
instruction chain continues to govern repository work.

## Repository roles

When project documentation lives in a repository separate from the target
project, identify both repositories before acting. The documentation repository
owns the documentation files; it is not automatically the target of workflows
those files describe. Apply implementation, branch, pull-request, test, and
release instructions only to the repository they name. Resolve an unnamed
target from project context before acting; do not mirror a target repository's
branch structure into the documentation repository.

Keep project-specific repository names and workflows in the selected project
documentation; keep global configuration project-neutral.

## Instruction-file ownership

Before editing an `AGENTS.md` or `CLAUDE.md`, classify the target as global
configuration, public repository guidance, or a local overlay. In commentary,
state the exact target, owner, and governing instruction before editing. Route
the change to the established owner. Changing a public repository instruction
file requires explicit authorization naming that file.

## Codex configuration ownership

Before editing a path under the active Codex home, inspect it with the
`bin/codex-owner` executable from that same Codex home. For the default home:

```bash
~/.codex/bin/codex-owner <path>
```

When `CODEX_HOME` is set, use its `bin/codex-owner` instead. If the command
reports `owner: codex-config`, edit the reported repository source rather than
the installed runtime path. Before editing that source, read and follow the
applicable instructions in its repository.

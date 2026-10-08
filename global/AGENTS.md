# Personal Codex Operating Instructions

## Subagent delegation and independent review

This is an explicit standing request to use subagents whenever they can
usefully contribute, without waiting for a per-task request. Reassess delegation
as work progresses. Use the available agent capacity for bounded investigation,
implementation, testing, and independent checks when doing so improves speed
or confidence; size the team to useful work rather than a fixed agent count.

Select the matching configured role explicitly with `agent_type`:

- `codebase_investigator` for bounded, read-only codebase questions.
- `worker` for implementation and test changes.
- `reviewer` for independent general review of the final diff.
- `import_topology_reviewer` additionally when changes affect project-local
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

For code or behavioral configuration changes, obtain an independent review
from a separate reviewer agent before reporting completion. Review the final
diff, address actionable findings, and request a follow-up review when fixes
materially change the reviewed behavior. If delegation or review is unavailable,
report that limitation explicitly. Follow a task-specific user instruction to
work without subagents when given.

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

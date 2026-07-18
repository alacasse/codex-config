## GitHub issues and comments

When creating or updating GitHub issues, PR comments, or issue comments, keep the GitHub body compact and actionable. Use GitHub for the decision-oriented core: summary, why, proposed direction, acceptance criteria, and links or paths to detailed design artifacts.

Do not put long design documents, large schema sketches, long logs, or giant Markdown dumps directly into GitHub issue/comment bodies. If the design is substantial, create or update a repo-owned planning/reference document and link or name that file from the issue instead. Prefer short follow-up comments for addenda.

## Subagent delegation

Main agents and workflow orchestrators are allowed to use any configured
subagents without asking for explicit per-task permission when delegation would
improve implementation, review, exploration, or context management. Use the
registered role that matches the work, keep prompts scoped, and close completed
subagents when the workflow requires it.

This includes the default/principal agent in a normal Codex session. Treat this
as the user's standing preference that the default agent may orchestrate
subagents as needed, without requiring the user to restate "use subagents" for
each task, unless a higher-priority runtime tool policy explicitly requires
fresh user permission.

This standing permission does not override narrower spawned-agent role
boundaries. If a worker, reviewer, or explorer role says not to spawn or
delegate to additional subagents, that role-specific instruction still applies
inside that spawned agent.

## Reusable workflow ownership

Repo-owned skills are reusable workflow code. Do not hard-code a single project's name, paths, validation commands, cache locations, issue policy, or local planning layout into a generic skill. If a workflow needs project-specific behavior, put those values in that project's instructions, local overlay, active spec, or a repo-owned reference document, then make the skill resolve them or stop when they are missing.

Repository exploration must remain tool-neutral. Do not require Graphify or any
specific knowledge-graph, indexing, or codebase-query product in reusable
skills, command-owner contracts, candidate refactors, acceptance criteria, or
required artifacts. Core workflows must work with normal repository reads and
search plus configured generic support agents. Optional exploration tools may be
used only when explicitly enabled by user or project instructions, and their
commands, paths, schemas, hooks, caches, and generated outputs must not become
semantic authority, required workflow state, or a portability assumption.

## Temporary Graphify suspension

Until the user explicitly lifts this suspension after the command-owner
refactor is complete, do not invoke Graphify, build, update, or query a Graphify
graph, install or refresh Graphify hooks, or use `graphify-out` outputs while
planning, reviewing, implementing, validating, or closing work in
`codex-config`. Historical Graphify references may be read as evidence, but they
are not required inputs and must not be treated as authority.

Use Planning State diagnostics, targeted repository reads and searches, and the
existing `codebase_investigator` when bounded read-only support is needed.

## Command-owner redesign checkout topology

For CCFG-18 through CCFG-29 and any review, planning, implementation, or
investigation of the command-owner redesign, resolve the stable and candidate
identities before drawing conclusions about current behavior or remaining work.
The current expected topology is:

- canonical planning and stable controller checkout:
  `/home/alacasse/projects/codex-config`, branch `master`;
- candidate implementation checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`;
- stable Codex home: `/home/alacasse/.codex`;
- candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`.

Treat the CCFG-18 candidate-generation receipts and the latest strict
cross-checkout context as the authoritative source for the exact roots, branches,
and revisions. Verify them rather than relying only on the expected paths above.
Stop when the documented and observed identities are missing, ambiguous, or
contradictory.

Apply these source rules:

1. Read canonical `CURRENT.md`, `LEDGER.md`, dispatches, runways, amendments, and
   other live planning state from the stable checkout.
2. Inspect code already produced by the redesign in the candidate checkout and
   candidate branch. Never use default-branch source alone to conclude that a
   target capability is absent or unimplemented.
3. For ownership-transfer work, inspect both generations: the stable source for
   the current controller and compatibility boundary, and the candidate source
   for the target owner and accumulated implementation.
4. Resolve and report the exact stable and candidate revisions used for the
   analysis before recommending architecture, replanning, implementation, or
   deletion.
5. Do not infer candidate behavior from stable planning prose when the candidate
   code can be inspected directly. Do not infer canonical planning state from
   candidate-local copies.

## Temporary stable-runway dogfooding policy

Before planning or executing CCFG-26 through CCFG-29, read and apply the
[temporary stable-runway dogfooding policy](docs/plans/programs/codex-config/notes/stable-runway-dogfooding-policy.md).
This repository-local hook is temporary and CCFG-29 removes it only after the
integrated candidate proves the policy's required behavior.

## Codex config ownership

When editing a path under `~/.codex`, first check whether it is linked from `/home/alacasse/src/codex-config`:

```bash
/home/alacasse/src/codex-config/scripts/codex_owner.py <path>
```

If the script reports `owner: codex-config`, treat the edit as work in `/home/alacasse/src/codex-config` even when the current task is happening in another project. Read `/home/alacasse/src/codex-config/.codex/AGENTS.md`, make the change through the linked file or the repo file, update `/home/alacasse/src/codex-config/CHANGELOG.md` for meaningful workflow or behavior changes, and report that repo's git status before finishing.

Vendor-owned or unmanaged `~/.codex` paths should not be copied into `/home/alacasse/src/codex-config` unless explicitly asked.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues for `alacasse/codex-config`; external PRs are not a triage request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default five-label triage vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo: read root `CONTEXT.md` and relevant ADRs under `docs/adr/`. See `docs/agents/domain.md`.
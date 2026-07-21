# CCFG-35 Candidate-Targeted Plan Supersession

## Status

`ccfg-35-planning-independent-review-hardening` was superseded on 2026-07-20
before any implementation began. The user explicitly rejected its candidate-
targeted implementation authority, restored CCFG-35 to `Open`, amended the
source finding with master-only implementation authority, and requested a fresh
plan from the planner surfaces actually used on master.

## Superseded Artifact Identities

The original artifacts remain unchanged as historical planning evidence:

| Artifact | SHA-256 |
|---|---|
| `dispatch.md` | `74591c5ba3f9b8703adbf25c66f7b8fb5c613d77306f55fac10f13643de3267e` |
| `runway.md` | `bdb2350c2dc8494b1403792d70bbec546a1c4fef90d3898906c63c8c93b47094` |
| `review.md` | `1ebf7c8f01ce3b4d9e71d7da5c4ff1149d740f89bcdbc9e2808290bb64c4ea42` |

Do not execute, resume, refresh, amend, or close this batch. Do not infer queue,
selection, active execution, implementation authority, current architecture, or
successor authority from any artifact in this directory. Its clean review is
bound only to the superseded candidate-targeted drafts and cannot authorize
their consumption.

## Exact Supersession Basis

- Canonical master checkout at supersession:
  `/home/alacasse/projects/codex-config`, branch `master`, commit
  `a701a5a9d8810e67ad193f2955eea24a4886007b`.
- Candidate evidence-only checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`, commit
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`.
- Implementation started: `false`.

## Reason

The superseded runway prescribed implementation against candidate-only planner
roles, scripts, schemas, tests, and candidate-home installation. Those are not
the planner used by the stable master session. On master, the installed public
planner is the repo-owned `skills/plan-batch` skill, which routes to the master
Architecture Program Runway and Batch Runway create-spec surfaces. A clean
review of candidate-only changes therefore could not prove that CCFG-35 changed
the planner used on master.

## Replacement Direction

The amended source authority is
`../../findings/planning-and-independent-review-hardening.md`. A separately
named replacement batch may be queued only after it:

- uses the canonical master checkout as its sole implementation target;
- excludes candidate-only planner machinery;
- receives a fresh independent exact-draft review; and
- requires accepted closeout evidence that independently proves the installed
  master planner changed.

# Codex Config Architecture Program Telemetry Recommendations

## Scope

This reviews the telemetry available from the catalog-boundary architecture-program run and recommends what the codex-config local runner should capture next, especially for context-size reduction.

This file was copied from a Graphify-local observation into `codex-config` and
generalized into a reusable runner plan. Paths below use `<ledger-dir>` for the
parent directory of `--program-ledger`; the runner must not assume a
project-specific planning root.

## Implementation Status

Implemented first pass in `codex-config`:

- structured runs write `telemetry/phases/*.telemetry.json` after launched
  phases;
- structured runs write `telemetry/run-telemetry.json` as an aggregate index;
- run manifests and final summaries link telemetry paths;
- phase telemetry records direct runner measurements: start/end timestamps,
  elapsed seconds, sandbox, model, observable exit code, prompt bytes,
  stdout/stderr byte counts, artifact sizes, and context budget status;
- phase telemetry parses `token_count` events into compact summaries when an
  exact session JSONL path is available;
- missing or unattributed token data is recorded as `status=missing` rather
  than reconstructed from broad session searches;
- phase prompts name an expected input-inventory path and ask agents to record
  broad reads, large file reads, and subagent report inputs there.

Still open:

- reliable discovery of the exact Codex session JSONL path for each
  runner-launched phase;
- worker/reviewer session attribution from execute-phase subagents;
- enforcement of input-inventory existence and schema;
- promotion of repeated hard context warnings into stop conditions.

Related local files:

- State: `<ledger-dir>/architecture-program-run-state.json`
- Dispatch: `<ledger-dir>/dispatch/catalog-boundary-reassessment-dispatch.md`
- Spec: `<ledger-dir>/install-sandbox-catalog-boundary-runway.md`
- Receipts: `<ledger-dir>/receipts/architecture-program-*.json`
- Layout plan: `<ledger-dir>/codex-config-architecture-program-artifact-layout-plan.md`

## What Current Telemetry Can Tell Us

The current runner receipts are enough for outcome-level diagnosis:

- `select-dispatch` completed and produced the dispatch packet.
- `create-spec` completed and produced the concrete Batch Runway spec.
- `execute` completed with commit range `7b845fa5^..c20e8c9d`.
- `execute` captured compact validation and review summaries.
- `closeout` failed with a precise stop reason: nested `codex exec` hit a read-only default Codex state DB, and the temporary `CODEX_HOME` retry hit restricted network sampling.

The current receipts also preserve useful file links:

- `program_ledger`
- `batch_id`
- `dispatch_path`
- `spec_path`
- `receipt_path`
- `evidence_paths`

That was enough to spot the closeout bug and write a good codex-config issue.

## What Current Telemetry Cannot Tell Us

The current runner artifacts are not enough to tune context use.

Missing fields:

- phase session id;
- phase session JSONL path;
- phase start/end timestamps;
- phase elapsed time;
- phase model;
- phase sandbox;
- runner prompt byte/token size;
- max input context for each phase;
- token-count samples per LLM turn inside each phase;
- context window size and percent used;
- cached input tokens versus uncached input tokens;
- output and reasoning tokens;
- worker/reviewer session ids spawned by the execute phase;
- broad file reads or search outputs that inflated live context;
- whether a phase read the whole ledger/spec versus a compact dispatch/receipt bundle.

`<ledger-dir>/architecture-program-run-state.json` has `last_codex_session: null`, so the runner does not currently link a phase result to the Codex session where token telemetry lives.

## Artifact Size Snapshot

Current local artifact sizes:

| Artifact | Lines | Bytes | Notes |
| --- | ---: | ---: | --- |
| `architecture-program-run-state.json` | 18 | 1,010 | compact state, but top-level and not run-scoped |
| `dispatch/catalog-boundary-reassessment-dispatch.md` | 36 | 2,160 | good compact selected-batch input |
| `install-sandbox-catalog-boundary-runway.md` | 506 | 24,812 | reasonable spec size, but can still be expensive if reread repeatedly |
| `receipts/select-dispatch` | 1 | 565 | compact |
| `receipts/create-spec` | 1 | 750 | compact |
| `receipts/execute` | 1 | 1,115 | compact |
| `receipts/closeout failed` | 1 | 1,205 | compact |

The visible artifact files are not the context problem. The risk is repeated broad reads and copied session context inside phase agents, workers, and reviewers.

## Session-Level Token Evidence Found

Codex session JSONL files under `<codex-home>/sessions/2026/06/26/` do include `event_msg` records with:

- `payload.type = token_count`
- `last_token_usage.input_tokens`
- `last_token_usage.cached_input_tokens`
- `last_token_usage.output_tokens`
- `last_token_usage.reasoning_output_tokens`
- `total_token_usage`
- `model_context_window`

That means exact context-size telemetry exists, but not in the runner artifacts.

Candidate phase sessions found by scanning for runner phase prompts:

| Candidate Phase | Session ID | Max Last Input Tokens | Final Last Input Tokens | Final Total Tokens | Context Window | Caveat |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `select-dispatch` | `019f0624-f55f-79f1-9c7f-5f3145142e56` | 43,838 | 43,838 | 351,275 | 258,400 | likely one select attempt |
| `create-spec` | `019f0626-99ce-76d3-8c52-d30c65c0f228` | 55,428 | 55,428 | 359,423 | 258,400 | likely create-spec phase |
| `execute` | `019f0628-8227-7db1-bb8d-df06b6119ef2` | 71,865 | 71,865 | 1,063,691 | 258,400 | early execute session |
| `execute` | `019f0679-3875-7601-a4f8-a2a22303f3c4` | 117,994 | 117,994 | 6,020,628 | 258,400 | likely large execute/retry or long coordinator session |
| `closeout` | `019f069b-f66c-7072-8662-24a780d040d0` | 61,995 | 61,995 | 983,325 | 258,400 | failed closeout phase |

Important caveat: this is reconstructed after the fact. Later sessions can contain copied earlier phase prompts, so text search over session logs overmatches. The runner needs to record exact session identity when it launches each `codex exec` phase.

One related session reached a much higher max last input token count:

```text
session: 019f0665-d5b6-7a91-9fa8-be01f5c6065b
cwd: <project-path>
max last input tokens: 231,800
context window: 258,400
```

I would treat this as a red flag, not as a confirmed phase measurement. Without runner-owned session attribution, it is not safe to say which phase or worker caused it.

## Issues The Current Telemetry Reveals

### 1. Phase Outcome Is Good; Phase Resource Use Is Missing

The receipts answer "what happened" but not "how expensive was it." For tuning, every phase needs a compact resource summary.

### 2. Session Attribution Is The First Missing Link

The runner launches fresh `codex exec` processes, but it does not record the session id or session log path. Since token telemetry is written by Codex outside the receipt, the runner needs to harvest and attach it.

### 3. Closeout Does Not Need A Large Context

Closeout had roughly 62k input tokens in the candidate session. That is not near the 258k window, but it is high for a phase that should only read compact execute receipt evidence, the program ledger closeout section, and maybe the dispatch/spec pointers.

After the closeout nested-Codex bug is fixed, closeout should become one of the smallest phases.

### 4. Execute Is The Context Hot Path

Candidate execute sessions ranged from roughly 52k to 118k input tokens, with one related session at 231k. This matches prior Batch Runway context audits: the coordinator's broad reads and repeated source/test context are usually more expensive than compact worker/reviewer returns.

### 5. Current Receipts Do Not Distinguish Main Phase From Worker/Reviewer Work

The execute receipt says review passed and validation passed, but it does not name worker/reviewer sessions or summarize their context cost. That makes it hard to decide whether context growth came from the execute coordinator, the coding worker, the reviewer, or copied prompts.

## Telemetry Recommendations

### Recommendation 1: Add Phase Session Telemetry

For each runner-launched phase, write a `phase-telemetry.json` artifact near the receipt.

Suggested shape:

```json
{
  "schema_version": 1,
  "run_id": "run-...",
  "batch_id": "catalog-boundary-reassessment",
  "phase": "execute",
  "codex_session_id": "019f0679-3875-7601-a4f8-a2a22303f3c4",
  "codex_session_path": "<codex-home>/sessions/2026/06/26/rollout-...",
  "started_at": "2026-06-27T00:27:15Z",
  "ended_at": "2026-06-27T01:05:12Z",
  "elapsed_seconds": 2277,
  "model": "gpt-5.5",
  "sandbox": "danger-full-access",
  "exit_code": 0,
  "prompt_bytes": 4100,
  "token_events": "token-events.jsonl",
  "summary": {
    "turn_count": 74,
    "max_input_tokens": 117994,
    "max_context_used_percent": 45.7,
    "final_input_tokens": 117994,
    "total_input_tokens": 5987348,
    "total_tokens": 6020628,
    "cached_input_tokens": 0
  }
}
```

Keep the full per-turn token events in `token-events.jsonl` and put only a summary in the phase receipt or manifest.

### Recommendation 2: Add A Runner Telemetry Index

The structured artifact layout plan should include a top-level telemetry index:

```text
architecture-program-runs/<ledger-stem>/<run-id>/
  telemetry/
    run-telemetry.json
    phases/
      01-select-dispatch.telemetry.json
      02-create-spec.telemetry.json
      03-execute.telemetry.json
      04-closeout.telemetry.json
      03-execute.token-events.jsonl
```

`run-telemetry.json` should aggregate:

- per-phase max input tokens;
- per-phase elapsed time;
- total runner tokens;
- max context percentage seen;
- final stop reason;
- session ids;
- artifact sizes;
- flags such as `context_pressure`, `nested_codex_attempted`, and `unattributed_session_growth`.

### Recommendation 3: Record Context Budgets Per Phase

Give each phase a soft context budget and record whether it stayed under budget.

Suggested initial budgets:

| Phase | Soft Budget | Hard Warning | Rationale |
| --- | ---: | ---: | --- |
| `select-dispatch` | 50k | 80k | should use ledger summaries and dispatch rules |
| `create-spec` | 60k | 90k | should consume dispatch plus minimal ledger context |
| `execute` | 120k | 180k | largest phase; still should delegate broad reads |
| `closeout` | 40k | 70k | should use compact receipts and ledger closeout only |

The runner should not necessarily fail on soft budget overflow at first. It should mark:

```json
"context_budget": {
  "soft_budget_tokens": 120000,
  "hard_warning_tokens": 180000,
  "max_input_tokens": 117994,
  "status": "ok"
}
```

Once enough data exists, promote repeated hard warnings into stop conditions.

### Recommendation 4: Capture Input Source Inventory

Token counts alone tell size, not cause. Require each phase to write a compact `input-inventory.json`:

```json
{
  "phase": "execute",
  "primary_inputs": [
    {"path": "<ledger-dir>/install-sandbox-catalog-boundary-runway.md", "bytes": 24812, "role": "spec"}
  ],
  "broad_reads": [
    {"command": "rg ...", "output_bytes": 18000, "reason": "caller scan"}
  ],
  "large_file_reads": [
    {"path": "tests/install_sandbox/test_install_target_models.py", "bytes": 22000}
  ],
  "subagent_reports": [
    {"role": "runway_worker", "summary_bytes": 1600},
    {"role": "runway_reviewer", "summary_bytes": 900}
  ]
}
```

This should be phase-agent reported, not inferred by the runner. The runner can validate that the file exists and include it in `evidence_paths`.

### Recommendation 5: Link Worker And Reviewer Sessions

For execute phases, record spawned worker/reviewer session ids or report artifact paths.

The goal is to answer:

- Did the execute coordinator stay compact while workers did broad reads?
- Did a worker/reviewer inherit too much coordinator context?
- Which role produced the largest context spike?
- Did the coordinator paste worker output verbatim instead of preserving compact reports?

This belongs in `execute.telemetry.json`:

```json
"subagents": [
  {
    "role": "runway_worker",
    "slice": 3,
    "session_id": "019f...",
    "max_input_tokens": 64000,
    "report_path": "..."
  },
  {
    "role": "runway_reviewer",
    "slice": 3,
    "session_id": "019f...",
    "max_input_tokens": 42000,
    "report_path": "..."
  }
]
```

### Recommendation 6: Keep Receipts Compact; Put Telemetry Beside Them

Do not expand the phase receipt schema into a huge telemetry object. Receipts should remain compact control-plane artifacts.

Better pattern:

- phase receipt: status, next phase, paths, compact summaries;
- phase telemetry: token and session metrics;
- input inventory: what entered live context;
- run manifest: links everything.

### Recommendation 7: Add A Context Regression Test Harness

Add tests in codex-config that do not need real token usage:

- parse a synthetic session JSONL with `token_count` events;
- produce phase telemetry summary;
- mark context budget status correctly;
- tolerate missing token telemetry with `status=missing`;
- preserve old runs with no telemetry;
- ensure final runner summary includes telemetry paths when present.

Then add one manual/live validation step for real runner sessions.

## Context Reduction Recommendations

### Reduce Closeout First

Closeout should read:

- execute receipt;
- run manifest;
- batch manifest;
- compact validation/review summaries;
- program ledger closeout target section.

Closeout should not read the full concrete spec unless a summary is missing, and it should not reload broad findings.

### Stop Copying Phase Prompts Into Child Work

Some session searches match old phase prompts in later sessions. That may be unavoidable in conversation history, but worker/reviewer prompts should avoid embedding the full architecture-runner prompt. Pass only:

- slice goal;
- spec path;
- exact slice section;
- validation profile;
- relevant artifact paths;
- expected compact report schema.

### Prefer Artifact Paths Over Pasted Evidence

The execute phase should return compact evidence paths, not pasted logs. The current execute receipt does this well. Preserve that pattern and extend it to telemetry.

### Add Source-Read Budgets To Prompts

Phase prompts should say:

```text
Prefer reading compact dispatch, receipt, and manifest artifacts first.
If you need a broad source read, record why in input-inventory.json.
Do not paste broad command output into the final response; write compact findings.
```

### Use Automatic Context Pressure Flags

Suggested flags:

- `context_ok`: max input < 50% of context window.
- `context_watch`: max input between 50% and 70%.
- `context_pressure`: max input between 70% and 85%.
- `context_stop_recommended`: max input above 85%.

For the current candidate sessions:

- most phase candidates are under 50%;
- the 117,994-token execute candidate is around 46%;
- the 231,800-token related session is around 90% and should have triggered `context_stop_recommended`.

## Minimum Useful Next Implementation

The smallest useful codex-config change was:

1. Add structured artifact layout from the companion plan. Done.
2. Write `phase-telemetry.json` after each launched phase. Done for direct
   runner measurements; exact session JSONL discovery remains open.
3. Parse `token_count` events into a compact summary. Done when a session JSONL
   path is available.
4. Add telemetry paths to the run manifest and final summary without changing
   the phase-result schema. Done.
5. Add context budgets and warning flags. Done as non-failing telemetry.
6. Record `last_codex_session` in runner state when a session UUID is exactly
   observable from `codex exec` output. Done; otherwise it remains `null`.

This is enough to answer the user's main question on future runs:

```text
At each phase, how large was the live context, and what phase caused growth?
```

## Recommendation For The Current Run

Do not overfit to the reconstructed session mapping. The reliable current conclusion is:

- current receipts are enough for correctness debugging;
- current receipts are not enough for context tuning;
- Codex session logs contain the token telemetry we need, but broad
  reconstruction is not reliable enough for runner artifacts;
- the runner must attach exact session ids and parse token-count events at phase
  boundaries when exact session paths are available;
- execute is the likely context hot path;
- closeout should be much smaller after the nested-Codex bug is fixed;
- any session above 85% of the context window should stop after the current safe checkpoint and resume from disk artifacts.

# CCFG-25 Planning Ownership Transfer Review

## Superseded, files were corrected after review.

## Verdict

Changes required before execution. Planning State is structurally valid and the
candidate baseline is unchanged, but the queued plan contains material contract,
validation, sequencing, and scope-preservation defects.

## Review Basis

- Review target:
  `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/`.
- Fixed point: `31d228d...HEAD`, covering commits `6f1692b`, `ace4817`,
  `d7ced83`, and `16ac681`.
- Standards sources: `AGENTS.md`, `CONTEXT.md`, `skills/plan-batch/SKILL.md`,
  `skills/batch-runway/SKILL.md`, and the applicable Batch Runway create-spec,
  project-values, cross-checkout, execution, agent-result, and validation-profile
  references.
- Spec sources: COR-008 at accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`, the CCFG-25 planning-quality
  amendment, the command-owner planning/execution carry-forward, and the CCFG-21,
  CCFG-23, CCFG-24B, and CCFG-33 closeouts.
- `planning_state.py current` and `validate` passed and identify this runway as the
  only queued batch.
- The candidate checkout is clean and remains exactly at
  `91179e84c7cfed666be224575db7000ca0ea01b3`.
- A current live-lease preflight against the stored snapshot returns `ready`. This
  confirms current execution facts; it does not retroactively provide the
  plan-time helper validation required before queueing.
- `git diff --check 31d228d...HEAD` passed for the reviewed directory.

## Standards

1. **High — hard: the queued runway lacks a validated planning snapshot.**

   `runway.md:129-135` says the strict planning payload was manually assembled
   because the installed helper was not run. `skills/plan-batch/SKILL.md:81-88`,
   `skills/batch-runway/references/create-spec.md:123-129`, and
   `skills/batch-runway/references/execution-contract-v2.md:19-24` require helper
   validation and stopping on missing or mismatched strict context.

2. **High — hard: manifest commands are both `required-green` and expected red.**

   The Slice 1, Slice 2, and final command blocks include the unfiltered
   `tests/test_codex_features_manifest.py` at `runway.md:437-456`, `555-573`, and
   `660-689`. The same sections permit two, one, and one known failures
   respectively. Pytest cannot fail and satisfy `required-green`.
   `skills/batch-runway/references/create-spec.md:277-299` requires one accurate
   status class per command. Separate the unfiltered diagnostic or select only the
   green node IDs.

3. **High — hard: final harness and installation validation is not executable as
   written.**

   `runway.md:603-617` requires a real clean candidate install, exact acceptance,
   output hashes, and stable-home comparison, but `runway.md:657-686` supplies only
   an installer dry run and unnamed CCFG-33, manifest, and legacy/projection
   diagnostics. The `command_owner_scenarios.py accept` command requires three
   explicit output paths, none of which is provided. This violates the concrete
   harness-command, fresh-output, and summary-read requirements in
   `skills/batch-runway/references/project-values.md:23-27,59-60` and the selected
   validation profile.

4. **High — execution contradiction: Slice 1's sole-owner gate depends on Slice 2.**

   Slice 1 deliberately leaves legacy owners physically present
   (`runway.md:371-390`) while requiring `plan-batch` already be the sole normal
   planning and queue route (`runway.md:418-432`). Slice 2 owns the actual APR,
   Batch Runway, runner, manifest, and caller rewiring/removal
   (`runway.md:514-550`). Manifest dependency removal is also assigned to both
   `runway.md:400-405` and `529-531`. The Slice 1 acceptance gate is not
   satisfiable as written.

5. **Medium — hard: per-slice delegation briefs and review bases are missing.**

   The runway names review roles at `runway.md:458-459`, `575-576`, and
   `691-692`, but no slice includes the required role-scoped worker/reviewer brief
   or reviewer `diff_basis`. This breaches
   `skills/batch-runway/references/create-spec.md:301-322`.

6. **Medium — hard plus judgement call: the dispatch duplicates the runway.**

   `dispatch.md:68-248` contains proportionality, full inclusion/deferment,
   three-slice shape, approval, validation, closeout, and stop contracts. This is
   effectively a second batch spec, contrary to `CONTEXT.md:87-89`, which defines
   a dispatch packet as a compact handoff and says to avoid a batch spec. Possible
   **Duplicated Code**: the same planning logic appears in dispatch and runway and
   has already drifted on the exact Batch Runway responsibilities retained for
   CCFG-26.

## Spec

1. **High — behavioral acceptance incorrectly tests vocabulary rather than
   topology.**

   The carry-forward requires target scenarios not to depend on old APR, Batch
   Runway, exact prompt prose, stable-only paths, or historical helper topology
   (`findings/command-owner-redesign-planning-execution-carry-forward.md:60-62`).
   `runway.md:648-650` instead requires scenarios to contain none of the forbidden
   legacy terms, contradicting its own structural-testing rule at
   `runway.md:532-536`. Legitimate negative or historical assertions could be
   deleted or rejected solely because of wording.

2. **High — the CCFG-26 preservation inventory is incomplete.**

   The carry-forward reserves proceed, stop, recovery, delegation, validation,
   review, commit, receipt, closeout, and same-batch reconciliation for CCFG-26
   (`findings/command-owner-redesign-planning-execution-carry-forward.md:95-108`).
   The runway's supposedly exact retained-owner inventory omits proceed/stop,
   delegation, receipts, and closeout/reconciliation from the Batch Runway list
   (`runway.md:478-490`, `518-524`, and `651-652`). “Retains only named support”
   could therefore authorize premature removal before CCFG-26.

3. **High — the proportionality verdict does not cover material scope additions.**

   The planning-quality amendment requires every addition beyond the minimum to
   name the failure it prevents and why the minimum cannot solve it more simply
   (`findings/ccfg-25-planning-quality-amendment.md:70-73`).
   `dispatch.md:94-101` justifies only the two TOMLs and deterministic script, while
   the Planning State helper-link ownership transfer and architecture runner
   rewiring appear only later (`runway.md:403-405`, `525-531`). The
   `verdict: proportionate` at `dispatch.md:113` is therefore unsupported for the
   complete planned scope.

4. **Medium — reviewer lineage does not bind the selected dispatch.**

   The planning-quality amendment requires the independent reviewer to receive
   the selected dispatch as well as sources, user constraints, current facts,
   exact draft, and proportionality record
   (`findings/ccfg-25-planning-quality-amendment.md:37-41`).
   `runway.md:216-219` binds `review_basis` to the latter inputs but omits the
   selected-dispatch identity, allowing a clean review to be associated with the
   wrong selection lineage.

Not counted: `dispatch.md:25-27` is selection-time history, not a contradiction
with the now-queued live state.

**Summary: Standards — 6 findings; worst issue is the unvalidated strict planning
snapshot. Spec — 4 findings; worst issue is the incomplete CCFG-26 preservation
boundary.**

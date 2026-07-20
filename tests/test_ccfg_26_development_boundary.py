from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTEXT = REPO_ROOT / "CONTEXT.md"
INSTRUCTIONS = REPO_ROOT / "AGENTS.md"
ADR_0003 = REPO_ROOT / "docs/adr/0003-canonical-batch-execution-state.md"
ADR_0004 = (
    REPO_ROOT / "docs/adr/0004-single-generation-command-owner-development-boundary.md"
)
PROGRAM_ROOT = REPO_ROOT / "docs/plans/programs/codex-config"
CURRENT = PROGRAM_ROOT / "CURRENT.md"
LEDGER = PROGRAM_ROOT / "LEDGER.md"
SLICE_SHAPE_POLICY = PROGRAM_ROOT / "findings/slice-shape-policy-direction.md"
DOGFOOD_POLICY = PROGRAM_ROOT / "notes/stable-runway-dogfooding-policy.md"
ISSUE_62_FINDING = (
    PROGRAM_ROOT / "findings/github-issue-62-stable-runway-dogfooding-bootstrap.md"
)
SUPERSESSION = (
    PROGRAM_ROOT / "batches/ccfg-26-execution-state-foundation/superseded.md"
)


def normalized_text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).strip()


def raw_markdown_section(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        rf"(?ms)^{re.escape(heading)}\n(.*?)(?=^## |\Z)",
        text,
    )
    if match is None:
        raise AssertionError(f"missing {heading!r} in {path}")
    return match.group(1).strip()


def markdown_section(path: Path, heading: str) -> str:
    return re.sub(r"\s+", " ", raw_markdown_section(path, heading)).strip()


def markdown_bullets(path: Path, heading: str) -> tuple[str, ...]:
    bullets: list[str] = []
    current: list[str] = []
    for line in raw_markdown_section(path, heading).splitlines():
        if line.startswith("- "):
            if current:
                bullets.append(re.sub(r"\s+", " ", " ".join(current)))
            current = [line[2:]]
        elif current and line.strip():
            current.append(line.strip())
    if current:
        bullets.append(re.sub(r"\s+", " ", " ".join(current)))
    return tuple(bullets)


def ledger_row(prefix: str) -> str:
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line
    raise AssertionError(f"missing ledger row starting with {prefix!r}")


def core_ccfg26_and_ccfg29_authority() -> tuple[str, ...]:
    return (
        *markdown_bullets(CURRENT, "## Open Ledger"),
        markdown_section(CURRENT, "## Next Safe Action"),
        *markdown_bullets(LEDGER, "## Current Direction"),
        ledger_row("| CCFG-26. Transfer Execution"),
        ledger_row("| CCFG-29. Contract-First Convergence"),
    )


def active_guardrail_authority() -> tuple[str, ...]:
    return (
        *markdown_bullets(CURRENT, "## Stop Conditions"),
        *markdown_bullets(LEDGER, "## Closeout Rules"),
    )


def active_ccfg26_and_ccfg29_authority() -> str:
    return "\n".join(
        (*core_ccfg26_and_ccfg29_authority(), *active_guardrail_authority())
    ).lower()


class Ccfg26DevelopmentBoundaryTests(unittest.TestCase):
    def test_current_state_has_an_empty_queue_and_planning_only_next_action(
        self,
    ) -> None:
        current = CURRENT.read_text(encoding="utf-8")

        for field in (
            "- Selected dispatch path: `None`",
            "- Active Batch Runway spec path: `None`",
            "- Queued batch path or ID: `None`",
        ):
            with self.subTest(field=field):
                self.assertIn(field, current)

        next_action = markdown_section(CURRENT, "## Next Safe Action")
        for fragment in (
            "`plan-batch CCFG-26`",
            "COR-009",
            "ADR 0004",
            "current candidate implementation seam",
            "planning-only",
            "do not implement candidate code",
            "independently reviewed and queued",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, next_action)

    def test_single_generation_boundary_is_active_in_adr_and_instructions(
        self,
    ) -> None:
        adr = normalized_text(ADR_0004)
        instructions = normalized_text(INSTRUCTIONS)

        self.assertIn("## Status Accepted.", adr)
        for fragment in (
            "development integrity boundary, not a product runtime interface",
            "One real batch is controlled by one toolchain generation",
            "stable and candidate do not import, invoke, synchronize with, or "
            "share runtime execution state with one another",
            "controller under construction does not control its own "
            "implementation batch",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment.lower(), adr.lower())
                self.assertIn(fragment.lower(), instructions.lower())

    def test_execution_state_foundation_and_adr_are_historical(self) -> None:
        adr = normalized_text(ADR_0003)
        supersession = normalized_text(SUPERSESSION)
        batch_row = ledger_row("| `ccfg-26-execution-state-foundation` |")

        self.assertTrue(SUPERSESSION.is_file())
        self.assertIn("## Status Superseded by", adr)
        self.assertIn("It is not current CCFG-26 architecture", adr)
        self.assertIn("historical evidence", supersession)
        self.assertIn("| superseded |", batch_row)
        self.assertIn("superseded.md", batch_row)

    def test_active_ccfg26_instructions_reject_the_speculative_runtime_model(
        self,
    ) -> None:
        active_pickup = active_ccfg26_and_ccfg29_authority()

        for rejected_requirement in (
            "batch execution state",
            "automatic same-batch continuation",
            "recovery advisor",
            "read-only advisor",
            "runway_recovery_advisor",
            "fresh coordinator process",
            "fresh coordinator flight",
            "fresh execution-flight process",
            "new coordinator process",
            "execution flight",
            "cross-generation runtime coordination",
            "anchored filesystem",
            "namespace substitution",
            "win32",
            "nt backend",
        ):
            with self.subTest(rejected_requirement=rejected_requirement):
                self.assertNotIn(rejected_requirement, active_pickup)

        boundary = normalized_text(ADR_0004)
        self.assertIn(
            "CCFG-26 does not assume a new canonical Batch Execution State",
            boundary,
        )
        self.assertIn(
            "late namespace substitution is not an implicit requirement",
            boundary,
        )

    def test_rejected_issues_are_not_active_dependencies_or_parity_gates(
        self,
    ) -> None:
        core_authority = "\n".join(core_ccfg26_and_ccfg29_authority()).lower()

        for rejected_reference in (
            "#59",
            "#61",
            "github issue #60",
            "issues #59, #60, and #61",
            "#59/#60/#61 parity",
        ):
            with self.subTest(rejected_reference=rejected_reference):
                self.assertNotIn(rejected_reference, core_authority)

        issue_guardrails = {
            sentence
            for guardrail in active_guardrail_authority()
            for sentence in re.split(r"(?<=[.!?])\s+", guardrail.lower())
            if "#59" in sentence or "#61" in sentence
        }
        self.assertEqual(
            issue_guardrails,
            {
                "stop if replacement ccfg-26 work or ccfg-26c through ccfg-26e "
                "changes cor-009 identity, treats rejected github issues #59 or "
                "#61 as an input, dependency, requirement, or parity gate, or "
                "treats the raw issue #60 body as a current implementation "
                "specification instead of consuming the accepted slice-shape "
                "policy and its completed correction evidence.",
                "stop if the completed historical ccfg-26a scope is rewritten "
                "beyond its vertical-planning behavior or if rejected issue "
                "#59/#61 execution behavior is promoted from historical evidence "
                "into current authority.",
                "issues #59 and #61 are rejected, not-planned historical evidence "
                "and are not inputs, dependencies, requirements, or parity gates.",
                "rejected issues #59 and #61 and deferred issue #60 telemetry are "
                "not integration parity gates.",
            },
        )

        issue_60_guardrails = {
            sentence
            for guardrail in active_guardrail_authority()
            for sentence in re.split(r"(?<=[.!?])\s+", guardrail.lower())
            if "#60" in sentence
        }
        self.assertEqual(
            issue_60_guardrails,
            {
                next(
                    sentence
                    for sentence in issue_guardrails
                    if "raw issue #60" in sentence
                ),
                "stop if future ccfg-26 planning treats execution telemetry, "
                "changed-file or line-delta counts, review or validation breadth, "
                "or coordinator compaction as completed issue #60 behavior or as "
                "a prerequisite.",
                "any replacement ccfg-26 planning must preserve ccfg-26 and "
                "cor-009 identity and may consume completed issue #60 behavior "
                "only through `findings/slice-shape-policy-direction.md` and the "
                "slice-shape correction closeout evidence.",
                "rejected issues #59 and #61 and deferred issue #60 telemetry are "
                "not integration parity gates.",
            },
        )

        source_context = markdown_section(LEDGER, "## Source Context")
        self.assertIn("GitHub issue #59", source_context)
        self.assertIn("GitHub issue #61", source_context)
        self.assertIn("closed as not planned", source_context)
        self.assertIn("historical evidence only", source_context)

    def test_completed_issue_60_authority_is_repo_owned_and_shape_only(
        self,
    ) -> None:
        finding_row = ledger_row("| CCFG-26. Transfer Execution")
        integration_row = ledger_row("| CCFG-29. Contract-First Convergence")

        for authority_path in (
            "findings/slice-shape-policy-direction.md",
            "batches/ccfg-26-slice-shape-policy-correction/closeout.md",
            "batches/ccfg-26-slice-shape-policy-correction/"
            "post-closeout-correction.md",
        ):
            with self.subTest(authority_path=authority_path):
                self.assertIn(authority_path, finding_row)

        self.assertNotIn("GitHub issue #60", finding_row)
        for active_row in (finding_row, integration_row):
            with self.subTest(active_row=active_row[:40]):
                self.assertIn(
                    "notes/stable-runway-dogfooding-policy.md",
                    active_row,
                )
                self.assertNotIn(
                    "findings/github-issue-62-stable-runway-dogfooding-bootstrap.md",
                    active_row,
                )

        self.assertTrue(DOGFOOD_POLICY.is_file())
        contract_boundary = markdown_section(
            SLICE_SHAPE_POLICY,
            "## Completed Issue #60 Contract Boundary",
        )
        for rejected_scope in (
            "fresh coordinator processes",
            "execution flights",
            "automatic same-batch continuation",
            "a recovery advisor",
            "Batch Execution State",
            "cross-generation runtime coordination",
        ):
            with self.subTest(rejected_scope=rejected_scope):
                self.assertIn(rejected_scope, contract_boundary)
        self.assertIn("does not authorize", contract_boundary)

        policy_text = normalized_text(SLICE_SHAPE_POLICY)
        self.assertNotIn(
            "Current direction is "
            "`ccfg-26-execution-state-authority-direction.md`",
            policy_text,
        )
        self.assertIn(
            "Current CCFG-26 direction comes only from canonical `CURRENT.md`, "
            "`LEDGER.md`, and ADR 0004",
            policy_text,
        )
        self.assertIn(
            "retained only as rejected historical evidence",
            policy_text,
        )

        issue_62_relationship = markdown_section(
            ISSUE_62_FINDING,
            "## CCFG-26 And CCFG-29 Relationship",
        )
        self.assertIn("earlier interpretation", issue_62_relationship)
        self.assertIn("is superseded", issue_62_relationship)
        self.assertIn("#59 and #61 are rejected not-planned ideas", issue_62_relationship)
        self.assertIn("No issue-number parity gate applies", issue_62_relationship)

    def test_issue_60_telemetry_and_compaction_metrics_remain_deferred(
        self,
    ) -> None:
        active_authority = active_ccfg26_and_ccfg29_authority()
        contract_boundary = markdown_section(
            SLICE_SHAPE_POLICY,
            "## Completed Issue #60 Contract Boundary",
        ).lower()
        deferred_questions = markdown_section(
            SLICE_SHAPE_POLICY,
            "## Deferred Design Questions",
        ).lower()

        for metric in (
            "execution telemetry",
            "changed-file counts",
            "line deltas",
            "review breadth",
            "validation breadth",
            "coordinator-compaction metrics",
        ):
            with self.subTest(metric=metric):
                self.assertIn(metric, contract_boundary)

        for prohibited_requirement in (
            "requires execution telemetry",
            "must record execution telemetry",
            "requires changed-file counts",
            "requires line deltas",
            "requires review breadth",
            "requires validation breadth",
            "requires coordinator-compaction metrics",
            "telemetry prerequisite",
            "compaction prerequisite",
        ):
            with self.subTest(prohibited_requirement=prohibited_requirement):
                self.assertNotIn(prohibited_requirement, active_authority)

        metric_sentences = tuple(
            sentence.strip()
            for unit in active_authority.splitlines()
            for sentence in re.split(r"(?<=[.!?])\s+", unit)
            if "telemetry" in sentence or "compaction" in sentence
        )
        self.assertGreaterEqual(len(metric_sentences), 5)
        for sentence in metric_sentences:
            with self.subTest(active_metric_context=sentence):
                self.assertRegex(sentence, r"\bdefer\w*|\bstop if\b|\bnot\b")
                for obligation in re.finditer(
                    r"\b(?:must|requires?|required|prerequisites?|gates?)\b",
                    sentence,
                ):
                    prefix = sentence[: obligation.start()]
                    self.assertRegex(prefix, r"\bstop if\b|\bnot\b")

        self.assertIn(
            "telemetry and coordinator-compaction metrics remain deferred",
            active_authority,
        )
        self.assertIn(
            "not part of the completed issue #60 contract",
            contract_boundary,
        )
        self.assertIn("not a prerequisite for ccfg-26", contract_boundary)
        self.assertIn("execution telemetry", deferred_questions)
        self.assertIn("coordinator compaction", deferred_questions)

    def test_canonical_vocabulary_does_not_promote_rejected_runtime_concepts(
        self,
    ) -> None:
        context = CONTEXT.read_text(encoding="utf-8")

        for rejected_concept in (
            "Execution Flight",
            "Execution Attempt",
            "Flight Reservation",
            "Attempt Resolution",
            "Completed Slice Prefix",
            "Batch Execution State",
            "Execution Transition Receipt",
            "Execution Flight Result",
            "Execution Next Action",
            "Automatic Same-Batch Continuation",
        ):
            with self.subTest(rejected_concept=rejected_concept):
                self.assertNotIn(rejected_concept, context)

        for established_concept in (
            "**Batch**:",
            "**Slice**:",
            "**Planning State Diagnostic**:",
            "**Run State**:",
            "**Phase Result**:",
            "**Phase Receipt**:",
        ):
            with self.subTest(established_concept=established_concept):
                self.assertIn(established_concept, context)


if __name__ == "__main__":
    unittest.main()

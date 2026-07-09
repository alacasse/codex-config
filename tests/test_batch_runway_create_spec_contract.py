from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills/batch-runway/SKILL.md"
CREATE_SPEC = REPO_ROOT / "skills/batch-runway/references/create-spec.md"
EXECUTE_SPEC = REPO_ROOT / "skills/batch-runway/references/execute-spec.md"
REFERENCE_FILES = tuple((REPO_ROOT / "skills/batch-runway/references").rglob("*.md"))
PROGRAM_CURRENT = REPO_ROOT / "docs/plans/programs/codex-config/CURRENT.md"
PROGRAM_LEDGER = REPO_ROOT / "docs/plans/programs/codex-config/LEDGER.md"
BATCH_RUNWAY_ROOT = REPO_ROOT / "docs/plans/programs"
PST_18_RUNWAY = (
    REPO_ROOT
    / "docs/plans/programs/planning-state-tooling/batches/"
    "batch-runway-create-spec-output-contract/runway.md"
)
CCFG_7_COMPLETED_RUNWAY = (
    REPO_ROOT
    / "docs/plans/programs/codex-config/batches/"
    "ccfg-7-batch-runway-hot-path-pruning/runway.md"
)

FORBIDDEN_OVERRIDE_PATTERNS = (
    re.compile(r"\btreat this .*create[- ]spec\b", re.IGNORECASE),
    re.compile(r"\bimplementation starts(?:\s+in\s+a)?\s+later\b", re.IGNORECASE),
    re.compile(
        r"\bsession[- ]local\b.*\b(create[- ]spec|mode|context)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bcreate[- ]spec\b.*\bsession[- ]local\b",
        re.IGNORECASE,
    ),
)

NON_ROUTINE_REFERENCE_NAMES = (
    "execute-recovery-v1.md",
    "finalize-batch-v1.md",
    "subagent-briefs.md",
    "reporting-contracts-v1.md",
    "test-quality-review.md",
    "projection-reporting.md",
)

DOWNSTREAM_PROJECT_PATTERNS = (
    "/home/alacasse/projects/" + "graphify",
    "my-docs/" + "plans",
    "codex-config-" + "uv-cache",
    "Graphify-" + "specific",
    "project-specific " + "validation",
)

LEAN_REFERENCE_EXAMPLES = (
    "skills/batch-runway/references/execute-slice-core-v1.md",
    "skills/batch-runway/references/execution-contract-v1.md",
    "skills/batch-runway/references/reporting-contracts-v1.md",
    "skills/batch-runway/references/ledger-retention-v1.md",
)

OLD_ABSOLUTE_BATCH_RUNWAY_REFERENCE_PLACEHOLDER = re.compile(
    r"`<absolute path to batch-runway>/references/[^`]+`"
)
LOCAL_CODEX_CONFIG_SKILL_PREFIX = "/home/alacasse/projects/codex-config/skills/"
PLANNING_RUNWAY_PATH = re.compile(
    r"docs/plans/programs/[^\s`|]+/batches/[^\s`|]+/runway\.md"
)
PLANNING_DISPATCH_PATH = re.compile(
    r"docs/plans/programs/[^\s`|]+/batches/[^\s`|]+/dispatch\.md"
)


def normalized(markdown: str) -> str:
    return re.sub(r"\s+", " ", markdown)


def section_between(markdown: str, start_heading: str, end_heading: str) -> str:
    start = markdown.index(start_heading)
    end = markdown.index(end_heading, start)
    return markdown[start:end]


def override_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    lines = markdown.splitlines()

    for index, line in enumerate(lines):
        if line.strip() != "Overrides:":
            continue

        block_lines: list[str] = []
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if not stripped or stripped.startswith("#"):
                break
            block_lines.append(candidate)
        blocks.append("\n".join(block_lines))

    return blocks


def active_runway_paths() -> set[Path]:
    current_text = PROGRAM_CURRENT.read_text(encoding="utf-8")
    ledger_text = PROGRAM_LEDGER.read_text(encoding="utf-8")
    active_paths: set[Path] = set()

    for text in (current_text, ledger_text):
        for match in PLANNING_RUNWAY_PATH.finditer(text):
            path = REPO_ROOT / match.group(0)
            if path.is_relative_to(BATCH_RUNWAY_ROOT):
                active_paths.add(path)
        for match in PLANNING_DISPATCH_PATH.finditer(text):
            path = REPO_ROOT / match.group(0)
            runway_path = path.with_name("runway.md")
            if runway_path.is_relative_to(BATCH_RUNWAY_ROOT):
                active_paths.add(runway_path)

    return {
        path
        for path in active_paths
        if path.exists()
        and not any(
            f"| `{path.parent.name}` | {inactive_status} |" in ledger_text
            for inactive_status in ("completed", "superseded", "abandoned")
        )
    }


class BatchRunwayCreateSpecContractTests(unittest.TestCase):
    def assert_no_session_local_override_claims(
        self,
        path: Path,
    ) -> None:
        blocks = override_blocks(path.read_text(encoding="utf-8"))

        self.assertGreater(len(blocks), 0, f"no Overrides blocks found in {path}")
        for pattern in FORBIDDEN_OVERRIDE_PATTERNS:
            for block in blocks:
                with self.subTest(path=str(path), pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(block), block)

    def assert_not_mandatory_for_routine_slices(
        self,
        path: Path,
        text: str,
    ) -> None:
        for reference_name in NON_ROUTINE_REFERENCE_NAMES:
            escaped_reference = re.escape(reference_name)
            forbidden_patterns = (
                rf"\bFor routine (?:slice execution|slices?)\b[^.]*\bread\b"
                rf"[^.]*`[^`]*{escaped_reference}`",
                rf"\bDuring routine execution\b[^.]*\bread\b[^.]*`[^`]*"
                rf"{escaped_reference}`",
                rf"\broutine (?:slice execution|slices?|execution)\b[^.]*"
                rf"\bmust\b[^.]*\bread\b[^.]*`[^`]*{escaped_reference}`",
                rf"\broutine (?:slice execution|slices?|execution)\b[^.]*"
                rf"\brequires?\b[^.]*`[^`]*{escaped_reference}`",
                rf"\bread\b[^.]*`[^`]*{escaped_reference}`[^.]*\bfor "
                rf"routine (?:slice execution|slices?|execution)\b",
            )

            for pattern in forbidden_patterns:
                with self.subTest(path=str(path), reference=reference_name):
                    self.assertIsNone(re.search(pattern, text), pattern)

    def test_create_spec_guidance_keeps_session_mode_out_of_overrides(self) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")

        self.assertIn(
            "Use `Overrides` only for durable execution-contract deviations",
            text,
        )
        self.assertIn("Do not use `Overrides` for session-local", text)
        self.assertIn(
            "Place create-spec task context in the current baseline",
            text,
        )
        self.assert_no_session_local_override_claims(CREATE_SPEC)

    def test_lean_create_spec_reference_examples_are_repo_relative(self) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")
        lean_contract = section_between(
            text,
            "For lean specs, do not paste the full standard execution contract.",
            "Use `Overrides` only for durable execution-contract deviations",
        )

        self.assertIsNone(
            OLD_ABSOLUTE_BATCH_RUNWAY_REFERENCE_PLACEHOLDER.search(lean_contract),
            lean_contract,
        )
        for example in LEAN_REFERENCE_EXAMPLES:
            with self.subTest(example=example):
                self.assertIn(f"- `{example}`", lean_contract)

    def test_create_spec_guidance_allows_relative_reusable_references(self) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")
        reference_guidance = section_between(
            text,
            "Generated dispatch and runway artifacts should use repo-relative",
            "Use `Overrides` only for durable execution-contract deviations",
        )
        normalized_reference_guidance = normalized(reference_guidance)

        self.assertIn(
            "`skills/batch-runway/references/execution-contract-v1.md`",
            reference_guidance,
        )
        self.assertIn(
            "`references/execution-contract-v1.md`",
            reference_guidance,
        )
        self.assertIn(
            "Do not embed local absolute paths for those reusable repo-owned "
            "skill references.",
            normalized_reference_guidance,
        )
        self.assertIn(
            "This rule does not ban absolute paths for user-provided local "
            "values",
            normalized_reference_guidance,
        )

    def test_active_runway_artifacts_do_not_embed_local_skill_paths(self) -> None:
        self.assertIn(
            LOCAL_CODEX_CONFIG_SKILL_PREFIX,
            CCFG_7_COMPLETED_RUNWAY.read_text(encoding="utf-8"),
        )

        active_paths = active_runway_paths()
        ledger_text = PROGRAM_LEDGER.read_text(encoding="utf-8")
        ccfg_17_runway = (
            REPO_ROOT
            / "docs/plans/programs/codex-config/batches/"
            "ccfg-17-absolute-runway-reference-paths/runway.md"
        )

        if "| `ccfg-17-absolute-runway-reference-paths` | queued |" in ledger_text:
            self.assertIn(ccfg_17_runway, active_paths)
        self.assertNotIn(CCFG_7_COMPLETED_RUNWAY, active_paths)

        for path in active_paths:
            with self.subTest(path=str(path)):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn(LOCAL_CODEX_CONFIG_SKILL_PREFIX, text)

    def test_pst_18_queued_runway_keeps_session_mode_out_of_overrides(self) -> None:
        self.assert_no_session_local_override_claims(PST_18_RUNWAY)

    def test_forbidden_patterns_cover_known_implementation_later_forms(self) -> None:
        examples = (
            "implementation starts later",
            "implementation starts in a later session",
        )

        for example in examples:
            with self.subTest(example=example):
                self.assertTrue(
                    any(pattern.search(example) for pattern in FORBIDDEN_OVERRIDE_PATTERNS)
                )

    def test_routine_execute_spec_hot_path_stays_compact(self) -> None:
        skill_text = normalized(SKILL.read_text(encoding="utf-8"))
        execute_spec_text = normalized(EXECUTE_SPEC.read_text(encoding="utf-8"))

        self.assertIn(
            "For routine slice execution, read "
            "`references/execute-slice-core-v1.md` and only the selected "
            "validation profile file under `references/validation-profiles/`.",
            skill_text,
        )
        self.assertIn(
            "For routine slice execution, prefer `execute-slice-core-v1.md` "
            "plus the selected profile file under `validation-profiles/`.",
            execute_spec_text,
        )
        self.assertIn(
            "For routine slice execution, use `execute-slice-core-v1.md` and "
            "the selected validation profile file.",
            execute_spec_text,
        )
        self.assertIn(
            "For routine slices, follow "
            "`references/execute-slice-core-v1.md`; it owns the "
            "worker/reviewer handoffs, validation/review loop, commit "
            "receipt, ledger/archive update, anomaly logging, and "
            "continuation.",
            skill_text,
        )
        self.assert_not_mandatory_for_routine_slices(SKILL, skill_text)
        self.assert_not_mandatory_for_routine_slices(EXECUTE_SPEC, execute_spec_text)

    def test_non_routine_references_remain_trigger_loaded(self) -> None:
        skill_text = normalized(SKILL.read_text(encoding="utf-8"))
        execute_spec_text = normalized(EXECUTE_SPEC.read_text(encoding="utf-8"))

        skill_trigger_patterns = (
            (
                r"`\.\./planning-state/references/projection-reporting\.md`: "
                r"read before broad history/reporting scans"
            ),
            (
                r"`references/reporting-contracts-v1\.md`: read before "
                r"requesting .* outside the routine core path"
            ),
            (
                r"`references/execute-recovery-v1\.md`: read only when "
                r"validation fails, review finds issues, blockers appear, .* "
                r"escalation is required"
            ),
            (
                r"`references/finalize-batch-v1\.md`: read only when closing "
                r"a batch or producing a final report"
            ),
            (
                r"`references/subagent-briefs\.md`: read only when full brief "
                r"variants, support-agent guidance, triggered specialist "
                r"review routing, or non-routine subagent prompting is needed"
            ),
            (
                r"`references/test-quality-review\.md`: read only when a "
                r"slice explicitly asks for test quality review or when "
                r"changed tests trigger test-review routing"
            ),
        )

        execute_spec_trigger_patterns = (
            (
                r"Use this file as the routing surface for compatibility "
                r"questions, non-routine execution, recovery, and finalization"
            ),
            (
                r"When execution needs pending-batch inventory, .* read "
                r"`\.\./\.\./planning-state/references/"
                r"projection-reporting\.md`"
            ),
            (
                r"Read the full Batch Runway reference files named by the spec "
                r"only when the spec is full-runway, the slice is non-routine"
            ),
            r"Use `subagent-briefs\.md` for triggered specialist-review "
            r"routing",
            r"Read `execute-recovery-v1\.md` when validation fails, review "
            r"finds issues",
            r"Read `finalize-batch-v1\.md` before closing the batch",
        )

        for pattern in skill_trigger_patterns:
            with self.subTest(path=str(SKILL), pattern=pattern):
                self.assertRegex(skill_text, pattern)

        for pattern in execute_spec_trigger_patterns:
            with self.subTest(path=str(EXECUTE_SPEC), pattern=pattern):
                self.assertRegex(execute_spec_text, pattern)

    def test_reusable_batch_runway_guidance_stays_project_neutral(self) -> None:
        for path in (SKILL, EXECUTE_SPEC, *REFERENCE_FILES):
            text = path.read_text(encoding="utf-8")
            for pattern in DOWNSTREAM_PROJECT_PATTERNS:
                with self.subTest(path=str(path), pattern=pattern):
                    self.assertNotIn(pattern, text)

    def test_create_spec_validation_commands_require_status_classes(self) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")
        validation_contract = section_between(
            text,
            "Every focused validation command in a generated runway",
            "Each slice must include:",
        )
        normalized_contract = normalized(validation_contract)

        self.assertIn("declare exactly one status class", normalized_contract)
        for status_class in (
            "required-green",
            "known-red-baseline",
            "implementation-created",
            "conditional",
            "diagnostic-only",
        ):
            with self.subTest(status_class=status_class):
                self.assertIn(f"`{status_class}`", validation_contract)

    def test_required_green_requires_evidence_or_slice_owned_remediation(self) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")
        validation_contract = normalized(
            section_between(
                text,
                "Every focused validation command in a generated runway",
                "Each slice must include:",
            )
        )

        self.assertRegex(
            validation_contract,
            r"`required-green`: .*expected to pass now, or the slice explicitly "
            r"owns the remediation",
        )
        self.assertRegex(
            validation_contract,
            r"Use this only with a current passing result, or with a named "
            r"slice-owned remediation path and acceptance criteria",
        )

    def test_non_green_statuses_require_explicit_gating_context(self) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")
        validation_contract = normalized(
            section_between(
                text,
                "Every focused validation command in a generated runway",
                "Each slice must include:",
            )
        )

        self.assertRegex(
            validation_contract,
            r"`known-red-baseline`: .*currently fails.*cannot block execution "
            r"until a named slice fixes the failure and promotes it with green "
            r"evidence",
        )
        self.assertRegex(
            validation_contract,
            r"`implementation-created`: .*does not exist yet\. Name the slice "
            r"that creates it before the command can become a required gate",
        )
        self.assertRegex(
            validation_contract,
            r"`conditional`: .*State the trigger condition precisely enough "
            r"that an executor can decide whether to run it",
        )

    def test_diagnostic_and_future_commands_cannot_be_silent_required_gates(
        self,
    ) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")
        validation_contract = normalized(
            section_between(
                text,
                "Every focused validation command in a generated runway",
                "Each slice must include:",
            )
        )

        self.assertIn(
            "Do not silently promote a known-red command, a missing "
            "future-created command, or a diagnostic command to "
            "`required-green`.",
            validation_contract,
        )
        self.assertIn(
            "Promotion requires explicit evidence that the command is now "
            "green, or an explicitly named slice-owned remediation path that "
            "makes it green before it gates downstream work.",
            validation_contract,
        )

    def test_generated_spec_checklist_requires_batch_kind(self) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")
        checklist = section_between(
            text,
            "The spec must include:",
            "Every generated dispatch or runway artifact",
        )

        self.assertIn("- batch kind and slice risk contract", checklist)

    def test_create_spec_guidance_names_batch_kinds_and_slice_risk_classes(
        self,
    ) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")
        batch_kind_contract = section_between(
            text,
            "Every generated dispatch or runway artifact must declare exactly one "
            "batch",
            "Every generated slice that can change",
        )
        slice_risk_contract = section_between(
            text,
            "Every generated slice that can change",
            "Destructive or contract-narrowing slices require",
        )

        for batch_kind in (
            "characterization",
            "decision",
            "migration",
            "destructive-cleanup",
            "mixed-risk",
        ):
            with self.subTest(batch_kind=batch_kind):
                self.assertIn(f"`{batch_kind}`", batch_kind_contract)

        for risk_class in (
            "none",
            "evidence-only",
            "decision-only",
            "migration",
            "contract-narrowing",
            "destructive-cleanup",
        ):
            with self.subTest(risk_class=risk_class):
                self.assertIn(f"`{risk_class}`", slice_risk_contract)

    def test_destructive_cleanup_in_evidence_or_characterization_work_is_gated(
        self,
    ) -> None:
        text = CREATE_SPEC.read_text(encoding="utf-8")
        risk_gate_contract = normalized(
            section_between(
                text,
                "Destructive or contract-narrowing slices require",
                "For lean specs, do not paste",
            )
        )

        self.assertRegex(
            risk_gate_contract,
            r"Destructive or contract-narrowing slices require an explicit "
            r"approval gate",
        )
        self.assertRegex(
            risk_gate_contract,
            r"A `characterization` batch or an `evidence-only` slice must not "
            r"include destructive cleanup or contract narrowing",
        )
        self.assertRegex(
            risk_gate_contract,
            r"If a batch combines evidence-only or decision-only work with "
            r"destructive cleanup, contract narrowing, or migration, declare "
            r"the batch kind as `mixed-risk`, name the risky slices, and list "
            r"the approval gate for each risky slice",
        )


if __name__ == "__main__":
    unittest.main()

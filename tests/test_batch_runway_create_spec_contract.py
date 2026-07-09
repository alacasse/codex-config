from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills/batch-runway/SKILL.md"
CREATE_SPEC = REPO_ROOT / "skills/batch-runway/references/create-spec.md"
EXECUTE_SPEC = REPO_ROOT / "skills/batch-runway/references/execute-spec.md"
PST_18_RUNWAY = (
    REPO_ROOT
    / "docs/plans/programs/planning-state-tooling/batches/"
    "batch-runway-create-spec-output-contract/runway.md"
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


def normalized(markdown: str) -> str:
    return re.sub(r"\s+", " ", markdown)


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
            "For routine slices, read `execute-slice-core-v1.md` and only the "
            "selected validation profile file.",
            execute_spec_text,
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
            r"Invoke specialist support reviewers only when triggered .* "
            r"using `subagent-briefs\.md` for routing",
            r"If focused validation fails, read `execute-recovery-v1\.md`",
            r"If review finds issues, read `execute-recovery-v1\.md`",
            r"Read `finalize-batch-v1\.md` before closing the batch",
        )

        for pattern in skill_trigger_patterns:
            with self.subTest(path=str(SKILL), pattern=pattern):
                self.assertRegex(skill_text, pattern)

        for pattern in execute_spec_trigger_patterns:
            with self.subTest(path=str(EXECUTE_SPEC), pattern=pattern):
                self.assertRegex(execute_spec_text, pattern)


if __name__ == "__main__":
    unittest.main()

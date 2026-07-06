from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CREATE_SPEC = REPO_ROOT / "skills/batch-runway/references/create-spec.md"
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


if __name__ == "__main__":
    unittest.main()

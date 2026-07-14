from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BATCH_RUNWAY = REPO_ROOT / "skills/batch-runway/SKILL.md"
CREATE_SPEC = REPO_ROOT / "skills/batch-runway/references/create-spec.md"
ARCHITECTURE_PROGRAM_RUNWAY = REPO_ROOT / "skills/architecture-program-runway/SKILL.md"
PORT_BY_CONTRACT = REPO_ROOT / "skills/port-by-contract/SKILL.md"
LEGACY_REMOVAL = REPO_ROOT / "skills/legacy-removal/SKILL.md"

REUSABLE_PLANNING_SURFACES = (
    BATCH_RUNWAY,
    CREATE_SPEC,
    ARCHITECTURE_PROGRAM_RUNWAY,
    PORT_BY_CONTRACT,
    LEGACY_REMOVAL,
)
SLICE_NUMBER = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
NUMERIC_SLICE_CONSTRAINTS = (
    re.compile(
        rf"\b{SLICE_NUMBER}\s*(?:[-–]|to|through)\s*{SLICE_NUMBER}"
        r"\s+slices?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:at least|at most|exactly|minimum(?: of)?|maximum(?: of)?)"
        rf"\s+{SLICE_NUMBER}\s+slices?\b",
        re.IGNORECASE,
    ),
)


def normalized(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


class SemanticSliceShapeContractTests(unittest.TestCase):
    def test_numeric_constraint_patterns_cover_range_and_limit_forms(self) -> None:
        forbidden_examples = (
            "Pick 3-5 slices.",
            "Pick three to five slices.",
            "Use at least 3 slices.",
            "Use exactly five slices.",
        )
        allowed_examples = (
            "For one slice, record the shared boundary.",
            "More than five slices are allowed when justified.",
        )

        for example in forbidden_examples:
            with self.subTest(example=example):
                self.assertTrue(
                    any(
                        pattern.search(example) for pattern in NUMERIC_SLICE_CONSTRAINTS
                    )
                )
        for example in allowed_examples:
            with self.subTest(example=example):
                self.assertFalse(
                    any(
                        pattern.search(example) for pattern in NUMERIC_SLICE_CONSTRAINTS
                    )
                )

    def test_reusable_planning_surfaces_set_no_numeric_slice_constraint(self) -> None:
        for path in REUSABLE_PLANNING_SURFACES:
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                text = path.read_text(encoding="utf-8")
                for pattern in NUMERIC_SLICE_CONSTRAINTS:
                    self.assertIsNone(pattern.search(text), pattern.pattern)

    def test_create_spec_derives_slice_count_from_semantic_boundaries(self) -> None:
        create_spec = normalized(CREATE_SPEC)

        self.assertIn("Start with one slice", create_spec)
        self.assertIn("Add a split only when", create_spec)
        self.assertIn("Merge proposed slices when", create_spec)
        self.assertIn("There is no normative numeric range", create_spec)
        self.assertIn(
            "independently testable, reviewable, and committable", create_spec
        )

    def test_one_slice_keeps_associated_tests_and_guidance_with_behavior(self) -> None:
        create_spec = normalized(CREATE_SPEC)
        create_spec_lower = create_spec.lower()

        self.assertIn(
            "one owner, risk, validation, and acceptance boundary",
            create_spec,
        )
        self.assertIn(
            "generic documentation, metadata, tests, or closeout work",
            create_spec_lower,
        )
        self.assertIn("must not become a standalone slice", create_spec_lower)

    def test_semantic_splits_cover_producer_consumer_and_risky_boundaries(
        self,
    ) -> None:
        create_spec = normalized(CREATE_SPEC)

        self.assertIn(
            "a later slice consumes a new API, artifact, or boundary",
            create_spec,
        )
        self.assertIn("intermediate state is valid and testable", create_spec)
        self.assertIn(
            "destructive cleanup or contract narrowing must be isolated",
            create_spec,
        )

    def test_slice_shape_explains_every_adjacent_multi_slice_boundary(self) -> None:
        create_spec = normalized(CREATE_SPEC)

        self.assertIn("`slice_shape`", create_spec)
        self.assertIn("every adjacent pair", create_spec)
        self.assertIn("applicable split condition", create_spec)
        self.assertIn("More than five slices", create_spec)
        self.assertIn("not rejected solely because of count", create_spec)

    def test_handoff_skills_delegate_semantic_slice_shape_without_a_count(self) -> None:
        expected_contracts: dict[Path, tuple[str, ...]] = {
            ARCHITECTURE_PROGRAM_RUNWAY: (
                "Optional `slice_shape` rationale",
                "without full execution contracts or a target count",
            ),
            PORT_BY_CONTRACT: ("cohesive semantic slice shape",),
            LEGACY_REMOVAL: (
                "slice shape will be derived from semantic execution boundaries",
            ),
        }

        for path, expected_fragments in expected_contracts.items():
            text = normalized(path)
            for fragment in expected_fragments:
                with self.subTest(
                    path=str(path.relative_to(REPO_ROOT)),
                    fragment=fragment,
                ):
                    self.assertIn(fragment, text)


if __name__ == "__main__":
    unittest.main()

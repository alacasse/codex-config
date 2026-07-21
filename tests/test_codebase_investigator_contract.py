from __future__ import annotations

import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENT_PATH = REPO_ROOT / "agents" / "codebase_investigator.toml"


def test_investigator_is_bounded_read_only_support() -> None:
    config = tomllib.loads(AGENT_PATH.read_text(encoding="utf-8"))
    instructions = config["developer_instructions"]

    assert config["name"] == "codebase_investigator"
    assert "without modifying files" in instructions
    assert "Never spawn, delegate to, or wait" in instructions
    assert "Answer the exact delegated question" in instructions
    assert "direct evidence, reasonable inference, and unresolved uncertainty" in instructions


def test_investigator_response_guidance_is_compact_and_evidence_backed() -> None:
    instructions = tomllib.loads(AGENT_PATH.read_text(encoding="utf-8"))[
        "developer_instructions"
    ]
    for guidance in (
        "Lead with the answer",
        "precise file and line references",
        "direct evidence, reasonable inference, and unresolved uncertainty",
        "Omit raw logs",
    ):
        assert guidance in instructions
    assert "Return YAML only" not in instructions
    assert "machine-readable" not in instructions

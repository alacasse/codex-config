from __future__ import annotations

from pathlib import Path


SKILL = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "dead-surface-audit"
    / "SKILL.md"
)


def test_dead_surface_audit_owns_a_small_evidence_vocabulary() -> None:
    text = SKILL.read_text(encoding="utf-8")
    for status in (
        "keep",
        "delete-now",
        "migrate-tests-first",
        "keep-thin-entrypoint",
        "human-contract-decision",
    ):
        assert f"`{status}`" in text
    assert "tests as evidence, not" in text
    assert "does not authorize\ndeletion" in text


def test_dead_surface_audit_requires_behavioral_caller_evidence() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "Run the dual deletion test" in text
    assert "production/runtime code" in text
    assert "topology-assertion" in text
    assert "Require a named caller or contract" in text
    assert "Do not create queues, execution state" in text

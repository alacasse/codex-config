"""Read-only Planning Artifact Layout v1 state model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


NONE_VALUES = {"", "none", "none selected", "n/a", "tbd"}


@dataclass(frozen=True)
class ArtifactPointer:
    label: str
    value: str | None
    source_path: Path
    exists: bool | None = None


@dataclass(frozen=True)
class RedirectEvidence:
    source_path: Path
    target_path: str | None
    current_state_path: str | None = None


@dataclass(frozen=True)
class StateWarning:
    code: str
    message: str
    source_path: Path | None = None


@dataclass(frozen=True)
class ValidationMessage:
    severity: str
    code: str
    message: str
    source_path: Path | None = None


@dataclass(frozen=True)
class ProgramState:
    slug: str
    current_path: Path
    purpose: str | None
    ledger: ArtifactPointer
    selected_dispatch: ArtifactPointer
    active_runway: ArtifactPointer
    queued_batch: ArtifactPointer
    latest_closeout: ArtifactPointer
    run_artifact_location: ArtifactPointer
    archive_location: ArtifactPointer
    next_safe_action: str | None
    stop_conditions: tuple[str, ...] = ()


@dataclass(frozen=True)
class RootState:
    root_path: Path
    current_path: Path
    layout: str | None
    planning_root: str | None
    run_artifact_root: str | None
    output_root: str | None
    one_shot_intake: str | None
    program_archive_root: str | None
    active_programs: tuple[ArtifactPointer, ...]
    next_safe_action: str | None


@dataclass(frozen=True)
class PlanningState:
    root: RootState
    programs: tuple[ProgramState, ...]
    redirects: tuple[RedirectEvidence, ...] = ()
    warnings: tuple[StateWarning, ...] = ()
    validation_messages: tuple[ValidationMessage, ...] = ()


def load_planning_state(root: str | Path) -> PlanningState:
    """Load Planning Artifact Layout v1 state without mutating files."""

    root_path = Path(root)
    root_current = root_path / "CURRENT.md"
    root_text = _read_text(root_current)
    root_fields = _field_map(root_text)
    active_programs = _active_programs(root_text, root_current)
    root_state = RootState(
        root_path=root_path,
        current_path=root_current,
        layout=root_fields.get("layout"),
        planning_root=root_fields.get("planning root"),
        run_artifact_root=root_fields.get("run artifact root"),
        output_root=root_fields.get("output root"),
        one_shot_intake=root_fields.get("one-shot intake"),
        program_archive_root=root_fields.get("program archive root"),
        active_programs=tuple(active_programs),
        next_safe_action=_section_text(root_text, "Next Safe Action"),
    )

    programs = tuple(_load_program(root_path, pointer) for pointer in active_programs)
    redirects = tuple(_redirects(root_path))
    warnings = tuple(_warnings(root_path, root_state, programs, redirects))
    validation_messages = tuple(_validation_messages(root_state, programs, redirects))
    return PlanningState(
        root=root_state,
        programs=programs,
        redirects=redirects,
        warnings=warnings,
        validation_messages=validation_messages,
    )


def _load_program(root_path: Path, pointer: ArtifactPointer) -> ProgramState:
    current_path = _resolve_pointer(root_path, pointer.value)
    text = _read_text(current_path)
    fields = _field_map(text)
    slug = fields.get("program slug") or pointer.label
    return ProgramState(
        slug=slug,
        current_path=current_path,
        purpose=fields.get("purpose"),
        ledger=_artifact("current ledger", fields, current_path, root_path),
        selected_dispatch=_artifact("selected dispatch path", fields, current_path, root_path),
        active_runway=_artifact("active batch runway spec path", fields, current_path, root_path),
        queued_batch=_artifact("queued batch path or id", fields, current_path, root_path),
        latest_closeout=_artifact(("latest closeout path", "latest closeout"), fields, current_path, root_path),
        run_artifact_location=_artifact("run artifact location", fields, current_path, root_path),
        archive_location=_artifact("program archive location", fields, current_path, root_path),
        next_safe_action=_section_text(text, "Next Safe Action"),
        stop_conditions=tuple(_list_items(_section_text(text, "Stop Conditions") or "")),
    )


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _field_map(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.strip()
        match = re.match(r"^(?:-\s*)?([^:|]+):\s*(.*)$", line)
        if match and not line.startswith("|"):
            key = _normal_key(match.group(1))
            value = _clean_value(match.group(2))
            if not value and index + 1 < len(lines):
                next_line = lines[index + 1].strip()
                if next_line.startswith("`") or next_line.startswith("<"):
                    value = _clean_value(next_line)
                    index += 1
            fields[key] = value
        index += 1
    return fields


def _active_programs(text: str, source_path: Path) -> list[ArtifactPointer]:
    programs: list[ArtifactPointer] = []
    in_table = False
    for line in text.splitlines():
        if line.strip().lower() == "## active programs":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.lstrip().startswith("|"):
            continue
        cells = [_clean_value(cell) for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() in {"program", "---"}:
            continue
        programs.append(
            ArtifactPointer(
                label=cells[0],
                value=_none_to_null(cells[1]),
                source_path=source_path,
            )
        )
    return programs


def _artifact(
    label: str | tuple[str, ...],
    fields: dict[str, str],
    source_path: Path,
    root_path: Path,
) -> ArtifactPointer:
    labels = (label,) if isinstance(label, str) else label
    value = _none_to_null(next((fields[key] for key in labels if key in fields), None))
    exists = None
    if value is not None and "/" in value:
        exists = _resolve_pointer(root_path, value).exists()
    return ArtifactPointer(label=labels[0], value=value, source_path=source_path, exists=exists)


def _redirects(root_path: Path) -> Iterable[RedirectEvidence]:
    for path in sorted(root_path.glob("*.md")):
        if path.name in {"CURRENT.md", "README.md"}:
            continue
        text = _read_text(path)
        if not re.search(r"^#\s*Redirect:", text, re.MULTILINE):
            continue
        fields = _field_map(text)
        target = fields.get("new path") or _first_code_path_after(text, "moved to")
        current_state = fields.get("program current state")
        yield RedirectEvidence(path, target, current_state)


def _warnings(
    root_path: Path,
    root_state: RootState,
    programs: tuple[ProgramState, ...],
    redirects: tuple[RedirectEvidence, ...],
) -> Iterable[StateWarning]:
    active_paths = {root_state.current_path, *(program.current_path for program in programs)}
    for redirect in redirects:
        yield StateWarning(
            "redirect_ledger",
            f"{redirect.source_path.name} redirects to {redirect.target_path or 'an unknown target'}",
            redirect.source_path,
        )
    for path in sorted(root_path.glob("*pickup*.md")):
        if path not in active_paths:
            yield StateWarning(
                "stale_pickup_note",
                f"{path.name} is pickup evidence, not active state",
                path,
            )
    historical_patterns = ("*-runway.md", "dispatch/*.md")
    for pattern in historical_patterns:
        for path in sorted(root_path.glob(pattern)):
            if "programs" not in path.parts:
                yield StateWarning(
                    "historical_batch_artifact",
                    f"{path.relative_to(root_path)} is historical evidence, not active state",
                    path,
                )
    selected_values = [
        program.selected_dispatch.value or program.active_runway.value or program.queued_batch.value
        for program in programs
    ]
    if not any(selected_values) and any(root_path.glob("*pickup*.md")):
        yield StateWarning(
            "stale_pickup_contradiction",
            "pickup notes exist while CURRENT.md files select no active batch",
            root_path,
        )


def _validation_messages(
    root_state: RootState,
    programs: tuple[ProgramState, ...],
    redirects: tuple[RedirectEvidence, ...],
) -> Iterable[ValidationMessage]:
    if not root_state.current_path.exists():
        yield ValidationMessage("error", "missing_root_current", "root CURRENT.md is missing", root_state.current_path)
    if root_state.layout != "Planning Artifact Layout v1":
        yield ValidationMessage("warning", "unknown_layout", "layout is not Planning Artifact Layout v1", root_state.current_path)
    if not root_state.active_programs:
        yield ValidationMessage("warning", "no_active_programs", "root CURRENT.md lists no active programs", root_state.current_path)
    for pointer, program in zip(root_state.active_programs, programs, strict=False):
        if pointer.value and not program.current_path.exists():
            yield ValidationMessage("error", "missing_program_current", f"{pointer.value} is missing", root_state.current_path)
        if program.ledger.value and program.ledger.exists is False:
            yield ValidationMessage("error", "missing_program_ledger", f"{program.ledger.value} is missing", program.current_path)
    for redirect in redirects:
        if not redirect.target_path:
            yield ValidationMessage("warning", "redirect_without_target", "redirect has no target path", redirect.source_path)


def _resolve_pointer(root_path: Path, value: str | None) -> Path:
    if value is None:
        return root_path
    path = Path(value)
    if path.is_absolute():
        return path
    for width in range(min(len(path.parts), len(root_path.parts)), 0, -1):
        if path.parts[:width] == root_path.parts[-width:]:
            return root_path.joinpath(*path.parts[width:])
    return root_path / path


def _normal_key(value: str) -> str:
    return _clean_value(value).lower()


def _clean_value(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^`(.*)`$", r"\1", value)
    return value.strip()


def _none_to_null(value: str | None) -> str | None:
    if value is None:
        return None
    value = _clean_value(value)
    if value.lower() in NONE_VALUES:
        return None
    return value


def _section_text(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    section_lines: list[str] = []
    in_section = False
    heading_marker = f"## {heading}".lower()
    for line in lines:
        if line.strip().lower() == heading_marker:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            section_lines.append(line)
    value = "\n".join(section_lines).strip()
    return value or None


def _list_items(text: str) -> Iterable[str]:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            yield line[2:].strip()


def _first_code_path_after(text: str, marker: str) -> str | None:
    marker_index = text.lower().find(marker)
    if marker_index == -1:
        return None
    match = re.search(r"`([^`]+)`", text[marker_index:])
    if not match:
        return None
    return match.group(1)

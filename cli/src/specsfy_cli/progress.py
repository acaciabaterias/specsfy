from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path


FIELD = re.compile(r"^\*\*(?P<name>[^*]+)\*\*:\s*(?P<value>.+?)\s*$")
TABLE_FIELD = re.compile(
    r"^\|\s*(?P<name>[^|]+?)\s*\|\s*(?P<value>[^|]+?)\s*\|\s*$"
)
CHECKLIST_ITEM = re.compile(r"^\s*[-*+]\s*\[(?P<done>[ xX])\]\s+(?P<label>.+?)\s*$")
TASK_ID = re.compile(r"^(?:\*\*|`)?T\d+\b", re.IGNORECASE)
GATE_NAMES = ("definition gate", "plan gate", "delivery gate")


@dataclass(frozen=True)
class SpecProgress:
    slug: str
    title: str
    path: Path
    content: str
    status: str
    definition_gate: str
    plan_gate: str
    delivery_gate: str
    passed_gates: int
    total_gates: int
    completed_tasks: int
    pending_tasks: int
    total_tasks: int
    completed_items: int
    pending_items: int
    total_items: int
    percent: int

    def to_dict(self) -> dict:
        value = asdict(self)
        value.pop("content")
        value["path"] = str(self.path)
        return value


@dataclass(frozen=True)
class ProgressSummary:
    total_specs: int
    completed_specs: int
    completed_tasks: int
    pending_tasks: int
    total_tasks: int
    completed_items: int
    pending_items: int
    total_items: int
    passed_gates: int
    total_gates: int
    percent: int

    def to_dict(self) -> dict:
        return asdict(self)


def scan_specs(project: Path) -> list[SpecProgress]:
    root = project.expanduser().resolve()
    return [_parse_spec(path) for path in _spec_paths(root)]


def summarize_specs(specs: list[SpecProgress]) -> ProgressSummary:
    completed_items = sum(spec.completed_items for spec in specs)
    total_items = sum(spec.total_items for spec in specs)
    completed_tasks = sum(spec.completed_tasks for spec in specs)
    total_tasks = sum(spec.total_tasks for spec in specs)
    passed_gates = sum(spec.passed_gates for spec in specs)
    total_gates = sum(spec.total_gates for spec in specs)
    percent = _ratio(
        completed_items if total_items else passed_gates,
        total_items if total_items else total_gates,
    )
    return ProgressSummary(
        total_specs=len(specs),
        completed_specs=sum(spec.status.lower() == "complete" for spec in specs),
        completed_tasks=completed_tasks,
        pending_tasks=total_tasks - completed_tasks,
        total_tasks=total_tasks,
        completed_items=completed_items,
        pending_items=total_items - completed_items,
        total_items=total_items,
        passed_gates=passed_gates,
        total_gates=total_gates,
        percent=percent,
    )


def specs_fingerprint(project: Path) -> str:
    root = project.expanduser().resolve()
    digest = hashlib.sha256()
    for path in _spec_paths(root):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        try:
            digest.update(path.read_bytes())
        except OSError:
            continue
        digest.update(b"\0")
    return digest.hexdigest()


def _spec_paths(root: Path) -> list[Path]:
    canonical = root.glob("specs/specs/*/spec.md")
    legacy = root.glob("specs/*/spec.md")
    return sorted({path for path in (*canonical, *legacy) if path.is_file()})


def _parse_spec(path: Path) -> SpecProgress:
    fields: dict[str, str] = {}
    title = path.parent.name
    completed_tasks = total_tasks = 0
    completed_items = total_items = 0
    content = path.read_text(encoding="utf-8")
    for line in content.splitlines():
        if line.startswith("# ") and title == path.parent.name:
            title = line.removeprefix("# ").strip()
        field = FIELD.match(line) or TABLE_FIELD.match(line)
        if field:
            fields[field.group("name").strip().lower()] = field.group("value").strip()
        item = CHECKLIST_ITEM.match(line)
        if not item:
            continue
        done = item.group("done").lower() == "x"
        total_items += 1
        completed_items += done
        if TASK_ID.match(item.group("label")):
            total_tasks += 1
            completed_tasks += done
    passed_gates = sum(
        fields.get(name, "").lower() == "passed" for name in GATE_NAMES
    )
    total_gates = len(GATE_NAMES)
    percent = _ratio(
        completed_items if total_items else passed_gates,
        total_items if total_items else total_gates,
    )
    return SpecProgress(
        slug=path.parent.name,
        title=title,
        path=path,
        content=content,
        status=fields.get("status", "Unknown"),
        definition_gate=fields.get("definition gate", "Unknown"),
        plan_gate=fields.get("plan gate", "Unknown"),
        delivery_gate=fields.get("delivery gate", "Unknown"),
        passed_gates=passed_gates,
        total_gates=total_gates,
        completed_tasks=completed_tasks,
        pending_tasks=total_tasks - completed_tasks,
        total_tasks=total_tasks,
        completed_items=completed_items,
        pending_items=total_items - completed_items,
        total_items=total_items,
        percent=percent,
    )


def _ratio(completed: int, total: int) -> int:
    return round(completed * 100 / total) if total else 0

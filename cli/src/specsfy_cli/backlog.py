from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


FIELD = re.compile(r"^\*\*(?P<name>[^*]+)\*\*:\s*(?P<value>.+?)\s*$")
TABLE_FIELD = re.compile(
    r"^\|\s*(?P<name>[^|]+?)\s*\|\s*(?P<value>[^|]+?)\s*\|\s*$"
)


@dataclass(frozen=True)
class BacklogItem:
    slug: str
    title: str
    identifier: str
    status: str
    path: Path
    content: str


def scan_backlogs(project: Path) -> list[BacklogItem]:
    root = project.expanduser().resolve()
    return [_parse_backlog(path) for path in _backlog_paths(root)]


def backlogs_fingerprint(project: Path) -> str:
    root = project.expanduser().resolve()
    digest = hashlib.sha256()
    for path in _backlog_paths(root):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        try:
            digest.update(path.read_bytes())
        except OSError:
            continue
        digest.update(b"\0")
    return digest.hexdigest()


def _backlog_paths(root: Path) -> list[Path]:
    return sorted(
        path for path in root.glob("specs/backlog/*.md") if path.is_file()
    )


def _parse_backlog(path: Path) -> BacklogItem:
    content = path.read_text(encoding="utf-8")
    title = path.stem
    fields: dict[str, str] = {}
    for line in content.splitlines():
        if line.startswith("# ") and title == path.stem:
            title = line.removeprefix("# ").strip()
            if title.lower().startswith("backlog:"):
                title = title.split(":", 1)[1].strip()
        field = FIELD.match(line) or TABLE_FIELD.match(line)
        if field:
            fields[field.group("name").strip().lower()] = field.group("value").strip()
    return BacklogItem(
        slug=path.stem,
        title=title,
        identifier=fields.get("id", path.stem),
        status=fields.get("status", "Unknown"),
        path=path,
        content=content,
    )

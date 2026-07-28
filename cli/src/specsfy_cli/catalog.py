from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .github import api_headers


DEFAULT_CATALOG_URL = (
    "https://api.github.com/repos/promovaweb/specsfy/"
    "contents/specialists/catalog.json?ref=main"
)


@dataclass(frozen=True)
class CatalogEntry:
    name: str
    description: str
    category: str
    tags: tuple[str, ...]
    files: tuple[str, ...]
    dependencies: tuple[str, ...]
    requires: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "CatalogEntry":
        detect = value.get("detect", {})
        return cls(
            name=value["name"],
            description=value["description"],
            category=value["category"],
            tags=tuple(value.get("tags", [])),
            files=tuple(detect.get("files", [])),
            dependencies=tuple(detect.get("dependencies", [])),
            requires=tuple(value.get("requires", [])),
        )


class Catalog:
    def __init__(self, entries: list[CatalogEntry]) -> None:
        self.entries = sorted(entries, key=lambda entry: entry.name)
        self._by_name = {entry.name: entry for entry in entries}

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "Catalog":
        if payload.get("schema_version") != 1:
            raise ValueError("versão de catálogo não suportada")
        return cls([CatalogEntry.from_dict(value) for value in payload["skills"]])

    @classmethod
    def from_path(cls, path: Path) -> "Catalog":
        return cls.from_payload(json.loads(path.read_text(encoding="utf-8")))

    @classmethod
    def fetch(cls, url: str | None = None) -> "Catalog":
        override = os.environ.get("SPECSFY_SPECIALISTS_CATALOG")
        if override:
            return cls.from_path(Path(override).expanduser().resolve())
        request = urllib.request.Request(
            url or DEFAULT_CATALOG_URL,
            headers=api_headers(
                "specsfy-cli",
                accept="application/vnd.github.raw+json",
            ),
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return cls.from_payload(json.load(response))
        except urllib.error.HTTPError as error:
            if error.code in {401, 403, 404}:
                raise RuntimeError(
                    "catálogo de especialistas indisponível; autentique o GitHub "
                    "com `gh auth login` ou defina GH_TOKEN"
                ) from error
            raise

    def require(self, name: str) -> CatalogEntry:
        if not name.startswith("specsfy-specialist-"):
            raise ValueError("a skill especialista deve usar o prefixo specsfy-specialist-")
        try:
            return self._by_name[name]
        except KeyError as error:
            raise ValueError(f"skill não encontrada no catálogo: {name}") from error

    def resolve(self, names: list[str]) -> list[CatalogEntry]:
        resolved: list[CatalogEntry] = []
        completed: set[str] = set()
        active: set[str] = set()

        def visit(name: str) -> None:
            if name in completed:
                return
            if name in active:
                raise ValueError(
                    f"dependência circular entre especialistas: {name}"
                )
            entry = self.require(name)
            active.add(name)
            for required_name in entry.requires:
                visit(required_name)
            active.remove(name)
            completed.add(name)
            resolved.append(entry)

        for name in names:
            visit(name)
        return resolved

    def detect(self, project: Path) -> list[CatalogEntry]:
        dependencies = _read_dependencies(project)
        detected = []
        for entry in self.entries:
            file_match = any((project / marker).exists() for marker in entry.files)
            dependency_match = any(
                dependency in dependencies for dependency in entry.dependencies
            )
            if file_match or dependency_match:
                detected.append(entry)
        return detected


def _read_dependencies(project: Path) -> set[str]:
    dependencies: set[str] = set()
    for filename in ("package.json", "composer.json"):
        path = project / filename
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for key in (
            "dependencies",
            "devDependencies",
            "require",
            "require-dev",
            "peerDependencies",
        ):
            value = payload.get(key, {})
            if isinstance(value, dict):
                dependencies.update(value)
    return dependencies

#!/usr/bin/env python3
"""Collect safe, read-only evidence from this Specsfy hub only."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPOSITORIES = (
    (".", "dev"),
    ("brand", "brand"),
    ("skills", "skills"),
    ("docs", "docs"),
    ("example", "example"),
    ("specsfy", "specsfy"),
    ("specialists", "specialists"),
    ("cli", "cli"),
)
SOURCE_CANDIDATES = (
    "AGENTS.md",
    "README.md",
    "Spec.md",
    "pyproject.toml",
    "uv.lock",
    "composer.json",
    "composer.lock",
    "package.json",
    "package-lock.json",
)


class HubError(RuntimeError):
    """Raised when the selected workspace is not the canonical Specsfy hub."""


def git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise HubError(f"{repository}: git {' '.join(arguments)} falhou: {detail}")
    return result.stdout.rstrip("\n")


def normalize_remote(remote: str) -> str:
    value = remote.strip().removesuffix("/")
    if value.startswith("git@github.com:"):
        value = "https://github.com/" + value.removeprefix("git@github.com:")
    return value.removesuffix(".git")


def expected_remote(repository: str) -> str:
    return f"https://github.com/specsfy/{repository}"


def collect_repository(workspace: Path, relative: str, name: str) -> dict[str, object]:
    path = workspace if relative == "." else workspace / relative
    if not path.is_dir():
        raise HubError(f"raiz ausente: {relative} (esperado specsfy/{name})")

    observed_remote = normalize_remote(git(path, "remote", "get-url", "origin"))
    wanted_remote = expected_remote(name)
    if observed_remote != wanted_remote:
        raise HubError(
            f"{relative}: remoto origin é {observed_remote!r}; esperado {wanted_remote!r}"
        )

    tracked = [line for line in git(path, "ls-files").splitlines() if line]
    status = [line for line in git(path, "status", "--short").splitlines() if line]
    sources = [candidate for candidate in SOURCE_CANDIDATES if (path / candidate).is_file()]
    branch = git(path, "branch", "--show-current")
    head = git(path, "rev-parse", "HEAD")
    return {
        "path": relative,
        "repository": f"specsfy/{name}",
        "remote": observed_remote,
        "branch": branch,
        "head": head,
        "dirty": bool(status),
        "changes": status,
        "tracked_files": len(tracked),
        "sources": sources,
    }


def collect(workspace: Path) -> dict[str, object]:
    root = workspace.expanduser().resolve()
    try:
        repositories = [
            collect_repository(root, relative, name)
            for relative, name in REPOSITORIES
        ]
    except HubError as error:
        raise HubError(f"{root} não representa o hub Specsfy: {error}") from error
    return {
        "workspace": "specsfy/dev",
        "root": str(root),
        "repositories": repositories,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Coleta evidência somente leitura do hub Specsfy."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        required=True,
        help="raiz do checkout specsfy/dev que contém os sete repositórios filhos",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    try:
        evidence = collect(arguments.workspace)
    except HubError as error:
        print(error, file=sys.stderr)
        return 2
    print(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Calcula o fingerprint dos inputs que exigem rebuild do executável."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "bin",
    "dist",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def source_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES or not (path.is_file() or path.is_symlink()):
            continue
        digest.update(relative.as_posix().encode())
        digest.update(b"\0")
        # O Git preserva somente a distinção entre arquivo comum e executável.
        # Bits de escrita de grupo/usuário variam entre worktrees e runners.
        git_mode = b"120000" if path.is_symlink() else (
            b"100755" if path.lstat().st_mode & 0o111 else b"100644"
        )
        digest.update(git_mode)
        digest.update(b"\0")
        if path.is_symlink():
            digest.update(path.readlink().as_posix().encode())
        else:
            digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) > 1:
        print("uso: source_fingerprint.py [raiz]", file=sys.stderr)
        return 2
    root = Path(arguments[0] if arguments else ".").expanduser().resolve()
    if not root.is_dir():
        print(f"erro: raiz inválida: {root}", file=sys.stderr)
        return 1
    print(source_fingerprint(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

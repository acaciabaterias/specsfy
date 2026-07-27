#!/usr/bin/env python3
"""Prepare and extract one canonical Specsfy CLI changelog release section."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path


SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
UNRELEASED = "## [Unreleased]"


def stable_version(value: str) -> tuple[int, int, int]:
    match = SEMVER.fullmatch(value)
    if match is None:
        raise ValueError(f"versão estável inválida: {value}")
    return tuple(int(part) for part in match.groups())


def replace_once(text: str, pattern: str, replacement: str, source: Path) -> str:
    updated, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(
            f"{source} deve conter exatamente uma versão reconhecível; encontrou {count}"
        )
    return updated


def normalized_notes(path: Path) -> str:
    notes = path.read_text(encoding="utf-8").strip()
    if not notes:
        raise ValueError("as notas de release não podem estar vazias")
    if re.search(r"(?m)^## \[", notes):
        raise ValueError("as notas não podem declarar outra seção de versão")
    return f"{notes}\n"


def prepare(cli: Path, version: str, release_date: str, notes_file: Path) -> None:
    next_version = stable_version(version)
    try:
        dt.date.fromisoformat(release_date)
    except ValueError as error:
        raise ValueError(f"data ISO inválida: {release_date}") from error

    pyproject = cli / "pyproject.toml"
    package_init = cli / "src" / "specsfy_cli" / "__init__.py"
    changelog = cli / "CHANGELOG.md"
    for source in (pyproject, package_init, changelog, notes_file):
        if not source.is_file():
            raise ValueError(f"arquivo obrigatório ausente: {source}")

    pyproject_text = pyproject.read_text(encoding="utf-8")
    init_text = package_init.read_text(encoding="utf-8")
    pyproject_match = re.search(
        r'(?m)^version = "(\d+\.\d+\.\d+)"$', pyproject_text
    )
    init_match = re.search(
        r'(?m)^__version__ = "(\d+\.\d+\.\d+)"$', init_text
    )
    if pyproject_match is None or init_match is None:
        raise ValueError("fontes de versão do pacote não são reconhecíveis")
    if pyproject_match.group(1) != init_match.group(1):
        raise ValueError("fontes de versão atuais divergem")
    current_version = stable_version(pyproject_match.group(1))
    if next_version <= current_version:
        raise ValueError(
            f"a versão {version} deve ser maior que {pyproject_match.group(1)}"
        )

    changelog_text = changelog.read_text(encoding="utf-8")
    if changelog_text.count(UNRELEASED) != 1:
        raise ValueError("CHANGELOG.md deve conter uma única seção Unreleased")
    if re.search(rf"(?m)^## \[{re.escape(version)}\](?: |$)", changelog_text):
        raise ValueError(f"a versão {version} já existe no CHANGELOG.md")

    notes = normalized_notes(notes_file)
    release_section = (
        f"{UNRELEASED}\n\n"
        f"## [{version}] - {release_date}\n\n"
        f"{notes.rstrip()}"
    )
    updated_changelog = changelog_text.replace(UNRELEASED, release_section, 1)

    pyproject.write_text(
        replace_once(
            pyproject_text,
            r'^(version = ")\d+\.\d+\.\d+("$)',
            rf"\g<1>{version}\g<2>",
            pyproject,
        ),
        encoding="utf-8",
    )
    package_init.write_text(
        replace_once(
            init_text,
            r'^(__version__ = ")\d+\.\d+\.\d+("$)',
            rf"\g<1>{version}\g<2>",
            package_init,
        ),
        encoding="utf-8",
    )
    changelog.write_text(updated_changelog, encoding="utf-8")


def release_notes(changelog: Path, version: str) -> str:
    stable_version(version)
    text = changelog.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"(?ms)^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}\n\n"
        rf"(.*?)(?=^## \[|\Z)"
    )
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise ValueError(
            f"CHANGELOG.md deve conter exatamente uma seção para {version}"
        )
    return f"{matches[0].strip()}\n"


def verify_release_body(changelog: Path, version: str, release_json: Path) -> None:
    expected = release_notes(changelog, version)
    payload = json.loads(release_json.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("body"), str):
        raise ValueError("resposta do GitHub Release não contém body textual")
    if payload["body"] != expected:
        raise ValueError(
            "o corpo do GitHub Release diverge da seção do CHANGELOG.md"
        )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    commands = result.add_subparsers(dest="command", required=True)

    prepare_command = commands.add_parser("prepare")
    prepare_command.add_argument("--cli", type=Path, required=True)
    prepare_command.add_argument("--version", required=True)
    prepare_command.add_argument("--date", required=True)
    prepare_command.add_argument("--notes-file", type=Path, required=True)

    extract_command = commands.add_parser("extract")
    extract_command.add_argument("--changelog", type=Path, required=True)
    extract_command.add_argument("--version", required=True)
    extract_command.add_argument("--output", type=Path, required=True)

    verify_command = commands.add_parser("verify")
    verify_command.add_argument("--changelog", type=Path, required=True)
    verify_command.add_argument("--version", required=True)
    verify_command.add_argument("--release-json", type=Path, required=True)
    return result


def main() -> int:
    arguments = parser().parse_args()
    try:
        if arguments.command == "prepare":
            prepare(
                arguments.cli.resolve(),
                arguments.version,
                arguments.date,
                arguments.notes_file.resolve(),
            )
        elif arguments.command == "extract":
            notes = release_notes(
                arguments.changelog.resolve(),
                arguments.version,
            )
            arguments.output.write_text(notes, encoding="utf-8")
        else:
            verify_release_body(
                arguments.changelog.resolve(),
                arguments.version,
                arguments.release_json.resolve(),
            )
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

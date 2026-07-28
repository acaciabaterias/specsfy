from __future__ import annotations

import asyncio
import json
import os
import shlex
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .skill_lock import assert_consumer_project


@dataclass(frozen=True)
class TestCommand:
    label: str
    argv: tuple[str, ...]
    cwd: Path

    @property
    def display(self) -> str:
        return shlex.join(self.argv)


@dataclass(frozen=True)
class TestRun:
    command: TestCommand
    exit_code: int
    duration_seconds: float = 0.0
    summary_lines: tuple[str, ...] = ()


def detect_project_test_command(project: Path) -> TestCommand:
    root = project.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"projeto não encontrado: {root}")
    assert_consumer_project(root)

    artisan = root / "artisan"
    if artisan.is_file() and _uses_pest(root):
        return TestCommand(
            label="Laravel Pest",
            argv=("php", "artisan", "test"),
            cwd=root,
        )

    raise ValueError(
        "Pest não foi detectado no projeto. "
        "É esperado um projeto Laravel com artisan e pestphp/pest."
    )


def run_project_tests(
    project: Path,
    *,
    emit: Callable[[str], None] = print,
) -> TestRun:
    command = detect_project_test_command(project)
    started_at = time.monotonic()
    lines: list[str] = []
    structured_summary: tuple[str, ...] = ()
    process = subprocess.Popen(
        command.argv,
        cwd=command.cwd,
        env=_test_environment(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    if process.stdout is None:
        raise RuntimeError("não foi possível capturar a saída do Pest")
    for raw_line in process.stdout:
        line = raw_line.rstrip("\r\n")
        presented, summary = _present_output_line(line)
        lines.extend(presented)
        if summary:
            structured_summary = summary
        for presented_line in presented:
            emit(presented_line)
    exit_code = process.wait()
    return TestRun(
        command=command,
        exit_code=exit_code,
        duration_seconds=time.monotonic() - started_at,
        summary_lines=structured_summary or _summary_lines(lines),
    )


async def stream_project_tests(
    project: Path,
    *,
    emit: Callable[[str], None],
) -> TestRun:
    command = detect_project_test_command(project)
    started_at = time.monotonic()
    lines: list[str] = []
    structured_summary: tuple[str, ...] = ()
    process = await asyncio.create_subprocess_exec(
        *command.argv,
        cwd=command.cwd,
        env=_test_environment(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    if process.stdout is None:
        raise RuntimeError("não foi possível capturar a saída do Pest")
    try:
        while raw_line := await process.stdout.readline():
            line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
            presented, summary = _present_output_line(line)
            lines.extend(presented)
            if summary:
                structured_summary = summary
            for presented_line in presented:
                emit(presented_line)
        exit_code = await process.wait()
    except asyncio.CancelledError:
        process.terminate()
        await process.wait()
        raise
    return TestRun(
        command=command,
        exit_code=exit_code,
        duration_seconds=time.monotonic() - started_at,
        summary_lines=structured_summary or _summary_lines(lines),
    )


def _uses_pest(root: Path) -> bool:
    if (root / "tests/Pest.php").is_file() or (root / "vendor/bin/pest").is_file():
        return True
    composer = root / "composer.json"
    if not composer.is_file():
        return False
    try:
        payload = json.loads(composer.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"composer.json inválido em {root}: {error.msg}") from error
    if not isinstance(payload, dict):
        return False
    requirements: dict[str, object] = {}
    for section in ("require", "require-dev"):
        values = payload.get(section)
        if isinstance(values, dict):
            requirements.update(values)
    return "pestphp/pest" in requirements


def _test_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment.setdefault("NO_COLOR", "1")
    return environment


def _summary_lines(lines: list[str]) -> tuple[str, ...]:
    markers = ("tests:", "duration:", "passed", "failed", "skipped", "todo")
    candidates = [
        line.strip()
        for line in lines
        if line.strip() and any(marker in line.casefold() for marker in markers)
    ]
    return tuple(candidates[-3:])


def _present_output_line(line: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        return (line,), ()
    if not (
        isinstance(payload, dict)
        and payload.get("tool") == "pest"
        and isinstance(payload.get("result"), str)
    ):
        return (line,), ()

    total = _integer(payload.get("tests"))
    passed = _integer(payload.get("passed"))
    errors = _integer(payload.get("errors"))
    assertions = _integer(payload.get("assertions"))
    duration_ms = _integer(payload.get("duration_ms"))
    summary = (
        f"Tests: {total} total · {passed} passed · {errors} errors",
        f"Assertions: {assertions}",
        f"Duration: {duration_ms / 1000:.2f}s",
    )
    presented: list[str] = []
    details = payload.get("error_details")
    if isinstance(details, list):
        for detail in details:
            if not isinstance(detail, dict):
                continue
            test = str(detail.get("test", "Teste desconhecido"))
            file = str(detail.get("file", "arquivo desconhecido"))
            line_number = detail.get("line", "?")
            message = str(detail.get("message", "Erro sem mensagem"))
            presented.extend(
                (
                    f"FAIL  {test}",
                    f"      {file}:{line_number}",
                    f"      {message}",
                    "",
                )
            )
    if not presented:
        presented.append(summary[0])
    return tuple(presented), summary


def _integer(value: object) -> int:
    return value if isinstance(value, int) else 0

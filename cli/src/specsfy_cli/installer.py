from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .skill_lock import (
    assert_consumer_project,
    ensure_skills_lock,
    installed_skill_names,
)


MONOREPO_REPOSITORY = "https://github.com/promovaweb/specsfy.git"
BASE_DIRECTORY = "skills"
SPECIALISTS_DIRECTORY = "specialists"
BASE_SKILLS = (
    "specsfy-base-backlog",
    "specsfy-base-interview",
    "specsfy-base-specify",
    "specsfy-base-validate",
    "specsfy-base-tasks",
    "specsfy-base-tdd-bdd",
    "specsfy-base-implement",
    "specsfy-base-update-spec",
    "specsfy-base-progress",
)
AUXILIARY_SKILLS = (
    "specsfy-aux-stack",
    "specsfy-aux-rules",
    "specsfy-aux-database",
)
DOCUMENTATION_SKILLS = ("specsfy-documentator",)
FRAMEWORK_SKILLS = (
    "specsfy-setup",
    *AUXILIARY_SKILLS,
    *DOCUMENTATION_SKILLS,
    *BASE_SKILLS,
)
RENAMED_BASE_SKILLS = {
    "specsfy-base-discuss": "specsfy-base-interview",
}
FRAMEWORK_START = "<!-- specsfy:framework:start -->"
FRAMEWORK_END = "<!-- specsfy:framework:end -->"
SPEC_PATH_TOKEN = "{{SPECSFY_SPEC_PATH}}"
CONSUMER_SPEC_PATH = ".specsfy/Spec.md"
CONSUMER_TEMPLATE_PATH = ".specsfy/templates/Spec.md"
CONSUMER_EXAMPLE_PATH = ".specsfy/examples/Spec.md"


class SkillInstaller:
    def __init__(self, project: Path, *, force: bool = False) -> None:
        self.project = project.expanduser().resolve()
        self.force = force
        assert_consumer_project(self.project)
        ensure_skills_lock(self.project)

    def install_base(self) -> list[Path]:
        return self.install_base_selection(list(FRAMEWORK_SKILLS))

    def install_base_selection(self, names: list[str]) -> list[Path]:
        invalid = sorted(set(names) - set(FRAMEWORK_SKILLS))
        if invalid:
            raise ValueError(f"skill do framework desconhecida: {', '.join(invalid)}")
        with _RepositoryCheckout(
            MONOREPO_REPOSITORY,
            directory=BASE_DIRECTORY,
        ) as checkout:
            return self.install_base_from_checkout(checkout, names=names)

    def install_base_from_checkout(
        self,
        checkout: Path,
        *,
        names: list[str] | tuple[str, ...] | None = None,
    ) -> list[Path]:
        selected = tuple(names) if names is not None else BASE_SKILLS
        self._validate_skill_installation(checkout, selected)
        legacy_targets = self._legacy_base_targets()
        changed = self.install_framework_from_checkout(checkout)
        changed.extend(
            self.install_from_checkout(checkout, selected, source_name="base")
        )
        changed.extend(self._remove_legacy_base(legacy_targets))
        return changed

    def _validate_skill_installation(
        self,
        checkout: Path,
        names: tuple[str, ...] | list[str],
    ) -> None:
        lock = self._read_lock()
        destination = self.project / ".agents" / "skills"
        for name in names:
            source = checkout / name
            if not (source / "SKILL.md").is_file():
                raise ValueError(f"skill inválida ou ausente na origem: {name}")
            target = destination / name
            if not target.exists():
                continue
            source_digest = _skill_digest(source)
            target_digest = _skill_digest(target)
            if source_digest == target_digest:
                continue
            recorded_digest = lock["skills"].get(name, {}).get("content_sha256")
            if not self.force and recorded_digest != target_digest:
                raise FileExistsError(
                    f"{target} possui alterações locais; preserve-as ou use --force "
                    "para substituir"
                )

    def _legacy_base_targets(self) -> list[tuple[str, Path]]:
        lock = self._read_lock()
        targets: list[tuple[str, Path]] = []
        for old_name in RENAMED_BASE_SKILLS:
            target = self.project / ".agents" / "skills" / old_name
            if not target.exists():
                continue
            recorded_digest = lock["skills"].get(old_name, {}).get("content_sha256")
            if not self.force and recorded_digest != _skill_digest(target):
                raise FileExistsError(
                    f"{target} foi renomeada e possui alterações locais; preserve-as "
                    "ou use --force para removê-la após instalar a substituta"
                )
            targets.append((old_name, target))
        return targets

    def _remove_legacy_base(
        self,
        targets: list[tuple[str, Path]],
    ) -> list[Path]:
        if not targets:
            return []
        lock = self._read_lock()
        removed: list[Path] = []
        for name, target in targets:
            if target.exists():
                shutil.rmtree(target)
                removed.append(target)
            lock["skills"].pop(name, None)
        self._write_lock(lock)
        return removed

    def install_framework_from_checkout(self, checkout: Path) -> list[Path]:
        source_spec = checkout / "Spec.md"
        source_template = checkout / "templates" / "Spec.md"
        source_example = checkout / "examples" / "Spec.md"
        source_agents = checkout / "AGENTS.md"
        for structural_file in (source_spec, source_template, source_example):
            if not structural_file.is_file():
                raise ValueError(
                    f"arquivo estrutural ausente na origem: {structural_file}"
                )
        if not source_agents.is_file():
            raise ValueError(f"arquivo estrutural ausente na origem: {source_agents}")

        spec_content = source_spec.read_text(encoding="utf-8")
        template_content = source_template.read_text(encoding="utf-8")
        example_content = source_example.read_text(encoding="utf-8")
        agents_block = _extract_source_block(source_agents).replace(
            SPEC_PATH_TOKEN,
            CONSUMER_SPEC_PATH,
        )
        claude_block = (
            f"{FRAMEWORK_START}\n@{CONSUMER_SPEC_PATH}\n{FRAMEWORK_END}"
        )
        lock = self._read_lock()
        previous = lock.get("framework", {})
        spec_target = self.project / CONSUMER_SPEC_PATH
        template_target = self.project / CONSUMER_TEMPLATE_PATH
        example_target = self.project / CONSUMER_EXAMPLE_PATH
        agents_target = self.project / "AGENTS.md"
        claude_target = self.project / "CLAUDE.md"

        plans = (
            (
                spec_target,
                _plan_managed_file(
                    spec_target,
                    spec_content,
                    recorded_digest=previous.get("spec_sha256"),
                    force=self.force,
                ),
            ),
            (
                template_target,
                _plan_managed_file(
                    template_target,
                    template_content,
                    recorded_digest=previous.get("template_sha256"),
                    force=self.force,
                ),
            ),
            (
                example_target,
                _plan_managed_file(
                    example_target,
                    example_content,
                    recorded_digest=previous.get("example_sha256"),
                    force=self.force,
                ),
            ),
            (
                agents_target,
                _plan_managed_block(
                    agents_target,
                    agents_block,
                    recorded_digest=previous.get("agents_sha256"),
                    force=self.force,
                ),
            ),
            (
                claude_target,
                _plan_managed_block(
                    claude_target,
                    claude_block,
                    recorded_digest=previous.get("claude_sha256"),
                    force=self.force,
                ),
            ),
        )
        changed: list[Path] = []
        for target, planned_content in plans:
            if planned_content is None:
                continue
            _write_text_atomic(target, planned_content)
            changed.append(target)

        framework_record = {
            "source": "base",
            "spec_sha256": _content_digest(spec_content),
            "template_sha256": _content_digest(template_content),
            "example_sha256": _content_digest(example_content),
            "agents_sha256": _content_digest(agents_block),
            "claude_sha256": _content_digest(claude_block),
        }
        if previous != framework_record:
            lock["framework"] = framework_record
            self._write_lock(lock)
        return changed

    def install_specialists(self, names: list[str]) -> list[Path]:
        return self.install_from_repository(
            MONOREPO_REPOSITORY,
            names,
            source_name="specialists",
            directory=SPECIALISTS_DIRECTORY,
        )

    def update_all(self) -> list[Path]:
        installed = installed_skill_names(self.project)
        base = sorted(set(FRAMEWORK_SKILLS) & installed)
        specialists = sorted(
            name
            for name in installed
            if name.startswith("specsfy-specialist-")
        )
        changed: list[Path] = []
        if base:
            changed.extend(self.install_base_selection(base))
        if specialists:
            changed.extend(self.install_specialists(specialists))
        return changed

    def install_from_repository(
        self,
        repository: str,
        names: tuple[str, ...] | list[str],
        *,
        source_name: str,
        directory: str | None = None,
    ) -> list[Path]:
        with _RepositoryCheckout(repository, directory=directory) as checkout:
            return self.install_from_checkout(
                checkout,
                names,
                source_name=source_name,
            )

    def install_from_checkout(
        self,
        checkout: Path,
        names: tuple[str, ...] | list[str],
        *,
        source_name: str,
    ) -> list[Path]:
        destination = self.project / ".agents" / "skills"
        destination.mkdir(parents=True, exist_ok=True)
        lock = self._read_lock()
        operations: list[tuple[str, Path, Path, str]] = []
        for name in names:
            source = checkout / name
            if not (source / "SKILL.md").is_file():
                raise ValueError(f"skill inválida ou ausente na origem: {name}")
            target = destination / name
            source_digest = _skill_digest(source)
            if not target.exists():
                operations.append(("install", source, target, source_digest))
                continue
            target_digest = _skill_digest(target)
            if target_digest == source_digest:
                operations.append(("current", source, target, source_digest))
                continue
            recorded_digest = lock["skills"].get(name, {}).get("content_sha256")
            if not self.force and recorded_digest != target_digest:
                raise FileExistsError(
                    f"{target} possui alterações locais; preserve-as ou use --force "
                    "para substituir"
                )
            operations.append(("replace", source, target, source_digest))

        installed: list[Path] = []
        lock_changed = False
        changed_names = [
            target.name
            for action, _, target, _ in operations
            if action != "current"
        ]
        if changed_names:
            _install_with_skills_cli(
                source=checkout,
                names=changed_names,
                project=self.project,
            )
        for action, source, target, source_digest in operations:
            name = target.name
            previous = lock["skills"].get(name, {})
            if action != "current":
                if not target.is_dir() or _skill_digest(target) != source_digest:
                    raise RuntimeError(
                        f"skills CLI não materializou {name} corretamente em {target}"
                    )
                installed.append(target)
            if (
                previous.get("source") == source_name
                and previous.get("content_sha256") == source_digest
            ):
                continue
            now = datetime.now(timezone.utc).isoformat()
            record = {
                "source": source_name,
                "installed_at": previous.get("installed_at", now),
                "content_sha256": source_digest,
            }
            if previous and action != "current":
                record["updated_at"] = now
            lock["skills"][name] = record
            lock_changed = True
        if lock_changed:
            self._write_lock(lock)
        return installed

    def remove(self, names: list[str]) -> list[Path]:
        lock = self._read_lock()
        official_names = installed_skill_names(self.project)
        targets: list[tuple[str, Path]] = []
        for name in names:
            if not (
                name.startswith("specsfy-base-")
                or name.startswith("specsfy-aux-")
                or name == "specsfy-setup"
                or name in DOCUMENTATION_SKILLS
                or name.startswith("specsfy-specialist-")
            ):
                raise ValueError(f"nome de skill Specsfy inválido: {name}")
            target = self.project / ".agents" / "skills" / name
            if target.exists() and not self.force:
                recorded_digest = lock["skills"].get(name, {}).get("content_sha256")
                if recorded_digest != _skill_digest(target):
                    raise FileExistsError(
                        f"{target} possui alterações locais; preserve-as ou use "
                        "--force para remover"
                    )
            targets.append((name, target))
        removed = []
        lock_changed = False
        registered_names = [
            name
            for name, target in targets
            if target.exists() or name in official_names
        ]
        if registered_names:
            _remove_with_skills_cli(names=registered_names, project=self.project)
        for name, target in targets:
            if target.exists():
                shutil.rmtree(target)
                removed.append(target)
            if lock["skills"].pop(name, None) is not None:
                lock_changed = True
        if lock_changed:
            self._write_lock(lock)
        return removed

    def _read_lock(self) -> dict:
        path = self.project / ".specsfy" / "skills-lock.json"
        if not path.is_file():
            return {"schema_version": 1, "skills": {}}
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"lock inválido: {path}")
        payload.setdefault("skills", {})
        return payload

    def _write_lock(self, payload: dict) -> None:
        directory = self.project / ".specsfy"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "skills-lock.json"
        temporary = directory / ".skills-lock.json.tmp"
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)


class _RepositoryCheckout:
    def __init__(self, repository: str, *, directory: str | None = None) -> None:
        self.repository = repository
        self.directory = directory
        self._temporary: tempfile.TemporaryDirectory | None = None

    def __enter__(self) -> Path:
        self._temporary = tempfile.TemporaryDirectory(prefix="specsfy-install-")
        checkout = Path(self._temporary.name) / "checkout"
        result = subprocess.run(
            ["git", "clone", "--depth", "1", self.repository, str(checkout)],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            self._temporary.cleanup()
            self._temporary = None
            raise RuntimeError(result.stderr.strip() or "falha ao baixar catálogo")
        source = checkout / self.directory if self.directory else checkout
        if not source.is_dir():
            self._temporary.cleanup()
            self._temporary = None
            raise RuntimeError(f"diretório ausente no monorepo: {self.directory}")
        return source

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._temporary is not None:
            self._temporary.cleanup()


def _extract_source_block(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    block = _managed_block(content, path)
    if block is None:
        raise ValueError(
            f"bloco {FRAMEWORK_START} ausente no arquivo estrutural: {path}"
        )
    if SPEC_PATH_TOKEN not in block:
        raise ValueError(f"token {SPEC_PATH_TOKEN} ausente no bloco de {path}")
    return block


def _plan_managed_file(
    path: Path,
    expected: str,
    *,
    recorded_digest: str | None,
    force: bool,
) -> str | None:
    if not path.exists():
        return expected
    if not path.is_file():
        raise FileExistsError(f"{path} existe e não é um arquivo")
    current = path.read_text(encoding="utf-8")
    if current == expected:
        return None
    if force or recorded_digest == _content_digest(current):
        return expected
    raise FileExistsError(
        f"{path} possui alterações locais; preserve-as ou use --force para substituir"
    )


def _plan_managed_block(
    path: Path,
    expected_block: str,
    *,
    recorded_digest: str | None,
    force: bool,
) -> str | None:
    if path.exists() and not path.is_file():
        raise FileExistsError(f"{path} existe e não é um arquivo")
    content = path.read_text(encoding="utf-8") if path.is_file() else ""
    current_block = _managed_block(content, path)
    if current_block is None:
        return _append_block(content, expected_block)
    if current_block == expected_block:
        return None
    if not force and recorded_digest != _content_digest(current_block):
        raise FileExistsError(
            f"{path} possui alterações locais no bloco Specsfy; "
            "preserve-as ou use --force para substituir somente o bloco"
        )
    start = content.index(FRAMEWORK_START)
    end = content.index(FRAMEWORK_END, start) + len(FRAMEWORK_END)
    return content[:start] + expected_block + content[end:]


def _managed_block(content: str, path: Path) -> str | None:
    starts = content.count(FRAMEWORK_START)
    ends = content.count(FRAMEWORK_END)
    if starts == ends == 0:
        return None
    if starts != 1 or ends != 1:
        raise ValueError(f"bloco Specsfy malformado em {path}")
    start = content.index(FRAMEWORK_START)
    end = content.index(FRAMEWORK_END, start) + len(FRAMEWORK_END)
    return content[start:end]


def _append_block(content: str, block: str) -> str:
    if not content:
        return block + "\n"
    if content.endswith("\n\n"):
        separator = ""
    elif content.endswith("\n"):
        separator = "\n"
    else:
        separator = "\n\n"
    return content + separator + block + "\n"


def _write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.parent / f".{path.name}.specsfy.tmp"
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def _content_digest(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


def _skills_command() -> list[str]:
    override = os.environ.get("SPECSFY_SKILLS_CLI")
    if override:
        executable = Path(override).expanduser().resolve()
        if not executable.is_file() or not os.access(executable, os.X_OK):
            raise RuntimeError(f"SPECSFY_SKILLS_CLI não é executável: {executable}")
        return [str(executable)]
    installed = shutil.which("skills")
    if installed:
        return [installed]
    npx = shutil.which("npx")
    if npx:
        return [npx, "--yes", "skills"]
    raise RuntimeError(
        "skills CLI não encontrado; instale https://github.com/vercel-labs/skills "
        "ou disponibilize npx no PATH"
    )


def _install_with_skills_cli(
    *,
    source: Path,
    names: list[str],
    project: Path,
) -> None:
    command = [
        *_skills_command(),
        "add",
        str(source.resolve()),
    ]
    for name in names:
        command.extend(("--skill", name))
    command.extend(("--agent", "universal", "--copy", "-y", "--full-depth"))
    result = subprocess.run(
        command,
        cwd=project,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(
            "skills CLI falhou ao instalar "
            f"{', '.join(names)}: {detail or f'exit {result.returncode}'}"
        )


def _remove_with_skills_cli(*, names: list[str], project: Path) -> None:
    command = [
        *_skills_command(),
        "remove",
        *names,
        "--agent",
        "universal",
        "-y",
    ]
    result = subprocess.run(
        command,
        cwd=project,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(
            "skills CLI falhou ao remover "
            f"{', '.join(names)}: {detail or f'exit {result.returncode}'}"
        )


def _skill_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for entry in sorted(path.rglob("*")):
        relative_path = entry.relative_to(path)
        if _is_generated(relative_path):
            continue
        digest.update(relative_path.as_posix().encode())
        digest.update(b"\0")
        if entry.is_symlink():
            digest.update(b"link:")
            digest.update(entry.readlink().as_posix().encode())
        elif entry.is_file():
            digest.update(f"{entry.stat().st_mode & 0o777:o}".encode())
            digest.update(b":")
            digest.update(entry.read_bytes())
        else:
            digest.update(b"dir")
        digest.update(b"\0")
    return digest.hexdigest()


def _is_generated(path: Path) -> bool:
    return (
        "__pycache__" in path.parts
        or path.name == ".DS_Store"
        or path.suffix in {".pyc", ".pyo"}
    )

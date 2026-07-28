from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


DEFAULT_WATCH_INTERVAL = 0.75


@dataclass(frozen=True)
class ProjectConfig:
    project: Path
    watch_interval: float = DEFAULT_WATCH_INTERVAL

    def to_dict(self) -> dict:
        value = asdict(self)
        value["project"] = str(self.project)
        return value


def load_config(project: Path) -> ProjectConfig:
    root = project.expanduser().resolve()
    payload = _read_payload(root)
    interval = float(payload.get("watch_interval", DEFAULT_WATCH_INTERVAL))
    _validate_interval(interval)
    return ProjectConfig(project=root, watch_interval=interval)


def update_config(project: Path, *, watch_interval: float) -> ProjectConfig:
    root = project.expanduser().resolve()
    _validate_interval(watch_interval)
    payload = _read_payload(root)
    payload["schema_version"] = 1
    payload["watch_interval"] = watch_interval
    directory = root / ".specsfy"
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "config.json"
    temporary = directory / ".config.json.tmp"
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(target)
    return ProjectConfig(project=root, watch_interval=watch_interval)


def _read_payload(project: Path) -> dict[str, Any]:
    path = project / ".specsfy/config.json"
    if not path.is_file():
        return {"schema_version": 1}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"configuração inválida: {path}")
    if payload.get("schema_version", 1) != 1:
        raise ValueError("versão de configuração não suportada")
    return payload


def _validate_interval(interval: float) -> None:
    if not math.isfinite(interval) or interval <= 0:
        raise ValueError("watch interval deve ser um número finito maior que zero")

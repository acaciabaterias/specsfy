from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

from . import __version__
from .github import api_headers


TAGS_API_URL = "https://api.github.com/repos/promovaweb/specsfy/tags?per_page=100"
UV_TOOL_NAME = "specsfy-cli"
SEMANTIC_TAG = re.compile(r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40,64}$")
DEFAULT_CHECK_INTERVAL_SECONDS = 86400
NETWORK_TIMEOUT_SECONDS = 4


@dataclass(frozen=True)
class UpdateInfo:
    current_version: str
    latest_version: str
    tag: str
    commit_sha: str


def global_config_path(*, home: Path | None = None) -> Path:
    root = home if home is not None else Path.home()
    return root / ".specsfy" / "cli.json"


def ensure_global_config(path: Path | None = None) -> dict[str, Any]:
    target = path or global_config_path()
    if target.is_file():
        payload = _read_global_config(target)
    else:
        payload = {}
    changed = False
    if payload.get("schema_version") != 1:
        payload["schema_version"] = 1
        changed = True
    settings = payload.setdefault("settings", {})
    if not isinstance(settings, dict):
        raise ValueError(f"settings inválido em {target}")
    defaults = {
        "check_updates_on_startup": True,
        "check_interval_seconds": DEFAULT_CHECK_INTERVAL_SECONDS,
    }
    for key, value in defaults.items():
        if key not in settings:
            settings[key] = value
            changed = True
    cache = payload.setdefault("cache", {})
    if not isinstance(cache, dict):
        raise ValueError(f"cache inválido em {target}")
    if changed or not target.is_file():
        _write_global_config(target, payload)
    else:
        target.chmod(0o600)
    return payload


def check_for_update(
    current_version: str = __version__,
    *,
    cache_path: Path | None = None,
    now: float | None = None,
    opener=None,
    force: bool = False,
) -> UpdateInfo | None:
    target = cache_path or global_config_path()
    payload = ensure_global_config(target)
    settings = payload["settings"]
    cache = payload["cache"]
    if not settings.get("check_updates_on_startup", True) and not force:
        return None

    checked_at = cache.get("last_checked_at")
    interval = settings.get(
        "check_interval_seconds",
        DEFAULT_CHECK_INTERVAL_SECONDS,
    )
    timestamp = time.time() if now is None else now
    if (
        not force
        and isinstance(checked_at, (int, float))
        and isinstance(interval, (int, float))
        and interval > 0
        and timestamp - checked_at < interval
    ):
        return _cached_update(current_version, cache)

    open_url = opener or urllib.request.urlopen
    headers = api_headers(f"specsfy-cli/{current_version}")
    etag = cache.get("etag")
    if isinstance(etag, str) and etag:
        headers["If-None-Match"] = etag
    request = urllib.request.Request(TAGS_API_URL, headers=headers)
    try:
        with open_url(request, timeout=NETWORK_TIMEOUT_SECONDS) as response:
            tags = json.loads(response.read().decode("utf-8"))
            response_etag = response.headers.get("ETag")
    except urllib.error.HTTPError as error:
        if error.code == 304:
            cache["last_checked_at"] = timestamp
            cache.pop("last_error", None)
            _write_global_config(target, payload)
            return _cached_update(current_version, cache)
        return _record_check_error(
            current_version,
            target,
            payload,
            timestamp,
            error,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return _record_check_error(
            current_version,
            target,
            payload,
            timestamp,
            error,
        )

    try:
        latest = _latest_semantic_tag(tags)
    except ValueError as error:
        return _record_check_error(
            current_version,
            target,
            payload,
            timestamp,
            error,
        )
    cache["last_checked_at"] = timestamp
    cache.pop("last_error", None)
    if isinstance(response_etag, str):
        cache["etag"] = response_etag
    if latest is None:
        for key in ("latest_version", "latest_tag", "latest_commit"):
            cache.pop(key, None)
    else:
        version, tag, commit_sha = latest
        cache.update(
            {
                "latest_version": version,
                "latest_tag": tag,
                "latest_commit": commit_sha,
            }
        )
    _write_global_config(target, payload)
    return _cached_update(current_version, cache)


def uv_upgrade_command(uv_executable: str = "uv") -> list[str]:
    return [uv_executable, "tool", "upgrade", UV_TOOL_NAME]


def upgrade_with_uv(
    *,
    runner=subprocess.run,
    uv_executable: str | None = None,
) -> None:
    executable = uv_executable or shutil.which("uv")
    if executable is None:
        raise RuntimeError(
            "uv não foi encontrado no PATH; instale-o e execute "
            "`uv tool upgrade specsfy-cli`"
        )
    runner(uv_upgrade_command(executable), check=True)


def offer_startup_update(
    *,
    checker=check_for_update,
    upgrader=upgrade_with_uv,
    input_fn=input,
    output: TextIO = sys.stdout,
    interactive: bool | None = None,
) -> bool:
    is_interactive = (
        sys.stdin.isatty() and sys.stdout.isatty()
        if interactive is None
        else interactive
    )
    if not is_interactive:
        return False
    try:
        update = checker()
    except (ValueError, OSError) as error:
        print(f"Aviso: não foi possível verificar atualizações: {error}", file=output)
        return False
    if update is None:
        return False

    print(
        f"Uma nova versão do Specsfy CLI está disponível: "
        f"{update.current_version} → {update.latest_version}.",
        file=output,
    )
    answer = input_fn("Deseja atualizar agora? [s/N] ").strip().casefold()
    if answer not in {"s", "sim", "y", "yes"}:
        print("Atualização adiada. Abrindo a aplicação normalmente.", file=output)
        return False
    try:
        upgrader()
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        print(f"Falha ao atualizar: {error}. Abrindo normalmente.", file=output)
        return False
    print(
        f"O uv atualizou o ambiente do Specsfy CLI para {update.latest_version}. "
        "O CLI será fechado; abra-o novamente para usar a nova versão.",
        file=output,
    )
    return True


def _read_global_config(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"configuração global inválida em {path}: {error.msg}") from error
    if not isinstance(payload, dict):
        raise ValueError(f"configuração global inválida em {path}")
    return payload


def _write_global_config(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".cli-",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(0o600)
        os.replace(temporary, path)
        path.chmod(0o600)
    finally:
        temporary.unlink(missing_ok=True)


def _latest_semantic_tag(tags: object) -> tuple[str, str, str] | None:
    if not isinstance(tags, list):
        raise ValueError("resposta de tags inválida")
    candidates: list[tuple[tuple[int, int, int], str, str]] = []
    for item in tags:
        if not isinstance(item, dict):
            continue
        tag = item.get("name")
        commit = item.get("commit")
        if not isinstance(tag, str) or not isinstance(commit, dict):
            continue
        match = SEMANTIC_TAG.fullmatch(tag)
        commit_sha = commit.get("sha")
        if (
            match is None
            or not isinstance(commit_sha, str)
            or COMMIT_SHA.fullmatch(commit_sha) is None
        ):
            continue
        version_tuple = tuple(
            int(match.group(name)) for name in ("major", "minor", "patch")
        )
        candidates.append((version_tuple, tag, commit_sha))
    if not candidates:
        return None
    version_tuple, tag, commit_sha = max(candidates)
    version = ".".join(str(part) for part in version_tuple)
    return version, tag, commit_sha


def _version_tuple(version: str) -> tuple[int, int, int]:
    match = SEMANTIC_TAG.fullmatch(version)
    if match is None:
        raise ValueError(f"versão semântica inválida: {version}")
    return tuple(int(match.group(name)) for name in ("major", "minor", "patch"))


def _cached_update(
    current_version: str,
    cache: dict[str, Any],
) -> UpdateInfo | None:
    latest_version = cache.get("latest_version")
    tag = cache.get("latest_tag")
    commit_sha = cache.get("latest_commit")
    if not all(isinstance(value, str) for value in (latest_version, tag, commit_sha)):
        return None
    if COMMIT_SHA.fullmatch(commit_sha) is None:
        return None
    tag_match = SEMANTIC_TAG.fullmatch(tag)
    if tag_match is None or _version_tuple(tag) != _version_tuple(latest_version):
        return None
    if _version_tuple(latest_version) <= _version_tuple(current_version):
        return None
    return UpdateInfo(
        current_version=current_version,
        latest_version=latest_version,
        tag=tag,
        commit_sha=commit_sha,
    )


def _record_check_error(
    current_version: str,
    path: Path,
    payload: dict[str, Any],
    timestamp: float,
    error: Exception,
) -> UpdateInfo | None:
    cache = payload["cache"]
    cache["last_checked_at"] = timestamp
    cache["last_error"] = str(error)
    _write_global_config(path, payload)
    return _cached_update(current_version, cache)

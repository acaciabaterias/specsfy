from __future__ import annotations

import os
import shutil
import subprocess


def api_headers(
    user_agent: str,
    *,
    accept: str = "application/vnd.github+json",
) -> dict[str, str]:
    headers = {
        "Accept": accept,
        "User-Agent": user_agent,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = _token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _token() -> str | None:
    for variable in ("GH_TOKEN", "GITHUB_TOKEN"):
        token = os.environ.get(variable, "").strip()
        if token:
            return token

    executable = shutil.which("gh")
    if executable is None:
        return None
    result = subprocess.run(
        [executable, "auth", "token"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None

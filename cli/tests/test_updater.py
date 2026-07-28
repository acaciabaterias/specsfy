from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from specsfy_cli.updater import (
    UpdateInfo,
    check_for_update,
    ensure_global_config,
    offer_startup_update,
    upgrade_with_uv,
    uv_upgrade_command,
)


class FakeResponse:
    def __init__(
        self,
        payload: bytes,
        *,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.payload = payload
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def read(self) -> bytes:
        return self.payload


class UpdaterTests(unittest.TestCase):
    def test_creates_global_cache_with_private_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".specsfy/cli.json"

            payload = ensure_global_config(path)

            self.assertTrue(path.is_file())
            self.assertEqual(1, payload["schema_version"])
            self.assertTrue(payload["settings"]["check_updates_on_startup"])
            self.assertEqual(86400, payload["settings"]["check_interval_seconds"])
            self.assertEqual(0o600, path.stat().st_mode & 0o777)

    def test_selects_latest_stable_tag_and_caches_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".specsfy/cli.json"
            calls = []

            def open_url(request, *, timeout):
                calls.append((request, timeout))
                return FakeResponse(
                    json.dumps(
                        [
                            {"name": "v0.7.0", "commit": {"sha": "7" * 40}},
                            {"name": "invalid", "commit": {"sha": "1" * 40}},
                            {"name": "v0.8.0", "commit": {"sha": "8" * 40}},
                            {"name": "v0.9.0-beta.1", "commit": {"sha": "9" * 40}},
                        ]
                    ).encode(),
                    headers={"ETag": '"tags-v1"'},
                )

            with patch.dict("os.environ", {"GH_TOKEN": "private-token"}, clear=True):
                update = check_for_update(
                    "0.6.0",
                    cache_path=path,
                    now=1000,
                    opener=open_url,
                )

            self.assertEqual("0.8.0", update.latest_version)
            self.assertEqual("v0.8.0", update.tag)
            self.assertEqual("8" * 40, update.commit_sha)
            self.assertEqual(1, len(calls))
            self.assertEqual(
                "Bearer private-token",
                calls[0][0].get_header("Authorization"),
            )
            cache = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("v0.8.0", cache["cache"]["latest_tag"])
            self.assertEqual('"tags-v1"', cache["cache"]["etag"])

    def test_reuses_recent_cache_without_network(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".specsfy/cli.json"
            path.parent.mkdir()
            path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "settings": {
                            "check_updates_on_startup": True,
                            "check_interval_seconds": 86400,
                            "custom": "preservar",
                        },
                        "cache": {
                            "last_checked_at": 900,
                            "latest_version": "0.7.0",
                            "latest_tag": "v0.7.0",
                            "latest_commit": "7" * 40,
                        },
                    }
                ),
                encoding="utf-8",
            )
            opener = Mock(side_effect=AssertionError("rede não deveria ser usada"))

            update = check_for_update(
                "0.6.0",
                cache_path=path,
                now=1000,
                opener=opener,
            )

            self.assertEqual("v0.7.0", update.tag)
            opener.assert_not_called()
            cache = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("preservar", cache["settings"]["custom"])

    def test_global_setting_can_disable_startup_network_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".specsfy/cli.json"
            payload = ensure_global_config(path)
            payload["settings"]["check_updates_on_startup"] = False
            path.write_text(json.dumps(payload), encoding="utf-8")
            opener = Mock(side_effect=AssertionError("rede não deveria ser usada"))

            update = check_for_update(
                "0.6.0",
                cache_path=path,
                opener=opener,
            )

            self.assertIsNone(update)
            opener.assert_not_called()

    def test_delegates_the_upgrade_to_the_uv_tool_environment(self) -> None:
        runner = Mock()
        runner.return_value.returncode = 0

        upgrade_with_uv(runner=runner, uv_executable="/opt/bin/uv")

        runner.assert_called_once_with(
            ["/opt/bin/uv", "tool", "upgrade", "specsfy-cli"],
            check=True,
        )

    def test_builds_the_public_uv_upgrade_command(self) -> None:
        self.assertEqual(
            ["/usr/local/bin/uv", "tool", "upgrade", "specsfy-cli"],
            uv_upgrade_command("/usr/local/bin/uv"),
        )

    def test_requires_uv_to_manage_the_installed_tool(self) -> None:
        with (
            patch("specsfy_cli.updater.shutil.which", return_value=None),
            self.assertRaisesRegex(RuntimeError, "uv não foi encontrado"),
        ):
            upgrade_with_uv()

    def test_startup_offer_updates_and_requests_application_exit(self) -> None:
        info = UpdateInfo("0.6.0", "0.7.0", "v0.7.0", "a" * 40)
        checker = Mock(return_value=info)
        upgrader = Mock()
        output = io.StringIO()

        should_exit = offer_startup_update(
            checker=checker,
            upgrader=upgrader,
            input_fn=lambda _prompt: "sim",
            output=output,
            interactive=True,
        )

        self.assertTrue(should_exit)
        upgrader.assert_called_once_with()
        self.assertIn("0.7.0", output.getvalue())
        self.assertIn("uv", output.getvalue())

    def test_startup_offer_declined_opens_application_normally(self) -> None:
        info = UpdateInfo("0.6.0", "0.7.0", "v0.7.0", "a" * 40)
        upgrader = Mock()

        should_exit = offer_startup_update(
            checker=Mock(return_value=info),
            upgrader=upgrader,
            input_fn=lambda _prompt: "não",
            output=io.StringIO(),
            interactive=True,
        )

        self.assertFalse(should_exit)
        upgrader.assert_not_called()

    def test_startup_offer_continues_when_update_check_fails(self) -> None:
        output = io.StringIO()

        should_exit = offer_startup_update(
            checker=Mock(side_effect=OSError("offline")),
            upgrader=Mock(),
            output=output,
            interactive=True,
        )

        self.assertFalse(should_exit)
        self.assertIn("não foi possível verificar", output.getvalue())


if __name__ == "__main__":
    unittest.main()

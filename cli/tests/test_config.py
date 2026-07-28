from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from specsfy_cli.config import load_config, update_config


class ConfigurationTests(unittest.TestCase):
    def test_updates_watch_interval_atomically_and_preserves_unknown_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            path = project / ".specsfy/config.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "watch_interval": 1.0,
                        "user_preference": "preservar",
                    }
                ),
                encoding="utf-8",
            )

            updated = update_config(project, watch_interval=0.5)

            self.assertEqual(0.5, updated.watch_interval)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("preservar", payload["user_preference"])
            self.assertEqual(0.5, load_config(project).watch_interval)

    def test_rejects_non_positive_watch_interval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "maior que zero"):
                update_config(Path(directory), watch_interval=0)
            with self.assertRaisesRegex(ValueError, "finito"):
                update_config(Path(directory), watch_interval=float("nan"))

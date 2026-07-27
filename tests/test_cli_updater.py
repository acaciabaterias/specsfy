from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cli" / "src"))

from specsfy_cli.updater import global_config_path, uv_upgrade_command


class CliUpdaterContractTests(unittest.TestCase):
    def test_global_cache_uses_the_specsfy_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)

            self.assertEqual(
                home / ".specsfy/cli.json",
                global_config_path(home=home),
            )

    def test_cli_upgrade_is_managed_by_uv_tool(self) -> None:
        command = uv_upgrade_command("/usr/local/bin/uv")

        self.assertEqual(
            ["/usr/local/bin/uv", "tool", "upgrade", "specsfy-cli"],
            command,
        )


if __name__ == "__main__":
    unittest.main()

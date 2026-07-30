import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPDATER = (ROOT / "cli/src/updater.ts").read_text(encoding="utf-8")


class CliUpdaterContractTests(unittest.TestCase):
    def test_global_cache_uses_the_specsfy_path(self) -> None:
        self.assertIn('join(home, ".specsfy", "cli.json")', UPDATER)

    def test_cli_upgrade_is_managed_by_npm(self) -> None:
        self.assertIn('NPM_PACKAGE_NAME = "@promovaweb/specsfy"', UPDATER)
        self.assertIn('["install", "--global",', UPDATER)


if __name__ == "__main__":
    unittest.main()

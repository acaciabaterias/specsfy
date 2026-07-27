from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cli" / "src"))

from specsfy_cli.testing import detect_project_test_command


class CliTestRunnerContractTests(unittest.TestCase):
    def test_detects_the_laravel_pest_command_in_a_consumer_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "artisan").write_text("#!/usr/bin/env php\n", encoding="utf-8")
            (project / "composer.json").write_text(
                json.dumps({"require-dev": {"pestphp/pest": "^4.7"}}),
                encoding="utf-8",
            )

            command = detect_project_test_command(project)

            self.assertEqual(("php", "artisan", "test"), command.argv)
            self.assertEqual(project.resolve(), command.cwd)


if __name__ == "__main__":
    unittest.main()

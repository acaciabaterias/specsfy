from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from specsfy_cli.testing import (
    TestRun,
    detect_project_test_command,
    run_project_tests,
)


class ProjectTestingTests(unittest.TestCase):
    def test_detects_laravel_pest_without_executing_project_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "artisan").write_text("#!/usr/bin/env php\n", encoding="utf-8")
            (project / "composer.json").write_text(
                json.dumps({"require-dev": {"pestphp/pest": "^4.0"}}),
                encoding="utf-8",
            )

            command = detect_project_test_command(project)

            self.assertEqual("Laravel Pest", command.label)
            self.assertEqual(
                ("php", "artisan", "test"),
                command.argv,
            )
            self.assertEqual(project.resolve(), command.cwd)

    def test_rejects_project_without_supported_test_runner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Pest"):
                detect_project_test_command(Path(directory))

    def test_streams_pest_output_and_preserves_failure_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "artisan").write_text("#!/usr/bin/env php\n", encoding="utf-8")
            (project / "tests").mkdir()
            (project / "tests/Pest.php").write_text("<?php\n", encoding="utf-8")
            process = Mock()
            process.stdout = iter(["PASS  Tests/Unit/ExampleTest.php\n", "1 failed\n"])
            process.wait.return_value = 1
            output: list[str] = []

            with patch("specsfy_cli.testing.subprocess.Popen", return_value=process):
                result = run_project_tests(project, emit=output.append)

            self.assertIsInstance(result, TestRun)
            self.assertEqual(1, result.exit_code)
            self.assertEqual(
                ["PASS  Tests/Unit/ExampleTest.php", "1 failed"],
                output,
            )
            self.assertEqual(
                ("1 failed",),
                result.summary_lines,
            )
            process.wait.assert_called_once_with()

    def test_formats_structured_pest_report_into_summary_and_test_lines(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "artisan").write_text("#!/usr/bin/env php\n", encoding="utf-8")
            (project / "tests").mkdir()
            (project / "tests/Pest.php").write_text("<?php\n", encoding="utf-8")
            process = Mock()
            process.stdout = iter(
                [
                    json.dumps(
                        {
                            "tool": "pest",
                            "result": "failed",
                            "tests": 2,
                            "passed": 1,
                            "errors": 1,
                            "assertions": 3,
                            "duration_ms": 1250,
                            "error_details": [
                                {
                                    "test": "DashboardTest::loads dashboard",
                                    "file": "/project/tests/DashboardTest.php",
                                    "line": 12,
                                    "message": "Expected status 200.",
                                }
                            ],
                        }
                    )
                    + "\n"
                ]
            )
            process.wait.return_value = 1
            output: list[str] = []

            with patch("specsfy_cli.testing.subprocess.Popen", return_value=process):
                result = run_project_tests(project, emit=output.append)

            self.assertEqual(
                (
                    "Tests: 2 total · 1 passed · 1 errors",
                    "Assertions: 3",
                    "Duration: 1.25s",
                ),
                result.summary_lines,
            )
            self.assertIn("FAIL  DashboardTest::loads dashboard", output)
            self.assertIn("      Expected status 200.", output)
            self.assertNotIn('"error_details"', "\n".join(output))


if __name__ == "__main__":
    unittest.main()

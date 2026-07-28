from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATE_DIR = ROOT / "specsfy-base-validate" / "scripts"
sys.path.insert(0, str(VALIDATE_DIR))
VALIDATE_SPEC_FILE = VALIDATE_DIR / "validate_spec.py"
VALIDATE_SPEC_MODULE = importlib.util.spec_from_file_location(
    "validate_spec_minimum_coverage",
    VALIDATE_SPEC_FILE,
)
assert VALIDATE_SPEC_MODULE is not None and VALIDATE_SPEC_MODULE.loader is not None
VALIDATE_SPEC = importlib.util.module_from_spec(VALIDATE_SPEC_MODULE)
VALIDATE_SPEC_MODULE.loader.exec_module(VALIDATE_SPEC)

TRACE = ROOT / "specsfy-base-tdd-bdd" / "scripts" / "check_traceability.py"


def acceptance(ac_id: str, covers: str) -> str:
    tags = " ".join(f"@{item}" for item in covers.split(", "))
    return (
        f"#### {ac_id} — Contexto {ac_id}\n\n"
        f"**Cobre**: {covers}\n\n"
        "```gherkin\n"
        f"{tags} @{ac_id}\n"
        "Feature: Cobertura contextual\n\n"
        f"  Scenario: Exemplo {ac_id}\n"
        "    Given um estado conhecido\n"
        "    When uma ação acontece\n"
        "    Then um resultado é observado\n"
        "```\n"
    )


class MinimumBddCoverageTests(unittest.TestCase):
    def test_requires_three_distinct_bdd_scenarios_for_each_user_story(self) -> None:
        text = (
            "#### US-001 — História\n"
            + acceptance("AC-001", "US-001, FR-001")
            + acceptance("AC-002", "US-001, FR-001")
            + acceptance("AC-003", "US-002, FR-001")
            + "- **FR-001**: Requisito.\n"
        )

        errors = VALIDATE_SPEC.minimum_bdd_coverage_errors(text)

        self.assertIn(
            "US-001 possui 2 cenários BDD; mínimo exigido: 3.",
            errors,
        )

    def test_requires_three_distinct_bdd_scenarios_for_each_requirement(self) -> None:
        text = (
            "#### US-001 — História\n"
            + acceptance("AC-001", "US-001, FR-001, NFR-001")
            + acceptance("AC-002", "US-001, FR-001, NFR-001")
            + acceptance("AC-003", "US-001, FR-002, NFR-002")
            + "- **FR-001**: Requisito.\n"
            + "- **FR-002**: Requisito.\n"
            + "- **NFR-001**: Qualidade. **Verificação**: teste.\n"
            + "- **NFR-002**: Qualidade. **Verificação**: teste.\n"
        )

        errors = VALIDATE_SPEC.minimum_bdd_coverage_errors(text)

        self.assertIn(
            "FR-001 possui 2 cenários BDD; mínimo exigido: 3.",
            errors,
        )
        self.assertIn(
            "NFR-001 possui 2 cenários BDD; mínimo exigido: 3.",
            errors,
        )

    def test_accepts_three_bdd_scenarios_for_feature_story_and_requirements(self) -> None:
        covers = "US-001, FR-001, NFR-001"
        text = (
            "#### US-001 — História\n"
            + acceptance("AC-001", covers)
            + acceptance("AC-002", covers)
            + acceptance("AC-003", covers)
            + "- **FR-001**: Requisito.\n"
            + "- **NFR-001**: Qualidade. **Verificação**: teste.\n"
        )

        self.assertEqual([], VALIDATE_SPEC.minimum_bdd_coverage_errors(text))


class MinimumTddCoverageTests(unittest.TestCase):
    def test_requires_three_distinct_tdd_case_markers_per_traceable_item(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec = root / "specs/specs/0001-example/spec.md"
            test = root / "tests/test_example.py"
            spec.parent.mkdir(parents=True)
            test.parent.mkdir(parents=True)
            spec.write_text(
                "#### US-001 — Example\n"
                "#### AC-001 — Example\n"
                "#### AC-002 — Example\n"
                "#### AC-003 — Example\n"
                "- **FR-001**: Example.\n"
                "- **NFR-001**: Example. **Verificação**: teste.\n",
                encoding="utf-8",
            )
            test.write_text(
                "# SPECSFY: US-001 FR-001 NFR-001 AC-001\n"
                "def test_first(): pass\n"
                "# SPECSFY: US-001 FR-001 NFR-001 AC-002\n"
                "def test_second(): pass\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(TRACE),
                    str(spec),
                    str(root),
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(1, completed.returncode)
            self.assertIn('"US-001": 1', completed.stdout)
            self.assertIn('"FR-001": 1', completed.stdout)
            self.assertIn('"NFR-001": 1', completed.stdout)

    def test_accepts_three_distinct_tdd_case_markers_per_traceable_item(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec = root / "specs/specs/0001-example/spec.md"
            test = root / "tests/test_example.py"
            spec.parent.mkdir(parents=True)
            test.parent.mkdir(parents=True)
            spec.write_text(
                "#### US-001 — Example\n"
                "#### AC-001 — Example\n"
                "#### AC-002 — Example\n"
                "#### AC-003 — Example\n"
                "- **FR-001**: Example.\n"
                "- **NFR-001**: Example. **Verificação**: teste.\n",
                encoding="utf-8",
            )
            test.write_text(
                "# SPECSFY: US-001 FR-001 NFR-001 AC-001\n"
                "def test_first(): pass\n"
                "# SPECSFY: US-001 FR-001 NFR-001 AC-002\n"
                "def test_second(): pass\n"
                "# SPECSFY: US-001 FR-001 NFR-001 AC-003\n"
                "def test_third(): pass\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(TRACE),
                    str(spec),
                    str(root),
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            self.assertIn('"required_cases": 3', completed.stdout)
            self.assertIn('"feature_cases": 3', completed.stdout)

    def test_one_shared_marker_counts_as_one_tdd_case(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec = root / "specs/specs/0001-example/spec.md"
            test = root / "tests/test_example.py"
            spec.parent.mkdir(parents=True)
            test.parent.mkdir(parents=True)
            spec.write_text(
                "#### US-001 — Example\n"
                "#### AC-001 — Example\n"
                "#### AC-002 — Example\n"
                "#### AC-003 — Example\n"
                "- **FR-001**: Example.\n"
                "- **NFR-001**: Example. **Verificação**: teste.\n",
                encoding="utf-8",
            )
            test.write_text(
                "# SPECSFY: US-001 FR-001 NFR-001 AC-001 AC-002 AC-003\n"
                "def test_first(): pass\n"
                "def test_second(): pass\n"
                "def test_third(): pass\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(TRACE),
                    str(spec),
                    str(root),
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(1, completed.returncode)
            self.assertIn('"feature_cases": 1', completed.stdout)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "bin" / "specsfy"


CANONICAL_SPEC = """# Especificação integrada: Entrega concluída

| Campo | Valor |
| --- | --- |
| Formato | Specsfy/2.0 |
| Status | Complete |
| Definition Gate | Passed |
| Plan Gate | Passed |
| Delivery Gate | Passed |
"""


class CliProgressContractTests(unittest.TestCase):
    def test_projects_canonical_table_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "specs/specs/0001-entrega/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text(CANONICAL_SPEC, encoding="utf-8")

            result = subprocess.run(
                [str(CLI), "progress", "--project", str(root), "--json"],
                text=True,
                capture_output=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            spec = payload["specs"][0]

            self.assertEqual("Complete", spec["status"])
            self.assertEqual("Passed", spec["definition_gate"])
            self.assertEqual("Passed", spec["plan_gate"])
            self.assertEqual("Passed", spec["delivery_gate"])
            self.assertEqual(3, spec["passed_gates"])
            self.assertNotIn("content", spec)
            self.assertEqual(1, payload["summary"]["completed_specs"])


if __name__ == "__main__":
    unittest.main()

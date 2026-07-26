from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cli" / "src"))

from specsfy_cli.progress import scan_specs, summarize_specs


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

            specs = scan_specs(root)

            self.assertEqual("Complete", specs[0].status)
            self.assertEqual("Passed", specs[0].definition_gate)
            self.assertEqual("Passed", specs[0].plan_gate)
            self.assertEqual("Passed", specs[0].delivery_gate)
            self.assertEqual(3, specs[0].passed_gates)
            self.assertEqual(1, summarize_specs(specs).completed_specs)


if __name__ == "__main__":
    unittest.main()

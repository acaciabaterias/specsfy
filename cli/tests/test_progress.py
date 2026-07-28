from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from specsfy_cli.progress import scan_specs, specs_fingerprint, summarize_specs


SPEC = """# Especificação integrada: Exemplo

**Status**: Implementing
**Definition Gate**: Passed
**Plan Gate**: Passed
**Delivery Gate**: Pending

- [x] Intenção confirmada
- [ ] Evidência final registrada
- [x] T001 [CODE] Primeira
- [ ] T002 [TEST] Segunda
"""

TABLE_SPEC = """# Especificação integrada: Exemplo concluído

| Campo | Valor |
| --- | --- |
| Formato | Specsfy/2.0 |
| Status | Complete |
| Definition Gate | Passed |
| Plan Gate | Passed |
| Delivery Gate | Passed |
"""


class ProgressTests(unittest.TestCase):
    def test_reads_canonical_table_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = root / "specs/specs/0001-exemplo/spec.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(TABLE_SPEC, encoding="utf-8")

            progress = scan_specs(root)

            self.assertEqual("Complete", progress[0].status)
            self.assertEqual("Passed", progress[0].definition_gate)
            self.assertEqual("Passed", progress[0].plan_gate)
            self.assertEqual("Passed", progress[0].delivery_gate)
            self.assertEqual(3, progress[0].passed_gates)
            self.assertEqual(1, summarize_specs(progress).completed_specs)

    def test_scans_specs_and_calculates_progress(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = root / "specs/specs/0001-exemplo/spec.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(SPEC, encoding="utf-8")

            progress = scan_specs(root)

            self.assertEqual(1, len(progress))
            self.assertEqual(spec.read_text(encoding="utf-8"), progress[0].content)
            self.assertNotIn("content", progress[0].to_dict())
            self.assertEqual("Implementing", progress[0].status)
            self.assertEqual(1, progress[0].completed_tasks)
            self.assertEqual(2, progress[0].total_tasks)
            self.assertEqual(50, progress[0].percent)
            self.assertEqual(2, progress[0].completed_items)
            self.assertEqual(4, progress[0].total_items)
            self.assertEqual(2, progress[0].pending_items)
            self.assertEqual(2, progress[0].passed_gates)
            self.assertEqual(3, progress[0].total_gates)

            summary = summarize_specs(progress)
            self.assertEqual(1, summary.total_specs)
            self.assertEqual(1, summary.completed_tasks)
            self.assertEqual(1, summary.pending_tasks)
            self.assertEqual(2, summary.completed_items)
            self.assertEqual(2, summary.pending_items)
            self.assertEqual(50, summary.percent)

    def test_fingerprint_changes_when_spec_content_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = root / "specs/specs/0001-exemplo/spec.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(SPEC, encoding="utf-8")
            before = specs_fingerprint(root)

            spec.write_text(SPEC.replace("- [ ] T002", "- [x] T002"), encoding="utf-8")

            self.assertNotEqual(before, specs_fingerprint(root))

    def test_empty_project_returns_empty_projection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual([], scan_specs(Path(directory)))

    def test_reads_legacy_layout_without_counting_backlog_as_spec(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            legacy = root / "specs/0001-legada/spec.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text(SPEC, encoding="utf-8")
            backlog = root / "specs/backlog/0001-ideia.md"
            backlog.parent.mkdir(parents=True)
            backlog.write_text("- [ ] Ideia\n", encoding="utf-8")

            progress = scan_specs(root)

            self.assertEqual(["0001-legada"], [item.slug for item in progress])

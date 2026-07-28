from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from specsfy_cli.backlog import backlogs_fingerprint, scan_backlogs


class BacklogTests(unittest.TestCase):
    def test_scans_canonical_backlogs_with_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            first = project / "specs/backlog/0001-login.md"
            second = project / "specs/backlog/0002-alertas.md"
            first.parent.mkdir(parents=True)
            first.write_text(
                "# Backlog: Login seguro\n\n"
                "**ID**: BACKLOG-0001\n"
                "**Status**: Refining\n",
                encoding="utf-8",
            )
            second.write_text(
                "# Alertas\n\n**Status**: Captured\n",
                encoding="utf-8",
            )

            items = scan_backlogs(project)

            self.assertEqual(["0001-login", "0002-alertas"], [item.slug for item in items])
            self.assertEqual("Login seguro", items[0].title)
            self.assertEqual("BACKLOG-0001", items[0].identifier)
            self.assertEqual("Refining", items[0].status)
            self.assertEqual("0002-alertas", items[1].identifier)

    def test_scans_metadata_table_generated_by_current_backlog_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            backlog = project / "specs/backlog/0001-painel.md"
            backlog.parent.mkdir(parents=True)
            backlog.write_text(
                "# Backlog: Painel\n\n"
                "| Metainformação | Valor |\n"
                "| --- | --- |\n"
                "| ID | BACKLOG-0001 |\n"
                "| Status | Captured |\n",
                encoding="utf-8",
            )

            [item] = scan_backlogs(project)

            self.assertEqual("BACKLOG-0001", item.identifier)
            self.assertEqual("Captured", item.status)

    def test_fingerprint_changes_with_backlog_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            backlog = project / "specs/backlog/0001-ideia.md"
            backlog.parent.mkdir(parents=True)
            backlog.write_text("# Ideia inicial\n", encoding="utf-8")
            before = backlogs_fingerprint(project)

            backlog.write_text("# Ideia refinada\n", encoding="utf-8")

            self.assertNotEqual(before, backlogs_fingerprint(project))

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "specsfy-01-inbox/scripts/capturar_inbox.py"
SKILL = ROOT / "specsfy-01-inbox/SKILL.md"
TEMPLATE = ROOT / "templates/Inbox.md"


class InboxCaptureTests(unittest.TestCase):
    def test_contract_forbids_questions_and_preserves_the_input(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        template = TEMPLATE.read_text(encoding="utf-8")
        normalized = " ".join(skill.split())

        self.assertIn("não faça perguntas", normalized.casefold())
        self.assertIn("não peça confirmação", normalized.casefold())
        self.assertIn("texto original", normalized.casefold())
        self.assertIn("declaração", normalized.casefold())
        self.assertIn("inferência", normalized.casefold())
        self.assertIn("a revisar", normalized.casefold())
        self.assertIn("## Texto original", template)
        self.assertIn("## Análise inicial", template)
        self.assertIn("## Pontos a revisar no futuro", template)

    def test_captures_with_timestamp_slug_and_preprocessed_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            templates = project / ".specsfy/templates"
            templates.mkdir(parents=True)
            (templates / "Inbox.md").write_text(
                TEMPLATE.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            idea = (
                "Quero um modo de avisar clientes quando uma entrega atrasar, "
                "talvez por e-mail."
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPT),
                    "--input",
                    idea,
                    "--title",
                    "Avisar clientes sobre atrasos",
                    "--summary",
                    "Notificar clientes afetados por atrasos de entrega.",
                    "--problem",
                    "Clientes não recebem contexto quando a entrega atrasa.",
                    "--people",
                    "Clientes com entrega em andamento.",
                    "--value",
                    "Reduzir incerteza durante atrasos.",
                    "--signals",
                    "Canal sugerido no texto: e-mail.",
                    "--review",
                    "Definir gatilho, destinatários e conteúdo da notificação.",
                    "--root",
                    str(project),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            created = Path(result.stdout.strip())
            self.assertRegex(
                created.name,
                r"^\d{4}-\d{2}-\d{2}-\d{6}-avisar-clientes-sobre-atrasos\.md$",
            )
            self.assertEqual(project / "specs/inbox", created.parent)
            content = created.read_text(encoding="utf-8")
            self.assertIn(idea, content)
            self.assertIn("Notificar clientes afetados", content)
            self.assertIn("Clientes não recebem contexto", content)
            self.assertIn("Clientes com entrega", content)
            self.assertIn("Reduzir incerteza", content)
            self.assertIn("Canal sugerido", content)
            self.assertIn("Definir gatilho", content)
            self.assertIsNotNone(
                re.search(r"\| Capturada em \| \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", content)
            )
            self.assertFalse((project / "specs/backlog").exists())
            self.assertFalse((project / "specs/specs").exists())

    def test_same_second_never_overwrites_an_existing_idea(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            templates = project / ".specsfy/templates"
            templates.mkdir(parents=True)
            (templates / "Inbox.md").write_text(
                TEMPLATE.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            command = [
                sys.executable,
                "-B",
                str(SCRIPT),
                "--input",
                "Uma ideia curta.",
                "--title",
                "Ideia curta",
                "--root",
                str(project),
            ]

            first = subprocess.run(
                command, text=True, capture_output=True, check=False
            )
            second = subprocess.run(
                command, text=True, capture_output=True, check=False
            )

            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertNotEqual(first.stdout.strip(), second.stdout.strip())
            self.assertEqual(
                2,
                len(list((project / "specs/inbox").glob("*.md"))),
            )

    def test_prefers_custom_template_over_installed_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            templates = project / ".specsfy/templates"
            custom = templates / "custom"
            custom.mkdir(parents=True)
            (templates / "Inbox.md").write_text(
                TEMPLATE.read_text(encoding="utf-8").replace(
                    "# Inbox:",
                    "# Template padrão:",
                ),
                encoding="utf-8",
            )
            (custom / "Inbox.md").write_text(
                TEMPLATE.read_text(encoding="utf-8").replace(
                    "# Inbox:",
                    "# Template customizado:",
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPT),
                    "--input",
                    "Capturar com template customizado.",
                    "--title",
                    "Precedência customizada",
                    "--root",
                    str(project),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            content = Path(result.stdout.strip()).read_text(encoding="utf-8")
            self.assertIn("# Template customizado:", content)
            self.assertNotIn("# Template padrão:", content)


if __name__ == "__main__":
    unittest.main()

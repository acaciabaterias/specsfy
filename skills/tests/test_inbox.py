from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "specsfy-01-inbox/scripts/capturar_inbox.mjs"
SKILL = ROOT / "specsfy-01-inbox/SKILL.md"
TEMPLATE = ROOT / "templates/Inbox.md"
MVP_INTERVIEWER = ROOT / "specsfy-mvp-milestone-interviewer/SKILL.md"
MVP_IMPORTER = ROOT / "specsfy-mvp-milestone-interviewer/scripts/importar_mvp.mjs"


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
        self.assertIn("Informações que talvez precisem ser guardadas", template)

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
                    "node",
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
            self.assertIn("Não identificado no texto original.", content)
            self.assertIsNotNone(
                re.search(r"\| Capturada em \| \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", content)
            )
            self.assertFalse((project / "specs/backlog").exists())
            self.assertFalse((project / "specs/draft").exists())

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
                "node",
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
                    "node",
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

    def test_registers_conversation_context_for_a_series_of_inboxes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            templates = project / ".specsfy/templates"
            templates.mkdir(parents=True)
            (templates / "Inbox.md").write_text(
                TEMPLATE.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    "node",
                    str(SCRIPT),
                    "--input",
                    "Quero validar a primeira jornada do produto.",
                    "--title",
                    "Descoberta do produto",
                    "--session",
                    "DESC-20260820-produto",
                    "--turn",
                    "2",
                    "--sources",
                    "- `MVP.md`: presente e consultado.\n- `BRAND.md`: presente e consultado.",
                    "--root",
                    str(project),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            content = Path(result.stdout.strip()).read_text(encoding="utf-8")
            self.assertIn("DESC-20260820-produto", content)
            self.assertIn("| Turno da conversa | 2 |", content)
            self.assertIn("`MVP.md`: presente e consultado.", content)
            self.assertIn("`BRAND.md`: presente e consultado.", content)

    def test_mvp_interviewer_uses_root_context_inboxes_and_confirmed_milestones(self) -> None:
        source = MVP_INTERVIEWER.read_text(encoding="utf-8")
        normalized = " ".join(source.split()).casefold()

        self.assertIn("`mvp.md`", source.casefold())
        self.assertIn("`brand.md`", source.casefold())
        self.assertIn("fila ordenada de inboxes e backlogs", normalized)
        self.assertIn("$specsfy-01-inbox", source)
        self.assertIn("$specsfy-02-backlog", source)
        self.assertIn("`specs/milestones/m01.md`", source.casefold())
        self.assertIn("milestone 1.0", normalized)
        self.assertIn("não sobrescreva a milestone 1.0", normalized)
        self.assertIn("$specsfy-data-discovery", source)
        self.assertIn("$specsfy-02-backlog", source)
        self.assertIn("$specsfy-milestone-governor", source)
        self.assertIn("$specsfy-03-specify", source)
        self.assertIn("texto integral da opção escolhida", normalized)
        self.assertIn("informação a guardar ausente ou ambígua", normalized)
        self.assertIn("Português do Brasil", source)
        self.assertIn("superprojeto", normalized)
        self.assertIn("--show-superproject-working-tree", source)

    def test_imports_mvp_as_milestone_and_creates_interviewable_backlogs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "MVP.md").write_text(
                "# Produto\n\n## Captar pedidos\n\nReceber pedidos de clientes.\n\n## Acompanhar pedidos\n\nMostrar o andamento de cada pedido.\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(MVP_IMPORTER), "--root", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            imported = __import__("json").loads(result.stdout)
            self.assertEqual("specs/milestones/M01.md", imported["milestone"])
            self.assertEqual(2, len(imported["items"]))

            milestone = project / imported["milestone"]
            self.assertIn("# Milestone 1.0", milestone.read_text(encoding="utf-8"))
            self.assertIn("Receber pedidos de clientes.", milestone.read_text(encoding="utf-8"))

            for item in imported["items"]:
                inbox = project / item["inbox"]
                backlog = project / item["backlog"]
                self.assertTrue(inbox.is_file())
                self.assertTrue(backlog.is_file())
                backlog_content = backlog.read_text(encoding="utf-8")
                self.assertIn(item["inbox"], backlog_content)
                self.assertIn("specs/milestones/M01.md", backlog_content)
                self.assertIn("Entrevista obrigatória", backlog_content)

    def test_mvp_import_never_overwrites_the_first_milestone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "MVP.md").write_text("# Produto\n\nPrimeira jornada.\n", encoding="utf-8")
            (project / "specs/milestones").mkdir(parents=True)
            (project / "specs/milestones/M01.md").write_text("Conteúdo existente.\n", encoding="utf-8")

            result = subprocess.run(
                ["node", str(MVP_IMPORTER), "--root", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("não será sobrescrita", result.stderr)
            self.assertFalse((project / "specs/inbox").exists())


if __name__ == "__main__":
    unittest.main()

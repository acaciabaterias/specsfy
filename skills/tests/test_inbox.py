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

    def test_mvp_interviewer_uses_root_context_and_defers_inbox_treatment(self) -> None:
        source = MVP_INTERVIEWER.read_text(encoding="utf-8")
        normalized = " ".join(source.split()).casefold()

        self.assertIn("`mvp.md`", source.casefold())
        self.assertIn("`brand.md`", source.casefold())
        self.assertIn("série de capturas", normalized)
        self.assertIn("$specsfy-01-inbox", source)
        self.assertIn("$specsfy-02-backlog", source)
        self.assertIn("`specs/milestones/m01.md`", source.casefold())
        self.assertIn("`milestone 1.0`", source.casefold())
        self.assertIn("não o sobrescreva", normalized)
        self.assertIn("superprojeto", normalized)
        self.assertIn("--show-superproject-working-tree", source)

    def test_imports_mvp_as_milestone_one_without_overwriting_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            source = "# Produto\n\nPermitir o primeiro fluxo completo.\n"
            (project / "MVP.md").write_text(source, encoding="utf-8")

            first = subprocess.run(
                ["node", str(MVP_IMPORTER), "--root", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )
            milestone = project / "specs/milestones/M01.md"
            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(str(milestone), first.stdout.strip())
            content = milestone.read_text(encoding="utf-8")
            self.assertIn("# Milestone 1.0", content)
            self.assertIn("Permitir o primeiro fluxo completo.", content)
            self.assertIn("SHA-256", content)

            second = subprocess.run(
                ["node", str(MVP_IMPORTER), "--root", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, second.returncode)
            self.assertIn("não será sobrescrita", second.stderr)

    def test_imports_mvp_from_superproject_when_consumer_is_a_submodule(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            source_repository = workspace / "consumer-source"
            hub = workspace / "hub"

            for repository in (source_repository, hub):
                subprocess.run(
                    ["git", "init", str(repository)],
                    text=True,
                    capture_output=True,
                    check=True,
                )
                subprocess.run(
                    ["git", "-C", str(repository), "config", "user.email", "tests@specsfy.dev"],
                    text=True,
                    capture_output=True,
                    check=True,
                )
                subprocess.run(
                    ["git", "-C", str(repository), "config", "user.name", "Testes Specsfy"],
                    text=True,
                    capture_output=True,
                    check=True,
                )
                (repository / "README.md").write_text("# Projeto\n", encoding="utf-8")
                subprocess.run(
                    ["git", "-C", str(repository), "add", "README.md"],
                    text=True,
                    capture_output=True,
                    check=True,
                )
                subprocess.run(
                    ["git", "-C", str(repository), "commit", "-m", "Preparar projeto de teste"],
                    text=True,
                    capture_output=True,
                    check=True,
                )

            subprocess.run(
                [
                    "git",
                    "-c",
                    "protocol.file.allow=always",
                    "-C",
                    str(hub),
                    "submodule",
                    "add",
                    str(source_repository),
                    "consumer",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            source = "# MVP do Hub\n\nEntregar a primeira jornada completa.\n"
            (hub / "MVP.md").write_text(source, encoding="utf-8")
            consumer = hub / "consumer"

            result = subprocess.run(
                ["node", str(MVP_IMPORTER), "--root", str(consumer)],
                text=True,
                capture_output=True,
                check=False,
            )

            milestone = consumer / "specs/milestones/M01.md"
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(str(milestone), result.stdout.strip())
            self.assertIn("Entregar a primeira jornada completa.", milestone.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

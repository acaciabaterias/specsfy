from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/specsfy-mvp-milestone-interviewer/scripts/importar_mvp.mjs"


class MvpImporterTests(unittest.TestCase):
    def test_generates_a_draft_spec_for_every_mvp_theme(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "MVP.md").write_text(
                """# MVP

## Cadastro

Problema: dados dispersos.

## Consulta

Resultado: consultar registros.
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(SCRIPT), "--root", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            items = json.loads(result.stdout)["items"]
            self.assertEqual(2, len(items))
            self.assertEqual(
                {project / item["spec"] for item in items},
                set((project / "specs/draft").glob("*/spec.md")),
            )

    def test_imports_mvp_into_inbox_backlog_and_draft_spec_with_obvious_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "MVP.md").write_text(
                """# MVP

## Cadastro de clientes

Problema: a equipe perde tempo procurando dados espalhados.

Público: pessoas responsáveis pelo atendimento.

Resultado: o sistema deve permitir consultar os dados em um único lugar.

Contexto: durante o atendimento de cada cliente.

Menus: menu principal com Clientes para /clientes.
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(SCRIPT), "--root", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(1, len(output["items"]))
            item = output["items"][0]
            inbox = project / item["inbox"]
            backlog = project / item["backlog"]
            spec = project / item["spec"]

            self.assertTrue(inbox.is_file())
            self.assertTrue(backlog.is_file())
            self.assertTrue(spec.is_file())
            self.assertEqual(1, len(list((project / "specs/inbox").glob("*.md"))))
            self.assertEqual(1, len(list((project / "specs/backlog").glob("*.md"))))
            self.assertEqual(1, len(list((project / "specs/draft").glob("*/spec.md"))))

            inbox_content = inbox.read_text(encoding="utf-8")
            backlog_content = backlog.read_text(encoding="utf-8")
            spec_content = spec.read_text(encoding="utf-8")
            self.assertIn("a equipe perde tempo procurando dados espalhados", inbox_content)
            self.assertIn("## Defaults aplicados automaticamente", backlog_content)
            self.assertIn("| Status | Promoted |", backlog_content)
            self.assertIn(f"| Spec promovida | `{item['spec']}` |", backlog_content)
            self.assertIn("a equipe perde tempo procurando dados espalhados", spec_content)
            self.assertIn("pessoas responsáveis pelo atendimento", spec_content)
            self.assertIn("#### Menus e navegação principal", spec_content)
            self.assertIn("menu principal com Clientes para /clientes", backlog_content)
            self.assertIn("menu principal com Clientes para /clientes", spec_content)
            self.assertIn("| Status | Draft |", spec_content)
            self.assertIn("| Definition Gate | Pending |", spec_content)
            self.assertIn("Pendente:", spec_content)
            self.assertFalse((project / "src").exists())
            validation = subprocess.run(
                [
                    "node",
                    str(ROOT / "skills/specsfy-04-validate/scripts/validate_spec.mjs"),
                    str(spec),
                    "--allow-draft",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, validation.returncode, validation.stdout + validation.stderr)

    def test_keeps_unanswered_fields_pending_instead_of_inventing_them(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "MVP.md").write_text(
                "## Consulta de registros\n\nA aplicação deve consultar registros.\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(SCRIPT), "--root", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            item = json.loads(result.stdout)["items"][0]
            spec_content = (project / item["spec"]).read_text(encoding="utf-8")
            self.assertIn("Pendente: o MVP não declara o problema percebido", spec_content)
            self.assertIn("Pendente: o MVP não identifica a pessoa afetada", spec_content)
            self.assertIn("Pendente: o MVP não declara o resultado ou valor esperado", spec_content)
            self.assertIn("Pendente: o MVP não declara os menus ou a navegação principal", spec_content)
            self.assertIn("| Definition Gate | Pending |", spec_content)

    def test_keeps_contextual_themes_out_of_backlog_and_specs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "MVP.md").write_text(
                """# MVP

## Visão do produto

Uma solução simples para organizar o trabalho.

## Público-alvo

Equipes pequenas.

## Cadastro de clientes

O sistema deve permitir cadastrar clientes.
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(SCRIPT), "--root", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            items = json.loads(result.stdout)["items"]
            self.assertEqual(3, len(items))
            self.assertEqual(2, sum(item["developable"] is False for item in items))
            self.assertEqual(1, sum(item["developable"] is True for item in items))
            self.assertEqual(1, len(list((project / "specs/backlog").glob("*.md"))))
            self.assertEqual(1, len(list((project / "specs/draft").glob("*/spec.md"))))
            skipped = [item for item in items if not item["developable"]]
            self.assertTrue(all(item["backlog"] is None and item["spec"] is None for item in skipped))
            inboxes = list((project / "specs/inbox").glob("*.md"))
            self.assertEqual(3, len(inboxes))
            self.assertTrue(any("Não criar backlog nem spec" in path.read_text(encoding="utf-8") for path in inboxes))


if __name__ == "__main__":
    unittest.main()

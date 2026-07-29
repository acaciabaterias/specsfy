from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "specsfy-02-backlog/scripts/iniciar_backlog.py"
SKILL = ROOT / "specsfy-02-backlog/SKILL.md"
TEMPLATE = ROOT / "templates/Backlog.md"


class BacklogTests(unittest.TestCase):
    def test_requires_adaptive_dialogue_before_persisting_a_minimal_item(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        template = TEMPLATE.read_text(encoding="utf-8")

        self.assertIn("## Garantir a captura mínima", skill)
        self.assertIn("problema percebido", skill)
        self.assertIn("pessoa afetada ou beneficiada", skill)
        self.assertIn("resultado ou valor esperado", skill)
        self.assertIn("contexto suficiente para distinguir a entrada", skill)
        self.assertIn("uma pergunta por vez", skill)
        self.assertIn("Reavalie as lacunas depois de cada resposta", skill)
        self.assertIn(
            "Não crie nem atualize o arquivo enquanto algum item essencial",
            skill,
        )
        self.assertIn("## Pessoa afetada ou beneficiada", template)
        self.assertIn("## Contexto", template)

    def test_searches_related_project_material_before_creating_an_item(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        template = TEMPLATE.read_text(encoding="utf-8")

        self.assertIn("## Buscar duplicatas e referências", skill)
        self.assertIn("termos derivados do pedido do usuário", skill)
        self.assertIn("`specs/backlog/*.md`", skill)
        self.assertIn("`specs/specs/*/spec.md`", skill)
        self.assertIn("`docs/**/*.md`", skill)
        self.assertIn("possível duplicata", skill)
        self.assertIn("confirme com o usuário", skill)
        self.assertIn("## Referências relacionadas", template)

    def test_template_starts_with_a_metadata_table_instead_of_a_list(self) -> None:
        template = TEMPLATE.read_text(encoding="utf-8")
        lines = template.splitlines()

        self.assertEqual("# Backlog: {{BACKLOG_NAME}}", lines[0])
        self.assertEqual("| Metainformação | Valor |", lines[2])
        self.assertEqual("| --- | --- |", lines[3])
        for field in (
            "ID",
            "Status",
            "Produto",
            "Épico",
            "Funcionalidade",
            "Tipo",
            "Prioridade",
            "Criado em",
            "Spec promovida",
        ):
            self.assertIn(f"| {field} |", template)
            self.assertNotIn(f"**{field}**:", template)

    def test_refuses_to_create_an_item_with_an_empty_essential_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPT),
                    "--title",
                    "Painel de acompanhamento",
                    "--idea",
                    "Precisamos de um painel de acompanhamento.",
                    "--problem",
                    "",
                    "--person",
                    "Pessoas responsáveis pelo produto.",
                    "--result",
                    "Visualizar rapidamente o andamento das entregas.",
                    "--context",
                    "Durante o acompanhamento semanal do produto.",
                    "--root",
                    str(project),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(1, result.returncode)
            self.assertIn("o problema percebido não pode ficar vazio", result.stderr)
            self.assertFalse((project / "specs/backlog").exists())

    def test_creates_numbered_backlog_item_without_creating_a_spec(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPT),
                    "--title",
                    "Painel de acompanhamento",
                    "--idea",
                    "Precisamos de um painel de acompanhamento.",
                    "--problem",
                    "A equipe não enxerga o andamento das entregas.",
                    "--person",
                    "Pessoas responsáveis pelo produto.",
                    "--result",
                    "Visualizar rapidamente o andamento das entregas.",
                    "--context",
                    "Durante o acompanhamento semanal do produto.",
                    "--root",
                    str(project),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            expected = project / "specs/backlog/0001-painel-de-acompanhamento.md"
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(str(expected.resolve()), result.stdout.strip())
            self.assertTrue(expected.is_file())
            content = expected.read_text(encoding="utf-8")
            self.assertIn("| ID | BACKLOG-0001 |", content)
            self.assertIn("| Status | Captured |", content)
            self.assertIn("| Produto |", content)
            self.assertIn("| Épico |", content)
            self.assertIn("| Funcionalidade |", content)
            self.assertIn("| Prioridade |", content)
            self.assertIn(
                "A equipe não enxerga o andamento das entregas.",
                content,
            )
            self.assertIn("Pessoas responsáveis pelo produto.", content)
            self.assertIn(
                "Visualizar rapidamente o andamento das entregas.",
                content,
            )
            self.assertIn(
                "Durante o acompanhamento semanal do produto.",
                content,
            )
            self.assertIn("## Comportamento esperado", content)
            self.assertIn("## Regras de negócio", content)
            self.assertIn("## Critérios de aceitação", content)
            self.assertIn("## Qualidades e operação", content)
            self.assertIn("## Dependências", content)
            self.assertIn("## Situações de erro", content)
            self.assertIn("## Pronto para desenvolvimento", content)
            self.assertFalse((project / "specs/specs").exists())

    def test_allocates_backlog_ids_independently_from_specs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            backlog = project / "specs/backlog"
            backlog.mkdir(parents=True)
            (backlog / "0003-anterior.md").write_text("# anterior\n", encoding="utf-8")
            (project / "specs/specs/0099-feature").mkdir(parents=True)

            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPT),
                    "--title",
                    "Próxima ideia",
                    "--idea",
                    "Registrar a próxima ideia.",
                    "--problem",
                    "A ideia ainda não está preservada.",
                    "--person",
                    "Pessoa responsável pelo produto.",
                    "--result",
                    "Preservar a ideia para retomada.",
                    "--context",
                    "No planejamento do produto.",
                    "--root",
                    str(project),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((backlog / "0004-proxima-ideia.md").is_file())

    def test_prefers_custom_template_over_installed_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            templates = project / ".specsfy/templates"
            custom = templates / "custom"
            custom.mkdir(parents=True)
            (templates / "Backlog.md").write_text(
                TEMPLATE.read_text(encoding="utf-8").replace(
                    "# Backlog:",
                    "# Template padrão:",
                ),
                encoding="utf-8",
            )
            (custom / "Backlog.md").write_text(
                TEMPLATE.read_text(encoding="utf-8").replace(
                    "# Backlog:",
                    "# Template customizado:",
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPT),
                    "--title",
                    "Precedência customizada",
                    "--idea",
                    "Usar um template customizado.",
                    "--problem",
                    "O template padrão não representa o projeto.",
                    "--person",
                    "Equipe do projeto.",
                    "--result",
                    "Aplicar a estrutura local.",
                    "--context",
                    "Durante a criação do backlog.",
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

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMPORTER = (
    ROOT
    / "skills"
    / "specsfy-mvp-milestone-interviewer"
    / "scripts"
    / "importar_mvp.mjs"
)


class MvpMilestoneImportTests(unittest.TestCase):
    """O MVP importa somente requisitos de desenvolvimento para o Specsfy."""

    def test_imports_development_requirements_without_inboxes_or_business_context(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "MVP.md").write_text(
                """# MVP\n\n## Modelo de negócio\n\nAssinatura mensal para equipes comerciais.\n\n## Cadastro de clientes\n\nO sistema deve permitir criar, consultar e editar clientes.\n""",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(IMPORTER), "--root", str(project)],
                check=True,
                capture_output=True,
                text=True,
            )

            output = json.loads(result.stdout)
            milestone = project / output["milestone"]
            backlogs = list((project / "specs" / "backlog").glob("*.md"))
            specs = list((project / "specs" / "draft").glob("*/spec.md"))

            self.assertFalse((project / "specs" / "inbox").exists())
            self.assertEqual(1, len(backlogs))
            self.assertEqual(1, len(specs))
            self.assertEqual(1, len(output["items"]))
            self.assertEqual("Cadastro de clientes", output["items"][0]["title"])
            self.assertIn("Cadastro de clientes", backlogs[0].read_text(encoding="utf-8"))
            self.assertNotIn("Modelo de negócio", milestone.read_text(encoding="utf-8"))
            self.assertNotIn("Assinatura mensal", milestone.read_text(encoding="utf-8"))

    def test_keeps_a_business_only_mvp_outside_specs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "MVP.md").write_text(
                """# MVP\n\n## Público-alvo\n\nAgências de marketing de pequeno porte.\n\n## Modelo de negócio\n\nCobrança por assinatura mensal.\n\n## Métricas de sucesso\n\nCriar uma carteira com 100 clientes ativos.\n""",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(IMPORTER), "--root", str(project)],
                check=True,
                capture_output=True,
                text=True,
            )

            output = json.loads(result.stdout)
            milestone = project / output["milestone"]

            self.assertEqual([], output["items"])
            self.assertFalse((project / "specs" / "inbox").exists())
            self.assertFalse((project / "specs" / "backlog").exists())
            self.assertFalse((project / "specs" / "draft").exists())
            self.assertNotIn("Agências de marketing", milestone.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

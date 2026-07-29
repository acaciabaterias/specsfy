from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
USER = DOCS / "user"
DEVELOP = DOCS / "develop"
BASE_SKILLS = (
    "specsfy-01-inbox",
    "specsfy-02-backlog",
    "specsfy-03-specify",
    "specsfy-04-validate",
    "specsfy-05-tasks",
    "specsfy-06-tdd-bdd",
    "specsfy-07-implement",
    "specsfy-update-spec",
    "specsfy-progress",
)


class DocumentationAudienceContractTests(unittest.TestCase):
    def test_docs_has_exactly_the_user_and_develop_trees(self) -> None:
        directories = {
            path.name for path in DOCS.iterdir() if path.is_dir()
        }
        self.assertEqual({"user", "develop"}, directories)
        self.assertTrue((DOCS / "README.md").is_file())

    def test_user_portal_covers_the_complete_product_journey(self) -> None:
        portal = (USER / "README.md").read_text(encoding="utf-8")
        expected_routes = {
            "Instalação": "installation.md",
            "Primeiro projeto": "getting-started.md",
            "Metodologia": "method.md",
            "Inbox": "inbox.md",
            "CLI e TUI": "cli.md",
            "Informações permanentes do projeto": "project-context.md",
            "Especialistas": "specialists.md",
            "Documentação do sistema": "system-documentation.md",
            "Mudanças posteriores": "update-spec.md",
            "Laravel": "laravel.md",
            "Astro": "astro.md",
            "Next.js": "nextjs.md",
            "Skills base": "skills/README.md",
        }
        for label, target in expected_routes.items():
            with self.subTest(route=label):
                self.assertIn(label, portal)
                self.assertIn(f"]({target})", portal)
                self.assertTrue((USER / target).exists())

        for phrase in (
            "ideia",
            "especificação",
            "teste",
            "implementação",
            "progresso",
            "exemplo",
        ):
            self.assertIn(phrase, portal.casefold())

    def test_each_base_skill_has_an_accessible_in_depth_user_page(self) -> None:
        index = (USER / "skills" / "README.md").read_text(encoding="utf-8")
        for skill in BASE_SKILLS:
            with self.subTest(skill=skill):
                page = USER / "skills" / f"{skill}.md"
                self.assertTrue(page.is_file())
                self.assertIn(f"]({skill}.md)", index)
                text = page.read_text(encoding="utf-8")
                self.assertIn(f"`{skill}`", text)
                for section in (
                    "## Quando usar",
                    "## Como descrever a tarefa",
                    "## Exemplo passo a passo",
                    "## O que esperar",
                    "## Erros comuns",
                    "## Próximo passo",
                ):
                    self.assertIn(section, text)
                self.assertIn("```text", text)

    def test_develop_tree_explains_how_to_change_the_framework(self) -> None:
        required = {
            "README.md": ("agentes", "humanos", "contribuir"),
            "methodology.md": (
                "Specsfy/2.0",
                "Ato I",
                "Ato II",
                "Ato III",
                "Definition Gate",
                "Plan Gate",
                "Delivery Gate",
            ),
            "contributing.md": (
                "RED",
                "GREEN",
                "owner",
                "regressão",
                "documentação",
            ),
            "skills.md": (
                "SKILL.md",
                "description",
                "agents/openai.yaml",
                "handoff",
            ),
            "cli.md": (
                "cli/src/specsfy_cli",
                "catálogo",
                "GitHub",
                "fingerprint",
            ),
        }
        for relative, evidence in required.items():
            with self.subTest(document=relative):
                path = DEVELOP / relative
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8")
                for term in evidence:
                    self.assertIn(term, text)

        for relative in (
            "context/README.md",
            "context/documentation.md",
            "context/architecture/modules.md",
            "context/architecture/dependencies.md",
            "context/engineering/testing.md",
            "context/data/privacy.md",
            "context/flows/README.md",
            "decisions/README.md",
        ):
            self.assertTrue((DEVELOP / relative).is_file(), relative)

    def test_root_agents_and_context_govern_the_two_audiences(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        context_router = (
            DEVELOP / "context" / "README.md"
        ).read_text(encoding="utf-8")
        context_path = DEVELOP / "context" / "documentation.md"

        self.assertIn("docs/README.md", agents)
        self.assertIn("apenas o roteador", agents)
        self.assertIn("conteúdo temático", agents)
        self.assertIn("docs/user/", agents)
        self.assertIn("linguagem simples", agents)
        self.assertIn("docs/develop/", agents)
        self.assertIn("agentes e humanos", agents)
        self.assertIn("atualize os dois percursos", agents)

        self.assertTrue(context_path.is_file())
        self.assertIn("documentation.md", context_router)
        context = context_path.read_text(encoding="utf-8")
        for term in (
            "docs/README.md",
            "docs/user/",
            "docs/develop/",
            "uma página por skill base",
            "linguagem simples",
            "agentes e humanos",
            "ambos os percursos",
        ):
            self.assertIn(term, context)


if __name__ == "__main__":
    unittest.main()

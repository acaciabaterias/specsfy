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
    "specsfy-interviewer",
    "specsfy-mvp-milestone-interviewer",
    "specsfy-roadmap-milestone-interviewer",
    "specsfy-milestone-governor",
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
            "Milestones": "milestones.md",
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

    def test_method_reference_explains_the_transversal_contracts(self) -> None:
        reference = (USER / "method-reference.md").read_text(encoding="utf-8")
        for section in (
            "## A spec como registro único",
            "## Effort",
            "### Faixas e perfis",
            "### Quando atualizar",
            "### Effort não é prioridade",
            "## Estados e transições",
            "### Retornos permitidos",
            "## Gates",
            "### Definition Gate",
            "### Plan Gate",
            "### Delivery Gate",
            "## Anatomia completa da spec",
            "### Ato I: seções 1 a 7",
            "### Ato II: seções 8 a 15",
            "### Ato III: seções 16 a 18",
            "## Identificadores e rastreabilidade",
            "## Tarefas, pesquisa e progresso",
            "## Dúvidas frequentes",
        ):
            with self.subTest(section=section):
                self.assertIn(section, reference)

    def test_system_documentation_explains_generation_and_maintenance(self) -> None:
        guide = (USER / "system-documentation.md").read_text(encoding="utf-8")
        for section in (
            "## O que esta documentação explica",
            "## O que é gerado e o que é preservado",
            "## Como ler cada documento",
            "## Procedimento depois de uma mudança",
            "## Situações que impedem a conclusão",
        ):
            with self.subTest(section=section):
                self.assertIn(section, guide)
        for document in (
            "docs/architecture.md",
            "docs/database.md",
            "docs/flows.md",
            "docs/testing.md",
            "docs/integrations.md",
            ".specsfy/PACKAGES.md",
        ):
            with self.subTest(document=document):
                self.assertIn(document, guide)

    def test_each_public_cli_command_has_a_user_documentation_route(self) -> None:
        cli_source = (ROOT / "cli" / "src" / "cli.ts").read_text(
            encoding="utf-8"
        )
        routes = {
            "install": ("specsfy install", "installation.md"),
            "skills": ("specsfy skills", "cli.md"),
            "transition": ("specsfy transition", "cli.md"),
            "migrate": ("specsfy migrate", "cli.md"),
            "effort": ("specsfy effort", "method-reference.md"),
            "progress": ("specsfy progress", "cli.md"),
            "milestones": ("specsfy milestones", "milestones.md"),
            "test": ("specsfy test", "cli.md"),
            "tui": ("specsfy tui", "cli.md"),
            "config": ("specsfy config", "cli.md"),
        }
        for command, (invocation, route) in routes.items():
            with self.subTest(command=command):
                self.assertIn(f'.command("{command}")', cli_source)
                self.assertIn(
                    invocation,
                    (USER / route).read_text(encoding="utf-8"),
                )

    def test_glossary_defines_the_transversal_method_vocabulary(self) -> None:
        glossary = (DEVELOP / "context" / "glossary.md").read_text(
            encoding="utf-8"
        )
        for term in (
            "Estado operacional",
            "Status",
            "Transição",
            "Effort",
            "Definition Gate",
            "Plan Gate",
            "Delivery Gate",
            "Rastreabilidade",
            "Projeção de progresso",
            "Contexto persistente",
            "Documentação reconstruída",
        ):
            with self.subTest(term=term):
                self.assertIn(f"| {term} |", glossary)

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
                "cli/src/",
                "TypeScript",
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

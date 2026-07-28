from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "specsfy-monorepo-documentator"
CLAUDE_SKILL = ROOT / ".claude" / "skills" / "specsfy-monorepo-documentator"


class MonorepoDocumentationIntegrationTests(unittest.TestCase):
    def test_skill_uses_codex_and_claude_repository_locations(self) -> None:
        self.assertTrue((SKILL / "SKILL.md").is_file())
        self.assertTrue(CLAUDE_SKILL.is_symlink())
        self.assertEqual(SKILL.resolve(), CLAUDE_SKILL.resolve())

    def test_collector_recognizes_the_current_workspace(self) -> None:
        before = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        result = subprocess.run(
            [
                "python3",
                "-B",
                str(SKILL / "scripts" / "collect_monorepo_evidence.py"),
                "--workspace",
                str(ROOT),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertEqual("promovaweb/specsfy", evidence["workspace"])
        self.assertEqual("https://github.com/promovaweb/specsfy", evidence["remote"])
        self.assertEqual(8, len(evidence["modules"]))
        self.assertEqual(before.splitlines(), evidence["changes"])
        after = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(before, after)

    def test_collector_refuses_a_directory_outside_the_monorepo(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    "python3",
                    "-B",
                    str(SKILL / "scripts" / "collect_monorepo_evidence.py"),
                    "--workspace",
                    directory,
                ],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("não representa o monorepo Specsfy", result.stderr)

    def test_monorepo_skill_is_local_and_consumer_documentator_remains_installed(self) -> None:
        contract = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        consumer = (
            ROOT / "skills" / "specsfy-documentator" / "SKILL.md"
        ).read_text(encoding="utf-8")
        installer = (
            ROOT / "cli" / "src" / "specsfy_cli" / "installer.py"
        ).read_text(encoding="utf-8")

        self.assertIn("documenta a metodologia", contract)
        self.assertIn("monorepo", contract)
        self.assertIn("Manter em `docs/`", consumer)
        self.assertNotIn("specsfy-monorepo-documentator", installer)
        self.assertIn('"specsfy-documentator"', installer)
        self.assertFalse(
            (ROOT / "skills" / "specsfy-monorepo-documentator").exists()
        )

    def test_official_docs_publish_technical_and_user_routes(self) -> None:
        standard = (
            SKILL / "references" / "documentation-standard.md"
        ).read_text(encoding="utf-8")
        guide = (ROOT / "docs" / "monorepo-documentation.md").read_text(encoding="utf-8")
        router = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")

        for heading in ("Documentação técnica", "Guias para usuários"):
            self.assertIn(heading, standard)
            self.assertIn(heading, guide)
        self.assertIn("monorepo-documentation.md", router)

    def test_monorepo_skill_publishes_cli_and_framework_installation_guide(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        standard = (
            SKILL / "references" / "documentation-standard.md"
        ).read_text(encoding="utf-8")
        installation_path = ROOT / "docs" / "installation.md"
        router = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        cli_guide = (ROOT / "docs" / "cli.md").read_text(encoding="utf-8")

        for source in (skill, standard):
            self.assertIn("docs/installation.md", source)
        self.assertTrue(installation_path.is_file())

        installation = installation_path.read_text(encoding="utf-8")
        for evidence in (
            "Python 3.11",
            "uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'",
            "specsfy --version",
            "specsfy install --project .",
            ".agents/skills/specsfy-base-*",
            ".specsfy/Spec.md",
        ):
            self.assertIn(evidence, installation)
        self.assertIn("[Guia de instalação](installation.md)", router)
        self.assertIn("[guia de instalação](installation.md)", cli_guide)

    def test_public_entrypoint_and_thematic_guides_cover_the_user_journey(
        self,
    ) -> None:
        public_entrypoint = (ROOT / "specsfy" / "README.md").read_text(
            encoding="utf-8"
        )
        router = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        standard = (
            SKILL / "references" / "documentation-standard.md"
        ).read_text(encoding="utf-8")

        for evidence in (
            "uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'",
            "specsfy --version",
            "specsfy install --project .",
            "uv tool upgrade specsfy-cli",
            "specsfy skills update --project .",
            "specsfy-base-backlog",
            "Ato I — Definir",
            "Ato II — Projetar e provar",
            "Ato III — Entregar",
            "specsfy progress --project .",
            "## Dicas para usar o CLI",
            "specsfy --help",
            "specsfy progress --project . --json",
            "specsfy progress --project . --watch",
            "Nada é instalado ou removido antes de **Aplicar**",
        ):
            self.assertIn(evidence, public_entrypoint)

        base_flow = (
            "$specsfy-base-backlog",
            "$specsfy-base-interview",
            "$specsfy-base-specify",
            "$specsfy-base-validate",
            "$specsfy-base-tasks",
            "$specsfy-base-tdd-bdd",
            "$specsfy-base-implement",
            "$specsfy-base-update-spec",
            "$specsfy-base-progress",
        )
        basic_usage = (ROOT / "docs" / "basic-usage.md").read_text(
            encoding="utf-8"
        )
        for source in (public_entrypoint, basic_usage):
            practical_journey = (
                "### 1. Guarde a ideia — `$specsfy-base-backlog`",
                "### 2. Tire as dúvidas — `$specsfy-base-interview`",
                "### 3. Crie a especificação — `$specsfy-base-specify`",
                "### 4. Confira a especificação — `$specsfy-base-validate`",
                "### 5. Divida o trabalho — `$specsfy-base-tasks`",
                "### 6. Prepare a verificação — `$specsfy-base-tdd-bdd`",
                "### 7. Implemente — `$specsfy-base-implement`",
                "### 8. Altere a especificação — `$specsfy-base-update-spec`",
                "### 9. Veja o progresso — `$specsfy-base-progress`",
            )
            for evidence in practical_journey:
                self.assertIn(evidence, source)
            practical_evidence = (
                "specs/backlog/0001-pagina-boas-vindas.md",
                "Brief pronto para especificar",
                "specs/specs/0001-pagina-boas-vindas/spec.md",
                "READY",
                "2 tarefas preparadas",
                "Verificação preparada",
                "Implementação concluída",
                "Pedido incorporado na especificação 0001-pagina-boas-vindas",
                "Implementação atualizada",
                "Complete",
                "nenhuma pendência",
                "Use $specsfy-base-interview para aprofundar este texto:",
                "Use $specsfy-base-interview em specs/backlog/0001-pagina-boas-vindas.md",
                "Use $specsfy-base-specify para criar uma especificação a partir deste texto:",
                "Use $specsfy-base-specify para promover specs/backlog/0001-pagina-boas-vindas.md",
                "**Opção 1 — texto livre**",
                "**Opção 2 — arquivo de backlog**",
                "Use $specsfy-base-validate em specs/specs/0001-pagina-boas-vindas/spec.md",
                "Use $specsfy-base-tasks em specs/specs/0001-pagina-boas-vindas/spec.md",
                "Use $specsfy-base-tdd-bdd em specs/specs/0001-pagina-boas-vindas/spec.md",
                "Use $specsfy-base-implement em specs/specs/0001-pagina-boas-vindas/spec.md",
            )
            for evidence in practical_evidence:
                self.assertIn(evidence, source)
            for code in ("<?php", "Route::", "test("):
                self.assertNotIn(code, source)
            for skill in base_flow:
                self.assertIn(skill, source)
            positions = [source.index(skill) for skill in base_flow]
            self.assertEqual(sorted(positions), positions)

        guides = {
            "basic-usage.md": ("specsfy-base-backlog", "Definition Gate"),
            "update-spec.md": (
                "specsfy-base-update-spec",
                "esqueci",
                "adicionar",
                "remover",
                "corrigir",
                "mudar",
            ),
            "advanced-usage.md": ("--detected", "--specialist"),
            "repositories.md": (
                "specsfy/",
                "docs/",
                "skills/",
                "specialists/",
                "cli/",
                "example/",
                "brand/",
                "promovaweb/specsfy",
            ),
            "credits.md": ("Promovaweb", "Luiz Eduardo Oliveira Fonseca"),
            "laravel.md": (
                "specsfy-specialist-laravel",
                "artisan",
                "composer.json",
            ),
            "astro.md": (
                "specsfy-specialist-astro",
                "astro.config",
                "package.json",
            ),
            "nextjs.md": (
                "specsfy-specialist-nextjs",
                "next.config",
                "package.json",
            ),
        }
        for filename, evidence in guides.items():
            with self.subTest(guide=filename):
                path = ROOT / "docs" / filename
                self.assertTrue(path.is_file())
                guide = path.read_text(encoding="utf-8")
                self.assertIn(f"]({filename})", router)
                self.assertIn(f"docs/{filename}", standard)
                for term in evidence:
                    self.assertIn(term, guide)

    def test_cli_guide_publishes_the_provided_tui_screenshots(self) -> None:
        cli_guide = (ROOT / "docs" / "cli.md").read_text(encoding="utf-8")
        public_entrypoint = (ROOT / "specsfy" / "README.md").read_text(
            encoding="utf-8"
        )
        screenshots = (
            ("cli-dash.png", "Dashboard Home"),
            ("cli-backlogs.png", "Backlogs"),
            ("cli-specs.png", "Specs"),
            ("cli-skills.png", "Skills"),
        )

        for filename, alt_text in screenshots:
            with self.subTest(screenshot=filename):
                path = ROOT / "docs" / "screen" / "cli" / filename
                self.assertTrue(path.is_file())
                self.assertEqual(b"\x89PNG\r\n\x1a\n", path.read_bytes()[:8])
                self.assertIn(
                    f"![{alt_text}](screen/cli/{filename})",
                    cli_guide,
                )

        self.assertIn(
            "https://raw.githubusercontent.com/promovaweb/specsfy/main/docs/screen/cli/cli-dash.png",
            public_entrypoint,
        )


if __name__ == "__main__":
    unittest.main()

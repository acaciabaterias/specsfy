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
            ROOT / "cli" / "src" / "installer.ts"
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
        guide = (ROOT / "docs" / "develop" / "documentation.md").read_text(
            encoding="utf-8"
        )
        router = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")

        for route in ("docs/user/", "docs/develop/"):
            self.assertIn(route, standard)
            self.assertIn(route, guide)
        self.assertIn("develop/README.md", router)

    def test_monorepo_skill_publishes_cli_and_framework_installation_guide(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        standard = (
            SKILL / "references" / "documentation-standard.md"
        ).read_text(encoding="utf-8")
        installation_path = ROOT / "docs" / "user" / "installation.md"
        router = (ROOT / "docs" / "user" / "README.md").read_text(
            encoding="utf-8"
        )
        cli_guide = (ROOT / "docs" / "user" / "cli.md").read_text(
            encoding="utf-8"
        )

        for source in (skill, standard):
            self.assertIn("docs/user/installation.md", source)
        self.assertTrue(installation_path.is_file())

        installation = installation_path.read_text(encoding="utf-8")
        for evidence in (
            "Node.js 22.12",
            "npm install --global @promovaweb/specsfy",
            "get.specsfy.dev",
            "curl -fL get.specsfy.dev",
            "specsfy --version",
            "specsfy install --project .",
            "specsfy skills list",
            "specsfy progress --project .",
            "## Corrija falhas comuns",
            ".agents/skills/specsfy-01-inbox",
            ".specsfy/Spec.md",
        ):
            self.assertIn(evidence, installation)
        for unnecessary_setup in (
            "## Papel",
            "### Pré-requisitos",
            "gh auth login",
            "uv tool install",
            "git+https://github.com/promovaweb/specsfy",
            "## Atualize quando",
            "## Não use para",
            "## Fonte da verdade e precedência",
            ".specsfy/templates/Inbox.md",
        ):
            self.assertNotIn(unnecessary_setup, installation)
        self.assertIn("[Instalação](installation.md)", router)
        self.assertIn("[guia de instalação](installation.md)", cli_guide)

    def test_public_entrypoint_and_thematic_guides_cover_the_user_journey(
        self,
    ) -> None:
        public_entrypoint = (ROOT / "specsfy" / "README.md").read_text(
            encoding="utf-8"
        )
        router = (ROOT / "docs" / "user" / "README.md").read_text(
            encoding="utf-8"
        )
        standard = (
            SKILL / "references" / "documentation-standard.md"
        ).read_text(encoding="utf-8")

        for evidence in (
            "get.specsfy.dev",
            "specsfy --version",
            "specsfy install --project .",
            "npm update --global @promovaweb/specsfy",
            "specsfy skills update --project .",
            "specsfy-01-inbox",
            "specsfy-02-backlog",
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
            "$specsfy-01-inbox",
            "$specsfy-02-backlog",
            "$specsfy-03-specify",
            "$specsfy-04-validate",
            "$specsfy-05-tasks",
            "$specsfy-06-tdd-bdd",
            "$specsfy-07-implement",
            "$specsfy-update-spec",
            "$specsfy-progress",
            "$specsfy-interviewer",
        )
        basic_usage = (ROOT / "docs" / "user" / "getting-started.md").read_text(
            encoding="utf-8"
        )
        for source in (public_entrypoint, basic_usage):
            practical_evidence = (
                "specs/inbox/2026-07-28-143205-pagina-boas-vindas.md",
                "specs/backlog/0001-pagina-boas-vindas.md",
                "specs/<estado>/0001-pagina-boas-vindas/spec.md",
                "READY",
                "Reviewing",
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
            "getting-started.md": ("specsfy-01-inbox", "Definition Gate"),
            "update-spec.md": (
                "specsfy-update-spec",
                "esqueci",
                "adicionar",
                "remover",
                "corrigir",
                "mudar",
            ),
            "advanced-usage.md": ("--detected", "--specialist"),
            "../develop/modules.md": (
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
                path = ROOT / "docs" / "user" / filename
                self.assertTrue(path.is_file())
                guide = path.read_text(encoding="utf-8")
                self.assertIn(f"]({filename})", router)
                for term in evidence:
                    self.assertIn(term, guide)

    def test_public_cli_download_uses_the_canonical_short_url(self) -> None:
        for relative in (
            "README.md",
            "cli/README.md",
            "specsfy/README.md",
            "skills/README.md",
            "docs/user/installation.md",
        ):
            with self.subTest(path=relative):
                content = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn("`get.specsfy.dev`", content)
                self.assertNotIn("https://get.specsfy.dev", content)

    def test_cli_guide_publishes_the_provided_tui_screenshots(self) -> None:
        cli_guide = (ROOT / "docs" / "user" / "cli.md").read_text(
            encoding="utf-8"
        )
        cli_readme = (ROOT / "cli" / "README.md").read_text(encoding="utf-8")
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
                path = ROOT / "docs" / "user" / "assets" / "cli" / filename
                self.assertTrue(path.is_file())
                self.assertEqual(b"\x89PNG\r\n\x1a\n", path.read_bytes()[:8])
                self.assertIn(
                    f"![{alt_text}](assets/cli/{filename})",
                    cli_guide,
                )

        stacked_screenshots = "\n\n".join(
            f"![{alt_text}](https://promovaweb.com/docs/specsfy/cli/{filename})"
            for filename, alt_text in screenshots
        )
        self.assertIn(stacked_screenshots, cli_readme)

        self.assertIn(
            "![Dashboard Home do Specsfy](../docs/user/assets/cli/cli-dash.png)",
            public_entrypoint,
        )


if __name__ == "__main__":
    unittest.main()

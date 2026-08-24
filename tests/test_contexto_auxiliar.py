from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "specsfy-setup",
    "specsfy-aux-stack",
    "specsfy-aux-rules",
    "specsfy-aux-database",
}


class AuxiliaryContextIntegrationTests(unittest.TestCase):
    def test_catalog_installer_docs_and_framework_publish_same_contract(self) -> None:
        discovered = {
            path.parent.name
            for path in SKILLS.glob("specsfy-*/SKILL.md")
        }
        self.assertTrue(EXPECTED <= discovered)

        installer = (
            ROOT / "cli/src/installer.ts"
        ).read_text(encoding="utf-8")
        guide = (ROOT / "docs/user/project-context.md").read_text(encoding="utf-8")
        framework = (SKILLS / "Spec.md").read_text(encoding="utf-8")
        for name in EXPECTED:
            self.assertIn(f'"{name}"', installer)
            self.assertIn(f"${name}", guide)
        for path in (
            "PROJECT.md",
            "DESIGNSYSTEM.MD",
            ".specsfy/USER-PROFILE.md",
            ".specsfy/STACK.md",
            ".specsfy/RULES.md",
            ".specsfy/DATABASE.md",
        ):
            self.assertIn(path, framework)
            self.assertIn(path, guide)

        for path in (
            ".specify/memory/constitution.md",
            ".specsfy/SPECKIT.md",
        ):
            self.assertIn(path, guide)
            self.assertIn(path, framework)

        setup = (SKILLS / "specsfy-setup/SKILL.md").read_text(encoding="utf-8")
        setup_script = (
            SKILLS / "specsfy-setup/scripts/setup_context.mjs"
        ).read_text(encoding="utf-8")
        self.assertIn("sync_speckit_context.mjs", setup_script)
        self.assertIn('join(project, "DESIGNSYSTEM.MD")', setup_script)
        self.assertIn('join(project, ".specsfy", "USER-PROFILE.md")', setup_script)
        self.assertIn("Nunca", setup)
        self.assertIn("escrever, mover, renomear ou remover", setup)
        self.assertIn("Nas execuções obrigatórias seguintes", setup)
        self.assertIn("pergunta novamente", setup.casefold())
        self.assertIn("iniciante", setup.casefold())
        self.assertIn("experiente", setup.casefold())
        self.assertIn("Antes de iniciar qualquer skill do framework", framework)
        self.assertIn("antes de iniciar cada skill", guide)

    def test_setup_reference_matches_agents_publishable_block(self) -> None:
        agents = (SKILLS / "AGENTS.md").read_text(encoding="utf-8")
        reference = (
            SKILLS / "specsfy-setup/references/framework-instructions.md"
        ).read_text(encoding="utf-8")
        match = re.search(
            r"<!-- specsfy:framework:start -->.*?"
            r"<!-- specsfy:framework:end -->",
            agents,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        reference_match = re.search(
            r"<!-- specsfy:framework:start -->.*?"
            r"<!-- specsfy:framework:end -->",
            reference,
            re.DOTALL,
        )
        self.assertIsNotNone(reference_match)
        self.assertEqual(reference_match.group(0).strip(), match.group(0).strip())

    def test_workflow_skills_share_context_monitor(self) -> None:
        monitor = SKILLS / "specsfy-setup/scripts/monitor_context.mjs"
        self.assertTrue(monitor.is_file())
        content = monitor.read_text(encoding="utf-8")
        for document in (
            ".specsfy/STACK.md",
            ".specsfy/RULES.md",
            ".specsfy/DATABASE.md",
            ".specsfy/USER-PROFILE.md",
            "PROJECT.md",
        ):
            self.assertIn(document, content)
        for name in (
            "specsfy-05-tasks",
            "specsfy-07-implement",
            "specsfy-progress",
        ):
            skill = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("monitor_context.mjs", skill)


if __name__ == "__main__":
    unittest.main()

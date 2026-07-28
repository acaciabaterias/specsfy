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
            ROOT / "cli/src/specsfy_cli/installer.py"
        ).read_text(encoding="utf-8")
        guide = (ROOT / "docs/user/project-context.md").read_text(encoding="utf-8")
        framework = (SKILLS / "Spec.md").read_text(encoding="utf-8")
        for name in EXPECTED:
            self.assertIn(f'"{name}"', installer)
            self.assertIn(f"${name}", guide)
        for path in (
            "PROJECT.md",
            ".specsfy/STACK.md",
            ".specsfy/RULES.md",
            ".specsfy/DATABASE.md",
        ):
            self.assertIn(path, framework)
            self.assertIn(path, guide)

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
        monitor = SKILLS / "specsfy-setup/scripts/monitor_context.py"
        self.assertTrue(monitor.is_file())
        content = monitor.read_text(encoding="utf-8")
        for document in (
            ".specsfy/STACK.md",
            ".specsfy/RULES.md",
            ".specsfy/DATABASE.md",
            "PROJECT.md",
        ):
            self.assertIn(document, content)
        for name in (
            "specsfy-base-tasks",
            "specsfy-base-implement",
            "specsfy-base-progress",
        ):
            skill = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("monitor_context.py", skill)


if __name__ == "__main__":
    unittest.main()

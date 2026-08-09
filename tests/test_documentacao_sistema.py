from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


class SystemDocumentationIntegrationTests(unittest.TestCase):
    def test_documentator_is_installed_and_handed_off_after_implementation(self) -> None:
        installer = (
            ROOT / "cli/src/installer.ts"
        ).read_text(encoding="utf-8")
        implementation = (
            SKILLS / "specsfy-07-implement/SKILL.md"
        ).read_text(encoding="utf-8")
        framework = (SKILLS / "Spec.md").read_text(encoding="utf-8")

        self.assertIn('"specsfy-documentator"', installer)
        self.assertIn("$specsfy-documentator", implementation)
        self.assertIn("$specsfy-documentator", framework)
        self.assertIn("Depois de cada tarefa", implementation)

    def test_documentator_publishes_complete_rebuild_contract(self) -> None:
        skill = (
            SKILLS / "specsfy-documentator" / "SKILL.md"
        ).read_text(encoding="utf-8")
        builder = (
            SKILLS
            / "specsfy-documentator"
            / "scripts"
            / "build_documentation.mjs"
        ).read_text(encoding="utf-8")
        guide = (ROOT / "docs/user/system-documentation.md").read_text(
            encoding="utf-8"
        )

        for term in (
            "arquitetura",
            "banco",
            "fluxos",
            "testes",
            "React",
            "Tailwind",
            "pacotes",
            "GitHub",
        ):
            self.assertIn(term, skill + builder + guide)
        for diagram in (
            "flowchart",
            "classDiagram",
            "erDiagram",
            "sequenceDiagram",
        ):
            self.assertIn(diagram, builder)
        self.assertIn("--check", skill)

    def test_monitor_requires_generated_docs_for_application_or_database(self) -> None:
        monitor = (
            SKILLS / "specsfy-setup" / "scripts" / "monitor_context.mjs"
        ).read_text(encoding="utf-8")
        self.assertIn("documentation_review_required", monitor)
        self.assertIn("specsfy-documentator", monitor)
        self.assertIn('"docs/"', monitor)


if __name__ == "__main__":
    unittest.main()

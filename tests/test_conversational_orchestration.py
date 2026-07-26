from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_SKILLS = (
    "specsfy-base-backlog",
    "specsfy-base-interview",
    "specsfy-base-specify",
    "specsfy-base-validate",
    "specsfy-base-tasks",
    "specsfy-base-tdd-bdd",
    "specsfy-base-implement",
    "specsfy-base-progress",
)


class ConversationalOrchestrationIntegrationTests(unittest.TestCase):
    def test_executable_contract_and_user_docs_publish_same_handoff_policy(
        self,
    ) -> None:
        framework = (ROOT / "skills" / "Spec.md").read_text(encoding="utf-8")
        skills_readme = (ROOT / "skills" / "README.md").read_text(
            encoding="utf-8"
        )
        docs_readme = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        flow = (ROOT / "docs" / "context" / "flows" / "README.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("## Orquestração conversacional", framework)
        self.assertIn("## Orquestração conversacional", skills_readme)
        self.assertIn("## Conversa contínua entre etapas", docs_readme)
        self.assertIn("avanço", flow)
        self.assertIn("retorno", flow)
        self.assertIn("confirmação", flow)
        self.assertIn("mesma conversa", flow)

    def test_all_base_skills_implement_the_integrated_policy(self) -> None:
        for name in BASE_SKILLS:
            with self.subTest(skill=name):
                content = (
                    ROOT / "skills" / name / "SKILL.md"
                ).read_text(encoding="utf-8")
                normalized = " ".join(content.split())

                self.assertIn("## Orquestrar a conversa", content)
                self.assertIn("Transição proposta:", content)
                self.assertIn("Pendência detectada:", content)
                self.assertIn("confirmação", normalized)
                self.assertIn("mesma conversa", normalized)
                self.assertIn("não a invoque", normalized)


if __name__ == "__main__":
    unittest.main()

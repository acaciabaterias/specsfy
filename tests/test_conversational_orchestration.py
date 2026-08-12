from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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


class ConversationalOrchestrationIntegrationTests(unittest.TestCase):
    def test_executable_contract_and_user_docs_publish_same_handoff_policy(
        self,
    ) -> None:
        framework = (ROOT / "skills" / "Spec.md").read_text(encoding="utf-8")
        skills_readme = (ROOT / "skills" / "README.md").read_text(
            encoding="utf-8"
        )
        docs_readme = (ROOT / "docs" / "user" / "README.md").read_text(
            encoding="utf-8"
        )
        flow = (
            ROOT / "docs" / "develop" / "context" / "flows" / "README.md"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn("## Orquestração conversacional", framework)
        self.assertIn("## Orquestração conversacional", skills_readme)
        self.assertIn("## Conversa contínua entre etapas", docs_readme)
        self.assertIn("avanço", flow)
        self.assertIn("retorno", flow)
        self.assertIn("retomada", flow)
        self.assertIn("automaticamente", flow)
        self.assertIn("mesma conversa", flow)

    def test_all_base_skills_implement_the_integrated_policy(self) -> None:
        for name in BASE_SKILLS[1:]:
            with self.subTest(skill=name):
                content = (
                    ROOT / "skills" / name / "SKILL.md"
                ).read_text(encoding="utf-8")
                normalized = " ".join(content.split())

                self.assertIn("## Orquestrar a conversa", content)
                self.assertIn("Transição automática:", content)
                self.assertIn("Retomada automática:", normalized)
                self.assertIn("Pendência detectada:", content)
                self.assertIn("sem pedir confirmação", normalized)
                self.assertIn("carregue imediatamente a skill de destino", normalized)
                self.assertIn("mesma conversa", normalized)

    def test_late_change_has_one_public_and_executable_entrypoint(self) -> None:
        implement = (
            ROOT / "skills" / "specsfy-07-implement" / "SKILL.md"
        ).read_text(encoding="utf-8")
        update = (
            ROOT / "skills" / "specsfy-update-spec" / "SKILL.md"
        ).read_text(encoding="utf-8")
        advanced = (ROOT / "docs" / "user" / "advanced-usage.md").read_text(
            encoding="utf-8"
        )
        entrypoint = (ROOT / "specsfy" / "README.md").read_text(encoding="utf-8")

        for source in (implement, advanced, entrypoint):
            self.assertIn("$specsfy-update-spec", source)
        self.assertIn("esqueceu", update)
        self.assertIn("reabr", update)

    def test_backlog_loop_is_consistent_across_contract_and_user_docs(
        self,
    ) -> None:
        sources = (
            ROOT / "skills" / "Spec.md",
            ROOT / "skills" / "specsfy-02-backlog" / "SKILL.md",
            ROOT / "docs" / "user" / "skills" / "specsfy-02-backlog.md",
            ROOT / "docs" / "user" / "method.md",
        )

        for path in sources:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                normalized = " ".join(content.split()).casefold()
                self.assertIn("sem limite máximo", normalized)
                self.assertTrue(
                    "pelo menos três perguntas numeradas" in normalized
                    or "pelo menos três lacunas reais" in normalized
                )
                self.assertIn("`avançar`", normalized)
                self.assertIn("encerr", normalized)
                self.assertTrue(
                    "responder depois" in normalized
                    or "responde depois" in normalized
                )

        backlog = sources[1].read_text(encoding="utf-8")
        self.assertIn("contexto acumulado e as novas respostas", backlog)
        self.assertIn("Área encerrada pelo usuário", backlog)
        self.assertIn("Área adiada pelo usuário", backlog)
        self.assertIn("Definition Gate: Pending", backlog)


if __name__ == "__main__":
    unittest.main()

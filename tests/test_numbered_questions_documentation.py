from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONING_SKILLS = (
    "specsfy-02-backlog",
    "specsfy-03-specify",
    "specsfy-04-validate",
    "specsfy-05-tasks",
    "specsfy-06-tdd-bdd",
    "specsfy-07-implement",
    "specsfy-aux-rules",
    "specsfy-interviewer",
    "specsfy-milestone-governor",
    "specsfy-mvp-milestone-interviewer",
    "specsfy-data-discovery",
    "specsfy-roadmap-milestone-interviewer",
    "specsfy-setup",
    "specsfy-update-spec",
)
NON_QUESTIONING_SKILLS = (
    "specsfy-01-inbox",
    "specsfy-aux-database",
    "specsfy-aux-stack",
    "specsfy-documentator",
    "specsfy-progress",
)


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class NumberedQuestionsDocumentationTests(unittest.TestCase):
    """Mantém documentação de usuário e técnica alinhada ao contrato."""

    def test_user_documentation_explains_the_complete_response_format(self) -> None:
        documentation = read("docs/user/skills/README.md")
        normalized = " ".join(documentation.split())
        for expected in (
            "Pergunta 1",
            "três respostas sugeridas",
            "Escrever outra resposta",
            "Gere outras opções",
            "Avançar",
            "primeira rodada",
            "encerrar definitivamente",
            "responder depois",
            "reabra",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, normalized)

    def test_technical_documentation_lists_every_interaction_mode(self) -> None:
        documentation = read("docs/develop/skills.md")
        self.assertIn("## Modos de interação", documentation)
        for skill in QUESTIONING_SKILLS + NON_QUESTIONING_SKILLS:
            with self.subTest(skill=skill):
                self.assertIn(f"`{skill}`", documentation)

    def test_canonical_contract_and_documentation_use_the_same_choices(self) -> None:
        contract = read("skills/Spec.md")
        technical = read("docs/develop/skills.md")
        for expected in (
            "Pergunta 1",
            "Escrever outra resposta",
            "Gere outras opções",
            "Avançar",
            "Área encerrada pelo usuário",
            "Área adiada pelo usuário",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, contract)
                self.assertIn(expected, technical)


if __name__ == "__main__":
    unittest.main()

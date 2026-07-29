from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class BacklogLoopContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.backlog = (
            ROOT / "skills" / "specsfy-02-backlog" / "SKILL.md"
        ).read_text(encoding="utf-8")
        cls.mcr = (
            ROOT
            / "skills"
            / "specsfy-03-specify"
            / "references"
            / "mcr-10.md"
        ).read_text(encoding="utf-8")
        cls.specify = (
            ROOT / "skills" / "specsfy-03-specify" / "SKILL.md"
        ).read_text(encoding="utf-8")
        cls.update_spec = (
            ROOT / "skills" / "specsfy-update-spec" / "SKILL.md"
        ).read_text(encoding="utf-8")

    def test_backlog_reanalyses_every_answer_without_question_limit(self) -> None:
        for source in (self.backlog, self.mcr):
            with self.subTest(source=source[:40]):
                self.assertIn("sem limite máximo de perguntas", source)
                self.assertIn("contexto acumulado e a nova resposta", source)
                self.assertIn("enquanto existir lacuna aplicável", source)

    def test_advance_is_offered_only_after_ten_questions(self) -> None:
        for source in (self.backlog, self.mcr):
            with self.subTest(source=source[:40]):
                self.assertIn("A partir da 11ª pergunta", source)
                self.assertIn("`avançar`", source)

    def test_advance_preserves_open_gaps_and_pending_definition(self) -> None:
        self.assertIn("encerre somente o ciclo atual", self.backlog)
        self.assertIn("lacunas não resolvidas", self.backlog)
        self.assertIn("Status: Draft", self.backlog)
        self.assertIn("Definition Gate: Pending", self.backlog)

    def test_definition_skills_delegate_material_questions_to_backlog(self) -> None:
        self.assertIn(
            "carregue `$specsfy-02-backlog` para executar o ciclo",
            self.specify,
        )
        self.assertIn(
            "retome esta skill ao final do ciclo",
            self.specify,
        )
        self.assertIn(
            "retome esta skill ao final do ciclo",
            self.update_spec,
        )

    def test_advance_does_not_immediately_reopen_the_same_loop(self) -> None:
        validate = (
            ROOT / "skills" / "specsfy-04-validate" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for source in (self.specify, self.update_spec, validate):
            with self.subTest(source=source[:40]):
                self.assertIn("não reabra o mesmo ciclo", source)


if __name__ == "__main__":
    unittest.main()

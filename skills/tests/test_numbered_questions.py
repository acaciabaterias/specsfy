from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
QUESTIONING_SKILLS = {
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
    "specsfy-roadmap-milestone-interviewer",
    "specsfy-setup",
    "specsfy-update-spec",
    "specsfy-data-discovery",
}
NON_QUESTIONING_SKILLS = {
    "specsfy-01-inbox",
    "specsfy-aux-database",
    "specsfy-aux-stack",
    "specsfy-documentator",
    "specsfy-progress",
}


class NumberedQuestionsContractTest(unittest.TestCase):
    def skill_source(self, name: str) -> str:
        return (ROOT / name / "SKILL.md").read_text(encoding="utf-8")

    def test_every_skill_declares_its_interaction_mode(self) -> None:
        skill_names = {
            path.parent.name for path in ROOT.glob("*/SKILL.md")
        }
        self.assertEqual(
            skill_names,
            QUESTIONING_SKILLS | NON_QUESTIONING_SKILLS,
        )

        for name in QUESTIONING_SKILLS:
            source = self.skill_source(name)
            self.assertIn("Modo de interação: `perguntas`.", source, name)
            self.assertIn("Contrato de perguntas numeradas", source, name)

        for name in NON_QUESTIONING_SKILLS:
            source = self.skill_source(name)
            self.assertIn("Modo de interação: `sem perguntas`.", source, name)

    def test_central_contract_defines_the_complete_round(self) -> None:
        contract = (ROOT / "Spec.md").read_text(encoding="utf-8")
        for required in (
            "## Contrato de perguntas numeradas",
            "exatamente uma pergunta numerada por rodada",
            "pelo menos três opções numeradas",
            "`Escrever outra resposta`",
            "`Gere outras opções`",
            "`Avançar`",
            "desde a primeira rodada",
            "Pergunta 1",
            "encerrar definitivamente",
            "responder depois",
            "Área encerrada pelo usuário",
            "Área adiada pelo usuário",
            "Português do Brasil",
            "texto completo da opção",
            "no máximo oito perguntas por área",
        ):
            self.assertIn(required, contract)

    def test_questioning_skills_do_not_keep_the_previous_protocol(self) -> None:
        for name in QUESTIONING_SKILLS:
            source = self.skill_source(name)
            self.assertNotIn("pelo menos três perguntas numeradas", source, name)
            self.assertNotIn("A partir da 11ª pergunta", source, name)
            self.assertNotIn("Antes disso, não ofereça essa saída", source, name)


if __name__ == "__main__":
    unittest.main()

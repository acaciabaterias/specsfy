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


class ConversationalOrchestrationTests(unittest.TestCase):
    def test_framework_defines_automatic_bidirectional_handoffs(self) -> None:
        framework = (ROOT / "Spec.md").read_text(encoding="utf-8")
        normalized = " ".join(framework.split())

        self.assertIn("## Orquestração conversacional", framework)
        self.assertIn("Transição automática:", framework)
        self.assertIn("Retomada automática:", framework)
        self.assertIn("Pendência detectada:", framework)
        self.assertIn("sem pedir confirmação", normalized)
        self.assertIn("mesma conversa", normalized)
        self.assertIn("não peça que a pessoa repita o comando", normalized)
        self.assertIn("retorno", normalized)

    def test_every_base_skill_can_be_loaded_by_an_automatic_handoff(self) -> None:
        for name in BASE_SKILLS[1:]:
            with self.subTest(skill=name):
                skill = (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                metadata = (
                    ROOT / name / "agents" / "openai.yaml"
                ).read_text(encoding="utf-8")
                description = skill.split("---", 2)[1]
                normalized = " ".join(skill.split())

                self.assertIn("transição automática", description)
                self.assertIn("## Orquestrar a conversa", skill)
                self.assertIn("Transição automática:", skill)
                self.assertIn("Retomada automática:", normalized)
                self.assertIn("Pendência detectada:", skill)
                self.assertIn("carregue imediatamente a skill de destino", normalized)
                self.assertIn("sem pedir confirmação", normalized)
                self.assertIn("mesma conversa", normalized)
                self.assertIn("transições", metadata)
                self.assertIn("automáticas", metadata)

    def test_handoff_is_automatic_but_sensitive_actions_remain_explicit(self) -> None:
        framework = (ROOT / "Spec.md").read_text(encoding="utf-8")
        normalized = " ".join(framework.split())

        self.assertIn("não peça confirmação para o handoff", normalized.lower())
        self.assertIn("autorização específica", normalized)
        self.assertIn("ações destrutivas", normalized)
        self.assertIn("instalação de especialista", normalized)

    def test_specialist_handoffs_separate_loading_from_installation(self) -> None:
        references = sorted(ROOT.glob("specsfy-*/references/specialists.md"))

        self.assertEqual(7, len(references))
        for path in references:
            with self.subTest(reference=path.parent.parent.name):
                normalized = " ".join(
                    path.read_text(encoding="utf-8").split()
                )
                self.assertIn("transição automática", normalized)
                self.assertIn("mesma conversa", normalized)
                self.assertIn("instal", normalized)

    def test_missing_red_reopens_the_plan_before_automatic_tdd(self) -> None:
        framework = " ".join((ROOT / "Spec.md").read_text(encoding="utf-8").split())
        implement = " ".join(
            (ROOT / "specsfy-07-implement" / "SKILL.md")
            .read_text(encoding="utf-8")
            .split()
        )
        tasks = " ".join(
            (ROOT / "specsfy-05-tasks" / "SKILL.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("Plan Gate já estiver `Passed`", framework)
        self.assertIn("retorne automaticamente para `$specsfy-05-tasks`", implement)
        self.assertIn("`Defined`, `Planned` ou `Implementing`", tasks)
        self.assertIn("reabra o Ato II", tasks)
        self.assertIn("chame automaticamente `$specsfy-06-tdd-bdd`", tasks)

    def test_main_chain_and_critical_returns_name_automatic_destinations(
        self,
    ) -> None:
        skills = {
            name: " ".join(
                (ROOT / name / "SKILL.md").read_text(encoding="utf-8").split()
            )
            for name in BASE_SKILLS
        }

        expected_routes = {
            "specsfy-01-inbox": "$specsfy-02-backlog",
            "specsfy-02-backlog": "$specsfy-03-specify",
            "specsfy-03-specify": "$specsfy-04-validate",
            "specsfy-04-validate": "$specsfy-05-tasks",
            "specsfy-05-tasks": "$specsfy-06-tdd-bdd",
            "specsfy-06-tdd-bdd": "$specsfy-05-tasks",
            "specsfy-07-implement": "$specsfy-progress",
            "specsfy-update-spec": "$specsfy-04-validate",
        }
        for source, destination in expected_routes.items():
            with self.subTest(source=source, destination=destination):
                self.assertIn(destination, skills[source])

        self.assertIn(
            "carregue automaticamente `$specsfy-update-spec`",
            skills["specsfy-07-implement"],
        )
        self.assertIn(
            "carregue automaticamente `$specsfy-update-spec`",
            skills["specsfy-progress"],
        )
        for source in (
            "specsfy-02-backlog",
            "specsfy-04-validate",
            "specsfy-05-tasks",
        ):
            with self.subTest(late_change_return=source):
                self.assertIn(
                    "$specsfy-update-spec",
                    skills[source],
                )

    def test_update_spec_is_the_obvious_entrypoint_for_late_changes(self) -> None:
        skill = (
            ROOT / "specsfy-update-spec" / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(skill.split())
        description = skill.split("---", 2)[1]

        for trigger in ("esqueceu", "adicionar", "remover", "corrigir", "mudar"):
            self.assertIn(trigger, description)
        self.assertIn("spec existente", description)
        self.assertIn("não cria uma spec nova", normalized)
        self.assertIn("não implementa", normalized)
        self.assertIn("$specsfy-02-backlog", normalized)
        self.assertIn("$specsfy-04-validate", normalized)
        self.assertIn("$specsfy-05-tasks", normalized)
        self.assertIn("analyze_change.mjs", skill)


if __name__ == "__main__":
    unittest.main()

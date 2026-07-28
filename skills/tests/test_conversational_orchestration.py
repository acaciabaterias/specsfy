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
    "specsfy-base-update-spec",
    "specsfy-base-progress",
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
        for name in BASE_SKILLS:
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
        references = sorted(ROOT.glob("specsfy-base-*/references/specialists.md"))

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
            (ROOT / "specsfy-base-implement" / "SKILL.md")
            .read_text(encoding="utf-8")
            .split()
        )
        tasks = " ".join(
            (ROOT / "specsfy-base-tasks" / "SKILL.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("Plan Gate já estiver `Passed`", framework)
        self.assertIn("retorne automaticamente para `$specsfy-base-tasks`", implement)
        self.assertIn("`Defined`, `Planned` ou `Implementing`", tasks)
        self.assertIn("reabra o Ato II", tasks)
        self.assertIn("chame automaticamente `$specsfy-base-tdd-bdd`", tasks)

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
            "specsfy-base-backlog": "$specsfy-base-interview",
            "specsfy-base-interview": "$specsfy-base-specify",
            "specsfy-base-specify": "$specsfy-base-validate",
            "specsfy-base-validate": "$specsfy-base-tasks",
            "specsfy-base-tasks": "$specsfy-base-tdd-bdd",
            "specsfy-base-tdd-bdd": "$specsfy-base-tasks",
            "specsfy-base-implement": "$specsfy-base-progress",
            "specsfy-base-update-spec": "$specsfy-base-validate",
        }
        for source, destination in expected_routes.items():
            with self.subTest(source=source, destination=destination):
                self.assertIn(destination, skills[source])

        self.assertIn(
            "carregue automaticamente `$specsfy-base-update-spec`",
            skills["specsfy-base-implement"],
        )
        self.assertIn(
            "carregue automaticamente `$specsfy-base-update-spec`",
            skills["specsfy-base-progress"],
        )
        for source in (
            "specsfy-base-interview",
            "specsfy-base-validate",
            "specsfy-base-tasks",
        ):
            with self.subTest(late_change_return=source):
                self.assertIn(
                    "$specsfy-base-update-spec",
                    skills[source],
                )

    def test_update_spec_is_the_obvious_entrypoint_for_late_changes(self) -> None:
        skill = (
            ROOT / "specsfy-base-update-spec" / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(skill.split())
        description = skill.split("---", 2)[1]

        for trigger in ("esqueceu", "adicionar", "remover", "corrigir", "mudar"):
            self.assertIn(trigger, description)
        self.assertIn("spec existente", description)
        self.assertIn("não cria uma spec nova", normalized)
        self.assertIn("não implementa", normalized)
        self.assertIn("$specsfy-base-interview", normalized)
        self.assertIn("$specsfy-base-validate", normalized)
        self.assertIn("$specsfy-base-tasks", normalized)
        self.assertIn("analyze_change.py", skill)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FrameworkFileTests(unittest.TestCase):
    def test_root_files_publish_loadable_framework_rules(self) -> None:
        spec = ROOT / "Spec.md"
        template = ROOT / "templates/Spec.md"
        example = ROOT / "examples/Spec.md"
        agents = ROOT / "AGENTS.md"
        claude = ROOT / "CLAUDE.md"

        self.assertTrue(spec.is_file())
        self.assertIn("specs/backlog/", spec.read_text(encoding="utf-8"))
        self.assertIn("specs/specs/", spec.read_text(encoding="utf-8"))
        self.assertTrue(template.is_file())
        template_content = template.read_text(encoding="utf-8")
        self.assertIn("{{SPEC_NAME}}", template_content)
        self.assertIn("| Campo | Valor |", template_content)
        self.assertNotIn("**Formato**:", template_content)
        self.assertTrue(example.is_file())
        example_content = example.read_text(encoding="utf-8")
        self.assertNotIn("{{", example_content)
        self.assertIn("| Campo | Valor |", example_content)
        self.assertNotIn("**Formato**:", example_content)
        self.assertEqual(3, example_content.count("## Ato "))
        self.assertEqual(
            18,
            sum(
                line.startswith("### ")
                and line[4:6].rstrip(".").isdigit()
                for line in example_content.splitlines()
            ),
        )
        agents_content = agents.read_text(encoding="utf-8")
        self.assertIn("<!-- specsfy:framework:start -->", agents_content)
        self.assertIn("{{SPECSFY_SPEC_PATH}}", agents_content)
        self.assertTrue(claude.is_file())
        self.assertIn("@Spec.md", claude.read_text(encoding="utf-8"))

    def test_framework_routes_agents_to_canonical_project_context(self) -> None:
        spec = (ROOT / "Spec.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        instructions = (
            ROOT / "specsfy-setup/references/framework-instructions.md"
        ).read_text(encoding="utf-8")
        for path in (
            "PROJECT.md",
            ".specsfy/STACK.md",
            ".specsfy/RULES.md",
            ".specsfy/DATABASE.md",
        ):
            self.assertIn(path, spec)
        self.assertIn("$specsfy-setup", spec)
        self.assertIn("$specsfy-aux-database", spec)
        self.assertIn("Antes de iniciar qualquer skill do framework", spec)
        self.assertIn("não se chama recursivamente", spec)
        self.assertIn("transição automática", spec)
        self.assertIn("Antes de iniciar qualquer skill do framework", agents)
        self.assertIn("Antes de iniciar qualquer skill do framework", instructions)

    def test_todas_as_skills_operacionais_carregam_o_setup(self) -> None:
        setup = ROOT / "specsfy-setup" / "SKILL.md"
        self.assertTrue(setup.is_file())

        skills = sorted(ROOT.glob("specsfy-*/SKILL.md"))
        self.assertGreater(len(skills), 1)
        for skill in skills:
            if skill == setup:
                continue
            with self.subTest(skill=skill.parent.name):
                content = skill.read_text(encoding="utf-8")
                self.assertIn("## Preparação obrigatória", content)
                self.assertIn(
                    "Antes de executar esta skill, carregue obrigatoriamente "
                    "`$specsfy-setup`",
                    content,
                )
                self.assertIn("Em handoff automático, carregue-o de novo", content)

    def test_bdd_runner_contract_is_stack_aware(self) -> None:
        tdd_skill = (
            ROOT / "specsfy-06-tdd-bdd" / "SKILL.md"
        ).read_text(encoding="utf-8")
        tasks_skill = (
            ROOT / "specsfy-05-tasks" / "SKILL.md"
        ).read_text(encoding="utf-8")
        verifier = (
            ROOT / "specsfy-04-validate" / "scripts" / "verify_repo.mjs"
        ).read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("PHP", tdd_skill)
        self.assertIn("Pest", tdd_skill)
        self.assertIn("Node", tdd_skill)
        self.assertIn("Vitest", tdd_skill)
        self.assertIn("SPECSFY:", tdd_skill)
        self.assertIn("referência", tdd_skill)
        self.assertNotIn("Cucumber.js", tdd_skill)
        self.assertNotIn("[BDD]", tasks_skill)
        self.assertNotIn('shutil.which("behave")', verifier)
        self.assertNotIn("behave behave", agents)
        self.assertNotIn("behave behave", readme)


if __name__ == "__main__":
    unittest.main()

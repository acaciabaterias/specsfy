from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "specsfy-base-validate/scripts/verify_repo.py"
SPEC = importlib.util.spec_from_file_location("verify_repo", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
VERIFY_REPO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY_REPO)


class VerifyRepositoryTests(unittest.TestCase):
    def create_skill(self, root: Path, name: str) -> None:
        skill = root / ".agents" / "skills" / name
        (skill / "agents").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Skill de teste.\n---\n",
            encoding="utf-8",
        )
        (skill / "agents/openai.yaml").write_text(
            "interface:\n  display_name: Test\n",
            encoding="utf-8",
        )

    def test_skill_check_accepts_base_catalog_with_specialists(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for number in range(10):
                self.create_skill(root, f"specsfy-base-example-{number}")
            for number in range(2):
                self.create_skill(root, f"specsfy-specialist-example-{number}")
            self.create_skill(root, "specsfy-setup")
            self.create_skill(root, "specsfy-documentator")
            for name in ("stack", "rules", "database"):
                self.create_skill(root, f"specsfy-aux-{name}")

            result = VERIFY_REPO.skill_check(root)

            self.assertEqual("passed", result["status"])
            self.assertEqual(
                "17 skills válidas (10 base, 3 auxiliares, 1 setup, "
                "1 documentador, "
                "2 especialistas)",
                result["detail"],
            )

    def test_skill_check_accepts_source_checkout_catalog(self) -> None:
        result = VERIFY_REPO.skill_check(ROOT)

        self.assertEqual("passed", result["status"])
        self.assertIn("10 base", result["detail"])
        self.assertIn("3 auxiliares", result["detail"])
        self.assertIn("1 setup", result["detail"])
        self.assertIn("1 documentador", result["detail"])

    def test_php_project_selects_pest_even_when_node_is_also_present(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "composer.json").write_text(
                '{"require-dev":{"pestphp/pest":"^4.0"}}',
                encoding="utf-8",
            )
            (root / "package.json").write_text(
                '{"scripts":{"test:tdd":"vitest run"}}',
                encoding="utf-8",
            )
            (root / "artisan").write_text("", encoding="utf-8")

            policy = VERIFY_REPO.tdd_policy(root)

            self.assertEqual("pest", policy["runner"])
            self.assertEqual(["php", "artisan", "test", "--compact"], policy["command"])
            self.assertIsNone(policy["question"])

    def test_node_project_without_bdd_script_requires_user_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "package.json").write_text(
                '{"scripts":{"test":"node --test"}}',
                encoding="utf-8",
            )

            policy = VERIFY_REPO.tdd_policy(root)

            self.assertEqual("node-undecided", policy["runner"])
            self.assertIsNone(policy["command"])
            self.assertIn("pergunte", policy["question"].lower())
            self.assertIn("vitest", policy["suggestion"].lower())
            self.assertNotIn("cucumber", policy["suggestion"].lower())

    def test_node_project_runs_explicit_bdd_script_after_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "package.json").write_text(
                '{"scripts":{"test:tdd":"vitest run tests/tdd"}}',
                encoding="utf-8",
            )

            policy = VERIFY_REPO.tdd_policy(root)

            self.assertEqual("node", policy["runner"])
            self.assertEqual(["npm", "run", "test:tdd"], policy["command"])
            self.assertIsNone(policy["question"])

    def test_node_project_rejects_feature_file_runner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "package.json").write_text(
                '{"scripts":{"test:tdd":"cucumber-js tests/features"}}',
                encoding="utf-8",
            )

            policy = VERIFY_REPO.tdd_policy(root)

            self.assertEqual("node-reference-violation", policy["runner"])
            self.assertIsNone(policy["command"])
            self.assertIn("vitest", policy["suggestion"].lower())


if __name__ == "__main__":
    unittest.main()

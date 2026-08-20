from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_SKILLS = {
    "specsfy-01-inbox",
    "specsfy-02-backlog",
    "specsfy-03-specify",
    "specsfy-04-validate",
    "specsfy-05-tasks",
    "specsfy-06-tdd-bdd",
    "specsfy-07-implement",
    "specsfy-update-spec",
    "specsfy-progress",
    "specsfy-interviewer",
    "specsfy-mvp-milestone-interviewer",
    "specsfy-roadmap-milestone-interviewer",
    "specsfy-milestone-governor",
    "specsfy-data-discovery",
}
CONTEXT_SKILLS = {
    "specsfy-setup",
    "specsfy-aux-stack",
    "specsfy-aux-rules",
    "specsfy-aux-database",
}
DOCUMENTATION_SKILLS = {"specsfy-documentator"}
FRAMEWORK_SKILLS = BASE_SKILLS | CONTEXT_SKILLS | DOCUMENTATION_SKILLS
LEGACY_SKILLS = {
    "specsfy-base-idea",
    "specsfy-base-backlog",
    "specsfy-base-interview",
    "specsfy-base-specify",
    "specsfy-base-validate",
    "specsfy-base-tasks",
    "specsfy-base-tdd-bdd",
    "specsfy-base-implement",
    "specsfy-base-update-spec",
    "specsfy-base-progress",
    "specsfy-base-discuss",
}


class BaseCatalogTests(unittest.TestCase):
    def test_base_catalog_uses_explicit_namespace(self) -> None:
        discovered = {
            path.parent.name
            for path in ROOT.glob("*/SKILL.md")
            if path.parent.name.startswith("specsfy-")
        }
        self.assertEqual(FRAMEWORK_SKILLS, discovered)
        self.assertFalse(LEGACY_SKILLS & discovered)

    def test_frontmatter_folder_and_openai_prompt_agree(self) -> None:
        for name in sorted(FRAMEWORK_SKILLS):
            with self.subTest(skill=name):
                skill = ROOT / name
                content = (skill / "SKILL.md").read_text(encoding="utf-8")
                metadata = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
                match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
                self.assertIsNotNone(match)
                self.assertEqual(name, match.group(1).strip())
                self.assertIn(f"${name}", metadata)

    def test_catalog_contains_no_legacy_skill_references(self) -> None:
        for name in LEGACY_SKILLS:
            with self.subTest(skill=name):
                self.assertFalse((ROOT / name).exists())


if __name__ == "__main__":
    unittest.main()

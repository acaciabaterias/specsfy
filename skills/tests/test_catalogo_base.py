from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_SKILLS = {
    "specsfy-base-backlog",
    "specsfy-base-interview",
    "specsfy-base-specify",
    "specsfy-base-validate",
    "specsfy-base-tasks",
    "specsfy-base-tdd-bdd",
    "specsfy-base-implement",
    "specsfy-base-update-spec",
    "specsfy-base-progress",
}
CONTEXT_SKILLS = {
    "specsfy-setup",
    "specsfy-aux-stack",
    "specsfy-aux-rules",
    "specsfy-aux-database",
}
DOCUMENTATION_SKILLS = {"specsfy-documentator"}
FRAMEWORK_SKILLS = BASE_SKILLS | CONTEXT_SKILLS | DOCUMENTATION_SKILLS
LEGACY_SKILLS = {name.replace("specsfy-base-", "specsfy-") for name in BASE_SKILLS}


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
        legacy_pattern = re.compile(
            r"(?<!base-)specsfy-(backlog|interview|discuss|specify|validate|tasks|tdd-bdd|implement|progress)"
        )
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            if path == Path(__file__):
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(legacy_pattern.search(content))


if __name__ == "__main__":
    unittest.main()

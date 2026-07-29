from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from specsfy_cli.skill_lock import (
    empty_skills_lock,
    ensure_skills_lock,
    installed_skill_names,
    read_skills_lock,
)


class SkillLockTests(unittest.TestCase):
    def test_creates_official_compatible_empty_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)

            payload = ensure_skills_lock(project)

            self.assertEqual(empty_skills_lock(), payload)
            self.assertEqual(
                {"version": 1, "skills": {}},
                json.loads((project / "skills-lock.json").read_text(encoding="utf-8")),
            )

    def test_reads_installed_skills_from_project_root_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "skills-lock.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "skills": {
                            "specsfy-02-backlog": {
                                "source": "skills/",
                                "sourceType": "github",
                                "computedHash": "abc",
                            },
                            "external-skill": {
                                "source": "vendor/repository",
                                "sourceType": "github",
                                "computedHash": "def",
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                {"specsfy-02-backlog", "external-skill"},
                installed_skill_names(project),
            )

    def test_rejects_incompatible_lock_without_overwriting_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            lock = project / "skills-lock.json"
            lock.write_text('{"schema_version": 1, "skills": []}', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "versão de lock"):
                read_skills_lock(project)

            self.assertEqual(
                '{"schema_version": 1, "skills": []}',
                lock.read_text(encoding="utf-8"),
            )

    def test_refuses_to_create_lock_in_orchestrator_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "AGENTS.md").write_text(
                "# Specsfy\n\nmonorepo oficial do Specsfy\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "monorepo oficial"):
                ensure_skills_lock(project)

            self.assertFalse((project / "skills-lock.json").exists())

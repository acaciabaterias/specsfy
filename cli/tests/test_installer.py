from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from specsfy_cli.installer import (
    MONOREPO_REPOSITORY,
    SkillInstaller,
    _RepositoryCheckout,
)


def write_template_files(source: Path) -> None:
    (source / "templates").mkdir(exist_ok=True)
    templates = {
        "Idea.md": "# Ideia: {{IDEA_NAME}}\n",
        "Backlog.md": "# Backlog: {{BACKLOG_NAME}}\n",
        "Spec.md": "# {{SPEC_NAME}}\n",
        "Tasks.md": "## 14. Tarefas\n",
        "Project.md": "# Projeto {{STACK_LABEL}}\n{{STACK_GUIDANCE}}\n",
        "Stack.md": "# Stack\n{{STACK_ROWS}}\n",
        "Rules.md": "# Regras {{STACK_LABEL}}\n{{STACK_GUIDANCE}}\n",
        "Database.md": "# Banco {{STACK_LABEL}}\n{{STACK_GUIDANCE}}\n",
    }
    for name, content in templates.items():
        (source / "templates" / name).write_text(content, encoding="utf-8")
    (source / "examples").mkdir(exist_ok=True)
    (source / "examples/Spec.md").write_text(
        "# Exemplo completo\n",
        encoding="utf-8",
    )


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.command_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.command_directory.cleanup)
        command_root = Path(self.command_directory.name)
        self.skills_log = command_root / "skills-command.jsonl"
        command = command_root / "skills"
        command.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            "import os\n"
            "import shutil\n"
            "import sys\n"
            "from pathlib import Path\n"
            "arguments = sys.argv[1:]\n"
            "with Path(os.environ['SPECSFY_SKILLS_LOG']).open('a', encoding='utf-8') as log:\n"
            "    log.write(json.dumps(arguments) + '\\n')\n"
            "lock_path = Path.cwd() / 'skills-lock.json'\n"
            "lock = json.loads(lock_path.read_text(encoding='utf-8')) if lock_path.is_file() else {'version': 1, 'skills': {}}\n"
            "if arguments and arguments[0] == 'remove':\n"
            "    for name in arguments[1:arguments.index('--agent')]:\n"
            "        lock['skills'].pop(name, None)\n"
            "    lock_path.write_text(json.dumps(lock), encoding='utf-8')\n"
            "    raise SystemExit(0)\n"
            "if not arguments or arguments[0] != 'add':\n"
            "    raise SystemExit(0)\n"
            "source = Path(arguments[1])\n"
            "names = [arguments[index + 1] for index, value in enumerate(arguments) if value == '--skill']\n"
            "destination = Path.cwd() / '.agents' / 'skills'\n"
            "destination.mkdir(parents=True, exist_ok=True)\n"
            "for name in names:\n"
            "    shutil.copytree(source / name, destination / name, dirs_exist_ok=True)\n"
            "    lock['skills'][name] = {'source': str(source), 'sourceType': 'local', 'computedHash': 'test'}\n"
            "lock_path.write_text(json.dumps(lock), encoding='utf-8')\n",
            encoding="utf-8",
        )
        command.chmod(0o755)
        self.environment = patch.dict(
            os.environ,
            {
                "SPECSFY_SKILLS_CLI": str(command),
                "SPECSFY_SKILLS_LOG": str(self.skills_log),
            },
        )
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_repository_checkout_selects_a_monorepo_module(self) -> None:
        def clone(command, **kwargs):
            checkout = Path(command[-1])
            (checkout / "skills").mkdir(parents=True)
            return subprocess.CompletedProcess(command, 0, "", "")

        with patch("specsfy_cli.installer.subprocess.run", side_effect=clone):
            with _RepositoryCheckout(
                MONOREPO_REPOSITORY,
                directory="skills",
            ) as source:
                self.assertEqual("skills", source.name)
                self.assertTrue(source.is_dir())

    def test_installs_selected_skill_and_writes_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            skill = source / "specsfy-specialist-react"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: specsfy-specialist-react\ndescription: React\n---\n",
                encoding="utf-8",
            )

            installer = SkillInstaller(project)
            installed = installer.install_from_checkout(
                source, ["specsfy-specialist-react"], source_name="specialists"
            )

            self.assertEqual(
                project / ".agents/skills/specsfy-specialist-react", installed[0]
            )
            lock = json.loads(
                (project / ".specsfy/skills-lock.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                "specialists", lock["skills"]["specsfy-specialist-react"]["source"]
            )
            self.assertIn(
                "content_sha256",
                lock["skills"]["specsfy-specialist-react"],
            )
            invocation = json.loads(
                self.skills_log.read_text(encoding="utf-8").splitlines()[-1]
            )
            self.assertEqual("add", invocation[0])
            self.assertIn(str(source), invocation)
            self.assertIn("--copy", invocation)
            self.assertIn("--full-depth", invocation)
            self.assertIn("universal", invocation)

    def test_updates_all_installed_specsfy_skills_by_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            installer = SkillInstaller(project)
            base_path = project / ".agents/skills/specsfy-base-backlog"
            setup_path = project / ".agents/skills/specsfy-setup"
            stack_path = project / ".agents/skills/specsfy-aux-stack"
            specialist_path = project / ".agents/skills/specsfy-specialist-react"

            with (
                patch(
                    "specsfy_cli.installer.installed_skill_names",
                    return_value={
                        "external-skill",
                        "specsfy-specialist-react",
                        "specsfy-base-backlog",
                        "specsfy-setup",
                        "specsfy-aux-stack",
                    },
                ),
                patch.object(
                    installer,
                    "install_base_selection",
                    return_value=[base_path, setup_path, stack_path],
                ) as install_base,
                patch.object(
                    installer,
                    "install_specialists",
                    return_value=[specialist_path],
                ) as install_specialists,
            ):
                changed = installer.update_all()

            self.assertEqual(
                [base_path, setup_path, stack_path, specialist_path],
                changed,
            )
            install_base.assert_called_once_with(
                [
                    "specsfy-aux-stack",
                    "specsfy-base-backlog",
                    "specsfy-setup",
                ]
            )
            install_specialists.assert_called_once_with(
                ["specsfy-specialist-react"]
            )

    def test_accepts_setup_documentator_and_auxiliary_skills_from_framework_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            names = (
                "specsfy-setup",
                "specsfy-aux-stack",
                "specsfy-aux-rules",
                "specsfy-aux-database",
                "specsfy-documentator",
            )
            for name in names:
                skill = source / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(name, encoding="utf-8")
            (source / "Spec.md").write_text("# Specsfy\n", encoding="utf-8")
            write_template_files(source)
            (source / "AGENTS.md").write_text(
                "<!-- specsfy:framework:start -->\n"
                "Leia `{{SPECSFY_SPEC_PATH}}`.\n"
                "<!-- specsfy:framework:end -->\n",
                encoding="utf-8",
            )
            installer = SkillInstaller(project)

            changed = installer.install_base_from_checkout(source, names=names)

            for name in names:
                self.assertIn(project / ".agents" / "skills" / name, changed)

    def test_repeated_install_is_a_no_op(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            skill = source / "specsfy-base-interview"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("source", encoding="utf-8")
            installer = SkillInstaller(project)

            installer.install_from_checkout(source, [skill.name], source_name="base")
            lock_before = (
                project / ".specsfy/skills-lock.json"
            ).read_text(encoding="utf-8")
            generated = (
                project
                / ".agents/skills/specsfy-base-interview/__pycache__/helper.pyc"
            )
            generated.parent.mkdir()
            generated.write_bytes(b"cache local descartavel")
            installed = installer.install_from_checkout(
                source, [skill.name], source_name="base"
            )

            self.assertEqual([], installed)
            self.assertEqual(
                lock_before,
                (project / ".specsfy/skills-lock.json").read_text(encoding="utf-8"),
            )

    def test_installs_only_selected_base_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            selected = source / "specsfy-base-backlog"
            unselected = source / "specsfy-base-interview"
            for skill in (selected, unselected):
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(skill.name, encoding="utf-8")
            (source / "Spec.md").write_text("# Specsfy\n", encoding="utf-8")
            write_template_files(source)
            (source / "AGENTS.md").write_text(
                "<!-- specsfy:framework:start -->\n"
                "Leia `{{SPECSFY_SPEC_PATH}}`.\n"
                "<!-- specsfy:framework:end -->\n",
                encoding="utf-8",
            )
            installer = SkillInstaller(project)

            changed = installer.install_base_from_checkout(
                source,
                names=["specsfy-base-backlog"],
            )

            self.assertIn(
                project / ".agents/skills/specsfy-base-backlog",
                changed,
            )
            self.assertTrue(
                (project / ".agents/skills/specsfy-base-backlog/SKILL.md").is_file()
            )
            self.assertFalse(
                (project / ".agents/skills/specsfy-base-interview").exists()
            )

    def test_remove_reconciles_skill_recorded_only_in_official_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            installer = SkillInstaller(project)
            (project / "skills-lock.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "skills": {
                            "specsfy-specialist-react": {
                                "source": "specialists/",
                                "sourceType": "github",
                                "computedHash": "abc",
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            removed = installer.remove(["specsfy-specialist-react"])

            self.assertEqual([], removed)
            official = json.loads(
                (project / "skills-lock.json").read_text(encoding="utf-8")
            )
            self.assertNotIn("specsfy-specialist-react", official["skills"])
            invocation = json.loads(
                self.skills_log.read_text(encoding="utf-8").splitlines()[-1]
            )
            self.assertEqual("remove", invocation[0])

    def test_updates_unchanged_managed_skill_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            skill = source / "specsfy-base-interview"
            skill.mkdir(parents=True)
            skill_file = skill / "SKILL.md"
            skill_file.write_text("version one", encoding="utf-8")
            installer = SkillInstaller(project)
            installer.install_from_checkout(source, [skill.name], source_name="base")

            skill_file.write_text("version two", encoding="utf-8")
            installed = installer.install_from_checkout(
                source, [skill.name], source_name="base"
            )

            self.assertEqual([project / ".agents/skills" / skill.name], installed)
            self.assertEqual(
                "version two",
                (project / ".agents/skills" / skill.name / "SKILL.md").read_text(
                    encoding="utf-8"
                ),
            )

    def test_refuses_to_replace_or_remove_locally_modified_managed_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            skill = source / "specsfy-base-interview"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("source", encoding="utf-8")
            installer = SkillInstaller(project)
            installer.install_from_checkout(source, [skill.name], source_name="base")
            target = project / ".agents/skills" / skill.name / "SKILL.md"
            target.write_text("customização local", encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "alterações locais"):
                installer.install_from_checkout(source, [skill.name], source_name="base")
            with self.assertRaisesRegex(FileExistsError, "alterações locais"):
                installer.remove([skill.name])

            self.assertEqual("customização local", target.read_text(encoding="utf-8"))

    def test_refuses_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            skill = source / "specsfy-base-interview"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("source", encoding="utf-8")
            target = project / ".agents/skills/specsfy-base-interview"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("local", encoding="utf-8")

            installer = SkillInstaller(project)
            with self.assertRaisesRegex(FileExistsError, "--force"):
                installer.install_from_checkout(source, [skill.name], source_name="base")
            self.assertEqual("local", (target / "SKILL.md").read_text(encoding="utf-8"))

    def test_bootstraps_framework_and_preserves_user_instruction_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            skill = source / "specsfy-base-interview"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("skill", encoding="utf-8")
            (source / "Spec.md").write_text("# Regras Specsfy\n", encoding="utf-8")
            write_template_files(source)
            (source / "AGENTS.md").write_text(
                "# Interno\n"
                "<!-- specsfy:framework:start -->\n"
                "Leia e siga `{{SPECSFY_SPEC_PATH}}`.\n"
                "<!-- specsfy:framework:end -->\n",
                encoding="utf-8",
            )
            project.mkdir()
            (project / "AGENTS.md").write_text(
                "# Regras do usuário\n\nPreservar isto.\n",
                encoding="utf-8",
            )
            (project / "CLAUDE.md").write_text(
                "# Claude do usuário\n",
                encoding="utf-8",
            )
            installer = SkillInstaller(project)

            with patch(
                "specsfy_cli.installer.BASE_SKILLS",
                ("specsfy-base-interview",),
            ):
                changed = installer.install_base_from_checkout(source)
                tracked = (
                    project / "AGENTS.md",
                    project / "CLAUDE.md",
                    project / ".specsfy/Spec.md",
                    project / ".specsfy/templates/Spec.md",
                    project / ".specsfy/templates/Idea.md",
                    project / ".specsfy/templates/Backlog.md",
                    project / ".specsfy/templates/Tasks.md",
                    project / ".specsfy/templates/Project.md",
                    project / ".specsfy/templates/Stack.md",
                    project / ".specsfy/templates/Rules.md",
                    project / ".specsfy/templates/Database.md",
                    project / ".specsfy/examples/Spec.md",
                    project / ".specsfy/skills-lock.json",
                )
                state_after_first = {
                    path: path.read_text(encoding="utf-8") for path in tracked
                }
                repeated = installer.install_base_from_checkout(source)

            self.assertEqual(13, len(changed))
            self.assertEqual([], repeated)
            self.assertEqual(
                state_after_first,
                {path: path.read_text(encoding="utf-8") for path in tracked},
            )
            agents = (project / "AGENTS.md").read_text(encoding="utf-8")
            claude = (project / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertIn("Preservar isto.", agents)
            self.assertIn("`.specsfy/Spec.md`", agents)
            self.assertNotIn("# Interno", agents)
            self.assertIn("# Claude do usuário", claude)
            self.assertIn("@.specsfy/Spec.md", claude)
            self.assertEqual(
                "# {{SPEC_NAME}}\n",
                (project / ".specsfy/templates/Spec.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                "# Ideia: {{IDEA_NAME}}\n",
                (project / ".specsfy/templates/Idea.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                "# Backlog: {{BACKLOG_NAME}}\n",
                (project / ".specsfy/templates/Backlog.md").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertEqual(
                "## 14. Tarefas\n",
                (project / ".specsfy/templates/Tasks.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                "# Exemplo completo\n",
                (project / ".specsfy/examples/Spec.md").read_text(encoding="utf-8"),
            )

    def test_refuses_locally_modified_framework_block_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            skill = source / "specsfy-base-interview"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("skill", encoding="utf-8")
            (source / "Spec.md").write_text("# Regras Specsfy\n", encoding="utf-8")
            write_template_files(source)
            (source / "AGENTS.md").write_text(
                "<!-- specsfy:framework:start -->\n"
                "Leia `{{SPECSFY_SPEC_PATH}}`.\n"
                "<!-- specsfy:framework:end -->\n",
                encoding="utf-8",
            )
            installer = SkillInstaller(project)
            with patch(
                "specsfy_cli.installer.BASE_SKILLS",
                ("specsfy-base-interview",),
            ):
                installer.install_base_from_checkout(source)
                agents = project / "AGENTS.md"
                agents.write_text(
                    agents.read_text(encoding="utf-8").replace(
                        "Leia `.specsfy/Spec.md`.",
                        "Bloco alterado localmente.",
                    ),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(FileExistsError, "AGENTS.md"):
                    installer.install_base_from_checkout(source)

    def test_refuses_locally_modified_framework_spec_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            skill = source / "specsfy-base-interview"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("skill", encoding="utf-8")
            (source / "Spec.md").write_text("# Regras Specsfy\n", encoding="utf-8")
            write_template_files(source)
            (source / "AGENTS.md").write_text(
                "<!-- specsfy:framework:start -->\n"
                "Leia `{{SPECSFY_SPEC_PATH}}`.\n"
                "<!-- specsfy:framework:end -->\n",
                encoding="utf-8",
            )
            installer = SkillInstaller(project)
            with patch(
                "specsfy_cli.installer.BASE_SKILLS",
                ("specsfy-base-interview",),
            ):
                installer.install_base_from_checkout(source)
                framework_spec = project / ".specsfy/Spec.md"
                framework_spec.write_text(
                    "# Regras customizadas\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(FileExistsError, "Spec.md"):
                    installer.install_base_from_checkout(source)

    def test_refuses_locally_modified_spec_template_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            skill = source / "specsfy-base-interview"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("skill", encoding="utf-8")
            (source / "Spec.md").write_text("# Regras Specsfy\n", encoding="utf-8")
            write_template_files(source)
            (source / "AGENTS.md").write_text(
                "<!-- specsfy:framework:start -->\n"
                "Leia `{{SPECSFY_SPEC_PATH}}`.\n"
                "<!-- specsfy:framework:end -->\n",
                encoding="utf-8",
            )
            installer = SkillInstaller(project)
            with patch(
                "specsfy_cli.installer.BASE_SKILLS",
                ("specsfy-base-interview",),
            ):
                installer.install_base_from_checkout(source)
                template = project / ".specsfy/templates/Spec.md"
                template.write_text("# Template do usuário\n", encoding="utf-8")
                with self.assertRaisesRegex(FileExistsError, "templates/Spec.md"):
                    installer.install_base_from_checkout(source)

    def test_migrates_renamed_discuss_skill_when_it_is_unmodified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            project = root / "consumer"
            old_skill = source / "specsfy-base-discuss"
            old_skill.mkdir(parents=True)
            (old_skill / "SKILL.md").write_text("old", encoding="utf-8")
            installer = SkillInstaller(project)
            installer.install_from_checkout(
                source,
                [old_skill.name],
                source_name="base",
            )
            new_skill = source / "specsfy-base-interview"
            new_skill.mkdir()
            (new_skill / "SKILL.md").write_text("new", encoding="utf-8")
            (source / "Spec.md").write_text("# Regras\n", encoding="utf-8")
            write_template_files(source)
            (source / "AGENTS.md").write_text(
                "<!-- specsfy:framework:start -->\n"
                "Leia `{{SPECSFY_SPEC_PATH}}`.\n"
                "<!-- specsfy:framework:end -->\n",
                encoding="utf-8",
            )

            with patch(
                "specsfy_cli.installer.BASE_SKILLS",
                ("specsfy-base-interview",),
            ):
                installer.install_base_from_checkout(source)

            skills = project / ".agents/skills"
            self.assertFalse((skills / "specsfy-base-discuss").exists())
            self.assertTrue((skills / "specsfy-base-interview").is_dir())

    def test_refuses_parent_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "AGENTS.md").write_text(
                "Este AGENTS governa o workspace Specsfy Dev\n"
                "não crie `specs/`, `.agents/` ou `.claude/` nesta raiz.",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "monorepo"):
                SkillInstaller(project)

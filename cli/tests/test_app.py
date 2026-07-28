from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from textual.containers import VerticalScroll
from textual.widgets import (
    Button,
    DataTable,
    Input,
    Markdown,
    RichLog,
    Static,
    TabbedContent,
)

from specsfy_cli.app import build_parser, main
from specsfy_cli.catalog import Catalog, CatalogEntry
from specsfy_cli.config import update_config
from specsfy_cli.installer import BASE_SKILLS, FRAMEWORK_SKILLS
from specsfy_cli.testing import TestCommand, TestRun
from specsfy_cli.tui import BASE_DESCRIPTIONS, SpecPreviewModal, SpecsfyApp


class ApplicationTests(unittest.TestCase):
    def test_framework_exposes_the_update_spec_skill(self) -> None:
        self.assertIn("specsfy-base-update-spec", BASE_SKILLS)
        self.assertIn("specsfy-base-update-spec", FRAMEWORK_SKILLS)
        self.assertIn("specsfy-base-update-spec", BASE_DESCRIPTIONS)

    def test_parser_exposes_framework_skills_progress_and_tui(self) -> None:
        parser = build_parser()
        for command in (
            ["install"],
            ["skills", "list"],
            ["skills", "detect"],
            ["skills", "add", "specsfy-specialist-react"],
            ["skills", "remove", "specsfy-specialist-react"],
            ["skills", "update"],
            ["config", "show"],
            ["config", "set", "--watch-interval", "0.5"],
            ["progress"],
            ["progress", "--watch"],
            ["test"],
            ["tui"],
        ):
            with self.subTest(command=command):
                self.assertIsNotNone(parser.parse_args(command))

    def test_tui_can_be_constructed(self) -> None:
        app = SpecsfyApp()
        self.assertEqual("Specsfy", app.TITLE)
        bindings = {
            binding.key: (binding.action, binding.description)
            for binding in app.BINDINGS
        }
        self.assertEqual(("quit", "Sair"), bindings["ctrl+q"])
        self.assertEqual(("back", "Voltar"), bindings["escape"])
        self.assertEqual(("refresh", "Atualizar"), bindings["ctrl+u"])
        self.assertEqual(("install_base", "Framework"), bindings["ctrl+b"])
        self.assertEqual(("detect_skills", "Detectar"), bindings["ctrl+d"])
        self.assertEqual(("toggle_skill", "Alternar"), bindings["ctrl+e"])
        self.assertEqual(
            ("activate_selection", "Abrir/alternar"),
            bindings["space"],
        )
        self.assertEqual(("apply_skills", "Aplicar"), bindings["ctrl+a"])
        self.assertEqual(("update_skills", "Atualizar skills"), bindings["ctrl+r"])
        self.assertEqual(("select_visible", "Marcar"), bindings["ctrl+m"])
        self.assertEqual(("clear_visible", "Limpar"), bindings["ctrl+l"])
        self.assertEqual(("filter_all", "Todas"), bindings["ctrl+t"])
        self.assertEqual(("filter_installed", "Instaladas"), bindings["ctrl+i"])
        self.assertEqual(("filter_detected", "Recomendadas"), bindings["ctrl+c"])
        self.assertEqual(("show_home", "Home"), bindings["ctrl+h"])
        self.assertEqual(("show_backlogs", "Backlogs"), bindings["ctrl+g"])
        self.assertEqual(("show_specs", "Specs"), bindings["ctrl+s"])
        self.assertEqual(("show_tests", "Testes"), bindings["ctrl+j"])
        self.assertEqual(("run_tests", "Executar testes"), bindings["ctrl+x"])
        self.assertEqual(("show_skills", "Skills"), bindings["ctrl+k"])
        self.assertEqual(("show_about", "Sobre"), bindings["ctrl+o"])

    def test_progress_json_contains_summary_and_specs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            spec = project / "specs/specs/0001-dashboard/spec.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(
                "# Dashboard\n\n**Status**: Implementing\n\n"
                "- [x] T001 Feita\n- [ ] T002 Pendente\n",
                encoding="utf-8",
            )
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(["progress", "--project", str(project), "--json"])

            payload = json.loads(output.getvalue())
            self.assertEqual(0, exit_code)
            self.assertEqual(1, payload["summary"]["total_specs"])
            self.assertEqual(50, payload["summary"]["percent"])
            self.assertEqual("0001-dashboard", payload["specs"][0]["slug"])

    def test_test_command_streams_output_and_returns_pest_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            result = TestRun(
                command=TestCommand(
                    label="Laravel Pest",
                    argv=("php", "artisan", "test"),
                    cwd=project,
                ),
                exit_code=1,
            )

            with patch(
                "specsfy_cli.app.run_project_tests",
                return_value=result,
            ) as run_tests:
                exit_code = main(["test", "--project", str(project)])

            self.assertEqual(1, exit_code)
            run_tests.assert_called_once_with(project)

    def test_startup_update_closes_before_mounting_tui(self) -> None:
        with (
            patch(
                "specsfy_cli.app.offer_startup_update",
                return_value=True,
            ) as offer_update,
            patch("specsfy_cli.tui.SpecsfyApp.run") as run_tui,
        ):
            exit_code = main([])

        self.assertEqual(0, exit_code)
        offer_update.assert_called_once_with()
        run_tui.assert_not_called()

    def test_declined_startup_update_mounts_tui_normally(self) -> None:
        with (
            patch(
                "specsfy_cli.app.offer_startup_update",
                return_value=False,
            ),
            patch("specsfy_cli.tui.SpecsfyApp.run") as run_tui,
        ):
            exit_code = main([])

        self.assertEqual(0, exit_code)
        run_tui.assert_called_once_with()

    def test_skills_update_updates_every_installed_specsfy_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            changed = project / ".agents/skills/specsfy-base-backlog"
            installer = Mock()
            installer.update_all.return_value = [changed]
            output = io.StringIO()

            with (
                patch("specsfy_cli.app.SkillInstaller", return_value=installer),
                redirect_stdout(output),
            ):
                exit_code = main(
                    ["skills", "update", "--project", str(project)]
                )

            self.assertEqual(0, exit_code)
            installer.update_all.assert_called_once_with()
            self.assertEqual(f"{changed}\n", output.getvalue())

    def test_skills_add_installs_required_specialists_together(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            ui = CatalogEntry(
                name="specsfy-specialist-ui-design",
                description="UI.",
                category="design",
                tags=("ui",),
                files=(),
                dependencies=(),
            )
            components = CatalogEntry(
                name="specsfy-specialist-react-ui-components",
                description="Componentes React.",
                category="design",
                tags=("react", "ui"),
                files=(),
                dependencies=("react", "tailwindcss"),
                requires=("specsfy-specialist-ui-design",),
            )
            installer = Mock()
            installer.install_specialists.return_value = []

            with (
                patch(
                    "specsfy_cli.app.Catalog.fetch",
                    return_value=Catalog([ui, components]),
                ),
                patch(
                    "specsfy_cli.app.SkillInstaller",
                    return_value=installer,
                ),
            ):
                exit_code = main(
                    [
                        "skills",
                        "add",
                        "specsfy-specialist-react-ui-components",
                        "--project",
                        str(project),
                    ]
                )

            self.assertEqual(0, exit_code)
            installer.install_specialists.assert_called_once_with(
                [
                    "specsfy-specialist-ui-design",
                    "specsfy-specialist-react-ui-components",
                ]
            )


class TuiTests(unittest.IsolatedAsyncioTestCase):
    async def test_tui_mounts_tabs_and_specsfy_skill_selector_from_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "skills-lock.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "skills": {
                            "specsfy-specialist-react": {},
                            "external-skill": {},
                        },
                    }
                ),
                encoding="utf-8",
            )
            catalog = Catalog(
                [
                    CatalogEntry(
                        name="specsfy-specialist-react",
                        description="React completo.",
                        category="frontend",
                        tags=("react",),
                        files=(),
                        dependencies=("react",),
                    )
                ]
            )
            app = SpecsfyApp(project, catalog=catalog)

            async with app.run_test() as pilot:
                await pilot.pause()
                self.assertEqual(1, len(app.query("#tab-home")))
                self.assertEqual(1, len(app.query("#tab-backlogs")))
                self.assertEqual(1, len(app.query("#tab-specs")))
                self.assertEqual(1, len(app.query("#tab-tests")))
                self.assertEqual(1, len(app.query("#tab-skills")))
                self.assertEqual(1, len(app.query("#tab-about")))
                self.assertEqual(1, len(app.query("#progress")))
                self.assertEqual(1, len(app.query("#summary-specs")))
                self.assertEqual(1, len(app.query("#summary-tasks")))
                self.assertEqual(1, len(app.query("#summary-items")))
                self.assertEqual(1, len(app.query("#summary-progress")))
                summary_backgrounds = {
                    app.query_one(f"#summary-{card}", Static)
                    .styles.background.hex
                    for card in ("specs", "tasks", "items", "progress")
                }
                self.assertEqual(
                    {"#173E67", "#3F2D63", "#174B43", "#4A381C"},
                    summary_backgrounds,
                )
                self.assertEqual(1, len(app.query("#apply-skills")))
                skill_table = app.query_one("#skills-table", DataTable)
                self.assertEqual(15, skill_table.row_count)
                self.assertEqual(0, len(app.query("#skills-list")))
                self.assertEqual(
                    ["Manter", "React", "Frontend", "Instalada"],
                    skill_table.get_row("specsfy-specialist-react"),
                )
                self.assertTrue(
                    app.query_one("#skill-detail-pane", VerticalScroll).can_focus
                )
                self.assertIn("specsfy-specialist-react", app._selected_skills)
                self.assertNotIn("external-skill", app._selected_skills)
                self.assertNotIn("specsfy-base-backlog", app._selected_skills)
                self.assertIn(
                    "Ideias, descoberta inicial",
                    str(app.query_one("#skill-detail", Static).render()),
                )
                skill_table.move_cursor(
                    row=skill_table.get_row_index("specsfy-specialist-react")
                )
                await pilot.pause()
                self.assertIn(
                    "React completo.",
                    str(app.query_one("#skill-detail", Static).render()),
                )
                self.assertIn(
                    "1 skill(s) Specsfy",
                    str(app.query_one("#skills-status").render()),
                )
                for button_id in (
                    "refresh",
                    "filter-all",
                    "filter-installed",
                    "filter-detected",
                    "detect",
                    "install",
                    "select-visible",
                    "clear-visible",
                    "toggle-skill",
                    "apply-skills",
                    "update-skills",
                    "run-tests",
                ):
                    self.assertIn(
                        "^",
                        str(app.query_one(f"#{button_id}", Button).label),
                    )
                footer = app.query_one("Footer")
                self.assertIsNotNone(footer)

                app.action_show_skills()
                await pilot.pause()
                self.assertEqual(
                    "tab-skills",
                    app.query_one("#workspace-tabs", TabbedContent).active,
                )
                search = app.query_one("#skills-search", Input)
                self.assertTrue(search.can_focus)
                self.assertTrue(
                    await pilot.click("#skills-search", offset=(5, 1))
                )
                await pilot.pause()
                self.assertEqual("skills-search", app.focused.id)
                await pilot.press("tab")
                self.assertNotEqual("skills-search", app.focused.id)
                app.query_one("#skills-search", Input).value = "specsfy-base-"
                await pilot.pause()
                self.assertEqual(9, skill_table.row_count)
                app.query_one("#skills-search", Input).value = "backlog"
                await pilot.pause()
                self.assertEqual(1, skill_table.row_count)
                app.query_one("#skills-search", Input).value = ""
                await pilot.pause()
                await pilot.press("ctrl+l")
                await pilot.pause()
                self.assertFalse(
                    set(BASE_SKILLS) & app._selected_skills
                )
                await pilot.press("ctrl+b")
                await pilot.pause()
                self.assertTrue(
                    set(FRAMEWORK_SKILLS) <= app._selected_skills
                )
                skill_table.focus()
                skill_table.move_cursor(row=0)
                await pilot.press("down")
                self.assertEqual(1, skill_table.cursor_row)
                app.action_show_about()
                self.assertEqual(
                    "tab-about",
                    app.query_one("#workspace-tabs", TabbedContent).active,
                )
                await pilot.press("escape")
                self.assertEqual(
                    "tab-home",
                    app.query_one("#workspace-tabs", TabbedContent).active,
                )

    async def test_tui_applies_checked_specialist_selection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            catalog = Catalog(
                [
                    CatalogEntry(
                        name="specsfy-specialist-react",
                        description="React completo.",
                        category="frontend",
                        tags=("react",),
                        files=(),
                        dependencies=("react",),
                    )
                ]
            )
            app = SpecsfyApp(project, catalog=catalog)
            installer = Mock()
            installer.install_specialists.return_value = [
                project / ".agents/skills/specsfy-specialist-react"
            ]
            installer.remove.return_value = []

            async with app.run_test() as pilot:
                await pilot.pause()
                skill_table = app.query_one("#skills-table", DataTable)
                skill_table.focus()
                skill_table.move_cursor(
                    row=skill_table.get_row_index("specsfy-specialist-react")
                )
                await pilot.pause()
                self.assertTrue(await pilot.click("#toggle-skill"))
                await pilot.pause()
                self.assertIn("specsfy-specialist-react", app._selected_skills)
                self.assertEqual(
                    "Instalar",
                    skill_table.get_row("specsfy-specialist-react")[0],
                )
                with patch(
                    "specsfy_cli.tui.SkillInstaller",
                    return_value=installer,
                ):
                    await app.action_apply_skills()

            installer.install_specialists.assert_called_once_with(
                ["specsfy-specialist-react"]
            )
            installer.remove.assert_not_called()

    async def test_tui_applies_required_specialists_together(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            ui = CatalogEntry(
                name="specsfy-specialist-ui-design",
                description="UI.",
                category="design",
                tags=("ui",),
                files=(),
                dependencies=(),
            )
            components = CatalogEntry(
                name="specsfy-specialist-react-ui-components",
                description="Componentes React.",
                category="design",
                tags=("react", "ui"),
                files=(),
                dependencies=("react", "tailwindcss"),
                requires=("specsfy-specialist-ui-design",),
            )
            app = SpecsfyApp(project, catalog=Catalog([ui, components]))
            installer = Mock()
            installer.install_specialists.return_value = [
                project / ".agents/skills/specsfy-specialist-ui-design",
                project
                / ".agents/skills/specsfy-specialist-react-ui-components",
            ]
            installer.remove.return_value = []

            async with app.run_test() as pilot:
                await pilot.pause()
                skill_table = app.query_one("#skills-table", DataTable)
                skill_table.focus()
                skill_table.move_cursor(
                    row=skill_table.get_row_index(
                        "specsfy-specialist-react-ui-components"
                    )
                )
                await pilot.press("space")
                await pilot.pause()
                with patch(
                    "specsfy_cli.tui.SkillInstaller",
                    return_value=installer,
                ):
                    await app.action_apply_skills()

            installer.install_specialists.assert_called_once_with(
                [
                    "specsfy-specialist-ui-design",
                    "specsfy-specialist-react-ui-components",
                ]
            )
            installer.remove.assert_not_called()

    async def test_tui_removes_unchecked_installed_specsfy_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "skills-lock.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "skills": {
                            "specsfy-specialist-react": {},
                            "third-party-skill": {},
                        },
                    }
                ),
                encoding="utf-8",
            )
            catalog = Catalog(
                [
                    CatalogEntry(
                        name="specsfy-specialist-react",
                        description="React completo.",
                        category="frontend",
                        tags=("react",),
                        files=(),
                        dependencies=("react",),
                    )
                ]
            )
            app = SpecsfyApp(project, catalog=catalog)
            installer = Mock()
            installer.remove.return_value = [
                project / ".agents/skills/specsfy-specialist-react"
            ]

            async with app.run_test() as pilot:
                await pilot.pause()
                skill_table = app.query_one("#skills-table", DataTable)
                skill_table.focus()
                skill_table.move_cursor(
                    row=skill_table.get_row_index("specsfy-specialist-react")
                )
                await pilot.press("space")
                await pilot.pause()
                self.assertNotIn(
                    "specsfy-specialist-react",
                    app._selected_skills,
                )
                self.assertEqual(
                    "Remover",
                    skill_table.get_row("specsfy-specialist-react")[0],
                )
                with patch(
                    "specsfy_cli.tui.SkillInstaller",
                    return_value=installer,
                ):
                    await app.action_apply_skills()

            installer.remove.assert_called_once_with(
                ["specsfy-specialist-react"]
            )

    async def test_tui_updates_all_installed_specsfy_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            app = SpecsfyApp(project, catalog=Catalog([]))
            installer = Mock()
            installer.update_all.return_value = [
                project / ".agents/skills/specsfy-base-backlog"
            ]

            async with app.run_test() as pilot:
                await pilot.pause()
                with patch(
                    "specsfy_cli.tui.SkillInstaller",
                    return_value=installer,
                ):
                    await app.action_update_skills()

                self.assertIn(
                    "Skills atualizadas: 1 alteração(ões).",
                    str(app.query_one("#skills-status", Static).render()),
                )

            installer.update_all.assert_called_once_with()

    async def test_tui_navigates_backlogs_and_renders_markdown_preview(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            backlog_root = project / "specs/backlog"
            backlog_root.mkdir(parents=True)
            (backlog_root / "0001-primeiro.md").write_text(
                "# Backlog: Primeiro\n\n"
                "**ID**: BACKLOG-0001\n"
                "**Status**: Captured\n\n"
                "Conteúdo do primeiro.",
                encoding="utf-8",
            )
            second = backlog_root / "0002-segundo.md"
            second.write_text(
                "# Backlog: Segundo\n\n"
                "**ID**: BACKLOG-0002\n"
                "**Status**: Refining\n\n"
                "Conteúdo do segundo.",
                encoding="utf-8",
            )
            update_config(project, watch_interval=0.02)
            app = SpecsfyApp(project, catalog=Catalog([]))

            async with app.run_test() as pilot:
                await pilot.pause()
                app.action_show_backlogs()
                table = app.query_one("#backlog-list")
                preview = app.query_one("#backlog-preview", Markdown)
                preview_pane = app.query_one(
                    "#backlog-preview-pane",
                    VerticalScroll,
                )
                self.assertEqual(2, table.row_count)
                self.assertTrue(preview_pane.can_focus)
                self.assertIn("Conteúdo do primeiro.", preview.source)

                table.focus()
                await pilot.press("down")
                await pilot.pause()

                self.assertIn("Conteúdo do segundo.", preview.source)
                second.write_text(
                    "# Backlog: Segundo\n\n"
                    "**ID**: BACKLOG-0002\n"
                    "**Status**: Ready for interview\n\n"
                    "Conteúdo atualizado em tempo real.",
                    encoding="utf-8",
                )
                for _ in range(10):
                    await pilot.pause(0.03)
                    if "tempo real" in preview.source:
                        break

                self.assertIn("Conteúdo atualizado em tempo real.", preview.source)

    async def test_tui_runs_pest_and_streams_output_in_tests_tab(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            app = SpecsfyApp(project, catalog=Catalog([]))
            command = TestCommand(
                label="Laravel Pest",
                argv=("php", "artisan", "test"),
                cwd=project,
            )

            async def stream_tests(selected_project, *, emit):
                self.assertEqual(project.resolve(), selected_project)
                emit("PASS  Tests/Feature/DashboardTest.php")
                emit("Tests: 1 passed")
                return TestRun(
                    command=command,
                    exit_code=0,
                    duration_seconds=0.12,
                    summary_lines=("Tests: 1 passed",),
                )

            async with app.run_test() as pilot:
                await pilot.pause()
                with patch(
                    "specsfy_cli.tui.stream_project_tests",
                    side_effect=stream_tests,
                ):
                    worker = app.action_run_tests()
                    await worker.wait()
                    await pilot.pause()

                self.assertEqual(
                    "tab-tests",
                    app.query_one("#workspace-tabs", TabbedContent).active,
                )
                self.assertIn(
                    "Testes passaram",
                    str(app.query_one("#tests-status", Static).render()),
                )
                self.assertIn(
                    "Tests: 1 passed",
                    str(app.query_one("#tests-summary", Static).render()),
                )
                self.assertEqual(1, len(app.query("#tab-tests-summary")))
                self.assertEqual(1, len(app.query("#tab-tests-output")))
                app.query_one("#test-results-tabs", TabbedContent).active = (
                    "tab-tests-output"
                )
                await pilot.pause()
                output = app.query_one("#tests-output", RichLog)
                rendered = "\n".join(line.text for line in output.lines)
                self.assertIn("DashboardTest.php", rendered)
                self.assertIn("1 passed", rendered)

    async def test_tui_opens_highlighted_spec_in_markdown_modal_with_space(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            first = project / "specs/specs/0001-primeira/spec.md"
            first.parent.mkdir(parents=True)
            first.write_text(
                "# Primeira\n\n**Status**: Planned\n\nConteúdo inicial.",
                encoding="utf-8",
            )
            second = project / "specs/specs/0002-segunda/spec.md"
            second.parent.mkdir(parents=True)
            second.write_text(
                "# Segunda\n\n**Status**: Implementing\n\n"
                "Detalhes completos da segunda spec.",
                encoding="utf-8",
            )
            app = SpecsfyApp(project, catalog=Catalog([]))

            async with app.run_test() as pilot:
                await pilot.pause()
                app.action_show_specs()
                table = app.query_one("#progress", DataTable)
                table.focus()
                await pilot.press("down")
                await pilot.press("space")
                await pilot.pause()

                self.assertIsInstance(app.screen, SpecPreviewModal)
                self.assertIn(
                    "Detalhes completos da segunda spec.",
                    app.screen.query_one("#spec-preview", Markdown).source,
                )
                self.assertIn(
                    "0002-segunda · Implementing",
                    str(app.screen.query_one("#spec-preview-title", Static).render()),
                )

                await pilot.press("escape")
                await pilot.pause()
                self.assertNotIsInstance(app.screen, SpecPreviewModal)
                self.assertEqual("progress", app.focused.id)

    async def test_tui_recalculates_when_a_spec_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            spec = project / "specs/specs/0001-live/spec.md"
            spec.parent.mkdir(parents=True)
            spec.write_text("# Live\n\n- [ ] T001 Pendente\n", encoding="utf-8")
            update_config(project, watch_interval=0.02)
            app = SpecsfyApp(project, catalog=Catalog([]))

            async with app.run_test() as pilot:
                await pilot.pause()
                table = app.query_one("#progress")
                self.assertEqual(1, table.row_count)
                spec.write_text("# Live\n\n- [x] T001 Feita\n", encoding="utf-8")
                for _ in range(10):
                    await pilot.pause(0.03)
                    if "100%" in str(app.query_one("#summary-progress").render()):
                        break

                self.assertIn(
                    "100%",
                    str(app.query_one("#summary-progress").render()),
                )

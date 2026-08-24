from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "skills" / "templates" / "DESIGNSYSTEM.MD"
SKILL = ROOT / "specialists" / "specsfy-specialist-design-system" / "SKILL.md"
CATALOG = ROOT / "specialists" / "catalog.json"
INSTALLER = ROOT / "cli" / "src" / "installer.ts"
INTERFACE = ROOT / "skills" / "templates" / "Interface.md"
SETUP_SCRIPT = ROOT / "skills" / "specsfy-setup" / "scripts" / "setup_context.mjs"
TABLE_ASSET = (
    ROOT
    / "specialists"
    / "specsfy-specialist-react-ui-components"
    / "assets"
    / "components"
    / "data-display"
    / "table.tsx"
)
LARAVEL_APP_LAYOUT = (
    ROOT / "example" / "resources" / "js" / "layouts" / "app-layout.tsx"
)
LARAVEL_BREADCRUMBS = (
    ROOT / "example" / "resources" / "js" / "components" / "breadcrumbs.tsx"
)
LARAVEL_BREADCRUMB_PRIMITIVE = (
    ROOT / "example" / "resources" / "js" / "components" / "ui" / "breadcrumb.tsx"
)


class InterfaceDesignSystemContractTests(unittest.TestCase):
    def test_template_declares_canonical_crud_compositions_and_scenarios(self) -> None:
        content = TEMPLATE.read_text(encoding="utf-8")
        for term in (
            "DataGrid",
            "DetailLists",
            "PageHeader",
            "Breadcrumb",
            "seções",
            "duas colunas",
            "grid-cols-2",
            "mobile",
            "vermelho",
            "abaixo",
            "Cenários canônicos",
        ):
            self.assertIn(term, content)

    def test_template_declares_common_dashboard_and_component_patterns(self) -> None:
        content = TEMPLATE.read_text(encoding="utf-8")
        for term in (
            "Dashboard canônico",
            "KPI",
            "shadcn/ui",
            "ReUI",
            "Skeleton",
            "teclado",
            "prefers-reduced-motion",
        ):
            self.assertIn(term, content)

    def test_datagrid_declares_full_row_navigation_and_action_exceptions(self) -> None:
        template = TEMPLATE.read_text(encoding="utf-8")
        asset = TABLE_ASSET.read_text(encoding="utf-8")
        for term in (
            "linha inteira",
            "teclado",
            "ações internas",
            "TableRowAction",
            "data-row-link",
        ):
            self.assertIn(term, template + asset)
        self.assertIn("data-row-action", asset)
        self.assertIn("absolute inset-0", asset)
        row = asset[
            asset.index("export function TableRow(") : asset.index(
                "export function TableRowAction"
            )
        ]
        cell = asset[asset.index("export function TableCell") :]
        self.assertIn("href?: string", row)
        self.assertIn("TableRowContext.Provider", row)
        self.assertIn("children,", row)
        self.assertIn("{children}", row)
        self.assertIn("<Link", cell)
        self.assertIn("tabIndex", cell)
        self.assertIn("z-0", cell)
        self.assertIn("relative z-10", asset)

    def test_create_and_update_forms_use_sections_and_two_columns(self) -> None:
        content = TEMPLATE.read_text(encoding="utf-8")
        specialist = SKILL.read_text(encoding="utf-8")
        for term in (
            "seções",
            "duas colunas",
            "coluna de contexto",
            "grid-cols-2",
            "mobile",
        ):
            self.assertIn(term, content + specialist)

    def test_laravel_reuses_existing_breadcrumb_and_includes_current_team(self) -> None:
        layout = LARAVEL_APP_LAYOUT.read_text(encoding="utf-8")
        breadcrumb = LARAVEL_BREADCRUMBS.read_text(encoding="utf-8")
        primitive = LARAVEL_BREADCRUMB_PRIMITIVE.read_text(encoding="utf-8")
        for term in (
            "usePage",
            "currentTeam",
            "currentTeam.name",
            "dashboard(currentTeam.slug)",
            "AppLayoutTemplate breadcrumbs={breadcrumbsWithTeam}",
        ):
            self.assertIn(term, layout)
        self.assertIn("export function Breadcrumbs", breadcrumb)
        self.assertIn('aria-label="breadcrumb"', primitive)

    def test_skill_declares_defaults_and_scoped_exceptions(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        for term in (
            "DESIGNSYSTEM.MD",
            "não informa direção visual",
            "defaults",
            "exceções",
            "alcance",
            "personalidade",
            "hierarquia",
        ):
            self.assertIn(term, content)

    def test_cli_catalog_and_interface_template_are_wired(self) -> None:
        installer = INSTALLER.read_text(encoding="utf-8")
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        interface = INTERFACE.read_text(encoding="utf-8")
        self.assertIn('"DESIGNSYSTEM.MD"', installer)
        self.assertIn("DESIGNSYSTEM.MD", interface)
        self.assertIn("Padrão de dashboard", interface)
        self.assertIn("ReUI", interface)

        entries = {entry["name"]: entry for entry in catalog["skills"]}
        self.assertIn("specsfy-specialist-design-system", entries)
        for name in (
            "specsfy-specialist-interface-experience",
            "specsfy-specialist-ui-design",
            "specsfy-specialist-ux-design",
            "specsfy-specialist-react-ui-components",
        ):
            self.assertIn("specsfy-specialist-design-system", entries[name].get("requires", []))

    def test_setup_creates_and_preserves_design_system_template(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            templates = project / ".specsfy" / "templates"
            templates.mkdir(parents=True)
            for name in (
                "Project.md",
                "Stack.md",
                "Rules.md",
                "Database.md",
                "Interface.md",
                "DESIGNSYSTEM.MD",
            ):
                source = ROOT / "skills" / "templates" / name
                (templates / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            first_run = subprocess.run(
                ["node", str(SETUP_SCRIPT), "--project", str(project)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(first_run.returncode, 0, first_run.stderr)
            design_system = project / "DESIGNSYSTEM.MD"
            self.assertEqual(
                design_system.read_text(encoding="utf-8"),
                TEMPLATE.read_text(encoding="utf-8").rstrip() + "\n",
            )

            local_content = "# Direção local\n\nEste conteúdo pertence ao produto.\n"
            design_system.write_text(local_content, encoding="utf-8")
            second_run = subprocess.run(
                ["node", str(SETUP_SCRIPT), "--project", str(project)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(second_run.returncode, 0, second_run.stderr)
            self.assertEqual(design_system.read_text(encoding="utf-8"), local_content)


if __name__ == "__main__":
    unittest.main()

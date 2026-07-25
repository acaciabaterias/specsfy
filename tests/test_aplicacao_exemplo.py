from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ROOT = ROOT / "example"
EXAMPLE_README = EXAMPLE_ROOT / "README.md"
DOCS_ROOT = ROOT / "docs"
LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:)([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


def markdown_anchor(title: str) -> str:
    value = re.sub(r"[^\w\s-]", "", title.casefold())
    return re.sub(r"[\s-]+", "-", value).strip("-")


def heading_anchors(path: Path) -> set[str]:
    return {
        markdown_anchor(title)
        for title in HEADING.findall(path.read_text(encoding="utf-8"))
    }


def local_links(path: Path) -> list[tuple[Path, str]]:
    links: list[tuple[Path, str]] = []
    for raw in LOCAL_LINK.findall(path.read_text(encoding="utf-8")):
        target = unquote(raw.strip().strip("<>"))
        relative, separator, anchor = target.partition("#")
        destination = path if not relative else (path.parent / relative).resolve()
        links.append((destination, anchor if separator else ""))

    return links


class ExampleApplicationDocumentationTest(unittest.TestCase):
    """SPECSFY: FR-001 FR-002 FR-003 FR-004 FR-005 AC-001."""

    def test_readme_covers_application_contract(self) -> None:
        self.assertTrue(EXAMPLE_README.is_file(), "example/README.md ausente")
        text = EXAMPLE_README.read_text(encoding="utf-8")

        for heading in (
            "## Papel no Specsfy",
            "## Capacidades demonstradas",
            "## Arquitetura",
            "## Persistência e dados",
            "## Rotas e jornadas",
            "## Preparar o ambiente",
            "## Executar",
            "## Qualidade e testes",
            "## Mapa de referências",
        ):
            self.assertIn(heading, text, f"seção ausente: {heading}")

        for capability in (
            "autenticação",
            "perfil",
            "passkey",
            "dois fatores",
            "equipe",
            "owner",
            "admin",
            "member",
            "convite",
        ):
            self.assertIn(capability, text.casefold(), f"capacidade ausente: {capability}")

        self.assertIn("documentação oficial", text.casefold())
        self.assertIn("ambiente interno", text.casefold())

    def test_readme_references_executable_sources(self) -> None:
        self.assertTrue(EXAMPLE_README.is_file(), "example/README.md ausente")
        destinations = {destination for destination, _ in local_links(EXAMPLE_README)}
        required = {
            EXAMPLE_ROOT / "composer.json",
            EXAMPLE_ROOT / "package.json",
            EXAMPLE_ROOT / ".env.example",
            EXAMPLE_ROOT / "routes" / "web.php",
            EXAMPLE_ROOT / "routes" / "settings.php",
            EXAMPLE_ROOT / "app" / "Models" / "User.php",
            EXAMPLE_ROOT / "app" / "Models" / "Team.php",
            EXAMPLE_ROOT / "database" / "migrations",
            EXAMPLE_ROOT / "resources" / "js" / "pages",
            EXAMPLE_ROOT / "tests",
        }
        missing = sorted(path for path in required if path.resolve() not in destinations)
        self.assertEqual([], missing, f"fontes sem link no README: {missing}")


class DocumentationBoundaryTest(unittest.TestCase):
    """SPECSFY: FR-006 FR-007 FR-008 FR-009 FR-010 AC-002."""

    def test_documentation_authority_and_example_owner_are_explicit(self) -> None:
        sources = {
            "workspace": ROOT / "README.md",
            "project": DOCS_ROOT / "context" / "project.md",
            "architecture": DOCS_ROOT / "context" / "architecture" / "README.md",
            "modules": DOCS_ROOT / "context" / "architecture" / "modules.md",
            "dependencies": DOCS_ROOT / "context" / "architecture" / "dependencies.md",
            "stack": DOCS_ROOT / "context" / "engineering" / "stack.md",
            "testing": DOCS_ROOT / "context" / "engineering" / "testing.md",
            "persistence": DOCS_ROOT / "context" / "data" / "persistence.md",
        }
        texts = {
            name: path.read_text(encoding="utf-8").casefold()
            for name, path in sources.items()
        }

        self.assertIn("example/", texts["workspace"])
        self.assertIn("specsfy/dev", texts["workspace"])
        self.assertIn("documentação oficial", texts["project"])
        self.assertIn("usuários", texts["project"])
        for name in ("architecture", "modules", "dependencies"):
            self.assertIn("example/", texts[name], f"{name} não referencia example/")
        self.assertIn("aplicação interna", texts["architecture"])
        self.assertIn("specsfy/dev", texts["modules"])
        for name in ("stack", "testing", "persistence"):
            self.assertIn("example/", texts[name], f"{name} não referencia example/")

    def test_every_change_requires_documentation(self) -> None:
        agent_guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8").casefold()
        conventions = (
            DOCS_ROOT / "context" / "engineering" / "conventions.md"
        ).read_text(encoding="utf-8").casefold()

        for text, source in (
            (agent_guide, "AGENTS.md"),
            (conventions, "conventions.md"),
        ):
            self.assertIn("toda criação ou alteração", text, source)
            self.assertIn("mesma entrega", text, source)
            self.assertIn("documentação", text, source)


class DocumentationIntegrityTest(unittest.TestCase):
    """SPECSFY: FR-011 FR-012 NFR-001 NFR-002 NFR-003 AC-003."""

    def test_local_markdown_links_and_anchors_resolve(self) -> None:
        documents = (
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            EXAMPLE_README,
            DOCS_ROOT / "README.md",
            *(DOCS_ROOT / "context").rglob("*.md"),
        )
        checked = 0
        for path in documents:
            self.assertTrue(path.is_file(), f"documento ausente: {path}")
            for destination, anchor in local_links(path):
                checked += 1
                self.assertTrue(
                    destination.exists(),
                    f"link quebrado: {path.relative_to(ROOT)} -> {destination}",
                )
                if anchor:
                    self.assertTrue(destination.is_file())
                    self.assertIn(
                        anchor,
                        heading_anchors(destination),
                        f"âncora quebrada: {path.relative_to(ROOT)} -> "
                        f"{destination}#{anchor}",
                    )
        self.assertGreater(checked, 0, "nenhum link local foi auditado")

    def test_documented_routes_and_commands_exist(self) -> None:
        self.assertTrue(EXAMPLE_README.is_file(), "example/README.md ausente")
        text = EXAMPLE_README.read_text(encoding="utf-8")
        route_result = subprocess.run(
            ["php", "artisan", "route:list", "--json"],
            cwd=EXAMPLE_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            0,
            route_result.returncode,
            route_result.stdout + route_result.stderr,
        )
        routes = json.loads(route_result.stdout)
        route_names = {route["name"] for route in routes if route.get("name")}
        documented_routes = set(re.findall(r"`route:([^`]+)`", text))
        self.assertTrue(documented_routes, "nenhuma rota nomeada documentada")
        self.assertEqual(
            set(),
            documented_routes - route_names,
            "README referencia rotas nomeadas ausentes",
        )

        composer = json.loads((EXAMPLE_ROOT / "composer.json").read_text(encoding="utf-8"))
        package = json.loads((EXAMPLE_ROOT / "package.json").read_text(encoding="utf-8"))
        documented_composer = set(re.findall(r"`composer ([a-z][\w:-]+)`", text))
        documented_npm = set(re.findall(r"`npm run ([a-z][\w:-]+)`", text))
        self.assertTrue(documented_composer)
        self.assertTrue(documented_npm)
        self.assertEqual(set(), documented_composer - composer["scripts"].keys())
        self.assertEqual(set(), documented_npm - package["scripts"].keys())


if __name__ == "__main__":
    unittest.main()

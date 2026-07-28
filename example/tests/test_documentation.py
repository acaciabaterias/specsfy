from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:)([^)]+)\)")


def local_destinations(path: Path) -> set[Path]:
    destinations: set[Path] = set()
    for raw in LOCAL_LINK.findall(path.read_text(encoding="utf-8")):
        target = unquote(raw.strip().strip("<>")).partition("#")[0]
        destination = path if not target else (path.parent / target).resolve()
        destinations.add(destination)

    return destinations


class ExampleDocumentationTest(unittest.TestCase):
    def test_readme_covers_application_contract(self) -> None:
        self.assertTrue(README.is_file(), "README.md ausente")
        text = README.read_text(encoding="utf-8")

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
            self.assertIn(capability, text.casefold(), capability)

        self.assertIn("documentação oficial", text.casefold())
        self.assertIn("ambiente interno", text.casefold())

    def test_readme_references_executable_sources(self) -> None:
        destinations = local_destinations(README)
        required = {
            ROOT / "composer.json",
            ROOT / "package.json",
            ROOT / ".env.example",
            ROOT / "routes" / "web.php",
            ROOT / "routes" / "settings.php",
            ROOT / "app" / "Models" / "User.php",
            ROOT / "app" / "Models" / "Team.php",
            ROOT / "database" / "migrations",
            ROOT / "resources" / "js" / "pages",
            ROOT / "tests",
        }
        missing = sorted(path for path in required if path.resolve() not in destinations)
        self.assertEqual([], missing, f"fontes sem link no README: {missing}")
        self.assertTrue(all(destination.exists() for destination in destinations))

    def test_documented_routes_and_commands_exist(self) -> None:
        text = README.read_text(encoding="utf-8")
        route_result = subprocess.run(
            ["php", "artisan", "route:list", "--json"],
            cwd=ROOT,
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
        self.assertTrue(documented_routes)
        self.assertEqual(set(), documented_routes - route_names)

        composer = json.loads((ROOT / "composer.json").read_text(encoding="utf-8"))
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        documented_composer = set(re.findall(r"`composer ([a-z][\w:-]+)`", text))
        documented_npm = set(re.findall(r"`npm run ([a-z][\w:-]+)`", text))
        self.assertTrue(documented_composer)
        self.assertTrue(documented_npm)
        self.assertEqual(set(), documented_composer - composer["scripts"].keys())
        self.assertEqual(set(), documented_npm - package["scripts"].keys())


if __name__ == "__main__":
    unittest.main()

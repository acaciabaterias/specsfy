from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from specsfy_cli.catalog import Catalog, CatalogEntry


class CatalogTests(unittest.TestCase):
    def test_loads_and_detects_file_and_dependency_markers(self) -> None:
        entries = {
            "schema_version": 1,
            "skills": [
                {
                    "name": "specsfy-specialist-nextjs",
                    "description": "Next.js",
                    "category": "frontend",
                    "tags": ["nextjs"],
                    "detect": {"files": ["next.config.ts"], "dependencies": ["next"]},
                },
                {
                    "name": "specsfy-specialist-ui-design",
                    "description": "UI",
                    "category": "design",
                    "tags": ["ui"],
                    "detect": {"files": [], "dependencies": []},
                },
                {
                    "name": "specsfy-specialist-react-ui-components",
                    "description": "React UI",
                    "category": "design",
                    "tags": ["react", "ui"],
                    "requires": ["specsfy-specialist-ui-design"],
                    "detect": {
                        "files": [],
                        "dependencies": ["react", "tailwindcss"],
                    },
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            catalog_path = project / "catalog.json"
            catalog_path.write_text(json.dumps(entries), encoding="utf-8")
            (project / "package.json").write_text(
                json.dumps({"dependencies": {"next": "1"}}), encoding="utf-8"
            )
            catalog = Catalog.from_path(catalog_path)

            self.assertEqual(
                ["specsfy-specialist-nextjs"],
                [entry.name for entry in catalog.detect(project)],
            )
            self.assertEqual(
                "specsfy-specialist-ui-design",
                catalog.require("specsfy-specialist-ui-design").name,
            )
            self.assertEqual(
                [
                    "specsfy-specialist-ui-design",
                    "specsfy-specialist-react-ui-components",
                ],
                [
                    entry.name
                    for entry in catalog.resolve(
                        ["specsfy-specialist-react-ui-components"]
                    )
                ],
            )

    def test_rejects_unknown_or_non_namespaced_skill(self) -> None:
        catalog = Catalog([])
        with self.assertRaisesRegex(ValueError, "não encontrada"):
            catalog.require("specsfy-specialist-unknown")
        with self.assertRaisesRegex(ValueError, "prefixo"):
            catalog.require("unknown")

    def test_rejects_circular_specialist_dependencies(self) -> None:
        def entry(name: str, requires: tuple[str, ...]) -> CatalogEntry:
            return CatalogEntry(
                name=name,
                description=name,
                category="design",
                tags=(),
                files=(),
                dependencies=(),
                requires=requires,
            )

        first = "specsfy-specialist-first"
        second = "specsfy-specialist-second"
        catalog = Catalog(
            [
                entry(first, (second,)),
                entry(second, (first,)),
            ]
        )

        with self.assertRaisesRegex(ValueError, "dependência circular"):
            catalog.resolve([first])

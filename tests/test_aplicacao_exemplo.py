from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"


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
        self.assertIn("specsfy/example", texts["workspace"])
        self.assertIn("documentação oficial", texts["project"])
        self.assertIn("usuários", texts["project"])
        for name in ("architecture", "modules", "dependencies"):
            self.assertIn(
                "specsfy/example",
                texts[name],
                f"{name} não referencia specsfy/example",
            )
        self.assertIn("aplicação interna", texts["architecture"])
        self.assertIn("specsfy/example", texts["modules"])
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


if __name__ == "__main__":
    unittest.main()

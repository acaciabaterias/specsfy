from __future__ import annotations

import re
import unittest
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"
CONTEXT_ROOT = DOCS_ROOT / "context"
COMMON_HEADINGS = (
    "## Classificação",
    "## Papel",
    "## Como usar",
    "## Atualize quando",
    "## Não use para",
    "## Fonte da verdade e precedência",
)
CLASSIFICATION_FIELDS = ("Natureza", "Escopo", "Autoridade")
CLASSIFICATION_VALUES = {"índice", "normativo", "descritivo", "histórico"}
GENERAL_GUIDE_HEADINGS = (
    "## Como a documentação está organizada",
    "## Como navegar",
    "## Autoridade das fontes",
    "## Onde registrar cada informação",
    "## Quando criar um documento",
    "## Como manter a documentação",
)
MINIMUM_PATHS = {
    "docs/README.md",
    "docs/context/README.md",
    "docs/context/project.md",
    "docs/context/glossary.md",
    "docs/context/architecture/README.md",
    "docs/context/architecture/modules.md",
    "docs/context/architecture/dependencies.md",
    "docs/context/engineering/README.md",
    "docs/context/engineering/stack.md",
    "docs/context/engineering/packages.md",
    "docs/context/engineering/conventions.md",
    "docs/context/engineering/testing.md",
    "docs/context/data/README.md",
    "docs/context/data/persistence.md",
    "docs/context/data/privacy.md",
    "docs/context/flows/README.md",
    "docs/decisions/README.md",
}
REQUIRED_CONTENT_HEADINGS = {
    "docs/README.md": ("## Mapa da documentação", *GENERAL_GUIDE_HEADINGS),
    "docs/context/README.md": (
        "## Roteamento por tipo de alteração",
        "## Precedência das fontes",
    ),
    "docs/context/project.md": (
        "## Problema e finalidade",
        "## Limites normativos",
    ),
    "docs/context/glossary.md": (
        "## Termos canônicos",
        "## Regras de vocabulário",
    ),
    "docs/context/architecture/README.md": (
        "## Roteamento de arquitetura",
        "## Visão arquitetural",
        "## Integrações",
        "## Invariantes transversais",
    ),
    "docs/context/engineering/README.md": (
        "## Roteamento de engenharia",
    ),
    "docs/context/data/README.md": (
        "## Roteamento de dados",
        "## Migrations",
    ),
    "docs/context/flows/README.md": (
        "## Fluxos transversais",
        "## Contrato de um fluxo",
    ),
    "docs/decisions/README.md": (
        "## Índice de decisões",
        "## Ciclo de vida de um ADR",
        "## Formato de um ADR",
    ),
}
DOMAIN_INDEXES = (
    CONTEXT_ROOT / "architecture" / "README.md",
    CONTEXT_ROOT / "engineering" / "README.md",
    CONTEXT_ROOT / "data" / "README.md",
)
PREVENTIVE_FILES = (
    CONTEXT_ROOT / "architecture" / "integrations.md",
    CONTEXT_ROOT / "data" / "migrations.md",
)
LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:)([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


def documentation_files() -> set[Path]:
    return {path.resolve() for path in DOCS_ROOT.rglob("*.md") if path.is_file()}


def split_target(raw: str) -> tuple[str, str]:
    target = raw.strip().strip("<>")
    path, separator, anchor = target.partition("#")
    return path, anchor if separator else ""


def anchor_for(title: str) -> str:
    value = re.sub(r"[^\w\s-]", "", title.casefold())
    return re.sub(r"[\s-]+", "-", value).strip("-")


def heading_anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return {anchor_for(title) for title in HEADING.findall(text)}


def local_links(path: Path) -> list[tuple[Path, str]]:
    text = path.read_text(encoding="utf-8")
    links: list[tuple[Path, str]] = []
    for raw in LOCAL_LINK.findall(text):
        relative, anchor = split_target(raw)
        destination = path if not relative else (path.parent / relative).resolve()
        links.append((destination, anchor))
    return links


def reachable_documents(start: Path) -> set[Path]:
    reached: set[Path] = set()
    pending: deque[Path] = deque([start.resolve()])
    while pending:
        path = pending.popleft()
        if path in reached or not path.is_file() or path.suffix.casefold() != ".md":
            continue
        reached.add(path)
        for destination, _ in local_links(path):
            if destination.is_file() and destination.is_relative_to(DOCS_ROOT.resolve()):
                pending.append(destination)
    return reached


def classification(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    result: dict[str, str] = {}
    for field in CLASSIFICATION_FIELDS:
        match = re.search(
            rf"^\|\s*{re.escape(field)}\s*\|\s*([^|]+?)\s*\|$",
            text,
            re.MULTILINE,
        )
        if match:
            result[field] = match.group(1).strip()
    return result


class ProjectContextContractTests(unittest.TestCase):
    """SPECSFY: US-001 US-002 US-003 FR-001 FR-002 FR-003 FR-004 FR-005 FR-006 FR-007 FR-008 FR-009 FR-010 FR-011 FR-012 FR-013 FR-014 NFR-001 NFR-002 NFR-003 AC-001 AC-002 AC-003 AC-004 AC-005"""

    def test_minimum_tree_exists_without_preventive_leaf_files(self) -> None:
        observed = {
            path.relative_to(ROOT).as_posix() for path in documentation_files()
        }
        self.assertTrue(MINIMUM_PATHS <= observed, MINIMUM_PATHS - observed)
        for path in PREVENTIVE_FILES:
            self.assertFalse(path.exists(), f"arquivo preventivo: {path}")

    def test_every_document_declares_contract_classification_and_specific_role(self) -> None:
        for path in sorted(documentation_files()):
            relative = path.relative_to(ROOT).as_posix()
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertRegex(text, r"\A# .+")
                for heading in COMMON_HEADINGS:
                    self.assertIn(heading, text)
                values = classification(path)
                self.assertEqual(set(CLASSIFICATION_FIELDS), set(values))
                self.assertIn(values["Natureza"].casefold(), CLASSIFICATION_VALUES)
                self.assertTrue(values["Escopo"])
                self.assertTrue(values["Autoridade"])
                for heading in REQUIRED_CONTENT_HEADINGS.get(relative, ()):
                    self.assertIn(heading, text)

    def test_all_documents_are_reachable_from_portal(self) -> None:
        documents = documentation_files()
        reached = reachable_documents(DOCS_ROOT / "README.md")
        self.assertEqual(documents, reached, f"órfãos: {documents - reached}")

    def test_local_links_resolve_files_and_anchors(self) -> None:
        for path in sorted(documentation_files()):
            for destination, anchor in local_links(path):
                with self.subTest(source=path.relative_to(ROOT), target=destination):
                    self.assertTrue(destination.exists())
                    if anchor:
                        self.assertTrue(destination.is_file())
                        self.assertIn(anchor, heading_anchors(destination))

    def test_hierarchical_indexes_route_to_exact_leaf_files(self) -> None:
        root_router = (CONTEXT_ROOT / "README.md").read_text(encoding="utf-8")
        for index in DOMAIN_INDEXES:
            with self.subTest(index=index.relative_to(ROOT)):
                self.assertTrue(index.is_file())
                relative = index.relative_to(CONTEXT_ROOT).as_posix()
                self.assertIn(f"]({relative})", root_router)
                text = index.read_text(encoding="utf-8")
                self.assertIn("Leia quando", text)
                self.assertIn("Atualize quando", text)
        direct_leaf_links = re.findall(
            r"\]\(((?:architecture|engineering|data)/(?!README\.md)[^)]+\.md)\)",
            root_router,
        )
        self.assertEqual([], direct_leaf_links)

    def test_agent_routes_are_exact_and_human_readme_only_presents(self) -> None:
        agent_guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/context/README.md", agent_guide)
        self.assertIn("docs/README.md", readme)
        broad_routes = re.findall(r"`(docs/context/(?:architecture|engineering|data)/)`", agent_guide)
        self.assertEqual([], broad_routes)
        self.assertIn("apresentação", readme.casefold())
        project = (CONTEXT_ROOT / "project.md").read_text(encoding="utf-8")
        self.assertIn("## Limites normativos", project)
        self.assertNotIn("## Capacidades", project)

    def test_docs_readme_is_general_guide_without_operational_routing(self) -> None:
        guide = (DOCS_ROOT / "README.md").read_text(encoding="utf-8")
        router = (CONTEXT_ROOT / "README.md").read_text(encoding="utf-8")
        for heading in GENERAL_GUIDE_HEADINGS:
            self.assertIn(heading, guide)
        self.assertIn("](context/README.md)", guide)
        operational_heading = "## Roteamento por tipo de alteração"
        self.assertNotIn(operational_heading, guide)
        self.assertIn(operational_heading, router)

    def test_size_policy_uses_review_threshold_and_hard_limit(self) -> None:
        for path in sorted(documentation_files()):
            text = path.read_text(encoding="utf-8")
            lines = len(text.splitlines())
            with self.subTest(path=path.relative_to(ROOT), lines=lines):
                self.assertLessEqual(lines, 400)
                if lines > 250:
                    self.assertIn("## Justificativa de tamanho", text)

    def test_context_is_free_of_editorial_markers(self) -> None:
        forbidden = ("TO" + "DO", "T" + "BD", "[preencher]", "Última atualização")
        for path in sorted(documentation_files()):
            text = path.read_text(encoding="utf-8")
            for marker in forbidden:
                with self.subTest(path=path.relative_to(ROOT), marker=marker):
                    self.assertNotIn(marker, text)

    def test_every_adr_is_listed_in_decision_index(self) -> None:
        index = (DOCS_ROOT / "decisions" / "README.md").read_text(encoding="utf-8")
        adrs = sorted((DOCS_ROOT / "decisions").glob("ADR-*.md"))
        for adr in adrs:
            with self.subTest(adr=adr.name):
                self.assertIn(adr.name, index)

    def test_context_points_to_executable_sources_instead_of_copying_inventories(self) -> None:
        packages = (
            CONTEXT_ROOT / "engineering" / "packages.md"
        ).read_text(encoding="utf-8")
        persistence = (
            CONTEXT_ROOT / "data" / "persistence.md"
        ).read_text(encoding="utf-8")
        flows = (CONTEXT_ROOT / "flows" / "README.md").read_text(encoding="utf-8")
        self.assertIn("manifests e lockfiles", packages.casefold())
        self.assertIn("schemas e migrations", persistence.casefold())
        self.assertIn("specs/<slug>/spec.md", flows)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import re
from collections import deque
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
DOCS_ROOT = ROOT / "docs"
DEVELOP_ROOT = DOCS_ROOT / "develop"
CONTEXT_ROOT = DEVELOP_ROOT / "context"
COMMON_HEADINGS = (
    "## Classificação",
    "## Papel",
    "## Como usar",
    "## Atualize quando",
    "## Não use para",
    "## Fonte da verdade e precedência",
)
DOMAIN_INDEXES = (
    CONTEXT_ROOT / "architecture" / "README.md",
    CONTEXT_ROOT / "engineering" / "README.md",
    CONTEXT_ROOT / "data" / "README.md",
)
LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:)([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


def markdown_files() -> set[Path]:
    return {path.resolve() for path in DOCS_ROOT.rglob("*.md") if path.is_file()}


def context_contract_files() -> set[Path]:
    return {
        path.resolve()
        for root in (CONTEXT_ROOT, DEVELOP_ROOT / "decisions")
        for path in root.rglob("*.md")
        if path.is_file()
    }


def split_target(raw: str) -> tuple[str, str]:
    target = raw.strip().strip("<>")
    path, separator, anchor = target.partition("#")
    return path, anchor if separator else ""


def anchor_for(title: str) -> str:
    value = re.sub(r"[^\w\s-]", "", title.casefold())
    return re.sub(r"[\s-]+", "-", value).strip("-")


def heading_anchors(path: Path) -> set[str]:
    return {anchor_for(title) for title in HEADING.findall(path.read_text(encoding="utf-8"))}


def local_links(path: Path) -> list[tuple[Path, str]]:
    links: list[tuple[Path, str]] = []
    for raw in LOCAL_LINK.findall(path.read_text(encoding="utf-8")):
        target, anchor = split_target(raw)
        destination = path if not target else (path.parent / target).resolve()
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


@given("o repositório Specsfy e o contrato vigente da biblioteca de contexto")
def given_repository_and_contract(context) -> None:
    context.root = ROOT


@when("a biblioteca de contexto é inspecionada")
def when_context_library_is_inspected(context) -> None:
    context.context_files = sorted(context_contract_files())


@then("cada documento explica seu papel, classificação e regras de uso")
def then_documents_explain_contract(context) -> None:
    assert context.context_files, "nenhum documento encontrado"
    for path in context.context_files:
        text = path.read_text(encoding="utf-8")
        absent = [heading for heading in COMMON_HEADINGS if heading not in text]
        assert not absent, f"{path.relative_to(ROOT)} sem headings: {absent}"
        for field in ("Natureza", "Escopo", "Autoridade"):
            assert f"| {field} |" in text, f"{path.relative_to(ROOT)} sem {field}"


@then("os contextos respeitam a política de tamanho e os links locais")
def then_contexts_respect_size_and_links(context) -> None:
    for path in context.context_files:
        text = path.read_text(encoding="utf-8")
        lines = len(text.splitlines())
        assert lines <= 400, f"{path.relative_to(ROOT)} possui {lines} linhas"
        if lines > 250:
            assert "## Justificativa de tamanho" in text
        for destination, anchor in local_links(path):
            assert destination.exists(), f"link quebrado: {path} -> {destination}"
            if anchor:
                assert destination.is_file(), f"âncora aponta para diretório: {destination}"
                assert anchor in heading_anchors(destination), (
                    f"âncora quebrada: {path.relative_to(ROOT)} -> {destination}#{anchor}"
                )


@given("as portas de entrada e os índices hierárquicos da biblioteca")
def given_entrypoints_and_indexes(context) -> None:
    context.agent_guide = ROOT / "AGENTS.md"
    context.human_guide = ROOT / "README.md"
    context.router = CONTEXT_ROOT / "README.md"
    context.domain_indexes = DOMAIN_INDEXES


@when("uma pessoa ou agente procura orientação para uma mudança")
def when_someone_seeks_change_guidance(context) -> None:
    paths = (
        context.agent_guide,
        context.human_guide,
        context.router,
        *context.domain_indexes,
    )
    context.entrypoint_text = {
        path: path.read_text(encoding="utf-8") if path.is_file() else ""
        for path in paths
    }


@then("encontra arquivos exatos de leitura e atualização por tipo de alteração")
def then_finds_exact_routes(context) -> None:
    agent_text = context.entrypoint_text[context.agent_guide]
    human_text = context.entrypoint_text[context.human_guide]
    router_text = context.entrypoint_text[context.router]
    assert "docs/develop/context/README.md" in agent_text
    assert "docs/README.md" in human_text
    for broad_route in (
        "`docs/develop/context/architecture/`",
        "`docs/develop/context/engineering/`",
        "`docs/develop/context/data/`",
    ):
        assert broad_route not in agent_text, f"rota ampla encontrada: {broad_route}"
    for index in context.domain_indexes:
        assert index.is_file(), f"índice ausente: {index.relative_to(ROOT)}"
        relative = index.relative_to(CONTEXT_ROOT).as_posix()
        assert relative in router_text
        domain_text = context.entrypoint_text[index]
        assert "Leia quando" in domain_text
        assert "Atualize quando" in domain_text


@then("encontra a precedência entre contexto, especificação e fonte executável")
def then_finds_source_precedence(context) -> None:
    router_text = context.entrypoint_text[context.router]
    assert "specs/specs/<NNNN>-<slug>/spec.md" in router_text
    assert "fontes executáveis" in router_text
    assert "AGENTS.md" in router_text


@given("a árvore de documentação e seus índices")
def given_documentation_tree(context) -> None:
    context.portal = DOCS_ROOT / "README.md"
    context.documents = markdown_files()


@when("o contrato percorre links e decisões arquiteturais")
def when_contract_traverses_docs(context) -> None:
    context.reached = reachable_documents(context.portal)
    context.adr_files = {
        path.resolve()
        for path in (DEVELOP_ROOT / "decisions").glob("ADR-*.md")
        if path.is_file()
    }


@then("todo documento é alcançável a partir do portal")
def then_all_documents_are_reachable(context) -> None:
    orphaned = sorted(context.documents - context.reached)
    assert not orphaned, (
        "documentos órfãos: "
        + ", ".join(str(path.relative_to(ROOT)) for path in orphaned)
    )


@then("cada arquivo, âncora e ADR referenciado existe")
def then_every_target_and_adr_exists(context) -> None:
    for path in context.documents:
        for destination, anchor in local_links(path):
            assert destination.exists(), f"destino ausente: {path} -> {destination}"
            if anchor:
                assert anchor in heading_anchors(destination)
    decision_index = (DEVELOP_ROOT / "decisions" / "README.md").read_text(
        encoding="utf-8"
    )
    for adr in context.adr_files:
        assert adr.name in decision_index, f"ADR sem índice: {adr.name}"


@given("os contextos vigentes do Specsfy")
def given_current_contexts(context) -> None:
    context.architecture_index = CONTEXT_ROOT / "architecture" / "README.md"
    context.data_index = CONTEXT_ROOT / "data" / "README.md"


@when("a estrutura progressiva é inspecionada")
def when_progressive_structure_is_inspected(context) -> None:
    context.preventive_files = (
        CONTEXT_ROOT / "architecture" / "integrations.md",
        CONTEXT_ROOT / "data" / "migrations.md",
    )


@then("assuntos sem conteúdo independente permanecem no índice do domínio")
def then_premature_subjects_stay_in_indexes(context) -> None:
    assert not any(path.exists() for path in context.preventive_files)
    architecture = context.architecture_index.read_text(encoding="utf-8")
    data = context.data_index.read_text(encoding="utf-8")
    assert "Integrações" in architecture
    assert "Migrations" in data


@then("arquivos acima do limiar exigem justificativa em vez de divisão automática")
def then_large_files_require_justification(context) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        lines = len(text.splitlines())
        assert lines <= 400
        if lines > 250:
            assert "## Justificativa de tamanho" in text


@given("o guia geral e o roteador operacional da documentação")
def given_general_guide_and_operational_router(context) -> None:
    context.general_guide = DOCS_ROOT / "README.md"
    context.operational_router = CONTEXT_ROOT / "README.md"


@when("uma pessoa consulta como documentar uma mudança")
def when_person_consults_how_to_document(context) -> None:
    context.general_guide_text = context.general_guide.read_text(encoding="utf-8")
    context.operational_router_text = context.operational_router.read_text(
        encoding="utf-8"
    )


@then("encontra organização, autoridades e destinos para cada informação")
def then_finds_organization_authorities_and_destinations(context) -> None:
    assert "](user/README.md)" in context.general_guide_text
    assert "](develop/README.md)" in context.general_guide_text
    assert "## Fonte da verdade" in context.general_guide_text


@then("encontra critérios de criação e manutenção sem duplicar o roteador")
def then_finds_creation_and_maintenance_without_duplication(context) -> None:
    assert "docs/develop/context/" in context.general_guide_text
    operational_heading = "## Roteamento por tipo de alteração"
    assert operational_heading not in context.general_guide_text
    assert operational_heading in context.operational_router_text


@given("o monorepo e seus módulos públicos")
def given_orchestrator_and_child_repositories(context) -> None:
    context.repository_entrypoints = {
        "dev": ROOT / "README.md",
        "brand": ROOT / "brand" / "README.md",
        "skills": ROOT / "skills" / "README.md",
        "specialists": ROOT / "specialists" / "README.md",
        "cli": ROOT / "cli" / "README.md",
        "docs": ROOT / "docs" / "README.md",
        "specsfy": ROOT / "specsfy" / "README.md",
    }


@when("uma pessoa ou agente consulta suas portas de entrada")
def when_entrypoints_are_consulted(context) -> None:
    context.repository_texts = {
        name: path.read_text(encoding="utf-8") if path.is_file() else ""
        for name, path in context.repository_entrypoints.items()
    }


@then("cada módulo declara público responsabilidade e ownership")
def then_each_repository_declares_a_boundary(context) -> None:
    expected_terms = {
        "dev": ("monorepo", "módulos"),
        "brand": ("marca", "fonte normativa"),
        "skills": ("metodologia executável", "skills"),
        "specialists": ("catálogo oficial", "opcionais"),
        "cli": ("cli e tui", "progresso"),
        "docs": ("documentação", "usuário", "develop"),
        "specsfy": ("porta de entrada", "usuário final"),
    }
    for name, terms in expected_terms.items():
        text = context.repository_texts[name].casefold()
        assert text, f"README ausente para {name}"
        for term in terms:
            assert term.casefold() in text, f"{name}/README.md sem {term}"
    agent_guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8").casefold()
    assert "fronteiras git" in agent_guide
    assert "skills/agents.md" in agent_guide


@then("a metodologia documentação identidade e visão geral possuem módulos próprios")
def then_each_concern_has_one_owner(context) -> None:
    modules = (CONTEXT_ROOT / "architecture" / "modules.md").read_text(
        encoding="utf-8"
    )
    dependencies = (CONTEXT_ROOT / "architecture" / "dependencies.md").read_text(
        encoding="utf-8"
    )
    for repository in (
        "promovaweb/specsfy",
        "brand/",
        "skills/",
        "docs/",
        "example/",
        "specsfy/",
        "specialists/",
        "cli/",
    ):
        assert repository in modules, f"owner ausente: {repository}"
    assert "https://github.com/promovaweb/specsfy" in dependencies
    assert not (ROOT / ".gitmodules").exists()


@then("a raiz centraliza as regras de gitignore de todos os módulos")
def then_root_centralizes_module_gitignore_rules(context) -> None:
    root_gitignore = ROOT / ".gitignore"
    rules = root_gitignore.read_text(encoding="utf-8")
    for expected in (
        "/brand/guide/build/",
        "/cli/.venv/",
        "/cli/dist/",
        "/example/vendor/",
        "/example/node_modules/",
        "/example/storage/logs/*",
    ):
        assert expected in rules

    ignored_parts = {".venv", "dist", "node_modules", "vendor"}
    nested = []
    for module in ("brand", "cli", "docs", "example", "skills", "specialists", "specsfy"):
        nested.extend(
            candidate
            for candidate in (ROOT / module).rglob(".gitignore")
            if not ignored_parts.intersection(candidate.relative_to(ROOT).parts)
        )
    assert nested == []


@then("a raiz mantém só as skills locais operacionais e não instala as skills do projeto")
def then_parent_is_independent_from_project_skills(context) -> None:
    assert not (ROOT / "specs").exists()
    local_skills = {"specsfy-monorepo-documentator", "specsfy-release-cli"}
    assert {
        path.name for path in (ROOT / ".agents" / "skills").iterdir()
    } == local_skills
    for name in local_skills:
        codex_skill = ROOT / ".agents" / "skills" / name
        claude_skill = ROOT / ".claude" / "skills" / name
        assert (codex_skill / "SKILL.md").is_file()
        assert claude_skill.is_symlink()
        assert claude_skill.resolve() == codex_skill.resolve()
    forbidden = re.compile(
        r"skills/"
        + r"specsfy-(?!(?:monorepo-documentator|release-cli))[^/\s]+/scripts/"
    )
    for path in (
        ROOT / "AGENTS.md",
        ROOT / "README.md",
        *sorted((ROOT / "tests").rglob("*.py")),
        *sorted((ROOT / ".github" / "workflows").glob("*.yml")),
        *sorted((ROOT / ".github" / "workflows").glob("*.yaml")),
    ):
        assert forbidden.search(path.read_text(encoding="utf-8")) is None, path

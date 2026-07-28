from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]


@given("a skill de documentação do monorepo")
def given_monorepo_documentation_skill(context) -> None:
    context.skill_path = (
        ROOT / ".agents" / "skills" / "specsfy-monorepo-documentator" / "SKILL.md"
    )
    context.claude_skill_path = (
        ROOT / ".claude" / "skills" / "specsfy-monorepo-documentator"
    )


@when("sua identidade e fronteiras são inspecionadas")
def when_monorepo_boundaries_are_inspected(context) -> None:
    context.skill = context.skill_path.read_text(encoding="utf-8")
    context.collector = (
        ROOT
        / ".agents"
        / "skills"
        / "specsfy-monorepo-documentator"
        / "scripts"
        / "collect_monorepo_evidence.py"
    ).read_text(encoding="utf-8")
    context.installer = (
        ROOT / "cli" / "src" / "specsfy_cli" / "installer.py"
    ).read_text(encoding="utf-8")


@then("ela é descoberta nas pastas padrão de Codex e Claude")
def then_is_discovered_by_codex_and_claude(context) -> None:
    assert context.skill_path.is_file()
    assert context.claude_skill_path.is_symlink()
    assert context.claude_skill_path.resolve() == context.skill_path.parent.resolve()


@then("ela valida a raiz Git única e os módulos")
def then_validates_monorepo_modules(context) -> None:
    assert "show-toplevel" in context.collector
    for module in (
        "brand",
        "skills",
        "docs",
        "example",
        "specsfy",
        "specialists",
        "cli",
    ):
        assert module in context.collector


@then("ela publica em docs")
def then_publishes_only_in_docs(context) -> None:
    assert "docs/" in context.skill


@then("ela não é instalada pelo CLI em projetos consumidores")
def then_is_not_installed_for_consumers(context) -> None:
    assert "specsfy-monorepo-documentator" not in context.installer


@given("a fonte da verdade distribuída do Specsfy")
def given_distributed_sources(context) -> None:
    context.root = ROOT


@when("o contrato documental do monorepo é inspecionado")
def when_monorepo_documentation_contract_is_inspected(context) -> None:
    skill_root = ROOT / ".agents" / "skills" / "specsfy-monorepo-documentator"
    context.skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    context.standard = (
        skill_root / "references" / "documentation-standard.md"
    ).read_text(encoding="utf-8")
    context.guide = (
        ROOT / "docs" / "develop" / "documentation.md"
    ).read_text(encoding="utf-8")
    context.installation = ROOT / "docs" / "user" / "installation.md"
    context.router = (ROOT / "docs" / "user" / "README.md").read_text(
        encoding="utf-8"
    )
    context.cli_guide = (ROOT / "docs" / "user" / "cli.md").read_text(
        encoding="utf-8"
    )
    context.cli_readme = (ROOT / "cli" / "README.md").read_text(
        encoding="utf-8"
    )
    context.public_entrypoint = (
        ROOT / "specsfy" / "README.md"
    ).read_text(encoding="utf-8")
    context.basic_usage = (
        ROOT / "docs" / "user" / "getting-started.md"
    ).read_text(encoding="utf-8")


@then("ele roteia arquitetura módulos dependências stack dados fluxos e testes")
def then_routes_technical_docs(context) -> None:
    for term in (
        "arquitetura",
        "módulos",
        "dependências",
        "stack",
        "dados",
        "fluxos",
        "testes",
    ):
        assert term in context.standard


@then("ele roteia instalação método CLI contexto especialistas e documentação do sistema")
def then_routes_user_guides(context) -> None:
    for term in (
        "instalação",
        "método",
        "CLI",
        "contexto",
        "especialistas",
        "documentação do sistema",
    ):
        assert term in context.standard


@then("a documentação oficial explica como executar a skill do monorepo")
def then_official_docs_explain_monorepo_skill(context) -> None:
    assert "$specsfy-monorepo-documentator" in context.guide
    assert "monorepo" in context.guide


@then("a skill exige um guia temático de instalação em specsfy docs")
def then_skill_requires_installation_guide(context) -> None:
    for source in (context.skill, context.standard):
        assert "docs/user/installation.md" in source
    assert context.installation.is_file()


@then("o guia instala o CLI e o framework no projeto consumidor")
def then_guide_installs_cli_and_framework(context) -> None:
    installation = context.installation.read_text(encoding="utf-8")
    assert "Python 3.11" in installation
    assert "uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'" in installation
    assert "specsfy install --project ." in installation
    assert "specsfy --version" in installation
    assert ".agents/skills/specsfy-base-*" in installation
    assert ".specsfy/Spec.md" in installation


@then("o portal e o guia operacional do CLI apontam para a instalação")
def then_routes_point_to_installation(context) -> None:
    assert "[Instalação](installation.md)" in context.router
    assert "[guia de instalação](installation.md)" in context.cli_guide


@then("a porta pública ensina instalação atualização e primeiro uso")
def then_public_entrypoint_teaches_the_first_journey(context) -> None:
    for evidence in (
        "uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'",
        "specsfy --version",
        "specsfy install --project .",
        "uv tool upgrade specsfy-cli",
        "specsfy skills update --project .",
        "specsfy-base-idea",
        "specsfy-base-backlog",
        "Ato I — Definir",
        "Ato II — Projetar e provar",
        "Ato III — Entregar",
        "specsfy progress --project .",
    ):
        assert evidence in context.public_entrypoint


@then("os dois exemplos percorrem todas as skills base até a projeção final")
def then_examples_cover_the_complete_base_flow(context) -> None:
    base_flow = (
        "$specsfy-base-idea",
        "$specsfy-base-backlog",
        "$specsfy-base-interview",
        "$specsfy-base-specify",
        "$specsfy-base-validate",
        "$specsfy-base-tasks",
        "$specsfy-base-tdd-bdd",
        "$specsfy-base-implement",
        "$specsfy-base-update-spec",
        "$specsfy-base-progress",
    )
    for source in (context.public_entrypoint, context.basic_usage):
        for skill in base_flow:
            assert skill in source
        positions = [source.index(skill) for skill in base_flow]
        assert positions == sorted(positions)


@then("os exemplos mostram cada comando e seu resultado sem código de implementação")
def then_examples_show_each_command_and_result_without_source_code(context) -> None:
    practical_journey = (
        "### 1. Capture a ideia — `$specsfy-base-idea`",
        "### 2. Refine no backlog — `$specsfy-base-backlog`",
        "### 3. Tire as dúvidas — `$specsfy-base-interview`",
        "### 4. Crie a especificação — `$specsfy-base-specify`",
        "### 5. Confira a especificação — `$specsfy-base-validate`",
        "### 6. Divida o trabalho — `$specsfy-base-tasks`",
        "### 7. Prepare a verificação — `$specsfy-base-tdd-bdd`",
        "### 8. Implemente — `$specsfy-base-implement`",
        "### 9. Altere a especificação — `$specsfy-base-update-spec`",
        "### 10. Veja o progresso — `$specsfy-base-progress`",
    )
    for source in (context.public_entrypoint, context.basic_usage):
        for evidence in practical_journey:
            assert evidence in source
        for evidence in (
            "specs/ideias/2026-07-28-143205-pagina-boas-vindas.md",
            "specs/backlog/0001-pagina-boas-vindas.md",
            "Brief pronto para especificar",
            "specs/specs/0001-pagina-boas-vindas/spec.md",
            "READY",
            "2 tarefas preparadas",
            "Verificação preparada",
            "Implementação concluída",
            "Pedido incorporado na especificação 0001-pagina-boas-vindas",
            "Implementação atualizada",
            "Complete",
            "nenhuma pendência",
            "Use $specsfy-base-interview para aprofundar este texto:",
            "Use $specsfy-base-interview em specs/backlog/0001-pagina-boas-vindas.md",
            "Use $specsfy-base-specify para criar uma especificação a partir deste texto:",
            "Use $specsfy-base-specify para promover specs/backlog/0001-pagina-boas-vindas.md",
            "**Opção 1 — texto livre**",
            "**Opção 2 — arquivo de backlog**",
            "Use $specsfy-base-validate em specs/specs/0001-pagina-boas-vindas/spec.md",
            "Use $specsfy-base-tasks em specs/specs/0001-pagina-boas-vindas/spec.md",
            "Use $specsfy-base-tdd-bdd em specs/specs/0001-pagina-boas-vindas/spec.md",
            "Use $specsfy-base-implement em specs/specs/0001-pagina-boas-vindas/spec.md",
        ):
            assert evidence in source
        for code in ("<?php", "Route::", "test("):
            assert code not in source


@then("a porta pública oferece dicas operacionais do CLI")
def then_public_entrypoint_offers_cli_tips(context) -> None:
    for evidence in (
        "## Dicas para usar o CLI",
        "specsfy --help",
        "specsfy progress --project . --json",
        "specsfy progress --project . --watch",
        "Nada é instalado ou removido antes de **Aplicar**",
    ):
        assert evidence in context.public_entrypoint


@then("a documentação separa uso básico uso avançado repositórios e créditos")
def then_docs_separate_user_journeys(context) -> None:
    for filename in (
        "getting-started.md",
        "update-spec.md",
        "advanced-usage.md",
        "../develop/modules.md",
        "credits.md",
    ):
        assert (ROOT / "docs" / "user" / filename).is_file()
        assert f"]({filename})" in context.router


@then("Laravel Astro e Nextjs possuem guias temáticos verificáveis")
def then_framework_guides_are_verifiable(context) -> None:
    expectations = {
        "laravel.md": ("specsfy-specialist-laravel", "artisan", "composer.json"),
        "astro.md": ("specsfy-specialist-astro", "astro.config", "package.json"),
        "nextjs.md": ("specsfy-specialist-nextjs", "next.config", "package.json"),
    }
    for filename, evidence in expectations.items():
        path = ROOT / "docs" / "user" / filename
        assert path.is_file()
        guide = path.read_text(encoding="utf-8")
        assert f"]({filename})" in context.router
        for term in evidence:
            assert term in guide


@then("o guia do CLI incorpora as quatro capturas fornecidas")
def then_cli_guide_embeds_the_provided_screenshots(context) -> None:
    screenshots = (
        ("cli-dash.png", "Dashboard Home"),
        ("cli-backlogs.png", "Backlogs"),
        ("cli-specs.png", "Specs"),
        ("cli-skills.png", "Skills"),
    )
    for filename, alt_text in screenshots:
        path = ROOT / "docs" / "user" / "assets" / "cli" / filename
        assert path.is_file()
        assert path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
        assert f"![{alt_text}](assets/cli/{filename})" in context.cli_guide


@then("o README do módulo CLI empilha as quatro capturas verticalmente")
def then_cli_readme_stacks_screenshots_vertically(context) -> None:
    screenshots = (
        ("cli-dash.png", "Dashboard Home"),
        ("cli-backlogs.png", "Backlogs"),
        ("cli-specs.png", "Specs"),
        ("cli-skills.png", "Skills"),
    )
    stacked_screenshots = "\n\n".join(
        f"![{alt_text}](../docs/user/assets/cli/{filename})"
        for filename, alt_text in screenshots
    )
    assert stacked_screenshots in context.cli_readme


@then("a porta pública apresenta a visão Home do dashboard")
def then_public_entrypoint_previews_the_dashboard(context) -> None:
    assert "![Dashboard Home do Specsfy](../docs/user/assets/cli/cli-dash.png)" in (
        context.public_entrypoint
    )


@when("a nova topologia documental é inspecionada")
def when_new_documentation_topology_is_inspected(context) -> None:
    context.docs = ROOT / "docs"
    context.user_docs = context.docs / "user"
    context.develop_docs = context.docs / "develop"
    context.user_portal = (context.user_docs / "README.md").read_text(
        encoding="utf-8"
    )
    context.develop_portal = (context.develop_docs / "README.md").read_text(
        encoding="utf-8"
    )


@then("docs possui somente os percursos user e develop")
def then_docs_has_only_user_and_develop(context) -> None:
    directories = {
        path.name for path in context.docs.iterdir() if path.is_dir()
    }
    assert directories == {"user", "develop"}


@then("o percurso user oferece um guia geral simples para toda a jornada")
def then_user_route_has_complete_simple_guide(context) -> None:
    for term in (
        "Instalação",
        "Primeiro projeto",
        "Metodologia",
        "CLI e TUI",
        "Skills base",
        "Especialistas",
        "Documentação do sistema",
    ):
        assert term in context.user_portal


@then("cada skill base possui uma página de uso aprofundada com exemplo")
def then_each_base_skill_has_an_in_depth_page(context) -> None:
    skills = (
        "specsfy-base-idea",
        "specsfy-base-backlog",
        "specsfy-base-interview",
        "specsfy-base-specify",
        "specsfy-base-validate",
        "specsfy-base-tasks",
        "specsfy-base-tdd-bdd",
        "specsfy-base-implement",
        "specsfy-base-update-spec",
        "specsfy-base-progress",
    )
    for skill in skills:
        path = context.user_docs / "skills" / f"{skill}.md"
        assert path.is_file()
        page = path.read_text(encoding="utf-8")
        assert "## Exemplo passo a passo" in page
        assert "## O que esperar" in page


@then("o percurso develop explica metodologia arquitetura skills CLI e contribuição")
def then_develop_route_explains_framework_internals(context) -> None:
    for filename in (
        "methodology.md",
        "contributing.md",
        "skills.md",
        "cli.md",
    ):
        assert (context.develop_docs / filename).is_file()
        assert f"]({filename})" in context.develop_portal
    assert (context.develop_docs / "context" / "architecture" / "README.md").is_file()


@then("agentes e humanos encontram contexto técnico e validações no mesmo portal")
def then_agents_and_humans_share_technical_context(context) -> None:
    for term in ("agentes", "humanos", "contexto", "testes", "contribuir"):
        assert term in context.develop_portal.casefold()

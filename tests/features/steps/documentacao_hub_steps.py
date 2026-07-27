from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]


@given("a skill de documentação do hub")
def given_hub_documentation_skill(context) -> None:
    context.skill_path = (
        ROOT / ".agents" / "skills" / "specsfy-hub-documentator" / "SKILL.md"
    )
    context.claude_skill_path = (
        ROOT / ".claude" / "skills" / "specsfy-hub-documentator"
    )


@when("sua identidade e fronteiras são inspecionadas")
def when_hub_boundaries_are_inspected(context) -> None:
    context.skill = context.skill_path.read_text(encoding="utf-8")
    context.collector = (
        ROOT
        / ".agents"
        / "skills"
        / "specsfy-hub-documentator"
        / "scripts"
        / "collect_hub_evidence.py"
    ).read_text(encoding="utf-8")
    context.installer = (
        ROOT / "cli" / "src" / "specsfy_cli" / "installer.py"
    ).read_text(encoding="utf-8")


@then("ela é descoberta nas pastas padrão de Codex e Claude")
def then_is_discovered_by_codex_and_claude(context) -> None:
    assert context.skill_path.is_file()
    assert context.claude_skill_path.is_symlink()
    assert context.claude_skill_path.resolve() == context.skill_path.parent.resolve()


@then("ela valida as oito raízes Git do workspace")
def then_validates_eight_roots(context) -> None:
    for repository in (
        "dev",
        "brand",
        "skills",
        "docs",
        "example",
        "specsfy",
        "specialists",
        "cli",
    ):
        assert repository in context.collector


@then("ela publica somente no repositório specsfy docs")
def then_publishes_only_in_docs(context) -> None:
    assert "Somente `docs/`" in context.skill
    assert "specsfy/docs" in context.skill


@then("ela não é instalada pelo CLI em projetos consumidores")
def then_is_not_installed_for_consumers(context) -> None:
    assert "specsfy-hub-documentator" not in context.installer


@given("a fonte da verdade distribuída do Specsfy")
def given_distributed_sources(context) -> None:
    context.root = ROOT


@when("o contrato documental do hub é inspecionado")
def when_hub_documentation_contract_is_inspected(context) -> None:
    skill_root = ROOT / ".agents" / "skills" / "specsfy-hub-documentator"
    context.skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    context.standard = (
        skill_root / "references" / "documentation-standard.md"
    ).read_text(encoding="utf-8")
    context.guide = (
        ROOT / "docs" / "hub-documentation.md"
    ).read_text(encoding="utf-8")
    context.installation = ROOT / "docs" / "installation.md"
    context.router = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    context.cli_guide = (ROOT / "docs" / "cli.md").read_text(encoding="utf-8")
    context.public_entrypoint = (
        ROOT / "specsfy" / "README.md"
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


@then("a documentação oficial explica como executar a skill do hub")
def then_official_docs_explain_hub_skill(context) -> None:
    assert "$specsfy-hub-documentator" in context.guide
    assert "oito repositórios" in context.guide


@then("a skill exige um guia temático de instalação em specsfy docs")
def then_skill_requires_installation_guide(context) -> None:
    for source in (context.skill, context.standard):
        assert "docs/installation.md" in source
    assert context.installation.is_file()


@then("o guia instala o CLI e o framework no projeto consumidor")
def then_guide_installs_cli_and_framework(context) -> None:
    installation = context.installation.read_text(encoding="utf-8")
    assert "Python 3.11" in installation
    assert "uv tool install git+https://github.com/specsfy/cli" in installation
    assert "specsfy install --project ." in installation
    assert "specsfy --version" in installation
    assert ".agents/skills/specsfy-base-*" in installation
    assert ".specsfy/Spec.md" in installation


@then("o portal e o guia operacional do CLI apontam para a instalação")
def then_routes_point_to_installation(context) -> None:
    assert "[Guia de instalação](installation.md)" in context.router
    assert "[guia de instalação](installation.md)" in context.cli_guide


@then("a porta pública ensina instalação atualização e primeiro uso")
def then_public_entrypoint_teaches_the_first_journey(context) -> None:
    for evidence in (
        "uv tool install git+https://github.com/specsfy/cli",
        "specsfy --version",
        "specsfy install --project .",
        "uv tool upgrade specsfy-cli",
        "specsfy-base-backlog",
        "specsfy progress --project .",
    ):
        assert evidence in context.public_entrypoint


@then("a documentação separa uso básico uso avançado repositórios e créditos")
def then_docs_separate_user_journeys(context) -> None:
    for filename in (
        "basic-usage.md",
        "advanced-usage.md",
        "repositories.md",
        "credits.md",
    ):
        assert (ROOT / "docs" / filename).is_file()
        assert f"]({filename})" in context.router
        assert f"docs/{filename}" in context.standard


@then("Laravel Astro e Nextjs possuem guias temáticos verificáveis")
def then_framework_guides_are_verifiable(context) -> None:
    expectations = {
        "laravel.md": ("specsfy-specialist-laravel", "artisan", "composer.json"),
        "astro.md": ("specsfy-specialist-astro", "astro.config", "package.json"),
        "nextjs.md": ("specsfy-specialist-nextjs", "next.config", "package.json"),
    }
    for filename, evidence in expectations.items():
        path = ROOT / "docs" / filename
        assert path.is_file()
        guide = path.read_text(encoding="utf-8")
        assert f"]({filename})" in context.router
        assert f"docs/{filename}" in context.standard
        for term in evidence:
            assert term in guide

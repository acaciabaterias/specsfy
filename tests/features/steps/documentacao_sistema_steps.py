from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]


@given("os repositórios integrados do framework Specsfy")
def given_integrated_repositories(context) -> None:
    context.root = ROOT


@when("o contrato do documentador é inspecionado")
def when_documentator_contract_is_inspected(context) -> None:
    context.documentator = (
        ROOT / "skills" / "specsfy-documentator" / "SKILL.md"
    ).read_text(encoding="utf-8")
    context.installer = (
        ROOT / "cli/src/installer.ts"
    ).read_text(encoding="utf-8")
    context.guide = (
        ROOT / "docs/user/system-documentation.md"
    ).read_text(encoding="utf-8")


@then("a instalação inclui a skill de documentação")
def then_installation_includes_documentator(context) -> None:
    assert '"specsfy-documentator"' in context.installer


@then("a skill cobre arquitetura aplicação banco fluxos testes frontend pacotes integrações e decisões")
def then_skill_has_full_coverage(context) -> None:
    for term in (
        "arquitetura",
        "aplicação",
        "banco",
        "fluxos",
        "testes",
        "frontend",
        "pacotes",
        "integrações",
        "decisões",
    ):
        assert term in context.documentator


@then("a documentação oficial explica a projeção reconstruível no consumidor")
def then_official_docs_explain_projection(context) -> None:
    assert "<projeto>/docs/" in context.guide
    assert "reconstrói" in context.guide


@given("o fluxo de implementação e monitoramento do Specsfy")
def given_implementation_and_monitoring(context) -> None:
    context.implementation = (
        ROOT / "skills" / "specsfy-07-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    context.monitor = (
        ROOT / "skills" / "specsfy-setup" / "scripts" / "monitor_context.mjs"
    ).read_text(encoding="utf-8")
    context.builder = (
        ROOT
        / "skills"
        / "specsfy-documentator"
        / "scripts"
        / "build_documentation.mjs"
    ).read_text(encoding="utf-8")


@when("aplicação ou persistência muda")
def when_application_or_persistence_changes(context) -> None:
    pass


@then("a implementação faz handoff obrigatório para o documentador")
def then_implementation_hands_off(context) -> None:
    assert "$specsfy-documentator" in context.implementation
    assert "Depois de cada tarefa `[CODE]`" in context.implementation


@then("o monitor bloqueia entrega sem mudança em docs")
def then_monitor_blocks_without_docs(context) -> None:
    assert "documentation_review_required" in context.monitor
    assert "specsfy-documentator" in context.monitor


@then("o builder oferece verificação de documentação atual")
def then_builder_supports_check(context) -> None:
    assert '"--check"' in context.builder

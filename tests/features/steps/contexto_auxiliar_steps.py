from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "skills"
EXPECTED_SKILLS = {
    "specsfy-setup",
    "specsfy-aux-stack",
    "specsfy-aux-rules",
    "specsfy-aux-database",
}


@given("os repositórios de skills, CLI e documentação do Specsfy")
def given_repositories(context) -> None:
    context.skills = SKILLS
    context.cli = ROOT / "cli"
    context.docs = ROOT / "docs"


@when("o contrato de contexto auxiliar é inspecionado")
def when_contract_is_inspected(context) -> None:
    context.skill_documents = {
        name: (context.skills / name / "SKILL.md").read_text(encoding="utf-8")
        for name in EXPECTED_SKILLS
    }
    context.framework = (context.skills / "Spec.md").read_text(encoding="utf-8")
    context.installer = (
        context.cli / "src/installer.ts"
    ).read_text(encoding="utf-8")


@then("setup e as três skills auxiliares possuem responsabilidades distintas")
def then_skills_have_distinct_responsibilities(context) -> None:
    for name, document in context.skill_documents.items():
        assert f"name: {name}" in document
    assert ".specsfy/STACK.md" in context.skill_documents["specsfy-aux-stack"]
    assert ".specsfy/RULES.md" in context.skill_documents["specsfy-aux-rules"]
    assert ".specsfy/DATABASE.md" in context.skill_documents["specsfy-aux-database"]


@then("o projeto consumidor recebe caminhos canônicos para projeto stack regras e banco")
def then_consumer_receives_canonical_paths(context) -> None:
    for path in (
        "PROJECT.md",
        ".specsfy/STACK.md",
        ".specsfy/RULES.md",
        ".specsfy/DATABASE.md",
    ):
        assert path in context.framework
    guide = (
        context.docs / "user" / "project-context.md"
    ).read_text(encoding="utf-8")
    assert "$specsfy-setup" in guide


@then("as diretrizes publicáveis dos agentes possuem uma referência sincronizada")
def then_agent_reference_is_synchronized(context) -> None:
    start = "<!-- specsfy:framework:start -->"
    end = "<!-- specsfy:framework:end -->"
    agents = (context.skills / "AGENTS.md").read_text(encoding="utf-8")
    published = start + agents.split(start, 1)[1].split(end, 1)[0] + end
    reference = (
        context.skills
        / "specsfy-setup/references/framework-instructions.md"
    ).read_text(encoding="utf-8")
    referenced = start + reference.split(start, 1)[1].split(end, 1)[0] + end
    assert published.strip() == referenced.strip()


@then("a instalação reconhece setup e skills auxiliares como parte do framework")
def then_installer_recognizes_framework_skills(context) -> None:
    for name in EXPECTED_SKILLS:
        assert f'"{name}"' in context.installer


@given("o monitor de contexto publicado pela skill de setup")
def given_context_monitor(context) -> None:
    context.monitor = (
        SKILLS / "specsfy-setup/scripts/monitor_context.py"
    ).read_text(encoding="utf-8")


@when("manifests banco ou código da aplicação mudam")
def when_monitored_paths_change(context) -> None:
    context.workflow_skills = {
        name: (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
        for name in (
            "specsfy-05-tasks",
            "specsfy-07-implement",
            "specsfy-progress",
        )
    }


@then("o fluxo exige os documentos mantenedores correspondentes")
def then_flow_requires_context_documents(context) -> None:
    for path in (
        ".specsfy/STACK.md",
        ".specsfy/DATABASE.md",
        "PROJECT.md",
        ".specsfy/RULES.md",
    ):
        assert path in context.monitor


@then("planejamento implementação e progresso consultam o mesmo monitor")
def then_workflow_uses_same_monitor(context) -> None:
    for name, text in context.workflow_skills.items():
        assert "monitor_context.py" in text, name

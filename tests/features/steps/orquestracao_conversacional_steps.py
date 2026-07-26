from __future__ import annotations

from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
BASE_SKILLS = (
    "specsfy-base-backlog",
    "specsfy-base-interview",
    "specsfy-base-specify",
    "specsfy-base-validate",
    "specsfy-base-tasks",
    "specsfy-base-tdd-bdd",
    "specsfy-base-implement",
    "specsfy-base-progress",
)


@given("o contrato executável e a documentação oficial do Specsfy")
def given_integrated_sources(context) -> None:
    context.framework = (ROOT / "skills" / "Spec.md").read_text(encoding="utf-8")
    context.skills_readme = (ROOT / "skills" / "README.md").read_text(
        encoding="utf-8"
    )
    context.docs = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    context.flow = (
        ROOT / "docs" / "context" / "flows" / "README.md"
    ).read_text(encoding="utf-8")
    context.skills = [
        (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        for name in BASE_SKILLS
    ]


@when("uma etapa conclui ou detecta pendência de outra responsabilidade")
def when_handoff_is_needed(context) -> None:
    assert "Pendência detectada:" in context.framework


@then("todas as skills base anunciam a transição e pedem confirmação")
def then_skills_announce_and_confirm(context) -> None:
    assert len(context.skills) == 8
    for content in context.skills:
        assert "Transição proposta:" in content
        assert "confirmação" in content


@then("o fluxo documenta avanço, retorno e permanência no ponto seguro")
def then_flow_documents_both_directions(context) -> None:
    normalized = " ".join(context.flow.split())
    assert "avanço" in normalized
    assert "retorno" in normalized
    assert "ponto seguro" in normalized


@then("a confirmação continua a etapa escolhida na mesma conversa")
def then_confirmation_continues(context) -> None:
    assert "## Orquestração conversacional" in context.skills_readme
    assert "## Conversa contínua entre etapas" in context.docs
    assert "mesma conversa" in " ".join(context.framework.split())

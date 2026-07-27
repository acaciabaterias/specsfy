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
    "specsfy-base-update-spec",
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


@then("todas as skills base anunciam e executam a transição automaticamente")
def then_skills_announce_and_execute(context) -> None:
    assert len(context.skills) == 9
    for content in context.skills:
        assert "Transição automática:" in content
        assert "carregue imediatamente a skill de destino" in " ".join(
            content.split()
        )


@then("o fluxo documenta avanço, retorno e retomada automáticos")
def then_flow_documents_both_directions(context) -> None:
    normalized = " ".join(context.flow.split())
    assert "avanço" in normalized
    assert "retorno" in normalized
    assert "retomada" in normalized
    assert "automaticamente" in normalized


@then("a etapa escolhida continua na mesma conversa sem confirmação")
def then_automatic_handoff_continues(context) -> None:
    assert "## Orquestração conversacional" in context.skills_readme
    assert "## Conversa contínua entre etapas" in context.docs
    assert "mesma conversa" in " ".join(context.framework.split())
    assert "sem pedir confirmação" in " ".join(context.framework.split())


@then("mudança tardia usa uma entrada pública e executável")
def then_late_change_has_one_entrypoint(context) -> None:
    update = (
        ROOT / "skills" / "specsfy-base-update-spec" / "SKILL.md"
    ).read_text(encoding="utf-8")
    implement = (
        ROOT / "skills" / "specsfy-base-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    entrypoint = (ROOT / "specsfy" / "README.md").read_text(encoding="utf-8")
    for source in (implement, entrypoint):
        assert "$specsfy-base-update-spec" in source
    assert "esqueceu" in update

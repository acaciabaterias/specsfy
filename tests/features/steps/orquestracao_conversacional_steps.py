from __future__ import annotations

from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
BASE_SKILLS = (
    "specsfy-01-inbox",
    "specsfy-02-backlog",
    "specsfy-03-specify",
    "specsfy-04-validate",
    "specsfy-05-tasks",
    "specsfy-06-tdd-bdd",
    "specsfy-07-implement",
    "specsfy-update-spec",
    "specsfy-progress",
)


@given("o contrato executável e a documentação oficial do Specsfy")
def given_integrated_sources(context) -> None:
    context.framework = (ROOT / "skills" / "Spec.md").read_text(encoding="utf-8")
    context.skills_readme = (ROOT / "skills" / "README.md").read_text(
        encoding="utf-8"
    )
    context.docs = (
        ROOT / "docs" / "user" / "README.md"
    ).read_text(encoding="utf-8")
    context.flow = (
        ROOT / "docs" / "develop" / "context" / "flows" / "README.md"
    ).read_text(encoding="utf-8")
    context.skills = [
        (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        for name in BASE_SKILLS[1:]
    ]


@when("uma etapa conclui ou detecta pendência de outra responsabilidade")
def when_handoff_is_needed(context) -> None:
    assert "Pendência detectada:" in context.framework


@then("as skills posteriores à captura anunciam e executam a transição automaticamente")
def then_skills_announce_and_execute(context) -> None:
    assert len(context.skills) == 8
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
        ROOT / "skills" / "specsfy-update-spec" / "SKILL.md"
    ).read_text(encoding="utf-8")
    implement = (
        ROOT / "skills" / "specsfy-07-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    entrypoint = (ROOT / "specsfy" / "README.md").read_text(encoding="utf-8")
    for source in (implement, entrypoint):
        assert "$specsfy-update-spec" in source
    assert "esqueceu" in update


@given("o contrato do refinamento do backlog e do método MCR-10")
def given_backlog_contract(context) -> None:
    context.backlog = (
        ROOT / "skills" / "specsfy-02-backlog" / "SKILL.md"
    ).read_text(encoding="utf-8")
    context.mcr = (
        ROOT
        / "skills"
        / "specsfy-03-specify"
        / "references"
        / "mcr-10.md"
    ).read_text(encoding="utf-8")


@when("a pessoa responde uma pergunta do refinamento do backlog")
def when_person_answers_backlog(context) -> None:
    assert "## Conduzir a descoberta adaptativa" in context.backlog


@then("o refinamento do backlog reavalia o contexto acumulado com a nova resposta")
def then_backlog_reanalyses_context(context) -> None:
    for source in (context.backlog, context.mcr):
        assert "contexto acumulado e a nova resposta" in source


@then("continua sem limite máximo enquanto existir lacuna aplicável")
def then_backlog_has_no_question_limit(context) -> None:
    for source in (context.backlog, context.mcr):
        assert "sem limite máximo de perguntas" in source
        assert "enquanto existir lacuna aplicável" in source


@then("oferece avançar a partir da décima primeira pergunta")
def then_backlog_offers_advance(context) -> None:
    for source in (context.backlog, context.mcr):
        assert "A partir da 11ª pergunta" in source
        assert "`avançar`" in source


@then("o avanço preserva as lacunas e mantém a definição pendente")
def then_advance_preserves_open_gaps(context) -> None:
    assert "lacunas não resolvidas" in context.backlog
    assert "Status: Draft" in context.backlog
    assert "Definition Gate: Pending" in context.backlog

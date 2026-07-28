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


def orchestration_contract() -> str:
    contents = [(ROOT / "Spec.md").read_text(encoding="utf-8")]
    contents.extend(
        (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
        for name in BASE_SKILLS
    )
    return " ".join("\n".join(contents).split())


@given("uma skill base concluiu sua responsabilidade")
@given("uma etapa posterior encontra uma pendência de uma etapa anterior")
@given("uma transição automática exige uma ação sensível")
@given("as nove skills base instaladas")
def given_orchestration_context(context) -> None:
    context.contract = orchestration_contract()


@when("ela identifica a próxima etapa responsável")
@when("ela identifica a skill responsável pela correção")
@when("a skill responsável é carregada")
@when("o estado canônico exige outra responsabilidade")
def when_transition_is_evaluated(context) -> None:
    assert context.contract


@then("anuncia a transição, o motivo e a pendência ou resultado esperado")
def then_announces_transition(context) -> None:
    assert "Transição automática:" in context.contract
    assert "motivo" in context.contract
    assert "Pendência detectada:" in context.contract


@then("carrega automaticamente a skill de destino sem pedir confirmação")
def then_loads_destination_automatically(context) -> None:
    assert "sem pedir confirmação" in context.contract
    assert "carregue imediatamente a skill de destino" in context.contract


@then("continua na mesma conversa sem pedir o comando novamente")
def then_continues_in_same_conversation(context) -> None:
    assert "mesma conversa" in context.contract
    assert "não peça que a pessoa repita o comando" in context.contract


@then("anuncia a pendência e executa o retorno")
def then_announces_return(context) -> None:
    assert "Pendência detectada:" in context.contract
    assert "retorno" in context.contract


@then("após a correção retoma automaticamente a etapa que detectou a pendência")
def then_resumes_automatically(context) -> None:
    assert "Retomada automática:" in context.contract


@then("a cadeia principal chama backlog, interview, specify, validate, tasks, tdd-bdd, implement e progress")
def then_routes_main_chain(context) -> None:
    expected_handoffs = (
        "$specsfy-base-interview",
        "$specsfy-base-specify",
        "$specsfy-base-validate",
        "$specsfy-base-tasks",
        "$specsfy-base-tdd-bdd",
        "$specsfy-base-implement",
        "$specsfy-base-progress",
    )
    for destination in expected_handoffs:
        assert destination in context.contract


@then("mudança tardia chama update-spec automaticamente")
def then_late_change_routes_to_update_spec(context) -> None:
    implement = (ROOT / "specsfy-base-implement" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(implement.split())
    assert "carregue automaticamente `$specsfy-base-update-spec`" in normalized


@then("ausência de especificação chama specify automaticamente")
def then_missing_spec_routes_to_specify(context) -> None:
    progress = (ROOT / "specsfy-base-progress" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(progress.split())
    assert "carregue automaticamente `$specsfy-base-update-spec`" in normalized


@then("o handoff não pede confirmação")
def then_handoff_does_not_request_confirmation(context) -> None:
    assert "não peça confirmação para o handoff" in context.contract


@then("a ação sensível continua exigindo autorização específica")
def then_sensitive_action_requires_authorization(context) -> None:
    assert "autorização específica" in context.contract

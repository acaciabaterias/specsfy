from pathlib import Path

from behave import given, then, when

from tests.test_numbered_questions import (
    NON_QUESTIONING_SKILLS,
    QUESTIONING_SKILLS,
)


ROOT = Path(__file__).resolve().parents[3]


@given("o contrato central de interação do Specsfy")
def given_central_interaction_contract(context) -> None:
    context.contract = (ROOT / "Spec.md").read_text(encoding="utf-8")


@when("uma skill precisa perguntar algo à pessoa")
def when_skill_needs_to_ask(context) -> None:
    context.round_contract = context.contract


@then("a rodada contém exatamente uma pergunta numerada")
def then_round_has_one_numbered_question(context) -> None:
    assert "exatamente uma pergunta numerada por rodada" in context.round_contract
    assert "Pergunta 1" in context.round_contract


@then("a pergunta oferece pelo menos três opções numeradas")
def then_question_has_three_numbered_options(context) -> None:
    assert "pelo menos três opções numeradas" in context.round_contract


@then("a pergunta oferece escrever outra resposta, gerar outras opções ou avançar")
def then_question_has_free_and_advance_options(context) -> None:
    assert "`Escrever outra resposta`" in context.round_contract
    assert "`Gere outras opções`" in context.round_contract
    assert "`Avançar`" in context.round_contract
    assert "desde a primeira rodada" in context.round_contract


@when("uma área chegar a oito perguntas")
def when_area_reaches_the_question_limit(context) -> None:
    context.limit_contract = context.contract


@then("o agente apresenta uma síntese e para a conversa daquela área")
def then_agent_stops_the_area(context) -> None:
    assert "apresente uma síntese" in context.limit_contract
    assert "pare o ciclo" in context.limit_contract


@then("só continua se a pessoa pedir mais perguntas e informar quantas quer responder")
def then_agent_requires_a_new_finite_limit(context) -> None:
    assert "pedir explicitamente" in context.limit_contract
    assert "quantas perguntas quer responder" in context.limit_contract


@when("a pessoa escolhe avançar em uma área")
def when_person_advances_an_area(context) -> None:
    context.advance_contract = context.contract


@then("a rodada seguinte oferece encerrar a área, responder depois ou retomar agora")
def then_next_round_confirms_area_destination(context) -> None:
    assert "encerrar definitivamente" in context.advance_contract
    assert "responder depois" in context.advance_contract
    assert "voltar a responder agora" in context.advance_contract


@then("a escolha de encerrar ou adiar fica registrada")
def then_area_choice_is_recorded(context) -> None:
    assert "Área encerrada pelo usuário" in context.advance_contract
    assert "Área adiada pelo usuário" in context.advance_contract


@then("uma área encerrada não volta ao roteiro sem reabertura explícita")
def then_closed_area_stays_closed(context) -> None:
    contract = " ".join(context.advance_contract.split())
    assert "não volte ao assunto" in contract
    assert "reabrir explicitamente" in contract


@given("todas as skills base e auxiliares do Specsfy")
def given_all_specsfy_skills(context) -> None:
    context.skills = {
        path.parent.name: path.read_text(encoding="utf-8")
        for path in ROOT.glob("*/SKILL.md")
    }


@when("seus contratos de interação são inspecionados")
def when_interaction_contracts_are_inspected(context) -> None:
    assert set(context.skills) == QUESTIONING_SKILLS | NON_QUESTIONING_SKILLS


@then("toda skill que pode perguntar aponta para o contrato numerado")
def then_questioning_skills_use_contract(context) -> None:
    for name in QUESTIONING_SKILLS:
        source = context.skills[name]
        assert "Modo de interação: `perguntas`." in source, name
        assert "Contrato de perguntas numeradas" in source, name


@then("toda skill restante declara que não faz perguntas")
def then_other_skills_forbid_questions(context) -> None:
    for name in NON_QUESTIONING_SKILLS:
        source = context.skills[name]
        assert "Modo de interação: `sem perguntas`." in source, name

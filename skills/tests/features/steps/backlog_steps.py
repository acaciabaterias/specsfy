from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "specsfy-02-backlog/scripts/iniciar_backlog.mjs"
SKILL = ROOT / "specsfy-02-backlog/SKILL.md"


@given("um projeto consumidor vazio para backlog")
def given_empty_project(context) -> None:
    context.project = Path(tempfile.mkdtemp(prefix="backlog-project-"))
    context.add_cleanup(shutil.rmtree, context.project, ignore_errors=True)


@when('o agente registra a ideia "{title}"')
def when_capture_backlog_entry(context, title: str) -> None:
    context.result = subprocess.run(
        [
            "node",
            str(SCRIPT),
            "--title",
            title,
            "--idea",
            f"Quero registrar a ideia: {title}.",
            "--problem",
            "A equipe não possui uma visão consolidada do andamento.",
            "--person",
            "Pessoas responsáveis pelo produto.",
            "--result",
            "Acompanhar o andamento das entregas.",
            "--context",
            "Durante a revisão semanal do produto.",
            "--root",
            str(context.project),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


@then("o arquivo specs/backlog/0001-painel-de-acompanhamento.md é criado")
def then_backlog_created(context) -> None:
    expected = context.project / "specs/backlog/0001-painel-de-acompanhamento.md"
    assert context.result.returncode == 0, context.result.stderr
    assert expected.is_file()
    context.backlog = expected.read_text(encoding="utf-8")


@then("suas metainformações aparecem em uma tabela no topo")
def then_metadata_table_at_top(context) -> None:
    lines = context.backlog.splitlines()
    assert lines[2] == "| Metainformação | Valor |"
    assert lines[3] == "| --- | --- |"
    assert "| ID | BACKLOG-0001 |" in context.backlog
    assert "**ID**:" not in context.backlog


@then("nenhuma especificação convertida é criada")
def then_no_spec_created(context) -> None:
    assert not (context.project / "specs/specs").exists()


@given("uma ideia de backlog com informações essenciais ausentes ou ambíguas")
def given_incomplete_or_ambiguous_idea(context) -> None:
    context.skill = SKILL.read_text(encoding="utf-8")


@when("o agente avalia se a ideia está minimamente completa")
def when_agent_checks_minimum(context) -> None:
    context.minimum_section = context.skill.partition(
        "## Garantir a captura mínima"
    )[2].partition("\n## ")[0]


@then("ele pergunta uma lacuna relevante por vez")
def then_asks_one_gap_at_a_time(context) -> None:
    assert "uma pergunta por vez" in context.minimum_section


@then("reavalia o que falta depois de cada resposta")
def then_rechecks_after_each_answer(context) -> None:
    assert "Reavalie as lacunas depois de cada resposta" in context.minimum_section


@then(
    "só persiste o backlog quando problema, pessoa, resultado e contexto estão claros"
)
def then_only_persists_complete_minimum(context) -> None:
    expected = (
        "problema percebido",
        "pessoa afetada ou beneficiada",
        "resultado ou valor esperado",
        "contexto suficiente para distinguir a entrada",
        "Não crie nem atualize o arquivo enquanto algum item essencial",
    )
    for phrase in expected:
        assert phrase in context.minimum_section


@given("um pedido para registrar uma ideia de backlog")
def given_request_to_capture_backlog(context) -> None:
    context.skill = SKILL.read_text(encoding="utf-8")


@when("o agente procura material relacionado")
def when_agent_searches_related_material(context) -> None:
    context.search_section = context.skill.partition(
        "## Buscar duplicatas e referências"
    )[2].partition("\n## ")[0]


@then("ele pesquisa termos do pedido em backlogs, specs e documentação")
def then_searches_project_sources(context) -> None:
    expected = (
        "termos derivados do pedido do usuário",
        "`specs/backlog/*.md`",
        "`specs/<estado>/*/spec.md`",
        "`docs/**/*.md`",
    )
    for phrase in expected:
        assert phrase in context.search_section


@then("confirma com o usuário antes de criar uma possível duplicata")
def then_confirms_possible_duplicate(context) -> None:
    assert "possível duplicata" in context.search_section
    assert "confirme com o usuário" in context.search_section


@then("preserva referências relevantes no item")
def then_preserves_references(context) -> None:
    assert "Referências relacionadas" in context.search_section

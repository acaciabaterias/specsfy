import json
import subprocess
import tempfile
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
TUI = ROOT / "cli/src/tui.ts"


CANONICAL_SPEC = """# Especificação integrada: Entrega concluída

| Campo | Valor |
| --- | --- |
| Formato | Specsfy/2.0 |
| Status | Complete |
| Definition Gate | Passed |
| Plan Gate | Passed |
| Delivery Gate | Passed |
"""


@given("uma spec concluída com o cabeçalho tabular canônico")
def given_completed_spec_with_canonical_table(context) -> None:
    context.temporary_directory = tempfile.TemporaryDirectory()
    context.add_cleanup(context.temporary_directory.cleanup)
    context.project = Path(context.temporary_directory.name)
    path = context.project / "specs/specs/0001-entrega/spec.md"
    path.parent.mkdir(parents=True)
    path.write_text(CANONICAL_SPEC, encoding="utf-8")


@when("o CLI projeta o progresso da especificação")
def when_cli_projects_spec_progress(context) -> None:
    result = subprocess.run(
        [
            str(ROOT / "cli/bin/specsfy"),
            "progress",
            "--project",
            str(context.project),
            "--json",
        ],
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    context.specs = payload["specs"]
    context.summary = payload["summary"]


@then("o status e os três gates são reconhecidos")
def then_status_and_gates_are_recognized(context) -> None:
    spec = context.specs[0]
    assert spec["status"] == "Complete"
    assert spec["definition_gate"] == "Passed"
    assert spec["plan_gate"] == "Passed"
    assert spec["delivery_gate"] == "Passed"
    assert spec["passed_gates"] == 3


@then("o resumo contabiliza a spec como concluída")
def then_summary_counts_completed_spec(context) -> None:
    assert context.summary["completed_specs"] == 1


@given("a implementação da aba Specs do CLI")
def given_cli_specs_implementation(context) -> None:
    context.tui = TUI.read_text(encoding="utf-8")


@when("o contrato de visualização da spec é inspecionado")
def when_spec_view_contract_is_inspected(context) -> None:
    context.specs_markup = context.tui.partition(
        "private renderSpecs("
    )[2].partition("private openSpec(")[0]


@then("a tabela preserva gates, tarefas, checklist e progresso")
def then_specs_table_preserves_progress(context) -> None:
    assert "blessed.list(" in context.specs_markup
    normalized = context.specs_markup.upper()
    for column in (
        "SPEC",
        "STATUS",
        "GATES",
        "TAREFAS",
        "CHECKLIST",
        "PROGRESSO",
    ):
        assert column in normalized


@then("a barra de espaço abre a spec destacada em um modal Markdown")
def then_space_opens_spec_markdown_modal(context) -> None:
    assert 'list.key(["space"], open)' in context.tui
    assert "private openSpec(" in context.tui
    assert "renderMarkdown(spec.content)" in context.tui
    assert "this.openSpec(spec)" in context.tui


@then("o modal informa como voltar para a listagem")
def then_modal_explains_how_to_return(context) -> None:
    assert "Esc: voltar para a lista de specs" in context.tui

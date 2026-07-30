from __future__ import annotations

from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
TESTING = ROOT / "cli/src/project-testing.ts"
APP = ROOT / "cli/src/cli.ts"
TUI = ROOT / "cli/src/tui.ts"


@given("a implementação do runner de testes do CLI")
def given_cli_test_runner(context) -> None:
    context.testing = TESTING.read_text(encoding="utf-8")
    context.app = APP.read_text(encoding="utf-8")
    context.tui = TUI.read_text(encoding="utf-8")


@when("o contrato de execução de testes é inspecionado")
def when_test_execution_contract_is_inspected(context) -> None:
    context.tests_markup = context.tui.partition(
        "private renderTests("
    )[2].partition("private async runTests(")[0]


@then("o CLI detecta Laravel com Pest sem executar comandos arbitrários")
def then_cli_detects_laravel_pest_safely(context) -> None:
    assert '["php", "artisan", "test"]' in context.testing
    assert "spawn(" in context.testing
    assert "shell:" not in context.testing


@then("o comando specsfy test transmite a saída e preserva o exit code")
def then_cli_test_streams_and_preserves_exit_code(context) -> None:
    assert '.command("test")' in context.app
    assert "runProjectTests(options.project)" in context.app
    assert "process.exitCode = result.exit_code" in context.app


@then("a TUI separa o resumo e os testes em subabas")
def then_tui_separates_summary_and_tests(context) -> None:
    assert 'label: " Resumo "' in context.tests_markup
    assert 'label: " Testes "' in context.tests_markup
    assert "this.#testSummary" in context.tests_markup


@then("a saída detalhada permanece rolável e a execução é explícita")
def then_tui_has_detailed_live_log(context) -> None:
    assert "blessed.log(" not in context.tests_markup
    assert 'content: this.#testOutput.join("\\n")' in context.tests_markup
    assert "scrollable: true" in context.tests_markup
    assert '" Executar testes ^X "' in context.tests_markup
    assert "runProjectTests(" in context.tui

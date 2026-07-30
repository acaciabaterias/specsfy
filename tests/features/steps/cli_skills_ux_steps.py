from __future__ import annotations

from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
TUI = ROOT / "cli/src/tui.ts"
APP = ROOT / "cli/src/cli.ts"
INSTALLER = ROOT / "cli/src/installer.ts"


@given("a implementação da aba Skills do CLI")
def given_cli_skills_implementation(context) -> None:
    context.tui = TUI.read_text(encoding="utf-8")
    context.app = APP.read_text(encoding="utf-8")
    context.installer = INSTALLER.read_text(encoding="utf-8")


@when("o contrato de apresentação é inspecionado")
def when_presentation_contract_is_inspected(context) -> None:
    context.skills_markup = context.tui.partition(
        "private renderSkills("
    )[2].partition("private renderAbout(")[0]


@then("as skills aparecem em uma tabela com plano, nome, categoria e estado")
def then_skills_appear_in_table(context) -> None:
    assert "blessed.list(" in context.skills_markup
    for column in ("Plano", "Skill", "Categoria", "Estado"):
        assert column.upper() in context.skills_markup


@then("a skill destacada possui um painel de detalhes e uma ação explícita")
def then_highlighted_skill_has_details(context) -> None:
    assert 'label: " Detalhes "' in context.skills_markup
    assert "toggleSelectedSkill" in context.skills_markup


@then("a decisão pode ser alternada por teclado ou mouse sem aplicação imediata")
def then_decision_can_be_toggled(context) -> None:
    assert 'list.key(["space"], toggle)' in context.tui
    assert 'screen.key(["C-e"]' in context.tui
    assert "toggleSelectedSkill" in context.tui
    assert "applySkills" in context.tui


@then("a aba oferece uma ação para atualizar todas as skills instaladas")
def then_tab_updates_all_installed_skills(context) -> None:
    assert "Atualizar  ^R" in context.skills_markup
    assert 'screen.key(["C-r"]' in context.tui
    assert ".updateAll()" in context.tui


@then("o CLI oferece a atualização não interativa equivalente")
def then_cli_has_equivalent_update(context) -> None:
    assert '.command("update")' in context.app
    assert "installer.updateAll()" in context.app
    assert "async updateAll()" in context.installer

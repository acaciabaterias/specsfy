from __future__ import annotations

from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
TUI = ROOT / "cli/src/specsfy_cli/tui.py"
APP = ROOT / "cli/src/specsfy_cli/app.py"
INSTALLER = ROOT / "cli/src/specsfy_cli/installer.py"


@given("a implementação da aba Skills do CLI")
def given_cli_skills_implementation(context) -> None:
    context.tui = TUI.read_text(encoding="utf-8")
    context.app = APP.read_text(encoding="utf-8")
    context.installer = INSTALLER.read_text(encoding="utf-8")


@when("o contrato de apresentação é inspecionado")
def when_presentation_contract_is_inspected(context) -> None:
    context.skills_markup = context.tui.partition(
        'with TabPane("Skills", id="tab-skills"):'
    )[2].partition('with TabPane("Sobre", id="tab-about"):')[0]


@then("as skills aparecem em uma tabela com plano, nome, categoria e estado")
def then_skills_appear_in_table(context) -> None:
    assert 'DataTable(id="skills-table")' in context.skills_markup
    assert 'SelectionList(id="skills-list")' not in context.skills_markup
    for column in ("Plano", "Skill", "Categoria", "Estado"):
        assert f'"{column}"' in context.tui


@then("a skill destacada possui um painel de detalhes e uma ação explícita")
def then_highlighted_skill_has_details(context) -> None:
    assert 'id="skill-detail"' in context.skills_markup
    assert 'id="toggle-skill"' in context.skills_markup


@then("a decisão pode ser alternada por teclado ou mouse sem aplicação imediata")
def then_decision_can_be_toggled(context) -> None:
    assert '"space", "toggle_skill"' in context.tui
    assert '"ctrl+e", "toggle_skill"' in context.tui
    assert "action_toggle_skill" in context.tui
    assert "action_apply_skills" in context.tui


@then("a aba oferece uma ação para atualizar todas as skills instaladas")
def then_tab_updates_all_installed_skills(context) -> None:
    assert 'Button("Atualizar  ^R", id="update-skills")' in context.skills_markup
    assert '"ctrl+r",\n            "update_skills"' in context.tui
    assert "SkillInstaller(self._selected_project()).update_all()" in context.tui


@then("o CLI oferece a atualização não interativa equivalente")
def then_cli_has_equivalent_update(context) -> None:
    assert '"update",' in context.app
    assert "SkillInstaller(args.project, force=args.force).update_all()" in context.app
    assert "def update_all(self)" in context.installer

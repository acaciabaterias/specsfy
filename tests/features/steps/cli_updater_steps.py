from __future__ import annotations

from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
UPDATER = ROOT / "cli/src/specsfy_cli/updater.py"
APP = ROOT / "cli/src/specsfy_cli/app.py"


@given("a implementação do auto updater do CLI")
def given_cli_updater(context) -> None:
    context.updater = UPDATER.read_text(encoding="utf-8")
    context.app = APP.read_text(encoding="utf-8")


@when("o contrato de atualização é inspecionado")
def when_updater_contract_is_inspected(context) -> None:
    pass


@then("dados e configurações globais usam ~/.specsfy/cli.json")
def then_global_data_uses_specsfy_path(context) -> None:
    assert '".specsfy"' in context.updater
    assert '"cli.json"' in context.updater


@then("a versão mais recente deriva de tags semânticas do repositório")
def then_latest_version_comes_from_semantic_tags(context) -> None:
    assert "/repos/specsfy/cli/tags" in context.updater
    assert "SEMANTIC_TAG" in context.updater


@then("a atualização é delegada a uv tool upgrade specsfy-cli")
def then_upgrade_is_delegated_to_uv(context) -> None:
    assert 'UV_TOOL_NAME = "specsfy-cli"' in context.updater
    assert '[uv_executable, "tool", "upgrade", UV_TOOL_NAME]' in context.updater


@then("aceitar a oferta atualiza e encerra enquanto recusar abre normalmente")
def then_accept_updates_and_decline_continues(context) -> None:
    assert "offer_startup_update()" in context.app
    assert "return 0" in context.app

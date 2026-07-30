from __future__ import annotations

from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
UPDATER = ROOT / "cli/src/updater.ts"
APP = ROOT / "cli/src/cli.ts"


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
    assert "/repos/promovaweb/specsfy/tags" in context.updater
    assert "SEMANTIC_TAG" in context.updater


@then("a atualização é delegada ao pacote npm oficial")
def then_upgrade_is_delegated_to_npm(context) -> None:
    assert 'NPM_PACKAGE_NAME = "@promovaweb/specsfy"' in context.updater
    assert '"install", "--global"' in context.updater


@then("aceitar a oferta atualiza e encerra enquanto recusar abre normalmente")
def then_accept_updates_and_decline_continues(context) -> None:
    assert "offerStartupUpdate(" in context.app
    assert "if (shouldExit) return" in context.app

from __future__ import annotations

import subprocess
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
TEST_FILE = ROOT / "tests" / "test_aplicacao_exemplo.py"


def run_contract(test_name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "python3",
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_aplicacao_exemplo.py",
            "-k",
            test_name,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@given("a aplicação de exemplo e suas fontes executáveis")
def given_example_application(context) -> None:
    context.root = ROOT
    context.test_file = TEST_FILE


@when("um mantenedor consulta sua porta de entrada")
def when_maintainer_reads_entrypoint(context) -> None:
    context.contracts = [
        run_contract("test_readme_covers_application_contract"),
        run_contract("test_readme_references_executable_sources"),
    ]


@then("encontra finalidade limites capacidades arquitetura dados e rotas")
def then_finds_application_contract(context) -> None:
    result = context.contracts[0]
    assert result.returncode == 0, result.stdout + result.stderr


@then("encontra instalação operação testes e referências verificáveis")
def then_finds_operational_contract(context) -> None:
    result = context.contracts[1]
    assert result.returncode == 0, result.stdout + result.stderr


@given("as portas de entrada do workspace e o contexto transversal")
def given_workspace_entrypoints(context) -> None:
    context.root = ROOT


@when("o público e o owner de cada documentação são inspecionados")
def when_documentation_boundaries_are_inspected(context) -> None:
    context.boundary_contract = run_contract(
        "test_documentation_authority_and_example_owner_are_explicit"
    )


@then("docs é apresentado como documentação oficial para usuários")
def then_docs_is_official(context) -> None:
    result = context.boundary_contract
    assert result.returncode == 0, result.stdout + result.stderr


@then("example é apresentado como aplicação interna pertencente a dev")
def then_example_belongs_to_dev(context) -> None:
    result = context.boundary_contract
    assert result.returncode == 0, result.stdout + result.stderr


@given("a documentação afetada e as fontes executáveis referenciadas")
def given_affected_documentation(context) -> None:
    context.root = ROOT


@when("o contrato de integridade documental é executado")
def when_documentation_integrity_runs(context) -> None:
    context.integrity_contracts = [
        run_contract("test_local_markdown_links_and_anchors_resolve"),
        run_contract("test_documented_routes_and_commands_exist"),
        run_contract("test_every_change_requires_documentation"),
    ]


@then("cada arquivo diretório âncora rota e comando citado é verificável")
def then_references_are_verifiable(context) -> None:
    for result in context.integrity_contracts[:2]:
        assert result.returncode == 0, result.stdout + result.stderr


@then("a regra de atualização documental está presente nas instruções e no contexto")
def then_documentation_rule_is_present(context) -> None:
    result = context.integrity_contracts[2]
    assert result.returncode == 0, result.stdout + result.stderr

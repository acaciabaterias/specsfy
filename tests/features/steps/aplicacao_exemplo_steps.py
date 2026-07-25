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


@then("example é apresentado como aplicação interna com owner próprio")
def then_example_has_its_own_owner(context) -> None:
    result = context.boundary_contract
    assert result.returncode == 0, result.stdout + result.stderr

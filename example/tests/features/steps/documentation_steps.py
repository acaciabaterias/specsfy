from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]


@given("a documentação operacional da aplicação")
def given_application_documentation(context) -> None:
    context.readme = ROOT / "README.md"
    assert context.readme.is_file()


@when("o contrato documental local é executado")
def when_local_documentation_contract_runs(context) -> None:
    context.result = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_documentation.py",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@then("capacidades fontes rotas e comandos são verificáveis")
def then_documentation_is_verifiable(context) -> None:
    assert context.result.returncode == 0, (
        context.result.stdout + context.result.stderr
    )

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]


@given("um projeto com nove skills base e dois especialistas válidos")
def given_base_and_specialist_catalog(context) -> None:
    context.test = ROOT / "tests/test_verify_repo.mjs"
    assert context.test.is_file()


@when("o contrato do catálogo instalado é executado")
def when_catalog_contract_runs(context) -> None:
    context.result = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "tests.test_verify_repo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@then("o catálogo completo é aceito sem enfraquecer as skills base")
def then_catalog_is_accepted(context) -> None:
    assert context.result.returncode == 0, (
        context.result.stdout + context.result.stderr
    )

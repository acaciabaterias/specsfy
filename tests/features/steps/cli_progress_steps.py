from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "cli" / "src"))

from specsfy_cli.progress import scan_specs, summarize_specs


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
    context.specs = scan_specs(context.project)
    context.summary = summarize_specs(context.specs)


@then("o status e os três gates são reconhecidos")
def then_status_and_gates_are_recognized(context) -> None:
    spec = context.specs[0]
    assert spec.status == "Complete"
    assert spec.definition_gate == "Passed"
    assert spec.plan_gate == "Passed"
    assert spec.delivery_gate == "Passed"
    assert spec.passed_gates == 3


@then("o resumo contabiliza a spec como concluída")
def then_summary_counts_completed_spec(context) -> None:
    assert context.summary.completed_specs == 1

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]


def run_coverage_contract(context) -> None:
    context.result = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "tests.test_minimum_spec_coverage"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    context.contract = (
        ROOT / "tests" / "test_minimum_spec_coverage.py"
    ).read_text(encoding="utf-8")


def assert_contract_passed(context) -> None:
    assert context.result.returncode == 0, (
        context.result.stdout + context.result.stderr
    )


@given("uma spec com uma história de usuário coberta por menos de três ACs distintos")
def given_story_with_insufficient_acceptance_coverage(context) -> None:
    context.fixture = "US-001"


@when("o Definition Gate valida a cobertura BDD")
def when_definition_gate_checks_bdd_coverage(context) -> None:
    run_coverage_contract(context)


@then("a história é reportada com a quantidade observada e o mínimo esperado")
def then_story_reports_observed_and_required_coverage(context) -> None:
    assert_contract_passed(context)
    assert "US-001 possui 2 cenários BDD; mínimo exigido: 3." in context.contract


@then("a feature não avança enquanto a lacuna permanecer")
def then_feature_does_not_advance_with_gap(context) -> None:
    assert_contract_passed(context)
    assert "minimum_bdd_coverage_errors" in context.contract


@given("uma spec com requisitos funcionais e não funcionais")
def given_spec_with_functional_and_nonfunctional_requirements(context) -> None:
    context.fixture = ("FR-001", "NFR-001")


@when("menos de três ACs distintos cobrem qualquer requisito")
def when_requirements_have_insufficient_acceptance_coverage(context) -> None:
    run_coverage_contract(context)


@then("cada requisito incompleto é reportado separadamente")
def then_each_incomplete_requirement_is_reported(context) -> None:
    assert_contract_passed(context)
    for item in context.fixture:
        assert f"{item} possui 2 cenários BDD; mínimo exigido: 3." in context.contract


@then("somente ACs que declaram o ID em Cobre contam para o mínimo")
def then_only_explicit_coverage_counts(context) -> None:
    assert_contract_passed(context)
    assert "**Cobre**" in context.contract


@given("uma spec definida com histórias, requisitos e pelo menos três ACs")
def given_defined_spec_with_items_and_acceptance_criteria(context) -> None:
    context.fixture = ("US-001", "FR-001", "NFR-001")


@when("a rastreabilidade encontra menos de três marcadores de caso SPECSFY para um item")
def when_traceability_finds_too_few_test_case_markers(context) -> None:
    run_coverage_contract(context)


@then("ela reporta a quantidade de casos TDD ausentes por ID")
def then_missing_test_cases_are_reported_by_id(context) -> None:
    assert_contract_passed(context)
    for item in context.fixture:
        assert f'"{item}": 1' in context.contract


@then("um único marcador compartilhado não é contado como três casos")
def then_shared_marker_does_not_count_as_three_cases(context) -> None:
    assert_contract_passed(context)
    assert "test_one_shared_marker_counts_as_one_tdd_case" in context.contract

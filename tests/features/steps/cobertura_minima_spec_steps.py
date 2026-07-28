from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]


@given("os contratos de cobertura de skills e documentação")
def given_coverage_contracts(context) -> None:
    context.skills = ROOT / "skills"
    context.docs = ROOT / "docs"


@when("a política mínima da spec é inspecionada")
def when_minimum_policy_is_inspected(context) -> None:
    context.validator = (
        context.skills / "specsfy-base-validate/scripts/validate_spec.py"
    ).read_text(encoding="utf-8")
    context.traceability = (
        context.skills
        / "specsfy-base-tdd-bdd/scripts/check_traceability.py"
    ).read_text(encoding="utf-8")
    context.framework = (context.skills / "Spec.md").read_text(encoding="utf-8")
    context.template = (
        context.skills / "templates/Spec.md"
    ).read_text(encoding="utf-8")
    context.testing = (
        context.docs / "develop/context/engineering/testing.md"
    ).read_text(encoding="utf-8")


@then("o Definition Gate exige três ACs distintos por feature US FR e NFR")
def then_definition_requires_three_scenarios(context) -> None:
    assert "MINIMUM_CONTEXT_SCENARIOS = 3" in context.validator
    assert 'for kind in ("US", "FR", "NFR")' in context.validator
    assert "**Cobre**" in context.framework


@then("a rastreabilidade exige três marcadores de caso por feature US FR e NFR")
def then_traceability_requires_three_cases(context) -> None:
    assert "DEFAULT_MINIMUM_TESTS = 3" in context.traceability
    assert 'default="US,FR,NFR,AC"' in context.traceability
    assert "feature_cases_missing" in context.traceability


@then("cada AC continua exigindo ao menos um caso TDD")
def then_each_acceptance_requires_a_case(context) -> None:
    assert '1 if item.startswith("AC-")' in context.traceability


@then("template contrato central e guia oficial explicam o mínimo de três")
def then_published_surfaces_explain_three(context) -> None:
    for source in (context.template, context.framework, context.testing):
        assert "três" in source.lower() or "3" in source
    for acceptance_id in ("AC-001", "AC-002", "AC-003"):
        assert acceptance_id in context.template

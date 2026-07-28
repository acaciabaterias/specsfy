from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / ".agents" / "skills" / "specsfy-release-cli"


@given("a skill local de release do CLI")
def given_local_cli_release_skill(context) -> None:
    context.release_skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    context.release_script = SKILL / "scripts" / "release_changelog.py"


@when("uma versão semântica estável e suas notas são preparadas")
def when_stable_release_is_prepared(context) -> None:
    context.release_unit_contract = (
        ROOT / "tests" / "test_cli_release_skill.py"
    ).read_text(encoding="utf-8")


@then("a versão é atualizada nas fontes do pacote")
def then_package_versions_are_updated(context) -> None:
    assert "pyproject.toml" in context.release_skill
    assert "src/specsfy_cli/__init__.py" in context.release_skill
    assert "replace_once" in context.release_script.read_text(encoding="utf-8")


@then("o changelog promove as notas para a versão datada")
def then_changelog_promotes_notes(context) -> None:
    assert "## [X.Y.Z] - YYYY-MM-DD" in context.release_skill
    assert "test_prepare_updates_versions" in context.release_unit_contract


@then("as notas extraídas para o GitHub Release são idênticas ao changelog")
def then_release_notes_match_changelog(context) -> None:
    assert "release_changelog.py extract" in context.release_skill
    assert "assertEqual" in context.release_unit_contract


@when("o fluxo de publicação é inspecionado")
def when_release_flow_is_inspected(context) -> None:
    context.release_flow = (
        ROOT / "docs" / "develop" / "context" / "flows" / "cli-release.md"
    ).read_text(encoding="utf-8")


@then("ele valida o monorepo a main sincronizada e a worktree limpa")
def then_validates_hub_branch_and_worktree(context) -> None:
    for evidence in (
        "git remote get-url origin",
        "git status --porcelain",
        "git rev-parse origin/main",
    ):
        assert evidence in context.release_skill


@then("ele executa testes e reconstrói o executável antes do commit")
def then_tests_and_build_precede_commit(context) -> None:
    build = context.release_skill.index("./scripts/build-executable.sh")
    tests = context.release_skill.index("python -B -m unittest discover")
    commit = context.release_skill.index('git commit -m')
    assert build < commit
    assert tests < commit


@then("ele cria e envia a tag semântica no commit de release")
def then_creates_and_pushes_release_tag(context) -> None:
    assert "git tag -a vX.Y.Z" in context.release_skill
    assert "git push --atomic origin main vX.Y.Z" in context.release_skill


@then("ele publica o GitHub Release com a seção exata do changelog")
def then_publishes_exact_changelog_section(context) -> None:
    assert "gh release create vX.Y.Z" in context.release_skill
    assert "--notes-file /caminho/release-notes.md" in context.release_skill
    assert "mesma seção do changelog" in context.release_flow


@then("ele permite retomar uma publicação parcial sem duplicar a versão")
def then_partial_release_is_resumable(context) -> None:
    assert "não recriar commit, tag ou versão" in context.release_skill
    assert "não cria outra" in context.release_flow

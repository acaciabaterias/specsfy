from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
CLI_SOURCE = ROOT.parent / "cli" / "src"
if str(CLI_SOURCE) not in sys.path:
    sys.path.insert(0, str(CLI_SOURCE))

from specsfy_cli.installer import FRAMEWORK_TEMPLATE_NAMES, SkillInstaller


def temporary_project(context) -> Path:
    temporary = tempfile.TemporaryDirectory()
    context.add_cleanup(temporary.cleanup)
    return Path(temporary.name)


@given("um projeto consumidor inicializado para ideias")
def given_consumer_initialized_for_ideas(context) -> None:
    context.project = temporary_project(context)
    templates = context.project / ".specsfy" / "templates"
    templates.mkdir(parents=True)
    (templates / "Idea.md").write_text(
        (ROOT / "templates" / "Idea.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    context.skill = (
        ROOT / "specsfy-base-idea" / "SKILL.md"
    ).read_text(encoding="utf-8")


@when("o agente recebe somente o texto da ideia")
def when_agent_receives_idea_text(context) -> None:
    context.original = (
        "Quero avisar clientes quando uma entrega atrasar, talvez por e-mail."
    )
    context.result = subprocess.run(
        [
            sys.executable,
            "-B",
            str(ROOT / "specsfy-base-idea" / "scripts" / "capturar_ideia.py"),
            "--input",
            context.original,
            "--title",
            "Avisar clientes sobre atrasos",
            "--summary",
            "Notificar clientes afetados por atrasos.",
            "--problem",
            "Clientes ficam sem contexto quando a entrega atrasa.",
            "--people",
            "Clientes com entrega em andamento.",
            "--value",
            "Reduzir incerteza durante atrasos.",
            "--signals",
            "Canal sugerido: e-mail.",
            "--review",
            "Definir gatilho e conteúdo.",
            "--root",
            str(context.project),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert context.result.returncode == 0, context.result.stderr
    context.created = Path(context.result.stdout.strip())


@then("ele não faz perguntas nem solicita confirmação")
def then_does_not_ask_questions(context) -> None:
    normalized = " ".join(context.skill.casefold().split())
    assert "não faça perguntas" in normalized
    assert "não peça confirmação" in normalized


@then("cria specs/ideias/data-hora-slug.md a partir do template instalado")
def then_creates_timestamped_idea(context) -> None:
    assert context.created.parent == context.project / "specs" / "ideias"
    assert context.created.name.endswith("-avisar-clientes-sobre-atrasos.md")
    assert context.created.is_file()


@then("preserva o texto original e separa análise, inferências e pontos a revisar")
def then_preserves_and_separates_analysis(context) -> None:
    content = context.created.read_text(encoding="utf-8")
    for expected in (
        context.original,
        "## Análise inicial",
        "**Inferência:**",
        "## Pontos a revisar no futuro",
    ):
        assert expected in content


@then("não cria backlog, spec, tarefas ou código")
def then_creates_only_the_idea(context) -> None:
    assert not (context.project / "specs" / "backlog").exists()
    assert not (context.project / "specs" / "specs").exists()
    assert set((context.project / "specs").rglob("*")) == {
        context.project / "specs" / "ideias",
        context.created,
    }


@given("uma instalação base do Specsfy")
def given_base_installation(context) -> None:
    context.project = temporary_project(context)
    context.installer = SkillInstaller(context.project)


@when("o CLI publica os arquivos estruturais no projeto consumidor")
def when_cli_publishes_structural_files(context) -> None:
    context.changed = context.installer.install_framework_from_checkout(ROOT)


@then(
    ".specsfy/templates contém Idea.md, Backlog.md, Spec.md, Tasks.md, "
    "Project.md, Stack.md, Rules.md e Database.md"
)
def then_all_framework_templates_are_installed(context) -> None:
    installed = context.project / ".specsfy" / "templates"
    assert set(FRAMEWORK_TEMPLATE_NAMES) == {
        path.name for path in installed.iterdir() if path.is_file()
    }
    assert all(
        installed / name in context.changed
        for name in FRAMEWORK_TEMPLATE_NAMES
    )

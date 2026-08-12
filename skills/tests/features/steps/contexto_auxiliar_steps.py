from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
SETUP = ROOT / "specsfy-setup" / "scripts" / "setup_context.mjs"
STACK = ROOT / "specsfy-aux-stack" / "scripts" / "update_stack.mjs"
DATABASE = ROOT / "specsfy-aux-database" / "scripts" / "update_database.mjs"
MONITOR = ROOT / "specsfy-setup" / "scripts" / "monitor_context.mjs"


def temporary_project(context) -> Path:
    temporary = tempfile.TemporaryDirectory()
    context.add_cleanup(temporary.cleanup)
    return Path(temporary.name)


def run(script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", str(script), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


@given("um projeto Laravel, Next ou Astro ainda sem contexto auxiliar")
def given_known_project_without_context(context) -> None:
    context.project = temporary_project(context)
    (context.project / "composer.json").write_text(
        '{"require":{"laravel/framework":"^12.0"}}',
        encoding="utf-8",
    )


@when("a skill specsfy-setup é executada")
def when_setup_runs(context) -> None:
    context.result = run(SETUP, "--project", str(context.project))
    assert context.result.returncode == 0, context.result.stderr


@then("PROJECT.md existe na raiz do projeto")
def then_project_exists(context) -> None:
    assert (context.project / "PROJECT.md").is_file()


@then("STACK.md, RULES.md e DATABASE.md existem sob .specsfy")
def then_context_files_exist(context) -> None:
    for name in ("STACK.md", "RULES.md", "DATABASE.md"):
        assert (context.project / ".specsfy" / name).is_file()


@then("os modelos refletem o stack observado")
def then_templates_reflect_stack(context) -> None:
    assert "Laravel" in (
        context.project / ".specsfy" / "STACK.md"
    ).read_text(encoding="utf-8")


@then("AGENTS.md e CLAUDE.md reservam um bloco para as diretrizes do framework")
def then_agent_files_have_reserved_blocks(context) -> None:
    for name in ("AGENTS.md", "CLAUDE.md"):
        text = (context.project / name).read_text(encoding="utf-8")
        assert "<!-- specsfy:framework:start -->" in text
        assert "<!-- specsfy:framework:end -->" in text


@given("arquivos auxiliares com dados adicionados pela pessoa")
def given_human_context(context) -> None:
    context.project = temporary_project(context)
    (context.project / "package.json").write_text(
        '{"dependencies":{"next":"15.0.0"}}',
        encoding="utf-8",
    )
    (context.project / "PROJECT.md").write_text(
        "# Projeto\n\nNota humana preservada.\n",
        encoding="utf-8",
    )
    (context.project / "AGENTS.md").write_text(
        "# Instruções humanas\n",
        encoding="utf-8",
    )


@when("setup ou uma skill specsfy-aux é executada novamente")
def when_context_tools_rerun(context) -> None:
    first = run(SETUP, "--project", str(context.project))
    stack = run(STACK, "--project", str(context.project))
    context.stack_before = (
        context.project / ".specsfy" / "STACK.md"
    ).read_text(encoding="utf-8")
    second = run(SETUP, "--project", str(context.project))
    stack_again = run(STACK, "--project", str(context.project))
    context.stack_after = (
        context.project / ".specsfy" / "STACK.md"
    ).read_text(encoding="utf-8")
    assert (
        first.returncode,
        second.returncode,
        stack.returncode,
        stack_again.returncode,
    ) == (0, 0, 0, 0)


@then("o conteúdo existente permanece no arquivo")
def then_existing_content_remains(context) -> None:
    assert "Nota humana preservada." in (
        context.project / "PROJECT.md"
    ).read_text(encoding="utf-8")


@then("somente observações novas e ausentes são acrescentadas")
def then_only_new_observations_are_added(context) -> None:
    assert context.stack_after == context.stack_before


@then("instruções do usuário fora do bloco Specsfy permanecem intactas")
def then_human_agent_instructions_remain(context) -> None:
    agents = (context.project / "AGENTS.md").read_text(encoding="utf-8")
    assert agents.startswith("# Instruções humanas")
    assert "<!-- specsfy:framework:start -->" in agents


@given("uma migration ou estrutura de banco criada no projeto")
def given_migration(context) -> None:
    context.project = temporary_project(context)
    migration = context.project / "database/migrations/2026_create_orders.php"
    migration.parent.mkdir(parents=True)
    migration.write_text(
        "<?php Schema::create('orders', function ($table) {"
        "$table->id(); $table->string('status'); });",
        encoding="utf-8",
    )
    database = context.project / ".specsfy/DATABASE.md"
    database.parent.mkdir(parents=True)
    database.write_text("# Banco\n\nDecisão humana.\n", encoding="utf-8")


@when("a skill mantenedora do banco é executada")
def when_database_maintainer_runs(context) -> None:
    context.result = run(DATABASE, "--project", str(context.project))
    assert context.result.returncode == 0, context.result.stderr


@then("DATABASE.md registra a estrutura em tabelas Markdown")
def then_database_has_tables(context) -> None:
    text = (context.project / ".specsfy/DATABASE.md").read_text(encoding="utf-8")
    assert "| Estrutura | Tipo | Campos | Relações | Fonte |" in text
    assert "orders" in text


@then("as notas e decisões humanas continuam intactas")
def then_database_human_notes_remain(context) -> None:
    assert "Decisão humana." in (
        context.project / ".specsfy/DATABASE.md"
    ).read_text(encoding="utf-8")


@given("mudanças em código da aplicação, manifests ou estruturas persistentes")
def given_monitored_changes(context) -> None:
    context.paths = [
        "package.json",
        "app/Models/Order.php",
        "database/migrations/2026_create_orders.php",
    ]


@when("o monitor de contexto compara os caminhos alterados")
def when_monitor_compares(context) -> None:
    result = run(MONITOR, "--project", "/tmp/project", "--json", "--paths", *context.paths)
    assert result.returncode == 0
    context.report = json.loads(result.stdout)


@then("ele exige STACK.md para mudanças estruturais de stack")
def then_monitor_requires_stack(context) -> None:
    assert any(
        item["document"] == ".specsfy/STACK.md"
        for item in context.report["pending"]
    )


@then("exige DATABASE.md para mudanças de banco ou migration")
def then_monitor_requires_database(context) -> None:
    assert any(
        item["document"] == ".specsfy/DATABASE.md"
        for item in context.report["pending"]
    )


@then("exige revisão explícita de PROJECT.md para mudanças da aplicação")
def then_monitor_requires_project(context) -> None:
    assert context.report["project_review_required"] is True


@then("a entrega não conclui enquanto uma obrigação documental estiver aberta")
def then_delivery_is_blocked(context) -> None:
    assert context.report["status"] == "pending"
    assert any(
        item["skill"] == "specsfy-documentator"
        for item in context.report["pending"]
    )

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "specsfy-base-specify/scripts/iniciar_spec.py"


def temporary_directory(context, name: str) -> Path:
    path = Path(tempfile.mkdtemp(prefix=f"specsfy-{name}-"))
    context.add_cleanup(shutil.rmtree, path, ignore_errors=True)
    return path


def command(
    cwd: Path,
    title: str,
    *,
    root: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, "-B", str(SCRIPT), "--title", title]
    if root is not None:
        args.extend(["--root", str(root)])
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


@given("um diretório de trabalho sem pasta specs")
@given("um diretório de trabalho sem specs")
def given_empty_working_directory(context) -> None:
    context.project = temporary_directory(context, "project")
    assert not (context.project / "specs").exists()


@when('o agente inicia a spec "{title}"')
def when_initialize_named_spec(context, title: str) -> None:
    context.result = command(context.project, title)


@then(
    "o arquivo specs/specs/0001-minha-primeira-feature/spec.md é criado nesse diretório"
)
def then_spec_is_created_in_cwd(context) -> None:
    context.spec = (
        context.project
        / "specs"
        / "specs"
        / "0001-minha-primeira-feature"
        / "spec.md"
    )
    assert context.result.returncode == 0, context.result.stderr
    assert context.spec.is_file()
    assert not (context.spec.parent / "0001-spec.md").exists()


@then("o cabeçalho é uma tabela com ID, título, slug e data preenchidos")
def then_spec_header_table_is_filled(context) -> None:
    content = context.spec.read_text(encoding="utf-8")
    assert "| Campo | Valor |" in content
    assert "| --- | --- |" in content
    assert "| ID | SPEC-0001 |" in content
    assert "# Especificação integrada: Minha Primeira Feature" in content
    assert "| Slug | 0001-minha-primeira-feature |" in content
    assert "| Atualizada em |" in content
    assert "**ID**:" not in content
    assert "{{" not in content


@then("o arquivo preserva os três atos e as dezoito seções")
def then_spec_contract_is_preserved(context) -> None:
    content = context.spec.read_text(encoding="utf-8")
    assert content.count("## Ato ") == 3
    assert sum(
        line.startswith("### ") and line[4:6].rstrip(".").isdigit()
        for line in content.splitlines()
    ) == 18


@given("o agente está fora do diretório do projeto alvo")
def given_agent_outside_target(context) -> None:
    context.outside = temporary_directory(context, "outside")
    context.project = temporary_directory(context, "target")


@when("o agente inicia uma spec informando a raiz do projeto alvo")
def when_initialize_with_explicit_root(context) -> None:
    context.result = command(
        context.outside,
        "Raiz Explicita",
        root=context.project,
    )


@then("a spec é criada somente sob a raiz informada")
def then_only_explicit_root_is_used(context) -> None:
    expected = (
        context.project
        / "specs"
        / "specs"
        / "0001-raiz-explicita"
        / "spec.md"
    )
    assert context.result.returncode == 0, context.result.stderr
    assert expected.is_file()
    assert not (context.outside / "specs").exists()


@given("um projeto com specs convertidas 0001-primeira, 0003-terceira e legado")
def given_numbered_and_legacy_specs(context) -> None:
    context.project = temporary_directory(context, "sequence")
    specs = context.project / "specs" / "specs"
    for name in ("0001-primeira", "0003-terceira", "legado"):
        (specs / name).mkdir(parents=True)


@when("o agente inicia uma nova spec")
def when_initialize_new_spec(context) -> None:
    context.result = command(context.project, "Quarta")


@then("a nova spec recebe o ID SPEC-0004")
def then_new_spec_has_fourth_id(context) -> None:
    context.spec = (
        context.project / "specs" / "specs" / "0004-quarta" / "spec.md"
    )
    assert context.result.returncode == 0, context.result.stderr
    assert "| ID | SPEC-0004 |" in context.spec.read_text(encoding="utf-8")


@then("seu diretório começa com 0004-")
def then_directory_starts_with_fourth_id(context) -> None:
    assert context.spec.parent.name.startswith("0004-")


@given("duas inicializações no mesmo projeto vazio")
def given_two_initializations(context) -> None:
    context.project = temporary_directory(context, "concurrent")


@when("ambas alocam um identificador")
def when_both_allocate(context) -> None:
    commands = []
    for title in ("Alpha", "Beta"):
        commands.append(
            subprocess.Popen(
                [sys.executable, "-B", str(SCRIPT), "--title", title],
                cwd=context.project,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
        )
    context.results = [process.communicate() + (process.returncode,) for process in commands]


@then("os diretórios criados possuem os IDs 0001 e 0002 sem duplicidade")
def then_concurrent_ids_are_unique(context) -> None:
    assert all(returncode == 0 for _, _, returncode in context.results), context.results
    names = sorted(
        path.name for path in (context.project / "specs" / "specs").iterdir()
    )
    assert [name[:4] for name in names] == ["0001", "0002"]


@when(
    "o agente tenta iniciar uma spec com título sem caracteres alfanuméricos"
)
def when_initialize_with_invalid_title(context) -> None:
    context.result = command(context.project, "!!!")


@then("o comando termina com erro acionável")
def then_command_fails_actionably(context) -> None:
    assert context.result.returncode != 0
    assert "erro:" in context.result.stderr.lower()


@then("nenhum spec.md parcial é criado")
def then_no_partial_spec(context) -> None:
    assert not list(context.project.rglob("spec.md"))

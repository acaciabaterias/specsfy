from __future__ import annotations

import subprocess
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]


def select_test(context, filename: str) -> None:
    context.directory_test = ROOT / "tests" / "Feature" / "Directory" / filename
    assert context.directory_test.is_file()


@given("existem dezesseis usuários com nomes conhecidos")
@given("uma pessoa não autenticada consulta usuários")
def given_user_directory(context) -> None:
    select_test(context, "UserDirectoryTest.php")


@given("existem usuários com nomes semelhantes e diferentes")
@given("nenhum usuário corresponde ao termo informado")
def given_user_search(context) -> None:
    select_test(context, "UserSearchTest.php")


@given("um usuário participa de equipes com papéis diferentes")
@given("não existe usuário com o identificador solicitado")
def given_user_profile(context) -> None:
    select_test(context, "UserProfileTest.php")


@given("existem equipes pessoais e compartilhadas com membros")
@given("o contrato cobre o estado sem equipes")
def given_team_directory(context) -> None:
    select_test(context, "TeamDirectoryTest.php")


@given("uma equipe possui owner admin e member")
@given("existe uma equipe sem membros")
def given_team_detail(context) -> None:
    select_test(context, "TeamDetailTest.php")


@when("uma pessoa autenticada abre o diretório de usuários")
@when("ela abre o diretório global de usuários")
@when("uma pessoa autenticada busca parte de um nome em caixa diferente")
@when("uma pessoa autenticada realiza a busca de usuário")
@when("outra pessoa autenticada abre seu perfil público")
@when("uma pessoa autenticada abre esse perfil inexistente")
@when("uma pessoa autenticada abre o diretório de equipes")
@when("uma pessoa autenticada consulta o diretório vazio de equipes")
@when("uma pessoa autenticada abre o detalhe da equipe")
@when("uma pessoa autenticada abre o detalhe da equipe vazia")
def when_directory_contract_runs(context) -> None:
    context.directory_result = subprocess.run(
        [
            "php",
            "artisan",
            "test",
            "--compact",
            str(context.directory_test.relative_to(ROOT)),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@then("recebe quinze usuários ordenados por nome e sem e-mails")
@then("é redirecionada para o login sem receber dados do diretório")
@then("recebe somente os nomes correspondentes e o filtro normalizado")
@then("recebe uma página vazia com o termo preservado")
@then("vê nome estado e equipes com os papéis sem ver e-mail")
@then("recebe uma resposta de usuário não encontrado")
@then("vê todas as equipes ordenadas com tipo e contagem de membros")
@then("vê um estado vazio de equipes sem erro")
@then("vê o resumo e membros ordenados com seus papéis")
@then("vê um estado vazio de membros sem dados pessoais")
def then_directory_contract_passes(context) -> None:
    assert context.directory_result.returncode == 0, (
        context.directory_result.stdout + context.directory_result.stderr
    )

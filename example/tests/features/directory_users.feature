@US-001 @FR-001 @FR-002 @FR-003 @NFR-001 @NFR-002 @AC-001
Feature: Diretório global de usuários

  Scenario: Pessoa autenticada consulta a primeira página
    Given existem dezesseis usuários com nomes conhecidos
    When uma pessoa autenticada abre o diretório de usuários
    Then recebe quinze usuários ordenados por nome e sem e-mails

  Scenario: Visitante tenta consultar usuários
    Given uma pessoa não autenticada consulta usuários
    When ela abre o diretório global de usuários
    Then é redirecionada para o login sem receber dados do diretório

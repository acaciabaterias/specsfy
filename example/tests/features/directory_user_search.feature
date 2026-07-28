@US-001 @FR-001 @FR-002 @FR-003 @NFR-001 @NFR-002 @AC-001
Feature: Busca e paginação de usuários

  Scenario: Busca encontra nomes ignorando caixa
    Given existem usuários com nomes semelhantes e diferentes
    When uma pessoa autenticada busca parte de um nome em caixa diferente
    Then recebe somente os nomes correspondentes e o filtro normalizado

  Scenario: Busca sem correspondência
    Given nenhum usuário corresponde ao termo informado
    When uma pessoa autenticada realiza a busca de usuário
    Then recebe uma página vazia com o termo preservado

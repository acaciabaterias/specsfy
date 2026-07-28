@US-001 @FR-001 @FR-002 @FR-003 @NFR-001 @NFR-002 @AC-001
Feature: Detalhe público de equipe

  Scenario: Pessoa autenticada consulta membros e papéis
    Given uma equipe possui owner admin e member
    When uma pessoa autenticada abre o detalhe da equipe
    Then vê o resumo e membros ordenados com seus papéis

  Scenario: Equipe sem membros
    Given existe uma equipe sem membros
    When uma pessoa autenticada abre o detalhe da equipe vazia
    Then vê um estado vazio de membros sem dados pessoais

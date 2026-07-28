@US-001 @FR-001 @FR-002 @FR-003 @NFR-001 @NFR-002 @AC-001
Feature: Diretório global de equipes

  Scenario: Pessoa autenticada consulta equipes pessoais e compartilhadas
    Given existem equipes pessoais e compartilhadas com membros
    When uma pessoa autenticada abre o diretório de equipes
    Then vê todas as equipes ordenadas com tipo e contagem de membros

  Scenario: Diretório sem equipes relevantes
    Given o contrato cobre o estado sem equipes
    When uma pessoa autenticada consulta o diretório vazio de equipes
    Then vê um estado vazio de equipes sem erro

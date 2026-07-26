@cli @progress
Feature: Projetar o progresso das especificações

  Scenario: Reconhecer os metadados tabulares de uma spec concluída
    Given uma spec concluída com o cabeçalho tabular canônico
    When o CLI projeta o progresso da especificação
    Then o status e os três gates são reconhecidos
    And o resumo contabiliza a spec como concluída

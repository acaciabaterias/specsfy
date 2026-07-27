@cli @progress
Feature: Projetar o progresso das especificações

  Scenario: Reconhecer os metadados tabulares de uma spec concluída
    Given uma spec concluída com o cabeçalho tabular canônico
    When o CLI projeta o progresso da especificação
    Then o status e os três gates são reconhecidos
    And o resumo contabiliza a spec como concluída

  Scenario: Abrir a spec destacada sem abandonar a tabela de progresso
    Given a implementação da aba Specs do CLI
    When o contrato de visualização da spec é inspecionado
    Then a tabela preserva gates, tarefas, checklist e progresso
    And a barra de espaço abre a spec destacada em um modal Markdown
    And o modal informa como voltar para a listagem

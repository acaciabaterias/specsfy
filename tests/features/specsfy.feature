@specsfy @NFR-001 @NFR-002 @NFR-003 @NFR-004
Feature: Executar todo o fluxo SDD a partir de uma única fonte da verdade
  O projeto deve usar um spec.md rígido para pesquisa, produto, plano,
  Gherkin, TDD, validações, tarefas, execução e evidências.

  @US-001 @FR-001 @FR-002 @AC-001
  Scenario: Conduzir descoberta com uma skill dedicada
    Given o repositório Specsfy
    When executo a verificação de aceite "skill-catalog"
    Then a verificação de aceite passa

  @US-002 @FR-003 @FR-004 @AC-002
  Scenario: Manter um pacote autocontido com uma única fonte normativa
    Given o repositório Specsfy
    When executo a verificação de aceite "rigid-source"
    Then a verificação de aceite passa

  @US-003 @FR-005 @AC-003
  Scenario: Validar formato e conteúdo da fonte
    Given o repositório Specsfy
    When executo a verificação de aceite "strict-validation"
    Then a verificação de aceite passa

  @US-004 @FR-006 @FR-007 @AC-004
  Scenario: Exigir aceite Gherkin e RED TDD
    Given o repositório Specsfy
    When executo a verificação de aceite "bdd-tdd-contract"
    Then a verificação de aceite passa

  @US-005 @FR-008 @AC-005
  Scenario: Validar tarefas embutidas no spec
    Given o repositório Specsfy
    When executo a verificação de aceite "embedded-tasks"
    Then a verificação de aceite passa

  @US-006 @FR-009 @FR-010 @AC-006
  Scenario: Executar e concluir pela fonte única
    Given o repositório Specsfy
    When executo a verificação de aceite "execution"
    Then a verificação de aceite passa

  @US-007 @FR-011 @FR-012 @AC-007
  Scenario: Acompanhar progresso por checklist
    Given o repositório Specsfy
    When executo a verificação de aceite "task-checklists"
    Then a verificação de aceite passa

  @US-008 @FR-013 @FR-014 @AC-008
  Scenario: Consultar progresso geral de todas as especificações
    Given o repositório Specsfy
    When executo a verificação de aceite "overall-progress"
    Then a verificação de aceite passa

  @US-009 @FR-015 @FR-016 @AC-009
  Scenario: Aplicar descoberta categorial sem perder a intenção
    Given o repositório Specsfy
    When executo a verificação de aceite "mcr-10"
    Then a verificação de aceite passa

  @US-010 @FR-017 @FR-018 @AC-010
  Scenario: Percorrer três atos com handoffs explícitos
    Given o repositório Specsfy
    When executo a verificação de aceite "three-act-flow"
    Then a verificação de aceite passa

  @US-011 @FR-019 @FR-020 @FR-021 @NFR-005 @AC-011
  Scenario: Publicar visão geral e metodologia sem misturar seus owners
    Given o repositório Specsfy
    When executo a verificação de aceite "readme-guide"
    Then a verificação de aceite passa

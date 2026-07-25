@US-001
Feature: Aplicação de exemplo do Specsfy

  @US-002 @FR-006 @FR-007 @FR-008 @FR-009 @AC-002
  Scenario: Distinguir documentação oficial de documentação interna
    Given as portas de entrada do workspace e o contexto transversal
    When o público e o owner de cada documentação são inspecionados
    Then docs é apresentado como documentação oficial para usuários
    And example é apresentado como aplicação interna com owner próprio

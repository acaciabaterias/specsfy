@specsfy @cli @ux
Feature: Catálogo de skills na TUI
  Para decidir instalações e remoções sem interpretar uma lista densa
  Como pessoa usando o CLI
  Quero comparar skills em uma tabela e inspecionar a decisão antes de aplicá-la

  Scenario: Planejar skills por tabela e painel de detalhes
    Given a implementação da aba Skills do CLI
    When o contrato de apresentação é inspecionado
    Then as skills aparecem em uma tabela com plano, nome, categoria e estado
    And a skill destacada possui um painel de detalhes e uma ação explícita
    And a decisão pode ser alternada por teclado ou mouse sem aplicação imediata

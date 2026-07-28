@specsfy @validation @testing
Feature: Cobertura mínima de comportamento por item da spec
  Para dar contexto suficiente a pessoas e agentes antes da implementação
  Como pessoa responsável pela qualidade da especificação
  Quero pelo menos três cenários BDD e três casos TDD por história, feature e requisito

  Scenario: Rejeitar definição com menos de três cenários por história
    Given uma spec com uma história de usuário coberta por menos de três ACs distintos
    When o Definition Gate valida a cobertura BDD
    Then a história é reportada com a quantidade observada e o mínimo esperado
    And a feature não avança enquanto a lacuna permanecer

  Scenario: Rejeitar definição com menos de três cenários por requisito
    Given uma spec com requisitos funcionais e não funcionais
    When menos de três ACs distintos cobrem qualquer requisito
    Then cada requisito incompleto é reportado separadamente
    And somente ACs que declaram o ID em Cobre contam para o mínimo

  Scenario: Rejeitar entrega com menos de três casos TDD rastreáveis
    Given uma spec definida com histórias, requisitos e pelo menos três ACs
    When a rastreabilidade encontra menos de três marcadores de caso SPECSFY para um item
    Then ela reporta a quantidade de casos TDD ausentes por ID
    And um único marcador compartilhado não é contado como três casos

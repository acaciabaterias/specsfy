@specsfy @testing
Feature: Cobertura mínima por item da especificação
  Para dar contexto suficiente aos agentes em cada fatia
  Como pessoa que aplica o Specsfy
  Quero três cenários BDD e três casos TDD por feature, história e requisito

  Scenario: Bloquear definição com contexto BDD insuficiente
    Given os contratos de cobertura de skills e documentação
    When a política mínima da spec é inspecionada
    Then o Definition Gate exige três ACs distintos por feature US FR e NFR

  Scenario: Bloquear entrega com casos TDD insuficientes
    Given os contratos de cobertura de skills e documentação
    When a política mínima da spec é inspecionada
    Then a rastreabilidade exige três marcadores de caso por feature US FR e NFR
    And cada AC continua exigindo ao menos um caso TDD

  Scenario: Publicar a mesma regra no template e na documentação
    Given os contratos de cobertura de skills e documentação
    When a política mínima da spec é inspecionada
    Then template contrato central e guia oficial explicam o mínimo de três

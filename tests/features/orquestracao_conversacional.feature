Feature: Orquestração conversacional integrada
  Como pessoa que aplica o Specsfy
  Quero atravessar etapas na mesma conversa
  Para não precisar descobrir e repetir comandos de handoff

  Scenario: Publicar o protocolo em metodologia e documentação
    Given o contrato executável e a documentação oficial do Specsfy
    When uma etapa conclui ou detecta pendência de outra responsabilidade
    Then todas as skills base anunciam e executam a transição automaticamente
    And o fluxo documenta avanço, retorno e retomada automáticos
    And a etapa escolhida continua na mesma conversa sem confirmação

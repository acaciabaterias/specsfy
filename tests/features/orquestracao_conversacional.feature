Feature: Orquestração conversacional integrada
  Como pessoa que aplica o Specsfy
  Quero atravessar etapas na mesma conversa
  Para não precisar descobrir e repetir comandos de handoff

  Scenario: Publicar o protocolo em metodologia e documentação
    Given o contrato executável e a documentação oficial do Specsfy
    When uma etapa conclui ou detecta pendência de outra responsabilidade
    Then as skills posteriores à captura anunciam e executam a transição automaticamente
    And o fluxo documenta avanço, retorno e retomada automáticos
    And a etapa escolhida continua na mesma conversa sem confirmação
    And mudança tardia usa uma entrada pública e executável

  Scenario: Refinar o backlog até fechar lacunas ou receber avanço explícito
    Given o contrato do refinamento do backlog e do método MCR-10
    When a pessoa responde uma pergunta do refinamento do backlog
    Then o refinamento do backlog reavalia o contexto acumulado com a nova resposta
    And continua sem limite máximo enquanto existir lacuna aplicável
    And oferece avançar a partir da décima primeira pergunta
    And o avanço preserva as lacunas e mantém a definição pendente

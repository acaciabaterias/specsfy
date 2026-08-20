@specsfy @interaction
Feature: Perguntas numeradas em todas as skills conversacionais
  Para responder às entrevistas do Specsfy sem depender da ordem visual
  Como pessoa que usa as skills do framework
  Quero perguntas e opções numeradas com saídas livres em cada rodada

  Scenario: Exibir uma rodada completa de perguntas
    Given o contrato central de interação do Specsfy
    When uma skill precisa perguntar algo à pessoa
    Then a rodada contém exatamente uma pergunta numerada
    And a pergunta oferece pelo menos três opções numeradas
    And a pergunta oferece escrever outra resposta, gerar outras opções ou avançar

  Scenario: Limitar uma área de conversa
    Given o contrato central de interação do Specsfy
    When uma área chegar a oito perguntas
    Then o agente apresenta uma síntese e para a conversa daquela área
    And só continua se a pessoa pedir mais perguntas e informar quantas quer responder

  Scenario: Confirmar o destino da área depois de avançar
    Given o contrato central de interação do Specsfy
    When a pessoa escolhe avançar em uma área
    Then a rodada seguinte oferece encerrar a área, responder depois ou retomar agora
    And a escolha de encerrar ou adiar fica registrada
    And uma área encerrada não volta ao roteiro sem reabertura explícita

  Scenario: Classificar todas as skills pelo modo de interação
    Given todas as skills base e auxiliares do Specsfy
    When seus contratos de interação são inspecionados
    Then toda skill que pode perguntar aponta para o contrato numerado
    And toda skill restante declara que não faz perguntas

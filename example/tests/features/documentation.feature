@documentation
Feature: Documentação operacional da aplicação de exemplo

  Scenario: Consultar capacidades e fontes executáveis
    Given a documentação operacional da aplicação
    When o contrato documental local é executado
    Then capacidades fontes rotas e comandos são verificáveis

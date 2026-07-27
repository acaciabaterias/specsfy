@contexto-auxiliar
Feature: Contexto persistente em projetos consumidores
  Para que agentes compreendam o sistema sem apagar conhecimento humano
  Como pessoa que aplica o Specsfy
  Quero setup e mantenedores próprios para projeto, stack, regras e banco

  Scenario: Publicar o contrato completo de contexto auxiliar
    Given os repositórios de skills, CLI e documentação do Specsfy
    When o contrato de contexto auxiliar é inspecionado
    Then setup e as três skills auxiliares possuem responsabilidades distintas
    And o projeto consumidor recebe caminhos canônicos para projeto stack regras e banco
    And as diretrizes publicáveis dos agentes possuem uma referência sincronizada
    And a instalação reconhece setup e skills auxiliares como parte do framework

  Scenario: Bloquear entrega com contexto documental pendente
    Given o monitor de contexto publicado pela skill de setup
    When manifests banco ou código da aplicação mudam
    Then o fluxo exige os documentos mantenedores correspondentes
    And planejamento implementação e progresso consultam o mesmo monitor

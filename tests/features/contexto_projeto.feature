@US-001
Feature: Contexto compartilhado do projeto

  @US-002 @FR-001 @FR-002 @FR-003 @FR-006 @FR-007 @NFR-001 @NFR-002 @NFR-003 @AC-001
  Scenario: Consultar o contrato de cada arquivo de contexto
    Given o repositório Specsfy e o contrato vigente da biblioteca de contexto
    When a biblioteca de contexto é inspecionada
    Then cada documento explica seu papel, classificação e regras de uso
    And os contextos respeitam a política de tamanho e os links locais

  @US-002 @FR-004 @FR-005 @FR-008 @FR-010 @NFR-002 @AC-002
  Scenario: Selecionar contexto pelo tipo de alteração
    Given as portas de entrada e os índices hierárquicos da biblioteca
    When uma pessoa ou agente procura orientação para uma mudança
    Then encontra arquivos exatos de leitura e atualização por tipo de alteração
    And encontra a precedência entre contexto, especificação e fonte executável

  @US-002 @FR-008 @FR-011 @FR-012 @NFR-002 @AC-003
  Scenario: Auditar a navegabilidade de toda a documentação
    Given a árvore de documentação e seus índices
    When o contrato percorre links e decisões arquiteturais
    Then todo documento é alcançável a partir do portal
    And cada arquivo, âncora e ADR referenciado existe

  @US-002 @FR-009 @FR-010 @NFR-001 @AC-004
  Scenario: Manter apenas unidades de contexto independentes
    Given os contextos vigentes do Specsfy
    When a estrutura progressiva é inspecionada
    Then assuntos sem conteúdo independente permanecem no índice do domínio
    And arquivos acima do limiar exigem justificativa em vez de divisão automática

  @US-003 @FR-013 @FR-014 @NFR-002 @NFR-003 @AC-005
  Scenario: Aprender a usar o sistema documental
    Given o guia geral e o roteador operacional da documentação
    When uma pessoa consulta como documentar uma mudança
    Then encontra organização, autoridades e destinos para cada informação
    And encontra critérios de criação e manutenção sem duplicar o roteador

  @US-004 @FR-015 @FR-016 @FR-017 @FR-018 @FR-019 @FR-020 @NFR-002 @NFR-003 @AC-006
  Scenario: Encontrar a fonte correta em cada repositório independente
    Given o workspace orquestrador e os quatro repositórios filhos
    When uma pessoa ou agente consulta suas portas de entrada
    Then cada repositório declara público responsabilidade e fronteira Git
    And a metodologia documentação identidade e visão geral possuem um único owner
    And o pai não instala nem executa as skills do projeto

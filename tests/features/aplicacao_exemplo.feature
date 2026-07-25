@US-001
Feature: Aplicação de exemplo do Specsfy

  @US-001 @FR-001 @FR-002 @FR-003 @FR-004 @FR-005 @AC-001
  Scenario: Compreender e operar o ambiente de validação
    Given a aplicação de exemplo e suas fontes executáveis
    When um mantenedor consulta sua porta de entrada
    Then encontra finalidade limites capacidades arquitetura dados e rotas
    And encontra instalação operação testes e referências verificáveis

  @US-002 @FR-006 @FR-007 @FR-008 @FR-009 @AC-002
  Scenario: Distinguir documentação oficial de documentação interna
    Given as portas de entrada do workspace e o contexto transversal
    When o público e o owner de cada documentação são inspecionados
    Then docs é apresentado como documentação oficial para usuários
    And example é apresentado como aplicação interna pertencente a dev

  @US-003 @FR-010 @FR-011 @FR-012 @NFR-001 @NFR-002 @NFR-003 @AC-003
  Scenario: Auditar documentação junto com a mudança
    Given a documentação afetada e as fontes executáveis referenciadas
    When o contrato de integridade documental é executado
    Then cada arquivo diretório âncora rota e comando citado é verificável
    And a regra de atualização documental está presente nas instruções e no contexto

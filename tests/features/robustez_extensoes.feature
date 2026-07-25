@robustez-extensoes @NFR-001 @NFR-002 @NFR-003 @NFR-004 @NFR-005 @NFR-006
Feature: Robustez das extensões nativas

  @US-001 @FR-001 @FR-002 @AC-001
  Scenario: Rejeitar evidência cujo arquivo mudou depois da atestação
    Given o contrato de robustez das extensões
    When executo o contrato de robustez "attested-evidence"
    Then o contrato de robustez passa

  @US-002 @FR-003 @AC-002
  Scenario: Alterar o digest quando a política muda
    Given o contrato de robustez das extensões
    When executo o contrato de robustez "policy-digest"
    Then o contrato de robustez passa

  @US-003 @FR-004 @AC-003
  Scenario: Rejeitar QA sem check atestado para a spec
    Given o contrato de robustez das extensões
    When executo o contrato de robustez "attested-qa"
    Then o contrato de robustez passa

  @US-004 @FR-005 @AC-004
  Scenario: Exigir pins imutáveis no workflow
    Given o contrato de robustez das extensões
    When executo o contrato de robustez "immutable-ci"
    Then o contrato de robustez passa

  @US-005 @FR-006 @FR-007 @AC-005
  Scenario: Encerrar check lento e truncar saída excessiva
    Given o contrato de robustez das extensões
    When executo o contrato de robustez "runner-limits"
    Then o contrato de robustez passa

  @US-006 @FR-008 @AC-006
  Scenario: Rejeitar finding sem integridade referencial
    Given o contrato de robustez das extensões
    When executo o contrato de robustez "finding-integrity"
    Then o contrato de robustez passa

  @US-007 @FR-009 @AC-007
  Scenario: Rejeitar claim sem orçamento ou âncora válida
    Given o contrato de robustez das extensões
    When executo o contrato de robustez "research-integrity"
    Then o contrato de robustez passa

  @US-008 @FR-010 @AC-008
  Scenario: Preservar classe de impacto após renumeração
    Given o contrato de robustez das extensões
    When executo o contrato de robustez "semantic-impact"
    Then o contrato de robustez passa

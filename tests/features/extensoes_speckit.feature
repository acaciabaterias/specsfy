@extensoes-speckit @NFR-001 @NFR-002 @NFR-003 @NFR-004 @NFR-005 @NFR-006
Feature: Adaptar extensões úteis do Spec Kit ao contrato Specsfy
  As capacidades devem permanecer nativas, rastreáveis e compatíveis com a
  fonte única e as sete skills existentes.

  @US-001 @FR-001 @FR-002 @FR-003 @AC-001
  Scenario: Aplicar os mesmos gates em todas as fronteiras
    Given o contrato de adaptações Spec Kit
    When executo o contrato focal "gate-parity"
    Then o contrato focal passa

  @US-002 @FR-004 @FR-005 @FR-006 @AC-002
  Scenario: Rejeitar conclusão fantasma
    Given o contrato de adaptações Spec Kit
    When executo o contrato focal "evidence-chain"
    Then o contrato focal passa

  @US-003 @FR-007 @FR-008 @FR-009 @AC-003
  Scenario: Carregar somente research indexado e decidido
    Given o contrato de adaptações Spec Kit
    When executo o contrato focal "research"
    Then o contrato focal passa

  @US-004 @FR-010 @FR-011 @AC-004
  Scenario: Antecipar impacto e explicar o histórico
    Given o contrato de adaptações Spec Kit
    When executo o contrato focal "change"
    Then o contrato focal passa

  @US-005 @FR-012 @FR-013 @FR-014 @AC-005
  Scenario: Validar findings especializados sem decidir requisitos
    Given o contrato de adaptações Spec Kit
    When executo o contrato focal "reviews"
    Then o contrato focal passa

  @US-006 @FR-015 @AC-006
  Scenario: Auditar prova de QA para cada AC
    Given o contrato de adaptações Spec Kit
    When executo o contrato focal "qa"
    Then o contrato focal passa

  @US-007 @FR-016 @AC-007
  Scenario: Distinguir estimativa de medição de contexto
    Given o contrato de adaptações Spec Kit
    When executo o contrato focal "context"
    Then o contrato focal passa

  @US-008 @FR-017 @AC-008
  Scenario: Renderizar resumo somente de entrega comprovada
    Given o contrato de adaptações Spec Kit
    When executo o contrato focal "delivery"
    Then o contrato focal passa


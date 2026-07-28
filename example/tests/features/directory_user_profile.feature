@US-001 @FR-001 @FR-002 @FR-003 @NFR-001 @NFR-002 @AC-001
Feature: Perfil público de usuário

  Scenario: Pessoa autenticada consulta as equipes de um usuário
    Given um usuário participa de equipes com papéis diferentes
    When outra pessoa autenticada abre seu perfil público
    Then vê nome estado e equipes com os papéis sem ver e-mail

  Scenario: Perfil inexistente
    Given não existe usuário com o identificador solicitado
    When uma pessoa autenticada abre esse perfil inexistente
    Then recebe uma resposta de usuário não encontrado

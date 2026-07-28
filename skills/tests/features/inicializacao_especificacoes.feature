@specsfy @initialization
Feature: Inicialização de especificações
  Para manter a fonte normativa no projeto correto
  Como agente de especificação
  Quero iniciar specs ordenadas a partir do template canônico

  @US-001 @FR-001 @FR-002 @FR-003 @FR-004 @AC-001
  Scenario: Criar uma spec preenchida no projeto atual
    Given um diretório de trabalho sem pasta specs
    When o agente inicia a spec "Minha Primeira Feature"
    Then o arquivo specs/specs/0001-minha-primeira-feature/spec.md é criado nesse diretório
    And o cabeçalho é uma tabela com ID, título, slug e data preenchidos
    And o arquivo preserva os três atos e as dezoito seções

  @US-001 @FR-001 @FR-002 @AC-002
  Scenario: Criar uma spec em uma raiz explicitamente selecionada
    Given o agente está fora do diretório do projeto alvo
    When o agente inicia uma spec informando a raiz do projeto alvo
    Then a spec é criada somente sob a raiz informada

  @US-002 @FR-005 @FR-006 @AC-003
  Scenario: Alocar o próximo identificador local
    Given um projeto com specs convertidas 0001-primeira, 0003-terceira e legado
    When o agente inicia uma nova spec
    Then a nova spec recebe o ID SPEC-0004
    And seu diretório começa com 0004-

  @US-002 @FR-005 @FR-007 @AC-004
  Scenario: Inicializar duas specs simultaneamente
    Given duas inicializações no mesmo projeto vazio
    When ambas alocam um identificador
    Then os diretórios criados possuem os IDs 0001 e 0002 sem duplicidade

  @US-001 @US-002 @FR-004 @FR-007 @AC-005
  Scenario: Rejeitar título que não produz slug válido
    Given um diretório de trabalho sem specs
    When o agente tenta iniciar uma spec com título sem caracteres alfanuméricos
    Then o comando termina com erro acionável
    And nenhum spec.md parcial é criado

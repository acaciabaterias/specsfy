@interface-design-system
Feature: Governança de interface do Specsfy
  Para manter personalidade e consistência nas telas SaaS
  Como pessoa que especifica ou implementa uma interface
  Quero uma fonte macro com padrões e cenários canônicos

  Scenario: Registrar os padrões SaaS obrigatórios
    Given o template global de design system do Specsfy
    When os padrões de CRUD são lidos
    Then listas usam DataGrid com PageHeader
    And detalhes usam DetailLists com PageHeader
    And criação e edição usam seções com duas colunas responsivas
    And erros de campo aparecem em vermelho abaixo do campo

  Scenario: Aplicar defaults sem apagar uma direção explícita
    Given a skill especialista de design system do Specsfy
    When sua política de direção é lida
    Then ela aplica os defaults quando a pessoa não informa direção visual
    And ela registra exceções com alcance definido
    And ela preserva a personalidade do produto na hierarquia de informação

  Scenario: Entregar o design system ao projeto consumidor
    Given o instalador e o catálogo de especialistas do Specsfy
    When a integração do design system é lida
    Then o CLI publica o template DESIGNSYSTEM.MD
    And o especialista de experiência depende do especialista de design system
    And o template Interface.md aponta para DESIGNSYSTEM.MD

  Scenario: Orientar dashboards e blocos comuns de interface
    Given o template global de design system do Specsfy
    When os padrões comuns de interface são lidos
    Then dashboards usam PageHeader, filtros e indicadores com contexto
    And primitives de shadcn/ui e blocos ReUI podem compor CRUDs e dashboards
    And a interface cobre teclado, foco, estados e responsividade

  Scenario: Tornar a linha do DataGrid uma ação de detalhe
    Given o contrato de interação do DataGrid do Specsfy
    When a navegação da lista é lida
    Then toda a linha abre o detalhe por clique e teclado
    And ações internas não disparam a navegação da linha

  Scenario: Exibir o contexto da equipe em todas as telas
    Given o contrato de navegação contextual do Specsfy
    When o breadcrumb global é lido
    Then toda tela exibe equipe, módulo e tela atual
    And Laravel reaproveita o breadcrumb existente do layout

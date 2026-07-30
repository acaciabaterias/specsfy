@cli @updater
Feature: Atualizar o CLI instalado como pacote npm
  Para receber correções pelo gerenciador usado na instalação
  Como pessoa que abre a aplicação Specsfy
  Quero ser avisada e decidir antes de instalar uma versão nova

  Scenario: Verificar, oferecer e instalar uma atualização segura
    Given a implementação do auto updater do CLI
    When o contrato de atualização é inspecionado
    Then dados e configurações globais usam ~/.specsfy/cli.json
    And a versão mais recente deriva de tags semânticas do repositório
    And a atualização é delegada ao pacote npm oficial
    And aceitar a oferta atualiza e encerra enquanto recusar abre normalmente

@cli-release
Feature: Publicar versões do Specsfy CLI a partir do dev hub
  Para manter tag, pacote, changelog e GitHub Release coerentes
  Como pessoa mantenedora do Specsfy
  Quero uma skill local que publique uma versão do CLI de forma verificável

  Scenario: Preparar uma versão com uma única fonte para as notas
    Given a skill local de release do CLI
    When uma versão semântica estável e suas notas são preparadas
    Then a versão é atualizada nas fontes do pacote
    And o changelog promove as notas para a versão datada
    And as notas extraídas para o GitHub Release são idênticas ao changelog

  Scenario: Publicar commit tag e GitHub Release
    Given a skill local de release do CLI
    When o fluxo de publicação é inspecionado
    Then ele valida o hub a main sincronizada e a worktree limpa
    And ele executa testes e reconstrói o executável antes do commit
    And ele cria e envia a tag semântica no commit de release
    And ele publica o GitHub Release com a seção exata do changelog
    And ele permite retomar uma publicação parcial sem duplicar a versão

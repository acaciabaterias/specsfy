@icone-framework
Feature: Ícone oficial do framework Specsfy
  Para reconhecer o framework de forma consistente em todo o ecossistema
  Como equipe responsável pela identidade do Specsfy
  Quero publicar os formatos vetorial e raster a partir do owner de marca

  Scenario: Manter o ícone canônico disponível
    Given os novos arquivos SVG e PNG do ícone do framework
    When a adoção visual do workspace é inspecionada
    Then os dois formatos permanecem canônicos no repositório de marca
    And o manual distingue o ícone do framework do logo e dos ícones conceituais

  Scenario: Publicar o manual de marca em PDF a partir do Markdown
    Given a fonte Markdown do guia completo de marca
    When o contrato de build do manual é inspecionado
    Then o PDF canônico fica na raiz do repositório de marca
    And o monorepo possui o gerador e a folha de estilo da marca
    And o comando make brand-guide reconstrói o PDF quando suas fontes mudam

  Scenario: Exibir o logo oficial em todos os READMEs do monorepo
    Given os READMEs versionados encontrados recursivamente
    When a adoção do logo oficial nesses arquivos é inspecionada
    Then todos os READMEs encontrados recursivamente exibem os lockups oficiais

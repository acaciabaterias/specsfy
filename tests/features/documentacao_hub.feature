@documentacao-hub
Feature: Documentação oficial do workspace Specsfy
  Para publicar conhecimento técnico e orientação de uso sem misturar owners
  Como equipe responsável pelo hub de desenvolvimento
  Quero uma skill local que reconcilie os oito repositórios com specsfy docs

  Scenario: Restringir a skill ao hub
    Given a skill de documentação do hub
    When sua identidade e fronteiras são inspecionadas
    Then ela é descoberta nas pastas padrão de Codex e Claude
    And ela valida as oito raízes Git do workspace
    And ela publica somente no repositório specsfy docs
    And ela não é instalada pelo CLI em projetos consumidores

  Scenario: Cobrir documentação técnica e guias do usuário
    Given a fonte da verdade distribuída do Specsfy
    When o contrato documental do hub é inspecionado
    Then ele roteia arquitetura módulos dependências stack dados fluxos e testes
    And ele roteia instalação método CLI contexto especialistas e documentação do sistema
    And a documentação oficial explica como executar a skill do hub

  Scenario: Publicar a instalação do CLI e do framework
    Given a fonte da verdade distribuída do Specsfy
    When o contrato documental do hub é inspecionado
    Then a skill exige um guia temático de instalação em specsfy docs
    And o guia instala o CLI e o framework no projeto consumidor
    And o portal e o guia operacional do CLI apontam para a instalação

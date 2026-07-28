@specsfy @documentation
Feature: Documentação técnica viva do sistema
  Para que humanos e agentes compreendam a aplicação existente
  Como equipe que aplica o Specsfy
  Quero reconstruir um mapa técnico completo depois de cada implementação

  Scenario: Documentar uma aplicação Laravel com frontend React
    Given uma aplicação Laravel existente com banco, rotas, testes e frontend
    When a skill specsfy-documentator constrói a documentação
    Then docs contém arquitetura aplicação banco fluxos testes frontend pacotes integrações e decisões
    And os mapas usam Mermaid para componentes fluxo classes e entidades
    And controllers models views React Tailwind e Pest são inventariados

  Scenario: Documentar uma aplicação Node existente
    Given uma aplicação Node existente com Next React Tailwind e Vitest
    When a skill specsfy-documentator constrói a documentação
    Then a documentação descreve páginas componentes APIs testes e comandos
    And cada pacote possui classificação versão fonte e referência GitHub

  Scenario: Reconstruir sem apagar conhecimento humano
    Given uma documentação gerada com observações adicionadas pela equipe
    When o documentador é executado novamente depois de uma implementação
    Then os blocos detectados refletem o código atual
    And o conteúdo humano fora dos blocos permanece intacto

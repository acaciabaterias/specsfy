@specsfy @ideia
Feature: Captura imediata de ideias
  Para não perder uma intenção ainda incompleta
  Como pessoa usuária do Specsfy
  Quero armazenar meu texto sem responder perguntas

  Scenario: Capturar e pré-processar uma ideia sem diálogo
    Given um projeto consumidor inicializado para ideias
    When o agente recebe somente o texto da ideia
    Then ele não faz perguntas nem solicita confirmação
    And cria specs/ideias/data-hora-slug.md a partir do template instalado
    And preserva o texto original e separa análise, inferências e pontos a revisar
    And não cria backlog, spec, tarefas ou código

  Scenario: Instalar todos os templates documentais do framework
    Given uma instalação base do Specsfy
    When o CLI publica os arquivos estruturais no projeto consumidor
    Then .specsfy/templates contém Idea.md, Backlog.md, Spec.md, Tasks.md, Project.md, Stack.md, Rules.md e Database.md

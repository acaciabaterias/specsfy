@specsfy @inbox
Feature: Captura imediata na Inbox
  Para não perder uma intenção ainda incompleta
  Como pessoa usuária do Specsfy
  Quero armazenar meu texto sem responder perguntas

  Scenario: Capturar e pré-processar uma entrada sem diálogo
    Given um projeto consumidor inicializado para a Inbox
    When o agente recebe somente o texto da entrada
    Then ele não faz perguntas nem solicita confirmação
    And cria specs/inbox/data-hora-slug.md a partir do template instalado
    And preserva o texto original e separa análise, inferências e pontos a revisar
    And não cria backlog, spec, tarefas ou código

  Scenario: Instalar todos os templates documentais do framework
    Given uma instalação base do Specsfy
    When o CLI publica os arquivos estruturais no projeto consumidor
    Then .specsfy/templates contém Inbox.md, Backlog.md, Spec.md, Tasks.md, Project.md, Stack.md, Rules.md e Database.md
    And cria .specsfy/templates/custom sem gerenciar seu conteúdo

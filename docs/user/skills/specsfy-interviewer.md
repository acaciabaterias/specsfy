# Conversar com uma spec

`specsfy-interviewer` ajuda você a resolver uma lacuna que pode mudar a próxima
etapa da spec. Ele lê o estado atual, faz uma pergunta relevante por vez e só
registra respostas que você confirmou.

## Quando usar

Use durante `draft`, `defined`, `planned`, `in-progress` ou `review` quando
uma escolha de produto, escopo, dependência, teste ou aceite ainda estiver
aberta. A Inbox não usa entrevistador: ela preserva sua mensagem sem perguntas.

## Como descrever a tarefa

Peça “converse comigo sobre a spec de login social antes de montar as tarefas”
ou informe o ID da spec e a dúvida que precisa resolver.

## Exemplo passo a passo

O entrevistador lê a spec e pergunta apenas o ponto que impede o
plano, como o provedor de identidade ou o comportamento quando a conta já
existe.

```text
specs/planned/0042-login-social/spec.md
```

Depois de cada resposta, ele verifica se mudou a estimativa de execução. Se
necessário, registra `Effort`, data e justificativa com o comando do CLI.

## O que esperar

Effort vai de 1 a 10 e mede a capacidade de execução necessária, não duração:

- 1–2: alteração atômica;
- 3–6: trabalho local ou integração conhecida;
- 7–8: migração ou integração transversal;
- 9–10: arquitetura ou incerteza que pede revisão humana frequente.

O histórico fica na própria `spec.md`, para que você entenda por que a
estimativa mudou.

## Erros comuns

- usar o entrevistador para capturar uma Inbox, que não recebe perguntas;
- esperar que ele aprove um gate ou mova a pasta sem a skill da etapa;
- usar Effort como prazo ou vinculá-lo a um modelo específico.

## Próximo passo

O entrevistador não aprova gates, implementa código ou move a spec. Ao fechar a
lacuna, ele entrega o trabalho à skill responsável pela fase atual. Quando
ClickUpfy estiver instalado e houver uma tarefa vinculada, essa skill também
atualiza a projeção remota.

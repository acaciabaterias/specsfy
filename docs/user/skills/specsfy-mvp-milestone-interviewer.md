# Definir o MVP por milestones

Use `$specsfy-mvp-milestone-interviewer` (`specsfy-mvp-milestone-interviewer`)
para explorar o menor produto utilizável sem perder o caminho da conversa. A
skill lê `MVP.md` e `BRAND.md` da raiz quando eles existem e preserva cada
resposta em uma Inbox da mesma sessão.

## Quando usar

Use antes de criar um conjunto de specs para um produto novo ou quando o MVP
ainda não tem uma jornada confirmada. Se `MVP.md` existir, a skill o importa
uma vez como `specs/milestones/M01.md`, com o título `Milestone 1.0`. Ela nunca
substitui um marco que já exista.

Cada rodada traz pelo menos três perguntas numeradas. Abaixo de cada pergunta,
você recebe três ou mais sugestões, `Escrever outra resposta` e `Avançar`
desde a primeira rodada.

## Como descrever a tarefa

Peça: “use o entrevistador de MVP para organizar os marcos do meu sistema de
leads”.

## Exemplo passo a passo

```text
Ideia → entrevista adaptativa → síntese aprovada → M01, M02 e specs vinculadas
```

## O que esperar

Cada resposta é salva em `specs/inbox/` e recebe a mesma identificação de
sessão. Ao final, você recebe uma síntese e os caminhos das capturas. Peça o
refinamento quando quiser que `$specsfy-02-backlog` trate a série inteira. A
skill não cria backlog, spec, tarefa ou código durante a conversa.

## Erros comuns

- pedir tarefas técnicas antes de tratar as Inboxes;
- misturar uma hipótese da conversa com o texto que foi registrado;
- esperar que a importação substitua uma `Milestone 1.0` já existente.

## Próximo passo

Leia [Milestones](../milestones.md) para conhecer arquivos e sincronização.

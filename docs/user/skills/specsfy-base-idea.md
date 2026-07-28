# Capturar uma ideia com `specsfy-base-idea`

Esta skill funciona como uma caixa de entrada: recebe seu texto, guarda o
original e organiza uma primeira leitura sem interromper você com perguntas.

## Quando usar

Use quando quiser anotar uma ideia, oportunidade, necessidade ou pensamento
para retomar depois. O arquivo fica em `specs/ideias/`.

Não use para refinar prioridade, decidir requisitos ou iniciar implementação.
Esses trabalhos pertencem às etapas seguintes.

## Como pedir

```text
Use $specsfy-base-idea para capturar:
seria útil avisar clientes quando uma entrega atrasar, talvez por e-mail.
```

Você também pode simplesmente pedir “guarde esta ideia” e incluir o texto.

## Exemplo passo a passo

1. Você envia o texto livre.
2. O agente preserva o texto original.
3. Sem fazer perguntas, ele extrai resumo, problema ou oportunidade, pessoas,
   valor esperado, sinais, riscos e pontos a revisar.
4. Ele cria um nome com data, hora e slug.
5. Ele informa o caminho criado e encerra a captura.

## O que esperar

```text
specs/ideias/2026-07-28-143205-avisar-clientes-sobre-atrasos.md
```

O arquivo diferencia o que você declarou, o que foi inferido e o que ainda
precisa ser revisto. Nenhum backlog, spec, tarefa ou código é criado.

Os metadados incluem horário da captura, origem, slug, status, hash do texto
original e links futuros para backlog ou spec.

## Erros comuns

- esperar que a captura faça perguntas ou complete decisões ausentes;
- tratar a análise inicial como requisito aprovado;
- implementar diretamente a partir de `specs/ideias/`;
- editar o texto original em vez de registrar uma evolução no backlog;
- procurar o template dentro da skill: ele vive em
  `.specsfy/templates/Idea.md`.

## Próximo passo

Deixe a ideia guardada ou use
[`specsfy-base-backlog`](specsfy-base-backlog.md) quando quiser refiná-la.

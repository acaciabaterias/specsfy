# Aprofundar uma ideia com `specsfy-base-interview`

Esta skill conduz uma conversa para transformar dúvidas importantes em decisões
testáveis. Ela faz uma pergunta prioritária por vez e entrega um brief na
própria conversa.

## Quando usar

Use quando uma ideia ou backlog precisa de mais clareza: público, finalidade,
regras, limites, privacidade, falhas ou resultado esperado.

Não use para escrever `spec.md`; essa responsabilidade é da skill specify.

## Como pedir

Com um arquivo de backlog:

```text
Use $specsfy-base-interview para aprofundar
specs/backlog/0003-idioma-da-interface.md.
```

Com texto livre:

```text
Use $specsfy-base-interview para me ajudar a definir uma recuperação de senha.
```

## Exemplo passo a passo

1. O agente resume: “pessoas sem acesso à senha precisam recuperar a conta”.
2. Ele pergunta: “como a pessoa comprova que controla a conta?”.
3. Você responde: “por um link enviado ao e-mail cadastrado”.
4. Ele pergunta sobre expiração, mensagens de erro e privacidade.
5. Ao terminar, entrega:

```text
Brief pronto para especificar:
- ator: pessoa com conta existente;
- resultado: receber um link temporário;
- limite: não revelar se o e-mail existe;
- aberto: duração do link.
```

Se uma decisão material continuar aberta, a entrevista não finge que a
definição está pronta.

## O que esperar

- perguntas adaptadas ao seu caso;
- uma lacuna importante por vez;
- distinção entre fato, hipótese e decisão;
- exemplos de sucesso e falha;
- um brief pronto para a próxima etapa.

## Erros comuns

- responder todas as categorias como um formulário fixo;
- decidir algo importante no lugar da pessoa responsável;
- esconder uma dúvida para acelerar;
- criar arquivos normativos durante a entrevista.

## Próximo passo

Use [`specsfy-base-specify`](specsfy-base-specify.md) para criar a especificação.
Se a conversa mostrar que a ideia ainda é superficial, volte ao
[`specsfy-base-backlog`](specsfy-base-backlog.md).

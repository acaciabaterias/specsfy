# Guardar uma ideia com `specsfy-base-backlog`

Esta skill preserva uma ideia sem exigir todas as respostas agora. Ela conversa
de forma leve, procura itens parecidos e cria ou atualiza um arquivo em
`specs/backlog/`.

## Quando usar

Use quando você disser “anote isso para depois”, trouxer um problema ainda
vago ou quiser avaliar uma oportunidade antes de criar uma especificação.

Não use para planejar tarefas, escrever testes ou iniciar código.

## Como pedir

Você pode escrever naturalmente:

```text
Use $specsfy-base-backlog para guardar esta ideia:
permitir que a pessoa escolha o idioma da interface.
```

Também pode informar contexto:

```text
Anote no backlog: clientes internacionais não entendem os e-mails atuais.
Ainda não decidimos quais idiomas serão oferecidos.
```

## Exemplo passo a passo

1. Você apresenta a ideia.
2. O agente procura itens semelhantes em `specs/backlog/` e nas specs.
3. Ele pergunta somente o necessário para diferenciar a ideia.
4. Você responde: “o problema afeta e-mails e a interface”.
5. A skill cria:

```text
specs/backlog/0003-idioma-da-interface.md
```

O item registra problema, público, resultado esperado e dúvidas abertas. Ele
continua sendo uma ideia; não autoriza implementação.

## O que esperar

- poucas perguntas;
- preservação das suas palavras;
- indicação de duplicatas ou relações;
- um caminho claro para retomar depois;
- nenhuma `spec.md` criada automaticamente sem promoção.

## Erros comuns

- transformar o backlog em uma especificação completa;
- inventar solução técnica quando o problema ainda está aberto;
- criar um segundo item sem procurar duplicatas;
- tratar o item como aprovação para implementar.

## Próximo passo

Quando quiser aprofundar a ideia, use
[`specsfy-base-interview`](specsfy-base-interview.md). Se ela já estiver clara,
você pode promovê-la com
[`specsfy-base-specify`](specsfy-base-specify.md).

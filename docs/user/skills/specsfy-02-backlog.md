# Refinar uma entrada com `specsfy-02-backlog`

Esta skill transforma uma entrada da Inbox em backlog refinável. Ela procura
itens parecidos, registra o contexto inicial e, quando necessário, conduz uma
pergunta prioritária por vez até produzir um brief pronto para especificar.

## Quando usar

Use quando quiser organizar uma captura em `specs/inbox/`, avaliar uma
oportunidade ou fechar lacunas sobre público, finalidade, regras, limites,
privacidade, falhas e resultado esperado. Para apenas salvar sem perguntas,
use `specsfy-01-inbox`.

Não use para planejar tarefas, escrever testes ou iniciar código, pois um item
de backlog ainda não passou pelos gates que autorizam essas etapas.

## Como descrever a tarefa

Descreva a entrada e o destino esperado na mesma mensagem. A skill usará esse
texto para criar um item reconhecível em `specs/backlog/`, sem tratá-lo como
autorização para implementar. Por exemplo:

```text
Use $specsfy-02-backlog para refinar esta entrada:
permitir que a pessoa escolha o idioma da interface.
```

Quando houver itens parecidos em `specs/backlog/`, inclua a situação que
diferencia esta entrada das demais. Isso ajuda a skill a atualizar o item correto
e a manter visíveis as definições que continuam abertas:

```text
Anote no backlog: clientes internacionais não entendem os e-mails atuais.
Ainda não decidimos quais idiomas serão oferecidos.
```

## Exemplo passo a passo

1. Você apresenta a entrada ou aponta o arquivo da Inbox.
2. O agente também pode ler a origem em `specs/inbox/`.
3. Ele procura itens semelhantes em `specs/backlog/` e nas specs.
4. Ele pergunta uma lacuna material por vez.
5. Você responde: “o problema afeta e-mails e a interface”.
6. A skill cria o item com `.specsfy/templates/custom/Backlog.md` quando
   presente ou com `.specsfy/templates/Backlog.md`:

```text
specs/backlog/0003-idioma-da-interface.md
```

O item registra problema, público, resultado esperado e dúvidas abertas. Ele
continua sendo backlog e não autoriza implementação.

## Como o ciclo termina

O refinamento funciona sem limite máximo de perguntas. A cada resposta, o
agente reconsidera o pedido original, o contexto acumulado e a nova resposta.
Ele continua enquanto existir uma lacuna aplicável, sem seguir uma lista fixa.

A partir da 11ª pergunta, cada rodada também oferece `avançar`. Essa opção
permite encerrar o ciclo atual mesmo com decisões abertas. Nesse caso, o brief
lista as lacunas, a spec permanece `Status: Draft` e o
`Definition Gate: Pending`; avançar não equivale a aprovar a definição.

## O que esperar

- perguntas adaptadas ao caso, uma lacuna importante por vez.
- preservação das suas palavras.
- indicação de duplicatas ou relações.
- distinção entre fato, hipótese e escolha confirmada.
- um brief pronto para especificar.
- um caminho claro para retomar depois.
- nenhuma `spec.md` criada automaticamente sem promoção.

## Erros comuns

- transformar o backlog em uma especificação completa.
- inventar solução técnica quando o problema ainda está aberto.
- criar um segundo item sem procurar duplicatas.
- tratar o item como aprovação para implementar.
- responder categorias como um formulário fixo.
- esconder uma dúvida para encurtar a conversa.

## Próximo passo

Quando o backlog estiver claro, use
[`specsfy-03-specify`](specsfy-03-specify.md). Se ainda houver uma decisão
material aberta, continue o ciclo nesta mesma skill.

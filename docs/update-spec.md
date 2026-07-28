# Atualizar uma especificação

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | pedidos surgidos depois da definição inicial de uma spec |
| Autoridade | uso público de `specsfy-base-update-spec` |

## Papel

Permitir que uma pessoa adicione, remova, corrija ou mude um pedido sem conhecer
os atos internos do Specsfy e sem deixar código, testes e tarefas divergirem da
especificação.

## Como usar

Quando lembrar de algo durante ou depois da implementação, diga diretamente o
que mudou. Use esta entrada para adicionar, remover, corrigir ou mudar um
pedido:

```text
Use $specsfy-base-update-spec em
specs/specs/0001-pagina-boas-vindas/spec.md:
esqueci de pedir que o nome tenha no máximo 80 caracteres.
```

Também funcionam pedidos naturais como:

```text
Quero adicionar uma regra à especificação atual.
Remova o comportamento de visitante.
Corrija o que acontece quando o nome estiver vazio.
Mude esta entrega para exigir autenticação.
```

A skill preserva o pedido, compara-o com a spec existente e informa primeiro o
resultado prático. Você não precisa escolher manualmente qual gate ou etapa
reabrir.

## O que acontece

| Tipo do pedido | Tratamento |
| --- | --- |
| correção interna sem efeito observável | mantém a spec e registra a avaliação na evidência |
| esclarecimento sem mudança de significado | ajusta a redação sem invalidar gates |
| comportamento, aceite, escopo, dados ou segurança | atualiza a mesma spec e reabre desde o Ato I |
| solução, tarefas ou estratégia de testes | atualiza a mesma spec e reabre desde o Ato II |
| capacidade independente | preserva a spec atual e encaminha o pedido para backlog ou nova spec |
| decisão material ausente | faz uma pergunta objetiva e retoma a atualização depois da resposta |

Quando a mudança pertence à spec atual, o fluxo é automático:

```text
pedido tardio → update-spec → validate ou tasks → TDD/BDD → implement → progress
                         ↘ interview, somente se faltar uma decisão
```

Testes e tarefas que continuam válidos são preservados. Provas dependentes do
comportamento anterior voltam a ficar pendentes; a implementação só é retomada
depois de existir novo RED válido e os gates necessários voltarem a `Passed`.

## Resultado esperado

- o pedido novo está incorporado à única `spec.md` normativa;
- IDs e decisões ainda válidos foram preservados;
- os gates afetados foram reabertos;
- validação, tarefas e testes foram reconciliados;
- a etapa que recebeu o pedido foi retomada automaticamente.

## Limites

- não cria `change-request.md`, `plan.md`, `tasks.md` ou outra fonte paralela;
- não transforma uma capacidade independente em aumento silencioso de escopo;
- não inventa uma decisão material;
- não altera código antes de atualizar a spec e preparar novo RED;
- handoffs automáticos não autorizam deploy, publicação ou ação destrutiva.

## Atualize quando

- a classificação de mudanças tardias mudar;
- a política de invalidação dos gates mudar;
- a responsabilidade ou o nome de `specsfy-base-update-spec` mudar.

## Não use para

- criar a primeira versão de uma spec;
- capturar uma ideia ainda superficial;
- editar código sem mudança normativa;
- manter histórico fora da spec.

## Fonte da verdade e precedência

A execução pertence a
[`specsfy-base-update-spec`](../skills/specsfy-base-update-spec/).
A spec atualizada permanece como única fonte normativa no projeto consumidor.

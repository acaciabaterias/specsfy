# Skills base

<!-- markdownlint-disable MD033 -->
<p align="center">
  <picture>
    <source srcset="../../../brand/logo/icon.svg" type="image/svg+xml">
    <img src="../../../brand/logo/icon.png" alt="Logo do Specsfy" width="128">
  </picture>
</p>
<!-- markdownlint-enable MD033 -->

As skills base dividem o método por responsabilidade. Você pode chamar uma
delas pelo nome ou explicar o resultado esperado. O agente lê o estado da spec,
seleciona a etapa responsável e anuncia cada transição necessária.

| Etapa | Skill | Resultado principal |
| --- | --- | --- |
| capturar sem perguntas | [`specsfy-01-inbox`](specsfy-01-inbox.md) | arquivo em `specs/inbox/` |
| refinar uma entrada e aprofundar definições | [`specsfy-02-backlog`](specsfy-02-backlog.md) | item em `specs/backlog/` e brief na conversa |
| criar a fonte única | [`specsfy-03-specify`](specsfy-03-specify.md) | `spec.md` |
| revisar definição | [`specsfy-04-validate`](specsfy-04-validate.md) | Definition Gate confiável |
| decompor o plano | [`specsfy-05-tasks`](specsfy-05-tasks.md) | tarefas dentro da spec |
| preparar e executar testes | [`specsfy-06-tdd-bdd`](specsfy-06-tdd-bdd.md) | RED/GREEN rastreável |
| produzir a mudança | [`specsfy-07-implement`](specsfy-07-implement.md) | código, testes e evidência |
| incorporar mudança posterior | [`specsfy-update-spec`](specsfy-update-spec.md) | spec atualizada e gates reabertos |
| consultar o estado | [`specsfy-progress`](specsfy-progress.md) | relatório somente leitura |

## Encontre a skill pelo estado do trabalho

Uma anotação que precisa ser preservada vai para `specsfy-01-inbox`. Quando
você quiser comparar essa ideia com itens existentes e esclarecer o mínimo
necessário, `specsfy-02-backlog` cria ou atualiza o arquivo numerado e
aprofunda as definições que mudam o comportamento e
entrega um brief na conversa.

Com a intenção de criar uma entrega confirmada,
`specsfy-03-specify` monta a `spec.md` e `specsfy-04-validate` comprova o
Ato I. A skill `specsfy-05-tasks` organiza o plano, chama
`specsfy-06-tdd-bdd` para materializar os testes e só aprova o Plan Gate
depois de um RED válido. `specsfy-07-implement` executa as tarefas com
evidência e documentação atualizada.

Uma necessidade surgida depois da definição retorna à mesma spec por
`specsfy-update-spec`. Para apenas consultar gates, tarefas e o próximo
trabalho sem alterar arquivos, use `specsfy-progress`.

Volte ao [guia completo](../README.md) ou leia [como a metodologia
funciona](../method.md).

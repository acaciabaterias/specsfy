# Skills base

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../../brand/logo/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../../../brand/logo/logo-light.svg">
    <img src="../../../brand/logo/logo-light.svg" alt="Logo oficial do Specsfy" width="180">
  </picture>
</p>

As skills base dividem o método em responsabilidades pequenas. Você pode pedir
uma delas pelo nome ou simplesmente explicar o que quer; o agente seleciona e
encadeia as etapas necessárias.

| Etapa | Skill | Resultado principal |
| --- | --- | --- |
| capturar sem perguntas | [`specsfy-base-idea`](specsfy-base-idea.md) | arquivo em `specs/ideias/` |
| guardar uma ideia | [`specsfy-base-backlog`](specsfy-base-backlog.md) | item em `specs/backlog/` |
| aprofundar decisões | [`specsfy-base-interview`](specsfy-base-interview.md) | brief na conversa |
| criar a fonte única | [`specsfy-base-specify`](specsfy-base-specify.md) | `spec.md` |
| revisar definição | [`specsfy-base-validate`](specsfy-base-validate.md) | Definition Gate confiável |
| decompor o plano | [`specsfy-base-tasks`](specsfy-base-tasks.md) | tarefas dentro da spec |
| preparar e executar testes | [`specsfy-base-tdd-bdd`](specsfy-base-tdd-bdd.md) | RED/GREEN rastreável |
| produzir a mudança | [`specsfy-base-implement`](specsfy-base-implement.md) | código, testes e evidência |
| incorporar pedido tardio | [`specsfy-base-update-spec`](specsfy-base-update-spec.md) | spec atualizada e gates reabertos |
| consultar o estado | [`specsfy-base-progress`](specsfy-base-progress.md) | relatório somente leitura |

## Como escolher

- Quer apenas guardar o texto agora? Comece pela captura de ideia.
- Quer refinar uma captura vaga? Use o backlog.
- Você quer decidir detalhes antes de criar uma spec? Use a entrevista.
- A entrega está clara, mas ainda não possui `spec.md`? Use specify.
- Quer saber se a definição está pronta? Use validate.
- A definição está aprovada e precisa virar passos executáveis? Use tasks.
- Precisa criar ou comprovar testes? Use TDD/BDD.
- O plano está aprovado e há tarefa pronta? Use implement.
- O pedido mudou depois da definição? Use update-spec.
- Quer apenas saber quanto falta? Use progress.

Volte ao [guia completo](../README.md) ou leia [como a metodologia
funciona](../method.md).

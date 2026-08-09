# Metodologia executável

Este documento descreve o contrato técnico do Specsfy para quem altera o
framework. A fonte executável principal vive em `skills/Spec.md`, no template,
nos validadores e nas skills. Este texto oferece contexto, não redefine esses
artefatos.

## Unidade normativa

Em um projeto consumidor, cada fatia usa:

```text
specs/<estado>/<NNNN>-<slug>/spec.md
```

O formato atual é `Specsfy/2.0`. O pacote pode conter `research/` para
evidências externas indexadas, mas somente `spec.md` é normativo. `plan.md`,
`tasks.md`, `research.md` e `data-model.md` são proibidos porque criariam
fontes concorrentes.

## Estados

```text
Draft → Defined → Planned → Implementing → Reviewing → Complete
```

- `Draft`: definição em construção.
- `Defined`: Definition Gate aprovado.
- `Planned`: Plan Gate aprovado e RED comprovado.
- `Implementing`: tarefas de produção em andamento.
- `Reviewing`: entrega implementada, aguardando aceite final.
- `Complete`: Delivery Gate aprovado.

As pastas seguem a mesma ordem: `draft`, `defined`, `planned`,
`in-progress`, `review` e `completed`. `specsfy transition` move o pacote e
sincroniza o campo `Status`; `specsfy migrate` converte o layout anterior.

`Effort` é inteiro de 1 a 10, acompanhado de data e justificativa. O
entrevistador recalibra a estimativa quando novas informações alteram a
capacidade de execução exigida. Quando ClickUpfy está instalado e `ClickUp
Task` existe na spec, a skill da etapa sincroniza a projeção remota.

Transições não são meras etiquetas. Cada uma depende da evidência registrada na
spec e nos testes.

## Ato I — Definir

Antes do Ato I, a entrada possui duas camadas não normativas:

```text
input → specs/inbox/ → specs/backlog/
```

`specsfy-01-inbox` preserva e pré-processa sem perguntas. O backlog adiciona
refinamento dialogado. Ambas mantêm proveniência, mas somente `spec.md` governa
o comportamento.

O refinamento do backlog concentra as decisões materiais. Depois de cada resposta, ele
recalcula as lacunas usando a entrada original, o contexto acumulado e a nova
resposta. Não existe teto de perguntas: o ciclo termina ao fechar as lacunas
aplicáveis ou quando a pessoa escolhe `avançar`, opção disponível da 11ª
pergunta em diante. Essa saída mantém a definição em Draft e o gate pendente.

Responsabilidades:

- descobrir finalidade, atores, linguagem e limites.
- separar declaração, inferência, hipótese e decisão.
- produzir histórias, `FR`, `NFR`, critérios e Gherkin.
- indexar research sem promovê-lo automaticamente.
- validar formato, clareza, completude, consistência e testabilidade.

Skills principais:

```text
specsfy-01-inbox
specsfy-02-backlog
specsfy-03-specify
specsfy-04-validate
```

Saída:

```text
Definition Gate: Passed
Status: Defined
```

## Ato II — Projetar e provar

Responsabilidades:

- escolher abordagem compatível com o código observado.
- modelar contratos, dados, riscos e rollback.
- decompor tarefas pequenas e ordenadas.
- materializar casos TDD derivados dos critérios.
- observar RED válido antes de produção.

Skills principais:

```text
specsfy-05-tasks
specsfy-06-tdd-bdd (modo prepare)
```

Saída:

```text
Plan Gate: Passed
Status: Planned
```

Erro de ambiente, dependência ausente ou fixture inválida não é RED de
comportamento.

## Ato III — Entregar e validar

Cada tarefa executa:

```text
RED → GREEN → REFACTOR
```

`specsfy-07-implement` exige predecessoras TDD e gates válidos. Depois do
GREEN focal, executa regressão proporcional ao risco, atualiza evidências e
aciona `specsfy-documentator` quando código ou persistência mudam.

Saída final:

```text
Delivery Gate: Passed
Status: Reviewing
```

`specsfy-04-validate` confirma o aceite em `review/` e conclui a transição para
`completed/`.

## Cobertura e rastreabilidade

Cada feature, `US`, `FR` e `NFR` possui pelo menos três cenários BDD distintos.
Cada critério possui caso TDD, e os casos executáveis declaram marcadores
`SPECSFY:` junto à definição do teste.

O Gherkin permanece dentro da spec como linguagem de descoberta e referência.
A suíte normal do projeto contém a prova executável. Não se cria uma segunda
árvore `.feature` no consumidor.

## Mudança tardia

`specsfy-update-spec` preserva o novo pedido, calcula o impacto e invalida
somente o necessário:

| Mudança | Reabre |
| --- | --- |
| comportamento, escopo ou aceite | Atos I–III |
| plano, tarefa ou abordagem | Atos II–III |
| evidência sem mudança normativa | validações afetadas do Ato III |

Depois da correção, a orquestração retoma a etapa original.

## Orquestração e handoff

As skills anunciam pendências, transições e retomadas. Um handoff transfere a
responsabilidade, não o contexto normativo. A skill de destino lê novamente a
spec e as evidências necessárias.

O fluxo evita confirmação artificial entre etapas, mas não elimina autorização
para ações sensíveis como push, deploy, exclusão ou alteração externa.

## Projeções

CLI, TUI e `specsfy-progress` projetam o estado observado nas specs. Eles
não mantêm uma fonte paralela de progresso e não podem aprovar gates.

Milestones são estados demonstráveis de produto e ficam em
`specs/milestones/MNN.md`. Specs e backlog declaram relações no campo
`Milestones`; `specs.md` é uma projeção derivada mantida por
`specsfy milestones sync --project .`. O percentual considera apenas specs
`Complete`, enquanto a condição de saída do marco exige validação humana.

## Ao modificar a metodologia

Uma alteração em estado, gate, formato ou handoff normalmente exige mudanças
coordenadas em:

- `skills/Spec.md`, template e exemplo.
- skills responsáveis e suas referências.
- validadores e testes de `skills/`.
- instalador ou projeção do `cli/`, quando aplicável.
- documentação em `docs/user/` e `docs/develop/`.
- contratos integrados em `tests/`.

Siga [Contribuir](contributing.md) antes de editar.

# Metodologia executável

Este documento descreve o contrato técnico do Specsfy para quem altera o
framework. A fonte executável principal vive em `skills/Spec.md`, no template,
nos validadores e nas skills. Este texto oferece contexto, não redefine esses
artefatos.

## Unidade normativa

Em um projeto consumidor, cada fatia usa:

```text
specs/specs/<NNNN>-<slug>/spec.md
```

O formato atual é `Specsfy/2.0`. O pacote pode conter `research/` para
evidências externas indexadas, mas somente `spec.md` é normativo. `plan.md`,
`tasks.md`, `research.md` e `data-model.md` são proibidos porque criariam
fontes concorrentes.

## Estados

```text
Draft → Defined → Planned → Implementing → Complete
```

- `Draft`: definição em construção;
- `Defined`: Definition Gate aprovado;
- `Planned`: Plan Gate aprovado e RED comprovado;
- `Implementing`: tarefas de produção em andamento;
- `Complete`: Delivery Gate aprovado.

Transições não são meras etiquetas. Cada uma depende da evidência registrada na
spec e nos testes.

## Ato I — Definir

Antes do Ato I, a entrada possui duas camadas não normativas:

```text
input → specs/ideias/ → specs/backlog/
```

`specsfy-base-idea` preserva e pré-processa sem perguntas. O backlog adiciona
refinamento dialogado. Ambas mantêm proveniência, mas somente `spec.md` governa
o comportamento.

Responsabilidades:

- descobrir finalidade, atores, linguagem e limites;
- separar declaração, inferência, hipótese e decisão;
- produzir histórias, `FR`, `NFR`, critérios e Gherkin;
- indexar research sem promovê-lo automaticamente;
- validar formato, clareza, completude, consistência e testabilidade.

Skills principais:

```text
specsfy-base-idea
specsfy-base-backlog
specsfy-base-interview
specsfy-base-specify
specsfy-base-validate
```

Saída:

```text
Definition Gate: Passed
Status: Defined
```

## Ato II — Projetar e provar

Responsabilidades:

- escolher abordagem compatível com o código observado;
- modelar contratos, dados, riscos e rollback;
- decompor tarefas pequenas e ordenadas;
- materializar casos TDD derivados dos critérios;
- observar RED válido antes de produção.

Skills principais:

```text
specsfy-base-tasks
specsfy-base-tdd-bdd (modo prepare)
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

`specsfy-base-implement` exige predecessoras TDD e gates válidos. Depois do
GREEN focal, executa regressão proporcional ao risco, atualiza evidências e
aciona `specsfy-documentator` quando código ou persistência mudam.

Saída final:

```text
Delivery Gate: Passed
Status: Complete
```

## Cobertura e rastreabilidade

Cada feature, `US`, `FR` e `NFR` possui pelo menos três cenários BDD distintos.
Cada critério possui caso TDD, e os casos executáveis declaram marcadores
`SPECSFY:` junto à definição do teste.

O Gherkin permanece dentro da spec como linguagem de descoberta e referência.
A suíte normal do projeto contém a prova executável. Não se cria uma segunda
árvore `.feature` no consumidor.

## Mudança tardia

`specsfy-base-update-spec` preserva o novo pedido, calcula o impacto e invalida
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

CLI, TUI e `specsfy-base-progress` projetam o estado observado nas specs. Eles
não mantêm uma fonte paralela de progresso e não podem aprovar gates.

## Ao modificar a metodologia

Uma alteração em estado, gate, formato ou handoff normalmente exige mudanças
coordenadas em:

- `skills/Spec.md`, template e exemplo;
- skills responsáveis e suas referências;
- validadores e testes de `skills/`;
- instalador ou projeção do `cli/`, quando aplicável;
- documentação em `docs/user/` e `docs/develop/`;
- contratos integrados em `tests/`.

Siga [Contribuir](contributing.md) antes de editar.

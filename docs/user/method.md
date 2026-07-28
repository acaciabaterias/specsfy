# Como a metodologia funciona

O Specsfy organiza uma entrega do começo ao fim. A meta é simples: todo mundo
consulta a mesma definição, e cada avanço possui uma prova atual.

## Uma única especificação

Cada entrega usa:

```text
specs/specs/<NNNN>-<slug>/spec.md
```

`NNNN` é um número, como `0001`. O `slug` é um nome curto, como
`recuperar-senha`.

Dentro de `spec.md` ficam:

- o problema e o resultado esperado;
- histórias e requisitos;
- exemplos de comportamento;
- decisões e plano técnico;
- testes e evidências;
- tarefas e estado da entrega.

Arquivos como `plan.md` e `tasks.md` não são usados. Assim, a equipe não precisa
descobrir qual documento está atualizado.

## Ideia, spec e código

Uma ideia pode passar por três estados fáceis de reconhecer:

```text
ideia capturada → ideia no backlog → spec definida → código entregue
```

`specs/ideias/` recebe o texto sem perguntas. O backlog serve para algo ainda
aberto que será refinado. A spec serve para uma entrega escolhida.
O código só começa quando definição, plano e testes estão prontos.

## Os três atos

### Ato I — Definir

O agente entende quem precisa da mudança, qual problema será resolvido, quais
regras importam e como reconhecer o sucesso.

O ato termina com:

```text
Definition Gate: Passed
```

Esse gate significa “a definição está clara o suficiente para planejar”. Não
significa que o código está pronto.

### Ato II — Projetar e provar

O agente escolhe a abordagem, organiza tarefas e cria testes derivados dos
exemplos de comportamento. Pelo menos um teste precisa falhar pela ausência da
mudança. Essa prova é chamada de RED.

O ato termina com:

```text
Plan Gate: Passed
```

### Ato III — Entregar e validar

O agente implementa uma tarefa por vez:

```text
RED → GREEN → REFACTOR
```

- **RED:** o teste falha pela razão esperada;
- **GREEN:** a menor implementação faz o teste passar;
- **REFACTOR:** o código é melhorado sem mudar o comportamento.

Depois da regressão completa e da documentação, o ato termina com:

```text
Delivery Gate: Passed
Status: Complete
```

## BDD e TDD sem complicação

BDD descreve um comportamento por exemplo:

```gherkin
Cenário: pessoa solicita recuperação de senha
  Dado que existe uma conta para o e-mail informado
  Quando a pessoa solicita a recuperação
  Então o sistema confirma o pedido sem revelar dados privados
```

TDD transforma esse exemplo em um teste executável. O Gherkin ajuda pessoas e
agentes a entenderem a regra; o teste comprova que o sistema a cumpre.

## Mudanças durante o trabalho

Você pode corrigir, adicionar ou remover um pedido a qualquer momento. A
mudança entra na mesma `spec.md`. O Specsfy reabre somente o que perdeu
validade:

- mudou o comportamento: volta à definição, ao plano e à entrega;
- mudou somente o plano: volta ao plano e à entrega;
- mudou apenas uma evidência: repete a validação necessária.

Use [`specsfy-base-update-spec`](skills/specsfy-base-update-spec.md) para esse
fluxo.

## Skills base

As dez skills formam a jornada principal:

1. [`specsfy-base-idea`](skills/specsfy-base-idea.md);
2. [`specsfy-base-backlog`](skills/specsfy-base-backlog.md);
3. [`specsfy-base-interview`](skills/specsfy-base-interview.md);
4. [`specsfy-base-specify`](skills/specsfy-base-specify.md);
5. [`specsfy-base-validate`](skills/specsfy-base-validate.md);
6. [`specsfy-base-tasks`](skills/specsfy-base-tasks.md);
7. [`specsfy-base-tdd-bdd`](skills/specsfy-base-tdd-bdd.md);
8. [`specsfy-base-implement`](skills/specsfy-base-implement.md);
9. [`specsfy-base-update-spec`](skills/specsfy-base-update-spec.md);
10. [`specsfy-base-progress`](skills/specsfy-base-progress.md).

As transições são automáticas. Você pode começar com uma intenção comum, como
“implemente esta melhoria”; o agente verifica as etapas necessárias antes de
alterar produção.

## O que o método não faz

- não decide requisitos importantes sem você;
- não trata pesquisa como requisito aprovado;
- não considera erro de ambiente como RED válido;
- não substitui os testes e ferramentas do seu projeto;
- não garante qualidade sem evidência atual;
- não transforma toda ideia em uma spec.

Para experimentar, siga o [primeiro projeto](getting-started.md).

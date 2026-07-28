# Planejar tarefas com `specsfy-base-tasks`

Esta skill transforma uma definição aprovada em tarefas pequenas, ordenadas e
verificáveis. As tarefas ficam na seção 14 da própria `spec.md`.

## Quando usar

Use depois do Definition Gate ou quando uma alteração exigir replanejamento.
Não use para escrever código nem para marcar uma tarefa como concluída.

## Como pedir

```text
Use $specsfy-base-tasks em
specs/specs/0004-recuperar-senha/spec.md.
```

Você também pode pedir uma fatia:

```text
Prepare as tarefas da primeira fatia vertical da spec 0004.
```

## Exemplo passo a passo

1. A skill lê a spec e o código existente.
2. Identifica a menor entrega observável: solicitar o link.
3. Liga cada tarefa aos requisitos e critérios correspondentes.
4. Declara predecessoras de teste antes da tarefa de produção.
5. Registra:

```text
T001 [ ] Criar caso TDD para solicitação válida — cobre AC-001
T002 [ ] Criar caso TDD para e-mail desconhecido — cobre AC-002
T003 [ ] Implementar solicitação sem revelar existência da conta
```

6. Confirma que dependências, rollback e validações estão claros antes de
aprovar o Plan Gate.

## O que esperar

- tarefas pequenas e com resultado verificável;
- ordem explícita de dependência;
- testes antes de produção;
- caminhos e comandos reais do projeto;
- tarefas mantidas dentro da fonte única.

## Erros comuns

- criar `tasks.md`;
- escrever tarefas vagas como “fazer backend”;
- colocar várias mudanças independentes em uma tarefa;
- planejar sem inspecionar a stack real;
- marcar uma tarefa pronta sem evidência.

## Próximo passo

Use [`specsfy-base-tdd-bdd`](specsfy-base-tdd-bdd.md) em modo `prepare` para
materializar o próximo teste e observar RED.

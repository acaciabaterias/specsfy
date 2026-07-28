# Incorporar mudanças com `specsfy-base-update-spec`

Esta skill atualiza uma spec que já foi definida, planejada, iniciada ou
concluída. O pedido novo entra na mesma fonte, e somente os atos afetados são
reabertos.

## Quando usar

Use quando você disser “esqueci”, “adicione”, “remova”, “corrija” ou “mude”
algo de uma entrega existente.

Para criar a primeira versão da spec, use specify.

## Como pedir

```text
Use $specsfy-base-update-spec para adicionar expiração de 30 minutos à
specs/specs/0004-recuperar-senha/spec.md.
```

Você também pode pedir uma remoção:

```text
Remova a exigência de SMS da spec 0004 e ajuste o trabalho afetado.
```

## Exemplo passo a passo

1. A skill preserva literalmente o pedido novo.
2. Lê requisitos, testes, tarefas, gates e evidências atuais.
3. Classifica a mudança:

```text
Mudança de definição: altera comportamento e critério de aceite.
Atos reabertos: I, II e III.
```

4. Atualiza a mesma `spec.md`.
5. Invalida apenas os gates que perderam validade.
6. Retoma entrevista, validação, tarefas, testes e implementação na ordem
necessária.
7. Registra a nova evidência sem apagar o histórico relevante.

## O que esperar

- pedido original preservado;
- impacto explicado antes da retomada;
- nenhuma spec duplicada;
- trabalho já válido mantido;
- transições automáticas até o estado coerente.

## Erros comuns

- editar apenas o código e deixar a spec antiga;
- reabrir todos os gates sem analisar impacto;
- manter teste ou tarefa que contradiz o pedido novo;
- esconder a mudança em notas soltas;
- criar uma segunda especificação para a mesma entrega.

## Próximo passo

A própria skill encaminha para a etapa reaberta. Depois da atualização, use
[`specsfy-base-progress`](specsfy-base-progress.md) para revisar o estado geral.

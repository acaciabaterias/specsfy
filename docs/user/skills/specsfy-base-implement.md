# Entregar código com `specsfy-base-implement`

Esta skill executa as tarefas aprovadas da spec em ordem. Ela altera produção
somente quando existe um plano válido e um teste focal em RED.

## Quando usar

Use para implementar a próxima tarefa pronta, continuar uma entrega ou concluir
uma feature planejada. Não use para pular definição, planejamento ou testes.

## Como pedir

```text
Use $specsfy-base-implement para executar a próxima tarefa pronta de
specs/specs/0004-recuperar-senha/spec.md.
```

Ou indique uma tarefa:

```text
Implemente T003 da spec 0004 e valide a regressão.
```

## Exemplo passo a passo

1. A skill confirma Definition Gate e Plan Gate aprovados.
2. Verifica a tarefa predecessora e o RED atual.
3. Faz a menor mudança de produção.
4. Executa o teste focal até obter GREEN.
5. Refatora sem alterar o comportamento.
6. Executa a regressão e atualiza evidências:

```text
T003 [x] Implementar solicitação sem revelar existência da conta
Teste focal: passou
Regressão: passou
```

7. Ao concluir a entrega, chama o documentador do projeto consumidor.

## O que esperar

- uma tarefa por vez;
- mudanças limitadas ao escopo aprovado;
- testes focais e regressão;
- documentação aplicável atualizada;
- status e checkboxes sustentados por evidência.

## Erros comuns

- implementar com gate pendente;
- aceitar um RED causado por dependência ausente;
- ampliar o escopo sem atualizar a spec;
- marcar conclusão antes da regressão;
- esquecer documentação ou contexto afetado.

## Próximo passo

Continue com a próxima tarefa ou consulte
[`specsfy-base-progress`](specsfy-base-progress.md). Se surgir um pedido novo,
use [`specsfy-base-update-spec`](specsfy-base-update-spec.md).

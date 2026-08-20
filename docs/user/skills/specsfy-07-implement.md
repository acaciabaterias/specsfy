# Entregar código com `specsfy-07-implement`

Esta skill executa as tarefas aprovadas da spec em ordem. Ela altera produção
somente quando existe um plano válido e um teste focal em RED.

## Quando usar

Use para implementar a próxima tarefa pronta, continuar uma entrega ou concluir
uma feature planejada. Não use para pular definição, planejamento ou testes.

Quando uma autorização ou escolha for necessária, a skill apresenta exatamente
uma pergunta numerada. Ela contém três ou mais respostas sugeridas, `Escrever
outra resposta`, `Gere outras opções` e `Avançar` desde a primeira rodada.

## Como descrever a tarefa

```text
Use $specsfy-07-implement para executar a próxima tarefa pronta de
specs/<estado>/0004-recuperar-senha/spec.md.
```

Quando houver mais de uma tarefa pronta, indique o ID da tarefa que deve ser
executada:

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
T003 [x] Implementar solicitação sem revelar existência do cadastro
Teste focal: passou
Regressão: passou
```

Depois de cada tarefa de código, a skill chama o documentador do projeto
consumidor. A execução só continua quando `docs/` estiver atualizado.

## O que esperar

- uma tarefa por vez.
- mudanças limitadas ao escopo aprovado.
- testes focais e regressão.
- documentação aplicável atualizada.
- status e checkboxes comprovados por evidência.

## Erros comuns

- implementar com gate pendente.
- aceitar um RED causado por dependência ausente.
- ampliar o escopo sem atualizar a spec.
- marcar conclusão sem regressão.
- deixar `docs/`, `PROJECT.md` ou os arquivos `.specsfy/` incompatíveis com o
  código alterado.

## Próximo passo

Continue com a próxima tarefa ou consulte
[`specsfy-progress`](specsfy-progress.md). Se surgir uma necessidade
nova, use [`specsfy-update-spec`](specsfy-update-spec.md).

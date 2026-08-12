# Preparar testes com `specsfy-06-tdd-bdd`

Esta skill usa os cenários da spec para criar testes executáveis. Ela mantém a
rastreabilidade entre o comportamento descrito e a prova no código.

## Quando usar

Use para preparar o RED que autoriza a implementação, executar um ciclo
RED–GREEN–REFACTOR ou verificar testes e rastreabilidade.

Se precisar escolher runner, comando ou caso focal, a skill apresenta pelo
menos três perguntas numeradas. Cada uma contém três ou mais respostas
sugeridas, `Escrever outra resposta` e `Avançar` desde a primeira rodada.

## Como descrever a tarefa

Para preparar o próximo teste focal e produzir a evidência de RED, use o modo
`prepare`:

```text
Use $specsfy-06-tdd-bdd em modo prepare para
specs/<estado>/0004-recuperar-senha/spec.md.
```

Para conferir os testes e a rastreabilidade de uma entrega existente, use o
modo `verify`:

```text
Use $specsfy-06-tdd-bdd em modo verify na spec 0004.
```

## Exemplo passo a passo

1. A skill seleciona a próxima condição de aceite.
2. Encontra o runner real do projeto.
3. Cria um teste com marcador de rastreabilidade.
4. Executa somente o teste focal.
5. Confirma:

```text
RED válido: o teste falhou porque a recuperação ainda não foi implementada.
Caso: TDD-AC-001
```

Depois da implementação, a skill repete o teste focal e executa a regressão
para confirmar que o comportamento ficou GREEN sem quebrar o restante.

O bloco Gherkin da spec é uma referência legível. A prova automatizada fica na
suíte normal do projeto, não em um arquivo `.feature` nem em uma segunda suíte.

## O que esperar

- caso de teste ligado a uma condição de aceite da spec.
- comando e resultado registrados.
- distinção entre falha esperada e problema de ambiente.
- cobertura de sucesso, regra e limite.
- regressão depois do GREEN.

## Erros comuns

- chamar erro de configuração de RED.
- escrever produção no modo `prepare`.
- criar testes que não correspondem às condições de aceite.
- considerar o Gherkin sozinho como teste executado.
- aprovar o plano sem prova focal.

## Próximo passo

Com RED válido e tarefa pronta, use
[`specsfy-07-implement`](specsfy-07-implement.md). Para apenas reorganizar
as tarefas, volte a [`specsfy-05-tasks`](specsfy-05-tasks.md).

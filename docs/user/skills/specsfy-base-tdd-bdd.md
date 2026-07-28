# Preparar testes com `specsfy-base-tdd-bdd`

Esta skill usa os cenários da spec para criar testes executáveis. Ela mantém a
rastreabilidade entre o comportamento descrito e a prova no código.

## Quando usar

Use para preparar o RED antes da implementação, executar um ciclo
RED–GREEN–REFACTOR ou verificar testes e rastreabilidade.

## Como pedir

Antes do código:

```text
Use $specsfy-base-tdd-bdd em modo prepare para
specs/specs/0004-recuperar-senha/spec.md.
```

Para verificar uma entrega existente:

```text
Use $specsfy-base-tdd-bdd em modo verify na spec 0004.
```

## Exemplo passo a passo

1. A skill seleciona o próximo critério de aceite.
2. Encontra o runner real do projeto.
3. Cria um teste com marcador de rastreabilidade.
4. Executa somente o teste focal.
5. Confirma:

```text
RED válido: o teste falhou porque o pedido de recuperação ainda não existe.
Caso: TDD-AC-001
```

6. Depois da implementação, repete o teste e a regressão.

O arquivo Gherkin da spec é uma referência legível. A prova automatizada fica
na suíte normal do projeto, não em uma segunda suíte paralela.

## O que esperar

- caso de teste ligado a um critério da spec;
- comando e resultado registrados;
- distinção entre falha esperada e problema de ambiente;
- cobertura de sucesso, regra e limite;
- regressão depois do GREEN.

## Erros comuns

- chamar erro de configuração de RED;
- escrever produção no modo `prepare`;
- criar testes que não correspondem aos critérios;
- considerar o Gherkin sozinho como teste executado;
- aprovar o plano sem prova focal.

## Próximo passo

Com RED válido e tarefa pronta, use
[`specsfy-base-implement`](specsfy-base-implement.md). Para apenas reorganizar
as tarefas, volte a [`specsfy-base-tasks`](specsfy-base-tasks.md).

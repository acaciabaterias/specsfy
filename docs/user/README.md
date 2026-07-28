# Guia completo do usuário

O Specsfy ajuda você a transformar uma ideia em software testado sem espalhar
requisitos, planos e tarefas por vários arquivos. Você conversa normalmente
com o agente; as skills organizam o trabalho e mantêm uma única especificação
como referência.

Este guia é para quem quer **usar** o Specsfy. Você não precisa conhecer a
implementação do framework, decorar comandos internos nem entender todos os
termos antes de começar.

## Comece por aqui

| Quero… | Leia |
| --- | --- |
| preparar meu computador | [Instalação](installation.md) |
| fazer a primeira entrega | [Primeiro projeto](getting-started.md) |
| entender a Metodologia | [Como o método funciona](method.md) |
| capturar um texto sem responder perguntas | [Caixa de entrada de ideias](ideas.md) |
| organizar ideias antes de especificar | [Backlog](backlog.md) |
| conhecer cada etapa em profundidade | [Skills base](skills/README.md) |
| usar comandos e a interface visual | [CLI e TUI](cli.md) |
| registrar stack, regras e banco | [Contexto do projeto](project-context.md) |
| escolher conhecimento técnico extra | [Especialistas](specialists.md) |
| gerar documentação da minha aplicação | [Documentação do sistema](system-documentation.md) |
| corrigir ou mudar um pedido já definido | [Mudanças posteriores](update-spec.md) |
| usar opções de automação | [Uso avançado](advanced-usage.md) |
| aplicar em um projeto Laravel | [Laravel](laravel.md) |
| aplicar em um projeto Astro | [Astro](astro.md) |
| aplicar em um projeto Next.js | [Next.js](nextjs.md) |
| conhecer os módulos do monorepo | [Mapa técnico](../develop/modules.md) |
| consultar autoria e identidade | [Créditos](credits.md) |

## A ideia central

Cada entrega tem um arquivo principal:

```text
specs/specs/<número>-<nome-curto>/spec.md
```

Esse arquivo reúne o problema, os requisitos, os exemplos de comportamento, o
plano técnico, os testes, as tarefas e as evidências. O Specsfy evita criar
`plan.md`, `tasks.md` ou outros documentos que poderiam ficar diferentes da
especificação.

Um texto que você só quer preservar pode entrar primeiro na caixa de ideias:

```text
specs/ideias/<data>-<hora>-<nome-curto>.md
```

Uma ideia escolhida para refinamento pode seguir para o backlog:

```text
specs/backlog/<número>-<nome-curto>.md
```

## Uma jornada completa, em linguagem simples

Imagine que você queira adicionar uma página de boas-vindas.

### 1. Capture sem perguntas

```text
Use $specsfy-base-idea para capturar:
quero uma página de boas-vindas para pessoas que acabaram de criar a conta.
```

O agente preserva e pré-processa o texto em `specs/ideias/`, sem perguntar
nada. Veja a [caixa de entrada de ideias](ideas.md).

### 2. Refine no backlog

```text
Use $specsfy-base-backlog para guardar esta ideia:
quero uma página de boas-vindas para pessoas que acabaram de criar a conta.
```

O agente faz poucas perguntas e cria um item em `specs/backlog/`. Veja
[como usar o backlog](skills/specsfy-base-backlog.md).

### 3. Tire as dúvidas

```text
Use $specsfy-base-interview para aprofundar
specs/backlog/0001-pagina-boas-vindas.md.
```

O agente pergunta uma coisa importante por vez: quem verá a página, qual
resultado precisa acontecer e quais limites importam. Veja
[como funciona a entrevista](skills/specsfy-base-interview.md).

### 4. Crie a especificação

```text
Use $specsfy-base-specify para promover
specs/backlog/0001-pagina-boas-vindas.md.
```

O resultado fica em
`specs/specs/0001-pagina-boas-vindas/spec.md`. Veja
[como montar uma spec](skills/specsfy-base-specify.md).

### 5. Confira se está pronta

```text
Use $specsfy-base-validate em
specs/specs/0001-pagina-boas-vindas/spec.md.
```

Se algo estiver ambíguo, o agente volta à pergunta necessária. Quando a
definição estiver pronta, o `Definition Gate` é aprovado. Veja
[como validar](skills/specsfy-base-validate.md).

### 6. Divida o trabalho

```text
Use $specsfy-base-tasks em
specs/specs/0001-pagina-boas-vindas/spec.md.
```

As tarefas são pequenas, ordenadas e continuam dentro de `spec.md`. Veja
[como preparar tarefas](skills/specsfy-base-tasks.md).

### 7. Prepare os testes

```text
Use $specsfy-base-tdd-bdd em modo prepare para
specs/specs/0001-pagina-boas-vindas/spec.md.
```

O agente transforma os exemplos de comportamento em testes executáveis e
mostra o RED: a falha esperada antes do código existir. Veja
[como usar TDD e BDD](skills/specsfy-base-tdd-bdd.md).

### 8. Implemente

```text
Use $specsfy-base-implement para concluir a próxima tarefa pronta de
specs/specs/0001-pagina-boas-vindas/spec.md.
```

Cada tarefa passa por RED, GREEN e refatoração. Veja
[como implementar](skills/specsfy-base-implement.md).

### 9. Incorpore uma mudança

Se você lembrar depois que a página também precisa de um botão:

```text
Use $specsfy-base-update-spec para adicionar um botão "Começar" à
specs/specs/0001-pagina-boas-vindas/spec.md.
```

O agente atualiza a mesma especificação e reabre somente as etapas afetadas.
Veja [como mudar uma spec](skills/specsfy-base-update-spec.md).

### 10. Veja o progresso

```text
Use $specsfy-base-progress para mostrar o estado geral do projeto.
```

O relatório lê as specs, sem criar uma segunda fonte de status. Veja
[como consultar progresso](skills/specsfy-base-progress.md).

## Conversa contínua entre etapas

Quando uma etapa depende de outra skill, o agente anuncia a transição, resolve
a pendência e retoma o trabalho na mesma conversa. Você não precisa repetir o
pedido nem decorar a ordem das skills.

## Os três atos

O fluxo completo é dividido em três partes:

1. **Ato I — Definir:** entender e validar o que deve ser entregue.
2. **Ato II — Projetar e provar:** planejar tarefas e mostrar testes falhando
   pela razão certa.
3. **Ato III — Entregar e validar:** implementar, obter testes verdes e
   registrar evidências.

Você não precisa conduzir as transições manualmente. Quando uma etapa depende de
outra skill, o agente anuncia a transição e continua na mesma conversa.

## CLI e interface visual

Depois da [instalação](installation.md), estes comandos cobrem o uso mais comum:

```bash
specsfy
specsfy install --project .
specsfy progress --project .
specsfy skills list
specsfy skills detect --project .
specsfy test --project .
```

Executar `specsfy` sem subcomando abre a TUI, uma interface visual no terminal
com specs, backlog, testes, skills e progresso. O [guia do CLI e da
TUI](cli.md) explica cada opção.

## Contexto e conhecimento técnico

O setup cria arquivos para descrever o projeto, a stack, as regras e o banco.
Isso ajuda agentes a entenderem o sistema sem adivinhar. Veja
[Contexto do projeto](project-context.md).

As skills base cuidam do método. Quando uma entrega exige conhecimento de
Laravel, React, segurança, banco ou outro domínio, use uma
[skill especialista](specialists.md).

Depois da implementação, `specsfy-documentator` pode reconstruir a
[documentação técnica da sua aplicação](system-documentation.md).

## Próximos passos

1. conclua a [instalação](installation.md);
2. siga o [primeiro projeto](getting-started.md);
3. consulte as [páginas das skills base](skills/README.md) quando quiser
   aprofundar uma etapa;
4. use o [guia técnico](../develop/README.md) somente se quiser contribuir ou
   modificar o próprio framework.

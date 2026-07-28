# Uso básico do Specsfy

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | primeira fatia de trabalho em um projeto consumidor |
| Autoridade | metodologia executável de `skills/` |

## Papel

Conduzir uma ideia do backlog até uma entrega comprovada, mantendo uma única
fonte normativa e sem exigir que a pessoa memorize toda a sequência de skills.

## Como usar

### Pré-condições

- CLI e framework instalados conforme o [guia de instalação](installation.md);
- agente aberto na raiz do projeto consumidor;
- uma ideia de produto ou mudança que possa ser descrita em linguagem comum.

## Veja o Specsfy trabalhando

Vamos criar uma página de boas-vindas em um projeto Laravel que já usa Pest.
Os nove comandos abaixo mostram a jornada completa.

### 1. Guarde a ideia — `$specsfy-base-backlog`

```text
Use $specsfy-base-backlog para guardar esta ideia:
criar uma página /boas-vindas que cumprimente a pessoa pelo nome.
```

Resultado:

```text
Ideia registrada em specs/backlog/0001-pagina-boas-vindas.md
```

### 2. Tire as dúvidas — `$specsfy-base-interview`

**Opção 1 — texto livre**

```text
Use $specsfy-base-interview para aprofundar este texto:
quero uma página /boas-vindas que cumprimente a pessoa pelo nome.
```

**Opção 2 — arquivo de backlog**

```text
Use $specsfy-base-interview em specs/backlog/0001-pagina-boas-vindas.md
```

O agente pergunta somente o que realmente falta:

```text
Agente: O que deve aparecer quando nenhum nome for informado?
Você: Olá, visitante!

Brief pronto para especificar.
```

### 3. Crie a especificação — `$specsfy-base-specify`

**Opção 1 — texto livre**

```text
Use $specsfy-base-specify para criar uma especificação a partir deste texto:
a página /boas-vindas mostra Olá e o nome informado; sem nome, usa visitante.
```

**Opção 2 — arquivo de backlog**

```text
Use $specsfy-base-specify para promover specs/backlog/0001-pagina-boas-vindas.md
```

Resultado:

```text
Especificação criada em
specs/specs/0001-pagina-boas-vindas/spec.md
3 cenários BDD cobrem a feature, sua história e seus requisitos.
```

### 4. Confira a especificação — `$specsfy-base-validate`

```text
Use $specsfy-base-validate em specs/specs/0001-pagina-boas-vindas/spec.md
```

Resultado:

```text
READY
Definition Gate: Passed
```

`READY` significa que o pedido está claro o bastante para seguir.

### 5. Divida o trabalho — `$specsfy-base-tasks`

```text
Use $specsfy-base-tasks em specs/specs/0001-pagina-boas-vindas/spec.md
```

Resultado:

```text
2 tarefas preparadas.
```

### 6. Prepare a verificação — `$specsfy-base-tdd-bdd`

```text
Use $specsfy-base-tdd-bdd em specs/specs/0001-pagina-boas-vindas/spec.md
para preparar a verificação.
```

Resultado:

```text
Verificação preparada: 3 casos TDD com marcadores SPECSFY: próprios.
RED observado antes da implementação.
```

O mínimo de três usa contextos diferentes — por exemplo, caminho feliz,
variação crítica e falha material — sem duplicar o mesmo exemplo.

### 7. Implemente — `$specsfy-base-implement`

```text
Use $specsfy-base-implement em specs/specs/0001-pagina-boas-vindas/spec.md
```

Resultado:

```text
Implementação concluída.
Página /boas-vindas criada.
Verificação aprovada.
```

### 8. Altere a especificação — `$specsfy-base-update-spec`

Depois de implementar, imagine que você lembrou de uma regra:

```text
Use $specsfy-base-update-spec em
specs/specs/0001-pagina-boas-vindas/spec.md:
o nome deve ter no máximo 80 caracteres.
```

Resultado:

```text
Pedido incorporado na especificação 0001-pagina-boas-vindas.
Etapas afetadas retomadas automaticamente.
Implementação atualizada.
```

A mudança continua na mesma spec e volta apenas às etapas necessárias.

### 9. Veja o progresso — `$specsfy-base-progress`

```text
Use $specsfy-base-progress para mostrar o resultado final.
```

Resultado:

```text
Complete · 3/3 etapas · nenhuma pendência
```

Você pode conferir a mesma entrega pelo CLI:

```bash
specsfy progress --project .
specsfy progress --project . --json
specsfy tui --project .
```

Ao autorizar a jornada completa, você não precisa enviar os nove comandos
manualmente: cada skill pode chamar a próxima e continuar na mesma conversa.
O passo a passo separado serve para aprender, inspecionar ou retomar qualquer
etapa.

## Resultado esperado

Ao final, a ideia está registrada, as dúvidas foram resolvidas, a especificação
foi validada, a página foi implementada e o progresso mostra `Complete`.

## Limites

- `specsfy-base-update-spec` faz mudança de comportamento reabrir os Atos I–III;
- `specsfy-base-update-spec` faz mudança de plano reabrir os Atos II–III;
- backlog não autoriza implementação;
- não crie `plan.md`, `tasks.md`, `research.md` ou `data-model.md`;
- deploy, publicação, instalação e ações destrutivas mantêm autorização própria.

## Próximos passos

- [Uso avançado](advanced-usage.md)
- [CLI e TUI](cli.md)
- [Contexto persistente do projeto](project-context.md)
- [Documentação técnica do sistema](system-documentation.md)

## Atualize quando

- a sequência dos atos ou a responsabilidade de uma skill base mudar;
- os gates, estados ou caminhos canônicos mudarem;
- a primeira jornada do usuário ganhar ou perder uma etapa.

## Não use para

- definir comandos avançados do CLI;
- reproduzir o contrato completo de cada skill;
- registrar requisitos ou evidências de um projeto consumidor.

## Fonte da verdade e precedência

A metodologia executável pertence a
[`skills/`](../../skills/). A fonte normativa de
cada fatia pertence ao projeto consumidor em
`specs/specs/<NNNN>-<slug>/spec.md`.

# Specsfy

<p align="center">
  <picture>
    <source srcset="../brand/icons/icon.svg" type="image/svg+xml">
    <img src="../brand/icons/icon.png" alt="Ícone do framework Specsfy" width="160">
  </picture>
</p>

> Especifique. Prove. Entregue.

Specsfy é uma metodologia prática para desenvolver software a partir de uma
especificação única, executável e rastreável. Esta é a porta de entrada para o
usuário final: instale o CLI, prepare um projeto e conduza a primeira fatia de
trabalho pelo passo a passo abaixo.

![Dashboard Home do Specsfy](../docs/user/assets/cli/cli-dash.png)

A TUI transforma specs, tarefas, checklists e gates em uma visão operacional.
Veja as demais telas e comandos no
[guia do CLI](../docs/user/cli.md).

## O que você precisa

- Python 3.11 ou superior;
- [`uv`](https://docs.astral.sh/uv/) disponível no terminal;
- o comando [`skills`](https://github.com/vercel-labs/skills) ou `npx`;
- um projeto existente ou recém-criado no qual o Specsfy será aplicado.

O monorepo [`promovaweb/specsfy`](https://github.com/promovaweb/specsfy) não é um projeto
consumidor e recusa o bootstrap.

## Instalação passo a passo

### 1. Instale o CLI

```bash
uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'
```

Confirme a instalação:

```bash
specsfy --version
```

Se o comando não for encontrado, aplique a orientação de `PATH` exibida pelo
`uv`, abra um novo terminal e repita a verificação.

### 2. Entre no projeto

```bash
cd caminho/do/projeto
```

### 3. Instale o framework

```bash
specsfy install --project .
```

O comando instala as skills base, setup, documentação e contexto auxiliar em
`.agents/skills/`, publica o contrato em `.specsfy/Spec.md` e reconcilia blocos
gerenciados em `AGENTS.md` e `CLAUDE.md`. Ele não cria uma spec de produto.

### 4. Verifique o projeto

```bash
specsfy skills list
specsfy progress --project .
```

Uma instalação nova ainda pode mostrar zero specs. Isso confirma que o CLI
consegue ler o projeto; a primeira spec nasce no fluxo de uso.

## Veja o Specsfy trabalhando

Vamos criar uma página de boas-vindas em um projeto Laravel que já usa Pest.
Este exemplo mostra os nove comandos base, do começo ao fim.

### 1. Guarde a ideia — `$specsfy-base-backlog`

Envie:

```text
Use $specsfy-base-backlog para guardar esta ideia:
criar uma página /boas-vindas que cumprimente a pessoa pelo nome.
```

Você verá algo assim:

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

O agente faz somente as perguntas necessárias. Neste exemplo:

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
```

Ela registra dois resultados esperados: com `?nome=Ana`, mostrar `Olá, Ana!`;
sem nome, mostrar `Olá, visitante!`.

### 4. Confira a especificação — `$specsfy-base-validate`

Envie:

```text
Use $specsfy-base-validate em specs/specs/0001-pagina-boas-vindas/spec.md
```

Resultado:

```text
READY
Definition Gate: Passed
```

`READY` significa que a ideia está clara o bastante para virar trabalho.

### 5. Divida o trabalho — `$specsfy-base-tasks`

Envie:

```text
Use $specsfy-base-tasks em specs/specs/0001-pagina-boas-vindas/spec.md
```

Resultado:

```text
2 tarefas preparadas.
```

### 6. Prepare a verificação — `$specsfy-base-tdd-bdd`

Envie:

```text
Use $specsfy-base-tdd-bdd em specs/specs/0001-pagina-boas-vindas/spec.md
para preparar a verificação.
```

Resultado:

```text
Verificação preparada.
```

### 7. Implemente — `$specsfy-base-implement`

Envie:

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

Envie:

```text
Use $specsfy-base-progress para mostrar o resultado final.
```

Resultado:

```text
Complete · 3/3 etapas · nenhuma pendência
```

Você também pode abrir a mesma visão pelo CLI:

```bash
specsfy progress --project .
specsfy progress --project . --json
specsfy tui --project .
```

Pronto: uma ideia pequena atravessou `Ato I — Definir`,
`Ato II — Projetar e provar` e `Ato III — Entregar`. Depois que você autoriza a
jornada completa, o agente também pode passar de um comando ao próximo
automaticamente.

## Atualização

Atualize o ambiente isolado do CLI:

```bash
uv tool upgrade specsfy-cli
```

Depois, atualize as skills Specsfy instaladas no projeto:

```bash
specsfy skills update --project .
```

Alterações locais em conteúdo gerenciado são preservadas e bloqueiam a
substituição. Revise o conflito antes de decidir por `--force`, pois essa opção
descarta a customização protegida.

## Dicas para usar o CLI

- Descubra comandos e opções sem sair do terminal:

  ```bash
  specsfy --help
  specsfy skills --help
  ```

- `--project .` usa o diretório atual. Troque `.` por outro caminho para
  inspecionar ou operar um projeto sem entrar nele:

  ```bash
  specsfy progress --project caminho/do/projeto
  ```

- Para automações, solicite um snapshot em JSON. Durante o desenvolvimento,
  `--watch` emite outro snapshot somente quando as specs mudam:

  ```bash
  specsfy progress --project . --json
  specsfy progress --project . --watch
  ```

- Use `specsfy skills detect --project .` para consultar especialistas
  recomendados sem instalá-los. Na aba **Skills** da TUI, alterações também
  permanecem como um plano. Nada é instalado ou removido antes de **Aplicar**.

- Trate o progresso como leitura: o CLI projeta checkboxes e gates, mas não
  aprova gates nem altera a fonte normativa da spec.

## Uso por stack

O framework base é independente de linguagem. Especialistas acrescentam
critérios técnicos sem alterar os três atos:

- [Laravel](../docs/user/laravel.md);
- [Astro](../docs/user/astro.md);
- [Next.js](../docs/user/nextjs.md).

Você pode instalar recomendações detectadas:

```bash
specsfy install --project . --detected
```

Ou escolher uma explicitamente:

```bash
specsfy skills add specsfy-specialist-laravel --project .
```

Instalar especialista é uma ação explícita; uma recomendação do agente não o
instala automaticamente.

## Próximos guias

- [Instalação completa](../docs/user/installation.md)
- [Uso básico](../docs/user/getting-started.md)
- [Atualizar uma especificação](../docs/user/update-spec.md)
- [Uso avançado](../docs/user/advanced-usage.md)
- [CLI, TUI e atualização](../docs/user/cli.md)
- [Mapa dos módulos](../docs/develop/modules.md)
- [Documentação completa](../docs/)

## O que o Specsfy garante

Cada fatia atravessa:

```text
Draft → Defined → Planned → Implementing → Complete
```

Os mesmos IDs conectam histórias, requisitos, critérios de aceite, testes,
tarefas e evidências:

```text
US → FR/NFR → AC → teste BDD/TDD → tarefa → evidência
```

O Specsfy não substitui julgamento de produto, pesquisa, segurança ou
engenharia. Ele também não impõe arquitetura nem gerenciador de projetos; seu
contrato é tornar decisões e conclusão rastreáveis.

## Ecossistema

| Repositório | Responsabilidade |
| --- | --- |
| [`specsfy/`](./) | porta de entrada pública |
| [`docs/`](../docs/) | documentação oficial para usuários |
| [`skills/`](../skills/) | metodologia executável |
| [`specialists/`](../specialists/) | conhecimento técnico opcional |
| [`cli/`](../cli/) | instalação, CLI, TUI e progresso |
| [`example/`](../example/) | aplicação interna de validação |
| [`brand/`](../brand/) | identidade visual e verbal |
| [`promovaweb/specsfy`](https://github.com/promovaweb/specsfy) | orquestração e testes integrados |

Veja responsabilidades, públicos e limites no
[guia dos módulos](../docs/develop/modules.md).

## Créditos

Specsfy é um projeto da [Promovaweb](https://promovaweb.com), mantido por
**Luiz Eduardo Oliveira Fonseca** e pela comunidade.

Contato: [contato@promovaweb.com](mailto:contato@promovaweb.com).
Consulte os [créditos completos](../docs/user/credits.md).

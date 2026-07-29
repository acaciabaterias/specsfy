# Specsfy

<!-- markdownlint-disable MD033 -->
<p align="center">
  <picture>
    <source srcset="../brand/logo/icon.svg" type="image/svg+xml">
    <img src="../brand/logo/icon.png" alt="Logo do Specsfy" width="128">
  </picture>
</p>
<!-- markdownlint-enable MD033 -->

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

- Python 3.11 ou superior.
- [`uv`](https://docs.astral.sh/uv/) disponível no terminal.
- o comando [`skills`](https://github.com/vercel-labs/skills) ou `npx`.
- um projeto existente ou recém-criado no qual o Specsfy será aplicado.

O monorepo
[`promovaweb/specsfy`](https://github.com/promovaweb/specsfy) não é um
projeto consumidor e recusa o bootstrap.

## Instalação passo a passo

### 1. Instale o CLI

Baixe o executável pela URL oficial
`get.specsfy.dev`. Para manter a instalação e as atualizações gerenciadas pelo
`uv`, use:

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
gerenciados em `AGENTS.md` e `CLAUDE.md`. Os templates ficam juntos em
`.specsfy/templates/`. Personalizações homônimas ficam em
`.specsfy/templates/custom/`, têm precedência e não são sobrescritas pelo CLI.
Ele não cria uma spec de produto.

### 4. Verifique o projeto

```bash
specsfy skills list
specsfy progress --project .
```

Uma instalação nova ainda pode mostrar zero specs. Isso confirma que o CLI
consegue ler o projeto. A primeira spec é criada durante o fluxo de uso.

## Veja o Specsfy trabalhando

Vamos criar uma página de boas-vindas em um projeto Laravel que já usa Pest.
Este exemplo mostra as nove skills base, do começo ao fim.

### 1. Capture uma entrada — `$specsfy-01-inbox`

Envie:

```text
Use $specsfy-01-inbox para capturar:
criar uma página /boas-vindas que cumprimente a pessoa pelo nome.
```

Sem fazer perguntas, o agente cria algo como:

```text
Entrada capturada em
specs/inbox/2026-07-28-143205-pagina-boas-vindas.md
```

### 2. Refine no backlog — `$specsfy-02-backlog`

Envie:

```text
Use $specsfy-02-backlog para refinar esta entrada:
criar uma página /boas-vindas que cumprimente a pessoa pelo nome.
```

Você verá algo assim:

```text
Backlog registrado em specs/backlog/0001-pagina-boas-vindas.md
```

#### Refinar a partir de texto livre

```text
Use $specsfy-02-backlog para aprofundar este texto:
quero uma página /boas-vindas que cumprimente a pessoa pelo nome.
```

#### Refinar a partir do backlog

```text
Use $specsfy-02-backlog em specs/backlog/0001-pagina-boas-vindas.md
```

O agente reavalia cada resposta e continua enquanto houver lacunas aplicáveis,
sem um limite máximo de perguntas. A partir da 11ª pergunta, também oferece
`avançar`; essa saída encerra o refinamento do backlog atual, mas mantém a definição
pendente. Neste exemplo:

```text
Agente: O que deve aparecer quando nenhum nome for informado?
Você: Olá, visitante!

Brief pronto para especificar.
```

### 3. Crie a especificação — `$specsfy-03-specify`

#### Especificar a partir de texto livre

```text
Use $specsfy-03-specify para criar uma especificação a partir deste texto:
a página /boas-vindas mostra Olá e o nome informado.
Sem nome, usa visitante.
```

#### Especificar a partir do backlog

```text
Use $specsfy-03-specify para promover specs/backlog/0001-pagina-boas-vindas.md
```

Resultado:

```text
Especificação criada em
specs/specs/0001-pagina-boas-vindas/spec.md
```

Ela registra dois resultados esperados: com `?nome=Ana`, mostrar `Olá, Ana!`.
Sem nome, mostrar `Olá, visitante!`.

### 4. Confira a especificação — `$specsfy-04-validate`

Envie:

```text
Use $specsfy-04-validate em specs/specs/0001-pagina-boas-vindas/spec.md
```

Resultado:

```text
READY
Definition Gate: Passed
```

`READY` significa que a ideia está clara o bastante para virar trabalho.

### 5. Divida o trabalho — `$specsfy-05-tasks`

Envie:

```text
Use $specsfy-05-tasks em specs/specs/0001-pagina-boas-vindas/spec.md
```

Resultado:

```text
2 tarefas preparadas.
```

### 6. Prepare a verificação — `$specsfy-06-tdd-bdd`

Envie:

```text
Use $specsfy-06-tdd-bdd em specs/specs/0001-pagina-boas-vindas/spec.md
para preparar a verificação.
```

Resultado:

```text
Verificação preparada.
```

### 7. Implemente — `$specsfy-07-implement`

Envie:

```text
Use $specsfy-07-implement em specs/specs/0001-pagina-boas-vindas/spec.md
```

Resultado:

```text
Implementação concluída.
Página /boas-vindas criada.
Verificação aprovada.
```

### 8. Altere a especificação — `$specsfy-update-spec`

Depois de implementar, imagine que você lembrou de uma regra:

```text
Use $specsfy-update-spec em
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

### 9. Veja o progresso — `$specsfy-progress`

Envie:

```text
Use $specsfy-progress para mostrar o resultado final.
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

Alterações locais em conteúdo gerenciado são preservadas e impedem a
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
orientação técnica sem alterar os três atos:

- [Laravel](../docs/user/laravel.md).
- [Astro](../docs/user/astro.md).
- [Next.js](../docs/user/nextjs.md).

Você pode instalar recomendações detectadas:

```bash
specsfy install --project . --detected
```

Ou escolher uma explicitamente:

```bash
specsfy skills add specsfy-specialist-laravel --project .
```

Instalar especialista é uma ação explícita. Uma recomendação do agente não o
instala automaticamente.

## Próximos guias

- [Instalação completa](../docs/user/installation.md)
- [Uso básico](../docs/user/getting-started.md)
- [Atualizar uma especificação](../docs/user/update-spec.md)
- [Uso avançado](../docs/user/advanced-usage.md)
- [CLI, TUI e atualização](../docs/user/cli.md)
- [Módulos do monorepo](../docs/develop/modules.md)
- [Documentação completa](../docs/)

## O que o Specsfy garante

Cada fatia atravessa:

```text
Draft → Defined → Planned → Implementing → Complete
```

Os mesmos IDs conectam histórias, requisitos, condições de aceite, testes,
tarefas e evidências:

```text
US → FR/NFR → AC → teste BDD/TDD → tarefa → evidência
```

O Specsfy não substitui julgamento de produto, pesquisa, segurança ou
engenharia. Ele também não impõe arquitetura nem gerenciador de projetos. Seu
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

### Inspirações e fontes

O projeto reconhece o
[GitHub Spec Kit](https://github.github.com/spec-kit/), o
[OpenSpec](https://openspec.dev/) e o livro
[*Categorias*, de Aristóteles](https://classics.mit.edu/Aristotle/categories.html)
como inspirações. Eles contribuíram, respectivamente, para o estudo de fluxos
de specification-driven development, acordos leves entre pessoas e agentes e
classificação explícita de objetos, atributos, relações e estados.

Essas referências não são dependências do Specsfy nem indicam equivalência
entre os métodos. O contrato executável do projeto permanece nas skills, nos
templates, nos validadores e nos testes deste repositório.

Contato: [contato@promovaweb.com](mailto:contato@promovaweb.com).
Consulte os [créditos completos](../docs/user/credits.md).

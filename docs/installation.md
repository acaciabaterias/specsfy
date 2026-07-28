# Instalação do Specsfy

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | instalação do CLI e do framework em um projeto consumidor |
| Autoridade | interfaces públicas de `cli/` e `skills/` |

## Papel

Instalar o executável `specsfy` para o usuário atual e materializar o framework
em um projeto que aplicará a metodologia.

## Como usar

### Pré-requisitos

- Python 3.11 ou superior;
- [`uv`](https://docs.astral.sh/uv/) disponível no terminal;
- o comando [`skills`](https://github.com/vercel-labs/skills) ou `npx`
  disponível para o fallback usado pelo CLI;
- um projeto consumidor no qual você possa criar ou atualizar arquivos.

O monorepo é privado. Antes de instalar, execute `gh auth login` e confirme com
`gh auth status`. Em CI, defina `GH_TOKEN` ou `GITHUB_TOKEN` com acesso de
leitura. O CLI reutiliza a mesma credencial para consultar catálogo e versões,
sem persistir o token.

Não execute o bootstrap na raiz oficial `promovaweb/specsfy`. O CLI reconhece
essa raiz e recusa a instalação para que o monorepo não seja convertido em projeto
consumidor.

## 1. Instale o CLI

Instale o CLI em um ambiente isolado gerenciado pelo `uv`:

```bash
uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'
```

Confirme que o executável está disponível:

```bash
specsfy --version
```

Se o shell não localizar `specsfy`, siga a orientação de PATH exibida pelo
`uv`, abra um novo terminal e repita a verificação.

### Atualize o CLI

O `uv` mantém a origem Git e as opções usadas na instalação. Atualize o ambiente
isolado do CLI com:

```bash
uv tool upgrade specsfy-cli
```

Use novamente `uv tool install` somente quando quiser trocar a origem ou uma
restrição de versão.

## 2. Instale o framework no projeto

Entre na raiz do projeto consumidor e indique o destino explicitamente:

```bash
cd caminho/do/projeto
specsfy install --project .
```

O comando instala e reconcilia:

- as nove skills `.agents/skills/specsfy-base-*`, incluindo
  `specsfy-base-update-spec`;
- `.agents/skills/specsfy-setup`;
- `.agents/skills/specsfy-documentator`;
- as três skills `.agents/skills/specsfy-aux-*`;
- `.specsfy/Spec.md`, com as regras centrais do framework;
- `.specsfy/templates/Spec.md` e `.specsfy/examples/Spec.md`;
- blocos gerenciados em `AGENTS.md` e `CLAUDE.md`;
- os registros `skills-lock.json` e `.specsfy/skills-lock.json`.

O CLI delega a cópia das skills ao instalador `skills`. Quando esse executável
não está disponível, usa `npx --yes skills`.

## 3. Verifique o resultado

Confirme que o comando concluiu sem erro e inspecione, no projeto consumidor:

```text
.agents/skills/specsfy-base-*
.agents/skills/specsfy-setup
.agents/skills/specsfy-documentator
.agents/skills/specsfy-aux-*
.specsfy/Spec.md
```

Uma nova execução de `specsfy install --project .` é idempotente. Conteúdo
humano fora dos blocos gerenciados é preservado. Uma alteração local em skill,
regra ou bloco gerenciado interrompe a substituição; `--force` é a decisão
explícita para descartar essa customização.

O bootstrap instala o framework, mas não cria uma spec de produto. Ideias e
especificações passam a existir somente quando seus respectivos fluxos são
acionados no projeto consumidor.

## Próximos passos

- Conduza a primeira fatia no [guia de uso básico](basic-usage.md).
- Abra `specsfy` na raiz do projeto para usar a TUI.
- Consulte [CLI e TUI](cli.md) para comandos, atualização, progresso e
  segurança.
- Veja o [uso avançado](advanced-usage.md) para detecção e seleção explícita de
  especialistas.
- Use o [catálogo da metodologia](../skills/) para
  conhecer as responsabilidades das skills.

## Atualize quando

- o método de distribuição ou os pré-requisitos do CLI mudarem;
- o comando de bootstrap ou seu destino mudar;
- o conjunto obrigatório do framework mudar;
- os arquivos gerenciados ou as proteções de reinstalação mudarem.

## Não use para

- preparar o workspace de desenvolvimento `promovaweb/specsfy`;
- instalar skills técnicas opcionais;
- criar specs, alterar gates ou iniciar uma implementação;
- instalar dependências da aplicação consumidora.

## Fonte da verdade e precedência

A distribuição, o bootstrap e as proteções executáveis pertencem a
[`cli/`](../cli/). A metodologia e as skills
instaladas pertencem a
[`skills/`](../skills/). Este guia explica a
jornada pública sem substituir essas fontes.

# Arquitetura do CLI e da TUI

O módulo `cli/` distribui o framework, gerencia especialistas, projeta progresso
e oferece a interface terminal. Ele não define requisitos nem aprova gates.

## Entradas

`cli/src/specsfy_cli/app.py` define:

```text
specsfy install
specsfy skills
specsfy progress
specsfy test
specsfy tui
specsfy config
```

Sem subcomando, a aplicação abre a TUI.

## Componentes

| Módulo | Responsabilidade |
| --- | --- |
| `app.py` | parser, despacho e saída não interativa |
| `installer.py` | framework, skills, merge e proteção local |
| `catalog.py` | catálogo remoto de especialistas |
| `skill_lock.py` | seleção instalada, fingerprints e proteção |
| `progress.py` | leitura e resumo das specs |
| `backlog.py` | projeção dos itens de backlog |
| `testing.py` | detecção e execução do runner consumidor |
| `config.py` | configuração por projeto |
| `updater.py` | descoberta de tags e oferta de atualização |
| `github.py` | headers e autenticação da API do GitHub |
| `tui.py` | dashboard Textual e interações |

## Instalação

`SkillInstaller` valida que o destino é um projeto consumidor, obtém `skills/`
do monorepo e instala o conjunto `FRAMEWORK_SKILLS`. Esse conjunto inclui setup,
três auxiliares, documentador e dez skills base.

Conteúdo gerenciado recebe fingerprints. Se a cópia local divergir do último
fingerprint registrado, atualização e remoção recusam a operação sem `--force`.

O instalador publica `Idea.md`, `Backlog.md`, `Spec.md`, `Tasks.md`,
`Project.md`, `Stack.md`, `Rules.md` e `Database.md` em
`.specsfy/templates/`. Cada template possui digest próprio; assim, uma
customização local em qualquer um deles bloqueia somente uma substituição
explicitamente forçada.

## Catálogo

`specialists/catalog.json` é a fonte executável. `Catalog.fetch()` usa a API de
conteúdo do GitHub e aceita override local por
`SPECSFY_SPECIALISTS_CATALOG`.

Como o repositório é privado, a autenticação procura:

1. `GH_TOKEN`;
2. `GITHUB_TOKEN`;
3. `gh auth token`.

O token permanece no ambiente ou no armazenamento do GitHub CLI e não é
gravado pelo Specsfy.

## Progresso

O scanner lê `specs/specs/*/spec.md`, com compatibilidade de leitura do layout
legado. Status, gates, tarefas e checklists são projeções. `--watch` recalcula
quando o fingerprint das fontes muda.

## Testes do consumidor

`testing.py` reconhece runners suportados a partir do projeto selecionado. O
comando transmite saída e preserva o exit code. A TUI separa resumo e detalhes,
mas usa o mesmo contrato.

## Atualização

`updater.py` consulta tags semânticas estáveis, respeita intervalo e ETag,
oferece consentimento e delega a instalação a:

```text
uv tool upgrade specsfy-cli
```

Falha de rede não impede a abertura. Configurações e metadados ficam em
`~/.specsfy/cli.json` com permissão `0600`; credenciais não são persistidas.

## Artefato versionado

`scripts/build-executable.sh` constrói `cli/bin/specsfy` e
`cli/bin/specsfy.build.json`. O executável é distribuído publicamente por
`get.specsfy.dev`. O fingerprint usa modos equivalentes aos preservados
pelo Git para produzir o mesmo resultado localmente e no CI.

Toda mudança em `cli/` reconstrói e versiona esses artefatos.

## Testes

```bash
cd cli
uv sync --locked
uv run python -B -m unittest discover -s tests -p 'test_*.py'
uv build
uv run specsfy --help
./scripts/build-executable.sh
./bin/specsfy --version
```

Mudanças de interface atualizam também
[`docs/user/cli.md`](../user/cli.md).

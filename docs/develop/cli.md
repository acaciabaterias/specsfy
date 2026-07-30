# Arquitetura do CLI e da TUI

O módulo `cli/` distribui o framework, gerencia especialistas, projeta progresso
e oferece a interface terminal. A implementação usa TypeScript sobre Node.js e
não define requisitos nem aprova gates.

## Entradas

`cli/src/cli.ts` define:

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
| `cli.ts` | parser Commander, despacho e saída não interativa |
| `installer.ts` | framework, skills, merge e proteção local |
| `catalog.ts` | catálogo remoto de especialistas |
| `skill-lock.ts` | seleção instalada, fingerprints e proteção |
| `progress.ts` | leitura e resumo das specs |
| `backlog.ts` | projeção dos itens de backlog |
| `project-testing.ts` | detecção e execução do runner consumidor |
| `config.ts` | configuração por projeto |
| `updater.ts` | descoberta de tags e oferta de atualização |
| `github.ts` | headers e autenticação da API do GitHub |
| `tui.ts` | dashboard neo-blessed e interações |

## Instalação

`SkillInstaller` valida que o destino é um projeto consumidor, obtém `skills/`
do monorepo e instala o conjunto `FRAMEWORK_SKILLS`. Esse conjunto inclui setup,
três auxiliares, documentador e nove skills base.

Conteúdo gerenciado recebe fingerprints. Se a cópia local divergir do último
fingerprint registrado, atualização e remoção recusam a operação sem `--force`.

O instalador publica `Inbox.md`, `Backlog.md`, `Spec.md`, `Tasks.md`,
`Project.md`, `Stack.md`, `Rules.md` e `Database.md` em
`.specsfy/templates/`. Cada template possui digest próprio. Assim, uma
customização local em qualquer um deles impede somente uma substituição
explicitamente forçada.

O instalador também cria `.specsfy/templates/custom/`, sem registrar os
arquivos desse diretório no lock. Um arquivo
`.specsfy/templates/custom/<Nome>.md` prevalece sobre o homônimo gerenciado.
Atualizações, remoções e `--force` nunca alteram essa camada do usuário.

## Catálogo

`specialists/catalog.json` é a fonte executável. `Catalog.fetch()` usa a API de
conteúdo do GitHub e aceita override local por
`SPECSFY_SPECIALISTS_CATALOG`.

Como o repositório é privado, a autenticação procura:

1. `GH_TOKEN`.
2. `GITHUB_TOKEN`.
3. `gh auth token`.

O token permanece no ambiente ou no armazenamento do GitHub CLI e não é
gravado pelo Specsfy.

## Progresso

O scanner lê `specs/specs/*/spec.md`, com compatibilidade de leitura do layout
legado. Status, gates, tarefas e checklists são projeções. `--watch` recalcula
quando o fingerprint das fontes muda.

## Testes do consumidor

`project-testing.ts` reconhece runners suportados a partir do projeto
selecionado. O comando transmite a saída e preserva o exit code. A TUI separa
resumo e detalhes, mas usa o mesmo contrato.

O painel detalhado usa uma caixa rolável com o conteúdo acumulado. O componente
`blessed.log` não deve ser usado nessa tela porque agenda a rolagem depois da
renderização e tenta acessar o widget anterior quando uma nova linha recria a
aba.

## Atualização

`updater.ts` consulta tags semânticas estáveis, respeita intervalo e ETag,
oferece consentimento e delega a instalação a:

```text
npm install --global @promovaweb/specsfy@latest
```

Falha de rede não impede a abertura. Configurações e metadados ficam em
`~/.specsfy/cli.json` com permissão `0600`. Credenciais não são persistidas.

## Artefato versionado

`scripts/build-executable.mjs` constrói `cli/bin/specsfy` e
`cli/bin/specsfy.build.json`. O executável Node é distribuído publicamente por
`get.specsfy.dev`. O fingerprint usa modos equivalentes aos preservados pelo
Git para produzir o mesmo resultado localmente e no CI.

Toda mudança em `cli/` reconstrói e versiona esses artefatos.

## Testes

`SpecsfyTui.start()` aceita um `screen` do neo-blessed, um catálogo conhecido e
a opção de desligar o polling. A suíte monta o mesmo renderer usado pelo
executável em terminais virtuais de `80x24`, `129x44` e `160x50`. O buffer
resultante confirma as seis abas, os painéis e os textos visíveis; eventos de
teclado e mouse conferem foco, filtros, busca, seleção de skills e o modal de
spec. Os atalhos de controle também são enviados como bytes de terminal. Essa
cobertura inclui os nomes `linefeed` e `backspace`, usados pelo neo-blessed para
`Ctrl+J` e `Ctrl+H`, e impede combinações indistinguíveis de `Tab` e `Enter`.

```bash
cd cli
npm ci
npm run build:executable
npm run check
node dist/main.js --help
./bin/specsfy --version
```

Mudanças de interface atualizam também
[`docs/user/cli.md`](../user/cli.md).

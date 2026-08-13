# Specsfy CLI

<!-- markdownlint-disable MD033 -->
<p align="center">
  <picture>
    <source srcset="https://promovaweb.com/opensource/specsfy/icon.svg" type="image/svg+xml">
    <img
      src="https://promovaweb.com/opensource/specsfy/icon.png"
      alt="Logo do Specsfy"
      width="128"
    >
  </picture>
</p>
<!-- markdownlint-enable MD033 -->

CLI e TUI para instalar e atualizar skills do Specsfy com segurança, detectar
tecnologias e acompanhar em tempo real o progresso das specs de um projeto.

## Pré-requisitos

- Node.js 22.20 ou superior, com o npm disponível.
- Git para obter o framework e acesso de escrita ao projeto consumidor.
- acesso autenticado ao repositório privado: execute `gh auth login` no uso
  interativo ou defina `GH_TOKEN`/`GITHUB_TOKEN` na automação.

## Download oficial

O executável versionado é publicado em `get.specsfy.dev`. Ele reúne o código e
as dependências JavaScript em um arquivo, mas continua usando o Node.js
instalado na máquina. Coloque o arquivo em um diretório do seu `PATH` e preserve
a permissão de execução.

## Instalar com npm

```bash
npm install --global @promovaweb/specsfy
specsfy --version
```

O npm instala o pacote publicado e disponibiliza o comando `specsfy`. Para
atualizar a instalação global:

```bash
specsfy upgrade
```

A instalação pelo npm inclui o `skills`, do projeto
[`vercel-labs/skills`](https://github.com/vercel-labs/skills). O Specsfy também
aceita uma instalação global, `SPECSFY_SKILLS_CLI` ou `npx` como alternativas.
O executável avulso de `get.specsfy.dev` não carrega pacotes externos; nesse
caso, mantenha `skills` ou `npx` disponível no `PATH`.

O catálogo e a verificação de versões usam a API do GitHub. O CLI procura,
nesta ordem, `GH_TOKEN`, `GITHUB_TOKEN` e a sessão retornada por
`gh auth token`. As credenciais não são gravadas pelo Specsfy.

Para instalar uma versão específica, informe a versão no próprio pacote:

```bash
npm install --global @promovaweb/specsfy@0.8.1
```

## Comandos

```bash
specsfy
specsfy doctor --project .
specsfy setup --project .
specsfy install --project .
specsfy install --project . --detected
specsfy install --project . \
  --specialist specsfy-specialist-laravel \
  --specialist specsfy-specialist-postgres
specsfy skills list
specsfy skills detect --project .
specsfy skills add specsfy-specialist-laravel --project .
specsfy skills remove specsfy-specialist-laravel --project .
specsfy update --project .
specsfy upgrade
specsfy transition 0001-recuperar-senha defined --project .
specsfy migrate --project .
specsfy effort 0001-recuperar-senha 7 \
  --reason "Inclui migração e integração externa." --project .
specsfy progress --project .
specsfy progress --project . --json
specsfy progress --project . --watch
specsfy milestones sync --project .
specsfy test --project .
specsfy config show --project .
specsfy config set --project . --watch-interval 0.5
```

Dependências declaradas pelo catálogo são resolvidas automaticamente. Por
exemplo, instalar `specsfy-specialist-react-ui-components` também instala
`specsfy-specialist-ui-design`, tanto pelo comando quanto pela TUI:

```bash
specsfy skills add specsfy-specialist-react-ui-components --project .
```

Sem subcomando, `specsfy` abre o dashboard TUI no diretório atual. A interface
possui seis abas:

- **Home**: totais de specs, tarefas, checklists e progresso global.
- **Backlogs**: lista navegável à esquerda e preview Markdown formatado à
  direita.
- **Specs**: tabela detalhada com gates e progresso de cada especificação.
  destaque uma linha e pressione `Espaço` para abrir a spec completa em um
  modal Markdown rolável, retornando à listagem com `Esc`.
- **Testes**: executa o Pest do projeto e separa o resultado entre as subabas
  **Resumo** e **Testes**, mantendo a saída detalhada rolável.
- **Skills**: catálogo tabular com plano, nome, categoria e estado, acompanhado
  por um painel de detalhes e resumo das alterações pendentes.
- **Sobre**: versão e finalidade do CLI.

A interface usa a paleta escura oficial do Specsfy. O turquesa identifica foco
e abas ativas, o violeta marca seleções e o petróleo diferencia superfícies e
ações primárias. Os estados continuam nomeados no próprio controle para que a
cor não seja o único sinal disponível.

## Capturas de tela

![Dashboard Home](https://promovaweb.com/docs/specsfy/cli/cli-dash.png)

![Backlogs](https://promovaweb.com/docs/specsfy/cli/cli-backlogs.png)

![Specs](https://promovaweb.com/docs/specsfy/cli/cli-specs.png)

![Skills](https://promovaweb.com/docs/specsfy/cli/cli-skills.png)

Alterações em `specs/inbox/*.md`, `specs/backlog/*.md`,
`specs/<estado>/*/spec.md` e no `skills-lock.json` são detectadas
automaticamente.

Em projetos Laravel com Pest, `specsfy test --project .` detecta `artisan` e
`pestphp/pest`, executa `php artisan test` a partir da raiz selecionada,
transmite a saída e devolve o mesmo exit code. Na TUI, `Executar testes ^X`
mostra status, runner, comando, duração e resumo em uma subaba. A outra exibe
cada teste e falha. Relatórios Pest estruturados são convertidos em linhas
legíveis com arquivo, linha e mensagem.

O bootstrap instala as treze skills base, incluindo `specsfy-01-inbox` e
`specsfy-update-spec` para pedidos surgidos depois da definição, as skills de
conversa e as de milestones,
`specsfy-setup`,
`specsfy-documentator` e as três skills `specsfy-aux-*`, publica as regras em
`.specsfy/Spec.md`, os templates `Inbox.md`, `Backlog.md`, `Spec.md`, `Tasks.md`,
`Project.md`, `Stack.md`, `Rules.md` e `Database.md` em
`.specsfy/templates/`, cria o diretório não gerenciado
`.specsfy/templates/custom/`, publica um exemplo em
`.specsfy/examples/Spec.md` e mescla blocos gerenciados em `AGENTS.md` e
`CLAUDE.md`, preservando as instruções do usuário. Instalações repetidas são
idempotentes. O lock registra fingerprints: versões intactas podem ser
atualizadas, mas conteúdo gerenciado customizado localmente só é substituído ou
removido com `--force`. Arquivos em `.specsfy/templates/custom/` sempre têm
precedência sobre os homônimos gerenciados e nunca são alterados, nem com
`--force`.

A materialização das skills é delegada ao comando oficial:

```bash
npx skills add <repositorio> \
  --skill <nome> \
  --agent universal \
  --copy \
  -y \
  --full-depth
```

O `skills-lock.json` gerado por essa ferramenta registra a proveniência e é a
fonte usada pela aba Skills para marcar os checkboxes instalados. Quando ainda
não existe em um projeto consumidor, o CLI cria o lock vazio compatível:

```json
{
  "version": 1,
  "skills": {}
}
```

O gerenciador lista exclusivamente `specsfy-setup`, `specsfy-documentator` e
skills do catálogo base, `specsfy-aux-*` e `specsfy-specialist-*`. Skills externas
presentes no mesmo lock não aparecem na interface e nunca são removidas ou
alteradas. O `.specsfy/skills-lock.json`
mantém os fingerprints usados pelo Specsfy para impedir que uma atualização
descarte alterações locais.

Na aba Skills, o botão `Atualizar ^R` baixa as origens atuais e atualiza de uma
vez todas as skills Specsfy instaladas. O comando equivalente é
`specsfy update --project .`. O nome anterior
`specsfy skills update --project .` permanece compatível. Customizações locais
continuam protegidas e só podem ser substituídas explicitamente com `--force`.

## Atualização do CLI gerenciada pelo npm

`specsfy update` atualiza as skills do projeto. `specsfy upgrade` consulta a
versão estável mais recente e atualiza o próprio pacote global. O segundo
comando só chama o npm quando encontra uma versão superior à atual.

Ao abrir `specsfy` ou `specsfy tui` em um terminal interativo, o CLI consulta
as tags semânticas estáveis do monorepo. A consulta é limitada pelo cache
global `~/.specsfy/cli.json`, cujo intervalo padrão é de 24 horas. Falha de rede
ou do GitHub nunca impede a abertura do dashboard.

Quando existe versão mais recente, o CLI mostra as versões atual e disponível e
pergunta antes de atualizar. Uma resposta negativa abre a aplicação normalmente.
Uma resposta positiva delega a atualização ao npm, que instala a versão mais
recente de `@promovaweb/specsfy` no escopo global. O processo então fecha. Abra
`specsfy` novamente para iniciar a versão instalada.

O arquivo global usa permissão `0600`, preserva chaves desconhecidas e separa:

- `settings.check_updates_on_startup`.
- `settings.check_interval_seconds`.
- `cache.last_checked_at`, tag, versão, commit, ETag e eventual erro recente.

Para publicar uma versão atualizável a partir do workspace de desenvolvimento,
use a skill local `$specsfy-release-cli`. Ela promove as notas confirmadas para
o [`CHANGELOG.md`](CHANGELOG.md), atualiza as versões do pacote e o lock,
reconstrói os artefatos versionados, cria a tag anotada `v<versão>` no mesmo
commit e usa exatamente a seção promovida como corpo do GitHub Release. O CI
valida o build e a correspondência da tag.

Novas specs usam `specs/draft/<NNNN>-<slug>/spec.md`. Capturas imediatas ficam
em `specs/inbox/<data-hora>-<slug>.md` e itens refináveis em
`specs/backlog/<NNNN>-<slug>.md`. O dashboard mantém leitura do layout
legado. A skill de especificação renderiza cada arquivo novo a partir do
template instalado. O CLI recusa instalação na raiz do monorepo oficial.

## Executável versionado

O executável empacotado fica em `bin/specsfy`, contém as dependências do CLI e
requer apenas o Node.js compatível. Reconstrua-o depois de qualquer alteração
neste módulo:

```bash
npm run build:executable
```

`bin/specsfy.build.json` registra o fingerprint dos inputs. A suíte de testes
falha quando o artefato não corresponde ao estado atual.

O pacote publicado no npm usa `@promovaweb/specsfy`. A tag estável dispara o
job de publicação depois que tipos, testes, build, instalação local e
executável versionado passam no CI. O job inclui proveniência quando o
repositório estiver público. Enquanto ele permanecer privado, publica com o
token do registro e sem essa atestação.

## Atalhos da TUI

- `Ctrl+Q`: sair.
- `Ctrl+U`: atualizar.
- `Ctrl+D`: detectar recomendações.
- `Ctrl+B`: selecionar todas as skills do framework.
- `Ctrl+E`: alternar o plano da skill destacada.
- `Ctrl+V` / `Ctrl+L`: marcar ou limpar os itens visíveis.
- `Ctrl+A`: aplicar.
- `Ctrl+R`: atualizar todas as skills Specsfy instaladas.
- `Ctrl+T`, `Ctrl+N`, `Ctrl+C`: filtros Todas, Instaladas e Recomendadas.
- `Ctrl+H`, `Ctrl+G`, `Ctrl+S`, `Ctrl+K`, `Ctrl+O`: Home, Backlogs, Specs,
  Skills e Sobre.
- `Ctrl+J`: abre Testes.
- `Ctrl+X`: executa os testes do projeto.
- `Espaço`: abre a spec destacada ou alterna a skill destacada, conforme a aba.
- `Esc`: fecha o modal da spec, limpa a busca de Skills ou volta para Home.

Cada botão mostra seu atalho no próprio rótulo. `Tab` e `Shift+Tab` percorrem
os controles e as setas navegam as tabelas. Na aba Skills, `Enter` ou `Espaço`
alternam o plano entre instalar, manter, remover e ignorar. Na aba Specs, abrem
o modal da linha destacada. O campo de projeto entra em edição com `Enter` ou
com um clique e atualiza o dashboard depois da confirmação. `Esc` retorna, e o
mouse opera abas, linhas e botões. Nada é instalado ou removido antes de
`Aplicar`.

A documentação completa está no
[portal público do Specsfy](https://promovaweb.com/docs/specsfy/). A
[referência dos comandos](https://promovaweb.com/docs/specsfy/referencia-cli/)
detalha parâmetros, saídas, efeitos persistentes e exemplos de automação.

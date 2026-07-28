# Specsfy CLI

<p align="center">
  <picture>
    <source srcset="../brand/icons/icon.svg" type="image/svg+xml">
    <img src="../brand/icons/icon.png" alt="Ícone do framework Specsfy" width="128">
  </picture>
</p>

CLI e TUI para instalar e atualizar skills do Specsfy com segurança, detectar
tecnologias e acompanhar em tempo real o progresso das specs de um projeto.

## Pré-requisitos

- Python 3.11 ou superior para instalação via `uv`;
- `skills`, do projeto
  [`vercel-labs/skills`](https://github.com/vercel-labs/skills), ou `npx`
  disponível para executá-lo sob demanda;
- acesso autenticado ao repositório privado: execute `gh auth login` no uso
  interativo ou defina `GH_TOKEN`/`GITHUB_TOKEN` na automação.

## Instalar com uv

```bash
uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'
```

O `uv` cria um ambiente isolado, registra a origem Git e publica o comando
`specsfy` no diretório de ferramentas do usuário. Para atualizar mantendo a
mesma origem e as mesmas opções da instalação:

```bash
uv tool upgrade specsfy-cli
```

O catálogo e a verificação de versões usam a API do GitHub. O CLI procura,
nesta ordem, `GH_TOKEN`, `GITHUB_TOKEN` e a sessão retornada por
`gh auth token`; as credenciais não são gravadas pelo Specsfy.

Para trocar a origem ou uma restrição de versão, execute novamente
`uv tool install` com o novo requisito.

## Comandos

```bash
specsfy
specsfy install --project .
specsfy install --project . --detected
specsfy install --project . \
  --specialist specsfy-specialist-laravel \
  --specialist specsfy-specialist-postgres
specsfy skills list
specsfy skills detect --project .
specsfy skills add specsfy-specialist-laravel --project .
specsfy skills remove specsfy-specialist-laravel --project .
specsfy skills update --project .
specsfy progress --project .
specsfy progress --project . --json
specsfy progress --project . --watch
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

- **Home**: totais de specs, tarefas, checklists e progresso global;
- **Backlogs**: lista navegável à esquerda e preview Markdown formatado à
  direita;
- **Specs**: tabela detalhada com gates e progresso de cada especificação;
  destaque uma linha e pressione `Espaço` para abrir a spec completa em um
  modal Markdown rolável, retornando à listagem com `Esc`;
- **Testes**: executa o Pest do projeto e separa o resultado entre as subabas
  **Resumo** e **Testes**, mantendo a saída detalhada rolável;
- **Skills**: catálogo tabular com plano, nome, categoria e estado, acompanhado
  por um painel de detalhes e resumo das alterações pendentes;
- **Sobre**: versão e finalidade do CLI.

Alterações em `specs/backlog/*.md`, `specs/specs/*/spec.md` e no
`skills-lock.json` são detectadas automaticamente.

Em projetos Laravel com Pest, `specsfy test --project .` detecta `artisan` e
`pestphp/pest`, executa `php artisan test` a partir da raiz selecionada,
transmite a saída e devolve o mesmo exit code. Na TUI, `Executar testes ^X`
mostra status, runner, comando, duração e resumo em uma subaba; a outra exibe
cada teste e falha. Relatórios Pest estruturados são convertidos em linhas
legíveis com arquivo, linha e mensagem.

O bootstrap instala as nove skills base, incluindo
`specsfy-base-update-spec` para pedidos surgidos depois da definição,
`specsfy-setup`,
`specsfy-documentator` e as três skills `specsfy-aux-*`, publica as regras em
`.specsfy/Spec.md`, o template em `.specsfy/templates/Spec.md`, um exemplo em
`.specsfy/examples/Spec.md` e mescla blocos gerenciados em `AGENTS.md` e
`CLAUDE.md`, preservando as instruções do usuário. Instalações repetidas são
idempotentes. O lock registra fingerprints: versões intactas podem ser
atualizadas, mas conteúdo gerenciado customizado localmente só é substituído ou
removido com `--force`.

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
skills `specsfy-base-*`, `specsfy-aux-*` e `specsfy-specialist-*`. Skills externas
presentes no mesmo lock não aparecem na interface e nunca são removidas ou
alteradas. O `.specsfy/skills-lock.json`
mantém os fingerprints usados pelo Specsfy para impedir que uma atualização
descarte alterações locais.

Na aba Skills, o botão `Atualizar ^R` baixa as origens atuais e atualiza de uma
vez todas as skills Specsfy instaladas. O comando equivalente é
`specsfy skills update --project .`; customizações locais continuam protegidas e
só podem ser substituídas explicitamente com `--force` no comando.

## Atualização do CLI gerenciada pelo uv

Ao abrir `specsfy` ou `specsfy tui` em um terminal interativo, o CLI consulta
as tags semânticas estáveis do monorepo. A consulta é limitada pelo cache
global `~/.specsfy/cli.json`, cujo intervalo padrão é de 24 horas. Falha de rede
ou do GitHub nunca impede a abertura do dashboard.

Quando existe versão mais recente, o CLI mostra as versões atual e disponível e
pergunta antes de atualizar. Uma resposta negativa abre a aplicação normalmente.
Uma resposta positiva delega a atualização ao comando
`uv tool upgrade specsfy-cli`, que gerencia o ambiente isolado e preserva a
origem registrada durante a instalação. O processo então fecha; abra `specsfy`
novamente para iniciar a versão instalada.

O arquivo global usa permissão `0600`, preserva chaves desconhecidas e separa:

- `settings.check_updates_on_startup`;
- `settings.check_interval_seconds`;
- `cache.last_checked_at`, tag, versão, commit, ETag e eventual erro recente.

Para publicar uma versão atualizável a partir do workspace de desenvolvimento,
use a skill local `$specsfy-release-cli`. Ela promove as notas confirmadas para
o [`CHANGELOG.md`](CHANGELOG.md), atualiza as versões do pacote e o lock,
reconstrói os artefatos versionados, cria a tag anotada `v<versão>` no mesmo
commit e usa exatamente a seção promovida como corpo do GitHub Release. O CI
valida o build e a correspondência da tag.

Novas specs usam `specs/specs/<NNNN>-<slug>/spec.md`; ideias ainda superficiais
ficam em `specs/backlog/<NNNN>-<slug>.md`. O dashboard mantém leitura do layout
legado. A skill de especificação renderiza cada arquivo novo a partir do
template instalado. O CLI recusa instalação na raiz do monorepo oficial.

## Executável versionado

O executável empacotado fica em `bin/specsfy` e não depende do checkout para
rodar. Reconstrua-o depois de qualquer alteração neste módulo:

```bash
./scripts/build-executable.sh
```

`bin/specsfy.build.json` registra o fingerprint dos inputs. A suíte de testes
falha quando o artefato não corresponde ao estado atual.

## Atalhos da TUI

- `Ctrl+Q`: sair;
- `Ctrl+U`: atualizar;
- `Ctrl+D`: detectar recomendações;
- `Ctrl+B`: selecionar todas as skills do framework;
- `Ctrl+E`: alternar o plano da skill destacada;
- `Ctrl+M` / `Ctrl+L`: marcar ou limpar os itens visíveis;
- `Ctrl+A`: aplicar;
- `Ctrl+R`: atualizar todas as skills Specsfy instaladas;
- `Ctrl+T`, `Ctrl+I`, `Ctrl+C`: filtros Todas, Instaladas e Recomendadas;
- `Ctrl+H`, `Ctrl+G`, `Ctrl+S`, `Ctrl+K`, `Ctrl+O`: Home, Backlogs, Specs,
  Skills e Sobre.
- `Ctrl+J`: abre Testes;
- `Ctrl+X`: executa os testes do projeto;
- `Espaço`: abre a spec destacada ou alterna a skill destacada, conforme a aba;
- `Esc`: fecha o modal da spec ou volta para Home.

Cada botão mostra seu atalho no próprio rótulo. `Tab` e `Shift+Tab` percorrem
os controles e as setas navegam as tabelas. Na aba Skills, `Enter` ou `Espaço`
alternam o plano entre instalar, manter, remover e ignorar; na aba Specs, abrem
o modal da linha destacada. `Esc` retorna, e o mouse opera abas, linhas e
botões. Nada é instalado ou removido antes de `Aplicar`.

A documentação completa está em [`docs/`](../docs/).

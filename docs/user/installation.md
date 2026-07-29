# Instalação do Specsfy

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | instalação do CLI e do framework em um projeto consumidor |
| Autoridade | interfaces públicas de `cli/` e `skills/` |

## Baixe o CLI

O executável do Specsfy é um aplicativo Python empacotado e requer Python 3.11
ou superior. O download oficial fica em `get.specsfy.dev`. Os comandos abaixo
salvam o arquivo em `$HOME/.local/bin`, uma pasta comum para executáveis do
próprio usuário:

```bash
mkdir -p "$HOME/.local/bin"
curl -fL get.specsfy.dev -o "$HOME/.local/bin/specsfy"
chmod +x "$HOME/.local/bin/specsfy"
```

Execute `specsfy --version` para confirmar que o sistema localiza o arquivo e
que o Python consegue abrir o aplicativo. A saída esperada é o número da versão
instalada:

```bash
specsfy --version
```

Uma resposta com o número da versão confirma a instalação. Se o terminal
mostrar `specsfy: command not found`, acrescente a pasta ao `PATH` da sessão e
repita a conferência:

```bash
export PATH="$HOME/.local/bin:$PATH"
specsfy --version
```

Para manter o caminho disponível em novos terminais, registre o mesmo `export`
no arquivo de configuração do seu shell. Em Bash, o arquivo costuma ser
`~/.bashrc`. Em Zsh, use `~/.zshrc`.

## Prepare o projeto consumidor

Abra a raiz do repositório que receberá a metodologia. Não execute a instalação
dentro do monorepo oficial do Specsfy, porque o CLI reconhece essa raiz como
ambiente de desenvolvimento e recusa a operação:

```bash
cd caminho/do/projeto
specsfy install --project .
```

O instalador publica as etapas numeradas a partir de
`.agents/skills/specsfy-01-inbox`, grava o contrato central em
`.specsfy/Spec.md` e adiciona templates, exemplos e registros técnicos em
`.specsfy/`. Ele também insere blocos gerenciados em `AGENTS.md` e `CLAUDE.md`,
preservando o conteúdo que já existe fora desses blocos.

Para personalizar um template sem impedir atualizações, copie-o para
`.specsfy/templates/custom/` com o mesmo nome. Essa versão tem precedência e
nunca é sobrescrita pelo instalador, inclusive com `--force`.

A instalação inclui as nove skills base, o setup, o documentador do sistema e as
três skills auxiliares. Ela prepara os arquivos usados pelo agente, mas não cria
uma spec de produto nem altera o código da aplicação.

## Confira os arquivos instalados

Na mesma raiz, liste o catálogo e consulte o progresso. O primeiro comando deve
mostrar as skills instaladas, e o segundo deve conseguir ler o diretório de
specs:

```bash
specsfy skills list
specsfy progress --project .
```

O catálogo deve mostrar as skills do Specsfy. Em um projeto novo, o comando de
progresso pode retornar zero specs. Esse resultado confirma que o CLI leu o
repositório e ainda não encontrou arquivos em
`specs/specs/<NNNN>-<slug>/spec.md`.

O comando sem subcomando abre a interface visual no diretório atual. O nome do
projeto aparece no topo e as abas devem carregar mesmo quando ainda não houver
spec:

```bash
specsfy
```

O dashboard deve carregar as abas do projeto mesmo quando as tabelas ainda
estiverem vazias. Use `Ctrl+Q` para sair.

## Atualize sem perder customizações

Para atualizar apenas o CLI, repita o download e a permissão de execução:

```bash
curl -fL get.specsfy.dev -o "$HOME/.local/bin/specsfy"
chmod +x "$HOME/.local/bin/specsfy"
specsfy --version
```

Para atualizar as skills já instaladas, execute `skills update`. O CLI compara
os fingerprints e preserva os arquivos customizados:

```bash
specsfy skills update --project .
```

O Specsfy registra fingerprints dos arquivos gerenciados. Uma atualização
normal substitui versões intactas e preserva arquivos customizados. Se o CLI
informar que encontrou alterações locais, revise a diferença. `--force`
descarta a customização protegida no arquivo indicado.

## Corrija falhas comuns

- **Comando ausente:** confirme que `$HOME/.local/bin` está no `PATH` e abra
  outro terminal depois de atualizar o arquivo do shell.
- **Python incompatível:** execute `python3 --version`. O aplicativo requer
  Python 3.11 ou uma versão mais recente.
- **Permissão negada:** execute novamente
  `chmod +x "$HOME/.local/bin/specsfy"` e confira se o arquivo pertence ao seu
  usuário.
- **Instalação das skills interrompida:** disponibilize o comando `skills` ou
  o `npx`, usado pelo CLI como alternativa.
- **Arquivo gerenciado customizado:** preserve sua versão ou compare as
  mudanças oficiais e só então repita o comando com `--force`.

Com o ambiente conferido, siga o [primeiro projeto](getting-started.md) para
criar uma entrega pequena e observar a primeira `spec.md`. O
[guia do CLI e da TUI](cli.md) detalha os comandos de atualização, progresso,
testes e configuração.

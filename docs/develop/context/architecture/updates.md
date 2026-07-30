# Atualização remota do CLI

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | descoberta, consentimento e instalação de versões do CLI |
| Autoridade | limites de rede, cache, confiança e fallback do updater |

## Papel

Definir como o CLI descobre tags publicadas, oferece uma atualização e delega
ao npm o gerenciamento do pacote global sem tornar rede ou GitHub requisitos
para abrir a aplicação.

## Como usar

Leia ao alterar a origem das versões, o cache global, o comando do npm, o
prompt inicial, o intervalo de consulta ou a forma de publicação.

## Atualize quando

- a API, o repositório ou o formato de tag mudar.
- o nome do pacote ou mecanismo de atualização mudar.
- dados globais, timeout, consentimento ou fallback mudar.

## Não use para

- atualizar skills ou dependências do projeto consumidor.
- instalar versão sem consentimento explícito.
- guardar token, conteúdo de projeto ou dado pessoal no cache.

## Fonte da verdade e precedência

O código e os testes de `cli/` implementam esta política. Tags selecionam
versões publicadas. O npm resolve e instala o pacote global. O cache apenas
reduz consultas e nunca autoriza uma instalação.

## Fluxo

1. Ao abrir a TUI interativa, o CLI lê ou cria `~/.specsfy/cli.json`.
2. Se o intervalo venceu, obtém credencial de `GH_TOKEN`, `GITHUB_TOKEN` ou
   `gh auth token` e consulta as tags de `cli/` com timeout curto.
3. Considera somente tags estáveis `vMAJOR.MINOR.PATCH` e registra o SHA
   apontado como evidência da consulta.
4. Se a versão for superior, pede consentimento no terminal.
5. Ao aceitar, executa
   `npm install --global @promovaweb/specsfy@latest`.
6. Depois que o npm conclui, o CLI encerra para que a próxima abertura use o
   ambiente atualizado.
7. Recusa ou falha abre a aplicação atual normalmente.

## Cache e privacidade

O JSON global tem permissão `0600`, preserva chaves desconhecidas e separa
configurações de dados efêmeros. Ele pode guardar habilitação, intervalo,
horário, ETag, tag, versão, commit e erro recente. Não guarda credenciais,
telemetria nem conteúdo do projeto.

A credencial existe somente no ambiente do processo ou no armazenamento
governado pelo GitHub CLI. O Specsfy não a imprime nem a copia para seu cache.

## Distribuição e publicação

O pacote instalável é definido por `cli/package.json`, expõe o comando
`specsfy` e inclui suas dependências no lockfile. O download público do
executável usa `get.specsfy.dev`. A instalação gerenciada usa
`npm install --global @promovaweb/specsfy` e a atualização usa
`npm update --global @promovaweb/specsfy`. Uma tag atualizável aponta para o
commit cuja versão do pacote corresponde ao nome `v<versão>`, verificado pelo
CI antes da publicação no npm. A proveniência é acrescentada quando o
repositório estiver público, porque o registro exige uma origem pública para
essa atestação.

O executável Node versionado continua sendo um artefato de distribuição e
validação do repositório. Ele contém as dependências do CLI e usa o runtime
Node.js instalado na máquina.

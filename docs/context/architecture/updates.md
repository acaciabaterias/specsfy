# Atualização remota do CLI

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | descoberta, consentimento e instalação de versões do CLI |
| Autoridade | fronteira de rede, cache, confiança e fallback do updater |

## Papel

Definir como o CLI descobre tags publicadas, oferece uma atualização e delega
ao `uv` o gerenciamento do ambiente isolado sem tornar rede ou GitHub
requisitos para abrir a aplicação.

## Como usar

Leia ao alterar a origem das versões, o cache global, o comando do `uv`, o
prompt inicial, o intervalo de consulta ou a forma de publicação.

## Atualize quando

- a API, o repositório ou o formato de tag mudar;
- o nome do pacote ou mecanismo de atualização mudar;
- dados globais, timeout, consentimento ou fallback mudar.

## Não use para

- atualizar skills ou dependências do projeto consumidor;
- instalar versão sem consentimento explícito;
- guardar token, conteúdo de projeto ou dado pessoal no cache.

## Fonte da verdade e precedência

O código e os testes de `cli/` implementam esta política. Tags selecionam
versões publicadas; o ambiente, a origem e a resolução da ferramenta pertencem
ao `uv`; o cache apenas reduz consultas e nunca autoriza uma instalação.

## Fluxo

1. Ao abrir a TUI interativa, o CLI lê ou cria `~/.specsfy/cli.json`.
2. Se o intervalo venceu, consulta as tags de `cli/` com timeout curto.
3. Considera somente tags estáveis `vMAJOR.MINOR.PATCH` e registra o SHA
   apontado como evidência da consulta.
4. Se a versão for superior, pede consentimento no terminal.
5. Ao aceitar, executa `uv tool upgrade specsfy-cli`; o `uv` preserva a origem,
   as opções e as restrições registradas na instalação.
6. Depois que o `uv` conclui, o CLI encerra para que a próxima abertura use o
   ambiente atualizado.
7. Recusa ou falha abre a aplicação atual normalmente.

## Cache e privacidade

O JSON global tem permissão `0600`, preserva chaves desconhecidas e separa
configurações de dados efêmeros. Ele pode guardar habilitação, intervalo,
horário, ETag, tag, versão, commit e erro recente. Não guarda credenciais,
telemetria nem conteúdo do projeto.

## Distribuição e publicação

O pacote instalável é definido por `pyproject.toml`, expõe o comando `specsfy`
e inclui suas dependências no lockfile. A instalação pública usa
`uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'`; a atualização usa
`uv tool upgrade specsfy-cli`. Uma tag atualizável aponta para o commit cuja
versão do pacote corresponde ao nome `v<versão>`, verificado pelo CI.

O zipapp versionado continua sendo artefato de validação do repositório, mas
não é a unidade instalada nem substituída pelo fluxo gerenciado pelo `uv`.

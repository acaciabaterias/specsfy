# Changelog

Todas as mudanças relevantes do Specsfy CLI são registradas neste arquivo.

## [Unreleased]

## [0.7.0] - 2026-07-30

- Migra o CLI e a TUI de Python para Node.js 22, com instalação global por
  `@promovaweb/specsfy`.
- Mantém as seis abas da TUI e adiciona execução do Pest com resumo e saída
  rolável.
- Corrige os atalhos de controle interpretados pelo `neo-blessed` e evita o
  encerramento da TUI durante a atualização da saída dos testes.
- Adiciona o fluxo de release com changelog, commit, tag anotada, GitHub
  Actions, publicação npm e GitHub Release vinculados à mesma versão.
- Atualiza o instalador, o catálogo de especialistas e a documentação do
  usuário para os comandos do CLI em Node.js.

- Autentica catálogo e verificação de tags em repositórios privados com
  `GH_TOKEN`, `GITHUB_TOKEN` ou a sessão do GitHub CLI.
- Torna o fingerprint do executável estável entre permissões equivalentes do
  Git e ambientes locais/CI.

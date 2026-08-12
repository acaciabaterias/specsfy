# Changelog

Todas as mudanças relevantes do Specsfy CLI são registradas neste arquivo.

## [Unreleased]

## [0.8.1] - 2026-08-12

- Adiciona `specsfy doctor` e executa o mesmo diagnóstico antes do setup para
  conferir Node.js, Git, npm, projeto e disponibilidade do `skills` ou `npx`.
- Adiciona `specsfy update` para atualizar todas as skills Specsfy instaladas e
  preserva `specsfy skills update` como comando compatível.
- Adiciona `specsfy upgrade` para consultar uma versão estável mais recente e
  atualizar o próprio CLI pelo pacote oficial do npm sem fazer downgrade.
- Documenta separadamente instalação, atualização das skills e atualização do
  CLI nos guias, na referência de comandos, no ebook e no site.

## [0.8.0] - 2026-08-12

- Adiciona os comandos `transition`, `migrate` e `effort` para manter pasta,
  status e estimativa das specs pela mesma interface, com saída JSON e
  integração opcional com o ClickUpfy.
- Adiciona `milestones sync` para projetar o progresso dos milestones em
  `specs.md` e `specs/milestones/`, preservando o conteúdo escrito pelo
  usuário.
- Passa a ler o ciclo de vida em `specs/<estado>/`, mantém compatibilidade com
  o layout anterior e inclui Effort e perfil de execução no progresso.
- Amplia o bootstrap com as skills de entrevista e governança de milestones e
  mantém a instalação protegida por fingerprints.
- Reorganiza a paleta escura da TUI com cores semânticas e contraste verificado
  para texto, foco, seleção, bordas, campos, botões e barras de rolagem.
- Atualiza capturas, documentação de usuário e desenvolvimento, referência de
  comandos, ebook e publicação dos guias no site da Promovaweb.

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

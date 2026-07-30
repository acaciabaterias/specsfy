# Guia de desenvolvimento do Specsfy CLI

Este módulo possui o executável Node.js `specsfy`, a TUI e os testes de
instalação/progresso. Skills pertencem a `skills/` e
`specialists/`; documentação final pertence a `docs/`.

## Regras

- Instalar somente no projeto explicitamente selecionado.
- Nunca instalar skills na raiz do monorepo oficial.
- Delegar instalação a `skills add` de
  `https://github.com/vercel-labs/skills`, com destino universal em
  `.agents/skills`.
- Usar o `skills-lock.json` do instalador oficial para proveniência e
  `.specsfy/skills-lock.json` para fingerprints e proteção Specsfy.
- Ler a seleção instalada do `skills-lock.json` na raiz do consumidor e criar
  o lock vazio compatível (`{"version": 1, "skills": {}}`) quando ele faltar.
- Manter a TUI organizada nas abas Home, Backlogs, Specs, Testes, Skills e
  Sobre. A aba
  Backlogs usa lista e preview Markdown em duas colunas; a aba Skills usa
  busca, filtros, catálogo tabular, plano de alteração e painel de detalhes,
  exibindo e gerenciando exclusivamente `specsfy-setup`,
  `specsfy-documentator`, skills base, `specsfy-aux-*` e
  `specsfy-specialist-*`.
- Todo botão visível declara no próprio rótulo um atalho global `Ctrl+letra`.
- Toda a interface permanece navegável por setas, Tab/Shift+Tab, Esc, atalhos
  e mouse, com foco e seleção de alto contraste.
- Fazer downloads dos catálogos em diretório temporário antes de delegar a
  instalação.
- Nunca sobrescrever skill local sem `--force`.
- Não criar specs; ler `specs/specs/*/spec.md` para progresso e manter leitura
  compatível do layout legado `specs/*/spec.md`.
- Manter comandos não interativos equivalentes às ações da TUI.
- Testes não usam rede nem alteram repositório real.
- Toda mudança neste módulo deve executar `npm run build:executable` e
  versionar `bin/specsfy` e `bin/specsfy.build.json`. O teste de fingerprint
  reprova qualquer alteração não reconstruída.
- Releases estáveis usam `CHANGELOG.md` como fonte única das notas, atualizam
  `package.json`, `src/version.ts`, `package-lock.json` e os artefatos
  versionados no mesmo commit, criam a tag anotada `v<versão>` nesse commit e
  publicam a seção correspondente no GitHub Release.

## Validação

```bash
npm ci
npm run build:executable
npm run check
node dist/main.js --help
./bin/specsfy --version
```

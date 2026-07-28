# Documentação oficial do monorepo

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | descritivo |
| Escopo | manutenção da documentação do próprio Specsfy |
| Autoridade | fluxo da skill local; fontes executáveis prevalecem |

## Papel

Explicar como reconciliar os módulos do monorepo e publicar documentação
técnica e guias para usuários em `docs/`.

## Como usar

Acione `$specsfy-monorepo-documentator` somente na raiz de
[`promovaweb/specsfy`](https://github.com/promovaweb/specsfy). A skill confirma
o remoto e a raiz Git única antes de coletar evidências:

```bash
python3 -B .agents/skills/specsfy-monorepo-documentator/scripts/collect_monorepo_evidence.py \
  --workspace .
```

O coletor é somente leitura. Ele registra remoto, branch, commit, estado Git,
quantidade de arquivos rastreados e fontes estruturais disponíveis em cada
módulo. Um checkout parcial, outro remoto ou um projeto consumidor é recusado.

## Documentação técnica

Decisões transversais ficam em `context/`: finalidade, vocabulário, arquitetura,
módulos, dependências, stack, dados, fluxos e testes.

## Guias para usuários

Jornadas públicas ficam na raiz de `docs/`: instalação, uso básico, CLI,
backlog, contexto persistente, especialistas e manutenção do próprio projeto.

## Evidência e publicação

- Confirme cada afirmação na fonte do módulo.
- Use links relativos entre arquivos do monorepo.
- Publique documentação oficial em `docs/`.
- Execute testes focais dos módulos, a regressão integrada e revise o diff único.

A skill local vive em
[`/.agents/skills/specsfy-monorepo-documentator`](../.agents/skills/specsfy-monorepo-documentator/)
e não integra o catálogo instalado em consumidores. A skill
[`specsfy-documentator`](../skills/specsfy-documentator/) reconstrói
`<projeto>/docs/` de uma aplicação consumidora.

`$specsfy-release-cli` também é local. Ela versiona os artefatos em `cli/`,
cria uma tag no commit do monorepo e publica a seção correspondente do
`cli/CHANGELOG.md` no GitHub Release.

## Atualize quando

- a topologia, automação documental ou percurso público mudar.

## Não use para

- documentar uma aplicação consumidora;
- substituir specs ou fontes executáveis.

## Fonte da verdade e precedência

Fontes executáveis de cada módulo prevalecem; `docs/context/` governa decisões
transversais e os guias explicam interfaces públicas.

# Padrão da documentação oficial do hub

Leia esta referência local ao criar, mover ou reconciliar documentação do projeto
Specsfy. O repositório `specsfy/docs` publica dois percursos complementares.

## Documentação técnica

Use `docs/context/README.md` como roteador e mantenha cada decisão no menor
contexto que possua gatilho próprio.

| Assunto | Owner documental |
| --- | --- |
| finalidade, capacidades e limites | `docs/context/project.md` |
| vocabulário | `docs/context/glossary.md` |
| arquitetura e integrações | `docs/context/architecture/README.md` |
| módulos e ownership | `docs/context/architecture/modules.md` |
| dependências entre repositórios e componentes | `docs/context/architecture/dependencies.md` |
| stack, pacotes, convenções e testes | `docs/context/engineering/` |
| persistência, migrations e privacidade de dados | `docs/context/data/` |
| fluxos entre três ou mais componentes | `docs/context/flows/` |
| motivação histórica de decisão arquitetural | `docs/decisions/` |

Contexto técnico explica decisões transversais e precedência. Não copie
inventários de rotas, classes, versões ou schemas mantidos por fontes
executáveis.

## Guias para usuários

Mantenha a raiz de `docs/` orientada a tarefas reais.

| Jornada | Guia |
| --- | --- |
| entender e iniciar o método | `docs/README.md` |
| instalar o CLI e o framework no projeto consumidor | `docs/installation.md` |
| conduzir a primeira fatia | `docs/basic-usage.md` |
| atualizar uma spec depois da definição | `docs/update-spec.md` |
| operar seleção técnica e automação | `docs/advanced-usage.md` |
| atualizar e operar o CLI/TUI | `docs/cli.md` |
| aplicar o método em Laravel | `docs/laravel.md` |
| aplicar o método em Astro | `docs/astro.md` |
| aplicar o método em Next.js | `docs/nextjs.md` |
| capturar e promover ideias | `docs/backlog.md` |
| manter contexto do projeto consumidor | `docs/project-context.md` |
| consultar a documentação do sistema consumidor | `docs/system-documentation.md` |
| selecionar especialistas e contexto técnico opcional | `docs/specialists.md` |
| entender os owners do ecossistema | `docs/repositories.md` |
| consultar autoria e identidade | `docs/credits.md` |
| manter a documentação do próprio hub | `docs/hub-documentation.md` |

Um guia explica finalidade, pré-condições, sequência observável, resultado,
limites e fonte da verdade. Não exponha detalhes internos sem utilidade para a
jornada.

O guia `docs/installation.md` deriva a distribuição e os pré-requisitos do
repositório `specsfy/cli`, e deriva o conjunto do framework dos owners
`specsfy/cli` e `specsfy/skills`. O guia `docs/cli.md` aponta para essa
instalação e não mantém uma segunda sequência de bootstrap.

Os guias de stack derivam detecção, escopo e critérios técnicos de
`specsfy/specialists`; eles não repetem suas referências extensas nem
substituem a descoberta da versão e das convenções do projeto consumidor.

## Fontes por repositório

| Repositório | Evidência primária |
| --- | --- |
| `specsfy/dev` | `AGENTS.md` e contratos integrados em `tests/` |
| `specsfy/brand` | identidade e diretrizes publicadas pelo próprio owner |
| `specsfy/skills` | `SKILL.md`, scripts, referências e testes |
| `specsfy/docs` | contexto transversal e guias oficiais |
| `specsfy/example` | aplicação e documentação operacional de validação |
| `specsfy/specsfy` | visão geral pública e entrada do projeto |
| `specsfy/specialists` | catálogo, skills técnicas e testes |
| `specsfy/cli` | código, manifests, testes e interface pública |

Classifique afirmações antes de publicá-las:

- `confirmada`: sustentada pela fonte proprietária atual;
- `inferida`: conclusão útil, rotulada e ligada à evidência;
- `conflitante`: fontes autorizadas divergem; não escolha silenciosamente;
- `ausente`: falta evidência; registre a lacuna sem preencher por plausibilidade.

## Reconciliação

1. Identificar os repositórios afetados pelo assunto.
2. Ler instruções e evidências somente nesses owners.
3. Atualizar contexto técnico quando uma decisão transversal mudou.
4. Atualizar guia quando uma jornada ou interface pública mudou.
5. Atualizar ambos quando a mesma mudança altera arquitetura e uso.
6. Validar links, testes e status Git por raiz.
7. Registrar quando não houver impacto documental material, sem criar conteúdo
   artificial.

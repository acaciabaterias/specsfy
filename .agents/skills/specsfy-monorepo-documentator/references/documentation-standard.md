# Padrão da documentação oficial

O módulo `docs/` publica dois percursos complementares do monorepo Specsfy.
Eles cobrem arquitetura, módulos, dependências, stack, dados, fluxos, testes,
instalação, método, CLI, contexto, especialistas e documentação do sistema.

## Documentação técnica

Use `docs/context/README.md` como roteador.

| Assunto | Owner documental |
| --- | --- |
| finalidade, capacidades e limites | `docs/context/project.md` |
| vocabulário | `docs/context/glossary.md` |
| arquitetura e integrações | `docs/context/architecture/README.md` |
| módulos e ownership | `docs/context/architecture/modules.md` |
| dependências entre componentes | `docs/context/architecture/dependencies.md` |
| stack, pacotes, convenções e testes | `docs/context/engineering/` |
| persistência, migrations e privacidade | `docs/context/data/` |
| fluxos entre três ou mais componentes | `docs/context/flows/` |
| motivação histórica | `docs/decisions/` |

## Guias para usuários

| Jornada | Guia |
| --- | --- |
| entender e iniciar o método | `docs/README.md` |
| instalar o CLI e o framework | `docs/installation.md` |
| conduzir a primeira fatia | `docs/basic-usage.md` |
| atualizar uma spec | `docs/update-spec.md` |
| operar seleção técnica | `docs/advanced-usage.md` |
| atualizar e operar o CLI/TUI | `docs/cli.md` |
| aplicar em Laravel | `docs/laravel.md` |
| aplicar em Astro | `docs/astro.md` |
| aplicar em Next.js | `docs/nextjs.md` |
| capturar e promover ideias | `docs/backlog.md` |
| manter contexto consumidor | `docs/project-context.md` |
| consultar documentação gerada | `docs/system-documentation.md` |
| selecionar especialistas | `docs/specialists.md` |
| entender os módulos | `docs/repositories.md` |
| consultar autoria e identidade | `docs/credits.md` |
| manter a documentação oficial | `docs/monorepo-documentation.md` |

O guia de instalação deriva sua interface de `cli/` e o framework de `skills/`.
Os guias técnicos derivam a descoberta de `specialists/`.

## Fontes por módulo

| Módulo | Evidência primária |
| --- | --- |
| raiz | `AGENTS.md`, automação e contratos integrados |
| `brand/` | identidade e diretrizes |
| `skills/` | `SKILL.md`, scripts, referências e testes |
| `docs/` | contexto transversal e guias |
| `example/` | aplicação e documentação operacional |
| `specsfy/` | tutorial público detalhado |
| `specialists/` | catálogo, skills e testes |
| `cli/` | código, manifests, testes e interface pública |

## Reconciliação

1. Identificar os módulos afetados.
2. Ler instruções e evidências nesses módulos.
3. Atualizar contexto técnico quando uma decisão transversal mudou.
4. Atualizar guia quando uma jornada pública mudou.
5. Atualizar ambos quando arquitetura e uso mudaram.
6. Validar links, testes e o status único do monorepo.

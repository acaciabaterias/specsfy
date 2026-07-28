# Documentação técnica do sistema

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | descritivo |
| Escopo | documentação derivada no projeto consumidor |
| Autoridade | uso de `specsfy-documentator`; código e fontes normativas prevalecem |

## Papel

Explicar como reconstruir uma visão técnica completa de uma aplicação existente
em `<projeto>/docs/`. Essa documentação pertence ao projeto consumidor e não se
confunde com este repositório, que documenta a metodologia Specsfy.

## Como usar

Execute `$specsfy-documentator` livremente para documentar um sistema legado ou
atualizar sua visão técnica. O handoff também é obrigatório depois de cada
tarefa de código concluída por `$specsfy-base-implement`.

A skill lê o código completo, manifests, locks, rotas, migrations, testes,
configuração e o contexto persistente. Cada execução reconstrói blocos
delimitados nos seguintes arquivos, preservando texto humano externo:

| Arquivo no consumidor | Conteúdo |
| --- | --- |
| `docs/README.md` | portal e ordem de leitura |
| `docs/architecture.md` | componentes, dependências e UML Mermaid |
| `docs/application.md` | módulos e implementações observadas |
| `docs/database.md` | entidades, campos, relações e `erDiagram` |
| `docs/flows.md` | rotas, `flowchart` e `sequenceDiagram` |
| `docs/testing.md` | runners, comandos, inventário e resumo |
| `docs/frontend.md` | views, páginas, componentes, React e Tailwind |
| `docs/packages.md` | runtime, framework, nativos, integrados e terceiros |
| `docs/integrations.md` | serviços externos e nomes de configuração |
| `docs/decisions.md` | decisões explícitas e suas fontes |

Laravel inclui rotas, controllers, models, services, jobs, policies, Blade,
migrations e Pest/PHPUnit. Node, Next.js, React e Astro incluem páginas, APIs,
componentes, módulos, scripts e Vitest, Jest ou Node Test quando observados.
Pacotes registram versão e link do repositório GitHub; quando a fonte não puder
ser confirmada localmente, a saída usa uma busca rotulada e não inventa URL.

Depois da reconstrução, a própria skill executa:

```bash
python3 -B .agents/skills/specsfy-documentator/scripts/build_documentation.py \
  --project . --check
```

O monitor do setup também bloqueia a entrega quando código de aplicação ou
persistência mudou e nenhum arquivo de `docs/` foi reconstruído.

## Atualize quando

- a topologia documental gerada mudar;
- um framework, runner, diagrama ou classe de inventário passar a ser coberto;
- o handoff entre implementação, monitor e documentador mudar.

## Não use para

- substituir `spec.md`, `PROJECT.md` ou arquivos `.specsfy/`;
- copiar segredos, valores de ambiente, dados de produção ou código integral;
- declarar uma inferência como decisão confirmada;
- manter documentação oficial da metodologia dentro do projeto consumidor.

## Fonte da verdade e precedência

O código, os testes, os manifests, os schemas e as migrations comprovam o estado
implementado. A spec governa o comportamento da fatia; `PROJECT.md` e
`.specsfy/` preservam o contexto transversal do consumidor. Os arquivos em
`<projeto>/docs/` são uma projeção reconstruível dessas fontes.

# Guia do workspace Specsfy Dev

Este `AGENTS.md` governa o workspace orquestrador em
`/home/luizeof/specsfy`. Ele coordena repositórios independentes; não transforma
o conjunto em monorepo e não atribui ao pai o ownership dos filhos.

## Fronteiras Git

| Caminho | Raiz Git | Ownership |
| --- | --- | --- |
| `./` | `specsfy/dev` | orquestração, specs e testes integrados |
| `brand/` | `specsfy/brand` | identidade visual e verbal |
| `skills/` | `specsfy/skills` | metodologia executável e skills |
| `docs/` | `specsfy/docs` | documentação final para o usuário |
| `specsfy/` | `specsfy/specsfy` | porta de entrada e visão geral pública |

- Execute `git status`, `git diff`, commits e branches na raiz proprietária.
- Considere mudanças transversais como uma entrega coordenada com commits
  independentes.
- Não adicione os filhos ao índice de `dev`, não crie `.gitmodules` e não
  converta a árvore em submódulos sem uma nova decisão normativa.
- Links dentro da mesma raiz Git são relativos. Links entre repositórios usam
  `https://github.com/specsfy/<repositorio>`.
- Preserve alterações preexistentes em qualquer uma das cinco worktrees.

## Fonte da verdade

- Cada fatia vertical possui uma única fonte normativa em
  `specs/<slug>/spec.md` no workspace de desenvolvimento.
- Pesquisa consultada fica somente em `specs/<slug>/research/` e deve ser
  indexada na spec.
- A metodologia executável vive em `skills/`; siga `skills/AGENTS.md`, publicado
  como
  [`AGENTS.md` de specsfy/skills](https://github.com/specsfy/skills/blob/main/AGENTS.md)
  ao alterar uma skill.
- A documentação oficial da metodologia para usuários vive em `docs/`.
- A aplicação interna de validação e sua documentação operacional vivem em
  `example/` e pertencem à raiz Git `specsfy/dev`.
- A visão geral pública vive em `specsfy/`.
- A identidade vive em `brand/`.
- Testes, manifests e configurações comprovam o estado implementado em sua raiz
  proprietária.

Não crie `plan.md`, `tasks.md`, `research.md`, `data-model.md` ou outra fonte
normativa paralela.

## Disciplina documental

- Toda criação ou alteração deve atualizar, na mesma entrega, a documentação
  aplicável dentro do owner e do escopo corretos.
- Quando não houver impacto documental material, registre essa avaliação na
  evidência da tarefa em vez de criar conteúdo artificial.
- Documentação deriva das fontes executáveis e não transforma README, contexto
  ou guia em inventário concorrente de manifests, rotas, schemas ou testes.
- Detalhes internos de `example/` permanecem em `example/README.md`; somente
  decisões transversais da metodologia pertencem a `docs/`.

## Contexto compartilhado

Use `docs/context/README.md`, publicado como
[`roteador de contexto`](https://github.com/specsfy/docs)
como ponto de entrada. Leia a `spec.md` ativa, estas instruções e apenas os
contextos exigidos pela mudança.

| Alteração | Contexto mínimo |
| --- | --- |
| finalidade ou vocabulário | `docs/context/project.md` e `docs/context/glossary.md` |
| visão arquitetural ou integrações | `docs/context/architecture/README.md` |
| módulos e responsabilidades | `docs/context/architecture/modules.md` |
| direção das dependências | `docs/context/architecture/dependencies.md` |
| tecnologias estruturais | `docs/context/engineering/stack.md` |
| pacotes e dependências | `docs/context/engineering/packages.md` |
| padrões de implementação | `docs/context/engineering/conventions.md` |
| estratégia de testes | `docs/context/engineering/testing.md` |
| persistência e ownership de dados | `docs/context/data/persistence.md` |
| migrations sem mecanismo próprio | `docs/context/data/README.md` |
| privacidade, retenção ou exposição | `docs/context/data/privacy.md` |
| fluxo entre módulos | `docs/context/flows/README.md` |
| decisão arquitetural histórica | `docs/decisions/README.md` |

Atualize o contexto afetado na mesma entrega que altera uma decisão transversal.
Em divergência, preserve o estado observado e siga a precedência declarada no
roteador.

## Fluxo de uma mudança

1. Identifique a spec e as raízes Git afetadas.
2. Inspecione instruções, contexto, status e diff de cada raiz.
3. Atualize comportamento, Gherkin, requisitos, tarefas e gates na mesma spec.
4. Materialize BDD e TDD e observe RED antes da mudança derivada.
5. Edite cada arquivo somente na raiz que possui sua responsabilidade.
6. Execute testes focais na raiz proprietária e regressão no workspace.
7. Registre evidência e avance os checklists conforme cada resultado acontece.
8. Revise status e diff das cinco raízes antes de concluir.

Mudança de comportamento reabre os Atos I–III. Mudança de plano reabre os Atos
II–III. Nenhum gate posterior permanece válido sobre uma entrada alterada.

## Três atos

- **Ato I — Definir:** descobrir intenção, requisitos e Gherkin; termina com
  `Definition Gate: Passed`.
- **Ato II — Projetar e provar:** decompor tarefas, materializar BDD/TDD e
  comprovar RED; termina com `Plan Gate: Passed`.
- **Ato III — Entregar e validar:** produzir GREEN, executar regressão e
  registrar evidência; termina com `Delivery Gate: Passed`.

O estado canônico é
`Draft → Defined → Planned → Implementing → Complete`.

## Validação

Use `python3 -B` ou `PYTHONDONTWRITEBYTECODE=1` para não criar caches.

```bash
python3 -B .agents/skills/specsfy-validate/scripts/validate_spec.py \
  specs/<slug>/spec.md
python3 -B .agents/skills/specsfy-tasks/scripts/validate_tasks.py \
  specs/<slug>/spec.md
python3 -B .agents/skills/specsfy-tdd-bdd/scripts/check_traceability.py \
  specs/<slug>/spec.md . --kinds FR,AC,NFR
python3 -B -m unittest discover -s tests -p 'test_*.py'
uv run --quiet --with behave behave tests/features --no-capture
python3 -B .agents/skills/specsfy-validate/scripts/verify_repo.py . \
  --boundary local
```

Valide também cada skill alterada:

```bash
uv run --quiet --with pyyaml python \
  /home/luizeof/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/<nome>
```

## Critério de entrega

- o owner de cada arquivo está correto;
- links locais não atravessam uma raiz Git;
- links públicos usam a organização `specsfy`;
- BDD e TDD tiveram RED válido e estão verdes;
- regressão e rastreabilidade passaram;
- nenhum cache, placeholder ou arquivo normativo paralelo foi criado;
- os cinco itens de cada tarefa e os gates possuem evidência atual;
- cada repositório alterado foi revisado separadamente.

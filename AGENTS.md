# Guia de desenvolvimento das skills

Este `AGENTS.md` governa todo o repositório. O projeto desenvolve uma metodologia
prática de software baseada em especificação, exemplos executáveis, testes antes
da implementação e evidência de conclusão.

## Fonte da verdade

- Cada fatia vertical possui uma única fonte normativa em
  `specs/<slug>/spec.md`.
- Pesquisa consultada fica em `specs/<slug>/research/` e deve ser indexada na
  spec. Não crie `plan.md`, `tasks.md`, `research.md` ou `data-model.md`.
- Mecanismos reutilizáveis vivem apenas em `.agents/skills/<nome>/`.
- Código, testes e documentos publicados por uma skill são artefatos derivados;
  seus requisitos e evidências permanecem na spec.

## Contexto compartilhado

Use [`docs/context/README.md`](docs/context/README.md) como roteador. Leia apenas
os contextos indicados para o tipo de alteração, além da `spec.md` ativa e das
instruções aplicáveis ao caminho.

| Alteração | Contexto mínimo |
|---|---|
| finalidade ou vocabulário | `docs/context/project.md` e `docs/context/glossary.md` |
| visão arquitetural ou integrações | `docs/context/architecture/README.md` |
| módulos e responsabilidades | `docs/context/architecture/modules.md` |
| direção das dependências | `docs/context/architecture/dependencies.md` |
| tecnologias estruturais | `docs/context/engineering/stack.md` |
| pacotes e dependências | `docs/context/engineering/packages.md` |
| padrões de implementação | `docs/context/engineering/conventions.md` |
| estratégia de testes | `docs/context/engineering/testing.md` |
| persistência e ownership | `docs/context/data/persistence.md` |
| migrations sem mecanismo próprio | `docs/context/data/README.md` |
| privacidade, retenção ou exposição | `docs/context/data/privacy.md` |
| fluxo entre módulos | `docs/context/flows/README.md` |
| decisão arquitetural histórica | `docs/decisions/README.md` |

- Atualize o contexto afetado na mesma entrega que altera uma decisão transversal.
- Não carregue toda a árvore por padrão; siga os gatilhos `Leia quando`.
- Não copie requisitos de feature, versões ou schemas para os contextos.
- Em divergência, preserve o estado observado e siga a precedência declarada no roteador.

## Três atos por fatia vertical

### Ato I — Definir

Descobrir problema, finalidade, atores, linguagem, regras, limites e efeitos.
Aplicar BDD como técnica de descoberta e escrever Gherkin. O ato termina quando
não existe dúvida P1 e o `Definition Gate` está `Passed`.

Skills principais: `specsfy-discuss`, `specsfy-specify` e `specsfy-validate`.

### Ato II — Projetar e provar

Definir arquitetura, dados, migrations, models, controllers, views, queries,
APIs, riscos e rollback. Decompor em tarefas verticais com dependências
explícitas; então materializar os predecessores `.feature` e TDD e observar RED
antes de criar ou alterar implementação. O ato termina com `Plan Gate: Passed`.

Skills principais: `specsfy-tdd-bdd` no modo `prepare` e `specsfy-tasks`.

### Ato III — Entregar e validar

Executar cada tarefa no ciclo `READY → RED → GREEN → VERIFIED → DONE`. Rodar
aceite Gherkin, TDD, regressão, rastreabilidade e validadores. O ato termina com
`Delivery Gate: Passed`, todas as tarefas fechadas e `Status: Complete`.

Skills principais: `specsfy-implement`, `specsfy-tdd-bdd` e
`specsfy-progress`.

Uma mudança no comportamento reabre os atos I–III. Uma mudança no plano reabre
os atos II–III. Nenhum gate posterior permanece válido sobre uma decisão
anterior alterada.

O estado canônico é
`Draft → Defined → Planned → Implementing → Complete`. A transição entre atos é
um handoff verificável, não apenas uma mudança editorial.

## MCR-10

`specsfy-discuss` e `specsfy-specify` usam a referência canônica
`.agents/skills/specsfy-specify/references/mcr-10.md`.

Antes de perguntar:

1. preserve a formulação original;
2. distinga o pedido literal da finalidade desejada;
3. identifique termos ambíguos, equivalentes e derivados;
4. analise silenciosamente as dez categorias aplicáveis;
5. marque informação como declaração, inferência, hipótese, decisão, conflito
   ou aberto;
6. selecione a lacuna P1 de maior impacto e incerteza.

Faça uma pergunta por vez e use a linguagem do usuário. As categorias são lentes
do agente, não um questionário a ser recitado. Não prometa descobrir um estado
mental: formule a intenção operacional, mostre a síntese e peça confirmação.

As categorias recebem adaptações modernas para domínio, cardinalidade,
qualidade, relações, contexto, tempo, estados, capacidades, comandos e efeitos.
Finalidade, evidência, risco, privacidade, observabilidade e reversibilidade são
preocupações adicionais do método, não categorias atribuídas a Aristóteles.

### Aprendizados de design

- Cobertura categorial não prova completude nem substitui o aceite.
- Finalidade vem antes das categorias para separar problema e solução sugerida.
- Posição, posse e afecção são analogias operacionais ao tratar estado,
  autorização e efeitos em software.
- `P1/P2/P3` prioriza perguntas de descoberta, não histórias do backlog.
- Uma fila interna pode conter várias lacunas, mas a conversa apresenta uma por
  vez e recalcula as demais após cada resposta.
- Declaração, inferência e decisão nunca são intercambiáveis.

## Responsabilidade das skills

| Skill | Responsabilidade | Não deve fazer |
|---|---|---|
| `specsfy-discuss` | descobrir intenção e decisões em diálogo | escrever arquivos por padrão |
| `specsfy-specify` | consolidar `spec.md` e research | implementar ou criar backlog externo |
| `specsfy-validate` | auditar prontidão sem editar por padrão | decidir requisitos pelo usuário |
| `specsfy-tdd-bdd` | materializar BDD/TDD e provar RED/GREEN | inventar comportamento |
| `specsfy-tasks` | manter tarefas nas seções 14–15 | criar `tasks.md` ou código |
| `specsfy-implement` | executar tarefa pronta e registrar evidência | trabalhar sem BDD/TDD RED |
| `specsfy-progress` | projetar o estado global sem escrita | alterar gates ou checkboxes |

Descrições devem ter fronteiras claras. Se duas skills puderem responder ao
mesmo gatilho, ajuste `description` e a seção de limites antes de publicar.

## Estrutura de uma skill

```text
.agents/skills/<nome>/
  SKILL.md
  agents/openai.yaml
  scripts/       # automação determinística, quando necessária
  references/    # conhecimento consultado pelo agente
  assets/        # templates e materiais usados na saída
```

- `SKILL.md` deve ter frontmatter com `name` e `description`, menos de 500 linhas
  e instruções imperativas.
- `agents/openai.yaml` deve conter prompt padrão que mencione `$<nome>`.
- Coloque detalhes extensos em referências de um nível e indique exatamente
  quando lê-las.
- Mantenha uma fonte canônica; não copie a mesma referência entre skills.
- Scripts usam Python 3 e biblioteca padrão, retornam códigos úteis e não fazem
  rede, instalação global ou ação destrutiva por padrão.

## Criar ou alterar uma skill

1. Atualize `specs/<slug>/spec.md` com comportamento, Gherkin, requisitos,
   tarefas e gates.
2. Escreva o cenário BDD e o teste TDD de contrato.
3. Execute ambos e registre RED causado pelo comportamento ausente.
4. Para skill nova, use o `skill-creator`:

```bash
python3 /home/luizeof/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  <nome> --path .agents/skills
```

5. Faça a menor alteração que satisfaça o contrato.
6. Execute testes focais, refatore e repita a regressão.
7. Atualize imediatamente `PREP`, `EXECUTE`, `VERIFY`, `EVIDENCE` e `IMPROVE`
   na tarefa correspondente.
8. Valide a skill e a fonte única.

Não existe implementação “pequena demais” para BDD/TDD. Ajuste a profundidade do
teste ao risco, mas não pule RED.

## Comandos de validação

```bash
python3 -B .agents/skills/specsfy-validate/scripts/validate_spec.py \
  specs/<slug>/spec.md
python3 -B .agents/skills/specsfy-tasks/scripts/validate_tasks.py \
  specs/<slug>/spec.md
python3 -B .agents/skills/specsfy-tdd-bdd/scripts/check_traceability.py \
  specs/<slug>/spec.md . --kinds FR,AC,NFR
python3 -B -m unittest discover -s tests -p 'test_*.py'
uv run --quiet --with behave behave tests/features --no-capture
uv run --quiet --with pyyaml python \
  /home/luizeof/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  .agents/skills/<nome>
python3 -B .agents/skills/specsfy-progress/scripts/progress.py .
python3 -B .agents/skills/specsfy-validate/scripts/verify_repo.py . \
  --boundary local
```

Use `PYTHONDONTWRITEBYTECODE=1` ou `python3 -B` para não deixar caches dentro das
skills.

## Critério de publicação

Antes de declarar uma skill pronta:

- frontmatter e metadata são válidos;
- não existem placeholders, caches ou links quebrados;
- gatilhos positivos e limites negativos estão claros;
- referências possuem origem, data e distinção entre fonte e adaptação;
- BDD e TDD tiveram RED válido e estão verdes;
- a regressão completa passou;
- requisitos e testes estão rastreáveis;
- tarefas e cinco itens de cada checklist estão concluídos;
- `specsfy-progress` não mostra blocker.

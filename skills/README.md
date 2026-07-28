# Specsfy Skills

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../brand/logo/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../brand/logo/logo-light.svg">
    <img src="../brand/logo/logo-light.svg" alt="Logo oficial do Specsfy" width="180">
  </picture>
</p>

Este módulo do monorepo mantém a metodologia executável do
Specsfy: skills, scripts determinísticos, referências, assets e metadata para
agentes.

A visão geral para o usuário final está em
[`specsfy/`](../specsfy/). A documentação de uso
está em [`docs/`](../docs/).

## Responsabilidade

Este módulo possui:

- as instruções operacionais das dez skills base, do setup, do documentador e
  das três auxiliares;
- os templates de ideia, backlog, spec e tarefas em `templates/`;
- um documento preenchido e não normativo em `examples/Spec.md`;
- o MCR-10 e referências dos gates;
- scripts de validação, rastreabilidade, evidência e progresso;
- metadata de descoberta em `agents/openai.yaml`;
- BDD, testes e fixtures que validam as próprias skills.

Specs pertencem a cada projeto consumidor. A raiz do monorepo
[`promovaweb/specsfy`](https://github.com/promovaweb/specsfy) não instala nem executa este
catálogo. A identidade pertence a [`brand/`](../brand/).
Conhecimento técnico opcional pertence a
[`specialists/`](../specialists/) e é instalado
por [`cli/`](../cli/).

## Metodologia executável

O fluxo preservado pelas skills é:

```text
capturar imediatamente em specs/ideias
  → refinar no backlog
  → entrevistar
  → especificar
  → validar definição
  → planejar tarefas
  → usar o BDD da spec para provar TDD RED
  → implementar GREEN
  ↳ atualizar a spec e reabrir o fluxo quando surgir um pedido tardio
  → reconstruir a documentação técnica
  → validar entrega
  → consultar progresso
```

Cada fatia usa uma única fonte normativa em
`specs/specs/<NNNN>-<slug>/spec.md` e atravessa:

```text
Draft → Defined → Planned → Implementing → Complete
```

Nenhum `Definition Gate`, `Plan Gate` ou `Delivery Gate` passa sem evidência
compatível com o ato correspondente.

## Orquestração conversacional

As skills fazem handoff dentro da mesma conversa. Quando uma responsabilidade
termina ou encontra uma pendência de outra etapa, a skill atual:

1. anuncia `Pendência detectada` quando houver trabalho bloqueante;
2. apresenta `Transição automática`, com origem, destino, motivo e resultado;
3. carrega imediatamente a skill responsável sem pedir confirmação nem exigir
   que a pessoa repita o comando;
4. preserva o contexto e resolve a pendência na mesma conversa;
5. apresenta `Retomada automática` e retorna à etapa de origem quando a correção
   terminar.

O protocolo também vale para retornos. Pedido tardio entra por
`specsfy-base-update-spec`; mudança de comportamento reabre definição e
validação, mudança de plano retorna às tarefas e ausência de teste ou RED chama
TDD/BDD. O handoff é automático, mas não autoriza instalação, deploy,
publicação ou ação destrutiva, que continuam exigindo autorização específica.

## Catálogo

| Skill | Responsabilidade | Limite principal |
| --- | --- | --- |
| [`specsfy-base-idea`](specsfy-base-idea/SKILL.md) | preservar e pré-processar o input sem perguntas | não refina, promove ou implementa |
| [`specsfy-base-backlog`](specsfy-base-backlog/SKILL.md) | pesquisar, conversar e registrar ideias minimamente completas | não cria especificações |
| [`specsfy-base-interview`](specsfy-base-interview/SKILL.md) | descobrir intenção com MCR-10 | não escreve arquivos por padrão |
| [`specsfy-base-specify`](specsfy-base-specify/SKILL.md) | promover decisões para `spec.md` e research | não implementa nem captura ideia vaga |
| [`specsfy-base-validate`](specsfy-base-validate/SKILL.md) | auditar o Definition Gate | não decide requisitos |
| [`specsfy-base-tasks`](specsfy-base-tasks/SKILL.md) | manter tarefas nas seções 14–15 | não cria `tasks.md` nem código |
| [`specsfy-base-tdd-bdd`](specsfy-base-tdd-bdd/SKILL.md) | usar o BDD da spec para criar TDD e provar RED/GREEN | não executa Gherkin nem inventa comportamento |
| [`specsfy-base-implement`](specsfy-base-implement/SKILL.md) | executar tarefas prontas e evidenciar | não trabalha sem RED |
| [`specsfy-base-update-spec`](specsfy-base-update-spec/SKILL.md) | incorporar pedido tardio e reabrir somente os atos afetados | não cria nova spec nem implementa |
| [`specsfy-base-progress`](specsfy-base-progress/SKILL.md) | projetar o estado global | não altera gates ou checkboxes |
| [`specsfy-setup`](specsfy-setup/SKILL.md) | detectar o stack, criar contexto ausente e reconciliar blocos de agentes | não sobrescreve arquivos de contexto existentes |
| [`specsfy-documentator`](specsfy-documentator/SKILL.md) | reconstruir documentação completa do sistema existente em `docs/` | não inventa decisões, relações ou referências |
| [`specsfy-aux-stack`](specsfy-aux-stack/SKILL.md) | manter `.specsfy/STACK.md` a partir de evidência executável | não inventa nem copia toda dependência |
| [`specsfy-aux-rules`](specsfy-aux-rules/SKILL.md) | ajudar a registrar regras confirmadas em `.specsfy/RULES.md` | não decide regras pela pessoa |
| [`specsfy-aux-database`](specsfy-aux-database/SKILL.md) | manter `.specsfy/DATABASE.md` após toda mudança persistente | não copia dados ou segredos |

`PROJECT.md` fica na raiz do projeto consumidor. `STACK.md`, `RULES.md` e
`DATABASE.md` ficam em `.specsfy/`. O setup pode ser executado novamente para
garantir presença e consistência, preservando arquivos existentes e todo
conteúdo fora dos blocos gerenciados em `AGENTS.md` e `CLAUDE.md`.

Durante planejamento, implementação e projeção de progresso,
`specsfy-setup/scripts/monitor_context.py` classifica mudanças staged, unstaged
e untracked. Alterações estruturais exigem `STACK.md`; alterações de
persistência exigem `DATABASE.md`; código de aplicação exige revisão de
`PROJECT.md`. A ausência de impacto material é registrada na evidência da
tarefa, nunca presumida silenciosamente.

`specsfy-documentator` funciona de forma independente e também é um handoff
obrigatório após cada tarefa de implementação. Em toda execução, ele reavalia o
código existente e reconstrói arquitetura, aplicação, banco, fluxos, testes,
frontend, pacotes, integrações e decisões dentro dos blocos gerenciados de
`docs/`, preservando texto humano externo.

## Capacidades nativas

As skills incorporam capacidades inspiradas em extensões de specification
development sem instalar outro runtime ou criar fontes paralelas:

| Capacidade | Owner |
| --- | --- |
| Quality Gates | `specsfy-base-validate` |
| CI Guard | `specsfy-base-validate` |
| Verify Tasks | `specsfy-base-implement` |
| Spec Trace | `specsfy-base-tdd-bdd` |
| Spec Reference Loader | `specsfy-base-specify` |
| Research Harness | `specsfy-base-specify` |
| What-if | `specsfy-base-update-spec` |
| Spec Changelog | `specsfy-base-update-spec` |
| Spec Critique | `specsfy-base-validate` |
| Architecture Guard | `specsfy-base-validate` |
| Security Review | `specsfy-base-validate` |
| QA Testing | `specsfy-base-tdd-bdd` |
| Token Consumption Analyzer | `specsfy-base-progress` |
| PR Bridge | `specsfy-base-implement` |

## Especialistas sob demanda

Cada skill base possui `references/specialists.md` com critérios para recomendar
contexto técnico opcional:

```bash
specsfy skills add specsfy-specialist-<nome>
```

As bases podem propor um especialista já instalado e carregá-lo após
confirmação. Instalação recebe confirmação específica e nunca ocorre como
efeito implícito do handoff. O workspace `promovaweb/specsfy` não é projeto consumidor
e não recebe nenhuma categoria.

## Estrutura

```text
templates/
├── Idea.md, Backlog.md, Spec.md e Tasks.md
└── Project.md, Stack.md, Rules.md e Database.md
examples/
└── Spec.md        # fixture preenchida para agentes, CLI e testes
specsfy-{base-<responsabilidade>|setup|documentator|aux-<responsabilidade>}/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/       # quando há automação determinística
├── references/    # conhecimento consultado pela skill
└── assets/        # templates e materiais de saída
```

- `SKILL.md` possui frontmatter com `name` e `description`.
- `agents/openai.yaml` menciona `$<nome-da-skill>` no prompt padrão.
- Scripts usam Python 3 e biblioteca padrão, sem rede ou ação destrutiva por
  padrão.
- Referências extensas vivem a um nível da skill e possuem gatilho explícito de
  leitura.
- Uma regra normativa possui uma única fonte; outros arquivos apontam para ela.
- O CLI publica os templates e o exemplo sob `.specsfy/`; somente uma spec criada a
  partir do template se torna normativa para uma feature.

## Disponibilizar as skills

Instale o catálogo base com o CLI:

```bash
uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'
specsfy install
```

O monorepo oficial mantém este módulo como fonte do catálogo, sem instalar as
skills na própria raiz.

## Desenvolver

Leia [`AGENTS.md`](AGENTS.md) antes de alterar uma skill.

Uma mudança de comportamento segue:

```text
spec → Gherkin → teste TDD → RED → skill/script → GREEN → regressão → evidência
```

O ciclo técnico permanece `RED → GREEN → REFACTOR`.

Testes e fixtures das skills permanecem neste módulo e criam specs somente
em diretórios temporários.

Nos projetos consumidores, o runner dos testes derivados do BDD é selecionado
pela stack. Projetos PHP, inclusive Laravel com frontend Node, usam Pest. Em
projetos exclusivamente Node, o agente pergunta qual runner adotar antes de
criar ou executar testes e sugere Vitest como padrão. O Gherkin permanece
somente na `spec.md` como referência: agentes derivam testes executáveis dele,
sem criar ou executar `.feature`. A decisão Node é materializada no script
`test:tdd`. Cada feature, história e requisito recebe no mínimo três cenários
BDD distintos e três casos TDD executáveis; cada caso TDD possui seu próprio
marcador `SPECSFY:`.

## Validar

Valide cada skill alterada:

```bash
uv run --quiet --with pyyaml python \
  /home/luizeof/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  specsfy-base-<nome>
```

Execute os contratos das skills a partir desta raiz:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 -B specsfy-base-validate/scripts/verify_repo.py . \
  --boundary local
```

O verificador exige as dez skills base. Os contratos do catálogo também
validam o setup, o documentador e as três auxiliares; especialistas instalados
são validados sem limitar o tamanho total do catálogo.

## Publicação

Antes de publicar:

- frontmatter e metadata são válidos;
- gatilhos positivos e limites negativos estão claros;
- não existem placeholders, caches ou links locais quebrados;
- os testes TDD informados pelo BDD tiveram RED válido e estão verdes;
- requisitos, testes, tarefas e evidências estão rastreáveis;
- a regressão do workspace passou;
- o diff integrado mantém este módulo e seus consumidores coerentes.

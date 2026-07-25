# Specsfy

Specsfy é uma metodologia prática para escrever software a partir de uma
especificação única, executável e rastreável. O método organiza cada fatia
vertical em três atos rígidos:

1. definir com clareza o que precisa existir;
2. projetar e provar os testes antes da implementação;
3. entregar, verificar e concluir com evidência.

O objetivo não é produzir mais documentação. É reduzir a distância entre a
intenção do usuário, o comportamento aceito, os testes, as tarefas e o código.

> O `README.md` explica o método. A fonte normativa de cada trabalho continua
> sendo `specs/<slug>/spec.md`.

Esta é a apresentação pública do projeto; limites normativos e decisões
transversais permanecem na biblioteca de contexto.

O mapa para pessoas, arquitetura, tecnologias, dados, convenções e decisões
transversais está em [`docs/README.md`](docs/README.md). Agentes devem começar
pelo roteamento seletivo definido no `AGENTS.md`.

## Proposta

O Specsfy parte de seis compromissos:

1. **Fonte única:** cada fatia possui um único `spec.md` normativo.
2. **Descoberta antes da solução:** ambiguidades materiais são tratadas antes
   do planejamento.
3. **BDD como aceite:** comportamentos são expressos em Gherkin observável.
4. **TDD antes da implementação:** código novo exige RED BDD e RED TDD.
5. **Trabalho rastreável:** histórias, requisitos, cenários, testes e tarefas
   compartilham IDs.
6. **Conclusão por evidência:** nenhum estado ou checkbox avança apenas por
   intenção.

O método é adequado para trabalho humano, desenvolvimento assistido por IA e
equipes que desejam tornar decisões e handoffs verificáveis.

### O que o método tenta evitar

- especificações, planos e tarefas divergindo em arquivos diferentes;
- questionários longos que não acompanham a conversa;
- requisitos tecnicamente elegantes, mas ambíguos;
- BDD reduzido a frases informais não executáveis;
- testes escritos somente depois do código;
- tarefas concluídas sem verificação ou evidência;
- um “pronto” genérico que não informa o que foi realmente aprovado.

## Fonte da verdade

Cada fatia vertical vive em:

```text
specs/<slug>/
├── spec.md
└── research/       # opcional; somente evidências externas consultadas
```

O arquivo `specs/<slug>/spec.md` reúne:

- problema, resultado e métricas;
- research, fontes e dúvidas respondidas;
- escopo, atores, princípios e restrições;
- histórias de usuário;
- cenários BDD em Gherkin;
- requisitos funcionais e não funcionais;
- plano técnico;
- migrations, models, controllers, views, queries e jobs;
- modelo de dados, estados e retenção;
- APIs, eventos e contratos;
- estratégia TDD e matriz de rastreabilidade;
- gates e resultados de validação;
- tarefas, dependências e checklists;
- riscos, decisões e Definition of Done.

Não crie fontes normativas paralelas como `plan.md`, `tasks.md`,
`research.md` ou `data-model.md`.

O diretório `research/` não é uma segunda especificação. Ele preserva snapshots,
schemas, contratos, documentação e notas de proveniência realmente consultados.
Toda evidência deve ser indexada no `spec.md`; toda decisão continua no
`spec.md`.

O contrato estrutural está no
[template Specsfy/2.0](.agents/skills/specsfy-specify/assets/spec-template.md).

## Os três atos rígidos

Os atos não são categorias editoriais. Cada ato representa um compromisso,
possui entrada, atividades, saída, gate e handoff próprios.

### Ato I — Definir

**Pergunta central:** o que deve ser construído e como saberemos que está
correto?

**Entrada:** uma ideia, dor, solicitação, história ou especificação preliminar.

**Atividades:**

- descobrir problema, finalidade, atores e resultado;
- esclarecer termos ambíguos, equivalentes e derivados;
- separar declarações, inferências, hipóteses, decisões e conflitos;
- definir escopo e fora de escopo;
- identificar regras, limites, falhas e efeitos;
- escrever histórias e requisitos verificáveis;
- escrever o aceite em Gherkin;
- confirmar que não resta dúvida P1.

**BDD neste ato:** o cenário em `spec.md` funciona como linguagem de descoberta.
Ele define o comportamento aceito antes de existir como arquivo executável.

**Saída:** intenção operacional recomposta em afirmações verificáveis.

**Gate:** `Definition Gate`.

**Estado após aprovação:** `Defined`.

**Handoff:** o Ato II recebe uma definição estável, IDs rastreáveis e Gherkin
aceito.

### Ato II — Projetar e provar

**Pergunta central:** como entregar o comportamento e como provar, antes do
código, que os testes detectam sua ausência?

**Entrada:** `Status: Defined` e `Definition Gate: Passed`.

**Atividades:**

- inspecionar arquitetura e convenções reais do repositório;
- definir dados, migrations, models, controllers, views e queries;
- documentar APIs, contratos, timeouts, retries, rollback e riscos;
- decompor o trabalho em fatias verticais;
- criar tarefas com caminhos, referências e dependências;
- criar tarefas BDD e TDD anteriores a cada tarefa de código;
- materializar o `.feature` e seus steps;
- escrever o menor teste TDD de unidade ou integração;
- observar RED válido nos dois níveis;
- registrar comandos, causas e rastreabilidade.

O handoff interno do Ato II é deliberadamente bifásico:

```text
planejar tarefas → preparar BDD/TDD e observar RED → validar o plano
```

O `Plan Gate` não passa apenas porque as tarefas de teste foram mencionadas.
Os predecessores BDD e TDD de cada tarefa de código precisam estar concluídos
com RED registrado.

**Saída:** plano executável, backlog rastreável e testes sensíveis ao
comportamento ausente.

**Gate:** `Plan Gate`.

**Estado após aprovação:** `Planned`.

**Handoff:** o Ato III recebe tarefas prontas e provas de que os testes protegem
o comportamento.

### Ato III — Entregar e validar

**Pergunta central:** a implementação satisfaz o comportamento e todas as
evidências continuam coerentes?

**Entrada:** `Status: Planned`, `Definition Gate: Passed` e
`Plan Gate: Passed`.

**Atividades:**

- selecionar a próxima tarefa com dependências satisfeitas;
- confirmar os REDs BDD e TDD da mesma fatia;
- escrever a menor implementação que produz GREEN;
- executar teste focal e cenário Gherkin;
- refatorar sem alterar o comportamento;
- executar regressão, lint, tipos e build disponíveis;
- auditar rastreabilidade;
- atualizar evidências e checklists conforme o trabalho acontece;
- revisar Definition of Done;
- consultar o progresso global.

O ciclo técnico é:

```text
RED → GREEN → REFACTOR
```

O ciclo operacional de cada tarefa é:

```text
PREP → EXECUTE → VERIFY → EVIDENCE → IMPROVE
```

**Saída:** comportamento entregue, testes verdes, evidências atuais e nenhuma
tarefa aberta.

**Gate:** `Delivery Gate`.

**Estado final:** `Complete`.

## Máquina de estados e gates

O fluxo canônico é:

```text
Draft → Defined → Planned → Implementing → Complete
```

| Estado | Definition Gate | Plan Gate | Delivery Gate | Significado |
|---|---|---|---|---|
| `Draft` | `Pending` ou `Failed` | `Pending` | `Pending` | definição ainda aberta |
| `Defined` | `Passed` | `Pending` ou `Failed` | `Pending` | Ato I aprovado |
| `Planned` | `Passed` | `Passed` | `Pending` | Ato II aprovado |
| `Implementing` | `Passed` | `Passed` | `In Progress` ou `Failed` | entrega em execução |
| `Complete` | `Passed` | `Passed` | `Passed` | três atos concluídos |

Os validadores rejeitam combinações impossíveis. Um estado posterior nunca
compensa um gate anterior inválido.

### Invalidação

- Mudança em comportamento, aceite, escopo, dados ou segurança reabre o Ato I e
  invalida plano e entrega.
- Mudança somente no plano, tarefas ou estratégia de testes reabre o Ato II e
  invalida a entrega.
- Mudança interna reversível que não altera comportamento pode permanecer no
  Ato III, com evidência.

Regra geral:

> quando a entrada de um ato muda, seus resultados e todos os atos posteriores
> deixam de ser confiáveis até nova validação.

## BDD e TDD

BDD e TDD cumprem papéis diferentes e complementares.

### BDD

BDD define valor e comportamento observável. Cada critério `AC-NNN` contém
Gherkin real:

```gherkin
@US-001 @FR-001 @AC-001
Feature: Capacidade observável

  Scenario: Resultado aceito
    Given um estado inicial conhecido
    When o ator executa uma ação
    Then o resultado observável acontece
```

No Ato I, o cenário ajuda a descobrir e confirmar a intenção. No Ato II, ele é
materializado em `tests/features/*.feature`. No Ato III, funciona como aceite
executável.

### TDD

TDD dirige a implementação no nível mais baixo que ainda prova a regra.

1. Escreva o teste.
2. Execute e observe uma falha pelo comportamento ausente.
3. Implemente o mínimo necessário.
4. Observe GREEN.
5. Refatore.
6. Execute a regressão.

Falha de sintaxe, importação, fixture ou ambiente não conta como RED válido. O
teste deve falhar pela ausência ou incorreção do comportamento especificado.

### Regra de precedência

Toda tarefa `[CODE]` precisa depender de:

- uma tarefa `[TEST]` BDD que aponta para `.feature`;
- uma tarefa `[TEST]` TDD de unidade ou integração;
- RED registrado para os mesmos IDs.

Sem ambos, produção não deve ser alterada.

## MCR-10

O Método Categorial de Requisitos é a técnica de descoberta do Specsfy. Ele usa
as dez categorias de Aristóteles como lentes adaptadas ao desenvolvimento
moderno:

| Categoria | Lente de software |
|---|---|
| Substância | ator, entidade, identidade e serviço externo |
| Quantidade | cardinalidade, volume, quota e precisão |
| Qualidade | atributo, invariável, validação e NFR mensurável |
| Relação | associação, dependência, propriedade e autorização |
| Lugar | canal, módulo, ambiente, região e fronteira de confiança |
| Tempo | ordem, duração, expiração, retenção e concorrência |
| Posição | estado, etapa, ordenação e configuração |
| Posse | papel, permissão, credencial, plano e capability |
| Ação | comando, evento, gatilho, idempotência e reversão |
| Afecção | resultado, mudança de estado, erro e efeito colateral |

Antes das categorias, o método identifica a finalidade: problema observável,
quem o percebe e qual mudança seria útil.

As categorias não são um questionário. A análise ocorre silenciosamente e a
conversa apresenta uma pergunta por vez: a lacuna P1 de maior
`impacto × incerteza`.

O método:

1. decompõe o relato;
2. identifica vocabulário e lacunas;
3. classifica a origem de cada afirmação;
4. prioriza perguntas;
5. recompõe o conteúdo em sujeito, condição, ação e efeito observável;
6. deriva regras, histórias, falhas e Gherkin.

Leia a referência completa em
[MCR-10 — Método Categorial de Requisitos](.agents/skills/specsfy-specify/references/mcr-10.md).

## Tarefas e evidências

As tarefas permanecem na seção 14 do `spec.md`:

```markdown
- [ ] T003 [CODE] [US-001] Implementar regra em src/recurso.py — Refs: FR-001, AC-001 — Depends: T001, T002
  - [ ] **PREP**: Confirmar escopo, IDs, dependências e baseline.
  - [ ] **EXECUTE**: Produzir a entrega no caminho declarado.
  - [ ] **VERIFY**: Executar a verificação focal.
  - [ ] **EVIDENCE**: Registrar comando, resultado e IDs.
  - [ ] **IMPROVE**: Aplicar melhoria ou justificar sua ausência.
```

Cada tarefa possui:

- um ID estável;
- um tipo: `TEST`, `CODE`, `DOC` ou `OPS`;
- uma história opcional;
- um resultado único;
- um caminho concreto;
- referências para a especificação;
- dependências explícitas;
- exatamente cinco itens de checklist.

O pai só pode ser marcado depois dos cinco itens. Um item não pode avançar
enquanto uma dependência estiver aberta.

### Rastreabilidade

Os mesmos IDs atravessam:

```text
US → FR/NFR → AC → teste BDD/TDD → tarefa → evidência
```

Essa cadeia permite responder:

- por que este código existe;
- qual comportamento ele implementa;
- qual teste o protege;
- qual tarefa o produziu;
- qual evidência permite concluir.

## Catálogo atual de skills

O repositório implementa atualmente sete skills:

| Skill atual | Responsabilidade | Ato principal |
|---|---|---|
| `specsfy-discuss` | descoberta conversacional com MCR-10 | Ato I |
| `specsfy-specify` | criação e atualização do `spec.md` | Ato I |
| `specsfy-validate` | validação estrutural e semântica da definição | Ato I |
| `specsfy-tasks` | planejamento e validação das tarefas | Ato II |
| `specsfy-tdd-bdd` | preparação RED e ciclos de teste | Atos II e III |
| `specsfy-implement` | execução da próxima tarefa pronta | Ato III |
| `specsfy-progress` | projeção somente leitura do estado global | transversal |

Fontes:

- [specsfy-discuss](.agents/skills/specsfy-discuss/SKILL.md)
- [specsfy-specify](.agents/skills/specsfy-specify/SKILL.md)
- [specsfy-validate](.agents/skills/specsfy-validate/SKILL.md)
- [specsfy-tasks](.agents/skills/specsfy-tasks/SKILL.md)
- [specsfy-tdd-bdd](.agents/skills/specsfy-tdd-bdd/SKILL.md)
- [specsfy-implement](.agents/skills/specsfy-implement/SKILL.md)
- [specsfy-progress](.agents/skills/specsfy-progress/SKILL.md)

## Nomenclatura recomendada

> **Proposta ainda não implementada.** Os diretórios, frontmatters, testes e
> comandos continuam usando o catálogo atual da seção anterior.

Os nomes atuais indicam a função, mas nem sempre tornam visíveis o ato, a etapa
e a ordem. `specsfy-tdd-bdd` também atravessa dois atos, enquanto progresso é
transversal.

O formato recomendado é:

```text
specsfy-a<ato>-s<etapa>-<responsabilidade>
```

| Escopo | Etapa | Nome recomendado | Responsabilidade |
|---|---:|---|---|
| Ato I | 1 | `specsfy-a1-s1-discover` | descobrir intenção e ambiguidades |
| Ato I | 2 | `specsfy-a1-s2-specify` | escrever a fonte normativa |
| Ato I | 3 | `specsfy-a1-s3-validate-definition` | aprovar o Definition Gate |
| Ato II | 1 | `specsfy-a2-s1-plan` | projetar e decompor tarefas |
| Ato II | 2 | `specsfy-a2-s2-prove-plan` | materializar BDD/TDD RED e aprovar o Plan Gate |
| Ato III | 1 | `specsfy-a3-s1-implement` | produzir GREEN e refatorar |
| Ato III | 2 | `specsfy-a3-s2-validate-delivery` | regressão, rastreabilidade e Delivery Gate |
| Transversal | 1 | `specsfy-x-s1-progress` | informar progresso sem alterar estado |

### Por que oito skills

A divisão recomendada corrige duas sobreposições:

1. `specsfy-tdd-bdd` deixaria de misturar preparação RED do Ato II com
   verificação GREEN do Ato III.
2. validação de definição e validação de entrega teriam nomes distintos,
   vinculados aos respectivos gates.

O prefixo numérico oferece:

- ordem lexicográfica;
- ato e etapa visíveis no comando;
- handoffs previsíveis;
- menor ambiguidade para pessoas e agentes;
- espaço explícito para capacidades transversais com `x`.

Uma eventual migração deve atualizar atomicamente:

- diretórios e frontmatters;
- `agents/openai.yaml`;
- referências entre skills;
- `AGENTS.md`, template e spec;
- testes e Gherkin;
- scripts, mensagens e comandos;
- documentação pública.

Não é recomendado manter aliases como skills duplicadas, pois isso faria o
catálogo expor estados concorrentes. É melhor fornecer um mapa de migração
temporário na documentação e trocar o contrato de uma vez.

## Fluxo completo

```text
ideia
  ↓
descoberta MCR-10
  ↓
spec + Gherkin
  ↓
Definition Gate
  ↓
plano + tarefas
  ↓
BDD/TDD RED
  ↓
Plan Gate
  ↓
implementação GREEN
  ↓
refactor + regressão + rastreabilidade
  ↓
Delivery Gate
  ↓
Complete
```

### Handoffs atuais

```text
$specsfy-discuss
  → $specsfy-specify
  → $specsfy-validate
  → $specsfy-tasks
  → $specsfy-tdd-bdd prepare
  → $specsfy-tasks
  → $specsfy-implement
  → $specsfy-tdd-bdd verify
  → $specsfy-progress
```

O retorno para `specsfy-tasks` após `prepare` é intencional: ele confirma que
os predecessores BDD/TDD foram realmente concluídos antes de aprovar o plano.

## Estrutura do repositório

```text
.
├── AGENTS.md
├── README.md
├── .agents/
│   └── skills/
│       ├── specsfy-discuss/
│       ├── specsfy-specify/
│       ├── specsfy-validate/
│       ├── specsfy-tasks/
│       ├── specsfy-tdd-bdd/
│       ├── specsfy-implement/
│       └── specsfy-progress/
├── specs/
│   └── <slug>/
│       ├── spec.md
│       └── research/
└── tests/
    ├── features/
    └── test_specsfy.py
```

Responsabilidades:

- `README.md`: visão pública e orientação de uso;
- `AGENTS.md`: regras para desenvolver as skills deste repositório;
- `.agents/skills/`: mecanismos reutilizáveis;
- `specs/<slug>/spec.md`: fonte normativa da fatia;
- `specs/<slug>/research/`: evidência externa não normativa;
- `tests/`: BDD e contratos derivados.

## Anatomia do spec.md

O formato `Specsfy/2.0` possui exatamente três atos e 18 seções, nesta ordem:

| Ato | Seção | Conteúdo |
|---|---:|---|
| I | 1 | problema, resultado desejado e métricas |
| I | 2 | research, fontes, documentação e dúvidas |
| I | 3 | escopo, fora de escopo e atores |
| I | 4 | princípios e restrições |
| I | 5 | histórias de usuário priorizadas |
| I | 6 | critérios de aceite em Gherkin |
| I | 7 | requisitos funcionais, não funcionais e erros |
| II | 8 | plano técnico e estrutura de arquivos |
| II | 9 | entidades, estados, migração e retenção |
| II | 10 | APIs, documentação, eventos e contratos |
| II | 11 | estratégia TDD e evidência RED-GREEN-REFACTOR |
| II | 12 | matriz de testes e rastreabilidade |
| II | 13 | resultados dos três gates |
| II | 14 | tarefas e checklists operacionais |
| II | 15 | ordem de execução e caminho crítico |
| III | 16 | dependências, riscos e suposições |
| III | 17 | decisões e possibilidades futuras |
| III | 18 | Definition of Done |

O Ato III atualiza evidências e checklists localizados nas seções 11–14 sem
mover essas seções. A posição registra o plano; o estado dos itens registra a
execução.

### IDs normativos

| Prefixo | Registro | Exemplo |
|---|---|---|
| `US` | história de usuário | `US-001` |
| `AC` | critério de aceite | `AC-001` |
| `FR` | requisito funcional | `FR-001` |
| `NFR` | requisito não funcional | `NFR-001` |
| `DEC` | decisão | `DEC-001` |
| `T` | tarefa | `T001` |

IDs não são renumerados nem reutilizados. Alterações preservam o histórico e
invalidam somente os resultados dependentes.

## Componentes internos

### Estrutura de uma skill

```text
.agents/skills/<nome>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/       # opcional
├── references/    # opcional
└── assets/        # opcional
```

- `SKILL.md` contém gatilhos, responsabilidade, processo, limites e handoffs.
- `agents/openai.yaml` contém nome de exibição, descrição curta e prompt padrão
  para a interface do host; não contém regras normativas.
- `scripts/` reúne automações determinísticas em Python.
- `references/` contém conhecimento que a skill consulta.
- `assets/` contém templates usados para produzir ou atualizar artefatos.

### Arquivos por skill

| Skill | Arquivos auxiliares | Função |
|---|---|---|
| `specsfy-discuss` | `references/discovery-map.md` | seleciona áreas de descoberta sem criar questionário |
| `specsfy-specify` | template, MCR-10, loader de research e análise de mudança | define a fonte, verifica claims e projeta impacto/changelog |
| `specsfy-validate` | validadores, runner agregado e lentes de review | valida estrutura, semântica, findings e paridade local/Git/CI |
| `specsfy-tasks` | `scripts/validate_tasks.py`, `assets/tasks-section.md` | define e valida tarefas, cobertura e dependências |
| `specsfy-tdd-bdd` | rastreabilidade, níveis de teste e auditor QA | verifica cadeia completa, Gherkin, cobertura e resultado por AC |
| `specsfy-implement` | seletor, evidence verifier e delivery renderer | seleciona trabalho, prova entrega material e resume PR |
| `specsfy-progress` | progresso e análise de contexto | agrega estado e mede contexto sem modificar arquivos |

### Scripts

#### `validate_spec.py`

Valida:

- caminho `specs/<slug>/spec.md`;
- formato `Specsfy/2.0`;
- três atos, 18 seções e subseções obrigatórias;
- metadata, estados e gates;
- IDs, referências e Gherkin;
- ausência de placeholders em estados aprovados;
- pacote restrito a `spec.md` e `research/`;
- indexação e portabilidade do research;
- tarefas e DoD fechadas quando `Status: Complete`.

Opções:

- `--allow-draft`: valida um estado intermediário sem exigir Definition Gate;
- `--json`: produz resultado estruturado.

#### `validate_tasks.py`

Valida:

- formato da seção 14;
- checklist canônico;
- referências, caminhos e tags;
- dependências inexistentes ou cíclicas;
- cobertura de `US`, `FR`, `NFR` e `AC`;
- tarefa BDD e tarefa TDD por aceite;
- precedência BDD/TDD para código;
- REDs concluídos antes de `Plan Gate: Passed`;
- coerência entre pai, itens e dependências.

Opções:

- `--allow-draft`: valida o plano enquanto o Plan Gate está aberto;
- `--json`: produz contagens e achados estruturados.

#### `check_traceability.py`

Procura tags Gherkin e marcadores `SPECSFY:` nos arquivos de teste. Ele informa:

- IDs obrigatórios;
- IDs cobertos;
- critérios `AC` sem arquivo `.feature`;
- marcadores órfãos;
- arquivos que fornecem cada evidência.

`--kinds FR,AC,NFR` define os tipos obrigatórios e `--json` produz a matriz em
formato estruturado. `--full-chain` exige requisito, teste, tarefa e evidence.

#### `next_task.py`

Lê somente a seção 14 e:

- rejeita gates ou status incompatíveis;
- confirma dependências;
- diferencia trabalho pronto, bloqueado e concluído;
- mostra a próxima tarefa;
- mostra o próximo item de checklist;
- oferece `--all` e `--json`.

#### `progress.py`

Descobre somente `specs/*/spec.md` e calcula:

- specs concluídas;
- gates aprovados;
- tarefas e itens concluídos;
- percentuais e denominadores;
- ato atual;
- blockers;
- próxima tarefa e próximo item;
- próxima skill sugerida.

Aceita `--slug <slug>` e `--json`. A consulta nunca atualiza a fonte.

### Capacidades adaptadas do ecossistema Spec Kit

As 14 sugestões de prioridade alta e média foram adaptadas às sete skills, sem
instalar Spec Kit ou criar `.specify/`:

- Quality Gates + CI Guard → `verify_repo.py` e workflow GitHub;
- Verify Tasks + Spec Trace → `verify_evidence.py` e `--full-chain`;
- Spec Reference Loader + Research Harness → `load_research.py`;
- What-if + Spec Changelog → `analyze_change.py`;
- Spec Critique + Architecture Guard + Security Review → findings `PROD/ARCH/SEC`;
- QA Testing → `verify_acceptance.py`;
- Token Consumption Analyzer → `analyze_context.py`;
- PR Bridge → `render_delivery.py`.

Todas as projeções escrevem em stdout/JSON por padrão. Atestação exige caminho
explícito; findings e evidence normativos permanecem dentro da spec.

O endurecimento de robustez adiciona:

- atestação schema 2 com commit, checks observados e hashes por tarefa;
- digest da política calculado de comandos, limites e validadores;
- timeout e limite de saída configuráveis por check;
- QA opcionalmente conferida contra `acceptance:<slug>` na atestação;
- integridade de IDs, refs, evidence, budgets e âncoras;
- impacto classificado por títulos semânticos, com fallback conservador;
- Python, pacotes e Actions fixados no workflow.

```bash
python3 -B .agents/skills/specsfy-validate/scripts/verify_repo.py . --boundary local \
  --timeout-seconds 300 --max-output-bytes 65536 --attestation /tmp/specsfy.json
python3 -B .agents/skills/specsfy-specify/scripts/load_research.py specs/<slug>/spec.md
python3 -B .agents/skills/specsfy-specify/scripts/analyze_change.py specs/<slug>/spec.md --mode impact
python3 -B .agents/skills/specsfy-implement/scripts/verify_evidence.py specs/<slug>/spec.md .
python3 -B .agents/skills/specsfy-tdd-bdd/scripts/verify_acceptance.py specs/<slug>/spec.md .
python3 -B .agents/skills/specsfy-progress/scripts/analyze_context.py specs/<slug>/spec.md
python3 -B .agents/skills/specsfy-implement/scripts/render_delivery.py specs/<slug>/spec.md --preview
```

Depois de gerar a atestação, acrescente `--attestation /tmp/specsfy.json` aos
comandos de evidence e acceptance. O modo legado continua disponível para
specs existentes, mas não oferece o vínculo criptográfico com os arquivos
observados pelo runner.

### Códigos de retorno

| Comando | `0` | `1` | `2` |
|---|---|---|---|
| validadores de spec/tarefas | entrada válida | achados que invalidam | erro de argumentos pelo Python |
| rastreabilidade | sem gaps | gaps ou órfãos | spec, raiz ou tipos inválidos |
| próxima tarefa | pronta ou completa | tarefas bloqueadas | contrato ou arquivo inválido |
| progresso | relatório produzido | não utilizado | nenhuma spec ou slug encontrado |
| extensões adaptadas | resultado válido | gap ou blocker | uso, arquivo ou ambiente inválido |

Para automação, prefira `--json` e use o código de retorno como decisão
primária.

## Requisitos de ambiente

Para utilizar os scripts:

- Python 3;
- host compatível com skills em `.agents/skills`;
- repositório com permissão para criar `specs/<slug>/`.

Os scripts das skills usam somente a biblioteca padrão do Python.

Para executar a suite do próprio projeto:

- `uv`, usado para ambientes efêmeros;
- `behave`, carregado pelo comando BDD;
- `pyyaml`, carregado para validar metadata das skills.

O fluxo não exige instalação global, acesso de rede em runtime nem banco de
dados próprio.

## Testes do projeto

O próprio Specsfy é desenvolvido pelo método que propõe:

- [cenários de aceite](tests/features/specsfy.feature);
- [steps BDD](tests/features/steps/specsfy_steps.py);
- [testes de contrato](tests/test_specsfy.py).

Os testes protegem:

- catálogo e metadata das skills;
- fonte única e research;
- estrutura rígida;
- estados e gates;
- Gherkin e rastreabilidade;
- precedência BDD/TDD;
- checklists e dependências;
- relatório de progresso;
- publicação do MCR-10;
- documentação pública.

Uma nova capacidade do projeto deve seguir:

```text
spec → cenário BDD → teste TDD → RED → mudança → GREEN → regressão
```

## Desenvolvimento das skills

O arquivo [AGENTS.md](AGENTS.md) governa contribuições neste repositório.

Para criar ou alterar uma skill:

1. atualize `specs/<slug>/spec.md`;
2. adicione história, requisito e Gherkin;
3. crie tarefas BDD e TDD;
4. observe RED;
5. faça a menor alteração;
6. execute GREEN e regressão;
7. atualize os cinco itens da tarefa conforme a evidência;
8. valide a skill e consulte o progresso.

Uma skill publicável precisa:

- frontmatter com `name` e `description`;
- `agents/openai.yaml` válido;
- gatilhos positivos e limites negativos claros;
- menos de 500 linhas em `SKILL.md`;
- referências sem duplicação normativa;
- scripts seguros e determinísticos;
- BDD, TDD, rastreabilidade e regressão verdes;
- nenhuma tarefa ou checklist aberto.

## Como usar

### 1. Começar por uma ideia

Use `$specsfy-discuss` quando a intenção ainda precisa ser descoberta. A
conversa aplica o MCR-10, uma pergunta por vez, e termina com um brief pronto
para especificar.

### 2. Criar a especificação

Use `$specsfy-specify` para criar:

```text
specs/<slug>/spec.md
```

O arquivo nasce em `Draft`.

### 3. Validar a definição

```bash
python3 -B .agents/skills/specsfy-validate/scripts/validate_spec.py specs/<slug>/spec.md
```

Uma definição válida atravessa o `Definition Gate` e assume `Defined`.

### 4. Planejar

Use `$specsfy-tasks` para criar tarefas BDD, TDD, código, documentação e
fechamento na seção 14.

Validação intermediária:

```bash
python3 -B .agents/skills/specsfy-tasks/scripts/validate_tasks.py specs/<slug>/spec.md --allow-draft
```

### 5. Provar RED

Use `$specsfy-tdd-bdd` no modo `prepare`. Materialize o `.feature`, seus steps
e o teste TDD. Execute os dois e registre as falhas válidas.

Depois valide o plano:

```bash
python3 -B .agents/skills/specsfy-tasks/scripts/validate_tasks.py specs/<slug>/spec.md
```

### 6. Implementar

Use `$specsfy-implement`. A skill seleciona a próxima tarefa pronta:

```bash
python3 -B .agents/skills/specsfy-implement/scripts/next_task.py specs/<slug>/spec.md
```

### 7. Verificar rastreabilidade

```bash
python3 -B .agents/skills/specsfy-tdd-bdd/scripts/check_traceability.py specs/<slug>/spec.md . --kinds FR,AC,NFR
```

### 8. Consultar progresso

```bash
python3 -B .agents/skills/specsfy-progress/scripts/progress.py .
```

A consulta é somente leitura e deriva seu resultado de `specs/*/spec.md`.

## Validação

Comandos principais:

```bash
python3 -B .agents/skills/specsfy-validate/scripts/validate_spec.py specs/<slug>/spec.md
python3 -B .agents/skills/specsfy-tasks/scripts/validate_tasks.py specs/<slug>/spec.md
python3 -B .agents/skills/specsfy-tdd-bdd/scripts/check_traceability.py specs/<slug>/spec.md . --kinds FR,AC,NFR
python3 -B .agents/skills/specsfy-validate/scripts/verify_repo.py . --boundary local
python3 -B -m unittest discover -s tests -p 'test_*.py'
uv run --quiet --with behave behave tests/features --no-capture
python3 -B .agents/skills/specsfy-progress/scripts/progress.py .
```

Cada skill também deve passar pelo validador oficial:

```bash
uv run --quiet --with pyyaml python \
  /home/luizeof/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  .agents/skills/<nome>
```

## Limites e antipadrões

### O que o Specsfy não é

- um gerenciador de projetos externo;
- um substituto para pesquisa com usuários;
- uma garantia automática de valor comercial;
- uma arquitetura obrigatória;
- um motivo para documentar detalhes irrelevantes;
- uma licença para o agente decidir questões materiais pelo usuário.

### Antipadrões

- **Fonte duplicada:** manter `tasks.md` e a seção 14 simultaneamente.
- **Gherkin decorativo:** escrever Given/When/Then que não pode ser executado.
- **RED falso:** contar erro de ambiente como prova de comportamento ausente.
- **Gate nominal:** trocar metadata para `Passed` sem satisfazer as invariantes.
- **Checkbox em lote:** marcar etapas no encerramento sem acompanhar evidência.
- **Categoria como formulário:** perguntar mecanicamente pelas dez categorias.
- **Intenção presumida:** apresentar inferência do agente como fala do usuário.
- **Research normativo:** esconder decisões em snapshots externos.
- **Solução prematura:** transformar preferência técnica em requisito de produto.
- **Nomes enganosos:** atribuir uma skill transversal a um único ato.

### Rigor proporcional

O método admite profundidade proporcional ao risco:

- `Lite`: mudança pequena, reversível e de baixo impacto;
- `Standard`: feature comum;
- `Crítico`: dinheiro, autorização, privacidade, irreversibilidade ou migração.

O perfil reduz documentação irrelevante. Ele não permite pular dúvida P1, BDD,
TDD ou evidência.

## Evolução recomendada

As melhorias mais valiosas para as próximas versões são:

1. migrar o catálogo para nomes que expressem ato e etapa;
2. representar a máquina de estados em um contrato estruturado único;
3. gerar documentação e validadores a partir desse contrato;
4. oferecer um migrador assistido `Specsfy/1.0 → Specsfy/2.0`;
5. avaliar gates por fatia em especificações muito grandes;
6. medir empiricamente o MCR-10 com relatos anonimizados;
7. acompanhar redução de ambiguidades, turnos de descoberta e retrabalho.

Qualquer evolução deve preservar:

- uma fonte normativa;
- três atos;
- BDD e TDD antes da implementação;
- gates verificáveis;
- invalidação explícita;
- rastreabilidade;
- progresso derivado, nunca paralelo.

## Referências internas

- [Guia de desenvolvimento das skills](AGENTS.md)
- [Especificação normativa do próprio Specsfy](specs/specsfy/spec.md)
- [Template rígido Specsfy/2.0](.agents/skills/specsfy-specify/assets/spec-template.md)
- [MCR-10](.agents/skills/specsfy-specify/references/mcr-10.md)
- [Gates de qualidade](.agents/skills/specsfy-validate/references/quality-gates.md)
- [Gates de conclusão](.agents/skills/specsfy-implement/references/completion-gates.md)

## Créditos

Specsfy é um projeto da [Promovaweb](https://promovaweb.com), mantido por
**Luiz Eduardo Oliveira Fonseca** e pela comunidade.

Contato: [promovaweb.com](https://promovaweb.com) ou
[contato@promovaweb.com](mailto:contato@promovaweb.com).

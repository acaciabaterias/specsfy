# Voz — guia aprofundado

`../description.md` é normativo para posicionamento, tagline e elevator
pitches — não duplique isso aqui. Este arquivo é o complemento operacional:
o glossário de termos que não podem variar entre documentos, e exemplos
reais de como a voz soa em canais diferentes. Se um exemplo aqui contradisser
`../description.md`, `description.md` vence — abra uma correção nos dois.

## Por que um glossário existe

O método inteiro depende de IDs e nomes de estado que não podem ter
sinônimo — `US-01` não pode virar "a primeira história" em um documento e
continuar `US-01` em outro, ou a rastreabilidade que é a proposta central do
Specsfy quebra silenciosamente. A voz da marca aplica a mesma disciplina à
prosa: um termo, uma grafia, sempre.

## Glossário de termos canônicos

| Termo | Grafia fixa | Nunca escreva | Nota |
|---|---|---|---|
| Gate | `Gate` (maiúsculo, en) | "portão", "checkpoint", "milestone" | Sempre com o nome completo: `Definition Gate`, `Plan Gate`, `Delivery Gate`. |
| Ato | Ato I / Ato II / Ato III | "fase", "etapa", "sprint", "estágio" | Numeração romana, sempre. |
| spec.md | `spec.md` (mono) | "a especificação" isolado quando se refere ao arquivo | "a especificação" é aceitável quando fala do conceito, não do arquivo. |
| RED / GREEN | `RED` / `GREEN` (mono, maiúsculo) | "vermelho"/"verde" quando se refere ao estado do teste | "vermelho"/"verde" só valem falando de cor, nunca do estado TDD. |
| Estado canônico | `Draft → Defined → Planned → Implementing → Complete` | reordenar, renomear ou abreviar os estados | É uma sequência fixa, não uma lista de exemplos. |
| Ciclo de tarefa | `READY → RED → GREEN → VERIFIED → DONE` | pular etapas na descrição ("de READY direto pra DONE") | Mesmo em prosa corrida, cite a cadeia completa na primeira menção. |
| Handoff | `handoff` | "entrega" (confunde com Ato III — Entregar) | Handoff = transição verificável entre atos; entrega = o ato inteiro. |
| Evidência | `evidência` | "prova" como substantivo solto | "provar"/"prova" como verbo/ação é ok ("provar o teste"); "evidência" é o registro. |
| IDs (`US-01`, `RQ-04`, `CN-02`) | mono, formato `PREFIXO-NN` | escrever por extenso ("história de usuário um") | Sempre cite o ID mesmo quando parafrasear o conteúdo. |

## Exemplos por canal

**Commit message:**
```
fix: corrige contraste do vermelho semântico (RED) para AA

DC2626 dava 4.47:1 sobre Praxeti White, abaixo do mínimo de texto.
Troca para B91C1C (6.0:1). Ver brand/accessibility.md.
```
Direto, técnico, sem "melhorias" vagas — diz o número, diz a causa.

**Mensagem de validação/erro (ex.: `validate_spec.py`):**
```
Definition Gate: Failed
US-03 não tem cenário BDD associado — adicione um Scenario em spec.md
antes de marcar este Gate como Passed.
```
Diz o que falhou, onde, e a ação exata para resolver. Nunca "algo deu
errado" ou "verifique sua configuração".

**Título de seção de documentação:**
> ✅ "Ato II — Projetar e provar"
> ❌ "Fase de Planejamento 🚀"

Sem emoji como marcador de seção, sem hype no título de algo que já é
estrutural.

**Resposta de um agente conversando com o usuário (ex.: `specsfy-base-interview`):**
> "US-04 depende de um comportamento que ainda não está confirmado: o que
> acontece se o usuário cancelar no meio da importação? Isso muda o
> cenário BDD que vou escrever a seguir."

Uma pergunta por vez, nomeando o ID afetado, explicando a consequência —
não "me conte mais sobre seus requisitos" genérico.

**Post/anúncio (uso raro, mas se existir):**
> "Specsfy: uma especificação, rastreável até o código. Sem plan.md
> paralelo, sem 'pronto' sem evidência."

Ainda factual — vende pelo mecanismo, não pelo adjetivo.

## Nunca dizer (além do que já está em `../description.md`)

- **"Simplesmente"** antes de qualquer instrução — minimiza esforço real do
  leitor e geralmente esconde um passo faltando.
- **Emoji como marcador de seção ou de status** (✅/🚀/🔥 no lugar de
  `Gate: Passed`) — o método já tem um vocabulário de estado; emoji o
  duplica informalmente.
- **"Nosso/nossa IA"** referindo-se genericamente ao agente — nomeie a
  skill (`specsfy-base-interview`, `specsfy-base-validate`) quando o contexto permite;
  é mais preciso e mais rastreável, coerente com o resto da marca.
- **Desculpas performáticas em mensagem de erro** ("Ops! Algo deu errado 😅")
  — diga o que falhou e como corrigir, sem tom.
- **Voz passiva para esconder responsabilidade** ("o Gate não foi
  aprovado" sem dizer por quê) — sempre nomeie a causa verificável.

## Idioma

Português é o idioma primário de prosa (specs, guidelines, conversas). Os
identificadores literais do sistema — nomes de estado, arquivos, siglas,
nomes de Gate — permanecem em inglês e mono porque são *tokens*, não texto:
traduzi-los quebraria a busca por texto e a rastreabilidade entre
documentos. A regra de bolso: se aparece em um `grep` do repositório para
rastrear algo, não traduza; se é explicação ao redor, português.
